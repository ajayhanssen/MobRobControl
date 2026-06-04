from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'mobrob'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'rviz'), ['rviz/mobrob.rviz']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='andreasthoeni',
    maintainer_email='an.thoeni@mci4me.at',
    description='Mobile Robotics Demonstrator Project I',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'tf2_broadcaster = mobrob.tf2_broadcaster:main',
            'tf2_broadcaster_tsim = mobrob.tf2_broadcaster_turtlesim:main',
            'controller = mobrob.controller:main',
            'visualizer = mobrob.visualizer:main',
            'camera = mobrob.camera:main',
            'path_publisher = mobrob.path_publisher:main',
            'watchdog = mobrob_ekf.watchdog:main',
        ],
    },
)
