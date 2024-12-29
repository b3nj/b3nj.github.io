---
layout: post
title:  "Tunneling connections with Putty"
date:   2009-12-03 21:00:00 +0200
categories: system
---
* This will become a table of contents (this text will be scrapped).
{:toc}

# How to use the SSH protocol to encapsulate traffic on Windows

Let’s say, you want to access a remote server on ports TCP 7333 and 809, but they are closed by your network administrator and you just can connect via SSH to the remote server (this howto works with a third server that could be used to tunnel connections). This is far enough, you can use PuTTY to forward the connections from your local machine to the remote ports via a SSH connection.

## Howto

To do this, open PuTTY, and enter the hostname on which you are able to connect :

![01](/assets/images/tunneling-connections-with-putty/01.jpg)

Then, go to Connection, SSH and Tunnels

![02](/assets/images/tunneling-connections-with-putty/02.jpg)

Here, add source port 802 and destination server.domain.tld:802

![03](/assets/images/tunneling-connections-with-putty/03.jpg)

Click add, and then add source port 7333 and destination server.domain.tld:7333

![04](/assets/images/tunneling-connections-with-putty/04.jpg)

Then finally, click add and open

![05](/assets/images/tunneling-connections-with-putty/05.jpg)

Now, if you connect to localhost at port 7333 or 802, your connections will be forwarded from your local machine to the remote server.

> [!NOTE] If you close PuTTY, your tunnels will be closed too. 