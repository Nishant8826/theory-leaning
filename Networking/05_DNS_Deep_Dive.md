# DNS Deep Dive

> 📌 **File:** 05_DNS_Deep_Dive.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

DNS (Domain Name System) is the internet's phone book — it translates domain names (`api.myapp.com`) to IP addresses (`54.23.189.12`). Every time your React app calls an API, every time Node.js connects to MongoDB Atlas, DNS happens first. It's invisible when it works and devastating when it breaks.

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────────┐
│  DNS in Your Stack                                                  │
├────────────────────────────────────┬─────────────────────────────────┤
│  myapp.com                         │ Route 53 → CloudFront (CDN)    │
│  api.myapp.com                     │ Route 53 → ALB (load balancer) │
│  cluster0.mongodb.net              │ Atlas DNS → replica set IPs    │
│  my-cache.xxxxx.cache.amazonaws.com│ ElastiCache DNS → Redis IP     │
│  my-db.xxxxx.rds.amazonaws.com     │ RDS DNS → PostgreSQL IP       │
│  s3.amazonaws.com                  │ AWS DNS → S3 regional endpoint │
│  d111xxxx.cloudfront.net           │ CloudFront DNS → nearest edge  │
├────────────────────────────────────┴─────────────────────────────────┤
│  EVERY connection starts with DNS. EVERY one.                       │
└──────────────────────────────────────────────────────────────────────┘
```

### What Happens During DNS (Unrolled)

```
User browser: fetch('https://api.myapp.com/products')

Step 1: Browser DNS cache → "Do I already know this?" → MISS
Step 2: OS DNS cache → "Has any app looked this up?" → MISS
Step 3: Router DNS cache → "Has anyone on the network asked?" → MISS
Step 4: ISP's recursive resolver → "Let me find out..."
Step 5: Root DNS server → "I know who handles .com" → return .com NS
Step 6: .com TLD server → "I know who handles myapp.com" → return NS records
Step 7: myapp.com authoritative DNS (Route 53) → "api.myapp.com = 54.23.189.12"
Step 8: Result cached at every level (TTL-based)

Next request: Browser cache → HIT → 0ms (cached for TTL seconds)
```

---

## Why this matters in real systems

### Scenario 1: "DNS propagation is taking hours!"

```
You changed api.myapp.com from old-server to new-server in Route 53.

Old Record: api.myapp.com → 54.23.189.12 (TTL: 86400 = 24 hours)
New Record: api.myapp.com → 54.23.189.99

Problem: Users still hitting old IP for up to 24 HOURS because:
  - Their ISP cached the old record for TTL duration
  - Their OS cached it
  - Their browser cached it

Prevention: Set TTL to 300 (5 min) BEFORE making changes.
  Step 1: Change TTL from 86400 → 300 (wait 24h for old TTL to expire)
  Step 2: Change the IP address
  Step 3: Full propagation in ~5 minutes
  Step 4: Optionally increase TTL back to 3600 after confirming
```

### Scenario 2: "My API works locally but times out on EC2"

```
Problem: EC2 can't resolve MongoDB Atlas hostname

Causes:
  1. VPC DNS resolution disabled (enableDnsSupport = false)
  2. VPC DNS hostnames disabled (enableDnsHostnames = false)
  3. Security group blocking outbound UDP port 53 (DNS)
  4. DHCP options set pointing to wrong DNS server

Fix: Check VPC settings:
  aws ec2 describe-vpc-attribute --vpc-id vpc-xxx --attribute enableDnsSupport
  aws ec2 describe-vpc-attribute --vpc-id vpc-xxx --attribute enableDnsHostnames
  Both should be true.
```

---

## How does it actually work?

### DNS Record Types (The Ones You'll Actually Use)

```
┌────────┬────────────────────────────────────────────────────────┐
│ Type   │ Purpose & Example                                     │
├────────┼────────────────────────────────────────────────────────┤
│ A      │ Domain → IPv4 address                                 │
│        │ api.myapp.com → 54.23.189.12                         │
│        │ Used for: EC2 instances, direct IP mapping           │
│        │                                                       │
│ AAAA   │ Domain → IPv6 address                                 │
│        │ api.myapp.com → 2600:1f18:xxxx::1                    │
│        │                                                       │
│ CNAME  │ Domain → another domain (alias)                       │
│        │ www.myapp.com → myapp.com                            │
│        │ api.myapp.com → my-alb-123.us-east-1.elb.amazonaws.com│
│        │ ❌ Cannot be used at zone apex (myapp.com)           │
│        │                                                       │
│ ALIAS  │ Like CNAME but works at zone apex (Route 53 only)    │
│        │ myapp.com → d111xxx.cloudfront.net                   │
│        │ ✅ Can be used at zone apex                           │
│        │                                                       │
│ MX     │ Domain → mail server                                  │
│        │ myapp.com → 10 mail.myapp.com                        │
│        │                                                       │
│ TXT    │ Domain → text data (verification, SPF, DKIM)         │
│        │ myapp.com → "v=spf1 include:_spf.google.com ~all"   │
│        │                                                       │
│ NS     │ Domain → authoritative nameservers                    │
│        │ myapp.com → ns-123.awsdns-45.com                     │
│        │                                                       │
│ SRV    │ Service discovery (used by MongoDB Atlas)             │
│        │ _mongodb._tcp.cluster0.xxxxx.mongodb.net              │
└────────┴────────────────────────────────────────────────────────┘
```

### Route 53 Routing Policies

```
┌─────────────────────────────────────────────────────────────────────┐
│  Policy          │ Use Case                                         │
├──────────────────┼──────────────────────────────────────────────────┤
│  Simple          │ Single resource: api.myapp.com → one ALB        │
│  Weighted        │ A/B testing: 90% → v2, 10% → v3                │
│  Latency         │ Multi-region: closest server to user             │
│  Failover        │ Primary/secondary: primary down → secondary     │
│  Geolocation     │ EU users → EU server, US users → US server      │
│  Multi-value     │ Return multiple IPs (poor man's load balancing) │
├──────────────────┴──────────────────────────────────────────────────┤
│  For your stack:                                                    │
│  - Single region: Simple routing to ALB                            │
│  - Multi-region: Latency-based routing to regional ALBs           │
│  - Blue/green deployments: Weighted routing (0% → 100% shift)    │
│  - DR: Failover routing with health checks                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Visual Diagram — DNS Resolution Chain

```
Browser: "What is the IP of api.myapp.com?"

Browser Cache ──→ OS Cache ──→ Router ──→ ISP Resolver
     │                │           │            │
   MISS             MISS        MISS          │
                                         ┌────▼────┐
                                         │ Root DNS│ "Try .com servers"
                                         │ (.)     │
                                         └────┬────┘
                                              │
                                         ┌────▼────┐
                                         │.com TLD │ "Try Route 53"
                                         │ DNS     │
                                         └────┬────┘
                                              │
                                         ┌────▼────────────────┐
                                         │ Route 53            │
                                         │ (authoritative for  │
                                         │  myapp.com)         │
                                         │                     │
                                         │ api.myapp.com       │
                                         │ → ALIAS → ALB DNS   │
                                         │ → A → 54.23.189.12  │
                                         └────┬────────────────┘
                                              │
                                    Answer: 54.23.189.12
                               Cached for TTL (e.g., 300 seconds)
```

---

## Commands & Debugging Tools

```bash
# Basic DNS lookup
nslookup api.myapp.com
dig api.myapp.com

# Detailed DNS lookup (dig is more powerful)
dig api.myapp.com +short          # Just the IP
dig api.myapp.com +trace          # Full resolution chain (root → TLD → auth)
dig api.myapp.com A               # IPv4 records
dig api.myapp.com AAAA            # IPv6 records
dig api.myapp.com CNAME           # CNAME records
dig api.myapp.com MX              # Mail records
dig api.myapp.com NS              # Nameservers
dig api.myapp.com TXT             # TXT records (SPF, DKIM)
dig api.myapp.com ANY             # All records

# Query specific DNS server
dig @8.8.8.8 api.myapp.com       # Ask Google DNS
dig @1.1.1.1 api.myapp.com       # Ask Cloudflare DNS
dig @ns-123.awsdns-45.com api.myapp.com  # Ask Route 53 directly

# Check TTL
dig api.myapp.com | grep -i ttl
# TTL decreases as cache ages: 300 → 299 → 298...

# DNS timing
dig api.myapp.com | grep "Query time"
# ;; Query time: 23 msec (cached)
# ;; Query time: 150 msec (not cached, full resolution)

# Flush DNS cache
# Windows:
ipconfig /flushdns
# Mac:
sudo dsdncacheutil -flushcache
# Linux:
sudo systemd-resolve --flush-caches

# Check DNS propagation worldwide:
# https://dnschecker.org/
```

---

## Node.js Implementation

```javascript
const dns = require('dns');
const { performance } = require('perf_hooks');

// ──── DNS Resolution with Timing ────
async function dnsLookup(hostname) {
  // Method 1: OS-level resolution (uses /etc/hosts, OS cache)
  const start1 = performance.now();
  const { address, family } = await dns.promises.lookup(hostname);
  const time1 = performance.now() - start1;
  
  console.log(`dns.lookup:  ${hostname} → ${address} (IPv${family}) [${time1.toFixed(1)}ms]`);
  console.log(`  (Uses OS resolver — checks /etc/hosts, OS cache first)`);
  
  // Method 2: Direct DNS query (bypasses OS cache)
  const start2 = performance.now();
  const addresses = await dns.promises.resolve4(hostname);
  const time2 = performance.now() - start2;
  
  console.log(`dns.resolve: ${hostname} → ${addresses.join(', ')} [${time2.toFixed(1)}ms]`);
  console.log(`  (Direct DNS query — always hits DNS server)\n`);
}

// ──── Full DNS Record Inspection ────
async function inspectDomain(domain) {
  console.log(`\n═══ DNS Records for ${domain} ═══\n`);
  
  try {
    const a = await dns.promises.resolve4(domain);
    console.log(`A (IPv4):     ${a.join(', ')}`);
  } catch { console.log('A: none'); }
  
  try {
    const cname = await dns.promises.resolveCname(domain);
    console.log(`CNAME:        ${cname.join(', ')}`);
  } catch { console.log('CNAME: none (direct A record)'); }
  
  try {
    const ns = await dns.promises.resolveNs(domain);
    console.log(`NS:           ${ns.join(', ')}`);
  } catch { console.log('NS: none'); }
  
  try {
    const mx = await dns.promises.resolveMx(domain);
    console.log(`MX (mail):    ${mx.map(r => `${r.priority} ${r.exchange}`).join(', ')}`);
  } catch { console.log('MX: none'); }
  
  try {
    const txt = await dns.promises.resolveTxt(domain);
    console.log(`TXT:          ${txt.map(r => r.join('')).join('\n              ')}`);
  } catch { console.log('TXT: none'); }
}

// ──── DNS Prefetching (Performance Optimization) ────
function prefetchDNS(hostnames) {
  console.log('\nPrefetching DNS for:', hostnames);
  return Promise.all(
    hostnames.map(async (host) => {
      const start = performance.now();
      try {
        const { address } = await dns.promises.lookup(host);
        console.log(`  ✅ ${host} → ${address} (${(performance.now() - start).toFixed(1)}ms)`);
      } catch (err) {
        console.log(`  ❌ ${host}: ${err.message}`);
      }
    })
  );
}

// Run diagnostics
(async () => {
  await dnsLookup('google.com');
  await dnsLookup('api.github.com');
  await inspectDomain('google.com');
  
  // Prefetch DNS for services your app connects to
  await prefetchDNS([
    'cluster0.xxxxx.mongodb.net',  // MongoDB Atlas
    'my-cache.xxxxx.cache.amazonaws.com', // ElastiCache
    'api.stripe.com',  // Payment provider
    's3.us-east-1.amazonaws.com'  // S3
  ]);
})();
```

### DNS Prefetching in Next.js

```html
<!-- In your Next.js _document.js or head -->
<head>
  <!-- Prefetch DNS for external APIs your app calls -->
  <link rel="dns-prefetch" href="https://api.stripe.com" />
  <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
  <link rel="dns-prefetch" href="https://cdn.myapp.com" />
  
  <!-- Preconnect: DNS + TCP + TLS (even faster) -->
  <link rel="preconnect" href="https://api.myapp.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
</head>
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────────┐
│  DNS Performance Impact                                          │
├───────────────────────────┬──────────────────────────────────────┤
│  Cached DNS lookup        │ < 1ms                                │
│  ISP resolver (cached)    │ 5-20ms                               │
│  Full recursive lookup    │ 50-200ms                             │
│  DNS failure + retry      │ 5-30 SECONDS (devastating)           │
├───────────────────────────┴──────────────────────────────────────┤
│                                                                  │
│  Optimization strategies:                                        │
│  1. DNS prefetching in HTML (<link rel="dns-prefetch">)         │
│  2. Low TTL before changes, higher after (300 → 3600)           │
│  3. Use ALIAS instead of CNAME at zone apex (one less lookup)   │
│  4. Health checks + failover in Route 53                        │
│  5. Connection keep-alive (avoid re-resolution)                  │
│  6. Node.js dns cache (dns.setDefaultResultOrder('ipv4first'))  │
│                                                                  │
│  Fun fact: Chrome caches DNS for 60 seconds.                    │
│  Node.js does NOT cache DNS by default!                          │
│  Use a library like 'cacheable-lookup' for Node.js DNS caching. │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Node.js DNS Not Cached

```javascript
// ❌ Node.js resolves DNS on EVERY HTTP request (no built-in cache)
// 100 requests to api.stripe.com = 100 DNS lookups

// ✅ Install cacheable-lookup
const CacheableLookup = require('cacheable-lookup');
const cacheable = new CacheableLookup();
cacheable.install(require('http').globalAgent);
cacheable.install(require('https').globalAgent);
// Now DNS is cached for TTL duration
```

### ❌ Using IP Addresses Instead of DNS Names

```javascript
// ❌ Hardcoded IP — breaks when server changes
mongoose.connect('mongodb://54.23.189.12:27017/mydb');

// ✅ Use DNS hostname — automatically resolves to current IP
mongoose.connect('mongodb+srv://cluster0.xxxxx.mongodb.net/mydb');
// MongoDB Atlas uses SRV DNS records for automatic discovery
```

---

## Practice Exercises

### Exercise 1: DNS Discovery
Use `dig` to find all DNS records for `amazon.com`. How many A records does it have? Why multiple?

### Exercise 2: TTL Observation
Run `dig google.com` twice, 30 seconds apart. Watch the TTL decrease. Calculate the original TTL.

### Exercise 3: DNS Latency
Compare DNS resolution time for `google.com` using different resolvers: `8.8.8.8`, `1.1.1.1`, and your ISP's default. Which is fastest?

---

## Interview Q&A

**Q1: How does DNS resolution work step by step?**
> Browser cache → OS cache → Recursive resolver (ISP) → Root server (.com referral) → TLD server (myapp.com referral) → Authoritative nameserver (returns IP). Results cached at each level based on TTL.

**Q2: What's the difference between CNAME and ALIAS records?**
> CNAME maps a domain to another domain (adds one DNS lookup). Cannot be used at zone apex (myapp.com). ALIAS (Route 53) resolves at the DNS level — returns the final IP directly. Can be used at zone apex. ALIAS is faster (one fewer lookup).

**Q3: How does DNS affect application performance?**
> First DNS lookup adds 50-200ms. Node.js doesn't cache DNS by default (unlike browsers). Each new hostname requires a new lookup. Solutions: DNS prefetch, connection keep-alive, cacheable-lookup module, preconnect hints.

**Q4: What happens when a DNS server goes down?**
> If your authoritative DNS is down, new lookups fail. Cached lookups continue until TTL expires. Route 53 has 100% SLA with 4 nameservers per hosted zone. For self-hosted DNS, this is a single point of failure.

**Q5: How does MongoDB Atlas use DNS (SRV records)?**
> Atlas uses SRV DNS records (`_mongodb._tcp.cluster0.xxxxx.mongodb.net`) that return a list of all replica set members with ports and priorities. The driver queries SRV on connect, discovers all nodes, and handles failover automatically. This is why the `mongodb+srv://` connection string works.
