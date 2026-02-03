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
            package='perception',
            executable='obu_perception',
            name='obu_perception_node',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        ),
        Node(
            package='perception',
            executable='traffic_light_handler',
            name='traffic_light_handler_node',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        ),
        # Disabled: superseded by object_prediction_handler + v2x_handler
        # Node(
        #     package='perception',
        #     executable='object_detection_handler',
        #     name='object_detection_handler_node',
        #     output='screen',
        #     arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        # ),
        Node(
            package='perception',
            executable='object_tracking_handler',
            name='object_tracking_handler_node',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        ),
        Node(
            package='perception',
            executable='object_prediction_handler',
            name='object_prediction_handler_node',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        ),
        Node(
            package='perception',
            executable='v2x_handler',
            name='v2x_handler_node',
            output='screen',
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        )
    ])
