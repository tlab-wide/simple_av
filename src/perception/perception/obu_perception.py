#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from autoware_perception_msgs.msg import DetectedObjects


class ObuPerception(Node):
    def __init__(self):
        super().__init__('obu_perception')

        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)

        self.input_topic = self.declare_parameter('input_topic', '/OBU/Sensing').value
        self.output_topic = self.declare_parameter('output_topic', '/simple_av/perception/obu_sensing').value

        self.sub = self.create_subscription(DetectedObjects, self.input_topic, self.callback, 10)
        self.pub = self.create_publisher(DetectedObjects, self.output_topic, 10)

    def callback(self, msg: DetectedObjects):
        # Refresh header stamp with local clock to avoid future/extrapolation issues
        msg.header.stamp = self.get_clock().now().to_msg()
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
