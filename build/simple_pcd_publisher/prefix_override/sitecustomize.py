import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ikun/OpenPCDet_ROS2/install/simple_pcd_publisher'
