from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import os


def generate_launch_description():
    pkg_share = get_package_share_directory('simple_av')
    urdf_path = os.path.join(pkg_share, 'urdf', 'bus_model.urdf')
    with open(urdf_path, 'r', encoding='utf-8') as urdf_file:
        robot_description = urdf_file.read()

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='bus_model_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen',
        ),
    ])
