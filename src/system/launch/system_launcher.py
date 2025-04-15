from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
       Node( 
            package='system',
            executable='sim_monitor',
            name='sim_monitor_node',
            output='screen'
        ),
        Node(
            package='system',
            executable='portal',
            name='portal_node',
            output='screen'
        )
    ])