import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point
from autoware_vehicle_msgs.msg import VelocityReport
import numpy as np
import yaml
import os
from ament_index_python.packages import get_package_share_directory
from simple_av_msgs.msg import Portal, DetectedObjectsArray, TrafficSignalsArray, SimMonitor, LocalizationIntersectionStatus, LocalizationMsg
import csv
from typing import List, Tuple
from dataclasses import dataclass
from scipy.spatial.transform import Rotation as R

@dataclass
class PolygonRegion:
    """Any polygon region from YAML (inside, sidewalks, lanes, etc.)"""
    name: str
    polygon_type: str               # 'inside', 'sw', 'lane', 'lanes'
    intersection_id: str
    polygon_id: str
    points: List[Tuple[float, float, float]]


class Logger(Node):
    def __init__(self):
        super().__init__('logger_node')

        # Load configs
        self.logger_config = self.config_file_loader("logger_config.yaml")
        self.logger_state = self.logger_config['logger_module']['state']

        # Handle logger off
        if not self.logger_state:
            self.get_logger().warn("Logger OFF → shutting down logger node")
            raise SystemExit   # clean exit

        self.get_logger().info("Logger ON")

        # Load intersection data
        self.intersection_profiles = self.load_intersections()
        
        self.intersection2_scenario2_enter_point = self.intersection_profiles['intersection_points']['2']['2']['1']
        self.intersection2_start_geometry_point = Point(x = self.intersection2_scenario2_enter_point['x'], y = self.intersection2_scenario2_enter_point['y'], z = self.intersection2_scenario2_enter_point['z'])
        
        self.intersection2_scenario2_exit_point = self.intersection_profiles['intersection_points']['2']['2']['2']
        self.intersection2_exit_geometry_point = Point(x = self.intersection2_scenario2_exit_point['x'], y = self.intersection2_scenario2_exit_point['y'], z = self.intersection2_scenario2_exit_point['z'])
        self.is_vehicle_inside_intersection = False
        self.has_exited_intersection = False
        
        
        # Load YAML sidewalk data
        self.intersections_layouts = self.load_intersection_layout()

        # ---- CSV PATH FIX ----
        pkg_share = get_package_share_directory('simple_av_logger')
        data_dir = os.path.join(pkg_share, 'data')
        os.makedirs(data_dir, exist_ok=True)

        csv_path = os.path.join(data_dir, 'test.csv')
        self.csv = open(csv_path, 'w')
        self.writer = csv.writer(self.csv)

        # Write header
        self.writer.writerow([
            'timestamp', 'speed', 
            'lane_id', 'x', 'y', 
            'is_in_intersection', 'does_danger_detected', 
            'traffic_light_state', 'traffic_light_id', 
            'round_number'
        ])

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

        self.subscriptionTrafficSignal = self.create_subscription(TrafficSignalsArray, 'simple_av/perception/traffic_signals', self.trafficSignal_callback, 10)
        self.trafficSignal = TrafficSignalsArray()

        self.subscriptionDetectedObjects = self.create_subscription(DetectedObjectsArray, 'simple_av/perception/detected_objects', self.detectedObjects_callback, 10)
        self.detectedObjects = DetectedObjectsArray()

        self.has_danger_detection_completed = False
        self.has_pedesrian_Detected_at_danger_zones = -1
        self.last_round_number = 0

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

    def load_intersection_layout(self) -> List[PolygonRegion]:
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

    def portal_callback(self, msg):
        self.reset = msg.reset
        self.round_number = msg.round_number
        self.finished = msg.finished

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
                    self.get_logger().info(
                        f"Pedestrian detected at ({ped_abs.x:.2f}, {ped_abs.y:.2f}) at intersection {p.intersection_id} inside: {p.polygon_type}{p.polygon_id}"
                    )

        if objects_in_zones > 0:
            self.get_logger().info(f"Total pedestrians in danger zones: {objects_in_zones}")
        else:
            self.get_logger().debug("No pedestrians in danger zones")
        return objects_in_zones > 0
    
    def update_is_vehicle_inside_intersection_state(self, current_pose, treshold = 2.0):
        
        if not self.is_vehicle_inside_intersection:
            if self.calculate_distance(current_pose, self.intersection2_start_geometry_point) < treshold:
                self.is_vehicle_inside_intersection = True
        else:
            if self.calculate_distance(current_pose, self.intersection2_exit_geometry_point) < treshold:
                self.is_vehicle_inside_intersection = False
                self.has_pedesrian_Detected_at_danger_zones = -1
        

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
            self.has_pedesrian_Detected_at_danger_zones = -1
            self.last_round_number = self.round_number

    def sim_monitor_callback(self, msg):
        self.sim_time = msg.sim_time
        self.sim_clock_rate = msg.sim_clock_rate
        self.simulation_snapshot()

    def simulation_snapshot(self):
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
        
        print("snapshot ...", self.sim_time)
        self.new_round_parameter_rest()
        current_speed = self.velocity_report.longitudinal_velocity
        vehicle_pose = self.pose.pose.position
        x = vehicle_pose.x
        y = vehicle_pose.y
        self.update_is_vehicle_inside_intersection_state(self.pose.pose.position)
        if self.is_vehicle_inside_intersection and not self.has_danger_detection_completed:
            self.has_pedesrian_Detected_at_danger_zones = self.is_object_detected_at_intersection_danger_zones('2')
            self.has_danger_detection_completed = True

        v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
        v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)
        
        self.writer.writerow([
            'timestamp', 'speed', 
            'lane_id', 'x', 'y', 
            'is_in_intersection', 'does_danger_detected', 
            'traffic_light_state', 'traffic_light_id', 
            'round_number'
        ])
        
        self.writer.writerow([self.sim_time, current_speed, 
                              self.location.closest_lane_names, x, y, 
                              self.is_vehicle_inside_intersection, self.has_pedesrian_Detected_at_danger_zones, 
                              0, 0, 
                              self.round_number])

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
