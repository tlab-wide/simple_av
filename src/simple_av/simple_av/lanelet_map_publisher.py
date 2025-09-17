import os
import xml.etree.ElementTree as ET

import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
from builtin_interfaces.msg import Duration
from geometry_msgs.msg import Point
from ament_index_python.packages import get_package_share_directory


class LaneletMapPublisher(Node):
    def __init__(self):
        super().__init__('lanelet_map_publisher')

        # Resolve the map path
        common_share = get_package_share_directory('common')
        map_path = os.path.join(common_share, 'maps', 'test.osm')
        self.get_logger().info(f"Loading Lanelet2 map from: {map_path}")

        # Publisher (latched-like QoS)
        qos = rclpy.qos.QoSProfile(
            depth=1,
            durability=rclpy.qos.QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=rclpy.qos.QoSReliabilityPolicy.RELIABLE
        )
        self.pub = self.create_publisher(MarkerArray, 'lanelet_map_markers', qos)

        # Load the OSM XML
        self.tree = ET.parse(map_path)
        self.root = self.tree.getroot()

        # Build node dictionary: id -> (x, y, z)
        self.nodes = {}
        for node in self.root.findall('node'):
            node_id = node.attrib['id']
            local_x = float(node.find("tag[@k='local_x']").attrib['v'])
            local_y = float(node.find("tag[@k='local_y']").attrib['v'])
            ele_tag = node.find("tag[@k='ele']")
            z = float(ele_tag.attrib['v']) if ele_tag is not None else 0.0
            self.nodes[node_id] = (local_x, local_y, z)

        # Build lanelets
        self.lanelets = []
        for lanelet in self.root.findall('lanelet'):
            left_nodes = [self.nodes[nd.attrib['ref']] for nd in lanelet.find('left').findall('nd')]
            right_nodes = [self.nodes[nd.attrib['ref']] for nd in lanelet.find('right').findall('nd')]
            self.lanelets.append({'left': left_nodes, 'right': right_nodes})

        # Publish marker array
        self.publish_map()

    def publish_map(self):
        marker_array = MarkerArray()
        marker_id = 0

        for lanelet in self.lanelets:
            # Left boundary
            left_marker = Marker()
            left_marker.header.frame_id = "map"
            left_marker.header.stamp = self.get_clock().now().to_msg()
            left_marker.ns = "lanelet_left"
            left_marker.id = marker_id
            marker_id += 1
            left_marker.type = Marker.LINE_STRIP
            left_marker.action = Marker.ADD
            left_marker.scale.x = 0.2
            left_marker.color.r = 1.0
            left_marker.color.a = 1.0
            left_marker.lifetime = Duration(sec=0)
            left_marker.points = [self.point_to_ros(p) for p in lanelet['left']]
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
            right_marker.scale.x = 0.2
            right_marker.color.g = 1.0
            right_marker.color.a = 1.0
            right_marker.lifetime = Duration(sec=0)
            right_marker.points = [self.point_to_ros(p) for p in lanelet['right']]
            marker_array.markers.append(right_marker)

        self.pub.publish(marker_array)
        self.get_logger().info("Published Lanelet2 map markers using local_x/local_y coordinates.")

    @staticmethod
    def point_to_ros(p):
        pt = Point()
        pt.x, pt.y, pt.z = p
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
