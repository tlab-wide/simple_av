from setuptools import find_packages
from setuptools import setup

setup(
    name='simple_av_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('simple_av_msgs', 'simple_av_msgs.*')),
)
