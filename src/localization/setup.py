from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'localization'

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
    description='Localization node for the AV project',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'localization = localization.localization:main',
            'global_localization = localization.global_localization:main',
            'intersection_detector = localization.intersection_detector:main',
            'localization_fusion = localization.localization_fusion:main',
                    ],
    },
)
