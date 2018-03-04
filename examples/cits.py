#!/usr/bin/python

"Sample file for SUMO"

import os
'''
from mininet.net import Mininet
from mininet.node import Controller, UserAP
from mininet.cli import CLI
from mininet.log import setLogLevel
'''
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def topology():
    "Create a network."
    net = Mininet(controller=Controller, switch=OVSKernelSwitch,
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
    
    e1 = net.addAccessPoint('e1', ssid='vanet-ssid', mac='00:00:00:11:00:01',
                            mode='g', channel='1', passwd='123456789a',
                            encrypt='wpa2', position='1127.02,513.27,0')
    e2 = net.addAccessPoint('e2', ssid='vanet-ssid', mac='00:00:00:11:00:02',
                            mode='g', channel='6', passwd='123456789a',
                            encrypt='wpa2', position='1024.82,469.75,0')
    e3 = net.addAccessPoint('e3', ssid='vanet-ssid', mac='00:00:00:11:00:03',
                            mode='g', channel='11', passwd='123456789a',
                            encrypt='wpa2', position='914.42,299.22,0')
    e4 = net.addAccessPoint('e4', ssid='vanet-ssid', mac='00:00:00:11:00:04',
                            mode='g', channel='1', passwd='123456789a',
                            encrypt='wpa2', position='1165.62,345.92,0')
    e5 = net.addAccessPoint('e5', ssid='vanet-ssid', mac='00:00:00:11:00:05',
                            mode='g', channel='6', passwd='123456789a',
                            encrypt='wpa2', position='1159.62,151.61,0')
    e6 = net.addAccessPoint('e6', ssid='vanet-ssid', mac='00:00:00:11:00:06',
                            mode='g', channel='11', passwd='123456789a',
                            encrypt='wpa2', position='1363.68,337.40,0')


    c1 = net.addController('c1', controller=Controller, ip='127.0.0.1',
                           port=6633)

    print "*** Configuring Propagation Model"
    net.propagationModel(model="logDistance", exp=2)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** add links"
    net.addLink(e1, e2)
    net.addLink(e2, e3)
    net.addLink(e3, e4)
    net.addLink(e4, e5)
    net.addLink(e5, e6)

    print "*** Starting SUMO"
    net.useExternalProgram('sumo-gui', config_file='ucla.sumocfg')

    print "*** Starting network"
    net.build()
    c1.start()
    e1.start([c1])
    e2.start([c1])
    e3.start([c1])
    e4.start([c1])
    e5.start([c1])
    e6.start([c1])

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
