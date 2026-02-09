#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point
from rclpy.duration import Duration as RclpyDuration
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener
from visualization_msgs.msg import Marker, MarkerArray

from autoware_vehicle_msgs.msg import GearCommand, VelocityReport
from autoware_control_msgs.msg import Control, Lateral, Longitudinal
from std_msgs.msg import Float32

from rclpy.qos import QoSProfile, DurabilityPolicy, HistoryPolicy, ReliabilityPolicy
from simple_av_msgs.msg import PlanningInternalMissionPlanMsg
from simple_av_msgs.msg import SimMonitor, LocalizationIntersectionStatus, Portal
import time
import math
from collections import deque
import numpy as np
import yaml
import os
from ament_index_python.packages import get_package_share_directory
from rclpy.parameter import Parameter
import time


class PIDController:
    def __init__(self, p_gain, i_gain, d_gain, sim_time=0.05, logger=None):
        self.kp = p_gain
        self.ki = i_gain
        self.kd = d_gain
        self.logger = logger

        self.current_time = sim_time
        self.last_time = self.current_time

        self.integrated_error = 0.0

        self.slidingWindow = deque(maxlen=20) # for storing only the 10 most recent errors

        self.previous_error = 0.0
    
    def updatePID(self, observed_vel, target_vel, sim_time):
        # print("debug speed: ", target_vel, observed_vel)
        error = target_vel - observed_vel
        self.current_time = sim_time
        
        delta_time = self.current_time - self.last_time  # Convert to seconds
        if self.logger:
            self.logger.debug(
                f"delta time: {delta_time} sim time: {sim_time} real time: {time.time()}"
            )
        self.slidingWindow.append(error)
        
        self.integrated_error = sum(self.slidingWindow) * delta_time
        derivative = (error - self.previous_error) / delta_time if delta_time > 0 else 0.0005

        P = self.kp * error
        I = self.ki * self.integrated_error
        D = self.kd * derivative
        
        acc_cmd = P + I + D

        self.last_time = self.current_time
        self.previous_error = error

        return acc_cmd


class VehicleControl(Node):
    def __init__(self):
        super().__init__('control')
        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        
        # Load configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.vehicle_model = self.scenario_config['scenario']['vehicle_model']
        self.vehicle_config = self.load_vehicle_config(self.vehicle_model)
        self.motion_behavior_config = self.config_file_loader("motion_behavior_config.yaml")

        self.vehicle_length = self.vehicle_config['dimensions']['length'] #meters
        self.vehicle_width = self.vehicle_config['dimensions']['width'] #meters
        self.wheel_base = self.vehicle_config['dimensions']['wheel_base'] #meters
        self.front_overhang = self.vehicle_config['dimensions']['front_overhang'] #meters
        self.back_overhang = self.vehicle_config['dimensions']['rear_overhang'] #meters
        
        self.previous_steering_angle = 0
        self.steering_gain = 0.2  # Proportional gain for steering
        perf_cfg = (
            self.motion_behavior_config['motion']
            .get('performance', {})
            .get(self.vehicle_model, {})
        )
        self.acceleration_rate = perf_cfg.get('acceleration_rate', 1.0)
        self.ACCEL_PROFILE = perf_cfg.get('accel_profile', [])
        
        self.maximum_Stereing = None
        self.normal_deceleration_rate = perf_cfg.get('normal_deceleration_rate', -1.0)
        
        # Use TF from localization fusion (map -> base_link)
        self.pose = PoseStamped()
        self.map_frame = 'map'
        self.base_frame = 'base_link'
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.subscriptionPose = self.create_subscription(PoseStamped, '/awsim/ground_truth/vehicle/pose', self.ground_truth_callback, 10)
        self.ground_truth = PoseStamped()

        self.subscriptionVelocityReport = self.create_subscription(VelocityReport, '/vehicle/status/velocity_status', self.velocity_report_callback, 10)
        self.velocity_report = VelocityReport()

        qos_profile_path = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL
        )
        self.subscriptionTrajectory = self.create_subscription(
            PlanningInternalMissionPlanMsg,
            '/simple_av/motion_planning/trajectory',
            self.trajectory_callback,
            qos_profile_path
        )
        self.path_of_waypoints = []
        self.speeds_on_path = []
        self.last_closest_point_index = None
        self.lookahead_point = None
        self.lookahead_index = None
        self.speed_limit = 0.0
        self.lookahead_distance_C = float(self.motion_behavior_config['motion']['lookahead']['coefficient'])
        self.lookahead_distance_B = float(self.motion_behavior_config['motion']['lookahead']['base'])
        self.densify_interval = float(self.motion_behavior_config['motion']['path']['densify_interval'])
        
        self.subscriptionIntersectionAwareness = self.create_subscription(
            LocalizationIntersectionStatus,
            'simple_av/localization/intersection_status',
            self.intersection_awareness_callback,
            10
        )
        self.intersection_awareness_intersection_name = None
        self.intersection_awareness_status = None

        self.subscriptionSimMonitor = self.create_subscription(SimMonitor, 'simple_av/sim_monitor', self.sim_monitor_callback, 100)
        self.sim_clock_rate = 0
        self.subscriptionPortal = self.create_subscription(
            Portal,
            'simple_av/portal',
            self.portal_callback,
            10
        )

        # Control loop timer (uses ROS time when use_sim_time is enabled)
        self.control_period_sec = 0.1
        self.control_timer = self.create_timer(self.control_period_sec, self.control)

        self.finished = False
        self.round_number = 0
        self.last_accel_cmd = 0.0
        self._last_log_time = {}

        # Publish topics
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            durability=DurabilityPolicy.TRANSIENT_LOCAL
        )
        
        # self.control_publisher = self.create_publisher(AckermannControlCommand, '/control/command/control_cmd', qos_profile)
        self.control_publisher = self.create_publisher(Control, '/control/command/control_cmd', qos_profile)
        self.gear_publisher = self.create_publisher(GearCommand, '/control/command/gear_cmd', qos_profile)
        # self.turn_indicator_publisher = self.create_publisher(TurnIndicatorsCommand, '/control/command/turn_indicators_cmd', qos_profile)
        self.status_marker_pub = self.create_publisher(
            MarkerArray,
            'simple_av/visualization/control_status_text',
            10
        )
        self.lookahead_marker_pub = self.create_publisher(
            Marker,
            '/simple_av/control/visualization/lookahead_point',
            10
        )
        self.speed_debug_pub = self.create_publisher(
            Float32,
            '/simple_av/control/debug/vehicle_speed',
            10
        )

        pid_config = self.motion_behavior_config.get('control', {}).get('pid', {})
        p_gain = float(pid_config.get('p_gain', 5.0))
        i_gain = float(pid_config.get('i_gain', 5.0))
        d_gain = float(pid_config.get('d_gain', 1.5))
        self.pid_controller = PIDController(p_gain=p_gain, i_gain=i_gain, d_gain=d_gain, logger=self.get_logger())

        self.node_shut = False
    
    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def load_vehicle_config(self, vehicle_model):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", "vehicle_config.yaml")

        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        # Retrieve the specific vehicle's configuration
        if vehicle_model in config["vehicles"]:
            return config["vehicles"][vehicle_model]
        else:
            raise ValueError(f"Vehicle type '{vehicle_model}' not found in the configuration.")

    def sim_monitor_callback(self, msg):
        self.sim_clock_rate = msg.sim_clock_rate

    def portal_callback(self, msg):
        self.round_number = int(msg.round_number)
        if not msg.finished or self.finished:
            return
        self.finished = True
        self.path_of_waypoints = []
        self.speeds_on_path = []
        self.lookahead_point = None
        self.lookahead_index = None
        self.speed_limit = 0.0
        self.last_closest_point_index = None

        gear_msg = GearCommand()
        gear_msg.stamp = self.get_clock().now().to_msg()
        gear_msg.command = GearCommand.PARK
        self.gear_publisher.publish(gear_msg)
        self.publish_status_markers(0.0, 0.0)
        self.node_shut = True
        self.get_logger().info("Scenario finished from portal -> parking and stopping control loop")

        if self.control_timer is not None:
            self.control_timer.cancel()

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
        self.pose = pose_msg
        return True

    def ground_truth_callback(self, msg):
        self.ground_truth = msg

    def velocity_report_callback(self, msg):
        self.velocity_report = msg

    def trajectory_callback(self, msg):
        if self.finished:
            return
        self.path_of_waypoints = [wp.waypoint for wp in msg.path]
        self.speeds_on_path = [float(getattr(wp, 'speed', 0.0)) for wp in msg.path]
        self.last_closest_point_index = None
        self.lookahead_point = None
        self.lookahead_index = None
        if msg.path:
            self.log_throttle(
                "info",
                "trajectory_rx",
                f"Received trajectory with {len(msg.path)} points",
                period_sec=1.0,
            )
    
    def intersection_awareness_callback(self, msg):
        self.intersection_awareness_intersection_name = msg.intersection_name
        self.intersection_awareness_status = msg.status

    def get_latest_messages(self):
        return self.pose, self.velocity_report
    
    def calculate_distance(self, point1, point2):
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def control(self):
        self.update_pose_from_tf()

        if self.finished:
            gear_msg = GearCommand()
            gear_msg.stamp = self.get_clock().now().to_msg()
            gear_msg.command = GearCommand.PARK
            self.gear_publisher.publish(gear_msg)
            return

        if not self.pose or not self.path_of_waypoints:
            self.get_logger().warning("No path or pose data")
            gear_msg = GearCommand()
            gear_msg.stamp = self.get_clock().now().to_msg()
            gear_msg.command = GearCommand.PARK
            self.gear_publisher.publish(gear_msg)
            return

        self.update_lookahead_point()
        current_speed = self.velocity_report.longitudinal_velocity if self.velocity_report else 0.0
        
        # Steer and Velocity Control
        control_msg = Control()
    
        control_msg.stamp = self.get_clock().now().to_msg()
        control_msg.lateral = self.get_lateral_command()
        control_msg.longitudinal = self.get_longitudinal_command()

        # Turn Indicator Light Control
        # turn_indicator_msg = TurnIndicatorsCommand()
        # turn_indicator_msg.stamp = self.get_clock().now().to_msg()
        
        # Gear Control
        gear_msg = GearCommand()
        gear_msg.stamp = self.get_clock().now().to_msg()
        self.get_logger().debug("drive")
        gear_msg.command = GearCommand.DRIVE

        self.control_publisher.publish(control_msg)
        # self.turn_indicator_publisher.publish(turn_indicator_msg)
        self.gear_publisher.publish(gear_msg)  
        self.publish_speed_debug()
        self.log_throttle(
            "info",
            "control_state",
            (
                f"traj_points={len(self.path_of_waypoints)} "
                f"lookahead_idx={self.lookahead_index} "
                f"speed_limit={self.speed_limit:.2f} "
                f"current_speed={current_speed:.2f}"
            ),
            period_sec=1.0,
        )

    def publish_speed_debug(self):
        speed_msg = Float32()
        speed_mps = float(self.velocity_report.longitudinal_velocity) if self.velocity_report else 0.0
        speed_msg.data = speed_mps * 3.6
        self.speed_debug_pub.publish(speed_msg)

    def log_throttle(self, level, key, msg, period_sec=1.0):
        now = self.get_clock().now().nanoseconds / 1e9
        last = self._last_log_time.get(key, 0.0)
        if now - last < period_sec:
            return
        self._last_log_time[key] = now
        if level == "debug":
            self.get_logger().debug(msg)
        elif level == "info":
            self.get_logger().info(msg)
        elif level == "warning":
            self.get_logger().warning(msg)
        elif level == "error":
            self.get_logger().error(msg)
        else:
            self.get_logger().info(msg)

    
    def get_lateral_command(self):
        lateral_command = Lateral()
        if self.pose and self.lookahead_point:
            steer = self.pure_pursuit_rear_axel()
            lateral_command.steering_tire_angle = steer
            lateral_command.steering_tire_rotation_rate = 0.1
            lateral_command.is_defined_steering_tire_rotation_rate = True
        else:
            lateral_command.steering_tire_angle = 0.0
            lateral_command.steering_tire_rotation_rate = 0.0
            lateral_command.is_defined_steering_tire_rotation_rate = True
        return lateral_command

    def get_longitudinal_command(self):

        current_speed = self.velocity_report.longitudinal_velocity if self.velocity_report else 0.0
        target_speed = self.speed_limit

        now_sec = self.get_clock().now().nanoseconds * 1e-9
        accel = self.pid_controller.updatePID(current_speed, target_speed, now_sec)
        
        deceleration_rate = self.normal_deceleration_rate

        self.get_logger().debug(f"calculated accel: {accel}")

        self.get_logger().debug("--------------------------")
        if accel > self.acceleration_rate:
            accel = self.get_accel_for_speed(current_speed)
        if accel < deceleration_rate:
            accel = deceleration_rate
        self.last_accel_cmd = accel

        longitudinal_command = Longitudinal()
        longitudinal_command.velocity = self.velocity_report.longitudinal_velocity
        longitudinal_command.acceleration = accel
        longitudinal_command.is_defined_acceleration = True
        longitudinal_command.jerk = 0.0
        longitudinal_command.is_defined_jerk = False

        self.get_logger().debug(
            f'speed: {current_speed}\n'
            f'accel: {accel}\n'
            f'target speed: {target_speed}\n'
        )
        self.publish_status_markers(target_speed, accel)
        return longitudinal_command

    def publish_status_markers(self, target_speed, accel_cmd=None):
        if not self.pose or not self.pose.pose:
            return
        marker_array = MarkerArray()
        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        base_x = self.pose.pose.position.x
        base_y = self.pose.pose.position.y - 2.0
        base_z = self.pose.pose.position.z + 3.0
        accel_value = self.last_accel_cmd if accel_cmd is None else float(accel_cmd)
        accel_is_decel = accel_value < -1e-3

        entries = [
            (
                "control_status_target_speed",
                "target_speed",
                f"{target_speed * 3.6:.1f} km/h",
                (1.0, 0.8, 0.2),
            ),
            (
                "control_status_speed_limit",
                "speed_limit",
                f"{self.speed_limit * 3.6:.1f} km/h",
                (0.8, 0.8, 1.0),
            ),
            (
                "control_status_acceleration",
                "acceleration",
                f"{accel_value:.2f} m/s^2" if accel_is_decel else f"{abs(accel_value):.2f} m/s^2",
                (1.0, 0.2, 0.2) if accel_is_decel else (0.2, 1.0, 0.2),
            ),
            (
                "control_status_intersection",
                "intersection",
                self.intersection_awareness_status or "none",
                (0.2, 1.0, 0.2),
            ),
            (
                "control_status_round",
                "round",
                f"{self.round_number}",
                (0.9, 0.9, 0.9),
            ),
        ]

        if self.finished:
            entries.append(
                (
                    "control_status_finished",
                    "scenario",
                    f"round {self.round_number} finished",
                    (1.0, 0.4, 0.1),
                )
            )

        for idx, (namespace, label, value, color) in enumerate(entries):
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = namespace
            marker.id = idx
            marker.type = Marker.TEXT_VIEW_FACING
            marker.action = Marker.ADD
            marker.pose.position = Point(
                x=base_x,
                y=base_y,
                z=base_z - idx * 0.6,
            )
            marker.pose.orientation.w = 1.0
            marker.scale.z = 0.6
            marker.color.r, marker.color.g, marker.color.b = color
            marker.color.a = 0.5
            marker.text = f"{label}: {value}"
            marker_array.markers.append(marker)

        self.status_marker_pub.publish(marker_array)

    def get_accel_for_speed(self, speed):
        for entry in self.ACCEL_PROFILE:
            try:
                min_speed = float(entry.get('min_speed', 0.0))
                max_speed = float(entry.get('max_speed', float('inf')))
                accel = float(entry.get('accel', self.acceleration_rate))
            except (TypeError, ValueError):
                continue
            if speed >= min_speed and speed < max_speed:
                return accel
        return self.acceleration_rate
    
    def filter(self, new_value, previous_value, gain):
        return gain * previous_value + (1 - gain) * new_value

    def find_closest_waypoint_index(self, vehicle_pose):
        if not self.path_of_waypoints:
            return None
        if self.last_closest_point_index is None:
            start_idx = 0
            end_idx = len(self.path_of_waypoints)
        else:
            window = 200
            start_idx = max(0, self.last_closest_point_index - window)
            end_idx = min(len(self.path_of_waypoints), self.last_closest_point_index + window)

        min_dist = float('inf')
        closest_idx = self.last_closest_point_index if self.last_closest_point_index is not None else 0
        for i in range(start_idx, end_idx):
            waypoint = self.path_of_waypoints[i]
            d = self.calculate_distance(waypoint, vehicle_pose)
            if d < min_dist:
                min_dist = d
                closest_idx = i

        if self.last_closest_point_index is not None and closest_idx < self.last_closest_point_index:
            closest_idx = self.last_closest_point_index

        self.last_closest_point_index = closest_idx
        return closest_idx

    def update_lookahead_point(self):
        if not self.path_of_waypoints or not self.pose:
            self.lookahead_point = None
            self.lookahead_index = None
            self.publish_lookahead_marker(None)
            return
        vehicle_pose = self.pose.pose.position
        closest_idx = self.find_closest_waypoint_index(vehicle_pose)
        if closest_idx is None:
            self.lookahead_point = None
            self.lookahead_index = None
            self.publish_lookahead_marker(None)
            return
        current_speed = self.velocity_report.longitudinal_velocity if self.velocity_report else 0.0
        lookahead_distance = current_speed * self.lookahead_distance_C + self.lookahead_distance_B
        steps = int(lookahead_distance / self.densify_interval) if self.densify_interval > 0.0 else 0
        lookahead_idx = min(len(self.path_of_waypoints) - 1, closest_idx + steps)
        self.lookahead_point = self.path_of_waypoints[lookahead_idx]
        self.lookahead_index = lookahead_idx
        if self.speeds_on_path:
            speed_idx = min(lookahead_idx, len(self.speeds_on_path) - 1)
            self.speed_limit = float(self.speeds_on_path[speed_idx])
        else:
            self.speed_limit = 0.0
        self.publish_lookahead_marker(self.lookahead_point)

    def publish_lookahead_marker(self, point):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "control_lookahead"
        marker.id = 0
        if point is None:
            marker.action = Marker.DELETE
            self.lookahead_marker_pub.publish(marker)
            return
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position = point
        marker.pose.orientation.w = 1.0
        marker.scale.x = 1.5
        marker.scale.y = 1.5
        marker.scale.z = 1.5
        marker.color.r = 35.0 / 255.0
        marker.color.g = 199.0 / 255.0
        marker.color.b = 48.0 / 255.0
        marker.color.a = 0.8
        self.lookahead_marker_pub.publish(marker)
    
    def pure_pursuit_rear_axel(self):
        yaw = self.get_yaw_from_pose(self.pose.pose.orientation)  # Vehicle heading (yaw angle)

        # Calculate lookahead point relative to base_link (rear axle center)
        lookahead_x = self.lookahead_point.x - self.pose.pose.position.x
        lookahead_y = self.lookahead_point.y - self.pose.pose.position.y

        # Adjust lookahead distance for vehicle length
        lookahead_dist = math.sqrt(lookahead_x ** 2 + lookahead_y ** 2)
        if lookahead_dist < 1e-6:
            return 0.0
        effective_lookahead_distance = lookahead_dist + self.front_overhang
        lookahead_x = effective_lookahead_distance * (lookahead_x / lookahead_dist)
        lookahead_y = effective_lookahead_distance * (lookahead_y / lookahead_dist)

        # Transform lookahead point to the vehicle's local coordinate system
        local_x = math.cos(yaw) * lookahead_x + math.sin(yaw) * lookahead_y
        local_y = -math.sin(yaw) * lookahead_x + math.cos(yaw) * lookahead_y

        # Calculate steering angle with effective wheelbase
        ld2 = lookahead_x ** 2 + lookahead_y ** 2
        effective_wheelbase = self.wheel_base + self.front_overhang + self.back_overhang + 5.0
        steering_angle = math.atan2(2.0 * local_y * effective_wheelbase, ld2)

        # Debugging info: left or right turn
        if steering_angle >= 0:
            self.get_logger().debug("Left Turn")
        else:
            self.get_logger().debug("Right Turn")

        return steering_angle

    def pure_pursuit_steering_angle(self):
        lookahead_x = self.lookahead_point.x - self.pose.pose.position.x
        lookahead_y = self.lookahead_point.y - self.pose.pose.position.y

        yaw = self.get_yaw_from_pose(self.pose.pose.orientation)
        self.get_logger().debug(f"degree: {math.degrees(yaw)}")

        local_x = math.cos(yaw) * lookahead_x + math.sin(yaw) * lookahead_y
        local_y = -math.sin(yaw) * lookahead_x + math.cos(yaw) * lookahead_y

        ld2 = lookahead_x ** 2 + lookahead_y ** 2
        steering_angle = math.atan2(2.0 * local_y * self.wheel_base, ld2)
        steering_angle = self.filter(steering_angle, self.previous_steering_angle, self.steering_gain)
        self.previous_steering_angle = steering_angle

        if steering_angle >= 0:
            self.get_logger().debug("Left")
        else:
            self.get_logger().debug("Right")
        # self.get_logger().info(
        #     f'steering_angle: {steering_angle}, yaw = {yaw}:\n'
        # )

        return steering_angle
    

    def get_yaw_from_pose(self, orientation):
        siny_cosp = 2 * (orientation.w * orientation.z + orientation.x * orientation.y)
        cosy_cosp = 1 - 2 * (orientation.y * orientation.y + orientation.z * orientation.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        return yaw


def main(args=None):
    rclpy.init(args=args)
    node = VehicleControl()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
