#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point
from visualization_msgs.msg import Marker, MarkerArray

from autoware_vehicle_msgs.msg import GearCommand, VelocityReport
from autoware_control_msgs.msg import Control, Lateral, Longitudinal

from rclpy.qos import QoSProfile, DurabilityPolicy, HistoryPolicy, ReliabilityPolicy
from simple_av_msgs.msg import PlanningPathPlanningMsg, PlanningMotionPlanningMsg, CollisionPredictionInfo
from simple_av_msgs.msg import SimMonitor, LocalizationIntersectionStatus
import time
import math
from collections import deque
import numpy as np
import yaml
import os
from ament_index_python.packages import get_package_share_directory
from simple_av_msgs.msg import Portal
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

        self.vehicle_length = self.vehicle_config['dimensions']['length'] #meters
        self.vehicle_width = self.vehicle_config['dimensions']['width'] #meters
        self.wheel_base = self.vehicle_config['dimensions']['wheel_base'] #meters
        self.front_overhang = self.vehicle_config['dimensions']['front_overhang'] #meters
        self.back_overhang = self.vehicle_config['dimensions']['rear_overhang'] #meters
        
        self.previous_steering_angle = 0
        self.steering_gain = 0.2  # Proportional gain for steering
        self.acceleration_rate = self.vehicle_config['performance']['acceleration_rate']
        self.ACCEL_PROFILE = self.vehicle_config['performance'].get('accel_profile', [])
        
        self.maximum_Stereing = None
        self.normal_deceleration_rate = self.vehicle_config['performance']['normal_deceleration_rate']
        self.normal_braking_deceleration_rate = self.vehicle_config['performance']['normal_braking_deceleration_rate']
        self.max_braking_deceleration_rate = self.vehicle_config['performance']['max_braking_deceleration_rate']
        
        # Subscribe topics
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        self.pose = PoseStamped()
        
        self.subscriptionPose = self.create_subscription(PoseStamped, '/awsim/ground_truth/vehicle/pose', self.ground_truth_callback, 10)
        self.ground_truth = PoseStamped()

        self.subscriptionVelocityReport = self.create_subscription(VelocityReport, '/vehicle/status/velocity_status', self.velocity_report_callback, 10)
        self.velocity_report = VelocityReport()

        self.subscriptionBehaviorPathPlanning = self.create_subscription(PlanningPathPlanningMsg, '/simple_av/planning/path_planning', self.path_planning_callback, 10)
        self.path_plan = PlanningPathPlanningMsg()
        
        self.subscriptionBehaviorMotionPlanning = self.create_subscription(PlanningMotionPlanningMsg, '/simple_av/planning/motion_planning', self.motion_planning_callback, 10)
        self.motion_plan = PlanningMotionPlanningMsg()

        self.subscriptionCollisionPrediction = self.create_subscription(
            CollisionPredictionInfo,
            "simple_av/planning/collision_prediction_info",
            self.collision_prediction_callback,
            10
        )
        self.collision_prediction_info = CollisionPredictionInfo()

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

        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False
        self.prev_reset = False
        self.last_reset_time_ns = None
        self.reset_cooldown = self.scenario_config['scenario'].get('reset_cooldown_seconds', 2.0)

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

        # self.pid_controller = PIDController(p_gain=2.8, i_gain=25.0, d_gain=1.5, logger=self.get_logger())
        self.pid_controller = PIDController(p_gain=5.0, i_gain=20.0, d_gain=1.5, logger=self.get_logger())

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
        now_ns = self.get_clock().now().nanoseconds
        reset_edge = msg.reset and not self.prev_reset
        cooldown_ok = (
            self.last_reset_time_ns is None or
            (now_ns - self.last_reset_time_ns) / 1e9 >= self.reset_cooldown
        )
        self.reset = reset_edge and cooldown_ok
        self.finished = msg.finished
        if self.reset:
            self.last_reset_time_ns = now_ns
        self.prev_reset = msg.reset

    def pose_callback(self, msg):
        self.pose = msg

    def ground_truth_callback(self, msg):
        self.ground_truth = msg

    def velocity_report_callback(self, msg):
        self.velocity_report = msg

    def path_planning_callback(self, msg):
        self.path_plan = msg
    
    def motion_planning_callback(self, msg):
        self.motion_plan = msg
    
    def collision_prediction_callback(self, msg):
        self.collision_prediction_info = msg
    
    def intersection_awareness_callback(self, msg):
        self.intersection_awareness_intersection_name = msg.intersection_name
        self.intersection_awareness_status = msg.status

    def get_latest_messages(self):
        return self.pose, self.velocity_report
    
    def calculate_distance(self, point1, point2):
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def control(self):

        if not self.velocity_report and not self.path_plan and not self.pose:
            self.get_logger().error("No, velocity report or lookahead or pose data")
            return
        
        if self.finished:
            self.node_shut = True
            gear_msg = GearCommand()
            gear_msg.stamp = self.get_clock().now().to_msg()
            self.get_logger().debug("park")
            gear_msg.command = GearCommand.PARK
            self.gear_publisher.publish(gear_msg)  
            return
        
        # if self.reset:
        #     time.sleep(0.2)

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
        if self.motion_plan.status.data == "Park":
            self.get_logger().debug("park")
            gear_msg.command = GearCommand.PARK
        else:
            self.get_logger().debug("drive")
            gear_msg.command = GearCommand.DRIVE

        self.control_publisher.publish(control_msg)
        # self.turn_indicator_publisher.publish(turn_indicator_msg)
        self.gear_publisher.publish(gear_msg)  


    
    def get_lateral_command(self):
        lateral_command = Lateral()
        if self.motion_plan.status.data == "Park" and self.reset:
            self.get_logger().debug("debug PARK")
            lateral_command.steering_tire_angle = 0.0
            lateral_command.steering_tire_rotation_rate = 0.0
        else:
            if self.pose and self.path_plan:
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
        target_speed = self.path_plan.speed_limit
        stop_point = self.motion_plan.stop_point
        if self.motion_plan.status.data == "Decelerate" and self.collision_prediction_info.collision_detected:
            stop_point = self.collision_prediction_info.object_position
        distance_to_stop = self.calculate_distance(stop_point, self.pose.pose.position)

        self.get_logger().debug(f"status: {self.motion_plan.status.data}")
        self.get_logger().debug(f"current_speed: {current_speed}")
        self.get_logger().debug(f"distance_to_stop: {distance_to_stop}")

        if self.motion_plan.status.data == "Decelerate" or self.motion_plan.status.data == "Stop_red" or self.reset:
            # print("debug: ", self.motion_plan.stop_point, type(self.motion_plan.stop_point))
            # print("debug: ", self.pose.pose.position, type(self.pose.pose.position))
            
            target_speed = self.calculate_target_speed_for_stop(distance_to_stop, current_speed)
            if self.motion_plan.status.data == "Stop_red" and distance_to_stop <= 4.0:
                self.get_logger().debug("Full stop!")
                target_speed = 0.0
            if self.motion_plan.status.data == "Decelerate" and distance_to_stop <= 4.0:
                self.get_logger().debug("Full stop!")
                target_speed = 0.0
            if self.reset:
                self.get_logger().debug("Full stop!")
                target_speed = 0.0
            
            self.get_logger().debug(f"Decelerate or stop red target_speed: {target_speed}")

        accel = self.pid_controller.updatePID(current_speed, target_speed, time.time() * self.sim_clock_rate)
        
        deceleration_rate = self.normal_deceleration_rate

        self.get_logger().debug(f"calculated accel: {accel}")
        if self.motion_plan.status.data == "Decelerate" or self.motion_plan.status.data == "Stop_red" or self.reset:
            self.get_logger().debug(
                f"normal braking deceleration {self.normal_braking_deceleration_rate}"
            )
            deceleration_rate = self.normal_braking_deceleration_rate

        if self.motion_plan.status.data == "Decelerate":
            if self.normal_braking_deceleration_rate != 0.0:
                stopping_distance = (current_speed ** 2) / (2.0 * abs(self.normal_braking_deceleration_rate))
            else:
                stopping_distance = float('inf')
            if distance_to_stop <= stopping_distance:
                deceleration_rate = self.max_braking_deceleration_rate

        if self.motion_plan.status.data == "Stop_red":
            if self.normal_braking_deceleration_rate != 0.0:
                stopping_distance = (current_speed ** 2) / (2.0 * abs(self.normal_braking_deceleration_rate))
            else:
                stopping_distance = float('inf')
            if distance_to_stop <= stopping_distance or (distance_to_stop <= 8.0 and current_speed >= 2):
                self.get_logger().debug(
                    f"MAX braking deceleration {self.max_braking_deceleration_rate}"
                )
                deceleration_rate = self.max_braking_deceleration_rate

        self.get_logger().debug("--------------------------")
        if accel > self.acceleration_rate:
            accel = self.get_accel_for_speed(current_speed)
        if accel < deceleration_rate:
            accel = deceleration_rate

        longitudinal_command = Longitudinal()
        longitudinal_command.velocity = self.velocity_report.longitudinal_velocity
        longitudinal_command.acceleration = accel
        longitudinal_command.is_defined_acceleration = True
        longitudinal_command.jerk = 0.0
        longitudinal_command.is_defined_jerk = False

        if self.motion_plan.status.data == "Decelerate" or self.motion_plan.status.data == "Stop_red":
            self.get_logger().debug(
            f'speed: {current_speed}\n'
            f'accel: {accel}\n'
            f'target speed: {target_speed}\n'
            f'stop distance: {distance_to_stop}\n'
            f'status : {self.motion_plan.status.data}\n'
        )
        else:
            self.get_logger().debug(
                f'speed: {current_speed}\n'
                f'accel: {accel}\n'
                f'target speed: {target_speed}\n'
                f'status : {self.motion_plan.status.data}\n'
            )
        self.publish_status_markers(distance_to_stop)
        return longitudinal_command

    def publish_status_markers(self, distance_to_stop):
        if not self.pose or not self.pose.pose:
            return
        marker_array = MarkerArray()
        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        base_x = self.pose.pose.position.x
        base_y = self.pose.pose.position.y - 2.0
        base_z = self.pose.pose.position.z + 3.0

        entries = [
            ("distance_to_stop", f"{distance_to_stop:.1f} m", (1.0, 0.2, 0.2)),
            ("motion_status", self.motion_plan.status.data, (1.0, 1.0, 0.2)),
            ("intersection", self.intersection_awareness_status or "none", (0.2, 1.0, 0.2)),
            ("reset", "true" if self.reset else "false", (1.0, 1.0, 1.0)),
        ]

        for idx, (label, value, color) in enumerate(entries):
            marker = Marker()
            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "control_status"
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
    
    def calculate_target_speed_for_stop(self, distance_to_stop, current_speed):
        # Gradual deceleration based on distance and current speed
        # Using a nonlinear deceleration curve for smoother braking
        
        # Adjusted deceleration factor
        target_speed = current_speed * (distance_to_stop / (self.path_plan.speed_limit * 3.0))**1.0
        
        # Clamp for realistic behavior
        return min(self.path_plan.speed_limit, max(1.0, target_speed))

    def filter(self, new_value, previous_value, gain):
        return gain * previous_value + (1 - gain) * new_value
    
    def pure_pursuit_rear_axel(self):
        # Calculate the rear axle position from the front axle (GNSS position)
        yaw = self.get_yaw_from_pose(self.pose.pose.orientation)  # Vehicle heading (yaw angle)
        rear_axle_x = self.pose.pose.position.x - self.wheel_base * math.cos(yaw)
        rear_axle_y = self.pose.pose.position.y - self.wheel_base * math.sin(yaw)
        
        # Calculate lookahead point relative to rear axle
        lookahead_x = self.path_plan.look_ahead_point.x - rear_axle_x
        lookahead_y = self.path_plan.look_ahead_point.y - rear_axle_y

        # Adjust lookahead distance for vehicle length
        effective_lookahead_distance = math.sqrt(lookahead_x ** 2 + lookahead_y ** 2) + self.front_overhang
        lookahead_x = effective_lookahead_distance * (lookahead_x / math.sqrt(lookahead_x ** 2 + lookahead_y ** 2))
        lookahead_y = effective_lookahead_distance * (lookahead_y / math.sqrt(lookahead_x ** 2 + lookahead_y ** 2))

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
        # print("coordinates: ",  self.path_plan.look_ahead_point.x, self.path_plan.look_ahead_point.y, self.path_plan.look_ahead_point.z)
    
        lookahead_x = self.path_plan.look_ahead_point.x - self.pose.pose.position.x
        lookahead_y = self.path_plan.look_ahead_point.y - self.pose.pose.position.y

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
        while rclpy.ok() and not node.node_shut:
            rclpy.spin_once(node, timeout_sec=0.1)# Set timeout to 0 to avoid delay
            node.control()   
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
