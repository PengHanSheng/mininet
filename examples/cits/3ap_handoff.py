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
    net = Mininet(controller=None, link=TCLink, accessPoint=OVSKernelAP)
    nodes=[]
    print"***Creating nodes"
    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')

    s1 = net.addSwitch('s1', mac='00:00:00:00:00:02')
    s3=net.addSwitch('s3')
    s4=net.addSwitch('s4')
    s5=net.addSwitch('s5')
    s6=net.addSwitch('s6')
    lte = net.addSwitch('s2', mac='00:00:00:00:00:04')
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:03', wlans=1,
                         position='60,40,0')
    nodes.append(sta1)
    #sta3 = net.addStation('sta3',wlans=2, ip='10.0.3.0/8',position='60,60,0')
    #nodes.append(sta3)
    #sta2 = net.addStation('sta2', mac='00:00:00:00:00:04', ip='10.0.2.0/8',
    #                     position='20,50,0')
    #nodes.append(sta2)
    nodes.append(h1)
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1',
                             position='30,50,0', range='40')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='1',
                            position='90,50,0', range='40')
    ap3 = net.addAccessPoint('ap3', ssid='ap3-ssid', mode='g', channel='1',
                            position='130,50,0', range='40')
    #c1 = net.addController('c1', controller=Controller)

    print "***Configuring propagation model"
    net.propagationModel(model="logDistance", exp=4)

    print "***Configuring wifi nodes"
    net.configureWifiNodes()

    print "***Associating and Creating links"
    net.addLink(s1, h1)

    '''link for AP1'''
    net.addLink(s3,s1, bw=10, delay='5ms', loss=2, use_htb=True)
    net.addLink(s4,s1, bw=10, delay='10ms', loss=1, use_htb=True)
    net.addLink(s5,s1, bw=10, delay='10ms', loss=1, use_htb=True)
    '''link for LTE'''
    #net.addLink(s6,s1 , bw=20, delay='50ms', loss=0, use_htb=True)
    net.addLink(lte,sta1)
    # net.addLink(ap1,sta3)
    # net.addLink(ap2,sta1)
    # net.addLink(ap2,sta3)
    #net.addLink(lte,sta1)
    net.addLink(ap1, s3)
    net.addLink(ap2, s4)
    net.addLink(ap3, s5)

    net.addLink(lte,s1,bw=10, delay='50ms', loss=1, use_htb=True)
    #net.addLink(lte,s6)
    #net.addLink(lte,sta3)

    # net.addLink(ap3, s1, bw=1000)

    net.plotGraph(max_x=200, max_y=200)

    # net.startMobility(time=0, AC='ssf')
    # net.mobility(sta1, 'start', time=30, position='1,50,0')
    # net.mobility(sta1, 'stop', time=60, position='29,50,0')
    # net.mobility(sta2, 'start', time=30, position='30,40,0')
    # net.mobility(sta2, 'stop', time=60, position='30,60,0')
    # net.stopMobility(time=10000)

    # iperf -c 10.0.0.1 -t 80 -i 2
    net.startMobility(time=0, AC='ssf')
    net.mobility(sta1, 'start', time=0, position='1,50,0')
    net.mobility(sta1, 'stop', time=100, position='160,50,0')
    net.stopMobility(time=110)

    print"***Starting network"
    net.start()
    # s1.start([c1])
    # s3.start([c1])
    # s4.start([c1])
    # s5.start([c1])
    # lte.start([c1])
    # ap1.start([c1])
    # ap2.start([c1])
    # ap3.start([c1])

    sta1.cmd('ifconfig sta1-wlan0 10.0.1.0/32')
    sta1.cmd('ifconfig sta1-eth1 10.0.1.1/32')

    sta1.cmd('ip route add default 10.0.0.254/8 via sta1-wlan0')
    sta1.cmd('ip route add default 192.168.0.254/24 via sta1-eth1')

    sta1.cmd('ip rule add from 10.0.1.0 table 1')
    sta1.cmd('ip rule add from 10.0.1.1 table 2')

    sta1.cmd('ip route add 10.0.1.0/32 dev sta1-wlan0 scope link table 1')
    sta1.cmd('ip route add default via 10.0.1.0 dev sta1-wlan0 table 1')

    sta1.cmd('ip route add 10.0.1.1/32 dev sta1-eth1 scope link table 2')
    sta1.cmd('ip route add default via 10.0.1.1 dev sta1-eth1 table 2')

    sta1.cmd('ip route add default scope global nexthop via 10.0.1.1 dev sta1-eth1')

    # sta3.cmd('ifconfig sta3-wlan0 10.0.3.0/32')
    # sta3.cmd('ifconfig sta3-wlan1 10.0.3.1/32')
    #
    #
    # sta3.cmd('ip rule add from 10.0.3.0 table 1')
    # sta3.cmd('ip rule add from 10.0.3.1 table 2')
    #
    # sta3.cmd('ip route add 10.0.3.0/32 dev sta3-wlan0 scope link table 1')
    # sta3.cmd('ip route add default via 10.0.3.0 dev sta3-wlan0 table 1')
    #
    # sta3.cmd('ip route add 10.0.3.1/32 dev sta3-wlan1 scope link table 2')
    # sta3.cmd('ip route add default via 10.0.3.1 dev sta3-wlan1 table 2')
    #
    # sta3.cmd('ip route add default scope global nexthop via 10.0.3.0 dev sta3-wlan0')

    print('*** set flow tables ***\n')
    call(["sudo", "bash","3ap_ft.sh"])
    users=["sta1"]
    nets=["ap1","ap2","ap3","s2"]
    FDM(net,users,nets,{},{},{})
    #FDM(net,users,nets,{"sta1":1,"sta2":1,"sta3":1},{},{},0,100,5)

    print"***Running CLI"
    #CLI(net)

    time.sleep(1)
    print("starting D-ITG servers...\n")
    h1.cmdPrint("/home/osboxes/DITG/bin/ITGRecv &")
    h1.cmd('popd')
    folderName = 'pcap'
    if not os.path.exists(folderName):
        os.mkdir(folderName)
        user = os.getenv('SUDO_USER')
        os.system('sudo chown -R osboxes:osboxes '+folderName)
    h1.cmd('tcpdump -i h1-eth0 -w '+folderName+'/h1.pcap &')

    time.sleep(2)
    sta1.cmdPrint("/home/osboxes/DITG/bin/ITGSend -T TCP  -a 10.0.0.1"+" -c 1000 -C 2000 -t 100000 -l send.log -x recv.log &")
    sta1.cmd('popd')
    sta1.cmd('tcpdump -i sta1-eth1 -w '+folderName+'/sta1-eth1.pcap &')
    sta1.cmd('tcpdump -i sta1-wlan0 -w '+folderName+'/sta1-wlan0.pcap &')
    time.sleep(115)
    CLI(net)
    #
    # CLI(net)
    # for i in range(0,0):
    # # start D-ITG Servers
    #
    #     srv = h1
    #     print("starting D-ITG servers...\n")
    #     srv.cmdPrint("cd ~/D-ITG-2.8.1-r1023/bin")
    #     srv.cmdPrint("./ITGRecv &")
    #     srv.cmdPrint("PID=$!")
    #
    #     time.sleep(1)
    #
    #     # start D-ITG application
    #     # set simulation time
    #     sTime = 30000  # default 120,000ms
    #     #bwReq = [12,12,12,12,12]
    #     # bwReq = [10,10,8,6,6]
    #     # bwReq = [24,4,4,4,22]
    #     bwReq=[6,6, 4]
    #     num_host=4
    #     for i in range(0, num_host - 1):
    #         sender = i
    #         receiver = num_host - 1
    #         ITGTest(sender, receiver, nodes, bwReq[i]*125, sTime)
    #         time.sleep(0.2)
    #     print("running simulaiton...\n")
    #     print("please wait...\n")
    #
    #     time.sleep(sTime/2000)
    #     ap1.dpctl("del-flows")
    #     ap2.dpctl("del-flows")
    #     call(["sudo", "bash","3ap_ft2.sh"])
    #     time.sleep(sTime/2000+10)
    #     for i in [num_host-1]:
    #         srv=nodes[i]
    #         print("killing D-ITG servers...\n")
    #         srv.cmdPrint("kill $PID")
    #     # You need to change the path here
    #     call(["sudo", "python","analysis.py"])


    print"***Stopping network"
    #time.sleep(50)
    net.stop()

def ITGTest(srcNo, dstNo, nodes, bw, sTime):
    src = nodes[srcNo]
    dst = nodes[dstNo]
    print("Sending message from ",src.name,"<->",dst.name,"...",'\n')
    src.cmdPrint("cd ~/D-ITG-2.8.1-r1023/bin")
    src.cmdPrint("./ITGSend -T TCP  -a 10.0.0.1"+" -c 1000 -C "+str(bw)+" -t "+str(sTime)+" -l sender"+str(srcNo)+".log -x receiver"+str(srcNo)+"ss"+str(dstNo)+".log &")


if __name__ == '__main__':
   setLogLevel('info')
   topology()
