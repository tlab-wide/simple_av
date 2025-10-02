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
        ),
        Node(
            package='system',
            executable='obu_sensor_tf_publisher',
            name='obu_sensor_tf_publisher_node',
            output='screen'
        ),
        Node(
            package='system',
            executable='point_visualizer',
            name='point_visualizer_node',
            output='screen'
        )
    ])