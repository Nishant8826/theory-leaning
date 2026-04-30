# 📌 Topic: WebSockets and Real-Time (Scaling Sticky Sessions)

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: WebSockets allow a permanent, two-way connection between a browser and a container. It's like a phone call that never hangs up, allowing for real-time chat or live dashboards.
**Expert**: Scaling WebSockets in Docker is a challenge because they are **Stateful**. Unlike standard HTTP where any container can handle any request, a WebSocket is tied to a *specific* container instance. If you have 5 containers, the client must stay connected to the *same* one for the duration of the session. Staff-level engineering requires implementing **Sticky Sessions** (Session Affinity) at the Load Balancer and using a **Pub/Sub Backbone** (like Redis) to synchronize messages across multiple container replicas.

## 🏗️ Mental Model
- **HTTP**: Sending letters. You can send your letter to any post office branch.
- **WebSockets**: A literal physical wire between your house and a specific office. If you move to another office, the wire is cut.
- **Redis Pub/Sub**: The intercom system. When Container A receives a message, it announces it over the intercom so Container B, C, and D can also tell their connected clients.

## ⚡ Actual Behavior
- **Connection Upgrade**: WebSockets start as an HTTP request with a `Upgrade: websocket` header. The server agrees, and the protocol "switches."
- **Persistence**: The connection stays open as long as both sides are alive. If the container restarts (e.g., during a deploy), all connected users are instantly disconnected.

## 🔬 Internal Mechanics (Load Balancing)
1. **L4 (TCP) Balancing**: The balancer just pipes the bits. Harder to do "Sticky Sessions" based on app logic.
2. **L7 (HTTP) Balancing**: The balancer (Nginx/ALB) reads the "Session Cookie." It ensures that all requests from User A go to Container 1.
3. **The Buffer**: If the Load Balancer has a short timeout (e.g., 60s), it will kill the WebSocket if no data is sent.

## 🔁 Execution Flow
1. Client sends HTTP Upgrade.
2. Load Balancer (Nginx) reads Cookie, routes to Container A.
3. Container A accepts Upgrade. Connection is now a persistent TCP socket.
4. App sends message: "User A joined."
5. Container A publishes to Redis: `channel:chat, msg: "User A joined"`.
6. Container B (subscribed to Redis) receives message and pushes it to User B.

## 🧠 Resource Behavior
- **Memory**: Each open WebSocket consumes memory in the container (to store session state) and in the Load Balancer. 100,000 connections can use several GBs of RAM.
- **File Descriptors**: Every connection is a file. You MUST increase the `ulimit nofile` for both the app and the proxy to handle thousands of users.

## 📐 ASCII Diagrams (REQUIRED)

```text
       SCALING WEBSOCKETS WITH REDIS
       
[ Client A ]       [ Client B ]
     |                  |
 (Socket)           (Socket)
     v                  v
[ Container 1 ]    [ Container 2 ]
     |                  |
     +----[ REDIS ]-----+
          (Intercom)
          
(1) A sends "Hi" -> C1
(2) C1 -> Redis (Publish)
(3) Redis -> C2 (Subscribe)
(4) C2 -> B sends "Hi"
```

## 🔍 Code (Nginx WebSocket Config)
```nginx
location /socket.io/ {
    proxy_pass http://nodeserver;
    proxy_http_version 1.1;
    # Essential headers for Upgrade
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    
    # Increase timeouts for long-lived sockets
    proxy_read_timeout 86400;
}
```

## 💥 Production Failures
- **The "Massive Disconnect"**: You deploy a new version of your container. All 50,000 active WebSockets are killed at once. All 50,000 clients try to reconnect at the exact same millisecond. This creates a **Thundering Herd** that crashes your Load Balancer and Database.
  *Fix*: Use "Jitter" in your client-side reconnection logic (wait random time between 1-5s).
- **The "Idle Timeout"**: Users complain they are disconnected every 60 seconds.
  *Fix*: Implement a "Heartbeat" (Ping/Pong) in your app or increase the LB timeout.

## 🧪 Real-time Q&A
**Q: Can I use standard Round-Robin load balancing for WebSockets?**
**A**: Only for the *initial* connection. Once the socket is open, it's pinned to the container. However, if your app uses a framework like Socket.IO, it often starts with "Long Polling" before upgrading. For Long Polling to work, you **MUST** have Sticky Sessions, otherwise, Request 1 goes to Container A and Request 2 goes to Container B, and the handshake fails.

## ⚠️ Edge Cases
- **Maximum Connections**: Linux default `ip_local_port_range` and `file-max` limits will stop you at ~65,000 connections. To go higher, you need multiple virtual IPs or heavy kernel tuning.

## 🏢 Best Practices
- **Use a Message Broker**: Redis or RabbitMQ is mandatory for scaling beyond one container.
- **Client Reconnection**: Always implement exponential backoff with jitter on the client side.
- **Monitor Connection Count**: Use `netstat -an | grep ESTABLISHED | wc -l` to track active sockets.

## ⚖️ Trade-offs
| Feature | HTTP | WebSockets |
| :--- | :--- | :--- |
| **State** | Stateless | **Stateful** |
| **Overhead** | High (per request) | **Low** (once open) |
| **Scaling** | Easy | **Hard** |

## 💼 Interview Q&A
**Q: How do you scale a Socket.IO application in Docker across multiple hosts?**
**A**: To scale Socket.IO, I use two things: 1. **Session Affinity (Sticky Sessions)** at the Load Balancer level (using cookies or IP hashing) to ensure the initial handshake and polling requests reach the same container. 2. A **Redis Adapter** to synchronize messages. Since a client is only connected to one container, that container must publish any outgoing messages to Redis so that other containers can receive them and forward them to their own connected clients.

## 🧩 Practice Problems
1. Build a simple Chat app with Socket.IO. Run 2 replicas. Notice that they can't "see" each other's messages.
2. Add Redis to the app and verify that messages are now synchronized across replicas.
3. Configure Nginx with `ip_hash` to provide sticky sessions and verify the connection upgrade works.

---
Prev: [05_Connection_Lifecycle_TCP_TLS.md](./05_Connection_Lifecycle_TCP_TLS.md) | Index: [00_Index.md](../00_Index.md) | Next: [01_Volumes_vs_Bind_Mounts.md](../Storage/01_Volumes_vs_Bind_Mounts.md)
---
