from setuptools import find_packages
from setuptools import setup

setup(
    name='autoware_system_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('autoware_system_msgs', 'autoware_system_msgs.*')),
)
