# Debugging Network Issues

> 📌 **File:** 20_Debugging_Network_Issues.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Network debugging is the art of finding WHERE in the network stack a problem lives. As a full-stack dev, you'll face: slow APIs, connection timeouts, DNS failures, TLS errors, WebSocket drops, and 502s. This chapter gives you a systematic methodology and the exact commands to diagnose each layer.

---

## The Debugging Methodology

```
┌──────────────────────────────────────────────────────────────────┐
│  Step 1: IDENTIFY the symptom                                   │
│    "Slow API" / "Connection refused" / "502 Bad Gateway"        │
│                                                                  │
│  Step 2: ISOLATE the layer (work bottom-up)                     │
│    DNS → IP connectivity → TCP → TLS → HTTP → Application      │
│                                                                  │
│  Step 3: REPRODUCE with debugging tools                         │
│    curl -v / tcpdump / dig / netstat / logs                     │
│                                                                  │
│  Step 4: FIX the root cause                                     │
│    Not the symptom. Not a workaround. The root cause.           │
│                                                                  │
│  Step 5: VERIFY the fix                                          │
│    Same test that revealed the problem should now pass.         │
└──────────────────────────────────────────────────────────────────┘
```

---

## Layer-by-Layer Debugging

### Layer 1: DNS — "Can we resolve the hostname?"

```bash
# Symptom: ERR_NAME_NOT_RESOLVED, ENOTFOUND, getaddrinfo ENOTFOUND

# Test DNS resolution
dig api.myapp.com +short
nslookup api.myapp.com

# If returns nothing or NXDOMAIN:
# → Domain doesn't exist or DNS is down
# → Check Route 53 hosted zone
# → Check VPC DNS settings (enableDnsSupport)

# Compare DNS servers
dig @8.8.8.8 api.myapp.com    # Google DNS
dig @1.1.1.1 api.myapp.com    # Cloudflare DNS
# If one works but not the other → DNS propagation issue

# Check TTL (is an old record cached?)
dig api.myapp.com | grep TTL

# Flush local DNS cache
ipconfig /flushdns               # Windows
sudo dscacheutil -flushcache     # Mac
sudo systemd-resolve --flush-caches  # Linux

# Node.js DNS issue
node -e "require('dns').lookup('api.myapp.com', console.log)"
# If this fails but dig works → Node.js using different resolver
```

### Layer 2: IP Connectivity — "Can packets reach the server?"

```bash
# Symptom: EHOSTUNREACH, ENETUNREACH, request timeout

# Basic connectivity
ping -c 4 54.23.189.12           # Test with IP (bypasses DNS)
ping -c 4 api.myapp.com          # Test with hostname

# If ping fails:
# → Security group blocking ICMP (common on AWS — not necessarily broken!)
# → Use TCP test instead:
nc -zv 54.23.189.12 443          # Test TCP port 443
curl -o /dev/null -s -w "%{http_code}" https://api.myapp.com  # HTTP test

# Trace the route
traceroute api.myapp.com         # Linux/Mac
tracert api.myapp.com            # Windows
mtr api.myapp.com                # Continuous traceroute

# Look for:
# * * * = router not responding (often firewalls, not necessarily broken)
# High latency jump = slow link or geographic distance
# Packet loss = network congestion or faulty router
```

### Layer 3: TCP — "Can we establish a connection?"

```bash
# Symptom: ECONNREFUSED, ETIMEDOUT, ECONNRESET

# Test TCP connectivity to specific port
nc -zv api.myapp.com 443        # HTTPS
nc -zv api.myapp.com 3000       # Node.js direct
nc -zv db-host 27017            # MongoDB
nc -zv redis-host 6379          # Redis
nc -zv rds-host 5432            # PostgreSQL

# ECONNREFUSED = port not listening (service down, wrong port)
# ETIMEDOUT = packets not reaching (firewall, wrong IP, SG blocking)
# ECONNRESET = connection killed (LB timeout, server crash)

# Check what's listening
netstat -tlnp | grep 3000       # Linux: who's listening on 3000?
ss -tlnp | grep 3000            # Linux (modern)
netstat -an | findstr 3000      # Windows

# Check connection states
ss -s                            # Summary of all connections
netstat -an | awk '{print $6}' | sort | uniq -c | sort -rn
# Result: ESTABLISHED (150), TIME_WAIT (45), CLOSE_WAIT (10)
# CLOSE_WAIT accumulating = your app isn't closing connections!
```

### Layer 4: TLS — "Is encryption working?"

```bash
# Symptom: ERR_CERT_AUTHORITY_INVALID, UNABLE_TO_VERIFY_LEAF_SIGNATURE

# Test TLS handshake
openssl s_client -connect api.myapp.com:443 -servername api.myapp.com

# Check certificate validity
echo | openssl s_client -connect api.myapp.com:443 2>/dev/null | \
  openssl x509 -noout -dates -subject -issuer

# Common TLS errors:
# "certificate has expired" → Renew cert (certbot renew)
# "self signed certificate" → Missing CA in trust store
# "hostname mismatch" → Cert doesn't include this domain in SAN
# "unable to verify" → Missing intermediate certificate

# Check cert chain completeness
openssl s_client -connect api.myapp.com:443 -showcerts

# curl with verbose TLS info
curl -vvv https://api.myapp.com 2>&1 | grep -E "SSL|TLS|certificate|verify"
```

### Layer 5: HTTP — "Is the application responding correctly?"

```bash
# Symptom: 4xx/5xx status codes, slow responses, wrong content

# Full request/response details
curl -v https://api.myapp.com/api/health

# Timing breakdown
curl -w "\n---TIMING---\nDNS:        %{time_namelookup}s\nConnect:    %{time_connect}s\nTLS:        %{time_appconnect}s\nFirstByte:  %{time_starttransfer}s\nTotal:      %{time_total}s\nHTTP Code:  %{http_code}\nSize:       %{size_download} bytes\n" \
  -o /dev/null -s https://api.myapp.com/api/health

# Interpret timing:
# DNS slow (> 100ms)    → DNS resolver issue, add caching
# Connect slow (> 50ms) → Server far away or overloaded
# TLS slow (> 200ms)    → TLS 1.2 (upgrade to 1.3), or server far
# FirstByte slow        → Application processing (slow DB query, bad code)
# Total large vs FirstByte → Large response body, check compression

# Check specific headers
curl -I https://api.myapp.com/api/products
# Look for: Content-Encoding (gzip?), Cache-Control, X-Response-Time

# Test with different methods
curl -X POST https://api.myapp.com/api/orders \
  -H "Content-Type: application/json" \
  -d '{"productId":"123"}' -v
```

### Layer 6: Application — "Is your code correct?"

```javascript
// ──── Add request timing to Express ────
app.use((req, res, next) => {
  const start = process.hrtime.bigint();
  
  res.on('finish', () => {
    const duration = Number(process.hrtime.bigint() - start) / 1e6; // ms
    
    if (duration > 1000) {
      console.warn(`⚠️ SLOW REQUEST: ${req.method} ${req.url} — ${duration.toFixed(0)}ms`);
    }
    
    console.log(JSON.stringify({
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: `${duration.toFixed(1)}ms`,
      ip: req.ip,
      userAgent: req.headers['user-agent']?.substring(0, 50)
    }));
  });
  
  next();
});

// ──── Database query timing ────
mongoose.set('debug', (collectionName, method, query, doc, options) => {
  const start = Date.now();
  // This logs after the query completes
  console.log(`MongoDB: ${collectionName}.${method} — ${Date.now() - start}ms`);
});

// ──── Catch unhandled promise rejections ────
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
  // Don't crash — log and monitor
});

// ──── Catch uncaught exceptions ────
process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  // Graceful shutdown
  process.exit(1);
});
```

---

## Common Production Issues — Diagnosis Playbook

### Issue: 502 Bad Gateway

```
Symptom: ALB returns 502
Meaning: ALB cannot reach your Node.js backend

Diagnosis:
  1. Is Node.js running?
     ssh ec2 → pm2 status → is it online?
     
  2. Is it listening on the right port?
     ss -tlnp | grep 3000
     
  3. Can ALB reach the port?
     Security group: inbound 3000 from ALB SG?
     
  4. Is keepAliveTimeout causing issues?
     Node.js keepAliveTimeout < ALB idle timeout → 502!
     Fix: server.keepAliveTimeout = 65000;
     
  5. Is the app crashing on certain requests?
     Check pm2 logs → look for uncaught exceptions
     
  6. Is the health check failing?
     curl http://localhost:3000/health from EC2
```

### Issue: 504 Gateway Timeout

```
Symptom: ALB returns 504 after 60 seconds
Meaning: Your backend didn't respond within ALB's idle timeout

Diagnosis:
  1. What's the slow query?
     Add request timing middleware → find requests > 60s
     
  2. Is it a database issue?
     Enable MongoDB profiler: db.setProfilingLevel(1, {slowms: 100})
     Check PostgreSQL slow query log
     
  3. Is it an external API call?
     Set timeouts on all axios/fetch calls: { timeout: 10000 }
     
  4. Is it a Node.js event loop block?
     Blocked event loop = ALL requests stall
     Check with: process._getActiveHandles().length
     
  Fix:
  - Add timeouts at every level
  - Offload slow operations to a queue (SQS)
  - Return 202 Accepted for long operations
```

### Issue: WebSocket Disconnects

```
Symptom: Socket.IO clients frequently reconnect

Diagnosis:
  1. Check disconnect reason:
     socket.on('disconnect', (reason) => console.log(reason));
     
  "transport close" → Connection killed by intermediary
    → ALB idle timeout (60s) vs ping interval (25s)
    → Fix: ALB timeout > Socket.IO ping interval
    
  "ping timeout" → Server didn't respond to ping
    → Server overloaded (event loop blocked)
    → Fix: Optimize, or increase pingTimeout
    
  "transport error" → Network issue
    → Unstable network, mobile switching WiFi/cellular
    → Fix: Socket.IO auto-reconnects (ensure enabled)
    
  2. Check Nginx config for WebSocket:
     Must have: proxy_set_header Upgrade $http_upgrade;
     proxy_read_timeout must be very high (86400s)
```

### Issue: Slow API for Some Users

```
Symptom: API fast in US, slow in India (300ms → 1200ms)

Diagnosis:
  curl -w "DNS:%{time_namelookup} TCP:%{time_connect} TLS:%{time_appconnect} 
  TTFB:%{time_starttransfer} Total:%{time_total}\n" \
  -o /dev/null -s https://api.myapp.com/api/products

  From US:   DNS:0.01 TCP:0.02 TLS:0.04 TTFB:0.10 Total:0.12
  From India: DNS:0.05 TCP:0.15 TLS:0.35 TTFB:0.80 Total:0.95
  
  TCP + TLS = 0.50s from India (3 × 150ms RTT!)
  
  Fix:
  1. CloudFront CDN (terminate TLS at nearest edge)
  2. Redis cache (reduce TTFB from 0.80 to 0.20)
  3. Multi-region deployment (deploy to ap-south-1 for India)
  4. HTTP/2 (multiplex requests, reduce round trips)
```

---

## The Debug Toolkit Cheatsheet

```
┌──────────────────────────────────────────────────────────────────┐
│  Symptom                    │ First Command                     │
├─────────────────────────────┼───────────────────────────────────┤
│  "Can't connect"            │ nc -zv host port                  │
│  "DNS not resolving"        │ dig domain +short                 │
│  "Slow response"            │ curl -w timing-format URL         │
│  "Connection dropped"       │ tcpdump -i any port X             │
│  "SSL error"                │ openssl s_client -connect host:443│
│  "502 Bad Gateway"          │ curl http://localhost:3000/health  │
│  "Too many connections"     │ ss -s                             │
│  "Port already in use"      │ lsof -i :3000 / netstat -tlnp    │
│  "What's my IP"             │ curl ifconfig.me                  │
│  "Route to host"            │ traceroute host                   │
│  "Packet loss"              │ mtr host                          │
│  "What headers returned"    │ curl -I URL                       │
│  "Is websocket upgrading"   │ curl -v -H "Upgrade: websocket"  │
│  "DB connection failing"    │ nc -zv db-host db-port            │
└─────────────────────────────┴───────────────────────────────────┘
```

---

## Node.js — Built-in Diagnostics

```javascript
// ──── Monitor event loop lag (detect blocking code) ────
let lastCheck = Date.now();
setInterval(() => {
  const now = Date.now();
  const lag = now - lastCheck - 1000; // Expected 1000ms interval
  if (lag > 100) {
    console.warn(`⚠️ Event loop lag: ${lag}ms — possible blocking operation!`);
  }
  lastCheck = now;
}, 1000);

// ──── Monitor memory usage ────
setInterval(() => {
  const mem = process.memoryUsage();
  const heapUsedMB = (mem.heapUsed / 1024 / 1024).toFixed(1);
  const heapTotalMB = (mem.heapTotal / 1024 / 1024).toFixed(1);
  const rssMB = (mem.rss / 1024 / 1024).toFixed(1);
  
  if (mem.heapUsed / mem.heapTotal > 0.85) {
    console.warn(`⚠️ High memory: ${heapUsedMB}/${heapTotalMB}MB (RSS: ${rssMB}MB)`);
  }
}, 30000);

// ──── Active handles and requests ────
function diagnostics() {
  return {
    activeHandles: process._getActiveHandles().length,
    activeRequests: process._getActiveRequests().length,
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    cpu: process.cpuUsage(),
    pid: process.pid
  };
}

app.get('/debug/diagnostics', (req, res) => {
  res.json(diagnostics());
});
```

---

## Practice Exercises

### Exercise 1: Full Debug Flow
Intentionally break your API (stop MongoDB) and use the layer-by-layer debugging method to identify the problem without looking at the app logs first.

### Exercise 2: Timing Analysis
Use `curl -w` to measure timing for 5 different websites. Create a comparison table of DNS, TCP, TLS, and TTFB times. Explain the differences.

### Exercise 3: Connection State Audit
Run your Express server under load (use `autocannon`). Monitor connection states with `ss`. Identify TIME_WAIT, CLOSE_WAIT, and ESTABLISHED counts. Are any problematic?

---

## Interview Q&A

**Q1: How do you debug a slow API endpoint?**
> Layer-by-layer: `curl -w` timing (DNS/TCP/TLS/TTFB). If TTFB is slow → application layer. Add request timing middleware. Check database query times. Check external API calls. Profile event loop lag. Use `explain()` on database queries.

**Q2: What causes 502 Bad Gateway and how do you fix it?**
> The reverse proxy (ALB/Nginx) cannot reach the backend. Causes: Node.js crashed, wrong port, security group blocking, keepAliveTimeout mismatch (Node.js closes before ALB). Fix: check process status, verify ports, align timeout settings (Node.js keepAliveTimeout > ALB idle timeout).

**Q3: How do you diagnose intermittent connection failures?**
> Capture with tcpdump during failure window. Check for RST packets (connection reset), retransmissions (packet loss), or FIN (unexpected close). Check NAT gateway idle timeout (350s for AWS). Check load balancer connection draining. Add structured logging with timestamps to correlate events.

**Q4: How do you find out what's blocking the Node.js event loop?**
> Monitor event loop lag with a periodic timer. A lag > 100ms indicates blocking code. Use `--inspect` flag + Chrome DevTools profiler. Check for: synchronous file I/O, CPU-intensive computation, large JSON parsing, blocking database drivers. Move heavy work to worker threads.

**Q5: What tools do you use for network debugging in production?**
> `curl -v`/`curl -w` (HTTP debugging + timing), `tcpdump`/Wireshark (packet capture), `ss`/`netstat` (connection states), `dig`/`nslookup` (DNS), `traceroute`/`mtr` (path analysis), CloudWatch/Datadog (metrics + logs), and application-level logging with request IDs for distributed tracing.
