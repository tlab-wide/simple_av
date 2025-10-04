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
            'monitor = simple_av.monitor:main',
            'lanelet_map_publisher = simple_av.lanelet_map_publisher:main',
            'tf_publisher = system.tf_publisher:main',
            'point_visualizer = system.point_visualizer:main'
        ],
    },
)
