is this corrrect?
import os
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
from builtin_interfaces.msg import Duration
from ament_index_python.packages import get_package_share_directory
import lanelet2
import lanelet2.io
import lanelet2.projection


class LaneletMapPublisher(Node):
    def __init__(self):
        super().__init__('lanelet_map_publisher')

        # Resolve the map path
        common_share = get_package_share_directory('common')
        map_path = os.path.join(common_share, 'maps', 'lanelet2_map.osm')
        self.get_logger().info(f"Loading Lanelet2 map from: {map_path}")

        # Publisher (latched-like QoS)
        qos = rclpy.qos.QoSProfile(
            depth=1,
            durability=rclpy.qos.QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=rclpy.qos.QoSReliabilityPolicy.RELIABLE
        )
        self.pub = self.create_publisher(MarkerArray, 'lanelet_map_markers', qos)

        lat_origin = 35.733  # approx center of your map
        lon_origin = 139.934


        # Load lanelet map
        projector = lanelet2.projection.UtmProjector(lanelet2.io.Origin(lat_origin, lon_origin))
        self.map = lanelet2.io.load(map_path, projector)

        self.publish_map()

    def publish_map(self):
        marker_array = MarkerArray()
        marker_id = 0

        for lanelet in self.map.laneletLayer:
            # Left boundary
            left_marker = Marker()
            left_marker.header.frame_id = "map"
            left_marker.header.stamp = self.get_clock().now().to_msg()
            left_marker.ns = "lanelet_left"
            left_marker.id = marker_id
            marker_id += 1
            left_marker.type = Marker.LINE_STRIP
            left_marker.action = Marker.ADD
            left_marker.scale.x = 0.5
            left_marker.color.r = 1.0
            left_marker.color.a = 1.0
            left_marker.lifetime = Duration()  # zero duration → forever
            left_marker.points = [self.point_to_ros(p) for p in lanelet.leftBound]
            marker_array.markers.append(left_marker)

            # Right boundary
            right_marker = Marker()
            right_marker.header.frame_id = "map"
            right_marker.header.stamp = self.get_clock().now().to_msg()
            right_marker.ns = "lanelet_right"
            right_marker.id = marker_id
            marker_id += 1
            right_marker.type = Marker.LINE_STRIP
            right_marker.action = Marker.ADD
            right_marker.scale.x = 0.5
            right_marker.color.g = 1.0
            right_marker.color.a = 1.0
            right_marker.lifetime = Duration(sec=0)
            right_marker.points = [self.point_to_ros(p) for p in lanelet.rightBound]
            marker_array.markers.append(right_marker)

        self.pub.publish(marker_array)
        self.get_logger().info("Published Lanelet2 map markers once.")

    def point_to_ros(self, p):
        from geometry_msgs.msg import Point
        pt = Point()
        pt.x = p.x
        pt.y = p.y
        pt.z = p.z
        return pt


def main(args=None):
    rclpy.init(args=args)
    node = LaneletMapPublisher()

    # Spin a few times to ensure RViz receives the latched message
    for _ in range(5):
        rclpy.spin_once(node, timeout_sec=0.1)

    node.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()