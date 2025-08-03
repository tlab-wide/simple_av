#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import os
import json
import yaml
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped, Point
from std_msgs.msg import String
import math
from collections import deque
from simple_av_msgs.msg import TrafficSignalsArray, DetectedObjectsArray
from simple_av_msgs.msg import PlanningInternalMsg, PlanningInternalMissionPlanMsg, PlanningMotionPlanningMsg
from simple_av_msgs.msg import LocalizationMsg
from simple_av_msgs.msg import SimMonitor, Portal
import numpy as np
from scipy.spatial.transform import Rotation as R
from autoware_vehicle_msgs.msg import VelocityReport
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy

class BehaviorMotionPlanning(Node):
    def __init__(self):
        super().__init__('behavior_motion_planner_node')

        # Load scenario configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
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

        # Load av features configs
        self.av_features = self.config_file_loader("av_features.yaml")
        self.use_RSU_for_trafficlight = self.av_features['traffic_light']['use_rsu']
        self.use_RSU_for_object_detection = self.av_features['object_detection']['use_rsu']

        # Load motion & behavior configs
        self.motion_behavior_config = self.config_file_loader("motion_behavior_config.yaml")
        self.base_speed = self.motion_behavior_config['motion']['speed_limits']['base'] # m/s
        self.turning_speed = self.motion_behavior_config['motion']['speed_limits']['turning_speed'] # m/s

        self.range_low_pass_gain = self.motion_behavior_config['behavior']['range_low_pass_gain'] #meters
        
        self.collision_prediction_saftey_distance = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['safety_distance'] #meters
        self.saftey_distance = self.motion_behavior_config['behavior']['collision_avoidance']['on_path']['safety_distance'] #meters
        self.on_path_avoidance_saftey_distance = self.motion_behavior_config['behavior']['collision_avoidance']['on_path']['safety_distance'] #meters

        self.reaction_time_threshold = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['reaction_time_threshold'] #meters
        
        self.prediction_reaction_range_C = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['reaction_range']['coefficient']#meters
        self.prediction_reaction_range_B = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['reaction_range']['base']#meters
        self.prediction_detection_range_C = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['detection_range']['coefficient']#meters
        self.prediction_detection_range_B = self.motion_behavior_config['behavior']['collision_avoidance']['prediction']['detection_range']['base']#meters
        
        
        self.on_path_detection_range_C = self.motion_behavior_config['behavior']['collision_avoidance']['on_path']['detection_range']['coefficient']#meters
        self.on_path_detection_range_B = self.motion_behavior_config['behavior']['collision_avoidance']['on_path']['detection_range']['base']#meters


        # Subscribe topics
        self.subscriptionVelocityReport = self.create_subscription(VelocityReport, '/vehicle/status/velocity_status', self.velocity_report_callback, 10)
        self.velocity_report = VelocityReport()

        self.subscriptionTrafficSignal = self.create_subscription(TrafficSignalsArray, 'simple_av/perception/traffic_signals', self.trafficSignal_callback, 10)
        self.trafficSignal = TrafficSignalsArray()

        self.subscriptionDetectedObjects = self.create_subscription(DetectedObjectsArray, 'simple_av/perception/detected_objects', self.detectedObjects_callback, 10)
        self.detectedObjects = DetectedObjectsArray()

        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        self.pose = PoseStamped()

        self.subscriptionLocation = self.create_subscription(LocalizationMsg, 'simple_av/localization/location', self.location_callback, 10)
        self.location = LocalizationMsg()

        self.subscriptionCurveDetection = self.create_subscription(PlanningInternalMsg, 'simple_av/planning/internal_msg', self.internal_msg_callback, 10)
        self.isTurnDetected = False
        self.isEndOfPath = False

        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False

        self.subscriptionSimMonitor = self.create_subscription(SimMonitor, 'simple_av/sim_monitor', self.sim_monitor_callback, 100)
        self.sim_clock_rate = 0

        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        self.subscription_mission_plan = self.create_subscription(PlanningInternalMissionPlanMsg, 'simple_av/planning/mission_plan', self.mission_plan_callback, qos_profile)
        self.mission_plan = PlanningInternalMissionPlanMsg()
        self.path_as_lanes = None  # List of lanes from start lane to destination
        self.path = None  # List of waypoints in order of path_as_lanes
        self.path_of_waypoints = [] # List of waypoints in order of path_as_lanes

        # Publish topics
        self.planning_publisher = self.create_publisher(PlanningMotionPlanningMsg, 'simple_av/planning/motion_planning', 10)

        #Path
        self.isPathPlanned = False
        self.route = None # List of lanes from start lane to destination
        self.current_lane_index = 0
        self.search_depth = 5
        self.destination = Point()
        
        #Observation and detection range
        self.on_path_detection_range = self.base_speed * self.on_path_detection_range_C + self.on_path_detection_range_B # meters
        self.reaction_range = self.base_speed * self.prediction_reaction_range_C + self.prediction_reaction_range_B # meters
        self.detection_range = self.base_speed * self.prediction_detection_range_C + self.prediction_detection_range_B # meters
        self.current_speed = 0.0
        self.previous_speed_slidingWindow = deque(maxlen=8) # for storing 10 recent previous speed values
        self.previous_speed_slidingWindow.append(0.0)  # initializing the queue
        self.status = String() # Cruise, Decelerate, PrepareToStop, Turn

        self.densify_interval = 2.0 # meters / Distance between each two consecutive waypoints on a lane
        
        #Traffic light
        self.traffic_light_stopPoint_lastState = Point()
        self.traffic_light_state_lastState = 'Cruise_green'
        self.opposite_traffic_light_last_Color = 1

        #Shutting down
        self.node_shut = False

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

    def mission_plan_callback(self, msg):
        self.mission_plan = msg
        self.path = self.mission_plan.path
        self.path_as_lanes = self.mission_plan.path_as_lanes

    def sim_monitor_callback(self, msg):
        self.sim_clock_rate = msg.sim_clock_rate
    
    def velocity_report_callback(self, msg):
        self.velocity_report = msg
    
    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    
    def portal_callback(self, msg):
        self.reset = msg.reset
        self.finished = msg.finished

    def internal_msg_callback(self, msg):
        self.isTurnDetected = msg.is_curve_detected
        self.isEndOfPath = msg.is_end_of_path

    def trafficSignal_callback(self, msg):
        self.trafficSignal = msg

    def detectedObjects_callback(self, msg):
        self.detectedObjects = msg

    def pose_callback(self, msg):
        self.pose = msg

    def location_callback(self, msg):
        self.location = msg

    def calculate_distance(self, point1, point2, z=False):
        """
        Calculate the Euclidean distance between two points.
        Args:
            point1 (geometry_point): The first point with 'x', 'y', 'z' coordinates.
            point2 (geometry_point): The second point with 'x', 'y', 'z' coordinates.
        Returns:
            float: The Euclidean distance between the two points.
        """
        if z:
            return np.sqrt((point1.x - point2.x)**2 + 
                        (point1.y - point2.y)**2 + 
                        (point1.z - point2.z)**2)
        else:
            return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def calculate_vector(self, point1, point2):
        """
        Calculate the vector from point1 to point2.
        Args:
            point1 (geometry_point): The starting point with 'x', 'y', 'z' coordinates.
            point2 (geometry_point): The ending point with 'x', 'y', 'z' coordinates.
        Returns:
            np.array: The vector from point1 to point2.
        """
        return np.array([point2.x - point1.x, 
                        point2.y - point1.y, 
                        point2.z - point1.z])

    def calculate_dot_product(self, vector1, vector2):
        """
        Calculate the dot product of two vectors.
        Args:
            vector1 (np.array): The first vector.
            vector2 (np.array): The second vector.
        Returns:
            float: The dot product of the two vectors.
        """
        return np.dot(vector1, vector2)
    
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
        
    # TODO: create search area based on waypoints not lanes
    def create_search_area(self):
        try:
            lane_index = self.route.index(self.location.closest_lane_names.data)
        except:
            # vehicle is out of path
            # self.get_logger().warning("Vehicle is out of the Path")
            lane_index = self.current_lane_index
        if lane_index in range(self.current_lane_index, self.current_lane_index + self.search_depth):
            self.current_lane_index = lane_index
        search_area_as_lanes = self.path_as_lanes[self.current_lane_index: self.current_lane_index + self.search_depth]

        # convert lanes in the search are into a list of waypoints
        search_area = []
        for lane in search_area_as_lanes:
            lane_obj = self.find_lane_by_name(lane)
            waypoints = lane_obj['dense_waypoints']
            for waypoint in waypoints:
                search_area.append(Point(x=waypoint['x'], y=waypoint['y'], z=waypoint['z']))
        # print("debug - search area as lanes", search_area_as_lanes, "size of search area: ", len(search_area))
        return search_area, search_area_as_lanes

    def find_closest_waypoint_to_vehicle(self, vehicle_pose, search_area):
        # Finding the index of the closest point in search area
        distances_to_vehicle = []
        for waypoint in search_area:
            distances_to_vehicle.append(self.calculate_distance(waypoint, vehicle_pose))
        closest_waypoint_to_vehicle = search_area[distances_to_vehicle.index(min(distances_to_vehicle))]
        current_closest_point_to_vehicle = self.path_of_waypoints.index(closest_waypoint_to_vehicle)
        return current_closest_point_to_vehicle

    def update_observation_range(self, speed, is_speed_declining):
        gain = self.range_low_pass_gain if is_speed_declining else 0
        self.on_path_detection_range = (1 - gain) * (speed * self.on_path_detection_range_C + self.on_path_detection_range_B) + gain * self.on_path_detection_range 
        self.reaction_range = (1 - gain) * (speed * self.prediction_reaction_range_C + self.prediction_reaction_range_B) + gain * self.reaction_range # meters
        self.detection_range = (1 - gain) * (speed * self.prediction_detection_range_C + self.prediction_detection_range_B) + gain * self.detection_range # meters

    
    def get_traffic_light_color_by_id(self, traffic_light_id):
        v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
        v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)
        if traffic_light_id in v2i_traffic_signals_id:
            self.opposite_traffic_light_last_Color = v2i_traffic_signals_colors[v2i_traffic_signals_id.index(traffic_light_id)]
        return self.opposite_traffic_light_last_Color

    def get_traffic_light_color_by_lane(self, lane):
        lane_obj = self.find_lane_by_name(lane)
        current_lane_traffic_light_id = lane_obj['trafficlightsWayIDs']
        v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
        if current_lane_traffic_light_id and current_lane_traffic_light_id[0] in v2i_traffic_signals_id:
            v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)
            return v2i_traffic_signals_colors[v2i_traffic_signals_id.index(current_lane_traffic_light_id[0])]
        return None

    def get_traffic_light_stop_point_by_lane(self, lane):
        lane_obj = self.find_lane_by_name(lane)
        stop_point = self.calculate_traffic_light_stop_point(lane_obj['stopLinePoseP1'], lane_obj['stopLinePoseP2'])
        return stop_point

    def manage_traffic_lights(self):
        v2i_traffic_signals_id = list(self.trafficSignal.v2i_traffic_signals_id)
        v2i_traffic_signals_colors = list(self.trafficSignal.v2i_traffic_signals_colors)

        current_lane = self.route[self.current_lane_index]
        lane_obj = self.find_lane_by_name(current_lane)
        current_lane_traffic_light_id = lane_obj['trafficlightsRelationID']
        if current_lane_traffic_light_id: # this lane have a traffic light
            if current_lane_traffic_light_id[0] in v2i_traffic_signals_id: # traffic light id is on the list
                color = v2i_traffic_signals_colors[v2i_traffic_signals_id.index(current_lane_traffic_light_id[0])]
                stop_point = self.get_traffic_light_stop_point_by_lane(current_lane)
                self.traffic_light_stopPoint_lastState = stop_point
                if color == 1 or color == 2:
                    self.traffic_light_state_lastState = 'Stop_red'
                    return 'Stop_red', stop_point
                self.traffic_light_state_lastState = 'Cruise_green'
                return 'Cruise_green', None
            else:
                if self.traffic_light_state_lastState == 'Stop_red':
                    return 'Stop_red', self.traffic_light_stopPoint_lastState
                return 'Cruise_green', None

        # self.get_logger().info(f"Traffic light Not detected on {lane_obj['name']}")
        return 'Cruise',  None
        

    def get_detected_objects_in_front(self):
        if not self.detectedObjects:
            self.get_logger().warning("No Perception / no object detected!")
            return None

        objects_ahead = []
        for obj in self.detectedObjects.objects:
            object_direction = obj.relative_direction.data
            if object_direction == 'above' or object_direction == 'NW' or object_direction == 'NE':
                objects_ahead.append(obj)
        return objects_ahead
        
    def get_objects_in_range(self, objects_ahead, filter_dist):
        if not objects_ahead:
            print("No Object ahead")
            return None            
        objects_in_range = []
        for obj in objects_ahead:
            if obj.distance <= filter_dist: objects_in_range.append(obj)

        return objects_in_range
    
    def apply_quaternion_rotation(self, quaternion, vector):
        """
        Applies a quaternion rotation to a given vector.
        """
        rotation = R.from_quat(np.array([quaternion.x, quaternion.y, quaternion.z, quaternion.w]))
        transformed_vector = rotation.apply(np.array([vector.x, vector.y, vector.z]))
        return Point(x=transformed_vector[0], y=transformed_vector[1], z=transformed_vector[2])

    def get_object_absolute_position(self, vehicle_orientation, vehicle_pose, vector):
        """
        Converts an object's relative position back to its absolute position using the vehicle's pose.
        """
        # Apply the quaternion rotation (forward rotation)
        rotated_vector = self.apply_quaternion_rotation(vehicle_orientation, vector)

        # Add the rotated vector to the vehicle's position
        obj_x = vehicle_pose.x + rotated_vector.x
        obj_y = vehicle_pose.y + rotated_vector.y
        obj_z = vehicle_pose.z + rotated_vector.z

        # Create the absolute position
        object_absolute_pose = Point(x=obj_x, y=obj_y, z=obj_z)
        return object_absolute_pose
    
    def find_obstacle_on_path(self, objects_in_range, current_closest_point_to_vehicle_index, vehicle_pose):
        objects_on_path = []
        objects_absolute_positions = [self.get_object_absolute_position(self.pose.pose.orientation, vehicle_pose, obj.position) for obj in objects_in_range]
        waypoints = self.path_of_waypoints[current_closest_point_to_vehicle_index:current_closest_point_to_vehicle_index + int(self.on_path_detection_range / self.densify_interval) + 1]
        for i in range(len(objects_in_range)):
            for waypoint in waypoints:
                dist = self.calculate_distance(objects_absolute_positions[i], waypoint)
                if dist <= self.densify_interval*1.2:
                    objects_on_path.append({"object": objects_in_range[i], "waypoint": waypoint})
                    break
        
        # If no objects are on the path
        if not objects_on_path:
            return None
        
        # If only one object is on the path
        if len(objects_on_path) == 1:
            return objects_on_path[0]
        
        # Find the closest object on the path
        min_dist = float('inf')
        closest_object_info = None
        for object_on_path in objects_on_path:
            dist = self.calculate_distance(vehicle_pose, object_on_path['waypoint'])
            if dist < min_dist:
                closest_object_info = object_on_path
                min_dist = dist
        
        return closest_object_info
    
    def calculate_traffic_light_stop_point(self, p1, p2):
        return Point(x=(p1[0] + p2[0])/2, y=(p1[1] + p2[1])/2, z=(p1[2] + p2[2])/2)
    
    
    def find_intersection(self, object_pose, object_forward_vector, waypoint1, waypoint2):
        # Extract components
        x1, y1 = object_pose.x, object_pose.y
        a1, b1 = object_forward_vector
        x2, y2 = waypoint1.x, waypoint1.y
        x3, y3 = waypoint2.x, waypoint2.y

        # Direction vector of Line 2 (waypoints)
        a2 = x3 - x2
        b2 = y3 - y2

        # Equation of Line 1 (object path): y - y1 = m1 * (x - x1)
        # m1 = b1 / a1 (from vector)
        m1 = b1 / a1 if a1 != 0 else float('inf')  # Handle vertical line case

        # Equation of Line 2: y - y2 = m2 * (x - x2)
        m2 = b2 / a2 if a2 != 0 else float('inf')  # Handle vertical line case

        # Handle the vertical lines (infinite slope)
        if m1 == m2:
            self.get_logger().error("Parallel lines")
            return None  # Parallel vertical lines
        elif m1 == float('inf'):  # Line 1 is vertical
            x = x1
            y = m2 * (x - x2) + y2
        elif m2 == float('inf'):  # Line 2 is vertical
            x = x2
            y = m1 * (x - x1) + y1
        else:  # Neither line is vertical
            x = (y2 - y1 + m1 * x1 - m2 * x2) / (m1 - m2)
            y = m1 * (x - x1) + y1
        return Point(x=x, y=y, z=waypoint1.z)

    def dot_product(self, v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]

    def is_point_on_segment(self, object_pose, collison_point, waypoint1, waypoint2, forward_vector):
        # Unpack the intersection point and the waypoints
        x1, y1 = waypoint1.x, waypoint1.y
        x2, y2 = waypoint2.x, waypoint2.y
        x3, y3 = object_pose.x, object_pose.y

        object_to_intersect_vector = [collison_point.x-x3, collison_point.y-y3]
        # Check if the collison_point point is within the bounds of the segment
        if min(x1, x2) <= collison_point.x <= max(x1, x2) and min(y1, y2) <= collison_point.y <= max(y1, y2):
            if self.dot_product(object_to_intersect_vector, forward_vector) >= 0:
                return True  # collison_point point is on the segment
        return False  # collison_point point is outside the segment
        
    def get_forward_vector(self, quaternion):
        local_forward = np.array([1, 0, 0])
        # Convert the quaternion to a rotation object
        rotation = R.from_quat(np.array([quaternion.x, quaternion.y, quaternion.z, quaternion.w]))  # Quaternion format: [x, y, z, w]
        # Apply the rotation to the local forward vector
        global_forward = rotation.apply(local_forward)
        return global_forward [:2]
    
    def get_time_to_collison(self, current_pose, collision_point, speed):
        if speed == 0.0:
            return float('inf')  # Return infinity to indicate no collision
        dist = self.calculate_distance(collision_point, current_pose)
        time_to_collision = dist / speed
        time_to_collision = time_to_collision * self.sim_clock_rate
        return time_to_collision

    def will_collide_on_path(self, object_type, object_speed, object_pose, vehicle_pose, collison_point, corresponding_waypoint):
        current_vehicle_speed = self.velocity_report.longitudinal_velocity if self.velocity_report else 0.0   
        current_vehicle_speed = current_vehicle_speed if current_vehicle_speed > self.turning_speed else self.turning_speed
        t_vehicle = self.get_time_to_collison(vehicle_pose, collison_point, current_vehicle_speed)

        t_object = self.get_time_to_collison(object_pose, collison_point, object_speed)

        if abs(t_vehicle - t_object) <= self.reaction_time_threshold:
            self.get_logger().warning(f"CP - Vehciel mooving - Potential collision detected! Time difference: {abs(t_vehicle - t_object):.2f} seconds.")
            return True
        return False
    
    def get_stop_point_by_safety_distance(self, waypoint, vehicle_pose, collision_avoidance_type):
        # Helper function to calculate distances
        saftey_distance = self.motion_behavior_config['behavior']['collision_avoidance'][collision_avoidance_type]['safety_distance'] #meters
        dist_to_waypoint = self.calculate_distance(waypoint, vehicle_pose)
        if dist_to_waypoint <= saftey_distance: # Stop the vehicle if distance to the object is less that safety distance
            self.get_logger().warning("CP - INSTANT STOP!!")
            return vehicle_pose

        stop_point_index = self.path_of_waypoints.index(waypoint) - int(saftey_distance/self.densify_interval)
        stop_point = self.path_of_waypoints[stop_point_index]
        return Point(x=stop_point.x, y=stop_point.y, z=stop_point.z)
         

    def on_path_collision_avoidance(self, objects_ahead, current_closest_point_to_vehicle_index, vehicle_pose):
        objects_in_range = self.get_objects_in_range(objects_ahead, self.on_path_detection_range)
        if not objects_in_range:
            return None
        closest_object_info = self.find_obstacle_on_path(objects_in_range, current_closest_point_to_vehicle_index, vehicle_pose)
        # return False, None, 'Cruise'
        if not closest_object_info:
            self.get_logger().info("No Immediate danger")
            return None
        self.get_logger().info("Imediate threat. Objects ahead in danger zone")
        return self.get_stop_point_by_safety_distance(closest_object_info['waypoint'], vehicle_pose, 'on_path')
    
    def collison_prediction(self, objects_ahead, current_closest_point_to_vehicle_index, vehicle_pose):
        objects_in_range = self.get_objects_in_range(objects_ahead, self.detection_range)
        if not objects_in_range:
            return None
        objects_absolute_positions = [self.get_object_absolute_position(self.pose.pose.orientation, vehicle_pose, obj.position) for obj in objects_in_range]
        waypoints = self.path_of_waypoints[current_closest_point_to_vehicle_index:current_closest_point_to_vehicle_index + int(self.reaction_range / self.densify_interval) + 1]
        if self.use_RSU_for_trafficlight:
            if self.get_traffic_light_color_by_id(166893) == 1:
                return []
        predicted_stop_points = []
        for i in range(len(objects_in_range)):
            for j in range(1, len(waypoints) - 1):
                forward_vector = self.get_forward_vector(objects_in_range[i].orientation)
                collison_point = self.find_intersection(objects_absolute_positions[i], forward_vector, waypoints[j], waypoints[j+1])
                if collison_point:
                    if self.is_point_on_segment(objects_absolute_positions[i], collison_point, waypoints[j], waypoints[j+1], forward_vector):
                        if self.will_collide_on_path(objects_in_range[i].label, objects_in_range[i].velocity, objects_absolute_positions[i], vehicle_pose, collison_point, waypoints[j]):
                            self.get_logger().warning('P - Collide predicted!!!')
                            stop_point = self.get_stop_point_by_safety_distance(waypoints[j], vehicle_pose, 'prediction')
                            predicted_stop_points.append(stop_point)
                            break
        return predicted_stop_points
    
    def find_closest_stop_point(self, traffic_light_stopPoint, on_path_collision_avoidance_stopPoint, predicted_collisons_stopPoints, destination_stopPoint, vehicle_pose):
        # Create a dictionary for stop points
        stop_points = {}
        
        if traffic_light_stopPoint:
            stop_points[id(traffic_light_stopPoint)] = ('TrafficLight', traffic_light_stopPoint)
        if on_path_collision_avoidance_stopPoint:
            stop_points[id(on_path_collision_avoidance_stopPoint)] = ('CollisonAvoidance', on_path_collision_avoidance_stopPoint)
        if predicted_collisons_stopPoints:
            for point in predicted_collisons_stopPoints:
                stop_points[id(point)] = ('CollisonPrediction', point)
        if destination_stopPoint:
            stop_points[id(destination_stopPoint)] = ('Destination', destination_stopPoint)
        
        # Helper function to calculate distances
        def calculate_distance_to(point):
            return self.calculate_distance(
                vehicle_pose, 
                point
            )
        
        minimum_distance = float("inf")
        closest_stop_point = None
        stop_point_type = None
        
        for _, (type, stop_point) in stop_points.items():
            dist = calculate_distance_to(stop_point)
            if dist <= minimum_distance:
                minimum_distance = dist
                closest_stop_point = stop_point
                stop_point_type = type
        
        return closest_stop_point, stop_point_type


    def motion_planner(self, current_closest_point_to_vehicle_index):
        # Current vehicle position
        vehicle_pose = self.pose.pose.position

        # Distance to the destination
        # distance_to_destination = self.calculate_distance(vehicle_pose, self.destination)
        
        # TODO: Distance to the destination 

        # Traffic light detection
        trafficLightTask, traffic_light_stopPoint = self.manage_traffic_lights()
        # Collision avoidance
        objects_ahead = self.get_detected_objects_in_front()
        on_path_collision_avoidance_stopPoint = self.on_path_collision_avoidance(objects_ahead, current_closest_point_to_vehicle_index, vehicle_pose)
        predicted_collisons_stopPoints = self.collison_prediction(objects_ahead, current_closest_point_to_vehicle_index, vehicle_pose)
        stop_point, stop_point_type = self.find_closest_stop_point(traffic_light_stopPoint, on_path_collision_avoidance_stopPoint, predicted_collisons_stopPoints, self.destination, vehicle_pose)
        self.status.data = 'Cruise'

        if self.isTurnDetected:
            self.get_logger().info("Turn detected")
            self.status.data = 'Turn'

        if stop_point_type == 'CollisonAvoidance' or stop_point_type == 'CollisonPrediction':
            if stop_point_type == 'CollisonAvoidance':
                self.get_logger().info('Collison Avoidance')
            else:
                self.get_logger().info('Prediction')
            self.status.data = 'Decelerate'
        
        if stop_point_type == 'TrafficLight':
            self.get_logger().info('TrafficLight')
            self.status.data = trafficLightTask
        
        if self.isEndOfPath:
            self.get_logger().info("Approaching destination, decelerating.")
            self.status.data = 'Park'
        
        return stop_point
            
    def publish_motion_planning_msgs(self, stop_point):
        motion_plan = PlanningMotionPlanningMsg()
        motion_plan.stop_point = stop_point
        motion_plan.status = self.status
        self.planning_publisher.publish(motion_plan)

    def motion_planning(self):
        if not self.location and not self.pose:
            self.get_logger().warning("No location/pose input")
            return None
        
        if self.path and not self.isPathPlanned:
            self.get_logger().warning("Path has successfully initialized from Mission Planner")
            self.destination = self.path[-1].waypoint
            for i, waypoint in enumerate(self.path):
                self.path_of_waypoints.append(waypoint.waypoint)
            self.route = self.path_as_lanes[:]
            self.current_lane_index = 0

            self.isPathPlanned = True
        
        if not self.path :
            self.get_logger().warning("Path has not initialized from Mission Planner!!")
            self.isPathPlanned = False
            return
        
        if self.finished:
            self.status.data = 'Park'
            self.node_shut = True
            self.publish_motion_planning_msgs(None) # publishing
            return
        
        if self.reset:
            self.get_logger().warning("RESET")
            self.isPathPlanned = False
            self.route = self.path_as_lanes[:]
            self.current_lane_index = 0
            return

        search_area, search_area_as_lanes = self.create_search_area()
        self.current_speed = self.velocity_report.longitudinal_velocity if self.velocity_report else 0.0
        self.update_observation_range(self.current_speed, self.current_speed < self.previous_speed_slidingWindow[0])
        vehicle_pose = self.pose.pose.position

        current_closest_point_to_vehicle_index = self.find_closest_waypoint_to_vehicle(vehicle_pose, search_area)
        stop_point = self.motion_planner(current_closest_point_to_vehicle_index)
        
        self.publish_motion_planning_msgs(stop_point) # publishing
        
        self.get_logger().info(
            f'behavior motion planning\n'
            f'distance to stop point: {self.calculate_distance(vehicle_pose, stop_point)}\n'
            f'status: {self.status.data}\n'
        )
        
        self.previous_speed_slidingWindow.append(self.current_speed)

def main(args=None):
    rclpy.init(args=args)
    node = BehaviorMotionPlanning()
    try:
        while rclpy.ok() and not node.node_shut:
            rclpy.spin_once(node, timeout_sec=None)# Set timeout to 0 to avoid delay
            node.motion_planning()
    finally:
        node.destroy_node()
        rclpy.shutdown()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()