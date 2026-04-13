# TCP/IP Model

> 📌 **File:** 03_TCP_IP_Model.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

The TCP/IP model is what the internet **actually runs on** — a 4-layer protocol stack that every device uses. Unlike the 7-layer OSI model (academic), TCP/IP is pragmatic: Application, Transport, Internet, Network Access. Every request your React app makes, every MongoDB query, every Redis operation — all use this exact stack.

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  TCP/IP Layer       │ Protocol        │ Your Stack                      │
├─────────────────────┼─────────────────┼─────────────────────────────────┤
│  4. Application     │ HTTP, WS, DNS,  │ Express routes, fetch(),        │
│                     │ MongoDB Wire,   │ Socket.IO, mongoose.connect(),  │
│                     │ Redis RESP      │ redis.get(), DNS resolution     │
├─────────────────────┼─────────────────┼─────────────────────────────────┤
│  3. Transport       │ TCP, UDP        │ TCP: APIs, DB connections       │
│                     │                 │ UDP: DNS lookups, video streams │
├─────────────────────┼─────────────────┼─────────────────────────────────┤
│  2. Internet        │ IP (v4/v6),     │ EC2 private/public IPs,         │
│                     │ ICMP            │ VPC subnets, routing, NAT       │
├─────────────────────┼─────────────────┼─────────────────────────────────┤
│  1. Network Access  │ Ethernet, WiFi, │ AWS ENI, data center switches,  │
│                     │ ARP             │ your laptop's WiFi adapter      │
└─────────────────────┴─────────────────┴─────────────────────────────────┘
```

### Protocol Stack for Every Request Type

```
┌──────────────────────────────────────────────────────────────────┐
│  Action                    │ Protocol Stack (top → bottom)       │
├────────────────────────────┼─────────────────────────────────────┤
│  fetch('/api/users')       │ HTTP → TLS → TCP → IP → Ethernet   │
│  mongoose.connect()        │ MongoDB → TLS → TCP → IP → Ethernet│
│  redis.get('key')          │ RESP → TCP → IP → Ethernet         │
│  io.connect()              │ WS → TLS → TCP → IP → Ethernet     │
│  DNS lookup (dig)          │ DNS → UDP → IP → Ethernet           │
│  ping google.com           │ ICMP → IP → Ethernet                │
│  S3 putObject              │ HTTP → TLS → TCP → IP → Ethernet   │
│  Lambda invoke             │ HTTP → TLS → TCP → IP → Ethernet   │
├────────────────────────────┴─────────────────────────────────────┤
│  Notice: EVERYTHING goes through IP → Ethernet at the bottom.   │
│  The application protocol (HTTP, MongoDB, Redis) sits on top.   │
│  TCP or UDP is the transport choice.                             │
└──────────────────────────────────────────────────────────────────┘
```

---

## Why this matters in real systems

### Connection Lifecycle in Your App

```
Your Node.js server manages HUNDREDS of simultaneous connections,
each at a different stage of the TCP/IP lifecycle:

Active connections on a typical Express server:
┌────────────────────────────────────────────────────────────────┐
│  Connection Type    │ Count  │ Transport │ Application Proto  │
├─────────────────────┼────────┼───────────┼────────────────────┤
│  Client HTTP reqs   │ ~50    │ TCP:443   │ HTTP/1.1 or /2     │
│  MongoDB pool       │ 10     │ TCP:27017 │ MongoDB Wire       │
│  Redis pool         │ 5      │ TCP:6379  │ RESP               │
│  WebSocket clients  │ ~200   │ TCP:443   │ WebSocket          │
│  External APIs      │ ~10    │ TCP:443   │ HTTP/1.1           │
├─────────────────────┼────────┼───────────┼────────────────────┤
│  Total TCP conns    │ ~275   │           │                    │
└─────────────────────┴────────┴───────────┴────────────────────┘

Each TCP connection = file descriptor = memory + CPU
Node.js can handle ~50,000 concurrent TCP connections (event loop)
PostgreSQL can handle ~100-500 connections (process-per-connection)
This is WHY connection pooling matters!
```

### Port Allocation

```
┌──────────────────────────────────────────────────────────────┐
│  Port     │ Service              │ Your Usage                │
├───────────┼──────────────────────┼───────────────────────────┤
│  80       │ HTTP                 │ Nginx / ALB listener      │
│  443      │ HTTPS                │ Nginx / ALB (TLS)         │
│  3000     │ Node.js (Express)    │ Your API server           │
│  3001     │ React dev server     │ next dev / react-scripts  │
│  5432     │ PostgreSQL           │ RDS connection            │
│  27017    │ MongoDB              │ Atlas / local MongoDB     │
│  6379     │ Redis                │ ElastiCache / local Redis │
│  53       │ DNS                  │ Route 53 (UDP + TCP)      │
│  22       │ SSH                  │ EC2 access                │
├───────────┼──────────────────────┼───────────────────────────┤
│  1-1023   │ Well-known ports     │ Require root/admin        │
│  1024-    │ Ephemeral ports      │ Client source ports       │
│  49152+   │ Dynamic/private      │ Auto-assigned by OS       │
└───────────┴──────────────────────┴───────────────────────────┘

When your browser connects to https://api.myapp.com:
  Source: your-ip:52341  (ephemeral port, random)
  Dest:   54.23.189.12:443  (server IP, HTTPS port)

When Node.js connects to MongoDB:
  Source: 10.0.1.5:49152  (ephemeral)
  Dest:   10.0.2.10:27017  (MongoDB port)
```

---

## How does it actually work?

### Layer-by-Layer Breakdown

#### Layer 4: Application

```javascript
// You write application-layer code
// HTTP, WebSocket, database protocols

// Express creates HTTP messages:
app.get('/api/users', (req, res) => {
  // req = parsed HTTP request (method, path, headers, body)
  // res = HTTP response builder (status, headers, body)
  res.json({ users: [] });
  // Internally creates:
  // HTTP/1.1 200 OK\r\n
  // Content-Type: application/json\r\n
  // Content-Length: 13\r\n
  // \r\n
  // {"users":[]}
});
```

#### Layer 3: Transport (TCP/UDP)

```
TCP guarantees:
  ✅ Delivery (retransmits lost packets)
  ✅ Order (reassembles out-of-order packets)
  ✅ No duplicates
  ✅ Flow control (sender doesn't overwhelm receiver)
  ✅ Congestion control (doesn't overwhelm network)
  Cost: 3-way handshake (1.5 RTT), per-segment overhead

UDP guarantees:
  ❌ No delivery guarantee
  ❌ No order guarantee
  ❌ No flow/congestion control
  Benefit: No handshake, minimal overhead, low latency
  
Your stack uses TCP for almost everything.
UDP for: DNS lookups, real-time video (WebRTC), some game protocols.
```

#### Layer 2: Internet (IP)

```
IP provides:
  - Addressing: Every device gets a unique IP (like a postal address)
  - Routing: Routers forward packets toward the destination
  - Fragmentation: Large data split across multiple packets

IP does NOT guarantee:
  ❌ Delivery (packets can be dropped)
  ❌ Order (packets can arrive rearranged)
  ❌ Integrity (packets can be corrupted)
  → That's TCP's job (Layer 3)
  
Your EC2 instance has:
  Private IP: 10.0.1.5 (inside VPC, for internal communication)
  Public IP: 54.23.189.12 (internet-facing, via Internet Gateway)
  
NAT translation:
  Internal: 10.0.1.5:3000 ←→ External: 54.23.189.12:443
  (Internet Gateway / NAT Gateway handles this)
```

#### Layer 1: Network Access

```
Handles:
  - Physical medium (copper, fiber, WiFi)
  - MAC addresses (hardware addresses)
  - Framing (wrapping IP packets in Ethernet frames)
  - Error detection (CRC checksum)
  
AWS handles this entirely. You never touch it.
Inside a VPC, AWS uses virtual networking (SDN).
```

---

## Visual Diagram — Request Through TCP/IP Stack

```
React: fetch('https://api.myapp.com/api/users')

CLIENT SIDE                               SERVER SIDE
┌─────────────────┐                       ┌─────────────────┐
│  Application    │                       │  Application    │
│  HTTP GET /api/ │                       │  Express router │
│  users          │                       │  processes req  │
├─────────────────┤                       ├─────────────────┤
│  Transport      │                       │  Transport      │
│  TCP segment    │                       │  TCP segment    │
│  Src:52341      │                       │  Src:443        │
│  Dst:443        │                       │  Dst:52341      │
├─────────────────┤                       ├─────────────────┤
│  Internet       │                       │  Internet       │
│  IP packet      │                       │  IP packet      │
│  Src:203.0.113.5│    ─── Network ───    │  Src:54.23.189  │
│  Dst:54.23.189  │  (routers, switches)  │  Dst:203.0.113.5│
├─────────────────┤                       ├─────────────────┤
│  Network Access │                       │  Network Access │
│  Ethernet/WiFi  │                       │  Ethernet (EC2) │
└─────────────────┘                       └─────────────────┘
```

---

## Node.js Implementation

```javascript
// See TCP/IP details from Node.js
const net = require('net');
const dns = require('dns');
const os = require('os');

// ──── Layer 3 (Transport): Create a raw TCP server ────
const server = net.createServer((socket) => {
  // TCP connection details
  console.log('New TCP connection:');
  console.log(`  Remote: ${socket.remoteAddress}:${socket.remotePort}`);
  console.log(`  Local:  ${socket.localAddress}:${socket.localPort}`);
  console.log(`  Keep-Alive: ${socket.keepAlive}`);
  
  // Set TCP options
  socket.setKeepAlive(true, 60000);  // Send keep-alive probes every 60s
  socket.setNoDelay(true);           // Disable Nagle's algorithm (send immediately)
  socket.setTimeout(30000);          // 30 second idle timeout
  
  socket.on('timeout', () => {
    console.log('Connection timed out');
    socket.end();
  });
  
  socket.on('data', (data) => {
    console.log(`  Received ${data.length} bytes`);
    socket.write(`Echo: ${data}`);
  });
  
  socket.on('close', (hadError) => {
    console.log(`  Connection closed (error: ${hadError})`);
  });
});

server.listen(8080, () => {
  const addr = server.address();
  console.log(`TCP server listening on ${addr.address}:${addr.port}`);
});

// ──── Layer 2 (Internet): DNS Resolution ────
async function inspectDNS(hostname) {
  console.log(`\nDNS resolution for: ${hostname}`);
  
  // A records (IPv4)
  const ipv4 = await dns.promises.resolve4(hostname);
  console.log(`  IPv4 (A records): ${ipv4.join(', ')}`);
  
  // AAAA records (IPv6)
  try {
    const ipv6 = await dns.promises.resolve6(hostname);
    console.log(`  IPv6 (AAAA records): ${ipv6.join(', ')}`);
  } catch { console.log('  IPv6: not configured'); }
  
  // MX records (mail)
  try {
    const mx = await dns.promises.resolveMx(hostname);
    mx.forEach(r => console.log(`  MX: ${r.exchange} (priority: ${r.priority})`));
  } catch { console.log('  MX: not configured'); }
  
  // NS records (nameservers)
  const ns = await dns.promises.resolveNs(hostname);
  console.log(`  NS: ${ns.join(', ')}`);
}

inspectDNS('google.com');

// ──── Layer 1 (Network Access): Network Interfaces ────
console.log('\nNetwork Interfaces:');
const interfaces = os.networkInterfaces();
Object.entries(interfaces).forEach(([name, addrs]) => {
  addrs.forEach(addr => {
    console.log(`  ${name}: ${addr.address} (${addr.family}, MAC: ${addr.mac})`);
    //                       ^Layer 2(IP)     ^Layer 2        ^Layer 1(MAC)
  });
});
```

---

## SQL vs Networking Thinking

```
┌──────────────────────────────────────────────────────────────────┐
│  Database Concept       │ Networking Equivalent                  │
├─────────────────────────┼────────────────────────────────────────┤
│  Database connection    │ TCP connection (3-way handshake)       │
│  Connection pool        │ TCP connection pool (reuse sockets)    │
│  Query timeout          │ TCP socket timeout                     │
│  Transaction isolation  │ TCP stream isolation (per connection)  │
│  Index lookup           │ DNS lookup (name → address)            │
│  COMMIT                 │ TCP ACK (data received confirmation)   │
│  Connection refused     │ TCP RST (port not listening)           │
│  Max connections        │ File descriptor limit / port range     │
│  Replication lag        │ Network latency between primary/replica│
└─────────────────────────┴────────────────────────────────────────┘
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────────┐
│  TCP/IP Connection Costs                                        │
├───────────────────────────────┬──────────────────────────────────┤
│  New TCP connection           │ 1.5 RTT (handshake)              │
│  New TCP + TLS 1.2            │ 3.5 RTT (TCP + TLS)              │
│  New TCP + TLS 1.3            │ 2.5 RTT (TCP + TLS, fewer trips)│
│  Reused TCP (keep-alive)      │ 0 RTT (already connected)        │
│  Reused TCP + TLS resumption  │ 1 RTT (session ticket)           │
├───────────────────────────────┴──────────────────────────────────┤
│                                                                  │
│  Same region (us-east-1 → us-east-1): RTT ≈ 1ms                │
│    New connection cost: ~3.5ms (negligible)                      │
│                                                                  │
│  Cross-region (us-east-1 → ap-south-1): RTT ≈ 200ms            │
│    New connection cost: ~700ms (significant!)                    │
│    Reused connection: ~0ms overhead                              │
│                                                                  │
│  This is why connection pooling (MongoDB, Redis, PostgreSQL)    │
│  is critical for cross-region architectures.                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Not Understanding Port Conflicts

```bash
# Error: EADDRINUSE :::3000
# Another process is already using port 3000

# Find what's using the port:
lsof -i :3000              # Linux/Mac
netstat -ano | findstr 3000 # Windows

# Kill it:
kill -9 <PID>               # Linux/Mac
taskkill /PID <PID> /F      # Windows
```

### ❌ Confusing TCP and HTTP Timeouts

```javascript
// TCP timeout: connection-level (no data flowing)
server.setTimeout(60000);     // Close idle TCP connections after 60s

// HTTP timeout: request-level (how long to wait for a response)
server.requestTimeout = 30000; // Close request if not completed in 30s

// Both matter:
// TCP timeout prevents zombie connections
// HTTP timeout prevents stuck requests
// ALB idle timeout overrides both (default: 60s)
```

---

## Practice Exercises

### Exercise 1: Identify Protocol Stack

For each scenario, list the complete protocol stack (Application → Physical):
1. Browser loads `https://myapp.com/dashboard`
2. Node.js queries PostgreSQL on RDS
3. Redis cache lookup
4. DNS lookup for `api.example.com`

### Exercise 2: Connection Counting

Start your Express server, make 10 requests with `curl`, and use `netstat` to observe:
1. How many TCP connections were created?
2. What state are they in? (ESTABLISHED, TIME_WAIT, etc.)
3. What happens if you add `Connection: close` header?

---

## Interview Q&A

**Q1: What are the layers of the TCP/IP model?**
> Application (HTTP, DNS, SMTP), Transport (TCP, UDP), Internet (IP, ICMP), Network Access (Ethernet, WiFi). This is what the internet actually uses — the OSI model is a reference framework.

**Q2: Why does TCP need a 3-way handshake?**
> Both sides need to synchronize sequence numbers and confirm reachability. SYN establishes client→server, SYN-ACK confirms and establishes server→client, ACK confirms. Without this, either side could send data into the void.

**Q3: When would you choose UDP over TCP?**
> DNS lookups (single request-response, no connection needed), real-time video/audio (WebRTC — dropped frames are better than delayed frames), gaming (position updates — latest data matters, old data is stale), IoT sensor data (fire-and-forget).

**Q4: What is a port and why does it matter?**
> A 16-bit number (0-65535) that identifies a specific service on a host. IP gets the packet to the machine; the port directs it to the right process. Without ports, a machine could only run one network service at a time.

**Q5: What happens when you run out of ephemeral ports?**
> The OS has a limited range of ephemeral ports (~16,000-48,000). Each outbound TCP connection uses one. In TIME_WAIT state, ports aren't reusable for ~60 seconds. Under heavy load (many short-lived connections), you can exhaust ports. Fix: connection pooling, SO_REUSEADDR, reduce TIME_WAIT.


Prev : [02 OSI Model Vs Real World](./02_OSI_Model_Vs_Real_World.md) | Index: [0 Index](./0_Index.md) | Next : [04 IP Addressing And Subnetting](./04_IP_Addressing_And_Subnetting.md)
