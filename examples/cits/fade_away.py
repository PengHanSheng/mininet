#!/usr/bin/python
from subprocess import call, check_call, check_output
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import sys, time
flush=sys.stdout.flush
import os.path, string

def topology():
    call(["sudo", "sysctl","-w","net.mptcp.mptcp_enabled=0"])
    call(["sudo", "modprobe","mptcp_coupled"])
    call(["sudo", "sysctl","-w", "net.ipv4.tcp_congestion_control=cubic"])
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSKernelAP)
    nodes=[]
    print"***Creating nodes"
    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
    nodes.append(h1)

    s1 = net.addSwitch('s1', mac='00:00:00:00:00:02')
    nodes.append(s1)
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:03')
    nodes.append(sta1)
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
    net.addLink(s1, h1)
    '''link for AP1'''

    net.addLink(ap1,s1)
    net.addLink(ap2,s1)
    net.addLink(ap3,s1)

    net.plotGraph(max_x=200, max_y=200)
    net.startMobility(time=0, AC='ssf')
    net.mobility(sta1, 'start', time=0, position='1,50,0')
    net.mobility(sta1, 'stop', time=100, position='160,50,0')
    net.stopMobility(time=10000)
    print"***Starting network"
    net.start()

    c1.start()
    s1.start([c1])
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    
    print('*** set flow tables ***\n')
    #call(["sudo", "bash","fa_ft.sh"])
    users=["sta1"]
    nets=["ap1","ap2","ap3"]
    #FDM(net,users,nets,{},{},{},0,100,5)
    print"***Running CLI"
    CLI(net)

    time.sleep(1)
    print("starting D-ITG servers...\n")
    h1.cmdPrint("/home/osboxes/DITG/bin/ITGRecv &")
    time.sleep(2)
    sta1.cmdPrint("/home/osboxes/DITG/bin/ITGSend -T UDP  -a 10.0.0.1"+" -c 100 -C 200 -t 10000 -l send.log -x recv.log")
    time.sleep(5)

    print"***Running CLI"
    #CLI(net)

    print"***Stopping network"
    time.sleep(1)
    net.stop()

def ITGTest(src, dst, bw, sTime):
    print("Sending message from ",src.name,"<->",dst.name,"...",'\n')
    dst.cmdPrint("ITGRecv &")
    src.cmdPrint("ITGSend -T TCP  -a 10.0.0.1"+" -c 1000 -C "+str(bw)+" -t "+str(sTime)+" -l "+str(src)+".log -x "+str(dst)+".log &")


if __name__ == '__main__':
   setLogLevel('info')
   topology()
