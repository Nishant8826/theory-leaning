# 🌐 Networking & Internet Architecture – Complete Revision Guide

Welcome to the Complete Networking & Internet Architecture Revision Guide. This guide aggregates all key concepts, commands, configurations, best practices, and interview questions across the entire module from a single high-density file. It is designed to serve as a comprehensive, production-ready checklist to help you revise the entire networking stack in under 30 minutes.

---

## 📌 Module Navigation

* [01. Introduction & Setup](#01-introduction--setup)
* [02. How The Internet Actually Works](#02-how-the-internet-actually-works)
* [03. OSI Model Vs Real World](#03-osi-model-vs-real-world)
* [04. TCP/IP Model](#04-tcpip-model)
* [05. IP Addressing & Subnetting](#05-ip-addressing--subnetting)
* [06. DNS Deep Dive](#06-dns-deep-dive)
* [07. HTTP/HTTPS Internals](#07-httphttps-internals)
* [08. TCP Deep Dive](#08-tcp-deep-dive)
* [09. UDP & When To Use It](#09-udp--when-to-use-it)
* [10. TLS/SSL Handshake](#10-tlsssl-handshake)
* [11. Routing & NAT](#11-routing--nat)
* [12. Load Balancing](#12-load-balancing)
* [13. Firewalls & Security](#13-firewalls--security)
* [14. Proxies & Reverse Proxies](#14-proxies--reverse-proxies)
* [15. CDN & Caching](#15-cdn--caching)
* [16. WebSockets & Real-Time](#16-websockets--real-time)
* [17. API Gateways](#17-api-gateways)
* [18. Microservices Networking](#18-microservices-networking)
* [19. Containers & Networking](#19-containers--networking)
* [20. Kubernetes Networking](#20-kubernetes-networking)
* [21. Debugging Network Issues](#21-debugging-network-issues)
* [22. Performance Optimization](#22-performance-optimization)
* [23. Database Networking](#23-database-networking)
* [24. VPC Architecture & Design](#24-vpc-architecture--design)
* [25. Network Monitoring & Observability](#25-network-monitoring--observability)
* [26. Deployment & Production Infrastructure](#26-deployment--production-infrastructure)

---

## 01. Introduction & Setup

🔗 **Full Lesson:** [01_Introduction_And_Setup.md](./01_Introduction_And_Setup.md)

* **What**: Guides developers in setting up network inspection and troubleshooting tools (Wireshark, curl, netstat, nmap, nslookup, etc.) and building a test project (Express API + WebSocket Server) to visualize real-world networking traffic.
* **Why It Exists**: High-level application code hides the underlying layers (DNS, TCP, TLS, HTTP/WS, IP/routing), making it hard to debug latency, dropped connections, or caching issues. This setup provides hands-on tools to observe what's actually happening beneath application code.
* **Key Concepts**:
  * **Tooling Stack**:
    * `curl`: Performs HTTP requests via CLI; `-v` enables verbose output (headers, TLS, IP addresses) and `-w` prints custom timing metrics.
    * `ping`: Tests basic connectivity using ICMP echo requests.
    * `traceroute`/`tracert`: Identifies hops (routers) along the path to a destination IP.
    * `nslookup`/`dig`: Queries DNS servers to resolve domain names to IP addresses.
    * `netstat`/`ss`: Displays active TCP/UDP connections and ports listening (e.g., `netstat -an | grep 3000`).
    * `tcpdump`/`Wireshark`: Captures and inspects raw packets on the wire to debug handshakes, connection drops, and protocols.
    * `nmap`: Scans ports to discover open services and verify firewall rules.
    * `mtr`: Combines live ping and traceroute diagnostics.
    * `openssl s_client`: Diagnoses TLS/SSL handshakes and certificate chains.
  * **Node.js Express Server Setup**:
    * Uses `express`, `socket.io`, `cors`, `redis`, `mongoose`.
    * Endpoints like `/api/health` (inspects headers, connection type, IP), `/api/slow` (tests connection timeouts), and `/api/echo` (exposes IP, headers, local/remote ports).
    * Remote/local port diagnostics: remote port shows the browser's dynamic port, local port shows the server's listening port (3000).

### Key Commands / Code Example:

```bash
# Check verbose HTTP requests with custom timing outputs
curl -v http://localhost:3000/api/health
curl -w "\nDNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTLS: %{time_appconnect}s\nFirst Byte: %{time_starttransfer}s\nTotal: %{time_total}s\n" -o /dev/null -s https://httpbin.org/get

# Check which process is listening on Port 3000
netstat -an | grep 3000

# Test if port 443 is open on target server
nc -zv google.com 443
```

> [!NOTE]
> When running the Express backend behind reverse proxies or load balancers, client IPs retrieved via `req.ip` might show the proxy's IP. Enable `app.set('trust proxy', true)` to read the correct client IP from the `X-Forwarded-For` header.

---

## 02. How The Internet Actually Works

🔗 **Full Lesson:** [02_How_The_Internet_Actually_Works.md](./02_How_The_Internet_Actually_Works.md)

* **What**: Traces the physical and conceptual journey of data packets over fiber cables, routers, and DNS servers, detailing the complete lifecycle of a web request.
* **Why It Exists**: Information is bound by physics; data must be fragmented into packets and travel across physical distances, introducing latency. Understanding these components is critical for diagnosing performance, websocket drops, and timeout mismatches.
* **Key Concepts**:
  * **The Request Lifecycle**: Traces the steps of typing `https://myapp.com` (DNS resolution (Lesson 06) -> TCP 3-way handshake -> TLS handshake -> HTTP request/response -> browser rendering -> API calls).
  * **Undersea Cables & Light Speed**: Latency is physically limited by the speed of light in fiber (~200,000 km/s). NYC to Mumbai theoretical minimum is ~130ms; real RTT is ~160-200ms due to routing/processing.
  * **Websocket Drops**: Mid-route gateways (NATs/ALBs) drop idle connections after a timeout (AWS ALB: 60s, NAT Gateway: 350s). Solved with regular client-server heartbeats (Socket.IO default: 25s).
  * **Timeout mismatches**: If backend timeouts are not aligned (Node.js timeout > ALB idle timeout of 60s > MongoDB query timeout of 30s), a slow database query causes a 504 error while backend resources remain blocked.
  * **Parallelism**: Avoid sequential API calls in code (`await fetch(...)` one by one) to reduce total RTT by leveraging `Promise.all`.
  * **Connection Pooling**: Creating new TCP/TLS connections is slow. Reusing connections via pooling (MongoDB, Redis, keep-alive) eliminates handshake overhead.

### Key Commands / Code Example:

```javascript
// Parallel requests to avoid RTT stack-up
const [user, orders, products] = await Promise.all([
  fetch('/api/user'),
  fetch('/api/orders'),
  fetch('/api/products')
]);

// Connection Pool setup in MongoDB Atlas (reused connection)
const client = new MongoClient(uri, { maxPoolSize: 10 });
await client.connect(); // Establish once at startup
```

> [!IMPORTANT]
> On Node.js version 18 or older, `keepAlive` is `false` by default on HTTP agents, meaning every fetch/axios request makes a new TCP handshake. Explicitly enable `{ keepAlive: true }` in your HTTP agents on Node v18 or older.

---

## 03. OSI Model Vs Real World

🔗 **Full Lesson:** [03_OSI_Model_Vs_Real_World.md](./03_OSI_Model_Vs_Real_World.md)

* **What**: Compares the academic 7-layer OSI model to the real-world 4-5 layer TCP/IP stack, mapping cloud services and code variables to their respective layers.
* **Why It Exists**: Systematically troubleshooting "slowness" or "connection dropped" requires isolating which layer is failing (e.g., routing at Layer 3, port conflicts at Layer 4, encryption at Layer 5/6, or code at Layer 7).
* **Key Concepts**:
  * **Layer Mapping**:
    * L7: Application (HTTP, WebSockets, DB wire protocols).
    * L6: Presentation (JSON stringify/parse, TLS encryption, Gzip compression).
    * L5: Session (JWT/cookie session tracking, TLS session resumption).
    * L4: Transport (TCP ports, socket timeouts, NLB).
    * L3: Network (IP routing, CIDR blocks, Security Groups, VPC).
    * L2: Data Link (MAC addresses, Ethernet frames).
    * L1: Physical (cables, radio waves, fiber).
  * **Encapsulation**: As data moves down the stack, each layer wraps the payload with its own header. A 100-byte JSON payload becomes 400+ bytes on the wire due to headers (Ethernet + IP + TCP + TLS + HTTP).
  * **ALB vs NLB**:
    * **Application Load Balancer (Layer 7)**: Reads HTTP paths and headers. Supports path/host-based routing and WebSocket upgrades. Adds 1-5ms latency.
    * **Network Load Balancer (Layer 4)**: Protocol-agnostic, routes based on TCP/UDP ports. Ultra-low latency (<100 microseconds). Preserves client IP, handles millions of connections. Ideal for DB proxies, gaming, or gRPC.
  - **TLS Encryption Scope**: TLS encrypts everything *above* Layer 4 (headers, path, query, body). It does NOT encrypt TCP ports, IP addresses, or DNS queries (unless using DoH).

### Key Commands / Code Example:

```bash
# Check active network connections at Layer 4
netstat -an | grep :3000

# Capture Layer 7 HTTP traffic headers only (HEAD request)
curl -I https://example.com
```

> [!WARNING]
> Databases do not speak HTTP. Attempting to use a Layer 7 ALB in front of MongoDB or Redis will fail. You must use a Layer 4 NLB (TCP passthrough) for database load balancing.

---

## 04. TCP/IP Model

🔗 **Full Lesson:** [04_TCP_IP_Model.md](./04_TCP_IP_Model.md)

* **What**: Focuses on the pragmatics of the 4-layer TCP/IP model (Application, Transport, Internet, Network Access) that powers the internet.
* **Why It Exists**: Shows how all web applications run on a unified TCP/IP foundation. Port allocation, Dynamic/Ephemeral ports, and handshake costs dictate connection scale and reuse.
* **Key Concepts**:
  * **Layers**: Application (HTTP, WS, DNS, RESP), Transport (TCP, UDP), Internet (IP, ICMP), Network Access (Ethernet, WiFi).
  * **TCP Guarantees**: Delivery (retransmits lost), Ordering (reassembles segments), Integrity (no corruption via checksum), Flow Control (sender doesn't overwhelm receiver), Congestion Control (slow start cwnd).
  * **UDP Characteristics**: Lightweight, no handshake (0 RTT), no ordering, no delivery confirmation. Used for DNS queries, real-time video/gaming, and HTTP/3.
  * **Port Ranges**: Well-known (1-1023, requires root), Registered (1024-49151), Ephemeral/Dynamic (49152-65535, assigned by OS for outgoing connections).
  * **Ephemeral Port Exhaustion**: Under heavy load, short-lived connections that close quickly stack up in `TIME_WAIT` (retained for 120s). This exhausts the dynamic port pool, causing connection errors. Fix with connection pools.
  * **TCP Option Tuning**: Disabling Nagle's algorithm (`setNoDelay(true)`) sends small packets immediately instead of buffering them, reducing latency.

### Key Commands / Code Example:

```javascript
// Disable Nagle's algorithm in Node.js TCP socket
socket.setNoDelay(true);
// Send keep-alive probes every 60 seconds
socket.setKeepAlive(true, 60000);
```

> [!IMPORTANT]
> EADDRINUSE error means another process is already using your server's port. Find it with `lsof -i :3000` (Linux/Mac) or `netstat -ano | findstr 3000` (Windows) and kill the process ID.

---

## 05. IP Addressing & Subnetting

🔗 **Full Lesson:** [05_IP_Addressing_And_Subnetting.md](./05_IP_Addressing_And_Subnetting.md)

* **What**: Explains how IPv4 addresses are structured, private vs. public IP ranges, CIDR block math, and how they apply to AWS VPCs and Security Groups.
* **Why It Exists**: Properly segmenting networks prevents security breaches. Databases and internal caches must reside in private subnets, while load balancers live in public subnets with routes to the internet.
* **Key Concepts**:
  * **IP Structure**: 32 bits, 4 octets. Private ranges: `10.0.0.0/8` (VPCs), `172.16.0.0/12` (Docker), `192.168.0.0/16` (Home).
  * **CIDR Block Math**: `/X` represents fixed network bits. `/32` is 1 host (white-lists). `/24` is 256 IPs (251 usable in AWS, which reserves 5). `/16` is 65,536 IPs.
  * **VPC Subnet Design**:
    * **Public Subnet**: Connected to Internet Gateway (IGW). Instances get public IPs.
    * **Private Subnet**: No direct IGW route. Outbound internet requires routing through a NAT Gateway.
    * **Isolated Subnet**: No NAT/IGW route. Purely internal (ideal for DBs).
  * **AWS Subnet Reservations**: AWS reserves 5 IPs: `.0` (network), `.1` (VPC router), `.2` (DNS), `.3` (future use), `.255` (broadcast).
  * **Security Groups**: Stateful, instance-level firewalls. Inbound rule allows traffic; outbound response is automatically allowed.

### Key Commands / Code Example:

```javascript
// Check if an IP address falls within a CIDR block
function isIPInCIDR(ip, cidr) {
  const [network, bits] = cidr.split('/');
  const mask = -1 << (32 - parseInt(bits));
  const ipInt = ip.split('.').reduce((acc, oct) => (acc << 8) + parseInt(oct), 0);
  const netInt = network.split('.').reduce((acc, oct) => (acc << 8) + parseInt(oct), 0);
  return (ipInt & mask) === (netInt & mask);
}
console.log(isIPInCIDR('10.0.1.50', '10.0.1.0/24')); // true
```

> [!WARNING]
> Never open port 5432 or 27017 to `0.0.0.0/0` in your security groups. This exposes your database directly to the public internet, inviting brute-force and ransom attacks.

---

## 06. DNS Deep Dive

🔗 **Full Lesson:** [06_DNS_Deep_Dive.md](./06_DNS_Deep_Dive.md)

* **What**: Demystifies domain name resolution (Resolvers, TLDs, Root servers, Authoritative nameservers) and Route 53 policies.
* **Why It Exists**: DNS failures stall connection setups, causing slow page loads or downtime. Caching DNS lookups correctly in Node.js prevents per-request resolution latency.
* **Key Concepts**:
  * **Resolution Chain**: Browser Cache -> OS Cache -> Router -> ISP Recursive Resolver -> Root DNS (`.`) -> TLD Name Server (`.com`) -> Authoritative Name Server (Route 53) -> returns IP.
  * **Record Types**:
    * `A` (IPv4), `AAAA` (IPv6), `CNAME` (Alias, cannot be at zone apex), `ALIAS` (Route 53 specific, maps domain to ALB/CloudFront directly at zone apex).
    * `MX` (Mail), `TXT` (Verification/SPF/DKIM), `SRV` (Service discovery, used by MongoDB Atlas replica sets).
  * **Route 53 Policies**: Simple, Latency-based (routes to nearest region), Failover (routes to standby on health check fail), Weighted (A/B testing, Blue/Green), Geolocation (EU users to EU servers), Multi-value (returns multiple IPs).
  * **TTL (Time to Live)**: Duration DNS records are cached. Short TTLs (e.g., 300s) facilitate fast updates during migrations. Long TTLs (e.g., 86400s) reduce DNS lookup queries.
  * **Next.js Prehints**: `<link rel="dns-prefetch" href="..." />` and `<link rel="preconnect" href="..." />` pre-resolve hostnames on the browser to speed up dynamic API calls.

### Key Commands / Code Example:

```bash
# Check the full DNS resolution trace path
dig api.myapp.com +trace

# Query Google DNS directly for A records
dig @8.8.8.8 api.myapp.com A
```

> [!IMPORTANT]
> Node.js does NOT cache DNS lookups by default. A high-traffic Node.js app making 1,000 HTTP requests to external APIs will perform 1,000 DNS resolutions, hurting performance. Install `cacheable-lookup` to enable DNS caching in Node.js.

---

## 07. HTTP/HTTPS Internals

🔗 **Full Lesson:** [07_HTTP_HTTPS_Internals.md](./07_HTTP_HTTPS_Internals.md)

* **What**: Explains HTTP structure (Request/Response anatomy), differences between HTTP versions, and CORS.
* **Why It Exists**: Efficient API design requires managing headers, compression, caching (ETags), and properly configuring CORS policies to avoid browser blocker issues.
* **Key Concepts**:
  * **Anatomy**: Verb + Path + Version, Headers, Blank Line, Payload. The blank line tells parsers that the headers end and the body begins.
  * **HTTP/1.1 vs. HTTP/2 vs. HTTP/3**:
    * **HTTP/1.1**: Max 6 TCP connections per domain. Head-of-line blocking per connection. Plain text headers.
    * **HTTP/2**: Single TCP connection. Multiplexes streams (eliminating HTTP head-of-line blocking). Compresses headers with HPACK. Binary framing.
    * **HTTP/3**: Uses QUIC over UDP. Eliminates TCP-level head-of-line blocking (packet loss in one stream doesn't block other streams). 0-RTT/1-RTT connection setup.
  * **CORS (Cross-Origin Resource Sharing)**: Browser security model. For non-simple requests, browser sends `OPTIONS` preflight. Server must respond with `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, etc.
  * **HTTP Cache Headers**:
    * `Cache-Control`: `no-store` (never cache), `no-cache` (revalidate), `public, max-age` (shared cache), `private` (client only), `immutable` (never changes).
    * `ETag`: Resource hash. Client sends `If-None-Match`, server responds with 304 if unchanged.

### Key Commands / Code Example:

```javascript
// Express CORS & Compression Setup
const express = require('express');
const cors = require('cors');
const compression = require('compression');
const app = express();

app.use(compression()); // Gzip compression
app.use(cors({
  origin: ['https://myapp.com'],
  credentials: true,
  maxAge: 86400 // Cache preflight for 24 hours
}));
```

> [!WARNING]
> Returning 200 OK with an error message payload (e.g. `{ error: "Email exists" }`) blocks downstream API frameworks from detecting errors. Always return correct status codes (e.g., 400 Bad Request or 409 Conflict).

---

## 08. TCP Deep Dive

🔗 **Full Lesson:** [08_TCP_Deep_Dive.md](./08_TCP_Deep_Dive.md)

* **What**: Explores TCP handshake mechanics, connection teardowns, congestion control, and keep-alive timeout matching.
* **Why It Exists**: Incorrect keep-alive alignments between Node.js and load balancers trigger intermittent 502 Bad Gateway errors. Stale socket connections behind NATs cause EPIPE/ECONNRESET.
* **Key Concepts**:
  * **3-Way Handshake**: SYN -> SYN-ACK -> ACK. Establishes sequence numbers. Costs 1.5 RTT.
  * **Connection Teardown**: 4-way handshake (FIN -> ACK -> FIN -> ACK). Sockets enter `TIME_WAIT` for 2 minutes to clear late packets.
  * **TCP States**: `LISTEN` (waiting), `SYN_SENT`, `ESTABLISHED` (active), `TIME_WAIT` (cleanup), `CLOSE_WAIT` (half-closed, potential app leak).
  * **Congestion Control**: Slow Start. Starts with a small window (cwnd ≈ 14KB) and doubles each RTT until packet loss occurs, then halves the window. Connection pooling prevents starting at slow-start speed.
  * **Keep-Alive & NAT Gateway**: AWS NAT Gateway drops idle TCP streams after 350s. If pool connections are idle without probes, they go stale, triggering `ECONNRESET`. Fix by sending keep-alive probes every 120s.

### Key Commands / Code Example:

```bash
# Check connection counts by state
netstat -an | awk '/tcp/ {print $6}' | sort | uniq -c | sort -rn

# Monitor TCP packets on port 3000 (S=SYN, .=ACK, F=FIN, R=RST)
sudo tcpdump -i any port 3000 -nn
```

> [!IMPORTANT]
> Keep-Alive Timeout Mismatch: Ensure Node.js `keepAliveTimeout` is slightly larger than your ALB's idle timeout (e.g. 65s > 60s). If Node.js closes a socket early while ALB thinks it is alive, the next request triggers a 502 Bad Gateway.

---

## 09. UDP & When To Use It

🔗 **Full Lesson:** [09_UDP_And_When_To_Use_It.md](./09_UDP_And_When_To_Use_It.md)

* **What**: Focuses on UDP mechanics, datagram size constraints, and its integration in modern protocols like HTTP/3 (QUIC) and WebRTC.
* **Why It Exists**: UDP eliminates handshake and overhead costs (header is only 8 bytes vs. 20-60 bytes for TCP). Perfect for latency-sensitive, loss-tolerant streams.
* **Key Concepts**:
  * **Differences**: Stateless, fire-and-forget, no delivery checks, no flow control.
  * **DNS over UDP**: Resolvers query DNS servers via UDP port 53. If responses exceed 512 bytes, they fall back to TCP.
  * **HTTP/3 over QUIC**: QUIC runs on top of UDP. Implementing encryption and reliability at the application layer avoids TCP head-of-line blocking (packet loss in one stream doesn't block other streams).
  * **Datagram MTU Limit**: Standard Ethernet MTU is 1500 bytes. Subtracting IP (20 bytes) and UDP (8 bytes) headers leaves a practical datagram payload limit of ~1400 bytes. Larger payloads trigger IP fragmentation, increasing packet loss rates.
  * **Use Cases**: DNS, WebRTC, syslog, StatsD metrics, and multiplayer gaming.

### Key Commands / Code Example:

```javascript
// Sending fire-and-forget metrics via UDP in Node.js
const dgram = require('dgram');
const client = dgram.createSocket('udp4');
const metric = Buffer.from('api.response_time:45|ms');
client.send(metric, 8125, 'statsd-server', (err) => {
  client.close(); // Closed immediately, delivery is not verified
});
```

> [!NOTE]
> Do not use UDP for API calls, database operations, or file transfers where data integrity is required. Lost packets are gone forever, resulting in corrupted data or failed requests.

---

## 10. TLS/SSL Handshake

🔗 **Full Lesson:** [10_TLS_SSL_Handshake.md](./10_TLS_SSL_Handshake.md)

* **What**: Details Transport Layer Security (TLS 1.2 vs. 1.3), certificate validation, revocation, and security practices.
* **Why It Exists**: TLS protects client-server communication from sniffing, interception, and spoofing. Misconfigured certificate chains or disabling verification leaves applications open to Man-in-the-Middle (MITM) attacks.
* **Key Concepts**:
  * **Handshake Comparison**:
    * **TLS 1.2**: 2 RTTs. Exchanges ciphers, negotiates keys, and sends the certificate in plain text.
    * **TLS 1.3**: 1 RTT. Pre-sends Diffie-Hellman key shares in ClientHello. Encrypts the certificate. Removes legacy/weak ciphers.
  * **Asymmetric vs. Symmetric**: Asymmetric (RSA/ECDH) is used during the handshake to establish a shared secret. Symmetric (AES/ChaCha20) encrypts the actual data transfer (~1,000x faster).
  * **Perfect Forward Secrecy (PFS)**: Ephemeral DH keys are generated per session and discarded. If the server's private key leaks in the future, past recorded sessions cannot be decrypted.
  * **Certificate Chain**: Leaf Cert -> Intermediate CA -> Root CA (pre-installed in browser's trust store).
  * **Revocation**: CRL (revocation lists), OCSP (online check), OCSP Stapling (server staples signed status to handshake - recommended).
  * **TLS Termination**: Terminating TLS at the load balancer (ALB/CloudFront) offloads encryption work from Node.js, routing plain HTTP internally within the VPC.

### Key Commands / Code Example:

```bash
# Check TLS handshake details and certificate chain
openssl s_client -connect api.myapp.com:443 -servername api.myapp.com

# View certificate expiration dates
echo | openssl s_client -connect api.myapp.com:443 2>/dev/null | openssl x509 -noout -dates
```

> [!CAUTION]
> Never set `process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'` in production. This disables certificate verification globally, making your backend vulnerable to MITM attacks. If using private certs, load the CA file explicitly in your HTTPS agent config.

---

## 11. Routing & NAT

🔗 **Full Lesson:** [11_Routing_And_NAT.md](./11_Routing_And_NAT.md)

* **What**: Covers VPC routing rules, CIDR specificity, and NAT (Network Address Translation) gateways.
* **Why It Exists**: Instances in private subnets require a NAT Gateway to fetch external updates or connect to public APIs, while remaining unreachable from the public internet.
* **Key Concepts**:
  * **Route Selection**: Longest prefix match wins. A route to `10.0.1.0/24` beats `10.0.0.0/16` and `0.0.0.0/0`.
  * **NAT Translation**: Translates private IPs to a public IP. The NAT Gateway maps ports to track which private instance initiated the outgoing connection.
  * **VPC Peering**: Directly links two VPCs with non-overlapping CIDRs via private routing.
  * **AWS Cloud Map**: Private DNS service discovery mapping service names to internal IPs.

### Key Commands / Code Example:

```bash
# Check public IP as seen by the internet (verifies NAT is working)
curl https://ifconfig.me

# AWS CLI: List subnets and their route tables
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-xxxxx"
```

> [!NOTE]
> AWS NAT Gateways are billed hourly (~$32/mo) plus data processing charges ($0.045/GB). For development/staging VPCs, consider using public subnets with security groups to save costs.

---

## 12. Load Balancing

🔗 **Full Lesson:** [12_Load_Balancing.md](./12_Load_Balancing.md)

* **What**: Explores load balancer types, load distribution algorithms, sticky sessions, and graceful shutdowns.
* **Why It Exists**: Achieving high availability and zero-downtime deployments requires distributing load and smoothly draining traffic before stopping Node.js servers.
* **Key Concepts**:
  * **ALB (Layer 7)**: Smart, path-based (`/api/*`) and host-based routing. Supports WebSockets. Latency overhead of 1-5ms.
  * **NLB (Layer 4)**: Fast, passes raw TCP connections (Redis, MongoDB, gRPC). Latency overhead <100 microseconds.
  * **Graceful Shutdown**: Upon receiving a SIGTERM signal, Node.js should set a flag to return 503 on health checks, stop accepting new connections, finish in-flight requests, and close database connections before exiting.
  * **Target Group Draining**: When an instance is deregistered, the ALB waits for a cooldown period (default: 300s, recommend: 30s) to allow existing requests to complete.

### Key Commands / Code Example:

```javascript
// Node.js Graceful Shutdown handler
process.on('SIGTERM', () => {
  isShuttingDown = true;
  server.close(async () => {
    await mongoose.connection.close();
    await redis.quit();
    process.exit(0);
  });
  setTimeout(() => process.exit(1), 30000); // Hard exit force limit
});
```

> [!IMPORTANT]
> If you do not configure `app.set('trust proxy', true)` in your Express app behind an ALB, `req.ip` will return the internal IP of the ALB instead of the client's public IP.

---

## 13. Firewalls & Security

🔗 **Full Lesson:** [13_Firewalls_And_Security.md](./13_Firewalls_And_Security.md)

* **What**: Explains Security Groups (stateful), NACLs (stateless), WAF (Layer 7 filtering), and DDoS protections.
* **Why It Exists**: A secure infrastructure uses multiple firewall layers (Defense in Depth) to filter traffic by port, IP, and payload content.
* **Key Concepts**:
  * **Comparison**:
    * **Security Group**: Instance-level, stateful (automatically permits response traffic), allow-only rules.
    * **Network ACL**: Subnet-level, stateless (must explicitly allow both inbound and outbound traffic), allow and deny rules evaluated in order.
  * **AWS WAF**: Inspects HTTP content at Layer 7. Protects against SQL injection, XSS, rate limits by IP, and blocks known bad bots.
  * **Application Security**:
    * `helmet`: Sets HTTP security headers (CSP, HSTS).
    * `express-rate-limit`: Throttles requests by IP.
    * `express-mongo-sanitize`: Sanitizes queries to prevent NoSQL injection.

### Key Commands / Code Example:

```javascript
// Express security headers and rate limiter
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
app.use(helmet());
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100, // Limit each IP to 100 requests per window
  keyGenerator: (req) => req.ip
}));
```

> [!WARNING]
> NACLs are stateless. If you block outbound port ranges, you will break the return traffic path. Ensure ephemeral port ranges (1024-65535) are allowed outbound in your NACL configurations.

---

## 14. Proxies & Reverse Proxies

🔗 **Full Lesson:** [14_Proxies_And_Reverse_Proxies.md](./14_Proxies_And_Reverse_Proxies.md)

* **What**: Compares forward and reverse proxies, focusing on Nginx reverse proxy configurations.
* **Why It Exists**: Running Node.js directly on the public internet is slow for static files, lacks gzip/brotli out of the box, and poses security risks. Reverse proxies protect Node.js.
* **Key Concepts**:
  * **Forward Proxy**: Client-side. Acts on behalf of the client (hides client IP, content filtering).
  * **Reverse Proxy**: Server-side. Acts on behalf of the server (ALB, Nginx, CloudFront).
  * **Nginx Benefits**: Serves static files fast using the `sendfile` system call, buffers slow clients to protect Node.js event loops, terminates TLS, and compresses payloads.
  * **Proxy Buffering**: Nginx buffers the response from Node.js before delivering it to slow mobile clients, freeing Node.js threads immediately.

### Key Commands / Code Example:

```nginx
# Nginx WebSocket proxy configuration
location /socket.io/ {
    proxy_pass http://node_api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 86400s; # 24-hour timeout for WebSockets
}
```

> [!IMPORTANT]
> When setting `trust proxy` in Express, do not set it to `true` globally, as clients can spoof the `X-Forwarded-For` header. Set it to the exact number of trusted hop proxies (e.g. `app.set('trust proxy', 2)` if behind CloudFront + ALB).

---

## 15. CDN & Caching

🔗 **Full Lesson:** [15_CDN_And_Caching.md](./15_CDN_And_Caching.md)

* **What**: Explores CDN edge caching (CloudFront) and application memory caching (Redis).
* **Why It Exists**: Serving content from edge servers reduces geographical latency. Multi-layer caching speeds up reads but requires invalidation planning.
* **Key Concepts**:
  * **Caching Layers**: Browser Cache -> CDN Cache -> Redis Cache -> DB Query Cache.
  * **Caching Golden Rule**: Closer to the user = faster, but harder to invalidate.
  * **Cache Busting**: Hashing filenames (e.g. `bundle.abc123.js`) allows long client caching (`max-age=31536000, immutable`). A deploy updates the filename, bypassing the cache.
  * **Redis Cache-Aside**: Check Redis first. If miss, query DB, write to Redis with a TTL, and return.
  * **Thundering Herd**: When a hot cache key expires, concurrent queries hit the DB. Mitigated by locking, pre-warming, or setting jittered TTLs.

### Key Commands / Code Example:

```javascript
// Cache API response in Redis with TTL
app.get('/api/products/:id', async (req, res) => {
  const key = `products:${req.params.id}`;
  const cached = await redis.get(key);
  if (cached) return res.json(JSON.parse(cached));
  
  const product = await Product.findById(req.params.id).lean();
  await redis.set(key, JSON.stringify(product), 'EX', 300); // 5 min TTL
  res.json(product);
});
```

> [!CAUTION]
> Never cache user-specific data (like `/api/profile`) on the CDN or in a public cache. Set the `Cache-Control` header to `private, no-store` to prevent data leakage.

---

## 16. WebSockets & Real-Time

🔗 **Full Lesson:** [16_WebSockets_And_Real_Time.md](./16_WebSockets_And_Real_Time.md)

* **What**: Covers full-duplex WebSocket connections, scaling with Redis, and timeout mitigations.
* **Why It Exists**: Real-time communication requires open, low-overhead sockets. Scaling stateful connections requires Pub/Sub broker coordination.
* **Key Concepts**:
  * **WS Handshake**: HTTP request with `Upgrade: websocket` -> HTTP 101 Switching Protocols -> raw TCP frames.
  * **Overhead**: HTTP has ~800 bytes of headers. WebSockets use a 2-6 byte frame header, reducing bandwidth requirements by over 90% for small updates.
  * **Scaling Stateful connections**: If a user is connected to Server A and another to Server B, they cannot communicate directly. A Redis Pub/Sub adapter broadcasts messages across all servers.
  * **Keep-Alive**: Set ping intervals (e.g., 25s) lower than intermediary load balancer timeouts (60s) to keep sockets active.

### Key Commands / Code Example:

```javascript
// Scaling Socket.IO with Redis Adapter
const { Server } = require('socket.io');
const { createAdapter } = require('@socket.io/redis-adapter');
const { createClient } = require('redis');

const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();
Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  const io = new Server(server);
  io.adapter(createAdapter(pubClient, subClient));
});
```

> [!NOTE]
> Do not use WebSockets for regular CRUD operations. Keep REST endpoints for CRUD and files, and use WebSockets solely for real-time notifications, chat, and presence states.

---

## 17. API Gateways

🔗 **Full Lesson:** [17_API_Gateways.md](./17_API_Gateways.md)

* **What**: Covers centralized API Gateways (AWS API Gateway vs. custom Express gateways) and pattern designs.
* **Why It Exists**: Moving cross-cutting concerns (auth, rate limiting, CORS) to the gateway layer simplifies microservices.
* **Key Concepts**:
  * **Patterns**: Serverless (API Gateway -> Lambda -> DB) vs. Traditional (API Gateway -> ALB -> EC2).
  * **AWS API Gateway Types**:
    * **HTTP API**: Lightweight, fast, low latency, and 3.5x cheaper ($1/million requests).
    * **REST API**: Supports request validation, caching, API keys, and WAF integration ($3.50/million requests).
  * **Limitations**: Max execution timeout is 29 seconds (REST API) or 30 seconds (HTTP API). Payload size is limited to 10MB.

### Key Commands / Code Example:

```javascript
// Gateway forwarding request with trace headers
app.use('/api/orders', createProxyMiddleware({
  target: 'http://order-service:3002',
  pathRewrite: { '^/api/orders': '/orders' },
  changeOrigin: true,
  onProxyReq: (proxyReq, req) => {
    proxyReq.setHeader('x-user-id', req.user.id);
  }
}));
```

> [!IMPORTANT]
> If a backend process takes longer than 29s, the API Gateway will throw a 504 Gateway Timeout, even if your backend continues running. Offload long tasks to SQS queues and return 202 Accepted immediately.

---

## 18. Microservices Networking

🔗 **Full Lesson:** [18_Microservices_Networking.md](./18_Microservices_Networking.md)

* **What**: Discusses microservices communication patterns, service discovery, and circuit breakers.
* **Why It Exists**: Distributed architectures introduce latency and new failure modes. Circuit breakers and async queues prevent cascading service failures.
* **Key Concepts**:
  * **Communication**: Sync (REST, gRPC) vs. Async (SQS queues, Pub/Sub event buses like SNS/Kafka).
  * **Service Discovery**: DNS-based (Cloud Map), Load Balancer paths, or service meshes (App Mesh proxy sidecars).
  * **Circuit Breaker**: Prevents calling down services. Once failures exceed a threshold, the circuit opens, failing requests immediately. After a cooldown, it goes half-open to test recovery.
  * **Distributed Tracing**: Generate an `X-Request-ID` at the gateway and pass it along all downstream network hops.

### Key Commands / Code Example:

```javascript
// Simple Circuit Breaker implementation wrapper
class CircuitBreaker {
  constructor(action, threshold = 5) {
    this.action = action;
    this.threshold = threshold;
    this.failures = 0;
    this.state = 'CLOSED'; // CLOSED, OPEN
  }
  async execute(...args) {
    if (this.state === 'OPEN') throw new Error('Circuit Open');
    try {
      const res = await this.action(...args);
      this.failures = 0;
      return res;
    } catch (err) {
      if (++this.failures >= this.threshold) this.state = 'OPEN';
      throw err;
    }
  }
}
```

> [!WARNING]
> Avoid sharing databases between services. Each microservice must own its database schema to remain decoupled and scale independently.

---

## 19. Containers & Networking

🔗 **Full Lesson:** [19_Containers_And_Networking.md](./19_Containers_And_Networking.md)

* **What**: Covers Docker networking modes, Compose setups, and ECS Fargate awsvpc integrations.
* **Why It Exists**: Running containers requires isolating their networking interfaces while allowing dynamic service discovery by name.
* **Key Concepts**:
  * **Modes**: Bridge (default private IP), Host (shares host network), None (isolated), awsvpc (ECS task gets unique ENI and VPC IP).
  * **Docker Compose DNS**: Resolves service names defined in `docker-compose.yml` to their bridge network IPs.
  * **awsvpc Mode Benefits**: No port mapping bottlenecks. SGs attach directly to tasks, simplifying RDS white-listing.

### Key Commands / Code Example:

```yaml
# docker-compose bridge network DNS naming
services:
  api:
    build: .
    environment:
      - MONGO_URI=mongodb://mongodb:27017/myapp # Resolves by service name
  mongodb:
    image: mongo:7.0
```

> [!IMPORTANT]
> Do not use `localhost` to connect between containers in Docker. `localhost` refers to the container itself, not the host machine. Use the service name defined in docker-compose.

---

## 20. Kubernetes Networking

🔗 **Full Lesson:** [20_Kubernetes_Networking.md](./20_Kubernetes_Networking.md)

* **What**: Explores Kubernetes flat network designs, ClusterIP services, Ingress controllers, and network policies.
* **Why It Exists**: K8s routes traffic dynamically across multiple nodes. Services decouple pods from stable DNS endpoints.
* **Key Concepts**:
  * **IP-Per-Pod**: Every pod gets a unique IP. Pods communicate directly without NAT, even across nodes.
  * **Service Types**: ClusterIP (internal), NodePort (debug), LoadBalancer (provisions ALB/NLB).
  * **Ingress**: Layer 7 path routing rules. Managed on AWS using the ALB Ingress Controller.
  * **NetworkPolicy**: Pod-level firewall. Restricts incoming traffic by label selector.

### Key Commands / Code Example:

```yaml
# NetworkPolicy to restrict database access
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mongo-policy
spec:
  podSelector:
    matchLabels:
      app: mongodb
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api # Only allow pods with label app=api
```

> [!WARNING]
> Always set resources limits (CPU and Memory) on container specs. Without caps, a memory leak in one pod can consume all node resources, crashing other services on the host.

---

## 21. Debugging Network Issues

🔗 **Full Lesson:** [21_Debugging_Network_Issues.md](./21_Debugging_Network_Issues.md)

* **What**: Provides a methodology and tools for troubleshooting network issues.
* **Why It Exists**: Diagnosing production issues requires systematically verifying the network stack from the bottom up to save time.
* **Key Concepts**:
  * **Debugging Methodology**: DNS -> IP Connectivity -> TCP -> TLS -> HTTP -> Application.
  * **Common Errors**:
    * `ECONNREFUSED`: Port not listening (service down).
    * `ETIMEDOUT`: Packets blocked (firewall/security groups).
    * `ECONNRESET`: Connection closed (ALB timeout, backend crash).
    * `502 Bad Gateway`: ALB can't reach Node.js (Node.js down, port mismatch, keep-alive timeout).
    * `504 Gateway Timeout`: Backend request took >60s.

### Key Commands / Code Example:

```bash
# Test TCP port connectivity (Netcat)
nc -zv api.myapp.com 443

# Measure HTTP request timings
curl -w "DNS: %{time_namelookup}s TCP: %{time_connect}s TLS: %{time_appconnect}s TTFB: %{time_starttransfer}s Total: %{time_total}s\n" -o /dev/null -s https://api.myapp.com/api/health
```

> [!NOTE]
> Ping uses ICMP. AWS security groups block ICMP by default. A failed ping doesn't mean the server is down; verify TCP connectivity using `nc -zv` instead.

---

## 22. Performance Optimization

🔗 **Full Lesson:** [22_Performance_Optimization.md](./22_Performance_Optimization.md)

* **What**: Focuses on performance budgets, keep-alive connections, compression, and payload optimization.
* **Why It Exists**: Latency is a critical performance metric. Minimizing connection overhead and payload sizes speeds up page loads.
* **Key Concepts**:
  * **Latency vs. Throughput**: Latency is the time for a single round trip; throughput is the volume of requests processed per second.
  * **Optimization Checklist**: Cache DNS queries, reuse TCP connections (Keep-Alive), enable compression (Gzip/Brotli), use HTTP/2, paginate API responses, and use CDN edge caching.

### Key Commands / Code Example:

```javascript
// Node.js Outbound Keep-Alive Agent Setup
const https = require('https');
const agent = new https.Agent({
  keepAlive: true,
  maxSockets: 50,
  maxFreeSockets: 10
});
// Pass agent to axios or fetch options
```

> [!IMPORTANT]
> Under-optimized API payloads (missing pagination, returning unused fields) waste bandwidth. Always select required fields using projections (e.g. `.select('name price')` in Mongoose).

---

## 23. Database Networking

🔗 **Full Lesson:** [23_Database_Networking.md](./23_Database_Networking.md)

* **What**: Covers database connection pools, read replicas, and NAT gateway timeouts.
* **Why It Exists**: Database queries run over TCP. Reusing connections in a pool prevents connection overhead from slowing down queries.
* **Key Concepts**:
  * **Connection Pools**: Maintain open connections to reuse for queries. Limit size (e.g., `maxPoolSize: 10`) to avoid exhausting database connections.
  * **Read Scaling**: Route writes to the Primary DB and reads to Read Replicas (handles read volume, accepts replication lag).
  * **NAT Timeout**: AWS NAT Gateways drop idle connections after 350s. Set TCP keep-alive to <120s on database pools to keep connections active.

### Key Commands / Code Example:

```javascript
// Mongoose connection pool configuration
const mongoose = require('mongoose');
mongoose.connect(process.env.MONGO_URI, {
  maxPoolSize: 10,
  minPoolSize: 2,
  keepAlive: true,
  keepAliveInitialDelay: 120000 // Send keep-alive every 120s
});
```

> [!WARNING]
> Connecting to a database on every request (opening and closing connections) degrades performance due to handshake overhead. Always open the connection pool once at startup and reuse it.

---

## 24. VPC Architecture & Design

🔗 **Full Lesson:** [24_VPC_Architecture_And_Design.md](./24_VPC_Architecture_And_Design.md)

* **What**: Details VPC layouts, three-tier subnets, peering, and VPC endpoints.
* **Why It Exists**: Designing VPCs with separate public, private, and isolated tiers isolates critical workloads and prevents unauthorized access.
* **Key Concepts**:
  * **Three-Tier VPC Layout**: Public (ALB, NAT Gateway), Private App (ECS/EC2 tasks), Isolated Data (RDS, ElastiCache - no internet route).
  * **Multi-AZ Resilience**: Distribute subnets across 2+ Availability Zones. If one AZ goes down, the ALB fails over to the other.
  * **VPC Endpoints**: Route AWS services internally. Gateway endpoints (S3, DynamoDB) are free and save NAT Gateway transfer costs.

### Key Commands / Code Example:

```bash
# AWS CLI: Create a VPC Endpoint for S3 (Gateway type)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxxxx \
  --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids rtb-xxxxx
```

> [!NOTE]
> Ensure CIDRs do not overlap between VPCs if you plan to link them via VPC Peering. You cannot peer VPCs with overlapping address spaces.

---

## 25. Network Monitoring & Observability

🔗 **Full Lesson:** [25_Network_Monitoring_And_Observability.md](./25_Network_Monitoring_And_Observability.md)

* **What**: Explores metrics, logs, traces, CloudWatch alarms, and VPC Flow Logs.
* **Why It Exists**: Observability tools alert you to errors and latency spikes before they affect users.
* **Key Concepts**:
  * **Three Pillars**: Metrics (numerical time-series data like CloudWatch CPU/latency), Logs (structured JSON events), Traces (path of requests across services like X-Ray).
  * **VPC Flow Logs**: Captures metadata of all traffic in the VPC. Useful for finding blocked connections (`REJECT` actions).
  * **Prometheus Metrics**: Expose `/metrics` to scrape CPU, memory, and HTTP response latencies (p50, p95, p99).

### Key Commands / Code Example:

```bash
# CloudWatch CLI: Set alarm for high 5xx error rate on ALB
aws cloudwatch put-metric-alarm \
  --alarm-name "ALB-High-5xx" \
  --metric-name "HTTPCode_Target_5XX_Count" \
  --namespace "AWS/ApplicationELB" \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --dimensions Name=LoadBalancer,Value=app/my-alb/xxxxx
```

> [!IMPORTANT]
> Log structured data as JSON. Unstructured logs (plain text strings) are difficult to query or filter in CloudWatch Logs Insights.

---

## 26. Deployment & Production Infrastructure

🔗 **Full Lesson:** [26_Deployment_And_Production_Infrastructure.md](./26_Deployment_And_Production_Infrastructure.md)

* **What**: Synthesizes the architecture (DNS, CDN, ALB, EC2, RDS, Redis, CI/CD) for deploying production-grade applications.
* **Why It Exists**: Deploying full-stack applications with high availability and security requires integrating all layers of the networking stack.
* **Key Concepts**:
  * **Production Architecture**: Route 53 (DNS) -> CloudFront (CDN, TLS termination, static S3 files) -> ALB (routing) -> Auto Scaling Group EC2 (App) -> RDS Multi-AZ + Redis (Data).
  * **Rolling Deployments**: CodeDeploy/ECS updates one instance at a time. ALB redirects traffic after readiness probes pass.
  * **Backward Compatibility**: During deployments, v1 and v2 run concurrently. Changes to API payloads and databases must be backward-compatible.
  * **Disaster Recovery (DR)**: Backup & Restore (cheapest), Pilot Light (standby DB replica), Warm Standby (scaled-down stack), Active-Active (multi-region).

### Key Commands / Code Example:

```yaml
# GitHub Actions deploy snippet to force ECS rollout
- name: Deploy to ECS
  run: |
    aws ecs update-service \
      --cluster production-cluster \
      --service api-service \
      --force-new-deployment
```

> [!CAUTION]
> Always set up database backups (RDS snapshots) and test your Disaster Recovery plan. An untested backup strategy is not a backup strategy.

---

Previous : [00_Index.md](./00_Index.md) | Index : [00_Index.md](./00_Index.md) | Next : [01_Introduction_And_Setup.md](./01_Introduction_And_Setup.md)
