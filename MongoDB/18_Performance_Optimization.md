# Performance Optimization

> 📌 **File:** 18_Performance_Optimization.md | **Level:** SQL Expert → MongoDB

---

## What is it?

Performance optimization in MongoDB shares many principles with SQL (indexing, query analysis, connection pooling) but adds document-specific concerns: document size, embedding strategy, array growth, working set size, and shard key selection. As an SQL expert, you already know 60% of this — this chapter focuses on the MongoDB-specific 40%.

---

## SQL Parallel — Think of it like this

```
SQL Optimization Tool:              MongoDB Equivalent:
EXPLAIN ANALYZE                   → .explain("executionStats")
SHOW PROCESSLIST                  → db.currentOp()
pg_stat_statements                → Database Profiler
pg_stat_user_tables               → db.collection.stats()
pg_stat_user_indexes              → db.collection.aggregate([{$indexStats}])
VACUUM / ANALYZE                  → compact / reIndex
Connection pooling (PgBouncer)    → Driver connection pool (built-in)
Query cache (MySQL)               → ❌ No query cache (by design)
Materialized Views                → $merge / $out (on-demand)
Partitioning                      → Sharding (horizontal)
Read replicas                     → Secondary reads (replica set)
```

---

## The Performance Optimization Checklist

```
┌──────────────────────────────────────────────────────────────────┐
│              MongoDB Performance Optimization Pyramid            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Level 1: SCHEMA DESIGN (biggest impact)                        │
│  ├── Embed vs reference decisions                                │
│  ├── Document shape matches access patterns                     │
│  ├── No unbounded array growth                                   │
│  └── Pre-computed aggregations (computed pattern)               │
│                                                                  │
│  Level 2: INDEXING (second biggest impact)                      │
│  ├── Indexes for all frequent queries                            │
│  ├── Compound indexes following ESR rule                        │
│  ├── Covered queries where possible                              │
│  └── No unused indexes (waste write performance)                │
│                                                                  │
│  Level 3: QUERY OPTIMIZATION                                    │
│  ├── Projection (return only needed fields)                     │
│  ├── Cursor-based pagination (not skip/limit)                   │
│  ├── .lean() for read-only (Mongoose)                            │
│  └── Aggregation pipeline optimization                           │
│                                                                  │
│  Level 4: APPLICATION ARCHITECTURE                              │
│  ├── Connection pooling                                          │
│  ├── Caching (Redis)                                             │
│  ├── Read from secondaries for analytics                        │
│  └── Bulk operations for batch writes                            │
│                                                                  │
│  Level 5: INFRASTRUCTURE                                        │
│  ├── RAM > working set + indexes                                 │
│  ├── SSD storage                                                 │
│  ├── Replica set configuration                                   │
│  └── Sharding (last resort for horizontal scale)                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 1. Query Analysis with explain()

```javascript
// The most important debugging tool — equivalent to EXPLAIN ANALYZE
const explanation = db.products.find({
  "category.name": "Electronics",
  price: { $gte: 100, $lte: 1000 },
  stock: { $gt: 0 }
}).sort({ price: -1 }).explain("executionStats");

// Key metrics to check:
// ┌─────────────────────────────────────────────────────────────────┐
// │  Metric                    │ Good           │ Bad              │
// ├────────────────────────────┼────────────────┼──────────────────┤
// │  winningPlan.stage         │ IXSCAN         │ COLLSCAN         │
// │  nReturned                 │ (your results) │                  │
// │  totalDocsExamined         │ ≈ nReturned    │ >> nReturned     │
// │  totalKeysExamined         │ ≈ nReturned    │ >> nReturned     │
// │  executionTimeMillis       │ < 100ms        │ > 1000ms         │
// │  totalDocsExamined         │ 0 (covered!)   │ Any number       │
// └────────────────────────────┴────────────────┴──────────────────┘

// Ratio analysis:
const ratio = explanation.executionStats.totalDocsExamined /
              explanation.executionStats.nReturned;
// ratio ≈ 1 → ✅ Efficient (index is selective)
// ratio > 10 → ⚠️ Index not selective enough
// ratio > 100 → ❌ Missing index or wrong query pattern
```

### Profiler (= SQL Slow Query Log)

```javascript
// Enable profiler for slow queries
db.setProfilingLevel(1, { slowms: 100 })  // Log queries > 100ms

// Level 0: Off
// Level 1: Slow operations only
// Level 2: All operations (⚠️ heavy overhead)

// View slow queries
db.system.profile.find().sort({ ts: -1 }).limit(10)

// Find the slowest queries
db.system.profile.find({
  millis: { $gt: 100 }
}).sort({ millis: -1 }).limit(5).pretty()

// SQL equivalent: pg_stat_statements / slow query log
```

---

## 2. Index Optimization

### Index Usage Analysis

```javascript
// Which indexes are being used?
db.products.aggregate([{ $indexStats: {} }])

// Returns for each index:
// - accesses.ops: Number of times this index was used
// - accesses.since: When tracking started
// If ops = 0 for weeks → drop the index (wasting write performance)

// Check current index sizes
db.products.stats().indexSizes
// {
//   "_id_": 245760,
//   "idx_category_price": 163840,
//   "idx_name_text": 524288
// }
// Total should fit in RAM
```

### Creating Optimal Compound Indexes

```javascript
// Query to optimize:
db.orders.find({
  customerId: ObjectId("..."),    // Equality
  status: "shipped",              // Equality
  createdAt: { $gte: lastMonth }  // Range
}).sort({ createdAt: -1 })        // Sort

// Apply ESR rule:
// E (Equality): customerId, status
// S (Sort): createdAt (descending)
// R (Range): createdAt (same as sort here)

// Optimal index:
db.orders.createIndex({ customerId: 1, status: 1, createdAt: -1 })

// This single index covers:
// ✅ db.orders.find({ customerId: X })
// ✅ db.orders.find({ customerId: X, status: Y })
// ✅ db.orders.find({ customerId: X, status: Y }).sort({ createdAt: -1 })
// ✅ db.orders.find({ customerId: X, status: Y, createdAt: { $gte: D } })
```

### Covered Queries (Zero Document Reads)

```javascript
// Index contains all fields needed — no document read required
db.products.createIndex({ brand: 1, price: 1, name: 1 })

db.products.find(
  { brand: "Dell" },
  { brand: 1, price: 1, name: 1, _id: 0 }  // All fields in index, exclude _id
)
// explain(): totalDocsExamined = 0, stage: IXSCAN
// This is the fastest possible query
```

---

## 3. Document & Schema Optimization

### Document Size Impact

```
┌──────────────────────────────────────────────────────────────┐
│  Document Size     │ Impact                                  │
├────────────────────┼─────────────────────────────────────────┤
│  < 1 KB            │ ✅ Ideal for most workloads             │
│  1-16 KB           │ ✅ Good — typical for rich documents    │
│  16 KB - 1 MB      │ ⚠️ Acceptable — watch for growth       │
│  1-16 MB           │ ❌ Too large — causing slow reads/writes│
│  > 16 MB           │ 💥 Impossible — exceeds BSON limit     │
├────────────────────┴─────────────────────────────────────────┤
│                                                              │
│  Common causes of bloat:                                     │
│  - Unbounded embedded arrays (reviews, logs, messages)      │
│  - Base64-encoded images (use GridFS or S3 instead)         │
│  - Deeply nested objects with redundant data                 │
│  - Not using projection (returning huge docs to client)     │
│                                                              │
│  SQL comparison: Row size is typically < 1KB.                │
│  MongoDB documents can be 100x larger due to embedding.     │
│  This is both a feature (data locality) and a risk.         │
└──────────────────────────────────────────────────────────────┘
```

### Working Set Size (= Buffer Pool in SQL)

```
┌──────────────────────────────────────────────────────────────┐
│  Working Set = Frequently accessed data + indexes           │
│                                                              │
│  If working set fits in RAM:                                │
│  ├── All reads come from memory cache                       │
│  ├── Latency: < 1ms                                         │
│  └── Throughput: 100K+ ops/sec                              │
│                                                              │
│  If working set > RAM:                                      │
│  ├── Reads go to disk (page faults)                         │
│  ├── Latency: 5-50ms                                        │
│  └── Throughput: drops dramatically                          │
│                                                              │
│  Monitor:                                                    │
│  db.serverStatus().wiredTiger.cache                          │
│  "bytes currently in the cache"                              │
│  "maximum bytes configured"                                  │
│  "pages read into cache" (should decrease over time)         │
│                                                              │
│  SQL equivalent:                                             │
│  - PostgreSQL: shared_buffers + OS cache                     │
│  - MySQL: innodb_buffer_pool_size                            │
│  Same concept: Hot data should fit in memory.                │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Read Performance Optimization

### Use Projection

```javascript
// ❌ Returns entire document (10KB each × 1000 docs = 10MB over wire)
const products = await Product.find({ isActive: true }).lean();

// ✅ Returns only needed fields (200 bytes each = 200KB)
const products = await Product.find(
  { isActive: true },
  { name: 1, price: 1, 'category.name': 1, 'ratings.average': 1 }
).lean();
```

### Use lean() in Mongoose

```javascript
// Benchmark comparison (1000 documents):
// Without lean(): ~150ms (creates Mongoose doc instances with change tracking)
// With lean():    ~15ms  (plain JS objects)

// ✅ For API responses (read-only)
const products = await Product.find({}).lean();

// ❌ When you need to save
const product = await Product.findById(id);  // No lean
product.stock -= 1;
await product.save();  // Needs Mongoose document features
```

### Cursor-Based Pagination (for Large Datasets)

```javascript
// ❌ skip() performance degrades with offset
// Page 1: 2ms, Page 100: 50ms, Page 10000: 5000ms

// ✅ Cursor-based: constant O(1) regardless of page depth
app.get('/api/products', async (req, res) => {
  const { cursor, limit = 20 } = req.query;
  const filter = { isActive: true };

  if (cursor) {
    filter._id = { $gt: new ObjectId(cursor) };
  }

  const products = await db.collection('products')
    .find(filter)
    .sort({ _id: 1 })
    .limit(parseInt(limit) + 1)  // Fetch one extra to check hasMore
    .project({ name: 1, price: 1 })
    .toArray();

  const hasMore = products.length > limit;
  if (hasMore) products.pop();

  res.json({
    data: products,
    nextCursor: hasMore ? products[products.length - 1]._id : null,
    hasMore
  });
});
```

---

## 5. Write Performance Optimization

### Bulk Operations

```javascript
// ❌ Individual writes (N network round trips)
for (const item of items) {
  await db.collection('products').updateOne(
    { _id: item._id },
    { $set: { price: item.newPrice } }
  );
}
// 1000 items = 1000 round trips = ~2 seconds

// ✅ Bulk write (1 network round trip)
const ops = items.map(item => ({
  updateOne: {
    filter: { _id: item._id },
    update: { $set: { price: item.newPrice } }
  }
}));
await db.collection('products').bulkWrite(ops, { ordered: false });
// 1000 items = 1 round trip = ~50ms
// ordered: false = parallel execution = even faster
```

### Write Concern Tuning

```javascript
// For non-critical data (analytics, logs):
await db.collection('pageViews').insertOne(
  { pageId, timestamp: new Date(), userId },
  { writeConcern: { w: 0 } }  // Fire-and-forget (fastest, least safe)
);

// For important data (orders):
await db.collection('orders').insertOne(
  orderData,
  { writeConcern: { w: 'majority', j: true } }  // Durable (slowest, safest)
);
```

### Avoid Unnecessary Index Updates

```javascript
// Every write updates ALL indexes on the collection
// 10 indexes = 10 B-tree updates per write

// Monitor index usage:
db.products.aggregate([{ $indexStats: {} }])

// Drop unused indexes:
db.products.dropIndex('idx_rarely_used')
// Each dropped index = ~10% write performance improvement
```

---

## 6. Aggregation Pipeline Optimization

```javascript
// ❌ Slow pipeline — wrong stage order
db.orders.aggregate([
  { $group: { _id: "$status", total: { $sum: "$total" } } },  // Full scan
  { $match: { _id: "completed" } }                             // Filter AFTER
])

// ✅ Optimized — filter first
db.orders.aggregate([
  { $match: { status: "completed" } },    // Uses index, reduces data early
  { $group: { _id: "$status", total: { $sum: "$total" } } }
])

// ✅ More optimization tips:
db.orders.aggregate([
  // 1. $match FIRST (uses index)
  { $match: { status: "completed", createdAt: { $gte: lastMonth } } },

  // 2. $project early to reduce document size flowing through pipeline
  { $project: { total: 1, customerId: 1, createdAt: 1 } },

  // 3. $group on reduced data
  { $group: {
    _id: { $dateToString: { format: "%Y-%m", date: "$createdAt" } },
    revenue: { $sum: { $toDouble: "$total" } },
    orders: { $sum: 1 }
  }},

  // 4. $sort after $group (benefits from $limit)
  { $sort: { _id: -1 } },

  // 5. $limit
  { $limit: 12 }
], { allowDiskUse: true })  // For large datasets that exceed 100MB RAM limit
```

---

## 7. Connection Pool Optimization

```javascript
// MongoDB driver has a built-in connection pool
const client = new MongoClient(uri, {
  maxPoolSize: 50,          // Max concurrent connections
  minPoolSize: 5,           // Keep idle connections warm
  maxIdleTimeMS: 30000,     // Close idle connections after 30s
  waitQueueTimeoutMS: 5000, // Fail if can't get a connection in 5s
  retryWrites: true,
  retryReads: true
});

// Mongoose connection pool
mongoose.connect(uri, {
  maxPoolSize: 50,
  minPoolSize: 5,
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000
});

// Rule of thumb:
// maxPoolSize = number of concurrent request handlers
// For a Node.js server with 100 concurrent requests: maxPoolSize = 50-100
// Each connection uses ~1MB of server memory
```

---

## 8. Caching Strategy

```javascript
const Redis = require('ioredis');
const redis = new Redis();

// Cache-aside pattern (same as SQL caching)
async function getProduct(productId) {
  // 1. Check cache
  const cached = await redis.get(`product:${productId}`);
  if (cached) return JSON.parse(cached);

  // 2. Query database
  const product = await db.collection('products')
    .findOne({ _id: new ObjectId(productId) });

  // 3. Store in cache (TTL: 5 minutes)
  if (product) {
    await redis.set(`product:${productId}`, JSON.stringify(product), 'EX', 300);
  }

  return product;
}

// Invalidate on update
async function updateProduct(productId, updates) {
  await db.collection('products').updateOne(
    { _id: new ObjectId(productId) },
    { $set: updates }
  );
  await redis.del(`product:${productId}`);
}
```

---

## 9. Read from Secondaries

```javascript
// For analytics/reporting that can tolerate slight staleness
const { ReadPreference } = require('mongodb');

// Read from secondary replica
const analytics = await db.collection('orders')
  .find({ status: "completed" })
  .readPreference(ReadPreference.SECONDARY_PREFERRED)
  .toArray();

// Read preferences:
// PRIMARY              → Always primary (default, strongest consistency)
// PRIMARY_PREFERRED     → Primary, fallback to secondary
// SECONDARY            → Always secondary (may read stale data)
// SECONDARY_PREFERRED  → Secondary, fallback to primary
// NEAREST              → Lowest latency node

// SQL equivalent: Read replicas
// PostgreSQL: hot_standby_feedback, recovery_target_timeline
```

---

## Performance Monitoring

```javascript
// Server status (overall health)
db.serverStatus()

// Key metrics:
db.serverStatus().connections        // Active connections
db.serverStatus().opcounters         // Operation counters (insert/query/update/delete)
db.serverStatus().wiredTiger.cache   // Cache hit rate
db.serverStatus().globalLock         // Lock contention

// Collection-level stats
db.products.stats()
// .size          — data size
// .storageSize   — disk usage (with compression)
// .totalIndexSize — index memory usage
// .count         — document count

// Current operations (like SHOW PROCESSLIST)
db.currentOp()
db.currentOp({ "secs_running": { $gt: 5 } })  // Long-running ops

// Kill a slow operation
db.killOp(opId)
```

---

## Real-World Scenario — E-Commerce Performance

```javascript
// Before optimization: Product listing endpoint
// Response time: 800ms, 200 concurrent users → timeout

// Problem analysis:
db.products.find({ isActive: true }).explain("executionStats")
// COLLSCAN (no index), totalDocsExamined: 500,000, nReturned: 20

// Optimization steps:

// 1. Add compound index
db.products.createIndex({ isActive: 1, "category.slug": 1, price: -1 })

// 2. Use projection
db.products.find(
  { isActive: true, "category.slug": "electronics" },
  { name: 1, price: 1, "ratings.average": 1, images: { $slice: 1 } }
).sort({ price: -1 }).limit(20)

// 3. Cursor pagination instead of skip
// 4. Redis cache for category pages (TTL: 2 min)
// 5. .lean() in Mongoose

// After optimization: Response time: 15ms
// 50x improvement from schema + index + projection + caching
```

---

## Common Mistakes

### ❌ Not Monitoring Index Usage

```javascript
// You created 15 indexes but only 5 are used
// The other 10 slow down every write operation
// Check monthly: db.collection.aggregate([{ $indexStats: {} }])
```

### ❌ Returning Full Documents to Frontend

```javascript
// Product document: 15KB (has reviews, specs, metadata)
// API returns full document for product listing
// 100 products × 15KB = 1.5MB per API call
// Solution: Projection → 100 products × 200 bytes = 20KB
```

### ❌ N+1 Query Pattern with populate()

```javascript
// ❌ Populate inside a loop
const orders = await Order.find({ status: 'pending' });
for (const order of orders) {
  order.customer = await Customer.findById(order.customerId);
}
// 100 orders = 101 queries

// ✅ Batch populate
const orders = await Order.find({ status: 'pending' }).populate('customerId', 'name email');
// 2 queries total (orders + all customers in one $in query)

// ✅ Even better: Embed customer snapshot in order (0 extra queries)
```

---

## Practice Exercises

### Exercise 1: Performance Audit
Run `explain("executionStats")` on 5 of your most common queries. For each:
1. Is it using an index? (IXSCAN vs COLLSCAN)
2. What's the docs examined / returned ratio?
3. Create or modify indexes to optimize

### Exercise 2: Projection Impact
Measure the response size and time of an endpoint before and after adding projection. Calculate the reduction percentage.

### Exercise 3: Caching Layer
Add Redis caching to the product detail endpoint:
- Cache individual products with 5-minute TTL
- Invalidate on update
- Add cache-hit header to response

---

## Interview Q&A

**Q1: How do you identify slow queries in MongoDB?**
> Enable the database profiler (`db.setProfilingLevel(1, { slowms: 100 })`), check `db.system.profile`, use `explain("executionStats")` on suspect queries, and monitor with MongoDB Atlas or Ops Manager. Look for COLLSCAN (full collection scan), high `totalDocsExamined / nReturned` ratio, and in-memory sorts.

**Q2: What is the working set and why does it matter?**
> The working set is the frequently accessed data + indexes. If it fits in RAM, all reads come from memory (~0.1ms). If it exceeds RAM, reads go to disk (~5ms). Monitor with `db.serverStatus().wiredTiger.cache`. Size your instances so working set < 80% of available RAM.

**Q3: How does MongoDB compression affect performance?**
> WiredTiger compresses data (snappy default, zstd optional) and indexes (prefix compression). This reduces storage and I/O but adds CPU overhead. Snappy is faster with less compression; zstd gives better compression with more CPU. For read-heavy workloads, compression helps (fewer disk reads); for write-heavy, it can be a bottleneck.

**Q4: When should you use `allowDiskUse: true` in aggregation?**
> When a pipeline stage (usually `$sort` or `$group`) exceeds the 100MB RAM limit. It allows spilling to disk but is slower. Better approach: use `$match` early to reduce data, and `$project` to strip fields. `allowDiskUse` should be a last resort, not a default.

**Q5: How do you handle the N+1 query problem with Mongoose populate?**
> Mongoose batches populated queries (uses `$in`), so it's technically 2 queries instead of N+1. But for hot paths, avoid populate entirely — embed the needed data. For admin/reporting, populate is acceptable. For complex needs, use aggregation with `$lookup` for a single database call.
