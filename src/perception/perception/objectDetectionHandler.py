#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Quaternion, Vector3
from simple_av_msgs.msg import DetectedObject, DetectedObjectsArray
from autoware_auto_perception_msgs.msg import DetectedObjects
from autoware_auto_perception_msgs.msg import PredictedObjects
from geometry_msgs.msg import PoseStamped
from math import atan2, asin
import math
import yaml
import os
from ament_index_python.packages import get_package_share_directory
from scipy.spatial.transform import Rotation as R
import numpy as np
# import transformations as tf
from transformations import euler_from_quaternion
from simple_av_msgs.msg import Portal

class Perception(Node):
    def __init__(self):
        super().__init__('ObjectDetetionHandler')

        # Load scenario configs
        self.scenario_config = self.config_file_loader("scenario_config.yaml")
        self.vehicle_model = self.scenario_config['scenario']['vehicle_model']

        # Load vehicle configs
        self.vehicle_config = self.load_vehicle_config(self.vehicle_model)
        self.vehicle_length = self.vehicle_config['dimensions']['length'] #meters
        self.vehicle_width = self.vehicle_config['dimensions']['width'] #meters

        # Load av features configs
        self.av_features = self.config_file_loader("av_features.yaml")
        self.use_RSU_for_trafficlight = self.av_features['traffic_light']['use_rsu']
        self.use_RSU_for_object_detection = self.av_features['object_detection']['use_rsu']
        self.RSU_delay_enable = self.av_features['RSU_delay']['enable']
        self.RSU_delay_value = self.av_features['RSU_delay']['value']

        
        # Create subscriber for /OBU/Sensing topic. This topic publishes the information of detected objects from the POV of the vehicle.
        self.subscriptionSensor = self.create_subscription(DetectedObjects, '/OBU/Sensing', self.detectedObjects_callback, 10)
        # Create subscriber for /v2x/cooperative2 topic. This topic publishes the information of detected objects from RSU.
        self.subscriptionRSU_intersection2 = self.create_subscription(PredictedObjects, '/v2x/predicted_object2', self.intersection2_RSU_detectedObjects_callback, 10)
        self.subscriptionRSU_intersection1 = self.create_subscription(PredictedObjects, '/v2x/predicted_objects1', self.intersection1_RSU_detectedObjects_callback, 10)
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        # Create subscriber to simple_av/portal topic
        self.subscriptionPortal = self.create_subscription(Portal, 'simple_av/portal', self.portal_callback, 10)
        self.reset = False
        self.finished = False
        
        self.detectedObjects = DetectedObjects()  # Initialize detected objects message
        self.intersection2_RSU_detectedObjects = PredictedObjects()
        self.intersection1_RSU_detectedObjects = PredictedObjects()

        # Initialize the publishers
        self.publisher_detected_objects = self.create_publisher(DetectedObjectsArray, 'simple_av/perception/detected_objects', 10)

        self.vehicle_pose = PoseStamped()
        self.node_shut = False

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

    
    def detectedObjects_callback(self, msg):
        """Callback function to update the pose data."""
        self.detectedObjects = msg
    
    def intersection2_RSU_detectedObjects_callback(self, msg):
        """Callback function to update the pose data."""
        self.intersection2_RSU_detectedObjects = msg
    
    def intersection1_RSU_detectedObjects_callback(self, msg):
        """Callback function to update the pose data."""
        self.intersection1_RSU_detectedObjects = msg

    def pose_callback(self, msg):
        self.vehicle_pose = msg
    
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

    # Getting the direction of the object from Automated vehicle point of view
    def object_direction(self, x, y):
        if y <= 2.25 and y >= -2.25:
            # above or behind the vehicle
            if x >=0:
                # object is above the vehicle
                return 'above'
            else:
                # object is behind the vehicle
                return 'behind'
        elif y > 2.25:
            # Left side of the vehicle
            if x >=0:
                # object is above the vehicle
                return 'NW'
            else:
                # object is behind the vehicle
                return 'SW'
        else: 
            # Right side of the vehicle
            if x >=0:
                # object is above the vehicle
                return 'NE'
            else:
                # object is behind the vehicle
                return 'SE'

    def quaternion_to_yaw(self, q):
        """
        Convert a geometry_msgs.msg.Quaternion to a yaw angle in radians.
        :param q: Quaternion (x, y, z, w)
        :return: yaw angle in radians
        """
        t3 = 2.0 * (q.w * q.z + q.x * q.y)
        t4 = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        yaw = atan2(t3, t4)  # Angle around z-axis
        return yaw
    
    def calculate_bounding_box(self, shape, pose):
        """
        Calculate the bounding box of an object based on its shape and position.

        Args:
            shape (geometry_msgs/Vector3): Dimensions of the object (length, width, height).
            pose (geometry_msgs/Point): Position of the object's center.

        Returns:
            list[geometry_msgs/Point]: List of Points representing the bounding box corners.
        """
        half_length = shape.x / 2
        half_width = shape.y / 2
        # Left, Right, Back, Front
        bounding_box = [
            Point(x=pose.x, y=pose.y - half_width, z=pose.z), 
            Point(x=pose.x, y=pose.y + half_width, z=pose.z),
            Point(x=pose.x - half_length, y=pose.y, z=pose.z),
            Point(x=pose.x + half_length, y=pose.y, z=pose.z)
        ]
        return bounding_box
    
    def get_rsu_object_relative_position(self, vehicle_pose, object):
        obj_x = object.x - vehicle_pose['x']
        obj_y = object.y - vehicle_pose['y']
        obj_z = object.z - vehicle_pose['z']
        object_relative_pose = Point(x=obj_x, y=obj_y, z=obj_z)
        return object_relative_pose
    
    def get_object_absolute_position(self, vehicle_pose, object):
        obj_x = vehicle_pose['x'] + object.x
        obj_y = vehicle_pose['y'] + object.y
        obj_z = vehicle_pose['z'] + object.z
        object_absolute_pose = Point(x=obj_x, y=obj_y, z=obj_z)
        return object_absolute_pose

    def apply_inverse_quaternion_rotation(self, quaternion, vector):
        rotation = R.from_quat(np.array([quaternion.x, quaternion.y, quaternion.z, quaternion.w]))
        inverse_rotation = rotation.inv()
        transformed_vector = inverse_rotation.apply(np.array([vector.x, vector.y, vector.z]))
        return Point(x=transformed_vector[0], y=transformed_vector[1], z=transformed_vector[2])

    def quaternion_to_euler_numpy(self, orientation):
        t3 = 2.0 * (orientation.w * orientation.z + orientation.x * orientation.y)
        t4 = 1.0 - 2.0 * (orientation.y**2 + orientation.z**2)
        yaw = np.arctan2(t3, t4)
        return yaw

    def quaternion_multiply(self, object_local_quat, vehicle_global_quat):
        """
        Multiplies two quaternions q1 and q2.

        Args:
            q1 (list or np.array): First quaternion [x1, y1, z1, w1].
            q2 (list or np.array): Second quaternion [x2, y2, z2, w2].

        Returns:
            np.array: Resulting quaternion [x, y, z, w].
        """
        x1, y1, z1, w1 = object_local_quat.x, object_local_quat.y, object_local_quat.z, object_local_quat.w
        x2, y2, z2, w2 = vehicle_global_quat.x, vehicle_global_quat.y, vehicle_global_quat.z, vehicle_global_quat.w

        # Compute the product
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
        z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2

        return Quaternion(x=x, y=y, z=z, w=w)  # x, y, z, w


    def convert_to_global_orientation(self, object_local_quat, vehicle_global_quat):
        """
        Converts local orientation (relative to vehicle) to global orientation.
        
        Args:
            object_local_quat (list or np.array): Quaternion [x, y, z, w] for object relative to vehicle.
            vehicle_global_quat (list or np.array): Quaternion [x, y, z, w] for vehicle in global coordinates.
        
        Returns:
            np.array: Quaternion [x, y, z, w] for the object in global coordinates.
        """
        # Convert to scipy Rotation objects
        object_local_rot = R.from_quat([object_local_quat.x, object_local_quat.y, object_local_quat.z, object_local_quat.w])  # [x, y, z, w]
        vehicle_global_rot = R.from_quat([vehicle_global_quat.x, vehicle_global_quat.y, vehicle_global_quat.z, vehicle_global_quat.w])

        # Compute the global orientation of the object
        object_global_rot = vehicle_global_rot * object_local_rot

        # Return the resulting quaternion
        global_orientation = object_global_rot.as_quat()
        return Quaternion(x=global_orientation[0], y=global_orientation[1], z=global_orientation[2], w=global_orientation[3])  # x, y, z, w

    def handle_detected_objects(self, detected_objects, is_from_rsu):
        detected_objects_list = []
        vehicle_pose = {'x': self.vehicle_pose.pose.position.x, 'y': self.vehicle_pose.pose.position.y, 'z': self.vehicle_pose.pose.position.z}
        for obj in detected_objects.objects:
            detected_obj_msg = DetectedObject()
            
            # label
            if obj.classification:
                detected_obj_msg.label = obj.classification[0].label  # Assuming the first classification is the main one
            detected_obj_msg.is_from_rsu = is_from_rsu
            
            # Object pose (position and orientation)
            if is_from_rsu:
                pose = obj.kinematics.initial_pose_with_covariance.pose
                vector = self.get_rsu_object_relative_position(vehicle_pose, pose.position)
                object_relative_pose = self.apply_inverse_quaternion_rotation(self.vehicle_pose.pose.orientation, vector)
                detected_obj_msg.orientation = Quaternion(x=pose.orientation.x, y=pose.orientation.y, z=pose.orientation.z, w=pose.orientation.w)
                detected_obj_msg.position = Point(x=object_relative_pose.x, y=object_relative_pose.y, z=object_relative_pose.z)
                object_linear_velocity = obj.kinematics.initial_twist_with_covariance.twist.linear.x
                detected_obj_msg.velocity = object_linear_velocity
            else:
                pose = obj.kinematics.pose_with_covariance.pose
                detected_obj_msg.orientation = self.convert_to_global_orientation(pose.orientation, self.vehicle_pose.pose.orientation)
                detected_obj_msg.position = Point(x=pose.position.x, y=pose.position.y, z=pose.position.z)
                object_linear_velocity = obj.kinematics.twist_with_covariance.twist.linear.x
                detected_obj_msg.velocity = object_linear_velocity
            
            detected_obj_msg.relative_direction.data = self.object_direction(detected_obj_msg.position.x, detected_obj_msg.position.y)
            shape = obj.shape.dimensions
            detected_obj_msg.shape = Vector3(x=shape.x, y=shape.y, z=shape.z)
            
            # Bounding Box
            detected_obj_msg.bounding_box = self.calculate_bounding_box(shape, detected_obj_msg.position)

            # Relative Distance
            distances = []
            for objetc_side in detected_obj_msg.bounding_box:
                distances.append(math.sqrt(objetc_side.x**2 + objetc_side.y**2))
            detected_obj_msg.distance = min(distances)
            side = distances.index(min(distances))
            detected_obj_msg.nearest_object_side = side

            detected_objects_list.append(detected_obj_msg)

        return detected_objects_list

    def perception(self):
        if self.finished:
            self.node_shut = True
            return

        if self.vehicle_pose.pose.orientation.x == 0.0 and self.vehicle_pose.pose.orientation.y == 0.0 and \
            self.vehicle_pose.pose.orientation.z == 0.0 and self.vehicle_pose.pose.orientation.w == 0.0 and \
            self.vehicle_pose.pose.position.x == 0.0 and self.vehicle_pose.pose.position.y == 0.0 and self.vehicle_pose.pose.position.z == 0.0:
            self.get_logger().warning("Vehicle data is not available: No position nor orientation data")
            return

        # Handle detected objects
        detected_objects_list = self.handle_detected_objects(self.detectedObjects, False) # Mounted-sensor data
        if self.use_RSU_for_object_detection:
            detected_objects_list.extend(self.handle_detected_objects(self.intersection1_RSU_detectedObjects, True)) # RSU data

        # Create and publish detected objects message
        detected_objects_msg = DetectedObjectsArray()
        detected_objects_msg.objects = detected_objects_list
        self.publisher_detected_objects.publish(detected_objects_msg)

        print("number of objects: ", len(detected_objects_msg.objects))
        for obj in detected_objects_msg.objects:
            if obj.label != 8:
                print("is RSU:", obj.is_from_rsu)
                print("vehicle type:", obj.label)
                print("Direction from vehicle POV: ", obj.relative_direction.data)
                print("Object relative Position from Vehicle: ", obj.position.x, obj.position.y)
                print("Object Orientation: ", obj.orientation.x, obj.orientation.y, obj.orientation.z, obj.orientation.w)
                print("Object speed: ", obj.velocity)
                print("DEBUG - min dist: ", obj.distance) 
                print("object shape size: ", obj.shape)
                print("---------------------")

def main(args=None):
    rclpy.init(args=args)
    node = Perception()
    try:
        while rclpy.ok() and not node.node_shut:
            rclpy.spin_once(node, timeout_sec=0)  # Set timeout to 0 to avoid delay
            node.perception()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
