from setuptools import find_packages, setup

package_name = 'simple_pcd_publisher'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ikun',
    maintainer_email='ikun@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'kitti_pointcloud_publisher = simple_pcd_publisher.publisher_node:main',
        'detection_visualizer = simple_pcd_publisher.detection_visualizer:main',
        ],
    },
)
