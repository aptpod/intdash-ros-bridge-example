ARG ROS2_DISTRO="not-set"
FROM ros:${ROS2_DISTRO}
ARG ROS2_DISTRO

RUN apt-get update && apt-get install -y \
    ros-${ROS2_DISTRO}-sensor-msgs ros-${ROS2_DISTRO}-sensor-msgs-py \
    libopencv-dev python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install opencv-python

WORKDIR /ros_demo_ws

COPY src /ros_demo_ws/src

RUN /bin/bash -c 'source /opt/ros/${ROS2_DISTRO}/setup.bash && colcon build && rm -rf log && rm -rf build'
