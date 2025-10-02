import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from simple_av_msgs.msg import PlanningPathPlanningMsg  # adjust if your msg package is different

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


class LookaheadViz(Node):
    def __init__(self):
        super().__init__('lookahead_viz')

        # Publisher for visualization marker
        self.marker_pub = self.create_publisher(Marker, '/lookahead_point_marker', 10)

        # Subscribe to planning topic
        self.create_subscription(
            PlanningPathPlanningMsg,
            '/simple_av/planning/path_planning',
            self.lookahead_callback,
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
        marker.scale.x = 0.5
        marker.scale.y = 0.5
        marker.scale.z = 0.5
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0
        marker.lifetime.sec = 0  # 0 = forever

        self.marker_pub.publish(marker)
        self.get_logger().debug(f"Published lookahead point at {msg.look_ahead_point.x}, {msg.look_ahead_point.y}, {msg.look_ahead_point.z}")


def main(args=None):
    rclpy.init(args=args)
    node = LookaheadViz()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
