# TCP Deep Dive

> 📌 **File:** 07_TCP_Deep_Dive.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

TCP (Transmission Control Protocol) is the reliable transport layer beneath HTTP, WebSocket, MongoDB, Redis, and PostgreSQL. It guarantees delivery, ordering, and flow control. Every API call, every database query, every WebSocket message rides on TCP. Understanding TCP explains why connections timeout, why keep-alive matters, and why your app behaves differently under load.

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Your Code                       │ TCP Reality                      │
├──────────────────────────────────┼──────────────────────────────────┤
│  fetch() → response             │ TCP 3-way handshake → data →ACK │
│  mongoose.connect()              │ TCP connection to port 27017     │
│  redis.get()                     │ TCP send command, await reply    │
│  socket.io connection            │ TCP handshake→HTTP upgrade→data │
│  ECONNREFUSED error              │ TCP RST (port not listening)     │
│  ETIMEDOUT error                 │ TCP SYN sent, no SYN-ACK back   │
│  ECONNRESET error                │ TCP RST (connection killed)      │
│  Connection pool maxSize: 10     │ 10 TCP sockets maintained        │
│  Keep-alive                      │ TCP connection reused            │
│  ALB idle timeout: 60s           │ Closes TCP after 60s no data    │
│  Slow API under load             │ TCP congestion window shrinking  │
└──────────────────────────────────┴──────────────────────────────────┘
```

---

## How does it actually work?

### 3-Way Handshake (Connection Setup)

```
Client                          Server
  │                                │
  │  SYN (seq=100)                │   "I want to connect"
  │ ──────────────────────────►   │
  │                                │
  │  SYN-ACK (seq=300, ack=101)   │   "OK, I'm ready too"
  │ ◄──────────────────────────   │
  │                                │
  │  ACK (ack=301)                │   "Great, let's talk"
  │ ──────────────────────────►   │
  │                                │
  │  ═══ Connection ESTABLISHED ══│
  │                                │
  Cost: 1.5 RTT (round-trip times)
  Same region: 1.5 × 1ms = 1.5ms
  Cross-continent: 1.5 × 200ms = 300ms ← THIS IS WHY LATENCY MATTERS
```

### Data Transfer

```
Client                          Server
  │                                │
  │  DATA (seq=101, 500 bytes)    │
  │ ──────────────────────────►   │
  │                                │
  │  ACK (ack=601)                │   "Got bytes 101-600"
  │ ◄──────────────────────────   │
  │                                │
  │  DATA (seq=601, 500 bytes)    │
  │ ──────────────────────────►   │
  │                                │
  │  ACK (ack=1101)               │   "Got bytes 601-1100"
  │ ◄──────────────────────────   │

  TCP guarantees:
  ✅ Every byte is delivered (retransmits on loss)
  ✅ Bytes arrive in order (reassembles if out of order)
  ✅ No duplicates (sequence numbers detect dupes)
  ✅ Flow control (receiver tells sender how fast to go)
  ✅ Congestion control (adapts to network capacity)
```

### Connection Teardown (4-Way Handshake)

```
Client                          Server
  │                                │
  │  FIN                           │   "I'm done sending"
  │ ──────────────────────────►   │
  │                                │
  │  ACK                           │   "OK, noted"
  │ ◄──────────────────────────   │
  │                                │
  │  FIN                           │   "I'm done too"
  │ ◄──────────────────────────   │
  │                                │
  │  ACK                           │   "OK, goodbye"
  │ ──────────────────────────►   │
  │                                │
  │  ═══ TIME_WAIT (2 min) ═══   │   Client waits to handle late packets
```

### TCP States You'll See

```
┌────────────────┬────────────────────────────────────────────────────┐
│ State          │ What It Means                                      │
├────────────────┼────────────────────────────────────────────────────┤
│ LISTEN         │ Server waiting for connections (your Express app) │
│ SYN_SENT       │ Client sent SYN, waiting for SYN-ACK              │
│ SYN_RECEIVED   │ Server got SYN, sent SYN-ACK, waiting for ACK    │
│ ESTABLISHED    │ Connection active — data flowing                  │
│ FIN_WAIT_1     │ Sent FIN, waiting for ACK                         │
│ FIN_WAIT_2     │ Got ACK for our FIN, waiting for their FIN       │
│ TIME_WAIT      │ Connection closed, waiting 2 min (prevents dupes) │
│ CLOSE_WAIT     │ Remote side closed, we haven't closed yet ⚠️     │
│ LAST_ACK       │ Sent FIN, waiting for final ACK                   │
│ CLOSED         │ Connection fully terminated                        │
├────────────────┴────────────────────────────────────────────────────┤
│ CLOSE_WAIT accumulation = your app isn't closing connections!      │
│ TIME_WAIT accumulation = too many short-lived connections (normal) │
│ SYN_SENT stuck = server unreachable (firewall, wrong IP)          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Why this matters in real systems

### Scenario: "Why does my app slow down under load?"

```
TCP Congestion Control (Slow Start):

New connection starts with small congestion window (cwnd = ~14KB)
Gradually increases as ACKs come back:
  RTT 1: cwnd = 14KB  → can send 14KB unacknowledged
  RTT 2: cwnd = 28KB  → doubles
  RTT 3: cwnd = 56KB  → doubles again
  RTT 4: cwnd = 112KB → getting fast now
  ...
  RTT 10: cwnd = 7MB+ → full speed

If a packet is lost (congestion detected):
  cwnd drops by HALF → speed crashes → slow recovery

For a 500KB API response on a NEW connection:
  HTTP/1.1: Need ~5 RTTs to transfer (slow start limits throughput)
  Keep-alive: Already at full speed → 1-2 RTTs

This is why CONNECTION REUSE is critical.
```

### Scenario: "MongoDB/Redis connections going stale"

```
TCP Keep-Alive:
  After a connection is idle, TCP sends probe packets to check if
  the other side is still alive.

  Linux defaults:
    tcp_keepalive_time = 7200s (2 hours before first probe!)
    tcp_keepalive_intvl = 75s (between probes)
    tcp_keepalive_probes = 9 (give up after 9 failed probes)

  Problem: AWS NAT Gateway has a 350-second idle timeout.
  If your MongoDB connection is idle for 350s → NAT drops it.
  Next query → ECONNRESET (connection was silently killed).

  Fix: Set TCP keep-alive shorter than NAT timeout:
    socket.setKeepAlive(true, 120000); // 120 seconds
```

---

## Node.js Implementation

```javascript
const net = require('net');

// ──── TCP Server (see raw TCP) ────
const server = net.createServer((socket) => {
  console.log('New connection:', {
    remote: `${socket.remoteAddress}:${socket.remotePort}`,
    local: `${socket.localAddress}:${socket.localPort}`,
    bufferSize: socket.bufferSize,
    bytesRead: socket.bytesRead
  });
  
  // TCP Keep-Alive (critical for long-lived connections)
  socket.setKeepAlive(true, 120000);  // Probe every 120s
  socket.setNoDelay(true);            // Disable Nagle (send immediately)
  socket.setTimeout(30000);           // 30s idle timeout
  
  socket.on('data', (data) => {
    console.log(`Received: ${data.length} bytes, total: ${socket.bytesRead}`);
    socket.write(`Echo: ${data}`);
  });
  
  socket.on('timeout', () => {
    console.log('Socket timeout — closing');
    socket.end();
  });
  
  socket.on('error', (err) => {
    console.log(`Socket error: ${err.code} — ${err.message}`);
    // ECONNRESET: remote side killed connection
    // EPIPE: writing to closed connection
    // ETIMEDOUT: connection timed out
  });
  
  socket.on('close', (hadError) => {
    console.log(`Connection closed (error: ${hadError})`);
  });
});

server.maxConnections = 1000;  // Limit concurrent connections
server.listen(8080);

// ──── TCP Client with Connection Pool ────
class TCPPool {
  constructor(host, port, maxSize = 10) {
    this.host = host;
    this.port = port;
    this.maxSize = maxSize;
    this.pool = [];
    this.waiting = [];
  }
  
  async getConnection() {
    // Reuse existing idle connection
    const idle = this.pool.find(c => !c.inUse && !c.destroyed);
    if (idle) {
      idle.inUse = true;
      return idle;
    }
    
    // Create new if under limit
    if (this.pool.length < this.maxSize) {
      return this._createConnection();
    }
    
    // Wait for a connection to become available
    return new Promise((resolve) => this.waiting.push(resolve));
  }
  
  _createConnection() {
    return new Promise((resolve, reject) => {
      const socket = net.createConnection(this.port, this.host);
      socket.setKeepAlive(true, 120000);
      socket.inUse = true;
      
      socket.on('connect', () => {
        this.pool.push(socket);
        resolve(socket);
      });
      
      socket.on('error', reject);
    });
  }
  
  release(socket) {
    socket.inUse = false;
    if (this.waiting.length > 0) {
      socket.inUse = true;
      this.waiting.shift()(socket);
    }
  }
}
```

### Express Keep-Alive Configuration

```javascript
const http = require('http');
const express = require('express');
const app = express();

const server = http.createServer(app);

// TCP-level settings
server.keepAliveTimeout = 65000;          // Keep TCP alive for 65s (> ALB's 60s)
server.headersTimeout = 66000;            // Slightly more than keepAliveTimeout
server.maxHeadersCount = 100;             // Limit header count
server.timeout = 120000;                  // Max request processing time (2 min)

// Track connections
let connectionCount = 0;
server.on('connection', (socket) => {
  connectionCount++;
  console.log(`Connections: ${connectionCount}`);
  socket.on('close', () => {
    connectionCount--;
  });
});

server.listen(3000);
```

---

## Commands & Debugging Tools

```bash
# See TCP connections
netstat -an | grep ESTABLISHED    # All active connections
netstat -an | grep :3000          # Connections to your server
ss -s                             # Connection summary stats
ss -tlnp                          # Listening TCP ports with PIDs

# TCP connection states count
netstat -an | awk '/tcp/ {print $6}' | sort | uniq -c | sort -rn
# Example output:
# 150 ESTABLISHED
#  45 TIME_WAIT
#  10 CLOSE_WAIT  ← potential leak!
#   3 LISTEN

# Capture TCP packets
sudo tcpdump -i any port 3000 -nn
# Flags: S=SYN, .=ACK, F=FIN, R=RST, P=PUSH
# S  → connection start
# S. → SYN-ACK
# .  → ACK
# F. → connection close
# R  → connection reset (error!)

# Detailed packet capture
sudo tcpdump -i any port 3000 -A    # Show ASCII content
sudo tcpdump -i any port 3000 -X    # Show hex + ASCII

# Test TCP connectivity
nc -zv api.myapp.com 443           # Test if port is open
nc -zv 10.0.10.5 5432              # Test PostgreSQL port
nc -zv 10.0.10.15 6379             # Test Redis port
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────────┐
│  TCP Performance Tips                                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Connection pooling (MongoDB, Redis, PostgreSQL)             │
│     New conn: 1.5 RTT overhead. Pooled: 0 RTT.                 │
│                                                                  │
│  2. Keep-alive (HTTP connections)                               │
│     server.keepAliveTimeout = 65000 (> ALB timeout)             │
│     Avoids TCP+TLS handshake on every request                   │
│                                                                  │
│  3. Nagle's algorithm (setNoDelay)                              │
│     Default: buffers small packets to send together (good for   │
│     throughput, bad for latency).                                │
│     Interactive apps: socket.setNoDelay(true)                   │
│                                                                  │
│  4. TCP_QUICKACK                                                │
│     Acknowledge data immediately (default on most Linux).       │
│                                                                  │
│  5. Window scaling                                              │
│     Large receive windows for high-bandwidth connections.       │
│     Linux: enabled by default. Nothing to configure.            │
│                                                                  │
│  6. Avoid TIME_WAIT accumulation                                │
│     Many short connections = thousands of TIME_WAIT sockets.    │
│     Fix: connection pooling, keep-alive, SO_REUSEADDR.         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Keep-Alive Timeout Mismatch

```
ALB idle timeout: 60 seconds
Node.js keepAliveTimeout: 5 seconds (default prior to Node 19!)

What happens:
  1. Browser → ALB → Node.js (TCP established)
  2. 5 seconds silence → Node.js closes the socket
  3. 10 seconds later → ALB sends a request on the "alive" connection
  4. Node.js: ECONNRESET → ALB: 502 Bad Gateway
  
Fix: server.keepAliveTimeout = 65000 (always > ALB timeout)
```

### ❌ Not Handling ECONNRESET

```javascript
// ❌ Unhandled ECONNRESET crashes Node.js
process.on('uncaughtException', (err) => {
  console.error('Uncaught:', err); // ECONNRESET
  process.exit(1);
});

// ✅ Handle connection errors gracefully
app.use((err, req, res, next) => {
  if (err.code === 'ECONNRESET') {
    console.warn('Client disconnected');
    return; // Don't send response — client is gone
  }
  next(err);
});
```

---

## Practice Exercises

### Exercise 1: Observe the Handshake
Use `tcpdump` or Wireshark to capture a `curl http://localhost:3000` request. Identify the SYN, SYN-ACK, ACK packets.

### Exercise 2: Connection State Analysis
Run your Express server, make 20 requests, then run `netstat`. Count connections in each state. What state do closed connections enter?

### Exercise 3: Keep-Alive vs Close
Compare two scenarios with `curl`:
1. `curl -H "Connection: keep-alive"` (10 requests sequentially)
2. `curl -H "Connection: close"` (10 requests sequentially)
Count TCP handshakes in tcpdump output.

---

## Interview Q&A

**Q1: Why does TCP use a 3-way handshake?**
> Both sides need to exchange and acknowledge initial sequence numbers. SYN establishes client→server direction, SYN-ACK establishes server→client and acknowledges client's SYN, ACK confirms server's SYN. Two-way wouldn't confirm the server's sequence number was received.

**Q2: What is TCP's congestion control and how does it affect your app?**
> TCP starts with a small window (~14KB) and doubles it each RTT until packet loss occurs (slow start). On loss, the window halves. For new connections, large responses are throttled initially. Connection reuse avoids slow start. This is why keep-alive and connection pooling matter.

**Q3: What does TIME_WAIT mean and why does it exist?**
> After closing a TCP connection, the socket stays in TIME_WAIT for ~2 minutes to handle late-arriving packets and prevent old packets from being confused with new connections using the same ports. High TIME_WAIT counts indicate many short-lived connections — fix with connection pooling.

**Q4: What causes ECONNRESET in Node.js?**
> The remote side sent a TCP RST packet, forcefully closing the connection. Causes: client navigated away, load balancer closed idle connection, firewall killed the connection, server process crashed. Handle it gracefully — don't crash your process.

**Q5: How does TCP keep-alive work and why is it important for database connections?**
> TCP keep-alive sends probe packets on idle connections to detect dead peers. Default Linux timer is 2 hours — too long for NAT gateways (AWS: 350s timeout). Set keep-alive interval shorter than NAT timeout to prevent silent connection drops.
