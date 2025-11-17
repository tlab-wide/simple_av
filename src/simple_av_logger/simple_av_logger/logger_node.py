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
        self.finished = False

    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def sim_monitor_callback(self, msg):
        self.sim_time = msg.sim_time
        self.sim_clock_rate = msg.sim_clock_rate
        self.simulation_snapshot()

    def portal_callback(self, msg):
        self.reset = msg.reset
        self.finished = msg.finished

    def pose_callback(self, msg):
        self.pose = msg

    def velocity_report_callback(self, msg):
        self.velocity_report = msg

    def simulation_snapshot(self):
        print("snapshot ...", self.sim_time)
        current_speed = self.velocity_report.longitudinal_velocity
        x = self.pose.pose.position.x
        y = self.pose.pose.position.y
        self.writer.writerow([self.sim_time, current_speed, x, y, False, False, 0, 0, 0])

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
