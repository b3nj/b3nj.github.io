---
layout: post
title: "DNS outage at home: Quad9 and OpenDNS are both gone from France"
date: 2026-11-25 07:30:00 +0100
categories: [homelab, networking]
tags: [dns, adguard-home, quad9, opendns, france, raspberry-pi, doh, censorship, arcom]
excerpt: "My AdGuard Home was healthy, listening on :53, and still resolved nothing. The upstreams had left the country."
---

**TL;DR** — My AdGuard Home instance on a Raspberry Pi stopped resolving names. The daemon was fine; the *upstream* was not. Quad9 (my DoH upstream) withdrew from France on 2026-11-24, and OpenDNS, my fallback idea, has been refusing French clients since June 2024. Both are consequences of French court orders based on Article L.333-10 of the *Code du sport*, which lets sports rightsholders force DNS resolvers to block domains.

## Symptoms

For a few days, browsing from home was flaky. I assumed the Pi (`cerbere`) running AdGuard Home was hanging every once in a while and kept rebooting it. Wrong diagnosis. After today's reboot the service is up and happy:

```console
root@cerbere:~# systemctl status AdGuardHome.service
● AdGuardHome.service - AdGuard Home: Network-level blocker
     Loaded: loaded (/etc/systemd/system/AdGuardHome.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2026-11-25 05:56:35 CET; 38min ago
    Process: 385 ExecStartPre=/bin/mkdir -p /var/log/ (code=exited, status=0/SUCCESS)
   Main PID: 403 (AdGuardHome)
      Tasks: 12 (limit: 1595)
        CPU: 2min 19.113s
     CGroup: /system.slice/AdGuardHome.service
             └─403 /opt/AdGuardHome/AdGuardHome -s run
```

And it is bound on port 53 (TCP and UDP) and 80 for the web UI:

```console
root@cerbere:~# netstat -plunt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      516/sshd: /usr/sbin
tcp6       0      0 :::53                   :::*                    LISTEN      403/AdGuardHome
tcp6       0      0 :::22                   :::*                    LISTEN      516/sshd: /usr/sbin
tcp6       0      0 :::80                   :::*                    LISTEN      403/AdGuardHome
udp        0      0 0.0.0.0:68              0.0.0.0:*                           629/dhcpcd
udp        0      0 0.0.0.0:5353            0.0.0.0:*                           388/avahi-daemon: r
udp        0      0 0.0.0.0:57723           0.0.0.0:*                           388/avahi-daemon: r
udp6       0      0 :::53                   :::*                                403/AdGuardHome
udp6       0      0 :::5353                 :::*                                388/avahi-daemon: r
udp6       0      0 :::41368                :::*                                388/avahi-daemon: r
```

So: process alive, sockets open, yet `nslookup` returned nothing. When the local resolver is healthy but answers nothing, look **one hop upstream**.

## Root cause #1: Quad9 left France

My AdGuard Home upstream was Quad9 over DNS-over-HTTPS:

```text
https://dns.quad9.net/dns-query
```

Then I remembered the news: [Quad9 Service Deactivation in France](https://quad9.net/news/blog/quad9-service-deactivation-in-france/). Since **2026-11-24 at 09:00 (Paris time)**, any query reaching any Quad9 service address from a French IP is refused. No error page, no redirect: your resolver simply stops working, which is exactly what a home DNS filter looks like when the upstream dies.

You can check the other Quad9 addresses the same way (`9.9.9.9`, `149.112.112.112`, plus the IPv6 `2620:fe::fe` and `2620:fe::9`):

```console
root@cerbere:~# dig example.com @9.9.9.9
```

Quad9 selects French users by **GeoIP**, which they themselves describe as imprecise. Some French users may keep working for a while, and some non-French users may get cut off. That may explain why my symptoms looked intermittent rather than a clean outage. I can't prove that link, so treat it as a hypothesis.

## Root cause #2: OpenDNS FamilyShield refuses too

My next idea was Cisco's OpenDNS FamilyShield (`208.67.222.123`), a free family-safe resolver. Same disappointment:

```console
root@cerbere:~# dig google.fr @208.67.222.123

; <<>> DiG 9.16.50-Raspbian <<>> google.fr @208.67.222.123
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: REFUSED, id: 62383
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 2

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1410
; EDE: 16 (Censored)
;; QUESTION SECTION:
;google.fr.                     IN      A

;; ADDITIONAL SECTION:
google.fr.              0       IN      TXT     "The OpenDNS service is currently unavailable in France and some French territories due to a court order under Article L.333-10 of the French Sport Code. See https://support.opendns.com/hc/en-us"

;; Query time: 19 msec
;; SERVER: 208.67.222.123#53(208.67.222.123)
;; WHEN: Wed Nov 25 06:42:06 CET 2026
;; MSG SIZE  rcvd: 250
```

Worth reading carefully, this is a well-behaved refusal:

- `status: REFUSED` (RCODE 5): the server understood the query and declined to answer. It is *not* `NXDOMAIN`, and it is not a timeout.
- `EDE: 16 (Censored)`: an [Extended DNS Error](https://www.rfc-editor.org/rfc/rfc8914.html) (RFC 8914). Code 16 means the answer was blocked due to a requirement external to the resolver, as opposed to 15 (Blocked, resolver's own policy), 17 (Filtered, requested by the client) or 18 (Prohibited).
- The `TXT` record in the ADDITIONAL section is synthetic (TTL 0, owner name copied from the question). It is how OpenDNS tells a human what happened.

Note that this is not new: OpenDNS has been unavailable in France [since 2024-06-28](https://torrentfreak.com/opendns-suspends-service-in-france-due-to-canal-piracy-blocking-order-240629/). See [Cisco's own notice](https://support.opendns.com/hc/en-us/articles/27951404269204-OpenDNS-Service-Not-Available-To-Users-In-France-and-Portugal). It was never going to be a replacement.

## Why is this happening?

### The legal basis: Article L.333-10 of the Code du sport

[Article L.333-10](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044247629/) of the French Sport Code came from the Act of 25 October 2021. It allows sports rightsholders (leagues, broadcasters) to ask the Paris judicial court for "all proportionate measures" against **any online entity able to help** stop serious and repeated piracy of sports broadcasts. Arcom, the regulator, handles the dynamic updating of the blocklists.

Originally that meant ISPs: they poison their own DNS resolvers for the listed domains. The loophole was obvious. Users just switch to `8.8.8.8`, `1.1.1.1` or `9.9.9.9`. So rightsholders went after the public resolvers too.

### Timeline

| Date | Event |
|------|-------|
| 2021-10-25 | Act introducing L.333-10 |
| 2024-05 | Paris judicial court orders by Canal+ (Premier League, Champions League) |
| 2024-06-28 | Cisco withdraws **OpenDNS** from France (and Portugal) instead of complying |
| 2024-11 | Orders extended; Google and Cloudflare implement blocking in France |
| 2026-03-27 | Paris Court of Appeal rejects five appeals by Cisco, Cloudflare and Google |
| 2026-10-21 | Judgment against **Quad9** in the beIN case; daily penalty reduced from €580,000 to €1,000 |
| 2026-10-22 | Quad9 announces its withdrawal ([Farewell, France](https://quad9.net/news/blog/au-revoir-france/)) |
| 2026-11-24 | Quad9 stops serving France |

### The court's reasoning (paraphrased)

From the [TorrentFreak write-up](https://torrentfreak.com/google-cloudflare-cisco-lose-pirate-site-dns-blocking-appeal-in-france/) of the March 2026 appeal rulings:

- The "neutral and passive resolver" argument is irrelevant: the article is about *who can help block*, not about liability.
- Blocking does not have to be perfect to be proportionate. Circumvention (VPN, another resolver) does not make it ineffective.
- Cost arguments (Cisco claimed 64 person-weeks of engineering) were rejected as unsupported. Providers pay for implementation.

### Quad9's position

Quad9 is a Swiss non-profit. Its blocking is limited to security threats (malware, phishing), explicitly not content, and it refuses to block pirate-streaming domains. It also says it cannot comply cleanly:

- **Geo-blocking only for France?** GeoIP is imprecise, and in an earlier German case (Sony) a GeoIP-based approach still resulted in contempt-of-court fines.
- **Block globally?** That would apply a French court order to every user worldwide.

Their conclusion was to leave the French market entirely. They also mention roughly 20 other pending cases in France, and an appeal still in progress.

Whatever your opinion on piracy or on the court's choices, the practical effect for me is simple: a resolver I used for security *and* privacy is no longer reachable from my home line. For more perspectives: [Cloudflare's take](https://blog.cloudflare.com/quad9-withdrawal-from-france/), [the EFF](https://www.eff.org/deeplinks/2026/10/french-courts-site-blocking-orders-drive-quad9-out-france), and [TorrentFreak on the blocklist content](https://torrentfreak.com/inside-a-french-piracy-blocklist-expired-domains-a-seized-site-and-hong-kong-servers/).

*(I run infrastructure, I am not a lawyer. Read the primary sources linked above.)*

## Immediate fix and trade-offs

I temporarily switched the AdGuard Home upstream to Google (`8.8.8.8`). Resolution is back. The cost is real though:

- Google applies the French blocklist, as ordered. Quad9 did not.
- No more Quad9 threat-intel blocking (malware/phishing) at the resolver level.
- Google is not a family-safe resolver. The kids' protection now relies entirely on what AdGuard Home does *locally* (see below).
- More privacy exposure towards a large ad company.

## Hardening AdGuard Home so this doesn't bite again

### 1. Check `bootstrap_dns` too

A DoH upstream is addressed by hostname, so AdGuard Home needs a plain-DNS **bootstrap** to resolve it. Look at both places in `/opt/AdGuardHome/AdGuardHome.yaml`:

```console
root@cerbere:~# grep -nA6 -E '^\s+(upstream_dns|bootstrap_dns|fallback_dns):' /opt/AdGuardHome/AdGuardHome.yaml
```

Depending on your version and history, bootstrap may default to Quad9 addresses (for example `9.9.9.10`). In that case your upstream can break even if the DoH provider itself is still alive. Replace them with resolvers that serve France and are not the same provider.

### 2. Use more than one upstream provider, plus a fallback

Mix providers and jurisdictions, and set a fallback (**Settings → DNS settings** in the UI, `fallback_dns` in recent versions). One provider disappearing should degrade, not kill, your household's internet.

### 3. Don't outsource the child filtering to the upstream

Since the upstream is now generic, make sure the local filtering does the job. In **Settings → General settings**:

- Parental control (AdGuard's web service)
- Browsing security
- Enforce safe search

Plus adult-content blocklists under **Filters → DNS blocklists**. This is also a good moment to add a malware/phishing list to replace what Quad9 was doing for free.

### 4. Alternatives to test (from a French IP!)

I have not validated these from my line yet. Test before you trust them.

- **DNS4EU**, the EU-funded resolver, has a "Protective + Child Protection" variant (`child.joindns4.eu`, DoH `https://child.joindns4.eu/dns-query`). See [joindns4.eu](https://joindns4.eu/for-public). Its operators describe it as free of national blocking obligations, but being EU-based does not make it immune to French orders. Check, don't assume.
- **Run your own recursive resolver** ([Unbound](https://nlnetlabs.nl/projects/unbound/about/)) and use it as AdGuard Home's upstream. No third party in the loop, at the cost of less privacy towards authoritative servers and no shared threat intel.

### 5. Test the upstreams from where they matter

A quick loop to see which resolvers answer from your line:

```bash
for ns in 9.9.9.9 149.112.112.112 208.67.222.123 1.1.1.1 8.8.8.8 86.54.11.12; do
  printf '%-18s ' "$ns"
  dig +time=2 +tries=1 @"$ns" example.com A \
    | awk '/status:/ {gsub(",","",$6); s=$6} END {print (s ? s : "NO-REPLY")}'
done
```

You are looking for `NOERROR`. `REFUSED` or `NO-REPLY` means that upstream is out.

### 6. Monitor the *service*, not the process

`systemctl status` told me everything was fine while DNS was dead. A health check that does a real lookup through the local resolver is what you actually want:

```bash
#!/bin/sh
# /usr/local/bin/dns-healthcheck.sh : run from cron or a systemd timer
dig +short +time=2 +tries=1 @127.0.0.1 example.com A | grep -q . \
  || logger -t dns-healthcheck "AdGuard Home answers nothing for example.com"
```

Hook that logger line to whatever alerting you have (I use Telegram for other things).

## Lessons

1. A healthy daemon does not mean a working service. Test the full resolution path.
2. A single upstream provider is a single point of failure, and sometimes the failure is legal, not technical.
3. `REFUSED` plus an `EDE` code is the resolver telling you *why*. Read the OPT and ADDITIONAL sections.
4. Free third-party DNS is subject to the jurisdiction of its users, not just of its operator.

## References

- Quad9: [Farewell, France (2026-10-22)](https://quad9.net/news/blog/au-revoir-france/) and [Service Deactivation in France (2026-11-24)](https://quad9.net/news/blog/quad9-service-deactivation-in-france/)
- Cloudflare: [Quad9's withdrawal from France: a canary in the coal mine](https://blog.cloudflare.com/quad9-withdrawal-from-france/)
- EFF: [French courts' site-blocking orders drive Quad9 out of France](https://www.eff.org/deeplinks/2026/10/french-courts-site-blocking-orders-drive-quad9-out-france)
- TorrentFreak: [OpenDNS suspends service in France (2024)](https://torrentfreak.com/opendns-suspends-service-in-france-due-to-canal-piracy-blocking-order-240629/), [Google, Cloudflare, Cisco lose appeal (2026)](https://torrentfreak.com/google-cloudflare-cisco-lose-pirate-site-dns-blocking-appeal-in-france/)
- Cisco: [OpenDNS not available in France and Portugal](https://support.opendns.com/hc/en-us/articles/27951404269204-OpenDNS-Service-Not-Available-To-Users-In-France-and-Portugal)
- Légifrance: [Article L.333-10, Code du sport](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044247629/)
- RFC 8914: [Extended DNS Errors](https://www.rfc-editor.org/rfc/rfc8914.html)
- Stéphane Bortzmeyer: [OpenDNS n'est plus accessible depuis la France](https://www.bortzmeyer.org/opendns-quitte-france.html)
- DNS4EU: [joindns4.eu](https://joindns4.eu/for-public)
