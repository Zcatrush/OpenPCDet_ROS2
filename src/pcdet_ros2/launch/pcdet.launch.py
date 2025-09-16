import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from nav2_common.launch import RewrittenYaml

def generate_launch_description():
    package_name = 'pcdet_ros2'
    package_dir = get_package_share_directory(package_name)
    config_file = 'pcdet_pvrcnn.param.yaml'
    #config_file = 'pcdet_pointpillar.param.yaml'
    namespace = LaunchConfiguration('namespace')
    params_file = LaunchConfiguration('params_file')
    input_topic = LaunchConfiguration('input_topic')
    output_topic = LaunchConfiguration('output_topic')

    configured_params = RewrittenYaml(
        source_file=params_file,
        root_key=namespace,
        param_rewrites={}
    )

    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Top-level namespace')

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(package_dir, 'config', config_file),
        description='Full path to the ROS 2 parameters file to use for the launched nodes'
    )

    declare_input_topic_cmd = DeclareLaunchArgument(
        'input_topic',
        default_value='/point_cloud',  # 输入点云话题
        description='Input Point Cloud'
    )

    declare_output_topic_cmd = DeclareLaunchArgument(
        'output_topic',
        default_value='/cloud_detections',  # 目标检测的输出话题
        description='Output Object Detections'
    )

    # pcdet node (目标检测节点)
    pcdet = Node(
        package=package_name,
        executable='pcdet',
        name='pcdet',
        output='screen',
        parameters=[configured_params,
                    {'package_folder_path': package_dir}],
        remappings=[("input", input_topic),  # pcdet 接收点云数据
                    ("output", output_topic)]  # pcdet 发布目标检测结果
    )

    # pointcloud_publisher node (点云发布节点)
    pointcloud_publisher = Node(
        package='simple_pcd_publisher',
        executable='pointcloud_publisher',
        name='pointcloud_publisher',
        output='screen',
        parameters=[{
            'input_topic': input_topic  # 点云发布到 /point_cloud
        }]
    )

   

    # 使用 GroupAction 来并行启动节点
    ld = LaunchDescription()

    # 将所有节点添加到 GroupAction 中，确保它们并行启动
    group_action = GroupAction([
        declare_namespace_cmd,
        declare_params_file_cmd,
        declare_input_topic_cmd,
        declare_output_topic_cmd,
        pcdet,
        pointcloud_publisher
    ])

    ld.add_action(group_action)

    return ld
