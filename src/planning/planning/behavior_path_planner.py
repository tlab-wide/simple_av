#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import os
import json
import yaml
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped, Point
from std_msgs.msg import String
import math
from collections import deque
from simple_av_msgs.msg import PlanningPathPlanningMsg, PlanningInternalMsg, PlanningInternalMissionPlanMsg, PlanningWaypoint
from simple_av_msgs.msg import LocalizationMsg
from simple_av_msgs.msg import Portal
import numpy as np
from simple_av_msgs.srv import TriggerMissionPlan
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy


class BehaviorPathPlanner(Node):
    def __init__(self):
        super().__init__('behavior_path_planner_node')

        # Load scenario configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.vehicle_model = self.scenario_config['scenario']['vehicle_model']
        self.dest_lanelet = self.scenario_config['scenario']['destination']
        self.start_lanelet = None

        # Load the map
        self.map_data = self.load_map_data(self.vehicle_model)
        self.map_data = self.map_data["LaneLetsArray"]

        self.graph = {lanelet['name']: {
            'waypoints': lanelet['waypoints'],
            'nextLanes': lanelet.get('nextLanes', []),
            'prevLanes': lanelet.get('prevLanes', []),
            'adjacentLanes': lanelet.get('adjacentLanes', []),
        } for lanelet in self.map_data}

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
        self.path = None  # List of [waypoints,curve] in order of path_as_lanes
        self.path_of_waypoints = [] # List of waypoints in order of path_as_lanes

        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False

        # Publish topics
        self.planning_publisher = self.create_publisher(PlanningPathPlanningMsg, 'simple_av/planning/path_planning', 10)
        self.internal_msg_publisher = self.create_publisher(PlanningInternalMsg, 'simple_av/planning/internal_msg', 10)

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
        self.speeds_on_path = []
        self.prev_lookahead_index = 0

        self.densify_interval = 2.0 # meters / Distance between each two consecutive waypoints on a lane

        #Shutting down
        self.node_shut = False
    

    def load_map_data(self, vehicle_model):
        """
        Load the map data from a JSON file.
        Returns:
            dict: The map data loaded from the JSON file.
        """
        package_share_directory = get_package_share_directory('common')
        if vehicle_model == 'lexus':
            json_file_path = os.path.join(package_share_directory, 'maps', 'Kashiwa-lexus.json')
        else:
            json_file_path = os.path.join(package_share_directory, 'maps', 'Kashiwa-bus.json')
        # Load and read the JSON file
        with open(json_file_path, 'r') as json_file:
            map_data = json.load(json_file)
            return map_data
    
    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
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
            point1 (geometry_point): The first point with 'x', 'y', 'z' coordinates.
            point2 (geometry_point): The second point with 'x', 'y', 'z' coordinates.
        Returns:
            float: The Euclidean distance between the two points.
        """
        if z:
            return np.sqrt((point1.x - point2.x)**2 + 
                        (point1.y - point2.y)**2 + 
                        (point1.z - point2.z)**2)
        else:
            return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def calculate_vector(self, point1, point2):
        """
        Calculate the vector from point1 to point2.
        Args:
            point1 (geometry_point): The starting point with 'x', 'y', 'z' coordinates.
            point2 (geometry_point): The ending point with 'x', 'y', 'z' coordinates.
        Returns:
            np.array: The vector from point1 to point2.
        """
        return np.array([point2.x - point1.x, 
                        point2.y - point1.y, 
                        point2.z - point1.z])

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
        direction_vector = self.calculate_vector(self.path_of_waypoints[current_closest_point_index], self.path_of_waypoints[current_closest_point_index + 1])
        direction_vector_of_robot = self.calculate_vector(self.path_of_waypoints[current_closest_point_index], vehicle_pose)   
        first_ahead_point_index = 0

        # Find the first point ahead of the vehicle
        if self.calculate_dot_product(direction_vector, direction_vector_of_robot) >= 0: # Vehicle is ahead of the point
            first_ahead_point_index = current_closest_point_index + 1
        else: # Vehicle is Behind of the point
            first_ahead_point_index = current_closest_point_index
        return first_ahead_point_index
        
    def get_lookahead_distance_as_index(self):
        return int(self.lookahead_distance //  self.densify_interval)
       

    def find_lookahead_point(self, current_closest_point_index): 

        path_size = len(self.path)
        print("DEBUG: path size: ", path_size)
        lookahead_point_index = self.get_lookahead_distance_as_index() + current_closest_point_index
        print("DEBUG: lookahead_point_index: ", lookahead_point_index)
        if lookahead_point_index >= path_size - 2:
            print("Debug3: close to destination ")
            lookahead_point_index = path_size - 2
        if lookahead_point_index < self.prev_lookahead_index:
            lookahead_point_index = self.prev_lookahead_index
        else:
            self.prev_lookahead_index = lookahead_point_index
        
        return lookahead_point_index, self.path[lookahead_point_index].waypoint
    
    def adjust_speed_to_curve(self, curve_angle):
        # return self.base_speed
        if curve_angle >= 0.25:
            return float(math.ceil(self.base_speed / 3.0))
        else:
            return float(math.ceil(self.base_speed / 2))
    
    # TODO: create search area based on waypoints not lanes
    def create_search_area(self):
        print("Debug: in create search area")
        try:
            lane_index = self.route.index(self.location.closest_lane_names.data)
        except:
            # vehicle is out of path
            self.get_logger().warning("Vehicle is out of the Path")
            lane_index = self.current_lane_index
        if lane_index in range(self.current_lane_index, self.current_lane_index + self.search_depth):
            self.current_lane_index = lane_index
        search_area_as_lanes = self.path_as_lanes[self.current_lane_index: self.current_lane_index + self.search_depth]
        # convert lanes in the search are into a list of waypoints
        search_area = []
        for lane in search_area_as_lanes:
            lane_obj = self.find_lane_by_name(lane)
            # print("Debug: lane: ", lane)
            waypoints = lane_obj['dense_waypoints']
            for waypoint in waypoints:
                search_area.append(Point(x=waypoint['x'], y=waypoint['y'], z=waypoint['z']))
        # print("debug - search area as lanes", search_area_as_lanes, "size of search area: ", len(search_area))
        return search_area, search_area_as_lanes

    def find_closest_waypoint_to_vehicle(self, vehicle_pose, search_area):
        # Finding the index of the closest point in search area
        distances_to_vehicle = []
        for waypoint in search_area:
            distances_to_vehicle.append(self.calculate_distance(waypoint, vehicle_pose))
        closest_waypoint_to_vehicle = search_area[distances_to_vehicle.index(min(distances_to_vehicle))]
        current_closest_point_to_vehicle = self.path_of_waypoints.index(closest_waypoint_to_vehicle)
        return current_closest_point_to_vehicle
        
    def dot_product(self, v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]
            
    def publish_path_planning_msgs(self, look_ahead_point, speed):
        lookahead_point = PlanningPathPlanningMsg()
        # lookahead_point.look_ahead_point = Point(x=look_ahead_point['x'], y=look_ahead_point['y'], z=look_ahead_point['z'])
        lookahead_point.look_ahead_point = look_ahead_point
        lookahead_point.speed_limit = speed
        self.planning_publisher.publish(lookahead_point)
    
    def publish_curve_internal_msg(self, isTurnDetected, isEndOfPath):
        internal_msg = PlanningInternalMsg()
        internal_msg.is_curve_detected = isTurnDetected
        internal_msg.is_end_of_path = isEndOfPath
        self.internal_msg_publisher.publish(internal_msg)

    def request_mission_plan(self):
        request = TriggerMissionPlan.Request()
        future = self.mission_planner_client.call_async(request)
        return future
    
    def adjust_speed_to_curve(self, curvature, max_speed=11.0, k=1.0):
        # If curvature is zero, return the max speed (straight path)
        if curvature == 0:
            return max_speed
        
        # Calculate speed using the given formula
        speed = min(max_speed, k / curvature)
        return speed

    def get_path_speed_profile(self, path, accel = 2.0):
        speeds = []
        for i, waypoint in enumerate(path):
            speed = self.adjust_speed_to_curve(waypoint.curve)
            speeds.append(speed)
        
        updated_speeds = []
        for i in range(len(speeds) - 6):
            new_speed = min(speeds[i], math.sqrt((speeds[i+1]) ** 2 + 2 * accel))
            filtered_speed = new_speed + 0.6 * (abs(speeds[i+1] - new_speed))
            updated_speeds.append(max(filtered_speed, 2.5))

        j = 1
        for i in range(len(speeds) - 6, len(speeds) - 1):
            new_speed = 11.0 - j * float(11.0/6)
            if new_speed < 0:
                new_speed = 0
            updated_speeds.append(new_speed)
            j += 1
            
        updated_speeds.append(0.0)

        return updated_speeds

    def handle_mission_plan(self):

        if self.path and self.path_as_lanes:
            self.destination = self.path[-1].waypoint
            self.speeds_on_path = self.get_path_speed_profile(self.path)
            
            for i, waypoint in enumerate(self.path):
                self.path_of_waypoints.append(waypoint.waypoint)

            self.route = self.path_as_lanes[:]
            self.current_lane_index = 0
            self.isPathPlanned = True
            print("Debug: path of lanes: ", self.path_as_lanes)
            print("Debug: lanes size: ", len(self.path_as_lanes))

    def end_of_path_detection(self, current_closest_point_to_vehicle_index):
        current_pose = self.path_of_waypoints[current_closest_point_to_vehicle_index]
        
        distance = self.calculate_distance(current_pose, self.destination)
        if distance <= 2.0:
            return True
        return False

    def lane_following(self):
        if not self.location and not self.pose:
            self.get_logger().warning("No location/pose input")
            return None
        
        if not self.isPathPlanned:
            self.get_logger().info("Requesting Misson planning Service ...")
            self.request_mission_plan()
            rclpy.spin_once(self, timeout_sec=0.25)  # allow 0.25s to receive mission plan
            self.handle_mission_plan()
            self.get_logger().info("Start Local Path Planning...")
            if self.path and self.path_as_lanes:
                self.get_logger().info("Path has successfully initialized from Mission Planner")
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
            rclpy.spin_once(self, timeout_sec=0.125)  # allow 0.25s to receive mission plan
            self.handle_mission_plan()
        
        if not self.path and not self.path_as_lanes:
            self.get_logger().warning("Path has not initialized from Mission Planner!!")
            return
        
        vehicle_pose = self.pose.pose.position
        if vehicle_pose.x == 0.0 and vehicle_pose.y == 0.0 and vehicle_pose.z == 0.0:
            self.get_logger().warning("Vehicle Pose is not accessible")
            return None, None, None, None
            
        search_area, search_area_as_lanes = self.create_search_area()
        current_closest_point_to_vehicle_index = self.find_closest_waypoint_to_vehicle(vehicle_pose, search_area)
        look_ahead_point_index, look_ahead_point = self.find_lookahead_point(current_closest_point_to_vehicle_index)
        isEndOfPath = self.end_of_path_detection(current_closest_point_to_vehicle_index)
        if not look_ahead_point and not look_ahead_point_index:
            self.get_logger().warning("Lookahead point not set in local planning")
            return
        
        self.lookahead_distance = self.speeds_on_path[look_ahead_point_index] * self.lookahead_distance_C + self.lookahead_distance_B # meters

        isTurnDetected = False
        if self.speeds_on_path[look_ahead_point_index] < 10.0:
            isTurnDetected = True

        self.publish_curve_internal_msg(isTurnDetected, isEndOfPath)
        self.publish_path_planning_msgs(look_ahead_point, self.speeds_on_path[look_ahead_point_index]) # publishing
        
        self.get_logger().info(
            f'behavior path planning\n'
            f'lookahead distance:  {self.lookahead_distance}\n'
            f'current point index:  {current_closest_point_to_vehicle_index}\n'
            f'lookahead point index:  {look_ahead_point_index}\n'
            f'speed: {self.speeds_on_path[look_ahead_point_index]}\n'
            f'is turn detected: {isTurnDetected}\n'
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