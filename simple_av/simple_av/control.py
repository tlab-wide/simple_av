#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point
from autoware_auto_vehicle_msgs.msg import VelocityReport
from autoware_auto_vehicle_msgs.msg import GearCommand
from autoware_auto_control_msgs.msg import AckermannControlCommand, AckermannLateralCommand, LongitudinalCommand
from autoware_auto_vehicle_msgs.msg import TurnIndicatorsCommand
from rclpy.qos import QoSProfile, DurabilityPolicy, HistoryPolicy, ReliabilityPolicy
from simple_av_msgs.msg import LookAheadMsg, SimMonitor
import time
import math
from collections import deque
import numpy as np
import yaml
import os
from ament_index_python.packages import get_package_share_directory
from simple_av_msgs.msg import Portal
from rclpy.parameter import Parameter


class PIDController:
    def __init__(self, p_gain, i_gain, d_gain, sim_time=0.05):
        self.kp = p_gain
        self.ki = i_gain
        self.kd = d_gain

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
    def __init__(self, vehicle_type):
        super().__init__('control')
        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        
        # Load configs
        self.vehicle_type = vehicle_type
        self.vehicle_config = self.load_vehicle_config(vehicle_type)
        self.vehicle_length = self.vehicle_config['dimensions']['length'] #meters
        self.vehicle_width = self.vehicle_config['dimensions']['width'] #meters
        self.wheel_base = self.vehicle_config['dimensions']['wheel_base'] #meters
        self.front_overhang = self.vehicle_config['dimensions']['front_overhang'] #meters
        self.back_overhang = self.vehicle_config['dimensions']['back_overhang'] #meters
        
        self.previous_steering_angle = 0
        self.steering_gain = 0.3  # Proportional gain for steering
        self.maximum_accel = self.vehicle_config['max_acceleration']
        self.maximum_Stereing = None
        self.maximum_braking_accel = self.vehicle_config['max_braking_accel']

        # Subscribe topics
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        self.subscriptionPose = self.create_subscription(PoseStamped, '/awsim/ground_truth/vehicle/pose', self.ground_truth_callback, 10)
        self.subscriptionVelocityReport = self.create_subscription(VelocityReport, '/vehicle/status/velocity_status', self.velocity_report_callback, 10)
        self.subscriptionLookahead = self.create_subscription(LookAheadMsg, '/simple_av/planning/lookahead_point', self.lookahead_callback, 10)
        
        self.subscriptionSimMonitor = self.create_subscription(SimMonitor, 'simple_av/sim_monitor', self.sim_monitor_callback, 100)
        self.sim_clock_rate = 0

        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False

        self.pose = PoseStamped()
        self.ground_truth = PoseStamped()
        self.velocity_report = VelocityReport()
        self.lookAhead = LookAheadMsg()

        # Publish topics
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            durability=DurabilityPolicy.TRANSIENT_LOCAL
        )
        self.control_publisher = self.create_publisher(AckermannControlCommand, '/control/command/control_cmd', qos_profile)
        self.gear_publisher = self.create_publisher(GearCommand, '/control/command/gear_cmd', qos_profile)
        self.turn_indicator_publisher = self.create_publisher(TurnIndicatorsCommand, '/control/command/turn_indicators_cmd', qos_profile)

        self.pid_controller = PIDController(p_gain=1.8, i_gain=20.0, d_gain=0.5)

        self.node_shut = False

    def load_vehicle_config(self, vehicle_type="lexus"):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('simple_av')
        config_path = os.path.join(package_share_directory, "resource", "vehicle_config.yaml")

        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        # Retrieve the specific vehicle's configuration
        if vehicle_type in config["vehicles"]:
            return config["vehicles"][vehicle_type]
        else:
            raise ValueError(f"Vehicle type '{vehicle_type}' not found in the configuration.")

    def sim_monitor_callback(self, msg):
        self.sim_clock_rate = msg.sim_clock_rate

    def portal_callback(self, msg):
        self.reset = msg.reset
        self.finished = msg.finished

    def pose_callback(self, msg):
        self.pose = msg

    def ground_truth_callback(self, msg):
        self.ground_truth = msg

    def velocity_report_callback(self, msg):
        self.velocity_report = msg

    def lookahead_callback(self, msg):
        self.lookAhead = msg

    def get_latest_messages(self):
        return self.pose, self.velocity_report
    
    def calculate_distance(self, point1, point2):
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def control(self):

        if not self.velocity_report and not self.lookAhead and not self.pose and not self.ground_truth:
            return
        
        if self.finished:
            self.node_shut = True
            gear_msg = GearCommand()
            gear_msg.stamp = self.get_clock().now().to_msg()
            print("park")
            gear_msg.command = GearCommand.PARK
            self.gear_publisher.publish(gear_msg)  
            return

        # Steer and Velocity Control
        control_msg = AckermannControlCommand()
    
        control_msg.stamp = self.get_clock().now().to_msg()
        control_msg.lateral = self.get_lateral_command(self.lookAhead.status.data)
        control_msg.longitudinal = self.get_longitudinal_command(self.lookAhead.status.data)

        # Turn Indicator Light Control
        turn_indicator_msg = TurnIndicatorsCommand()
        turn_indicator_msg.stamp = self.get_clock().now().to_msg()
        
        # Gear Control
        gear_msg = GearCommand()
        gear_msg.stamp = self.get_clock().now().to_msg()
        if self.lookAhead.status.data == "Park":
            print("park")
            gear_msg.command = GearCommand.PARK
        else:
            print("drive")
            gear_msg.command = GearCommand.DRIVE

        self.control_publisher.publish(control_msg)
        # self.turn_indicator_publisher.publish(turn_indicator_msg)
        self.gear_publisher.publish(gear_msg)  


    
    def get_lateral_command(self, status):
        lateral_command = AckermannLateralCommand()
        if status == "Park":
            print("debug PARK")
            lateral_command.steering_tire_angle = 0.0
            lateral_command.steering_tire_rotation_rate = 0.0
        else:
            if self.pose and self.lookAhead and self.ground_truth:
                steer = self.pure_pursuit_rear_axel()
                lateral_command.steering_tire_angle = steer
                lateral_command.steering_tire_rotation_rate = 0.1
            else:
                lateral_command.steering_tire_angle = 0.0
                lateral_command.steering_tire_rotation_rate = 0.0
        return lateral_command

    def get_longitudinal_command(self, status):

        current_speed = self.velocity_report.longitudinal_velocity if self.velocity_report else 0.0
        target_speed = self.lookAhead.speed_limit

        if status == "Decelerate" or status == "Stop_red":
            distance_to_stop = self.calculate_distance(self.lookAhead.stop_point, self.pose.pose.position)
            target_speed = self.calculate_target_speed_for_stop(distance_to_stop, current_speed)
            if status == "Stop_red" and distance_to_stop <= 4.0:
                self.get_logger().warning("Full stop!")
                target_speed = 0.0
            if status == "Decelerate" and distance_to_stop <= 2.0:
                self.get_logger().warning("Full stop!")
                target_speed = 0.0

        accel = self.pid_controller.updatePID(current_speed, target_speed, time.time() * self.sim_clock_rate)
        if accel > self.maximum_accel:
            accel = self.maximum_accel
        if accel < self.maximum_braking_accel:
            accel = self.maximum_braking_accel

        longitudinal_command = LongitudinalCommand()
        longitudinal_command.speed = self.velocity_report.longitudinal_velocity
        longitudinal_command.acceleration = accel

        if status == "Decelerate" or status == "Stop_red":
            self.get_logger().info(
            f'speed: {current_speed}\n'
            f'accel: {accel}\n'
            f'target speed: {target_speed}\n'
            f'stop distance: {self.calculate_distance(self.lookAhead.stop_point, self.pose.pose.position)}\n'
            f'status : {self.lookAhead.status.data}\n'
        )
        else:
            self.get_logger().info(
                f'speed: {current_speed}\n'
                f'accel: {accel}\n'
                f'target speed: {target_speed}\n'
                f'status : {self.lookAhead.status.data}\n'
            )

        return longitudinal_command
    
    def calculate_target_speed_for_stop(self, distance_to_stop, current_speed):
        # Gradual deceleration based on distance and current speed
        # Using a nonlinear deceleration curve for smoother braking
        
        # Adjusted deceleration factor
        target_speed = current_speed * (distance_to_stop / (self.lookAhead.speed_limit * 3.0))**1.0
        
        # Clamp for realistic behavior
        return min(self.lookAhead.speed_limit, max(1.0, target_speed))

    def filter(self, new_value, previous_value, gain):
        return gain * previous_value + (1 - gain) * new_value
    
    def pure_pursuit_rear_axel(self):
        # Calculate the rear axle position from the front axle (GNSS position)
        yaw = self.get_yaw_from_pose(self.pose.pose.orientation)  # Vehicle heading (yaw angle)
        rear_axle_x = self.pose.pose.position.x - self.wheel_base * math.cos(yaw)
        rear_axle_y = self.pose.pose.position.y - self.wheel_base * math.sin(yaw)
        
        # Calculate lookahead point relative to rear axle
        lookahead_x = self.lookAhead.look_ahead_point.x - rear_axle_x
        lookahead_y = self.lookAhead.look_ahead_point.y - rear_axle_y

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
            self.get_logger().info("Left Turn")
        else:
            self.get_logger().info("Right Turn")

        return steering_angle

    def pure_pursuit_steering_angle(self):
        # print("coordinates: ",  self.lookAhead.look_ahead_point.x, self.lookAhead.look_ahead_point.y, self.lookAhead.look_ahead_point.z)
    
        lookahead_x = self.lookAhead.look_ahead_point.x - self.pose.pose.position.x
        lookahead_y = self.lookAhead.look_ahead_point.y - self.pose.pose.position.y

        yaw = self.get_yaw_from_pose(self.pose.pose.orientation)
        print("degree: ", math.degrees(yaw))

        local_x = math.cos(yaw) * lookahead_x + math.sin(yaw) * lookahead_y
        local_y = -math.sin(yaw) * lookahead_x + math.cos(yaw) * lookahead_y

        ld2 = lookahead_x ** 2 + lookahead_y ** 2
        steering_angle = math.atan2(2.0 * local_y * self.wheel_base, ld2)
        steering_angle = self.filter(steering_angle, self.previous_steering_angle, self.steering_gain)
        self.previous_steering_angle = steering_angle

        if steering_angle >= 0:
            self.get_logger().info("Left")
        else:
            self.get_logger().info("Right")
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
    node = VehicleControl('bus')

    try:
        while rclpy.ok() and not node.node_shut:
            rclpy.spin_once(node, timeout_sec=None)# Set timeout to 0 to avoid delay
            node.control()   
    finally:
        node.destroy_node()
        rclpy.shutdown()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
