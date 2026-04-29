# 📌 06 — Stateful vs Stateless: Scalability and Distributed Context

## 🧠 Concept Explanation

### Basic → Intermediate
A **Stateless** service treats every request as an independent transaction. It doesn't store any data about the user or the previous request in its own memory. A **Stateful** service "remembers" information across requests (e.g. session data in a local variable).

### Advanced → Expert
At a staff level, this is about **Horizontal Scalability**.
1. **Stateless**: You can spin up 100 instances of the service, and a load balancer can send a request to any one of them. This is the foundation of Cloud Native and Serverless architectures.
2. **Stateful**: The client must always hit the same instance (Sticky Sessions) because their data is only on that specific server's RAM. If that server crashes, the data is lost.

In modern backend engineering, we strive for **Stateless Services** with **Externalized State** (e.g. in Redis or a Database).

---

## 🏗️ Common Mental Model
"My app is stateless because I use a database."
**Correction**: Your app is stateless only if **zero** information about the current request's context is stored in the Node.js process memory. If you have a `currentUser` variable at the module level, your app is stateful.

---

## ⚡ Actual Behavior: The "Node.js Singleton" Trap
In Node.js, modules are cached. If you store data in a variable at the top level of a file, that variable is shared by **every request** hitting that process. This is a form of state that can lead to bugs if not managed carefully (e.g. data leaking between users).

---

## 🔬 Internal Mechanics (Memory + Distributed Systems)

### Session Affinity (Sticky Sessions)
If you MUST use a stateful service (like a WebSocket server without a Redis adapter), you must configure your Load Balancer (ALB, Nginx) to use **Session Affinity**. It uses a cookie or Source IP to ensure the client is always routed to the same PID.

### The Cost of Statelessness
Making a service stateless isn't free. You must perform an extra network hop to Redis/DB on every request to retrieve the context that was previously in memory. This adds 1-5ms of latency.

---

## 📐 ASCII Diagrams

### Stateless Scaling
```text
  CLIENTS ──────▶ [ LOAD BALANCER ]
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
  [ Instance 1 ]  [ Instance 2 ]  [ Instance 3 ]
         │               │               │
         └───────────────┴───────────────┘
                         │
                         ▼
                [ EXTERNAL STATE ]
                (Redis / Postgres)
```

---

## 🔍 Code Example: Moving State to Redis
```javascript
// ❌ STATEFUL: Data trapped in process memory
let userSession = {};
app.post('/login', (req, res) => {
  userSession[req.body.id] = { loggedIn: true };
  res.send('OK');
});

// ✅ STATELESS: Data stored externally
const Redis = require('ioredis');
const redis = new Redis();

app.post('/login', async (req, res) => {
  await redis.set(`session:${req.body.id}`, JSON.stringify({ loggedIn: true }));
  res.send('OK');
});
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Random" Logouts
**Problem**: Users report being randomly logged out while browsing the site.
**Reason**: You have 3 server instances and are storing sessions in a local JS object. When the load balancer sends the user to Instance 1, they log in. When it sends them to Instance 2, they don't exist in memory, so they are redirected to login.
**Fix**: Use a shared session store (Redis).

### Scenario: The Memory Leak in Global State
**Problem**: The server RSS grows over time.
**Reason**: You are storing "recent searches" in a global array to show to users. But you never clear the array. As more users search, the array grows until the process OOMs.
**Fix**: Use a **capped buffer** (e.g. `arr.slice(-100)`) or an external TTL-based store like Redis.

---

## 🧪 Real-time Production Q&A

**Q: "Can a stateless service ever have local cache?"**
**A**: **Yes**, but only for data that is **immutable** or has a very short TTL (Time To Live). If the local cache is just an optimization for data that *also* exists elsewhere, the service is still effectively stateless.

---

## 🏢 Industry Best Practices
- **Twelve-Factor App**: Process should be stateless and share-nothing.
- **JWT for Stateless Auth**: Use JSON Web Tokens to store user identity in the client's request instead of the server's memory.

---

## 💼 Interview Questions
**Q: How do you scale a stateful application?**
**A**: You use **Sharding**. Each instance is responsible for a specific subset of the state (e.g. Instance 1 handles users A-M, Instance 2 handles N-Z). Alternatively, you use a **Distributed Consensus** protocol like Raft or Paxos to synchronize state across instances (very complex).

---

## 🧩 Practice Problems
1. Build a simple "Counter" app. Run two instances on different ports and show how the counter is different on each if using a local variable, but the same if using Redis.
2. Refactor a stateful "Room Chat" implementation to be stateless using Redis Pub/Sub.

---

**Prev:** [05_Backend_For_Frontend.md](./05_Backend_For_Frontend.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [07_Backpressure_in_Distributed_Systems.md](./07_Backpressure_in_Distributed_Systems.md)
