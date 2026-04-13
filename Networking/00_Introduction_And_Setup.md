# Introduction & Setup

> 📌 **File:** 00_Introduction_And_Setup.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

This tutorial teaches you **how the internet actually works** beneath your code. You already know how to build APIs, deploy to AWS, and query databases — but when your API is slow, your WebSocket drops, or your CDN isn't caching, you need to understand what's happening at the **network level**.

This isn't a textbook networking course. Every concept is mapped to **your stack** — Node.js, React, MongoDB, Redis, AWS.

---

## What You Already Know (But Don't Realize is Networking)

```
┌─────────────────────────────────────────────────────────────────┐
│  What you DO in code          │  What's ACTUALLY happening      │
├───────────────────────────────┼─────────────────────────────────┤
│  fetch('/api/products')       │  DNS → TCP → TLS → HTTP → TCP  │
│  mongoose.connect(uri)        │  DNS → TCP → TLS → MongoDB Wire│
│  redis.get('cache:key')       │  TCP connection to Redis port   │
│  io.connect('wss://...')      │  HTTP Upgrade → WebSocket → TCP │
│  aws s3 cp file s3://bucket   │  DNS → HTTPS → S3 API → Storage│
│  next build && next start     │  Nginx → Node.js → listen(3000)│
│  curl https://api.example.com │  DNS → TCP → TLS → HTTP GET    │
├───────────────────────────────┴─────────────────────────────────┤
│  Every line of code you write that touches the network          │
│  goes through: DNS → IP → TCP/UDP → TLS → Application Protocol │
│  Understanding this stack = debugging superpowers.               │
└─────────────────────────────────────────────────────────────────┘
```

---

## What You'll Learn

```
Phase 1 (Files 00-03): How the internet works — models, protocols
Phase 2 (Files 04-09): Core protocols — IP, DNS, HTTP, TCP, UDP, TLS
Phase 3 (Files 10-14): Infrastructure — routing, load balancing, firewalls, CDN
Phase 4 (Files 15-19): Modern networking — WebSockets, API gateways, microservices, K8s
Phase 5 (Files 20-25): Production — debugging, performance, scaling, security, deployment
```

---

## Required Tools Setup

### 1. Node.js (You Already Have This)

```bash
node -v   # Should be 18+ or 20+
npm -v
```

### 2. Networking Tools

#### Windows (PowerShell)

```powershell
# Most tools already available:
ping google.com
tracert google.com
nslookup google.com
ipconfig /all
netstat -an
curl https://httpbin.org/ip

# Install additional tools:
winget install WiresharkFoundation.Wireshark
winget install Postman.Postman
```

#### macOS

```bash
brew install curl wget nmap mtr
# Wireshark: https://www.wireshark.org/download.html
```

#### Linux (Ubuntu)

```bash
sudo apt update
sudo apt install -y curl wget net-tools dnsutils traceroute \
  nmap tcpdump mtr-tiny wireshark
```

### 3. Postman / Insomnia

Download from: https://www.postman.com/downloads/

### 4. Wireshark (Packet Capture GUI)

Download from: https://www.wireshark.org/

```
Wireshark lets you SEE actual packets flowing through your network.
It's like a debugger, but for network traffic instead of code.

You'll use it to:
- See the TCP 3-way handshake
- Watch TLS negotiation
- Debug slow HTTP requests
- Understand WebSocket upgrade
```

---

## Create a Test Project

### Express API Server

```bash
mkdir networking-lab
cd networking-lab
npm init -y
npm install express socket.io cors redis mongoose dotenv
```

### `server.js` — Basic API + WebSocket

```javascript
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: '*' } });

app.use(cors());
app.use(express.json());

// ──── REST API Endpoints ────
app.get('/api/health', (req, res) => {
  res.json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    headers: req.headers,           // See what the browser actually sends
    ip: req.ip,                     // Client IP (after proxy)
    protocol: req.protocol,         // http or https
    hostname: req.hostname,         // Host header
    connection: req.get('Connection') // keep-alive or close
  });
});

app.get('/api/slow', (req, res) => {
  const delay = parseInt(req.query.delay) || 2000;
  setTimeout(() => {
    res.json({ message: 'This was intentionally slow', delay });
  }, delay);
});

app.get('/api/echo', (req, res) => {
  res.json({
    method: req.method,
    url: req.url,
    headers: req.headers,
    query: req.query,
    ip: req.ip,
    ips: req.ips,             // X-Forwarded-For chain
    remoteAddress: req.socket.remoteAddress,
    remotePort: req.socket.remotePort,
    localAddress: req.socket.localAddress,
    localPort: req.socket.localPort
  });
});

// ──── WebSocket ────
io.on('connection', (socket) => {
  console.log(`[WS] Client connected: ${socket.id} from ${socket.handshake.address}`);
  
  socket.emit('welcome', {
    message: 'Connected to WebSocket server',
    transport: socket.conn.transport.name  // "polling" or "websocket"
  });

  socket.on('ping', (data) => {
    const received = Date.now();
    socket.emit('pong', { 
      sent: data.timestamp,
      received,
      latency: received - data.timestamp
    });
  });

  socket.on('disconnect', (reason) => {
    console.log(`[WS] Client disconnected: ${socket.id}, reason: ${reason}`);
  });
});

// ──── Start Server ────
const PORT = process.env.PORT || 3000;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`
┌─────────────────────────────────────────┐
│  🚀 Server running on port ${PORT}         │
│                                         │
│  REST:  http://localhost:${PORT}/api/health│
│  WS:    ws://localhost:${PORT}             │
│                                         │
│  Try these:                             │
│  curl http://localhost:${PORT}/api/health  │
│  curl http://localhost:${PORT}/api/echo    │
│  curl http://localhost:${PORT}/api/slow    │
└─────────────────────────────────────────┘
  `);
});
```

### `client.html` — WebSocket Test Client

```html
<!DOCTYPE html>
<html>
<head>
  <title>Networking Lab - WebSocket Client</title>
  <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
</head>
<body>
  <h1>WebSocket Networking Lab</h1>
  <div id="status">Connecting...</div>
  <button onclick="measureLatency()">Measure Latency</button>
  <pre id="log"></pre>

  <script>
    const socket = io('http://localhost:3000');
    const log = document.getElementById('log');
    const status = document.getElementById('status');

    socket.on('connect', () => {
      status.textContent = `Connected (transport: ${socket.io.engine.transport.name})`;
      log.textContent += `[${new Date().toISOString()}] Connected: ${socket.id}\n`;
    });

    socket.on('welcome', (data) => {
      log.textContent += `[Server] ${JSON.stringify(data)}\n`;
    });

    socket.on('pong', (data) => {
      log.textContent += `[Latency] ${data.latency}ms (round-trip)\n`;
    });

    socket.on('disconnect', (reason) => {
      status.textContent = `Disconnected: ${reason}`;
      log.textContent += `[${new Date().toISOString()}] Disconnected: ${reason}\n`;
    });

    function measureLatency() {
      socket.emit('ping', { timestamp: Date.now() });
    }
  </script>
</body>
</html>
```

---

## Test Your Setup

### Test REST API

```bash
# Basic request
curl http://localhost:3000/api/health

# See full HTTP headers
curl -v http://localhost:3000/api/health

# With timing information
curl -w "\n\nDNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTLS: %{time_appconnect}s\nFirst Byte: %{time_starttransfer}s\nTotal: %{time_total}s\n" \
  -o /dev/null -s http://localhost:3000/api/health

# Test slow endpoint
curl -w "Total: %{time_total}s\n" http://localhost:3000/api/slow?delay=3000
```

### Test DNS

```bash
# Look up any domain's IP address
nslookup google.com
dig google.com          # More detailed (Linux/Mac)

# Look up your own server
nslookup localhost
```

### Test Connectivity

```bash
# Ping (ICMP echo — basic connectivity test)
ping -c 4 google.com

# Traceroute (show every router between you and destination)
traceroute google.com      # Linux/Mac
tracert google.com         # Windows

# Show your network configuration
ifconfig                   # Linux/Mac
ipconfig /all              # Windows
```

### Test TCP Connections

```bash
# Show active connections
netstat -an | grep 3000    # See connections to your server
ss -tlnp                   # Linux: show listening ports

# Test if a port is open
nc -zv google.com 443      # Test if HTTPS port is open
```

---

## Key Commands Reference

```
┌──────────────────────────────────────────────────────────────────┐
│  Command          │ What it does                                 │
├───────────────────┼──────────────────────────────────────────────┤
│  curl             │ Make HTTP requests (like Postman but CLI)    │
│  ping             │ Test basic connectivity (ICMP)               │
│  traceroute/rt    │ Show path packets take to destination        │
│  dig / nslookup   │ DNS lookup (domain → IP)                    │
│  netstat / ss     │ Show active network connections              │
│  tcpdump          │ Capture packets on the wire (CLI)            │
│  Wireshark        │ Capture packets on the wire (GUI)            │
│  nmap             │ Port scanning (find open services)           │
│  mtr              │ Combines ping + traceroute (live)            │
│  openssl s_client │ Test TLS/SSL connections                     │
│  curl -v          │ Verbose HTTP — see headers, TLS, etc.       │
│  curl -w          │ Custom timing output (DNS, connect, TTFB)   │
└───────────────────┴──────────────────────────────────────────────┘
```

---

## Verification Checklist

```
✅ Node.js server running on port 3000
✅ curl http://localhost:3000/api/health returns JSON
✅ curl -v shows HTTP headers
✅ ping google.com works
✅ nslookup google.com returns an IP
✅ netstat shows port 3000 listening
✅ WebSocket client connects (open client.html)
✅ Wireshark installed (optional but recommended)
✅ Postman installed and can hit your API
```

---

## What's Next?

In the next file, we'll trace **exactly what happens** when you type `https://yourapp.com` in a browser — every DNS lookup, TCP connection, TLS handshake, HTTP request, and response. You'll see how all the tools you set up here reveal the invisible network layer beneath your code.


Prev : N/A | Index: [0 Index](./0_Index.md) | Next : [01 How The Internet Actually Works](./01_How_The_Internet_Actually_Works.md)
