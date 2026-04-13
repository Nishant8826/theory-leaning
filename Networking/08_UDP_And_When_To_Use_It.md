# UDP & When To Use It

> 📌 **File:** 08_UDP_And_When_To_Use_It.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

UDP (User Datagram Protocol) is TCP's lightweight sibling — it sends data without connection setup, without delivery guarantees, and without ordering. It's faster but unreliable. You use it more than you think: every DNS lookup, WebRTC video call, and HTTP/3 (QUIC) request uses UDP.

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────┐
│  Protocol │ TCP or UDP │ Why                                     │
├───────────┼────────────┼─────────────────────────────────────────┤
│  HTTP/1.1 │ TCP        │ Reliability needed for web pages        │
│  HTTP/2   │ TCP        │ Same, with multiplexing                 │
│  HTTP/3   │ UDP (QUIC) │ Avoids TCP head-of-line blocking       │
│  DNS      │ UDP        │ Small query/response, fast              │
│  DNS (big)│ TCP        │ Response > 512 bytes, zone transfer    │
│  MongoDB  │ TCP        │ Must not lose database operations       │
│  Redis    │ TCP        │ Must not lose cache commands            │
│  PostgreSQL│ TCP       │ Must not lose queries                   │
│  WebSocket│ TCP        │ Reliable message delivery               │
│  WebRTC   │ UDP        │ Real-time video/audio (latency > loss) │
│  Socket.IO│ TCP        │ HTTP upgrade, then WebSocket over TCP  │
│  IoT/MQTT │ TCP        │ Reliable for sensor data                │
│  Gaming   │ UDP        │ Real-time position updates              │
│  Logs     │ UDP        │ Log shipping (syslog, StatsD)           │
│  Video    │ UDP (RTP)  │ Streaming — dropped frame < frozen video│
└───────────┴────────────┴─────────────────────────────────────────┘
```

### TCP vs UDP — Side by Side

```
┌────────────────────────────────────────────────────────────────────┐
│                   │ TCP                   │ UDP                    │
├───────────────────┼───────────────────────┼────────────────────────┤
│  Connection       │ ✅ 3-way handshake    │ ❌ No connection       │
│  Delivery         │ ✅ Guaranteed         │ ❌ Fire and forget     │
│  Ordering         │ ✅ In-order           │ ❌ Any order           │
│  Duplicates       │ ✅ Prevented          │ ❌ Possible            │
│  Flow control     │ ✅ Window-based       │ ❌ None                │
│  Congestion ctrl  │ ✅ Adapts to network  │ ❌ Can flood network   │
│  Speed            │ ⚠️ Slower (overhead)  │ ✅ Faster              │
│  Header size      │ 20-60 bytes           │ 8 bytes                │
│  Latency          │ 1.5 RTT connection    │ 0 RTT — just send     │
│  Use case         │ APIs, DBs, web page   │ DNS, video, gaming     │
├───────────────────┴───────────────────────┴────────────────────────┤
│  Decision rule:                                                    │
│  Can you tolerate lost data? → UDP                                │
│  Must every byte arrive? → TCP                                    │
│  Real-time > reliability? → UDP                                   │
│  Reliability > real-time? → TCP                                   │
└────────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Postal Service vs. The Paper Airplane)
Think of the difference between TCP and UDP as two ways to send a message:
- **TCP (Certified Mail):** You send a tracked package. The post office makes you sign for it (handshake), guarantees it will arrive in perfect sequence, and calls you to confirm delivery. It's incredibly secure but much slower.
- **UDP (Throwing a Paper Airplane):** You fold your message and chuck it out the window. You don't know if it hit the person, you don't know if the wind blew it away, and you honestly don't care. But it's *instantaneous*. This is exactly why live video calls use UDP. It's better for a single frame of video to drop completely than for the video to freeze while waiting for an old frame to arrive 5 seconds late.

---

## How does it actually work?

### UDP Datagram Format

```
TCP segment:
┌──────┬──────┬─────┬─────┬──────┬────────┬──────────────┐
│SrcPrt│DstPrt│ Seq │ Ack │Flags │Window  │Options+Data  │
│2 byte│2 byte│4 B  │4 B  │6 bits│2 byte  │ variable     │
└──────┴──────┴─────┴─────┴──────┴────────┴──────────────┘
Header: 20-60 bytes of overhead

UDP datagram:
┌──────┬──────┬──────┬──────┬──────────────┐
│SrcPrt│DstPrt│Length│Check │    Data       │
│2 byte│2 byte│2 B  │2 B   │  variable     │
└──────┴──────┴──────┴──────┴──────────────┘
Header: 8 bytes only (minimal overhead)
```

### DNS Over UDP (What You Use Every Day)

```
Your app: mongoose.connect('mongodb+srv://cluster0.xxxxx.mongodb.net/...')

Step 1: Node.js needs IP of cluster0.xxxxx.mongodb.net
Step 2: DNS resolver sends UDP datagram to DNS server port 53:
  
  ┌──────────────────────────────────────────────┐
  │ UDP src:52000 dst:53                          │
  │ DNS Query: cluster0.xxxxx.mongodb.net A?      │
  └──────────────────────────────────────────────┘
  
Step 3: DNS server responds via UDP:
  
  ┌──────────────────────────────────────────────┐
  │ UDP src:53 dst:52000                          │
  │ DNS Response: 54.23.189.12, 54.23.189.13     │
  └──────────────────────────────────────────────┘

Why UDP for DNS?
  - Small query + small response (< 512 bytes typically)
  - No connection needed (save 1.5 RTT)
  - Stateless — server handles millions of queries
  - If lost → client just retries after timeout
```

---

## Node.js Implementation

```javascript
const dgram = require('dgram');

// ──── UDP Server ────
const server = dgram.createSocket('udp4');

server.on('message', (msg, rinfo) => {
  console.log(`UDP message from ${rinfo.address}:${rinfo.port}: ${msg}`);
  
  // Respond (fire and forget)
  const response = Buffer.from(`Echo: ${msg}`);
  server.send(response, rinfo.port, rinfo.address, (err) => {
    if (err) console.error('Send error:', err);
    // No guarantee client receives this!
  });
});

server.on('listening', () => {
  const addr = server.address();
  console.log(`UDP server listening on ${addr.address}:${addr.port}`);
});

server.bind(41234);

// ──── UDP Client ────
const client = dgram.createSocket('udp4');
const message = Buffer.from('Hello UDP!');

client.send(message, 41234, 'localhost', (err) => {
  if (err) client.close();
  console.log('UDP message sent (no delivery guarantee!)');
});

client.on('message', (msg) => {
  console.log(`Received: ${msg}`);
  client.close();
});

// UDP timeout (since UDP doesn't have built-in connection timeout)
setTimeout(() => {
  console.log('No response received (UDP — expected sometimes)');
  client.close();
}, 3000);

// ──── Real-World: StatsD Metrics (UDP) ────
function sendMetric(metricName, value, type = 'c') {
  const client = dgram.createSocket('udp4');
  const message = Buffer.from(`${metricName}:${value}|${type}`);
  
  client.send(message, 8125, 'statsd-server', (err) => {
    client.close();
    // Don't care if it was received — metrics are best-effort
    // Losing a few metrics is fine; slowing down your app is not
  });
}

// Usage:
sendMetric('api.requests.total', 1, 'c');      // Counter
sendMetric('api.response_time', 45, 'ms');     // Timer
sendMetric('api.active_connections', 150, 'g'); // Gauge
```

---

## QUIC / HTTP/3 — The Future (UDP-Based)

```
┌──────────────────────────────────────────────────────────────────┐
│  QUIC (Quick UDP Internet Connections)                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  HTTP/2 over TCP:                                                │
│  ┌──────────────────────────────┐                               │
│  │ HTTP/2 (multiplexed streams) │                               │
│  │ TLS 1.3 (encryption)        │                               │
│  │ TCP (reliable, ordered)      │ ← If 1 packet lost,          │
│  └──────────────────────────────┘   ALL streams blocked!        │
│                                                                  │
│  HTTP/3 over QUIC:                                              │
│  ┌──────────────────────────────┐                               │
│  │ HTTP/3 (multiplexed streams) │                               │
│  │ QUIC (reliability + crypto) │ ← Per-stream loss handling    │
│  │ UDP (unreliable transport)   │   Stream A lost packet?      │
│  └──────────────────────────────┘   Only A is blocked, B/C     │
│                                      continue fine!              │
│                                                                  │
│  Connection setup:                                               │
│  TCP + TLS 1.3: 2 RTT (SYN, TLS)                              │
│  QUIC: 1 RTT first time, 0 RTT reconnect                      │
│                                                                  │
│  CloudFront supports HTTP/3 — enable it!                        │
│  Node.js QUIC: experimental (node --experimental-quic)         │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (Fixing the Traffic Jam)
This diagram perfectly highlights "Head-of-Line Blocking."
- Under **HTTP/2 (TCP)**, imagine all your website's data (HTML, JS, Images) is driving in a single lane on the highway. If the front car (a packet of data) crashes on its way, *every single car behind it* has to instantly stop and wait for it to be repaired and retransmitted. 
- Under **HTTP/3 (QUIC/UDP)**, each stream of data gets its own dedicated lane! If an image packet crashes, the HTML and JS packets driving right next to it in other lanes keep cruising unbothered. By building reliability directly on top of "unreliable" UDP, QUIC creates the fastest, most flexible transport ever designed.

---

## When to Use UDP in Your Stack

```
✅ Use UDP for:
  - Metrics/monitoring (StatsD, Prometheus UDP)
  - Logging (syslog over UDP)  
  - Real-time video/audio (WebRTC)
  - Game state updates
  - DNS lookups (handled by OS/libraries)
  - Service discovery (mDNS)

❌ Don't use UDP for:
  - API calls (use HTTP/TCP)
  - Database queries (use TCP)
  - File transfers (use TCP/HTTP)
  - WebSocket messages (TCP-based)
  - Anything where lost data = broken functionality
```

---

## Common Mistakes

### ❌ Using UDP When You Need Reliability

```javascript
// ❌ Sending critical order data over UDP
udpClient.send(JSON.stringify(orderData), port, host);
// Order might be lost forever!

// ✅ Use TCP (HTTP) for critical data
await fetch('/api/orders', { method: 'POST', body: JSON.stringify(orderData) });
```

### ❌ UDP Packets Too Large

```
UDP max datagram: 65,535 bytes (theoretical)
Practical limit: ~1,400 bytes (MTU - headers)
Exceeding MTU → IP fragmentation → increased loss probability

Rule: Keep UDP messages under 1,400 bytes
For larger data: use TCP or implement your own chunking + reassembly
```

---

## Interview Q&A

**Q1: When would you choose UDP over TCP?**
> When low latency matters more than reliability: DNS lookups, real-time video/audio (WebRTC), gaming position updates, metrics shipping (StatsD), and QUIC/HTTP/3. The key question: is lost data acceptable?

**Q2: How does HTTP/3 use UDP?**
> HTTP/3 uses QUIC — a protocol built on UDP that adds reliability per-stream, encryption (TLS 1.3 built-in), and congestion control. Unlike TCP where one lost packet blocks all streams, QUIC only blocks the affected stream. Connection setup is 1 RTT (0 RTT on reconnect).

**Q3: Why does DNS use UDP instead of TCP?**
> DNS queries are small (< 512 bytes), stateless, and need to be fast. UDP avoids TCP's 3-way handshake (saves 1.5 RTT). If a response is lost, the client retries. For large responses (> 512 bytes) or zone transfers, DNS falls back to TCP.

**Q4: What is UDP's maximum packet size?**
> Theoretical: 65,535 bytes. Practical: ~1,400 bytes (Ethernet MTU 1500 - IP header 20 - UDP header 8). Exceeding MTU causes IP fragmentation, which increases loss probability. Best practice: keep UDP datagrams under 1,400 bytes.

**Q5: Can you build a reliable protocol on top of UDP?**
> Yes — that's exactly what QUIC does. You implement sequence numbers, acknowledgments, retransmission, and flow control in your application layer. This gives you TCP's reliability with UDP's flexibility (custom congestion control, no head-of-line blocking). But it's complex — use existing implementations (QUIC libraries).


Prev : [07 TCP Deep Dive](./07_TCP_Deep_Dive.md) | Index: [0 Index](./0_Index.md) | Next : [09 TLS SSL Handshake](./09_TLS_SSL_Handshake.md)
