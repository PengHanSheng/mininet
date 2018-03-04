#!/usr/bin/python

'Simple idea around Vehicular Ad Hoc Networks - VANETs'

import os
import random
from subprocess import call, check_call, check_output
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.node import OVSKernelAP
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.log import setLogLevel
import sys, time
flush=sys.stdout.flush
import os.path, string

def topology():

    print "Create a network."
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSKernelAP)

    print "*** Creating nodes"
    cars = []
    nodes=[]
    print"***Creating nodes"
    h1 = net.addHost('h1', mac='00:00:00:11:00:01', ip='10.0.0.1/8')
    nodes.append(h1)
    s1 = net.addSwitch('s1', mac='00:00:00:11:00:02')
    nodes.append(s1)

    for x in range(0, 5):
        cars.append(x)
    for x in range(0, 5):
        min_ = random.randint(1, 4)
        max_ = random.randint(11, 30)
        cars[x] = net.addCar('car%s' % (x + 1), wlans=1,
                             ip='10.0.0.%s/8'% (x + 1), min_speed=min_,
                             max_speed=max_, range=100)
        #nodes.append(car[x])

    rsu11 = net.addAccessPoint('RSU11', ssid='RSU11', mode='g',
                               channel='1')
    rsu12 = net.addAccessPoint('RSU12', ssid='RSU12', mode='g',
                               channel='6')
    rsu13 = net.addAccessPoint('RSU13', ssid='RSU13', mode='g',
                               channel='11')

    c1 = net.addController('c1', controller=Controller)


    print "*** Configuring Propagation Model"
    net.propagationModel(model="logDistance", exp=4.5)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Associating and Creating links"
    net.addLink(s1, h1)

    net.addLink(rsu11, s1)
    net.addLink(rsu12, s1)
    net.addLink(rsu13, s1)

    for x in range(0, 5):
        net.addLink('car%s' % (x + 1), rsu11)
 
    net.plotGraph(max_x=500, max_y=500)

    net.roads(10)

    net.startMobility(time=20)

    print "*** Starting network"
    net.build()
    c1.start()
    rsu11.start([c1])
    rsu12.start([c1])
    rsu13.start([c1])
    #rsu14.start([c1])

    print('*** set flow tables ***\n')
    #call(["sudo", "bash","fa_ft.sh"])

    i = 201
    for sw in net.carsSW:
        sw.start([c1])
        os.system('ip addr add 10.0.0.%s dev %s' % (i, sw))
        i += 1

    i = 1
    j = 2
    k = 1
    for car in cars:
        car.setIP('192.168.0.%s/24' % k, intf='%s-wlan0' % car)
        car.setIP('192.168.1.%s/24' % i, intf='%s-eth1' % car)
        car.cmd('ip route add 10.0.0.0/8 via 192.168.1.%s' % j)
        i += 2
        j += 2
        k += 1

    i = 1
    j = 2
    for carsta in net.carsSTA:
        carsta.setIP('10.0.0.%s/24' % i, intf='%s-mp0' % carsta)
        carsta.setIP('192.168.1.%s/24' % j, intf='%s-eth2' % carsta)
        #May be confuse, but it allows ping to the name instead of ip addr
        carsta.setIP('10.0.0.%s/24' % i, intf='%s-wlan0' % carsta)
        carsta.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
        i += 1
        j += 2

    for carsta1 in net.carsSTA:
        i = 1
        j = 1
        for carsta2 in net.carsSTA:
            if carsta1 != carsta2:
                carsta1.cmd('route add -host 192.168.1.%s gw 10.0.0.%s' % (j, i))
            i += 1
            j += 2



    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()

def ITGTest(srcNo, dstNo, nodes, bw, sTime):
    src = nodes[srcNo]
    dst = nodes[dstNo]
    print("Sending message from ",src.name,"<->",dst.name,"...",'\n')
    src.cmdPrint("cd ~/D-ITG-2.8.1-r1023/bin")
    src.cmdPrint("./ITGSend -T TCP  -a 10.0.0.50"+" -c 1000 -C "+str(bw)+" -t "+str(sTime)+" -l sender"+str(srcNo)+".log -x receiver"+str(srcNo)+"ss"+str(dstNo)+".log &")

if __name__ == '__main__':
    setLogLevel('info')
    topology()
