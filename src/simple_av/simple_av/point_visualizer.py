import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from simple_av_msgs.msg import PlanningPathPlanningMsg, PlanningMotionPlanningMsg # adjust if your msg package is different

"""
points_visualizer Node

This ROS 2 node provides a generic mechanism to visualize important points 
in RViz. The purpose of this node is to make debugging and monitoring easier 
by displaying dynamic or static points used in various software modules, 
such as:

- Lookahead points from path planning (used by Pure Pursuit controllers)
- Stop points, goal points, or intermediate waypoints
- Any other points of interest in the vehicle or map frame

By using this node, multiple point topics can be visualized in RViz as 
Markers, providing clear visual feedback of the vehicle's planning, logic, 
and decision-making processes. This approach decouples visualization from 
the logic of the algorithms and keeps RViz displays organized and flexible.
"""


class point_visualizer(Node):
    def __init__(self):
        super().__init__('point_visualizer')

        # Publisher for visualization marker
        self.lookahead_pub = self.create_publisher(Marker, '/lookahead_point_marker', 10)
        self.stop_point_pub = self.create_publisher(Marker, '/stop_point_marker', 10)

        # Subscribe to path planning topic
        self.create_subscription(
            PlanningPathPlanningMsg,
            '/simple_av/planning/path_planning',
            self.lookahead_callback,
            10
        )

        # Subscribe to motion planning topic
        self.create_subscription(
            PlanningMotionPlanningMsg,
            '/simple_av/planning/motion_planning',
            self.stopPoint_callback,
            10
        )

    def lookahead_callback(self, msg: PlanningPathPlanningMsg):
        marker = Marker()
        marker.header.frame_id = "map"  # display in map frame
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "lookahead"
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position = msg.look_ahead_point  # geometry_msgs/Point
        marker.pose.orientation.w = 1.0
        marker.scale.x = 1.5
        marker.scale.y = 1.5
        marker.scale.z = 1.5
        marker.color.r = 35.0/255.0
        marker.color.g = 199.0/255.0
        marker.color.b = 48.0/255.0
        marker.color.a = 0.8
        marker.lifetime.sec = 0  # 0 = forever

        self.lookahead_pub.publish(marker)
        self.get_logger().debug(f"Published lookahead point at {msg.look_ahead_point.x}, {msg.look_ahead_point.y}, {msg.look_ahead_point.z}")

    def stopPoint_callback(self, msg: PlanningMotionPlanningMsg):
        marker = Marker()
        marker.header.frame_id = "map"  # display in map frame
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "stop_point"
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position = msg.stop_point  # geometry_msgs/Point
        marker.pose.orientation.w = 1.0
        marker.scale.x = 2.0
        marker.scale.y = 2.0
        marker.scale.z = 2.0
        marker.color.r = 200.0/255.0
        marker.color.g = 23.0/255.0
        marker.color.b = 38.0/255.0
        marker.color.a = 0.8
        marker.lifetime.sec = 0  # 0 = forever

        self.stop_point_pub.publish(marker)
        self.get_logger().debug(f"Published stop point at {msg.stop_point.x}, {msg.stop_point.y}, {msg.stop_point.z}")


def main(args=None):
    rclpy.init(args=args)
    node = point_visualizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
