#!/bin/bash
sudo ovs-vsctl -- set Port ap1-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=100000000 queues:1=@q1 queues:2=@q2 --  --id=@q1 create Queue other-config:min-rate=1000000 other-config:max-rate=1000000 -- --id=@q2 create Queue other-config:min-rate=200000 other-config:max-rate=200000
sudo ovs-vsctl -- set Port s2-eth2 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=100000000 queues:3=@q3 --  --id=@q3 create Queue other-config:min-rate=1800000 other-config:max-rate=1800000
sudo ovs-ofctl -O Openflow13 queue-stats s2
sudo ovs-ofctl -O Openflow13 queue-stats ap1
