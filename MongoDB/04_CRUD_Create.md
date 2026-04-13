# CRUD — Create

> 📌 **File:** 04_CRUD_Create.md | **Level:** SQL Expert → MongoDB

---

## What is it?

Create operations in MongoDB insert documents into collections. Unlike SQL's `INSERT INTO` which requires a predefined table schema, MongoDB's insert operations accept any valid BSON document — the collection is created automatically on first insert.

---

## SQL Parallel — Think of it like this

```
SQL:                                    MongoDB:
INSERT INTO t (c1, c2) VALUES (v1, v2)  → db.t.insertOne({ c1: v1, c2: v2 })
INSERT INTO t VALUES (...), (...), (...)→ db.t.insertMany([{...}, {...}, {...}])
INSERT ... ON DUPLICATE KEY UPDATE      → db.t.updateOne({}, {}, { upsert: true })
INSERT ... SELECT                       → db.t.insertMany(db.other.find().toArray())
LOAD DATA INFILE                        → mongoimport
COPY (PostgreSQL)                       → mongoimport
```

**What maps well:** Single/batch inserts, auto-generated IDs, bulk operations.
**What doesn't map:** No `INSERT ... SELECT` equivalent. No `DEFAULT` column values (handled by app/ODM). No `RETURNING` clause (use `insertedId`).

---

## Why this is different from SQL (CRITICAL)

### 1. No Schema Validation by Default

```sql
-- SQL: Schema enforces types and constraints
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL CHECK (price > 0),
  category_id INT REFERENCES categories(id)
);
-- INSERT with bad data → ERROR
INSERT INTO products (name, price) VALUES (NULL, -5);
-- ERROR: null value violates not-null constraint
```

```javascript
// MongoDB: No constraints by default
db.products.insertOne({ name: null, price: -5 })  // ✅ Accepted!
db.products.insertOne({ banana: "yes" })           // ✅ Also accepted!
// You MUST add validation manually (covered in file 16)
```

### 2. _id is Mandatory and Unique

```javascript
// MongoDB auto-generates _id if you don't provide it
db.products.insertOne({ name: "Laptop" })
// → { _id: ObjectId("..."), name: "Laptop" }

// Providing duplicate _id = Error (like PRIMARY KEY violation)
db.products.insertOne({ _id: 1, name: "Mouse" })
db.products.insertOne({ _id: 1, name: "Keyboard" })
// MongoServerError: E11000 duplicate key error
```

### 3. No Auto-Increment

```sql
-- SQL: AUTO_INCREMENT / SERIAL
CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(255));
INSERT INTO products (name) VALUES ('Laptop'); -- id = 1
INSERT INTO products (name) VALUES ('Mouse');  -- id = 2
```

```javascript
// MongoDB: ObjectId (12-byte, globally unique, sortable by time)
// No sequential 1, 2, 3... This is BY DESIGN for distributed systems.
// If you need sequential IDs, you must implement a counter yourself.
```

---

## How does it work?

### Insert Flow (Internal)

```
Client                    MongoDB Server                    Storage
  │                            │                               │
  │  insertOne({...})          │                               │
  │ ──────────────────────►    │                               │
  │                            │  1. Validate BSON             │
  │                            │  2. Generate _id if missing   │
  │                            │  3. Check unique indexes      │
  │                            │  4. Write to journal (WAL)    │
  │                            │  ──────────────────────────►  │
  │                            │  5. Write to collection       │
  │                            │  6. Update indexes            │
  │                            │  ──────────────────────────►  │
  │  { acknowledged: true,     │                               │
  │    insertedId: ObjectId }  │                               │
  │ ◄──────────────────────    │                               │
```

### Write Concern (Durability Guarantee)

```
┌─────────────────────────────────────────────────────────────┐
│  Write Concern    │ SQL Equivalent        │ Speed │ Safety  │
├───────────────────┼───────────────────────┼───────┼─────────┤
│  { w: 0 }         │ Fire-and-forget       │ ⚡⚡⚡ │ ❌      │
│  { w: 1 }         │ Commit (single node)  │ ⚡⚡  │ ⚡      │
│  { w: "majority"} │ Sync replication      │ ⚡    │ ⚡⚡⚡  │
│  { j: true }      │ fsync / WAL flush     │ ⚡    │ ⚡⚡⚡  │
└───────────────────┴───────────────────────┴───────┴─────────┘

Default: { w: 1 } — acknowledged by primary, not yet replicated.
For critical data: { w: "majority", j: true }
```

---

## Syntax

### insertOne()

```javascript
// SQL: INSERT INTO products (name, price, brand) VALUES ('Laptop', 999.99, 'Dell');

db.products.insertOne({
  name: "Laptop",
  price: NumberDecimal("999.99"),
  brand: "Dell",
  category: { name: "Electronics", slug: "electronics" },
  tags: ["computer", "portable", "work"],
  specs: {
    ram: "16GB",
    storage: "512GB SSD",
    cpu: "Intel i7-12700H"
  },
  stock: 45,
  ratings: { average: 0, count: 0 },
  createdAt: new Date(),
  updatedAt: new Date()
})

// Result:
{
  acknowledged: true,
  insertedId: ObjectId("65a1b2c3d4e5f6a7b8c9d0e1")
}
```

### insertMany()

```javascript
// SQL: INSERT INTO products (name, price) VALUES ('Mouse', 29.99), ('Keyboard', 59.99);

db.products.insertMany([
  {
    name: "Mouse",
    price: NumberDecimal("29.99"),
    brand: "Logitech",
    category: { name: "Electronics", slug: "electronics" },
    stock: 200,
    createdAt: new Date()
  },
  {
    name: "Keyboard",
    price: NumberDecimal("59.99"),
    brand: "Corsair",
    category: { name: "Electronics", slug: "electronics" },
    stock: 150,
    createdAt: new Date()
  },
  {
    name: "Headphones",
    price: NumberDecimal("149.99"),
    brand: "Sony",
    category: { name: "Electronics", slug: "electronics" },
    stock: 75,
    createdAt: new Date()
  }
])

// Result:
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId("..."),
    '1': ObjectId("..."),
    '2': ObjectId("...")
  }
}
```

### insertMany() with Ordered Option

```javascript
// Default: ordered = true
// If one fails, stop processing remaining documents
db.products.insertMany([
  { _id: 1, name: "A" },
  { _id: 1, name: "B" },  // ❌ Duplicate _id — stops here
  { _id: 2, name: "C" }   // Never inserted
], { ordered: true })

// ordered: false → Continue inserting despite errors
db.products.insertMany([
  { _id: 1, name: "A" },
  { _id: 1, name: "B" },  // ❌ Duplicate — skipped
  { _id: 2, name: "C" }   // ✅ Still inserted
], { ordered: false })

// SQL equivalent:
// INSERT IGNORE INTO ... (MySQL)
// INSERT ... ON CONFLICT DO NOTHING (PostgreSQL)
```

### Upsert (INSERT or UPDATE)

```javascript
// SQL: INSERT ... ON DUPLICATE KEY UPDATE (MySQL)
// SQL: INSERT ... ON CONFLICT (column) DO UPDATE SET ... (PostgreSQL)

// MongoDB: updateOne with upsert: true
db.products.updateOne(
  { sku: "LAPTOP-001" },                    // Filter
  {
    $set: { name: "Laptop", price: 999.99 }, // Update fields
    $setOnInsert: { createdAt: new Date() }  // Only on insert
  },
  { upsert: true }
)

// If sku "LAPTOP-001" exists → updates name and price
// If not → inserts new document with all fields + createdAt
```

---

## SQL vs MongoDB — Side-by-Side

```sql
-- SQL: Multiple related inserts (within transaction)
BEGIN;
INSERT INTO customers (name, email) VALUES ('John Doe', 'john@example.com')
  RETURNING id INTO @customer_id;
INSERT INTO addresses (customer_id, street, city)
  VALUES (@customer_id, '123 Main St', 'NYC');
INSERT INTO orders (customer_id, total) VALUES (@customer_id, 199.99)
  RETURNING id INTO @order_id;
INSERT INTO order_items (order_id, product_id, quantity)
  VALUES (@order_id, 42, 2);
COMMIT;
-- 4 INSERTs, 1 transaction, referential integrity enforced
```

```javascript
// MongoDB: Single document insert (no transaction needed)
db.orders.insertOne({
  customer: {
    name: "John Doe",
    email: "john@example.com",
    address: { street: "123 Main St", city: "NYC" }
  },
  items: [
    { productId: ObjectId("..."), name: "Widget", price: 99.99, quantity: 2 }
  ],
  total: NumberDecimal("199.98"),
  status: "pending",
  createdAt: new Date()
})
// 1 INSERT, no transaction needed, all data in one document
```

---

## Node.js Using MongoDB Driver (REQUIRED)

```javascript
const { MongoClient, ObjectId, Decimal128 } = require('mongodb');

async function createOperations() {
  const client = new MongoClient('mongodb://localhost:27017');
  await client.connect();
  const db = client.db('ecommerce');

  // ──────────── insertOne ────────────
  const product = await db.collection('products').insertOne({
    name: 'Gaming Laptop',
    price: Decimal128.fromString('1499.99'),
    brand: 'ASUS',
    category: { name: 'Electronics', slug: 'electronics' },
    specs: { ram: '32GB', gpu: 'RTX 4070', storage: '1TB NVMe' },
    tags: ['gaming', 'laptop', 'high-performance'],
    stock: 30,
    ratings: { average: 0, count: 0 },
    isActive: true,
    createdAt: new Date(),
    updatedAt: new Date()
  });
  console.log('Inserted product:', product.insertedId);

  // ──────────── insertMany ────────────
  const customers = await db.collection('customers').insertMany([
    {
      firstName: 'Alice',
      lastName: 'Johnson',
      email: 'alice@example.com',
      password: '$2b$10$hashedpasswordhere',  // Always hash!
      address: {
        street: '789 Pine St',
        city: 'Chicago',
        state: 'IL',
        zip: '60601',
        country: 'US'
      },
      preferences: { newsletter: true, theme: 'dark' },
      createdAt: new Date()
    },
    {
      firstName: 'Bob',
      lastName: 'Williams',
      email: 'bob@example.com',
      password: '$2b$10$anotherhashedpassword',
      address: {
        street: '321 Elm St',
        city: 'Austin',
        state: 'TX',
        zip: '73301',
        country: 'US'
      },
      preferences: { newsletter: false, theme: 'light' },
      createdAt: new Date()
    }
  ]);
  console.log('Inserted customers:', customers.insertedIds);

  // ──────────── Upsert ────────────
  const upsertResult = await db.collection('products').updateOne(
    { sku: 'MOUSE-001' },
    {
      $set: {
        name: 'Wireless Mouse',
        price: Decimal128.fromString('39.99'),
        updatedAt: new Date()
      },
      $setOnInsert: {
        stock: 100,
        ratings: { average: 0, count: 0 },
        createdAt: new Date()
      }
    },
    { upsert: true }
  );
  console.log('Upserted:', upsertResult.upsertedId || 'updated existing');

  // ──────────── Bulk Write ────────────
  const bulkResult = await db.collection('products').bulkWrite([
    {
      insertOne: {
        document: { name: 'USB Cable', price: Decimal128.fromString('9.99'), stock: 500 }
      }
    },
    {
      insertOne: {
        document: { name: 'HDMI Cable', price: Decimal128.fromString('14.99'), stock: 300 }
      }
    },
    {
      updateOne: {
        filter: { name: 'Gaming Laptop' },
        update: { $inc: { stock: -1 } }
      }
    }
  ], { ordered: false });
  console.log('Bulk:', bulkResult.insertedCount, 'inserted,', bulkResult.modifiedCount, 'modified');

  await client.close();
}
```

---

## ORM / ODM Comparison

```javascript
// ──── Sequelize (SQL ORM) ────
const product = await Product.create({
  name: 'Laptop',
  price: 999.99,
  categoryId: 1  // FK reference
});
// - Validates against model schema
// - FK constraint checked by DATABASE
// - Auto-sets id (AUTO_INCREMENT)
// - Auto-sets createdAt, updatedAt

// ──── Mongoose (MongoDB ODM) ────
const product = await Product.create({
  name: 'Laptop',
  price: 999.99,
  category: { name: 'Electronics' }  // Embedded
});
// - Validates against Mongoose schema (application-level)
// - No FK — embedding or manual references
// - Auto-sets _id (ObjectId)
// - Auto-sets createdAt, updatedAt (if timestamps: true)

// ──── Key Difference ────
// Sequelize: Database rejects invalid data
// Mongoose: Application rejects invalid data (database doesn't care)
```

---

## Real-World Scenario — Order Creation

### SQL Approach

```sql
-- Creating an order requires multiple tables + transaction
BEGIN;

-- Create order
INSERT INTO orders (customer_id, status, total, created_at)
VALUES (42, 'pending', 0, NOW())
RETURNING id INTO @order_id;

-- Create order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES 
  (@order_id, 101, 2, 29.99),
  (@order_id, 205, 1, 999.99);

-- Update total
UPDATE orders SET total = (
  SELECT SUM(quantity * unit_price) FROM order_items WHERE order_id = @order_id
) WHERE id = @order_id;

-- Decrement stock
UPDATE products SET stock = stock - 2 WHERE id = 101;
UPDATE products SET stock = stock - 1 WHERE id = 205;

COMMIT;
```

### MongoDB Approach

```javascript
// Single document insert (for the order itself)
const order = await db.collection('orders').insertOne({
  customerId: new ObjectId(req.body.customerId),
  customer: {  // Denormalized snapshot
    name: "John Doe",
    email: "john@example.com"
  },
  items: [
    {
      productId: new ObjectId("..."),
      name: "Mouse",          // Snapshot at time of order
      unitPrice: Decimal128.fromString("29.99"),
      quantity: 2,
      subtotal: Decimal128.fromString("59.98")
    },
    {
      productId: new ObjectId("..."),
      name: "Laptop",
      unitPrice: Decimal128.fromString("999.99"),
      quantity: 1,
      subtotal: Decimal128.fromString("999.99")
    }
  ],
  total: Decimal128.fromString("1059.97"),
  status: "pending",
  shippingAddress: {
    street: "123 Main St",
    city: "New York",
    state: "NY",
    zip: "10001"
  },
  createdAt: new Date(),
  updatedAt: new Date()
});

// Stock update still needs separate operation
// (Could use transaction if atomicity is critical)
await db.collection('products').bulkWrite([
  { updateOne: { filter: { _id: new ObjectId("...") }, update: { $inc: { stock: -2 } } } },
  { updateOne: { filter: { _id: new ObjectId("...") }, update: { $inc: { stock: -1 } } } }
]);
```

### Express API Endpoint

```javascript
// POST /api/orders
app.post('/api/orders', async (req, res) => {
  try {
    const { customerId, items } = req.body;
    const db = getDB();
    
    // Get product details for order snapshot
    const productIds = items.map(i => new ObjectId(i.productId));
    const products = await db.collection('products')
      .find({ _id: { $in: productIds } })
      .toArray();
    
    // Build order items with snapshots
    const orderItems = items.map(item => {
      const product = products.find(p => p._id.equals(new ObjectId(item.productId)));
      if (!product) throw new Error(`Product ${item.productId} not found`);
      if (product.stock < item.quantity) throw new Error(`Insufficient stock for ${product.name}`);
      
      const subtotal = parseFloat(product.price.toString()) * item.quantity;
      return {
        productId: product._id,
        name: product.name,
        unitPrice: product.price,
        quantity: item.quantity,
        subtotal: Decimal128.fromString(subtotal.toFixed(2))
      };
    });
    
    const total = orderItems.reduce(
      (sum, item) => sum + parseFloat(item.subtotal.toString()), 0
    );
    
    const result = await db.collection('orders').insertOne({
      customerId: new ObjectId(customerId),
      items: orderItems,
      total: Decimal128.fromString(total.toFixed(2)),
      status: 'pending',
      createdAt: new Date()
    });
    
    res.status(201).json({ orderId: result.insertedId });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});
```

---

## Performance Insight

### Insert Performance Comparison

```
┌───────────────────────────────────────────────────────────┐
│  Operation              │ SQL (PG)    │ MongoDB           │
├─────────────────────────┼─────────────┼───────────────────┤
│  Single insert          │ ~0.5ms      │ ~0.3ms            │
│  1000 inserts (loop)    │ ~500ms      │ ~150ms            │
│  1000 inserts (batch)   │ ~15ms       │ ~10ms             │
│  Insert with 5 indexes  │ ~2ms        │ ~1.5ms            │
│  Insert with FK check   │ +0.5ms      │ N/A (no FK)       │
│  Insert with validation │ ~0.5ms      │ ~0.5ms (if set)   │
├─────────────────────────┴─────────────┴───────────────────┤
│  Key insight: MongoDB is faster for inserts because:      │
│  - No FK constraint checking                              │
│  - No type coercion                                       │
│  - No schema validation (unless explicitly configured)    │
│  Trade-off: Data integrity is YOUR responsibility.        │
└───────────────────────────────────────────────────────────┘
```

### Batch Insert Best Practices

```javascript
// ❌ WRONG: Individual inserts in a loop
for (const item of items) {
  await db.collection('products').insertOne(item); // N round trips
}

// ✅ RIGHT: Batch insert
await db.collection('products').insertMany(items); // 1 round trip

// ✅ BEST: Bulk write with unordered (parallel execution)
await db.collection('products').insertMany(items, { ordered: false });
// Unordered = server can insert in parallel = faster
// But errors don't stop the batch
```

---

## Common Mistakes (SQL Developers Make)

### ❌ Mistake 1: Inserting Without Thinking About Read Patterns

```javascript
// SQL habit: normalize everything
db.orders.insertOne({ customerId: 1, productId: 42, quantity: 2 })
// Now you need $lookup on every read. Defeats MongoDB's purpose.

// Better: Include data needed for the most common read
db.orders.insertOne({
  customerId: ObjectId("..."),
  customer: { name: "John", email: "john@example.com" },
  items: [{ name: "Laptop", price: 999, quantity: 1 }],
  total: 999
})
```

### ❌ Mistake 2: Not Using Bulk Operations

```javascript
// 10,000 individual inserts = 10,000 network round trips = slow
// 1 insertMany with 10,000 docs = 1 network round trip = fast
```

### ❌ Mistake 3: Relying on insertOne's Return for Complex Flows

```javascript
// SQL gives you RETURNING clause
// INSERT INTO orders (...) RETURNING *;

// MongoDB insertOne only returns insertedId
const result = await db.collection('orders').insertOne(orderData);
// result = { acknowledged: true, insertedId: ObjectId("...") }

// To get the full document, you must query again:
const order = await db.collection('orders').findOne({ _id: result.insertedId });
```

---

## Practice Exercises

### Exercise 1: Basic Inserts

Insert the following into the `ecommerce` database:
1. 3 products with embedded category objects
2. 2 customers with embedded address objects
3. 1 order with embedded customer info and order items array

### Exercise 2: Bulk Import

Write a Node.js script that:
1. Reads a JSON file of 1000 products
2. Inserts them using `insertMany` with `ordered: false`
3. Reports how many succeeded and how many failed (duplicate `_id`)

### Exercise 3: Upsert Pattern

Implement an upsert endpoint that:
- Accepts a product SKU and updated fields
- If the SKU exists, updates the product
- If not, creates a new product with default values
- Uses `$setOnInsert` for fields that should only be set on creation

---

## Interview Q&A

**Q1: What is the difference between `insertOne` and `updateOne` with `upsert: true`?**
> `insertOne` always creates a new document (fails on duplicate `_id`). `updateOne` with `upsert: true` creates only if the filter matches no documents, otherwise updates the existing one. Upsert is MongoDB's `INSERT ... ON CONFLICT DO UPDATE`.

**Q2: How does MongoDB ensure uniqueness without a PRIMARY KEY definition?**
> The `_id` field has a unique index automatically created. You can also create unique indexes on other fields (`db.collection.createIndex({ email: 1 }, { unique: true })`), which is analogous to SQL's `UNIQUE` constraint.

**Q3: What is `ordered: false` in `insertMany` and when should you use it?**
> By default, `insertMany` is ordered — if one document fails, all subsequent documents are skipped. With `ordered: false`, MongoDB continues inserting remaining documents despite individual failures. Use it for bulk imports where partial success is acceptable.

**Q4: How do you handle `AUTO_INCREMENT`-style sequential IDs in MongoDB?**
> MongoDB doesn't have auto-increment. Options: (1) Use ObjectId (recommended), (2) Maintain a counter collection with `findOneAndUpdate` using `$inc`, (3) Use a UUID library. Sequential IDs don't work well with sharding — that's why ObjectId exists.

**Q5: What is write concern and how does it differ from SQL's commit?**
> Write concern controls durability guarantees. `w: 1` = acknowledged by primary (similar to SQL commit). `w: "majority"` = acknowledged by majority of replica set (similar to synchronous replication). `w: 0` = fire-and-forget (no SQL equivalent). SQL's COMMIT is always durable (equivalent to `w: 1, j: true`).
