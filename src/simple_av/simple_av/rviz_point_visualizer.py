import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import yaml
import os
from ament_index_python.packages import get_package_share_directory
from simple_av_msgs.msg import LocalizationMsg  # adjust if needed
from dataclasses import dataclass
from typing import List, Tuple
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy


"""
points_visualizer Node

This ROS 2 node provides a generic mechanism to visualize important points 
in RViz. The purpose of this node is to make debugging and monitoring easier 
by displaying dynamic or static points used in various software modules, 
such as:

- Lookahead points from path planning (used by Pure Pursuit controllers)
- Stop points, goal points, or intermediate waypoints

By using this node, multiple point topics can be visualized in RViz as 
Markers, providing clear visual feedback of the vehicle's planning, logic, 
and decision-making processes. This approach decouples visualization from 
the logic of the algorithms and keeps RViz displays organized and flexible.
"""

class point_visualizer(Node):
    def __init__(self):
        super().__init__('rviz_point_visualizer')

        # Publishers
        self.closest_point_pub = self.create_publisher(Marker, '/simple_av/visualization/closest_point_marker', 10)

        # Subscriptions
        self.create_subscription(
            LocalizationMsg,
            '/simple_av/localization/location',
            self.closest_point_callback,
            10
        )


    def closest_point_callback(self, msg: LocalizationMsg):
        marker = Marker()
        marker.header.frame_id = "map"  # display in map frame
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "closest_point"
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position = msg.closest_point  # geometry_msgs/Point
        marker.pose.orientation.w = 1.0
        marker.scale.x = 1.2
        marker.scale.y = 1.2
        marker.scale.z = 1.2
        marker.color.r = 45.0/255.0
        marker.color.g = 120.0/255.0
        marker.color.b = 240.0/255.0
        marker.color.a = 0.9
        marker.lifetime.sec = 0  # 0 = forever

        self.closest_point_pub.publish(marker)
        self.get_logger().debug(
            f"Published closest point at {msg.closest_point.x}, {msg.closest_point.y}, {msg.closest_point.z}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = point_visualizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
