---
layout: post
title:  "Debugging DNSSEC with delv"
date:   2014-04-29 21:00:00 +0200
categories: system
---
* This will become a table of contents (this text will be scrapped).
{:toc}

# Introduced with bind 9.10rc1

Because `dig` is not so self-explanatory, here’s something more useful.

Since `bind 9.10rc1`, the ISC team introduced a new team to help with the debug of `DNSSEC` eventual problems. Initially called `delve`, but changed to `delv`.

This is what a standard dns query (using a non-validating resolver) shows:

```bash
dig ANY +dnssec +nocrypto dnssec-failed.org

	; <<>> DiG 9.10.0rc1 <<>> ANY +dnssec +nocrypto dnssec-failed.org
	;; global options: +cmd
	;; Got answer:
	;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 31994
	;; flags: qr rd ra; QUERY: 1, ANSWER: 14, AUTHORITY: 0, ADDITIONAL: 1

	;; OPT PSEUDOSECTION:
	; EDNS: version: 0, flags: do; udp: 4096
	;; QUESTION SECTION:
	;dnssec-failed.org.		IN	ANY

	;; ANSWER SECTION:
	dnssec-failed.org.	85942	IN	SOA	dns101.comcast.org. dnsadmin.comcast.net. 2010101630 900 180 604800 7200
	dnssec-failed.org.	85942	IN	RRSIG	SOA 5 2 86400 20140505165107 20140428134607 28833 dnssec-failed.org. [omitted]
	dnssec-failed.org.	6742	IN	NSEC	www.dnssec-failed.org. NS SOA RRSIG NSEC DNSKEY
	dnssec-failed.org.	6742	IN	RRSIG	NSEC 5 2 7200 20140505165107 20140428134607 28833 dnssec-failed.org. [omitted]
	dnssec-failed.org.	6742	IN	NS	dns101.comcast.net.
	dnssec-failed.org.	6742	IN	NS	dns102.comcast.net.
	dnssec-failed.org.	6742	IN	NS	dns103.comcast.net.
	dnssec-failed.org.	6742	IN	NS	dns104.comcast.net.
	dnssec-failed.org.	6742	IN	NS	dns105.comcast.net.
	dnssec-failed.org.	6742	IN	RRSIG	NS 5 2 7200 20140505165107 20140428134607 28833 dnssec-failed.org. [omitted]
	dnssec-failed.org.	3142	IN	DNSKEY	256 3 5 [key id = 28833]
	dnssec-failed.org.	3142	IN	DNSKEY	257 3 5 [key id = 29521]
	dnssec-failed.org.	3142	IN	RRSIG	DNSKEY 5 2 3600 20140624135107 20140224095107 29521 dnssec-failed.org. [omitted]
	dnssec-failed.org.	3142	IN	RRSIG	DNSKEY 5 2 3600 20140505165107 20140428134607 28833 dnssec-failed.org. [omitted]

	;; Query time: 718 msec
	;; SERVER: 10.211.55.1#53(10.211.55.1)
	;; WHEN: Mon Apr 28 21:29:25 CEST 2014
	;; MSG SIZE  rcvd: 1703
```

Let’s try to debug a bit what’s wrong on this domain with `dig`:

```bash
dig +sigchase dnssec-failed.org. A
	;; NO ANSWERS: no more
	We want to prove the non-existence of a type of rdata 1 or of the zone:
	;; nothing in authority section : impossible to validate the non-existence : FAILED

	;; Impossible to verify the Non-existence, the NSEC RRset can't be validated: FAILED
```

And this is the basic output of delv:

```bash
delv ANY dnssec-failed.org
	;; validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
	;; no valid RRSIG resolving 'dnssec-failed.org/DNSKEY/IN': 10.211.55.1#53
	;; broken trust chain resolving 'dnssec-failed.org/ANY/IN': 10.211.55.1#53
	;; validating dnssec-failed.org/NSEC: bad cache hit (dnssec-failed.org/DNSKEY)
	;; validating dnssec-failed.org/NS: bad cache hit (dnssec-failed.org/DNSKEY)
	;; validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
	;; resolution failed: no valid RRSIG
```

Quite better ! and it can even be better by tracing validation process:

```bash
delv +vtrace ANY dnssec-failed.org
	;; fetch: dnssec-failed.org/ANY
	;; validating dnssec-failed.org/SOA: starting
	;; validating dnssec-failed.org/SOA: attempting positive response validation
	;; fetch: dnssec-failed.org/DNSKEY
	;; validating dnssec-failed.org/DNSKEY: starting
	;; validating dnssec-failed.org/DNSKEY: attempting positive response validation
	;; fetch: dnssec-failed.org/DS
	;; validating dnssec-failed.org/DS: starting
	;; validating dnssec-failed.org/DS: attempting positive response validation
	;; fetch: org/DNSKEY
	;; validating org/DNSKEY: starting
	;; validating org/DNSKEY: attempting positive response validation
	;; fetch: org/DS
	;; validating org/DS: starting
	;; validating org/DS: attempting positive response validation
	;; fetch: ./DNSKEY
	;; validating ./DNSKEY: starting
	;; validating ./DNSKEY: attempting positive response validation
	;; validating ./DNSKEY: verify rdataset (keyid=19036): success
	;; validating ./DNSKEY: signed by trusted key; marking as secure
	;; validating org/DS: in fetch_callback_validator
	;; validating org/DS: keyset with trust secure
	;; validating org/DS: resuming validate
	;; validating org/DS: verify rdataset (keyid=40926): success
	;; validating org/DS: marking as secure, noqname proof not needed
	;; validating org/DNSKEY: in dsfetched
	;; validating org/DNSKEY: dsset with trust secure
	;; validating org/DNSKEY: verify rdataset (keyid=21366): success
	;; validating org/DNSKEY: marking as secure (DS)
	;; validating dnssec-failed.org/DS: in fetch_callback_validator
	;; validating dnssec-failed.org/DS: keyset with trust secure
	;; validating dnssec-failed.org/DS: resuming validate
	;; validating dnssec-failed.org/DS: verify rdataset (keyid=28794): success
	;; validating dnssec-failed.org/DS: marking as secure, noqname proof not needed
	;; validating dnssec-failed.org/DNSKEY: in dsfetched
	;; validating dnssec-failed.org/DNSKEY: dsset with trust secure
	;; validating dnssec-failed.org/DNSKEY: no DNSKEY matching DS
	;; validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
	;; no valid RRSIG resolving 'dnssec-failed.org/DNSKEY/IN': 10.211.55.1#53
	;; validating dnssec-failed.org/SOA: in fetch_callback_validator
	;; validating dnssec-failed.org/SOA: fetch_callback_validator: got failure
	;; broken trust chain resolving 'dnssec-failed.org/ANY/IN': 10.211.55.1#53
	;; validating dnssec-failed.org/NSEC: starting
	;; validating dnssec-failed.org/NSEC: attempting positive response validation
	;; validating dnssec-failed.org/NSEC: bad cache hit (dnssec-failed.org/DNSKEY)
	;; validating dnssec-failed.org/NS: starting
	;; validating dnssec-failed.org/NS: attempting positive response validation
	;; validating dnssec-failed.org/NS: bad cache hit (dnssec-failed.org/DNSKEY)
	;; validating dnssec-failed.org/DNSKEY: starting
	;; validating dnssec-failed.org/DNSKEY: attempting positive response validation
	;; validating dnssec-failed.org/DNSKEY: no DNSKEY matching DS
	;; validating dnssec-failed.org/DNSKEY: no valid signature found (DS)
	;; validating dnssec-failed.org/DNSKEY: falling back to insecurity proof
	;; validating dnssec-failed.org/DNSKEY: checking existence of DS at 'org'
	;; validating dnssec-failed.org/DNSKEY: checking existence of DS at 'dnssec-failed.org'
	;; validating dnssec-failed.org/DNSKEY: insecurity proof failed
	;; resolution failed: no valid RRSIG
```

And this is when everything works fine:

```bash
delv bkraft.fr
	; fully validated
	bkraft.fr.		1715	IN	A	88.190.215.226
	bkraft.fr.		1715	IN	RRSIG	A 8 2 3600 20140517114420 20140417110001 17781 bkraft.fr. tpKCap/U35Al0wplUXg4t91X/8IuuF1lLQE5+cefGoymgmMdXXRVewb9 nuL2k+v4SaodwHzF/prDeLVOtuEw/Rd8ACKZc38aU9ZUigUNU0BkTMxe FeasgXOaQwr5WN8MlzTjW2IWRx8VH1A+YHlf2wzPRQAE8HCvJXdM+61m Ojj+T4Eu5nVm0dU7ROSMuRtPlMnoquYOni7fg9Cmkn62wqaGNaFZu7iy 1dio5ByH3XQWJAZDTh72RWuNJtOyQPFn2J/WAvid/PScyLxYNy7SiIZ1 qhPgMWBezxBzdmds/ZlM8TvKy0gFELMoYoHc5L6l6C+iul1Byel57Alf jguDxw==
```

I can bet that in the next weeks/months/years, we will need to use such kind of tool more and more often as `DNSSEC` spreads. Please also note that the `+sigchase` and `+topdown` switches have been removed from `dig`, starting with `bind 9.10`.