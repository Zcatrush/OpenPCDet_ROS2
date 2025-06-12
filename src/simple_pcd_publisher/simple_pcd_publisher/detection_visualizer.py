import rclpy
from rclpy.node import Node
from vision_msgs.msg import Detection3DArray
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point

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
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            marker.pose = box.center
            marker.scale = box.size
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 0.5
            marker.lifetime.sec = 1
            marker_array.markers.append(marker)
        self.publisher.publish(marker_array)
def main(args=None):
    rclpy.init(args=args)
    node = DetectionVisualizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

