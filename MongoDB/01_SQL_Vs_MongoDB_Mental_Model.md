# SQL vs MongoDB — Mental Model

> 📌 **File:** 01_SQL_Vs_MongoDB_Mental_Model.md | **Level:** SQL Expert → MongoDB

---

## What is it?

This is the **single most important chapter** in this entire tutorial. Everything you'll struggle with in MongoDB comes from trying to think in SQL terms. The mental model shift isn't about learning new syntax — it's about fundamentally changing **how you think about data**.

In SQL, you think: *"What entities exist? What are their relationships? Normalize to 3NF."*
In MongoDB, you think: *"What questions will the application ask? Store data the way it will be read."*

---

## The Core Mental Model Shift

```
┌──────────────────────────────────────────────────────────────────┐
│                     SQL THINKING (Data-Driven)                   │
│                                                                  │
│  "What IS the data?"                                             │
│   → Define entities → Normalize → Build relationships            │
│   → Then figure out queries                                      │
│                                                                  │
│  Design FIRST, query LATER                                       │
├──────────────────────────────────────────────────────────────────┤
│                  MONGODB THINKING (Query-Driven)                 │
│                                                                  │
│  "What does the APPLICATION NEED?"                               │
│   → Identify access patterns → Design documents around them     │
│   → Denormalize for read performance                             │
│                                                                  │
│  Query FIRST, design AROUND it                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## SQL Parallel — Think of it like this

### What Maps Well

| SQL Concept         | MongoDB Equivalent     | Notes                                     |
|---------------------|------------------------|--------------------------------------------|
| Database            | Database               | Identical concept                          |
| Table               | Collection             | No schema enforcement by default           |
| Row                 | Document               | Can have nested sub-documents              |
| Column              | Field                  | Fields can vary between documents          |
| PRIMARY KEY         | `_id`                  | Auto-generated ObjectId if not specified   |
| INDEX               | Index                  | Nearly identical syntax and behavior       |
| WHERE               | Query filter `{}`      | JSON-based filter object                   |
| ORDER BY            | `.sort({})`            | Same concept                               |
| LIMIT               | `.limit(n)`            | Same concept                               |
| COUNT(*)            | `.countDocuments()`    | Same concept                               |

### What Does NOT Map

| SQL Concept                      | MongoDB Reality                                      |
|----------------------------------|------------------------------------------------------|
| JOINs (cheap, fast)              | `$lookup` (expensive, avoid in hot paths)            |
| Foreign Keys                     | No foreign keys — referential integrity is YOUR job  |
| Normalization (3NF)              | Denormalization is the default strategy              |
| ALTER TABLE                      | No schema changes needed — just write different docs |
| Multi-table transactions         | Supported but expensive — design to avoid them       |
| Constraints (UNIQUE, NOT NULL)   | Must be manually set up (indexes + validation)       |
| VIEWs                            | `$merge` / `$out` or on-demand materialized views    |
| Stored Procedures                | No equivalent — logic lives in application code      |
| Triggers                         | Change Streams (different model)                     |

---

## Why this is different from SQL (CRITICAL)

### 1. No Joins By Default

In SQL, you split data into tables and JOIN them back:

```sql
-- SQL: 3 tables, 2 JOINs to get an order with customer and product info
SELECT o.id, c.name, p.name, o.quantity
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id
WHERE o.id = 1001;
```

In MongoDB, you **embed related data** in the document itself:

```javascript
// MongoDB: Single document, single read, zero joins
db.orders.findOne({ _id: ObjectId("...") })

// Returns:
{
  _id: ObjectId("..."),
  customer: {
    name: "John Doe",
    email: "john@example.com"
  },
  items: [
    { product: "Laptop", price: 999.99, quantity: 1 },
    { product: "Mouse", price: 29.99, quantity: 2 }
  ],
  total: 1059.97,
  status: "shipped",
  createdAt: ISODate("2024-01-15")
}
```

### 2. Denormalization is the Norm

```
SQL APPROACH (Normalized):
┌──────────┐     ┌──────────┐     ┌──────────┐
│ customers│     │  orders  │     │ products │
│----------│     │----------│     │----------│
│ id   PK  │◄────│ cust_id  │     │ id   PK  │
│ name     │     │ prod_id  │────►│ name     │
│ email    │     │ quantity │     │ price    │
│ address  │     │ total    │     │ category │
└──────────┘     └──────────┘     └──────────┘
                 3 disk seeks, 2 JOINs

MONGODB APPROACH (Denormalized):
┌─────────────────────────────────────┐
│             orders                  │
│─────────────────────────────────────│
│ _id                                 │
│ customer: { name, email }           │  ← Embedded
│ items: [                            │
│   { product: "Laptop", price: 999 } │  ← Embedded
│ ]                                   │
│ total                               │
│ status                              │
└─────────────────────────────────────┘
  1 disk seek, 0 JOINs
```

### 3. Query Patterns Drive Schema Design

In SQL, you design the schema first, then write queries. If a query is slow, you add indexes.

In MongoDB, you **start with the queries**, then design documents to serve them:

```
Step 1: "The product page needs: name, price, reviews, category name"
Step 2: Embed category and recent reviews IN the product document
Step 3: One read serves the entire page

NOT:
Step 1: Create products table, categories table, reviews table
Step 2: JOIN them on every product page load
Step 3: Cache because JOINs are slow
```

### 4. Schema Flexibility (Double-Edged Sword)

```javascript
// MongoDB allows this — two documents in the SAME collection with different shapes
db.products.insertOne({ name: "Laptop", price: 999, specs: { ram: "16GB" } })
db.products.insertOne({ name: "T-Shirt", price: 29, sizes: ["S", "M", "L"], color: "Blue" })

// In SQL, this would require:
// - A products table with nullable columns for all possible fields
// - Or separate tables (electronics, clothing) with shared base table
// - Or an EAV (Entity-Attribute-Value) pattern (nightmare)
```

**Warning:** Flexibility doesn't mean anarchy. You SHOULD enforce schemas (via Mongoose or MongoDB validation) — you just have the option to evolve them without downtime.

---

## How does it work?

### Document Storage Internals

```
┌──────────────────────────────────────────────────────────────┐
│                    Storage Engine (WiredTiger)                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Collection: products                                        │
│  ┌─────────────────────────────────────┐                     │
│  │ Document 1 (BSON binary)            │                     │
│  │ { _id: ObjectId, name: "Laptop" ..} │──► Stored as a     │
│  ├─────────────────────────────────────┤    single unit on   │
│  │ Document 2 (BSON binary)            │    disk. Reading    │
│  │ { _id: ObjectId, name: "Shoes" .. } │    one document =   │
│  ├─────────────────────────────────────┤    one disk seek.   │
│  │ Document 3 (BSON binary)            │                     │
│  │ { _id: ObjectId, name: "Coffee" ..} │                     │
│  └─────────────────────────────────────┘                     │
│                                                              │
│  Index: { name: 1 }                                          │
│  ┌───────────────────┐                                       │
│  │ B-Tree Index       │  ← Same concept as SQL indexes       │
│  │ "Coffee" → Doc 3   │                                      │
│  │ "Laptop" → Doc 1   │                                      │
│  │ "Shoes"  → Doc 2   │                                      │
│  └───────────────────┘                                       │
└──────────────────────────────────────────────────────────────┘
```

### Key Insight: Data Locality

In SQL, one "order" is spread across 3+ tables (orders, order_items, customers, products). Reading it requires:
- 3+ index lookups
- 3+ disk seeks (different table files)
- CPU work to JOIN in memory

In MongoDB, one "order" document is stored **contiguously** on disk. Reading it requires:
- 1 index lookup
- 1 disk seek
- Done.

This is **data locality** — and it's MongoDB's primary performance advantage.

---

## The Two Questions That Decide Your Schema

Before designing any MongoDB collection, ask:

```
┌─────────────────────────────────────────────────────┐
│  Q1: How will the application READ this data?       │
│      → Optimize for the most common read pattern    │
│      → Embed data that's read together              │
│                                                     │
│  Q2: How will the data CHANGE over time?            │
│      → If embedded data changes frequently,         │
│        you'll need to update it everywhere           │
│      → Consider referencing for volatile data        │
└─────────────────────────────────────────────────────┘
```

### Decision Matrix

```
                    Embed                     Reference
                    ─────                     ─────────
Read together?      ✅ Always                 ❌ Rarely
Data changes?       Rarely                    ✅ Frequently
Data size?          Small (< 1MB)             Large / Growing
Relationship?       1:1 or 1:few              1:many or many:many
Example             Order → Shipping Address   User → All Orders (10K+)
```

---

## Real-World Scenario — E-Commerce Product Page

### SQL Approach (5 queries or complex JOIN)

```sql
-- Get product
SELECT * FROM products WHERE id = 42;

-- Get category
SELECT name FROM categories WHERE id = (SELECT category_id FROM products WHERE id = 42);

-- Get reviews (paginated)
SELECT r.*, u.name FROM reviews r
JOIN users u ON r.user_id = u.id
WHERE r.product_id = 42
ORDER BY r.created_at DESC LIMIT 5;

-- Get related products
SELECT p.* FROM products p
JOIN product_relations pr ON p.id = pr.related_id
WHERE pr.product_id = 42 LIMIT 4;

-- Get inventory
SELECT warehouse, quantity FROM inventory WHERE product_id = 42;
```

**Result:** 5 queries, multiple JOINs, multiple disk seeks.

### MongoDB Approach (1 query)

```javascript
db.products.findOne({ _id: ObjectId("...") })

// Returns everything needed for the page:
{
  _id: ObjectId("..."),
  name: "Laptop",
  price: 999.99,
  category: { name: "Electronics", slug: "electronics" },
  specs: { ram: "16GB", storage: "512GB SSD" },
  reviews: [
    { user: "John", rating: 5, text: "Great!", date: ISODate("2024-01-10") },
    { user: "Jane", rating: 4, text: "Good value", date: ISODate("2024-01-08") }
  ],
  relatedProducts: [
    { id: ObjectId("..."), name: "Mouse", price: 29.99 },
    { id: ObjectId("..."), name: "Keyboard", price: 59.99 }
  ],
  inventory: [
    { warehouse: "NYC", quantity: 15 },
    { warehouse: "LA", quantity: 8 }
  ]
}
```

**Result:** 1 query, 1 document, 1 disk seek.

### Node.js API Comparison

```javascript
// SQL approach (Express + pg)
app.get('/api/products/:id', async (req, res) => {
  const { rows: [product] } = await pool.query(
    'SELECT p.*, c.name as category FROM products p JOIN categories c ON p.category_id = c.id WHERE p.id = $1',
    [req.params.id]
  );
  const { rows: reviews } = await pool.query(
    'SELECT r.*, u.name FROM reviews r JOIN users u ON r.user_id = u.id WHERE r.product_id = $1 LIMIT 5',
    [req.params.id]
  );
  product.reviews = reviews;
  res.json(product);
});

// MongoDB approach (Express + native driver)
app.get('/api/products/:id', async (req, res) => {
  const product = await db.collection('products').findOne({
    _id: new ObjectId(req.params.id)
  });
  res.json(product); // Already contains reviews, category, etc.
});
```

---

## Common Mistakes (SQL Developers Make)

### ❌ Mistake 1: Creating a Fully Normalized Schema

```javascript
// DON'T do this — this is SQL thinking in MongoDB
db.orders         // { customer_id, product_id, quantity }
db.customers      // { name, email }
db.products       // { name, price }
db.order_items    // { order_id, product_id, quantity }
db.addresses      // { customer_id, street, city }
// Now you need $lookup everywhere = slow

// DO this — think about what a single page/API needs
db.orders.findOne({})
// {
//   customer: { name, email },       ← embedded
//   items: [{ name, price, qty }],   ← embedded
//   shippingAddress: { street, city } ← embedded
// }
```

### ❌ Mistake 2: Using $lookup Like JOIN

```javascript
// This is NOT how you should think about MongoDB
db.orders.aggregate([
  { $lookup: { from: "customers", localField: "customer_id", foreignField: "_id", as: "customer" } },
  { $lookup: { from: "products", localField: "product_id", foreignField: "_id", as: "product" } },
  { $unwind: "$customer" },
  { $unwind: "$product" }
])
// Slow, defeats the purpose of MongoDB. If you need this, use SQL.
```

### ❌ Mistake 3: Thinking Schema-less Means No Schema

```javascript
// Without any validation, your collection becomes chaos:
{ name: "Laptop", price: 999 }
{ Name: "Mouse", cost: 29 }        // Different field names!
{ name: 123, price: "expensive" }   // Wrong types!

// ALWAYS use Mongoose schemas or MongoDB schema validation
```

---

## Performance Insight

| Scenario                              | SQL        | MongoDB     | Why                                |
|---------------------------------------|------------|-------------|------------------------------------|
| Read single entity + related data     | ⚡ Moderate | ⚡⚡ Fast    | Data locality, no JOINs            |
| Complex reporting across entities     | ⚡⚡ Fast   | ⚡ Moderate  | SQL JOINs are optimized for this   |
| Write-heavy with simple structure     | ⚡ Moderate | ⚡⚡ Fast    | No constraint checking overhead    |
| Transactions across multiple entities | ⚡⚡ Fast   | ⚡ Slower    | Multi-doc transactions are costly  |
| Schema evolution (ALTER TABLE)        | 🐌 Slow    | ⚡⚡ Instant | No migration needed                |
| Full-text search                      | ⚡ Moderate | ⚡ Moderate  | Both have it; Elasticsearch wins   |

---

## Practice Exercises

### Exercise 1: Schema Redesign

Given this SQL schema:

```sql
CREATE TABLE users (id INT PK, name VARCHAR, email VARCHAR);
CREATE TABLE posts (id INT PK, user_id INT FK, title VARCHAR, body TEXT);
CREATE TABLE comments (id INT PK, post_id INT FK, user_id INT FK, text TEXT);
CREATE TABLE likes (id INT PK, post_id INT FK, user_id INT FK);
```

Design a MongoDB document schema for a **blog application** where the primary access pattern is:
- "Show a blog post with author name, comments (with commenter names), and like count"

### Exercise 2: Identify the Anti-Pattern

What's wrong with this MongoDB design?

```javascript
// Collection: users
{ _id: 1, name: "John", email: "john@example.com" }

// Collection: user_addresses
{ _id: 1, user_id: 1, street: "123 Main", city: "NYC" }

// Collection: user_settings
{ _id: 1, user_id: 1, theme: "dark", notifications: true }
```

### Exercise 3: When NOT to Use MongoDB

List 3 scenarios where SQL is clearly the better choice. Explain why using MongoDB would be a mistake.

---

## Interview Q&A

**Q1: When would you choose MongoDB over PostgreSQL?**
> When the application has flexible/evolving schemas, needs horizontal scaling, deals with hierarchical/nested data, or when read performance with data locality is critical. Common examples: content management, IoT data, real-time analytics, user profiles with varying attributes.

**Q2: What's the biggest misconception SQL developers have about MongoDB?**
> That it's "schema-less." In production, you always enforce schemas — either through Mongoose, MongoDB's built-in schema validation, or both. The difference is that schema changes don't require migrations or downtime.

**Q3: How does MongoDB handle relationships without foreign keys?**
> Two strategies: (1) **Embedding** — store related data inside the document (preferred for 1:1, 1:few). (2) **Referencing** — store an ObjectId and use `$lookup` or application-level joins (for 1:many, many:many). There's no referential integrity enforcement — the application must handle orphaned references.

**Q4: Can MongoDB replace SQL entirely?**
> No. MongoDB is not suitable for: financial transactions requiring strict ACID across many entities, complex reporting with many JOINs, applications where referential integrity is critical (banking, ERP), legacy systems designed around relational schemas.

**Q5: What is data locality and why does it matter?**
> Data locality means storing related data physically close together on disk. When a product document contains its reviews, specs, and category — all are fetched in a single disk read. In SQL, this data would be spread across 4 tables requiring 4 separate disk seeks and CPU-intensive JOINs.

---

## Key Takeaway

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  SQL:   "How is my data STRUCTURED?"                           │
│         Design tables → Normalize → Write queries              │
│                                                                 │
│  Mongo: "How does my APPLICATION USE this data?"               │
│         Define access patterns → Design documents → Done        │
│                                                                 │
│  Neither is "better." They solve different problems.            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
