from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node
import os

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    rviz_config_path = os.path.join(
        get_package_share_directory('simple_av'),
        'rviz',
        'autoware.rviz'
    )

    map_path = os.path.join(
        get_package_share_directory('common'),
        'maps',
        'Kashiwa.osm'
    )

    return LaunchDescription([
        # Declare the RViz argument
        DeclareLaunchArgument(
            'with_rviz',
            default_value='true',
            description='Whether to launch RViz'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('system'), 'launch', 'system_launcher.py')
            )
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('localization'), 'launch', 'localization_launcher.py')
            )
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('perception'), 'launch', 'perception_launcher.py')
            )
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('planning'), 'launch', 'planning_launcher.py')
            )
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('control'), 'launch', 'control_launcher.py')
            )
        ),

        # Lanelet2 Map Loader
        Node(
            package='autoware_map_loader',
            executable='autoware_lanelet2_map_loader',
            name='lanelet2_map_loader',
            parameters=[{
                'lanelet2_map_path': map_path,
                'allow_unsupported_version': True,
                'center_line_resolution': 0.5,
                'use_waypoints': True,  # or false if you don’t want waypoint generation
                'use_streaming': False
            }]
        ),

        # Lanelet2 Map Visualizer
        Node(
            package='autoware_lanelet2_map_visualizer',
            executable='autoware_lanelet2_map_visualizer',
            name='lanelet2_map_visualizer'
        ),

        # RViz2 Node
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_path],
            condition=IfCondition(LaunchConfiguration('with_rviz'))
        ),
    ])
