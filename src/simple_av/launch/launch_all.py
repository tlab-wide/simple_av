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
        'simple_av.rviz'
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

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('simple_av_logger'), 'launch', 'logger_launcher.py')
            )
        ),

        # 👉 Lanelet2 Map Publisher
        Node(
            package='simple_av',
            executable='rviz_lanelet_map_publisher',
            name='rviz_lanelet_map_publisher_node',
            output='screen'
        ),

        # 👉 path monitor node
        Node(
            package='simple_av',
            executable='rviz_path_monitor',
            name='rviz_path_monitor_node',
            output='screen'
        ),
        Node(
            package='simple_av',
            executable='tf_publisher',
            name='tf_publisher_node',
            output='screen'
        ),
        Node(
            package='simple_av',
            executable='rviz_point_visualizer',
            name='rviz_point_visualizer_node',
            output='screen'
        ),
        Node(
            package='simple_av',
            executable='rviz_intersection_layout_visualizer',
            name='rviz_intersection_layout_visualizer_node',
            output='screen'
        ),
        Node(
            package='simple_av',
            executable='rviz_status_publisher',
            name='rviz_status_publisher_node',
            output='screen'
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
