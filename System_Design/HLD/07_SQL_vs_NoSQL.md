# 📌 SQL vs NoSQL

## 🧠 Concept Explanation (Story Format)

You're building a social media app. You have two types of data:

1. **User accounts** — always have: id, email, password, name. Very structured. Need to run financial queries across them.

2. **User posts** — sometimes have: photos, videos, text, polls, stories, reels. Different post types have different fields. Very flexible.

For user accounts → **SQL (PostgreSQL)** — structured, relationships matter, need ACID.
For posts → **NoSQL (MongoDB)** — flexible schema, each post type can have different fields.

This is why Facebook uses **both** MySQL AND Cassandra (NoSQL). Different data, different tools.

---

## 🏗️ Basic Design (Naive — One Database for Everything)

```
Everything in MongoDB:
{
  _id: "123",
  email: "alice@example.com",
  posts: [
    { type: "photo", url: "..." },
    { type: "text", content: "..." }
  ],
  orders: [
    { product: "book", price: 15.99, status: "shipped" }
  ]
}

Problems:
- Mixing user data with orders in one document
- Can't efficiently query across users for reports
- No joins → duplicate data everywhere
- Can't do financial calculations safely (no ACID)
```

---

## ⚡ Optimized Design (Right Tool for Right Job)

```
PostgreSQL (SQL):
├── users (id, email, name, created_at)
├── orders (id, user_id, total, status)
├── payments (id, order_id, amount, stripe_id)
└── Relationships enforced with foreign keys

MongoDB (NoSQL):
├── posts (flexible: photo, video, story, reel)
├── comments (nested or separate collection)
└── user_activity (logs, events — flexible structure)

Redis:
├── sessions (key-value)
├── caches (any hot data)
└── leaderboards (sorted sets)
```

---

## 🔍 Key Components

### SQL Databases (PostgreSQL, MySQL)

**When to choose SQL:**
- Data has clear structure and relationships
- Need joins between tables
- ACID compliance required (money, inventory)
- Complex queries (aggregations, reporting)
- Schema is stable and well-understood

**PostgreSQL Example:**
```sql
-- Query: Top 10 users by total spending this month
SELECT 
  u.name, 
  SUM(o.total) as total_spent
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.created_at >= NOW() - INTERVAL '30 days'
GROUP BY u.id, u.name
ORDER BY total_spent DESC
LIMIT 10;
```
This kind of query is easy in SQL, very painful in MongoDB.

---

### NoSQL Databases (MongoDB)

**When to choose MongoDB:**
- Schema varies by record (different post types)
- Need to embed related data (post + comments in one document)
- Horizontal sharding needed from the start
- Rapid development (schema changes without migrations)
- Storing JSON-like data from APIs

**MongoDB Example:**
```javascript
// Different post types in same collection — no schema conflict!
await db.collection('posts').insertMany([
  {
    type: 'photo',
    userId: '123',
    url: 'https://s3.../photo.jpg',
    filters: ['vintage', 'warm'],
    location: { lat: 40.7128, lng: -74.0060 }
  },
  {
    type: 'text',
    userId: '456',
    content: 'Just had the best coffee!',
    hashtags: ['coffee', 'morning']
  },
  {
    type: 'poll',
    userId: '789',
    question: 'Tea or Coffee?',
    options: [
      { text: 'Tea', votes: 150 },
      { text: 'Coffee', votes: 320 }
    ]
  }
]);
```

---

### NoSQL Types

| Type | Example | Use Case |
|------|---------|----------|
| Document | MongoDB | Posts, products, user profiles |
| Key-Value | Redis | Sessions, caches, counters |
| Column-family | Cassandra | Time-series, write-heavy (IoT) |
| Graph | Neo4j | Social networks, recommendations |

---

## ⚖️ Trade-offs

| Feature | PostgreSQL (SQL) | MongoDB (NoSQL) |
|---------|-----------------|-----------------|
| Schema | Strict (migrations needed) | Flexible (no migrations) |
| Relationships | Native JOIN support | Manual (lookup queries) |
| ACID | Full | Partial (single doc by default) |
| Horizontal Scale | Hard (sharding complex) | Native sharding |
| Query Power | Extremely powerful SQL | Good for document queries |
| Write Speed | Slower (ACID overhead) | Faster |
| Aggregations | Excellent (GROUP BY, etc.) | MongoDB Aggregation Pipeline |

---

## 📊 Scalability Discussion

### Scaling SQL vs NoSQL

**Scaling PostgreSQL:**
1. Vertical scaling (bigger server) — easiest
2. Read replicas (AWS RDS Multi-AZ)
3. Connection pooling (PgBouncer)
4. Table partitioning (split large tables by date)
5. Manual sharding (last resort, very complex)

**Scaling MongoDB:**
1. Replica sets (primary + secondaries)
2. Native horizontal sharding (easier than SQL)
3. Atlas Serverless (automatic scaling)

### Real World: Which Companies Use What?

| Company | SQL | NoSQL |
|---------|-----|-------|
| Instagram | PostgreSQL (users, follows) | Cassandra (timeline) |
| Uber | MySQL | Cassandra (trip data) |
| LinkedIn | MySQL | Espresso (NoSQL, in-house) |
| Twitter | MySQL (tweets) | Redis, Manhattan (NoSQL) |
| Airbnb | MySQL | Elasticsearch |
| Netflix | MySQL | Cassandra (watch history) |

**Pattern:** Almost every large company uses **both SQL and NoSQL**. The question is: which for what?

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: When would you choose MongoDB over PostgreSQL?

**Solution:**
Choose MongoDB when:
1. **Schema is dynamic:** Content management systems where each article type has different fields
2. **Embedding makes sense:** Blog post with its comments — stored as one document, fast to retrieve
3. **High write throughput:** IoT sensor data, logs, event streams
4. **Rapid iteration:** MVP where schema will change frequently
5. **Horizontal scaling needed:** MongoDB sharding is built-in and easier than PostgreSQL sharding

Example: For a product catalog where each category (electronics, clothing, food) has completely different attributes → MongoDB is perfect.

---

### Q2: Can MongoDB replace PostgreSQL completely?

**Solution:**
No. MongoDB is NOT a full replacement:
- **No true JOINs:** MongoDB has `$lookup` but it's slower and less powerful
- **Limited ACID:** Multi-document transactions only in MongoDB 4.0+, and slower
- **No referential integrity:** Can have orphaned documents (no foreign key enforcement)
- **Aggregations harder:** GROUP BY queries are more complex in MongoDB pipeline

For anything involving money, user accounts, relationships across entities → always use PostgreSQL.
For flexible content, large-scale writes, varied schemas → MongoDB is excellent.

---

### Q3: What is a MongoDB Aggregation Pipeline and when do you use it?

**Solution:**
Aggregation pipeline processes documents through stages, like a Unix pipe. Use it for complex data analysis.

```javascript
// Find top 5 most liked post types for users above age 25
const result = await db.collection('posts').aggregate([
  // Stage 1: Filter
  { $match: { status: 'published' } },
  
  // Stage 2: Join with users collection
  { $lookup: {
    from: 'users',
    localField: 'userId',
    foreignField: '_id',
    as: 'author'
  }},
  
  // Stage 3: Filter by user age
  { $match: { 'author.age': { $gte: 25 } } },
  
  // Stage 4: Group by post type
  { $group: {
    _id: '$type',
    totalLikes: { $sum: '$likesCount' },
    postCount: { $sum: 1 }
  }},
  
  // Stage 5: Sort by likes
  { $sort: { totalLikes: -1 } },
  
  // Stage 6: Limit
  { $limit: 5 }
]).toArray();
```

---

### Q4: How does database indexing differ between MongoDB and PostgreSQL?

**Solution:**
Both support similar index types, but with different syntax:

```javascript
// MongoDB indexes
await db.collection('posts').createIndex({ userId: 1 }); // Ascending
await db.collection('posts').createIndex({ createdAt: -1 }); // Descending (for recent first)
await db.collection('posts').createIndex({ content: 'text' }); // Full-text search
await db.collection('posts').createIndex({ location: '2dsphere' }); // Geospatial (Uber!)
// Compound index
await db.collection('posts').createIndex({ userId: 1, createdAt: -1 });
```

```sql
-- PostgreSQL indexes
CREATE INDEX idx_posts_user ON posts(user_id);
CREATE INDEX idx_posts_created ON posts(created_at DESC);
CREATE INDEX idx_posts_content ON posts USING GIN(to_tsvector('english', content)); -- Full text
-- Partial index (only index active posts — saves space!)
CREATE INDEX idx_active_posts ON posts(user_id) WHERE status = 'published';
```

Key difference: PostgreSQL has more index types (B-tree, Hash, GiST, GIN, BRIN) and better query planner.

---

### Q5: What is the BASE model in NoSQL?

**Solution:**
BASE is the opposite of ACID, common in NoSQL systems:
- **B**asically **A**vailable: System guarantees availability, but not every response will be the latest data
- **S**oft state: State of system may change over time even without input (due to eventual consistency)
- **E**ventually Consistent: Given enough time, all nodes will have the same data

Example: When you post on Instagram, your new follower in Australia might see your post 2 seconds later than your follower in New York. That's eventual consistency. It's acceptable because being slightly delayed is better than the entire system being down.

In our stack: Use PostgreSQL (ACID) for user auth and payments, MongoDB (BASE) for post feeds and activity logs.

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design the data storage strategy for an Uber-like app

**Solution:**
```
PostgreSQL (structured, relational):
├── users (id, name, email, phone, payment_method_id)
├── drivers (id, user_id, license, vehicle_id, rating)
├── vehicles (id, driver_id, make, model, license_plate)
├── rides (id, rider_id, driver_id, start_location, end_location, fare, status)
└── payments (id, ride_id, amount, stripe_charge_id, status)

MongoDB (flexible, high-write):
├── ride_tracking (ride_id, locations: [{lat, lng, timestamp}])  — high-frequency GPS data
├── driver_locations (driver_id, lat, lng, timestamp)  — real-time positions
└── surge_events (region, multiplier, timestamp)  — event log

Redis (real-time, fast):
├── active_drivers: geospatial set (GEOADD, GEORADIUS queries)
├── ride_state:{rideId}: current ride status
└── driver_session:{driverId}: online/offline status

AWS S3:
└── driver documents, profile photos
```

---

### Problem 2: Your MongoDB collection has 100 million posts and queries are slow. What do you do?

**Solution:**
1. **Check indexes:** `db.posts.explain("executionStats").find(query)` — look for COLLSCAN (full scan) vs IXSCAN (index scan)
2. **Add compound index:** Most queries filter by userId + createdAt? → `createIndex({ userId: 1, createdAt: -1 })`
3. **Shard the collection:** Split by userId using range-based or hash-based sharding
4. **Archive old posts:** Move posts older than 2 years to cheaper cold storage
5. **Projection:** Only fetch needed fields → `find(query, { content: 1, userId: 1 })`  (don't fetch huge embedded arrays)
6. **Redis caching:** Cache user's last 50 posts in Redis (most users only scroll recent content)

---

### Navigation
**Prev:** [06_Database_Basics.md](06_Database_Basics.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [08_Indexing_and_Partitioning.md](08_Indexing_and_Partitioning.md)
