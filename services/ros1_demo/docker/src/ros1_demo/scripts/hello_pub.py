#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('/hello', String, queue_size=10)
    rospy.init_node('hello_publisher', anonymous=True)
    rospy.loginfo("hello_publisher node started")
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        hello_str = "hello"
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass