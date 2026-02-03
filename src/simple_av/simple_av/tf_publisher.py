import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from tf2_ros import StaticTransformBroadcaster
import yaml
import os
import math
from ament_index_python.packages import get_package_share_directory

class SensorTFPublisher(Node):
    def __init__(self):
        super().__init__('tf_publisher')

        # Use simulation time when /clock is available
        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)

        self.sensors_calibration = self.config_file_loader("sensors_calibration.yaml")
        self.base_to_sensor_kit = self.sensors_calibration['base_link']['sensor_kit_base_link']
        self.sensor_kit_children = self.sensors_calibration.get('sensor_kit_base_link', {})

        # Setup static TF broadcaster
        self.br = StaticTransformBroadcaster(self)

        # Publish fixed transforms once on startup
        self.publish_sensor_tfs(self.get_clock().now().to_msg())
    
    def config_file_loader(self, file_name):
        # Path to the YAML file
        package_share_directory = get_package_share_directory('common')
        config_path = os.path.join(package_share_directory, "configs", file_name)
        # Load the configuration file
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config

    def publish_sensor_tfs(self, stamp=None):
        if stamp is None:
            stamp = self.get_clock().now().to_msg()
        transforms = [
            self.build_tf('base_link', 'sensor_kit_base_link', self.base_to_sensor_kit, stamp)
        ]
        for child_frame, spec in self.sensor_kit_children.items():
            transforms.append(
                self.build_tf('sensor_kit_base_link', child_frame, spec, stamp)
            )
        self.br.sendTransform(transforms)

    def build_tf(self, parent_frame, child_frame, spec, stamp):
        t_base_sensor = TransformStamped()
        t_base_sensor.header.stamp = stamp
        t_base_sensor.header.frame_id = parent_frame
        t_base_sensor.child_frame_id = child_frame
        t_base_sensor.transform.translation.x = spec.get('x', 0.0)
        t_base_sensor.transform.translation.y = spec.get('y', 0.0)
        t_base_sensor.transform.translation.z = spec.get('z', 0.0)
        qx, qy, qz, qw = self.quaternion_from_euler(
            spec.get('roll', 0.0),
            spec.get('pitch', 0.0),
            spec.get('yaw', 0.0),
        )
        t_base_sensor.transform.rotation.x = qx
        t_base_sensor.transform.rotation.y = qy
        t_base_sensor.transform.rotation.z = qz
        t_base_sensor.transform.rotation.w = qw
        return t_base_sensor

    def quaternion_from_euler(self, roll, pitch, yaw):
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        qw = cr * cp * cy + sr * sp * sy
        qx = sr * cp * cy - cr * sp * sy
        qy = cr * sp * cy + sr * cp * sy
        qz = cr * cp * sy - sr * sp * cy
        return qx, qy, qz, qw

def main(args=None):
    rclpy.init(args=args)
    node = SensorTFPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
