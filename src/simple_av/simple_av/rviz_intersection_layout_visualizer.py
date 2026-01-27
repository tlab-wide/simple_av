#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import yaml
import os
from dataclasses import dataclass
from typing import List, Tuple
from ament_index_python.packages import get_package_share_directory
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy


# ---------------------------------------
#              DATACLASSES
# ---------------------------------------

@dataclass
class PolygonRegion:
    """Any polygon region from YAML (inside, sidewalks, lanes, etc.)"""
    name: str
    polygon_type: str               # 'inside', 'sw', 'lane', 'lanes'
    intersection_id: str
    polygon_id: str
    points: List[Tuple[float, float, float]]


# ---------------------------------------
#              VISUALIZER NODE
# ---------------------------------------

class IntersectionVisualizer(Node):
    def __init__(self):
        super().__init__("intersection_danger_zone_visualizer")

        # QoS for static map layout
        qos = QoSProfile(
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_ALL
        )

        self.pub = self.create_publisher(Marker, "/intersection_layouts", qos)
        # self.pub = self.create_publisher(Marker, "/intersection_layouts", 10)


        # Load data
        self.polygons = self.load_intersections_layouts()
        
        if not self.polygons:
            self.get_logger().error("❌ No polygons parsed from YAML.")
        else:
            self.get_logger().info(f"✔ Loaded {len(self.polygons)} polygons from YAML.")

        # Publish once
        self.timer = self.create_timer(5.0, self.publish_polygons)


    # ---------------------------------------
    #              LOAD YAML
    # ---------------------------------------

    def load_intersections_layouts(self) -> List[PolygonRegion]:
        package_dir = get_package_share_directory("common")
        yaml_path = os.path.join(package_dir, "zones", "intersections_danger_zones.yaml")

        try:
            with open(yaml_path, "r") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            self.get_logger().error(f"❌ Failed to read YAML: {e}")
            return []

        if "intersections" not in data:
            self.get_logger().error("❌ YAML missing 'intersections' root key.")
            return []

        parsed_polygons = []

        # Iterate through intersections
        for inter_id, inter_data in data["intersections"].items():

            # Example categories: inside, sw, lane, lanes
            for category_name, category_value in inter_data.items():

                # Category that directly contains "points" (ex: inside)
                if isinstance(category_value, dict) and "points" in category_value:
                    parsed_polygons.append(
                        PolygonRegion(
                            name=f"{category_name}",
                            polygon_type=category_name,
                            intersection_id=str(inter_id),
                            polygon_id=str(0),
                            points=[tuple(p) for p in category_value["points"]]
                        )
                    )
                    continue

                # Categories containing multiple numbered polygons (sw / lane sets)
                if isinstance(category_value, dict):
                    for poly_id, poly_data in category_value.items():
                        if "points" in poly_data:
                            parsed_polygons.append(
                                PolygonRegion(
                                    name=f"{category_name}_{poly_id}",
                                    polygon_type=category_name,
                                    intersection_id=str(inter_id),
                                    polygon_id=str(poly_id),
                                    points=[tuple(p) for p in poly_data["points"]]
                                )
                            )

        return parsed_polygons


    # ---------------------------------------
    #              PUBLISHER
    # ---------------------------------------

    def publish_polygons(self):
        if not self.polygons:
            return
        for idx, poly in enumerate(self.polygons):
            try:
                self.get_logger().debug(
                    f"publishing : intersection_{poly.intersection_id}_{poly.polygon_type}_{poly.polygon_id}"
                )
                marker = Marker()
                marker.header.frame_id = "map"
                marker.header.stamp = rclpy.time.Time().to_msg()
                marker.ns = f"intersection_{poly.intersection_id}_{poly.polygon_type}_{poly.polygon_id}"
                marker.id = idx
                marker.type = Marker.LINE_STRIP
                marker.action = Marker.ADD
                marker.scale.x = 0.25   # line thickness

                # Color conventions
                if poly.polygon_type == "inside":
                    marker.color.r, marker.color.g, marker.color.b = (1.0, 0.5, 0.0)  # orange
                elif poly.polygon_type == "sw":
                    marker.color.r, marker.color.g, marker.color.b = (0.0, 1.0, 0.0)  # green
                elif poly.polygon_type == "cw":
                    marker.color.r, marker.color.g, marker.color.b = (1.0, 0.9, 0.0)  # yellow
                elif poly.polygon_type in ("lane", "lanes"):
                    marker.color.r, marker.color.g, marker.color.b = (0.0, 0.6, 1.0)  # blue
                else:
                    marker.color.r, marker.color.g, marker.color.b = (1.0, 0.0, 0.0)  # red default

                marker.color.a = 1.0

                # Add polygon points
                for x, y, z in poly.points:
                    p = Point(x=x, y=y, z=z)
                    marker.points.append(p)

                # Close loop
                if len(poly.points) > 2:
                    first = poly.points[0]
                    marker.points.append(Point(x=first[0], y=first[1], z=first[2]))

                marker.lifetime.sec = 0  # forever
                
                self.pub.publish(marker)

            except Exception as e:
                self.get_logger().error(f"❌ Failed to publish polygon {poly.name}: {e}")
        
        # 🔥 disable timer after first publish
        self.destroy_timer(self.timer)
        self.timer = None
        self.get_logger().info("Done. Timer destroyed, no more publishing.")
    


def main(args=None):
    rclpy.init(args=args)
    node = IntersectionVisualizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
