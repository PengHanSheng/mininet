#!/usr/bin/python

"""MPTCP Demo"""
from subprocess import call, check_call, check_output
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, Controller
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel


def topology():

    """
          *ap2--h4.      .s7.
         *         .    .    .
    sta1*           s6--     s9--h10
        *          .    .    .
         *        .      .  .
          *ap3--h5        s8
    """

    call(["sudo", "sysctl","-w","net.mptcp.mptcp_enabled=1"])
    call(["sudo", "modprobe","mptcp_coupled"])
    call(["sudo", "sysctl","-w", "net.ipv4.tcp_congestion_control=lia"])
    "Create a network."
    net = Mininet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )

    print "*** Creating nodes"
    sta1 = net.addStation(
        'sta1', wlans=1,   position='55,15,0' )

    '''
    ap2 = net.addAccessPoint(
        'ap2', mac='00:00:00:00:00:02',
         ssid= 'ssid_ap2', mode= 'g',
        channel= '1', position='50,10,0', range=40)
    '''
    ap3 = net.addAccessPoint(
        'ap3', mac='00:00:00:00:00:03',
         ssid= 'ssid_ap3', mode= 'g',
        channel= '6', position='70,50,0' , range=40)


    s6 = net.addSwitch( 's6', mac='00:00:00:00:00:06' )
    #s7 = net.addSwitch( 's7', mac='00:00:00:00:00:07', protocols='OpenFlow10' )
    #s8 = net.addSwitch( 's8', mac='00:00:00:00:00:08', protocols='OpenFlow10' )
    #s9 = net.addSwitch( 's9', mac='00:00:00:00:00:09', protocols='OpenFlow10' )
    h10 = net.addHost( 'h10', mac='00:00:00:00:00:10' )
    c11 = net.addController('c11', controller=Controller)
    #c11 = net.addController( 'c11', controller=RemoteController, ip='127.0.0.1' )
    net.propagationModel(model='logDistance', exp=4)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()
    net.plotGraph(max_x=120,max_y=120)

    net.addLink( ap3, sta1)
    #net.addLink(sta1, ap3)
    #net.addLink(sta1, s7)
    net.addLink(ap3, s6, bw=1000)
    #net.addLink(ap3, s6, bw=1000)

    net.addLink(s6,h10,bw=1000)
    '''
    net.addLink(ap2, h4, bw=1000)
    net.addLink(ap3, h5, bw=1000)
    net.addLink(s6, h4, bw=1000)
    net.addLink(s6, h5, bw=1000)
    net.addLink(s6, s7, bw=1000)
    net.addLink(s6, s8, bw=1000)
    net.addLink(s7, s9, bw=1000)
    net.addLink(s8, s9, bw=1000)
    net.addLink(s9, h10, bw=1000)
    '''


    print "*** Starting network"
    net.start()

    print "*** Associating and Creating links"
    '''
    sta1.cmd('ifconfig sta1-wlan0 10.0.1.0/32')
    sta1.cmd('ifconfig sta1-wlan1 10.0.1.1/32')

    #sta1.cmd('ip route add default 10.0.0.254/8 via sta1-wlan0')
    #sta1.cmd('ip route add default 192.168.0.254/24 via sta1-wlan1')

    sta1.cmd('ip rule add from 10.0.1.0 table 1')
    sta1.cmd('ip rule add from 10.0.1.1 table 2')

    sta1.cmd('ip route add 10.0.1.0/32 dev sta1-wlan0 scope link table 1')
    sta1.cmd('ip route add default via 10.0.1.0 dev sta1-wlan0 table 1')

    sta1.cmd('ip route add 10.0.1.1/32 dev sta1-wlan1 scope link table 2')
    sta1.cmd('ip route add default via 10.0.1.1 dev sta1-wlan1 table 2')

    sta1.cmd('ip route add default scope global nexthop via 10.0.1.0 dev sta1-wlan0')
    '''

    '''
    h10.cmd('ip route add 10.0.0.0/8 via 192.168.1.1')
    h10.cmd('ip route add 192.168.0.0/24 via 192.168.1.2')

    h4.cmd('sysctl -w net.ipv4.ip_forward=1')
    h5.cmd('sysctl -w net.ipv4.ip_forward=1')
    '''

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
