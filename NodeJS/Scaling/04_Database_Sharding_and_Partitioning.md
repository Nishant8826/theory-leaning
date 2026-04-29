# 📌 04 — Database Sharding and Partitioning: Handling Massive Datasets

## 🧠 Concept Explanation

### Basic → Intermediate
- **Partitioning**: Breaking a large table into smaller, more manageable pieces within the same database instance.
- **Sharding**: Distributing data across multiple completely independent database servers (Shards).

### Advanced → Expert
At a staff level, sharding is the **Last Resort** for scaling. It adds massive complexity to the application layer.
1. **Vertical Partitioning**: Splitting a table by columns (e.g. move a large `bio` text field to a separate `UserProfiles` table).
2. **Horizontal Partitioning (Sharding)**: Splitting a table by rows based on a **Sharding Key** (e.g. users with IDs 1-1M go to Shard A, 1M-2M go to Shard B).

The choice of Sharding Key is critical. A bad key leads to "Hot Shards" (one server doing all the work) and makes **Cross-Shard Queries** almost impossible.

---

## 🏗️ Common Mental Model
"I'll just shard by `region_id`."
**Correction**: If 90% of your users are in the `US-East` region, Shard A will be at 100% load while the others are idle. You should use a key that provides a **Uniform Distribution**, like a Hash of the `UserId`.

---

## ⚡ Actual Behavior: The Join Problem
Once you shard your data, you **lose the ability to perform SQL JOINs** across shards. If you need to join a `User` (on Shard A) with their `Orders` (on Shard B), you must perform the join in your **Node.js application code**, which is much slower and memory-intensive.

---

## 🔬 Internal Mechanics (Distributed Data)

### Consistent Hashing
A technique used to minimize the amount of data that needs to be moved when you add a new shard to the cluster.

### Global ID Generation
In a sharded system, you cannot use auto-incrementing integers for IDs (because Shard A and Shard B would both produce ID `1`). You must use **UUIDs** or a **Global ID Service** (like Twitter Snowflake).

---

## 📐 ASCII Diagrams

### Sharding by Hash
```text
  INCOMING DATA: [ User 42 ] ──▶ [ HASH(42) ] ──▶ [ Result: 1 ]
                                      │
       ┌──────────────────────────────┴─────────────┐
       ▼                                            ▼
  [ SHARD 1 ]                                  [ SHARD 2 ]
  (IDs: 0, 2, 4...)                            (IDs: 1, 3, 5...)
```

---

## 🔍 Code Example: Simple Application-Level Sharding
```javascript
const shards = [
  new Client('postgres://shard-1'),
  new Client('postgres://shard-2')
];

async function getClientForUser(userId) {
  // Simple modulo sharding
  const shardIndex = userId % shards.length;
  return shards[shardIndex];
}

async function getUser(userId) {
  const client = await getClientForUser(userId);
  return await client.query('SELECT * FROM users WHERE id = $1', [userId]);
}
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Hot" Shard
**Problem**: Shard 5 is constantly at 100% CPU, while the others are at 5%.
**Reason**: Your sharding key was `created_at` (month). All new signups are hitting the "Current Month" shard.
**Fix**: Re-shard using a non-sequential key like `user_id` or `uuid`.

### Scenario: The Cross-Shard Aggregation
**Problem**: A request to "List the top 10 richest users across the whole system" takes 30 seconds.
**Reason**: Node.js has to query every single shard, download the data, and sort it in memory.
**Fix**: Use a **Data Warehouse** (BigQuery/Snowflake) for analytical queries, or maintain a separate "Leaderboard" table in a centralized Redis.

---

## 🧪 Real-time Production Q&A

**Q: "Should I use Citus (Postgres) or Vitess (MySQL)?"**
**A**: **Yes.** These are "Sharding Middlewares." They handle the complexity of sharding and cross-shard queries for you, so your Node.js app can treat the cluster like a single massive database.

---

## 🏢 Industry Best Practices
- **Don't Shard until you have to**: Most apps can get very far with a single large Primary and multiple Read Replicas.
- **Fixed Number of Logical Shards**: Start with a large number of logical partitions (e.g. 1024) and map them to physical servers. This makes adding servers easier later.

---

## 💼 Interview Questions
**Q: What is a "Sharding Key" and how do you choose one?**
**A**: A sharding key is the column used to determine which shard a row belongs to. A good key should have **High Cardinality** (many unique values) and **Even Distribution** (data is spread equally across shards).

---

## 🧩 Practice Problems
1. Implement a consistent hashing algorithm in Node.js that maps 1000 IDs to 3 virtual nodes.
2. Design a schema for a "Twitter-like" system where tweets are sharded by `userId` to ensure a user's timeline can be fetched from a single shard.

---

**Prev:** [03_Caching_at_the_Edge_CDN.md](./03_Caching_at_the_Edge_CDN.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [05_Auto_Scaling_Groups.md](./05_Auto_Scaling_Groups.md)
