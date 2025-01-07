import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Quaternion, Vector3
from simple_av_msgs.msg import LocalizationMsg, TrafficSignalsArray, DetectedObject, DetectedObjectsArray
from v2x_msgs.msg import CooperativeSignalsMessage
from autoware_auto_perception_msgs.msg import DetectedObjects
from autoware_auto_perception_msgs.msg import PredictedObjects
from geometry_msgs.msg import PoseStamped
from math import atan2, asin
import math
import yaml
import os
from ament_index_python.packages import get_package_share_directory


class Perception(Node):
    def __init__(self, vehicle_type):
        super().__init__('Perception')

        self.vehicle_type = vehicle_type
        self.vehicle_config = self.load_vehicle_config(vehicle_type)
        # Create subscriber for /v2x/traffic_signals1 topic
        self.subscriptionPose = self.create_subscription(CooperativeSignalsMessage, '/v2x/traffic_signals1', self.trafficSignal_callback, 10)
        
        # Create subscriber for /OBU/Sensing topic. This topic publishes the information of detected objects from the POV of the vehicle.
        self.subscriptionPose = self.create_subscription(DetectedObjects, '/OBU/Sensing', self.detectedObjects_callback, 10)
        # Create subscriber for /OBU/Sensing topic. This topic publishes the information of detected objects from the POV of the vehicle.
        self.subscriptionPose = self.create_subscription(PredictedObjects, '/v2x/cooperative_pure1', self.RSU_detectedObjects_callback, 10)
        
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)
        self.trafficSignal = CooperativeSignalsMessage()  # Initialize traffic signal
        self.detectedObjects = DetectedObjects()  # Initialize detected objects message
        self.RSU_detectedObjects = PredictedObjects()

        # Initialize the publishers
        self.publisher_traffic_signals = self.create_publisher(TrafficSignalsArray, 'simple_av/perception/traffic_signals', 10)
        self.publisher_detected_objects = self.create_publisher(DetectedObjectsArray, 'simple_av/perception/detected_objects', 10)

        self.vehicle_pose = PoseStamped()

        self.vehicle_length = self.vehicle_config['dimensions']['length'] #meters
        self.vehicle_width = self.vehicle_config['dimensions']['width'] #meters

    def trafficSignal_callback(self, msg):
        """Callback function to update the traffic signal data."""
        self.trafficSignal = msg
    
    def detectedObjects_callback(self, msg):
        """Callback function to update the pose data."""
        self.detectedObjects = msg
    
    def RSU_detectedObjects_callback(self, msg):
        """Callback function to update the pose data."""
        self.RSU_detectedObjects = msg

    def pose_callback(self, msg):
        self.vehicle_pose = msg

    
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
        elif y > 2.0:
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
        print("vehicle absolute pos: ", vehicle_pose['x'], vehicle_pose['y'], vehicle_pose['z'])
        obj_x = vehicle_pose['x'] - object.x
        obj_y = vehicle_pose['y'] - object.y
        obj_z = vehicle_pose['z'] - object.z
        object_relative_pose = Point(x=obj_x, y=obj_y, z=obj_z)
        return object_relative_pose

    def handle_detected_objects(self, detected_objects, is_from_rsu):
        detected_objects_list = []
        vehicle_pose = {'x': self.pose.pose.position.x, 'y': self.pose.pose.position.y, 'z': self.pose.pose.position.z}

        for obj in detected_objects.objects:
            detected_obj_msg = DetectedObject()

            # label
            if obj.classification:
                detected_obj_msg.label = obj.classification[0].label  # Assuming the first classification is the main one

            # Sensor Type - is_from_rsu
            detected_obj_msg.is_from_rsu = is_from_rsu

            # pose (position and orientation)
            if is_from_rsu:
                pose = obj.kinematics.initial_pose_with_covariance.pose
            else:
                pose = obj.kinematics.pose_with_covariance.pose
            detected_obj_msg.position = Point(x=pose.position.x, y=pose.position.y, z=pose.position.z)
            detected_obj_msg.orientation = Quaternion(x=pose.orientation.x, y=pose.orientation.y, z=pose.orientation.z, w=pose.orientation.w)

            # relative direction TODO: for RSU the absulute position must be reformated to relative pose to calculate direction
            
            if is_from_rsu: #converting rsu absulute position to relative
                object_relative_pose = self.get_rsu_object_relative_position(vehicle_pose, detected_obj_msg.position)
                detected_obj_msg.relative_direction.data = self.object_direction(object_relative_pose.x, object_relative_pose.y)
            else:
                detected_obj_msg.relative_direction.data = self.object_direction(pose.position.x, pose.position.y)
            
            print("is RSU:", detected_obj_msg.is_from_rsu)
            print("vehicle type:", detected_obj_msg.label)
            print("Object Position: ", detected_obj_msg.position.x, detected_obj_msg.position.y)
            print("Direction from vehicle POV: ", detected_obj_msg.relative_direction.data)
            print("--------------------------------")
            return
            # Objects shape (dimensions)
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

    def get_trafficSignals(self):
        v2i_traffic_signals_id = []
        v2i_traffic_signals_colors = []
        if self.trafficSignal:
            signals = self.trafficSignal.traffic_signals.signals
            for signal in signals:
                map_primitive_id = signal.map_primitive_id
                # Each signal has a list of lights
                for light in signal.lights:
                    color = light.color
                    break
                v2i_traffic_signals_id.append(map_primitive_id)
                v2i_traffic_signals_colors.append(color)
        return v2i_traffic_signals_id, v2i_traffic_signals_colors

    def perception(self):
        
        self.handle_detected_objects(self.detectedObjects, False)
        self.handle_detected_objects(self.RSU_detectedObjects, True)

        return

        # Handle traffic signals
        v2i_traffic_signals_id, v2i_traffic_signals_colors = self.get_trafficSignals()

        # Create and publish traffic signals message
        traffic_signals_msg = TrafficSignalsArray()
        traffic_signals_msg.v2i_traffic_signals_id = v2i_traffic_signals_id
        traffic_signals_msg.v2i_traffic_signals_colors = v2i_traffic_signals_colors
        self.publisher_traffic_signals.publish(traffic_signals_msg)
        # self.get_logger().info('Published traffic signal data')

        # Handle detected objects
        detected_objects_list = self.handle_detected_objects()

        # Create and publish detected objects message
        detected_objects_msg = DetectedObjectsArray()
        detected_objects_msg.objects = detected_objects_list
        self.publisher_detected_objects.publish(detected_objects_msg)
        # self.get_logger().info('Published detected objects data')
        ground_truth = self.get_groundTruth_msg()
        q = Quaternion(x=ground_truth.pose.orientation.x, y=ground_truth.pose.orientation.y, z=ground_truth.pose.orientation.z, w=ground_truth.pose.orientation.w)
        yaw_degree_vehicle = math.degrees(self.quaternion_to_yaw(q))
        sides = ['left', 'right', 'back', 'front']
        print("number of objects: ", len(detected_objects_msg.objects))
        for obj in detected_objects_msg.objects:
            if obj.label != 7:
                print("is RSU:", obj.is_from_rsu)
                print("vehicle type:", obj.label)
                print("Direction from vehicle POV: ", obj.relative_direction.data)
                print("Object relative Position from Vehicle: ", obj.position.x, obj.position.y)
                print("closest side of the object: ", sides[obj.nearest_object_side])
                print("bounding_box left: ", obj.bounding_box[0])
                print("bounding_box right: ", obj.bounding_box[1])
                print("bounding_box back: ", obj.bounding_box[2])
                print("bounding_box front: ", obj.bounding_box[3])
                print("DEBUG - min dist: ", obj.distance) 
                print("object shape size: ", obj.shape)
                print("---------------------")


def main(args=None):
    rclpy.init(args=args)
    node = Perception('bus')
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0)  # Set timeout to 0 to avoid delay
            node.perception()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
