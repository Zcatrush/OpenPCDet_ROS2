# 构建方法
环境配置完成之后执行：
```
#新建终端
cd ~/ros2_ws
source install/setup.bash
ros2 run simple_pcd_publisher kitti_pointcloud_publisher
```
```
#新建终端
cd ~/ros2_ws
source install/setup.bash
ros2 launch pcdet_ros2 pcdet.launch.py
```
```
#新建终端
cd ~/ros2_ws
source install/setup.bash
ros2 run simple_pcd_publisher detection_visualizer
```
最后使用rviz2进行可视化.
