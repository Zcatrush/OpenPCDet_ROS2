# **环境要求**
参考https://github.com/pradhanshrijal/pcdet_ros2.git
- Ubuntu 22.04, ROS 2 Humble
- CUDA 11.7, CuDNN 8.5.0.96
- Python 3.10, PyTorch 2.0.1+cu117
- NumPy 1.25.2
- OpenPCDet框架
  - 官方项目：https://github.com/open-mmlab/OpenPCDet.git
  - 安装参考：https://zhuanlan.zhihu.com/p/663973630
# **使用方法**
构建：
```
cd ~/OpenPCDet_ROS2
python3 -m pip install catkin_pkg
sudo apt install ros-humble-ament-cmake-nose -y
python3 -m pip install nose
python3 -m pip install transform3d
rosdep install -i --from-path src --rosdistro humble -y
rm -rf build install log
colcon build --symlink-install --packages-select ros2_numpy pcdet_ros2 simple_pcd_publisher

```
构建完成之后执行：
```
#新建终端
cd ~/OpenPCDet_ROS2
source install/setup.bash
ros2 run simple_pcd_publisher pointcloud_publisher
```
```
#新建终端
cd ~/OpenPCDet_ROS2
source install/setup.bash
ros2 launch pcdet_ros2 pcdet.launch.py
```
```
#新建终端
cd ~/OpenPCDet_ROS2
source install/setup.bash
ros2 run simple_pcd_publisher detection_visualizer
```
最后使用rviz2进行可视化.

