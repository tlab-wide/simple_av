#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import os
import json
import yaml
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped, Point
from std_msgs.msg import String, ColorRGBA
import math
from collections import deque
from simple_av_msgs.msg import PlanningPathPlanningMsg, PlanningInternalMsg, PlanningInternalMissionPlanMsg, PlanningWaypoint
from simple_av_msgs.msg import LocalizationMsg, LocalizationIntersectionStatus
from simple_av_msgs.msg import Portal, DetectedObjectsArray
from visualization_msgs.msg import Marker, MarkerArray
from autoware_vehicle_msgs.msg import VelocityReport
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass
from simple_av_msgs.srv import TriggerMissionPlan
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy
from scipy.spatial.transform import Rotation as R

# ---------------------------------------
#              DATACLASSES
# ---------------------------------------

@dataclass
class PolygonRegion:
    """Any polygon region from YAML (inside, sidewalks, lanes, etc.)"""
    name: str
    polygon_type: str               # 'inside', 'sw', 'lane', 'lanes'
    intersection_id: str
    polygon_id: str
    points: List[Tuple[float, float, float]]


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
        self.is_cool4_speed_profile_enable = self.av_features['use_cool4_speed_profile']['enable']
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
        self.densify_interval = self.motion_behavior_config['motion']['path']['densify_interval']
        self.max_lateral_accel = self.motion_behavior_config['motion'].get('max_lateral_accel', 4.0)

        # Load Vehicle configs
        self.vehicle_config = self.load_vehicle_config(self.vehicle_model)

        self.NORMAL_ACCEL = self.vehicle_config['performance']['acceleration_rate']
        self.NORMAL_DECEL = self.vehicle_config['performance']['normal_deceleration_rate']
        self.MAX_JERK_ACCEL = self.vehicle_config['performance'].get('max_jerk_accel', 0.7)
        self.MAX_JERK_DECEL = self.vehicle_config['performance'].get('max_jerk_decel', 0.7)
        self.ACCEL_PROFILE = self.vehicle_config['performance'].get('accel_profile', [])

        self.MAX_SPEED = self.vehicle_config['performance']['max_speed']
        self.MIN_SPEED = self.vehicle_config['performance']['min_speed']
        self.COOL4_MIN_SPEED = self.vehicle_config['performance']['cool4_min_speed']
        self.COOL4_MIDDLE_SPEED = self.vehicle_config['performance']['cool4_middle_speed']
        self.COOL4_MAX_SPEED = self.vehicle_config['performance'].get('cool4_max_speed', self.COOL4_MIDDLE_SPEED)

        # Load intersection data
        self.intersection_profiles = self.load_intersections()
        self.intersection_points = self.intersection_profiles['intersection_points']
        self.intersection2_scenario2_points = self.intersection_profiles['intersection_points']['2']['2']
        # Load YAML sidewalk data
        self.intersections_layouts = self.load_intersections_layouts()

        # Create subscriber to simple_av/localization/intersection_status topic
        self.subscriptionIntersectionAwareness = self.create_subscription(LocalizationIntersectionStatus, 'simple_av/localization/intersection_status', self.intersectionAwareness_callback, 10)
        self.intersection_awareness_intersection_id = None
        self.intersection_awareness_status = None

        # Subscribe topics
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        self.pose = PoseStamped()

        self.subscriptionLocation = self.create_subscription(LocalizationMsg, 'simple_av/localization/location', self.location_callback, 10)
        self.location = LocalizationMsg()

        self.subscriptionVelocityReport = self.create_subscription(
            VelocityReport,
            '/vehicle/status/velocity_status',
            self.velocity_report_callback,
            10
        )
        self.velocity_report = VelocityReport()

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
        self.intersection_points = []
        self.cool4_triggered = False

        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False
        self.pending_reset = False
        self._last_log_time = {}
        self.prev_reset = False
        self.last_reset_time_ns = None
        self.reset_cooldown = 2.0
        self.reset_pose = None
        self.reset_lane = None
        self.reset_closest_point = None
        self.reset_time_ns = None
        self.reset_wait_distance = 5.0
        self.reset_wait_timeout = 2.0

        self.subscriptionDetectedObjects = self.create_subscription(DetectedObjectsArray, 'simple_av/perception/detected_objects', self.detectedObjects_callback, 10)
        self.detectedObjects = DetectedObjectsArray()

        # Publish topics
        self.planning_publisher = self.create_publisher(PlanningPathPlanningMsg, 'simple_av/planning/path_planning', 10)
        self.internal_msg_publisher = self.create_publisher(PlanningInternalMsg, 'simple_av/planning/internal_msg', 10)
        self.speed_profile_marker_pub = self.create_publisher(
            MarkerArray,
            'simple_av/planning/speed_profile_markers',
            qos_profile
        )
        self.path_markers_pub = self.create_publisher(
            MarkerArray,
            'simple_av/visualization/path_of_waypoints_markers',
            qos_profile
        )
        self.search_area_markers_pub = self.create_publisher(
            MarkerArray,
            'simple_av/visualization/search_area_markers',
            qos_profile
        )
        self.intersection_markers_pub = self.create_publisher(
            MarkerArray,
            'simple_av/visualization/intersection_point_markers',
            qos_profile
        )

        self.mission_planner_client = self.create_client(TriggerMissionPlan, '/planning/trigger_mission_plan')
        # Optional: check if service is ready
        while not self.mission_planner_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /planning/trigger_mission_plan service...')
        

        #Path planning
        self.isPathPlanned = False  # Flag to check if the path has been planned
        self.route = None # List of lanes from start lane to destination
        self.current_lane_index = 0
        self.initial_lane = None
        self.search_depth = 5 # previously it was 5
        self.destination = Point()
        
        #Lookahead
        self.lookahead_distance = self.base_speed * self.lookahead_distance_C + self.lookahead_distance_B # meters
        self.current_speed = 0.0
        
        #Curve handling
        self.curves = None
        self.speeds_on_path = []
        self.prev_lookahead_index = 0
        self.last_closest_point_index = None

        #Shutting down
        self.node_shut = False
        self._last_log_time = {}
    
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
        

    def load_intersections_layouts(self) -> List[PolygonRegion]:
        package_dir = get_package_share_directory("common")
        yaml_path = os.path.join(package_dir, "zones", "intersections_danger_zones.yaml")

        try:
            with open(yaml_path, "r") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            self.get_logger().error(f"❌ Failed to read YAML: {e}")
            return []

        if "intersections" not in data:
            self.get_logger().error("❌ YAML missing 'intersections' root key.")
            return []

        parsed_polygons = []

        # Iterate through intersections
        for inter_id, inter_data in data["intersections"].items():

            # Example categories: inside, sw, lane, lanes
            for category_name, category_value in inter_data.items():

                # Category that directly contains "points" (ex: inside)
                if isinstance(category_value, dict) and "points" in category_value:
                    parsed_polygons.append(
                        PolygonRegion(
                            name=f"{category_name}",
                            polygon_type=category_name,
                            intersection_id=str(inter_id),
                            polygon_id=str(0),
                            points=[tuple(p) for p in category_value["points"]]
                        )
                    )
                    continue

                # Categories containing multiple numbered polygons (sw / lane sets)
                if isinstance(category_value, dict):
                    for poly_id, poly_data in category_value.items():
                        if "points" in poly_data:
                            parsed_polygons.append(
                                PolygonRegion(
                                    name=f"{category_name}_{poly_id}",
                                    polygon_type=category_name,
                                    intersection_id=str(inter_id),
                                    polygon_id=str(poly_id),
                                    points=[tuple(p) for p in poly_data["points"]]
                                )
                            )

        return parsed_polygons

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
        self.intersection_awareness_intersection_id = msg.intersection_name
        self.intersection_awareness_status = msg.status

    def portal_callback(self, msg):
        now_ns = self.get_clock().now().nanoseconds
        reset_edge = msg.reset and not self.prev_reset
        cooldown_ok = (
            self.last_reset_time_ns is None or
            (now_ns - self.last_reset_time_ns) / 1e9 >= self.reset_cooldown
        )
        self.reset = reset_edge and cooldown_ok
        self.finished = msg.finished
        if self.reset:
            self.last_reset_time_ns = now_ns
        self.prev_reset = msg.reset
    
    def mission_plan_callback(self, msg):
        self.mission_plan = msg
        self.path = self.mission_plan.path
        self.path_as_lanes = self.mission_plan.path_as_lanes

    def pose_callback(self, msg):
        self.pose = msg

    def location_callback(self, msg):
        self.location = msg

    def velocity_report_callback(self, msg):
        self.velocity_report = msg
        self.current_speed = msg.longitudinal_velocity

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
        if lookahead_point_index < current_closest_point_index:
            lookahead_point_index = current_closest_point_index
        if lookahead_point_index >= path_size - 2:
            lookahead_point_index = path_size - 2
        self.prev_lookahead_index = lookahead_point_index
        
        return lookahead_point_index, self.path[lookahead_point_index].waypoint
    
    # TODO: create search area based on waypoints not lanes
    def create_search_area(self):
        try:
            lane_index = self.route.index(self.location.closest_lane_names.data)
        except:
            # vehicle is out of path
            self.get_logger().debug("create_search_area - Vehicle is out of the Path")
            lane_index = self.current_lane_index
        if lane_index in range(self.current_lane_index, self.current_lane_index + self.search_depth):
            self.current_lane_index = lane_index
        self.get_logger().debug(
            f"create_search_area - lane_index={lane_index} "
            f"current_lane_index={self.current_lane_index} "
            f"search_depth={self.search_depth} "
            f"total_lanes={len(self.path_as_lanes) if self.path_as_lanes else 0}"
        )
        search_area_as_lanes = self.path_as_lanes[self.current_lane_index: self.current_lane_index + self.search_depth]
        # convert lanes in the search are into a list of waypoints
        search_area = []
        for lane in search_area_as_lanes:
            lane_obj = self.find_lane_by_name(lane)
            waypoints = lane_obj['dense_waypoints']
            for waypoint in waypoints:
                search_area.append(Point(x=waypoint['x'], y=waypoint['y'], z=waypoint['z']))
        self.get_logger().debug(
            f"create_search_area - lanes_in_window={len(search_area_as_lanes)} "
            f"search_area_points={len(search_area)}"
        )
        return search_area, search_area_as_lanes

    def find_closest_waypoint_to_vehicle(self, vehicle_pose, search_area):
        # Finding the index of the closest point in search area
        distances_to_vehicle = []
        for waypoint in search_area:
            distances_to_vehicle.append(self.calculate_distance(waypoint, vehicle_pose))
        closest_waypoint_to_vehicle = search_area[distances_to_vehicle.index(min(distances_to_vehicle))]
        current_closest_point_to_vehicle = self.path_of_waypoints.index(closest_waypoint_to_vehicle)
        if self.last_closest_point_index is not None:
            if current_closest_point_to_vehicle < self.last_closest_point_index:
                current_closest_point_to_vehicle = self.last_closest_point_index
        self.last_closest_point_index = current_closest_point_to_vehicle
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

    def adjust_speed_to_curve(self, curvature, max_speed, max_lateral_accel=4.0):
        # Use lateral acceleration limit: v = sqrt(a_lat / curvature)
        if curvature <= 0.0:
            return max_speed
        curvature = max(curvature, 1e-6)
        speed = math.sqrt(max_lateral_accel / curvature)
        return min(max_speed, speed)

    def simple_av_speed_profile_maker(self, path, waypoint_distance=2.0):
        """
        Generate smooth, physically constrained speed profile.
        Vehicle starts at 0 and stops at the last waypoint.
        Enforces acceleration and deceleration limits and minimum speed.
        """

        _NORMAL_DECEL = abs(self.NORMAL_DECEL) * waypoint_distance

        # 1. Base speeds from curvature
        base_speeds = []
        for i, waypoint in enumerate(path):
            speed = self.adjust_speed_to_curve(waypoint.curve, self.MAX_SPEED, self.max_lateral_accel)
            base_speeds.append(speed)

        # 2. Forward pass (acceleration constraint)
        speeds = [0.0]  # Start from speed 0
        for i in range(1, len(base_speeds)):
            prev_speed = speeds[-1]
            accel_limit = self.get_accel_for_speed(prev_speed)
            accel_limit = max(accel_limit, 0.0)
            accel_step = max(accel_limit, 0.0) * waypoint_distance
            # Max speed allowed by acceleration
            max_next_speed = math.sqrt(prev_speed**2 + 2 * accel_step)
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

        speeds = self.apply_jerk_limit(speeds, waypoint_distance)
        for i in range(1, len(speeds) - 1):
            speeds[i] = max(min(speeds[i], self.MAX_SPEED), self.MIN_SPEED)

        speeds[0] = 0.0
        speeds[-1] = 0.0

        return speeds

    def get_accel_for_speed(self, speed):
        for entry in self.ACCEL_PROFILE:
            try:
                min_speed = float(entry.get('min_speed', 0.0))
                max_speed = float(entry.get('max_speed', float('inf')))
                accel = float(entry.get('accel', self.NORMAL_ACCEL))
            except (TypeError, ValueError):
                continue
            if speed >= min_speed and speed < max_speed:
                return accel
        return self.NORMAL_ACCEL

    def apply_jerk_limit(self, speeds, waypoint_distance):
        if len(speeds) < 3 or waypoint_distance <= 0.0:
            return speeds

        def forward_pass(input_speeds):
            output = [input_speeds[0]]
            a_prev = 0.0
            v_prev = input_speeds[0]

            for i in range(1, len(input_speeds)):
                v_des = input_speeds[i]
                a_des = (v_des**2 - v_prev**2) / (2 * waypoint_distance)
                if a_des >= 0.0:
                    j_max = self.MAX_JERK_ACCEL
                else:
                    j_max = self.MAX_JERK_DECEL

                a_min = a_prev - j_max * waypoint_distance
                a_max = a_prev + j_max * waypoint_distance
                a_clamped = max(a_min, min(a_des, a_max))

                v_new_sq = max(v_prev**2 + 2 * a_clamped * waypoint_distance, 0.0)
                v_new = min(v_des, math.sqrt(v_new_sq))
                output.append(v_new)

                a_prev = (v_new**2 - v_prev**2) / (2 * waypoint_distance)
                v_prev = v_new

            return output

        speeds = forward_pass(speeds)
        speeds = list(reversed(forward_pass(list(reversed(speeds)))))
        return speeds
    
    
    def get_detected_pedestrians(self):
        """
        Get detected pedestrians and cyclists from perception data.
        Returns a list of detected objects with labels:
        - 7: Cyclist/Bicycle & Pedestrian
        """
        if not self.detectedObjects or not self.detectedObjects.objects:
            self.get_logger().debug("No perception data or no objects detected")
            return []  # Return empty list instead of None

        detected_pedestrians = []
        for obj in self.detectedObjects.objects:
            object_type = obj.label
            # Label is int32, check for pedestrian and cyclist (7)
            if object_type in [7]:
                detected_pedestrians.append(obj)

        if detected_pedestrians:
            self.get_logger().debug(f"Detected {len(detected_pedestrians)} pedestrians/cyclists")

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

    def is_object_detected_on_intersection_danger_zones(self, intersection_id):
        self.get_logger().debug(f"insde is_object_detected_on_intersection_danger_zones ")
        # Validate that we have pose data
        if not self.pose or not self.pose.pose:
            self.get_logger().warning("No pose data available for danger zone detection")
            return False

        vehicle_pose = self.pose.pose.position
        vehicle_orientation = self.pose.pose.orientation

        # Check if pose is valid (not at origin)
        if vehicle_pose.x == 0.0 and vehicle_pose.y == 0.0 and vehicle_pose.z == 0.0:
            self.get_logger().debug("Vehicle pose at origin, skipping danger zone check")
            return False

        self.get_logger().debug("Checking intersection danger zones...")
        detected_pedestrians = self.get_detected_pedestrians()
        if not detected_pedestrians:
            self.get_logger().debug("No pedestrians detected")
            return False

        # Validate layout data exists
        if not self.intersections_layouts:
            self.get_logger().warning("No intersection layout data loaded")
            return False

        if not any(p.intersection_id == intersection_id for p in self.intersections_layouts):
            self.get_logger().warning(f"No intersection data for intersection '{intersection_id}'")
            return False

        danger_zones = [
            p for p in self.intersections_layouts
            if p.intersection_id == intersection_id and p.polygon_type == "sw"
        ]

        objects_in_zones = 0
        for ped in detected_pedestrians:
            # Convert relative position to absolute position
            ped_abs = self.get_object_absolute_position(vehicle_orientation, vehicle_pose, ped.position)
            self.get_logger().debug(f"Checking pedestrian at absolute position: ({ped_abs.x:.2f}, {ped_abs.y:.2f})")

            for p in danger_zones:
                if p.polygon_id == '3': #skipping sw3 for this scenario TODO: change this later
                    continue
                if self.is_point_in_polygon(ped_abs, p.points):
                    objects_in_zones += 1
                    self.get_logger().debug(
                        f"Pedestrian detected at ({ped_abs.x:.2f}, {ped_abs.y:.2f}) at intersection {p.intersection_id} inside: {p.polygon_type}{p.polygon_id}"
                    )

        if objects_in_zones > 0:
            self.get_logger().debug(f"Total pedestrians in danger zones: {objects_in_zones}")
        else:
            self.get_logger().debug("No pedestrians in danger zones")
        return objects_in_zones > 0


    # def cool4_speed_profile_adjustment(self, intersection_points,  waypoint_distance=2.0):
    #     start_idx, exit_idx, end_idx = intersection_points
    #
    #     # Only check danger zones if we're at intersection 2 and have intersection awareness data
    #     is_object_in_danger_zone = False
    #     self.get_logger().info(f"intersection_awareness_intersection_id: {self.intersection_awareness_intersection_id} ")
    #     self.get_logger().info(f"intersection_awareness_status: {self.intersection_awareness_status} ")
    #
    #     is_object_in_danger_zone = self.is_object_detected_on_intersection_danger_zones('2')
    #     self.get_logger().info(f"At intersection 2, checking danger zones: {is_object_in_danger_zone}")
    #
    #     self.get_logger().info(f"is_RSU_enabled: {self.is_RSU_enabled}, Danger: {is_object_in_danger_zone}")
    #     if self.is_RSU_enabled and not is_object_in_danger_zone:
    #         self.get_logger().info("RSU enabled, no danger detected - continuing through intersection at moderate speed (12 km/h)")
    #         # Case 1: RSU active and no danger → keep moderate constant speed
    #         self.speeds_on_path[start_idx:exit_idx] = [self.COOL4_MIDDLE_SPEED] * (exit_idx - start_idx)
    #
    #         # accelerate again from MIN_SPEED to MAX_SPEED after intersection
    #         n_points_after = end_idx - exit_idx
    #         if n_points_after > 0:
    #             accel_profile = []
    #             v = self.COOL4_MIDDLE_SPEED
    #             accel_profile.append(v)  # include initial speed
    #             for _ in range(1, n_points_after):
    #                 v = min(self.MAX_SPEED, math.sqrt(v**2 + 2 * self.NORMAL_ACCEL * waypoint_distance))
    #                 accel_profile.append(v)
    #             self.speeds_on_path[exit_idx:end_idx] = accel_profile
    #
    #     elif (self.is_RSU_enabled and is_object_in_danger_zone) or (not self.is_RSU_enabled):
    #         self.get_logger().info("Danger detected or RSU disabled - decelerating through intersection to minimum speed")
    #         # Case 2: RSU is_object_in_danger_zone OR no RSU → decelerate gradually from current speed → MIN_SPEED
    #         treshold_test = 10
    #         decel_profile = []
    #         current_speed = self.current_speed
    #         min_speed = self.COOL4_MIN_SPEED if current_speed > self.COOL4_MIN_SPEED else current_speed
    #         if treshold_test > 0:
    #             step = (current_speed - min_speed) / treshold_test
    #             for i in range(treshold_test):
    #                 decel_profile.append(current_speed - step * (i + 1))
    #         self.speeds_on_path[start_idx:start_idx+treshold_test] = decel_profile
    #         self.speeds_on_path[start_idx+treshold_test:exit_idx] = [min_speed] * (exit_idx - (start_idx+treshold_test))
    #
    #         # accelerate again from MIN_SPEED to MAX_SPEED after intersection
    #         n_points_after = end_idx - exit_idx
    #         if n_points_after > 0:
    #             accel_profile = []
    #             v = self.COOL4_MIN_SPEED
    #             accel_profile.append(v)  # include initial speed
    #             for _ in range(1, n_points_after):
    #                 v = min(self.MAX_SPEED, math.sqrt(v**2 + 2 * self.NORMAL_ACCEL * waypoint_distance))
    #                 accel_profile.append(v)
    #             self.speeds_on_path[exit_idx:end_idx] = accel_profile

    def cool4_speed_profile_adjustment(self, intersection_points, waypoint_distance=2.0):
        start_idx, exit_idx, end_idx = intersection_points

        if exit_idx <= start_idx:
            return

        self.get_logger().info(
            f"intersection_awareness_intersection_id: {self.intersection_awareness_intersection_id} "
        )
        self.get_logger().info(
            f"intersection_awareness_status: {self.intersection_awareness_status} "
        )

        is_object_in_danger_zone = self.is_object_detected_on_intersection_danger_zones('2')
        self.get_logger().info(
            f"At intersection 2, checking danger zones: {is_object_in_danger_zone}"
        )
        self.get_logger().info(
            f"is_RSU_enabled: {self.is_RSU_enabled}, Danger: {is_object_in_danger_zone}"
        )

        if self.is_RSU_enabled and not is_object_in_danger_zone:
            target_speed = self.COOL4_MAX_SPEED
            cap_speed = self.COOL4_MAX_SPEED
            self.get_logger().info(
                "RSU enabled, no danger detected - ramping to max speed through intersection"
            )
        else:
            target_speed = self.COOL4_MIN_SPEED
            cap_speed = max(self.current_speed, self.COOL4_MIDDLE_SPEED)
            self.get_logger().info(
                "Danger detected or RSU disabled - ramping to minimum speed through intersection"
            )

        current_speed = min(self.current_speed, cap_speed)
        ramp_points = exit_idx - start_idx
        if ramp_points > 0:
            ramp_profile = [cap_speed] * ramp_points
            ramp_profile[0] = current_speed
            ramp_profile[-1] = target_speed

            for i in range(1, ramp_points):
                prev_speed = ramp_profile[i - 1]
                accel_limit = max(self.get_accel_for_speed(prev_speed), 0.0)
                accel_step = accel_limit * waypoint_distance
                max_next_speed = math.sqrt(prev_speed**2 + 2 * accel_step)
                ramp_profile[i] = min(ramp_profile[i], max_next_speed, cap_speed)

            decel_step = abs(self.NORMAL_DECEL) * waypoint_distance
            for i in reversed(range(ramp_points - 1)):
                next_speed = ramp_profile[i + 1]
                max_prev_speed = math.sqrt(next_speed**2 + 2 * decel_step)
                ramp_profile[i] = min(ramp_profile[i], max_prev_speed, cap_speed)

            ramp_profile = self.apply_jerk_limit(ramp_profile, waypoint_distance)
            ramp_profile[0] = current_speed
            ramp_profile[-1] = target_speed
            for i in range(1, ramp_points - 1):
                ramp_profile[i] = max(
                    min(ramp_profile[i], cap_speed),
                    self.MIN_SPEED
                )

            self.speeds_on_path[start_idx:exit_idx] = ramp_profile

        n_points_after = end_idx - exit_idx
        if n_points_after > 0:
            accel_profile = []
            v = target_speed
            accel_profile.append(v)
            for _ in range(1, n_points_after):
                accel_limit = max(self.get_accel_for_speed(v), 0.0)
                accel_step = accel_limit * waypoint_distance
                v = min(self.MAX_SPEED, math.sqrt(v**2 + 2 * accel_step))
                accel_profile.append(v)
            self.speeds_on_path[exit_idx:end_idx] = accel_profile

    def check_cool4_speed_profile_trigger(self, vehicle_pose, threshold=6.0):
        if self.is_cool4_speed_profile_enable and self.intersection_awareness_intersection_id == '2' and self.intersection_awareness_status is not None:
            if self.intersection_points and not self.cool4_triggered:
                trigger_point_index = self.intersection_points[0]
                if self.calculate_distance(vehicle_pose, self.path[trigger_point_index].waypoint) <= threshold:
                    self.get_logger().info("Reached Cool4 trigger waypoint — adjusting speed profile...")
                    self.cool4_speed_profile_adjustment(self.intersection_points)
                    self.publish_speed_profile_markers()
                    self.cool4_triggered = True


    def find_intersection_start_and_exit_using_config(self, path):
        points = self.intersection2_scenario2_points
        intersection_points = []

        def nearest_index(target_point):
            nearest = None
            nearest_dist = float('inf')
            for i, waypoint in enumerate(path):
                wp = waypoint.waypoint
                dist = self.calculate_distance(wp, target_point, z=True)
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest = i
            return nearest

        p1 = Point(x=points['1']['x'], y=points['1']['y'], z=points['1']['z'])
        p2 = Point(x=points['2']['x'], y=points['2']['y'], z=points['2']['z'])
        intersection_points.append(nearest_index(p1))
        intersection_points.append(nearest_index(p2))
        if '3' in points:
            p3 = Point(x=points['3']['x'], y=points['3']['y'], z=points['3']['z'])
            intersection_points.append(nearest_index(p3))

        return intersection_points


    def handle_mission_plan(self):
        if self.path and self.path_as_lanes:
            self.destination = self.path[-1].waypoint
            self.speeds_on_path = self.simple_av_speed_profile_maker(self.path)
                            
            self.path_of_waypoints.clear()
            for i, waypoint in enumerate(self.path):
                self.path_of_waypoints.append(waypoint.waypoint)

            self.route = self.path_as_lanes[:]
            self.current_lane_index = 0
            self.isPathPlanned = True
            self.last_closest_point_index = None
            self.publish_speed_profile_markers()
            self.publish_path_of_waypoints_markers()

            if self.is_cool4_speed_profile_enable:
                self.intersection_points = self.find_intersection_start_and_exit_using_config(self.path)
                self.get_logger().info(f"Read intersection_points: {self.intersection_points}")
                #self.get_logger().info(f"intersection speed profile is updated")
                self.publish_intersection_point_markers()

    def end_of_path_detection(self, current_closest_point_to_vehicle_index):
        current_pose = self.path_of_waypoints[current_closest_point_to_vehicle_index]
        
        distance = self.calculate_distance(current_pose, self.destination)
        if distance <= 2.0:
            return True
        return False

    def speed_to_color(self, speed):
        if self.MAX_SPEED <= self.MIN_SPEED:
            t = 0.0
        else:
            t = (speed - self.MIN_SPEED) / (self.MAX_SPEED - self.MIN_SPEED)
        t = max(0.0, min(1.0, t))
        return ColorRGBA(r=t, g=0.2, b=1.0 - t, a=0.9)

    def publish_speed_profile_markers(self):
        if not self.path_of_waypoints or not self.speeds_on_path:
            return

        count = min(len(self.path_of_waypoints), len(self.speeds_on_path))
        marker_array = MarkerArray()

        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        now = self.get_clock().now().to_msg()
        points_marker = Marker()
        points_marker.header.frame_id = "map"
        points_marker.header.stamp = now
        points_marker.ns = "speed_profile"
        points_marker.id = 0
        points_marker.type = Marker.SPHERE_LIST
        points_marker.action = Marker.ADD
        points_marker.pose.orientation.w = 1.0
        points_marker.scale.x = 0.7
        points_marker.scale.y = 0.7
        points_marker.scale.z = 0.7

        text_id = 1
        for i in range(count):
            waypoint = self.path_of_waypoints[i]
            speed = self.speeds_on_path[i]
            color = self.speed_to_color(speed)
            points_marker.points.append(Point(x=waypoint.x, y=waypoint.y, z=waypoint.z))
            points_marker.colors.append(color)

            speed_marker = Marker()
            speed_marker.header.frame_id = "map"
            speed_marker.header.stamp = now
            speed_marker.ns = "speed_profile_text"
            speed_marker.id = text_id
            speed_marker.type = Marker.TEXT_VIEW_FACING
            speed_marker.action = Marker.ADD
            speed_marker.pose.position = Point(
                x=waypoint.x + 0.6,
                y=waypoint.y,
                z=waypoint.z + 1.6
            )
            speed_marker.pose.orientation.w = 1.0
            speed_marker.scale.z = 0.7
            speed_marker.color = color
            speed_marker.text = f"{speed * 3.6:.1f}"
            marker_array.markers.append(speed_marker)
            text_id += 1

            id_marker = Marker()
            id_marker.header.frame_id = "map"
            id_marker.header.stamp = now
            id_marker.ns = "speed_profile_id"
            id_marker.id = text_id
            id_marker.type = Marker.TEXT_VIEW_FACING
            id_marker.action = Marker.ADD
            id_marker.pose.position = Point(
                x=waypoint.x + 1.2,
                y=waypoint.y,
                z=waypoint.z + 1.6
            )
            id_marker.pose.orientation.w = 1.0
            id_marker.scale.z = 0.6
            id_marker.color.r = 1.0
            id_marker.color.g = 1.0
            id_marker.color.b = 1.0
            id_marker.color.a = 1.0
            id_marker.text = str(i)
            marker_array.markers.append(id_marker)
            text_id += 1

        marker_array.markers.append(points_marker)
        self.speed_profile_marker_pub.publish(marker_array)

    def publish_path_of_waypoints_markers(self):
        if not self.path_of_waypoints:
            return

        marker_array = MarkerArray()
        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        now = self.get_clock().now().to_msg()
        points_marker = Marker()
        points_marker.header.frame_id = "map"
        points_marker.header.stamp = now
        points_marker.ns = "path_of_waypoints"
        points_marker.id = 0
        points_marker.type = Marker.SPHERE_LIST
        points_marker.action = Marker.ADD
        points_marker.pose.orientation.w = 1.0
        points_marker.scale.x = 1.2
        points_marker.scale.y = 1.2
        points_marker.scale.z = 1.2
        points_marker.color.r = 0.6
        points_marker.color.g = 0.2
        points_marker.color.b = 0.8
        points_marker.color.a = 0.9

        for waypoint in self.path_of_waypoints:
            points_marker.points.append(Point(x=waypoint.x, y=waypoint.y, z=waypoint.z))

        marker_array.markers.append(points_marker)
        self.path_markers_pub.publish(marker_array)

    def publish_search_area_markers(self, search_area):
        if not search_area:
            return

        marker_array = MarkerArray()
        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        now = self.get_clock().now().to_msg()
        points_marker = Marker()
        points_marker.header.frame_id = "map"
        points_marker.header.stamp = now
        points_marker.ns = "search_area"
        points_marker.id = 0
        points_marker.type = Marker.SPHERE_LIST
        points_marker.action = Marker.ADD
        points_marker.pose.orientation.w = 1.0
        points_marker.scale.x = 0.8
        points_marker.scale.y = 0.8
        points_marker.scale.z = 0.8
        points_marker.color.r = 1.0
        points_marker.color.g = 0.6
        points_marker.color.b = 0.0
        points_marker.color.a = 0.9

        for waypoint in search_area:
            points_marker.points.append(Point(x=waypoint.x, y=waypoint.y, z=waypoint.z))

        marker_array.markers.append(points_marker)
        self.search_area_markers_pub.publish(marker_array)

    def publish_intersection_point_markers(self):
        if not self.intersection_points or not self.path:
            return
        if len(self.intersection_points) < 2:
            return

        marker_array = MarkerArray()
        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        now = self.get_clock().now().to_msg()
        colors = [
            (0.1, 0.9, 0.1),  # start: green
            (0.9, 0.1, 0.1),  # exit: red
            (0.1, 0.3, 0.9),  # end: blue
        ]

        for idx, point_index in enumerate(self.intersection_points[:3]):
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = now
            marker.ns = "intersection_points"
            marker.id = idx
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            waypoint = self.path[point_index].waypoint
            marker.pose.position = Point(x=waypoint.x, y=waypoint.y, z=waypoint.z)
            marker.pose.orientation.w = 1.0
            marker.scale.x = 1.5
            marker.scale.y = 1.5
            marker.scale.z = 1.5
            r, g, b = colors[idx]
            marker.color.r = r
            marker.color.g = g
            marker.color.b = b
            marker.color.a = 0.9
            marker_array.markers.append(marker)

        self.intersection_markers_pub.publish(marker_array)

    def lane_following(self):
        if not self.location and not self.pose:
            self.get_logger().warning("No location/pose input")
            return None

        if not self.isPathPlanned:
            self.get_logger().info(
                    f"Requesting mission plan with lane={self.location.closest_lane_names.data} "
                    f"closest_point=({self.location.closest_point.x:.2f}, "
                    f"{self.location.closest_point.y:.2f}, {self.location.closest_point.z:.2f})"
                )
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
            self.cool4_triggered = False
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
        
        self.check_cool4_speed_profile_trigger(vehicle_pose)

        search_area, search_area_as_lanes = self.create_search_area()
        current_closest_point_to_vehicle_index = self.find_closest_waypoint_to_vehicle(vehicle_pose, search_area)
        look_ahead_point_index, look_ahead_point = self.find_lookahead_point(current_closest_point_to_vehicle_index)
        isEndOfPath = self.end_of_path_detection(current_closest_point_to_vehicle_index)
        if not look_ahead_point and not look_ahead_point_index:
            self.get_logger().warning("Lookahead point not set in local planning")
            return
                  
        self.lookahead_distance = self.current_speed * self.lookahead_distance_C + self.lookahead_distance_B # meters

        isTurnDetected = False
        if self.speeds_on_path[look_ahead_point_index] < 10.0:
            isTurnDetected = True

        self.publish_curve_internal_msg(isTurnDetected, isEndOfPath)
        self.publish_path_planning_msgs(look_ahead_point, self.speeds_on_path[look_ahead_point_index]) # publishing

        self.get_logger().debug(
            f'lookahead distance:  {self.lookahead_distance}\n'
            f'current point index:  {current_closest_point_to_vehicle_index}\n'
            f'lookahead point index:  {look_ahead_point_index} {self.prev_lookahead_index}\n'
            f'speed: {self.speeds_on_path[look_ahead_point_index]}\n'
            f'is turn detected: {isTurnDetected}\n'
        )

    def log_throttle(self, level, key, msg, period_sec=1.0):
        now = self.get_clock().now().nanoseconds / 1e9
        last = self._last_log_time.get(key, 0.0)
        if now - last < period_sec:
            return
        self._last_log_time[key] = now
        if level == "debug":
            self.get_logger().debug(msg)
        elif level == "info":
            self.get_logger().info(msg)
        elif level == "warning":
            self.get_logger().warning(msg)
        elif level == "error":
            self.get_logger().error(msg)
        else:
            self.get_logger().info(msg)


def main(args=None):
    rclpy.init(args=args)
    node = BehaviorPathPlanner()
    try:
        while rclpy.ok() and not node.node_shut:
            rclpy.spin_once(node, timeout_sec=0.1)# Set timeout to 0 to avoid delay
            node.lane_following()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
