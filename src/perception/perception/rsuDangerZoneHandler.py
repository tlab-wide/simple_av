#!/usr/bin/env python3

import os
import yaml
from dataclasses import dataclass
from typing import List, Tuple

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.duration import Duration as RclpyDuration

from ament_index_python.packages import get_package_share_directory
from std_msgs.msg import Bool
from autoware_perception_msgs.msg import PredictedObjects
from simple_av_msgs.msg import LocalizationIntersectionStatus
from geometry_msgs.msg import Pose
from tf2_ros import Buffer, TransformListener
from tf2_geometry_msgs import do_transform_pose


@dataclass
class PolygonRegion:
    name: str
    polygon_type: str
    intersection_id: str
    polygon_id: str
    points: List[Tuple[float, float, float]]


class RsuDangerZoneHandler(Node):
    def __init__(self):
        super().__init__('rsu_danger_zone_handler')

        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('output_topic', '/simple_av/perception/rsu_danger_detected')
        self.declare_parameter('intersection_status_topic', 'simple_av/localization/intersection_status')
        self.declare_parameter('rsu1_topic', '/v2x/rsu1/predicted_object')
        self.declare_parameter('rsu2_topic', '/v2x/rsu2/predicted_object')
        self.declare_parameter('rsu4_topic', '/v2x/rsu4/predicted_object')
        self.declare_parameter('danger_polygon_type', 'sw')

        self.map_frame = self.get_parameter('map_frame').value
        self.output_topic = self.get_parameter('output_topic').value
        self.intersection_status_topic = self.get_parameter('intersection_status_topic').value
        self.danger_polygon_type = self.get_parameter('danger_polygon_type').value

        self.rsu_topics = {
            '1': self.get_parameter('rsu1_topic').value,
            '2': self.get_parameter('rsu2_topic').value,
            '4': self.get_parameter('rsu4_topic').value,
        }

        self.pub = self.create_publisher(Bool, self.output_topic, 10)

        self.subscriptionIntersectionAwareness = self.create_subscription(
            LocalizationIntersectionStatus,
            self.intersection_status_topic,
            self.intersectionAwareness_callback,
            10
        )

        self.rsu_subs = {}
        self.rsu_msgs = {}
        for key, topic in self.rsu_topics.items():
            self.rsu_subs[key] = self.create_subscription(
                PredictedObjects, topic, self.make_rsu_callback(key), 10
            )
            self.rsu_msgs[key] = None

        self.intersection_name = None

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.intersections_layouts = self.load_intersections_layouts()

    def make_rsu_callback(self, key):
        def _cb(msg):
            self.rsu_msgs[key] = msg
            if self.intersection_name == key:
                self.evaluate_and_publish(msg)
        return _cb

    def intersectionAwareness_callback(self, msg):
        self.intersection_name = msg.intersection_name
        if self.intersection_name in self.rsu_msgs and self.rsu_msgs[self.intersection_name] is not None:
            self.evaluate_and_publish(self.rsu_msgs[self.intersection_name])
        else:
            self.pub.publish(Bool(data=False))

    def load_intersections_layouts(self) -> List[PolygonRegion]:
        package_dir = get_package_share_directory("common")
        yaml_path = os.path.join(package_dir, "zones", "intersections_danger_zones.yaml")

        try:
            with open(yaml_path, "r") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            self.get_logger().error(f"Failed to read YAML: {e}")
            return []

        if "intersections" not in data:
            self.get_logger().error("YAML missing 'intersections' root key.")
            return []

        parsed_polygons = []
        for inter_id, inter_data in data["intersections"].items():
            for category_name, category_value in inter_data.items():
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

    def is_point_in_polygon(self, point, polygon_points):
        x, y = point[0], point[1]
        inside = False
        n = len(polygon_points)
        p1x, p1y = polygon_points[0][0], polygon_points[0][1]
        for i in range(n + 1):
            p2x, p2y = polygon_points[i % n][0], polygon_points[i % n][1]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def lookup_transform(self, target_frame, source_frame, stamp):
        try:
            return self.tf_buffer.lookup_transform(
                target_frame,
                source_frame,
                stamp,
                timeout=RclpyDuration(seconds=0.0),
            )
        except Exception:
            try:
                return self.tf_buffer.lookup_transform(
                    target_frame,
                    source_frame,
                    Time(),
                    timeout=RclpyDuration(seconds=0.0),
                )
            except Exception as exc:
                self.get_logger().warning(
                    f"TF transform failed {source_frame} -> {target_frame}: {exc}"
                )
                return None

    def evaluate_and_publish(self, msg: PredictedObjects):
        if not self.intersection_name:
            self.pub.publish(Bool(data=False))
            return

        danger_zones = [
            p for p in self.intersections_layouts
            if p.intersection_id == self.intersection_name and p.polygon_type == self.danger_polygon_type
        ]
        if not danger_zones:
            self.pub.publish(Bool(data=False))
            return

        source_frame = msg.header.frame_id if msg.header.frame_id else self.map_frame
        transform = None
        if source_frame != self.map_frame:
            transform = self.lookup_transform(self.map_frame, source_frame, msg.header.stamp)
            if transform is None:
                self.pub.publish(Bool(data=False))
                return

        for obj in msg.objects:
            pose = obj.kinematics.initial_pose_with_covariance.pose
            if transform is not None:
                pose = do_transform_pose(pose, transform)

            point = (pose.position.x, pose.position.y, pose.position.z)
            for polygon in danger_zones:
                if self.is_point_in_polygon(point, polygon.points):
                    self.pub.publish(Bool(data=True))
                    return

        self.pub.publish(Bool(data=False))


def main(args=None):
    rclpy.init(args=args)
    node = RsuDangerZoneHandler()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
