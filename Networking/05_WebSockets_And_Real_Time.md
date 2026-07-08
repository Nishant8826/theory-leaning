# WebSockets & Real-Time

> 📌 **File:** 05_WebSockets_And_Real_Time.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

WebSocket is a full-duplex communication protocol over a single TCP connection. Unlike HTTP (request → response → done), WebSocket keeps the connection open for bidirectional data flow. Socket.IO is a library that wraps WebSocket with fallbacks, reconnection, rooms, and broadcasting.

---

## Map it to MY STACK (CRITICAL)

```
HTTP (REST API):
  Client ──Request──► Server
  Client ◄──Response── Server
  Connection closed. Client must poll for updates.

WebSocket:
  Client ──Upgrade──► Server (HTTP → WebSocket)
  Client ◄════════════► Server (bidirectional, persistent)
  Both sides can send messages anytime.

Your use cases:
  ✅ Real-time chat
  ✅ Live notifications
  ✅ Collaborative editing
  ✅ Live dashboards (stock prices, analytics)
  ✅ Multiplayer gaming
  ✅ Presence indicators (user online/offline)
  ❌ CRUD operations (use REST)
  ❌ File uploads (use HTTP multipart)
  ❌ One-time data fetch (use REST)
```

---

## How does it actually work?

### The WebSocket Handshake

```
HTTP Upgrade Request:
GET /socket.io/?EIO=4&transport=websocket HTTP/1.1
Host: api.myapp.com
Upgrade: websocket                    ← "I want to switch to WebSocket"
Sec-WebSocket-Key: dGhlIHNhbXBsZQ==  ← Random key for verification
Origin: https://myapp.com

HTTP 101 Response:
HTTP/1.1 101 Switching Protocols      ← "OK, switching!"
Upgrade: websocket
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=  ← Calculated from key

═══ Now it's a WebSocket connection ═══
No more HTTP. Just raw frames flowing both ways over TCP.
```

### WebSocket vs HTTP vs SSE

```
┌─────────────────┬──────────────┬──────────────┬─────────────────┐
│                 │ HTTP (REST)  │ SSE          │ WebSocket       │
├─────────────────┼──────────────┼──────────────┼─────────────────┤
│ Direction       │ Client→Server│ Server→Client│ Bidirectional  │
│ Connection      │ Per request  │ Persistent   │ Persistent      │
│ Protocol        │ HTTP         │ HTTP         │ WS (over TCP)  │
│ Reconnection    │ N/A          │ Built-in     │ Manual/Socket.IO│
│ Binary data     │ ✅           │ ❌ Text only  │ ✅              │
│ Through CDN     │ ✅ Easy      │ ⚠️ Possible  │ ❌ Tricky       │
│ Proxy support   │ ✅ Universal │ ✅ Good      │ ⚠️ Needs config │
│ Scaling         │ ✅ Stateless │ ⚠️ Stateful  │ ❌ Stateful     │
│ Use case        │ CRUD, fetch  │ Notifications│ Chat, gaming    │
└─────────────────┴──────────────┴──────────────┴─────────────────┘
```

#### Diagram Explanation (The Telephone vs The Walkie-Talkie)
- **HTTP (Sending a Letter):** You send a request, the server writes back, and the transaction is 100% over. If you want to know if they replied again, you have to write *another* letter asking.
- **SSE (The Radio Broadcast):** You tune in to the server's station. The server can continuously broadcast live updates (like live sports scores) to you forever, but you *cannot* talk back on that channel. 
- **WebSocket (The Phone Call):** You call the server, they pick up, and you **stay on the line**. Both of you can talk instantly at any exact moment without needing to redial!

---

## Socket.IO Implementation (Production)

### Server

```javascript
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { createAdapter } = require('@socket.io/redis-adapter');
const { createClient } = require('redis');
const jwt = require('jsonwebtoken');

const app = express();
const server = http.createServer(app);

const io = new Server(server, {
  cors: {
    origin: ['https://myapp.com'],
    credentials: true
  },
  pingInterval: 25000,     // Send ping every 25s (keep NAT alive)
  pingTimeout: 20000,      // Wait 20s for pong before disconnect
  maxHttpBufferSize: 1e6,  // 1MB max message size
  transports: ['websocket', 'polling']
});

const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();
Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  io.adapter(createAdapter(pubClient, subClient));
});

io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (!token) return next(new Error('Authentication required'));
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    socket.userId = decoded.id;
    next();
  } catch (err) {
    next(new Error('Invalid token'));
  }
});

io.on('connection', (socket) => {
  socket.join(`user:${socket.userId}`);
  
  socket.on('join:room', (roomId) => {
    socket.join(`room:${roomId}`);
    socket.to(`room:${roomId}`).emit('user:joined', { userId: socket.userId });
  });
  
  socket.on('chat:message', async (data) => {
    const message = {
      id: crypto.randomUUID(),
      userId: socket.userId,
      text: data.text,
      roomId: data.roomId,
      timestamp: Date.now()
    };
    io.to(`room:${data.roomId}`).emit('chat:message', message);
  });
});
```

### React Client

```javascript
import { io } from 'socket.io-client';
import { useEffect, useState, useRef } from 'react';

function ChatRoom({ roomId, authToken }) {
  const socketRef = useRef(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const socket = io('https://api.myapp.com', {
      auth: { token: authToken },
      transports: ['websocket'],
      reconnection: true
    });

    socket.emit('join:room', roomId);
    socket.on('chat:message', (message) => {
      setMessages(prev => [...prev, message]);
    });

    socketRef.current = socket;
    return () => socket.disconnect();
  }, [roomId, authToken]);

  return (
    <div>
      {messages.map(msg => <div key={msg.id}>{msg.text}</div>)}
    </div>
  );
}
```

---

## Scaling WebSockets

```
Problem: WebSocket connections are STATEFUL.
User A is connected to Server 1, User B is connected to Server 2.
Server 1 has no idea User B exists.

Solution: Redis Pub/Sub Adapter (Megaphone Analogy)
When User A sends a message to User B:
1. Server 1 publishes a message to Redis.
2. Server 2 receives this message via Redis.
3. Server 2 delivers the message directly to User B.
```

---

## Why WebSocket Connections Drop

```
┌──────────────────────────────────────────────────────────────────┐
│  Cause                          │ Fix                            │
├─────────────────────────────────┼────────────────────────────────┤
│  ALB idle timeout (60s)         │ Socket.IO ping interval < 60s  │
│  NAT Gateway timeout (350s)    │ TCP keep-alive < 350s          │
│  Nginx proxy_read_timeout      │ Set to 86400s for WS           │
│  Client goes to sleep (mobile) │ Reconnection logic in client   │
└─────────────────────────────────┴────────────────────────────────┘
```

---

## Practice Exercises

### Exercise 1: Real-Time Notifications
Build a notification system: REST API creates an order → WebSocket pushes notification to the specific user's browser tab.

### Exercise 2: Typing Indicator
Add typing indicators to a chat room. Debounce typing events (don't spam on every keystroke). Show "User is typing..." for 3 seconds after last keystroke.

### Exercise 3: Connection Monitoring
Display WebSocket connection status, transport type, and latency in your React app. Add a manual reconnect button.

---

## Interview Q&A

**Q1: How does the WebSocket protocol differ from HTTP?**
> HTTP is request-response, half-duplex, and connectionless (per request). WebSocket starts with an HTTP upgrade handshake, then switches to a persistent, full-duplex, binary-framed protocol. Server can push data without client requesting it. Much lower overhead per message (2-6 bytes vs ~800 bytes).

**Q2: How do you scale WebSocket connections across multiple servers?**
> Use a pub/sub broker (Redis) as a message bus. Socket.IO's Redis adapter publishes events to Redis; all servers subscribe and deliver to their connected clients. ALB sticky sessions ensure reconnections hit the same server. Each Node.js instance handles ~10K-50K connections.

**Q3: What causes WebSocket disconnections and how do you handle them?**
> Causes: NAT/LB idle timeouts, network switches (WiFi→cellular), server restarts, client sleep mode. Solutions: application-level heartbeats (Socket.IO ping every 25s), auto-reconnection with exponential backoff, connection state recovery, and buffering messages during disconnection.

**Q4: When should you use SSE instead of WebSocket?**
> SSE (Server-Sent Events) for server→client only updates: live notifications, stock tickers, log streaming. SSE works over regular HTTP (easy through CDNs/proxies), auto-reconnects, and is simpler than WebSocket. Use WebSocket only when you need bidirectional communication (chat, gaming).

**Q5: How do you handle WebSocket authentication?**
> Pass JWT token in the `auth` object during Socket.IO handshake. Verify in server-side middleware before allowing connection. Don't pass tokens in query strings (logged in URLs). Implement token refresh: if token expires, disconnect → refresh token → reconnect with new token.

---

Prev : [04 DNS Deep Dive](./04_DNS_Deep_Dive.md) | Index: [00 Index](./00_Index.md) | Next : [06 OSI Model Vs Real World](./06_OSI_Model_Vs_Real_World.md)
