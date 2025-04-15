from setuptools import setup
import os
from glob import glob

package_name = 'bringup'

setup(
    name=package_name,
    version='0.0.1',
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Add this to include all .py files in the launch folder
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Hamid Reza Hemati',
    maintainer_email='your@email.com',
    description='Bringup launch files for simple_av',
    license='TODO: License',
    tests_require=['pytest'],
)
