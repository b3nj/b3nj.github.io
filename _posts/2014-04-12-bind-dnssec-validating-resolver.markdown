---
layout: post
title:  "Setup Bind as DNSSEC validating resolver"
date:   2014-04-12 21:00:00 +0200
categories: system
---
* This will become a table of contents (this text will be scrapped).
{:toc}

# Add some security to the most important service

The sooner or the later, `DNSSEC` will be deployed globally (although I don’t think this will be an easy story, we’ll need to see the evolutions of related software) and you’ll be in the need to have a `DNSSEC` enabled validating nameserver that will do the checks for you. This is a very small and simple tutorial to deploy one of those.

Last day’s [post](http://jpmens.net/2012/04/19/dnssec-training/) from Jan-Piet Mens about the great [SIDN DNSSEC](http://www.dnsseccourse.nl/) training made me think that it would be nice to show how to setup a basic validating `DNSSEC` resolver based on the packages that I’m providing on this very website (Bind 9.9.0 and Bind 9.8.2).

## Installation

It’s pretty straight forward, just install bind. (in fact, `bind-chroot` won’t be needed here)

```bash
rpm -Uvh noarch/bind-license-9.8.1-2.el6.noarch.rpm 
	Preparing...             ############################### [100%]
   	1:bind-license           ############################### [100%]
rpm -Uvh bind-chroot-9.8.1-2.el6.x86_64.rpm bind-9.8.1-2.el6.x86_64.rpm bind-libs-9.8.1-2.el6.x86_64.rpm bind-utils-9.8.1-2.el6.x86_64.rpm 
	Preparing...             ############################### [100%]
   	1:bind-libs              ############################### [ 25%]
   	2:bind                   ############################### [ 50%]
   	3:bind-chroot            ############################### [ 75%]
   	4:bind-utils             ############################### [100%]
```

## Configuration

```bind
options {
	listen-on port 53 { any; };
	listen-on-v6 port 53 { ::1; };
	directory 	"/var/named";
	dump-file 	"/var/named/data/cache_dump.db";
	statistics-file "/var/named/data/named_stats.txt";
	memstatistics-file "/var/named/data/named_mem_stats.txt";
	allow-query     { any; };
	recursion yes;
    version "[Secured]";
	
/* Those are the values you should disable if you don't want DNSSEC enabled */
	dnssec-enable yes;
	dnssec-validation yes;
	dnssec-lookaside auto;

/* Path to ISC DLV key */
	bindkeys-file "/etc/named.iscdlv.key";

	managed-keys-directory "/var/named/dynamic";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
	type hint;
	file "named.ca";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```

## Testing

Once configured and started, let’s query the resolver without asking for `DNSSEC` validation.

```bash
dig bkraft.fr @localhost

	; <<>> DiG 9.8.2-RedHat-9.8.2-0.el6 <<>> bkraft.fr @localhost
	;; global options: +cmd
	;; Got answer:
	;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 3408
	;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 2, ADDITIONAL: 0

	;; QUESTION SECTION:
	;bkraft.fr.			IN	A

	;; ANSWER SECTION:
	bkraft.fr.		300	IN	A	173.245.61.141
	bkraft.fr.		300	IN	A	173.245.61.54

	;; AUTHORITY SECTION:
	bkraft.fr.		172799	IN	NS	kara.ns.cloudflare.com.
	bkraft.fr.		172799	IN	NS	greg.ns.cloudflare.com.

	;; Query time: 958 msec
	;; SERVER: 127.0.0.1#53(127.0.0.1)
	;; WHEN: Sun Feb 19 16:36:11 2012
	;; MSG SIZE  rcvd: 114
```

Fine, now query with validation enabled :

```bash
dig +dnssec dns.be @localhost

	; <<>> DiG 9.8.2-RedHat-9.8.2-0.el6 <<>> +dnssec dns.be @localhost
	;; global options: +cmd
	;; Got answer:
	;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 42709
	;; flags: qr rd ra ad; QUERY: 1, ANSWER: 3, AUTHORITY: 7, ADDITIONAL: 13

	;; OPT PSEUDOSECTION:
	; EDNS: version: 0, flags: do; udp: 4096
	;; QUESTION SECTION:
	;dns.be.				IN	A

	;; ANSWER SECTION:
	dns.be.			3543	IN	A	149.126.56.7
	dns.be.			3543	IN	A	149.126.56.6
	dns.be.			3543	IN	RRSIG	A 8 2 3600 20120327144240 20120216135245 43356 dns.be. VUaS4KOKTXJAof7CbI/jz1StoEngTK5C5ldtgI534GWOJa4eqqkqCs2/ TRm7F7E/YO7cLLcBh+BJhsR9cb3zZq9e8RM5vc6nTI6s6NgIbWDGoZNl RkAeb5M4E7kjL6jGnyiT83bPEnbeJNXlHtFnrv/ZqT6RWv/zVGLHP/NN QX0=

	;; AUTHORITY SECTION:
	dns.be.			86342	IN	NS	brussels.ns.dns.be.
	dns.be.			86342	IN	NS	m.ns.dns.be.
	dns.be.			86342	IN	NS	prague.ns.dns.be.
	dns.be.			86342	IN	NS	c.ns.dns.be.
	dns.be.			86342	IN	NS	amsterdam.ns.dns.be.
	dns.be.			86342	IN	NS	london.ns.dns.be.
	dns.be.			86342	IN	RRSIG	NS 8 2 86400 20120327144240 20120216135245 43356 dns.be. hBRmAgH31yopygpKIlAeUwtwx4EXjPESJlbArjn+GgH1kkwyEB4SVBi6 Hrs8/XzGZXUHLB5jiCinvq9er2jST7xqJMzuqQXP3I8o6JiHmReYvX3+ KXhinSxDRFqwa77o5d3HZXZyag2XXlYkoRkQYVoOvxU3m2zF3fUKIPMQ 2hQ=

	;; ADDITIONAL SECTION:
	<..snip..>

	;; Query time: 0 msec
	;; SERVER: 127.0.0.1#53(127.0.0.1)
	;; WHEN: Sun Feb 19 16:38:44 2012
	;; MSG SIZE  rcvd: 1627
```

Great ! The `ad` flag means that the data displayed has been authenticated, the `OPT` pseudosection shows that our server used `EDNS0` to pass over the 512bits limit and finally we see all RRSIG for each displayed part of the response.

Using validation now is good, but the fact that all signing and key rollover management softwares are still pretty young, you should be warned that enabling `DNSSEC` might lead you to not see expected results where a standard resolver would respond. Also, it’s a good idea to limit the number of queries to this resolver as `DNSSEC` validation adds overhead on the server in comparison to standard resolution.