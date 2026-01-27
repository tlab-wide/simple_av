import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path


class GNSSPathPublisher(Node):
    def __init__(self):
        super().__init__('rviz_path_monitor')
        self.subscription = self.create_subscription(
            PoseStamped,
            '/sensing/gnss/pose',
            self.pose_callback,
            10
        )
        self.publisher = self.create_publisher(Path, '/simple_av/path', 10)
        self.path_msg = Path()
        self.path_msg.header.frame_id = 'map'  # Ensure this matches the incoming poses

        self.get_logger().info('GNSS to Path node initialized.')

    def pose_callback(self, msg: PoseStamped):
        # Append the new pose to the path
        self.path_msg.header.stamp = msg.header.stamp  # Keep the latest time
        self.path_msg.poses.append(msg)
        self.publisher.publish(self.path_msg)


def main(args=None):
    rclpy.init(args=args)
    node = GNSSPathPublisher()
    try:
        rclpy.spin(node)  # <-- keep node alive, RViz can subscribe anytime
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
