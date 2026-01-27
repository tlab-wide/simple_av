import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from std_msgs.msg import String
from geometry_msgs.msg import Point
from simple_av_msgs.msg import PlanningMotionPlanningMsg

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
        
        # Initialize defaults
        self.current_text = "Waiting for stop point..."
        self.stop_point = Point()
        self.stop_point.x = 0.0
        self.stop_point.y = 0.0
        self.stop_point.z = 0.0

        self.publish_text_marker()

    def stopPoint_callback(self, msg):
        """Callback to update text and position dynamically."""
        self.current_text = msg.stop_reason.data
        self.stop_point = msg.stop_point  # geometry_msgs/Point
        self.publish_text_marker()

    def publish_text_marker(self):
        """Publish text marker to RViz."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "text_display"
        marker.id = 0
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD

        # Position the text slightly above the stop point
        marker.pose.position.x = self.stop_point.x
        marker.pose.position.y = self.stop_point.y
        marker.pose.position.z = self.stop_point.z + 3.0  # lift text above the ground

        # Orientation
        marker.pose.orientation.w = 1.0

        # Text properties
        marker.scale.z = 1.5  # text height in meters
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0

        marker.text = self.current_text

        self.marker_pub.publish(marker)
        # self.get_logger().info(f"Displayed text '{self.current_text}' at ({self.stop_point.x:.2f}, {self.stop_point.y:.2f})")


def main(args=None):
    rclpy.init(args=args)
    node = RVizTextPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
