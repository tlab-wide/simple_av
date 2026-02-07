from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'simple_av'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(include=[package_name]),  # <--- Fix here
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.obj')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.mtl')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.dae')),
        (os.path.join('share', package_name, 'rviz', 'BusModel'), glob('rviz/BusModel/*')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Hamid Reza Hemati',
    maintainer_email='your@email.com',
    description='simple-av launch files for running the system',
    license='TODO: License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rviz_path_monitor = simple_av.rviz_path_monitor:main',
            'rviz_lanelet_map_publisher = simple_av.rviz_lanelet_map_publisher:main',
            'tf_publisher = simple_av.tf_publisher:main',
            'rviz_intersection_layout_visualizer = simple_av.rviz_intersection_layout_visualizer:main',
            'rviz_status_publisher = simple_av.rviz_status_publisher:main',
            'rviz_waypoint_speed_visualizer = simple_av.rviz_waypoint_speed_visualizer:main'
        ],
    },
)
