from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='planning',
            executable='mission_planning',
            name='mission_planning_node',
            output='screen'
        ),
        Node(
            package='planning',
            executable='behavior_path_planner',
            name='behavior_path_planner_node',
            output='screen'
        ),
        Node(
            package='planning',
            executable='behavior_motion_planner',
            name='behavior_motion_planner_node',
            output='screen'
        )
    ])