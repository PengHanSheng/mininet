#!/bin/bash
#sudo ifconfig ap1-eth2 txqueuelen 100
sudo ovs-vsctl -- set Port ap1-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=100000000 queues:1=@q1 queues:2=@q2 queues:3=@q3 -- --id=@q1 create Queue other-config:min-rate=2500000 other-config:max-rate=2500000 -- --id=@q2 create Queue other-config:min-rate=4000000 other-config:max-rate=5000000 -- --id=@q3 create Queue other-config:min-rate=2500000 other-config:max-rate=2500000
#sudo ifconfig ap2-eth2 txqueuelen 100
sudo ovs-vsctl -- set Port ap2-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=100000000 queues:4=@q4 queues:5=@q5 --  --id=@q4 create Queue other-config:min-rate=3500000 other-config:max-rate=3500000 -- --id=@q5 create Queue other-config:min-rate=3500000 other-config:max-rate=3500000

#sudo ovs-vsctl -- set Port s2-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=100000000 queues:4=@q4 queues:5=@q5 --  --id=@q3 create Queue other-config:min-rate=5800000 other-config:max-rate=6000000 -- --id=@q4 create Queue other-config:min-rate=5800000 other-config:max-rate=6000000
sudo ovs-ofctl -O Openflow13 queue-stats ap2
sudo ovs-ofctl -O Openflow13 queue-stats ap1

sudo ovs-ofctl add-flow ap1 ip,nw_src=10.0.1.0/32,actions=set_queue:1,output:2
sudo ovs-ofctl add-flow ap1 ip,nw_src=10.0.3.0/32,actions=set_queue:3,output:2
sudo ovs-ofctl add-flow ap1 ip,nw_src=10.0.2.0/32,actions=set_queue:2,output:2
sudo ovs-ofctl add-flow ap1 in_port=2,actions=normal

sudo ovs-ofctl add-flow ap2 ip,nw_src=10.0.1.1/32,actions=set_queue:4,output:2
sudo ovs-ofctl add-flow ap2 ip,nw_src=10.0.3.1/32,actions=set_queue:5,output:2

sudo ovs-ofctl add-flow ap2 in_port=2,actions=normal
sudo ovs-ofctl add-flow ap3 in_port=1,actions=output:2
sudo ovs-ofctl add-flow ap3 in_port=2,actions=normal
sudo ovs-ofctl add-flow s2 ip,nw_src=10.0.1.1/32,actions=set_queue:4,output:2
sudo ovs-ofctl add-flow s2 ip,nw_src=10.0.3.1/32,actions=set_queue:5,output:2
sudo ovs-ofctl add-flow s2 in_port=2,actions=normal

sudo ovs-ofctl add-flow s1 in_port=2,actions=output:1
sudo ovs-ofctl add-flow s1 in_port=3,actions=output:1
sudo ovs-ofctl add-flow s1 in_port=4,actions=output:1
sudo ovs-ofctl add-flow s1 in_port=5,actions=output:1
sudo ovs-ofctl add-flow s1 in_port=1,actions=normal

sudo ovs-ofctl add-flow s3 in_port=2,actions=output:1
sudo ovs-ofctl add-flow s3 in_port=1,actions=normal
sudo ovs-ofctl add-flow s4 in_port=2,actions=output:1
sudo ovs-ofctl add-flow s4 in_port=1,actions=normal
sudo ovs-ofctl add-flow s5 in_port=2,actions=output:1
sudo ovs-ofctl add-flow s5 in_port=1,actions=normal
sudo ovs-ofctl add-flow s6 in_port=2,actions=output:1
sudo ovs-ofctl add-flow s6 in_port=1,actions=normal

sudo ovs-ofctl add-flow ap1 priority=100,actions=normal
sudo ovs-ofctl add-flow ap2 priority=100,actions=normal
sudo ovs-ofctl add-flow ap3 priority=100,actions=normal
sudo ovs-ofctl add-flow s1 priority=100,actions=normal
sudo ovs-ofctl add-flow s2 priority=100,actions=normal
sudo ovs-ofctl add-flow s3 priority=100,actions=normal
sudo ovs-ofctl add-flow s4 priority=100,actions=normal
sudo ovs-ofctl add-flow s5 priority=100,actions=normal
sudo ovs-ofctl add-flow s6 priority=100,actions=normal
