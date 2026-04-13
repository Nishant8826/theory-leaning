# When to Use MongoDB vs SQL

> 📌 **File:** 19_When_To_Use_MongoDB_Vs_SQL.md | **Level:** SQL Expert → MongoDB

---

## What is it?

This is the **decision framework** for choosing between MongoDB and SQL databases for a given project or component. Most real-world systems aren't purely one or the other — they use **polyglot persistence** (different databases for different parts). This chapter gives you the criteria to make that decision confidently.

---

## The Decision Matrix

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        MongoDB vs SQL — Decision Matrix                 │
├──────────────────────────────┬───────────────────┬──────────────────────┤
│  Criteria                    │ MongoDB Wins      │ SQL Wins             │
├──────────────────────────────┼───────────────────┼──────────────────────┤
│  Schema flexibility          │ ✅ Evolving schema│ Fixed, well-known    │
│  Nested/hierarchical data    │ ✅ Natural fit    │ Requires JOINs/JSON  │
│  Read performance (single)   │ ✅ Data locality  │ Needs JOINs          │
│  Write throughput             │ ✅ Less overhead  │ Constraint overhead  │
│  Horizontal scaling           │ ✅ Native sharding│ Complex, limited     │
│  Complex relationships       │ Needs redesign    │ ✅ JOINs, FKs        │
│  Transactions (multi-entity) │ Supported, costly │ ✅ Core feature      │
│  Referential integrity       │ App responsibility│ ✅ DB-enforced        │
│  Complex reporting/analytics │ Aggregation works │ ✅ SQL is king        │
│  ACID across many tables     │ Limited            │ ✅ Native             │
│  Schema migrations           │ ✅ None needed    │ ALTER TABLE required  │
│  Developer velocity          │ ✅ Fast prototyping│ More upfront design  │
│  Data consistency guarantees │ Eventual (default)│ ✅ Strong (default)   │
│  Geospatial queries          │ ✅ Native 2dsphere│ PostGIS extension    │
│  Time-series data            │ ✅ Time-series col│ Partitioning needed  │
│  Full-text search             │ Moderate          │ Moderate             │
│  Team SQL expertise          │ Learning curve    │ ✅ Existing skills    │
└──────────────────────────────┴───────────────────┴──────────────────────┘
```

---

## Use MongoDB When

### 1. Content Management Systems (CMS)

```javascript
// Different content types with different fields
// Article: { title, body, author, tags, publishedAt }
// Video: { title, url, duration, resolution, subtitles }
// Gallery: { title, images: [...], layout }
// Podcast: { title, audioUrl, duration, transcript }

// In SQL: You'd need table-per-type or sparse columns
// In MongoDB: Single collection with polymorphic documents
db.content.insertMany([
  { type: "article", title: "...", body: "...", tags: [...] },
  { type: "video", title: "...", url: "...", duration: 300 },
  { type: "podcast", title: "...", audioUrl: "...", transcript: "..." }
])
// Flexible, fast, no schema migration when adding new content types
```

### 2. Real-Time Analytics & Event Logging

```javascript
// High-volume writes, flexible event schemas, time-series data
db.events.insertOne({
  eventType: "page_view",
  userId: ObjectId("..."),
  page: "/products/laptop",
  metadata: {
    referrer: "google.com",
    browser: "Chrome",
    device: "mobile",
    sessionId: "abc123"
  },
  timestamp: new Date()
})
// 10,000+ writes/second
// Schema varies by event type
// Bucket pattern for efficient time-range queries
```

### 3. User Profiles & Personalization

```javascript
// Different users have different attributes
{
  _id: ObjectId("..."),
  email: "john@example.com",
  profile: {
    name: "John",
    bio: "Developer",
    socialLinks: { github: "john", twitter: "@john" },
    preferences: {
      newsletter: true,
      theme: "dark",
      language: "en",
      categories: ["tech", "science"]
    },
    gamification: {
      points: 1500,
      badges: ["early_adopter", "contributor"],
      level: 5
    }
  },
  // Varies wildly between users — perfect for documents
}
```

### 4. Product Catalogs (Varying Attributes)

```javascript
// Electronics have specs; clothing has sizes; books have ISBN
// SQL: EAV pattern or 50 nullable columns
// MongoDB: Natural fit
{
  type: "electronics",
  name: "Laptop",
  specs: { ram: "16GB", storage: "512GB", cpu: "i7" }
}
{
  type: "clothing",
  name: "T-Shirt",
  sizes: ["S", "M", "L", "XL"],
  colors: ["Red", "Blue"],
  material: "Cotton"
}
```

### 5. IoT & Sensor Data

```javascript
// Millions of data points per day, time-series queries
// Bucket pattern + time-series collection
db.createCollection("sensor_data", {
  timeseries: {
    timeField: "timestamp",
    metaField: "sensorId",
    granularity: "minutes"
  }
})
```

### 6. Mobile / Offline-First Applications

```javascript
// MongoDB Realm Sync — sync between mobile and server
// Document model maps naturally to JSON-based mobile data
// Conflict resolution built into the sync protocol
```

---

## Use SQL When

### 1. Financial Systems (Banking, Payments)

```sql
-- ACID transactions across multiple tables are critical
-- Every cent must be accounted for
-- Referential integrity prevents orphaned records
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
  INSERT INTO ledger (from_id, to_id, amount) VALUES (1, 2, 100);
COMMIT;
-- SQL gives you: strong consistency, enforced constraints, audit trails
-- MongoDB CAN do this but with more overhead and less safety
```

### 2. ERP / Inventory Management

```sql
-- Complex relationships between entities
-- Products ↔ Warehouses ↔ Suppliers ↔ Purchase Orders ↔ Invoices
-- Many-to-many relationships everywhere
-- Strong referential integrity needed
-- Complex reports joining 5+ tables
SELECT
  p.name, w.location, s.name as supplier,
  SUM(i.quantity) as total_stock,
  AVG(po.unit_price) as avg_cost
FROM products p
JOIN inventory i ON p.id = i.product_id
JOIN warehouses w ON i.warehouse_id = w.id
JOIN purchase_order_items poi ON p.id = poi.product_id
JOIN purchase_orders po ON poi.order_id = po.id
JOIN suppliers s ON po.supplier_id = s.id
GROUP BY p.name, w.location, s.name;
-- This query is natural in SQL, painful in MongoDB
```

### 3. Complex Reporting & BI

```sql
-- Multi-dimensional analysis across many entities
-- Window functions, CTEs, subqueries
WITH monthly_revenue AS (
  SELECT
    DATE_TRUNC('month', created_at) as month,
    SUM(total) as revenue,
    LAG(SUM(total)) OVER (ORDER BY DATE_TRUNC('month', created_at)) as prev_month
  FROM orders
  WHERE created_at >= '2024-01-01'
  GROUP BY DATE_TRUNC('month', created_at)
)
SELECT
  month,
  revenue,
  prev_month,
  ROUND((revenue - prev_month) / prev_month * 100, 2) as growth_pct
FROM monthly_revenue
ORDER BY month;
-- SQL is built for this. MongoDB aggregation can do it but is more verbose.
```

### 4. Systems with Strong Consistency Requirements

```
- Banking: Account balances must always be correct
- Healthcare: Patient records must be complete and consistent
- Legal: Contracts and compliance records need referential integrity
- Government: Tax records, regulatory data
```

### 5. When Your Team is SQL-Expert

```
If your team has deep SQL expertise and limited MongoDB experience:
- Stick with SQL for critical systems
- Use MongoDB for new, complementary components
- Don't rewrite a working SQL system in MongoDB without clear benefits
```

---

## Polyglot Persistence — The Real-World Approach

```
┌──────────────────────────────────────────────────────────────────────┐
│                    E-Commerce Platform Architecture                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐   Product catalog, user profiles,              │
│  │    MongoDB       │   reviews, content, session storage            │
│  │                  │   → Flexible schema, read-heavy                │
│  └─────────────────┘                                                │
│                                                                      │
│  ┌─────────────────┐   Orders, payments, inventory,                 │
│  │   PostgreSQL     │   financial reports, admin data                │
│  │                  │   → ACID, complex relationships                │
│  └─────────────────┘                                                │
│                                                                      │
│  ┌─────────────────┐   Sessions, caching, rate limiting,            │
│  │     Redis        │   real-time leaderboards                       │
│  │                  │   → Speed, TTL, pub/sub                        │
│  └─────────────────┘                                                │
│                                                                      │
│  ┌─────────────────┐   Full-text search, autocomplete,              │
│  │  Elasticsearch   │   log aggregation                              │
│  │                  │   → Search, analytics                          │
│  └─────────────────┘                                                │
│                                                                      │
│  Each database does what it does BEST.                               │
│  No single database is optimal for everything.                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Node.js Polyglot Architecture

```javascript
// Multiple database connections in one application
const { MongoClient } = require('mongodb');
const { Pool } = require('pg');
const Redis = require('ioredis');

// MongoDB for products, content, user profiles
const mongoClient = new MongoClient(process.env.MONGO_URI);
const mongo = mongoClient.db('ecommerce');

// PostgreSQL for orders, payments, financial data
const pg = new Pool({ connectionString: process.env.PG_URI });

// Redis for caching and sessions
const redis = new Redis(process.env.REDIS_URI);

// Product search (MongoDB — flexible, fast reads)
app.get('/api/products', async (req, res) => {
  const products = await mongo.collection('products')
    .find({ isActive: true })
    .sort({ 'ratings.average': -1 })
    .limit(20)
    .toArray();
  res.json(products);
});

// Place order (PostgreSQL — ACID, financial data)
app.post('/api/orders', async (req, res) => {
  const client = await pg.connect();
  try {
    await client.query('BEGIN');
    const { rows: [order] } = await client.query(
      'INSERT INTO orders (customer_id, total) VALUES ($1, $2) RETURNING *',
      [req.body.customerId, req.body.total]
    );
    for (const item of req.body.items) {
      await client.query(
        'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES ($1, $2, $3, $4)',
        [order.id, item.productId, item.quantity, item.price]
      );
    }
    await client.query('COMMIT');
    res.status(201).json(order);
  } catch (err) {
    await client.query('ROLLBACK');
    res.status(500).json({ error: err.message });
  } finally {
    client.release();
  }
});

// Session management (Redis — fast, TTL)
app.use(session({
  store: new RedisStore({ client: redis }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  cookie: { maxAge: 86400000 }
}));
```

---

## Cost Comparison

```
┌──────────────────────────────────────────────────────────────┐
│                    Total Cost of Ownership                   │
├────────────────────────┬──────────────┬──────────────────────┤
│                        │ SQL (PG/MySQL)│ MongoDB              │
├────────────────────────┼──────────────┼──────────────────────┤
│  Hosting (self-managed)│ Free (OSS)   │ Free (Community)     │
│  Hosting (managed)     │ RDS: $$      │ Atlas: $$-$$$        │
│  Vertical scaling      │ $$           │ $$                   │
│  Horizontal scaling    │ $$$ (complex)│ $$ (native sharding) │
│  DBA expertise         │ $$ (common)  │ $$ (growing)         │
│  Schema migrations     │ $$$ (tooling)│ $ (minimal)          │
│  Application complexity│ $ (ORMs)     │ $ (Mongoose)         │
│  Backup/restore        │ $ (pg_dump)  │ $ (mongodump/Atlas)  │
├────────────────────────┴──────────────┴──────────────────────┤
│  MongoDB Atlas Free Tier: 512MB shared cluster (dev/testing) │
│  PostgreSQL on Supabase: Free tier available                 │
│  For small projects: Cost is similar.                         │
│  For scale: MongoDB is typically cheaper for horizontal scale │
│  but more expensive for managed service (Atlas M10+).        │
└──────────────────────────────────────────────────────────────┘
```

---

## Decision Flowchart

```
Start → What's your primary data access pattern?
  │
  ├── "Complex JOINs across many entities" → SQL ✅
  │
  ├── "Single-entity reads with embedded data" → MongoDB ✅
  │
  ├── "Financial transactions + strict consistency" → SQL ✅
  │
  ├── "Flexible/evolving schema + rapid development" → MongoDB ✅
  │
  ├── "Heavy analytics + reporting" → SQL ✅ (or data warehouse)
  │
  ├── "High write throughput + horizontal scale" → MongoDB ✅
  │
  ├── "Mix of patterns" → Polyglot Persistence ✅
  │     ├── Products, content, profiles → MongoDB
  │     ├── Orders, payments, finance → SQL
  │     ├── Cache, sessions → Redis
  │     └── Search → Elasticsearch
  │
  └── "I'm not sure" → Start with SQL (safer default)
        → Move specific components to MongoDB as needed
```

---

## Real-World Architecture Examples

### 1. Netflix

```
- User profiles, preferences: MongoDB (flexible, fast reads)
- Billing, subscriptions: SQL (ACID, financial)
- Viewing history: Cassandra (time-series, massive scale)
- Search: Elasticsearch
- Caching: EVCache (Memcached-based)
```

### 2. Uber

```
- Trip data: MySQL (sharded)
- Geospatial indexing: Custom (moved away from PostgreSQL/PostGIS)
- Real-time analytics: Apache Kafka + Flink
- Caching: Redis
```

### 3. Typical Startup

```
Phase 1 (MVP): MongoDB for everything (fast development)
Phase 2 (Growth): MongoDB + Redis (caching)
Phase 3 (Scale): MongoDB (products) + PostgreSQL (orders) + Redis + Elasticsearch
Phase 4 (Enterprise): Full polyglot persistence
```

---

## Common Mistakes

### ❌ Using MongoDB for Everything

```
"MongoDB is web-scale!" → puts financial transactions in MongoDB
→ discovers multi-document transactions are slow
→ discovers no referential integrity
→ discovers $lookup is 10x slower than SQL JOIN
→ rewrites to PostgreSQL
```

### ❌ Using SQL for Everything

```
"SQL is the gold standard!" → uses PostgreSQL for product catalog with 50 nullable columns
→ adds JSON columns for flexible data
→ adds PostGIS for geospatial
→ spends weeks on schema migrations
→ discovers MongoDB would have been simpler for this component
```

### ❌ Choosing Based on Hype

```
Choose based on:
✅ Access patterns
✅ Data relationships
✅ Consistency requirements
✅ Scale requirements
✅ Team expertise

Not based on:
❌ "MongoDB is modern"
❌ "SQL is legacy"
❌ "Our competitor uses MongoDB"
❌ "NoSQL is always faster"
```

---

## Practice Exercises

### Exercise 1: Database Selection

For each scenario, choose MongoDB, SQL, or polyglot. Justify your choice:

1. **Hospital Management System** — patient records, appointments, billing, prescriptions
2. **Social Media Platform** — user profiles, posts, stories, messages, notifications
3. **Stock Trading Platform** — order book, trade history, portfolio management
4. **IoT Smart Home** — sensor readings, device configurations, user preferences
5. **Online Learning Platform** — courses, enrollments, grades, certificates

### Exercise 2: Architecture Design

Design the database architecture for a food delivery app (like UberEats):
- Restaurants, menus, users, orders, payments, delivery tracking, reviews, notifications
- Which database for each component? Why?

---

## Interview Q&A

**Q1: When would you recommend MongoDB over PostgreSQL?**
> When the application has: flexible/evolving schemas, hierarchical data, read-heavy workloads with data locality needs, horizontal scaling requirements, or rapid prototyping needs. Specific examples: content management, product catalogs, IoT data, real-time analytics, user profiles.

**Q2: When is SQL clearly the better choice?**
> For: financial systems requiring strict ACID, complex reporting with many JOINs, systems with strong referential integrity needs, well-known and stable schemas, existing SQL expertise on the team. If you need multi-table transactions in every write path, use SQL.

**Q3: What is polyglot persistence?**
> Using different database technologies for different parts of an application, each chosen for its strengths. Example: MongoDB for product catalog, PostgreSQL for orders/payments, Redis for caching, Elasticsearch for search. This is the standard approach for modern large-scale applications.

**Q4: Can MongoDB handle transactions? Then why not use it for everything?**
> Yes, MongoDB supports multi-document ACID transactions. But they're 10-40x more expensive than SQL transactions. If your application needs transactions in > 10% of writes, the overhead is significant. MongoDB is designed to minimize transaction usage through document embedding, not to replace SQL's transaction model.

**Q5: What's the biggest mistake teams make when choosing between MongoDB and SQL?**
> Choosing based on technology preference instead of access patterns. The question isn't "which is better?" but "which fits my specific data access patterns, consistency needs, and scaling requirements?" Many teams also make the mistake of choosing one database for everything instead of using polyglot persistence.
