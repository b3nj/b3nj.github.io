---
layout: post
title:  "Loadbalancing your servers with LVS using connmark"
date:   2009-11-28 21:00:00 +0200
categories: system
---
* This will become a table of contents (this text will be scrapped).
{:toc}

# Face the load

## Foreword

One time or another, you’ll be facing the problem that your webserver isn’t powerfull enough as it can’t handle all the incoming traffic.
You may at this moment consider using load balancing the charge between more than one server.

Here is what you’ll have to know about the Network topology overview related to this howto:

* **client ip address:** 192.168.0.10
* **lb ip address:** 192.168.0.107
* **server1 ip address:** 192.168.0.108
* **server2 ip address:** 192.168.0.109
* **ip address used for loadbalancing:** 192.168.0.50 

> [!NOTE] Note: in this tutorial, I use the ifconfig command to configure interfaces, and I really don’t recommend you to do so. ifconfig is really deprecated and buggy on RedHat based systems, I strongly suggest you to use the ip command instead.

## Installing necessary packages

`iptables` should already been installed on your system, but make sure of it.
Next thing you’ll need is `ipvsadm` on the load balancer :

```bash
yum install ipvsadm
=>	Loaded plugins: fastestmirror
	Loading mirror speeds from cached hostfile
	 ...
	Setting up Install Process
	Resolving Dependencies
	--> Running transaction check
	---> Package ipvsadm.i386 0:1.24-10 set to be updated
	--> Finished Dependency Resolution
	...
	Complete!
```

## Network configuration

Now you should add the ip dedicated for load balancing on servers.

As alias of `eth0` on the load balancer :

```bash
ifconfig eth0:0 192.168.0.50 netmask 255.255.255.0
ifconfig eth0:0
=>	eth0:0    Link encap:Ethernet  HWaddr 00:0C:29:5A:78:22
	          inet addr:192.168.0.50  Bcast:192.168.0.255  Mask:255.255.255.0
	          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
	          Interrupt:75 Base address:0x2000
```

And as alias of `lo:0` on server1 and server2 :

```bash
ifconfig lo:0 192.168.0.50 netmask 255.255.255.255
ifconfig lo:0
=>	lo:0      Link encap:Local Loopback
	          inet addr:192.168.0.50  Mask:255.255.255.255
	          UP LOOPBACK RUNNING  MTU:16436  Metric:1
ifconfig lo:0 192.168.0.50 netmask 255.255.255.255
ifconfig lo:0
=>	lo:0      Link encap:Local Loopback
	          inet addr:192.168.0.50  Mask:255.255.255.255
	          UP LOOPBACK RUNNING  MTU:16436  Metric:1
```

Yeah, this is not a permanent way to configure the interfaces, but that’s specific to your distribution, so, do it your way.

## Prevent ARP problems

Well, as you configured ip addresses on all servers, every one of them will start to claim “i’ve got the 192.168.0.50 address !!!” via arp packets. This can result on an ARP tempest if you did this on many servers, and most certainly you’ll not be able to use the IP.

There’s a way of preventing this from happening, by telling servers to ignore arp and do not announce when they change something.
Put this in `/etc/sysctl.conf` of *each* real server:

```ini
net.ipv4.conf.all.arp_ignore = 1
net.ipv4.conf.all.arp_announce = 2
````

Then, apply changes you made in the `sysctl.conf` file :

```bash 
sysctl -p
```

## Let packets go through the load balancer

You need to let packets go through your load balancer, so add this in your /etc/sysctl.conf file on the load balancing server :

```ini
net.ipv4.ip_forward = 1
```

Then, apply changes you made in the `sysctl.conf` file :

```bash
sysctl -p
```

## Marking packets that should be load-balanced

What we want is that packets directed to the port 80 of the load balancer ip address are being marked (like a stamp) so that ipvs can regognize them and handle them accordingly to ipvs rules.

```bash
iptables -t mangle -A PREROUTING -j CONNMARK --restore-mark
iptables -t mangle -N myrule
iptables -t mangle -A PREROUTING -d 192.168.0.50 -p tcp --dport 80 -j myrule
iptables -t mangle -A myrule -j MARK --set-mark 0x1
iptables -t mangle -A myrule -j CONNMARK --save-mark
```

## Setting up the ipvs rules

Now we just have to tell `ipvsadm` to route marked packets to server1 and server2 (which is meaned to be twice powerful as server1), using weight round robin load balancing. This means that servers with higher weight will receive more packets than servers with lighter weights.
Concretely, telling that server2 has a weight of 2 and server1 a weight of 1, server2 will get 10 packets when server1 got 5.

```bash
ipvsadm -A -f 1 -s wrr
ipvsadm -a -f 1 -r 192.168.0.108:0 -w 1
ipvsadm -a -f 1 -r 192.168.0.109:0 -w 2
```

## Putting some load on the load balancing ip

Here is the result of putting some load on the virtual ip :

```bash
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
FWM  1 wrr
  -> 192.168.0.109:0              Route   2      0          1451
  -> 192.168.0.108:0              Route   1      0          721
```

We see that packets are transferred correctly to the servers, in accordance to their weight.