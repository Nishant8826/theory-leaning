# Database Sharding & Partitioning

> 📌 **File:** `23_Sharding_And_Partitioning.md` | **Level:** Expert → MERN Developer

---

## What is it?

When your application scales and your database grows from thousands of rows to hundreds of millions, a single database table starts slowing down queries, indexes become too large to fit in RAM, and disk reads bottleneck.

To solve this, database scaling relies on two core techniques for breaking massive datasets into smaller, faster-to-query chunks:
1. **Partitioning (Local):** Splitting a table into smaller logical subsets *within a single database server*.
2. **Sharding (Distributed):** Splitting a table across *multiple separate database servers* (instances).

---

## MERN Parallel — You Already Know This!

You've likely used MongoDB's native scaling mechanisms. Here is how they translate to SQL:

| MongoDB (NoSQL) | SQL (MySQL/PostgreSQL) | Scale Type | Description |
| :--- | :--- | :--- | :--- |
| Single collection on one server | Standard Table | Local | Holds all records in a single physical structure. |
| (Not natively common on a single node) | `PARTITION BY` | Local (Vertical/Horizontal) | Splits a table into sub-tables inside the *same* database instance. |
| **Sharded Cluster** (`mongos` + Config Servers + Shards) | **Database Sharding** (Vitess / Citus / App Routing) | Distributed (Horizontal) | Distributes chunks of a table across *multiple database machines*. |

---

## Why does it matter?

* **Limits of Vertical Scaling:** You can only scale a single database server (add RAM/CPU) so far before hardware becomes prohibitively expensive or hits physical limits.
* **Faster Queries:** Searching through a partition of 500,000 records is significantly faster than searching a table of 50,000,000 records.
* **Cost Efficiency:** Sharding allows you to run your database on many smaller, cheaper commodity servers instead of one ultra-expensive supercomputer.
* **Archiving Data:** If your table is partitioned by date, you can delete years of historical logs instantly by dropping a single partition instead of running a slow `DELETE FROM table WHERE date < ...` query that locks rows.

---

## How does it work?

---

### 🗂️ 1. Database Partitioning (Single Server)

Partitioning splits a table logically or physically, but **keeps all data on the same server**. 

```
Single Table (Unpartitioned):
┌───────────────────────────────────────────────┐
│ [All Orders (2023, 2024, 2025)]              │
└───────────────────────────────────────────────┘

Partitioned Table:
┌─────────────────┬─────────────────┬───────────┐
│ Partition 2023  │ Partition 2024  │ Future... │
│ [Orders 2023]   │ [Orders 2024]   │ [2025+]   │
└─────────────────┴─────────────────┴───────────┘
```

#### A. Horizontal Partitioning
Splits rows of a table based on a column condition. This is natively supported by MySQL and PostgreSQL.

##### SQL Example: Range Partitioning by Year
```sql
CREATE TABLE orders (
    id INT,
    order_date DATE NOT NULL,
    amount DECIMAL(10,2),
    PRIMARY KEY (id, order_date) -- The partition key must be part of the primary key
)
PARTITION BY RANGE (YEAR(order_date)) (
    PARTITION p_2023 VALUES LESS THAN (2024),
    PARTITION p_2024 VALUES LESS THAN (2025),
    PARTITION p_2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

##### ⚡ Under-the-Hood: Partition Pruning
When you run a query filtering by the partition key:
```sql
SELECT * FROM orders WHERE order_date = '2024-05-15';
```
The database engine performs **Partition Pruning**. It skips checking `p_2023`, `p_2025`, and `p_future` entirely. It reads *only* the `p_2024` data file, making the query extremely fast.

#### B. Vertical Partitioning
Splits columns of a table into separate tables. You do this when a table has some columns that are queried constantly (e.g., `username`, `password_hash`) and other columns that are large but rarely queried (e.g., a large `profile_picture_blob` or `user_bio_text`).

```
Vertical Partitioning Example:
Original table: [ id | username | password | bio | profile_picture_blob ]
  ├── Table 1:  [ id | username | password ]  <-- Fits entirely in RAM (Fast reads)
  └── Table 2:  [ id | bio | profile_picture_blob ] <-- Kept separate on disk
```

---

### 🌐 2. Database Sharding (Multiple Servers)

Sharding is horizontal partitioning **spread across multiple physical machines**. 

Unlike MongoDB (which handles sharding natively via `mongos` routers), standard relational engines (MySQL/PostgreSQL) do not scale horizontally out-of-the-box. To shard SQL, you must use one of two architectures:

```
App-Level Sharding:
┌────────────────────────────────┐
│   Node.js / Express Client     │
│   (Checks: user_id % 3)        │
└────┬──────────────┬────────────┬┘
     │ (0)          │ (1)        │ (2)
     ▼              ▼            ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Shard A  │   │ Shard B  │   │ Shard C  │
└──────────┘   └──────────┘   └──────────┘

Middleware-Level Sharding:
┌────────────────────────────────┐
│   Node.js / Express Client     │
└──────────────┬─────────────────┘
               │ (Direct SQL Connection)
               ▼
┌────────────────────────────────┐
│  Sharding Proxy / Middleware   │
│  (e.g., Vitess for MySQL)      │
└────┬──────────────┬────────────┬┘
     ▼              ▼            ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Shard A  │   │ Shard B  │   │ Shard C  │
└──────────┘   └──────────┘   └──────────┘
```

#### The Shard Key
To query or insert data, you must know which machine holds that data. You determine this using a **Shard Key** (e.g., `user_id` or `tenant_id`).

1. **Hash-Based Sharding:** The database computes a hash of the shard key modulo the number of shards:
   `target_shard = hash(user_id) % number_of_shards`
   * *Benefit:* Even distribution of data across all databases.
   * *Drawback:* Adding a new shard requires redistributing almost all data.
2. **Range-Based Sharding:** Data is distributed by ranges of values (e.g., Shard 1 holds IDs 1-1,000,000; Shard 2 holds 1,000,001-2,000,000).
   * *Benefit:* Easy to add new shards.
   * *Drawback:* Can lead to hot spots (if newer IDs are updated and queried more frequently, one server takes all the load).

---

## The Great Challenges of Sharding

Sharding is complex and is considered a **last resort** for database scaling. It breaks many guarantees of relational databases:

### 1. Cross-Shard JOINs (Broken Relationships)
You cannot perform a native SQL `JOIN` between tables residing on different servers.
* *Example:* If you join a `users` table on Shard A with an `orders` table on Shard B, the join will fail.
* *Workaround:* The application must make two separate database queries and merge the datasets in Node.js memory (very slow), or you must duplicate (denormalize) some data across all shards.

### 2. Distributed Transactions (Broken ACID)
Executing transactions across multiple servers requires a **Two-Phase Commit (2PC)** protocol.
* *Scenario:* You want to update an inventory count on Shard A and create a payment log on Shard B. If Shard B goes down mid-transaction, you must roll back Shard A.
* *Impact:* Managing this slows down write performance and increases network lag significantly.

### 3. Rebalancing Data
If Shard A becomes full ($90\%$) but Shard B is empty ($10\%$), moving records from Shard A to Shard B over a live network without causing application downtime is a massive, complex engineering operation.

---

## Common Pitfalls & Gotchas

* **Partitioning Keys constraint:** In relational databases (like MySQL), **every unique key on the table (including the Primary Key) must include the partition column**. If your primary key is just `id`, you cannot partition by `order_date` unless your primary key is changed to a composite key `(id, order_date)`.
* **The Hotspot Shard:** If you shard by `tenant_id` (company ID), and Company X has 10 million users while Company Y has 10 users, the shard holding Company X will crash under heavy I/O load. Choosing the right shard key is critical.
* **Premature Sharding:** Do not shard your database on day 1. Indexing, caching (Redis), replica databases (Read Replicas), and single-server partitioning can support your application up to millions of users before sharding is required.
