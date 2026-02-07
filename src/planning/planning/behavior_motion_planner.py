#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import os
import json
import yaml
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped, Point, Quaternion
from rclpy.duration import Duration as RclpyDuration
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener
from std_msgs.msg import String, ColorRGBA, Bool
import math
from collections import deque
from simple_av_msgs.msg import TrafficSignalsArray
from autoware_perception_msgs.msg import PredictedObjects, DetectedObjects
from simple_av_msgs.msg import PlanningInternalMsg, PlanningInternalMissionPlanMsg, CollisionPredictionInfo, PlanningWaypoint
from simple_av_msgs.msg import LocalizationMsg, LocalizationIntersectionStatus
from simple_av_msgs.msg import SimMonitor, Portal
import numpy as np
from dataclasses import dataclass, field
from scipy.spatial.transform import Rotation as R
from autoware_vehicle_msgs.msg import VelocityReport
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy
from autoware_perception_msgs.msg import TrafficLightGroup, TrafficLightElement
from visualization_msgs.msg import Marker, MarkerArray

@dataclass
class SimpleObject:
    label: int
    position: Point
    orientation: Quaternion
    velocity: float
    distance: float
    size_x: float
    size_y: float
    predicted_paths: list = field(default_factory=list)

class BehaviorMotionPlanning(Node):
    def __init__(self):
        super().__init__('behavior_motion_planner_node')
        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)

        # Load scenario configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.vehicle_model = self.scenario_config['scenario']['vehicle_model']

        # Load the map
        self.map_data = self.load_map_data(self.vehicle_model)
        self.map_data = self.map_data["LaneLetsArray"]

        self.graph = {lanelet['name']: {
            'waypoints': lanelet['waypoints'],
            'nextLanes': lanelet.get('nextLanes', []),
            'prevLanes': lanelet.get('prevLanes', []),
            'adjacentLanes': lanelet.get('adjacentLanes', []),
        } for lanelet in self.map_data}

        # Load av features configs
        self.av_features = self.config_file_loader("av_features.yaml")
        self.use_RSU_for_trafficlight = self.av_features['traffic_light']['use_rsu']
        self.use_RSU_for_object_detection = self.av_features['object_detection']['use_rsu']
        self.is_cool4_speed_profile_enable = self.av_features['use_cool4_speed_profile']['enable']
        self.allowed_object_directions = set(
            self.av_features['object_detection']
            .get('direction_filter', {})
            .get('allowed_directions', ['above', 'NW', 'NE'])
        )
        self.direction_filter_cfg = self.av_features['object_detection'].get('direction_filter', {})
        self.direction_lateral_threshold = float(self.direction_filter_cfg.get('lateral_threshold', 2.25))

        # Cool4 intersection profiles
        self.intersection_profiles = self.load_intersections()
        self.intersection2_scenario2_points = self.intersection_profiles['intersection_points']['2']['2']
        self.intersection_points = []

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
        self.trajectory_length = float(
            self.motion_behavior_config.get('motion', {})
            .get('trajectory', {})
            .get('length', 100.0)
        )
        self.max_lateral_accel = float(self.motion_behavior_config['motion'].get('max_lateral_accel', 4.0))
        self.traffic_light_stop_offset = float(
            self.motion_behavior_config.get('behavior', {})
            .get('traffic_light', {})
            .get('stop_offset', 1.0)
        )

        self.range_low_pass_gain = self.motion_behavior_config['behavior']['range_low_pass_gain'] #meters
        
        self.collision_prediction_saftey_distance = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['safety_distance'] #meters
        self.saftey_distance = self.motion_behavior_config['behavior']['collision_avoidance']['on_path']['safety_distance'] #meters
        self.on_path_avoidance_saftey_distance = self.motion_behavior_config['behavior']['collision_avoidance']['on_path']['safety_distance'] #meters
        self.on_path_distance_threshold = self.motion_behavior_config['behavior']['collision_avoidance']['on_path'].get('path_distance_threshold', 1.5)
        self.on_path_detection_angle_deg = self.motion_behavior_config['behavior']['collision_avoidance']['on_path'].get('detection_angle_deg', 120.0)

        self.reaction_time_threshold = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['reaction_time_threshold'] #meters
        self.prediction_detection_angle_deg = self.motion_behavior_config['behavior']['collision_avoidance']['prediction'].get('detection_angle_deg', 120.0)
        
        self.prediction_reaction_range_C = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['reaction_range']['coefficient']#meters
        self.prediction_reaction_range_B = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['reaction_range']['base']#meters
        self.prediction_detection_range_C = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['detection_range']['coefficient']#meters
        self.prediction_detection_range_B = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['detection_range']['base']#meters
        
        
        self.on_path_detection_range_C = self.motion_behavior_config['behavior']['collision_avoidance']['on_path']['detection_range']['coefficient']#meters
        self.on_path_detection_range_B = self.motion_behavior_config['behavior']['collision_avoidance']['on_path']['detection_range']['base']#meters


        # Subscribe topics
        self.subscriptionVelocityReport = self.create_subscription(VelocityReport, '/vehicle/status/velocity_status', self.velocity_report_callback, 10)
        self.velocity_report = VelocityReport()

        self.subscriptionTrafficSignal = self.create_subscription(TrafficSignalsArray, 'simple_av/perception/traffic_signals', self.trafficSignal_callback, 10)
        self.trafficSignal = TrafficSignalsArray()

        self.subscriptionDetectedObjects = self.create_subscription(
            DetectedObjects,
            'simple_av/perception/obu_sensing',
            self.detectedObjects_callback,
            10
        )
        self.detected_objects = []
        self.subscriptionRsuDanger = self.create_subscription(
            Bool,
            'simple_av/perception/rsu_danger_detected',
            self.rsu_danger_callback,
            10
        )
        self.rsu_danger_detected = False

        self.subscriptionPredictedObjects = self.create_subscription(
            PredictedObjects,
            'simple_av/perception/predicted_objects',
            self.predictedObjects_callback,
            10
        )
        self.predicted_objects = []

        self.pose = PoseStamped()
        self.map_frame = 'map'
        self.base_frame = 'base_link'
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.subscriptionLocation = self.create_subscription(LocalizationMsg, 'simple_av/localization/location', self.location_callback, 10)
        self.location = LocalizationMsg()

        self.subscriptionCurveDetection = self.create_subscription(PlanningInternalMsg, 'simple_av/planning/internal_msg', self.internal_msg_callback, 10)
        self.isTurnDetected = False
        self.isEndOfPath = False

        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False
        self.prev_reset = False
        self.round_number = 0
        self.last_reset_time_ns = None
        self.reset_cooldown = self.scenario_config['scenario'].get('reset_cooldown_seconds', 2.0)

        self.subscriptionSimMonitor = self.create_subscription(SimMonitor, 'simple_av/sim_monitor', self.sim_monitor_callback, 100)
        self.sim_clock_rate = 0

        # Create subscriber to simple_av/localization/intersection_status topic
        self.subscriptionIntersectionAwareness = self.create_subscription(LocalizationIntersectionStatus, 'simple_av/localization/intersection_status', self.intersectionAwareness_callback, 10)
        self.intersection_awareness_intersection_name = None
        self.intersection_awareness_status = None

        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        self.subscription_mission_plan = self.create_subscription(
            PlanningInternalMissionPlanMsg,
            '/simple_av/path_planning/trajectory',
            self.mission_plan_callback,
            qos_profile
        )
        self.mission_plan = PlanningInternalMissionPlanMsg()
        self.path_as_lanes = None  # List of lanes from start lane to destination
        self.path = None  # List of waypoints in order of path_as_lanes
        self.path_of_waypoints = [] # List of waypoints in order of path_as_lanes
        self.max_speeds_on_path = []

        # Publish topics
        self.trajectory_pub = self.create_publisher(
            PlanningInternalMissionPlanMsg,
            '/simple_av/motion_planning/trajectory',
            qos_profile
        )
        self.trajectory_marker_pub = self.create_publisher(
            MarkerArray,
            '/simple_av/motion_planning/visualization/trajectory',
            qos_profile
        )

        self.pub = self.create_publisher(
            TrafficLightGroup,
            '/planning/scenario_planning/lane_driving/behavior_planning/debug/traffic_signal',
            10
        )

        self.collision_info_pub = self.create_publisher(
            CollisionPredictionInfo,
            "simple_av/planning/collision_prediction_info",
            10
        )
        self.range_marker_pub = self.create_publisher(
            MarkerArray,
            "simple_av/visualization/collision_ranges",
            10
        )
        # prediction markers are now published via collision_points marker array
        self.stop_point_marker_pub = self.create_publisher(
            MarkerArray,
            "/simple_av/motion_planning/visualization/stop_points",
            10
        )
        self.collision_points_marker_pub = self.create_publisher(
            MarkerArray,
            "simple_av/motion_planner/visualization/collision_points",
            10
        )

        #Path
        self.isPathPlanned = False
        self.route = None # List of lanes from start lane to destination
        self.current_lane_index = 0
        self.search_depth = 5
        self.destination = Point()
        
        #Observation and detection range
        self.on_path_detection_range = self.base_speed * self.on_path_detection_range_C + self.on_path_detection_range_B # meters
        self.reaction_range = self.base_speed * self.prediction_reaction_range_C + self.prediction_reaction_range_B # meters
        self.detection_range = self.base_speed * self.prediction_detection_range_C + self.prediction_detection_range_B # meters
        self.current_speed = 0.0
        self.latest_collision_point = None
        self.previous_speed_slidingWindow = deque(maxlen=8) # for storing 10 recent previous speed values
        self.previous_speed_slidingWindow.append(0.0)  # initializing the queue
        self.status = String() # Cruise, Decelerate, PrepareToStop, Turn
        self.stop_reason = String() # Cruise, Decelerate, PrepareToStop, Turn

        self.densify_interval = self.motion_behavior_config['motion']['path']['densify_interval']

        # Vehicle dimensions for overlap checks
        self.vehicle_config = self.load_vehicle_config(self.vehicle_model)
        self.ego_length = float(self.vehicle_config['dimensions']['length'])
        self.ego_width = float(self.vehicle_config['dimensions']['width'])
        self.wheel_base = float(self.vehicle_config['dimensions'].get('wheel_base', 0.0))
        self.front_overhang = float(self.vehicle_config['dimensions'].get('front_overhang', 0.0))
        self.NORMAL_ACCEL = float(self.vehicle_config['performance'].get('acceleration_rate', 1.0))
        self.NORMAL_DECEL = float(self.vehicle_config['performance'].get('normal_deceleration_rate', -1.0))
        self.MAX_JERK_ACCEL = float(self.vehicle_config['performance'].get('max_jerk_accel', 0.7))
        self.MAX_JERK_DECEL = float(self.vehicle_config['performance'].get('max_jerk_decel', 0.7))
        self.ACCEL_PROFILE = self.vehicle_config['performance'].get('accel_profile', [])
        # Speed limits come only from motion_behavior_config.yaml
        self.front_offset = self.wheel_base + self.front_overhang
        if self.densify_interval > 0.0:
            self.front_offset_steps = int(self.front_offset / self.densify_interval)
        else:
            self.front_offset_steps = 0
        
        #Traffic light
        self.traffic_light_stopPoint_lastState = Point()
        self.traffic_light_state_lastState = 'Cruise_green'
        self.traffic_light_last_Color = 1

        #Shutting down
        self.node_shut = False
        self._last_log_time = {}
        # Motion planning loop timer (uses ROS time when use_sim_time is enabled)
        self.loop_period_sec = 0.05
        self.loop_timer = self.create_timer(self.loop_period_sec, self.motion_planning)

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
        # json_file_path = os.path.join(package_share_directory, 'resource', 'Shinjuku.json')
        # Load and read the JSON file
        with open(json_file_path, 'r') as json_file:
            map_data = json.load(json_file)
            return map_data

    def load_intersections(self):
        package_share_directory = get_package_share_directory('common')
        zones_path = os.path.join(package_share_directory, "zones", 'intersection_profiles.yaml')
        with open(zones_path, "r") as file:
            intersection_profiles = yaml.safe_load(file)
        return intersection_profiles

    def load_vehicle_config(self, vehicle_model):
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", "vehicle_config.yaml")
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        if vehicle_model in config["vehicles"]:
            return config["vehicles"][vehicle_model]
        raise ValueError(f"Vehicle type '{vehicle_model}' not found in the configuration.")

    def mission_plan_callback(self, msg):
        self.mission_plan = msg
        self.path = self.mission_plan.path
        self.path_as_lanes = list(self.mission_plan.path_as_lanes)
        self.path_of_waypoints = [wp.waypoint for wp in self.path]
        self.max_speeds_on_path = [
            float(getattr(wp, 'speed', self.base_speed)) for wp in self.path
        ]
        if self.is_cool4_speed_profile_enable and self.path:
            self.intersection_points = self.find_intersection_start_and_exit_using_config(self.path)
        if self.path:
            if self.route != self.path_as_lanes:
                self.route = self.path_as_lanes[:]
                self.current_lane_index = 0
            if not self.isPathPlanned:
                self.get_logger().info("Path has successfully initialized from Mission Planner")
                self.isPathPlanned = True
            self.destination = self.path[-1].waypoint
            self.log_throttle(
                "info",
                "path_rx",
                f"Received smoothed path with {len(self.path)} points",
                period_sec=1.0,
            )
    
    def intersectionAwareness_callback(self, msg):
        self.intersection_awareness_intersection_name = msg.intersection_name
        self.intersection_awareness_status = msg.status

    def sim_monitor_callback(self, msg):
        self.sim_clock_rate = msg.sim_clock_rate
    
    def velocity_report_callback(self, msg):
        self.velocity_report = msg
    
    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    
    def portal_callback(self, msg):
        now_ns = self.get_clock().now().nanoseconds
        round_changed = msg.round_number != self.round_number
        reset_edge = msg.reset and not self.prev_reset
        cooldown_ok = (
            self.last_reset_time_ns is None or
            (now_ns - self.last_reset_time_ns) / 1e9 >= self.reset_cooldown
        )
        self.reset = (reset_edge or round_changed) and cooldown_ok
        self.finished = msg.finished
        self.round_number = msg.round_number
        if self.reset:
            self.last_reset_time_ns = now_ns
        self.prev_reset = msg.reset

    def reset_cooldown_active(self):
        if self.last_reset_time_ns is None:
            return False
        now_ns = self.get_clock().now().nanoseconds
        return (now_ns - self.last_reset_time_ns) / 1e9 < self.reset_cooldown

    def internal_msg_callback(self, msg):
        self.isTurnDetected = msg.is_curve_detected
        self.isEndOfPath = msg.is_end_of_path

    def trafficSignal_callback(self, msg):
        self.trafficSignal = msg

    def predictedObjects_callback(self, msg: PredictedObjects):
        objs = []
        for obj in msg.objects:
            label = obj.classification[0].label if obj.classification else 0
            pose = obj.kinematics.initial_pose_with_covariance.pose
            twist = obj.kinematics.initial_twist_with_covariance.twist.linear
            speed = math.sqrt(twist.x ** 2 + twist.y ** 2 + twist.z ** 2)
            distance = math.sqrt(pose.position.x ** 2 + pose.position.y ** 2)
            size_x = float(obj.shape.dimensions.x) if obj.shape and obj.shape.dimensions else 0.0
            size_y = float(obj.shape.dimensions.y) if obj.shape and obj.shape.dimensions else 0.0
            predicted_paths = []
            for pred_path in obj.kinematics.predicted_paths:
                if not pred_path.path:
                    continue
                dt = pred_path.time_step.sec + pred_path.time_step.nanosec * 1e-9
                path_points = [p.position for p in pred_path.path]
                predicted_paths.append((path_points, dt))
            objs.append(SimpleObject(
                label=int(label),
                position=pose.position,
                orientation=pose.orientation,
                velocity=float(speed),
                distance=float(distance),
                size_x=size_x,
                size_y=size_y,
                predicted_paths=predicted_paths,
            ))
        self.predicted_objects = objs

    def rsu_danger_callback(self, msg: Bool):
        self.rsu_danger_detected = bool(msg.data)

    def detectedObjects_callback(self, msg: DetectedObjects):
        objs = []
        for obj in msg.objects:
            label = obj.classification[0].label if obj.classification else 0
            pose = obj.kinematics.pose_with_covariance.pose
            distance = math.sqrt(pose.position.x ** 2 + pose.position.y ** 2)
            size_x = float(obj.shape.dimensions.x) if obj.shape and obj.shape.dimensions else 0.0
            size_y = float(obj.shape.dimensions.y) if obj.shape and obj.shape.dimensions else 0.0
            objs.append(SimpleObject(
                label=int(label),
                position=pose.position,
                orientation=pose.orientation,
                velocity=0.0,
                distance=float(distance),
                size_x=size_x,
                size_y=size_y,
            ))
        self.detected_objects = objs

    def object_direction(self, x, y):
        if y <= self.direction_lateral_threshold and y >= -self.direction_lateral_threshold:
            if x >= 0:
                return 'above'
            return 'behind'
        if y > self.direction_lateral_threshold:
            return 'NW' if x >= 0 else 'SW'
        return 'NE' if x >= 0 else 'SE'

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

    def find_closest_waypoint_index_to_point(self, target_point):
        if not self.path_of_waypoints:
            return None
        min_idx = None
        min_dist = float('inf')
        for i, wp in enumerate(self.path_of_waypoints):
            d = self.calculate_distance(wp, target_point)
            if d < min_dist:
                min_dist = d
                min_idx = i
        return min_idx

    def offset_stop_point_before_line(self, stop_point, offset_m):
        if stop_point is None or not self.path_of_waypoints or offset_m <= 0.0:
            return stop_point
        stop_idx = self.find_closest_waypoint_index_to_point(stop_point)
        if stop_idx is None:
            return stop_point
        offset_idx = int(offset_m / max(self.densify_interval, 1e-6))
        new_idx = max(0, stop_idx - offset_idx)
        return self.path_of_waypoints[new_idx]

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
    
    def get_lane_by_name(self, lane_name):
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
            lane_obj = self.get_lane_by_name(lane)
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
        current_closest_point_to_vehicle = None
        min_path_dist = float('inf')
        for i, wp in enumerate(self.path_of_waypoints):
            d = self.calculate_distance(wp, closest_waypoint_to_vehicle)
            if d < min_path_dist:
                min_path_dist = d
                current_closest_point_to_vehicle = i
        return current_closest_point_to_vehicle

    def update_observation_range(self, speed, is_speed_declining):
        gain = self.range_low_pass_gain if is_speed_declining else 0
        self.on_path_detection_range = (1 - gain) * (speed * self.on_path_detection_range_C + self.on_path_detection_range_B) + gain * self.on_path_detection_range 
        self.reaction_range = (1 - gain) * (speed * self.prediction_reaction_range_C + self.prediction_reaction_range_B) + gain * self.reaction_range # meters
        self.detection_range = (1 - gain) * (speed * self.prediction_detection_range_C + self.prediction_detection_range_B) + gain * self.detection_range # meters

    def adjust_speed_to_curve(self, curvature, max_speed, max_lateral_accel=4.0, min_speed=0.0):
        if curvature <= 1e-6:
            return max_speed
        curvature = max(curvature, 1e-6)
        speed = math.sqrt(max_lateral_accel / curvature)
        speed = min(max_speed, speed)
        if min_speed > 0.0:
            speed = max(min_speed, speed)
        return speed

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
                j_max = self.MAX_JERK_ACCEL if a_des >= 0.0 else abs(self.MAX_JERK_DECEL)

                a_min = a_prev - j_max * waypoint_distance
                a_max = a_prev + j_max * waypoint_distance
                a_clamped = max(a_min, min(a_des, a_max))

                v_new_sq = max(v_prev**2 + 2 * a_clamped * waypoint_distance, 0.0)
                v_new = math.sqrt(v_new_sq)
                output.append(v_new)
                a_prev = a_clamped
                v_prev = v_new
            return output

        forward = forward_pass(speeds)
        backward = list(reversed(forward_pass(list(reversed(forward)))))
        return [min(f, b) for f, b in zip(forward, backward)]

    def build_speed_profile(self, segment, max_speeds, current_speed, stop_idx=None):
        if not segment:
            return []
        waypoint_distance = max(self.densify_interval, 1e-3)
        base_speeds = []
        for i, wp in enumerate(segment):
            max_speed = max_speeds[i] if i < len(max_speeds) else self.base_speed
            max_speed = max(max_speed, 0.0)
            base_speeds.append(
                self.adjust_speed_to_curve(
                    wp.curve,
                    max_speed,
                    self.max_lateral_accel,
                    self.MIN_SPEED,
                )
            )

        speeds = []
        speeds.append(min(base_speeds[0], max(current_speed, 0.0)))
        for i in range(1, len(base_speeds)):
            prev_speed = speeds[-1]
            accel_limit = max(self.get_accel_for_speed(prev_speed), 0.0)
            accel_step = accel_limit * waypoint_distance
            max_next_speed = math.sqrt(prev_speed**2 + 2 * accel_step)
            speeds.append(min(base_speeds[i], max_next_speed, self.MAX_SPEED))

        if stop_idx is not None and 0 <= stop_idx < len(speeds):
            speeds[stop_idx:] = [0.0] * (len(speeds) - stop_idx)
            decel_step = abs(self.NORMAL_DECEL) * waypoint_distance
            for i in reversed(range(stop_idx)):
                next_speed = speeds[i + 1]
                max_prev_speed = math.sqrt(next_speed**2 + 2 * decel_step)
                speeds[i] = min(speeds[i], max_prev_speed, self.MAX_SPEED)

        speeds = self.apply_jerk_limit(speeds, waypoint_distance)
        return speeds

    def publish_trajectory(self, start_idx, stop_idx_global=None):
        if not self.path or start_idx is None:
            return
        steps = int(self.trajectory_length / max(self.densify_interval, 1e-3))
        end_idx = min(len(self.path) - 1, start_idx + steps)
        segment = self.path[start_idx:end_idx + 1]
        max_speeds = self.max_speeds_on_path[start_idx:end_idx + 1] if self.max_speeds_on_path else []

        if (
            self.is_cool4_speed_profile_enable
            and self.intersection_points
            and self.intersection_awareness_intersection_name == '2'
        ):
            cap_speed = self.COOL4_MAX_SPEED if (self.use_RSU_for_object_detection and not self.rsu_danger_detected) else self.COOL4_MIN_SPEED
            start_i, exit_i, _ = self.intersection_points
            overlap_start = max(start_idx, start_i)
            overlap_end = min(end_idx, exit_i)
            if overlap_end > overlap_start:
                for global_idx in range(overlap_start, overlap_end):
                    local_idx = global_idx - start_idx
                    if 0 <= local_idx < len(max_speeds):
                        max_speeds[local_idx] = min(max_speeds[local_idx], cap_speed)

        stop_idx_local = None
        if stop_idx_global is not None and start_idx <= stop_idx_global <= end_idx:
            stop_idx_local = stop_idx_global - start_idx

        speeds = self.build_speed_profile(segment, max_speeds, self.current_speed, stop_idx_local)
        traj_msg = PlanningInternalMissionPlanMsg()
        traj_msg.path_as_lanes = list(self.path_as_lanes) if self.path_as_lanes else []
        traj_msg.path = []
        for i, wp in enumerate(segment):
            speed = speeds[i] if i < len(speeds) else (max_speeds[i] if i < len(max_speeds) else self.base_speed)
            traj_msg.path.append(
                PlanningWaypoint(waypoint=wp.waypoint, curve=wp.curve, speed=float(speed))
            )
        self.trajectory_pub.publish(traj_msg)
        self.publish_trajectory_markers(traj_msg)

    def speed_to_color(self, speed):
        if self.MAX_SPEED <= self.MIN_SPEED:
            t = 0.0
        else:
            t = (speed - self.MIN_SPEED) / (self.MAX_SPEED - self.MIN_SPEED)
        t = max(0.0, min(1.0, t))
        return ColorRGBA(r=t, g=0.2, b=1.0 - t, a=0.9)

    def publish_trajectory_markers(self, traj_msg):
        if not traj_msg.path:
            return
        marker_array = MarkerArray()
        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        now = self.get_clock().now().to_msg()
        points_marker = Marker()
        points_marker.header.frame_id = "map"
        points_marker.header.stamp = now
        points_marker.ns = "motion_planner_trajectory"
        points_marker.id = 0
        points_marker.type = Marker.SPHERE_LIST
        points_marker.action = Marker.ADD
        points_marker.pose.orientation.w = 1.0
        points_marker.scale.x = 1.0
        points_marker.scale.y = 1.0
        points_marker.scale.z = 1.0

        text_id = 1
        text_stride = 5
        for i, wp in enumerate(traj_msg.path):
            waypoint = wp.waypoint
            speed = float(getattr(wp, 'speed', self.base_speed))
            points_marker.points.append(Point(x=waypoint.x, y=waypoint.y, z=waypoint.z))
            points_marker.colors.append(self.speed_to_color(speed))

            if i % text_stride != 0:
                continue

            text_marker = Marker()
            text_marker.header.frame_id = "map"
            text_marker.header.stamp = now
            text_marker.ns = "motion_planner_speed"
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
        self.trajectory_marker_pub.publish(marker_array)

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

    
    def get_traffic_light_color_by_id(self, traffic_light_id):
        if self.intersection_awareness_intersection_name is not None:
            v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
            v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)
            if traffic_light_id in v2i_traffic_signals_id:
                return v2i_traffic_signals_colors[v2i_traffic_signals_id.index(traffic_light_id)]
        return None

    def get_traffic_light_color_by_lane(self, lane_obj):
        current_lane_traffic_light_id = lane_obj['trafficlightsWayIDs']
        v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
        if current_lane_traffic_light_id and current_lane_traffic_light_id[0] in v2i_traffic_signals_id:
            v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)
            return v2i_traffic_signals_colors[v2i_traffic_signals_id.index(current_lane_traffic_light_id[0])]
        return None

    def get_traffic_light_stop_point_by_lane(self, lane_obj):
        stop_point = self.calculate_traffic_light_stop_point(lane_obj['stopLinePoseP1'], lane_obj['stopLinePoseP2'])
        return stop_point

    def publish_rviz_traffic_light_status(self,color):
        msg = TrafficLightGroup()
        msg.traffic_light_group_id = 1

        element = TrafficLightElement()
        element.color = color
        element.shape = TrafficLightElement.CIRCLE
        element.status = TrafficLightElement.SOLID_ON
        element.confidence = 1.0
        msg.elements.append(element)

        self.pub.publish(msg)
        self.get_logger().debug("Published RViZ traffic light status")

    def manage_traffic_lights(self, current_lane_obj):
        v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
        v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)
        if not v2i_traffic_signals_id: # ego vehicle is out of intersection zone
            self.publish_rviz_traffic_light_status(0)

        current_lane_traffic_light_id = current_lane_obj['trafficlightsRelationID']
        if current_lane_traffic_light_id: # this lane have a traffic light
            if current_lane_traffic_light_id[0] in v2i_traffic_signals_id: # traffic light id is on the list
                color = v2i_traffic_signals_colors[v2i_traffic_signals_id.index(current_lane_traffic_light_id[0])]
                self.publish_rviz_traffic_light_status(color)
                stop_point = self.get_traffic_light_stop_point_by_lane(current_lane_obj)
                self.traffic_light_stopPoint_lastState = stop_point
                if color == 1 or color == 2:
                    self.traffic_light_state_lastState = 'Stop_red'
                    return 'Stop_red', stop_point, current_lane_traffic_light_id[0]
                self.traffic_light_state_lastState = 'Cruise_green'
                return 'Cruise_green', None, current_lane_traffic_light_id[0]

        return 'Cruise', None, None
        

    def filter_objects_by_range_and_angle(self, objects, max_range, fov_deg):
        if not objects:
            self.get_logger().debug("no object detected!")
            return None
        half_fov = math.radians(fov_deg / 2.0)
        objects_ahead = []
        for obj in objects:
            dx = obj.position.x
            dy = obj.position.y
            dist = obj.distance if obj.distance is not None else math.sqrt(dx ** 2 + dy ** 2)
            if dist > max_range:
                continue
            if dx <= 0.0:
                continue
            angle = abs(math.atan2(dy, dx))
            if angle <= half_fov:
                objects_ahead.append(obj)
        return objects_ahead
        
    def get_objects_in_range(self, objects_ahead, filter_dist):
        if not objects_ahead:
            self.get_logger().debug("No Object ahead")
            return None            
        objects_in_range = []
        for obj in objects_ahead:
            if obj.distance <= filter_dist: objects_in_range.append(obj)

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
        obj_x = vehicle_pose.x + rotated_vector.x
        obj_y = vehicle_pose.y + rotated_vector.y
        obj_z = vehicle_pose.z + rotated_vector.z

        # Create the absolute position
        object_absolute_pose = Point(x=obj_x, y=obj_y, z=obj_z)
        return object_absolute_pose

    def get_detected_pedestrians(self, objects):
        """
        Get detected pedestrians and cyclists from perception data.
        Returns a list of detected objects with labels:
        - 7: Cyclist/Bicycle & Pedestrian
        """
        if not objects:
            return []
        detected_pedestrians = []
        for obj in objects:
            # Label is int32, check for pedestrian and cyclist (7)
            if obj.label in [7]:
                detected_pedestrians.append(obj)

        if detected_pedestrians:
            self.get_logger().debug(f"DEBUG - ped : Found {len(detected_pedestrians)} pedestrians/cyclists")

        return detected_pedestrians

    def get_path_yaw(self, waypoint_index):
        if len(self.path_of_waypoints) < 2:
            return 0.0
        if waypoint_index < len(self.path_of_waypoints) - 1:
            p1 = self.path_of_waypoints[waypoint_index]
            p2 = self.path_of_waypoints[waypoint_index + 1]
        else:
            p1 = self.path_of_waypoints[waypoint_index - 1]
            p2 = self.path_of_waypoints[waypoint_index]
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        if abs(dx) < 1e-6 and abs(dy) < 1e-6:
            return 0.0
        return math.atan2(dy, dx)

    def is_overlapping_at_waypoint(self, object_position, obj, waypoint, yaw):
        dx = object_position.x - waypoint.x
        dy = object_position.y - waypoint.y
        cos_y = math.cos(-yaw)
        sin_y = math.sin(-yaw)
        x_local = dx * cos_y - dy * sin_y
        y_local = dx * sin_y + dy * cos_y

        ego_half_x = self.ego_length / 2.0
        ego_half_y = self.ego_width / 2.0
        obj_half_x = max(obj.size_x, 0.0) / 2.0
        obj_half_y = max(obj.size_y, 0.0) / 2.0

        return (
            abs(x_local) <= (ego_half_x + obj_half_x) and
            abs(y_local) <= (ego_half_y + obj_half_y)
        )
    
    def find_nearest_obstacle_on_path(self, objects_in_range, current_closest_waypoint_to_vehicle_index, vehicle_pose):
        """
        Find the nearest obstacle that lies on the path ahead of the vehicle.
        Returns:
            {
                "object": <object_msg>,
                "waypoint": <waypoint_point>
            }
        or None if no object lies on the path.
        """

        # Transform objects into global coordinates
        objects_absolute_positions = [
            self.get_object_absolute_position(self.pose.pose.orientation, vehicle_pose, obj.position)
            for obj in objects_in_range
        ]

        start_idx = min(
            len(self.path_of_waypoints) - 1,
            current_closest_waypoint_to_vehicle_index + self.front_offset_steps
        )
        end_idx = min(
            len(self.path_of_waypoints) - 1,
            start_idx + int(self.on_path_detection_range / self.densify_interval) + 1
        )

        candidates = []  # (object, waypoint, dist_vehicle_to_waypoint, object_global_pos)

        # Check each object against path waypoints
        for i, obj in enumerate(objects_in_range):
            obj_global_pos = objects_absolute_positions[i]

            for wp_idx in range(start_idx, end_idx + 1):
                waypoint = self.path_of_waypoints[wp_idx]
                dist_obj_to_wp = self.calculate_distance(obj_global_pos, waypoint)

                # Object is considered near the path if it sits close to any waypoint
                if dist_obj_to_wp <= self.on_path_distance_threshold:
                    yaw = self.get_path_yaw(wp_idx)
                    if not self.is_overlapping_at_waypoint(obj_global_pos, obj, waypoint, yaw):
                        continue

                    # distance from vehicle → waypoint determines the nearest obstacle
                    dist_vehicle_to_wp = self.calculate_distance(vehicle_pose, waypoint)

                    candidates.append((obj, waypoint, dist_vehicle_to_wp, obj_global_pos))
                    break  # Go to next object once a waypoint match is found

        # No objects lying on the path
        if not candidates:
            return None

        # Select nearest object by vehicle distance
        obj, wp, _, obj_global_pos = min(candidates, key=lambda x: x[2])

        return {
            "object": obj,
            "waypoint": wp,
            "object_position": obj_global_pos,
        }

    
    def calculate_traffic_light_stop_point(self, p1, p2):
        return Point(x=(p1[0] + p2[0])/2, y=(p1[1] + p2[1])/2, z=(p1[2] + p2[2])/2)
    
    
    def find_intersection_point(self, object_pose, object_forward_vector, waypoint1, waypoint2):
        # Extract components
        x1, y1 = object_pose.x, object_pose.y
        a1, b1 = object_forward_vector
        x2, y2 = waypoint1.x, waypoint1.y
        x3, y3 = waypoint2.x, waypoint2.y

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
            self.get_logger().debug("Parallel lines")
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
        return Point(x=x, y=y, z=waypoint1.z)

    def dot_product(self, v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]

    def is_point_on_segment(self, object_pose, collison_point, waypoint1, waypoint2, forward_vector):
        # Unpack the intersection point and the waypoints
        x1, y1 = waypoint1.x, waypoint1.y
        x2, y2 = waypoint2.x, waypoint2.y
        x3, y3 = object_pose.x, object_pose.y

        object_to_intersect_vector = [collison_point.x-x3, collison_point.y-y3]
        # Check if the collison_point point is within the bounds of the segment
        if min(x1, x2) <= collison_point.x <= max(x1, x2) and min(y1, y2) <= collison_point.y <= max(y1, y2):
            if self.dot_product(object_to_intersect_vector, forward_vector) >= 0:
                return True  # collison_point point is on the segment
        return False  # collison_point point is outside the segment
        
    def get_forward_vector(self, quaternion):
        local_forward = np.array([1, 0, 0])
        # Convert the quaternion to a rotation object
        rotation = R.from_quat(np.array([quaternion.x, quaternion.y, quaternion.z, quaternion.w]))  # Quaternion format: [x, y, z, w]
        # Apply the rotation to the local forward vector
        global_forward = rotation.apply(local_forward)
        return global_forward [:2]

    def find_segment_intersection(self, p1, p2, q1, q2, eps=1e-6):
        denom = (p1.x - p2.x) * (q1.y - q2.y) - (p1.y - p2.y) * (q1.x - q2.x)
        if abs(denom) < eps:
            return None
        det_p = p1.x * p2.y - p1.y * p2.x
        det_q = q1.x * q2.y - q1.y * q2.x
        x = (det_p * (q1.x - q2.x) - (p1.x - p2.x) * det_q) / denom
        y = (det_p * (q1.y - q2.y) - (p1.y - p2.y) * det_q) / denom
        if (x < min(p1.x, p2.x) - eps or x > max(p1.x, p2.x) + eps or
                y < min(p1.y, p2.y) - eps or y > max(p1.y, p2.y) + eps):
            return None
        if (x < min(q1.x, q2.x) - eps or x > max(q1.x, q2.x) + eps or
                y < min(q1.y, q2.y) - eps or y > max(q1.y, q2.y) + eps):
            return None
        return Point(x=x, y=y, z=q1.z)

    def get_predicted_path_time(self, path_points, dt, segment_index, collision_point):
        if dt is None or dt <= 0.0:
            return None
        seg_len = self.calculate_distance(path_points[segment_index], path_points[segment_index + 1])
        if seg_len < 1e-6:
            frac = 0.0
        else:
            frac = self.calculate_distance(path_points[segment_index], collision_point) / seg_len
        return (segment_index + frac) * dt
    
    def get_time_to_collison(self, current_pose, collision_point, speed):
        if speed == 0.0:
            return float('inf')  # Return infinity to indicate no collision
        dist = self.calculate_distance(collision_point, current_pose)
        time_to_collision = dist / speed
        time_to_collision = time_to_collision * self.sim_clock_rate
        return time_to_collision

    def will_collide_on_path_in_threshold(self, object_type, object_speed, object_pose, vehicle_pose, collison_point, corresponding_waypoint):
        current_vehicle_speed = self.velocity_report.longitudinal_velocity if self.velocity_report else 0.0   
        current_vehicle_speed = current_vehicle_speed if current_vehicle_speed > 1.5 else 1.5
        t_vehicle = self.get_time_to_collison(vehicle_pose, collison_point, current_vehicle_speed)

        t_object = self.get_time_to_collison(object_pose, collison_point, object_speed)

        if abs(t_vehicle - t_object) <= self.reaction_time_threshold:
            self.get_logger().debug(f"CP - Vehciel moving - Potential collision detected! Time difference: {abs(t_vehicle - t_object):.2f} seconds.")
            return True
        return False
    
    def get_stop_point_by_safety_distance(self, event_waypoint, vehicle_pose, collision_avoidance_type):
        # Helper function to calculate distances
        saftey_distance = self.motion_behavior_config['behavior']['collision_avoidance'][collision_avoidance_type]['safety_distance'] #meters
        if self.intersection_awareness_intersection_name == "2" and collision_avoidance_type == "prediction": #TODO: clean this
            saftey_distance = 4.0
        dist_to_waypoint = self.calculate_distance(event_waypoint, vehicle_pose)
        if dist_to_waypoint <= saftey_distance: # Stop the vehicle if distance to the object is less that safety distance
            self.get_logger().debug("CP - INSTANT STOP!!")
            return (vehicle_pose, event_waypoint)

        stop_point_index = self.path_of_waypoints.index(event_waypoint) - int(saftey_distance/self.densify_interval)
        stop_point = self.path_of_waypoints[stop_point_index]
        return (Point(x=stop_point.x, y=stop_point.y, z=stop_point.z), event_waypoint)
         
    def on_path_collision_avoidance(self, objects_ahead, current_closest_waypoint_to_vehicle_index, vehicle_pose):
        objects_in_range = self.get_objects_in_range(objects_ahead, self.on_path_detection_range)
        if not objects_in_range:
            return None
        closest_object_info = self.find_nearest_obstacle_on_path(objects_in_range, current_closest_waypoint_to_vehicle_index, vehicle_pose)
        # return False, None, 'Cruise'
        if not closest_object_info:
            self.get_logger().debug("No Immediate danger")
            return None
        self.get_logger().debug("Imediate threat. Objects ahead in danger zone")
        stop_point, event_waypoint = self.get_stop_point_by_safety_distance(closest_object_info['waypoint'], vehicle_pose, 'on_path')
        return (
            stop_point,
            event_waypoint,
            closest_object_info.get('object_position'),
            closest_object_info['object'],
        )
    
    def publish_collision_info(self, abs_pos, ttc, label, velocity):
        msg = CollisionPredictionInfo()
        msg.object_position = Point(
            x=abs_pos.x,
            y=abs_pos.y,
            z=abs_pos.z
        )
        msg.time_to_collision = ttc
        msg.object_label = label
        msg.object_velocity = velocity
        msg.collision_detected = True

        self.collision_info_pub.publish(msg)
    
    def publish_empty_collision_info(self):
        msg = CollisionPredictionInfo()
        msg.object_position = Point(x=0.0, y=0.0, z=0.0)
        msg.time_to_collision = 0.0
        msg.object_label = 0
        msg.object_velocity = 0.0
        msg.collision_detected = False

        self.collision_info_pub.publish(msg)

    def publish_range_markers(self, vehicle_pose):
        marker_array = MarkerArray()
        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        now = self.get_clock().now().to_msg()
        ranges = [
            ("on_path_detection", self.on_path_detection_range, ColorRGBA(r=1.0, g=0.6, b=0.0, a=0.9)),
            ("reaction_range", self.reaction_range, ColorRGBA(r=1.0, g=1.0, b=0.0, a=0.9)),
            ("detection_range", self.detection_range, ColorRGBA(r=0.2, g=0.6, b=1.0, a=0.9)),
        ]

        for idx, (ns, radius, color) in enumerate(ranges):
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = now
            marker.ns = ns
            marker.id = idx
            marker.type = Marker.LINE_STRIP
            marker.action = Marker.ADD
            marker.pose.orientation.w = 1.0
            marker.scale.x = 0.2
            marker.color = color

            segments = 36
            for i in range(segments + 1):
                angle = 2.0 * math.pi * i / segments
                x = vehicle_pose.x + radius * math.cos(angle)
                y = vehicle_pose.y + radius * math.sin(angle)
                marker.points.append(Point(x=x, y=y, z=vehicle_pose.z))

            marker_array.markers.append(marker)

        self.range_marker_pub.publish(marker_array)

    def publish_stop_point_marker(self, stop_point, stop_reason):
        marker_array = MarkerArray()
        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        if stop_point is None:
            self.stop_point_marker_pub.publish(marker_array)
            return

        now = self.get_clock().now().to_msg()

        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = now
        marker.ns = "stop_point"
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position = stop_point
        marker.pose.orientation.w = 1.0
        marker.scale.x = 2.0
        marker.scale.y = 2.0
        marker.scale.z = 2.0
        reason = (stop_reason or "unknown").lower()
        if "collision avoidance" in reason:
            color = ColorRGBA(r=1.0, g=0.2, b=0.2, a=0.9)
        elif "collision prediction" in reason:
            color = ColorRGBA(r=1.0, g=0.6, b=0.1, a=0.9)
        elif "stop_red" in reason or "stop red" in reason:
            color = ColorRGBA(r=1.0, g=0.9, b=0.1, a=0.9)
        elif "park" in reason:
            color = ColorRGBA(r=0.2, g=0.5, b=1.0, a=0.9)
        elif "reset" in reason:
            color = ColorRGBA(r=0.6, g=0.6, b=0.6, a=0.6)
        else:
            color = ColorRGBA(r=0.9, g=0.9, b=0.9, a=0.9)
        marker.color = color
        marker_array.markers.append(marker)

        text_marker = Marker()
        text_marker.header.frame_id = "map"
        text_marker.header.stamp = now
        text_marker.ns = "stop_reason"
        text_marker.id = 1
        text_marker.type = Marker.TEXT_VIEW_FACING
        text_marker.action = Marker.ADD
        text_marker.pose.position.x = stop_point.x
        text_marker.pose.position.y = stop_point.y
        text_marker.pose.position.z = stop_point.z + 3.0
        text_marker.pose.orientation.w = 1.0
        text_marker.scale.z = 1.2
        text_marker.color.a = 1.0
        text_marker.color.r = 1.0
        text_marker.color.g = 1.0
        text_marker.color.b = 1.0
        text_marker.text = stop_reason if stop_reason else "unknown"
        marker_array.markers.append(text_marker)

        self.stop_point_marker_pub.publish(marker_array)

    def publish_collision_points_markers(self, candidate_events, selected_event):
        marker_array = MarkerArray()
        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        if not candidate_events:
            self.collision_points_marker_pub.publish(marker_array)
            return

        colors = {
            "on_path": ColorRGBA(r=1.0, g=0.2, b=0.2, a=0.9),
            "collision_prediction": ColorRGBA(r=1.0, g=0.6, b=0.1, a=0.9),
            "traffic_light": ColorRGBA(r=1.0, g=1.0, b=0.2, a=0.9),
            "destination": ColorRGBA(r=0.2, g=0.6, b=1.0, a=0.9),
        }

        now = self.get_clock().now().to_msg()
        marker_id = 0
        for event in candidate_events:
            stop_point = event.get("stop_point")
            if stop_point is None:
                continue
            event_type = event.get("type", "unknown")
            reason = event.get("reason", event_type)
            color = colors.get(event_type, ColorRGBA(r=1.0, g=1.0, b=1.0, a=0.9))

            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = now
            marker.ns = "collision_points"
            marker.id = marker_id
            marker_id += 1
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            marker.pose.position = stop_point
            marker.pose.orientation.w = 1.0
            marker.scale.x = 1.5
            marker.scale.y = 0.2
            marker.scale.z = 2.0
            marker.color = color

            if selected_event and selected_event.get("stop_point") == stop_point:
                marker.scale.x = 2.0
                marker.scale.y = 0.3
                marker.scale.z = 2.5

            marker_array.markers.append(marker)

            text_marker = Marker()
            text_marker.header.frame_id = "map"
            text_marker.header.stamp = now
            text_marker.ns = "collision_points_text"
            text_marker.id = marker_id
            marker_id += 1
            text_marker.type = Marker.TEXT_VIEW_FACING
            text_marker.action = Marker.ADD
            text_marker.pose.position.x = stop_point.x
            text_marker.pose.position.y = stop_point.y
            text_marker.pose.position.z = stop_point.z + 3.0
            text_marker.pose.orientation.w = 1.0
            text_marker.scale.z = 1.0
            text_marker.color.a = 1.0
            text_marker.color.r = 1.0
            text_marker.color.g = 1.0
            text_marker.color.b = 1.0
            text_marker.text = reason
            marker_array.markers.append(text_marker)

            object_position = event.get("object_position")
            if object_position is not None:
                obj_marker = Marker()
                obj_marker.header.frame_id = "map"
                obj_marker.header.stamp = now
                obj_marker.ns = "collision_objects"
                obj_marker.id = marker_id
                marker_id += 1
                obj_marker.type = Marker.CUBE
                obj_marker.action = Marker.ADD
                obj_marker.pose.position = object_position
                obj_marker.pose.orientation.w = 1.0
                obj_marker.scale.x = 1.0
                obj_marker.scale.y = 0.2
                obj_marker.scale.z = 1.2
                obj_marker.color = ColorRGBA(r=0.9, g=0.2, b=0.8, a=0.9)
                marker_array.markers.append(obj_marker)

                obj_text = Marker()
                obj_text.header.frame_id = "map"
                obj_text.header.stamp = now
                obj_text.ns = "collision_objects_text"
                obj_text.id = marker_id
                marker_id += 1
                obj_text.type = Marker.TEXT_VIEW_FACING
                obj_text.action = Marker.ADD
                obj_text.pose.position.x = object_position.x
                obj_text.pose.position.y = object_position.y
                obj_text.pose.position.z = object_position.z + 2.0
                obj_text.pose.orientation.w = 1.0
                obj_text.scale.z = 0.9
                obj_text.color.a = 1.0
                obj_text.color.r = 1.0
                obj_text.color.g = 1.0
                obj_text.color.b = 1.0
                obj_text.text = "colliding_object"
                marker_array.markers.append(obj_text)

        self.collision_points_marker_pub.publish(marker_array)


    def predict_nearest_collision(self, objects_ahead, current_closest_waypoint_to_vehicle_index, vehicle_pose):
        """
        Predict potential collisions with objects ahead of the vehicle.
        Returns the nearest stop point and its object_occupied_waypoint_index.
        """
        candidates = []  # store (stop_point, object_occupied_wp_index, distance_to_vehicle)
        ttc_candidates = []   # (|t_vehicle - t_object|, abs_pos, label, velocity)

        # Get only objects within detection range
        objects_in_range = self.get_objects_in_range(objects_ahead, self.detection_range)
        if not objects_in_range:
            self.publish_empty_collision_info()
            return None

        # Extract waypoints ahead starting from the front of the vehicle
        start_idx = min(
            len(self.path_of_waypoints) - 1,
            current_closest_waypoint_to_vehicle_index + self.front_offset_steps
        )
        waypoints = self.path_of_waypoints[
            start_idx:
            start_idx + int(self.reaction_range / self.densify_interval) + 1
        ]

        for obj in objects_in_range:
            if not obj.predicted_paths:
                continue

            for path_points, dt in obj.predicted_paths:
                if len(path_points) < 2:
                    continue

                abs_points = [
                    self.get_object_absolute_position(self.pose.pose.orientation, vehicle_pose, p)
                    for p in path_points
                ]

                for k in range(len(abs_points) - 1):
                    p1 = abs_points[k]
                    p2 = abs_points[k + 1]

                    for j in range(1, len(waypoints) - 1):
                        w1 = waypoints[j]
                        w2 = waypoints[j + 1]
                        collide_point = self.find_segment_intersection(p1, p2, w1, w2)
                        if not collide_point:
                            continue

                        current_vehicle_speed = self.velocity_report.longitudinal_velocity if self.velocity_report else 0.0
                        current_vehicle_speed = current_vehicle_speed if current_vehicle_speed > 1.5 else 1.5
                        t_vehicle = self.get_time_to_collison(vehicle_pose, collide_point, current_vehicle_speed)

                        t_object = self.get_predicted_path_time(abs_points, dt, k, collide_point)
                        if t_object is None:
                            t_object = self.get_time_to_collison(abs_points[0], collide_point, obj.velocity)

                        ttc_diff = abs(t_vehicle - t_object)
                        ttc_candidates.append((ttc_diff, abs_points[0], obj.label, obj.velocity))

                        if ttc_diff <= self.reaction_time_threshold:
                            self.get_logger().debug('P - Collide predicted!!!')
                            stop_point, event_waypoint = self.get_stop_point_by_safety_distance(w1, vehicle_pose, 'prediction')

                            distance = self.calculate_distance(stop_point, vehicle_pose)
                            candidates.append((
                                stop_point,
                                event_waypoint,
                                distance,
                                ttc_diff,
                                abs_points[0],
                                obj.label,
                                obj.velocity,
                                collide_point
                            ))
                            break

        # No collision candidates → publish smallest time-to-collision
        if not candidates:
            if ttc_candidates:
                # Smallest TTC object (closest timing collision)
                best_ttc, abs_pos, label, velocity = min(ttc_candidates, key=lambda x: x[0])
                self.publish_collision_info(abs_pos, best_ttc, label, velocity)
            else:
                # No TTC objects → publish empty message
                self.publish_empty_collision_info()

            return None

        # Pick nearest collision stop point
        nearest = min(candidates, key=lambda x: x[2])  # x[2] = distance
        stop_point, event_waypoint, distance, best_ttc, abs_pos, label, velocity, collision_point = nearest

        # Publish TTC information of the *nearest collision object*
        self.publish_collision_info(abs_pos, best_ttc, label, velocity)
        return (stop_point, event_waypoint)


    def collison_prediction_core(self, objects_ahead, current_closest_waypoint_to_vehicle_index, vehicle_pose, current_lane_traffic_light_id):
        """
        High-level collision prediction logic with traffic light awareness.
        Decides whether to run collision prediction based on RSU traffic light data.
        """

        if self.use_RSU_for_trafficlight:
            self.get_logger().debug(
                f"collision prediction: using RSU for traffic light {self.use_RSU_for_trafficlight}"
            )

            if self.intersection_awareness_intersection_name is not None:
                if self.intersection_awareness_intersection_name == "1":
                    current_lane_traffic_light_color = self.get_traffic_light_color_by_id(current_lane_traffic_light_id)
                    light_166893 = self.get_traffic_light_color_by_id(166893) # opposite side of the intersection
                    light_165709 = self.get_traffic_light_color_by_id(165709) # adjacent side of the intersection


                    # TODO: add lane polygons to determine if the ego vehicle is inside or outside the intersection
                    if current_lane_traffic_light_color in [1,2]: # the Ego vehicle traffic light is red
                        pedestrians = self.get_detected_pedestrians(objects_ahead)
                        return self.predict_nearest_collision(pedestrians, current_closest_waypoint_to_vehicle_index, vehicle_pose)
                    if current_lane_traffic_light_color in [3] and light_166893 in [3]:
                        return self.predict_nearest_collision(objects_ahead, current_closest_waypoint_to_vehicle_index, vehicle_pose)
                    elif current_lane_traffic_light_color in [3] and light_166893 in [1,2]:
                        pedestrians = self.get_detected_pedestrians(objects_ahead)
                        return self.predict_nearest_collision(pedestrians, current_closest_waypoint_to_vehicle_index, vehicle_pose)

                
                if self.intersection_awareness_intersection_name == "2":
                    current_lane_traffic_light_color = self.get_traffic_light_color_by_id(current_lane_traffic_light_id)
                    light_166922 = self.get_traffic_light_color_by_id(166922)
                    light_166940 = self.get_traffic_light_color_by_id(166940)
                    self.get_logger().debug("collision prediction in intersection #2")
                    self.get_logger().debug(
                        "165626: "
                        f"{current_lane_traffic_light_color}, "
                        f"166922: {light_166922}, "
                        f"166940: {light_166940}"
                    )

                    if current_lane_traffic_light_color in [3]: # if the ego vehicle traffic light is green, other traffic lights are red.
                        self.get_logger().debug("light_165626 is green")
                        pedestrians = self.get_detected_pedestrians(objects_ahead)
                        self.get_logger().debug(
                            f"number of detected pedestrians: {len(pedestrians)}"
                        )
                        return self.predict_nearest_collision(pedestrians, current_closest_waypoint_to_vehicle_index, vehicle_pose)
                        
        # Default: always try to predict collisions
        self.get_logger().debug("NORMAL PREDICT")
        return self.predict_nearest_collision(objects_ahead, current_closest_waypoint_to_vehicle_index, vehicle_pose)


    def find_closest_stop_point(self, traffic_light_stopPoint, on_path_collision_avoidance_result, collision_prediction_result, destination_stopPoint, vehicle_pose):
        """
        Returns:
        {
            "type": "on_path" | "collision_prediction" | "traffic_light",
            "event_waypoint": waypoint,
            "stop_point": stop_point
        }
        or None if no event exists.
        """

        stop_points = {}
        candidate_events = []

        # -------------------------------
        # 1. On-path collision
        # -------------------------------
        if on_path_collision_avoidance_result:
            on_path_collision_stop_point, obstacle_occupied_wp, _, _ = on_path_collision_avoidance_result
            distance_to_obstacle = self.calculate_distance(vehicle_pose, obstacle_occupied_wp)
            distance_to_stop_point = self.calculate_distance(vehicle_pose, on_path_collision_stop_point)
            candidate_events.append({
                "type": "on_path",
                "event_distance": distance_to_obstacle,
                "stop_point": on_path_collision_stop_point,
                "stop_point_distance": distance_to_stop_point
            })

        # -------------------------------
        # 2. Collision prediction
        # -------------------------------
        if collision_prediction_result:
            collision_prediction_stop_point, predicted_collision_wp = collision_prediction_result
            distance_to_predicted_collision_wp = self.calculate_distance(vehicle_pose, predicted_collision_wp)
            distance_to_stop_point = self.calculate_distance(vehicle_pose, collision_prediction_stop_point)
            candidate_events.append({
                "type": "collision_prediction",
                "event_distance": distance_to_predicted_collision_wp,
                "stop_point": collision_prediction_stop_point,
                "stop_point_distance": distance_to_stop_point
            })

        # -------------------------------
        # 3. Traffic Light Stop
        # -------------------------------
        if traffic_light_stopPoint:
            distance_to_stop_point = self.calculate_distance(vehicle_pose, traffic_light_stopPoint)
            candidate_events.append({
                "type": "traffic_light",
                "event_distance": distance_to_stop_point,
                "stop_point": traffic_light_stopPoint,
                "stop_point_distance": distance_to_stop_point
            })

        # -------------------------------
        # 4. Destination
        # -------------------------------
        if destination_stopPoint:
            distance_to_destination = self.calculate_distance(vehicle_pose, destination_stopPoint)
            candidate_events.append({
                "type": "Destination",
                "event_distance": distance_to_destination,
                "stop_point": destination_stopPoint,
                "stop_point_distance": distance_to_destination
            })

        # Nothing found
        if not candidate_events:
            return None

        # -------------------------------------------------------------
        # SPECIAL CASE: Traffic light + at least one collision event
        # Select nearest based on EVENT distance (not stop_point distance)
        # -------------------------------------------------------------
        if traffic_light_stopPoint and (on_path_collision_avoidance_result or collision_prediction_result):
            closest_event = min(candidate_events, key=lambda x: x["event_distance"])
            return closest_event

        # -------------------------------------------------------------
        # DEFAULT CASE: choose based on stop_point distance
        # -------------------------------------------------------------
        closest_event = min(candidate_events, key=lambda x: x["stop_point_distance"])
        return closest_event



    def get_current_lane_name(self):
        try:
            lane_index = self.route.index(self.location.closest_lane_names.data)
            current_lane = self.route[lane_index]
        except:
            current_lane = self.route[self.current_lane_index]
        
        return current_lane
    

    def motion_planner(self, current_closest_waypoint_to_vehicle_index):
        # Current vehicle position
        vehicle_pose = self.pose.pose.position

        # Distance to the destination
        # distance_to_destination = self.calculate_distance(vehicle_pose, self.destination)

        current_lane_name = self.get_current_lane_name()
        current_lane_obj = self.get_lane_by_name(current_lane_name)

        # Traffic light detection
        trafficLightTask, traffic_light_stopPoint, current_lane_traffic_light_id = self.manage_traffic_lights(current_lane_obj)
        self.get_logger().debug(f"DEBUG_trafficlight - trafficLightTask: {trafficLightTask} - traffic_light_stopPoint: {traffic_light_stopPoint}")
        if trafficLightTask == 'Stop_red' and traffic_light_stopPoint is not None:
            stop_line_idx = self.find_closest_waypoint_index_to_point(traffic_light_stopPoint)
            if stop_line_idx is not None and current_closest_waypoint_to_vehicle_index >= stop_line_idx:
                self.get_logger().debug("Passed stop line on red/yellow -> proceed through intersection")
                trafficLightTask = 'Cruise'
                traffic_light_stopPoint = None
            else:
                traffic_light_stopPoint = self.offset_stop_point_before_line(
                    traffic_light_stopPoint,
                    self.traffic_light_stop_offset
                )
        # Collision avoidance
        objects_ahead_detected = self.filter_objects_by_range_and_angle(
            self.detected_objects,
            self.on_path_detection_range,
            self.on_path_detection_angle_deg,
        )
        objects_ahead_predicted = self.filter_objects_by_range_and_angle(
            self.predicted_objects,
            self.detection_range,
            self.prediction_detection_angle_deg,
        )
        on_path_collision_avoidance_result = self.on_path_collision_avoidance(objects_ahead_detected, current_closest_waypoint_to_vehicle_index, vehicle_pose)
        prediction_result = self.collison_prediction_core(objects_ahead_predicted, current_closest_waypoint_to_vehicle_index, vehicle_pose, current_lane_traffic_light_id)
        closest_event = self.find_closest_stop_point(traffic_light_stopPoint, on_path_collision_avoidance_result, prediction_result, self.destination, vehicle_pose)

        candidate_events = []
        if on_path_collision_avoidance_result:
            on_path_stop_point, _, on_path_object_pos, on_path_object = on_path_collision_avoidance_result
            candidate_events.append({
                "type": "on_path",
                "stop_point": on_path_stop_point,
                "reason": "collision_avoidance",
                "object_position": on_path_object_pos,
                "object_label": on_path_object.label if on_path_object else None,
            })
        if prediction_result:
            prediction_stop_point, _ = prediction_result
            candidate_events.append({
                "type": "collision_prediction",
                "stop_point": prediction_stop_point,
                "reason": "collision_prediction",
            })
        if traffic_light_stopPoint:
            candidate_events.append({
                "type": "traffic_light",
                "stop_point": traffic_light_stopPoint,
                "reason": trafficLightTask,
            })
        if self.destination:
            candidate_events.append({
                "type": "destination",
                "stop_point": self.destination,
                "reason": "destination",
            })
        
        self.status.data = 'Cruise'
        self.stop_reason.data = 'No stop'

        if self.isTurnDetected:
            self.get_logger().debug("Turn detected")
            self.status.data = 'Turn'

        if closest_event is not None:

            if closest_event['type'] in ('on_path', 'collision_prediction'):
                self.get_logger().debug('Collison Avoidance or prediction')
                self.status.data = 'Decelerate'
                self.stop_reason.data = (
                    'Collision Avoidance' if closest_event['type'] == 'on_path'
                    else 'Collision Prediction'
                )

            elif closest_event['type'] == 'traffic_light':
                self.get_logger().debug('traffic_light')
                self.status.data = trafficLightTask
                self.stop_reason.data = trafficLightTask
        
        if self.isEndOfPath:
            self.get_logger().debug("Approaching destination, decelerating.")
            self.status.data = 'Park'
            self.stop_reason.data = 'Park'

        return (closest_event['stop_point'] if closest_event else None), closest_event, candidate_events
            
    def motion_planning(self):
        self.update_pose_from_tf()
        if not self.location and not self.pose:
            self.get_logger().warning("No location/pose input")
            return None
        
        if not self.path :
            #self.get_logger().warning("Path has not initialized from Mission Planner!!")
            self.isPathPlanned = False
            self.publish_stop_point_marker(None, "no_path")
            return
        
        if self.finished:
            self.status.data = 'Park'
            self.node_shut = True
            self.publish_stop_point_marker(None, "park")
            return
        
        if self.reset:
            self.get_logger().warning("RESET")
            self.isPathPlanned = False
            self.route = None
            self.current_lane_index = 0
            self.path = []
            self.path_as_lanes = []
            self.path_of_waypoints = []
            self.max_speeds_on_path = []
            self.intersection_points = []
            self.reset = False
            self.publish_stop_point_marker(None, "reset")
            return

        if self.reset_cooldown_active():
            self.publish_stop_point_marker(None, "reset_cooldown")
            return

        search_area, search_area_as_lanes = self.create_search_area()
        self.current_speed = self.velocity_report.longitudinal_velocity if self.velocity_report else 0.0
        self.update_observation_range(self.current_speed, self.current_speed < self.previous_speed_slidingWindow[0])
        vehicle_pose = self.pose.pose.position

        self.publish_range_markers(vehicle_pose)
        current_closest_waypoint_to_vehicle_index = self.find_closest_waypoint_to_vehicle(vehicle_pose, search_area)
        stop_point, closest_event, candidate_events = self.motion_planner(current_closest_waypoint_to_vehicle_index)

        stop_point_for_traj = stop_point
        if self.stop_reason.data in ("No stop", "Cruise", "Cruise_green"):
            stop_point_for_traj = None
        self.publish_stop_point_marker(stop_point_for_traj, self.stop_reason.data)
        self.publish_collision_points_markers(candidate_events, closest_event)
        stop_idx = (
            self.find_closest_waypoint_index_to_point(stop_point_for_traj)
            if stop_point_for_traj is not None
            else None
        )
        self.publish_trajectory(current_closest_waypoint_to_vehicle_index, stop_idx)
        self.log_throttle(
            "info",
            "motion_state",
            (
                f"closest_idx={current_closest_waypoint_to_vehicle_index} "
                f"stop_idx={stop_idx} "
                f"status={self.status.data} "
                f"reason={self.stop_reason.data}"
            ),
            period_sec=1.0,
        )
        
        self.get_logger().debug(
            f'behavior motion planning\n'
            f'distance to stop point: {self.calculate_distance(vehicle_pose, stop_point)}\n'
            f'status: {self.status.data}\n'
            f'stop reason: {self.stop_reason.data}\n'
        )
        
        self.previous_speed_slidingWindow.append(self.current_speed)

def main(args=None):
    rclpy.init(args=args)
    node = BehaviorMotionPlanning()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
