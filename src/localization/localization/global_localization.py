#!/usr/bin/env python3

import json
import math
import os
import yaml

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration as RclpyDuration
from rclpy.time import Time
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy
from tf2_ros import Buffer, TransformListener
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
from std_srvs.srv import Trigger

from simple_av_msgs.msg import LocalizationMsg
from geometry_msgs.msg import Point as GeoPoint


class Point:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def distance_to(self, other_point):
        dx = self.x - other_point.x
        dy = self.y - other_point.y
        dz = self.z - other_point.z
        return math.sqrt(dx**2 + dy**2 + dz**2)


class GlobalLocalization(Node):
    def __init__(self):
        super().__init__('global_localization')

        # Load scenario configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.vehicle_model = self.scenario_config['scenario']['vehicle_model']

        # Load the Json map
        self.map_data = self.load_map(self.vehicle_model)
        self.map_data = self.map_data["LaneLetsArray"]

        # Use TF from localization fusion (map -> base_link)
        self.map_frame = 'map'
        self.base_frame = 'base_link'
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
        )
        self.publisher = self.create_publisher(LocalizationMsg, 'simple_av/localization/global_location', qos_profile)
        self.service = self.create_service(Trigger, '/localization/trigger_global_localization', self.handle_request)

        self.pose_msg = PoseStamped()

    def config_file_loader(self, file_name):
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    def load_map(self, vehicle_model):
        package_share_directory = get_package_share_directory('common')
        if vehicle_model == 'lexus':
            json_file_path = os.path.join(package_share_directory, 'maps', 'Kashiwa-lexus.json')
        else:
            json_file_path = os.path.join(package_share_directory, 'maps', 'Kashiwa-bus.json')
        with open(json_file_path, 'r') as json_file:
            return json.load(json_file)

    def update_pose_from_tf(self):
        try:
            tf = self.tf_buffer.lookup_transform(
                self.map_frame,
                self.base_frame,
                Time(),
                timeout=RclpyDuration(seconds=0.0),
            )
        except Exception:
            return False

        pose_msg = PoseStamped()
        pose_msg.header = tf.header
        pose_msg.pose.position.x = tf.transform.translation.x
        pose_msg.pose.position.y = tf.transform.translation.y
        pose_msg.pose.position.z = tf.transform.translation.z
        pose_msg.pose.orientation = tf.transform.rotation
        self.pose_msg = pose_msg
        return True

    def get_lane(self, lane_name):
        lane_number = lane_name.replace("lanelet", "")
        lane_number = int(lane_number)
        if lane_number > len(self.map_data):
            return None
        return self.map_data[lane_number - 1]

    def get_closest_point_and_lane(self, current_position):
        closest_point = Point()
        closest_lanes_names = []
        closest_lane_name = String()
        min_distance = float('inf')

        for lane in self.map_data:
            lane_name = lane['name']
            waypoints = lane['dense_waypoints']
            for waypoint in waypoints:
                point = Point(waypoint['x'], waypoint['y'], waypoint['z'])
                distance = current_position.distance_to(point)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point
                    closest_lanes_names = [lane_name]
                elif distance == min_distance:
                    closest_lanes_names.append(lane_name)

        if len(closest_lanes_names) > 1:
            min_avg_distance = float('inf')
            for lane_name in closest_lanes_names:
                lane = self.get_lane(lane_name)
                if lane is None:
                    continue
                waypoints = lane['waypoints']
                if not waypoints:
                    continue
                cumulative_distance = 0.0
                for waypoint in waypoints:
                    point = Point(waypoint['x'], waypoint['y'], waypoint['z'])
                    cumulative_distance += current_position.distance_to(point)
                avg_distance = cumulative_distance / len(waypoints)
                if avg_distance < min_avg_distance:
                    min_avg_distance = avg_distance
                    closest_lane_name = lane_name
        elif len(closest_lanes_names) == 1:
            closest_lane_name = closest_lanes_names[0]

        return closest_point, closest_lane_name, min_distance

    def publish_global_location(self, closest_point, closest_lane_name, min_distance):
        msg = LocalizationMsg()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.closest_point = GeoPoint(x=closest_point.x, y=closest_point.y, z=closest_point.z)
        msg.closest_lane_names.data = closest_lane_name
        msg.minimal_distance = min_distance
        self.publisher.publish(msg)

    def handle_request(self, request, response):
        self.get_logger().info("Global localization requested")
        if not self.update_pose_from_tf():
            response.success = False
            response.message = "No TF available for global localization."
            return response
        pose = self.pose_msg.pose.position
        if pose.x == 0.0 and pose.y == 0.0 and pose.z == 0.0:
            response.success = False
            response.message = "Pose is zero; cannot global-localize."
            return response
        current_position = Point(pose.x, pose.y, pose.z)
        closest_point, closest_lane_name, min_distance = self.get_closest_point_and_lane(current_position)
        self.publish_global_location(closest_point, closest_lane_name, min_distance)
        self.get_logger().info(
            f"Global localization result lane={closest_lane_name} "
            f"closest_point=({closest_point.x:.2f}, {closest_point.y:.2f}, {closest_point.z:.2f}) "
            f"min_distance={min_distance:.2f}"
        )
        response.success = True
        response.message = f"Global localization OK: lane={closest_lane_name}, dist={min_distance:.2f}"
        return response


def main(args=None):
    rclpy.init(args=args)
    node = GlobalLocalization()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
