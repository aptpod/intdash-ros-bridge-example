import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class HelloPublisher(Node):
    def __init__(self):
        super().__init__('hello_publisher')
        self.publisher_ = self.create_publisher(String, 'hello', 10)
        timer_period = 1 
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info('hello_publisher node started')

    def timer_callback(self):
        msg = String()
        msg.data = 'hello'
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    hello_publisher = HelloPublisher()
    rclpy.spin(hello_publisher)
    hello_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
