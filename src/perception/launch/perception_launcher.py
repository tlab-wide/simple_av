from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='perception',
            executable='traffic_light_handler',
            name='traffic_light_handler_node',
            output='screen'
        ),
        Node(
            package='perception',
            executable='object_detection_handler',
            name='object_detection_handler_node',
            output='screen'
        )
    ])
