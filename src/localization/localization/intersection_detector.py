import rclpy
from rclpy.node import Node
import os
import json
from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped
from simple_av_msgs.msg import LocalizationIntersectionStatus
import math

class IntersectionStatusDetector(Node):
    def __init__(self):
        super().__init__('intersection_status_detector_node')

        # Load intersection data
        self.intersections = self.load_intersections()

        # Create subscriber to gnss/pos topic
        self.subscriptionPose = self.create_subscription(PoseStamped, '/sensing/gnss/pose', self.pose_callback, 10)

        # Create publisher
        self.publisher = self.create_publisher(
            LocalizationIntersectionStatus,
            'simple_av/localization/intersection_status',
            10
        )

    def load_intersections(self):
        package_dir = get_package_share_directory('common')
        json_path = os.path.join(package_dir, 'zones', 'intersection_profiles.json')

        with open(json_path, 'r') as f:
            return json.load(f)

    def calculate_distance(self, p1, p2):
        return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)
    
    def pose_callback(self, msg: PoseStamped):
        vehicle_position = {
            'x': msg.pose.position.x,
            'y': msg.pose.position.y
        }
        print("vehicle position: ", vehicle_position)
        print(self.intersections)
        print("----------------------------")
        print("----------------------------")
        print(self.intersections.items())

        return

        closest = None
        min_distance = float('inf')

        for name, data in self.intersections.items():
            intersection_point = data['point']
            threshold = data['threshold']
            distance = self.calculate_distance(vehicle_position, intersection_point)

            if distance < threshold and distance < min_distance:
                closest = (name, distance, threshold)

        status_msg = LocalizationIntersectionStatus()

        if closest:
            name, distance, threshold = closest
            status_msg.intersection_name = name

            if distance < threshold * 0.33:
                status_msg.status = 'in'
            elif distance < threshold * 0.66:
                status_msg.status = 'approaching'
            else:
                status_msg.status = 'exiting'

            status_msg.distance_to_intersection = float(distance)
        else:
            status_msg.intersection_name = 'none'
            status_msg.status = 'none'
            status_msg.distance_to_intersection = float('inf')

        self.publisher.publish(status_msg)

def main(args=None):
    rclpy.init(args=args)
    node = IntersectionStatusDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
