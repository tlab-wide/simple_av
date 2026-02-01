import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point
from visualization_msgs.msg import Marker, MarkerArray
from autoware_vehicle_msgs.msg import VelocityReport
import numpy as np
import yaml
import os
from ament_index_python.packages import get_package_share_directory
from simple_av_msgs.msg import Portal, DetectedObjectsArray, TrafficSignalsArray, SimMonitor, LocalizationIntersectionStatus, LocalizationMsg, CollisionPredictionInfo
from autoware_control_msgs.msg import Control, Lateral, Longitudinal
import csv
from typing import List, Tuple
from dataclasses import dataclass
from scipy.spatial.transform import Rotation as R
from datetime import datetime

@dataclass
class PolygonRegion:
    """Any polygon region from YAML (inside, sidewalks, lanes, etc.)"""
    name: str
    polygon_type: str               # 'inside', 'sw', 'cw', 'lane', 'lanes'
    intersection_id: str
    polygon_id: str
    points: List[Tuple[float, float, float]]


class Logger(Node):
    def __init__(self):
        super().__init__('logger_node')

        # Load configs
        self.logger_config = self.config_file_loader("logger_config.yaml")
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.logger_state = self.logger_config['logger_module']['state']

        self.last_log_time = 0.0
        self.logging_interval = self.logger_config['logger_module']['log_time_interval']  # seconds

        # Load av features configs
        self.av_features = self.config_file_loader("av_features.yaml")
    
        # Handle logger off
        if not self.logger_state:
            self.get_logger().warn("Logger OFF → shutting down logger node")
            raise SystemExit   # clean exit

        self.get_logger().info("Logger ON")

        # Load intersection data
        self.intersection_profiles = self.load_intersections()
        
        # self.intersection2_scenario2_enter_point = self.intersection_profiles['intersection_points']['2']['2']['1']
        # self.intersection2_start_geometry_point = Point(x = self.intersection2_scenario2_enter_point['x'], y = self.intersection2_scenario2_enter_point['y'], z = self.intersection2_scenario2_enter_point['z'])
        # self.intersection2_scenario2_exit_point = self.intersection_profiles['intersection_points']['2']['2']['2']
        # self.intersection2_exit_geometry_point = Point(x = self.intersection2_scenario2_exit_point['x'], y = self.intersection2_scenario2_exit_point['y'], z = self.intersection2_scenario2_exit_point['z'])
        
        self.is_vehicle_inside_intersection = False
        self.has_exited_intersection = False
        
        # Load YAML sidewalk data
        self.intersections_layouts = self.load_intersections_layouts()
        self.intersection2_cw_areas = self.get_cross_walk_areas('2') # get cross walk areas of the Kakaiken intersection

        # ---- CSV PATH FIX ----
        pkg_share = get_package_share_directory('simple_av_logger')
        data_dir = os.path.join(pkg_share, 'data')
        os.makedirs(data_dir, exist_ok=True)

        self.intersection_id = self.logger_config['logger_module']['intersection']
        log_scenario = self.logger_config['logger_module']['scenario']

        # Speed profile
        if self.av_features['use_cool4_speed_profile']['enable']:
            speed_profile = 'cool4_SpeedProfile'
        else:
            speed_profile = 'SimpleAV_SpeedProfile'

        # RSU mode
        RSU = 'RSU_enabled' if self.av_features['object_detection']['use_rsu'] else 'RSU_disabled'

        # --- Timestamp ---
        now = datetime.now()
        date_str = now.strftime("%Y%m%d")          # 20250219
        time_str = now.strftime("%H%M%S")          # 153045
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")

        # --- Final CSV File Name ---
        csv_filename = f"Intersection{self.intersection_id}_Scenario{log_scenario}_{speed_profile}_{RSU}_{timestamp_str}.csv"

        csv_path = os.path.join(data_dir, csv_filename)
        self.csv = open(csv_path, 'w')
        self.writer = csv.writer(self.csv)

        # Write header
        header = [
            'round_number',
            'timestamp', 
            'speed', 
            'acceleration',
            'lane_id', 
            'pose_x', 
            'pose_y', 
            'is_in_intersection', 
            'does_danger_detected', 
            'rsu_detection_box_occupied', # previous rsu_detection - check when enter to the intersection 
            'rsu_objects', # format: [(ObjectID,type,BoxID,X,Y),(ObjectID,type,BoxID,X,Y), …]
            'obu_detection_box_occupied', # previous obu_detection - check when enter to the intersection 
            'obu_objects', # format: [(ObjectID,type,BoxID,X,Y),(ObjectID,type,BoxID,X,Y), …]
            'collision_prediction', # format: [(ObjectID,type,BoxID,X,Y)]
            'traffic_light_state'
        ]

        # --- Logging points config ---
        self.logging_points = []
        self.logging_points_default_threshold = 2.0
        self.reached_logging_points = set()
        logging_points_cfg = self.logger_config.get('logger_module', {}).get('logging_points', {})
        self.logging_points_default_threshold = logging_points_cfg.get('default_threshold', 2.0)
        self.logging_points = logging_points_cfg.get('points', [])
        self.get_logger().info(f"Logging points loaded: {self.logging_points}")
        self.logging_point_names = []
        for idx, point in enumerate(self.logging_points):
            name = point.get('name')
            if not name:
                name = f"point_{idx}"
            self.logging_point_names.append(name)
        header.extend(self.logging_point_names)
        self.writer.writerow(header)

        # Subscriptions
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        self.pose = PoseStamped()

        self.subscriptionVelocityReport = self.create_subscription(VelocityReport, '/vehicle/status/velocity_status', self.velocity_report_callback, 10)
        self.velocity_report = VelocityReport()

        self.subscriptionLocation = self.create_subscription(LocalizationMsg, 'simple_av/localization/location', self.location_callback, 10)
        self.location = LocalizationMsg()

        self.subscriptionIntersectionAwareness = self.create_subscription(LocalizationIntersectionStatus, 'simple_av/localization/intersection_status', self.intersectionAwareness_callback, 10)
        self.intersection_awareness_intersection_name = None
        self.intersection_awareness_status = None

        self.subscriptionSimMonitor = self.create_subscription(SimMonitor, 'simple_av/sim_monitor', self.sim_monitor_callback, 100)
        self.sim_time = 0
        self.sim_clock_rate = 0

        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.round_number = 0
        self.finished = False
        self.prev_reset = False
        self.last_reset_time_ns = None
        self.reset_cooldown = self.scenario_config['scenario'].get('reset_cooldown_seconds', 2.0)

        self.subscriptionTrafficSignal = self.create_subscription(TrafficSignalsArray, 'simple_av/perception/traffic_signals', self.trafficSignal_callback, 10)
        self.trafficSignal = TrafficSignalsArray()

        self.subscriptionDetectedObjects = self.create_subscription(DetectedObjectsArray, 'simple_av/perception/detected_objects', self.detectedObjects_callback, 10)
        self.detectedObjects = DetectedObjectsArray()

        # Logging points visualization
        self.logging_points_marker_pub = self.create_publisher(
            MarkerArray,
            'simple_av/visualization/logging_points',
            10
        )
        self.publish_logging_points_markers()
        # Republish periodically for RViz subscribers
        self.logging_points_timer = self.create_timer(1.0, self.publish_logging_points_markers)

        self.subscription = self.create_subscription(
            Control,
            '/control/command/control_cmd',
            self.control_callback,
            10
        )
        self.acceleration = None

        # Subscribe to the collision prediction topic
        self.subscription_collision = self.create_subscription(
            CollisionPredictionInfo,
            "simple_av/planning/collision_prediction_info",
            self.collision_callback,
            10
        )
        self.collision_prediction_info = None

        self.has_danger_detection_completed = False
        self.has_pedesrian_detected_at_danger_zones = -1
        self.rsu_detected = False
        self.obu_detected = False
        self.last_round_number = 0

        self.last_speed = 0
        self.visited_lanes = []          # ordered list of visited lane names/IDs
        self.last_lane = None            # to detect lane changes

    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def load_intersections(self):
        package_share_directory = get_package_share_directory('common')
        zones_path = os.path.join(package_share_directory, "zones", 'intersection_profiles.yaml')

        with open(zones_path, "r") as file:
            intersection_profiles = yaml.safe_load(file)
        return intersection_profiles

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
    
    def collision_callback(self, msg):
        self.collision_prediction_info = msg

    def control_callback(self, msg):
        # Extract longitudinal acceleration
        self.acceleration = msg.longitudinal.acceleration

    def portal_callback(self, msg):
        now_ns = self.get_clock().now().nanoseconds
        reset_edge = msg.reset and not self.prev_reset
        cooldown_ok = (
            self.last_reset_time_ns is None or
            (now_ns - self.last_reset_time_ns) / 1e9 >= self.reset_cooldown
        )
        self.reset = reset_edge and cooldown_ok
        self.round_number = msg.round_number
        self.finished = msg.finished
        if self.reset:
            self.last_reset_time_ns = now_ns
        self.prev_reset = msg.reset

    def reset_cooldown_active(self):
        if self.last_reset_time_ns is None:
            return False
        now_ns = self.get_clock().now().nanoseconds
        return (now_ns - self.last_reset_time_ns) / 1e9 < self.reset_cooldown

    def pose_callback(self, msg):
        self.pose = msg

    def velocity_report_callback(self, msg):
        self.velocity_report = msg
    
    def location_callback(self, msg):
        self.location = msg
    
    def intersectionAwareness_callback(self, msg):
        self.intersection_awareness_intersection_name = msg.intersection_name
        self.intersection_awareness_status = msg.status
    
    def trafficSignal_callback(self, msg):
        self.trafficSignal = msg
    
    def detectedObjects_callback(self, msg):
        self.detectedObjects = msg

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
    
    def apply_quaternion_rotation(self, quaternion, vector):
        """
        Applies a quaternion rotation to a given vector.
        """
        rotation = R.from_quat(np.array([quaternion.x, quaternion.y, quaternion.z, quaternion.w]))
        transformed_vector = rotation.apply(np.array([vector.x, vector.y, vector.z]))
        return Point(x=transformed_vector[0], y=transformed_vector[1], z=transformed_vector[2])
    
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
            self.get_logger().debug(f"Found {len(detected_pedestrians)} pedestrians/cyclists")

        return detected_pedestrians

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

    def is_object_detected_at_intersection_danger_zones(self, intersection_id):

        vehicle_pose = self.pose.pose.position
        vehicle_orientation = self.pose.pose.orientation

        detected_pedestrians = self.get_detected_pedestrians()
        if not detected_pedestrians:
            return False, False, False   # nobody detected at all

        # Validate intersection layout exists
        if not self.intersections_layouts:
            return False, False, False

        danger_zones = [
            p for p in self.intersections_layouts
            if p.intersection_id == intersection_id and p.polygon_type == "sw"
        ]

        any_detected = False
        rsu_detected = False
        obu_detected = False

        for ped in detected_pedestrians:

            # Convert from relative → absolute position
            ped_abs = self.get_object_absolute_position(
                vehicle_orientation, vehicle_pose, ped.position
            )

            for polygon in danger_zones:
                if polygon.polygon_id == '3':  # skip zone 3
                    continue
                if self.is_point_in_polygon(ped_abs, polygon.points):

                    any_detected = True

                    if ped.is_from_rsu:
                        rsu_detected = True
                    else:
                        obu_detected = True

                    # No need to check more polygons for this pedestrian
                    break

        return any_detected, rsu_detected, obu_detected

    
    def update_is_vehicle_inside_intersection_state(self, vehicle_pose, treshold = 2.0):
        
        enter_cw = None
        exit_cw = None
        for cw in self.intersection2_cw_areas:
            if cw.polygon_id == '3':
                enter_cw = cw
            elif cw.polygon_id == '2':
                exit_cw = cw
            else:
                continue

        if not self.is_vehicle_inside_intersection:
            if self.is_point_in_polygon(vehicle_pose, enter_cw.points):
                self.is_vehicle_inside_intersection = True
                # self.get_logger().error(f"Vehicle entered the intersection")
        else:
            if self.is_point_in_polygon(vehicle_pose, exit_cw.points):
                self.is_vehicle_inside_intersection = False
                self.has_pedesrian_detected_at_danger_zones = -1
                self.rsu_detected = False
                self.obu_detected = False
                # self.get_logger().error(f"Vehicle Exited the intersection")
        

    def get_traffic_light_color_by_id(self, traffic_light_id):
        if self.intersection_awareness_intersection_name is not None:
            v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
            v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)
            if traffic_light_id in v2i_traffic_signals_id:
                return v2i_traffic_signals_colors[v2i_traffic_signals_id.index(traffic_light_id)]
        return None
    

    def new_round_parameter_rest(self):
        if self.round_number > self.last_round_number:
            self.has_danger_detection_completed = False
            self.is_vehicle_inside_intersection = False
            self.has_pedesrian_detected_at_danger_zones = -1
            self.rsu_detected = False
            self.obu_detected = False
            self.last_round_number = self.round_number
            self.reached_logging_points.clear()

    def log_points_if_reached(self, vehicle_pose):
        if not self.logging_points:
            return
        for point in self.logging_points:
            name = point.get('name')
            if not name or name in self.reached_logging_points:
                continue
            try:
                px = float(point.get('x', 0.0))
                py = float(point.get('y', 0.0))
                pz = float(point.get('z', 0.0))
                threshold = float(point.get('threshold', self.logging_points_default_threshold))
            except (TypeError, ValueError):
                continue
            dx = vehicle_pose.x - px
            dy = vehicle_pose.y - py
            dz = vehicle_pose.z - pz
            dist = (dx * dx + dy * dy + dz * dz) ** 0.5
            if dist <= threshold:
                self.reached_logging_points.add(name)

    def publish_logging_points_markers(self):
        if not self.logging_points:
            return
        marker_array = MarkerArray()
        now = self.get_clock().now().to_msg()
        for idx, point in enumerate(self.logging_points):
            name = point.get('name', f"point_{idx}")
            try:
                px = float(point.get('x', 0.0))
                py = float(point.get('y', 0.0))
                pz = float(point.get('z', 0.0))
            except (TypeError, ValueError):
                continue
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = now
            marker.ns = "logging_points"
            marker.id = idx
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose.position = Point(x=px, y=py, z=pz)
            marker.pose.orientation.w = 1.0
            marker.scale.x = 0.8
            marker.scale.y = 0.8
            marker.scale.z = 0.8
            marker.color.r = 0.5
            marker.color.g = 1.0
            marker.color.b = 0.5
            marker.color.a = 0.9
            marker.text = name
            marker_array.markers.append(marker)

        self.logging_points_marker_pub.publish(marker_array)
    
    def get_cross_walk_areas(self, intersection_id):
        cw_zones = [
                p for p in self.intersections_layouts
                if p.intersection_id == intersection_id and p.polygon_type == "cw"
            ]
        return cw_zones

    def sim_monitor_callback(self, msg):
        self.sim_time = msg.sim_time
        self.sim_clock_rate = msg.sim_clock_rate
        self.simulation_snapshot()
            
    def update_lane_history(self, lane):
        if lane != self.last_lane:
            self.last_lane = lane
            if lane not in self.visited_lanes:
                self.visited_lanes.append(lane)


    def get_collision_prediction_info(self, intersection_id):
        """
        Returns a list of collision predictions with detected box info.
        Each entry: (object_label, polygon_type, polygon_id, x, y, ttc)
        """
        collision_prediction = []

        # No collision info or no collision detected
        if not self.collision_prediction_info or not self.collision_prediction_info.collision_detected:
            return collision_prediction

        obj_abs_pose = self.collision_prediction_info.object_position
        ttc = self.collision_prediction_info.time_to_collision
        object_label = self.collision_prediction_info.object_label

        # Validate intersection layout exists
        if not self.intersections_layouts:
            return collision_prediction

        # Define danger zones
        sw_danger_zones = [
            p for p in self.intersections_layouts
            if p.intersection_id == intersection_id and p.polygon_type == "sw"
        ]
        cw_danger_zones = [
            p for p in self.intersections_layouts
            if p.intersection_id == intersection_id and p.polygon_type == "cw"
        ]

        # Find which polygon the object belongs to
        found_box = False
        for polygon in sw_danger_zones:
            if polygon.polygon_id == '3':  # skip zone 3
                continue
            if self.is_point_in_polygon(obj_abs_pose, polygon.points):
                collision_prediction.append((object_label,'sw',polygon.polygon_id,ttc,round(obj_abs_pose.x, 4),round(obj_abs_pose.y, 4)))
                found_box = True
                break

        if not found_box:
            for polygon in cw_danger_zones:
                if self.is_point_in_polygon(obj_abs_pose, polygon.points):
                    collision_prediction.append((object_label,'sw',polygon.polygon_id,ttc,round(obj_abs_pose.x, 4),round(obj_abs_pose.y, 4)))
                    break

        # If object is not in any polygon, still return basic info
        if not collision_prediction:
            collision_prediction.append((object_label,'none','none',ttc,round(obj_abs_pose.x, 4),round(obj_abs_pose.y, 4)))

        return collision_prediction


    def get_detected_objects(self, rsu_check, intersection_id):
        vehicle_pose = self.pose.pose.position
        vehicle_orientation = self.pose.pose.orientation

        detected_pedestrians = self.get_detected_pedestrians()
        if not detected_pedestrians:
            return []
        
        # Validate intersection layout exists
        if not self.intersections_layouts:
            return []

        sw_danger_zones = [
            p for p in self.intersections_layouts
            if p.intersection_id == intersection_id and p.polygon_type == "sw"
        ]

        cw_danger_zones = [
            p for p in self.intersections_layouts
            if p.intersection_id == intersection_id and p.polygon_type == "cw"
        ]

        objects = []

        for ped in detected_pedestrians:
            if rsu_check:
                if ped.is_from_rsu:
                    # Convert from relative → absolute position
                    ped_abs = self.get_object_absolute_position(
                        vehicle_orientation, vehicle_pose, ped.position
                    )

                    for polygon in sw_danger_zones:
                        if polygon.polygon_id == '3':  # skip zone 3
                            continue
                        if self.is_point_in_polygon(ped_abs, polygon.points):
                            objects.append((ped.label,'sw',polygon.polygon_id,f"{ped_abs.x:.4f}",f"{ped_abs.y:.4f}"))
                    
                    for polygon in cw_danger_zones:
                        if self.is_point_in_polygon(ped_abs, polygon.points):
                            objects.append((ped.label,'cw',polygon.polygon_id,f"{ped_abs.x:.4f}",f"{ped_abs.y:.4f}"))
            else:
                if not ped.is_from_rsu:
                    # Convert from relative → absolute position
                    ped_abs = self.get_object_absolute_position(
                        vehicle_orientation, vehicle_pose, ped.position
                    )

                    for polygon in sw_danger_zones:
                        if polygon.polygon_id == '3':  # skip zone 3
                            continue
                        if self.is_point_in_polygon(ped_abs, polygon.points):
                            objects.append((ped.label,'sw',polygon.polygon_id,ped_abs.x,ped_abs.y))
                    
                    for polygon in cw_danger_zones:
                        if self.is_point_in_polygon(ped_abs, polygon.points):
                            objects.append((ped.label,'cw',polygon.polygon_id,f"{ped_abs.x:.4f}",f"{ped_abs.y:.4f}"))
                        
                        
        return objects


    def simulation_snapshot(self):

        # ---- Time-based logging throttle ----
        if (self.sim_time - self.last_log_time) < self.logging_interval:
            return
        self.last_log_time = self.sim_time

        if self.reset:
            self.reset = False
            return
        if self.reset_cooldown_active():
            return
        
        # ------- Data Evaluation -------
        if not self.pose or not self.pose.pose:
            self.get_logger().warning("No pose data available for danger zone detection")
            return

        if self.pose.pose.position.x == 0.0 and self.pose.pose.position.y == 0.0 and self.pose.pose.position.z == 0.0:
            self.get_logger().warning("Vehicle pose at origin")
            return
        
        # only log when in the intersection #2 - Kakaiken - area
        if self.intersection_awareness_intersection_name is None or self.intersection_awareness_intersection_name != '2':
            return
        # ------- ------- ------- -------
        
        # print("snapshot ...", self.sim_time)
        self.new_round_parameter_rest()
        self.update_lane_history(self.location.closest_lane_names.data)
        current_speed = self.velocity_report.longitudinal_velocity
        vehicle_pose = self.pose.pose.position
        x = vehicle_pose.x
        y = vehicle_pose.y
        self.update_is_vehicle_inside_intersection_state(vehicle_pose)
        self.log_points_if_reached(vehicle_pose)
        if self.is_vehicle_inside_intersection and not self.has_danger_detection_completed:
            # self.has_pedesrian_detected_at_danger_zones = self.is_object_detected_at_intersection_danger_zones('2')
            (any_detected, rsu_detected, obu_detected) = self.is_object_detected_at_intersection_danger_zones(self.intersection_id)
            self.has_pedesrian_detected_at_danger_zones = any_detected
            self.rsu_detected = rsu_detected
            self.obu_detected = obu_detected
            self.has_danger_detection_completed = True
        
        # rsu_objects = []
        # # '[(ObjectID,type,BoxID,X,Y),(ObjectID,type,BoxID,X,Y)]'
        # if not self.is_vehicle_inside_intersection and not self.has_danger_detection_completed: # RSU
        #     rsu_objects = self.get_detected_objects(True, self.intersection_id)


        # obu_objects = []
        # if self.is_vehicle_inside_intersection: # OBU
        #     obu_objects = self.get_detected_objects(False, self.intersection_id)

        rsu_objects = self.get_detected_objects(True, self.intersection_id)
        obu_objects = self.get_detected_objects(False, self.intersection_id)

        light_165626 = self.get_traffic_light_color_by_id(165626)
        if light_165626 == 1:
            light_165626 = 'red'
        elif light_165626 == 2:
            light_165626 = 'yellow'
        elif light_165626 == 3:
            light_165626 = 'green'
        else:
            light_165626 = 'unknown'
        
        if self.location.closest_lane_names.data is None or self.location.closest_lane_names.data == '':
            return

        if (self.location.closest_lane_names.data == 'lanelet1118' and current_speed <= 0.2) or (self.location.closest_lane_names.data == 'lanelet1156' and current_speed <= 0.05):
            return

        collision_predicted = self.get_collision_prediction_info(self.intersection_id)

        row = [
            self.round_number,
            f"{self.sim_time:.1f}",
            f"{current_speed:.2f}", 
            self.acceleration,
            self.location.closest_lane_names.data, 
            x, 
            y,
            self.is_vehicle_inside_intersection,
            self.has_pedesrian_detected_at_danger_zones,
            self.rsu_detected,
            rsu_objects,
            self.obu_detected,
            obu_objects,
            collision_predicted,
            light_165626
        ]
        for name in self.logging_point_names:
            row.append(str(name in self.reached_logging_points))
        self.writer.writerow(row)
        
    def destroy_node(self):
        self.get_logger().info("Closing CSV file")
        if self.csv:
            self.csv.flush()
            self.csv.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = Logger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
