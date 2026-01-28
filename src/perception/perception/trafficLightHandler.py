#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from simple_av_msgs.msg import TrafficSignalsArray, LocalizationIntersectionStatus
from v2x_msgs.msg import V2XSignals
from geometry_msgs.msg import PoseStamped
from math import atan2, asin
import yaml
import os
from ament_index_python.packages import get_package_share_directory
from scipy.spatial.transform import Rotation as R
import numpy as np
# import transformations as tf
from transformations import euler_from_quaternion
from simple_av_msgs.msg import Portal


class TrafficSignalHandler(Node):
    def __init__(self):
        super().__init__('TrafficLightHandler')

        # Load scenario configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.vehicle_model = self.scenario_config['scenario']['vehicle_model']

        # Load av features configs
        self.av_features = self.config_file_loader("av_features.yaml")
        self.enable_trafficlight = self.av_features['traffic_light']['enable']
        self.enable_RSU_for_trafficlight = self.av_features['traffic_light']['use_rsu']

        
        # Create subscriber for /v2x/traffic_signals_intersection<n> topics
        self.subscriptionTrafficLight_intersection1 = self.create_subscription(V2XSignals, '/v2x/rsu1/traffic_signals', self.trafficSignal_callback_intersection1, 10)
        self.trafficSignal_intersection1 = V2XSignals()  # Initialize traffic signal for intersection number 1
        
        self.subscriptionTrafficLight_intersection2 = self.create_subscription(V2XSignals, '/v2x/rsu2/traffic_signals', self.trafficSignal_callback_intersection2, 10)
        self.trafficSignal_intersection2 = V2XSignals()  # Initialize traffic signal for intersection number 2
        
        self.subscriptionTrafficLight_intersection4 = self.create_subscription(V2XSignals, '/v2x/rsu4/traffic_signals', self.trafficSignal_callback_intersection4, 10)
        self.trafficSignal_intersection4 = V2XSignals()  # Initialize traffic signal for intersection number 4
        
        self.subscriptionTrafficLight_intersection5 = self.create_subscription(V2XSignals, '/v2x/rsu5/traffic_signals', self.trafficSignal_callback_intersection5, 10)
        self.trafficSignal_intersection5 = V2XSignals()  # Initialize traffic signal for intersection number 5

        # Create subscriber for /sensing/gnss/pose topic
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        
        # Create subscriber to simple_av/portal topic
        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False
        self.prev_reset = False
        self.last_reset_time_ns = None
        self.reset_cooldown = self.scenario_config['scenario'].get('reset_cooldown_seconds', 2.0)

        # Create subscriber to simple_av/localization/intersection_status topic
        self.subscriptionIntersectionAwareness = self.create_subscription(LocalizationIntersectionStatus, 'simple_av/localization/intersection_status', self.intersectionAwareness_callback, 10)
        self.intersection_awareness_intersection_name = None
        self.intersection_awareness_status = None
        
        # Initialize the publishers
        self.publisher_traffic_signals = self.create_publisher(TrafficSignalsArray, 'simple_av/perception/traffic_signals', 10)

        self.vehicle_pose = PoseStamped()
        self.node_shut = False

    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    
    def intersectionAwareness_callback(self, msg):
        self.intersection_awareness_intersection_name = msg.intersection_name
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

    def pose_callback(self, msg):
        self.vehicle_pose = msg

    def trafficSignal_callback_intersection1(self, msg):
        self.trafficSignal_intersection1 = msg
    
    def trafficSignal_callback_intersection2(self, msg):
        self.trafficSignal_intersection2 = msg
    
    def trafficSignal_callback_intersection4(self, msg):
        self.trafficSignal_intersection4 = msg
    
    def trafficSignal_callback_intersection5(self, msg):
        self.trafficSignal_intersection5 = msg

    def process_traffic_signals(self):
        """
        Processes traffic signals for the current intersection.

        Returns:
            - v2i_traffic_signals_id: List of traffic signal IDs.
            - v2i_traffic_signals_colors: List of corresponding signal colors.
        """

        intersection_number = self.intersection_awareness_intersection_name  # e.g., '1'
        # print("debug: intersection number: ", intersection_number)
        try:
            trafficSignal = getattr(self, f"trafficSignal_intersection{intersection_number}")
        except AttributeError:
            self.get_logger().debug(f"No traffic signal data for intersection {intersection_number}")
            return [], []
        self.get_logger().debug(f"trafficSignal_intersection{intersection_number}")
        v2i_traffic_signals_id = []
        v2i_traffic_signals_colors = []

        if not trafficSignal.traffic_signals:
            self.get_logger().debug("No traffic signal data")
            return [], []

        for traffic_signal in trafficSignal.traffic_signals.signals:
            v2i_traffic_signals_id.append(traffic_signal.traffic_signal_id)
            for element in traffic_signal.elements:
                v2i_traffic_signals_colors.append(element.color)

        return v2i_traffic_signals_id, v2i_traffic_signals_colors

    def trafficSignalDetection(self):
        if self.finished:
            self.node_shut = True
            return
        
        v2i_traffic_signals_id = []
        v2i_traffic_signals_colors = []

        # Handle traffic signals
        self.get_logger().debug(
            f"intersection awareness: {self.intersection_awareness_intersection_name}"
        )
        if self.enable_trafficlight and self.intersection_awareness_intersection_name is not None:
            v2i_traffic_signals_id, v2i_traffic_signals_colors = self.process_traffic_signals()
            self.get_logger().debug(f'ids: {v2i_traffic_signals_id}')
            self.get_logger().debug(f'colors: {v2i_traffic_signals_colors}')

        # Create and publish traffic signals message
        traffic_signals_msg = TrafficSignalsArray()
        traffic_signals_msg.v2i_traffic_signals_id = v2i_traffic_signals_id
        traffic_signals_msg.v2i_traffic_signals_colors = v2i_traffic_signals_colors
        self.publisher_traffic_signals.publish(traffic_signals_msg)
        

def main(args=None):
    rclpy.init(args=args)
    node = TrafficSignalHandler()
    try:
        while rclpy.ok() and not node.node_shut:
            rclpy.spin_once(node, timeout_sec=0)  # Set timeout to 0 to avoid delay
            node.trafficSignalDetection()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
