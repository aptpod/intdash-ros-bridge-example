ARG ROS1_DISTRO="not-set"
FROM ros:${ROS1_DISTRO}-ros-base
ARG ROS1_DISTRO

RUN if [ "$ROS1_DISTRO" = "melodic" ]; then \
        apt-get update && apt-get install -y \
        python-rosinstall \
        python-rosinstall-generator \
        python-wstool \
        build-essential \
        libopencv-dev \
        python-opencv \
        ros-${ROS1_DISTRO}-cv-bridge; \
    elif [ "$ROS1_DISTRO" = "noetic" ]; then \
        apt-get update && apt-get install -y \
        python3-rosinstall \
        python3-rosinstall-generator \
        python3-wstool \
        build-essential \
        libopencv-dev \
        python3-opencv \
        ros-${ROS1_DISTRO}-cv-bridge \
        python-is-python3; \
    else \
        echo "Unsupported ROS1_DISTRO: $ROS1_DISTRO" && exit 1; \
    fi

WORKDIR /root/catkin_ws

RUN /bin/bash -c 'mkdir -p /root/catkin_ws/src && \
    cd /root/catkin_ws && \
    /bin/bash -c ". /opt/ros/${ROS1_DISTRO}/setup.bash; catkin_make"'

COPY ./src /root/catkin_ws/src

RUN /bin/bash -c '. /opt/ros/${ROS1_DISTRO}/setup.bash; cd /root/catkin_ws; catkin_make'

#ENV ROS_PACKAGE_PATH="/root/catkin_ws/src:$ROS_PACKAGE_PATH"
