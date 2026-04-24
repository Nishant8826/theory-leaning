# 📌 Indexing and Partitioning

## 🧠 Concept Explanation (Story Format)

**Indexing:** Imagine a book with 1000 pages. You want to find all mentions of "Redis". Without an index (table of contents), you read every page — 1000 pages read. With an index at the back → jump directly to pages 45, 200, 670. Done in seconds.

Database indexing works the same way. Without an index on `email`, finding a user means scanning EVERY row. With an index → jump directly to the right row.

**Partitioning:** Your restaurant has grown to 50 tables. Instead of one big chaotic seating chart, you split the restaurant into zones: Zone A (parties of 1-4), Zone B (parties of 5-10). Now the host finds tables faster because they only search the relevant zone.

Partitioning splits your huge database table into smaller, more manageable pieces (partitions). Each partition is like a separate mini-table.

---

## 🏗️ Basic Design (Naive)

```
posts table: 500 million rows
---------------------------------
id | user_id | content | created_at
---------------------------------
1  | 123     | "..."   | 2020-01-01
2  | 456     | "..."   | 2020-01-02
... (500 million more rows)

Query: SELECT * FROM posts WHERE user_id = 123 ORDER BY created_at DESC LIMIT 20;

Result: PostgreSQL scans all 500 million rows → VERY SLOW (minutes!)
```

---

## ⚡ Optimized Design

```
With Index:
B-tree index on (user_id, created_at):
→ Jump directly to user 123's rows → milliseconds!

With Partitioning:
posts_2022 | posts_2023 | posts_2024 | posts_2025
Each partition: ~100M rows (instead of 500M)
Query only searches relevant partition → even faster!

Architecture:
[Node.js Query]
    ↓
[PostgreSQL Query Planner]
    ↓ (uses index to skip rows)
[B-tree Index on user_id, created_at]
    ↓ (partition pruning — only searches 2024 partition)
[posts_2024 partition]
    ↓
Returns 20 rows in milliseconds!
```

---

## 🔍 Key Components

### Types of Indexes

**B-tree Index (Default)**
```sql
-- Good for: equality, range queries, sorting
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);

-- Queries that USE this index:
SELECT * FROM posts WHERE user_id = 123;                          -- ✅
SELECT * FROM posts WHERE user_id = 123 AND created_at > '2024-01-01'; -- ✅
SELECT * FROM posts WHERE user_id = 123 ORDER BY created_at DESC; -- ✅

-- Queries that DON'T use it:
SELECT * FROM posts WHERE content = 'hello';  -- ❌ content not indexed
```

**Hash Index**
```sql
-- Good for: ONLY equality checks (not range!)
CREATE INDEX idx_users_email_hash ON users USING HASH(email);

-- Fast for: WHERE email = 'alice@example.com'
-- NOT for: WHERE email LIKE 'alice%'
```

**GIN Index (Full-Text Search)**
```sql
-- Good for: full-text search, array contains queries
CREATE INDEX idx_posts_content_fts ON posts USING GIN(to_tsvector('english', content));

-- Full-text search query
SELECT * FROM posts WHERE to_tsvector('english', content) @@ to_tsquery('redis & caching');
```

**GiST Index (Geospatial)**
```sql
-- Good for: location queries (nearby drivers in Uber!)
CREATE INDEX idx_drivers_location ON drivers USING GIST(location);

-- Find drivers within 5km
SELECT * FROM drivers WHERE ST_Distance(location, ST_Point(-74.0060, 40.7128)) < 5000;
```

**Partial Index (Space-efficient)**
```sql
-- Only index rows that match a condition — saves disk space!
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;
-- 80% of users inactive? This index is 80% smaller!
```

**Composite Index (Most Important)**
```sql
-- Index multiple columns together
CREATE INDEX idx_posts_compound ON posts(user_id, status, created_at DESC);

-- ⚠️ ORDER MATTERS! Left-most columns must be in query for index to be used.
-- ✅ Uses index: WHERE user_id = 123 AND status = 'published'
-- ✅ Uses index: WHERE user_id = 123
-- ❌ Skips index: WHERE status = 'published'  (no user_id in query)
```

---

### EXPLAIN ANALYZE — Your Debugging Tool

```sql
EXPLAIN ANALYZE
SELECT * FROM posts WHERE user_id = 123 ORDER BY created_at DESC LIMIT 20;

-- Output shows:
-- Seq Scan on posts (cost=0.00..15000.00 rows=500000)  ← BAD! Full table scan
-- vs
-- Index Scan using idx_posts_user_created (cost=0.43..8.45 rows=20) ← GOOD!

-- Key things to look for:
-- "Seq Scan" → Missing index!
-- "cost=XXXX" → Higher cost = slower
-- "actual time=XX ms" → Real execution time
```

---

### Table Partitioning

**Range Partitioning (By Date)**
```sql
-- Partition posts by year
CREATE TABLE posts (
  id UUID,
  user_id UUID,
  content TEXT,
  created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

CREATE TABLE posts_2023 PARTITION OF posts
  FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE posts_2024 PARTITION OF posts
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Query automatically goes to the right partition!
SELECT * FROM posts WHERE created_at >= '2024-01-01'; -- Only scans posts_2024
```

**Hash Partitioning (By User)**
```sql
-- Split users into 4 partitions by hash of user_id
CREATE TABLE posts PARTITION BY HASH (user_id);

CREATE TABLE posts_0 PARTITION OF posts FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE posts_1 PARTITION OF posts FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE posts_2 PARTITION OF posts FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE posts_3 PARTITION OF posts FOR VALUES WITH (MODULUS 4, REMAINDER 3);

-- User 123's posts always go to posts_123%4=3 → posts_3
```

---

## ⚖️ Trade-offs

| | Benefit | Cost |
|-|---------|------|
| **Index** | Fast reads | Slower writes (index must be updated) |
| **More indexes** | More queries optimized | More disk space, slower inserts |
| **Partitioning** | Fast scans on large tables | Added complexity in schema management |
| **Partial index** | Saves space | Only useful for specific queries |

**Index Rule of Thumb:**
- Add indexes on columns used in `WHERE`, `ORDER BY`, `JOIN` clauses
- Don't add indexes on columns with very few unique values (gender: M/F → index not helpful)
- For every write-heavy table, be conservative with indexes

---

## 📊 Scalability Discussion

### MongoDB Indexing

```javascript
// Create indexes in MongoDB
// Compound index for feed queries
await db.collection('posts').createIndex({ userId: 1, createdAt: -1 });

// Text search index
await db.collection('posts').createIndex({ content: 'text', title: 'text' });

// Geospatial index for location-based apps
await db.collection('drivers').createIndex({ location: '2dsphere' });

// TTL index — auto-delete documents after expiry!
await db.collection('sessions').createIndex(
  { createdAt: 1 }, 
  { expireAfterSeconds: 3600 }  // Delete sessions after 1 hour!
);

// Check index usage
await db.collection('posts').aggregate([{ $indexStats: {} }]).toArray();
```

### Monitoring Index Usage in PostgreSQL

```sql
-- Find unused indexes (wasting space and slowing writes)
SELECT 
  schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0  -- Never used!
ORDER BY pg_total_relation_size(indexrelid) DESC;

-- Find tables missing indexes (slow full scans)
SELECT 
  schemaname, tablename, seq_scan, seq_tup_read
FROM pg_stat_user_tables
WHERE seq_scan > 1000  -- Being scanned a lot!
ORDER BY seq_scan DESC;
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: How does a database index work internally?

**Solution:**
Most database indexes use a **B-tree (Balanced Tree)** data structure:
```
         [user_id: 500]
         /              \
[user_id: 250]      [user_id: 750]
   /       \           /        \
[100-249] [250-499] [500-749] [750-1000]
                                  ↓
                              [Leaf node: actual row pointer]
```
- Tree stays balanced → search is always O(log n)
- 1 billion rows → only ~30 comparisons to find a value!
- Without index: O(n) → scan all 1 billion rows

---

### Q2: What is the difference between clustered and non-clustered indexes?

**Solution:**
- **Clustered Index:** Data rows are physically stored in the order of the index. One per table. In PostgreSQL, the primary key creates a clustered index (via heap storage). In MySQL InnoDB, data is stored in primary key order.
- **Non-clustered (Secondary) Index:** Index is stored separately, contains pointers to the actual rows. Multiple allowed per table.

```sql
-- Clustered: rows are physically sorted by id
PRIMARY KEY (id)  -- In MySQL InnoDB, this IS the clustered index

-- Non-clustered: just an index, data is elsewhere
CREATE INDEX idx_email ON users(email);  -- Points to row location
```

When you query by a secondary index → it finds the row pointer → fetches the actual row (extra step). That's why primary key lookups are fastest.

---

### Q3: What is an index scan vs sequential scan?

**Solution:**
- **Sequential Scan (Seq Scan):** Read the ENTIRE table row by row. Like reading a book cover to cover.
- **Index Scan:** Use the B-tree index to jump directly to matching rows. Like using the book's index.

When does PostgreSQL choose Seq Scan over Index Scan?
- When query matches a LOT of rows (e.g., `WHERE status = 'active'` and 90% are active — faster to just scan all)
- When table is tiny (index overhead not worth it)
- When statistics are outdated: `ANALYZE posts;` — force PostgreSQL to recalculate

---

### Q4: What is partition pruning?

**Solution:**
When you run a query on a partitioned table, PostgreSQL's query planner examines the `WHERE` clause and determines which partitions to skip entirely.

```sql
-- Table partitioned by year
SELECT * FROM posts WHERE created_at >= '2024-01-01';

-- Without partition pruning: scan posts_2022, posts_2023, posts_2024
-- With partition pruning: skip posts_2022, posts_2023 → only scan posts_2024!

-- This only works if the partition key is in the WHERE clause:
-- ✅ WHERE created_at >= '2024-01-01' → pruning works
-- ❌ WHERE user_id = 123 → pruning doesn't work (partitioned by date, not user_id)
```

---

### Q5: How do you identify and fix slow queries in production?

**Solution:**
**Step 1:** Enable slow query logging
```sql
-- PostgreSQL: log queries slower than 100ms
ALTER SYSTEM SET log_min_duration_statement = '100';
SELECT pg_reload_conf();
```

**Step 2:** Find the slowest queries
```sql
-- pg_stat_statements extension
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

**Step 3:** Analyze the query
```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM posts WHERE user_id = 123;
```

**Step 4:** Fix it
```sql
-- Add missing index
CREATE INDEX CONCURRENTLY idx_posts_user ON posts(user_id);
-- CONCURRENTLY: Doesn't lock the table! Safe for production.
```

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: You have a posts table with 1 billion rows. Users want to search posts by hashtag. Design the indexing strategy.

**Solution:**
```sql
-- Option 1: PostgreSQL full-text search with GIN index
ALTER TABLE posts ADD COLUMN search_vector tsvector;
UPDATE posts SET search_vector = to_tsvector('english', content || ' ' || array_to_string(hashtags, ' '));
CREATE INDEX idx_posts_search ON posts USING GIN(search_vector);

-- Search query
SELECT * FROM posts WHERE search_vector @@ to_tsquery('#redis & #caching')
ORDER BY created_at DESC LIMIT 20;

-- Option 2: Separate hashtags table (better for many hashtags)
CREATE TABLE post_hashtags (
  post_id UUID REFERENCES posts(id),
  hashtag VARCHAR(100),
  PRIMARY KEY (post_id, hashtag)
);
CREATE INDEX idx_hashtags_tag ON post_hashtags(hashtag);
CREATE INDEX idx_hashtags_post ON post_hashtags(post_id);

-- Find all posts with #redis
SELECT p.* FROM posts p
JOIN post_hashtags ph ON p.id = ph.post_id
WHERE ph.hashtag = 'redis'
ORDER BY p.created_at DESC LIMIT 20;

-- For truly massive scale: Use Elasticsearch (see HLD/20_Search_Design.md)
```

---

### Problem 2: Design a partitioning strategy for an e-commerce orders table that will have 10 billion rows in 5 years

**Solution:**
```sql
-- Range partition by year-month for recent access patterns
CREATE TABLE orders (
  id UUID,
  user_id UUID,
  total DECIMAL(10,2),
  status VARCHAR(50),
  created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE orders_2024_01 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- For archive: yearly partitions for old data
CREATE TABLE orders_2022 PARTITION OF orders
  FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');

-- Index each partition
CREATE INDEX ON orders_2024_01(user_id, created_at DESC);
CREATE INDEX ON orders_2024_01(status) WHERE status IN ('pending', 'processing');

-- Automate partition creation with pg_partman extension
-- Drop old partitions to archive (move to S3 + Athena for cold storage)

-- Node.js: No query changes needed! PostgreSQL handles partition routing transparently.
const orders = await pool.query(
  'SELECT * FROM orders WHERE user_id = $1 ORDER BY created_at DESC LIMIT 10',
  [userId]
);
```

---

### Navigation
**Prev:** [07_SQL_vs_NoSQL.md](07_SQL_vs_NoSQL.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [09_Replication_and_Sharding.md](09_Replication_and_Sharding.md)
