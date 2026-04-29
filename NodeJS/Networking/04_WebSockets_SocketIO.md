# 📌 04 — WebSockets and Socket.IO: Real-Time Bidirectional Streams

## 🧠 Concept Explanation

### Basic → Intermediate
WebSockets (WS) allow for a persistent, full-duplex connection between a client and a server. Unlike HTTP, where the client must initiate every request, WS allows the server to push data to the client at any time.

### Advanced → Expert
At a systems level, WebSockets start as an **HTTP Upgrade request**. 
1. The client sends an HTTP GET with `Upgrade: websocket`.
2. The server responds with `101 Switching Protocols`.
3. The underlying TCP socket is now repurposed for the WebSocket protocol.
4. Data is exchanged in **Frames**, which have a lightweight header (2-14 bytes) compared to heavy HTTP headers.

**Socket.IO** is not a WebSocket library; it is a **Real-Time Engine** built on top of Engine.io. it provides features that raw WS lacks: Auto-reconnect, Heartbeats, Namespaces, and Rooms.

---

## 🏗️ Common Mental Model
"WebSockets are just faster HTTP."
**Correction**: WebSockets are **stateful**. This means the server must maintain an open TCP connection for every active user. This has massive implications for memory and load balancing.

---

## ⚡ Actual Behavior: Sticky Sessions
Since Socket.IO often starts with HTTP Long-Polling before upgrading to WS, the client must hit the **same server instance** for multiple requests to complete the handshake. This requires "Sticky Sessions" at your load balancer level.

---

## 🔬 Internal Mechanics (libuv + Networking)

### The Upgrade Handshake
Node.js's `http` module emits an `'upgrade'` event when it sees the upgrade header. Libraries like `ws` or `socket.io` listen for this event and take over the raw socket handle from Node's internal pool.

### Heartbeats and Zombies
TCP doesn't always know if a connection is dead (e.g. client cable pulled). Socket.IO implements its own **Ping/Pong** mechanism at the application layer to detect and clean up "Zombie" connections.

---

## 📐 ASCII Diagrams

### WebSocket Handshake (The Upgrade)
```text
  CLIENT                                 SERVER
    │                                       │
    │ 1. GET /socket.io HTTP/1.1            │
    │    Upgrade: websocket                 │
    │    Connection: Upgrade                │
    ├──────────────────────────────────────▶│
    │                                       │
    │ 2. HTTP/1.1 101 Switching Protocols   │
    │    Upgrade: websocket                 │
    │    Connection: Upgrade                │
    │◀──────────────────────────────────────┤
    │                                       │
    │ 3. [ BINARY DATA FRAMES ]             │
    │◀─────────────────────────────────────▶│
```

---

## 🔍 Code Example: Scaling with Redis Adapter
```javascript
const express = require('express');
const { Server } = require('socket.io');
const { createAdapter } = require('@socket.io/redis-adapter');
const { createClient } = require('redis');

const app = express();
const server = require('http').createServer(app);
const io = new Server(server);

// Redis is required for multi-node Socket.IO setups
const pubClient = createClient({ url: 'redis://localhost:6379' });
const subClient = pubClient.duplicate();

Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  io.adapter(createAdapter(pubClient, subClient));
  
  io.on('connection', (socket) => {
    console.log(`User connected: ${socket.id}`);
    
    socket.on('chat message', (msg) => {
      // Broadcast to all clients across ALL servers via Redis
      io.emit('chat message', msg);
    });
  });
});

server.listen(3000);
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Max Sockets" OOM
**Problem**: The server crashes with OOM after reaching 50,000 connections, even though each connection is idle.
**Reason**: Every open socket in Node.js consumes memory (approx 20KB-50KB for internal buffers and V8 objects). 50k * 40KB = 2GB. 
**Fix**: Increase the server memory or use `ws` (which is lighter than Socket.IO) for high-concurrency needs.

### Scenario: Reconnection Storm
**Problem**: After a server restart, the CPU spikes to 100% and the server crashes again.
**Reason**: All 50,000 clients attempt to reconnect at the exact same millisecond. The SSL handshake and auth logic for 50k users simultaneously is too much for the CPU.
**Fix**: Implement **Exponential Backoff** with **Jitter** in your client-side reconnection logic.

---

## 🧪 Real-time Production Q&A

**Q: "Should I use raw `ws` or `Socket.IO`?"**
**A**: Use **raw `ws`** if you need maximum performance and are building a simple protocol. Use **Socket.IO** if you need rooms, namespaces, and reliable reconnection out of the box.

---

## 🧪 Debugging Toolchain
- **Chrome DevTools -> Network -> WS**: Inspect frames in real-time.
- **`socket.io-client` with `DEBUG=socket.io-client:*`**: See internal heartbeat and reconnection logs.

---

## 🏢 Industry Best Practices
- **Use a Redis/NATS Adapter**: To sync messages across multiple server instances.
- **Auth in the Handshake**: Don't allow a connection to be fully established before checking the JWT.

---

## 💼 Interview Questions
**Q: How do you handle load balancing for WebSockets?**
**A**: Use a load balancer that supports **Sticky Sessions** (session affinity) so the initial handshake succeeds. Alternatively, use raw WebSockets (without polling) which don't require stickiness if the auth is handled in the connection event.

---

## 🧩 Practice Problems
1. Build a "Stock Ticker" that pushes a random price every 100ms to all connected clients. Use `io.to(room)` to segment users by stock symbol.
2. Monitor the `heartbeat` interval. What happens to the server memory if you set the ping interval to 1 second for 10,000 clients?

---

**Prev:** [03_Middleware_Deep_Dive.md](./03_Middleware_Deep_Dive.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [05_TCP_UDP_Basics.md](./05_TCP_UDP_Basics.md)
