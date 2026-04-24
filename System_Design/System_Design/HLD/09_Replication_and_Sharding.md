# 📌 Replication and Sharding

## 🧠 Concept Explanation (Story Format)

**Replication:** You're a restaurant owner. You have one master recipe book. What if it gets destroyed? You'd lose everything! Smart move: make copies of the recipe book and store them in different locations.

Database replication = making copies of your database. If the primary crashes, a copy (replica) takes over.

**Sharding:** Your restaurant became a global chain with 1000 outlets. One recipe book can't handle all 1000 outlets calling in for recipes simultaneously. Solution: Give Recipe Book A to outlets 1-333, Recipe Book B to 334-666, Recipe Book C to 667-1000.

Database sharding = splitting your data across multiple database servers, each serving a portion of the total load.

---

## 🏗️ Basic Design (Naive)

```
All app servers
      ↓
[Single PostgreSQL Server]
      ↓
All reads + writes go here

Problems:
- Server crash → entire DB down
- High read traffic → server overwhelmed
- Approaching storage limits
- Can't scale beyond one machine
```

---

## ⚡ Optimized Design

```
REPLICATION:
Node.js API Servers
      ↓
   [Reads]          [Writes]
      ↓                 ↓
[Read Replica 1]  [Primary DB]  ← Handles all writes
[Read Replica 2]       ↓
                   Replication (async)
                  → Read Replica 1
                  → Read Replica 2

SHARDING (for massive scale):
User ID 1-250K → [Shard 1: PostgreSQL]
User ID 250K-500K → [Shard 2: PostgreSQL]
User ID 500K-750K → [Shard 3: PostgreSQL]
User ID 750K-1M → [Shard 4: PostgreSQL]

[Shard Router / App Logic] → decides which shard to query
```

---

## 🔍 Key Components

### Replication

**How it works:**
1. Primary DB writes data + logs every change to WAL (Write-Ahead Log)
2. Replicas stream and apply the WAL changes
3. Replica is always a few milliseconds behind (replication lag)

**Synchronous vs Asynchronous Replication:**

| | Synchronous | Asynchronous |
|-|-------------|--------------|
| Write completes when | All replicas confirm | Only primary confirms |
| Data safety | Zero data loss | May lose recent writes on crash |
| Write speed | Slower | Faster |
| Use case | Financial data | Logs, activity feeds |

```javascript
// AWS RDS with read replica routing in Node.js
const { Pool } = require('pg');

const writePool = new Pool({ connectionString: process.env.RDS_PRIMARY_URL });
const readPool = new Pool({ connectionString: process.env.RDS_REPLICA_URL });

// Always write to primary
async function createPost(data) {
  return writePool.query(
    'INSERT INTO posts (user_id, content) VALUES ($1, $2) RETURNING *',
    [data.userId, data.content]
  );
}

// Read from replica (may be slightly stale, but that's OK for feeds)
async function getUserPosts(userId) {
  return readPool.query(
    'SELECT * FROM posts WHERE user_id = $1 ORDER BY created_at DESC LIMIT 20',
    [userId]
  );
}

// Read from PRIMARY when you need guaranteed fresh data (after a write!)
async function getPostAfterCreate(postId) {
  return writePool.query('SELECT * FROM posts WHERE id = $1', [postId]);
}
```

---

### Sharding

**Sharding Strategies:**

**1. Range-Based Sharding**
```javascript
// Users with ID 1-1M on Shard 1, 1M-2M on Shard 2, etc.
function getShardForUser(userId) {
  if (userId <= 1_000_000) return 'shard1';
  if (userId <= 2_000_000) return 'shard2';
  return 'shard3';
}

// Problem: "Hot shards" — early users (celebrities!) are all on Shard 1
// Shard 1 gets 10x more traffic than Shard 3
```

**2. Hash-Based Sharding (Better)**
```javascript
// Hash distributes data evenly across shards
function getShardForUser(userId) {
  const shardCount = 4;
  const shardIndex = userId % shardCount;
  return `shard${shardIndex}`;
}

// userId 123 → 123 % 4 = 3 → shard3
// userId 456 → 456 % 4 = 0 → shard0
// Even distribution! No hot shards.

// ⚠️ Problem: If you add a 5th shard, ALL data needs to be rehashed!
// Solution: Consistent Hashing (used by DynamoDB, Cassandra)
```

**3. Directory-Based Sharding**
```javascript
// A lookup table tells you which shard has which user
const shardDirectory = {
  // userId → shard
  'user:1': 'shard3',
  'user:2': 'shard1',
  // etc. stored in Redis or a separate DB
};

function getShardForUser(userId) {
  return shardDirectory[`user:${userId}`];
}

// Pros: Flexible, can move data between shards without app changes
// Cons: Lookup table is a bottleneck and single point of failure
```

**4. Consistent Hashing**
```javascript
// Imagine a ring of positions 0-360
// Servers occupy positions on the ring
// Each user goes to the nearest server clockwise

// Adding a new server only redistributes a small portion of keys!
// Used by: Redis Cluster, Cassandra, DynamoDB, Memcached

// Libraries: 'hashring' for Node.js
const HashRing = require('hashring');
const ring = new HashRing(['shard1', 'shard2', 'shard3']);
ring.get('user:123'); // → 'shard2'
ring.add('shard4');   // Only ~25% of keys move!
```

---

### MongoDB Sharding

MongoDB has built-in sharding support:

```javascript
// MongoDB shard key selection is critical!
// Shard by userId for user data
db.adminCommand({ shardCollection: 'app.posts', key: { userId: 'hashed' } });

// Bad shard key: timestamps (all writes go to one shard — hotspot!)
// Good shard key: userId with hashed (even distribution)
// Good shard key: compound {userId, createdAt} (good cardinality + ordering)
```

---

## ⚖️ Trade-offs

### Replication Trade-offs

| | Pros | Cons |
|-|------|------|
| Read replicas | Scales read traffic | Replication lag (stale reads) |
| Sync replication | Zero data loss | Slower writes |
| Multi-region replicas | Low latency globally | Higher cost, more complexity |

### Sharding Trade-offs

| | Pros | Cons |
|-|------|------|
| Horizontal scaling | Virtually unlimited | Cannot do cross-shard JOINs |
| Better performance | Each shard has less data | Complex application logic |
| Geographic sharding | Users near their data | Re-sharding is painful |

**Cross-shard queries are a nightmare!**
```sql
-- This is IMPOSSIBLE with sharding (data is on different servers):
SELECT users.name, posts.content 
FROM users JOIN posts ON users.id = posts.user_id
-- users might be on shard1, posts on shard3!

-- Solution: Denormalize (store user info in the posts document/table)
-- OR: Only join within a shard (same user_id → same shard for both)
```

---

## 📊 Scalability Discussion

### AWS Multi-AZ vs Read Replicas

```
AWS RDS Multi-AZ (for availability, not performance):
Primary DB (us-east-1a)
    ↓ Synchronous replication
Standby DB (us-east-1b)
→ Automatic failover in 1-2 minutes if primary fails
→ NOT used for reads — just standby!

AWS RDS Read Replicas (for performance):
Primary DB (us-east-1)
    ↓ Asynchronous replication
Read Replica 1 (us-east-1) ← Local reads
Read Replica 2 (eu-west-1) ← European users read from here!
Read Replica 3 (ap-south-1) ← Asian users read from here!
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is database replication and what problem does it solve?

**Solution:**
Replication is the process of copying and maintaining database data across multiple servers. It solves:
1. **High Availability:** If primary crashes, a replica is promoted automatically (failover)
2. **Read Scalability:** Multiple replicas handle read traffic; primary handles only writes
3. **Geographic Performance:** Put replicas near users (European users read from European replica)
4. **Backup:** Replicas serve as live backups (though not a replacement for proper backups)

In AWS: Use RDS Multi-AZ for availability + Read Replicas for performance. Both together = production-ready setup.

---

### Q2: What is sharding and how does it differ from partitioning?

**Solution:**
- **Partitioning:** Splits data within a SINGLE database server into multiple smaller tables. All data is still on one machine. Good for large tables on one server.
- **Sharding:** Splits data ACROSS multiple database servers. Each shard is a separate database server. Data is truly distributed.

```
Partitioning: One server, multiple tables
  Server1: posts_2022, posts_2023, posts_2024 (all partitions)

Sharding: Multiple servers
  Shard1 (Server1): user IDs 1-1M
  Shard2 (Server2): user IDs 1M-2M
  Shard3 (Server3): user IDs 2M-3M
```

Use partitioning first. Only add sharding when you've outgrown a single server (even a massive one).

---

### Q3: What is consistent hashing and why is it important for sharding?

**Solution:**
**Problem with simple hash sharding:** If you have 3 shards and add a 4th, `userId % 4` gives completely different results than `userId % 3`. You need to move almost ALL data!

**Consistent hashing solution:**
- Arrange shards on a virtual ring (0 to 2^32)
- Hash each user ID to a position on the ring
- User's shard = next shard clockwise from their position
- Adding shard4: Only the data between shard3 and shard4's ring position moves!
- Only ~25% of data moves (not 100%)

Used by: Amazon DynamoDB, Apache Cassandra, Memcached clusters, Redis Cluster.

---

### Q4: How do you handle the "hot shard" problem?

**Solution:**
Hot shard = one shard getting disproportionately more traffic than others.

**Causes:**
- Celebrity users (millions of followers, all traffic goes to their shard)
- Viral content (one post gets 100x normal traffic)
- Poor shard key selection (timestamps → all new data on one shard)

**Solutions:**
1. **Hash-based sharding:** Distribute data more evenly
2. **Separate celebrity data:** Detect hot keys and replicate them more aggressively
3. **Caching:** Redis absorbs traffic spikes before they hit the shard
4. **Sub-sharding:** Split the hot shard into multiple smaller shards
5. **Add random salt to shard key:** `userId + "_" + Math.floor(Math.random() * 10)` → spread across more shards

---

### Q5: What is replication lag and how do you handle it?

**Solution:**
Replication lag = the delay between when data is written to the primary and when it appears on replicas. Usually 1-100ms, but can be seconds during high load.

**Problem scenarios:**
- User posts a comment → write to primary
- User immediately refreshes → reads from replica → comment not there yet!
- User thinks "my comment was lost!" → bad UX

**Solutions:**
1. **Read-your-own-writes:** After a write, read from primary for the same user for 1-2 seconds

```javascript
async function createPost(userId, content) {
  const post = await primaryDB.query('INSERT INTO posts...', [userId, content]);
  
  // Mark user as "recently wrote" in Redis for 5 seconds
  await redis.setex(`user:recent_write:${userId}`, 5, '1');
  
  return post;
}

async function getUserFeed(userId) {
  const recentlyWrote = await redis.get(`user:recent_write:${userId}`);
  const db = recentlyWrote ? primaryDB : replicaDB;
  return db.query('SELECT * FROM posts WHERE user_id = $1', [userId]);
}
```

2. **Monotonic reads:** Same user always reads from same replica (using sticky routing)
3. **Sync replication:** More lag-free but slower writes (use for critical data only)

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design the database architecture for a 100M user social app

**Solution:**
```
Write Path:
Node.js API → Primary PostgreSQL (AWS RDS)
                     ↓ (async replication)
              Read Replica 1 (us-east)
              Read Replica 2 (eu-west)  ← European users
              Read Replica 3 (ap-south) ← Asian users

Read Path:
- User's location → Route 53 → Nearest read replica
- After a write: Read from primary for 2 seconds (avoid replication lag)
- Cache in Redis: Most read data never reaches DB

Sharding (only if > 500M rows in main tables):
- User data: Hash shard by userId across 8 PostgreSQL instances
- Shard key: hash(userId) % 8

Posts/Activity (high write volume → MongoDB):
- MongoDB with native sharding on userId
- Each shard: 3-node replica set (1 primary + 2 secondaries)
- 8 shards × 3 nodes = 24 MongoDB instances for activity data

Avoid cross-shard queries:
- Denormalize: store username + avatar in the posts collection
- Social graph (who follows who): Separate service with graph DB or Redis sets
```

---

### Problem 2: Instagram says their DB replication is causing users to see stale feeds. How do you fix it?

**Solution:**
1. **Root cause:** Posts are written to primary, but feed is read from replica before replication catches up.
2. **Immediate fix:** For the 1 second after posting, read the feed from primary for that user
3. **Better fix:** Separate the "my new posts" from the "social feed":
   - "My new post" → read from primary (guaranteed fresh)
   - "Social feed" → read from replica (slightly stale, acceptable — your friend's post from 2s ago is fine)
4. **Architectural fix:** Use an event-driven feed system:
   - User posts → writes to primary DB
   - A background worker reads the new post and pushes it to Redis lists of all followers
   - Followers' feeds are pre-computed in Redis, not read from DB replica
   - Redis is always consistent (no replication lag for feed reads)

---

### Navigation
**Prev:** [08_Indexing_and_Partitioning.md](08_Indexing_and_Partitioning.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [10_CAP_Theorem.md](10_CAP_Theorem.md)
