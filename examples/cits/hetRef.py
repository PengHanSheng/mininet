#!/usr/bin/python
from subprocess import call, check_call, check_output
from mininet.fdm import FDM
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import sys, time
flush=sys.stdout.flush
import os.path, string

def topology():
    call(["sudo", "sysctl","-w","net.mptcp.mptcp_enabled=1"])
    call(["sudo", "modprobe","mptcp_coupled"])
    call(["sudo", "sysctl","-w", "net.ipv4.tcp_congestion_control=lia"])
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSKernelAP)
    nodes=[]
    print"***Creating nodes"
    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
    nodes.append(h1)
    s1 = net.addSwitch('s1', mac='00:00:00:00:00:02')

    #lte = net.addSwitch('s2')
    lte = net.addSwitch('s2', mac='00:00:00:00:00:04')

    sta1 = net.addStation('sta1', mac='00:00:00:00:00:03', wlans=1,
                         position='1,50,0')
    nodes.append(sta1)
    s3=net.addSwitch('s3')
    s4=net.addSwitch('s4')
    s5=net.addSwitch('s5')
    s6=net.addSwitch('s6')

    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1',
                             position='30,50,0', range='40')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='1',
                            position='90,50,0', range='40')
    ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='g', channel='1',
                            position='130,50,0', range='40')
    c1 = net.addController('c1', controller=Controller)

    print "***Configuring propagation model"
    net.propagationModel(model="logDistance", exp=4)

    print "***Configuring wifi nodes"
    net.configureWifiNodes()

    print "***Associating and Creating links"
    net.addLink(h1, s1)

    #net.addLink(ap1,s1)
    #net.addLink(ap2,s1)
    #net.addLink(ap3,s1)

    net.addLink(ap1, s3)
    net.addLink(ap2, s4)
    net.addLink(ap3, s5)

    net.addLink(s3,s1, bw=10, delay='5ms', loss=2, use_htb=True)
    net.addLink(s4,s1, bw=10, delay='10ms', loss=1, use_htb=True)
    net.addLink(s5,s1, bw=10, delay='10ms', loss=1, use_htb=True)
    #net.addLink(s6,s1 , bw=20, delay='50ms', loss=0, use_htb=True)

    net.addLink(lte,s1 , bw=20, delay='50ms', loss=0, use_htb=True)

    #net.addLink(lte,sta1)
    #net.addLink(ap1,sta1)

    net.plotGraph(max_x=200, max_y=200)

    net.startMobility(time=0, AC='ssf')
    net.mobility(sta1, 'start', time=0, position='1,50,0')
    net.mobility(sta1, 'stop', time=100, position='13,50,0')
    net.stopMobility(time=1000)

    print"***Starting network"
    net.start()

    c1.start()
    s1.start([c1])
    s3.start([c1])
    s4.start([c1])
    s5.start([c1])
    lte.start([c1])
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])

    print"***Running CLI"
    CLI(net)

    time.sleep(1)
    print("starting D-ITG servers...\n")
    h1.cmdPrint("/home/osboxes/DITG/bin/ITGRecv &")
    time.sleep(2)
    sta1.cmdPrint("/home/osboxes/DITG/bin/ITGSend -T TCP  -a 10.0.0.1"+" -c 1000 -C 2000 -t 10000 -l send.log -x recv.log")


    print("running simulaiton...\n")
    time.sleep(10)
    #time.sleep(sTime/2000)


    print"***Stopping network"
    net.stop()

def ITGTest(srcNo, dstNo, nodes, bw, sTime):
    src = nodes[srcNo]
    dst = nodes[dstNo]
    print("Sending message from ",src.name,"<->",dst.name,"...",'\n')
    src.cmdPrint("cd ~/DITG/bin")
    src.cmdPrint("./ITGSend -T TCP  -a 10.0.0.1"+" -c 1000 -C "+str(bw)+" -t "+str(sTime)+" -l sender"+str(srcNo)+".log -x receiver"+str(srcNo)+"ss"+str(dstNo)+".log &")


if __name__ == '__main__':
   setLogLevel('info')
   topology()
