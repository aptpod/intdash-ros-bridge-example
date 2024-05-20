#!/bin/bash

source /opt/ros/$ROS1_DISTRO/setup.bash
source /opt/epsis_ws/install/setup.bash

echo "start ROS core"
roscore &
roscore_pid=$!
sleep 2

echo "start Integration Service"
stdbuf -o0 integration-service /opt/vm2m/etc/config.yml &
is_pid=$!

cleanup() {
  echo "SIGTERM received, sending SIGTERM to subprocesses..."
  kill -TERM $is_pid
  kill -TERM $roscore_pid
  exit 0
}

trap 'cleanup' TERM

wait $is_pid
wait $roscore_pid
