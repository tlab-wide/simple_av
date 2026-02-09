#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import os
import json
import yaml
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped, Point
from rclpy.duration import Duration as RclpyDuration
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener
from std_msgs.msg import String, ColorRGBA, Bool
import math
from collections import deque
from simple_av_msgs.msg import PlanningInternalMsg, PlanningInternalMissionPlanMsg, PlanningWaypoint
from simple_av_msgs.msg import LocalizationIntersectionStatus
from simple_av_msgs.msg import Portal
from visualization_msgs.msg import Marker, MarkerArray
from autoware_vehicle_msgs.msg import VelocityReport
import numpy as np
from typing import List, Tuple
from dataclasses import dataclass
from simple_av_msgs.srv import TriggerMissionPlan
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy
from scipy.spatial.transform import Rotation as R
import traceback

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
        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)

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
        speed_limits = self.motion_behavior_config['motion']['speed_limits']
        self.base_speed = float(speed_limits['base'])  # m/s
        self.turning_speed = float(speed_limits['turning_speed'])  # m/s
        self.MIN_SPEED = float(speed_limits.get('min', 0.0))
        self.MAX_SPEED = self.base_speed
        self.COOL4_MIN_SPEED = float(speed_limits.get('cool4_min', self.MIN_SPEED))
        self.COOL4_MIDDLE_SPEED = float(speed_limits.get('cool4_middle', self.COOL4_MIN_SPEED))
        self.COOL4_MAX_SPEED = float(speed_limits.get('cool4_max', self.MAX_SPEED))
        self.densify_interval = self.motion_behavior_config['motion']['path']['densify_interval']
        self.curve_calc_dist = int(self.motion_behavior_config['motion'].get('curve_calc_dist', 6))
        self.max_lateral_accel = self.motion_behavior_config['motion'].get('max_lateral_accel', 4.0)

        # Vehicle configs (geometry only; performance handled by motion planner)
        self.vehicle_config = self.load_vehicle_config(self.vehicle_model)

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
        self.pose = PoseStamped()
        self.map_frame = 'map'
        self.base_frame = 'base_link'
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

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
        self.subscription_mission_plan = self.create_subscription(
            PlanningInternalMissionPlanMsg,
            '/simple_av/mission_planning/path',
            self.mission_plan_callback,
            qos_profile
        )
        self.mission_plan = PlanningInternalMissionPlanMsg()
        self.mission_plan_densified_pub = self.create_publisher(
            PlanningInternalMissionPlanMsg,
            '/simple_av/path_planning/trajectory',
            qos_profile
        )
        self.path_as_lanes = None  # List of lanes from start lane to destination
        self.path = None  # List of [waypoints,curve] in order of path_as_lanes
        self.path_of_waypoints = [] # List of waypoints in order of path_as_lanes
        self.base_path_points = []
        self.base_max_speed = self.base_speed
        self.intersection_points = []
        self.cool4_triggered = False

        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False
        self.pending_reset = False
        self._last_log_time = {}
        self.prev_reset = False
        self.round_number = 0
        self.last_reset_time_ns = None
        # Reset cooldown disabled for behavior path planner.
        # self.reset_cooldown = self.scenario_config['scenario'].get('reset_cooldown_seconds', 2.0)
        self.reset_pose = None
        self.reset_lane = None
        self.reset_closest_point = None
        self.reset_time_ns = None
        self.reset_wait_distance = 5.0
        self.reset_wait_timeout = 2.0

        self.subscriptionRsuDanger = self.create_subscription(
            Bool,
            'simple_av/perception/rsu_danger_detected',
            self.rsu_danger_callback,
            10
        )
        self.rsu_danger_detected = False

        # Publish topics
        self.internal_msg_publisher = self.create_publisher(PlanningInternalMsg, 'simple_av/planning/internal_msg', 10)
        self.speed_profile_marker_pub = self.create_publisher(
            MarkerArray,
            'simple_av/planning/speed_profile_markers_smoothed',
            qos_profile
        )
        self.path_markers_pub = self.create_publisher(
            MarkerArray,
            '/simple_av/path_planning/visualization/smoothed_path',
            qos_profile
        )
        self.curvature_markers_pub = self.create_publisher(
            MarkerArray,
            '/simple_av/path_planning/visualization/smoothed_path/curvature',
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
        self.mission_plan_requested = False
        self.mission_plan_request_time_ns = None
        self.mission_plan_retry_count = 0
        self.mission_plan_retry_base_seconds = 0.5
        self.mission_plan_retry_max_seconds = 5.0
        self.mission_plan_retry_backoff = 2.0
        self.route = None # List of lanes from start lane to destination
        self.current_lane_index = 0
        self.initial_lane = None
        self.search_depth = 5 # previously it was 5
        self.destination = Point()
        
        #Lookahead (handled in control now)
        self.current_speed = 0.0
        
        #Curve handling
        self.curves = None
        self.speeds_on_path = []
        self.last_closest_point_index = None

        #Shutting down
        self.node_shut = False
        self._last_log_time = {}
        # Path planning loop timer (uses ROS time when use_sim_time is enabled)
        self.loop_period_sec = 0.05
        self.loop_timer = self.create_timer(self.loop_period_sec, self.lane_following_timer_cb)

    def lane_following_timer_cb(self):
        if self.node_shut:
            return
        try:
            self.lane_following()
        except Exception:
            self.get_logger().error("lane_following exception:\n" + traceback.format_exc())
    
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
    
    def rsu_danger_callback(self, msg):
        self.rsu_danger_detected = bool(msg.data)

    def intersectionAwareness_callback(self, msg):
        self.intersection_awareness_intersection_id = msg.intersection_name
        self.intersection_awareness_status = msg.status

    def portal_callback(self, msg):
        now_ns = self.get_clock().now().nanoseconds
        round_changed = msg.round_number != self.round_number
        reset_edge = msg.reset and not self.prev_reset
        # Reset cooldown disabled for behavior path planner.
        # cooldown_ok = (
        #     self.last_reset_time_ns is None or
        #     (now_ns - self.last_reset_time_ns) / 1e9 >= self.reset_cooldown
        # )
        cooldown_ok = True
        self.reset = (reset_edge or round_changed) and cooldown_ok
        self.finished = msg.finished
        self.round_number = msg.round_number
        if self.reset:
            self.last_reset_time_ns = now_ns
            self.pending_reset = True
        self.prev_reset = msg.reset

    def reset_cooldown_active(self):
        # Reset cooldown disabled for behavior path planner.
        return False

    def mission_plan_retry_delay(self):
        delay = self.mission_plan_retry_base_seconds * (self.mission_plan_retry_backoff ** self.mission_plan_retry_count)
        return min(self.mission_plan_retry_max_seconds, delay)
    
    def mission_plan_callback(self, msg):
        self.mission_plan = msg
        self.base_path_points = [wp.waypoint for wp in msg.path]
        self.path_as_lanes = list(msg.path_as_lanes)
        if msg.path:
            self.base_max_speed = float(getattr(msg.path[0], 'speed', self.base_speed))
            self.log_throttle(
                "info",
                "base_path_rx",
                f"Received base path with {len(msg.path)} points",
                period_sec=1.0,
            )

    def update_pose_from_tf(self):
        try:
            tf = self.tf_buffer.lookup_transform(
                self.map_frame,
                self.base_frame,
                Time(),
                timeout=RclpyDuration(seconds=0.0),
            )
        except Exception:
            return False

        pose_msg = PoseStamped()
        pose_msg.header = tf.header
        pose_msg.pose.position.x = tf.transform.translation.x
        pose_msg.pose.position.y = tf.transform.translation.y
        pose_msg.pose.position.z = tf.transform.translation.z
        pose_msg.pose.orientation = tf.transform.rotation
        self.pose = pose_msg
        return True

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

    def smooth_points(self, points, window_size=5):
        if len(points) < 3:
            return list(points)
        half = max(1, window_size // 2)
        smoothed = []
        for i in range(len(points)):
            start = max(0, i - half)
            end = min(len(points), i + half + 1)
            sx = sum(p.x for p in points[start:end])
            sy = sum(p.y for p in points[start:end])
            sz = sum(p.z for p in points[start:end])
            count = end - start
            smoothed.append(Point(x=sx / count, y=sy / count, z=sz / count))
        return smoothed

    def resample_points(self, points, spacing):
        if len(points) < 2:
            return list(points)
        resampled = [points[0]]
        carry = 0.0
        for i in range(1, len(points)):
            p0 = points[i - 1]
            p1 = points[i]
            dx = p1.x - p0.x
            dy = p1.y - p0.y
            dz = p1.z - p0.z
            seg_len = math.sqrt(dx * dx + dy * dy + dz * dz)
            if seg_len <= 1e-6:
                continue
            dist = carry
            while dist + spacing <= seg_len:
                dist += spacing
                t = dist / seg_len
                resampled.append(Point(
                    x=p0.x + dx * t,
                    y=p0.y + dy * t,
                    z=p0.z + dz * t,
                ))
            carry = seg_len - dist
        if (resampled[-1].x != points[-1].x or
                resampled[-1].y != points[-1].y or
                resampled[-1].z != points[-1].z):
            resampled.append(points[-1])
        return resampled

    def compute_curves(self, points, curve_calc_dist=6):
        if len(points) < 2 * curve_calc_dist:
            return [0.0 for _ in points]
        curves = [0.0 for _ in points]
        for i in range(curve_calc_dist, len(points) - curve_calc_dist):
            p1 = points[i - curve_calc_dist]
            p2 = points[i]
            p3 = points[i + curve_calc_dist]
            a = math.hypot(p2.x - p1.x, p2.y - p1.y)
            b = math.hypot(p3.x - p2.x, p3.y - p2.y)
            c = math.hypot(p3.x - p1.x, p3.y - p1.y)
            if a < 1e-6 or b < 1e-6 or c < 1e-6:
                continue
            cross = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
            curvature = 2.0 * abs(cross) / (a * b * c)
            curves[i] = curvature
        return curves
    
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
        
    # Create search area based on waypoint indices instead of lanes.
    def create_search_area(self):
        if not self.path_of_waypoints:
            return [], []

        if self.last_closest_point_index is None:
            center_idx = 0
        else:
            center_idx = max(0, min(self.last_closest_point_index, len(self.path_of_waypoints) - 1))

        points_per_lane = 20
        window = max(self.search_depth * points_per_lane, 50)
        start_idx = max(0, center_idx - window)
        end_idx = min(len(self.path_of_waypoints), center_idx + window)
        search_area = self.path_of_waypoints[start_idx:end_idx]
        self.get_logger().debug(
            f"create_search_area - index_window=[{start_idx}:{end_idx}] "
            f"center_idx={center_idx} "
            f"search_area_points={len(search_area)}"
        )
        return search_area, []

    def find_closest_waypoint_to_vehicle(self, vehicle_pose, search_area):
        # Finding the index of the closest point in search area
        distances_to_vehicle = []
        for waypoint in search_area:
            distances_to_vehicle.append(self.calculate_distance(waypoint, vehicle_pose))
        closest_waypoint_to_vehicle = search_area[distances_to_vehicle.index(min(distances_to_vehicle))]
        current_closest_point_to_vehicle = None
        min_path_dist = float('inf')
        for i, wp in enumerate(self.path_of_waypoints):
            d = self.calculate_distance(wp, closest_waypoint_to_vehicle)
            if d < min_path_dist:
                min_path_dist = d
                current_closest_point_to_vehicle = i
        if self.last_closest_point_index is not None:
            if current_closest_point_to_vehicle < self.last_closest_point_index:
                current_closest_point_to_vehicle = self.last_closest_point_index
        self.last_closest_point_index = current_closest_point_to_vehicle
        return current_closest_point_to_vehicle
        
    def dot_product(self, v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]
            
    def publish_curve_internal_msg(self, isTurnDetected, isEndOfPath):
        internal_msg = PlanningInternalMsg()
        internal_msg.is_curve_detected = bool(isTurnDetected)
        internal_msg.is_end_of_path = bool(isEndOfPath)
        self.internal_msg_publisher.publish(internal_msg)

    def request_mission_plan(self):
        self.get_logger().info("Requesting mission plan")
        request = TriggerMissionPlan.Request()
        future = self.mission_planner_client.call_async(request)
        return future

    # Removed path-level speed shaping; motion planner handles acceleration/deceleration.
    
    
    def get_detected_pedestrians(self):
        """
        Get detected pedestrians and cyclists from perception data.
        Returns a list of detected objects with labels:
        - 7: Cyclist/Bicycle & Pedestrian
        """
        self.get_logger().debug("Detected objects input disabled; use v2x_handler output.")
        return []

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
        self.get_logger().debug("danger zone check via v2x_handler")
        return self.rsu_danger_detected


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

    def cool4_speed_profile_adjustment(self, intersection_points, waypoint_distance=None):
        """
        Apply simple speed caps through the intersection; motion planner handles
        actual acceleration/deceleration shaping.
        """
        start_idx, exit_idx, end_idx = intersection_points

        if exit_idx <= start_idx:
            return

        is_object_in_danger_zone = self.is_object_detected_on_intersection_danger_zones('2')

        if self.is_RSU_enabled and not is_object_in_danger_zone:
            cap_speed = self.COOL4_MAX_SPEED
            self.get_logger().info("RSU enabled, no danger detected - capping to COOL4_MAX_SPEED through intersection")
        else:
            cap_speed = self.COOL4_MIN_SPEED
            self.get_logger().info("Danger detected or RSU disabled - capping to COOL4_MIN_SPEED through intersection")

        # Cap speeds inside intersection
        ramp_points = max(0, exit_idx - start_idx)
        if ramp_points > 0:
            self.speeds_on_path[start_idx:exit_idx] = [cap_speed] * ramp_points

        # Restore to base max after intersection
        n_points_after = max(0, end_idx - exit_idx)
        if n_points_after > 0:
            self.speeds_on_path[exit_idx:end_idx] = [float(self.base_max_speed)] * n_points_after

    def check_cool4_speed_profile_trigger(self, vehicle_pose, threshold=6.0):
        if self.is_cool4_speed_profile_enable and self.intersection_awareness_intersection_id == '2' and self.intersection_awareness_status is not None:
            if self.intersection_points and not self.cool4_triggered:
                trigger_point_index = self.intersection_points[0]
                if self.calculate_distance(vehicle_pose, self.path[trigger_point_index].waypoint) <= threshold:
                    self.get_logger().info("Reached Cool4 trigger waypoint — motion planner handles speed updates.")
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

        enter_point = points.get('enter', points.get('1'))
        mid_point = points.get('mid', points.get('2'))
        exit_point = points.get('exit', points.get('3'))

        if enter_point is not None:
            p_enter = Point(x=enter_point['x'], y=enter_point['y'], z=enter_point['z'])
            intersection_points.append(nearest_index(p_enter))
        if mid_point is not None:
            p_mid = Point(x=mid_point['x'], y=mid_point['y'], z=mid_point['z'])
            intersection_points.append(nearest_index(p_mid))
        if exit_point is not None:
            p_exit = Point(x=exit_point['x'], y=exit_point['y'], z=exit_point['z'])
            intersection_points.append(nearest_index(p_exit))

        return intersection_points

    def smooth_points(self, points, window_size=5):
        if len(points) < 3:
            return list(points)
        half = max(1, window_size // 2)
        smoothed = []
        for i in range(len(points)):
            start = max(0, i - half)
            end = min(len(points), i + half + 1)
            sx = sum(p.x for p in points[start:end])
            sy = sum(p.y for p in points[start:end])
            sz = sum(p.z for p in points[start:end])
            count = end - start
            smoothed.append(Point(x=sx / count, y=sy / count, z=sz / count))
        return smoothed

    def resample_points(self, points, spacing):
        if len(points) < 2:
            return list(points)
        if spacing <= 0.0:
            return list(points)

        cumulative = [0.0]
        for i in range(1, len(points)):
            p0 = points[i - 1]
            p1 = points[i]
            seg_len = math.sqrt(
                (p1.x - p0.x) ** 2 +
                (p1.y - p0.y) ** 2 +
                (p1.z - p0.z) ** 2
            )
            cumulative.append(cumulative[-1] + seg_len)

        total_len = cumulative[-1]
        if total_len <= 1e-6:
            return [points[0]]

        num_samples = int(total_len // spacing)
        sample_distances = [i * spacing for i in range(num_samples + 1)]
        if sample_distances[-1] < total_len:
            sample_distances.append(total_len)

        resampled = []
        seg_idx = 0
        for d in sample_distances:
            while seg_idx < len(points) - 1 and d > cumulative[seg_idx + 1]:
                seg_idx += 1
            if seg_idx >= len(points) - 1:
                resampled.append(points[-1])
                continue
            p0 = points[seg_idx]
            p1 = points[seg_idx + 1]
            seg_len = cumulative[seg_idx + 1] - cumulative[seg_idx]
            if seg_len <= 1e-6:
                resampled.append(Point(x=p0.x, y=p0.y, z=p0.z))
                continue
            t = (d - cumulative[seg_idx]) / seg_len
            resampled.append(Point(
                x=p0.x + (p1.x - p0.x) * t,
                y=p0.y + (p1.y - p0.y) * t,
                z=p0.z + (p1.z - p0.z) * t,
            ))
        return resampled

    def compute_curves(self, points, curve_calc_dist=6):
        if len(points) < 2 * curve_calc_dist:
            return [0.0 for _ in points]
        curves = [0.0 for _ in points]
        for i in range(curve_calc_dist, len(points) - curve_calc_dist):
            p1 = points[i - curve_calc_dist]
            p2 = points[i]
            p3 = points[i + curve_calc_dist]
            a = math.hypot(p2.x - p1.x, p2.y - p1.y)
            b = math.hypot(p3.x - p2.x, p3.y - p2.y)
            c = math.hypot(p3.x - p1.x, p3.y - p1.y)
            if a < 1e-6 or b < 1e-6 or c < 1e-6:
                continue
            cross = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
            curvature = 2.0 * abs(cross) / (a * b * c)
            curves[i] = curvature
        return curves


    def handle_mission_plan(self):
        if self.base_path_points and self.path_as_lanes:
            self.get_logger().info("received mission plan response")
            smoothed_points = self.smooth_points(self.base_path_points, window_size=5)
            dense_points = self.resample_points(smoothed_points, self.densify_interval)
            self.curves = self.compute_curves(dense_points, self.curve_calc_dist)
            self.path = [
                PlanningWaypoint(
                    waypoint=pt,
                    curve=self.curves[i],
                    speed=float(self.base_max_speed),
                )
                for i, pt in enumerate(dense_points)
            ]
            self.destination = self.path[-1].waypoint if self.path else Point()
            self.speeds_on_path = [float(self.base_max_speed)] * len(self.path)

            self.path_of_waypoints.clear()
            for waypoint in self.path:
                self.path_of_waypoints.append(waypoint.waypoint)

            self.route = self.path_as_lanes[:]
            self.current_lane_index = 0
            self.isPathPlanned = True
            self.mission_plan_requested = False
            self.mission_plan_request_time_ns = None
            self.mission_plan_retry_count = 0
            self.last_closest_point_index = None
            self.publish_path_of_waypoints_markers()
            self.publish_curvature_markers()
            self.publish_smoothed_mission_plan()
            self.log_throttle(
                "info",
                "smoothed_path_pub",
                f"Published smoothed trajectory with {len(self.path)} points",
                period_sec=1.0,
            )

            if self.is_cool4_speed_profile_enable:
                self.intersection_points = self.find_intersection_start_and_exit_using_config(self.path)
                self.get_logger().info(f"Cool4 is enabled -> Read intersection_points: {self.intersection_points}")
                self.publish_intersection_point_markers()
            return True
        return False

    def publish_smoothed_mission_plan(self):
        densified_msg = PlanningInternalMissionPlanMsg()
        densified_msg.path = self.path
        densified_msg.path_as_lanes = self.path_as_lanes
        self.mission_plan_densified_pub.publish(densified_msg)

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

            if i % 5 != 0:
                continue

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

    def curvature_to_color(self, curvature, max_curvature):
        if max_curvature <= 1e-9:
            t = 0.0
        else:
            t = max(0.0, min(1.0, curvature / max_curvature))
        return ColorRGBA(r=t, g=0.2, b=1.0 - t, a=0.9)

    def publish_curvature_markers(self):
        marker_array = MarkerArray()
        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        if not self.path:
            self.curvature_markers_pub.publish(marker_array)
            return

        max_curvature = max((float(getattr(wp, 'curve', 0.0)) for wp in self.path), default=0.0)
        now = self.get_clock().now().to_msg()

        points_marker = Marker()
        points_marker.header.frame_id = "map"
        points_marker.header.stamp = now
        points_marker.ns = "path_curvature"
        points_marker.id = 0
        points_marker.type = Marker.SPHERE_LIST
        points_marker.action = Marker.ADD
        points_marker.pose.orientation.w = 1.0
        points_marker.scale.x = 0.85
        points_marker.scale.y = 0.85
        points_marker.scale.z = 0.85

        text_id = 1
        text_stride = 5
        for i, waypoint_profile in enumerate(self.path):
            waypoint = waypoint_profile.waypoint
            curvature = float(getattr(waypoint_profile, 'curve', 0.0))
            color = self.curvature_to_color(curvature, max_curvature)
            points_marker.points.append(Point(x=waypoint.x, y=waypoint.y, z=waypoint.z))
            points_marker.colors.append(color)

            if i % text_stride != 0:
                continue

            text_marker = Marker()
            text_marker.header.frame_id = "map"
            text_marker.header.stamp = now
            text_marker.ns = "path_curvature_text"
            text_marker.id = text_id
            text_marker.type = Marker.TEXT_VIEW_FACING
            text_marker.action = Marker.ADD
            text_marker.pose.position = Point(
                x=waypoint.x - 0.6,
                y=waypoint.y,
                z=waypoint.z + 1.4
            )
            text_marker.pose.orientation.w = 1.0
            text_marker.scale.z = 0.5
            text_marker.color = color
            text_marker.text = f"{curvature:.3f}"
            marker_array.markers.append(text_marker)
            text_id += 1

        marker_array.markers.append(points_marker)
        self.curvature_markers_pub.publish(marker_array)

    def publish_path_of_waypoints_markers(self):
        if not self.path:
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
        points_marker.scale.x = 1.0
        points_marker.scale.y = 1.0
        points_marker.scale.z = 1.0

        text_id = 1
        text_stride = 5
        for i, waypoint_profile in enumerate(self.path):
            waypoint = waypoint_profile.waypoint
            speed = float(getattr(waypoint_profile, 'speed', self.base_speed))
            points_marker.points.append(Point(x=waypoint.x, y=waypoint.y, z=waypoint.z))
            points_marker.colors.append(self.speed_to_color(speed))

            if i % text_stride == 0:
                text_marker = Marker()
                text_marker.header.frame_id = "map"
                text_marker.header.stamp = now
                text_marker.ns = "path_speed"
                text_marker.id = text_id
                text_marker.type = Marker.TEXT_VIEW_FACING
                text_marker.action = Marker.ADD
                text_marker.pose.position = Point(
                    x=waypoint.x + 0.8,
                    y=waypoint.y,
                    z=waypoint.z + 1.2
                )
                text_marker.pose.orientation.w = 1.0
                text_marker.scale.z = 0.6
                text_marker.color.r = 1.0
                text_marker.color.g = 1.0
                text_marker.color.b = 1.0
                text_marker.color.a = 0.9
                text_marker.text = f"{speed:.1f}"
                marker_array.markers.append(text_marker)
                text_id += 1

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
            (0.1, 0.9, 0.1),  # enter: green
            (0.9, 0.1, 0.1),  # mid: red
            (0.1, 0.3, 0.9),  # exit: blue
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
        if self.pending_reset:
            self.get_logger().warning("RESET")
            self.isPathPlanned = False
            self.cool4_triggered = False
            self.current_lane_index = 0
            self.mission_plan_requested = False
            self.mission_plan_request_time_ns = None
            self.mission_plan_retry_count = 0
            self.path = None
            self.path_as_lanes = None
            self.path_of_waypoints.clear()
            self.speeds_on_path = []
            self.publish_curvature_markers()
            self.pending_reset = False
            self.reset = False
            return
        self.update_pose_from_tf()
        if not self.pose:
            self.get_logger().warning("No pose input")
            return None

        if not self.isPathPlanned:
            if self.reset_cooldown_active():
                return
            if self.mission_plan_requested:
                self.handle_mission_plan()
                if self.isPathPlanned:
                    return
                now_ns = self.get_clock().now().nanoseconds
                if self.mission_plan_request_time_ns is None:
                    self.mission_plan_request_time_ns = now_ns
                    return
                elapsed = (now_ns - self.mission_plan_request_time_ns) / 1e9
                if elapsed < self.mission_plan_retry_delay():
                    return
                self.request_mission_plan()
                self.mission_plan_request_time_ns = now_ns
                self.mission_plan_retry_count += 1
                self.handle_mission_plan()
                return
            self.request_mission_plan()
            self.mission_plan_requested = True
            self.mission_plan_request_time_ns = self.get_clock().now().nanoseconds
            self.handle_mission_plan()
            self.get_logger().info("Start Local Path Planning...")
            if self.path and self.path_as_lanes:
                self.get_logger().info("Path has successfully initialized from Mission Planner")
            return
         
        if self.finished:
            if not self.node_shut:
                self.get_logger().info("Scenario Finished, Parking the Vehicle...")
                self.node_shut = True
                if self.loop_timer is not None:
                    self.loop_timer.cancel()
            return

        if self.reset_cooldown_active():
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
        isEndOfPath = self.end_of_path_detection(current_closest_point_to_vehicle_index)
        if current_closest_point_to_vehicle_index is None:
            self.get_logger().warning("Closest waypoint not set in local planning")
            return

        isTurnDetected = False
        if self.curves and current_closest_point_to_vehicle_index < len(self.curves):
            turn_threshold_rad = math.radians(
                float(self.motion_behavior_config['motion'].get('max_turning_angle', 35.0))
            ) * 0.5
            idx = current_closest_point_to_vehicle_index
            if 0 <= idx - self.curve_calc_dist and idx + self.curve_calc_dist < len(self.path_of_waypoints):
                p1 = self.path_of_waypoints[idx - self.curve_calc_dist]
                p3 = self.path_of_waypoints[idx + self.curve_calc_dist]
                window_len = self.calculate_distance(p1, p3)
            else:
                window_len = self.densify_interval * 2.0 * self.curve_calc_dist
            turn_angle = self.curves[idx] * window_len
            isTurnDetected = turn_angle > turn_threshold_rad

        self.publish_curve_internal_msg(isTurnDetected, isEndOfPath)

        self.get_logger().debug(
            f'current point index:  {current_closest_point_to_vehicle_index}\n'
            f'speed: {self.speeds_on_path[current_closest_point_to_vehicle_index]}\n'
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
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
