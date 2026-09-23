# Database Sharding & Partitioning

> 📌 **File:** `23_Sharding_And_Partitioning.md` | **Level:** Expert → MERN Developer

---

## What is it?

When your application scales from thousands of records to tens or hundreds of millions of rows, a single database table begins to hit severe physical bottlenecks:
* B+Tree indexes grow too large to fit in memory (RAM), forcing frequent slow disk I/O reads.
* Maintenance tasks (like backups, index rebuilds, and `ALTER TABLE` schema changes) take hours or days.
* Read and write throughput saturates CPU, connection limits, and disk I/O operations per second (IOPS).

To solve these scalability challenges, database engineering relies on two distinct scaling techniques:
1. **Database Partitioning (Local Scaling):** Splitting a massive table into smaller, self-contained physical storage chunks **within the same single database server**.
2. **Database Sharding (Distributed Scaling):** Splitting a dataset horizontally across **multiple independent physical database servers** (instances).

---

## MERN Parallel — You Already Know This!

If you have worked with MongoDB at scale, you already understand these concepts conceptually:

| MongoDB (NoSQL) | SQL (MySQL/PostgreSQL) | Scale Level | Description |
| :--- | :--- | :--- | :--- |
| Single collection on one server | Standard Table | Single Node | Holds all records in a single physical file/tablespace. |
| (Not natively standard on single node) | `PARTITION BY RANGE / LIST / HASH` | Single Node (Partitioning) | Splits a table into smaller disk files inside the same MySQL instance. |
| **Sharded Cluster** (`mongos` + Config Servers + Shards) | **Database Sharding** (Vitess / Citus / App Routing) | Multi-Node (Distributed) | Distributes chunks of tables across independent physical database servers. |
| **Shard Key** (e.g. `{ tenantId: 1, _id: 1 }`) | **Shard Key / Partition Key** | Routing Key | The column chosen to determine where each row lives. |
| Scatter-Gather aggregation | Distributed Query Engine | Multi-Node Query | Queries sent to all shards and merged in memory. |

---

## Why does it matter?

* **Breaking the Vertical Scaling Ceiling:** You can only upgrade CPU and RAM on a single machine up to physical hardware and budget limits. Sharding enables near-infinite horizontal scaling with commodity servers.
* **Query Speedup via Partition Pruning:** Instead of scanning a 100-million-row table, the query engine scans only a 1-million-row partition, executing in milliseconds.
* **Instant Data Archiving / Deletion:** Dropping an old partition (`ALTER TABLE orders DROP PARTITION p_2020;`) takes milliseconds and uses zero transaction log overhead, unlike `DELETE FROM orders WHERE order_date < '2021-01-01'`, which locks rows, bloats Undo logs, and takes hours.
* **High Availability & Fault Isolation:** If one shard in a 10-shard cluster experiences hardware failure, $90\%$ of your users remain completely unaffected.

---

## How does it work?

---

### 🗂️ 1. Database Partitioning (Single Server)

Partitioning splits a table into smaller physical segments while presenting a **single logical table** to your application. Your SQL queries still say `SELECT * FROM orders`, but the database engine routes queries to specific partition files under the hood.

```
Logical Table View (What your API sees):
┌──────────────────────────────────────────────────────────┐
│                      orders table                        │
└──────────────────────────────────────────────────────────┘
                            │
              Under-The-Hood Physical Storage
    ┌───────────────────────┼───────────────────────┐
    ▼                       ▼                       ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ Partition: 2023 │   │ Partition: 2024 │   │ Partition: 2025 │
│ orders_2023.ibd │   │ orders_2024.ibd │   │ orders_2025.ibd │
└─────────────────┘   └─────────────────┘   └─────────────────┘
```

#### Types of Horizontal Partitioning

1. **Range Partitioning:** Rows are assigned to partitions based on column values falling within specified contiguous ranges. Ideal for time-series and date-based datasets.
2. **List Partitioning:** Rows are assigned based on explicit discrete values matching a predefined list (e.g., country codes `'IN'`, `'US'`, `'UK'`).
3. **Hash Partitioning:** The database calculates a hash function on a column (`MOD(expr, N)`) to distribute rows evenly across $N$ partitions.
4. **Key Partitioning:** Similar to Hash, but MySQL uses its internal hashing algorithm based on the primary key.
5. **Subpartitioning (Composite Partitioning):** Splits range/list partitions further into subpartitions using Hash or Key (e.g., Range by Year $\rightarrow$ Hash by `user_id`).

#### ⚡ Under-the-Hood: Partition Pruning

The core performance superpower of partitioning is **Partition Pruning**. 

When an incoming query contains the partition key in its `WHERE` clause:
```sql
SELECT * FROM orders WHERE order_date = '2024-06-15';
```
The MySQL Cost-Based Optimizer inspects the table metadata, determines that this date falls exclusively into partition `p_2024`, and **completely skips reading the disk files** for `p_2023`, `p_2025`, and `p_future`.

You can verify partition pruning using `EXPLAIN`:
```sql
EXPLAIN SELECT * FROM orders WHERE order_date = '2024-06-15';
-- Look at the 'partitions' column: it will show 'p_2024' instead of all partitions.
```

#### ⚠️ Critical Partitioning Rule: The Primary Key Constraint
In MySQL InnoDB, **every unique index and primary key on a partitioned table MUST contain every column used in the partitioning expression**.
* If your partition key is `order_date`, your primary key cannot be just `id INT`. It **must** be a composite key: `PRIMARY KEY (id, order_date)`.
* *Why?* To enforce uniqueness on `id` without checking every single partition file on every insert (which would destroy write performance), the engine requires the partition key in the index so it only needs to check the local partition.

#### Vertical Partitioning (Column Splitting)
Vertical partitioning involves splitting columns into separate tables with a 1-to-1 relationship:
* **Hot Table:** High-frequency, small columns (`id`, `email`, `password_hash`, `status`) $\rightarrow$ fits in InnoDB Buffer Pool (RAM) for ultra-fast queries.
* **Cold Table:** Large, rarely queried columns (`user_id`, `bio`, `profile_picture_blob`, `raw_payload_json`) $\rightarrow$ stored separately on disk and loaded only when requested.

---

### 🌐 2. Database Sharding (Multiple Servers)

Sharding is horizontal partitioning **spread across multiple separate database servers**. Each database server (a **shard**) holds a unique subset of the total rows.

```
                         ┌─────────────────────────────┐
                         │      Node.js Express API    │
                         └──────────────┬──────────────┘
                                        │
                         ┌──────────────▼──────────────┐
                         │   Routing Layer / Gateway   │
                         │    (e.g., Vitess / Proxy)   │
                         └──────┬───────┬───────┬──────┘
                                │       │       │
             ┌──────────────────┘       │       └──────────────────┐
             ▼                          ▼                          ▼
     ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
     │   Shard 1    │           │   Shard 2    │           │   Shard 3    │
     │  (Server A)  │           │  (Server B)  │           │  (Server C)  │
     │ Users 1–10M  │           │ Users 11–20M │           │ Users 21–30M │
     └──────────────┘           └──────────────┘           └──────────────┘
```

#### Architectural Approaches for SQL Sharding

1. **Application-Level Sharding:** The application code (e.g., Express middleware) inspects the query parameter (e.g., `req.user.tenant_id`), calculates the target shard, and selects the corresponding database connection pool.
   * *Pros:* Simple to start, no extra infrastructure.
   * *Cons:* Application code becomes complex; schema migrations must be run across all shards manually.
2. **Proxy / Middleware-Level Sharding:** A transparent proxy layer (e.g., **Vitess** for MySQL, **Citus** for PostgreSQL, **ProxySQL**) sits between your API and the database nodes.
   * *Pros:* Application writes standard SQL queries; the proxy handles routing, rebalancing, and scatter-gather queries.
   * *Cons:* Additional operational infrastructure and maintenance.

#### Shard Key Distribution Strategies

| Strategy | How it works | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Hash-Based** | `shard = hash(user_id) % num_shards` | Uniform, even data distribution across shards. | Adding new shards requires re-hashing and rebalancing data. |
| **Range-Based** | IDs 1–10M $\rightarrow$ Shard 1; IDs 10M–20M $\rightarrow$ Shard 2 | Simple routing, easy to add new shards. | Hotspots: New active users hit only the newest shard. |
| **Directory / Lookup** | Lookup table maps `tenant_id` $\rightarrow$ `shard_ip` | Flexible; can move big enterprise tenants to dedicated shards. | Lookup table is a single point of failure and adds latency. |

#### Consistent Hashing Ring
To avoid mass data redistribution when scaling from $N$ to $N+1$ shards, production systems use a **Consistent Hashing Ring**:
* Both database shards and shard keys are hashed onto a circular $360^\circ$ ring ($0$ to $2^{32}-1$).
* A record is stored on the first shard node encountered moving clockwise on the ring.
* Adding a new shard node only requires moving a fraction ($1/N$) of the data from its immediate neighbor.

```
Consistent Hashing Ring:
                  [Shard 1] (0°)
                 /              \
                /                \
      [Key A]  /                  \  [Key B]
              |                    |
   [Shard 3]  |                    |  [Shard 2] (120°)
    (240°)    \                  /
               \                /
                 \            /
```

---

## The Great Engineering Challenges of Sharding

Sharding is considered a **last resort** for database architecture because it breaks fundamental relational guarantees:

### 1. Cross-Shard JOINs
You cannot execute a native SQL `JOIN` between tables stored on two different physical database servers.
* *Solution:* 
  * Denormalize shared data (e.g., replicate the small `roles` or `categories` lookup table across all shards).
  * Execute two queries in Node.js and merge results in application memory (**Scatter-Gather**).

### 2. Distributed Unique ID Generation
Standard `AUTO_INCREMENT` produces duplicate IDs on different shards (e.g., Shard 1 creates `id=1`, Shard 2 creates `id=1`).
* *Solutions:*
  * **UUIDv7:** 128-bit time-ordered UUIDs that prevent B+Tree index fragmentation while guaranteeing global uniqueness without central coordination.
  * **Snowflake IDs (Twitter):** 64-bit integers composed of: `Timestamp (41 bits) + Node/Shard ID (10 bits) + Sequence (12 bits)`.

### 3. Distributed Transactions (ACID across Shards)
When an operation mutates records on multiple shards (e.g., transferring funds from User on Shard A to User on Shard B), you cannot use a single `START TRANSACTION; COMMIT;`.
* **Two-Phase Commit (2PC):** A coordinator asks all shards to prepare (`Phase 1`), then instructs all to commit (`Phase 2`). Very slow due to blocking locks and network round trips.
* **Saga Pattern (Eventual Consistency):** Series of local transactions coordinated via message queues (RabbitMQ / Kafka) with compensating transactions (rollbacks) if a subsequent step fails.

---

## Visual Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│               SHARDING QUERY ROUTING & SCATTER-GATHER FLOW              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. Single-Shard Query (Fast Direct Route via Shard Key: user_id = 42): │
│     API Request ──▶ Hash(42) % 3 = Shard 2 ──▶ [Shard 2 Database]       │
│                                                                         │
│  2. Cross-Shard Scatter-Gather Query (e.g., SELECT * WHERE status='vip'):│
│     API Request ──▶ Gateway Router                                      │
│                           ├─── Dispatch Query ──▶ [Shard 1] (Returns 2) │
│                           ├─── Dispatch Query ──▶ [Shard 2] (Returns 5) │
│                           └─── Dispatch Query ──▶ [Shard 3] (Returns 1) │
│                                                          │              │
│                     Gateway Merges & Sorts (8 rows) ◀────┘              │
│                           │                                             │
│                     Returns to Client                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Syntax & Practical SQL

### 1. Range Partitioning by Year
```sql
CREATE TABLE orders_partitioned (
    id BIGINT NOT NULL,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
    -- Partition key MUST be in the Primary Key:
    PRIMARY KEY (id, order_date)
)
PARTITION BY RANGE (YEAR(order_date)) (
    PARTITION p_2023 VALUES LESS THAN (2024),
    PARTITION p_2024 VALUES LESS THAN (2025),
    PARTITION p_2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### 2. List Partitioning by Region
```sql
CREATE TABLE customers_regional (
    id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    country_code VARCHAR(3) NOT NULL,
    region_id INT NOT NULL,
    PRIMARY KEY (id, region_id)
)
PARTITION BY LIST (region_id) (
    PARTITION p_north_america VALUES IN (1, 2),   -- 1: USA, 2: Canada
    PARTITION p_europe VALUES IN (10, 11, 12),     -- 10: UK, 11: Germany, 12: France
    PARTITION p_asia_pacific VALUES IN (20, 21)    -- 20: India, 21: Japan
);
```

### 3. Hash & Composite Subpartitioning
```sql
CREATE TABLE user_logs (
    id BIGINT NOT NULL,
    user_id INT NOT NULL,
    log_date DATE NOT NULL,
    message TEXT,
    PRIMARY KEY (id, log_date, user_id)
)
PARTITION BY RANGE (YEAR(log_date))
SUBPARTITION BY HASH (user_id)
SUBPARTITIONS 4 (
    PARTITION p_2024 VALUES LESS THAN (2025),
    PARTITION p_2025 VALUES LESS THAN (2026)
);
```

### 4. Partition Maintenance Operations
```sql
-- View partition status and row distributions
SELECT 
    table_name, partition_name, table_rows, data_length, index_length 
FROM information_schema.partitions 
WHERE table_name = 'orders_partitioned';

-- Add a new partition for the coming year
ALTER TABLE orders_partitioned 
ADD PARTITION (PARTITION p_2026 VALUES LESS THAN (2027));

-- Drop old archived partition (instantly reclaims disk space)
ALTER TABLE orders_partitioned 
DROP PARTITION p_2023;

-- Truncate a single partition (empties data without changing structure)
ALTER TABLE orders_partitioned 
TRUNCATE PARTITION p_2024;
```

---

## MERN vs SQL — Side-by-Side Code

### MongoDB Native Sharding vs MySQL Partitioning Query

```javascript
// ============================================
// MongoDB (MERN): Sharded Collection Query
// ============================================
// In MongoDB, the mongos router directs this query
// to the exact shard based on the shard key { tenantId: 'tenant_123' }
const orders = await Order.find({ 
  tenantId: 'tenant_123', 
  createdAt: { $gte: new Date('2024-01-01') } 
});
```

```sql
-- ============================================
-- MySQL: Partition-Pruned SQL Query
-- ============================================
-- The MySQL Query Optimizer analyzes the WHERE clause,
-- accesses ONLY the 'p_2024' partition file, and ignores others.
SELECT * FROM orders_partitioned 
WHERE order_date >= '2024-01-01' AND order_date < '2024-02-01';
```

---

## ORM Equivalent (Sequelize / Raw Migrations)

Because partitioning is a database storage engine configuration, standard ORM schema sync tools do not generate `PARTITION BY` syntax automatically. In production, you define partitioned tables using raw SQL migrations:

```javascript
// database/migrations/20260101-create-partitioned-orders.js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.sequelize.query(`
      CREATE TABLE orders_partitioned (
        id BIGINT NOT NULL,
        order_date DATE NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        PRIMARY KEY (id, order_date)
      )
      PARTITION BY RANGE (YEAR(order_date)) (
        PARTITION p_2024 VALUES LESS THAN (2025),
        PARTITION p_2025 VALUES LESS THAN (2026),
        PARTITION p_max VALUES LESS THAN MAXVALUE
      );
    `);
  },
  down: async (queryInterface, Sequelize) => {
    await queryInterface.dropTable('orders_partitioned');
  }
};
```

---

## Real-World Scenario + Full Stack Code

### Application-Level Sharding Router in Node.js (Express + mysql2)

Below is a production-ready application-level sharding implementation where tenants are routed to dedicated shard database pools based on consistent hashing of their `tenant_id`.

```javascript
// server.js
const express = require('express');
const mysql = require('mysql2/promise');
const crypto = require('crypto');

const app = express();
app.use(express.json());

// 1. Configure Connection Pools for Multiple Shards
const shards = [
  { id: 'shard_0', pool: mysql.createPool({ host: 'db-shard-0.internal', user: 'app', password: 'secret', database: 'tenant_db', connectionLimit: 10 }) },
  { id: 'shard_1', pool: mysql.createPool({ host: 'db-shard-1.internal', user: 'app', password: 'secret', database: 'tenant_db', connectionLimit: 10 }) },
  { id: 'shard_2', pool: mysql.createPool({ host: 'db-shard-2.internal', user: 'app', password: 'secret', database: 'tenant_db', connectionLimit: 10 }) }
];

// 2. Consistent Shard Router Function
function getShardForTenant(tenantId) {
  // Compute deterministic hash of tenantId
  const hash = crypto.createHash('md5').update(tenantId.toString()).digest('hex');
  const numericVal = parseInt(hash.substring(0, 8), 16);
  const shardIndex = numericVal % shards.length;
  return shards[shardIndex];
}

// 3. Shard-Aware Middleware
function routeTenant(req, res, next) {
  const tenantId = req.headers['x-tenant-id'] || req.body.tenant_id || req.query.tenant_id;
  if (!tenantId) {
    return res.status(400).json({ error: 'Missing x-tenant-id header' });
  }
  const targetShard = getShardForTenant(tenantId);
  req.shard = targetShard;
  req.tenantId = tenantId;
  next();
}

// 4. API Route: Create Order on Target Shard
app.post('/api/orders', routeTenant, async (req, res) => {
  const { amount, customerName } = req.body;
  const orderId = Date.now(); // In production, use Snowflake ID or UUIDv7

  try {
    const [result] = await req.shard.pool.query(
      'INSERT INTO orders (id, tenant_id, amount, customer_name, created_at) VALUES (?, ?, ?, ?, NOW())',
      [orderId, req.tenantId, amount, customerName]
    );

    res.status(201).json({
      success: true,
      orderId,
      shard: req.shard.id,
      affectedRows: result.affectedRows
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 5. Cross-Shard Scatter-Gather Route: Aggregate Admin Analytics
app.get('/api/admin/total-revenue', async (req, res) => {
  try {
    // Scatter query to all shards simultaneously
    const shardPromises = shards.map(async (shard) => {
      const [rows] = await shard.pool.query('SELECT SUM(amount) AS shard_revenue FROM orders');
      return { shard: shard.id, revenue: Number(rows[0].shard_revenue) || 0 };
    });

    const results = await Promise.all(shardPromises);
    
    // Gather and merge results in Node.js memory
    const totalCompanyRevenue = results.reduce((acc, curr) => acc + curr.revenue, 0);

    res.json({
      totalRevenue: totalCompanyRevenue,
      shardBreakdown: results
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(5000, () => console.log('Sharded API Server running on port 5000'));
```

---

## Impact

| Architecture Decision | What Happens |
| :--- | :--- |
| **Partitioning without partition key in Primary Key** | Table creation fails with error `A PRIMARY KEY must include all columns in the table's partitioning function`. |
| **Querying partitioned table without partition key in WHERE** | MySQL scans ALL partitions, resulting in slower execution than an unpartitioned table due to file metadata overhead. |
| **Sharding prematurely on Day 1** | Massive engineering overhead, broken JOINs, complex transactions, and wasted developer time before hitting hardware limits. |
| **Bad Shard Key selection (e.g. status or region)** | Hotspot shards where one node takes $90\%$ of traffic and crashes while other nodes sit idle. |
| **Using `DELETE` instead of `DROP PARTITION` for log purging** | High disk I/O, heavy table locking, Undo log growth, and table fragmentation. |

---

## Real-World Q&A

### ❓ Q1: When should I choose Single-Server Partitioning vs Multi-Server Sharding?
> **💡 Answer:** 
> * Choose **Partitioning** when your data fits on a single server's disk, but individual tables are becoming too large ($>50\text{M}$ rows), index scans are slowing down, or you need instant data lifecycle purging (e.g. dropping logs older than 90 days).
> * Choose **Sharding** only when a single server has exhausted maximum vertical CPU, RAM, or disk IOPS capacity, or when write traffic exceeds what one master database node can physically process.

### ❓ Q2: What is the difference between Partition Pruning and Index Scanning?
> **💡 Answer:**
> * **Partition Pruning** happens at the storage engine file level before reading index trees. It eliminates entire partition disk files from being opened.
> * **Index Scanning** happens inside the chosen partition file by traversing B+Tree pages. Partition pruning and indexes complement each other: pruning narrows the scan to one file, and indexes locate specific rows within that file.

### ❓ Q3: How do you handle schema migrations across 50 sharded databases?
> **💡 Answer:** Use an automated migration orchestrator (like Liquibase, Flyway, or custom CI/CD scripts) that runs migrations sequentially or in parallel batches across all shard connection strings. In Kubernetes environments, tools like **Vitess** handle schema migrations (VSchema) declaratively without requiring manual multi-database scripts.

---

## Interview Q&A

### ❓ Q1: What is Partition Pruning and how do you verify it?
> **💡 Answer:** Partition pruning is an optimization where the database engine reads only the partitions containing data relevant to the query `WHERE` filter and skips all other partition files. You verify it by running `EXPLAIN SELECT ...` and inspecting the `partitions` column in the output table.

### ❓ Q2: What is the primary key requirement for partitioned tables in MySQL InnoDB?
> **💡 Answer:** Every unique constraint and primary key on a partitioned table must include all columns used in the partitioning expression. This allows InnoDB to enforce uniqueness locally within a single partition without having to scan all other partitions during an `INSERT`.

### ❓ Q3: What is a Shard Key and what makes a good vs bad Shard Key?
> **💡 Answer:** A Shard Key is the attribute used by the routing logic to determine which database node holds a given record.
> * **Good Shard Key:** High cardinality, uniform distribution (e.g., `user_id` or `uuid`), and present in majority of queries to avoid cross-shard scatter-gather queries.
> * **Bad Shard Key:** Low cardinality (e.g., `country` or `status`), leading to data skew and hotspots where one shard receives almost all traffic.

### ❓ Q4: How do you resolve distributed transactions across shards without using slow 2-Phase Commit (2PC)?
> **💡 Answer:** Modern microservices use the **Saga Pattern** with asynchronous message queues. Instead of locking multiple databases simultaneously, each shard executes its local transaction and publishes an event. If a subsequent step fails, compensating transactions are triggered to revert previous actions, achieving **Eventual Consistency**.

---

| [← Previous Topic: Deployment On EC2](./22_Deployment_On_EC2.md) | [Index](./00_index.md) | [Next: CTEs & Recursive Queries →](./24_CTEs_And_Recursive_Queries.md) |
