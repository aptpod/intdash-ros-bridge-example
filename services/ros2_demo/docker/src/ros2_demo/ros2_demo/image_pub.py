import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage
import time

class CompressedImagePublisher(Node):
    def __init__(self):
        super().__init__('compressed_image_publisher')
        self.publisher_ = self.create_publisher(CompressedImage, 'compressed_image', 10)
        self.timer = self.create_timer(0.2, self.timer_callback)
        self.blue = 0 
        self.get_logger().info('compressed_image_publisher node started')

    def generate_color_bar_image(self, width=400, height=200):
        image = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(width):
            r = int((i / float(width)) * 255.0)
            g = 255 - int((i / float(width)) * 255.0)
            b = self.blue % 255
            image[:, i, :] = [b, g, r]
        self.blue += 10 
        return image

    def timer_callback(self):
        image = self.generate_color_bar_image(width=400, height=200)

        result, encoded_image = cv2.imencode('.jpg', image)
        if not result:
            raise RuntimeError("Could not encode image!")

        msg = CompressedImage()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.format = "jpeg"
        msg.data = np.array(encoded_image).tobytes()

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CompressedImagePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
