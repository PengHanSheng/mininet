#!/usr/bin/python

"Sample file for SUMO"

import os

from mininet.net import Mininet
from mininet.node import Controller, UserAP
from mininet.cli import CLI
from mininet.log import setLogLevel

def topology():
    "Create a network."
    net = Mininet(controller=None, accessPoint=UserAP,
                  enable_wmediumd=True, enable_interference=True)
    
    print "*** Creating nodes"
    cars = []
    stas = []
    for x in range(0, 10):
        cars.append(x)
        stas.append(x)
    for x in range(0, 10):
        cars[x] = net.addCar('car%s' % (x),
                             wlans=1, ip='10.0.0.%s/8' % (x + 1))
    
    ap1 = net.addAccessPoint('ap1', ssid='vanet-ssid',
                            mode='g', channel='1', position='1127.02,513.27,0', range='40')
    ap2 = net.addAccessPoint('ap2', ssid='vanet-ssid',
                            mode='g', channel='6', position='1024.82,469.75,0', range='40')
    ap3 = net.addAccessPoint('ap3', ssid='vanet-ssid',
                            mode='g', channel='11', position='914.42,299.22,0', range='40')
    ap4 = net.addAccessPoint('ap4', ssid='vanet-ssid',
                            mode='g', channel='1', position='1165.62,345.92,0', range='40')
    ap5 = net.addAccessPoint('ap5', ssid='vanet-ssid',
                            mode='g', channel='6', position='1159.62,151.61,0', range='40')
    ap6 = net.addAccessPoint('ap6', ssid='vanet-ssid',
                            mode='g', channel='11', position='1363.68,337.40,0', range='40')


    c1 = net.addController('c1', controller=Controller, ip='127.0.0.1',
                           port=6633)

    h1 = net.addHost('h1', mac='00:00:00:11:00:01', ip='10.0.0.1/8')

    s1 = net.addSwitch('s1', mac='00:00:00:00:00:01')
    s2 = net.addSwitch('s2', mac='00:00:00:00:00:02')
    s3 = net.addSwitch('s3', mac='00:00:00:00:00:03')
    s4 = net.addSwitch('s4', mac='00:00:00:00:00:04')
    lte = net.addSwitch('s10', mac='00:00:00:00:00:10')

    print "*** Setting bgscan"
    net.setBgscan(signal=-45, s_inverval=5, l_interval=10)

    print "*** Configuring Propagation Model"
    net.propagationModel(model="logDistance", exp=2)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Add Wifi links"
    net.addLink(s1, h1)
    net.addLink(s2,s1, bw=10, delay='5ms', loss=2, use_htb=True)
    net.addLink(s3,s1, bw=10, delay='10ms', loss=1, use_htb=True)
    net.addLink(s4,s1, bw=10, delay='10ms', loss=1, use_htb=True)

    net.addLink(ap1, s2)
    net.addLink(ap2, s3)
    net.addLink(ap3, s4)

    print "*** Add LTE links"
    for x in range(0, 10):
        net.addLink(lte,'car%s' % (x))
    net.addLink(lte,s1,bw=10, delay='50ms', loss=1, use_htb=True)

    print "*** Starting SUMO"
    net.useExternalProgram('sumo-gui', config_file='ucla.sumocfg')

    print "*** Starting network"
    net.build()
'''
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])
    ap5.start([c1])
    ap6.start([c1])
'''
    i = 201
    for sw in net.carsSW:
        sw.start([c1])
        os.system('ip addr add 10.0.0.%s dev %s' % (i, sw))
        i += 1

    i = 1
    j = 2
    for car in cars:
        car.setIP('192.168.0.%s/24' % i, intf='%s-wlan0' % car)
        car.setIP('192.168.1.%s/24' % i, intf='%s-eth1' % car)
        car.cmd('ip route add 10.0.0.0/8 via 192.168.1.%s' % j)
        i += 2
        j += 2

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


if __name__ == '__main__':
    setLogLevel('info')
    topology()
