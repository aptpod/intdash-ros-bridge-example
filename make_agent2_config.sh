#!/bin/bash

set -e
if [ $# -eq 0 ]; then
  echo "making config for intdash Edge Agent2"
  set -a
  source .env
  set +a 
  docker run --rm -v $(pwd)/services/agent2:/tmp/output -v $(pwd)/make_agent2_config.sh:/tmp/make_config.sh public.ecr.aws/aptpod/intdash-edge-agent2:$AGENT2_VERSION /tmp/make_config.sh in_docker
  echo "done"
  exit 0
fi

sudo /etc/init.d/intdash-agentd start

#upstream
intdash-agentctl config connection --modify '
    server_url: https://xxxxxx.intdash.jp
    project_uuid: 00000000-0000-0000-0000-000000000000
    edge_uuid: 00000001-0000-0000-0000-000000000000
    client_secret: x000000000000000000000000000000000000000000000000000000000000001
  '

intdash-agentctl config upstream --create '
    id: up-ros-data
    flush_policy: immediately
    qos: partial
    recover: false
  '
intdash-agentctl config device-connector upstream --create '
    id: dc-up-ros-data
    data_name_prefix: "v1/10/"
    dest_ids:
      - up-ros-data
    format: iscp-v2-compat
    ipc:
      type: fifo
      path: /var/run/intdash/up-ros-data.fifo
  '

intdash-agentctl config device-connector upstream --create '
    id: dc-up-ros-video
    data_name_prefix: "v1/200/"
    dest_ids:
      - up-ros-data
    format: logger-msg
    ipc:
      type: fifo
      path: /var/run/intdash/up-ros-video.fifo
  '

#downstream
intdash-agentctl config device-connector downstream --create '
    id: dc-down-ros-data
    enabled: true
    format: iscp-v2-compat
    ipc:
      type: fifo
      path: /var/run/intdash/down-ros-data.fifo
    '

intdash-agentctl config downstream --create "
    id: up-ros-data
    enabled: true
    dest_ids:
      - dc-down-ros-data
    filters:
    - src_edge_uuid: 00000002-0000-0000-0000-000000000000
      data_filters:
      - type: '#'
        name: '#'
    "

sleep 1
intdash-agentd config show | sudo tee /tmp/output/agent2_config.yml
