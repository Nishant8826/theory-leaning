# BSON & Data Types

> 📌 **File:** 03_BSON_And_Data_Types.md | **Level:** SQL Expert → MongoDB

---

## What is it?

BSON (Binary JSON) is MongoDB's internal data format. You write JSON, MongoDB stores BSON. Think of it as JSON with **type information** baked in — it knows the difference between an integer and a double, a date and a string, unlike plain JSON where everything could be ambiguous.

**SQL parallel:** In SQL, every column has a strict type (`INT`, `VARCHAR`, `DECIMAL`, `TIMESTAMP`). In MongoDB, every **value** has a type, but different documents in the same collection can have different types for the same field name. This is both powerful and dangerous.

---

## SQL Parallel — Think of it like this

| SQL Type                | MongoDB/BSON Type    | Notes                                    |
|-------------------------|----------------------|------------------------------------------|
| `INT` / `BIGINT`        | `NumberInt` / `NumberLong` | 32-bit / 64-bit integers          |
| `FLOAT` / `DOUBLE`      | `Double`             | 64-bit IEEE 754 floating point           |
| `DECIMAL(10,2)`         | `Decimal128`         | Exact decimal — use for money            |
| `VARCHAR` / `TEXT`       | `String`             | UTF-8 encoded                            |
| `BOOLEAN`               | `Boolean`            | `true` / `false`                         |
| `DATE` / `TIMESTAMP`    | `Date`               | Millisecond precision UTC                |
| `BLOB` / `BYTEA`        | `BinData`            | Binary data                              |
| `NULL`                  | `null`               | Explicit null                            |
| `JSON` / `JSONB` (PG)   | Native (it IS JSON)  | MongoDB's core format                    |
| `ARRAY` (PG)            | `Array`              | First-class type in BSON                 |
| `SERIAL` / `AUTO_INCREMENT` | `ObjectId`      | 12-byte unique identifier                |
| No equivalent           | `Regex`              | Store regex patterns natively            |
| No equivalent           | `Timestamp`          | Internal replication timestamp           |
| No equivalent           | `MinKey` / `MaxKey`  | Compare lower/higher than all values     |

---

## Why this is different from SQL (CRITICAL)

### 1. Type is Per-Value, Not Per-Column

```sql
-- SQL: price is ALWAYS decimal in every row
CREATE TABLE products (price DECIMAL(10,2));
-- Inserting a string into price = ERROR
```

```javascript
// MongoDB: price can be different types in different documents
db.products.insertOne({ name: "Laptop", price: 999.99 })  // double
db.products.insertOne({ name: "Free Gift", price: "free" })  // string!
db.products.insertOne({ name: "TBD", price: null })  // null

// All valid. All dangerous. Query behavior will surprise you:
db.products.find({ price: { $gt: 100 } })
// Only returns documents where price is a NUMBER > 100
// Silently ignores "free" and null — no error
```

### 2. BSON Has More Types Than JSON

```
JSON types (7):         BSON types (20+):
  string                  String
  number                  Double, Int32, Int64, Decimal128
  boolean                 Boolean
  null                    Null
  object                  Object (embedded document)
  array                   Array
  (none)                  ObjectId, Date, Regex, BinData,
                          Timestamp, MinKey, MaxKey, Code,
                          UUID, ...
```

### 3. Numbers Are Tricky

```javascript
// In mongosh:
db.test.insertOne({ a: 42 })         // Stored as Double (64-bit float)
db.test.insertOne({ a: NumberInt(42) })  // Stored as Int32
db.test.insertOne({ a: NumberLong(42) }) // Stored as Int64
db.test.insertOne({ a: NumberDecimal("19.99") }) // Stored as Decimal128

// Why does this matter?
0.1 + 0.2 === 0.3  // false (IEEE 754 floating point)
// For money, ALWAYS use Decimal128

// In Node.js driver:
const { Decimal128, Int32, Long } = require('mongodb');
await db.collection('products').insertOne({
  price: Decimal128.fromString("19.99"),  // Exact decimal
  stock: new Int32(100),                   // 32-bit int
  viewCount: Long.fromNumber(1000000)      // 64-bit int
});
```

---

## How does it work?

### BSON Encoding

```
JSON input:                          BSON on disk:
{                                    ┌──────────────────────────┐
  "name": "Laptop",                  │ \x45\x00\x00\x00        │ total size
  "price": 999.99,   ──────────►    │ \x02 name \x00           │ type 02 = string
  "inStock": true                    │ \x07 Laptop \x00         │ value
}                                    │ \x01 price \x00          │ type 01 = double
                                     │ \x40\x8F\x3F\xF9...     │ 999.99 as double
                                     │ \x08 inStock \x00        │ type 08 = bool
                                     │ \x01                     │ true
                                     │ \x00                     │ end of document
                                     └──────────────────────────┘
```

### Why BSON and not JSON?

```
┌────────────────────────────────────────────────────────┐
│  JSON:                                                 │
│  ✗ No integer vs float distinction                     │
│  ✗ No date type (dates are strings)                    │
│  ✗ No binary data type                                 │
│  ✗ Must parse entire document to find a field          │
│  ✗ Numbers are imprecise (all doubles)                 │
│                                                        │
│  BSON:                                                 │
│  ✓ Rich type system (20+ types)                        │
│  ✓ Length-prefixed — can skip fields without parsing   │
│  ✓ Native Date, Decimal128, Binary, ObjectId          │
│  ✓ Efficient encoding for numerics                     │
│  ✓ Designed for fast field traversal                   │
└────────────────────────────────────────────────────────┘
```

---

## Visual Diagram — BSON Types

```
┌─────────────────────────── BSON Type Hierarchy ───────────────────────────┐
│                                                                          │
│  Scalar Types:                                                           │
│  ├── Double (1)         → 64-bit float. Default for numbers in shell.    │
│  ├── String (2)         → UTF-8. Max ~16MB within a document.            │
│  ├── Boolean (8)        → true / false                                   │
│  ├── Int32 (16)         → NumberInt(). 32-bit signed integer.            │
│  ├── Int64 (18)         → NumberLong(). 64-bit signed integer.           │
│  ├── Decimal128 (19)    → NumberDecimal(). 128-bit. For money.           │
│  ├── Null (10)          → null. Also: field absence ≠ field: null.       │
│  ├── Date (9)           → ISODate(). Milliseconds since epoch.           │
│  └── ObjectId (7)       → 12-byte unique ID (default _id).              │
│                                                                          │
│  Container Types:                                                        │
│  ├── Object (3)         → Embedded document { key: value }              │
│  └── Array (4)          → Ordered list [ ... ]                          │
│                                                                          │
│  Special Types:                                                          │
│  ├── BinData (5)        → Binary (files, hashes, UUIDs)                 │
│  ├── Regex (11)         → /pattern/flags                                │
│  ├── Timestamp (17)     → Internal. Don't use directly.                 │
│  ├── MinKey (255)       → Compares lower than all values                │
│  └── MaxKey (127)       → Compares higher than all values               │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Syntax — Working with Types

### Type Checking in Queries

```javascript
// SQL: You can't query by type (because types are fixed per column)
// MongoDB: You can AND should query by type

// Find all products where price is a number
db.products.find({ price: { $type: "number" } })

// Find all products where price is a string (data quality issue!)
db.products.find({ price: { $type: "string" } })

// Type codes can also be used
db.products.find({ price: { $type: 1 } })   // double
db.products.find({ price: { $type: 16 } })  // int32
db.products.find({ price: { $type: 19 } })  // decimal128

// Check for null vs missing
db.products.find({ discount: null })           // Matches null AND missing
db.products.find({ discount: { $exists: true } }) // Field exists (even if null)
db.products.find({ discount: { $type: "null" } }) // Explicitly null (not missing)
```

### Dates

```javascript
// SQL: INSERT INTO orders (created_at) VALUES (NOW());

// MongoDB:
db.orders.insertOne({
  createdAt: new Date(),                    // Current time
  scheduledFor: new Date("2024-06-15"),     // Specific date
  expiresAt: ISODate("2024-12-31T23:59:59Z") // ISO format (mongosh only)
})

// Date queries (same logic as SQL WHERE)
db.orders.find({
  createdAt: {
    $gte: new Date("2024-01-01"),
    $lt: new Date("2024-02-01")
  }
})

// Node.js:
const sevenDaysAgo = new Date();
sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
await db.collection('orders').find({
  createdAt: { $gte: sevenDaysAgo }
}).toArray();
```

### ObjectId

```javascript
// Auto-generated (recommended)
db.products.insertOne({ name: "Laptop" })
// _id: ObjectId("507f1f77bcf86cd799439011")

// Construct from string
const { ObjectId } = require('mongodb');
const id = new ObjectId("507f1f77bcf86cd799439011");

// Extract timestamp
id.getTimestamp();  // 2012-10-17T20:46:15.000Z

// Generate new ObjectId
const newId = new ObjectId();

// Compare ObjectIds
id.equals(new ObjectId("507f1f77bcf86cd799439011")); // true

// Common API mistake — string vs ObjectId
// ❌ WRONG: db.products.findOne({ _id: "507f1f77bcf86cd799439011" })
// ✅ RIGHT: db.products.findOne({ _id: new ObjectId("507f1f77bcf86cd799439011") })
```

### Decimal128 for Money

```javascript
const { Decimal128 } = require('mongodb');

// Insert with exact decimal
await db.collection('products').insertOne({
  name: "Widget",
  price: Decimal128.fromString("19.99"),
  taxRate: Decimal128.fromString("0.0875")
});

// Read back
const product = await db.collection('products').findOne({ name: "Widget" });
const price = parseFloat(product.price.toString()); // Convert for calculation
console.log(price); // 19.99 (exact)
```

---

## SQL vs MongoDB — Side-by-Side Type Handling

```sql
-- SQL: Strict type enforcement
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  tags TEXT[],                    -- PostgreSQL array
  metadata JSONB,                 -- PostgreSQL JSON
  created_at TIMESTAMP DEFAULT NOW()
);

-- Type violation = ERROR
INSERT INTO products (name, price) VALUES ('Laptop', 'expensive');
-- ERROR: invalid input syntax for type numeric: "expensive"
```

```javascript
// MongoDB: No type enforcement (unless you add validation)
db.products.insertOne({
  name: "Laptop",
  price: NumberDecimal("999.99"),
  tags: ["computer", "portable"],       // Native array
  metadata: { weight: "2.5kg" },        // Native object
  createdAt: new Date()
})

// Type violation = silently accepted
db.products.insertOne({ name: 42, price: "expensive" })
// No error! This is why you need schema validation.
```

---

## Node.js Using MongoDB Driver — Type Handling

```javascript
const { MongoClient, ObjectId, Decimal128, Int32, Long } = require('mongodb');

async function typeExamples() {
  const client = new MongoClient('mongodb://localhost:27017');
  await client.connect();
  const db = client.db('ecommerce');

  // Insert with explicit types
  const result = await db.collection('products').insertOne({
    name: 'Precision Widget',
    price: Decimal128.fromString('49.99'),     // Exact decimal
    stock: new Int32(250),                      // 32-bit integer
    totalSales: Long.fromNumber(1500000),       // 64-bit integer
    weight: 2.5,                                // JavaScript number → BSON Double
    isActive: true,                             // Boolean
    tags: ['gadget', 'tool'],                   // Array
    dimensions: { length: 10, width: 5, height: 3 }, // Embedded doc
    createdAt: new Date(),                      // Date
    sku: null,                                  // Null
    image: Buffer.from('...binary data...')     // BinData
  });

  // Query with type checking
  const badData = await db.collection('products').find({
    $or: [
      { price: { $type: 'string' } },        // Price stored as string
      { name: { $type: 'number' } },          // Name stored as number
      { stock: { $type: 'double' } }          // Stock as float (should be int)
    ]
  }).toArray();

  if (badData.length > 0) {
    console.warn('Found documents with incorrect types:', badData.length);
  }

  // Type-aware aggregation
  const priceStats = await db.collection('products').aggregate([
    { $match: { price: { $type: 'decimal' } } },
    { $group: {
      _id: null,
      avgPrice: { $avg: { $toDouble: '$price' } },
      count: { $sum: 1 }
    }}
  ]).toArray();

  await client.close();
}
```

---

## ORM / ODM Comparison

```javascript
// Sequelize (SQL ORM) — Types defined in model
const Product = sequelize.define('Product', {
  name: { type: DataTypes.STRING(255), allowNull: false },
  price: { type: DataTypes.DECIMAL(10, 2) },
  stock: { type: DataTypes.INTEGER },
  metadata: { type: DataTypes.JSONB }  // PostgreSQL only
});
// Type enforcement: DATABASE level. Wrong type = SQL error.

// Mongoose (MongoDB ODM) — Types defined in schema
const productSchema = new mongoose.Schema({
  name: { type: String, required: true, maxlength: 255 },
  price: { type: mongoose.Types.Decimal128, required: true },
  stock: { type: Number, min: 0 },
  tags: [String],                    // Array of strings
  specs: { type: Map, of: String },  // Key-value pairs
  metadata: mongoose.Schema.Types.Mixed  // Any type
});
// Type enforcement: APPLICATION level. Wrong type = Mongoose validation error.
// Database will accept anything — Mongoose catches it before writing.
```

---

## Real-World Scenario — Price Precision Problem

### The Bug

```javascript
// Developer stores prices as JavaScript numbers (doubles)
db.products.insertOne({ name: "Widget", price: 19.99 })
db.products.insertOne({ name: "Tax", amount: 0.1 + 0.2 })

// Later, in billing calculation:
const items = await db.collection('products').find({}).toArray();
let total = 0;
items.forEach(item => { total += item.price });
console.log(total); // 20.09000000000000003 ← WRONG

// Customer is billed $20.09000000000000003
```

### The Fix

```javascript
// Always use Decimal128 for money
const { Decimal128 } = require('mongodb');

db.products.insertOne({ 
  name: "Widget", 
  price: Decimal128.fromString("19.99") 
})

// For calculation, convert or use aggregation:
const result = await db.collection('products').aggregate([
  { $group: { _id: null, total: { $sum: { $toDouble: "$price" } } } }
]).toArray();
// For production: use a proper decimal library (decimal.js) on the application side
```

---

## Performance Insight

### Type Impact on Storage & Queries

```
┌──────────────────────────────────────────────────────────┐
│  Type          │ Size    │ When to use                   │
├──────────────────────────────────────────────────────────┤
│  Int32         │ 4 bytes │ Counters, small numbers       │
│  Int64         │ 8 bytes │ Large counters, timestamps    │
│  Double        │ 8 bytes │ Measurements, non-money       │
│  Decimal128    │ 16 bytes│ Money, precise calculations   │
│  String        │ Variable│ Text                          │
│  ObjectId      │ 12 bytes│ References, IDs               │
│  Boolean       │ 1 byte  │ Flags                         │
│  Date          │ 8 bytes │ Timestamps                    │
│  Null          │ 0 bytes │ Explicit absence              │
│  (missing)     │ 0 bytes │ Implicit absence              │
├──────────────────────────────────────────────────────────┤
│  Tip: Int32 is 4 bytes vs Double's 8 bytes.             │
│  For large collections, this matters.                    │
│  1M docs × 10 number fields = 40MB (Int32) vs 80MB      │
└──────────────────────────────────────────────────────────┘
```

### Null vs Missing — Query Behavior

```javascript
// These are DIFFERENT in MongoDB:
{ price: null }    // Field exists, value is null
{ }                // Field doesn't exist (missing)

// But this query matches BOTH:
db.products.find({ price: null })

// To distinguish:
db.products.find({ price: { $exists: true, $type: "null" } })  // Only null
db.products.find({ price: { $exists: false } })                // Only missing

// SQL comparison:
// In SQL, NULL is NULL. There's no concept of "column doesn't exist."
// In MongoDB, a field can exist-as-null or not-exist. Both are valid.
```

---

## Common Mistakes (SQL Developers Make)

### ❌ Mistake 1: Using Doubles for Money

```javascript
// WRONG — floating point precision loss
{ price: 19.99 }  // Actually stored as 19.989999999999998...

// RIGHT — Decimal128
{ price: NumberDecimal("19.99") }
```

### ❌ Mistake 2: Storing Dates as Strings

```javascript
// WRONG — can't do date math, can't range query efficiently
{ createdAt: "2024-01-15T10:30:00Z" }

// RIGHT — native Date type
{ createdAt: new Date("2024-01-15T10:30:00Z") }
```

### ❌ Mistake 3: Forgetting ObjectId in Queries

```javascript
// WRONG — string comparison, won't match any document
db.products.findOne({ _id: "507f1f77bcf86cd799439011" })

// RIGHT — ObjectId comparison
db.products.findOne({ _id: ObjectId("507f1f77bcf86cd799439011") })
```

### ❌ Mistake 4: Ignoring Type Inconsistency

```javascript
// Over time, different developers insert different types:
{ age: 25 }        // Int32
{ age: 25.0 }      // Double
{ age: "25" }      // String
{ age: "twenty-five" } // String

// Query: db.products.find({ age: { $gt: 20 } })
// Only returns numeric ages — silently ignores strings!
// Use schema validation to prevent this.
```

---

## Practice Exercises

### Exercise 1: Type Identification

What BSON type will each value be stored as?

```javascript
db.test.insertOne({
  a: 42,                    // ?
  b: NumberInt(42),          // ?
  c: NumberLong(42),         // ?
  d: NumberDecimal("42"),    // ?
  e: "42",                   // ?
  f: true,                   // ?
  g: null,                   // ?
  h: new Date(),             // ?
  i: /pattern/i,             // ?
  j: [1, 2, 3],             // ?
  k: { nested: "doc" },     // ?
  l: ObjectId()              // ?
})
```

### Exercise 2: Type Migration

You discover your `products` collection has prices stored as mixed types (strings, doubles, and integers). Write a MongoDB script to:
1. Find all documents where `price` is not Decimal128
2. Convert them all to Decimal128

### Exercise 3: Null vs Missing

Write queries to find:
1. Products where `discount` is explicitly `null`
2. Products where `discount` field doesn't exist
3. Products where `discount` exists and is greater than 0

---

## Interview Q&A

**Q1: What is BSON and why does MongoDB use it instead of JSON?**
> BSON (Binary JSON) is a binary-encoded format that adds rich types (Date, Decimal128, ObjectId, Binary), length prefixes for fast traversal, and efficient numeric encoding. MongoDB uses it because JSON lacks type distinction (no int vs float), has no date type, and requires full parsing to access any field.

**Q2: How do you handle monetary values in MongoDB?**
> Use `Decimal128` (`NumberDecimal()` in shell, `Decimal128.fromString()` in Node.js). Never use doubles for money due to IEEE 754 floating-point precision issues. This is different from SQL where `DECIMAL(10,2)` is the standard and enforced per column.

**Q3: What's the difference between `null` and a missing field in MongoDB?**
> `{ field: null }` means the field exists with a null value. A missing field means the key doesn't exist in the document. `find({ field: null })` matches both. Use `$exists` and `$type: "null"` to distinguish them. SQL has no equivalent — every column always exists in every row.

**Q4: What happens if the same field has different types across documents?**
> MongoDB stores whatever you give it. Queries using comparison operators (`$gt`, `$lt`) only match documents with compatible types — strings and numbers are not compared. This is a common source of subtle bugs. Use schema validation to prevent type inconsistency.

**Q5: How does BSON type ordering work?**
> BSON defines a comparison order: MinKey < Null < Numbers < Symbol < String < Object < Array < BinData < ObjectId < Boolean < Date < Timestamp < Regex < MaxKey. This matters for sorting and range queries across mixed-type fields.
