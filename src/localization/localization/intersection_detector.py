import rclpy
from rclpy.node import Node
import os
import yaml
from geometry_msgs.msg import PoseStamped
from simple_av_msgs.msg import LocalizationIntersectionStatus
import math
from ament_index_python.packages import get_package_share_directory
from collections import deque

class IntersectionStatusDetector(Node):
    def __init__(self):
        super().__init__('intersection_status_detector_node')

        # Load intersection data
        self.intersection_profiles = self.load_intersections()

        # Create subscriber to gnss/pos topic
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)

        # Create publisher
        self.publisher = self.create_publisher(
            LocalizationIntersectionStatus,
            'simple_av/localization/intersection_status',
            10
        )
        self.intersection_names = ["intersection_1", "intersection_2", "intersection_3", "intersection_4"]
        self.position_log = deque(maxlen=20)
        self.status = None

    def load_intersections(self):
        package_share_directory = get_package_share_directory('common')
        zones_path = os.path.join(package_share_directory, "zones", 'intersection_profiles.yaml')

        with open(zones_path, "r") as file:
            intersection_profiles = yaml.safe_load(file)
        return intersection_profiles


    def calculate_distance(self, p1, p2):
        return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)
    
    def pose_callback(self, msg: PoseStamped):
        vehicle_position = {
            'x': msg.pose.position.x,
            'y': msg.pose.position.y
        }
        intersections = self.intersection_profiles['intersections']
        self.position_log.append(vehicle_position)

        closest = None
        for name, data in intersections.items():
            # print(f"intersection name: {data['name']}")
            intersection_referece_point = data['reference_point']
            # print(f"reference point x: {intersection_referece_point}")
            threshold = data['threshold']
            # print(f"threshold: {threshold}")
            distance = self.calculate_distance(vehicle_position, intersection_referece_point)

            if distance < threshold:
                closest = (name, distance, intersection_referece_point, threshold)
        
        print('closest: ', closest)
        intersection_status_msg = LocalizationIntersectionStatus()
        if closest:
            name, distance, intersection_referece_point, threshold = closest
            
            distance_to_prev_pose = self.calculate_distance(self.position_log[0], intersection_referece_point)
            if distance < distance_to_prev_pose:
                self.status = 'approaching'      
                print("approaching")         
            elif distance > distance_to_prev_pose:
                self.status = 'exiting'
                print("exiting")
            elif distance == distance_to_prev_pose and self.status == 'approaching':
                print("== aproaching")
                self.status = 'approaching'
            elif distance == distance_to_prev_pose and self.status == 'exiting':
                print("== exiting")
                self.status = 'exiting'

            if distance < threshold * 0.3:
                self.status = 'in'
                print("in")
            
            intersection_status_msg.intersection_name = name
            intersection_status_msg.status = self.status
            intersection_status_msg.distance_to_intersection = float(distance)
        else:
            intersection_status_msg.intersection_name = 'none'
            intersection_status_msg.status = 'none'
            intersection_status_msg.distance_to_intersection = float('inf')

        self.publisher.publish(intersection_status_msg)

def main(args=None):
    rclpy.init(args=args)
    node = IntersectionStatusDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
