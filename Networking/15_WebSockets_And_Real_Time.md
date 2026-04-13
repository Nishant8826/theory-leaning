# WebSockets & Real-Time

> 📌 **File:** 15_WebSockets_And_Real_Time.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

WebSocket is a full-duplex communication protocol over a single TCP connection. Unlike HTTP (request → response → done), WebSocket keeps the connection open for bidirectional data flow. Socket.IO is your library that wraps WebSocket with fallbacks, reconnection, rooms, and broadcasting.

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
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZQ==  ← Random key for verification
Sec-WebSocket-Version: 13
Origin: https://myapp.com

HTTP 101 Response:
HTTP/1.1 101 Switching Protocols      ← "OK, switching!"
Upgrade: websocket
Connection: Upgrade
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
│                 │              │ Live feeds   │ Collaboration   │
└─────────────────┴──────────────┴──────────────┴─────────────────┘

For your stack:
  - Real-time updates (one-way): Consider SSE (simpler)
  - Bidirectional real-time: WebSocket / Socket.IO
  - Regular CRUD: REST API (always)
```

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

// ──── Socket.IO with Redis Adapter (for scaling) ────
const io = new Server(server, {
  cors: {
    origin: ['https://myapp.com'],
    credentials: true
  },
  pingInterval: 25000,     // Send ping every 25s (keep NAT alive)
  pingTimeout: 20000,      // Wait 20s for pong before disconnect
  maxHttpBufferSize: 1e6,  // 1MB max message size
  transports: ['websocket', 'polling']  // Prefer WebSocket
});

// Redis adapter — share events across multiple Node.js instances
const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();
Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  io.adapter(createAdapter(pubClient, subClient));
  console.log('Socket.IO Redis adapter connected');
});

// ──── Authentication Middleware ────
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (!token) return next(new Error('Authentication required'));
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    socket.userId = decoded.id;
    socket.userEmail = decoded.email;
    next();
  } catch (err) {
    next(new Error('Invalid token'));
  }
});

// ──── Connection Handler ────
io.on('connection', (socket) => {
  console.log(`Connected: ${socket.userId} (${socket.id})`);
  
  // Join user-specific room (for targeted notifications)
  socket.join(`user:${socket.userId}`);
  
  // ── Chat Room ──
  socket.on('join:room', async (roomId) => {
    socket.join(`room:${roomId}`);
    
    // Notify others in the room
    socket.to(`room:${roomId}`).emit('user:joined', {
      userId: socket.userId,
      timestamp: Date.now()
    });
    
    console.log(`${socket.userId} joined room ${roomId}`);
  });
  
  socket.on('chat:message', async (data) => {
    const message = {
      id: crypto.randomUUID(),
      userId: socket.userId,
      text: data.text,
      roomId: data.roomId,
      timestamp: Date.now()
    };
    
    // Save to MongoDB
    await db.collection('messages').insertOne(message);
    
    // Broadcast to room (including sender)
    io.to(`room:${data.roomId}`).emit('chat:message', message);
  });
  
  // ── Typing Indicator ──
  socket.on('typing:start', (data) => {
    socket.to(`room:${data.roomId}`).emit('typing:start', {
      userId: socket.userId
    });
  });
  
  socket.on('typing:stop', (data) => {
    socket.to(`room:${data.roomId}`).emit('typing:stop', {
      userId: socket.userId
    });
  });
  
  // ── Presence ──
  socket.on('disconnect', async (reason) => {
    console.log(`Disconnected: ${socket.userId}, reason: ${reason}`);
    
    // Update user status in Redis
    await pubClient.hSet(`presence:${socket.userId}`, {
      status: 'offline',
      lastSeen: Date.now().toString()
    });
    
    // Notify contacts
    io.emit('user:offline', { userId: socket.userId });
  });
});

// ──── Send Notification from REST API ────
app.post('/api/orders', async (req, res) => {
  const order = await createOrder(req.body);
  
  // Push real-time notification via WebSocket
  io.to(`user:${order.customerId}`).emit('order:created', {
    orderId: order._id,
    status: 'pending',
    total: order.total
  });
  
  res.status(201).json(order);
});

server.listen(3000);
```

### React Client

```javascript
import { io } from 'socket.io-client';
import { useEffect, useState, useCallback, useRef } from 'react';

// ──── Custom Hook: useSocket ────
function useSocket(url, token) {
  const socketRef = useRef(null);
  const [connected, setConnected] = useState(false);
  const [transport, setTransport] = useState('');

  useEffect(() => {
    const socket = io(url, {
      auth: { token },
      transports: ['websocket'],      // Skip polling, go straight to WS
      reconnection: true,
      reconnectionAttempts: 10,
      reconnectionDelay: 1000,         // Start with 1s
      reconnectionDelayMax: 30000,     // Max 30s between retries
      timeout: 10000                   // Connection timeout
    });

    socket.on('connect', () => {
      setConnected(true);
      setTransport(socket.io.engine.transport.name);
      console.log('WebSocket connected:', socket.id);
    });

    socket.on('disconnect', (reason) => {
      setConnected(false);
      console.log('WebSocket disconnected:', reason);
      // reason = 'io server disconnect' | 'transport close' | 'ping timeout'
    });

    socket.on('connect_error', (err) => {
      console.error('Connection error:', err.message);
      if (err.message === 'Invalid token') {
        // Redirect to login
      }
    });

    socketRef.current = socket;
    return () => socket.disconnect();
  }, [url, token]);

  return { socket: socketRef.current, connected, transport };
}

// ──── Chat Component ────
function ChatRoom({ roomId }) {
  const { socket, connected } = useSocket('https://api.myapp.com', authToken);
  const [messages, setMessages] = useState([]);
  const [typing, setTyping] = useState([]);

  useEffect(() => {
    if (!socket) return;

    socket.emit('join:room', roomId);

    socket.on('chat:message', (message) => {
      setMessages(prev => [...prev, message]);
    });

    socket.on('typing:start', ({ userId }) => {
      setTyping(prev => [...new Set([...prev, userId])]);
    });

    socket.on('typing:stop', ({ userId }) => {
      setTyping(prev => prev.filter(id => id !== userId));
    });

    return () => {
      socket.off('chat:message');
      socket.off('typing:start');
      socket.off('typing:stop');
    };
  }, [socket, roomId]);

  const sendMessage = useCallback((text) => {
    socket.emit('chat:message', { roomId, text });
  }, [socket, roomId]);

  return (
    <div>
      <div>{connected ? '🟢 Connected' : '🔴 Disconnected'}</div>
      {messages.map(msg => <div key={msg.id}>{msg.text}</div>)}
      {typing.length > 0 && <div>{typing.join(', ')} typing...</div>}
    </div>
  );
}
```

---

## Scaling WebSockets

```
Problem: WebSocket connections are STATEFUL.
User A connected to Server 1, User B connected to Server 2.
User A sends message to User B → Server 1 doesn't know about User B!

Solution: Redis Pub/Sub Adapter

Server 1 (has User A)              Server 2 (has User B)
     │                                  │
     └──── Redis Pub/Sub ──────────────┘
     
When User A sends a message:
1. Server 1 publishes to Redis channel
2. Server 2 receives from Redis channel
3. Server 2 delivers to User B

This is what @socket.io/redis-adapter does.
All servers share state through Redis.

┌──────────────────────────────────────────────────────────────────┐
│  Scaling Strategy                                               │
├─────────────────────────────────────────────────────────────────┤
│  1. ALB with sticky sessions (same client → same server)       │
│  2. Redis adapter (share events across all servers)            │
│  3. PM2 cluster mode (multiple Node.js per EC2)                │
│  4. Auto-scaling group (add EC2s under load)                   │
│                                                                 │
│  Connection capacity per Node.js instance:                      │
│  ~10,000-50,000 WebSocket connections                          │
│  Limited by: memory (each conn ~10KB) and file descriptors     │
│                                                                 │
│  3 EC2 instances = ~30,000-150,000 concurrent users            │
└──────────────────────────────────────────────────────────────────┘
```

---

## Why WebSocket Connections Drop

```
┌──────────────────────────────────────────────────────────────────┐
│  Cause                          │ Fix                            │
├─────────────────────────────────┼────────────────────────────────┤
│  ALB idle timeout (60s)         │ Socket.IO ping interval < 60s │
│  NAT Gateway timeout (350s)    │ TCP keep-alive < 350s          │
│  Nginx proxy_read_timeout      │ Set to 86400s for WS           │
│  Client goes to sleep (mobile) │ Reconnection logic in client   │
│  Network switch (WiFi→cellular)│ Socket.IO auto-reconnect       │
│  Server restart/deploy          │ Graceful shutdown + reconnect  │
│  Memory leak on server          │ Monitor + restart workers      │
│  Too many connections           │ Scale horizontally             │
├─────────────────────────────────┴────────────────────────────────┤
│  Socket.IO handles most of these automatically:                  │
│  - Heartbeat (ping/pong every 25s)                              │
│  - Auto-reconnection with exponential backoff                   │
│  - Transport fallback (WebSocket → long-polling)                │
│  - Connection state recovery                                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────────┐
│  WebSocket vs HTTP Polling Performance                          │
├──────────────────┬───────────────────────────────────────────────┤
│  HTTP Polling    │ 1 request/second × 10,000 users              │
│  (every 1 sec)   │ = 10,000 HTTP requests/second                │
│                  │ = 10,000 TCP connections (or keep-alive)      │
│                  │ = massive overhead, 1 second delay            │
│                  │                                               │
│  WebSocket       │ 10,000 persistent connections                 │
│                  │ Messages only when data changes               │
│                  │ = ~100 messages/second (actual updates)       │
│                  │ = 99% less traffic, instant delivery          │
├──────────────────┴───────────────────────────────────────────────┤
│                                                                  │
│  Per-message overhead:                                           │
│  HTTP: ~800 bytes (headers) + payload                           │
│  WebSocket: 2-6 bytes (frame header) + payload                  │
│                                                                  │
│  For 100-byte messages:                                          │
│  HTTP: 900 bytes per message (89% overhead!)                    │
│  WebSocket: 106 bytes per message (6% overhead)                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Using WebSocket for Everything

```javascript
// ❌ Fetching products list via WebSocket
socket.emit('getProducts', {}, (products) => {
  setProducts(products);
});

// ✅ Use REST for CRUD, WebSocket for real-time events
const products = await fetch('/api/products').then(r => r.json());
// WebSocket only for: "Product X price just changed!"
socket.on('product:updated', (update) => {
  setProducts(prev => prev.map(p => p.id === update.id ? update : p));
});
```

### ❌ Not Authenticating WebSocket Connections

```javascript
// ❌ Anyone can connect and listen to all events
io.on('connection', (socket) => {
  socket.join('admin-room'); // No auth check!
});

// ✅ Authenticate in middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    socket.user = jwt.verify(token, secret);
    next();
  } catch { next(new Error('Unauthorized')); }
});
```

### ❌ No Redis Adapter with Multiple Servers

```
Server 1 has users A, B. Server 2 has users C, D.
User A sends message to room "general".
Without Redis adapter: Only B sees it (same server).
With Redis adapter: B, C, D all see it (broadcast via Redis).
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
