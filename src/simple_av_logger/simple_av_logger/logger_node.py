import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy, HistoryPolicy, ReliabilityPolicy
from simple_av_msgs.msg import PlanningPathPlanningMsg, PlanningMotionPlanningMsg
from geometry_msgs.msg import PoseStamped, Point
from autoware_vehicle_msgs.msg import GearCommand, VelocityReport
from simple_av_msgs.msg import SimMonitor
import time
import math
from collections import deque
import numpy as np
import yaml
import os
from ament_index_python.packages import get_package_share_directory
from simple_av_msgs.msg import Portal
from rclpy.parameter import Parameter
import time
import csv
from typing import List, Tuple
from dataclasses import dataclass

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
        self.is_in_intersection = False
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
            'timestamp', 'linear_speed', 'x', 'y', 'is_in_intersection', 'does_danger_detected', 'traffic_light_state', 'traffic_light_id', 'round_number'
        ])

        # Subscriptions
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        self.pose = PoseStamped()

        self.subscriptionVelocityReport = self.create_subscription(VelocityReport, '/vehicle/status/velocity_status', self.velocity_report_callback, 10)
        self.velocity_report = VelocityReport()

        self.subscriptionSimMonitor = self.create_subscription(SimMonitor, 'simple_av/sim_monitor', self.sim_monitor_callback, 100)
        self.sim_time = 0
        self.sim_clock_rate = 0

        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.round_number = 0
        self.finished = False

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
    
    def sim_monitor_callback(self, msg):
        self.sim_time = msg.sim_time
        self.sim_clock_rate = msg.sim_clock_rate
        self.simulation_snapshot()

    def portal_callback(self, msg):
        self.reset = msg.reset
        self.round_number = msg.round_number
        self.finished = msg.finished

    def pose_callback(self, msg):
        self.pose = msg

    def velocity_report_callback(self, msg):
        self.velocity_report = msg
    
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
    
    def check_intersection_start_and_exit(self, current_pose, treshold = 3.0):
        
        if not self.is_in_intersection:
            if self.calculate_distance(current_pose, self.intersection2_start_geometry_point) < treshold:
                self.is_in_intersection = True
        else:
            if self.calculate_distance(current_pose, self.intersection2_exit_geometry_point) < treshold:
                self.is_in_intersection = False
        

    def simulation_snapshot(self):
        print("snapshot ...", self.sim_time)
        current_speed = self.velocity_report.longitudinal_velocity
        x = self.pose.pose.position.x
        y = self.pose.pose.position.y
        self.check_intersection_start_and_exit(self.pose.pose.position)
        
        # 'timestamp', 'linear_speed', 'x', 'y', 'is_in_intersection', 'does_danger_detected', 'traffic_light_state', 'traffic_light_id', 'round_number'
        self.writer.writerow([self.sim_time, current_speed, x, y, self.is_in_intersection, False, 0, 0, self.round_number])

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
