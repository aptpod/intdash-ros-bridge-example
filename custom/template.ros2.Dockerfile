ARG ROS_DISTRO="humble"
ARG BASE_IMAGE="public.ecr.aws/aptpod/intdash-ros-bridge"
ARG IMAGE_ARCH="amd64"
ARG VERSION=""

FROM $BASE_IMAGE:$ROS_DISTRO-$VERSION-slim-$IMAGE_ARCH AS builder

ARG VERSION
ARG MIX_ROS1_PACKAGES=""
ARG MIX_ROS2_PACKAGES=""
ARG MIX_ACTION_PACKAGES=""
ENV MIX_PROXY_PACKAGES=""

SHELL ["/bin/bash", "-c"]

# Copy source directory for custom messages
ADD msg_src/ /opt/epsis_ws/src/

# Install custom messages from packages
RUN apt-get update && apt-get -y install \
    ros-$ROS_DISTRO-example-interfaces && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Build ROS2 custom messages
RUN /ros_entrypoint.sh \
    colcon build --packages-select $MIX_ROS2_PACKAGES $MIX_ACTION_PACKAGES \
                --cmake-args -DCMAKE_BUILD_TYPE=Release

# Find action packages and build Action Proxy
RUN /ros_entrypoint.sh \
    /opt/epsis_ws/src/action_proxy/build.sh

# Rebuild ROS2-SH
RUN /ros_entrypoint.sh \
    colcon build --packages-select is-ros2 \
                --cmake-args -DMIX_ROS1_PACKAGES="" \
                            -DMIX_ROS2_PACKAGES="" \
                            -DCMAKE_BUILD_TYPE=Release

# Run mix generator
RUN if [ -n "${MIX_ACTION_PACKAGES}" ]; then \
        MIX_PROXY_PACKAGES=""; \
        for pkg in $MIX_ACTION_PACKAGES; do \
            MIX_PROXY_PACKAGES="${MIX_PROXY_PACKAGES} ${pkg}_proxy_types"; \
        done; \
        echo "Modified MIX_ACTION_PACKAGES: $MIX_PROXY_PACKAGES"; \
    else \
        echo "MIX_ACTION_PACKAGES is empty"; \
    fi && \
    /ros_entrypoint.sh \
    colcon build --packages-select $MIX_PROXY_PACKAGES \
                --cmake-args -DCMAKE_BUILD_TYPE=Release && \
    /ros_entrypoint.sh \
    colcon build --packages-select is-ros2-mix-generator \
                --cmake-args -DMIX_ROS1_PACKAGES="$MIX_ROS1_PACKAGES" \
                            -DMIX_ROS2_PACKAGES="$MIX_ROS2_PACKAGES $MIX_PROXY_PACKAGES" \
                            -DCMAKE_BUILD_TYPE=Release && \
    rm -rf /opt/epsis_ws/build /opt/epsis_ws/log /opt/epsis_ws/src

# Release stage
FROM ros:$ROS_DISTRO

ARG ROS_DISTRO

# Copy binary from builder
COPY --from=builder /opt/epsis_ws/install /opt/epsis_ws/install
RUN sed -i '$isource "/opt/epsis_ws/install/setup.bash"' /ros_entrypoint.sh

# Dependendies for eProsima Integration-Service
RUN apt-get update && apt-get -y install \
    libyaml-cpp-dev \
    libboost-program-options-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install custom messages from packages
RUN apt-get update && apt-get -y install \
    ros-$ROS_DISTRO-example-interfaces && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /etc/intdash_ros_bridge /etc/intdash_ros_bridge

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
