import rclpy
from rclpy.node import Node
from vision_msgs.msg import Detection3DArray
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point, Vector3

class DetectionVisualizer(Node):
    def __init__(self):
        super().__init__('detection_visualizer')
        self.subscription = self.create_subscription(
            Detection3DArray,
            '/cloud_detections',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(MarkerArray, '/detection_markers', 10)
        self.get_logger().info("Visualization node started, subscribing to /cloud_detections")

    def listener_callback(self, msg):
        marker_array = MarkerArray()
        for idx, detection in enumerate(msg.detections):
            box = detection.bbox
            marker = Marker()
            marker.header = msg.header
            marker.ns = "detection"
            marker.id = idx
            marker.type = Marker.LINE_LIST  # 使用 LINE_LIST 来绘制 3D 框
            marker.action = Marker.ADD

            # 确保正确访问 position.x, y, z
            if isinstance(box.center, Point):
                marker.pose.position = box.center
            elif isinstance(box.center, Vector3):
                marker.pose.position = Point(x=box.center.x, y=box.center.y, z=box.center.z)
            elif hasattr(box.center, 'position'):  # 如果 box.center 是 Pose 类型
                marker.pose.position = box.center.position  # 正确访问 position

            marker.pose.orientation.x = 0.0
            marker.pose.orientation.y = 0.0
            marker.pose.orientation.z = 0.0
            marker.pose.orientation.w = 1.0

            # 设置框的颜色为绿色
            marker.color.r = 0.0
            marker.color.g = 1.0
            marker.color.b = 0.0
            marker.color.a = 1.0  # 完全不透明

            # 设置框的线宽度
            marker.scale.x = 0.1  # 线的粗细，可以调整

            # 构建矩形框的 8 个顶点
            p1 = Point()
            p1.x = box.center.position.x - box.size.x / 2  # 左下前
            p1.y = box.center.position.y - box.size.y / 2
            p1.z = box.center.position.z - box.size.z / 2

            p2 = Point()
            p2.x = box.center.position.x + box.size.x / 2  # 右下前
            p2.y = box.center.position.y - box.size.y / 2
            p2.z = box.center.position.z - box.size.z / 2

            p3 = Point()
            p3.x = box.center.position.x + box.size.x / 2  # 右上前
            p3.y = box.center.position.y + box.size.y / 2
            p3.z = box.center.position.z - box.size.z / 2

            p4 = Point()
            p4.x = box.center.position.x - box.size.x / 2  # 左上前
            p4.y = box.center.position.y + box.size.y / 2
            p4.z = box.center.position.z - box.size.z / 2

            p5 = Point()
            p5.x = box.center.position.x - box.size.x / 2  # 左下后
            p5.y = box.center.position.y - box.size.y / 2
            p5.z = box.center.position.z + box.size.z / 2

            p6 = Point()
            p6.x = box.center.position.x + box.size.x / 2  # 右下后
            p6.y = box.center.position.y - box.size.y / 2
            p6.z = box.center.position.z + box.size.z / 2

            p7 = Point()
            p7.x = box.center.position.x + box.size.x / 2  # 右上后
            p7.y = box.center.position.y + box.size.y / 2
            p7.z = box.center.position.z + box.size.z / 2

            p8 = Point()
            p8.x = box.center.position.x - box.size.x / 2  # 左上后
            p8.y = box.center.position.y + box.size.y / 2
            p8.z = box.center.position.z + box.size.z / 2

            # 画 3D 框的边：每两个点连接一条线
            # 前面四个点
            marker.points.append(p1)
            marker.points.append(p2)
            marker.points.append(p2)
            marker.points.append(p3)
            marker.points.append(p3)
            marker.points.append(p4)
            marker.points.append(p4)
            marker.points.append(p1)

            # 后面四个点
            marker.points.append(p5)
            marker.points.append(p6)
            marker.points.append(p6)
            marker.points.append(p7)
            marker.points.append(p7)
            marker.points.append(p8)
            marker.points.append(p8)
            marker.points.append(p5)

            # 连接前后面的点
            marker.points.append(p1)
            marker.points.append(p5)
            marker.points.append(p2)
            marker.points.append(p6)
            marker.points.append(p3)
            marker.points.append(p7)
            marker.points.append(p4)
            marker.points.append(p8)

            # 设置生命周期为 1 秒
            marker.lifetime.sec = 1
            marker_array.markers.append(marker)

        self.publisher.publish(marker_array)
        self.get_logger().info(f"Published {len(marker_array.markers)} markers.")

def main(args=None):
    rclpy.init(args=args)
    node = DetectionVisualizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
