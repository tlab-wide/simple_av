from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction

def generate_launch_description():
    return LaunchDescription([
        # Mission Planner starts immediately
        Node(
            package='planning',
            executable='mission_planning',
            name='mission_planning_node',
            output='screen'
        ),

        # 🕒 Delay Behavior Path Planner by 5 seconds
        TimerAction(
            period=3.0,
            actions=[
                Node(
                    package='planning',
                    executable='behavior_path_planner',
                    name='behavior_path_planner_node',
                    output='screen'
                )
            ]
        ),

        # 🕒 Delay Behavior Motion Planner by 7 seconds (a bit after path planner)
        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package='planning',
                    executable='behavior_motion_planner',
                    name='behavior_motion_planner_node',
                    output='screen'
                )
            ]
        )
    ])
