#!/usr/bin/env python3

import rclpy
import os
import yaml
from rclpy.node import Node
from geometry_msgs.msg import Point
import numpy as np
import math
from simple_av_msgs.msg import Portal
from ament_index_python.packages import get_package_share_directory
from nav_msgs.msg import Odometry


class portal(Node):
    def __init__(self):
        super().__init__('portal')

        fusion_cfg = self.config_file_loader("localization_fusion.yaml").get('localization_fusion', {})
        odom_topic = fusion_cfg.get('output_odom_topic', '/simple_av/localization/odometry_fused')

        # Create subscriber to fused localization output
        self.subscriptionPose = self.create_subscription(
            Odometry,
            odom_topic,
            self.pose_callback,
            10
        )
        self.portal_publisher = self.create_publisher(Portal, 'simple_av/portal', 10)
        self.pose = None
        self.initial_position = Point()
        self.isInitialPoseSampled = False
        self.isPortalReached = False
        self.finished = False
        self.last_pose = Point()
        self.current_pose = Point()
        self.repeat_counter = 0
        self.jumpThreshold = 15.0 # meters

        # Load configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.repeat_count = self.scenario_config['scenario']['repeat_count']
    
    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def pose_callback(self, msg):
        self.pose = msg.pose.pose
    

    def calculate_distance(self, point1, point2):
        return  math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def initial_pose(self):
        if self.pose and self.pose.position.x != 0 and self.pose.position.y != 0 and self.pose.position.z != 0:
            self.get_logger().debug(
                f"counter: {self.repeat_counter} target: {self.repeat_count}"
            )
            self.initial_position = self.pose.position
            self.current_pose = self.pose.position
            self.last_pose = self.current_pose
            self.isInitialPoseSampled = True

    def portal_detector(self):
        self.current_pose = self.pose.position
        if self.calculate_distance(self.current_pose, self.last_pose) > self.jumpThreshold :
            self.get_logger().debug(f"flag value: {self.isPortalReached}")
            self.get_logger().debug(
                f"jump value: {self.calculate_distance(self.current_pose, self.last_pose)}"
            )
            self.get_logger().info("Jump Detected")
            self.isPortalReached = True
            self.initial_position = self.current_pose
            self.repeat_counter += 1
            self.get_logger().debug(
                f"counter: {self.repeat_counter} target: {self.repeat_count}"
            )
            if self.repeat_counter == self.repeat_count:
                self.get_logger().info("Test finished")
                self.finished = True
        self.last_pose = self.current_pose
        self.publish_portal()
                

    def portal_reset(self):
        if not self.isInitialPoseSampled:
            self.initial_pose()
        else:
            self.portal_detector()

    def publish_portal(self):
        portal_reset = Portal()
        portal_reset.reset = self.isPortalReached
        portal_reset.finished = self.finished
        portal_reset.round_number = self.repeat_counter
        self.portal_publisher.publish(portal_reset)
        self.isPortalReached = False

def main(args=None):
    rclpy.init(args=args)
    node = portal()
    try:
        while rclpy.ok() and not node.finished:
            rclpy.spin_once(node, timeout_sec=0.1)# Set timeout to 0 to avoid delay
            node.portal_reset()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
