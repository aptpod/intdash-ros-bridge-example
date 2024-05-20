#!/bin/bash

check_roscore() {
    rostopic list > /dev/null 2>&1
}

until check_roscore; do
    echo "Waiting for roscore to start..."
    sleep 1
done

source /opt/ros/$ROS1_DISTRO/setup.bash
source /root/catkin_ws/devel/setup.bash
echo "start ROS demo container"
exec stdbuf -o0 roslaunch ros1_demo ros1_demo.launch
