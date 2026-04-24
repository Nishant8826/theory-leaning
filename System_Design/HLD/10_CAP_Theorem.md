# 📌 CAP Theorem

## 🧠 Concept Explanation (Story Format)

It's 2010. You have twin brothers Bob and Alice managing two copies of your banking ledger (for backup). They're in different cities.

Bob records: "Customer John has $1000".

An earthquake cuts off communication between Bob and Alice.

Now a customer wants to withdraw $500. What do you do?

**Option A:** Refuse the transaction until Bob and Alice can communicate again. (System is **unavailable** during the outage, but data is always **consistent**)

**Option B:** Let Alice process the withdrawal based on her (potentially outdated) ledger. (System stays **available**, but Alice's ledger might be out of sync — **inconsistency**)

You CANNOT do both when communication is cut off. This is the **CAP Theorem**.

---

## 🏗️ CAP Theorem Explained

**CAP stands for:**

```
C - Consistency:    Every read gets the most recent write (or an error)
A - Availability:   Every request receives a response (not necessarily the latest data)
P - Partition Tolerance: System works even when network between nodes fails
```

**The theorem states:**
> In a distributed system, you can ONLY guarantee TWO of these three properties at once.

```
         Consistency (C)
              /\
             /  \
            /    \
           / CA   \
          /        \
         /    CAP   \  ← IMPOSSIBLE!
        /______________\
Availability (A) ——— Partition Tolerance (P)
        AP              CP
```

**BUT: Partition Tolerance is NOT optional in practice!**

Why? Network partitions WILL happen. Networks fail. Servers get isolated. You MUST handle partitions.

So the real choice is: **CP vs AP when a partition occurs.**

---

## ⚡ Real World Choices

### CP Systems (Consistency + Partition Tolerance)
```
When partition occurs: System refuses reads/writes rather than return stale data
Example: Your bank account balance
→ Better to show "Service unavailable" than show wrong balance!

CP Databases: MongoDB (default), HBase, Zookeeper, Redis (single node)
```

### AP Systems (Availability + Partition Tolerance)
```
When partition occurs: System continues serving requests, but data might be stale
Example: Instagram likes count
→ Better to show "1,234 likes" (slightly off) than show error!

AP Databases: Cassandra, CouchDB, DynamoDB, Amazon S3
```

---

## 🔍 Key Components

### Applying CAP to Our Stack

**PostgreSQL (Primary + Replica setup):**
- By default: **CP system**
- During network partition between primary and replica:
  - PostgreSQL stops accepting writes to replica (consistency preserved)
  - Primary continues serving reads and writes
  - If primary and replica are separated, replica returns error (not stale data)

**MongoDB:**
- Default: **CP system**
- With `readPreference: 'secondary'` → **AP system** (may return stale data from replica)

```javascript
// MongoDB CP (default) - Consistent reads
const post = await db.collection('posts').findOne(
  { _id: postId },
  { readPreference: 'primary' }  // Always read from primary
);

// MongoDB AP - Available reads (may be stale)
const post = await db.collection('posts').findOne(
  { _id: postId },
  { readPreference: 'secondaryPreferred' }  // Read from replica, may be behind
);
```

**Redis (Cluster mode):**
- **AP system** by default
- Fast, available, but may return stale data during partition

**Cassandra:**
- **AP system** by design
- Uses "eventual consistency" — all nodes will eventually agree
- You can tune consistency level per query!

```javascript
// Cassandra consistency tuning
// QUORUM: Most nodes must agree (CP-like)
const result = await client.execute(query, params, { consistency: cassandra.types.consistencies.quorum });

// ONE: Just one node responds (AP-like, fastest)  
const result = await client.execute(query, params, { consistency: cassandra.types.consistencies.one });
```

---

### Consistency Spectrum

CAP theorem is binary, but reality is a spectrum:

```
Strong                                              Eventual
Consistency  ←————————————————————————————————→  Consistency

[Bank transfer] [User profile] [Post likes] [View count] [Analytics]
     CP               CP            AP            AP           AP
```

**Strong Consistency:** You always read your own writes and the latest data.
**Eventual Consistency:** Given enough time with no new updates, all nodes agree.

---

## ⚖️ Trade-offs

| Scenario | Choose | Why |
|----------|--------|-----|
| Bank transactions | CP | Wrong balance = legal/financial disaster |
| User authentication | CP | Can't let deleted/banned users login |
| Shopping cart | AP (mostly) | Shopping cart being 1s stale is OK |
| Social media likes | AP | "1,234 likes" vs "1,235 likes" — nobody cares |
| Inventory count | CP | Overselling is a business problem |
| User activity feed | AP | Slightly stale feed is fine |
| Config/feature flags | CP | Inconsistent feature flags → bugs |

---

## 📊 Scalability Discussion

### PACELC Model (Extension of CAP)

CAP only talks about partitions. **PACELC** extends it:

```
If Partition:
  Choose Consistency OR Availability (like CAP)
Else (no partition, normal operation):
  Choose Low Latency OR Consistency

PACELC: PA/EL = Partition Availability / Else Latency
```

- **DynamoDB:** PA/EL — During partition: Available. Normal: Low Latency.
- **PostgreSQL:** PC/EC — During partition: Consistent. Normal: Consistent.
- **Cassandra:** PA/EL — During partition: Available. Normal: Low Latency.

### Handling Consistency in Node.js

```javascript
// Strategy: Critical operations → use strong consistency (CP)
//           Non-critical → use eventual consistency (AP)

class UserService {
  // CRITICAL: Login must be consistent (can't login with stale password)
  async login(email, password) {
    // Always query primary DB
    const user = await primaryPool.query(
      'SELECT * FROM users WHERE email = $1', [email]
    );
    // ... verify password
  }

  // NON-CRITICAL: Profile view can be slightly stale
  async getProfile(userId) {
    // First check Redis cache (may be slightly stale but fast)
    const cached = await redis.get(`profile:${userId}`);
    if (cached) return JSON.parse(cached);
    
    // Cache miss: read from replica (slightly stale but OK)
    const profile = await replicaPool.query(
      'SELECT * FROM users WHERE id = $1', [userId]
    );
    await redis.setex(`profile:${userId}`, 300, JSON.stringify(profile.rows[0]));
    return profile.rows[0];
  }

  // CRITICAL: Changing password must be strongly consistent
  async changePassword(userId, newHash) {
    await primaryPool.query(
      'UPDATE users SET password_hash = $1 WHERE id = $2', [newHash, userId]
    );
    // Immediately invalidate cache — can't have stale password in cache!
    await redis.del(`profile:${userId}`);
  }
}
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: Explain the CAP theorem in simple terms.

**Solution:**
In a distributed system with multiple servers, when a **network partition** occurs (servers can't talk to each other), you must choose:
- **Consistency (C):** Return an error or wait — don't return stale data
- **Availability (A):** Return the best data you have (might be stale), but always respond

Since network partitions are inevitable in distributed systems, you always must handle them. So you always have **P**, and the real choice is **C vs A during partitions**.

Real example: Banking app (choose C — wrong balance is unacceptable) vs Instagram likes (choose A — slightly wrong count is fine).

---

### Q2: Why can't we have all three: Consistency, Availability, and Partition Tolerance?

**Solution:**
Imagine two database nodes, Node A and Node B. They have the same data.

A network partition occurs — they can't communicate.

A user writes new data to Node A. Now:
- Node A has new data
- Node B has old data (they can't sync because of the partition)

A different user reads from Node B:
- If we guarantee **Consistency:** Node B must return an error (it doesn't have the latest data)
- If we guarantee **Availability:** Node B returns stale data

We cannot return the latest data AND respond successfully at the same time when the nodes can't sync. Hence, you must pick one.

---

### Q3: How does MongoDB handle CAP? Is it CP or AP?

**Solution:**
MongoDB is **CP by default** (consistency + partition tolerance):
- All writes go to primary node
- If primary fails → cluster elects a new primary (may take 10-30 seconds)
- During election: No writes accepted (consistency preserved over availability)
- Reads from secondary with `{ readPreference: 'secondaryPreferred' }` → AP (may return stale data)

**MongoDB 4.0+ with replica sets:**
- Supports ACID transactions across multiple documents
- During a partition where primary is isolated: Automatically steps down, cluster elects new primary
- Data is never corrupted, but availability suffers briefly

---

### Q4: A startup says "We'll build a CA system." Why is this impossible?

**Solution:**
A CA (Consistent + Available, but no Partition Tolerance) system only works if the network NEVER fails. This is impossible in the real world.

A single-machine database (no distribution) is effectively "CA" — no network partition between nodes because there's only one node. But:
- Single machine = single point of failure
- Single machine = limited scaling
- The moment you add a second server → you have a network between them → potential partition → you're back to CAP

Any real distributed system must be **P** (partition tolerant). CA is only theoretical or for single-node setups.

---

### Q5: How would you design an e-commerce checkout system considering CAP?

**Solution:**
Different parts of checkout have different CAP requirements:

```
User Profile Display: AP
  → Show slightly stale profile data, always respond

Product Availability Check: CP
  → Don't show "In Stock" if actually out of stock (oversell!)
  → Use strong consistency for inventory reads

Price Calculation: CP
  → Prices must be accurate (legal issue if wrong)
  → Read from primary DB only

Payment Processing: CP (extremely strong consistency)
  → Use external payment service (Stripe) with their own consistency guarantees
  → Don't allow any eventual consistency here

Order Confirmation Email: AP (eventual)
  → Slightly delayed email is OK — queue it, send when system recovers

Implementation:
```

```javascript
async function checkout(userId, cartItems) {
  // CP: Check inventory (primary DB only)
  const inventory = await primaryDB.query(
    'SELECT * FROM inventory WHERE product_id = ANY($1) FOR UPDATE', // Lock rows!
    [cartItems.map(i => i.productId)]
  );
  
  // Verify all items in stock
  for (const item of cartItems) {
    const stock = inventory.find(i => i.product_id === item.productId);
    if (stock.quantity < item.quantity) {
      throw new Error(`${item.productId} out of stock`);
    }
  }
  
  // CP: Deduct inventory (atomic transaction)
  await primaryDB.query('BEGIN');
  for (const item of cartItems) {
    await primaryDB.query(
      'UPDATE inventory SET quantity = quantity - $1 WHERE product_id = $2',
      [item.quantity, item.productId]
    );
  }
  
  // CP: Process payment via Stripe (external strong consistency)
  const charge = await stripe.charges.create({ amount: total, currency: 'usd' });
  
  // CP: Create order record
  const order = await primaryDB.query('INSERT INTO orders...', [...]);
  await primaryDB.query('COMMIT');
  
  // AP: Send confirmation email (queued, can be slightly delayed)
  await emailQueue.add({ userId, orderId: order.id });
  
  return order;
}
```

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design a distributed counter (e.g., YouTube view count) considering CAP

**Solution:**
```
Requirements:
- Views count must eventually be accurate (not necessarily real-time exact)
- System must always be available (even if some nodes are down)
- Choice: AP (eventually consistent)

Design:
1. User watches video → Write to nearest Redis node (fast, always available)
   redis.incr('video:views:videoId')

2. Redis nodes may be temporarily inconsistent during partitions → AP choice

3. Periodic batch job (every 5 min): Aggregate all Redis counters
   → Write accurate total to PostgreSQL
   → Reset Redis counters

4. Display: Show Redis count (approximate, fast) for real-time feel
   → Underlying PostgreSQL for official count

Result:
- Display: "~1.2M views" (slightly approximate but always available)
- Analytics dashboard: "1,234,567 views" (accurate, from PostgreSQL, may lag 5 min)

Why not CP?
- If we make view counter strongly consistent:
  → Every view must be confirmed by all nodes before responding
  → YouTube would be unusable under high traffic
  → Users watching videos see "Loading..." for every view
  → NOT worth it for a view count
```

---

### Problem 2: WhatsApp message delivery — how does it handle CAP?

**Solution:**
```
Message delivery has mixed CAP requirements:

SENDING a message: AP (availability first)
  → Message accepted immediately (even if recipient's server is partitioned)
  → Stored in queue (Kafka/SQS)
  → "One tick" shown (sent to server)

DELIVERING to recipient: Eventually consistent
  → Server keeps retrying until recipient's device acknowledges
  → "Two ticks" shown (delivered)
  → "Blue ticks" shown (read)

Message ORDER: CP (consistency critical)
  → Messages must be delivered in order
  → WhatsApp uses sequence numbers per conversation
  → If order can't be guaranteed: hold messages until order is established

Implementation:
- Client sends message → API server (always available) accepts it
- Stored in message queue (Kafka)
- Delivery service picks up and delivers to recipient's socket
- If recipient offline: stored in DB, delivered when they come online
- ACK protocol ensures no message is lost (may be delayed, but never dropped)
```

---

### Navigation
**Prev:** [09_Replication_and_Sharding.md](09_Replication_and_Sharding.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [11_Consistency_Models.md](11_Consistency_Models.md)
