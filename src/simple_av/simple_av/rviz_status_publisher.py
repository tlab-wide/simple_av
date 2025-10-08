import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from std_msgs.msg import String
from simple_av_msgs.msg import PlanningPathPlanningMsg, PlanningMotionPlanningMsg # adjust if your msg package is different

class RVizTextPublisher(Node):
    def __init__(self):
        super().__init__('rviz_status_publisher')
        # Publisher for RViz text marker
        self.marker_pub = self.create_publisher(Marker, '/status_marker', 10)

        # Subscribe to motion planning topic
        self.create_subscription(
            PlanningMotionPlanningMsg,
            '/simple_av/planning/motion_planning',
            self.stopPoint_callback,
            10
        )

        self.current_text = "Hello world"
        self.publish_text_marker()

    def stopPoint_callback(self, msg):
        """Callback to update text dynamically."""
        self.current_text = msg.status.data
        self.publish_text_marker()

    def publish_text_marker(self):
        """Publish text marker to RViz."""
        marker = Marker()
        marker.header.frame_id = "map"  # or "base_link" depending on where you want it
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "text_display"
        marker.id = 0
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD

        # Position in RViz (adjust to make it visible)
        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 3.0  # height of the text

        # Orientation (optional)
        marker.pose.orientation.w = 1.0

        # Text properties
        marker.scale.x = 5.0
        marker.scale.y = 5.0
        marker.scale.z = 5.0
        marker.color.a = 1.0  # opacity (1 = fully visible)
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0

        marker.text = self.current_text

        self.marker_pub.publish(marker)
        self.get_logger().info(f"Displayed text: {self.current_text}")


def main(args=None):
    rclpy.init(args=args)
    node = RVizTextPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
