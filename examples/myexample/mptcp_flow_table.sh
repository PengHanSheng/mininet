#!/bin/bash

sudo ovs-ofctl add-flow ap2 in_port=1,actions=output:2
sudo ovs-ofctl add-flow ap2 in_port=2,actions=normal
sudo ovs-ofctl add-flow ap3 in_port=1,actions=output:2
sudo ovs-ofctl add-flow ap3 in_port=2,actions=normal
#sudo ovs-ofctl add-flow s7 in_port=1,actions=output:2
#sudo ovs-ofctl add-flow s7 in_port=2,actions=normal

sudo ovs-ofctl add-flow s6 in_port=1,actions=output:3
sudo ovs-ofctl add-flow s6 in_port=2,actions=output:3
sudo ovs-ofctl add-flow s6 in_port=3,actions=normal
sudo ovs-ofctl add-flow ap2 priority=100,actions=normal
sudo ovs-ofctl add-flow ap3 priority=100,actions=normal
sudo ovs-ofctl add-flow s6 priority=100,actions=normal
