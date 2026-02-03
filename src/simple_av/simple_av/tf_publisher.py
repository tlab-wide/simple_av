import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TransformStamped
from tf2_ros import TransformBroadcaster
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

        # Setup TF broadcaster
        self.br = TransformBroadcaster(self)

        # Subscribe to GNSS pose
        self.sub = self.create_subscription(
            PoseStamped,
            '/sensing/gnss/pose',
            self.gnss_callback,
            10
        )

        # Always publish fixed base_link -> sensor_kit_base_link and its children
        self.timer = self.create_timer(0.02, self.publish_sensor_tfs)
    
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

        # Build transform map -> base_link from GNSS pose
        t_map_base = TransformStamped()
        t_map_base.header.stamp = msg.header.stamp
        t_map_base.header.frame_id = "map"
        t_map_base.child_frame_id = "base_link"
        t_map_base.transform.translation.x = vehicle_pose.position.x
        t_map_base.transform.translation.y = vehicle_pose.position.y
        t_map_base.transform.translation.z = vehicle_pose.position.z
        t_map_base.transform.rotation = vehicle_pose.orientation

        self.get_logger().debug(
            f"tf publisher\n"
            f"base_link pose: {vehicle_pose.position.x}, {vehicle_pose.position.y}, {vehicle_pose.position.z}\n"
            f"sensor_kit_base_link offset: {self.base_to_sensor_kit['x']}, {self.base_to_sensor_kit['y']}, {self.base_to_sensor_kit['z']}\n"
        )

        self.br.sendTransform(t_map_base)
        self.publish_sensor_tfs(msg.header.stamp)

    def publish_sensor_tfs(self, stamp=None):
        # Publish even when GNSS isn't available yet
        if stamp is None:
            stamp = self.get_clock().now().to_msg()
        self.br.sendTransform(
            self.build_tf('base_link', 'sensor_kit_base_link', self.base_to_sensor_kit, stamp)
        )
        for child_frame, spec in self.sensor_kit_children.items():
            self.br.sendTransform(
                self.build_tf('sensor_kit_base_link', child_frame, spec, stamp)
            )

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
