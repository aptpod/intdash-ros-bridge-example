#!/bin/bash

sudo cp /tmp/agent.yaml /var/lib/intdash/agent.yaml
sudo sed -i "s/- src_edge_uuid: 00000002-0000-0000-0000-000000000000/- src_edge_uuid: $AGENT_INTDASH_SRC_EDGE_UUID/" /var/lib/intdash/agent.yaml
sudo chown intdash: /var/lib/intdash/agent.yaml

# agentd must receive term signal.
exec intdash-agentd serve
