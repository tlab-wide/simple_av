from setuptools import setup

package_name = 'localization'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['package.xml']),
        ('share/' + package_name, ['package.xml']),
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
            'localization = localization.localization_node:main',
        ],
    },
)
