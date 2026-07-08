# DNS Deep Dive

> 📌 **File:** 06_DNS_Deep_Dive.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

DNS (Domain Name System) is the phone book of the internet. It translates human-readable domain names (like `myapp.com`) into computer-readable IP addresses (like `54.23.189.12`). In AWS, Route 53 is the authoritative DNS service.

---

## Map it to MY STACK (CRITICAL)

```
Your Domain Name: myapp.com
Your Server IP: 54.23.189.12 (Elastic IP) or ALB endpoint

DNS Records you must configure:
  - A Record:     myapp.com → 54.23.189.12 (Direct IP)
  - CNAME Record: www.myapp.com → myapp.com (Alias)
  - MX Record:    myapp.com → mail.google.com (Emails)
  - TXT Record:   myapp.com → "google-site-verification=..." (Verification)

In AWS Route 53:
  Instead of CNAME for Root Domain (myapp.com), use ALIAS record:
  - ALIAS Record: myapp.com → alb-dns-name.amazonaws.com
  (DNS standard forbids CNAME on root domain; ALIAS solves this!)
```

---

## How DNS Resolution Works

```
┌──────────────────────────────────────────────────────────────────┐
│  DNS Resolution Flow (Iterative Query)                           │
│                                                                  │
│  Client (Your Browser)                                           │
│       │                                                          │
│       ├── 1. Check local browser cache, then OS hosts file       │
│       │                                                          │
│  ┌────▼────┐                                                     │
│  │Resolving│  Local Resolver (usually ISP, Google 8.8.8.8,       │
│  │Resolver │  or Cloudflare 1.1.1.1)                             │
│  └────┬────┘                                                     │
│       │                                                          │
│       ├── 2. Query Root Name Server (".")                        │
│       ├── 3. Query TLD Name Server (".com")                      │
│       └── 4. Query Authoritative Name Server (Route 53)          │
│                                                                  │
│  Server IP (e.g. 54.23.189.12) returned to Client                │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Library Catalog)
DNS resolution is visually exactly like finding a book in a library:
- **Local Cache (Your desk):** You check if the book is on your desk first.
- **Resolving Resolver (The Librarian):** You ask the librarian. The librarian does the walking for you.
- **Root Server (The Directory):** The librarian checks the directory, which says "All science books are in Section C" (points to `.com` TLD).
- **TLD Server (The Section Sign):** Section C says "Go to Shelf 4 for networking" (points to Route 53).
- **Authoritative Server (The Book Shelf):** Shelf 4 gives you the exact book page (returns the IP address).

---

## Key DNS Record Types

```
┌──────────────────────────────────────────────────────────────────┐
│  Record Type │ Maps From      │ Maps To       │ Use Case         │
├──────────────┼────────────────┼───────────────┼──────────────────┤
│  A           │ Domain Name    │ IPv4 Address  │ Standard server  │
│              │ (myapp.com)    │ (54.23.189.1) │ mapping          │
│              │                │               │                  │
│  AAAA        │ Domain Name    │ IPv6 Address  │ Modern IPv6      │
│              │                │               │ networks         │
│              │                │               │                  │
│  CNAME       │ Subdomain      │ Domain Name   │ Alias: redirect  │
│              │ (www.myapp.com)│ (myapp.com)   │ to another host  │
│              │                │               │                  │
│  MX          │ Domain Name    │ Mail Server   │ Email routing    │
│              │                │ (gmail-smtp)  │ (GSuite)         │
│              │                │               │                  │
│  TXT         │ Domain Name    │ Text String   │ Domain verification│
│              │                │               │ (SSL, Google)    │
└──────────────┴────────────────┴───────────────┴──────────────────┘
```

---

## TTL (Time To Live)

```
TTL determines how long DNS resolvers can cache your record.

Low TTL (e.g. 60 seconds):
  - Resolvers ask Route 53 for updates every 60s.
  - Good for migration: if you change server IP, users see it fast.
  - Bad for cost/latency: more DNS queries to Route 53 ($0.40/million).

High TTL (e.g. 86,400 seconds / 24 hours):
  - Resolvers cache your IP for 24 hours.
  - Good for latency: fast loads, low Route 53 queries.
  - Bad for migration: if server dies, users try old IP for 24 hours!
```

---

## Route 53 Routing Policies

```
AWS Route 53 can route traffic intelligently:

1. Simple Routing: Single resource (one IP). No health checks.
2. Weighted Routing: Split traffic (e.g. 90% to App v1, 10% to App v2).
3. Latency-Based Routing: Route user to the nearest AWS region.
4. Failover Routing: Active-Passive. Route to standby if active fails.
5. Geolocation Routing: Route by user country (e.g. EU users to EU server).
```

---

## Commands & Diagnostics

```bash
# Basic DNS lookup (returns A records)
nslookup myapp.com

# Detailed DNS query (mac/linux)
dig myapp.com

# Query specific DNS server (Google DNS) to check propagation
dig @8.8.8.8 myapp.com

# Trace DNS delegation path (root -> TLD -> Route 53)
dig +trace myapp.com

# Query TXT records (domain verification)
dig myapp.com TXT
```

---

## Common Mistakes

### ❌ CNAME on Root Domain (Zone Apex)

```
❌ CNAME myapp.com → alb-dns-name.amazonaws.com
   DNS standard forbids CNAME records at the root. It breaks MX records.

✅ Route 53 ALIAS record:
   A record: myapp.com → ALIAS to alb-dns-name.amazonaws.com
   This behaves like a CNAME but complies with standards.
```

### ❌ Forgetting to lower TTL before migration

```
❌ Server migration day: You change IP with TTL set to 86,400s (24h).
   → Half your users hit the old, dead server for 24 hours.

✅ Before migration: Change TTL to 60s, wait 24h.
   Perform migration: Change IP, verify.
   After migration: Raise TTL back to 86,400s.
```

---

## Practice Exercises

### Exercise 1: dig trace
Run `dig +trace google.com`. Identify: the root server names, the `.com` TLD servers, and Google's authoritative name servers.

### Exercise 2: DNS Propagation
Add a TXT record to your domain. Use `dig @1.1.1.1 myapp.com TXT` and `dig @8.8.8.8 myapp.com TXT` to observe how fast it propagates across different global DNS servers.

### Exercise 3: Local hosts override
Modify your local hosts file (`/etc/hosts` or `C:\Windows\System32\drivers\etc\hosts`). Add: `127.0.0.1 google.com`. Open browser and visit google.com. Document what happens. (Remove entry immediately after!)

---

## Interview Q&A

**Q1: What happens step-by-step when you type google.com in browser?**
> Browser checks local cache. If miss, asks Local DNS Resolver (ISP). Resolver queries Root server (returns `.com` TLD IP). Resolver queries `.com` TLD server (returns Google Name Server IP). Resolver queries Google Name Server (returns Google's A/AAAA IP). Resolver returns IP to browser. Browser initiates TCP connection.

**Q2: What is the difference between a CNAME and an A record?**
> An A record maps a hostname to an IP address (`myapp.com` → `54.23.189.1`). A CNAME maps a hostname to another hostname (`www.myapp.com` → `myapp.com`). CNAME cannot be used at the root zone (apex).

**Q3: What is a Route 53 ALIAS record?**
> An AWS-specific record that acts like a CNAME but can be used at the root zone (apex). Unlike CNAME, which redirects the client, ALIAS resolves the target internally on AWS DNS servers and returns the IP directly to the client.

**Q4: How do you perform a zero-downtime DNS migration?**
> Lower TTL to 60 seconds at least 24 hours before migration. Perform migration by changing IP. Verify traffic moves. Raise TTL back to normal (e.g. 1 hour) once stable.

**Q5: What is DNS Propagation delay?**
> The time it takes for DNS records to update across all global servers. Cached records remain valid until their TTL expires. Propagation delay is mostly determined by the TTL of the old record.

---

Prev : [05 IP Addressing And Subnetting](./05_IP_Addressing_And_Subnetting.md) | Index: [00 Index](./00_Index.md) | Next : [07 HTTP HTTPS Internals](./07_HTTP_HTTPS_Internals.md)
