from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation time'
        ),
        DeclareLaunchArgument(
            'log_level',
            default_value='WARN',
            description='Console log level: DEBUG, INFO, WARN'
        ),
        # Mission Planner starts immediately
        Node(
            package='planning',
            executable='mission_planning',
            name='mission_planning_node',
            output='screen',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
            arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
        ),

        # Delay Behavior Path Planner by 5 seconds
        TimerAction(
            period=3.0,
            actions=[
                Node(
                    package='planning',
                    executable='behavior_path_planner',
                    name='behavior_path_planner_node',
                    output='screen',
                    parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
                    arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
                )
            ]
        ),

        # Delay Behavior Motion Planner by 7 seconds (a bit after path planner)
        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package='planning',
                    executable='behavior_motion_planner',
                    name='behavior_motion_planner_node',
                    output='screen',
                    parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
                    arguments=['--ros-args', '--log-level', LaunchConfiguration('log_level')]
                )
            ]
        )
    ])
