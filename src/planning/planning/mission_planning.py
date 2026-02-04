#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import json
import os
import yaml
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped, Point
from std_msgs.msg import String
from collections import deque
from simple_av_msgs.msg import LocalizationMsg, Portal, PlanningInternalMissionPlanMsg, PlanningWaypoint
from std_srvs.srv import Trigger
from simple_av_msgs.srv import TriggerMissionPlan
import numpy as np
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy
import math

class CurveDetector2D:
    def __init__(self, points):
        self.points = points

    @staticmethod
    def direction_vector(p1, p2):
        """Calculate the direction vector between two 2D points."""
        return (p2['x'] - p1['x'], p2['y'] - p1['y'])

    @staticmethod
    def vector_magnitude(v):
        """Calculate the magnitude of a 2D vector."""
        return math.sqrt(v[0]**2 + v[1]**2)

    @staticmethod
    def dot_product(v1, v2):
        """Calculate the dot product of two 2D vectors."""
        return v1[0] * v2[0] + v1[1] * v2[1]

    @staticmethod
    def angle_between_vectors(v1, v2):
        """Calculate the angle between two 2D vectors."""
        dot_prod = CurveDetector2D.dot_product(v1, v2)
        mag_v1 = CurveDetector2D.vector_magnitude(v1)
        mag_v2 = CurveDetector2D.vector_magnitude(v2)
        if mag_v1 == 0 or mag_v2 == 0:
            return 0
        cos_theta = dot_prod / (mag_v1 * mag_v2)
        # Ensure the cosine value is within the valid range
        cos_theta = min(1.0, max(-1.0, cos_theta))
        return math.acos(cos_theta)

    def detect_curves(self, curve_calc_dist=6):
        """Detect curves based on the change in direction between points."""
        curves = []
        if len(self.points) < 2 * curve_calc_dist:
            return curves

        for i in range(curve_calc_dist):
            curves.append(0.0)

        for i in range(curve_calc_dist, len(self.points) - curve_calc_dist):
            v1 = self.direction_vector(self.points[i - curve_calc_dist], self.points[i])
            v2 = self.direction_vector(self.points[i], self.points[i + curve_calc_dist])
            curve = self.angle_between_vectors(v1, v2)
            curves.append(curve)
        
        for i in range(len(self.points) - curve_calc_dist, len(self.points)):
            curves.append(0.0)

        return curves


class MissionPlanner(Node):
    def __init__(self):
        super().__init__('mission_planner_node')

        # Load scenario configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.dest_lanelet = self.scenario_config['scenario']['destination']
        self.start_lanelet = None
        self.vehicle_model = self.scenario_config['scenario']['vehicle_model']
        self.motion_behavior_config = self.config_file_loader("motion_behavior_config.yaml")
        self.motion_behavior_config = self.config_file_loader("motion_behavior_config.yaml")

        # Load the map
        self.map_data = self.load_map_data(self.vehicle_model)
        self.map_data = self.map_data["LaneLetsArray"]

        self.graph = {lanelet['name']: {
            'waypoints': lanelet['waypoints'],
            'nextLanes': lanelet.get('nextLanes', []),
            'prevLanes': lanelet.get('prevLanes', []),
            'adjacentLanes': lanelet.get('adjacentLanes', []),
        } for lanelet in self.map_data}

        # Subscribe topics
        self.subscriptionLocation = self.create_subscription(
            LocalizationMsg,
            'simple_av/localization/global_location',
            self.location_callback,
            10,
        )
        self.global_location = LocalizationMsg()
        self.global_location_stamp_ns = None

        # Service
        self.replan_service = self.create_service(TriggerMissionPlan, '/planning/trigger_mission_plan', self.handle_mission_plan_request)
        self.global_localization_client = self.create_client(Trigger, '/localization/trigger_global_localization')

        # Publish topics
        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        self.mission_plan_publisher = self.create_publisher(PlanningInternalMissionPlanMsg, 'simple_av/planning/mission_plan', qos_profile)

        #Path planning
        # self.isPathPlanned = False  # Flag to check if the path has been planned
        self.path_as_lanes = []  # List of lanes from start lane to destination
        self.path = []  # Raw path from map
        self.curves = []
        self.initial_lane = None
        # self.isFirstRequest = True
        self.search_depth = 5

        self.densify_interval = float(
            self.motion_behavior_config['motion']['path']['densify_interval']
        )
        self.pending_replan = False
        self.global_loc_request_time_ns = None
        self.global_loc_in_flight = False
        self.global_loc_wait_timeout_sec = 1.0
        self.replan_timer = self.create_timer(0.1, self.replan_tick)
        
        #Shutting down
        self.node_shut = False
    
    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def load_map_data(self, vehicle_model):
        """
        Load the map data from a JSON file.
        Returns:
            dict: The map data loaded from the JSON file.
        """
        package_share_directory = get_package_share_directory('common')
        if vehicle_model == 'lexus':
            json_file_path = os.path.join(package_share_directory, 'maps', 'Kashiwa-lexus.json')
        else:
            json_file_path = os.path.join(package_share_directory, 'maps', 'Kashiwa-bus.json')
        # json_file_path = os.path.join(package_share_directory, 'resource', 'Shinjuku.json')
        # Load and read the JSON file
        with open(json_file_path, 'r') as json_file:
            map_data = json.load(json_file)
        return map_data

    def location_callback(self, msg):
        """
        Callback function to update the location data.
        Args:
            msg (LocalizationMsg): The localization message received from the topic.
        """
        self.global_location = msg
        self.global_location_stamp_ns = (msg.header.stamp.sec * 1_000_000_000) + msg.header.stamp.nanosec

    def request_global_localization(self):
        if self.global_loc_in_flight:
            return False
        if not self.global_localization_client.wait_for_service(timeout_sec=0.1):
            self.get_logger().warning("Global localization service not available")
            return False
        self.global_location_stamp_ns = None
        self.global_loc_request_time_ns = self.get_clock().now().nanoseconds
        self.global_loc_in_flight = True
        self.get_logger().info("Requesting global localization")
        future = self.global_localization_client.call_async(Trigger.Request())
        future.add_done_callback(self.on_global_localization_done)
        return True

    def on_global_localization_done(self, future):
        self.global_loc_in_flight = False
        if future.done() and future.result() is not None:
            if not future.result().success:
                self.get_logger().warning(f"Global localization failed: {future.result().message}")
            else:
                self.get_logger().info(f"Global localization success: {future.result().message}")
        else:
            self.get_logger().warning("Global localization call did not return a result.")

    def replan_tick(self):
        if not self.pending_replan:
            return
        if self.global_loc_request_time_ns is None and not self.global_loc_in_flight:
            self.request_global_localization()
            return
        if self.global_location_stamp_ns is None:
            return
        now_ns = self.get_clock().now().nanoseconds
        if self.global_loc_request_time_ns is not None:
            elapsed = (now_ns - self.global_loc_request_time_ns) / 1e9
            if self.global_location_stamp_ns < self.global_loc_request_time_ns and elapsed < self.global_loc_wait_timeout_sec:
                return

        self.initial_lane = self.global_location.closest_lane_names.data
        self.get_logger().info(
            f"Mission plan seed lane: {self.initial_lane}, closest_point: "
            f"({self.global_location.closest_point.x:.2f}, "
            f"{self.global_location.closest_point.y:.2f}, {self.global_location.closest_point.z:.2f})"
        )
        self.mission_planning()
        self.get_logger().info(f"path_as_lanes: {self.path_as_lanes}")
        self.publisher()
        self.get_logger().info(f"Published mission plan with {len(self.path)} points.")
        self.pending_replan = False
        self.global_loc_request_time_ns = None
    
    def find_lane_by_name(self, lane_name):
        """
        Get the lane object by its name.
        Args:
            lane_name (str): The name of the lane.
        Returns:
            dict: The lane object if found, else None.
        """
        lane_number = lane_name.replace("lanelet", "")
        lane_number = int(lane_number)
        if lane_number > len(self.map_data):
            return None
        return self.map_data[lane_number - 1]

    def generate_path_points(self):
        """
        Create a path of points based on the path of lanes.
        """
        points = []
        for lane_name in self.path_as_lanes:
            lane_obj = self.find_lane_by_name(lane_name)
            waypoints = lane_obj['dense_waypoints']
            for waypoint in waypoints:
                points.append(Point(x=waypoint['x'], y=waypoint['y'], z=waypoint['z']))

        # Remove duplicate points
        self.path = [
            points[i] for i in range(len(points))
            if i == 0 or (points[i].x != points[i - 1].x or points[i].y != points[i - 1].y or points[i].z != points[i - 1].z)
        ]

    def smooth_points(self, points, window_size=5):
        if len(points) < 3:
            return list(points)
        half = max(1, window_size // 2)
        smoothed = []
        for i in range(len(points)):
            start = max(0, i - half)
            end = min(len(points), i + half + 1)
            sx = sum(p.x for p in points[start:end])
            sy = sum(p.y for p in points[start:end])
            sz = sum(p.z for p in points[start:end])
            count = end - start
            smoothed.append(Point(x=sx / count, y=sy / count, z=sz / count))
        return smoothed

    def resample_points(self, points, spacing):
        if len(points) < 2:
            return list(points)
        resampled = [points[0]]
        carry = 0.0
        for i in range(1, len(points)):
            p0 = points[i - 1]
            p1 = points[i]
            dx = p1.x - p0.x
            dy = p1.y - p0.y
            dz = p1.z - p0.z
            seg_len = math.sqrt(dx * dx + dy * dy + dz * dz)
            if seg_len <= 1e-6:
                continue
            dist = carry
            while dist + spacing <= seg_len:
                dist += spacing
                t = dist / seg_len
                resampled.append(Point(
                    x=p0.x + dx * t,
                    y=p0.y + dy * t,
                    z=p0.z + dz * t,
                ))
            carry = seg_len - dist
        if (resampled[-1].x != points[-1].x or
                resampled[-1].y != points[-1].y or
                resampled[-1].z != points[-1].z):
            resampled.append(points[-1])
        return resampled

    def compute_curves(self, points, curve_calc_dist=6):
        if len(points) < 2 * curve_calc_dist:
            return [0.0 for _ in points]
        curves = []
        for _ in range(curve_calc_dist):
            curves.append(0.0)
        for i in range(curve_calc_dist, len(points) - curve_calc_dist):
            p1 = points[i - curve_calc_dist]
            p2 = points[i]
            p3 = points[i + curve_calc_dist]
            v1 = np.array([p2.x - p1.x, p2.y - p1.y])
            v2 = np.array([p3.x - p2.x, p3.y - p2.y])
            mag1 = np.linalg.norm(v1)
            mag2 = np.linalg.norm(v2)
            if mag1 < 1e-6 or mag2 < 1e-6:
                curves.append(0.0)
                continue
            dot = float(np.dot(v1, v2))
            cosang = max(-1.0, min(1.0, dot / (mag1 * mag2)))
            curves.append(math.acos(cosang))
        for _ in range(len(points) - curve_calc_dist, len(points)):
            curves.append(0.0)
        return curves
    

    def bfs(self, start_lanelet, dest_lanelet):
        """
        Perform Breadth-First Search (BFS) to find a path from start_lanelet to dest_lanelet.
        Args:
            start_lanelet (str): The name of the starting lanelet.
            dest_lanelet (str): The name of the destination lanelet.
        """
        if start_lanelet not in self.graph or dest_lanelet not in self.graph:
            return

        queue = deque([(start_lanelet, [start_lanelet])])
        visited = set()
        visited.add(start_lanelet)

        while queue:
            current_lanelet, path = queue.popleft()

            if current_lanelet == dest_lanelet:
                self.path_as_lanes = path
                self.generate_path_points() # creates a list of waypoints in the path

            for next_lanelet in self.graph[current_lanelet]['nextLanes']:
                if next_lanelet not in visited:
                    visited.add(next_lanelet)
                    queue.append((next_lanelet, path + [next_lanelet]))
                    for next_adj in self.graph[next_lanelet]['adjacentLanes']:
                        if next_adj not in visited:
                            visited.add(next_adj)
                            queue.append((next_adj, path + [next_adj]))
        
    def mission_planning(self, start_lanelet_respawn=None):
        """
        Perform global path planning to create a path from the current location to the destination.
        """
        if self.path is not None:
            self.path.clear()
        if self.path_as_lanes is not None:
            self.path_as_lanes.clear()

        if self.global_location_stamp_ns is not None:
            self.start_lanelet = self.initial_lane
            self.get_logger().info(
                f"Conducting mission plan with start_lanelet={self.start_lanelet} "
                f"dest_lanelet={self.dest_lanelet}"
            )
            self.bfs(self.start_lanelet, self.dest_lanelet) # Creates the path
            if self.path and self.path_as_lanes:
                smoothed_points = self.smooth_points(self.path, window_size=5)
                dense_points = self.resample_points(smoothed_points, self.densify_interval)
                self.path = dense_points
                self.curves = self.compute_curves(self.path)
        else:
            self.get_logger().warning("No Location data to process mission planning")
            
    def publisher(self):
        mission_msg = PlanningInternalMissionPlanMsg()

        point_list = []
        for i, wp in enumerate(self.path):
            waypoint_profile = PlanningWaypoint(waypoint=wp, curve=self.curves[i])
            point_list.append(waypoint_profile)

         # path_as_lanes is list of strings already
        mission_msg.path_as_lanes = self.path_as_lanes
        mission_msg.path = point_list
        self.mission_plan_publisher.publish(mission_msg)

    def handle_mission_plan_request(self, request, response):
        self.get_logger().info("Received mission planning request.")
        if self.pending_replan:
            response.success = True
            response.message = "Mission replan already pending."
            return response

        self.pending_replan = True
        if not self.request_global_localization():
            self.get_logger().warning("Global localization request could not be sent.")

        response.success = True
        response.message = "Mission replan accepted."
        return response
    

def main(args=None):
    rclpy.init(args=args)
    node = MissionPlanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
