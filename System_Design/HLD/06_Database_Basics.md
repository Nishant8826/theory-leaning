# 📌 Database Basics

## 🧠 Concept Explanation (Story Format)

A database is simply an organized way to store and retrieve data. Every app you've built uses one.

When you built your first Node.js + MongoDB app:
- Users data → stored in MongoDB collection
- You queried it with `db.collection('users').findOne({ email })`

When you built with PostgreSQL:
- Users table → rows with columns (id, email, password, created_at)
- You queried with `SELECT * FROM users WHERE email = $1`

But what happens when you have 500 million users? Your single database server can't hold all that data, can't process all queries fast enough, and becomes a critical failure point.

This file teaches you the **fundamentals** you need to make smart database choices in system design.

---

## 🏗️ Basic Design (Naive)

```
Node.js App
    ↓ (all queries)
Single Database Server
├── users table
├── posts table
├── comments table
├── orders table
└── products table

Problems:
- One DB = single point of failure
- All reads + writes go to same server
- Hard to scale different tables independently
- One slow query can slow down everything else
```

---

## ⚡ Optimized Design

```
Node.js App
    ↓
[Redis Cache] ← Read frequently accessed data
    ↓ (cache miss)
[Primary DB] ← Handle ALL writes
    ↓ (replication)
[Read Replica 1] ← Handle read traffic
[Read Replica 2] ← Handle read traffic

For different concerns:
[PostgreSQL] → Users, Transactions (need ACID)
[MongoDB] → Posts, Comments (flexible schema)
[Redis] → Sessions, Cache, Leaderboards
[S3] → Files, Images, Videos
```

---

## 🔍 Key Components

### ACID Properties (Critical Concept)

**A - Atomicity:** All operations in a transaction succeed, or ALL fail.
```sql
-- Transfer money: Both operations must succeed together
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- Only commits if BOTH succeeded
-- If server crashes between: ROLLBACK automatically!
```

**C - Consistency:** Database always goes from one valid state to another.
```sql
-- Constraint: balance cannot go negative
ALTER TABLE accounts ADD CONSTRAINT check_balance CHECK (balance >= 0);
-- This will FAIL and rollback if balance would go negative
```

**I - Isolation:** Concurrent transactions don't interfere with each other.
```
User A reads balance: $100
User B reads balance: $100
User A withdraws $100 → balance = $0
User B withdraws $100 → ERROR: balance would be -$100
(Without isolation: both could withdraw, resulting in -$100!)
```

**D - Durability:** Once committed, data survives crashes.
```
Power goes out mid-transaction → transaction rolls back on restart
Power goes out AFTER commit → data is preserved (written to disk WAL)
```

### Types of Database Relationships

```sql
-- One-to-Many: One user has many posts
CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(255));
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),  -- Foreign key
  content TEXT
);

-- Many-to-Many: Users can follow many users
CREATE TABLE follows (
  follower_id INT REFERENCES users(id),
  following_id INT REFERENCES users(id),
  PRIMARY KEY (follower_id, following_id)
);
```

### Database Connection Pooling

**Why you need it:** Opening a new DB connection takes ~50ms. Every Node.js request opening a new connection = disaster.

```javascript
// ✅ Use connection pool (pg library)
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,        // Maximum 20 connections in pool
  idleTimeoutMillis: 30000,  // Close idle connections after 30s
  connectionTimeoutMillis: 2000, // Fail if can't connect within 2s
});

// All requests SHARE the 20 connections (instead of creating new ones)
async function getUserById(id) {
  const client = await pool.connect();
  try {
    const result = await client.query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0];
  } finally {
    client.release(); // ALWAYS release back to pool!
  }
}
```

---

## ⚖️ Trade-offs

| Consideration | SQL (PostgreSQL) | NoSQL (MongoDB) |
|--------------|-----------------|-----------------|
| Schema | Fixed, enforced | Flexible, dynamic |
| ACID | Full support | Limited (MongoDB 4+ has transactions) |
| Scaling | Vertical + Read Replicas | Horizontal sharding |
| Joins | Excellent | Avoid (embedded docs instead) |
| Query Language | SQL (powerful) | MongoDB Query Language |
| Best for | Financial data, relationships | Catalogs, logs, user data |

---

## 📊 Scalability Discussion

### Read vs Write Scaling

**80% of database traffic is reads** (SELECT queries). Scale reads by:
1. **Read Replicas:** Copy of primary DB for read traffic
2. **Caching:** Redis absorbs most read traffic before it reaches DB
3. **Indexing:** Make reads 100x faster without more hardware

```javascript
// Route reads to replica, writes to primary
const primaryPool = new Pool({ connectionString: process.env.PRIMARY_DB });
const replicaPool = new Pool({ connectionString: process.env.REPLICA_DB });

async function getUser(id) {
  return replicaPool.query('SELECT * FROM users WHERE id = $1', [id]);
}

async function createUser(data) {
  return primaryPool.query('INSERT INTO users (name, email) VALUES ($1, $2)', 
                          [data.name, data.email]);
}
```

### N+1 Query Problem

The most common performance killer:

```javascript
// ❌ N+1: 1 query for posts + N queries for each user
const posts = await db.query('SELECT * FROM posts'); // 1 query
for (const post of posts.rows) {
  post.author = await db.query('SELECT * FROM users WHERE id = $1', 
                              [post.user_id]); // N queries!
}
// If 100 posts → 101 DB queries!

// ✅ JOIN: Single query gets everything
const posts = await db.query(`
  SELECT posts.*, users.name as author_name, users.avatar
  FROM posts 
  JOIN users ON posts.user_id = users.id
  ORDER BY posts.created_at DESC
  LIMIT 20
`); // Just 1 query!
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What are ACID properties? Why do they matter?

**Solution:**
ACID ensures database transactions are processed reliably:
- **Atomicity:** Transaction is all-or-nothing. Critical for money transfers — you can't debit without crediting.
- **Consistency:** DB constraints are always maintained. Can't insert a post without a valid user_id.
- **Isolation:** Concurrent transactions don't see each other's in-progress changes. Prevents double-spending.
- **Durability:** Committed data survives crashes. Your order isn't lost if server crashes after payment.

NoSQL databases like MongoDB sacrifice some ACID properties for scalability. This is why we ALWAYS use PostgreSQL for financial transactions.

---

### Q2: What is connection pooling and why is it important?

**Solution:**
Each database connection uses resources (memory, file descriptors) and takes time to establish (~50ms). Connection pooling maintains a pool of pre-opened connections that requests can borrow and return.

Without pooling: 1000 simultaneous requests = 1000 new connections = DB overload + 50 seconds wasted.
With pooling (pool size 20): 1000 requests share 20 connections = minimal overhead.

Key settings:
- `max: 20` - don't set too high (DB has max connections limit, usually 100)
- `idleTimeoutMillis` - close unused connections to save resources
- Always `release()` connections in a `finally` block!

---

### Q3: What is database normalization and when would you denormalize?

**Solution:**
**Normalization:** Eliminate data duplication. Each piece of info stored once.
```sql
-- Normalized: userName stored only in users table
users: { id, name, email }
posts: { id, user_id, content }  -- user_id references users.id
```

**Denormalization:** Intentionally duplicate data for read performance.
```sql
-- Denormalized: userName copied into posts table
posts: { id, user_id, author_name, content }  -- author_name duplicated
```

**When to denormalize:**
- When JOIN queries are too slow (e.g., showing posts feed with author names)
- Specific read-heavy paths that need max performance
- Accept that if user changes name, all posts need updating too

In practice: normalize first, denormalize specific hot paths when you hit performance issues.

---

### Q4: How do you handle database migrations in production without downtime?

**Solution:**
Use **expand-contract pattern (backward-compatible migrations)**:

Step 1 (Expand): Add new column, keep old column
```sql
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);
```

Step 2: Deploy new code that writes to BOTH old and new column

Step 3: Backfill: populate new column from old data
```sql
UPDATE users SET phone_number = old_phone WHERE phone_number IS NULL;
```

Step 4 (Contract): Remove old column (after validating new column is fully populated)
```sql
ALTER TABLE users DROP COLUMN old_phone;
```

Tools: Use `db-migrate`, `Flyway`, or `Sequelize migrations` to manage migration history.

---

### Q5: What is the difference between a primary key and a foreign key?

**Solution:**
- **Primary Key:** Unique identifier for each row in a table. Cannot be NULL. Each table has one. Example: `users.id`.
- **Foreign Key:** Column that references a primary key in another table. Creates a relationship. Example: `posts.user_id` references `users.id`.

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,      -- Primary key
  email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,  -- Foreign key
  content TEXT
);
-- ON DELETE CASCADE: If user is deleted, all their posts are deleted too
```

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design the database schema for a Twitter-like app

**Solution:**
```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  bio TEXT,
  avatar_url VARCHAR(500),
  followers_count INT DEFAULT 0,     -- Denormalized for performance
  following_count INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Tweets
CREATE TABLE tweets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  content VARCHAR(280) NOT NULL,
  likes_count INT DEFAULT 0,         -- Denormalized
  retweets_count INT DEFAULT 0,      -- Denormalized
  reply_to_id UUID REFERENCES tweets(id),  -- For replies
  created_at TIMESTAMP DEFAULT NOW()
);

-- Follows
CREATE TABLE follows (
  follower_id UUID REFERENCES users(id) ON DELETE CASCADE,
  following_id UUID REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (follower_id, following_id)
);

-- Likes
CREATE TABLE likes (
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  tweet_id UUID REFERENCES tweets(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (user_id, tweet_id)
);

-- Indexes for performance
CREATE INDEX idx_tweets_user_id ON tweets(user_id);
CREATE INDEX idx_tweets_created_at ON tweets(created_at DESC);
CREATE INDEX idx_follows_following_id ON follows(following_id);
```

---

### Problem 2: Your PostgreSQL is getting 10,000 queries/second and slowing down. What do you do?

**Solution:**
1. **Check slow query log:** `ALTER SYSTEM SET log_min_duration_statement = '100ms';`
2. **Add missing indexes:** Run `EXPLAIN ANALYZE` on slow queries
3. **Add Redis caching** for frequently read data (user profiles, post counts)
4. **Add read replicas** (AWS RDS): Route all SELECT queries to replica
5. **Optimize queries:** Fix N+1 problems, use JOINs instead of nested queries
6. **Connection pooling:** Use PgBouncer between Node.js and PostgreSQL
7. **Partition large tables:** Split by date (posts from 2020, 2021, 2022...)
8. **Archive old data:** Move 3-year-old data to cheaper storage

---

### Navigation
**Prev:** [05_Caching.md](05_Caching.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [07_SQL_vs_NoSQL.md](07_SQL_vs_NoSQL.md)
