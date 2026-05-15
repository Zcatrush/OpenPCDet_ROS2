# **环境要求**
- Ubuntu 22.04, ROS 2 Humble
- CUDA 11.7, CuDNN 8.5.0.96
- Python 3.10, PyTorch 2.0.1+cu117
- NumPy 1.25.2
- 参考：
  - https://github.com/pradhanshrijal/pcdet_ros2.git
  - https://github.com/open-mmlab/OpenPCDet.git
  - https://zhuanlan.zhihu.com/p/663973630
# **使用方法**
环境配置：
```
cd ~/OpenPCDet_ROS2
python3 -m pip install catkin_pkg
sudo apt install ros-humble-ament-cmake-nose -y
python3 -m pip install nose
python3 -m pip install transform3d
rosdep install -i --from-path src --rosdistro humble -y
sudo apt update
sudo apt install ros-$ROS_DISTRO-vision-msgs-rviz-plugins
echo "alias colbuild='COLCON_LOG_LEVEL=error AMENT_IGNORE_NONEXISTENT_PACKAGES=1 colcon build --symlink-install'" >> ~/.bashrc
source ~/.bashrc
```
构建：
```
cd ~/OpenPCDet_ROS2
rm -rf build install log
colbuild
```
运行：
```
cd ~/OpenPCDet_ROS2
source install/setup.bash
ros2 launch pcdet_ros2 pcdet.launch.py
```
最后使用rviz2进行可视化.
# **说明**
首先播放对应的rosbag文件，然后在`src/pcdet_ros2/launch/pcdet.launch.py`下更改对应的的input topic.
.pth文件请保存至路径：`src/pcdet_ros2/checkpoints`.  
若需要更改.pth文件，需要修改`src/pcdet_ros2/config`下对应的文件中的信息.  
如需要更改算法，需要修改`src/pcdet_ros2/launch/pcdet.launch.py`及`src/pcdet_ros2/config`中对应文件的信息.  

