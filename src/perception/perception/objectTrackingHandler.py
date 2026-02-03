#!/usr/bin/env python3

import math
from dataclasses import dataclass
from uuid import uuid4

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.time import Time

from geometry_msgs.msg import Pose, PoseWithCovariance, TwistWithCovariance, AccelWithCovariance
from unique_identifier_msgs.msg import UUID
from autoware_perception_msgs.msg import DetectedObjects, TrackedObjects, TrackedObject, TrackedObjectKinematics
from tf2_ros import Buffer, TransformListener
from tf2_geometry_msgs import do_transform_pose


@dataclass
class TrackState:
    uuid_msg: UUID
    label: int
    last_pos_global: np.ndarray
    last_stamp_ns: int


class ObjectTracking(Node):
    def __init__(self):
        super().__init__('object_tracking_node')

        self.declare_parameter('input_topic', '/simple_av/perception/obu_sensing')
        self.declare_parameter('output_topic', '/simple_av/perception/tracked_objects')
        self.declare_parameter('target_frame', 'base_link')
        self.declare_parameter('max_match_distance', 2.0)
        self.declare_parameter('track_timeout_sec', 1.0)
        self.input_topic = self.get_parameter('input_topic').value
        self.output_topic = self.get_parameter('output_topic').value
        self.target_frame = self.get_parameter('target_frame').value
        self.max_match_distance = float(self.get_parameter('max_match_distance').value)
        self.track_timeout_sec = float(self.get_parameter('track_timeout_sec').value)

        self.subscription = self.create_subscription(
            DetectedObjects,
            self.input_topic,
            self.detected_objects_callback,
            10
        )
        self.publisher = self.create_publisher(TrackedObjects, self.output_topic, 10)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.tracks = {}
        self.map_frame = 'map'

    def make_uuid(self):
        u = uuid4()
        msg = UUID()
        msg.uuid = list(u.bytes)
        return msg, u.hex

    def get_label(self, obj) -> int:
        if obj.classification:
            return int(obj.classification[0].label)
        return -1

    def to_global(self, pos_bl: np.ndarray, base_in_map_tf) -> np.ndarray:
        if base_in_map_tf is None:
            return pos_bl
        pose_bl = Pose()
        pose_bl.position.x = float(pos_bl[0])
        pose_bl.position.y = float(pos_bl[1])
        pose_bl.position.z = float(pos_bl[2])
        pose_bl.orientation.w = 1.0
        pose_map = do_transform_pose(pose_bl, base_in_map_tf)
        return np.array([
            pose_map.position.x,
            pose_map.position.y,
            pose_map.position.z
        ], dtype=float)

    def transform_pose_to_base(self, pose, sensor_to_base_tf, header):
        if header is None or not header.frame_id or header.frame_id == self.target_frame:
            return pose
        if sensor_to_base_tf is None:
            return None
        return do_transform_pose(pose, sensor_to_base_tf)

    def prune_tracks(self, now_ns: int):
        timeout_ns = int(self.track_timeout_sec * 1e9)
        stale = [k for k, v in self.tracks.items() if now_ns - v.last_stamp_ns > timeout_ns]
        for k in stale:
            del self.tracks[k]

    def match_track(self, label: int, pos_global: np.ndarray, used_tracks: set):
        best_id = None
        best_dist = None
        for track_id, track in self.tracks.items():
            if track_id in used_tracks:
                continue
            if track.label != label:
                continue
            dist = float(np.linalg.norm(pos_global - track.last_pos_global))
            if dist <= self.max_match_distance and (best_dist is None or dist < best_dist):
                best_dist = dist
                best_id = track_id
        return best_id

    def detected_objects_callback(self, msg: DetectedObjects):
        stamp = Time.from_msg(msg.header.stamp)
        now_ns = stamp.nanoseconds
        self.prune_tracks(now_ns)

        tracked_msg = TrackedObjects()
        tracked_msg.header = msg.header
        tracked_msg.header.frame_id = self.target_frame

        used_tracks = set()
        sensor_to_base_tf = None
        base_in_map_tf = None

        if msg.header.frame_id and msg.header.frame_id != self.target_frame:
            try:
                sensor_to_base_tf = self.tf_buffer.lookup_transform(
                    self.target_frame,
                    msg.header.frame_id,
                    msg.header.stamp,
                    timeout=Duration(seconds=0.0),
                )
            except Exception:
                try:
                    sensor_to_base_tf = self.tf_buffer.lookup_transform(
                        self.target_frame,
                        msg.header.frame_id,
                        Time(),
                        timeout=Duration(seconds=0.0),
                    )
                except Exception as exc:
                    self.get_logger().warning(
                        f"TF transform failed {msg.header.frame_id} -> {self.target_frame}: {exc}"
                    )

        try:
            base_in_map_tf = self.tf_buffer.lookup_transform(
                self.map_frame,
                self.target_frame,
                msg.header.stamp,
                timeout=Duration(seconds=0.0),
            )
        except Exception:
            try:
                base_in_map_tf = self.tf_buffer.lookup_transform(
                    self.map_frame,
                    self.target_frame,
                    Time(),
                    timeout=Duration(seconds=0.0),
                )
            except Exception as exc:
                self.get_logger().warning(
                    f"TF transform failed {self.map_frame} -> {self.target_frame}: {exc}"
                )

        for obj in msg.objects:
            label = self.get_label(obj)
            pose = obj.kinematics.pose_with_covariance.pose
            pose = self.transform_pose_to_base(pose, sensor_to_base_tf, msg.header)
            if pose is None:
                continue

            pos_bl = np.array([pose.position.x, pose.position.y, pose.position.z], dtype=float)
            pos_global = self.to_global(pos_bl, base_in_map_tf)

            track_id = self.match_track(label, pos_global, used_tracks)
            if track_id is None:
                uuid_msg, track_id = self.make_uuid()
                self.tracks[track_id] = TrackState(
                    uuid_msg=uuid_msg,
                    label=label,
                    last_pos_global=pos_global,
                    last_stamp_ns=now_ns,
                )
            else:
                track = self.tracks[track_id]
                track.last_pos_global = pos_global
                track.last_stamp_ns = now_ns

            used_tracks.add(track_id)

            tracked_obj = TrackedObject()
            tracked_obj.object_id = self.tracks[track_id].uuid_msg
            tracked_obj.existence_probability = obj.existence_probability
            tracked_obj.classification = obj.classification
            tracked_obj.shape = obj.shape

            kin = TrackedObjectKinematics()
            kin.pose_with_covariance = PoseWithCovariance()
            kin.pose_with_covariance.pose = pose
            kin.pose_with_covariance.covariance = obj.kinematics.pose_with_covariance.covariance

            if obj.kinematics.has_twist:
                kin.twist_with_covariance = obj.kinematics.twist_with_covariance
            else:
                kin.twist_with_covariance = TwistWithCovariance()

            kin.acceleration_with_covariance = AccelWithCovariance()
            kin.orientation_availability = obj.kinematics.orientation_availability
            speed = math.hypot(
                kin.twist_with_covariance.twist.linear.x,
                kin.twist_with_covariance.twist.linear.y
            )
            kin.is_stationary = speed < 0.2

            tracked_obj.kinematics = kin
            tracked_msg.objects.append(tracked_obj)

        self.publisher.publish(tracked_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ObjectTracking()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
