ARG ROS_DISTRO="noetic"
ARG BASE_IMAGE="public.ecr.aws/aptpod/intdash-ros-bridge"
ARG IMAGE_ARCH="amd64"
ARG VERSION=""

FROM $BASE_IMAGE:$ROS_DISTRO-$VERSION-slim-$IMAGE_ARCH AS builder

ARG VERSION
ARG MIX_ROS1_PACKAGES=""
ARG MIX_ROS2_PACKAGES=""

SHELL ["/bin/bash", "-c"]

# Copy source directory for custom messages
ADD msg_src/ /opt/epsis_ws/src/

# Install custom messages from packages
RUN apt-get update && apt-get -y install \
    ros-$ROS_DISTRO-roscpp-tutorials && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Build ROS2 custom messages
RUN /ros_entrypoint.sh \
    colcon build --packages-select $MIX_ROS1_PACKAGES \
                --cmake-args -DCMAKE_BUILD_TYPE=Release

# Run mix generator
RUN /ros_entrypoint.sh \
    colcon build --packages-select is-ros1-mix-generator \
                --cmake-args -DMIX_ROS1_PACKAGES="$MIX_ROS1_PACKAGES" \
                            -DMIX_ROS2_PACKAGES="$MIX_ROS2_PACKAGES" \
                            -DCMAKE_BUILD_TYPE=Release && \
    rm -rf /opt/epsis_ws/build /opt/epsis_ws/log /opt/epsis_ws/src

# Release stage
FROM ros:$ROS_DISTRO

ARG ROS_DISTRO

# Copy binary from builder
COPY --from=builder /opt/epsis_ws/install /opt/epsis_ws/install
RUN sed -i '$isource "/opt/epsis_ws/install/setup.bash"' /ros_entrypoint.sh

# Pre install for utils
RUN apt-get update && apt-get -y install \
    software-properties-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# GCC repository
RUN add-apt-repository ppa:ubuntu-toolchain-r/test

# Dependendies for eProsima Integration-Service
RUN apt-get update && apt-get -y install \
    gcc-9 g++-9 \
    libyaml-cpp-dev \
    libboost-program-options-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install custom messages from packages
RUN apt-get update && apt-get -y install \
    ros-$ROS_DISTRO-roscpp-tutorials && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "$VERSION" > /etc/intdash_ros_bridge_version

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
