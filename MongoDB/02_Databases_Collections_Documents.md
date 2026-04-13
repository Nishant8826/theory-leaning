# Databases, Collections & Documents

> 📌 **File:** 02_Databases_Collections_Documents.md | **Level:** SQL Expert → MongoDB

---

## What is it?

In SQL, your hierarchy is: **Server → Database → Table → Row → Column**.
In MongoDB, it's: **Server → Database → Collection → Document → Field**.

The key difference: a SQL row is flat (columns are scalar values), while a MongoDB document is **hierarchical** — fields can contain nested objects, arrays, and arrays of objects.

---

## SQL Parallel — Think of it like this

```
┌─────────────────────────────────────────────────────────────┐
│                 SQL                  │       MongoDB         │
├──────────────────────────────────────┼───────────────────────┤
│  CREATE DATABASE ecommerce;          │  use ecommerce        │
│  DROP DATABASE ecommerce;            │  db.dropDatabase()    │
│  CREATE TABLE products (...);        │  db.createCollection()│
│  DROP TABLE products;                │  db.products.drop()   │
│  INSERT INTO products VALUES (...);  │  db.products.insertOne│
│  SELECT * FROM products;             │  db.products.find()   │
│  DESCRIBE products;                  │  (no equivalent)      │
│  SHOW TABLES;                        │  show collections     │
│  SHOW DATABASES;                     │  show dbs             │
└──────────────────────────────────────┴───────────────────────┘
```

---

## Why this is different from SQL (CRITICAL)

### 1. Databases are Created Implicitly

```javascript
// In SQL:
// CREATE DATABASE ecommerce;  ← explicit command required

// In MongoDB:
use ecommerce  // Database doesn't exist yet — that's OK
db.products.insertOne({ name: "Laptop" })
// NOW the database exists (created on first write)
```

**Warning:** `show dbs` won't display empty databases. A database only appears after it contains at least one document.

### 2. Collections Have No Schema Definition

```sql
-- SQL: Must define schema BEFORE inserting data
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  category_id INT REFERENCES categories(id)
);
```

```javascript
// MongoDB: Just insert. Collection is created automatically.
db.products.insertOne({
  name: "Laptop",
  price: 999.99,
  category: { name: "Electronics" }  // No schema, no DDL, no migration
})
```

### 3. Documents Can Have Different Shapes

```javascript
// Same collection, different document structures — perfectly valid!
db.products.insertMany([
  {
    name: "Laptop",
    price: 999,
    specs: { ram: "16GB", cpu: "i7" },
    warranty: { years: 2, type: "manufacturer" }
  },
  {
    name: "T-Shirt",
    price: 29,
    sizes: ["S", "M", "L", "XL"],
    color: "Navy",
    material: "Cotton"
    // No specs, no warranty — different shape
  },
  {
    name: "Ebook",
    price: 9.99,
    format: "PDF",
    pages: 320
    // No sizes, no specs, no warranty — yet another shape
  }
])
```

In SQL, this would require either:
- One table with many nullable columns (sparse table)
- Multiple tables (electronics, clothing, books) — table-per-subtype
- EAV pattern (generic key-value pairs — anti-pattern)

---

## How does it work?

### Database Architecture

```
mongod (server instance)
  │
  ├── admin           (system database)
  ├── config          (sharding metadata)
  ├── local           (replication data)
  │
  ├── ecommerce       (your database)
  │   ├── products    (collection)
  │   │   ├── { _id: ..., name: "Laptop" }     (document)
  │   │   ├── { _id: ..., name: "Shoes" }      (document)
  │   │   └── { _id: ..., name: "Coffee" }     (document)
  │   │
  │   ├── customers   (collection)
  │   │   ├── { _id: ..., firstName: "John" }   (document)
  │   │   └── { _id: ..., firstName: "Jane" }   (document)
  │   │
  │   ├── orders      (collection)
  │   └── categories  (collection)
  │
  └── blog            (another database)
      ├── posts
      └── comments
```

### Document Internals

```
Document (what you write — JSON):
{
  "name": "Laptop",
  "price": 999.99,
  "tags": ["computer", "portable"]
}

Stored as (BSON — Binary JSON):
┌──────────────────────────────────────────────┐
│  Total Size: 87 bytes                        │
│  ┌─────────┬──────┬───────────┐              │
│  │ Type(02)│"name"│ "Laptop"  │              │
│  ├─────────┼──────┼───────────┤              │
│  │ Type(01)│"price│ 999.99    │  (double)    │
│  ├─────────┼──────┼───────────┤              │
│  │ Type(04)│"tags"│ [array]   │              │
│  └─────────┴──────┴───────────┘              │
│  Auto-added: _id: ObjectId(...)              │
└──────────────────────────────────────────────┘
```

### The `_id` Field

Every document MUST have an `_id` field. If you don't provide one, MongoDB generates an **ObjectId**.

```javascript
// Auto-generated ObjectId
{ _id: ObjectId("507f1f77bcf86cd799439011") }

// ObjectId anatomy (12 bytes):
// ┌──────────┬──────┬──────┬──────────┐
// │ Timestamp│Random│Random│ Counter  │
// │ (4 bytes)│(5 b) │      │ (3 bytes)│
// └──────────┴──────┴──────┴──────────┘
// 507f1f77    bcf86c  d799    439011

// Extract creation timestamp
ObjectId("507f1f77bcf86cd799439011").getTimestamp()
// → ISODate("2012-10-17T20:46:15Z")

// You CAN use your own _id
db.products.insertOne({ _id: "LAPTOP-001", name: "Laptop" })
db.products.insertOne({ _id: 42, name: "Mouse" })
// But ObjectId is recommended for distributed systems
```

**SQL comparison:**

```
SQL AUTO_INCREMENT:     1, 2, 3, 4, 5  (sequential, single server)
MongoDB ObjectId:       Globally unique, no coordination needed
                        Works across shards without conflicts
```

---

## Syntax

### Database Operations

```javascript
// Show all databases
show dbs

// Use / create database
use ecommerce

// Current database
db.getName()  // "ecommerce"

// Database stats (like SQL's information_schema)
db.stats()

// Drop database (⚠️ destructive)
db.dropDatabase()
```

### Collection Operations

```javascript
// Create collection explicitly (usually unnecessary)
db.createCollection("products")

// Create with options
db.createCollection("logs", {
  capped: true,           // Fixed-size collection (circular buffer)
  size: 10485760,         // 10MB max
  max: 5000               // Max 5000 documents
})
// Capped collections = no SQL equivalent. Think circular log buffer.

// List collections
show collections
db.getCollectionNames()

// Collection stats
db.products.stats()

// Rename collection (ALTER TABLE ... RENAME)
db.products.renameCollection("items")

// Drop collection (DROP TABLE)
db.products.drop()
```

### Document Operations (Preview)

```javascript
// Insert single document (INSERT INTO ... VALUES)
db.products.insertOne({
  name: "Laptop",
  price: 999.99,
  category: { name: "Electronics" },
  tags: ["computer", "portable"],
  createdAt: new Date()
})

// Insert multiple documents (batch INSERT)
db.products.insertMany([
  { name: "Mouse", price: 29.99 },
  { name: "Keyboard", price: 59.99 }
])

// Find all (SELECT *)
db.products.find()

// Find one (SELECT * ... LIMIT 1)
db.products.findOne({ name: "Laptop" })

// Count (SELECT COUNT(*))
db.products.countDocuments()
db.products.estimatedDocumentCount()  // Faster, uses metadata
```

---

## SQL vs MongoDB — Side-by-Side

```sql
-- SQL: Create database and table
CREATE DATABASE ecommerce;
USE ecommerce;

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2),
  brand VARCHAR(100),
  category_name VARCHAR(100),
  stock INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO products (name, price, brand, category_name, stock)
VALUES ('Laptop', 999.99, 'Dell', 'Electronics', 45);
```

```javascript
// MongoDB equivalent
use ecommerce

db.products.insertOne({
  name: "Laptop",
  price: 999.99,
  brand: "Dell",
  category: { name: "Electronics" },
  stock: 45,
  createdAt: new Date()
})
// Collection auto-created. No DDL needed.
```

---

## Node.js Using MongoDB Driver

```javascript
const { MongoClient, ObjectId } = require('mongodb');

async function databaseOperations() {
  const client = new MongoClient('mongodb://localhost:27017');
  await client.connect();

  // List databases (SHOW DATABASES)
  const adminDb = client.db('admin');
  const dbs = await adminDb.admin().listDatabases();
  console.log('Databases:', dbs.databases.map(d => d.name));

  // Get database reference
  const db = client.db('ecommerce');

  // List collections (SHOW TABLES)
  const collections = await db.listCollections().toArray();
  console.log('Collections:', collections.map(c => c.name));

  // Create collection with validation
  await db.createCollection('products', {
    validator: {
      $jsonSchema: {
        bsonType: 'object',
        required: ['name', 'price'],
        properties: {
          name: { bsonType: 'string', description: 'must be a string' },
          price: { bsonType: 'number', minimum: 0, description: 'must be positive' }
        }
      }
    }
  });

  // Collection reference
  const products = db.collection('products');

  // Insert and get back the _id
  const result = await products.insertOne({
    name: 'Laptop',
    price: 999.99,
    category: { name: 'Electronics' }
  });
  console.log('Inserted ID:', result.insertedId);

  // Collection stats
  const stats = await db.command({ collStats: 'products' });
  console.log('Document count:', stats.count);
  console.log('Storage size:', stats.storageSize);

  await client.close();
}
```

---

## ORM / ODM Comparison

```javascript
// SQL ORM (Sequelize) — Define model with strict schema
const Product = sequelize.define('Product', {
  name: { type: DataTypes.STRING, allowNull: false },
  price: { type: DataTypes.DECIMAL(10, 2), allowNull: false },
  brand: { type: DataTypes.STRING },
  stock: { type: DataTypes.INTEGER, defaultValue: 0 }
});

// Migration required for every schema change
await sequelize.sync(); // CREATE TABLE IF NOT EXISTS

// Mongoose (MongoDB ODM) — Similar concept, different trade-offs
const productSchema = new mongoose.Schema({
  name: { type: String, required: true },
  price: { type: Number, required: true, min: 0 },
  brand: String,
  category: {
    name: String,           // ← Nested object (impossible in flat SQL row)
    slug: String
  },
  tags: [String],           // ← Array of strings (impossible in flat SQL row)
  specs: mongoose.Schema.Types.Mixed,  // ← Any shape (ultimate flexibility)
  stock: { type: Number, default: 0 }
}, { timestamps: true });   // Adds createdAt, updatedAt automatically

const Product = mongoose.model('Product', productSchema);

// No migration needed — schema is application-level only
```

**Key differences:**
- Sequelize: Schema lives in DATABASE. Migrations required.
- Mongoose: Schema lives in APPLICATION CODE. No migrations.
- Mongoose schemas are optional guardrails, not database-level constraints.
- MongoDB doesn't enforce Mongoose schemas — Mongoose does. The database doesn't know about your schema.

---

## Real-World Scenario — Multi-Tenant SaaS

### SQL Approach

```sql
-- Option 1: Separate databases per tenant (expensive)
-- Option 2: Schema per tenant (PostgreSQL only)
-- Option 3: tenant_id column everywhere (messy)

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  tenant_id INT NOT NULL,
  name VARCHAR(255),
  price DECIMAL(10,2),
  FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

-- Every query must include WHERE tenant_id = ?
SELECT * FROM products WHERE tenant_id = 42 AND price > 100;
```

### MongoDB Approach

```javascript
// Option 1: Separate database per tenant (easy to implement)
const db = client.db(`tenant_${tenantId}`);

// Option 2: Collection per tenant
const products = db.collection(`products_${tenantId}`);

// Option 3: Same collection with tenant field (most common)
db.products.find({ tenantId: ObjectId("..."), price: { $gt: 100 } })

// Index for tenant isolation
db.products.createIndex({ tenantId: 1, price: 1 })
```

### Node.js API

```javascript
// Middleware to extract tenant
app.use((req, res, next) => {
  req.tenantId = req.headers['x-tenant-id'];
  req.db = client.db(`tenant_${req.tenantId}`);
  next();
});

app.get('/api/products', async (req, res) => {
  const products = await req.db.collection('products')
    .find({ price: { $gt: 0 } })
    .toArray();
  res.json(products);
});
```

---

## Performance Insight

### Collection Size Limits

```
SQL Table:           No practical row limit (billions with proper indexing)
MongoDB Collection:  No document count limit
                     Document size limit: 16MB per document
                     Namespace limit: ~24,000 collections per database
```

### Document Size Limit — 16MB

This is critical. A single document cannot exceed 16MB.

```
What fits in 16MB:
  ✅ Product with 100 reviews
  ✅ User profile with 50 addresses
  ✅ Blog post with 200 comments

What does NOT fit:
  ❌ User with 1,000,000 activity logs
  ❌ Product with 50,000 reviews
  ❌ Chat room with 100,000 messages

Solution: Use referencing (separate collection) for unbounded arrays.
```

---

## Common Mistakes (SQL Developers Make)

### ❌ Creating Too Many Collections

```javascript
// SQL thinking — DON'T do this in MongoDB
db.product_names       // { product_id, name }
db.product_prices      // { product_id, price }
db.product_categories  // { product_id, category }
db.product_specs       // { product_id, spec_key, spec_value }
// This is just a normalized SQL schema with extra steps

// MongoDB thinking — DO this
db.products  // { name, price, category: {...}, specs: {...} }
```

### ❌ Fear of Embedded Documents

```javascript
// SQL developers are afraid of this because it "feels wrong":
{
  name: "John",
  address: {           // ← "Shouldn't this be a separate table?"
    street: "123 Main",
    city: "NYC"
  }
}

// But this is PERFECT for MongoDB.
// It's one user, one address, read together. Embed it.
```

---

## Practice Exercises

### Exercise 1: Database & Collection Exploration

```javascript
// Connect to mongosh and run:
// 1. Show all databases
// 2. Switch to ecommerce
// 3. List all collections
// 4. Get document count for each collection
// 5. Get the storage stats for the products collection
// 6. Create a new "reviews" collection with a capped size of 5MB
// 7. Insert a document into it
// 8. Verify the collection exists
```

### Exercise 2: Document Design

Convert this SQL table into a MongoDB document:

```sql
CREATE TABLE employees (
  id INT PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  department_id INT,
  manager_id INT,
  skills TEXT,  -- comma-separated: "Python,JavaScript,SQL"
  address_line1 VARCHAR(100),
  address_line2 VARCHAR(100),
  city VARCHAR(50),
  state VARCHAR(2),
  zip VARCHAR(10)
);
```

### Exercise 3: Identify the Limits

Which of these documents will exceed the 16MB limit?
1. A user profile with 50 fields
2. A product with an array of 10,000 reviews (each 200 bytes)
3. A chat room with 500,000 messages
4. A blog post with a 10MB embedded image (base64)

---

## Interview Q&A

**Q1: What is a capped collection and when would you use it?**
> A fixed-size collection that overwrites oldest documents when full. Used for logs, event streams, and caching. No SQL equivalent — similar to a circular buffer. You can't delete individual documents from a capped collection.

**Q2: Why is the 16MB document limit important for schema design?**
> It forces you to think about unbounded arrays. If an array can grow indefinitely (messages, logs, reviews), you must use a separate collection with references. This is the primary constraint that drives embedding vs. referencing decisions.

**Q3: How does MongoDB handle schema evolution compared to SQL?**
> In SQL, `ALTER TABLE` locks the table and rewrites rows. In MongoDB, you just start writing documents with the new shape. Old documents keep the old shape. Your application code handles both shapes (or you run a background migration script).

**Q4: What happens if you insert a document without specifying `_id`?**
> MongoDB auto-generates a 12-byte ObjectId. It contains a timestamp, random value, and counter — making it globally unique without coordination between servers or shards.

**Q5: Can two documents in the same collection have completely different fields?**
> Yes. MongoDB is schema-flexible. But in production, you should use schema validation (MongoDB validator or Mongoose) to enforce consistency. "Schema-flexible" means you CAN have different shapes, not that you SHOULD.
