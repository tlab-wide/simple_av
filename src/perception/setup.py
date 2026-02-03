from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'perception'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hamid_ubuntu',
    maintainer_email='hrhhemati@gmail.com',
    description='Perception node for the simple_av project.',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'obu_perception = perception.obu_perception:main',
            'traffic_light_handler = perception.trafficLightHandler:main',
            'object_detection_handler = perception.objectDetectionHandler:main',
            'object_tracking_handler = perception.objectTrackingHandler:main',
            'object_prediction_handler = perception.objectPredictionHandler:main',
        ],
    },
)
