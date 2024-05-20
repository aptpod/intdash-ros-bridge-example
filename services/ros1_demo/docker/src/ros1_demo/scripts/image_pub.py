#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
import numpy as np

blue = 0

def generate_color_bar_image(width=400, height=200):
    global blue
    image = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(width):
        r = int((i / float(width)) * 255.0)
        g = 255 - int((i / float(width)) * 255.0)
        b = blue % 255
        image[:, i, :] = [b, g, r]
    blue = blue + 10
    return image

def talker():
    rospy.init_node('compressed_image_publisher', anonymous=True)
    rospy.loginfo("compressed_image_publisher node started")
    pub = rospy.Publisher('/compressed_image', CompressedImage, queue_size=10)
    rate = rospy.Rate(5)
    cnt = 0

    bridge = CvBridge()

    while not rospy.is_shutdown():
        cv_image = generate_color_bar_image()
        msg = bridge.cv2_to_compressed_imgmsg(cv_image, dst_format='jpeg')
        pub.publish(msg)
        rate.sleep()
        cnt = cnt + 1

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass