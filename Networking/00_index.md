# 🌐 Networking & Internet Architecture – Complete Revision Guide

Welcome to the Complete Networking & Internet Architecture Revision Guide. This guide aggregates all key concepts, commands, configurations, best practices, and interview questions across the entire module from a single high-density file. It is designed to serve as a comprehensive, production-ready checklist to help you revise the entire networking stack in under 30 minutes.

---

## 📌 Module Navigation

* [01. Introduction & Setup](#01-introduction--setup)
* [02. How The Internet Actually Works](#02-how-the-internet-actually-works)
* [03. HTTP/HTTPS Internals](#03-httphttps-internals)
* [04. DNS Deep Dive](#04-dns-deep-dive)
* [05. WebSockets & Real-Time](#05-websockets--real-time)
* [06. OSI Model Vs Real World](#06-osi-model-vs-real-world)
* [07. TCP/IP Model](#07-tcpip-model)
* [08. TCP Deep Dive](#08-tcp-deep-dive)
* [09. UDP & When To Use It](#09-udp--when-to-use-it)
* [10. TLS/SSL Handshake](#10-tlsssl-handshake)
* [11. IP Addressing & Subnetting](#11-ip-addressing--subnetting)
* [12. Routing & NAT](#12-routing--nat)
* [13. Load Balancing](#13-load-balancing)
* [14. Proxies & Reverse Proxies](#14-proxies--reverse-proxies)
* [15. CDN & Caching](#15-cdn--caching)
* [16. Firewalls & Security](#16-firewalls--security)
* [17. API Gateways](#17-api-gateways)
* [18. Microservices Networking](#18-microservices-networking)
* [19. Containers & Networking](#19-containers--networking)
* [20. Kubernetes Networking](#20-kubernetes-networking)
* [21. Database Networking](#21-database-networking)
* [22. VPC Architecture & Design](#22-vpc-architecture--design)
* [23. Debugging Network Issues](#23-debugging-network-issues)
* [24. Performance Optimization](#24-performance-optimization)
* [25. Network Monitoring & Observability](#25-network-monitoring--observability)
* [26. Deployment & Production Infrastructure](#26-deployment--production-infrastructure)

---

## 01. Introduction & Setup

🔗 **Full Lesson:** [01_Introduction_And_Setup.md](./01_Introduction_And_Setup.md)

* **What**: Guides developers in setting up network inspection and troubleshooting tools (Wireshark, curl, netstat, nmap, nslookup, etc.) and building a test project (Express API + WebSocket Server) to visualize real-world networking traffic.
* **Why It Exists**: High-level application code hides the underlying layers (DNS, TCP, TLS, HTTP/WS, IP/routing), making it hard to debug latency, dropped connections, or caching issues. This setup provides hands-on tools to observe what's actually happening beneath application code.
* **Key Concepts**:
  * **Tooling Stack**: `curl`, `ping`, `traceroute`, `nslookup`/`dig`, `netstat`/`ss`, `tcpdump`/`Wireshark`, `nmap`, `mtr`, `openssl s_client`.
  * **Node.js Express Server Setup**: Uses `express`, `socket.io`, `cors`, `redis`, `mongoose`.

### Key Commands:
```bash
curl -v http://localhost:3000/api/health
netstat -an | grep 3000
nc -zv google.com 443
```

---

## 02. How The Internet Actually Works

🔗 **Full Lesson:** [02_How_The_Internet_Actually_Works.md](./02_How_The_Internet_Actually_Works.md)

* **What**: Traces the physical and conceptual journey of data packets over fiber cables, routers, and DNS servers, detailing the complete lifecycle of a web request.
* **Why It Exists**: Information is bound by physics; data must be fragmented into packets and travel across physical distances, introducing latency. Understanding these components is critical for diagnosing performance, websocket drops, and timeout mismatches.
* **Key Concepts**:
  * **The Request Lifecycle**: Traces the steps of typing `https://myapp.com` (DNS resolution -> TCP 3-way handshake -> TLS handshake -> HTTP request/response -> browser rendering -> API calls).
  * **Undersea Cables & Light Speed**: Latency is physically limited by the speed of light in fiber (~200,000 km/s). NYC to Mumbai theoretical minimum is ~130ms; real RTT is ~160-200ms due to routing/processing.
  * **Websocket Drops**: Mid-route gateways (NATs/ALBs) drop idle connections after a timeout (AWS ALB: 60s, NAT Gateway: 350s). Solved with regular client-server heartbeats (Socket.IO default: 25s).
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
```

---

## 03. HTTP/HTTPS Internals

🔗 **Full Lesson:** [03_HTTP_HTTPS_Internals.md](./03_HTTP_HTTPS_Internals.md)

* **What**: Explains HTTP structure (Request/Response anatomy), differences between HTTP versions, and CORS.
* **Why It Exists**: Efficient API design requires managing headers, compression, caching (ETags), and properly configuring CORS policies to avoid browser blocker issues.
* **Key Concepts**:
  * **Anatomy**: Verb + Path + Version, Headers, Blank Line, Payload. The blank line tells parsers that the headers end and the body begins.
  * **HTTP/1.1 vs. HTTP/2 vs. HTTP/3**:
    * **HTTP/1.1**: Max 6 TCP connections per domain. Head-of-line blocking per connection. Plain text headers.
    * **HTTP/2**: Single TCP connection. Multiplexes streams. Compresses headers with HPACK. Binary framing.
    * **HTTP/3**: Uses QUIC over UDP. Eliminates TCP-level head-of-line blocking. 0-RTT/1-RTT connection setup.
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

app.use(compression());
app.use(cors({
  origin: ['https://myapp.com'],
  credentials: true,
  maxAge: 86400
}));
```

---

## 04. DNS Deep Dive

🔗 **Full Lesson:** [04_DNS_Deep_Dive.md](./04_DNS_Deep_Dive.md)

* **What**: Demystifies domain name resolution (Resolvers, TLDs, Root servers, Authoritative nameservers) and Route 53 policies.
* **Why It Exists**: DNS failures stall connection setups, causing slow page loads or downtime. Caching DNS lookups correctly in Node.js prevents per-request resolution latency.
* **Key Concepts**:
  * **Resolution Chain**: Browser Cache -> OS Cache -> Router -> ISP Recursive Resolver -> Root DNS (`.`) -> TLD Name Server (`.com`) -> Authoritative Name Server (Route 53) -> returns IP.
  * **Record Types**: `A` (IPv4), `AAAA` (IPv6), `CNAME` (Alias, cannot be at zone apex), `ALIAS` (Route 53 specific, maps domain to ALB/CloudFront directly at zone apex), `MX` (Mail), `TXT` (Verification/SPF/DKIM), `SRV` (Service discovery, used by MongoDB Atlas replica sets).
  * **Route 53 Policies**: Simple, Latency-based, Failover, Weighted, Geolocation, Multi-value.
  * **TTL (Time to Live)**: Duration DNS records are cached. Short TTLs facilitate fast updates during migrations. Long TTLs reduce DNS lookup queries.

### Key Commands:
```bash
dig api.myapp.com +trace
dig @8.8.8.8 api.myapp.com A
```

---

## 05. WebSockets & Real-Time

🔗 **Full Lesson:** [05_WebSockets_And_Real_Time.md](./05_WebSockets_And_Real_Time.md)

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

---

## 06. OSI Model Vs Real World

🔗 **Full Lesson:** [06_OSI_Model_Vs_Real_World.md](./06_OSI_Model_Vs_Real_World.md)

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
  * **TLS Encryption Scope**: TLS encrypts everything *above* Layer 4 (headers, path, query, body). It does NOT encrypt TCP ports, IP addresses, or DNS queries (unless using DoH).

### Key Commands:
```bash
netstat -an | grep :3000
curl -I https://example.com
```

---

## 07. TCP/IP Model

🔗 **Full Lesson:** [07_TCP_IP_Model.md](./07_TCP_IP_Model.md)

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

### Key Commands:
```bash
netstat -an | awk '/tcp/ {print $6}' | sort | uniq -c | sort -rn
sudo tcpdump -i any port 3000 -nn
```

---

## 09. UDP & When To Use It

🔗 **Full Lesson:** [09_UDP_And_When_To_Use_It.md](./09_UDP_And_When_To_Use_It.md)

* **What**: Focuses on UDP mechanics, datagram size constraints, and its integration in modern protocols like HTTP/3 (QUIC) and WebRTC.
* **Why It Exists**: UDP eliminates handshake and overhead costs (header is only 8 bytes vs. 20-60 bytes for TCP). Perfect for latency-sensitive, loss-tolerant streams.
* **Key Concepts**:
  * **Differences**: Stateless, fire-and-forget, no delivery checks, no flow control.
  * **DNS over UDP**: Resolvers query DNS servers via UDP port 53. If responses exceed 512 bytes, they fall back to TCP.
  * **HTTP/3 over QUIC**: QUIC runs on top of UDP. Implementing encryption and reliability at the application layer avoids TCP head-of-line blocking.
  * **Datagram MTU Limit**: Standard Ethernet MTU is 1500 bytes. Subtracting IP and UDP headers leaves a payload limit of ~1400 bytes. Larger payloads trigger IP fragmentation.

### Key Code Example:
```javascript
const dgram = require('dgram');
const client = dgram.createSocket('udp4');
const metric = Buffer.from('api.response_time:45|ms');
client.send(metric, 8125, 'statsd-server', (err) => {
  client.close();
});
```

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

### Key Commands:
```bash
openssl s_client -connect api.myapp.com:443 -servername api.myapp.com
echo | openssl s_client -connect api.myapp.com:443 2>/dev/null | openssl x509 -noout -dates
```

---

## 11. IP Addressing & Subnetting

🔗 **Full Lesson:** [11_IP_Addressing_And_Subnetting.md](./11_IP_Addressing_And_Subnetting.md)

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

### Key Code Example:
```javascript
// Check if an IP address falls within a CIDR block
function isIPInCIDR(ip, cidr) {
  const [network, bits] = cidr.split('/');
  const mask = -1 << (32 - parseInt(bits));
  const ipInt = ip.split('.').reduce((acc, oct) => (acc << 8) + parseInt(oct), 0);
  const netInt = network.split('.').reduce((acc, oct) => (acc << 8) + parseInt(oct), 0);
  return (ipInt & mask) === (netInt & mask);
}
```

---

## 12. Routing & NAT

🔗 **Full Lesson:** [12_Routing_And_NAT.md](./12_Routing_And_NAT.md)

* **What**: Covers VPC routing rules, CIDR specificity, and NAT (Network Address Translation) gateways.
* **Why It Exists**: Instances in private subnets require a NAT Gateway to fetch external updates or connect to public APIs, while remaining unreachable from the public internet.
* **Key Concepts**:
  * **Route Selection**: Longest prefix match wins. A route to `10.0.1.0/24` beats `10.0.0.0/16` and `0.0.0.0/0`.
  * **NAT Translation**: Translates private IPs to a public IP. The NAT Gateway maps ports to track which private instance initiated the outgoing connection.
  * **VPC Peering**: Directly links two VPCs with non-overlapping CIDRs via private routing.

### Key Commands:
```bash
curl https://ifconfig.me
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-xxxxx"
```

---

## 13. Load Balancing

🔗 **Full Lesson:** [13_Load_Balancing.md](./13_Load_Balancing.md)

* **What**: Explores load balancer types, load distribution algorithms, sticky sessions, and graceful shutdowns.
* **Why It Exists**: Achieving high availability and zero-downtime deployments requires distributing load and smoothly draining traffic before stopping Node.js servers.
* **Key Concepts**:
  * **ALB (Layer 7)**: Smart, path-based (`/api/*`) and host-based routing. Supports WebSockets. Latency overhead of 1-5ms.
  * **NLB (Layer 4)**: Fast, passes raw TCP connections (Redis, MongoDB, gRPC). Latency overhead <100 microseconds.
  * **Graceful Shutdown**: Upon receiving a SIGTERM signal, Node.js should set a flag to return 503 on health checks, stop accepting new connections, finish in-flight requests, and close database connections before exiting.
  * **Target Group Draining**: When an instance is deregistered, the ALB waits for a cooldown period to allow existing requests to complete.

### Key Code Example:
```javascript
process.on('SIGTERM', () => {
  isShuttingDown = true;
  server.close(async () => {
    await mongoose.connection.close();
    await redis.quit();
    process.exit(0);
  });
  setTimeout(() => process.exit(1), 30000);
});
```

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

### Key Nginx Config:
```nginx
location /socket.io/ {
    proxy_pass http://node_api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 86400s;
}
```

---

## 15. CDN & Caching

🔗 **Full Lesson:** [15_CDN_And_Caching.md](./15_CDN_And_Caching.md)

* **What**: Explores CDN edge caching (CloudFront) and application memory caching (Redis).
* **Why It Exists**: Serving content from edge servers reduces geographical latency. Multi-layer caching speeds up reads but requires invalidation planning.
* **Key Concepts**:
  * **Caching Layers**: Browser Cache -> CDN Cache -> Redis Cache -> DB Query Cache.
  * **Caching Golden Rule**: Closer to the user = faster, but harder to invalidate.
  * **Cache Busting**: Hashing filenames (e.g. `bundle.abc123.js`) allows long client caching. A deploy updates the filename, bypassing the cache.
  * **Redis Cache-Aside**: Check Redis first. If miss, query DB, write to Redis with a TTL, and return.

### Key Code Example:
```javascript
app.get('/api/products/:id', async (req, res) => {
  const key = `products:${req.params.id}`;
  const cached = await redis.get(key);
  if (cached) return res.json(JSON.parse(cached));
  
  const product = await Product.findById(req.params.id).lean();
  await redis.set(key, JSON.stringify(product), 'EX', 300);
  res.json(product);
});
```

---

## 16. Firewalls & Security

🔗 **Full Lesson:** [16_Firewalls_And_Security.md](./16_Firewalls_And_Security.md)

* **What**: Explains Security Groups (stateful), NACLs (stateless), WAF (Layer 7 filtering), and DDoS protections.
* **Why It Exists**: A secure infrastructure uses multiple firewall layers (Defense in Depth) to filter traffic by port, IP, and payload content.
* **Key Concepts**:
  * **Comparison**:
    * **Security Group**: Instance-level, stateful (automatically permits response traffic), allow-only rules.
    * **Network ACL**: Subnet-level, stateless (must explicitly allow both inbound and outbound traffic).
  * **AWS WAF**: Inspects HTTP content at Layer 7. Protects against SQL injection, XSS, rate limits by IP, and blocks known bad bots.
  * **Application Security**: `helmet` (HTTP headers), `express-rate-limit` (throttling).

### Key Code Example:
```javascript
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
app.use(helmet());
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
}));
```

---

## 17. API Gateways

🔗 **Full Lesson:** [17_API_Gateways.md](./17_API_Gateways.md)

* **What**: Covers centralized API Gateways (AWS API Gateway vs. custom Express gateways) and pattern designs.
* **Why It Exists**: Moving cross-cutting concerns (auth, rate limiting, CORS) to the gateway layer simplifies microservices.
* **Key Concepts**:
  * **Patterns**: Serverless (API Gateway -> Lambda -> DB) vs. Traditional (API Gateway -> ALB -> EC2).
  * **AWS API Gateway Types**:
    * **HTTP API**: Lightweight, fast, low latency ($1/million requests).
    * **REST API**: Supports request validation, caching, API keys, and WAF integration ($3.50/million requests).
  * **Limitations**: Max execution timeout is 29 seconds (REST API) or 30 seconds (HTTP API). Payload size is limited to 10MB.

### Key Code Example:
```javascript
app.use('/api/orders', createProxyMiddleware({
  target: 'http://order-service:3002',
  changeOrigin: true,
  onProxyReq: (proxyReq, req) => {
    proxyReq.setHeader('x-user-id', req.user.id);
  }
}));
```

---

## 18. Microservices Networking

🔗 **Full Lesson:** [18_Microservices_Networking.md](./18_Microservices_Networking.md)

* **What**: Discusses microservices communication patterns, service discovery, and circuit breakers.
* **Why It Exists**: Distributed architectures introduce latency and new failure modes. Circuit breakers and async queues prevent cascading service failures.
* **Key Concepts**:
  * **Communication**: Sync (REST, gRPC) vs. Async (SQS queues, Pub/Sub event buses like SNS/Kafka).
  * **Service Discovery**: DNS-based (Cloud Map), Load Balancer paths, or service meshes (App Mesh).
  * **Circuit Breaker**: Prevents calling down services. Once failures exceed a threshold, the circuit opens, failing requests immediately.
  * **Distributed Tracing**: Generate an `X-Request-ID` at the gateway and pass it along all downstream network hops.

### Key Code Example:
```javascript
class CircuitBreaker {
  constructor(action, threshold = 5) {
    this.action = action;
    this.threshold = threshold;
    this.failures = 0;
    this.state = 'CLOSED';
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

---

## 19. Containers & Networking

🔗 **Full Lesson:** [19_Containers_And_Networking.md](./19_Containers_And_Networking.md)

* **What**: Covers Docker networking modes, Compose setups, and ECS Fargate awsvpc integrations.
* **Why It Exists**: Running containers requires isolating their networking interfaces while allowing dynamic service discovery by name.
* **Key Concepts**:
  * **Modes**: Bridge (default private IP), Host (shares host network), None (isolated), awsvpc (ECS task gets unique ENI and VPC IP).
  * **Docker Compose DNS**: Resolves service names defined in `docker-compose.yml` to their bridge network IPs.
  * **awsvpc Mode Benefits**: No port mapping bottlenecks. SGs attach directly to tasks, simplifying RDS white-listing.

### Key Compose Snippet:
```yaml
services:
  api:
    build: .
    environment:
      - MONGO_URI=mongodb://mongodb:27017/myapp
  mongodb:
    image: mongo:7.0
```

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

### Key Policy Spec:
```yaml
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
              app: api
```

---

## 21. Database Networking

🔗 **Full Lesson:** [21_Database_Networking.md](./21_Database_Networking.md)

* **What**: Covers database connection pools, read replicas, and NAT gateway timeouts.
* **Why It Exists**: Database queries run over TCP. Reusing connections in a pool prevents connection overhead from slowing down queries.
* **Key Concepts**:
  * **Connection Pools**: Maintain open connections to reuse for queries. Limit size to avoid exhausting database connections.
  * **Read Scaling**: Route writes to the Primary DB and reads to Read Replicas (handles read volume, accepts replication lag).
  * **NAT Timeout**: AWS NAT Gateways drop idle connections after 350s. Set TCP keep-alive to <120s on database pools.

### Key Code Example:
```javascript
const mongoose = require('mongoose');
mongoose.connect(process.env.MONGO_URI, {
  maxPoolSize: 10,
  minPoolSize: 2,
  keepAlive: true,
  keepAliveInitialDelay: 120000
});
```

---

## 22. VPC Architecture & Design

🔗 **Full Lesson:** [22_VPC_Architecture_And_Design.md](./22_VPC_Architecture_And_Design.md)

* **What**: Details VPC layouts, three-tier subnets, peering, and VPC endpoints.
* **Why It Exists**: Designing VPCs with separate public, private, and isolated tiers isolates critical workloads and prevents unauthorized access.
* **Key Concepts**:
  * **Three-Tier VPC Layout**: Public (ALB, NAT Gateway), Private App (ECS/EC2 tasks), Isolated Data (RDS, ElastiCache - no internet route).
  * **Multi-AZ Resilience**: Distribute subnets across 2+ Availability Zones. If one AZ goes down, the ALB fails over to the other.
  * **VPC Endpoints**: Route AWS services internally. Gateway endpoints (S3, DynamoDB) are free and save NAT Gateway transfer costs.

### Key Commands:
```bash
# AWS CLI: Create a VPC Endpoint for S3 (Gateway type)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-xxxxx \
  --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids rtb-xxxxx
```

---

## 23. Debugging Network Issues

🔗 **Full Lesson:** [23_Debugging_Network_Issues.md](./23_Debugging_Network_Issues.md)

* **What**: Provides a methodology and tools for troubleshooting network issues.
* **Why It Exists**: Diagnosing production issues requires systematically verifying the network stack from the bottom up to save time.
* **Key Concepts**:
  * **Debugging Methodology**: DNS -> IP Connectivity -> TCP -> TLS -> HTTP -> Application.
  * **Common Errors**: `ECONNREFUSED` (service down), `ETIMEDOUT` (packets blocked), `ECONNRESET` (connection closed), `502 Bad Gateway` (ALB can't reach backend), `504 Gateway Timeout` (timeout exceeded).

### Key Commands:
```bash
nc -zv api.myapp.com 443
curl -w "DNS: %{time_namelookup}s TCP: %{time_connect}s TLS: %{time_appconnect}s TTFB: %{time_starttransfer}s Total: %{time_total}s\n" -o /dev/null -s https://api.myapp.com/api/health
```

---

## 24. Performance Optimization

🔗 **Full Lesson:** [24_Performance_Optimization.md](./24_Performance_Optimization.md)

* **What**: Focuses on performance budgets, keep-alive connections, compression, and payload optimization.
* **Why It Exists**: Latency is a critical performance metric. Minimizing connection overhead and payload sizes speeds up page loads.
* **Key Concepts**:
  * **Latency vs. Throughput**: Latency is the time for a single round trip; throughput is the volume of requests processed per second.
  * **Optimization Checklist**: Cache DNS queries, reuse TCP connections (Keep-Alive), enable compression (Gzip/Brotli), use HTTP/2, paginate API responses, and use CDN edge caching.

### Key Code Example:
```javascript
const https = require('https');
const agent = new https.Agent({
  keepAlive: true,
  maxSockets: 50,
  maxFreeSockets: 10
});
```

---

## 25. Network Monitoring & Observability

🔗 **Full Lesson:** [25_Network_Monitoring_And_Observability.md](./25_Network_Monitoring_And_Observability.md)

* **What**: Explores metrics, logs, traces, CloudWatch alarms, and VPC Flow Logs.
* **Why It Exists**: Observability tools alert you to errors and latency spikes before they affect users.
* **Key Concepts**:
  * **Three Pillars**: Metrics (numerical data like CloudWatch CPU/latency), Logs (structured JSON events), Traces (path of requests across services like X-Ray).
  * **VPC Flow Logs**: Captures metadata of all traffic in the VPC. Useful for finding blocked connections (`REJECT` actions).
  * **Prometheus Metrics**: Expose `/metrics` to scrape CPU, memory, and HTTP response latencies.

### Key Commands:
```bash
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

---

## 26. Deployment & Production Infrastructure

🔗 **Full Lesson:** [26_Deployment_And_Production_Infrastructure.md](./26_Deployment_And_Production_Infrastructure.md)

* **What**: Synthesizes the architecture (DNS, CDN, ALB, EC2, RDS, Redis, CI/CD) for deploying production-grade applications.
* **Why It Exists**: Deploying full-stack applications with high availability and security requires integrating all layers of the networking stack.
* **Key Concepts**:
  * **Production Architecture**: Route 53 (DNS) -> CloudFront (CDN, TLS termination, static S3 files) -> ALB (routing) -> Auto Scaling Group EC2 (App) -> RDS Multi-AZ + Redis (Data).
  * **Rolling Deployments**: CodeDeploy/ECS updates one instance at a time. ALB redirects traffic after readiness probes pass.
  * **Disaster Recovery (DR)**: Backup & Restore, Pilot Light, Warm Standby, Active-Active.

### Key Compose / Pipeline Snippet:
```yaml
- name: Deploy to ECS
  run: |
    aws ecs update-service \
      --cluster production-cluster \
      --service api-service \
      --force-new-deployment
```

---

Previous : [00_Index.md](./00_Index.md) | Index : [00_Index.md](./00_Index.md) | Next : [01_Introduction_And_Setup.md](./01_Introduction_And_Setup.md)
