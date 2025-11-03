import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import yaml
import os
from ament_index_python.packages import get_package_share_directory
from simple_av_msgs.msg import PlanningPathPlanningMsg, PlanningMotionPlanningMsg  # adjust if needed
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
- Any other points of interest in the vehicle or map frame

By using this node, multiple point topics can be visualized in RViz as 
Markers, providing clear visual feedback of the vehicle's planning, logic, 
and decision-making processes. This approach decouples visualization from 
the logic of the algorithms and keeps RViz displays organized and flexible.
"""

@dataclass
class Sidewalk:
    name: str
    points: List[Tuple[float, float, float]]


class point_visualizer(Node):
    def __init__(self):
        super().__init__('rviz_point_visualizer')

        # Publishers
        self.lookahead_pub = self.create_publisher(Marker, '/lookahead_point_marker', 10)
        self.stop_point_pub = self.create_publisher(Marker, '/stop_point_marker', 10)

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            durability=rclpy.qos.QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        self.sidewalk_pub = self.create_publisher(Marker, '/sidewalk_marker', qos)


        # Subscriptions
        self.create_subscription(
            PlanningPathPlanningMsg,
            '/simple_av/planning/path_planning',
            self.lookahead_callback,
            10
        )
        self.create_subscription(
            PlanningMotionPlanningMsg,
            '/simple_av/planning/motion_planning',
            self.stop_point_callback,
            10
        )


        # Load YAML sidewalk data
        self.layout_data = self.load_intersection_layout()
        if not self.layout_data:
            self.get_logger().error("No layout data to parse.")
        else:
            self.sidewalks = self.get_layout_data()
            self.layout_timer = self.create_timer(1.0, self.publish_layouts)


    def load_intersection_layout(self):
        package_share_directory = get_package_share_directory('common')
        intersections_danger_zones_path = os.path.join(package_share_directory, "zones", 'intersections_danger_zones.yaml')

        try:
            with open(intersections_danger_zones_path, 'r') as f:
                intersections_danger_zones = yaml.safe_load(f)
            self.get_logger().info("YAML file loaded successfully.")
        except Exception as e:
            self.get_logger().error(f"Failed to load YAML file: {e}")
            intersections_danger_zones = None

        return intersections_danger_zones

    # ---- parse into structured sidewalks ----
    def get_layout_data(self):
        sidewalks = []
        try:
            intersection = self.layout_data['intersections']['2']
            for sw_name, sw_data in intersection.items():
                self.get_logger().info(f"debug se name: {sw_name} - sw data: {sw_data}")
                points = [tuple(p) for p in sw_data["points"]]
                sidewalks.append(Sidewalk(name=sw_name, points=points))
            self.get_logger().info(f"Loaded {len(sidewalks)} sidewalks from YAML.")
        except Exception as e:
            self.get_logger().error(f"Failed to parse sidewalks: {e}")
            return None

        return sidewalks

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


    def stop_point_callback(self, msg: PlanningMotionPlanningMsg):
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


    def publish_layouts(self):
        """Publishes all layouts as red polygon outlines in RViz."""
        if not self.layout_data:
            self.get_logger().error("No sidewalk data loaded.")
            return

        for idx, sw in enumerate(self.sidewalks):
            try:
                marker = Marker()
                marker.header.frame_id = "map"
                marker.header.stamp = self.get_clock().now().to_msg()
                marker.ns = "sidewalk_layout"
                marker.id = idx
                marker.type = Marker.LINE_STRIP
                marker.action = Marker.ADD

                # Add each vertex as a Point
                for x, y, z in sw.points:
                    pt = Point()
                    pt.x, pt.y, pt.z = x, y, z
                    marker.points.append(pt)

                # Close polygon by connecting last → first
                if len(sw.points) > 2:
                    first = Point()
                    first.x, first.y, first.z = sw.points[0]
                    marker.points.append(first)

                # Line thickness
                marker.scale.x = 0.3

                # Red color for all
                marker.color.r = 1.0
                marker.color.g = 0.0
                marker.color.b = 0.0
                marker.color.a = 0.9

                # Lifetime forever
                marker.lifetime.sec = 0

                self.sidewalk_pub.publish(marker)
                self.get_logger().info(f"Published {sw.name} as red polygon with {len(sw.points)} vertices.")

            except Exception as e:
                self.get_logger().error(f"Error publishing {sw.name}: {e}")



def main(args=None):
    rclpy.init(args=args)
    node = point_visualizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
