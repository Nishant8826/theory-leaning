# 📌 Project: Real-Time Socket.io Cluster with Redis Pub/Sub

## 🏗️ Project Overview
Real-time applications (Chat, Collaboration, Dashboards) are notoriously difficult to scale. If User A is connected to Container 1 and User B is connected to Container 2, they cannot "talk" to each other because their WebSocket connections are local to those specific containers. In this project, we implement a **Scalable WebSocket Architecture** using **Redis Pub/Sub** as a message bus and **Nginx** with **Sticky Sessions**.

## 📐 Architecture Diagram

```text
       [ USER A ]              [ USER B ]
           |                       |
     ( WS Conn 1 )           ( WS Conn 2 )
           |                       |
    [ CONTAINER 1 ] <--( Redis )--> [ CONTAINER 2 ]
           |            (Bus)             |
           +--------------+---------------+
                          |
                  [ REDIS CLUSTER ]
```

## 🛠️ Step 1: The Socket.io Backend (Node.js)
We use the `@socket.io/redis-adapter` to sync messages across containers.
```javascript
const io = require("socket.io")(3000);
const { createClient } = require("redis");
const { createAdapter } = require("@socket.io/redis-adapter");

const pubClient = createClient({ url: "redis://cache:6379" });
const subClient = pubClient.duplicate();

Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  // Every message sent to this server is broadcast to Redis
  // Every server listening to Redis then broadcasts to its local clients
  io.adapter(createAdapter(pubClient, subClient));
  
  io.on("connection", (socket) => {
    socket.on("message", (msg) => {
      io.emit("message", msg); // This now works across the whole cluster!
    });
  });
});
```

## ⛓️ Step 2: The Sticky Load Balancer (Nginx)
WebSockets require a persistent handshake. If the Load Balancer switches containers halfway through the handshake, the connection fails.
```nginx
upstream socket_nodes {
    # Stickiness is mandatory for Socket.io handshakes
    ip_hash;
    server api-1:3000;
    server api-2:3000;
}

server {
    listen 80;
    location /socket.io/ {
        proxy_pass http://socket_nodes;
        proxy_http_version 1.1;
        # Enable WebSocket upgrade headers
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}
```

## 🔬 Internal Mechanics (The Broadcast)
1. User A sends "Hello" to Container 1.
2. Container 1's Socket.io adapter publishes "Hello" to the Redis channel `socket.io`.
3. Redis broadcasts "Hello" to Container 2 and Container 3.
4. Container 2 and 3 receive "Hello" from Redis and send it to their own connected users (including User B).
5. **Result**: Global real-time communication with horizontal scalability.

## 💥 Production Failures & Fixes
- **Failure**: The Redis container crashes. Suddenly, users can only chat with people on the same container. The global experience is broken.
  *Fix*: Use a **Redis Sentinel** or **Managed Redis (ElastiCache)** for High Availability.
- **Failure**: Connection timeouts. In high-traffic clusters, the default Nginx `proxy_read_timeout` (60s) might kill idle WebSocket connections.
  *Fix*: Increase the timeout and implement a "Heartbeat" (Ping/Pong) in the application code.

## 💼 Interview Q&A
**Q: Why is 'ip_hash' or Sticky Sessions required for scaling WebSockets behind Nginx?**
**A**: The Socket.io protocol starts with an HTTP Long Polling handshake before "upgrading" to a WebSocket. This handshake involves multiple requests (GET, POST). If the Load Balancer sends the GET to Container 1 and the POST to Container 2, Container 2 will reject the request because it has no record of the initial handshake. `ip_hash` ensures that all requests from a single IP during the handshake phase reach the same container, allowing the connection to be established successfully.

## 🧪 Lab Exercise
1. Launch the cluster with 3 API replicas.
2. Open two different browser tabs. Verify they can chat with each other.
3. Run `docker logs -f` on all API containers. See how only one container receives the initial message, but all containers "emit" the message after receiving it from Redis.

---
Prev: [01_Docker_Node_React_Deployment.md](./01_Docker_Node_React_Deployment.md) | Index: [00_Index.md](../00_Index.md) | Next: [03_Secure_Microservices_with_Vault.md](./03_Secure_Microservices_with_Vault.md)
---
