from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'log_level',
            default_value='WARN',
            description='Console log level: DEBUG, INFO, WARN'
        ),
        Node(
            package='localization',
            executable='localization',
            name='localization_node',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        ),
        Node(
            package='localization',
            executable='intersection_detector',
            name='intersection_detector_node',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        )
    ])
