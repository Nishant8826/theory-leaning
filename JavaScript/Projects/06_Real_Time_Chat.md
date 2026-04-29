# 📌 Project 06 — Real-Time Chat System

## 🌟 Introduction

Most of the web works on the **"Request-Response"** model: You ask for a page, and the server gives it to you. But for a chat app, that’s too slow. You don't want to refresh the page every 1 second to see if you have new messages!

The solution is **WebSockets**.

Think of it like a **Phone Call**:
-   **HTTP:** Is like sending a letter. You send it, wait, and get a reply days later.
-   **WebSockets:** Is like a phone call. The line stays open, and both people can talk at the exact same time (Full Duplex).

---

## 🏗️ 1. The Strategy

1.  **Connection:** When a user opens the app, they "dial" the server.
2.  **Tracking:** The server keeps a list of every active "phone line" (WebSocket).
3.  **Broadcasting:** When User A sends a message, the server finds everyone else in the list and "shouts" the message to them.

---

## 🏗️ 2. The Implementation (Node.js)

Using the popular `ws` library:

```javascript
const WebSocket = require('ws');

// 1. Start the server
const wss = new WebSocket.Server({ port: 8080 });

// 2. Listen for new "Calls" (Connections)
wss.on('connection', (ws) => {
  console.log("A new user joined the chat!");

  // 3. Listen for "Voice" (Messages) from this user
  ws.on('message', (message) => {
    console.log(`Received: ${message}`);

    // 4. BROADCAST: Send this message to EVERYONE else
    wss.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    });
  });

  ws.on('close', () => console.log("User disconnected."));
});
```

---

## 🚀 3. The "Heartbeat" Trick

Internet connections die all the time. Sometimes a user closes their laptop, but the server thinks they are still there. We use a **Heartbeat** (Ping/Pong) to check.

```javascript
// Every 30 seconds, the server sends a "Are you there?" (Ping)
setInterval(() => {
  wss.clients.forEach((ws) => {
    if (ws.isAlive === false) return ws.terminate();

    ws.isAlive = false;
    ws.ping(); // Send a Ping
  });
}, 30000);
```

---

## 📐 Visualizing the Broadcast

```text
 [ USER A ] ───▶ (Sends: "Hi!") ───▶ [ CHAT SERVER ]
                                           │
                    ┌──────────────────────┴──────────────────┐
                    ▼                                         ▼
              [ USER B ]                                [ USER C ]
            (Receives: "Hi!")                         (Receives: "Hi!")
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Binary vs. String
WebSockets can send two types of data: **UTF-8 Strings** and **Binary (ArrayBuffers)**. If you are building a text chat, strings are fine. But if you are building a high-speed game or a voice chat, you should use Binary data. V8 handles Binary data much more efficiently because it doesn't have to "encode" or "decode" it—it just passes the raw memory chunks directly to the network card.

---

## 💼 Interview Tips

-   **What is the "Handshake"?** A WebSocket starts as a regular HTTP request. If the server supports it, it "Upgrades" the connection to a WebSocket. This is called the **WebSocket Handshake**.
-   **How do you handle scaling?** One server can only handle about 10,000–50,000 connections. If you have a million users, you need multiple servers and a **Redis Pub/Sub** system to share messages between the servers.
-   **What is Backpressure in WebSockets?** If a user has a very slow 3G connection, the server might send messages faster than the user can receive them. You should check `ws.bufferedAmount` to see if the user's "inbox" is getting too full.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **WebSockets** | Real-time; very low latency. | Keeps a connection open (uses server memory). |
| **HTTP Polling** | Very simple; works everywhere. | High latency; wastes bandwidth. |
| **SSE (Server-Sent Events)** | Simpler than WebSockets (one-way).| Only works from Server -> Client. |

---

## 🔗 Navigation

**Prev:** [05_Build_Rate_Limiter.md](05_Build_Rate_Limiter.md) | **Index:** [../00_Index.md](../00_Index.md)
