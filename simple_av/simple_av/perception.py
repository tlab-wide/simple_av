import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Quaternion, Vector3
from simple_av_msgs.msg import LocalizationMsg, TrafficSignalsArray, DetectedObject, DetectedObjectsArray
from v2x_msgs.msg import CooperativeSignalsMessage
from autoware_auto_perception_msgs.msg import DetectedObjects
import math

class Perception(Node):
    def __init__(self):
        super().__init__('Perception')

        # Create subscriber for /v2x/traffic_signals1 topic
        self.subscriptionPose = self.create_subscription(CooperativeSignalsMessage, '/v2x/traffic_signals1', self.trafficSignal_callback, 10)
        
        # Create subscriber for /OBU/Sensing topic. This topic publishes the information of detected objects from the POV of the vehicle.
        self.subscriptionPose = self.create_subscription(DetectedObjects, '/OBU/Sensing', self.detectedObjects_callback, 10)

        self.trafficSignal = CooperativeSignalsMessage()  # Initialize traffic signal
        self.detectedObjects = DetectedObjects()  # Initialize detected objects message

        # Initialize the publishers
        self.publisher_traffic_signals = self.create_publisher(TrafficSignalsArray, 'simple_av/perception/traffic_signals', 10)
        self.publisher_detected_objects = self.create_publisher(DetectedObjectsArray, 'simple_av/perception/detected_objects', 10)

        self.vehicle_length = 4.8895 #meters
        self.vehicle_width = 1.895 #meters

    def trafficSignal_callback(self, msg):
        """Callback function to update the traffic signal data."""
        self.trafficSignal = msg
    
    def detectedObjects_callback(self, msg):
        """Callback function to update the pose data."""
        self.detectedObjects = msg

    def object_direction(self, x, y):
        if y <= 2.0 and y >= -2.0:
            # above or behind the vehicle
            if x >=0:
                # object is above the vehicle
                return 'S'
            else:
                # object is behind the vehicle
                return 'N'
        elif y > 2.0:
            # right side of the vehicle
            if x >=0:
                # object is above the vehicle
                return 'SE'
            else:
                # object is behind the vehicle
                return 'NE'
        else: 
            # left side of the vehicle
            if x >=0:
                # object is above the vehicle
                return 'SW'
            else:
                # object is behind the vehicle
                return 'NW'


    def handle_detected_objects(self):
        detected_objects_list = []

        for obj in self.detectedObjects.objects:
            detected_obj_msg = DetectedObject()

            # Extract label
            if obj.classification:
                detected_obj_msg.label = obj.classification[0].label  # Assuming the first classification is the main one

            # Extract pose (position and orientation)
            pose = obj.kinematics.pose_with_covariance.pose
            detected_obj_msg.relative_position = Point(x=pose.position.x, y=pose.position.y, z=pose.position.z)
            detected_obj_msg.orientation = Quaternion(x=pose.orientation.x, y=pose.orientation.y, z=pose.orientation.z, w=pose.orientation.w)

            # Finding the object direction
            detected_obj_msg.Direction = self.object_direction(pose.position.x, pose.position.y)

            # Extract shape (dimensions)
            shape = obj.shape.dimensions
            detected_obj_msg.shape = Vector3(x=shape.x, y=shape.y, z=shape.z)

            relative_x_distance = pose.position.x - shape.x / 2 - self.vehicle_length/2
            relative_y_distance = pose.position.y - shape.y / 2 - self.vehicle_width/2
            detected_obj_msg.relative_distance = Point(x=relative_x_distance, y=relative_y_distance, z=pose.position.z)

            detected_obj_msg.distance = math.sqrt(relative_x_distance**2 + relative_y_distance**2)

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
        print("number of objects: ", len(detected_objects_msg.objects))
        for obj in detected_objects_msg.objects:
            if obj.label != 7:
                print(obj.label)
                print(obj.relative_position.x, obj.relative_position.y, obj.relative_position.z)
                print(obj.relative_distance.x, obj.relative_distance.y)
                print(obj.distance)
                print(obj.shape)
                print("---------------------")


def main(args=None):
    rclpy.init(args=args)
    node = Perception()
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0)  # Set timeout to 0 to avoid delay
            node.perception()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
