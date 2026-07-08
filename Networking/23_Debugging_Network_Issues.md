# Debugging Network Issues

> 📌 **File:** 23_Debugging_Network_Issues.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Network debugging is the art of finding WHERE in the network stack a problem lives. As a full-stack dev, you'll face: slow APIs, connection timeouts, DNS failures, TLS errors, WebSocket drops, and 502s. This chapter gives you a systematic methodology and the exact commands to diagnose each layer.

---

## The Debugging Methodology

```
┌──────────────────────────────────────────────────────────────────┐
│  Step 1: IDENTIFY the symptom                                   │
│  Step 2: ISOLATE the layer (work bottom-up)                     │
│    DNS → IP connectivity → TCP → TLS → HTTP → Application      │
│  Step 3: REPRODUCE with debugging tools                         │
│  Step 4: FIX the root cause                                     │
│  Step 5: VERIFY the fix                                          │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Detective's Filter)
Think of network debugging like solving a water leak in a 5-story building:
- You start by checking the main water valve first (Layer 1: DNS), then the main pipes (Layer 2: IPs), then the individual floor's valve (Layer 3: TCP), then the specific room's faucet (Layer 5: HTTP).
- If you start ripping open the drywall on the 5th floor (Layer 6: Application code) without checking if the city turned off the water main (DNS errors), you waste hours of your life!

---

## Layer-by-Layer Debugging

### Layer 1: DNS
```bash
# Test DNS resolution
dig api.myapp.com +short
nslookup api.myapp.com

# Compare DNS servers
dig @8.8.8.8 api.myapp.com    # Google DNS
dig @1.1.1.1 api.myapp.com    # Cloudflare DNS

# Flush local DNS cache
ipconfig /flushdns               # Windows
sudo systemd-resolve --flush-caches  # Linux
```

### Layer 2: IP Connectivity
```bash
# Basic connectivity (ping can be blocked by firewalls)
ping -c 4 54.23.189.12
ping -c 4 api.myapp.com

# Use TCP test instead
nc -zv 54.23.189.12 443

# Trace the route
traceroute api.myapp.com         # Linux/Mac
tracert api.myapp.com            # Windows
```

### Layer 3: TCP
```bash
# Test TCP connectivity to specific ports
nc -zv api.myapp.com 443        # HTTPS
nc -zv db-host 27017            # MongoDB
nc -zv redis-host 6379          # Redis

# Check what's listening
netstat -tlnp | grep 3000       # Linux
ss -tlnp | grep 3000            # Linux (modern)
```

### Layer 4: TLS
```bash
# Test TLS handshake
openssl s_client -connect api.myapp.com:443 -servername api.myapp.com

# Check certificate dates and issuer
echo | openssl s_client -connect api.myapp.com:443 2>/dev/null | \
  openssl x509 -noout -dates -subject -issuer
```

### Layer 5: HTTP
```bash
# Full request/response details
curl -v https://api.myapp.com/api/health

# Timing breakdown
curl -w "\n---TIMING---\nDNS:        %{time_namelookup}s\nConnect:    %{time_connect}s\nTLS:        %{time_appconnect}s\nFirstByte:  %{time_starttransfer}s\nTotal:      %{time_total}s\n" \
  -o /dev/null -s https://api.myapp.com/api/health
```

---

## Common Production Issues — Diagnosis Playbook

### Issue: 502 Bad Gateway
- **Meaning:** ALB/Nginx cannot reach your Node.js backend.
- **Diagnosis:** Check if Node.js is running, listening on the right port (`ss -tlnp`), check security group rules, check for Node.js keepAliveTimeout mismatch (Node.js timeout must be > ALB timeout).

### Issue: 504 Gateway Timeout
- **Meaning:** Backend didn't respond within ALB's timeout limit.
- **Diagnosis:** Identify the slow request using timing middleware, profile slow database queries, verify external API timeouts.

---

## Practice Exercises

### Exercise 1: Timing Analysis
Use `curl -w` to measure your API's DNS, TCP, TLS, and TTFB times. Compare localhost vs public production API.

### Exercise 2: Simulated Outage
Turn off your local MongoDB instance. Attempt an API request and use the layer-by-layer debugging method to isolate the database port failure.

---

## Interview Q&A

**Q1: How do you debug a slow API endpoint?**
> Use `curl -w` to get a timing breakdown (DNS/TCP/TLS/TTFB). If TTFB is slow, the bottleneck is in the application. Add timing logs around database queries and external HTTP requests. Use query explanation on slow queries.

**Q2: What causes 502 Bad Gateway and how do you fix it?**
> The reverse proxy cannot reach the backend. Causes: Node.js crashed, wrong port, security group blocking, keepAliveTimeout mismatch (Node.js closes before ALB). Fix: check process status, verify ports, align timeout settings.

**Q3: How do you diagnose intermittent connection failures?**
> Capture packets with tcpdump. Check for unexpected RST packets, retransmissions, or FIN packets. Check for NAT gateway idle timeouts (350s for AWS) or load balancer connection draining settings.

**Q4: How do you find out what's blocking the Node.js event loop?**
> Monitor event loop lag with a periodic timer. A lag > 100ms indicates blocking code. Use the `--inspect` flag to run CPU profiling. Look for synchronous file I/O, heavy JSON serialization/deserialization, or CPU-bound algorithms.

**Q5: What tools do you use for network debugging in production?**
> `curl -v` / `curl -w` (HTTP details & timing), `tcpdump` / Wireshark (packet capture), `ss` (connections), `dig` (DNS resolution), and `traceroute` (route path analysis).

---

Prev : [22 VPC Architecture And Design](./22_VPC_Architecture_And_Design.md) | Index: [00 Index](./00_Index.md) | Next : [24 Performance Optimization](./24_Performance_Optimization.md)
