
from setuptools import find_packages, setup
import os

package_name = 'ros2_demo'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), [os.path.join('launch', 'ros2_demo.launch.xml')]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='TODO@apotpod.co.jp',
    description='ROS2 Package for intdash ROS Bridge demo',
    license='MIT',
    entry_points={
        'console_scripts': [
            'hello_publisher = ros2_demo.hello_pub:main',
            'cube_publisher = ros2_demo.pointcloud2_pub:main',
            'compressed_image_publisher = ros2_demo.image_pub:main',
        ],
    },
)
