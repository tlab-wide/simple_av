from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'common'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        # Install all config files to: install/share/common/configs/
        (os.path.join('share', package_name, 'configs'), glob('configs/*.yaml')),
        # Install all zone files to: install/share/common/zones/
        (os.path.join('share', package_name, 'zones'), glob('zones/*.yaml')),
        # Install all map files to: install/share/common/maps/
        (os.path.join('share', package_name, 'maps'), glob('maps/*.json')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hamid_ubuntu',
    maintainer_email='hrhhemati@gmail.com',
    description='Shared configs, maps, and utilities for simple_av project.',
    license='TODO: License declaration',
    tests_require=['pytest'],
)
