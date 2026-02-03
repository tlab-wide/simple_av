#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from autoware_perception_msgs.msg import DetectedObjects
from rclpy.duration import Duration
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener
from tf2_geometry_msgs import do_transform_pose


class ObuPerception(Node):
    def __init__(self):
        super().__init__('obu_perception')

        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)

        self.input_topic = self.declare_parameter('input_topic', '/OBU/Sensing').value
        self.output_topic = self.declare_parameter('output_topic', '/simple_av/perception/obu_sensing').value

        self.sub = self.create_subscription(DetectedObjects, self.input_topic, self.callback, 10)
        self.pub = self.create_publisher(DetectedObjects, self.output_topic, 10)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.target_frame = 'base_link'

    def callback(self, msg: DetectedObjects):
        # Refresh header stamp with local clock to avoid future/extrapolation issues
        msg.header.stamp = self.get_clock().now().to_msg()
        source_frame = msg.header.frame_id
        if not source_frame:
            self.get_logger().warning("OBU sensing message missing frame_id; skipping transform.")
            return

        transform = None
        try:
            transform = self.tf_buffer.lookup_transform(
                self.target_frame,
                source_frame,
                msg.header.stamp,
                timeout=Duration(seconds=0.0),
            )
        except Exception:
            try:
                transform = self.tf_buffer.lookup_transform(
                    self.target_frame,
                    source_frame,
                    Time(),
                    timeout=Duration(seconds=0.0),
                )
            except Exception as exc:
                self.get_logger().warning(
                    f"TF transform failed {source_frame} -> {self.target_frame}: {exc}"
                )
                return

        for obj in msg.objects:
            pose = obj.kinematics.pose_with_covariance.pose
            pose = do_transform_pose(pose, transform)
            obj.kinematics.pose_with_covariance.pose = pose

        msg.header.frame_id = self.target_frame
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ObuPerception()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
