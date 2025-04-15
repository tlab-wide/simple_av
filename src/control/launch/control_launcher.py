from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='control',
            executable='controller',
            name='control_node',
            output='screen'
        )
    ])