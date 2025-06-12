import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
import struct
import numpy as np
from std_msgs.msg import Header

class PointCloudPublisher(Node):
    def __init__(self):
        super().__init__('pointcloud_publisher')
        self.publisher_ = self.create_publisher(PointCloud2, '/point_cloud', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)  # 1秒发一次
        self.file_index = 0
        self.files = sorted(self.get_files('/home/ikun/OpenPCDet/data/kitti/training/velodyne'))
        self.get_logger().info(f'Found {len(self.files)} pointcloud files.')

    def get_files(self, folder):
        import os
        return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.bin')]

    def timer_callback(self):
        if self.file_index >= len(self.files):
            self.file_index = 0  # 循环播放
        file_path = self.files[self.file_index]
        points = self.read_bin_file(file_path)
        pc2_msg = self.create_pointcloud2(points)
        self.publisher_.publish(pc2_msg)
        self.get_logger().info(f'Publishing {file_path}')
        self.file_index += 1

    def read_bin_file(self, filename):
        points = np.fromfile(filename, dtype=np.float32).reshape(-1, 4)
        return points[:, :3]  # 只取xyz，丢掉反射强度

    def create_pointcloud2(self, points):
        msg = PointCloud2()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'velodyne'  # 根据你的TF调整

        msg.height = 1
        msg.width = points.shape[0]

        msg.fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
        ]

        msg.is_bigendian = False
        msg.point_step = 12  # 3*4 bytes
        msg.row_step = msg.point_step * points.shape[0]
        msg.is_dense = True
        msg.data = points.astype(np.float32).tobytes()
        return msg

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

