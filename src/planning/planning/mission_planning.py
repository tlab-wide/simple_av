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

    def detect_curves(self, curve_calc_dist=4):
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
        self.subscriptionLocation = self.create_subscription(LocalizationMsg, 'simple_av/localization/location', self.location_callback, 10)
        self.location = LocalizationMsg()

        # Service
        self.replan_service = self.create_service(TriggerMissionPlan, '/planning/trigger_mission_plan', self.handle_mission_plan_request)

        # Publish topics
        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        self.mission_plan_publisher = self.create_publisher(PlanningInternalMissionPlanMsg, 'simple_av/planning/mission_plan', qos_profile)

        #Path planning
        self.isPathPlanned = False  # Flag to check if the path has been planned
        self.path_as_lanes = []  # List of lanes from start lane to destination
        self.path = []  # List of waypoints in order of path_as_lanes
        self.curves = []
        self.initial_lane = None
        self.search_depth = 5

        self.densify_interval = 2.0 # meters / Distance between each two consecutive waypoints on a lane
        
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
        self.location = msg
    
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
                points.append(waypoint)

        # Remove duplicate points
        self.path = [points[i] for i in range(len(points)) if i == 0 or (points[i]['x'] != points[i - 1]['x'] or points[i]['y'] != points[i - 1]['y'] or points[i]['z'] != points[i - 1]['z'])]
    

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

        if self.location:
            self.get_logger().info("path planning")
            self.start_lanelet = self.location.closest_lane_names.data
            if start_lanelet_respawn:
                self.start_lanelet = start_lanelet_respawn
            self.bfs(self.start_lanelet, self.dest_lanelet) # Creates the path
            if self.path and self.path_as_lanes:
                self.isPathPlanned = True
                curve_detector = CurveDetector2D(self.path)
                self.curves = curve_detector.detect_curves()
        else:
            self.get_logger().warning("No Location data")
            
    def publisher(self):
        mission_msg = PlanningInternalMissionPlanMsg()

        point_list = []
        for i, wp in enumerate(self.path):
            point = Point(x=wp['x'], y=wp['y'], z=wp['z'])
            waypoint_profile = PlanningWaypoint(waypoint=point, curve=self.curves[i])
            point_list.append(waypoint_profile)

         # path_as_lanes is list of strings already
        mission_msg.path_as_lanes = self.path_as_lanes
        mission_msg.path = point_list
        self.mission_plan_publisher.publish(mission_msg)

    def handle_mission_plan_request(self, request, response):
        self.get_logger().info("Received replan request.")

        # Generate path and path_as_lanes
        self.mission_planning()
        print(self.path_as_lanes)
        # Publish the new mission
        self.publisher()

        self.get_logger().info(f"Published mission plan with {len(self.path)} points.")

        response.success = True
        response.message = "Mission replanned and published."
        return response
    

def main(args=None):
    rclpy.init(args=args)
    node = MissionPlanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()