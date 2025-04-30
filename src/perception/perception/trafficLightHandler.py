#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from simple_av_msgs.msg import TrafficSignalsArray
from v2x_msgs.msg import CooperativeSignalsMessage
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
        self.use_RSU_for_trafficlight = self.av_features['traffic_light']['use_rsu']
        self.use_RSU_for_object_detection = self.av_features['object_detection']['use_rsu']
        self.RSU_delay_enable = self.av_features['RSU_delay']['enable']
        self.RSU_delay_value = self.av_features['RSU_delay']['value']

        
        # Create subscriber for /v2x/traffic_signals topic
        self.subscriptionTrafficLight = self.create_subscription(CooperativeSignalsMessage, '/v2x/traffic_signals', self.trafficSignal_callback, 10)

        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        # Create subscriber to simple_av/portal topic
        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False
        
        self.trafficSignal = CooperativeSignalsMessage()  # Initialize traffic signal

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
    
    def portal_callback(self, msg):
        self.reset = msg.reset
        self.finished = msg.finished

    def pose_callback(self, msg):
        self.vehicle_pose = msg

    def trafficSignal_callback(self, msg):
        """Callback function to update the traffic signal data."""
        self.trafficSignal = msg
    

    def process_traffic_signals(self):
        """
        Processes traffic signals to extract signal IDs and colors for station_id = 2.

        Creates two lists:
        - v2i_traffic_signals_id: Contains traffic signal IDs for station_id = 2.
        - v2i_traffic_signals_colors: Contains corresponding colors of traffic signals.
        """
        # Check if the traffic signal data exists
        if not hasattr(self, 'trafficSignal') or not self.trafficSignal:
            print("No traffic signal data available.")
            return [], []

        # Initialize arrays for IDs and colors
        v2i_traffic_signals_id = []
        v2i_traffic_signals_colors = []

        # Ensure the station_id matches 2
        # Loop through traffic signals
        # if self.trafficSignal.station_id == 1:
        for traffic_signal in self.trafficSignal.traffic_signals.signals:
            for element in traffic_signal.elements:
                # Append traffic signal ID and color
                # print(traffic_signal.traffic_signal_id, element.color)
                v2i_traffic_signals_id.append(traffic_signal.traffic_signal_id)
                v2i_traffic_signals_colors.append(element.color)
        return v2i_traffic_signals_id, v2i_traffic_signals_colors

    def trafficSignalDetection(self):
        if self.finished:
            self.node_shut = True
            return
        
        # Handle traffic signals
        v2i_traffic_signals_id, v2i_traffic_signals_colors = self.process_traffic_signals()
        print(v2i_traffic_signals_id)
        print(v2i_traffic_signals_colors)
        if 166849 in v2i_traffic_signals_id:
            print("intersection 1 traffic light")
            

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
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
