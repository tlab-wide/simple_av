from setuptools import find_packages
from setuptools import setup

setup(
    name='autoware_internal_metric_msgs',
    version='1.12.0',
    packages=find_packages(
        include=('autoware_internal_metric_msgs', 'autoware_internal_metric_msgs.*')),
)
