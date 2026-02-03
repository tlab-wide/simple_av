#!/usr/bin/env python3

import math
from dataclasses import dataclass

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.time import Time

from autoware_perception_msgs.msg import TrackedObjects, PredictedObjects, PredictedObject, PredictedObjectKinematics, PredictedPath
from geometry_msgs.msg import Pose, PoseWithCovariance, TwistWithCovariance, AccelWithCovariance, Vector3Stamped
from builtin_interfaces.msg import Duration
from rclpy.duration import Duration as RclpyDuration
from tf2_ros import Buffer, TransformListener
from tf2_geometry_msgs import do_transform_pose, do_transform_vector3


@dataclass
class LastState:
    history: list  # list of (stamp_ns, pos)


class ObjectPrediction(Node):
    def __init__(self):
        super().__init__('object_prediction_node')

        self.declare_parameter('input_topic', '/simple_av/perception/tracked_objects')
        self.declare_parameter('output_topic', '/simple_av/perception/predicted_objects')
        self.declare_parameter('target_frame', 'base_link')
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('prediction_horizon_sec', 3.0)
        self.declare_parameter('prediction_time_step_sec', 0.5)
        self.declare_parameter('use_twist_from_input', False)
        self.declare_parameter('use_heading_from_velocity', False)
        self.declare_parameter('use_heading_for_twist', False)
        self.declare_parameter('use_velocity_for_heading', True)
        self.declare_parameter('min_speed_for_heading', 0.2)
        self.declare_parameter('history_size', 5)
        self.declare_parameter('min_history_samples', 3)

        self.input_topic = self.get_parameter('input_topic').value
        self.output_topic = self.get_parameter('output_topic').value
        self.target_frame = self.get_parameter('target_frame').value
        self.map_frame = self.get_parameter('map_frame').value
        self.prediction_horizon_sec = float(self.get_parameter('prediction_horizon_sec').value)
        self.prediction_time_step_sec = float(self.get_parameter('prediction_time_step_sec').value)
        self.use_twist_from_input = bool(self.get_parameter('use_twist_from_input').value)
        self.use_heading_from_velocity = bool(self.get_parameter('use_heading_from_velocity').value)
        self.use_heading_for_twist = bool(self.get_parameter('use_heading_for_twist').value)
        self.use_velocity_for_heading = bool(self.get_parameter('use_velocity_for_heading').value)
        self.min_speed_for_heading = float(self.get_parameter('min_speed_for_heading').value)
        self.history_size = int(self.get_parameter('history_size').value)
        self.min_history_samples = int(self.get_parameter('min_history_samples').value)

        self.subscription = self.create_subscription(
            TrackedObjects,
            self.input_topic,
            self.tracked_objects_callback,
            10
        )
        self.publisher = self.create_publisher(PredictedObjects, self.output_topic, 10)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.last_states = {}

    def uuid_key(self, uuid_msg) -> str:
        return bytes(uuid_msg.uuid).hex()

    def build_duration(self, seconds: float) -> Duration:
        sec = int(math.floor(seconds))
        nsec = int((seconds - sec) * 1e9)
        return Duration(sec=sec, nanosec=nsec)

    def quat_from_yaw(self, yaw: float):
        q = Pose().orientation
        q.w = math.cos(yaw / 2.0)
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        return q

    def yaw_from_quat(self, q):
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        return math.atan2(siny_cosp, cosy_cosp)

    def transform_vector(self, v: np.ndarray, transform) -> np.ndarray:
        vec = Vector3Stamped()
        vec.vector.x = float(v[0])
        vec.vector.y = float(v[1])
        vec.vector.z = float(v[2])
        vec_out = do_transform_vector3(vec, transform)
        return np.array([vec_out.vector.x, vec_out.vector.y, vec_out.vector.z], dtype=float)

    def estimate_velocity_from_history(self, history):
        if len(history) < 2:
            return None
        stamps = np.array([h[0] for h in history], dtype=float) / 1e9
        t0 = stamps[0]
        t = stamps - t0
        if np.max(t) <= 1e-6:
            return None
        positions = np.array([h[1] for h in history], dtype=float)
        # Fit x(t), y(t), z(t) with least squares line: p = a*t + b
        A = np.vstack([t, np.ones_like(t)]).T
        vx, _ = np.linalg.lstsq(A, positions[:, 0], rcond=None)[0]
        vy, _ = np.linalg.lstsq(A, positions[:, 1], rcond=None)[0]
        vz, _ = np.linalg.lstsq(A, positions[:, 2], rcond=None)[0]
        return np.array([vx, vy, vz], dtype=float)

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

    def tracked_objects_callback(self, msg: TrackedObjects):
        stamp = Time.from_msg(msg.header.stamp)
        now_ns = stamp.nanoseconds

        base_in_map_tf = self.lookup_transform(self.map_frame, self.target_frame, msg.header.stamp)
        map_in_base_tf = self.lookup_transform(self.target_frame, self.map_frame, msg.header.stamp)
        if base_in_map_tf is None or map_in_base_tf is None:
            return

        out = PredictedObjects()
        out.header = msg.header
        out.header.frame_id = self.target_frame

        dt_step = max(self.prediction_time_step_sec, 0.05)
        horizon = max(self.prediction_horizon_sec, dt_step)
        steps = int(horizon / dt_step)

        for obj in msg.objects:
            key = self.uuid_key(obj.object_id)
            pose = obj.kinematics.pose_with_covariance.pose
            pose_map = do_transform_pose(pose, base_in_map_tf)
            pos = np.array([pose_map.position.x, pose_map.position.y, pose_map.position.z], dtype=float)

            velocity = np.zeros(3, dtype=float)
            input_twist = np.array([
                obj.kinematics.twist_with_covariance.twist.linear.x,
                obj.kinematics.twist_with_covariance.twist.linear.y,
                obj.kinematics.twist_with_covariance.twist.linear.z,
            ], dtype=float)

            history_state = self.last_states.get(key)
            if history_state is None:
                history_state = LastState(history=[])
                self.last_states[key] = history_state

            history_state.history.append((now_ns, pos))
            if len(history_state.history) > self.history_size:
                history_state.history = history_state.history[-self.history_size:]

            if self.use_twist_from_input and np.linalg.norm(input_twist[:2]) > 1e-3:
                velocity = input_twist
            else:
                if len(history_state.history) >= max(2, self.min_history_samples):
                    v = self.estimate_velocity_from_history(history_state.history)
                    if v is not None:
                        velocity = v
                    else:
                        velocity = input_twist
                elif len(history_state.history) >= 2:
                    prev_ns, prev_pos = history_state.history[-2]
                    dt = (now_ns - prev_ns) / 1e9
                    if dt > 1e-6:
                        velocity = (pos - prev_pos) / dt
                    else:
                        velocity = input_twist
                else:
                    velocity = input_twist

            predicted_obj = PredictedObject()
            predicted_obj.object_id = obj.object_id
            predicted_obj.existence_probability = obj.existence_probability
            predicted_obj.classification = obj.classification
            predicted_obj.shape = obj.shape

            kin = PredictedObjectKinematics()
            kin.initial_pose_with_covariance = PoseWithCovariance()
            pose_bl = do_transform_pose(pose_map, map_in_base_tf)
            kin.initial_pose_with_covariance.pose = pose_bl
            kin.initial_pose_with_covariance.covariance = obj.kinematics.pose_with_covariance.covariance

            kin.initial_twist_with_covariance = TwistWithCovariance()
            kin.initial_acceleration_with_covariance = AccelWithCovariance()

            path = PredictedPath()
            path.time_step = self.build_duration(dt_step)
            path.confidence = 1.0
            path.path = []
            use_vel_heading = self.use_heading_from_velocity and np.linalg.norm(velocity[:2]) > 1e-3
            yaw = math.atan2(velocity[1], velocity[0]) if use_vel_heading else None

            first_map = None
            second_map = None
            for i in range(steps + 1):
                t = i * dt_step
                p_map = Pose()
                p_map.position.x = pose_map.position.x + velocity[0] * t
                p_map.position.y = pose_map.position.y + velocity[1] * t
                p_map.position.z = pose_map.position.z + velocity[2] * t
                if use_vel_heading:
                    p_map.orientation = self.quat_from_yaw(yaw)
                else:
                    p_map.orientation = pose_map.orientation
                if i == 0:
                    first_map = p_map
                elif i == 1:
                    second_map = p_map
                p_bl = do_transform_pose(p_map, map_in_base_tf)
                if i == 0 and self.use_velocity_for_heading and use_vel_heading:
                    kin.initial_pose_with_covariance.pose.orientation = p_bl.orientation
                path.path.append(p_bl)

            if first_map is not None and second_map is not None:
                vel_map = np.array([
                    (second_map.position.x - first_map.position.x) / dt_step,
                    (second_map.position.y - first_map.position.y) / dt_step,
                    (second_map.position.z - first_map.position.z) / dt_step,
                ], dtype=float)
                vel_bl = self.transform_vector(vel_map, map_in_base_tf)
            else:
                vel_bl = self.transform_vector(velocity, map_in_base_tf)

            kin.initial_twist_with_covariance = TwistWithCovariance()
            speed = float(np.linalg.norm(vel_bl[:2]))
            if self.use_heading_for_twist and speed >= self.min_speed_for_heading:
                yaw_bl = self.yaw_from_quat(kin.initial_pose_with_covariance.pose.orientation)
                kin.initial_twist_with_covariance.twist.linear.x = speed * math.cos(yaw_bl)
                kin.initial_twist_with_covariance.twist.linear.y = speed * math.sin(yaw_bl)
                kin.initial_twist_with_covariance.twist.linear.z = float(vel_bl[2])
            else:
                kin.initial_twist_with_covariance.twist.linear.x = float(vel_bl[0])
                kin.initial_twist_with_covariance.twist.linear.y = float(vel_bl[1])
                kin.initial_twist_with_covariance.twist.linear.z = float(vel_bl[2])

            kin.predicted_paths = [path]
            predicted_obj.kinematics = kin
            out.objects.append(predicted_obj)

        self.publisher.publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = ObjectPrediction()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
