#!/usr/bin/env python3

import math
import os
import yaml
import numpy as np

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TransformStamped
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from ament_index_python.packages import get_package_share_directory


class LocalizationFusion(Node):
    def __init__(self):
        super().__init__('localization_fusion')

        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)

        self.cfg = self.load_config('localization_fusion.yaml').get('localization_fusion', {})
        self.use_ground_truth = bool(self.cfg.get('use_ground_truth_pose', True))
        self.gnss_topic = self.cfg.get('gnss_topic', '/sensing/gnss/pose')
        self.imu_topic = self.cfg.get('imu_topic', '/sensing/imu/tamagawa/imu_raw')
        self.gt_topic = self.cfg.get('ground_truth_pose_topic', '/awsim/ground_truth/vehicle/pose')
        self.output_odom_topic = self.cfg.get('output_odom_topic', '/simple_av/localization/odometry_fused')
        self.map_frame = self.cfg.get('map_frame', 'map')
        self.base_frame = self.cfg.get('base_frame', 'base_link')
        self.publish_tf = bool(self.cfg.get('publish_tf', True))
        self.publish_rate_hz = float(self.cfg.get('publish_rate_hz', 50.0))
        self.use_imu_orientation = bool(self.cfg.get('use_imu_orientation', False))
        self.pos_alpha = float(self.cfg.get('position_smoothing_alpha', 0.2))
        self.ori_alpha = float(self.cfg.get('orientation_smoothing_alpha', 0.2))

        self.latest_gnss = None
        self.latest_imu = None
        self.filtered_pose = None

        self.prev_gt_pose = None
        self.prev_gt_time = None

        self.sub_gnss = self.create_subscription(PoseStamped, self.gnss_topic, self.gnss_callback, 10)
        self.sub_imu = self.create_subscription(Imu, self.imu_topic, self.imu_callback, 50)
        self.sub_gt = self.create_subscription(PoseStamped, self.gt_topic, self.gt_callback, 50)

        self.pub_odom = self.create_publisher(Odometry, self.output_odom_topic, 10)
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

    def gt_callback(self, msg: PoseStamped):
        if not self.use_ground_truth:
            return
        odom = Odometry()
        odom.header = msg.header
        odom.header.frame_id = self.map_frame
        odom.child_frame_id = self.base_frame
        odom.pose.pose = msg.pose

        if self.prev_gt_pose is not None and self.prev_gt_time is not None:
            dt = (msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9) - self.prev_gt_time
            if dt > 0.0:
                dx = msg.pose.position.x - self.prev_gt_pose.position.x
                dy = msg.pose.position.y - self.prev_gt_pose.position.y
                dz = msg.pose.position.z - self.prev_gt_pose.position.z
                speed = math.sqrt(dx * dx + dy * dy + dz * dz) / dt
                odom.twist.twist.linear.x = speed
        self.prev_gt_pose = msg.pose
        self.prev_gt_time = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9

        self.pub_odom.publish(odom)
        if self.publish_tf:
            self.publish_map_tf_from_odom(odom)

    def publish_fused(self):
        if self.use_ground_truth:
            return
        if self.latest_gnss is None:
            return

        fused = PoseStamped()
        fused.header = self.latest_gnss.header
        fused.header.frame_id = self.map_frame
        fused.pose.position = self.latest_gnss.pose.position

        if self.use_imu_orientation and self.latest_imu is not None:
            fused.pose.orientation = self.latest_imu.orientation
        else:
            fused.pose.orientation = self.latest_gnss.pose.orientation

        if self.filtered_pose is None:
            self.filtered_pose = fused
        else:
            self.filtered_pose.pose.position.x = self.lerp(self.filtered_pose.pose.position.x, fused.pose.position.x, self.pos_alpha)
            self.filtered_pose.pose.position.y = self.lerp(self.filtered_pose.pose.position.y, fused.pose.position.y, self.pos_alpha)
            self.filtered_pose.pose.position.z = self.lerp(self.filtered_pose.pose.position.z, fused.pose.position.z, self.pos_alpha)
            self.filtered_pose.pose.orientation = self.slerp_quat(self.filtered_pose.pose.orientation, fused.pose.orientation, self.ori_alpha)

        odom = Odometry()
        odom.header = self.filtered_pose.header
        odom.header.frame_id = self.map_frame
        odom.child_frame_id = self.base_frame
        odom.pose.pose = self.filtered_pose.pose
        self.pub_odom.publish(odom)

        if self.publish_tf:
            self.publish_map_tf_from_odom(odom)

    def publish_map_tf_from_odom(self, odom: Odometry):
        t_map_base = TransformStamped()
        t_map_base.header.stamp = odom.header.stamp
        t_map_base.header.frame_id = self.map_frame
        t_map_base.child_frame_id = self.base_frame
        t_map_base.transform.translation.x = odom.pose.pose.position.x
        t_map_base.transform.translation.y = odom.pose.pose.position.y
        t_map_base.transform.translation.z = odom.pose.pose.position.z
        t_map_base.transform.rotation = odom.pose.pose.orientation
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
    node = LocalizationFusion()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
