import rclpy
from rclpy.node import Node
import json
import os
import yaml
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped, Point
from std_msgs.msg import String
import math
from collections import deque
from simple_av_msgs.msg import LocalizationMsg
from simple_av_msgs.msg import Portal
from simple_av_msgs.msg import LookAheadMsg, SimMonitor
from v2x_msgs.msg import CooperativeSignalsMessage
import numpy as np
from simple_av_msgs.msg import TrafficSignalsArray, DetectedObjectsArray, DetectedObject
from scipy.spatial.transform import Rotation as R
from autoware_auto_vehicle_msgs.msg import VelocityReport

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


class Planning(Node):
    def __init__(self, vehicle_type):
        super().__init__('Planning')

        # Load vehicle configs
        self.vehicle_type = vehicle_type
        self.vehicle_config = self.load_vehicle_config(vehicle_type)
        self.vehicle_length = self.vehicle_config['dimensions']['length'] #meters
        self.vehicle_width = self.vehicle_config['dimensions']['width'] #meters

        # Load scenario configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.dest_lanelet = self.scenario_config['scenario']['destination']
        self.start_lanelet = None

        # Load av features configs
        self.av_features = self.config_file_loader("av_features.yaml")
        self.use_RSU_for_trafficlight = self.av_features['traffic_light']['use_rsu']
        self.use_RSU_for_object_detection = self.av_features['object_detection']['use_rsu']

        # Load motion & behavior configs
        self.motion_behavior_config = self.config_file_loader("motion_behavior_config.yaml")
        self.base_speed = self.motion_behavior_config['motion']['speed_limits']['base'] # m/s
        self.turning_speed = self.motion_behavior_config['motion']['speed_limits']['turning_speed'] # m/s
        self.lookahead_distance_C = self.motion_behavior_config['motion']['lookahead']['coefficient']
        self.lookahead_distance_B = self.motion_behavior_config['motion']['lookahead']['base']

        self.saftey_distance = self.motion_behavior_config['behavior']['safety_distance'] #meters
        self.reaction_time_threshold = self.motion_behavior_config['behavior']['reaction_time_threshold'] #meters
        self.range_low_pass_gain = self.motion_behavior_config['behavior']['range_low_pass_gain'] #meters

        self.on_path_detection_range_C = self.motion_behavior_config['behavior']['on_path_detection_range']['coefficient']
        self.on_path_detection_range_B = self.motion_behavior_config['behavior']['on_path_detection_range']['base']

        self.prediction_reaction_range_C = self.motion_behavior_config['behavior']['prediction_reaction_range']['coefficient']
        self.prediction_reaction_range_B = self.motion_behavior_config['behavior']['prediction_reaction_range']['base']
        self.prediction_detection_range_C = self.motion_behavior_config['behavior']['prediction_detection_range']['coefficient']
        self.prediction_detection_range_B = self.motion_behavior_config['behavior']['prediction_detection_range']['base']
        
        # Load the map
        self.map_data = self.load_map_data()
        self.map_data = self.map_data["LaneLetsArray"]

        self.graph = {lanelet['name']: {
            'waypoints': lanelet['waypoints'],
            'nextLanes': lanelet.get('nextLanes', []),
            'prevLanes': lanelet.get('prevLanes', []),
            'adjacentLanes': lanelet.get('adjacentLanes', []),
        } for lanelet in self.map_data}

        # Subscribe topics
        self.subscriptionVelocityReport = self.create_subscription(VelocityReport, '/vehicle/status/velocity_status', self.velocity_report_callback, 10)
        self.velocity_report = VelocityReport()

        self.subscriptionTrafficSignal = self.create_subscription(TrafficSignalsArray, 'simple_av/perception/traffic_signals', self.trafficSignal_callback, 10)
        self.trafficSignal = TrafficSignalsArray()

        self.subscriptionDetectedObjects = self.create_subscription(DetectedObjectsArray, 'simple_av/perception/detected_objects', self.detectedObjects_callback, 10)
        self.detectedObjects = DetectedObjectsArray()

        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        self.pose = PoseStamped()

        self.subscriptionLocation = self.create_subscription(LocalizationMsg, 'simple_av/localization/location', self.location_callback, 10)
        self.location = LocalizationMsg()

        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False

        self.subscriptionSimMonitor = self.create_subscription(SimMonitor, 'simple_av/sim_monitor', self.sim_monitor_callback, 100)
        self.sim_clock_rate = 0

        # Publish topics
        self.planning_publisher = self.create_publisher(LookAheadMsg, 'simple_av/planning/lookahead_point', 10)

        #Path planning
        self.isPathPlanned = False  # Flag to check if the path has been planned
        self.path_as_lanes = None  # List of lanes from start lane to destination
        self.path = None  # List of waypoints in order of path_as_lanes
        self.route = None # List of lanes from start lane to destination
        self.current_lane_index = 0
        self.initial_lane = None
        self.search_depth = 5
        self.destination = Point()
        
        #Lookahead, Observation and detection range
        self.lookahead_distance = self.base_speed * self.lookahead_distance_C + self.lookahead_distance_B # meters
        self.on_path_detection_range = self.base_speed * self.on_path_detection_range_C + self.on_path_detection_range_B # meters
        self.reaction_range = self.base_speed * self.prediction_reaction_range_C + self.prediction_reaction_range_B # meters
        self.detection_range = self.base_speed * self.prediction_detection_range_C + self.prediction_detection_range_B # meters
        self.current_speed = 0.0
        self.previous_speed_slidingWindow = deque(maxlen=8) # for storing 10 recent previous speed values
        self.previous_speed_slidingWindow.append(0.0)  # initializing the queue
        self.status = String() # Cruise, Decelerate, PrepareToStop, Turn
        
        #Curve handling
        self.curves = None
        self.isCurveFinished = False
        self.isCurveStarted = False
        self.curve_angle = 0.0
        self.curve_finish_point = None

        self.densify_interval = 2.0 # meters / Distance between each two consecutive waypoints on a lane
        
        #Traffic light
        self.traffic_light_stopPoint_lastState = Point()
        self.traffic_light_state_lastState = 'Cruise_green'
        self.opposite_traffic_light_last_Color = 'Green'

        #Shutting down
        self.node_shut = False

    def sim_monitor_callback(self, msg):
        self.sim_clock_rate = msg.sim_clock_rate
    
    def velocity_report_callback(self, msg):
        self.velocity_report = msg
    
    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('simple_av')
        config_path = os.path.join(package_share_directory, "resource", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def load_vehicle_config(self, vehicle_type="lexus"):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('simple_av')
        config_path = os.path.join(package_share_directory, "resource", "vehicle_config.yaml")

        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        # Retrieve the specific vehicle's configuration
        if vehicle_type in config["vehicles"]:
            return config["vehicles"][vehicle_type]
        else:
            raise ValueError(f"Vehicle type '{vehicle_type}' not found in the configuration.")
    

    def load_map_data(self):
        """
        Load the map data from a JSON file.
        Returns:
            dict: The map data loaded from the JSON file.
        """
        package_share_directory = get_package_share_directory('simple_av')
        json_file_path = os.path.join(package_share_directory, 'resource', 'Kashiwa.json')
        # json_file_path = os.path.join(package_share_directory, 'resource', 'Shinjuku.json')
        # Load and read the JSON file
        with open(json_file_path, 'r') as json_file:
            map_data = json.load(json_file)
            return map_data
    
    def portal_callback(self, msg):
        self.reset = msg.reset
        self.finished = msg.finished

    def trafficSignal_callback(self, msg):
        """
        Callback function to update the pose data.
        Args:
            msg (PoseStamped): The pose message received from the topic.
        """
        self.trafficSignal = msg

    def detectedObjects_callback(self, msg):
        """
        Callback function to update the pose data.
        Args:
            msg (PoseStamped): The pose message received from the topic.
        """
        self.detectedObjects = msg

    def pose_callback(self, msg):
        """
        Callback function to update the pose data.
        Args:
            msg (PoseStamped): The pose message received from the topic.
        """
        self.pose = msg

    def location_callback(self, msg):
        """
        Callback function to update the location data.
        Args:
            msg (LocalizationMsg): The localization message received from the topic.
        """
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
    
    def display_vehicle_position(self, msg_pose, closest_point, closest_lane_name, min_distance):
        self.get_logger().info(
                f'Received Pose :\n'
                f'Position - x: {msg_pose.pose.position.x}, y = {msg_pose.pose.position.y}, z = {msg_pose.pose.position.z}\n'
                f'Closest point: {closest_point.get_point()}\n'
                f'Closest Lane: {closest_lane_name}\n'
                f'Minimum distance - {min_distance}\n'
            )
    
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


    def densify_waypoints(self, waypoints):
        """
        Densifies a list of waypoints by adding interpolated points so that there is 
        approximately one point every `densify_interval` meters.
        
        Args:
            waypoints (list): A list of dictionaries, each with 'x', 'y', and 'z' keys representing
                            a waypoint's coordinates.
            densify_interval (float): The desired distance (in meters) between consecutive waypoints.

        Returns:
            list: A new list of waypoints with additional interpolated points.
        """
        dense_waypoints = []

        for i in range(len(waypoints) - 1):
            start = waypoints[i]
            end = waypoints[i + 1]
            dense_waypoints.append(start)

            distance = self.calculate_distance(start, end)
            num_points = int(distance // self.densify_interval)

            for j in range(1, num_points + 1):
                t = j / num_points
                new_point = {
                    'x': start['x'] + t * (end['x'] - start['x']),
                    'y': start['y'] + t * (end['y'] - start['y']),
                    'z': start['z'] + t * (end['z'] - start['z'])
                }
                dense_waypoints.append(new_point)

        dense_waypoints.append(waypoints[-1])
        return dense_waypoints

    def generate_path_points(self):
        """
        Create a path of points based on the path of lanes.
        """
        points = []
        for lane_name in self.path_as_lanes:
            lane_obj = self.find_lane_by_name(lane_name)
            waypoints = lane_obj['dense_waypoints']
            for waypoint in waypoints:
                points.append(waypoint)

        # Densify path of points
        # points = self.densify_waypoints(points)

        # Remove duplicate points
        self.path = [points[i] for i in range(len(points)) if i == 0 or (points[i]['x'] != points[i - 1]['x'] or points[i]['y'] != points[i - 1]['y'] or points[i]['z'] != points[i - 1]['z'])]
    

    def bfs(self, start_lanelet, dest_lanelet):
        """
        Perform Breadth-First Search (BFS) to find a path from start_lanelet to dest_lanelet.
        Args:
            start_lanelet (str): The name of the starting lanelet.
            dest_lanelet (str): The name of the destination lanelet.
        """
        if start_lanelet not in self.graph or dest_lanelet not in self.graph:
            return

        queue = deque([(start_lanelet, [start_lanelet])])
        visited = set()
        visited.add(start_lanelet)

        while queue:
            current_lanelet, path = queue.popleft()

            if current_lanelet == dest_lanelet:
                self.path_as_lanes = path
                self.generate_path_points() # creates a list of waypoints in the path

            for next_lanelet in self.graph[current_lanelet]['nextLanes']:
                if next_lanelet not in visited:
                    visited.add(next_lanelet)
                    queue.append((next_lanelet, path + [next_lanelet]))
                    for next_adj in self.graph[next_lanelet]['adjacentLanes']:
                        if next_adj not in visited:
                            visited.add(next_adj)
                            queue.append((next_adj, path + [next_adj]))
        
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

    def update_observation_range(self, speed, is_speed_declining):
        self.lookahead_distance = speed * self.lookahead_distance_C + self.lookahead_distance_B # meters
        gain = self.range_low_pass_gain if is_speed_declining else 0
        self.on_path_detection_range = (1 - gain) * (speed * self.on_path_detection_range_C + self.on_path_detection_range_B) + gain * self.on_path_detection_range 
        self.reaction_range = (1 - gain) * (speed * self.prediction_reaction_range_C + self.prediction_reaction_range_B) + gain * self.reaction_range # meters
        self.detection_range = (1 - gain) * (speed * self.prediction_detection_range_C + self.prediction_detection_range_B) + gain * self.detection_range # meters

    def local_planning(self, search_area):
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
        return look_ahead_point_index, look_ahead_point, current_closest_point_to_vehicle_index, isTurnDetected, target_speed
    
    def get_traffic_light_color_by_id(self, traffic_light_id):
        v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
        v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)
        if traffic_light_id in v2i_traffic_signals_id:
            self.opposite_traffic_light_last_Color = v2i_traffic_signals_colors[v2i_traffic_signals_id.index(traffic_light_id)]
        return self.opposite_traffic_light_last_Color

    def get_traffic_light_color_by_lane(self, lane):
        lane_obj = self.find_lane_by_name(lane)
        current_lane_traffic_light_id = lane_obj['trafficlightsWayIDs']
        v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
        if current_lane_traffic_light_id and current_lane_traffic_light_id[0] in v2i_traffic_signals_id:
            v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)
            return v2i_traffic_signals_colors[v2i_traffic_signals_id.index(current_lane_traffic_light_id[0])]
        return None

    def get_traffic_light_stop_point_by_lane(self, lane):
        lane_obj = self.find_lane_by_name(lane)
        stop_point = self.calculate_traffic_light_stop_point(lane_obj['stopLinePoseP1'], lane_obj['stopLinePoseP2'])
        return stop_point

    def manage_traffic_lights(self):
        v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
        v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)

        current_lane = self.route[self.current_lane_index]
        lane_obj = self.find_lane_by_name(current_lane)
        current_lane_traffic_light_id = lane_obj['trafficlightsWayIDs']
        if current_lane_traffic_light_id: # this lane have a traffic light
            if current_lane_traffic_light_id[0] in v2i_traffic_signals_id: # traffic light id is on the list
                color = v2i_traffic_signals_colors[v2i_traffic_signals_id.index(current_lane_traffic_light_id[0])]
                stop_point = self.get_traffic_light_stop_point_by_lane(current_lane)
                self.traffic_light_stopPoint_lastState = stop_point
                if color == 1 or color == 2:
                    self.traffic_light_state_lastState = 'Stop_red'
                    return 'Stop_red', stop_point
                self.traffic_light_state_lastState = 'Cruise_green'
                return 'Cruise_green', None
            else:
                if self.traffic_light_state_lastState == 'Stop_red':
                    return 'Stop_red', self.traffic_light_stopPoint_lastState
                return 'Cruise_green', None

        # self.get_logger().info(f"Traffic light Not detected on {lane_obj['name']}")
        return 'Cruise',  None
        

    def get_detected_objects_in_front(self):
        if not self.detectedObjects:
            self.get_logger().warning("No Perception / no object detected!")
            return None

        objects_ahead = []
        for obj in self.detectedObjects.objects:
            object_direction = obj.relative_direction.data
            # if object_direction == 'above' or object_direction == 'NW' or object_direction == 'NE' or object_direction == 'SE' or object_direction == 'SW':
            if object_direction == 'above' or object_direction == 'NW' or object_direction == 'NE':
                objects_ahead.append(obj)
        print("Number of Detected Objects in front: ", len(objects_ahead))
        return objects_ahead
        
    def get_objects_in_range(self, objects_ahead, filter_dist):
        if not objects_ahead:
            print("No Object ahead")
            return None            
        objects_in_range = []
        for obj in objects_ahead:
            if obj.distance <= filter_dist: objects_in_range.append(obj)

        print("Number of Detected Objects in detection radious: ", len(objects_in_range))
        return objects_in_range
    
    def apply_quaternion_rotation(self, quaternion, vector):
        """
        Applies a quaternion rotation to a given vector.
        """
        rotation = R.from_quat(np.array([quaternion.x, quaternion.y, quaternion.z, quaternion.w]))
        transformed_vector = rotation.apply(np.array([vector.x, vector.y, vector.z]))
        return Point(x=transformed_vector[0], y=transformed_vector[1], z=transformed_vector[2])

    def get_object_absolute_position(self, vehicle_orientation, vehicle_pose, vector):
        """
        Converts an object's relative position back to its absolute position using the vehicle's pose.
        """
        # Apply the quaternion rotation (forward rotation)
        rotated_vector = self.apply_quaternion_rotation(vehicle_orientation, vector)

        # Add the rotated vector to the vehicle's position
        obj_x = vehicle_pose['x'] + rotated_vector.x
        obj_y = vehicle_pose['y'] + rotated_vector.y
        obj_z = vehicle_pose['z'] + rotated_vector.z

        # Create the absolute position
        object_absolute_pose = Point(x=obj_x, y=obj_y, z=obj_z)
        return object_absolute_pose
    
    def find_obstacle_on_path(self, objects_in_range, current_closest_point_to_vehicle_index, vehicle_pose):
        objects_on_path = []
        objects_absulute_positions = [self.get_object_absolute_position(self.pose.pose.orientation, vehicle_pose, obj.position) for obj in objects_in_range]
        waypoints = self.path[current_closest_point_to_vehicle_index:current_closest_point_to_vehicle_index + int(self.on_path_detection_range / self.densify_interval) + 1]
        print("CC - waypoints size: ", len(waypoints))
        for i in range(len(objects_in_range)):
            print(f'Object {i}')
            for waypoint in waypoints:
                object_pose = {'x': objects_absulute_positions[i].x, 'y': objects_absulute_positions[i].y, 'z': objects_absulute_positions[i].z}
                dist = self.calculate_distance(object_pose, waypoint)
                if dist <= self.densify_interval*1.4:
                    print("CC - DEBUG collison avoidance object dist to waypoint: ", dist)
                    objects_on_path.append({"object": objects_in_range[i], "waypoint": waypoint})
                    break
        
        # If no objects are on the path
        if not objects_on_path:
            return None
        
        # If only one object is on the path
        if len(objects_on_path) == 1:
            print("One object on list")
            return objects_on_path[0]
        
        # Find the closest object on the path
        print("several object on list")
        min_dist = float('inf')
        closest_object_info = None
        for object_on_path in objects_on_path:
            dist = self.calculate_distance(vehicle_pose, object_on_path['waypoint'])
            if dist < min_dist:
                closest_object_info = object_on_path
                min_dist = dist
        
        return closest_object_info
    
    def calculate_traffic_light_stop_point(self, p1, p2):
        return Point(x=(p1[0] + p2[0])/2, y=(p1[1] + p2[1])/2, z=(p1[2] + p2[2])/2)
    
    
    def find_intersection(self, object_pose, object_forward_vector, waypoint1, waypoint2):
        # Extract components
        x1, y1 = object_pose.x, object_pose.y
        a1, b1 = object_forward_vector
        x2, y2 = waypoint1['x'], waypoint1['y']
        x3, y3 = waypoint2['x'], waypoint2['y']

        # Direction vector of Line 2 (waypoints)
        a2 = x3 - x2
        b2 = y3 - y2

        # Equation of Line 1 (object path): y - y1 = m1 * (x - x1)
        # m1 = b1 / a1 (from vector)
        m1 = b1 / a1 if a1 != 0 else float('inf')  # Handle vertical line case

        # Equation of Line 2: y - y2 = m2 * (x - x2)
        m2 = b2 / a2 if a2 != 0 else float('inf')  # Handle vertical line case

        # Handle the vertical lines (infinite slope)
        if m1 == m2:
            self.get_logger().error("Parallel lines")
            return None  # Parallel vertical lines
        elif m1 == float('inf'):  # Line 1 is vertical
            x = x1
            y = m2 * (x - x2) + y2
        elif m2 == float('inf'):  # Line 2 is vertical
            x = x2
            y = m1 * (x - x1) + y1
        else:  # Neither line is vertical
            x = (y2 - y1 + m1 * x1 - m2 * x2) / (m1 - m2)
            y = m1 * (x - x1) + y1
        return (x, y)

    def dot_product(self, v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]

    def is_point_on_segment(self, object_pose, intersection, waypoint1, waypoint2, forward_vector):
        # Unpack the intersection point and the waypoints
        x, y = intersection
        x1, y1 = waypoint1['x'], waypoint1['y']
        x2, y2 = waypoint2['x'], waypoint2['y']
        x3, y3 = object_pose.x, object_pose.y

        object_to_intersect_vector = [x-x3, y-y3]
        # Check if the intersection point is within the bounds of the segment
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            if self.dot_product(object_to_intersect_vector, forward_vector) >= 0:
                return True  # Intersection point is on the segment
        return False  # Intersection point is outside the segment
        
    def get_forward_vector(self, quaternion):
        local_forward = np.array([1, 0, 0])
        # Convert the quaternion to a rotation object
        rotation = R.from_quat(np.array([quaternion.x, quaternion.y, quaternion.z, quaternion.w]))  # Quaternion format: [x, y, z, w]
        # Apply the rotation to the local forward vector
        global_forward = rotation.apply(local_forward)
        return global_forward [:2]
    
    def get_time_to_collison(self, current_pose, collision_point, speed):
        if speed == 0.0:
            return float('inf')  # Return infinity to indicate no collision
        dist = self.calculate_distance({'x': collision_point.x, 'y': collision_point.y}, current_pose)
        time_to_collision = dist / speed
        time_to_collision = time_to_collision * self.sim_clock_rate
        print(f"P - dist: {dist}, speed: {speed}, time: {time_to_collision}")
        return time_to_collision

    def will_clooide_on_path(self, object_type, object_speed, object_pose, vehicle_pose, collison_point, corresponding_waypoint):
        print("---------------------")
        current_vehicle_speed = self.velocity_report.longitudinal_velocity if self.velocity_report else 0.0   
        t_vehicle = self.get_time_to_collison(vehicle_pose, collison_point, current_vehicle_speed)
        t_object = self.get_time_to_collison({'x': object_pose.x,'y': object_pose.y}, collison_point, object_speed)
        time_difference = abs(t_vehicle - t_object)
        dist_to_waypoint = self.calculate_distance(corresponding_waypoint, vehicle_pose)
        print(f"D - time_difference {time_difference}, dist to waypoint {dist_to_waypoint} current_vehicle_speed {current_vehicle_speed}")
        if time_difference <= self.reaction_time_threshold:
            self.get_logger().warning(f"P - Vehciel mooving - Potential collision detected! Time difference: {time_difference:.2f} seconds.")
            return True
        elif current_vehicle_speed <= 0.5 and t_object <= self.reaction_time_threshold and dist_to_waypoint <= self.saftey_distance:
            self.get_logger().warning(f"P - Vehciel stopping - Potential collision detected! Time difference: {time_difference:.2f} seconds.")
            return True
        else:
            print(f"P - Safe to proceed. Time difference: {time_difference:.2f} seconds.")
            return False
    
    def get_stop_point_by_safety_distance(self, waypoint, vehicle_pose):
        # Helper function to calculate distances
        dist_to_waypoint = self.calculate_distance(waypoint, vehicle_pose)
        print("CC - vehicle distance to waypoint: ", dist_to_waypoint)
        if dist_to_waypoint <= self.saftey_distance: # Stop the vehicle if distance to the object is less that safety distance
            return Point(x=vehicle_pose['x'], y=vehicle_pose['y'], z=vehicle_pose['z'])

        stop_point_index = self.path.index(waypoint) - int(self.saftey_distance/self.densify_interval)
        print('CC - stop point index on path: ', stop_point_index)
        stop_point = self.path[stop_point_index]
        return Point(x=stop_point['x'], y=stop_point['y'], z=stop_point['z'])
         

    def on_path_collision_avoidance(self, objects_ahead, current_closest_point_to_vehicle_index, vehicle_pose):
        print("CC - on path detection range: ", self.on_path_detection_range)
        objects_in_range = self.get_objects_in_range(objects_ahead, self.on_path_detection_range)
        if not objects_in_range:
            return None
        closest_object_info = self.find_obstacle_on_path(objects_in_range, current_closest_point_to_vehicle_index, vehicle_pose)
        # return False, None, 'Cruise'
        if not closest_object_info:
            self.get_logger().info("No Immediate danger")
            return None
        self.get_logger().info("Imediate threat. Objects ahead in danger zone")
        return self.get_stop_point_by_safety_distance(closest_object_info['waypoint'], vehicle_pose)
    
    def collison_prediction(self, objects_ahead, current_closest_point_to_vehicle_index, vehicle_pose):
        objects_in_range = self.get_objects_in_range(objects_ahead, self.detection_range)
        if not objects_in_range:
            return None
        
        objects_absulute_positions = [self.get_object_absolute_position(self.pose.pose.orientation, vehicle_pose, obj.position) for obj in objects_in_range]
        waypoints = self.path[current_closest_point_to_vehicle_index:current_closest_point_to_vehicle_index + int(self.reaction_range / self.densify_interval) + 1]
        # print(f"waypoints segment {len(waypoints)}")
        predicted_stop_points = []
        if self.get_traffic_light_color_by_id(166893) != 1:
            self.get_logger().warning(f"Traffic light enemy: {self.get_traffic_light_color_by_id(166893)}")
            for i in range(len(objects_in_range)):
                print(f"P - object {i}")
                dist_to_veh = self.calculate_distance(vehicle_pose, {'x': objects_absulute_positions[i].x,'y': objects_absulute_positions[i].y})
                for j in range(len(waypoints) - 1):
                    # print(f"P - object {i}, type: {objects_in_range[i].label}, dist: {dist_to_veh} - Waypoint {j}, {j+1}")
                    forward_vector = self.get_forward_vector(objects_in_range[i].orientation)
                    collison_point = self.find_intersection(objects_absulute_positions[i], forward_vector, waypoints[j], waypoints[j+1])
                    if collison_point:
                        # print(f"P - collision point founded")
                        if self.is_point_on_segment(objects_absulute_positions[i], collison_point, waypoints[j], waypoints[j+1], forward_vector):
                            # print(f"P - collision point is on segment")
                            collison_point = Point(x=collison_point[0], y=collison_point[1], z=waypoints[j]['z'])
                            # print(f'P - CollisonPoint found on: {collison_point.x, collison_point.y}')
                            # print(f'P - corresponding waypoint:  {waypoints[j]}')
                            if self.will_clooide_on_path(objects_in_range[i].label, objects_in_range[i].velocity, objects_absulute_positions[i], vehicle_pose, collison_point, waypoints[j]):
                                stop_point = self.get_stop_point_by_safety_distance(waypoints[j], vehicle_pose)
                                predicted_stop_points.append(stop_point)
                                break
        return predicted_stop_points
    
    def find_closest_stop_point(self, traffic_light_stopPoint, on_path_collision_avoidance_stopPoint, predicted_collisons_stopPoints, destination_stopPoint, vehicle_pose):
        # Create a dictionary for stop points
        stop_points = {}
        
        if traffic_light_stopPoint:
            stop_points[id(traffic_light_stopPoint)] = ('TrafficLight', traffic_light_stopPoint)
        if on_path_collision_avoidance_stopPoint:
            stop_points[id(on_path_collision_avoidance_stopPoint)] = ('CollisonAvoidance', on_path_collision_avoidance_stopPoint)
        if predicted_collisons_stopPoints:
            for point in predicted_collisons_stopPoints:
                stop_points[id(point)] = ('CollisonPrediction', point)
        if destination_stopPoint:
            stop_points[id(destination_stopPoint)] = ('Destination', destination_stopPoint)
        
        # Helper function to calculate distances
        def calculate_distance_to(point):
            return self.calculate_distance(
                vehicle_pose, 
                {'x': point.x, 'y': point.y, 'z': point.z}
            )
        
        minimum_distance = float("inf")
        closest_stop_point = None
        stop_point_type = None
        
        for _, (type, stop_point) in stop_points.items():
            dist = calculate_distance_to(stop_point)
            # print("DEBUG stop point selection: ", type, stop_point)
            if dist <= minimum_distance:
                minimum_distance = dist
                closest_stop_point = stop_point
                stop_point_type = type
        
        print(f'CC - closest stop point: {closest_stop_point}')
        print(f'CC - closest stop point type {stop_point_type}')
        print(f'CC - distance to stop point: {minimum_distance}')
        return closest_stop_point, stop_point_type


    def behavioral_planning(self, look_ahead_point, look_ahead_point_index, current_closest_point_to_vehicle_index, isTurnDetected):
        # Current vehicle position
        vehicle_pose = {
            'x': self.pose.pose.position.x,
            'y': self.pose.pose.position.y,
            'z': self.pose.pose.position.z
        }
        
        # Distance to the destination
        distance_to_destination = self.calculate_distance(
            vehicle_pose, 
            {'x': self.destination.x, 'y': self.destination.y, 'z': self.destination.z}
        )
        
        # Traffic light detection
        trafficLightTask, traffic_light_stopPoint = self.manage_traffic_lights()
        # Collision avoidance
        objects_ahead = self.get_detected_objects_in_front()
        on_path_collision_avoidance_stopPoint = self.on_path_collision_avoidance(objects_ahead, current_closest_point_to_vehicle_index, vehicle_pose)
        # predicted_collisons_stopPoints = self.collison_prediction(objects_ahead, current_closest_point_to_vehicle_index, vehicle_pose)
        predicted_collisons_stopPoints = []
        # if predicted_collisons_stopPoints:
        #     predicted_collisons_stopPoints = []
            # predicted_collisons_stopPoints.append(self.get_traffic_light_stop_point_by_lane('lanelet871'))
        
        stop_point, stop_point_type = self.find_closest_stop_point(traffic_light_stopPoint, on_path_collision_avoidance_stopPoint, predicted_collisons_stopPoints, self.destination, vehicle_pose)
        
        self.status.data = 'Cruise'

        if isTurnDetected:
            self.get_logger().info("Turn detected")
            self.status.data = 'Turn'
        
        if stop_point_type == 'CollisonAvoidance' or stop_point_type == 'CollisonPrediction':
            if stop_point_type == 'CollisonAvoidance':
                self.get_logger().warning('CC Collison Avoidance')
            else:
                self.get_logger().warning('Prediction')
            self.status.data = 'Decelerate'
        
        if stop_point_type == 'TrafficLight':
            self.get_logger().warning('TrafficLight')
            self.status.data = trafficLightTask
         
        if (distance_to_destination <= self.reaction_range and 
            look_ahead_point_index > len(self.path) - (self.reaction_range / self.densify_interval + 1)):
            self.get_logger().info("Approaching destination, decelerating.")
            self.status.data = 'Decelerate'
        
        return stop_point

           

    def mission_planning(self, start_lanelet_respawn=None):
        """
        Perform global path planning to create a path from the current location to the destination.
        """
        if self.location:
            self.get_logger().info("path planning")
            self.start_lanelet = self.location.closest_lane_names.data
            if start_lanelet_respawn:
                self.start_lanelet = start_lanelet_respawn
            self.bfs(self.start_lanelet, self.dest_lanelet) # Creates the path
            print(self.path_as_lanes)
            if self.path and self.path_as_lanes:
                self.destination = Point(x=self.path[-1]['x'], y=self.path[-1]['y'], z=self.path[-1]['z'])
                path_curve_detector = PathCurveDetector(self.path, angle_threshold=3) # initializing object from class
                self.curves = path_curve_detector.find_curves_in_path() # locating curves on the route/path
            if self.path and self.path_as_lanes and self.curves:
                print("path of lanes: ", self.path_as_lanes)
                # self.initial_lane = self.location.closest_lane_names.data
                self.route = self.path_as_lanes[:]
                self.current_lane_index = 0
                self.isPathPlanned = True
            

    def publish_planning_msgs(self, look_ahead_point, stop_point, speed):
        lookahead_point = LookAheadMsg()
        lookahead_point.look_ahead_point = Point(x=look_ahead_point['x'], y=look_ahead_point['y'], z=look_ahead_point['z'])
        lookahead_point.stop_point = stop_point
        lookahead_point.status = self.status
        lookahead_point.speed_limit = speed
        self.planning_publisher.publish(lookahead_point)
  
    def planning(self):
        """
        Main planning function to decide between global and local planning.
        """
        if not self.isPathPlanned:
            self.get_logger().info("Misson planning")
            self.mission_planning()  # generates the path and dencifies it.
            return
        
        if not self.location and not self.pose:
            self.get_logger().warning("No location/pose input")
            return None
        
        if self.finished:
            self.status.data = 'Park'
            self.node_shut = True
            self.publish_planning_msgs(None, None, 0) # publishing
            return
    
        if self.reset:
            self.get_logger().error("RESET")
            # self.isPathPlanned = False
            self.get_logger().info("Misson planning")
            print("DEBUG - start_lanelet_respawn: ", self.start_lanelet)
            self.mission_planning(self.start_lanelet)  # generates the path and dencifies it.
        
        self.current_speed = self.velocity_report.longitudinal_velocity if self.velocity_report else 0.0
        self.update_observation_range(self.current_speed, self.current_speed < self.previous_speed_slidingWindow[0])


        search_area, search_area_as_lanes = self.create_search_area()
        look_ahead_point_index, look_ahead_point, current_closest_point_to_vehicle_index, isTurnDetected, speed = self.local_planning(search_area)
        if not look_ahead_point and not look_ahead_point_index:
            self.get_logger().warning("Lookahead point not set in local planning")
            return
        
        stop_point = self.behavioral_planning(look_ahead_point, look_ahead_point_index, current_closest_point_to_vehicle_index, isTurnDetected)
        
        self.publish_planning_msgs(look_ahead_point, stop_point, speed) # publishing
        
        self.get_logger().info(
            f'planning\n'
            f'lookahead distance:  {self.lookahead_distance}\n'
            f'is turn detected: {isTurnDetected}\n'
            f'speed: {speed}\n'
            f'status: {self.status.data}\n'
        )
        
        self.previous_speed_slidingWindow.append(self.current_speed)

def main(args=None):
    rclpy.init(args=args)
    node = Planning('bus')
    try:
        while rclpy.ok() and not node.node_shut:
            rclpy.spin_once(node, timeout_sec=None)# Set timeout to 0 to avoid delay
            node.planning()
    finally:
        node.destroy_node()
        rclpy.shutdown()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()