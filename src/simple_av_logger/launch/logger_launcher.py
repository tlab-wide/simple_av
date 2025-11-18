from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='simple_av_logger',
            executable='logger_node',
            name='logger_node',
            output='screen'
        )
    ])