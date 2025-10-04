import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TransformStamped
from tf2_ros import TransformBroadcaster
import yaml
import os
from ament_index_python.packages import get_package_share_directory

class SensorTFPublisher(Node):
    def __init__(self):
        super().__init__('tf_publisher')

        self.sensors_calibration = self.config_file_loader("sensors_calibration.yaml")
        self.sensor_kit_base_link = self.sensors_calibration['base_link']['sensor_kit_base_link']

        # Setup TF broadcaster
        self.br = TransformBroadcaster(self)

        # Subscribe to GNSS pose
        self.sub = self.create_subscription(
            PoseStamped,
            '/sensing/gnss/pose',
            self.gnss_callback,
            10
        )
    
    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def gnss_callback(self, msg: PoseStamped):
        # Vehicle pose in map frame
        vehicle_pose = msg.pose


        # Build transform map -> sensor_kit_base_link
        t = TransformStamped()
        t.header.stamp = msg.header.stamp
        t.header.frame_id = "map"
        t.child_frame_id = "sensor_kit_base_link"

        # Just add the static offsets
        t.transform.translation.x = vehicle_pose.position.x + self.sensor_kit_base_link['x']
        t.transform.translation.y = vehicle_pose.position.y + self.sensor_kit_base_link['y']
        t.transform.translation.z = vehicle_pose.position.z + self.sensor_kit_base_link['z']

        # Orientation = vehicle orientation (no extra rotations needed)
        t.transform.rotation = vehicle_pose.orientation  

        self.get_logger().info(
            f"tf publisher\n"
            f"calibrations: {self.sensor_kit_base_link['x']}, {self.sensor_kit_base_link['y']}, {self.sensor_kit_base_link['z']}\n"
            f"vehicle pose: {vehicle_pose.position.x}, {vehicle_pose.position.y}, {vehicle_pose.position.z}\n"
        )


        self.br.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    node = SensorTFPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
