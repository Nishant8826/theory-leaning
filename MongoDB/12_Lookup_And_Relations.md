# $lookup & Relations

> 📌 **File:** 12_Lookup_And_Relations.md | **Level:** SQL Expert → MongoDB

---

## What is it?

`$lookup` is MongoDB's closest equivalent to SQL's `JOIN`. It performs a left outer join between two collections within the same database. However, unlike SQL JOINs which are a core design pattern, `$lookup` is a **last resort** in MongoDB — used when embedding isn't practical.

**SQL mindset:** "Normalize data, JOIN at query time."
**MongoDB mindset:** "Embed data, avoid JOINs entirely. Use $lookup only when you must."

---

## SQL Parallel — Think of it like this

```
SQL:                                     MongoDB:
INNER JOIN                             → $lookup + $unwind + $match
LEFT JOIN                              → $lookup (default is left outer)
RIGHT JOIN                             → ❌ Not supported (reverse the $lookup)
FULL OUTER JOIN                        → ❌ Not supported
CROSS JOIN                             → ❌ Not supported
Self JOIN                              → $lookup on same collection
Subquery in WHERE                      → $lookup + pipeline with $match
Correlated subquery                    → $lookup with let + pipeline
JOIN ... ON a.id = b.foreign_id       → $lookup with localField/foreignField
```

---

## Why this is different from SQL (CRITICAL)

### 1. $lookup is Expensive

```
SQL JOINs:
  - Optimized by query planner (hash join, merge join, nested loop)
  - Can use indexes on both sides
  - Built into the core engine

$lookup:
  - Uses nested loop join only
  - Index on foreign collection helps, but no hash/merge joins
  - Runs as aggregation stage (not core query engine)
  - Performance degrades with large collections
  
  In practice: $lookup is 5-50x slower than SQL JOINs for the same data.
```

### 2. $lookup Only Works Within Same Database

```javascript
// ✅ Works: same database
db.orders.aggregate([
  { $lookup: { from: "customers", ... } }  // customers in same DB
])

// ❌ Cannot join across databases
// No cross-database joins in MongoDB
// In SQL: SELECT * FROM db1.table1 JOIN db2.table2 ...
```

### 3. You Should Design to Avoid $lookup

```
If you need $lookup on every query for a collection,
your schema design is wrong for MongoDB.

Either:
  1. Embed the data (denormalize)
  2. Use application-level joins (multiple queries)
  3. Consider if SQL is the better choice for this workload
```

---

## Syntax

### Basic $lookup (Simple Equality Join)

```javascript
// SQL: SELECT o.*, c.* FROM orders o LEFT JOIN customers c ON o.customer_id = c._id;

db.orders.aggregate([
  { $lookup: {
    from: "customers",           // "Foreign" collection (the table to join)
    localField: "customerId",    // Field in orders (FK)
    foreignField: "_id",         // Field in customers (PK)
    as: "customer"               // Output array field name
  }},
  // $lookup always produces an ARRAY (even for 1:1)
  { $unwind: "$customer" }       // Flatten the array to a single object
])
```

### Pipeline $lookup (Correlated Subquery)

```javascript
// SQL: SELECT o.*, (SELECT name FROM customers WHERE id = o.customer_id) as customer_name

db.orders.aggregate([
  { $lookup: {
    from: "customers",
    let: { custId: "$customerId" },        // Variables from the outer document
    pipeline: [                              // Run this pipeline on customers
      { $match: {
        $expr: { $eq: ["$_id", "$$custId"] } // Match using the variable
      }},
      { $project: { name: 1, email: 1 } }   // Only return needed fields
    ],
    as: "customer"
  }},
  { $unwind: "$customer" }
])

// This is more powerful than basic $lookup because you can:
// - Filter the joined collection
// - Project specific fields
// - Sort and limit the joined results
// - Run additional stages on the joined data
```

### Multi-Collection Join

```javascript
// SQL: SELECT o.*, c.name, p.name FROM orders o
//      JOIN customers c ON o.customer_id = c.id
//      JOIN products p ON o.product_id = p.id;

db.orders.aggregate([
  // Join customers
  { $lookup: {
    from: "customers",
    localField: "customerId",
    foreignField: "_id",
    as: "customer"
  }},
  { $unwind: "$customer" },

  // Unwind items array (each item has a productId)
  { $unwind: "$items" },

  // Join products for each item
  { $lookup: {
    from: "products",
    localField: "items.productId",
    foreignField: "_id",
    as: "items.productDetails"
  }},
  { $unwind: "$items.productDetails" },

  // Reshape
  { $project: {
    orderDate: "$createdAt",
    customerName: "$customer.name",
    productName: "$items.productDetails.name",
    quantity: "$items.quantity",
    unitPrice: "$items.unitPrice"
  }}
])

// ⚠️ This is SLOW. If you need this pattern often, your schema is wrong.
// Embed customer name and product name in the order document instead.
```

---

## Relationship Patterns in MongoDB

### 1. One-to-One → Embed

```javascript
// SQL: users table + user_settings table (1:1 FK)
// MongoDB: Embed settings in user document

{
  _id: ObjectId("..."),
  name: "John",
  email: "john@example.com",
  settings: {                    // Embedded 1:1
    theme: "dark",
    notifications: true,
    language: "en"
  }
}
// Zero joins needed. Single read.
```

### 2. One-to-Few → Embed

```javascript
// SQL: users + addresses (1:few, max ~5)
// MongoDB: Embed array

{
  _id: ObjectId("..."),
  name: "John",
  addresses: [                   // Embedded 1:few
    { label: "home", street: "123 Main", city: "NYC" },
    { label: "work", street: "456 Office", city: "NYC" }
  ]
}
```

### 3. One-to-Many → Reference or Hybrid

```javascript
// SQL: users + orders (1:many, potentially thousands)
// MongoDB: Reference (avoid unbounded arrays)

// Orders collection
{
  _id: ObjectId("..."),
  customerId: ObjectId("user123"),   // Reference to customer
  customer: {                         // Denormalized snapshot
    name: "John Doe",
    email: "john@example.com"
  },
  items: [...],
  total: 199.99
}

// Query: Get orders for a customer (no $lookup needed)
db.orders.find({ customerId: ObjectId("user123") })
```

### 4. Many-to-Many → Array of References or Junction Collection

```javascript
// SQL: students + courses + enrollment table (M:N)
// MongoDB Option 1: Array of references
{
  _id: ObjectId("student1"),
  name: "Alice",
  enrolledCourses: [ObjectId("course1"), ObjectId("course2")]
}

// MongoDB Option 2: Embed denormalized data
{
  _id: ObjectId("student1"),
  name: "Alice",
  enrolledCourses: [
    { courseId: ObjectId("course1"), name: "Math 101", instructor: "Dr. Smith" },
    { courseId: ObjectId("course2"), name: "CS 201", instructor: "Prof. Jones" }
  ]
}
```

---

## Node.js Using MongoDB Driver (REQUIRED)

```javascript
// Application-level join (often faster than $lookup)
app.get('/api/orders/:id', async (req, res) => {
  const db = getDB();
  
  // Option 1: If data is embedded (PREFERRED)
  const order = await db.collection('orders').findOne({
    _id: new ObjectId(req.params.id)
  });
  // order already contains customer info, item details — done!

  // Option 2: Application-level join (when references exist)
  const order2 = await db.collection('orders').findOne({
    _id: new ObjectId(req.params.id)
  });
  const [customer, products] = await Promise.all([
    db.collection('customers').findOne({ _id: order2.customerId }),
    db.collection('products').find({
      _id: { $in: order2.items.map(i => i.productId) }
    }).toArray()
  ]);
  order2.customer = customer;
  order2.items = order2.items.map(item => ({
    ...item,
    product: products.find(p => p._id.equals(item.productId))
  }));

  // Option 3: $lookup in aggregation
  const [order3] = await db.collection('orders').aggregate([
    { $match: { _id: new ObjectId(req.params.id) } },
    { $lookup: {
      from: 'customers',
      localField: 'customerId',
      foreignField: '_id',
      as: 'customer'
    }},
    { $unwind: '$customer' },
    { $lookup: {
      from: 'products',
      localField: 'items.productId',
      foreignField: '_id',
      as: 'productDetails'
    }}
  ]).toArray();

  res.json(order); // Use whichever option fits your schema
});
```

---

## Real-World Scenario — Order History with Product Details

### SQL Approach (Natural)

```sql
SELECT o.id, o.created_at, o.total, o.status,
       c.name as customer_name,
       oi.quantity, oi.unit_price,
       p.name as product_name, p.image
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.customer_id = 42
ORDER BY o.created_at DESC
LIMIT 10;
```

### MongoDB Approach (Recommended — Embedded)

```javascript
// Schema designed for this query:
// Order document already contains everything
db.orders.find({ customerId: ObjectId("...") })
  .sort({ createdAt: -1 })
  .limit(10)
  .toArray()

// Each order already contains:
{
  customerId: ObjectId("..."),
  customer: { name: "John", email: "john@example.com" },
  items: [
    { productId: ObjectId("..."), name: "Laptop", image: "/img/laptop.jpg",
      unitPrice: 999.99, quantity: 1 }
  ],
  total: 999.99,
  status: "delivered",
  createdAt: ISODate("2024-01-15")
}
// ZERO joins. ONE index ({ customerId: 1, createdAt: -1 }). Done.
```

---

## Performance Insight

```
┌───────────────────────────────────────────────────────────────┐
│  Join Strategy           │ Performance    │ When to Use       │
├──────────────────────────┼────────────────┼───────────────────┤
│  Embedded (no join)      │ ⚡⚡⚡ Fastest  │ Default choice    │
│  Application join        │ ⚡⚡ Fast       │ Few docs, cached  │
│  $lookup (simple)        │ ⚡ Moderate     │ Rare lookups      │
│  $lookup (pipeline)      │ 🐌 Slow        │ Complex joins     │
│  Multiple $lookups       │ 🐌🐌 Very slow │ Avoid — redesign  │
├──────────────────────────┴────────────────┴───────────────────┤
│                                                               │
│  $lookup optimization tips:                                   │
│  1. Create index on foreignField in the "from" collection    │
│  2. Use pipeline $lookup with $match to filter early          │
│  3. Add $project in pipeline to limit returned fields        │
│  4. $unwind immediately after $lookup if expecting 1 result  │
│  5. If $lookup is in every query, REDESIGN your schema       │
│                                                               │
│  SQL comparison: A 3-table JOIN in PostgreSQL: ~2ms           │
│  Same data with 3 $lookups in MongoDB: ~20-50ms              │
│  Same data embedded (no joins): ~0.5ms                        │
└───────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Using $lookup Like SQL JOINs

```javascript
// ❌ This is SQL thinking — you're fighting MongoDB
db.orders.aggregate([
  { $lookup: { from: "customers", ... } },
  { $lookup: { from: "products", ... } },
  { $lookup: { from: "shipping", ... } },
  { $lookup: { from: "payments", ... } }
])
// 4 joins = use SQL instead, or redesign your MongoDB schema

// ✅ Embed what you need in the order document
```

### ❌ Not Indexing the Foreign Field

```javascript
// $lookup joins on foreignField — it NEEDS an index
// Without index: full collection scan on every $lookup

// ✅ Always index the foreign field
db.customers.createIndex({ _id: 1 })  // Already exists (default)
db.products.createIndex({ _id: 1 })   // Already exists (default)
db.orders.createIndex({ customerId: 1 }) // Add for reverse lookups
```

---

## Practice Exercises

### Exercise 1: Convert SQL JOIN to $lookup

```sql
SELECT p.name, c.name as category_name
FROM products p
JOIN categories c ON p.category_id = c._id
WHERE p.price > 100
ORDER BY p.price DESC;
```

### Exercise 2: Redesign to Avoid $lookup

Given collections `users`, `posts`, `comments` that all reference each other by ID, redesign the schema so that displaying a blog post (with author name and latest 5 comments with commenter names) requires ZERO $lookups.

### Exercise 3: Application-Level Join

Write a Node.js function that fetches an order with full product details using application-level joins (Promise.all) instead of $lookup. Compare performance with the $lookup version.

---

## Interview Q&A

**Q1: Why are $lookups slower than SQL JOINs?**
> MongoDB uses nested loop joins only (no hash or merge joins). The join runs as an aggregation stage, not in the core query engine. The foreign collection is queried for each document in the input stage. SQL query planners choose optimal join strategies based on data statistics.

**Q2: When is $lookup acceptable to use?**
> For infrequent queries (admin reports, analytics). For data that changes too frequently to embed (user profiles referenced by many collections). For many-to-many relationships where embedding would create excessive duplication. Never on hot read paths.

**Q3: What's the difference between simple $lookup and pipeline $lookup?**
> Simple `$lookup` joins on equality of two fields (localField = foreignField). Pipeline `$lookup` lets you run a full aggregation pipeline on the foreign collection, including filtering, sorting, projecting, and even nested $lookups. Pipeline version is more flexible but slower.

**Q4: How do you handle data consistency with denormalized/embedded data?**
> Options: (1) Accept eventual consistency — update embedded copies in background jobs. (2) Use Change Streams to propagate updates in real-time. (3) For critical data, store a reference AND a denormalized copy — verify on read if needed. (4) For data that rarely changes (category names), denormalization is nearly free.

**Q5: Can you do a self-join in MongoDB?**
> Yes, using `$lookup` with `from` pointing to the same collection. Example: finding employees and their managers when both are in the same collection. Use `$graphLookup` for recursive self-joins (like SQL's recursive CTE).
