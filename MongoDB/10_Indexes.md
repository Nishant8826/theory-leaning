# Indexes

> 📌 **File:** 10_Indexes.md | **Level:** SQL Expert → MongoDB

---

## What is it?

Indexes in MongoDB work almost identically to SQL indexes — B-tree data structures that speed up queries at the cost of slower writes and additional storage. If you understand SQL indexes, you understand 80% of MongoDB indexes. The key differences: **multikey indexes** (automatic indexing of array elements), **compound index ordering**, and the absence of clustered indexes.

---

## SQL Parallel — Think of it like this

```
SQL:                                       MongoDB:
CREATE INDEX idx ON t(col)               → db.t.createIndex({ col: 1 })
CREATE INDEX idx ON t(a, b)              → db.t.createIndex({ a: 1, b: 1 })
CREATE UNIQUE INDEX idx ON t(email)      → db.t.createIndex({ email: 1 }, { unique: true })
DROP INDEX idx ON t                      → db.t.dropIndex("idx_name")
EXPLAIN SELECT ...                       → db.t.find(...).explain()
CREATE INDEX CONCURRENTLY (PG)           → Default behavior (background)
SHOW INDEX FROM t                        → db.t.getIndexes()
Partial Index (PG: WHERE)                → Partial Index (partialFilterExpression)
Expression Index (PG)                    → Not directly supported
Full-text Index                          → db.t.createIndex({ field: "text" })
Spatial Index (PostGIS)                  → db.t.createIndex({ loc: "2dsphere" })
```

---

## Why this is different from SQL (CRITICAL)

### 1. Multikey Indexes (No SQL Equivalent)

```javascript
// MongoDB automatically creates a multikey index when the field is an array
db.products.createIndex({ tags: 1 })

// This index covers ALL elements of the tags array
db.products.find({ tags: "electronics" })  // Uses the index
db.products.find({ tags: "sale" })          // Also uses the index

// In SQL, you'd need a separate table:
// CREATE TABLE product_tags (product_id INT, tag VARCHAR);
// CREATE INDEX idx_tag ON product_tags(tag);
```

### 2. Compound Index Order Matters More

```javascript
// Index: { a: 1, b: 1, c: 1 }
// This index supports (left-prefix rule — same as SQL):
db.t.find({ a: "x" })                    // ✅ Uses index
db.t.find({ a: "x", b: "y" })            // ✅ Uses index
db.t.find({ a: "x", b: "y", c: "z" })    // ✅ Uses index
db.t.find({ b: "y" })                    // ❌ Cannot use index
db.t.find({ b: "y", c: "z" })            // ❌ Cannot use index
db.t.find({ a: "x", c: "z" })            // ⚠️ Partial — uses a only

// Sort direction matters (different from SQL):
// Index: { price: 1, name: 1 }
db.t.find().sort({ price: 1, name: 1 })   // ✅ Uses index (matching directions)
db.t.find().sort({ price: -1, name: -1 }) // ✅ Uses index (both reversed = OK)
db.t.find().sort({ price: 1, name: -1 })  // ❌ Cannot use index (mixed directions)
// For mixed sorts, create: { price: 1, name: -1 }
```

### 3. No Clustered Index

```
SQL (InnoDB):
  - Data IS the primary key index (clustered)
  - Secondary indexes point to the primary key
  - Table scan = primary key scan

MongoDB (WiredTiger):
  - Data is stored separately from indexes
  - _id index is just another index (not clustered)
  - All indexes point directly to documents
  - No "table scan" vs "index scan" distinction on _id
  
  Exception: MongoDB 5.3+ supports "clustered collections"
  db.createCollection("t", { clusteredIndex: { key: { _id: 1 }, unique: true } })
```

---

## How does it work?

### B-Tree Index Structure

```
Index: { price: 1 }

          ┌─────────────────────┐
          │  [500]              │         Root
          └──────┬──────────────┘
         ┌───────┴────────┐
    ┌────▼────┐      ┌────▼────┐
    │ [100,300]│      │[700,999]│         Internal
    └─┬───┬───┘      └─┬───┬───┘
   ┌──▼─┐ ┌▼──┐    ┌──▼─┐ ┌▼──┐
   │ 29 │ │199│    │ 599│ │999│         Leaf → Document Pointers
   │ 49 │ │299│    │ 699│ │   │
   │ 79 │ │399│    │ 799│ │   │
   └────┘ └───┘    └────┘ └───┘

Query: { price: { $gt: 200, $lt: 600 } }
→ Navigate to 200, scan right until 600
→ Only reads relevant leaf nodes (index scan)
→ Without index: reads EVERY document (collection scan)
```

### Index Size and Memory

```
┌──────────────────────────────────────────────────────────────┐
│  Rule: Indexes should fit in RAM for optimal performance.   │
│                                                             │
│  If index > RAM: MongoDB pages index from disk              │
│  = Dramatic slowdown                                        │
│                                                             │
│  Check index sizes:                                         │
│  db.products.stats().totalIndexSize                         │
│  db.products.stats().indexSizes                             │
│                                                             │
│  Example: 10M products × { price: 1 } index                │
│  ≈ 10M × ~20 bytes per entry = ~200MB                      │
│  This should fit in RAM easily.                             │
│                                                             │
│  Example: 10M products × { name: 1 } index                 │
│  ≈ 10M × ~100 bytes (avg name length) = ~1GB               │
│  Might not fit in RAM on small instances.                   │
└──────────────────────────────────────────────────────────────┘
```

---

## Syntax — All Index Types

### Single Field Index

```javascript
// Ascending
db.products.createIndex({ price: 1 })

// Descending (matters for sort operations)
db.products.createIndex({ createdAt: -1 })

// With name
db.products.createIndex({ price: 1 }, { name: "idx_price" })
```

### Compound Index

```javascript
// Equivalent to SQL: CREATE INDEX idx ON products(category, price, rating)
db.products.createIndex({
  "category.name": 1,   // First: equality
  price: -1,             // Second: range/sort
  "ratings.average": -1  // Third: additional filter
})

// ESR Rule (Equality → Sort → Range):
// 1. Equality fields first (exact match)
// 2. Sort fields next
// 3. Range fields last
// This is the optimal index field order for most queries.
```

### Unique Index

```javascript
// SQL: CREATE UNIQUE INDEX idx ON customers(email)
db.customers.createIndex({ email: 1 }, { unique: true })

// Duplicate email → E11000 error (like SQL's unique constraint violation)

// Compound unique
db.products.createIndex({ sku: 1, warehouse: 1 }, { unique: true })
// Combination of sku + warehouse must be unique
```

### Partial Index

```javascript
// SQL (PostgreSQL): CREATE INDEX idx ON products(name) WHERE is_active = true;
db.products.createIndex(
  { name: 1 },
  { partialFilterExpression: { isActive: true, stock: { $gt: 0 } } }
)
// Index only contains active, in-stock products
// Smaller index = less memory = faster queries

// ⚠️ Query must include the partial filter for the index to be used:
db.products.find({ name: "Laptop", isActive: true, stock: { $gt: 0 } }) // ✅ Uses index
db.products.find({ name: "Laptop" })  // ❌ Cannot use partial index
```

### Sparse Index

```javascript
// Index only documents where the field EXISTS
db.products.createIndex({ discount: 1 }, { sparse: true })
// Documents without "discount" field are NOT in the index

// ⚠️ Queries with sort on sparse-indexed field may skip documents:
db.products.find().sort({ discount: 1 })
// May not return documents without "discount" field!
```

### Text Index

```javascript
// SQL: CREATE INDEX idx ON products USING gin(to_tsvector('english', name || description));
db.products.createIndex({
  name: "text",
  description: "text"
}, {
  weights: { name: 10, description: 5 },  // Name matches rank higher
  default_language: "english"
})

// Usage
db.products.find({ $text: { $search: "gaming laptop" } })
db.products.find(
  { $text: { $search: "gaming laptop" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } })

// ⚠️ Only ONE text index per collection
```

### Geospatial Index

```javascript
// SQL: CREATE INDEX idx ON stores USING gist(location);
db.stores.createIndex({ location: "2dsphere" })

// Store location as GeoJSON
db.stores.insertOne({
  name: "Downtown Store",
  location: {
    type: "Point",
    coordinates: [-73.97, 40.77]  // [longitude, latitude]
  }
})

// Find within radius
db.stores.find({
  location: {
    $near: {
      $geometry: { type: "Point", coordinates: [-73.97, 40.77] },
      $maxDistance: 5000  // 5km in meters
    }
  }
})
```

### TTL Index

```javascript
// Auto-delete documents after time period
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 })
// Documents deleted ~60 seconds after createdAt + 3600 seconds
```

### Wildcard Index

```javascript
// Index all fields in a document (useful for schema-less data)
db.products.createIndex({ "$**": 1 })
// Indexes EVERY field in every document

// Specific subdocument
db.products.createIndex({ "specs.$**": 1 })
// Indexes all fields within specs: specs.ram, specs.cpu, specs.storage, etc.

// No SQL equivalent — because SQL schemas are fixed
```

---

## Index Management

```javascript
// List all indexes
db.products.getIndexes()

// Drop index by name
db.products.dropIndex("idx_price")

// Drop all indexes (except _id)
db.products.dropIndexes()

// Rebuild indexes
db.products.reIndex()  // ⚠️ Locks collection

// Hide index (test impact without dropping)
db.products.hideIndex("idx_price")    // Index exists but ignored by planner
db.products.unhideIndex("idx_price")  // Re-enable
```

---

## Explain Plans (= EXPLAIN ANALYZE)

```javascript
// Basic explain
db.products.find({ price: { $gt: 100 } }).explain()

// Detailed with execution stats
db.products.find({ price: { $gt: 100 } }).explain("executionStats")

// Full verbosity
db.products.find({ price: { $gt: 100 } }).explain("allPlansExecution")
```

### Reading the Explain Output

```javascript
// Key fields:
{
  "executionStats": {
    "executionTimeMillis": 2,         // Total time
    "nReturned": 50,                   // Documents returned
    "totalDocsExamined": 50,           // Documents read from disk
    "totalKeysExamined": 50            // Index entries scanned
  },
  "winningPlan": {
    "stage": "IXSCAN",                // ✅ Good — using index
    // vs "COLLSCAN"                   // ❌ Bad — full scan
    "indexName": "idx_price",
    "direction": "forward"
  }
}

// Performance rules:
// totalKeysExamined ≈ nReturned → ✅ Efficient
// totalDocsExamined ≈ nReturned → ✅ Efficient
// totalDocsExamined >> nReturned → ❌ Index not selective enough
// totalDocsExamined = 0 → 🏆 COVERED QUERY (best possible)
```

---

## Node.js Using MongoDB Driver (REQUIRED)

```javascript
async function indexOperations() {
  const db = client.db('ecommerce');
  const products = db.collection('products');

  // Create indexes
  await products.createIndex({ price: 1 }, { name: 'idx_price' });
  await products.createIndex({ 'category.name': 1, price: -1 }, { name: 'idx_cat_price' });
  await products.createIndex({ email: 1 }, { unique: true, name: 'idx_email_unique' });
  await products.createIndex(
    { name: 1 },
    { partialFilterExpression: { isActive: true }, name: 'idx_active_name' }
  );
  await products.createIndex(
    { name: 'text', description: 'text' },
    { weights: { name: 10, description: 5 } }
  );

  // List indexes
  const indexes = await products.listIndexes().toArray();
  console.log('Indexes:', indexes.map(i => `${i.name}: ${JSON.stringify(i.key)}`));

  // Check query performance
  const explanation = await products
    .find({ 'category.name': 'Electronics', price: { $gt: 100 } })
    .explain('executionStats');

  console.log('Stage:', explanation.executionStats.executionStages?.stage);
  console.log('Docs examined:', explanation.executionStats.totalDocsExamined);
  console.log('Keys examined:', explanation.executionStats.totalKeysExamined);
  console.log('Returned:', explanation.executionStats.nReturned);

  // Drop index
  await products.dropIndex('idx_price');
}
```

---

## Real-World Scenario — E-Commerce Index Strategy

```javascript
// Products collection — optimized index set
const products = db.collection('products');

// 1. Category browsing: GET /products?category=Electronics&sort=price
await products.createIndex({ 'category.slug': 1, price: 1 });

// 2. Search by name: GET /products?search=laptop
await products.createIndex({ name: 'text', description: 'text' });

// 3. Brand + price filtering: GET /products?brand=Dell&minPrice=500
await products.createIndex({ brand: 1, price: 1 });

// 4. Admin: find by SKU
await products.createIndex({ sku: 1 }, { unique: true });

// 5. Background: clean up inactive products
await products.createIndex(
  { updatedAt: 1 },
  { partialFilterExpression: { isActive: false } }
);

// Orders collection
const orders = db.collection('orders');

// 1. Customer order history: GET /orders?customerId=xxx
await orders.createIndex({ customerId: 1, createdAt: -1 });

// 2. Order status dashboard: GET /orders?status=pending
await orders.createIndex({ status: 1, createdAt: -1 });

// 3. Revenue reporting: aggregate by date range
await orders.createIndex({ createdAt: 1, total: 1 });
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────────┐
│  Index Type         │ Write Penalty  │ Read Benefit  │ Storage  │
├─────────────────────┼────────────────┼───────────────┼──────────┤
│  No indexes         │ ⚡ None        │ 🐌 Full scans │ None     │
│  1-2 indexes        │ ⚡ Minimal     │ ⚡ Fast        │ Small    │
│  5-10 indexes       │ ⚡ Moderate    │ ⚡ Fast        │ Medium   │
│  20+ indexes        │ 🐌 Significant │ ⚡ Fast        │ Large    │
├─────────────────────┴────────────────┴───────────────┴──────────┤
│                                                                  │
│  Rule of thumb:                                                 │
│  - Read-heavy apps (blogs, e-commerce): More indexes OK         │
│  - Write-heavy apps (IoT, logging): Minimize indexes            │
│  - Each index adds ~10-30% write overhead                       │
│  - Monitor with: db.products.stats().totalIndexSize             │
│  - Target: Total index size < available RAM                     │
│                                                                  │
│  Same trade-offs as SQL — nothing new here.                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Mistake 1: Index Everything

```javascript
// Don't create indexes you never query on
db.products.createIndex({ brand: 1 })
db.products.createIndex({ color: 1 })
db.products.createIndex({ weight: 1 })
db.products.createIndex({ material: 1 })
// 4 indexes that slow down every insert/update

// ✅ Only index fields you filter, sort, or join on
```

### ❌ Mistake 2: Wrong Compound Index Order

```javascript
// Query: find by category AND sort by price
db.products.find({ "category.name": "Electronics" }).sort({ price: -1 })

// ❌ Wrong order — can't use index for sort
db.products.createIndex({ price: -1, "category.name": 1 })

// ✅ Correct order — ESR: Equality first, then Sort
db.products.createIndex({ "category.name": 1, price: -1 })
```

### ❌ Mistake 3: Not Checking explain()

```javascript
// If you don't check, you won't know your query is slow
// Always verify critical queries use indexes:
db.products.find({ price: { $gt: 100 } }).explain('executionStats')
// Look for: COLLSCAN (bad) vs IXSCAN (good)
```

---

## Practice Exercises

### Exercise 1: Create an optimal index for this query:
```javascript
db.orders.find({
  customerId: ObjectId("..."),
  status: "shipped",
  createdAt: { $gte: new Date("2024-01-01") }
}).sort({ createdAt: -1 })
```

### Exercise 2: Analyze and fix this slow query using explain():
```javascript
db.products.find({
  "category.name": "Electronics",
  price: { $gte: 100, $lte: 1000 },
  stock: { $gt: 0 }
}).sort({ "ratings.average": -1 })
```

### Exercise 3: Design a complete index strategy for a blog application with: posts, comments, users, tags. Consider the top 5 most common queries.

---

## Interview Q&A

**Q1: What is the ESR rule for compound indexes?**
> Equality fields first, Sort fields second, Range fields last. `{ status: 1, createdAt: -1, price: 1 }` for a query that filters by status (equality), sorts by createdAt (sort), and ranges on price. This maximizes index efficiency.

**Q2: What is a multikey index?**
> When you index an array field, MongoDB creates an index entry for EACH element of the array. `createIndex({ tags: 1 })` creates entries for every tag in every document. A compound index can have at most ONE multikey (array) field.

**Q3: How do partial indexes improve performance?**
> They only index documents matching a filter expression. An index on `{ name: 1 }` with `partialFilterExpression: { isActive: true }` only indexes active products — smaller index, less memory, faster queries. SQL equivalent: PostgreSQL's `CREATE INDEX ... WHERE`.

**Q4: What's the difference between a covered query and an index scan?**
> An index scan (IXSCAN) reads the index to find document locations, then fetches documents from disk. A covered query reads ONLY the index — all fields needed are in the index, so no document fetch occurs. Covered queries are the fastest possible queries.

**Q5: When should you NOT create an index?**
> When: (1) The field has very low cardinality (e.g., boolean — only 2 values). (2) The collection is small (< 1000 docs). (3) Write throughput is critical and reads are rare. (4) The field is rarely queried. (5) The query uses `$ne` or `$nin` which have poor index selectivity.
