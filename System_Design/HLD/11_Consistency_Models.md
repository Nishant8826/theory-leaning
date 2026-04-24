# 📌 Consistency Models

## 🧠 Concept Explanation (Story Format)

You're editing a Google Doc with your team. When you type something, does your teammate see it:
- Instantly? (Strong consistency)
- After a 1-second delay? (Eventual consistency)
- In a different order than you typed? (Causal consistency issue)

Different applications need different consistency guarantees. A banking app cannot use "eventual consistency" for balances. But a social media "likes counter" can be slightly off for a few seconds.

Consistency models define the **rules** for how and when data changes become visible across distributed nodes.

---

## 🏗️ Basic Design (Naive)

```
Simple setup: Single server
Write → Server → Read

No consistency issues because there's only one copy of the data!
But: No fault tolerance, no scalability.
```

---

## ⚡ Optimized Design

```
Distributed setup with multiple nodes:
Write → Primary → Replicate to → Secondary 1
                             → Secondary 2
                             → Secondary 3

Different reads get different answers depending on
WHEN they happen and WHICH node they read from.

Consistency model defines: What guarantees do we make?
```

---

## 🔍 Consistency Models (Weakest to Strongest)

### 1. Eventual Consistency (Weakest)
Given enough time with no new updates, all nodes will eventually agree.

```
Timeline:
T=0: Write "likes=100" to Primary
T=1ms: User A reads "likes=100" from Primary ✅
T=1ms: User B reads "likes=99" from Replica (not yet replicated) ⚠️
T=50ms: Replication complete
T=50ms: User B reads "likes=100" from Replica ✅

Eventually all nodes agree. Temporary inconsistency is OK.
```

**Use when:** Like counts, view counts, activity feeds, product review counts.

```javascript
// Eventual consistency in Node.js — read from any replica
const likes = await replicaDB.query(
  'SELECT likes_count FROM posts WHERE id = $1', [postId]
);
// May return slightly stale count — that's OK for likes
```

---

### 2. Read-Your-Own-Writes Consistency
After a write, you always see your own write (but others may not yet).

```
T=0: Alice writes "username = AliceNew"
T=1ms: Alice reads → "AliceNew" ✅ (guaranteed to see own write)
T=1ms: Bob reads → "AliceOld" ⚠️ (may not see yet — OK)
T=50ms: Bob reads → "AliceNew" ✅
```

**Use when:** User profile updates, any UI that shows "your" data after you change it.

```javascript
// Implementation: Route reads to primary for 5 seconds after a write
async function updateUsername(userId, newName) {
  await primaryDB.query('UPDATE users SET name = $1 WHERE id = $2', [newName, userId]);
  await redis.setex(`user_wrote:${userId}`, 5, '1'); // Mark: just wrote
}

async function getUser(userId) {
  const justWrote = await redis.get(`user_wrote:${userId}`);
  const pool = justWrote ? primaryPool : replicaPool;
  return pool.query('SELECT * FROM users WHERE id = $1', [userId]);
}
```

---

### 3. Monotonic Reads Consistency
Once you read a value, you'll never read an older value later.

```
BAD (without monotonic reads):
T=0: User reads likes=100 (from Replica 1)
T=1: User reads likes=99  (from Replica 2, which is behind)
→ User sees count go BACKWARDS — confusing!

GOOD (with monotonic reads):
T=0: User reads likes=100 (from Replica 1)
T=1: User reads likes=100 or 101 (from same replica or more updated one)
→ Count never goes backwards
```

**Implementation:** Stick the same user to the same replica (session-based routing).

```javascript
// Route user to same replica using Redis to track assignment
async function getReplicaForUser(userId) {
  const assigned = await redis.get(`user_replica:${userId}`);
  if (assigned) return assigned;
  
  const replica = pickLeastLoadedReplica();
  await redis.setex(`user_replica:${userId}`, 3600, replica);
  return replica;
}
```

---

### 4. Causal Consistency
Operations that are causally related are seen in the correct order by all nodes.

```
Alice posts: "Who wants coffee?" → seen first
Bob replies: "Me!" → always seen AFTER Alice's post

Without causal consistency:
Bob's reply might appear BEFORE Alice's question → confusing!

With causal consistency:
Cause (Alice's post) always appears before effect (Bob's reply)
```

**Use when:** Messaging apps (WhatsApp), comment threads, any reply/response system.

```javascript
// WhatsApp-style: Attach vector clock to each message
const message = {
  id: uuid(),
  content: "Me!",
  replyToId: aliceMessageId,     // Causal dependency
  vectorClock: { alice: 1, bob: 1 },  // Track causality
  timestamp: Date.now()
};
// Server ensures replyTo is delivered BEFORE the reply
```

---

### 5. Sequential Consistency (Linearizability)
All operations appear to happen in some global sequential order, and each operation takes effect atomically.

```
All nodes see ALL operations in the SAME order.

Node A write: X=1
Node B write: X=2

All reads everywhere must see either X=1 or X=2,
but ALL must see them in the same order (1 then 2, or 2 then 1, but consistently)

No node can see 2 first and then 1.
```

---

### 6. Strong Consistency (Linearizability — Strongest)
Every read returns the most recent write, as if there's only one copy of the data.

```
T=0ms: Write "balance=500"
T=1ms: Read → returns 500 (guaranteed!)

No stale data ever. Every read reflects all prior writes.
```

**Use when:** Bank balances, inventory counts, leader election, distributed locks.

```javascript
// Force strong consistency: Always read from primary
async function getAccountBalance(accountId) {
  // Never use replica for financial data!
  const result = await primaryPool.query(
    'SELECT balance FROM accounts WHERE id = $1', [accountId]
  );
  return result.rows[0].balance;
}

// Redis also supports strong consistency for distributed locks
const redlock = new Redlock([redis]);
const lock = await redlock.acquire(['lock:account:123'], 5000);
try {
  // Only one server can execute this at a time!
  await updateBalance(accountId, amount);
} finally {
  await lock.release();
}
```

---

## ⚖️ Trade-offs

| Model | Guarantee | Latency | Complexity | Use Case |
|-------|-----------|---------|------------|----------|
| Eventual | Will eventually agree | Lowest | Simple | Social likes, views |
| Read-Your-Writes | You see your writes | Low | Medium | Profile updates |
| Monotonic Reads | No backward time | Low | Medium | Feed scrolling |
| Causal | Cause before effect | Medium | High | Messaging, comments |
| Strong | Always latest data | Highest | High | Banking, inventory |

---

## 📊 Scalability Discussion

### Consistency vs Performance Curve

```
Strong Consistency
        ↑ 
        |  Latency
        |  /
        | /
        |/________________________
        └───────────────────────→
   Strong                    Eventual
   Consistency             Consistency

As you relax consistency → lower latency + higher throughput
```

### AWS DynamoDB Consistency Options

```javascript
const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB.DocumentClient();

// Eventually consistent read (default, faster, cheaper)
const result = await dynamodb.get({
  TableName: 'Users',
  Key: { userId: '123' }
}).promise();

// Strongly consistent read (slower, costs 2x read capacity)
const result = await dynamodb.get({
  TableName: 'Users',
  Key: { userId: '123' },
  ConsistentRead: true  // Strong consistency!
}).promise();
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is the difference between eventual consistency and strong consistency?

**Solution:**
- **Strong Consistency:** Every read returns the most recent write. All nodes appear as one. Like a single database. Latency is higher because you must wait for all nodes to agree.
- **Eventual Consistency:** After a write, different nodes may temporarily return different values. But given time, all nodes converge to the latest value. Much faster and more available.

Real analogy:
- Strong: Like a bank ATM — you always see your exact balance.
- Eventual: Like a social media like count — might show 1,234 or 1,233 for a brief moment.

---

### Q2: When would you use eventual consistency vs strong consistency?

**Solution:**
Use **Eventual Consistency** for:
- View counts (YouTube)
- Like counts (Instagram)
- Activity feeds (Twitter timeline)
- Analytics/reporting
- Product review averages
- Any read-heavy, write-sometimes data

Use **Strong Consistency** for:
- Bank account balances
- Payment processing
- Seat reservation (flight booking)
- Inventory management (can't oversell)
- User authentication (can't login with stale banned status)
- Distributed locks

Rule of thumb: "Can the user tolerate seeing slightly old data for 1-5 seconds?" → Eventual. "No? Absolutely must be current?" → Strong.

---

### Q3: How do you implement read-your-own-writes consistency in a Node.js + PostgreSQL system?

**Solution:**
```javascript
// Using a "read timestamp" approach
class ConsistencyManager {
  async write(userId, query, params) {
    const result = await primaryDB.query(query, params);
    // Store the transaction ID or timestamp of the last write per user
    const txTimestamp = Date.now();
    await redis.setex(`user_last_write:${userId}`, 30, txTimestamp.toString());
    return result;
  }

  async read(userId, query, params) {
    const lastWriteTime = await redis.get(`user_last_write:${userId}`);
    
    if (!lastWriteTime) {
      // User hasn't written recently → use replica (fast)
      return replicaDB.query(query, params);
    }
    
    const timeSinceWrite = Date.now() - parseInt(lastWriteTime);
    if (timeSinceWrite < 5000) { // Less than 5 seconds since write
      // Use primary to guarantee seeing own write
      return primaryDB.query(query, params);
    }
    
    // Enough time has passed → replica is caught up
    return replicaDB.query(query, params);
  }
}
```

---

### Q4: Explain vector clocks and why they're used in distributed systems.

**Solution:**
Vector clocks track causal relationships between events in a distributed system.

```javascript
// Vector clock: { server1: 3, server2: 1, server3: 0 }
// Means: "I've seen 3 events from server1, 1 from server2, 0 from server3"

class VectorClock {
  constructor(nodeId, initialClock = {}) {
    this.nodeId = nodeId;
    this.clock = initialClock;
  }
  
  increment() {
    this.clock[this.nodeId] = (this.clock[this.nodeId] || 0) + 1;
    return { ...this.clock };
  }
  
  merge(otherClock) {
    // Take the max of each node's counter
    const merged = { ...this.clock };
    for (const [node, time] of Object.entries(otherClock)) {
      merged[node] = Math.max(merged[node] || 0, time);
    }
    this.clock = merged;
    return merged;
  }
  
  happensBefore(otherClock) {
    // This clock happened before otherClock if all my values ≤ other's values
    return Object.entries(this.clock).every(
      ([node, time]) => time <= (otherClock[node] || 0)
    );
  }
}

// Use in messaging to determine message order:
const msg1 = { content: "Hello", clock: { alice: 1, bob: 0 } };
const msg2 = { content: "Hi back!", clock: { alice: 1, bob: 1 } };
// msg1 happened before msg2 because alice:1 ≤ alice:1 AND bob:0 ≤ bob:1
```

Used by: Amazon DynamoDB, Apache Cassandra, Riak.

---

### Q5: What is a distributed lock and how do you implement it?

**Solution:**
A distributed lock ensures only one process across all servers can execute a critical section at a time.

```javascript
// Using Redis Redlock algorithm
const Redlock = require('redlock');
const redis = require('ioredis');

const redisClient = new redis(process.env.REDIS_URL);
const redlock = new Redlock([redisClient], {
  retryCount: 3,
  retryDelay: 200,  // Wait 200ms between retries
  retryJitter: 50   // Add random jitter to avoid thundering herd
});

// Use case: Only one server should process a payment at a time
async function processPayment(orderId, amount) {
  const lockKey = `lock:payment:${orderId}`;
  const lockTTL = 10000; // 10 second lock
  
  let lock;
  try {
    lock = await redlock.acquire([lockKey], lockTTL);
    // Only one server can be here at a time!
    
    // Check if already processed (idempotency)
    const alreadyProcessed = await redis.get(`payment:processed:${orderId}`);
    if (alreadyProcessed) return { status: 'already_processed' };
    
    // Process the payment
    const result = await stripe.charges.create({ amount });
    
    // Mark as processed
    await redis.setex(`payment:processed:${orderId}`, 86400, result.id);
    
    return result;
  } finally {
    if (lock) await lock.release();
  }
}
```

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design the consistency strategy for a real-time collaborative document editor (Google Docs-like)

**Solution:**
```
Required: Causal Consistency (changes must be in causal order)
Operational Transformation (OT) or CRDTs (Conflict-free Replicated Data Types)

Architecture:
1. Each client maintains local copy and vector clock
2. User types → Apply change locally immediately (optimistic UI)
3. Send operation to server with vector clock
4. Server reorders operations based on causal order
5. Broadcast ordered operations to all clients
6. Clients apply remote operations using OT to merge with local changes

Node.js Implementation with Socket.IO:
```

```javascript
// Server-side: Ordering operations causally
const operations = []; // In-memory for simplicity (use Redis in production)

io.on('connection', (socket) => {
  socket.on('operation', (op) => {
    // op: { type: 'insert', position: 5, char: 'A', vectorClock: {...}, userId: '...' }
    
    // Transform against concurrent operations
    const transformedOp = operationalTransform(op, operations);
    operations.push(transformedOp);
    
    // Broadcast in causal order to all clients
    socket.broadcast.emit('remote_operation', transformedOp);
  });
});

function operationalTransform(newOp, existingOps) {
  // Find concurrent operations (not causally dependent)
  const concurrent = existingOps.filter(op => isConcurrent(op, newOp));
  
  // Transform newOp against each concurrent op
  let transformed = newOp;
  for (const concurrentOp of concurrent) {
    transformed = transform(transformed, concurrentOp);
  }
  return transformed;
}
```

---

### Problem 2: Your social media app shows users their like count going backward (5002 → 5001 → 5003). How do you fix it?

**Solution:**
This is a **monotonic reads violation** — different replicas returning different values.

**Root cause:** User's requests hitting different replicas in different states.

**Fix 1: Session-based replica affinity**
```javascript
// Route same user to same replica for 1 minute
app.use(async (req, res, next) => {
  if (!req.user) return next();
  
  const userId = req.user.id;
  let assignedReplica = await redis.get(`replica:${userId}`);
  
  if (!assignedReplica) {
    assignedReplica = loadBalancer.pickReplica();
    await redis.setex(`replica:${userId}`, 60, assignedReplica);
  }
  
  req.dbPool = getPoolForReplica(assignedReplica);
  next();
});
```

**Fix 2: Use Redis as the source of truth for counts (not DB replica)**
```javascript
// Store like counts in Redis (single source, no replication lag)
async function getLikeCount(postId) {
  const count = await redis.get(`likes:${postId}`);
  if (count !== null) return parseInt(count);
  
  // Cache miss: load from primary DB
  const result = await primaryDB.query('SELECT likes_count FROM posts WHERE id = $1', [postId]);
  await redis.set(`likes:${postId}`, result.rows[0].likes_count);
  return result.rows[0].likes_count;
}

async function likePost(postId, userId) {
  // Atomic increment in Redis (no race condition, no replication lag)
  await redis.incr(`likes:${postId}`);
  // Async: persist to DB (eventual consistency for storage, not display)
  queue.add('persistLike', { postId, userId });
}
```

---

### Navigation
**Prev:** [10_CAP_Theorem.md](10_CAP_Theorem.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [12_API_Design.md](12_API_Design.md)
