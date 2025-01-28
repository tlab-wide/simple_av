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
from simple_av_msgs.msg import LookAheadMsg
from v2x_msgs.msg import CooperativeSignalsMessage
import numpy as np
from simple_av_msgs.msg import TrafficSignalsArray, DetectedObjectsArray, DetectedObject
from scipy.spatial.transform import Rotation as R

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
        
        self.vehicle_type = vehicle_type
        self.vehicle_config = self.load_vehicle_config(vehicle_type)
        
        # Load the Json map
        self.map_data = self.load_map_data()
        self.map_data = self.map_data["LaneLetsArray"]

        self.graph = {lanelet['name']: {
            'waypoints': lanelet['waypoints'],
            'nextLanes': lanelet.get('nextLanes', []),
            'prevLanes': lanelet.get('prevLanes', []),
            'adjacentLanes': lanelet.get('adjacentLanes', []),
        } for lanelet in self.map_data}

        # Create subscriber to 'simple_av/perception/traffic_signals' topic /v2x/traffic_signals1
        self.subscriptionTrafficSignal = self.create_subscription(TrafficSignalsArray, 'simple_av/perception/traffic_signals', self.trafficSignal_callback, 10)

        # Create subscriber to 'simple_av/perception/detected_objects' topic
        self.subscriptionDetectedObjects = self.create_subscription(DetectedObjectsArray, 'simple_av/perception/detected_objects', self.detectedObjects_callback, 10)

        # Create subscriber to /sensing/gnss/pose topic
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)

        # Create subscriber to /localization/location topic
        self.subscriptionLocation = self.create_subscription(LocalizationMsg, 'simple_av/localization/location', self.location_callback, 10)

        # Create subscriber to simple_av/portal topic
        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False

        # Initialize the publisher
        ## TODO: rename the lookahead_point topic to planned_route
        self.planning_publisher = self.create_publisher(LookAheadMsg, 'simple_av/planning/lookahead_point', 10)

        self.pose = PoseStamped()  # Initialize pose
        self.location = LocalizationMsg()  # Initialize location
        self.trafficSignal = TrafficSignalsArray() # Initialize traffic signal
        self.detectedObjects = DetectedObjectsArray() # Initialize traffic signal

        self.isPathPlanned = False  # Flag to check if the path has been planned
        self.path_as_lanes = None  # List of lanes from start lane to destination
        self.path = None  # List of waypoints in order of path_as_lanes
        self.route = None # List of lanes from start lane to destination
        self.current_lane_index = 0
        
        self.base_speed = self.vehicle_config['base_speed'] # m/s
        self.max_speed = self.vehicle_config['max_speed'] # m/s
        self.turning_speed = self.vehicle_config['turning_speed'] # m/s
        self.lookahead_distance = self.base_speed * 2.0 + 3.0 # meters
        self.reaction_distance = self.base_speed * 5.0 + 5.25 # meters
        self.detection_radius = self.base_speed * 6.0 + 8.0 # meters
        self.status = String() # Cruise, Decelerate, PrepareToStop, Turn
        self.vehicle_length = self.vehicle_config['dimensions']['length'] #meters
        self.vehicle_width = self.vehicle_config['dimensions']['width'] #meters
        self.curves = None

        # self.saftey_distance = 2.0 + self.vehicle_length/2 #meters
        self.saftey_distance = 2.0 #meters
        
        self.isCurveFinished = False
        self.isCurveStarted = False
        self.curve_angle = 0.0
        
        self.densify_interval = 2.0 # meters
        
        self.initial_lane = None
        self.search_depth = 5

        self.curve_finish_point = None

        self.destination = Point()
        self.traffic_light_stopPoint_lastState = Point()
        self.traffic_light_state_lastState = 'Cruise_green'
        self.traffic_light_color_lastState = 'green'
        
        self.test_config = self.load_test_config()
        self.dest_lanelet = self.test_config['destination']

        self.node_shut = False
    
    def load_test_config(self):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('simple_av')
        config_path = os.path.join(package_share_directory, "resource", "test_config.yaml")
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
            self.get_logger().warning("Vehicle is out of the Path")
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
    
    def update_lookahead_distances(self, speed):
        self.lookahead_distance = speed * 2.0 + 2.5  # speed 7m/s: 16.5m / speed 1.75m/s: 6m
        self.reaction_distance = speed * 5.0 + 5.25  # 40m / 14m
        self.detection_radius = speed * 6.0 + 8.0  # 50m / 18.5m

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
        speed = self.update_target_speed(isTurnDetected)
        self.update_lookahead_distances(speed)

        # print("DEBUG - look ahead distance: ", self.lookahead_distance)
        return look_ahead_point_index, look_ahead_point, current_closest_point_to_vehicle_index, isTurnDetected, speed
    
    
    def manage_traffic_lights(self):
      
        v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
        v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)

        current_lane = self.route[self.current_lane_index]
        lane_obj = self.find_lane_by_name(current_lane)
        current_lane_traffic_light_id = lane_obj['trafficlightsWayIDs']
        
        if current_lane_traffic_light_id: # this lane have a traffic light
            self.get_logger().info(f"traffic light detected on {lane_obj['name']}")
            if current_lane_traffic_light_id[0] in v2i_traffic_signals_id: # traffic light id is on the list
                self.get_logger().info("GOOD SIGNAL")
                color = v2i_traffic_signals_colors[v2i_traffic_signals_id.index(current_lane_traffic_light_id[0])]
                stop_point = self.get_traffic_light_StopPoint(lane_obj['stopLinePoseP1'], lane_obj['stopLinePoseP2'])
                self.traffic_light_stopPoint_lastState = stop_point
                if color == 1 or color == 2:
                    self.traffic_light_state_lastState = 'Stop_red'
                    self.traffic_light_color_lastState = 'red'
                    return True, 'Stop_red', 'red', stop_point
                self.traffic_light_state_lastState = 'Cruise_green'
                self.traffic_light_color_lastState = 'green'
                return True, 'Cruise_green', 'green', stop_point
            else:
                self.get_logger().warning("BAD SIGNAL")
                return True, self.traffic_light_state_lastState, self.traffic_light_color_lastState, self.traffic_light_stopPoint_lastState

        self.get_logger().info(f"Traffic light Not detected on {lane_obj['name']}")
        return False, 'Cruise', 'unkown', None
        

    def get_detected_objects_in_front(self):
        if not self.detectedObjects:
            self.get_logger().warning("No Perception / no object detected!")
            return None

        objects_ahead = []
        for obj in self.detectedObjects.objects:
            object_direction = obj.relative_direction.data
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

        for i in range(len(objects_in_range)):
            for waypoint in self.path[current_closest_point_to_vehicle_index:current_closest_point_to_vehicle_index + int(self.reaction_distance / self.densify_interval) + 1]:
                object_pose = {'x': objects_absulute_positions[i].x, 'y': objects_absulute_positions[i].y, 'z': objects_absulute_positions[i].z}
                dist = self.calculate_distance(object_pose, waypoint)
                if dist <= self.densify_interval*2:
                    objects_on_path.append({"object": objects_in_range[i], "waypoint": waypoint})
                    break
        
        # If no objects are on the path
        if not objects_on_path:
            return None
        
        # If only one object is on the path
        if len(objects_on_path) == 1:
            return objects_on_path[0]
        
        # Find the closest object on the path
        min_dist = float('inf')
        closest_object_info = None
        for object_on_path in objects_on_path:
            dist = self.calculate_distance(vehicle_pose, object_on_path['waypoint'])
            if dist < min_dist:
                closest_object_info = object_on_path
                min_dist = dist
        
        return closest_object_info

    def collision_avoidance(self, objects_in_range, current_closest_point_to_vehicle_index, vehicle_pose):
        
        closest_object_info = self.find_obstacle_on_path(objects_in_range, current_closest_point_to_vehicle_index, vehicle_pose)
        # return False, None, 'Cruise'
        if not closest_object_info:
            self.get_logger().info("No Immediate danger")
            return False, None, 'Cruise'
        self.get_logger().info("Imediate threat. Objects ahead in danger zone")
        
        stop_point_index = self.path.index(closest_object_info['waypoint']) - int(closest_object_info['object'].shape.x / self.densify_interval) - 1
        # print("DEBUG - stop point index ", stop_point_index)
        stop_point = self.path[stop_point_index]
        # print("DEBUG - vehicle distance to stop point: ", self.calculate_distance(vehicle_pose, stop_point))
        stop_point = Point(x=stop_point['x'], y=stop_point['y'], z=stop_point['z'])

        task = 'Decelerate'
        return True, stop_point, task
    
    def get_traffic_light_StopPoint(self, p1, p2):
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
            self.get_logger().warning("Parallel lines")
            return None  # Parallel vertical lines
        elif m1 == float('inf'):  # Line 1 is vertical
            x = x1
            y = m2 * (x - x2) + y2
        elif m2 == float('inf'):  # Line 2 is vertical
            x = x2
            y = m1 * (x - x1) + y1
        else:  # Neither line is vertical
            # Solve the system of equations:
            # y = m1 * (x - x1) + y1
            # y = m2 * (x - x2) + y2
            # Set the two equations equal to each other
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
        # Define the local forward vector (Unity's forward is [0, 0, 1])
        local_forward = np.array([1, 0, 0])
        # Convert the quaternion to a rotation object
        rotation = R.from_quat(np.array([quaternion.x, quaternion.y, quaternion.z, quaternion.w]))  # Quaternion format: [x, y, z, w]
        # Apply the rotation to the local forward vector
        global_forward = rotation.apply(local_forward)
        return global_forward [:2]
    
    def objects_speed_info(self, object_type):
        speed = None
        if object_type == 7:
            speed = 1.0  
        
    def collison_prediction(self, objects_in_range, current_closest_point_to_vehicle_index, vehicle_pose):
        objects_absulute_positions = [self.get_object_absolute_position(self.pose.pose.orientation, vehicle_pose, obj.position) for obj in objects_in_range]
        path_to_predict = self.path[current_closest_point_to_vehicle_index:current_closest_point_to_vehicle_index + int(self.reaction_distance / self.densify_interval) + 1]
        predicted_collison_points = []
        predicted_stop_points = []
        for i in range(len(objects_in_range)):
            for j in range(len(path_to_predict) - 1):
                forward_vector = self.get_forward_vector(objects_in_range[i].orientation)
                collison_point = self.find_intersection(objects_absulute_positions[i], forward_vector, path_to_predict[j], path_to_predict[j+1])
                if collison_point:
                    if self.is_point_on_segment(objects_absulute_positions[i], collison_point, path_to_predict[j], path_to_predict[j+1], forward_vector):
                        if self.calculate_distance({'x': collison_point[0],'y': collison_point[1]}, {'x': objects_absulute_positions[i].x,'y': objects_absulute_positions[i].y}) <= 10.0:
                            collison_point = Point(x=collison_point[0], y=collison_point[1], z=path_to_predict[j]['z'])
                            predicted_collison_points.append(collison_point)
                            stop_point_index = j
                            if j >= 1:
                                stop_point_index = j - 1
                            stop_point = Point(x=path_to_predict[stop_point_index]['x'], y=path_to_predict[stop_point_index]['y'], z=path_to_predict[stop_point_index]['z'])
                            predicted_stop_points.append(stop_point)
                            break
        if predicted_stop_points:
            return True, predicted_stop_points
        return False, None
    
    def get_closest_stop_point(self, stop_points, vehicle_pose):
        # Helper function to calculate distances
        def calculate_distance_to(point):
            return self.calculate_distance(
                vehicle_pose, 
                {'x': point.x, 'y': point.y, 'z': point.z}
            )
        minimum_distance, closest_stop_point = float("inf"), None
        for stop_point in stop_points:
            dist = calculate_distance_to(stop_point)
            if dist < minimum_distance:
                minimum_distance = dist
                closest_stop_point = stop_point
        print(f'closest stop point {closest_stop_point}')
        print(f'distance to stoppoint {minimum_distance}')
        return closest_stop_point

    def behavioural_planning(self, look_ahead_point, look_ahead_point_index, current_closest_point_to_vehicle_index, isTurnDetected):
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
        
        # Manage traffic lights and collision avoidance
        # isTrafficLightDetected, vehicleTaskForTrafficLight, trafficLightColor, stop_point_for_traffic_light = self.manage_traffic_lights()
        
        objects_ahead = self.get_detected_objects_in_front()
        objects_in_range = self.get_objects_in_range(objects_ahead, self.reaction_distance)
        if objects_in_range:
            # isObjectAhead, stop_point_for_collision_avoidance, collision_task = self.collision_avoidance(objects_in_range, current_closest_point_to_vehicle_index, vehicle_pose)
            isCollisonPredicted, predicted_collison_points = self.collison_prediction(objects_in_range, current_closest_point_to_vehicle_index, vehicle_pose)
        else:
            isObjectAhead = False
            isCollisonPredicted = False

        if isCollisonPredicted:
            self.get_logger().warning("Collison predicted")
            stop_point = self.get_closest_stop_point(predicted_collison_points, vehicle_pose)
            self.status.data = 'Decelerate'
            return stop_point
        
        if (distance_to_destination <= self.reaction_distance and 
            look_ahead_point_index > len(self.path) - (self.reaction_distance / self.densify_interval + 1)):
            self.get_logger().info("Approaching destination, decelerating.")
            self.status.data = 'Decelerate'
            return self.destination
        
        # Handle turn without traffic light
        if isTurnDetected:
            self.get_logger().warning("Turn detected")
            self.status.data = 'Turn'
            return self.destination
        
        # Default behavior: cruising
        self.get_logger().info("No obstacles or turn detected. Cruising.")
        self.status.data = 'Cruise'
        return self.destination
           

    def mission_planning(self):
        """
        Perform global path planning to create a path from the current location to the destination.
        """
        if self.location:
            self.get_logger().info("path planning")
            start_lanelet = self.location.closest_lane_names.data
            self.bfs(start_lanelet, self.dest_lanelet) # Creates the path
            print(self.path_as_lanes)
            if self.path and self.path_as_lanes:
                self.destination = Point(x=self.path[-1]['x'], y=self.path[-1]['y'], z=self.path[-1]['z'])
                path_curve_detector = PathCurveDetector(self.path, angle_threshold=3) # initializing object from class
                self.curves = path_curve_detector.find_curves_in_path() # locating curves on the route/path
            if self.path and self.path_as_lanes and self.curves:
                self.isPathPlanned = True
                print("path of lanes: ", self.path_as_lanes)
                self.initial_lane = self.location.closest_lane_names.data
                self.route = self.path_as_lanes[:]
                self.current_lane_index = 0
                # print("path of lanes: ", self.path)
            

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
        else:
            if not self.location and not self.pose:
                self.get_logger().warning("No location/pose input")
                return None
            
            if self.initial_lane != self.path_as_lanes[0]:
                self.get_logger().error("Contradiction between Location initial Lane and the first Lane on the path")
                return
            
            if self.finished:
                self.status.data = 'Park'
                self.node_shut = True
                self.publish_planning_msgs(None, None, 0) # publishing
                return
        
            if self.reset:
                self.get_logger().warning("RESET")
                self.isPathPlanned = False
                return
            
            search_area, search_area_as_lanes = self.create_search_area()
            look_ahead_point_index, look_ahead_point, current_closest_point_to_vehicle_index, isTurnDetected, speed = self.local_planning(search_area)
            if not look_ahead_point and not look_ahead_point_index:
                self.get_logger().warning("Lookahead point not set in local planning")
                return
            
            stop_point = self.behavioural_planning(look_ahead_point, look_ahead_point_index, current_closest_point_to_vehicle_index, isTurnDetected)
            
            self.publish_planning_msgs(look_ahead_point, stop_point, speed) # publishing
            self.get_logger().info(
                f'planning\n'
                f'lookahead distance:  {self.lookahead_distance}\n'
                f'is turn detected: {isTurnDetected}\n'
                f'speed: {speed}\n'
                f'status: {self.status.data}\n'
            )

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