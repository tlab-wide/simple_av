#!/usr/bin/env python3

import math
from dataclasses import dataclass

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.time import Time

from autoware_perception_msgs.msg import TrackedObjects, PredictedObjects, PredictedObject, PredictedObjectKinematics, PredictedPath
from geometry_msgs.msg import Pose, PoseWithCovariance, TwistWithCovariance, AccelWithCovariance
from builtin_interfaces.msg import Duration


@dataclass
class LastState:
    pos: np.ndarray
    stamp_ns: int


class ObjectPrediction(Node):
    def __init__(self):
        super().__init__('object_prediction_node')

        self.declare_parameter('input_topic', '/simple_av/perception/tracked_objects')
        self.declare_parameter('output_topic', '/simple_av/perception/predicted_objects')
        self.declare_parameter('target_frame', 'base_link')
        self.declare_parameter('prediction_horizon_sec', 3.0)
        self.declare_parameter('prediction_time_step_sec', 0.5)
        self.declare_parameter('use_twist_from_input', False)
        self.declare_parameter('use_heading_from_velocity', False)

        self.input_topic = self.get_parameter('input_topic').value
        self.output_topic = self.get_parameter('output_topic').value
        self.target_frame = self.get_parameter('target_frame').value
        self.prediction_horizon_sec = float(self.get_parameter('prediction_horizon_sec').value)
        self.prediction_time_step_sec = float(self.get_parameter('prediction_time_step_sec').value)
        self.use_twist_from_input = bool(self.get_parameter('use_twist_from_input').value)
        self.use_heading_from_velocity = bool(self.get_parameter('use_heading_from_velocity').value)

        self.subscription = self.create_subscription(
            TrackedObjects,
            self.input_topic,
            self.tracked_objects_callback,
            10
        )
        self.publisher = self.create_publisher(PredictedObjects, self.output_topic, 10)

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

    def tracked_objects_callback(self, msg: TrackedObjects):
        stamp = Time.from_msg(msg.header.stamp)
        now_ns = stamp.nanoseconds

        out = PredictedObjects()
        out.header = msg.header
        out.header.frame_id = self.target_frame

        dt_step = max(self.prediction_time_step_sec, 0.05)
        horizon = max(self.prediction_horizon_sec, dt_step)
        steps = int(horizon / dt_step)

        for obj in msg.objects:
            key = self.uuid_key(obj.object_id)
            pose = obj.kinematics.pose_with_covariance.pose
            pos = np.array([pose.position.x, pose.position.y, pose.position.z], dtype=float)

            velocity = np.zeros(3, dtype=float)
            input_twist = np.array([
                obj.kinematics.twist_with_covariance.twist.linear.x,
                obj.kinematics.twist_with_covariance.twist.linear.y,
                obj.kinematics.twist_with_covariance.twist.linear.z,
            ], dtype=float)

            if self.use_twist_from_input and np.linalg.norm(input_twist[:2]) > 1e-3:
                velocity = input_twist
            else:
                last = self.last_states.get(key)
                if last is not None:
                    dt = (now_ns - last.stamp_ns) / 1e9
                    if dt > 1e-6:
                        velocity = (pos - last.pos) / dt
                    else:
                        velocity = input_twist
                else:
                    velocity = input_twist

            self.last_states[key] = LastState(pos=pos, stamp_ns=now_ns)

            predicted_obj = PredictedObject()
            predicted_obj.object_id = obj.object_id
            predicted_obj.existence_probability = obj.existence_probability
            predicted_obj.classification = obj.classification
            predicted_obj.shape = obj.shape

            kin = PredictedObjectKinematics()
            kin.initial_pose_with_covariance = PoseWithCovariance()
            kin.initial_pose_with_covariance.pose = pose
            kin.initial_pose_with_covariance.covariance = obj.kinematics.pose_with_covariance.covariance

            kin.initial_twist_with_covariance = TwistWithCovariance()
            kin.initial_twist_with_covariance.twist.linear.x = float(velocity[0])
            kin.initial_twist_with_covariance.twist.linear.y = float(velocity[1])
            kin.initial_twist_with_covariance.twist.linear.z = float(velocity[2])

            kin.initial_acceleration_with_covariance = AccelWithCovariance()

            path = PredictedPath()
            path.time_step = self.build_duration(dt_step)
            path.confidence = 1.0
            path.path = []
            use_vel_heading = self.use_heading_from_velocity and np.linalg.norm(velocity[:2]) > 1e-3
            yaw = math.atan2(velocity[1], velocity[0]) if use_vel_heading else None

            for i in range(steps + 1):
                t = i * dt_step
                p = Pose()
                p.position.x = pose.position.x + velocity[0] * t
                p.position.y = pose.position.y + velocity[1] * t
                p.position.z = pose.position.z + velocity[2] * t
                if use_vel_heading:
                    p.orientation = self.quat_from_yaw(yaw)
                else:
                    p.orientation = pose.orientation
                path.path.append(p)

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
