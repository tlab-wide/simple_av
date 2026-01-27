from setuptools import find_packages
from setuptools import setup

setup(
    name='autoware_adapi_version_msgs',
    version='1.7.0',
    packages=find_packages(
        include=('autoware_adapi_version_msgs', 'autoware_adapi_version_msgs.*')),
)
