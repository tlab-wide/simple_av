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
from simple_av_msgs.msg import LocalizationMsg, LocalizationIntersectionStatus
from simple_av_msgs.msg import Portal, DetectedObjectsArray
import numpy as np
from simple_av_msgs.srv import TriggerMissionPlan
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy
from scipy.spatial.transform import Rotation as R


class BehaviorPathPlanner(Node):
    def __init__(self):
        super().__init__('behavior_path_planner_node')

        # Load scenario configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.vehicle_model = self.scenario_config['scenario']['vehicle_model']
        self.dest_lanelet = self.scenario_config['scenario']['destination']
        self.start_lanelet = None

        # Load av features configs
        self.av_features = self.config_file_loader("av_features.yaml")
        self.is_cool4_speed_profile_enable = self.av_features['cool4_speed_profile_test']['enable']
        self.is_RSU_enabled = self.av_features['object_detection']['use_rsu']

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

        # Load Vehicle configs
        self.vehicle_config = self.load_vehicle_config(self.vehicle_model)

        self.NORMAL_ACCEL = self.vehicle_config['performance']['acceleration_rate']
        self.NORMAL_DECEL = self.vehicle_config['performance']['normal_deceleration_rate']

        self.MAX_SPEED = self.vehicle_config['performance']['max_speed']
        self.MIN_SPEED = self.vehicle_config['performance']['min_speed']
        self.MIDDLE_SPEED = self.vehicle_config['performance']['middle_speed']

        # Load intersection data
        self.intersection_profiles = self.load_intersections()
        self.intersection_points = self.intersection_profiles['intersection_points']
        self.intersection2_scenario2_points = self.intersection_profiles['intersection_points']['2']['2']
        # Load YAML sidewalk data
        self.layout_data = self.load_intersection_layout()

        # Create subscriber to simple_av/localization/intersection_status topic
        self.subscriptionIntersectionAwareness = self.create_subscription(LocalizationIntersectionStatus, 'simple_av/localization/intersection_status', self.intersectionAwareness_callback, 10)
        self.intersection_awareness_intersection_name = None
        self.intersection_awareness_status = None

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

        self.subscriptionDetectedObjects = self.create_subscription(DetectedObjectsArray, 'simple_av/perception/detected_objects', self.detectedObjects_callback, 10)
        self.detectedObjects = DetectedObjectsArray()

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
    
    def load_intersections(self):
        package_share_directory = get_package_share_directory('common')
        zones_path = os.path.join(package_share_directory, "zones", 'intersection_profiles.yaml')

        with open(zones_path, "r") as file:
            intersection_profiles = yaml.safe_load(file)
        return intersection_profiles
    
    def load_vehicle_config(self, vehicle_model):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", "vehicle_config.yaml")

        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        # Retrieve the specific vehicle's configuration
        if vehicle_model in config["vehicles"]:
            return config["vehicles"][vehicle_model]
        else:
            raise ValueError(f"Vehicle type '{vehicle_model}' not found in the configuration.")
        
    # ---- parse into structured sidewalks ----
    def load_intersection_layout(self):
        package_share_directory = get_package_share_directory('common')
        intersections_danger_zones_path = os.path.join(package_share_directory, "zones", 'intersections_danger_zones.yaml')

        try:
            with open(intersections_danger_zones_path, 'r') as f:
                intersections_danger_zones = yaml.safe_load(f)
            self.get_logger().info("YAML file loaded successfully.")
        except Exception as e:
            self.get_logger().error(f"Failed to load YAML file: {e}")
            intersections_danger_zones = None

        return intersections_danger_zones

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
    
    def detectedObjects_callback(self, msg):
        self.detectedObjects = msg

    def intersectionAwareness_callback(self, msg):
        self.intersection_awareness_intersection_name = msg.intersection_name
        self.intersection_awareness_status = msg.status

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
        lookahead_point_index = self.get_lookahead_distance_as_index() + current_closest_point_index
        if lookahead_point_index >= path_size - 2:
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
                search_area.append(Point(x=waypoint['x'], y=waypoint['y'], z=waypoint['z']))
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

    def simple_av_speed_profile_maker(self, path, waypoint_distance=2.0):
        """
        Generate smooth, physically constrained speed profile.
        Vehicle starts at 0 and stops at the last waypoint.
        Enforces acceleration and deceleration limits and minimum speed.
        """

        _NORMAL_ACCEL = (self.NORMAL_ACCEL - 0.1) * waypoint_distance
        _NORMAL_DECEL = abs(self.NORMAL_DECEL) * waypoint_distance

        # 1. Base speeds from curvature
        base_speeds = []
        for i, waypoint in enumerate(path):
            speed = self.adjust_speed_to_curve(waypoint.curve)
            base_speeds.append(speed)

        # 2. Forward pass (acceleration constraint)
        speeds = [0.0]  # Start from speed 0
        for i in range(1, len(base_speeds)):
            prev_speed = speeds[-1]
            # Max speed allowed by acceleration
            max_next_speed = math.sqrt(prev_speed**2 + 2 * _NORMAL_ACCEL * waypoint_distance)
            # Clamp by curvature and max speed
            speeds.append(min(base_speeds[i], max_next_speed, self.MAX_SPEED))

        # 3. Backward pass (deceleration constraint)
        speeds[-1] = 0.0  # Ensure full stop at the end
        for i in reversed(range(len(speeds) - 1)):
            next_speed = speeds[i + 1]
            # Max speed allowed by deceleration to reach next point safely
            max_prev_speed = math.sqrt(next_speed**2 + 2 * _NORMAL_DECEL * waypoint_distance)
            speeds[i] = min(speeds[i], max_prev_speed, self.MAX_SPEED)

        # 4. Clamp to MIN_SPEED (except first and last points)
        for i in range(1, len(speeds)-1):
            speeds[i] = max(speeds[i], self.MIN_SPEED)

        return speeds
    
    
    def get_detected_pedestrians(self):
        if not self.detectedObjects:
            self.get_logger().warning("No Perception / no object detected!")
            return None

        detected_pedestrians = []
        for obj in self.detectedObjects.objects:
            object_type = obj.label
            if object_type == '7' or object_type == '2':
                detected_pedestrians.append(obj)
        return detected_pedestrians

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
        obj_x = vehicle_pose.x + rotated_vector.x
        obj_y = vehicle_pose.y + rotated_vector.y
        obj_z = vehicle_pose.z + rotated_vector.z

        # Create the absolute position
        object_absolute_pose = Point(x=obj_x, y=obj_y, z=obj_z)
        return object_absolute_pose

    def is_point_in_polygon(self, point, polygon_points):
        """
        Check if a 2D point is inside a polygon (ray casting algorithm).
        polygon_points: list of [x, y, z]
        """
        x, y = point.x, point.y
        inside = False
        n = len(polygon_points)
        p1x, p1y = polygon_points[0][0], polygon_points[0][1]
        for i in range(n + 1):
            p2x, p2y = polygon_points[i % n][0], polygon_points[i % n][1]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def is_object_detected_on_intersection_danger_zones(self, intersection_name):
        vehicle_pose = self.pose.pose.position
        self.get_logger().debug("Checking intersection danger zones...")
        detected_pedestrians = self.get_detected_pedestrians()
        if not detected_pedestrians:
            return False

        intersection = self.layout_data["intersections"].get(str(intersection_name))
        if not intersection:
            self.get_logger().warning(f"No intersection data for {intersection_name}")
            return False

        objects_in_zones = 0
        for ped in detected_pedestrians:
            ped_abs = self.get_object_absolute_position(vehicle_pose, ped)
            for zone_name, zone_data in intersection.items():
                polygon = zone_data["points"]
                if self.is_point_in_polygon(ped_abs, polygon):
                    objects_in_zones += 1
                    self.get_logger().info(
                        f"Pedestrian detected in {zone_name} of intersection {intersection_name}"
                    )

        self.get_logger().info(f"Total pedestrians in danger zones: {objects_in_zones}")
        return objects_in_zones > 0


    def cool4_speed_profile_adjustment(self, cool4_adjusted_speed_profile, intersection_points,  waypoint_distance=2.0):
        start_idx, exit_idx, end_idx = intersection_points
        is_object_in_danger_zone = self.is_object_detected_on_intersection_danger_zones('2')

        print(f"is_RSU_enabled: {self.is_RSU_enabled}, Danger:{is_object_in_danger_zone}")
        if self.is_RSU_enabled and not is_object_in_danger_zone:
                print("DEBUG: RSU enabled, Danger false continue the curve with 12KM/H")
                # Case 1: RSU active and no danger → keep moderate constant speed
                cool4_adjusted_speed_profile[start_idx:exit_idx] = [self.MIDDLE_SPEED] * (exit_idx - start_idx)

                # accelerate again from MIN_SPEED to MAX_SPEED after intersection
                n_points_after = end_idx - exit_idx
                if n_points_after > 0:
                    accel_profile = []
                    v = self.MIDDLE_SPEED
                    accel_profile.append(v)  # include initial speed
                    for _ in range(1, n_points_after):
                        v = min(self.MAX_SPEED, math.sqrt(v**2 + 2 * self.NORMAL_ACCEL * waypoint_distance))
                        accel_profile.append(v)
                    cool4_adjusted_speed_profile[exit_idx:end_idx] = accel_profile

        elif (self.is_RSU_enabled and is_object_in_danger_zone) or (not self.is_RSU_enabled):
            print("DEBUG: RSU enabled/Disable, Danger TRUE or  continue the curve with 12KM/H->3KM/H")
            # Case 2: RSU is_object_in_danger_zone OR no RSU → decelerate gradually from MIDDLE_SPEED → MIN_SPEED
            n_points = exit_idx - start_idx
            if n_points > 0:
                decel_profile = []
                v = self.MIDDLE_SPEED
                for _ in range(n_points):
                    v = max(self.MIN_SPEED, math.sqrt(max(v**2 - 2 * self.NORMAL_DECEL * waypoint_distance, 0)))
                    decel_profile.append(v)
                cool4_adjusted_speed_profile[start_idx:exit_idx] = decel_profile

            # accelerate again from MIN_SPEED to MAX_SPEED after intersection
            n_points_after = end_idx - exit_idx
            if n_points_after > 0:
                accel_profile = []
                v = self.MIN_SPEED
                accel_profile.append(v)  # include initial speed
                for _ in range(1, n_points_after):
                    v = min(self.MAX_SPEED, math.sqrt(v**2 + 2 * self.NORMAL_ACCEL * waypoint_distance))
                    accel_profile.append(v)
                cool4_adjusted_speed_profile[exit_idx:end_idx] = accel_profile


        return cool4_adjusted_speed_profile

    def find_intersection_start_and_exit_using_config(self, path):
        intersection_start_point_idx = -1
        intersection_exit_point_idx = -1
        intersection_end_point_idx = -1
        has_found_on_path = False
        points = {}

        points = self.intersection2_scenario2_points

        for i, waypoint in enumerate(path):
            wp = waypoint.waypoint  # geometry_msgs/Point
            # print(f"i: {i}, waypoint: {wp}")

            if wp.x == points['1']['x'] and wp.y == points['1']['y'] and wp.z == points['1']['z']:
                intersection_start_point_idx = i
            if wp.x == points['2']['x'] and wp.y == points['2']['y'] and wp.z == points['2']['z']:
                intersection_exit_point_idx = i
            if '3' in points and wp.x == points['3']['x'] and wp.y == points['3']['y'] and wp.z == points['3']['z']:
                intersection_end_point_idx = i

        if intersection_start_point_idx != -1 and intersection_exit_point_idx != -1 and intersection_end_point_idx != -1:
            has_found_on_path = True

        return has_found_on_path, [intersection_start_point_idx, intersection_exit_point_idx, intersection_end_point_idx]

    def speed_profile_maker(self, path):

        speed_profile_base = self.simple_av_speed_profile_maker(path)

        
        if self.is_cool4_speed_profile_enable:
            has_found_on_path, intersection_points = self.find_intersection_start_and_exit_using_config(path)
            print(f"DEBUG - speed profile: has_found_on_path: {has_found_on_path}, indexes: {intersection_points}")
            if has_found_on_path:
                cool4_adjusted_speed_profile = self.cool4_speed_profile_adjustment(speed_profile_base, intersection_points)
                return cool4_adjusted_speed_profile
    
        return speed_profile_base

    def handle_mission_plan(self):

        if self.path and self.path_as_lanes:
            self.destination = self.path[-1].waypoint
            self.speeds_on_path = self.speed_profile_maker(self.path)
            
            for i, waypoint in enumerate(self.path):
                self.path_of_waypoints.append(waypoint.waypoint)

            self.route = self.path_as_lanes[:]
            self.current_lane_index = 0
            self.isPathPlanned = True

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
            rclpy.spin_once(self, timeout_sec=0.2)  # allow 0.25s to receive mission plan
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
            self.prev_lookahead_index = 0
            self.current_lane_index = 0
            return
        
        if not self.path and not self.path_as_lanes:
            self.get_logger().warning("Path has not initialized from Mission Planner!!")
            return
        
        vehicle_pose = self.pose.pose.position
        if vehicle_pose.x == 0.0 and vehicle_pose.y == 0.0 and vehicle_pose.z == 0.0:
            self.get_logger().warning("Vehicle Pose is not accessible")
            return
            
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
            f'lookahead point index:  {look_ahead_point_index} {self.prev_lookahead_index}\n'
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