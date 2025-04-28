import rclpy
from rclpy.node import Node
import os
import yaml
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped, Point
from std_msgs.msg import String
import math
from collections import deque
from simple_av_msgs.msg import PlanningPathPlanningMsg, PlanningInternalCurveDetectionMsg, PlanningInternalMissionPlanMsg
from simple_av_msgs.msg import LocalizationMsg
from simple_av_msgs.msg import Portal
import numpy as np
from simple_av_msgs.srv import TriggerMissionPlan
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy

class PathCurveDetector:
    def __init__(self, points, angle_threshold=15):
        self.points = points
        self.angle_threshold = math.radians(angle_threshold)  # Convert threshold to radians
        self.angle_max = math.radians(120.0)

    @staticmethod
    def direction_vector(p1, p2):
        return (p2['x'] - p1['x'], p2['y'] - p1['y'], p2['z'] - p1['z'])

    @staticmethod
    def vector_magnitude(v):
        return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

    @staticmethod
    def dot_product(v1, v2):
        return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

    @staticmethod
    def angle_between_vectors(v1, v2):
        dot_prod = PathCurveDetector.dot_product(v1, v2)
        mag_v1 = PathCurveDetector.vector_magnitude(v1)
        mag_v2 = PathCurveDetector.vector_magnitude(v2)
        if mag_v1 == 0 or mag_v2 == 0:
            return 0
        cos_theta = dot_prod / (mag_v1 * mag_v2)
        # Ensure the cosine value is within the valid range
        cos_theta = min(1.0, max(-1.0, cos_theta))
        return math.acos(cos_theta)

    def find_curves_in_path(self):
        curves = []
        if len(self.points) < 3:
            return curves

        for i in range(1, len(self.points) - 1):
            v1 = self.direction_vector(self.points[i-1], self.points[i])
            v2 = self.direction_vector(self.points[i], self.points[i+1])
            angle = self.angle_between_vectors(v1, v2)
            if self.angle_threshold < angle < self.angle_max:
                curve = {}
                curve[angle] = self.points[i]
                curves.append(curve)

        return curves


class BehaviorPathPlanner(Node):
    def __init__(self):
        super().__init__('behavior_path_planner_node')

        # Load scenario configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.dest_lanelet = self.scenario_config['scenario']['destination']
        self.start_lanelet = None

        # Load motion & behavior configs
        self.motion_behavior_config = self.config_file_loader("motion_behavior_config.yaml")
        self.base_speed = self.motion_behavior_config['motion']['speed_limits']['base'] # m/s
        self.turning_speed = self.motion_behavior_config['motion']['speed_limits']['turning_speed'] # m/s
        self.lookahead_distance_C = self.motion_behavior_config['motion']['lookahead']['coefficient']
        self.lookahead_distance_B = self.motion_behavior_config['motion']['lookahead']['base']

        # Subscribe topics
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        self.pose = PoseStamped()

        self.subscriptionLocation = self.create_subscription(LocalizationMsg, 'simple_av/localization/location', self.location_callback, 10)
        self.location = LocalizationMsg()

        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        self.subscription_mission_plan = self.create_subscription(PlanningInternalMissionPlanMsg, 'simple_av/planning/mission_plan', self.mission_plan_callback, qos_profile)
        self.mission_plan = PlanningInternalMissionPlanMsg()
        self.path_as_lanes = None  # List of lanes from start lane to destination
        self.path = None  # List of waypoints in order of path_as_lanes

        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False

        # Publish topics
        self.planning_publisher = self.create_publisher(PlanningPathPlanningMsg, 'simple_av/planning/path_planning', 10)
        self.curve_detection_publisher = self.create_publisher(PlanningInternalCurveDetectionMsg, 'simple_av/planning/curve_detection', 10)

        self.mission_planner_client = self.create_client(TriggerMissionPlan, '/planning/trigger_mission_plan')
        # Optional: check if service is ready
        while not self.mission_planner_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /planning/trigger_mission_plan service...')
        

        #Path planning
        self.isPathPlanned = False  # Flag to check if the path has been planned
        self.route = None # List of lanes from start lane to destination
        self.current_lane_index = 0
        self.initial_lane = None
        self.search_depth = 5
        self.destination = Point()
        
        #Lookahead
        self.lookahead_distance = self.base_speed * self.lookahead_distance_C + self.lookahead_distance_B # meters
        self.current_speed = 0.0
        
        #Curve handling
        self.curves = None
        self.isCurveFinished = False
        self.isCurveStarted = False
        self.curve_angle = 0.0
        self.curve_finish_point = None

        self.densify_interval = 2.0 # meters / Distance between each two consecutive waypoints on a lane

        #Shutting down
        self.node_shut = False
    
    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('simple_av')
        config_path = os.path.join(package_share_directory, "resource", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    
    def portal_callback(self, msg):
        self.reset = msg.reset
        self.finished = msg.finished
    
    def mission_plan_callback(self, msg):
        self.mission_plan = msg
        self.path = self.mission_plan.path
        self.path_as_lanes = self.mission_plan.path_as_lanes

    def pose_callback(self, msg):
        self.pose = msg

    def location_callback(self, msg):
        self.location = msg

    def calculate_distance(self, point1, point2, z=False):
        """
        Calculate the Euclidean distance between two points.
        Args:
            point1 (dict): The first point with 'x', 'y', 'z' coordinates.
            point2 (dict): The second point with 'x', 'y', 'z' coordinates.
        Returns:
            float: The Euclidean distance between the two points.
        """
        if z:
            return np.sqrt((point1['x'] - point2['x'])**2 + 
                        (point1['y'] - point2['y'])**2 + 
                        (point1['z'] - point2['z'])**2)
        else:
            return np.sqrt((point1['x'] - point2['x'])**2 + (point1['y'] - point2['y'])**2)

    def calculate_vector(self, point1, point2):
        """
        Calculate the vector from point1 to point2.
        Args:
            point1 (dict): The starting point with 'x', 'y', 'z' coordinates.
            point2 (dict): The ending point with 'x', 'y', 'z' coordinates.
        Returns:
            np.array: The vector from point1 to point2.
        """
        return np.array([point2['x'] - point1['x'], 
                        point2['y'] - point1['y'], 
                        point2['z'] - point1['z']])

    def calculate_dot_product(self, vector1, vector2):
        """
        Calculate the dot product of two vectors.
        Args:
            vector1 (np.array): The first vector.
            vector2 (np.array): The second vector.
        Returns:
            float: The dot product of the two vectors.
        """
        return np.dot(vector1, vector2)
    
    def find_lane_by_name(self, lane_name):
        """
        Get the lane object by its name.
        Args:
            lane_name (str): The name of the lane.
        Returns:
            dict: The lane object if found, else None.
        """
        lane_number = lane_name.replace("lanelet", "")
        lane_number = int(lane_number)
        if lane_number > len(self.map_data):
            return None
        return self.map_data[lane_number - 1]

    def get_first_ahead_point(self, vehicle_pose, current_closest_point_index):
        
        # Calculate direction vectors
        direction_vector = self.calculate_vector(self.path[current_closest_point_index], self.path[current_closest_point_index + 1])
        direction_vector_of_robot = self.calculate_vector(self.path[current_closest_point_index], vehicle_pose)   
        first_ahead_point_index = 0

        # Find the first point ahead of the vehicle
        if self.calculate_dot_product(direction_vector, direction_vector_of_robot) >= 0: # Vehicle is ahead of the point
            first_ahead_point_index = current_closest_point_index + 1
        else: # Vehicle is Behind of the point
            first_ahead_point_index = current_closest_point_index
        return first_ahead_point_index
        

    def find_lookahead_point(self, vehicle_pose, current_closest_point_index, search_area): 
        """
        Get the next point for the vehicle to move towards.
        Args:
            vehicle_pose (dict): The current pose of the vehicle.
            current_closest_point_index (int): The index of the current closest point in the path.
            search_area (list): The list of the points in the search area.
        Returns:
            tuple: The updated closest point index and the next point.
        """
        search_area_indexes_on_path = (self.path.index(search_area[0]), self.path.index(search_area[-1]))
        if current_closest_point_index == len(self.path) - 1:
            return current_closest_point_index, self.path[current_closest_point_index]
        first_ahead_point_index = self.get_first_ahead_point(vehicle_pose, current_closest_point_index)
        
        # final point in path
        if first_ahead_point_index >= len(self.path):
            return first_ahead_point_index, self.path[first_ahead_point_index]
        
        # find the lookahead point in front of the vehicle.  lookahead distance - interval < look ahead point distance <= lookahead distance
        for i in range(first_ahead_point_index, search_area_indexes_on_path[1]):
            dist = self.calculate_distance(vehicle_pose, self.path[i])
            if dist <= self.lookahead_distance + 4.0 and dist >= self.lookahead_distance:
                return i, self.path[i]
        
        self.get_logger().error("Look ahead point not found!")
        # TODO: modify this part
        if len(self.path) - first_ahead_point_index - 1 <= 10:
            return len(self.path) - 1, self.path[-1]
        return first_ahead_point_index + 10, self.path[first_ahead_point_index + 10]

    def adjust_speed_to_curve(self, curve_angle):
        # return self.base_speed
        if curve_angle >= 0.25:
            return float(math.ceil(self.base_speed / 3.0))
        else:
            return float(math.ceil(self.base_speed / 2))


    def curve_detector(self, curves, look_ahead_point, look_ahead_point_index):
        if look_ahead_point_index >= len(self.path) - 5 and look_ahead_point_index <= len(self.path):
            return False, 0.0

        if not self.isCurveStarted and not self.isCurveFinished:
            for curve in curves:
                k, v = next(iter(curve.items()))
                # if self.path[look_ahead_point_index - 2] == v or self.path[look_ahead_point_index - 1] == v or self.path[look_ahead_point_index] == v or self.path[look_ahead_point_index+1] == v or self.path[look_ahead_point_index+2] == v:
                if self.path[look_ahead_point_index - 1] == v or self.path[look_ahead_point_index] == v or self.path[look_ahead_point_index+1] == v:
                    # self.get_logger().info("curve started")
                    self.curve_angle = k
                    self.curve_finish_point = self.path[look_ahead_point_index + int(self.lookahead_distance//self.densify_interval) + 6]
                    self.isCurveStarted = True
                    self.isCurveFinished = False
                    # self.isCurveDetected = True
                    return True, self.curve_angle    
        if self.isCurveStarted and not self.isCurveFinished:
            vehicle_pose = {'x': self.pose.pose.position.x, 'y': self.pose.pose.position.y, 'z': self.pose.pose.position.z}
            if self.calculate_distance(vehicle_pose, self.curve_finish_point) <= self.densify_interval * 2:
                # self.get_logger().info("curve finished")
                self.isCurveFinished = True
                self.isCurveStarted = True
                return False, 0.0
            return True, self.curve_angle
        if self.isCurveStarted and self.isCurveFinished:
            self.isCurveStarted = False
            self.isCurveFinished = False
            # self.isCurveDetected = False
            return False, 0.0
        return False, 0.0


    def curve_handler(self, look_ahead_point, look_ahead_point_index):
        isTurnDetected, curve_angle = self.curve_detector(self.curves, look_ahead_point, look_ahead_point_index)
        return isTurnDetected
    
    # TODO: create search area based on waypoints not lanes
    def create_search_area(self):
        try:
            lane_index = self.route.index(self.location.closest_lane_names.data)
        except:
            # vehicle is out of path
            # self.get_logger().warning("Vehicle is out of the Path")
            lane_index = self.current_lane_index
        if lane_index in range(self.current_lane_index, self.current_lane_index + self.search_depth):
            self.current_lane_index = lane_index
        search_area_as_lanes = self.path_as_lanes[self.current_lane_index: self.current_lane_index + self.search_depth]

        # convert lanes in the search are into a list of waypoints
        search_area = []
        for lane in search_area_as_lanes:
            lane_obj = self.find_lane_by_name(lane)
            waypoints = lane_obj['dense_waypoints']
            for waypoint in waypoints:
                search_area.append(waypoint)
        # print("debug - search area as lanes", search_area_as_lanes, "size of search area: ", len(search_area))
        return search_area, search_area_as_lanes

    def find_closest_waypoint_to_vehicle(self, vehicle_pose, search_area):
        # Finding the index of the closest point in search area
        distances_to_vehicle = []
        for waypoint in search_area:
            distances_to_vehicle.append(self.calculate_distance(waypoint, vehicle_pose))
        closest_waypoint_to_vehicle = search_area[distances_to_vehicle.index(min(distances_to_vehicle))]
        current_closest_point_to_vehicle = self.path.index(closest_waypoint_to_vehicle)
        return current_closest_point_to_vehicle

    def update_target_speed(self, isTurnDetected):
        speed = self.base_speed
        if isTurnDetected:
            speed = self.turning_speed
        return speed

    def path_planning(self, search_area):
        """
        Perform local path planning to determine the next point for the vehicle.
        """
        if self.pose.pose.position.x == 0.0 and self.pose.pose.position.y == 0.0 and self.pose.pose.position.z == 0.0:
            self.get_logger().warning("Vehicle Pose is not accessible")
            return None, None, None, None, None
        vehicle_pose = {'x': self.pose.pose.position.x, 'y': self.pose.pose.position.y, 'z': self.pose.pose.position.z}
        
        current_closest_point_to_vehicle_index = self.find_closest_waypoint_to_vehicle(vehicle_pose, search_area)
        look_ahead_point_index, look_ahead_point = self.find_lookahead_point(vehicle_pose, current_closest_point_to_vehicle_index, search_area)
        isTurnDetected = self.curve_handler(look_ahead_point, look_ahead_point_index)
        target_speed = self.update_target_speed(isTurnDetected)
        
        # print("DEBUG - look ahead distance: ", self.lookahead_distance)
        return look_ahead_point_index, look_ahead_point, isTurnDetected, target_speed
        
    def dot_product(self, v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]
            
    def publish_path_planning_msgs(self, look_ahead_point, speed):
        lookahead_point = PlanningPathPlanningMsg()
        lookahead_point.look_ahead_point = Point(x=look_ahead_point['x'], y=look_ahead_point['y'], z=look_ahead_point['z'])
        lookahead_point.speed_limit = speed
        self.planning_publisher.publish(lookahead_point)
    
    def publish_curve_detection_msg(self, isTurnDetected):
        curve_detection = PlanningInternalCurveDetectionMsg()
        curve_detection.is_curve_detected = isTurnDetected
        self.curve_detection_publisher.publish(curve_detection)

    def request_mission_plan(self):
        request = TriggerMissionPlan.Request()
        future = self.mission_planner_client.call_async(request)
        self.get_logger().info('Requested mission plan from MissionPlanner.')
        return future

    def handle_mission_plan(self):
        self.get_logger().info("Finding Curves Along the Path ...")
        if self.path and self.path_as_lanes:
            self.destination = Point(x=self.path[-1]['x'], y=self.path[-1]['y'], z=self.path[-1]['z'])
            path_curve_detector = PathCurveDetector(self.path, angle_threshold=3) # initializing object from class
            self.curves = path_curve_detector.find_curves_in_path() # locating curves on the route/path
        if self.path and self.path_as_lanes and self.curves:
            self.get_logger().info("Curves found.")
            print("path of lanes: ", self.path_as_lanes)
            # self.initial_lane = self.location.closest_lane_names.data
            self.route = self.path_as_lanes[:]
            self.current_lane_index = 0
            self.isPathPlanned = True

    def lane_following(self):
        self.get_logger().info("lane following start...")
        if not self.location and not self.pose:
            self.get_logger().warning("No location/pose input")
            return None
        
        print("self.isPathPlanned: ", self.isPathPlanned)
        if not self.isPathPlanned:
            self.get_logger().info("Requesting Misson planning Service ...")
            self.request_mission_plan()
            rclpy.spin_once(self, timeout_sec=0.1)  # allow 0.1s to receive mission plan
            self.handle_mission_plan()
            self.get_logger().info("Start Local Path Planning...")
            return
        
        if self.finished:
            self.get_logger().info("Scenario Finished, Parking the Vehicle...")
            self.node_shut = True
            self.publish_path_planning_msgs(None, 0) # publishing
            return
    
        if self.reset:
            self.get_logger().warning("RESET")
            self.isPathPlanned = False
            self.get_logger().info("Requesting Misson planning Service ...")
            self.request_mission_plan()
            rclpy.spin_once(self, timeout_sec=0.1)  # allow 0.1s to receive mission plan
            self.handle_mission_plan()
        
        if self.path and self.path_as_lanes:
            self.get_logger().info("Path has successfully initialized from Mission Planner")
        else:
            self.get_logger().warning("Path has not initialized from Mission Planner!!")
            return
            
        search_area, search_area_as_lanes = self.create_search_area()
        look_ahead_point_index, look_ahead_point, isTurnDetected, speed = self.path_planning(search_area)
        if not look_ahead_point and not look_ahead_point_index:
            self.get_logger().warning("Lookahead point not set in local planning")
            return

        self.publish_curve_detection_msg(isTurnDetected)
        self.publish_path_planning_msgs(look_ahead_point, speed) # publishing
        
        self.get_logger().info(
            f'planning\n'
            f'lookahead distance:  {self.lookahead_distance}\n'
            f'speed: {speed}\n'
        )


def main(args=None):
    rclpy.init(args=args)
    node = BehaviorPathPlanner()
    try:
        while rclpy.ok() and not node.node_shut:
            rclpy.spin_once(node, timeout_sec=None)# Set timeout to 0 to avoid delay
            node.lane_following()
    finally:
        node.destroy_node()
        rclpy.shutdown()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()