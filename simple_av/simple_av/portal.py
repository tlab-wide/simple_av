import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
import numpy as np
import math
from simple_av_msgs.msg import Portal


class portal(Node):
    def __init__(self):
        super().__init__('portal')

        # Create subscriber to gnss/pos topic
        self.subscriptionPose = self.create_subscription(
            PoseStamped,
            '/sensing/gnss/pose',
            self.pose_callback,
            10
        )
        self.portal_publisher = self.create_publisher(Portal, 'simple_av/portal', 10)
        self.pose = PoseStamped()
        self.initial_position = Point()
        self.isInitialPoseSampled = False
        self.isPortalReached = False
        self.reset = False
        self.last_pose = Point()
        self.current_pose = Point()
    
    def pose_callback(self, msg):
        self.pose = msg
    
    def calculate_distance(self, point1, point2):
        return  math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def initial_pose(self):
        if self.pose and self.pose.pose.position.x != 0 and self.pose.pose.position.y != 0 and self.pose.pose.position.z != 0:
            # print(pose_msg.pose.position.x, pose_msg.pose.position.y, pose_msg.pose.position.z)
            self.initial_position = self.pose.pose.position
            self.current_pose = self.pose.pose.position
            self.last_pose = self.current_pose
            self.isInitialPoseSampled = True

    def portal_detector(self):
        self.current_pose = self.pose.pose.position
        if self.calculate_distance(self.current_pose, self.last_pose) > 75.0 :
            distance_to_init = self.calculate_distance(self.current_pose, self.initial_position)
            print("Jump detected")
            print(self.initial_position)
            print(self.current_pose)
            print(distance_to_init)
            if self.calculate_distance(self.current_pose, self.initial_position) < 5.0 and not self.isPortalReached:
                print("Portal Detected")
                self.isPortalReached = True
                self.initial_pose = self.current_pose
        self.last_pose = self.current_pose
        self.publish_portal()
                

    def portal_reset(self):
        if not self.isInitialPoseSampled:
            self.initial_pose()
        else:
            self.portal_detector()

    def publish_portal(self):
        portal_reset = Portal()
        portal_reset.reset = self.isPortalReached
        self.portal_publisher.publish(portal_reset)
        self.isPortalReached = False


def main(args=None):
    rclpy.init(args=args)
    node = portal()
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=None)# Set timeout to 0 to avoid delay
            node.portal_reset()
    finally:
        node.destroy_node()
        rclpy.shutdown()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()