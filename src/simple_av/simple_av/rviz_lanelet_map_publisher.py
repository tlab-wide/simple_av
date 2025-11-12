#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker, MarkerArray
import xml.etree.ElementTree as ET
import os
from builtin_interfaces.msg import Duration
from geometry_msgs.msg import Point
from ament_index_python.packages import get_package_share_directory


class LaneletMapPublisher(Node):
    def __init__(self):
        super().__init__('rviz_lanelet_map_publisher')

        # Resolve the map path
        common_share = get_package_share_directory('common')
        map_path = os.path.join(common_share, 'maps', 'test.osm')

        if not os.path.exists(map_path):
            self.get_logger().error(f"Lanelet map not found: {map_path}")
            return

        # Parse XML map
        self.nodes_dict = {}
        self.ways = []
        self._parse_map(map_path)

        # Publisher
        qos = rclpy.qos.QoSProfile(
            depth=1,
            durability=rclpy.qos.QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=rclpy.qos.QoSReliabilityPolicy.RELIABLE
        )
        self.publisher = self.create_publisher(MarkerArray, 'lanelet_map_markers', qos)
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info(f"Loaded lanelet map from: {map_path}")
        self.get_logger().info(f"Parsed {len(self.nodes_dict)} nodes and {len(self.ways)} ways.")

    def _parse_map(self, map_path: str):
        """Parse nodes and ways from Lanelet OSM file."""
        tree = ET.parse(map_path)
        root = tree.getroot()

        # Parse nodes (<node> with <tag k="local_x" v="..."/>)
        for node in root.findall('node'):
            node_id = node.attrib['id']
            x, y, z = None, None, None

            # Look for tags
            for tag in node.findall('tag'):
                if tag.attrib['k'] == 'local_x':
                    x = float(tag.attrib['v'])
                elif tag.attrib['k'] == 'local_y':
                    y = float(tag.attrib['v'])
                elif tag.attrib['k'] == 'ele':  # elevation (height)
                    z = float(tag.attrib['v'])

            # Fallback if no local_x/local_y found
            if x is None or y is None:
                x = float(node.attrib.get('lon'))
                y = float(node.attrib.get('lat'))

            if z is None:
                z = 0.0  # Default Z if not provided

            self.nodes_dict[node_id] = (x, y, z)

        # Parse ways (<way id> <nd ref=...>...</way>)
        for way in root.findall('way'):
            refs = [nd.attrib['ref'] for nd in way.findall('nd')]
            self.ways.append(refs)

    def create_marker(self, way_refs, way_id):
        """Create a Marker LINE_STRIP for a way."""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "lanelet_map"
        marker.id = way_id
        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD
        marker.scale.x = 0.3  # line thickness
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.color.a = 0.8  # fixed alpha

        # Convert node refs into geometry
        for ref in way_refs:
            if ref in self.nodes_dict:
                x, y, z = self.nodes_dict[ref]
                pt = Point()
                pt.x = x
                pt.y = y
                pt.z = z
                marker.points.append(pt)
            else:
                self.get_logger().warn(f"Missing node reference {ref} in way {way_id}")

        return marker

    def timer_callback(self):
        marker_array = MarkerArray()
        for i, way_refs in enumerate(self.ways):
            marker = self.create_marker(way_refs, i)
            marker_array.markers.append(marker)
        self.publisher.publish(marker_array)


def main(args=None):
    rclpy.init(args=args)
    node = LaneletMapPublisher()

    for i in range(2):
        rclpy.spin_once(node, timeout_sec=10.0)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
