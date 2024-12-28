---
layout: post
title:  "Automatize CentOS server installation"
date:   2009-11-28 21:00:00 +0200
categories: system
---
* This will become a table of contents (this text will be scrapped).
{:toc}

# Creating your kickstarting infrastructure

Did you ever wished that you automatize your server installation (called kickstarting) ? In this article you will see a way to automatize the installation of a linux server (it will be a RedHat based server) via the network.

## Introduction and requirements

Installing a server requires some components to be present on your network.
The process of the server kickstarting will be the following :

* `server1` (to be kickstarted) boots and makes dhcp discover (DHCPDISCOVER) request on his network to see if there’s a dhcp server available
* `server2` responds to the dhcp request (DHCPREQUEST) by making an offer with an IP address
* `server1` makes a DHCPREQUEST to the server in order to have the previously offered IP address
* `server2` acknowledges the request and indicates where the tftp server is (will be `server2` as well)
* `server1` makes a PXE (Preboot Execution Environment) to `server2`
* `server1` loads syslinux, a small network booting environment from `server2`
* You choose (can be defaulted) on what you want `server1` to boot
* `server1` fetches a kickstart file and runs the instructions

If we resume, you will need a dhcp server (most of you already have) and a tftp server. Optionally, you’ll need a web server to host you kickstart files.

## Installing and configuring

### dhcp server

Just one packet to go here :

```bash
yum install dhcp
=>	...
	Installed:
	  dhcp.i386 12:3.0.5-21.el5_4.1
```

Now we’ll configure the server by editing `/etc/dhcpd.conf`

```bash
cat > /etc/dhcpd.conf
	#Allow pxe requests
	allow booting;
	allow bootp;

	ddns-update-style interim;
	ignore client-updates;

	subnet 192.168.0.0 netmask 255.255.255.0 {
	#standard network configuration
	        option routers                  192.168.0.1;
	        option subnet-mask              255.255.255.0;

	        option nis-domain               "dotnul.com";
	        option domain-name              "dotnul.com";
	        option domain-name-servers      80.92.65.30;

	        default-lease-time 21600;
	        max-lease-time 43200;
	#here we're saying where server1 should make the pxe boot
	        next-server                     192.168.0.109;
	#and which file syslinux is on it
	        filename                        "pxelinux.0";

	#here is the reservation for server1
	        host server1 {
	                hardware ethernet 00:0C:29:26:FA:12;
	                fixed-address 192.168.0.108;
	        }
	}
^D
```

Start and add to the default runlevel the dhcp daemon

```bash
# Starting the server
/etc/init.d/dhcpd start
=>	Starting dhcpd:                                            [  OK  ]
# Adding the service to the default runlevel 
chkconfig dhcpd on
```

### tftp server

As tftp-server uses the xinetd super daemon to start, we’ll have to install it if not already present.

```bash
yum install tftp-server
=>	...
	Installed:
	  tftp-server.i386 0:0.49-2.el5.centos

	Dependency Installed:
	  xinetd.i386 2:2.3.14-10.el5
```

What we need to do is, in the `pxeboot` default directory, copy syslinux in it and create a default configuration file for syslinux along with the default boot menu.

```bash
cd /tftpboot
cp /usr/lib/syslinux/pxelinux.0 .
mkdir pxelinux.cfg
cd pxelinux.cfg/
cat > default
	default 1
	timeout 1000
	prompt 1
	display menu.msg

	label 1
	       localboot 1

	label 2
	       kernel centos/5.7/i386/vmlinuz
	       append initrd=centos/5.7/i386/initrd.img ramdisk_size=10000

	label 3
	       kernel centos/5.7/i386/vmlinuz
	       append initrd=centos/5.7/i386/initrd.img ramdisk_size=10000 \
	              ksdevice=eth0 ks=http://dotnul.com/centos-basic.ks
^D
cd ..
cat > menu.msg
	My PXE Menu

	choose between the following options :

	1 : boot local disk (default)
	2 : install centos by hand
	3 : install centos by kickstarting
^D
```

Now, we’ll have to find the installation kernel and initrd to boot the installation media from the network on a centOS repository.

```bash
mkdir -p centos/5.7/i386/
cd centos/5.7/i386/
wget http://mirror.dclux.com/centos/5.7/os/i386/images/pxeboot/initrd.img
wget http://mirror.dclux.com/centos/5.7/os/i386/images/pxeboot/vmlinuz
```

If you’re using `SELinux`, like me, make sure that the context is `root:object_r:tftpdir_t:s0`

Edit the tftp xinetd configuration file to enable tftp-server to work

```bash
vim /etc/xinetd.d/tftp
...
disable = no
...
```

Start and add to the default runlevel the xinet daemon

```bash
/etc/init.d/xinetd start
=>	Starting xinetd:                                            [  OK  ]
chkconfig xinetd on
```

Now, you need a kickstart file describing how you’d like to configure the server what you want to install on it. This step won’t be detailed here, I’ll use my personnal default kickstart located at ~~~http://dotnul.com/centos-basic.ks~~~. It does a basic installation without X and with password as root password.

### Booting

Let’s start `server1` and make a pxe boot

Hooray ! it worked …
Here’s what in `server2` /var/log/message :

```log
server2 dhcpd: DHCPDISCOVER from 00:0c:29:26:fa:12 via eth0
server2 dhcpd: DHCPOFFER on 192.168.0.108 to 00:0c:29:26:fa:12 via eth0
server2 dhcpd: DHCPREQUEST for 192.168.0.108 (192.168.0.109) from 00:0c:29:26:fa:12 via eth0
server2 dhcpd: DHCPACK on 192.168.0.108 to 00:0c:29:26:fa:12 via eth0
```

Now, type 3, and enter and the installation should run smoothly. It’s time for you to make some coffee, well done !