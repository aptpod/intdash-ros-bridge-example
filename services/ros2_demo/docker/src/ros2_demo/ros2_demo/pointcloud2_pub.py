import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2
from sensor_msgs.msg import Joy

class CubePublisher(Node):
    def __init__(self):
        super().__init__('cube_publisher')
        self.last_joy_msg = None
        self.publisher_ = self.create_publisher(PointCloud2, 'cube_points', 10)
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10)
        self.subscription
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.angle = 0.0
        self.cube_center = np.array([0.0, 0.0, 0.0])
        self.get_logger().info('cube_publisher node started')

    def joy_callback(self, msg):
        self.last_joy_msg = msg

    def get_latest_move(self):
        if self.last_joy_msg == None:
            return (0,0)
        x = self.last_joy_msg.axes[0] * -0.1
        y = self.last_joy_msg.axes[1] *  0.1
        self.last_joy_msg = None
        return (x,y)

    def create_rotating_cube_points(self):
        mx, my = self.get_latest_move()
        self.cube_center[0] += mx
        self.cube_center[1] += my

        x_values = np.linspace(-0.5, 0.5, 10) + self.cube_center[0]
        y_values = np.linspace(-0.5, 0.5, 10) + self.cube_center[1]
        z_values = np.linspace(-0.5, 0.5, 10)
        points = np.array(np.meshgrid(x_values, y_values, z_values)).T.reshape(-1, 3)

        theta = np.radians(self.angle)
        c, s = np.cos(theta), np.sin(theta)
        Rz = np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)))
        points = points.dot(Rz)

        return points.tolist()

    def timer_callback(self):
        points = self.create_rotating_cube_points()
        cloud = PointCloud2()
        cloud.header.stamp = self.get_clock().now().to_msg()
        cloud.header.frame_id = "cube_frame"

        cloud = PointCloud2()
        cloud.height = 1
        cloud.width = len(points)
        cloud.fields = [
            pc2.PointField(name='x', offset=0, datatype=pc2.PointField.FLOAT32, count=1),
            pc2.PointField(name='y', offset=4, datatype=pc2.PointField.FLOAT32, count=1),
            pc2.PointField(name='z', offset=8, datatype=pc2.PointField.FLOAT32, count=1)
        ]
        cloud.is_bigendian = False
        cloud.point_step = 12
        cloud.row_step = cloud.point_step * cloud.width
        cloud.is_dense = True
        cloud.data = np.asarray(points, np.float32).tobytes()

        self.publisher_.publish(cloud)

def main(args=None):
    rclpy.init(args=args)
    cube_publisher = CubePublisher()
    rclpy.spin(cube_publisher)
    cube_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
