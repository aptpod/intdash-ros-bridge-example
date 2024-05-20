#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import struct
import numpy as np
from sensor_msgs.msg import PointCloud2, PointField, Joy
from sensor_msgs import point_cloud2

class CubePublisher():
    def __init__(self):
        self.point_cloud_pub = rospy.Publisher("/cube_points", PointCloud2, queue_size=10)

        self.last_joy_msg = None
        rospy.Subscriber("/joy", Joy, self.joy_callback)

    def run(self):
        try:
            self.publish_point_cloud(self.point_cloud_pub)
        except rospy.ROSInterruptException:
            pass

    def joy_callback(self, msg):
        self.last_joy_msg = msg

    def get_latest_move(self):
        if self.last_joy_msg == None:
            return (0,0)
        x = self.last_joy_msg.axes[0] * -0.1
        y = self.last_joy_msg.axes[1] *  0.1
        self.last_joy_msg = None
        return (x,y)

    def create_dense_cube_points(self, x, y, z, size, density, angle):
        half_size = size / 2.0
        points = []
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)

        for i in np.linspace(-half_size, half_size, density):
            for j in np.linspace(-half_size, half_size, density):
                for (dx, dy, dz) in [(i, j, half_size), (i, j, -half_size), (i, half_size, j), (i, -half_size, j), (half_size, i, j), (-half_size, i, j)]:
                    rotated_x = cos_angle * dx - sin_angle * dy
                    rotated_y = sin_angle * dx + cos_angle * dy
                    rotated_z = dz
                    points.append([x + rotated_x, y + rotated_y, z + rotated_z])
        
        return points    

    def publish_point_cloud(self, pub):
        rospy.init_node('cube_publisher', anonymous=True)
        rospy.loginfo('cube_publisher node started')
        rate = rospy.Rate(10)

        angle = 0
        x = 0
        y = 0
        while not rospy.is_shutdown():
            mx, my = self.get_latest_move()
            x += mx
            y += my
            points = self.create_dense_cube_points(x, y, 0, 1.0, 10, angle)            
            header = rospy.Header(frame_id="base_link", stamp=rospy.Time.now())
            fields = [PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
                    PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
                    PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1)]
            cloud = point_cloud2.create_cloud(header, fields, points)            
            pub.publish(cloud)
            rate.sleep()


def main(args=None):
    cube_publisher = CubePublisher()
    cube_publisher.run()

if __name__ == '__main__':
    main()
