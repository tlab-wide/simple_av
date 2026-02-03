#!/usr/bin/env python3

import math
import os
import yaml
import numpy as np

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TransformStamped
from sensor_msgs.msg import Imu
from tf2_ros import TransformBroadcaster
from ament_index_python.packages import get_package_share_directory


class GnssImuFusion(Node):
    def __init__(self):
        super().__init__('gnss_imu_fusion')

        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)

        self.cfg = self.load_config('localization_fusion.yaml').get('localization_fusion', {})
        self.gnss_topic = self.cfg.get('gnss_topic', '/sensing/gnss/pose')
        self.imu_topic = self.cfg.get('imu_topic', '/sensing/imu/tamagawa/imu_raw')
        self.output_topic = self.cfg.get('output_topic', '/localization/pose')
        self.map_frame = self.cfg.get('map_frame', 'map')
        self.base_frame = self.cfg.get('base_frame', 'base_link')
        self.publish_tf = bool(self.cfg.get('publish_tf', True))
        self.publish_rate_hz = float(self.cfg.get('publish_rate_hz', 50.0))
        self.use_imu_orientation = bool(self.cfg.get('use_imu_orientation', True))
        self.pos_alpha = float(self.cfg.get('position_smoothing_alpha', 0.2))
        self.ori_alpha = float(self.cfg.get('orientation_smoothing_alpha', 0.2))

        self.latest_gnss = None
        self.latest_imu = None
        self.filtered_pose = None

        self.sub_gnss = self.create_subscription(
            PoseStamped, self.gnss_topic, self.gnss_callback, 10
        )
        self.sub_imu = self.create_subscription(
            Imu, self.imu_topic, self.imu_callback, 50
        )
        self.pub_pose = self.create_publisher(PoseStamped, self.output_topic, 10)
        self.br = TransformBroadcaster(self)

        period = 1.0 / max(self.publish_rate_hz, 1.0)
        self.timer = self.create_timer(period, self.publish_fused)

    def load_config(self, file_name):
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, 'configs', file_name)
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def gnss_callback(self, msg: PoseStamped):
        self.latest_gnss = msg

    def imu_callback(self, msg: Imu):
        self.latest_imu = msg

    def publish_fused(self):
        if self.latest_gnss is None:
            return

        fused = PoseStamped()
        fused.header = self.latest_gnss.header
        fused.header.frame_id = self.map_frame

        # Position from GNSS
        fused.pose.position = self.latest_gnss.pose.position

        # Orientation preference: IMU if available, else GNSS
        if self.use_imu_orientation and self.latest_imu is not None:
            fused.pose.orientation = self.latest_imu.orientation
        else:
            fused.pose.orientation = self.latest_gnss.pose.orientation

        # Smooth pose if we already have a filtered pose
        if self.filtered_pose is None:
            self.filtered_pose = fused
        else:
            self.filtered_pose.pose.position.x = self.lerp(
                self.filtered_pose.pose.position.x, fused.pose.position.x, self.pos_alpha
            )
            self.filtered_pose.pose.position.y = self.lerp(
                self.filtered_pose.pose.position.y, fused.pose.position.y, self.pos_alpha
            )
            self.filtered_pose.pose.position.z = self.lerp(
                self.filtered_pose.pose.position.z, fused.pose.position.z, self.pos_alpha
            )
            self.filtered_pose.pose.orientation = self.slerp_quat(
                self.filtered_pose.pose.orientation, fused.pose.orientation, self.ori_alpha
            )

        self.pub_pose.publish(self.filtered_pose)

        if self.publish_tf:
            t_map_base = TransformStamped()
            t_map_base.header.stamp = self.filtered_pose.header.stamp
            t_map_base.header.frame_id = self.map_frame
            t_map_base.child_frame_id = self.base_frame
            t_map_base.transform.translation.x = self.filtered_pose.pose.position.x
            t_map_base.transform.translation.y = self.filtered_pose.pose.position.y
            t_map_base.transform.translation.z = self.filtered_pose.pose.position.z
            t_map_base.transform.rotation = self.filtered_pose.pose.orientation
            self.br.sendTransform(t_map_base)

    def lerp(self, a, b, alpha):
        return a + (b - a) * alpha

    def slerp_quat(self, q1, q2, alpha):
        v1 = np.array([q1.x, q1.y, q1.z, q1.w], dtype=float)
        v2 = np.array([q2.x, q2.y, q2.z, q2.w], dtype=float)
        if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
            return q2
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        dot = float(np.dot(v1, v2))
        if dot < 0.0:
            v2 = -v2
            dot = -dot
        dot = min(1.0, max(dot, -1.0))
        if dot > 0.9995:
            result = v1 + alpha * (v2 - v1)
            result = result / np.linalg.norm(result)
        else:
            theta_0 = math.acos(dot)
            sin_theta_0 = math.sin(theta_0)
            theta = theta_0 * alpha
            sin_theta = math.sin(theta)
            s0 = math.cos(theta) - dot * sin_theta / sin_theta_0
            s1 = sin_theta / sin_theta_0
            result = (s0 * v1) + (s1 * v2)
        return type(q1)(x=float(result[0]), y=float(result[1]), z=float(result[2]), w=float(result[3]))


def main(args=None):
    rclpy.init(args=args)
    node = GnssImuFusion()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
