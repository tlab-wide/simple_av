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
            package='system',
            executable='sim_monitor',
            name='sim_monitor_node',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        ),
        Node(
            package='system',
            executable='portal',
            name='portal_node',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        )
    ])
