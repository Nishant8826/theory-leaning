# 🍃 MongoDB – Complete Revision Guide

Welcome to the comprehensive MongoDB Master Revision Guide. This single document compiles all core architectural concepts, SQL-to-NoSQL mental models, BSON data types, CRUD operators, indexing strategies, aggregation pipelines, schema design patterns, transactions, Mongoose features, and production deployment best practices across all 22 modules. Use this guide to review the entire curriculum in under 30 minutes from a single, self-contained reference file.

---

## 📌 Module Navigation

* [01. Introduction & Setup](#01-introduction--setup)
* [02. SQL vs MongoDB — Mental Model](#02-sql-vs-mongodb--mental-model)
* [03. Databases, Collections & Documents](#03-databases-collections--documents)
* [04. BSON & Data Types](#04-bson--data-types)
* [05. CRUD — Create](#05-crud--create)
* [06. CRUD — Read](#06-crud--read)
* [07. CRUD — Update](#07-crud--update)
* [08. CRUD — Delete](#08-crud--delete)
* [09. Query Operators](#09-query-operators)
* [10. Projection & Pagination](#10-projection--pagination)
* [11. Indexes](#11-indexes)
* [12. Aggregation Framework](#12-aggregation-framework)
* [13. $lookup & Relations](#13-lookup--relations)
* [14. Embedding vs Referencing](#14-embedding-vs-referencing)
* [15. Schema Design Strategies](#15-schema-design-strategies)
* [16. Transactions](#16-transactions)
* [17. Validation & Schema](#17-validation--schema)
* [18. Mongoose Deep Dive](#18-mongoose-deep-dive)
* [19. Performance Optimization](#19-performance-optimization)
* [20. When to Use MongoDB vs SQL](#20-when-to-use-mongodb-vs-sql)
* [21. Real-World Architecture](#21-real-world-architecture)
* [22. Deployment & Scaling](#22-deployment--scaling)

---

## 01. Introduction & Setup

🔗 **Full Lesson:** [01_Introduction_And_Setup.md](./01_Introduction_And_Setup.md)

* **What**: MongoDB is an open-source, document-oriented NoSQL database that stores data as flexible, hierarchical BSON (Binary JSON) documents within collections.
* **Why It Exists**: Relational databases struggle with rapidly evolving schemas (costly `ALTER TABLE` locks on large tables), hierarchical/nested data requiring multiple slow joins, and horizontal scaling across distributed commodity hardware.
* **Key Concepts**:
  * **Relational vs Document Mapping**: Tables map to Collections, Rows map to Documents, Columns map to Fields, Primary Keys map to `_id` (auto-generated 12-byte `ObjectId`), and JOINs map to `$lookup` or document embedding.
  * **Core Architectural Strengths**: Dynamic schema evolution (heterogeneous documents in the same collection), built-in horizontal sharding, native replica sets with automated failover, and high write throughput without table-locking DDL.
  * **Installation & Ecosystem**: `mongod` (database daemon server on default port `27017`), `mongosh` (interactive JavaScript shell replacing legacy `mongo`), MongoDB Compass (GUI visual query profiler and index analyzer), and official drivers (Native Node.js `mongodb` driver & `mongoose` ODM).
  * **Basic Shell Commands**: `show dbs` (lists non-empty databases), `use <dbName>` (switches database context, created lazily on first document write), and `show collections` (lists collection tables).
  * **Connection Architecture**: Node.js clients initialize a single shared `MongoClient` instance managing an internal connection pool rather than opening per-request connections.

### Key Commands / Code Example:

```javascript
// mongosh CLI basic commands
use ecommerce; // Switch to 'ecommerce' database context (created implicitly on write)

// Insert a sample document into 'products' collection
db.products.insertOne({
  name: "Gaming Laptop",
  price: 1299.99,
  brand: "Dell",
  category: { name: "Electronics", slug: "electronics" }, // Nested embedded object
  tags: ["computer", "portable", "work"],                 // Native array field
  stock: 45,
  ratings: { average: 4.5, count: 234 },
  createdAt: new Date()
});

// Query all documents in the collection
db.products.find();
```

> [!NOTE]
> Databases and collections are created **lazily** in MongoDB. Running `use ecommerce` does not immediately write metadata to disk; the database only appears in `show dbs` after inserting your first document.

---

## 02. SQL vs MongoDB — Mental Model

🔗 **Full Lesson:** [02_SQL_Vs_MongoDB_Mental_Model.md](./02_SQL_Vs_MongoDB_Mental_Model.md)

* **What**: The fundamental paradigm shift from data-driven normalization (SQL 3NF) to query-driven access pattern design (MongoDB document modeling).
* **Why It Exists**: Designing schemas around entities and foreign keys forces applications to perform multiple disk seeks and CPU-expensive in-memory joins; query-driven design co-locates related data on disk to serve an entire page in a single disk read.
* **Key Concepts**:
  * **Design Philosophy**: SQL designs *Data First, Queries Later* (entities → normalization → foreign keys). MongoDB designs *Queries First, Schema Around Access Patterns* (identify application UI requirements → co-locate data).
  * **Data Locality Advantage**: In SQL, fetching an order requires 3–4 index lookups and disk seeks across `orders`, `order_items`, `customers`, and `products`. In MongoDB, an entire order is stored contiguously on disk as one BSON block, requiring exactly 1 index lookup and 1 disk seek.
  * **The Two Core Schema Questions**: 
    1. *How will the application read this data?* (Embed data that is read together).
    2. *How will the data change over time?* (Reference data that is volatile, unbounded, or updated independently).
  * **Denormalization as Default**: Storing copies of related fields (e.g., customer name and product price inside an order document) eliminates joins on hot read paths while freezing historical snapshots.
  * **Common SQL Developer Anti-Patterns**: Creating 1:1 collections for every entity (e.g., `user_addresses`, `user_settings`), using `$lookup` on every query to simulate SQL joins, and assuming schema-less means zero validation.

### Key Commands / Code Example:

```javascript
// MongoDB Approach: Single document read serves entire order details view
db.orders.findOne({ _id: ObjectId("65a1b2c3d4e5f6a7b8c9d0e1") });

// Returns contiguous BSON containing customer snapshot and line items
// No $lookup or multiple round trips required
{
  _id: ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),
  customer: { name: "John Doe", email: "john@example.com" }, // Embedded snapshot
  items: [
    { product: "Laptop", price: 999.99, quantity: 1 },
    { product: "Mouse", price: 29.99, quantity: 2 }
  ],
  total: 1059.97,
  status: "shipped",
  createdAt: ISODate("2024-01-15T10:30:00Z")
}
```

> [!IMPORTANT]
> Avoid treating `$lookup` as a drop-in replacement for SQL `JOIN`. `$lookup` performs nested-loop evaluations in the aggregation memory space and is 5–50x slower than SQL native engine joins. Always design documents for **data locality**.

---

## 03. Databases, Collections & Documents

🔗 **Full Lesson:** [03_Databases_Collections_Documents.md](./03_Databases_Collections_Documents.md)

* **What**: The architectural hierarchy of MongoDB storage: Server Instance (`mongod`) → Databases → Collections → Documents → Fields.
* **Why It Exists**: Hierarchical, polymorphic document collections replace rigid rectangular tables, allowing records within the same collection to have varying attributes without sparse column bloat or complex EAV anti-patterns.
* **Key Concepts**:
  * **Storage Hierarchy**: `mongod` manages system databases (`admin`, `config`, `local`) alongside application databases containing individual collection namespaces.
  * **Polymorphic Documents**: Documents in the same collection can contain different fields and types (e.g., electronic items with `specs` and apparel with `sizes`).
  * **The Mandatory `_id` Field**: Every document must contain a unique `_id`. If omitted, MongoDB automatically generates a 12-byte `ObjectId`.
  * **Anatomy of an ObjectId (12 bytes / 24 hex characters)**:
    * `4 bytes`: Unix epoch timestamp in seconds (extractable via `ObjectId.getTimestamp()`).
    * `5 bytes`: Random value unique to the machine and process.
    * `3 bytes`: Incrementing counter starting at a random number.
  * **16MB Document Limit**: A single BSON document cannot exceed 16MB. This hard architectural limit prevents excessive RAM/cache bloat and forces developers to reference unbounded arrays (e.g., unlimited logs or reviews).
  * **Capped Collections**: Fixed-size circular buffer collections (`capped: true, size: N, max: M`) that automatically overwrite the oldest documents when full. They maintain strict insertion order, support high-speed logging, but cannot have documents manually deleted.

### Key Commands / Code Example:

```javascript
// Create a Capped Collection for circular event logging (10MB max, 5000 docs)
db.createCollection("system_logs", {
  capped: true,
  size: 10485760, // 10MB in bytes
  max: 5000       // Maximum number of documents
});

// Extract creation timestamp directly from auto-generated ObjectId
const docId = ObjectId("65a1b2c3d4e5f6a7b8c9d0e1");
console.log("Document Created At:", docId.getTimestamp());

// Native Driver collection creation with JSON Schema validation
await db.createCollection('products', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['name', 'price'],
      properties: {
        name: { bsonType: 'string' },
        price: { bsonType: 'number', minimum: 0 }
      }
    }
  }
});
```

> [!WARNING]
> You cannot delete individual documents from a **capped collection** (`deleteOne` throws an error). You can only insert new documents (which overwrite the oldest) or drop the entire collection via `db.collection.drop()`.

---

## 04. BSON & Data Types

🔗 **Full Lesson:** [04_BSON_And_Data_Types.md](./04_BSON_And_Data_Types.md)

* **What**: BSON (Binary JSON) is the binary-encoded serialization format used internally by MongoDB to store documents and perform network wire transmission.
* **Why It Exists**: Standard JSON only supports 7 basic types (no date, no int vs float, no binary, imprecise numbers) and requires complete parsing to access fields; BSON adds 20+ strongly typed definitions and length prefixes for fast field traversal.
* **Key Concepts**:
  * **BSON Scalar Types**: `Double` (64-bit float), `String` (UTF-8), `Boolean`, `Int32` (`NumberInt`), `Int64` (`NumberLong`), `Decimal128` (`NumberDecimal`), `Date` (UTC milliseconds), `Null`, and `ObjectId`.
  * **Container & Special Types**: `Object` (embedded subdocument), `Array`, `BinData` (UUIDs/buffers), `Regex`, `Timestamp` (internal replication sequence), `MinKey`, and `MaxKey`.
  * **Type is Per-Value**: In SQL, types are enforced per-column. In raw MongoDB, different documents can store different types in the same field name (e.g., `price: 99.99` vs `price: "free"`), which causes silent query exclusions unless validated.
  * **Handling Monetary Values (`Decimal128`)**: Never use standard JavaScript numbers (`Double`) for currency due to IEEE 754 floating-point rounding errors (`0.1 + 0.2 !== 0.3`). Always use `NumberDecimal("19.99")` in shell and `Decimal128.fromString("19.99")` in Node.js.
  * **Null vs Missing Fields**: `{ price: null }` (field exists with null value) is distinct from `{}` (field is absent). Querying `{ price: null }` matches both; use `{ price: { $exists: true, $type: "null" } }` to differentiate.
  * **BSON Type Ordering**: For mixed-type comparisons: MinKey < Null < Numbers (Int32, Int64, Double, Decimal) < Symbol < String < Object < Array < BinData < ObjectId < Boolean < Date < Timestamp < Regex < MaxKey.

### Key Commands / Code Example:

```javascript
const { MongoClient, ObjectId, Decimal128, Int32, Long } = require('mongodb');

// Inserting accurate BSON types via Node.js Native Driver
await db.collection('products').insertOne({
  name: "Precision Scale",
  price: Decimal128.fromString("199.99"), // 128-bit exact decimal for currency
  stock: new Int32(250),                  // 32-bit integer (4 bytes on disk)
  totalViews: Long.fromNumber(1500000),   // 64-bit integer (8 bytes on disk)
  isActive: true,                         // Boolean (1 byte)
  tags: ["gadget", "tool"],               // Native array
  specs: { precision: "0.01g" },          // Embedded object
  createdAt: new Date(),                  // BSON UTC Date (8 bytes)
  imageBuffer: Buffer.from("...")         // BSON BinData
});

// Querying fields by BSON type to detect data anomalies
db.products.find({ price: { $type: "string" } }); // Detect bad string prices
```

> [!IMPORTANT]
> Always query `_id` using an `ObjectId` instance (`{ _id: new ObjectId("...") }`). Querying `{ _id: "65a1b2..." }` as a string will return `null` because BSON string and ObjectId types do not match.

---

## 05. CRUD — Create

🔗 **Full Lesson:** [05_CRUD_Create.md](./05_CRUD_Create.md)

* **What**: Operations that insert new BSON documents into collections (`insertOne`, `insertMany`, `bulkWrite`).
* **Why It Exists**: Create operations allow applications to store complex nested payloads in a single network round-trip without prior DDL table migrations.
* **Key Concepts**:
  * **`insertOne(doc)`**: Inserts a single document and returns `{ acknowledged: true, insertedId: ObjectId }`.
  * **`insertMany([docs], options)`**: Inserts an array of documents.
  * **Ordered vs Unordered Inserts (`ordered: false`)**:
    * `ordered: true` (default): Executes sequentially. If document 2 fails (e.g., duplicate `_id`), execution halts and remaining documents are skipped.
    * `ordered: false`: Continues inserting remaining documents despite individual failures (equivalent to SQL `INSERT IGNORE` or `ON CONFLICT DO NOTHING`).
  * **Upsert Behavior (`{ upsert: true }`)**: When combined with `updateOne`, inserts a new document if no match is found, or updates the existing document. Use `$setOnInsert` for fields (like `createdAt`) that should only be initialized upon insertion.
  * **Write Concern (`w`, `j`, `wtimeout`)**: Controls durability guarantees.
    * `w: 1` (default): Acknowledged by primary node in memory.
    * `w: "majority"`: Acknowledged by a majority of replica set members.
    * `j: true`: Acknowledged only after writing to the on-disk journal (WAL).
  * **Bulk Writes (`bulkWrite`)**: Executes mixed batches of inserts, updates, and deletes in a single round-trip.

### Key Commands / Code Example:

```javascript
// Bulk Write combining inserts, upserts, and stock adjustments in 1 round trip
await db.collection('products').bulkWrite([
  {
    insertOne: {
      document: { name: 'USB-C Cable', price: Decimal128.fromString('9.99'), stock: 500 }
    }
  },
  {
    updateOne: {
      filter: { sku: 'MOUSE-001' },
      update: {
        $set: { name: 'Wireless Ergonomic Mouse', updatedAt: new Date() },
        $setOnInsert: { stock: 100, createdAt: new Date() } // Set only if inserted
      },
      upsert: true
    }
  },
  {
    updateOne: {
      filter: { sku: 'LAPTOP-001' },
      update: { $inc: { stock: -1 } } // Decrement stock atomically
    }
  }
], { ordered: false }); // Unordered = parallel execution on server
```

> [!TIP]
> Never insert documents one-by-one inside a `for` loop (N network round-trips). Always batch records using `insertMany(docs, { ordered: false })` or `bulkWrite()` to maximize write throughput.

---

## 06. CRUD — Read

🔗 **Full Lesson:** [06_CRUD_Read.md](./06_CRUD_Read.md)

* **What**: Methods for querying and retrieving documents from collections (`find`, `findOne`, `countDocuments`).
* **Why It Exists**: Query operations locate documents using flexible JSON filter objects, leveraging embedded indexes and dot-notation to extract deeply nested fields without joins.
* **Key Concepts**:
  * **Cursor vs Result Set**: `find()` returns a lazy **Cursor** (iterator). Data is fetched in batches (default 101 docs or 4MB). Calling `.toArray()` loads all matched documents into application memory, which causes memory exhaustion on large collections.
  * **`findOne(filter)`**: Returns the first matching document directly (or `null`) without returning a cursor.
  * **Dot Notation for Nested Queries**: Queries traverse nested object fields (`"category.name": "Electronics"`) and arrays (`tags: "portable"`).
  * **Execution Pipeline Order**: In MongoDB cursor chaining, stage order is deterministic: `Filter ($match) → Sort ($sort) → Skip ($skip) → Limit ($limit)` regardless of JavaScript method call sequence.
  * **Counting Documents**: `countDocuments(filter)` performs an accurate collection/index scan. `estimatedDocumentCount()` returns a near-instant count based on collection metadata (for unfiltered total sizes).
  * **`distinct(field, filter)`**: Returns an array of unique values across the collection.

### Key Commands / Code Example:

```javascript
// Complex read query with filtering, nested dot notation, sorting, and pagination
const cursor = db.collection('products').find({
  price: { $gte: 50, $lte: 1000 },
  "category.slug": "electronics",
  stock: { $gt: 0 },
  tags: { $in: ["computer", "gaming"] }
})
.project({ name: 1, price: 1, "ratings.average": 1, _id: 0 }) // Include only needed fields
.sort({ "ratings.average": -1, price: 1 })                     // Sort by rating DESC, price ASC
.skip(20)                                                      // Offset
.limit(10);                                                    // Page size

// Memory-efficient cursor streaming using for-await
for await (const product of cursor) {
  console.log(`Processing: ${product.name}`);
}
```

> [!NOTE]
> Projections cannot mix field inclusion (`name: 1`) and exclusion (`specs: 0`) in the same query. The only exception is `_id`, which can be explicitly excluded (`_id: 0`) alongside inclusions.

---

## 07. CRUD — Update

🔗 **Full Lesson:** [07_CRUD_Update.md](./07_CRUD_Update.md)

* **What**: Operations that modify existing documents using granular field-level update operators (`updateOne`, `updateMany`, `replaceOne`, `findOneAndUpdate`).
* **Why It Exists**: In SQL, updating a single column rewrites the entire row; MongoDB update operators modify specific fields in-place atomically without a read-modify-write cycle.
* **Key Concepts**:
  * **Field Update Operators**:
    * `$set`: Modifies or adds specific fields without overwriting other properties.
    * `$unset`: Removes a field entirely from the document (no `ALTER TABLE` needed).
    * `$inc` / `$mul`: Atomically increments, decrements, or multiplies numeric values.
    * `$min` / `$max`: Updates field value only if the specified value is smaller/larger than current.
    * `$currentDate`: Sets field to current date or timestamp.
    * `$rename`: Renames a field key in-place.
  * **Array Update Operators**:
    * `$push`: Appends values to an array (supports modifiers: `$each`, `$slice` to cap size, `$sort`).
    * `$pull`: Removes matching items from an array by value or condition.
    * `$addToSet`: Adds items only if they do not already exist (guarantees uniqueness).
    * `$pop`: Removes first (`-1`) or last (`1`) element.
  * **Positional Array Operators**:
    * `items.$`: Refers to the *first* array element that matched the query filter.
    * `items.$[]`: Applies update to *all* elements in the array.
    * `items.$[elem]` + `arrayFilters`: Updates array elements that match specific sub-conditions.
  * **`findOneAndUpdate(filter, update, options)`**: Atomically finds, modifies, and returns a document (`returnDocument: 'after'` or `'before'`). Solves race conditions in concurrent stock deduction.

### Key Commands / Code Example:

```javascript
// Atomic inventory deduction with race condition prevention
const updatedProduct = await db.collection('products').findOneAndUpdate(
  {
    _id: new ObjectId(productId),
    stock: { $gte: requestedQty } // Guard: only execute if sufficient stock exists
  },
  {
    $inc: { stock: -requestedQty, "stats.totalSold": requestedQty },
    $set: { updatedAt: new Date() }
  },
  { returnDocument: 'after' } // Return document state AFTER modification
);

if (!updatedProduct) {
  throw new Error("Product out of stock or does not exist");
}

// Updating specific array elements using arrayFilters
await db.collection('orders').updateOne(
  { _id: orderId },
  { $set: { "items.$[item].discountApplied": true } },
  { arrayFilters: [{ "item.price": { $gte: 100 } }] } // Discount only items >= 100
);
```

> [!WARNING]
> Never omit `$set` in `updateOne`. In older drivers, updating with `{ name: "New" }` instead of `{ $set: { name: "New" } }` would wipe out the entire document, replacing it with only the `name` field!

---

## 08. CRUD — Delete

🔗 **Full Lesson:** [08_CRUD_Delete.md](./08_CRUD_Delete.md)

* **What**: Operations that delete documents from collections (`deleteOne`, `deleteMany`, `findOneAndDelete`, `drop`).
* **Why It Exists**: Allows removal of documents while maintaining index consistency; however, MongoDB enforces **no foreign key cascade deletes**, making orphaned reference management an application responsibility.
* **Key Concepts**:
  * **`deleteOne(filter)` & `deleteMany(filter)`**: Deletes single or multiple matching documents and returns `{ acknowledged: true, deletedCount: N }`.
  * **`findOneAndDelete(filter, options)`**: Atomically removes and returns the deleted document (ideal for archiving, audit logging, and queue job consumption).
  * **`db.collection.drop()` vs `deleteMany({})`**:
    * `deleteMany({})`: Scans every document, removes entries from indexes, writes to WAL—O(n) and slow for millions of records.
    * `drop()`: Deletes collection metadata and drops storage blocks instantly—O(1).
  * **No CASCADE Deletes**: Deleting a customer does NOT delete their referenced orders. Applications must use transactions, manual multi-collection cleanup, or embedded architectures where deleting parent automatically purges children.
  * **TTL (Time To Live) Indexes**: Automatically deletes documents after a specified time threshold based on a date field. Handled by a background thread running every 60 seconds (ideal for user sessions, OTP tokens, and temporary logs).
  * **Disk Space Reclamation**: Deleting documents frees storage inside WiredTiger data files for future inserts, but does NOT return disk space to the OS. Use `db.collection.compact()` to reclaim OS space.

### Key Commands / Code Example:

```javascript
// 1. Create a TTL index to auto-delete expired user sessions after 24 hours (86400s)
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 86400 } // Auto-deleted 24 hours after 'createdAt' timestamp
);

// 2. Atomic find and archive pattern
const archivedOrder = await db.collection('orders').findOneAndDelete(
  { status: 'cancelled', createdAt: { $lt: new Date('2023-01-01') } },
  { sort: { createdAt: 1 } }
);

if (archivedOrder) {
  await db.collection('orders_archive').insertOne({
    ...archivedOrder,
    archivedAt: new Date()
  });
}
```

> [!IMPORTANT]
> TTL indexes only function on fields containing a true BSON `Date` object (or array of Dates). If the field contains a string or timestamp integer, the background cleanup thread will ignore the document and it will never expire.

---

## 09. Query Operators

🔗 **Full Lesson:** [09_Query_Operators.md](./09_Query_Operators.md)

* **What**: JSON-based filter operators replacing SQL `WHERE` clauses for comparison, logical branching, element evaluation, and array matching.
* **Why It Exists**: Enables rich declarative filtering over complex hierarchical documents and array elements directly within the database engine.
* **Key Concepts**:
  * **Comparison Operators**: `$eq` (`=`), `$ne` (`!=`), `$gt` (`>`), `$gte` (`>=`), `$lt` (`<`), `$lte` (`<=`), `$in` (`IN (...)`), and `$nin` (`NOT IN (...)`).
  * **Logical Operators**:
    * Implicit `$and`: Multiple fields in one object `{ brand: "Dell", stock: { $gt: 0 } }`.
    * Explicit `$and`: Required when specifying multiple conditions on the same field key to prevent JSON key overwrite `{ $and: [{ price: { $gt: 100 } }, { price: { $lt: 500 } }] }`.
    * `$or`: Matches if any condition is true; each branch can leverage independent indexes.
    * `$nor`: Matches if all conditions evaluate to false.
    * `$not`: Inverts the effect of a query operator and includes documents where the field is missing.
  * **Element Operators**: `$exists: true/false` (tests field existence) and `$type` (tests BSON type).
  * **Array Query Operators**:
    * `{ tags: "tech" }`: Matches if array contains the scalar value.
    * `$all`: Matches if array contains *all* specified elements.
    * `$size`: Matches arrays of exact length (cannot do range checks).
    * `$elemMatch`: Requires a **single array element** to satisfy all criteria (unlike dot notation which can match different elements across criteria).
  * **Evaluation Operators**: `$regex` (pattern matching), `$expr` (allows field-to-field comparisons like `salePrice < originalPrice`), and `$text` (full-text search).

### Key Commands / Code Example:

```javascript
// Query utilizing comparison, logical OR, array $elemMatch, and $expr
db.orders.find({
  status: { $in: ["processing", "shipped"] },
  $or: [
    { total: { $gte: 500 } },
    { "customer.tier": "VIP" }
  ],
  // $elemMatch: guarantees BOTH conditions match the SAME line item
  items: {
    $elemMatch: {
      price: { $gte: 100 },
      quantity: { $gte: 2 }
    }
  },
  // $expr: compares two fields in the same document
  $expr: { $gt: ["$shippingFee", "$discount"] }
});
```

> [!WARNING]
> Unanchored regular expressions (e.g., `{ name: { $regex: /laptop/i } }`) perform full collection scans (`COLLSCAN`), identical to SQL `LIKE '%laptop%'`. Always use anchored regex (`/^laptop/i`) to leverage B-tree indexes, or create a `$text` index.

---

## 10. Projection & Pagination

🔗 **Full Lesson:** [10_Projection_And_Pagination.md](./10_Projection_And_Pagination.md)

* **What**: Mechanisms to restrict returned document fields (Projection) and partition large result sets into pages (Pagination).
* **Why It Exists**: Reduces network bandwidth and RAM usage by preventing full 15KB+ documents from being sent over the wire when only a few fields are needed.
* **Key Concepts**:
  * **Field Inclusion / Exclusion**: `{ name: 1, price: 1 }` returns only `name`, `price`, and `_id`. `{ specs: 0 }` returns all fields except `specs`.
  * **Array Projection Operators**:
    * `$slice`: Returns a subset of an array `{ reviews: { $slice: 5 } }` (first 5) or `{ reviews: { $slice: -3 } }` (last 3).
    * `$` (Positional Projection): Returns only the first array element that matched the query filter `{ "reviews.$": 1 }`.
    * `$elemMatch` Projection: Projects only the first element in an array matching a specific condition.
  * **Offset-Based Pagination (`skip` / `limit`)**: Simple to implement for admin panels (`.skip((page - 1) * limit).limit(limit)`), but degrades to $O(N)$ on deep pages because MongoDB must scan and discard all skipped documents.
  * **Keyset / Cursor-Based Pagination**: High-performance $O(1)$ pagination using index range filters (`{ _id: { $gt: lastSeenId } }`). Eliminates performance degradation and prevents duplicate/missed records when documents are inserted in real time.
  * **Covered Queries**: When all queried filter fields and all projected return fields exist within a single index (and `_id: 0` is set), MongoDB satisfies the entire query from RAM index keys (`totalDocsExamined: 0`).

### Key Commands / Code Example:

```javascript
// High-performance Keyset Pagination Endpoint (Node.js)
app.get('/api/products/cursor-feed', async (req, res) => {
  const { cursor, limit = 20 } = req.query;
  const filter = { isActive: true };

  // Keyset condition: fetch documents created after the last seen item
  if (cursor) {
    filter._id = { $gt: new ObjectId(cursor) };
  }

  const products = await db.collection('products')
    .find(filter)
    .project({ name: 1, price: 1, brand: 1 }) // Field projection
    .sort({ _id: 1 })                          // Must sort by keyset field
    .limit(parseInt(limit) + 1)               // Fetch 1 extra to check hasMore
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

> [!TIP]
> Always aim for **Covered Queries** on high-frequency read endpoints. Create a compound index on `{ category: 1, price: 1, name: 1 }` and project `{ category: 1, price: 1, name: 1, _id: 0 }` to achieve zero disk seeks.

---

## 11. Indexes

🔗 **Full Lesson:** [11_Indexes.md](./11_Indexes.md)

* **What**: B-tree data structures that persist ordered subsets of collection fields to accelerate query lookups from $O(N)$ collection scans to $O(\log N)$ index scans.
* **Why It Exists**: Without indexes, every query executes a `COLLSCAN` reading every document from disk; indexes allow WiredTiger to jump directly to matching leaf pointers in memory.
* **Key Concepts**:
  * **Index Types**:
    * **Single Field**: `{ price: 1 }` (ascending) or `{ createdAt: -1 }` (descending).
    * **Compound Index**: `{ category: 1, price: -1 }` (index on multiple keys; order and sort direction matter).
    * **Multikey Index**: Automatically created when indexing an array field (creates an index entry for every array item). Compound indexes can contain at most one array field.
    * **Unique Index**: `{ email: 1 }, { unique: true }` enforces uniqueness (rejects duplicates with error `E11000`).
    * **Partial Index**: Indexes only documents matching a filter `{ partialFilterExpression: { isActive: true } }` (saves RAM and index overhead).
    * **Sparse Index**: Indexes only documents where the indexed field actually exists.
    * **Text Index**: Enables tokenized search across strings (`{ name: "text", description: "text" }`). Only one text index allowed per collection.
    * **Geospatial Index (`2dsphere`)**: Calculates spherical geometries and distance radii (`$near`, `$geoWithin`).
    * **Wildcard Index (`$**`)**: Indexes all arbitrary sub-fields in highly dynamic attribute documents.
  * **The ESR Rule for Compound Indexes**:
    1. **E**quality: Fields with exact match filters (`=`, `$in`) come first.
    2. **S**ort: Fields defining sort order come second.
    3. **R**ange: Fields with inequality range filters (`$gt`, `$lt`, `$gte`) come last.
  * **Explain Plans (`.explain("executionStats")`)**:
    * `winningPlan.stage`: `IXSCAN` (good) vs `COLLSCAN` (bad).
    * Efficiency Ratio: `totalDocsExamined / nReturned ≈ 1` (ideal). If `totalDocsExamined >> nReturned`, the index is not selective.

### Key Commands / Code Example:

```javascript
// 1. Create a compound index following the ESR Rule (Equality -> Sort -> Range)
db.orders.createIndex(
  {
    customerId: 1,   // Equality (E)
    status: 1,       // Equality (E)
    createdAt: -1,   // Sort (S)
    total: 1         // Range (R)
  },
  { name: "idx_orders_esr" }
);

// 2. Query execution analysis (Explain Plan)
const stats = db.orders.find({
  customerId: ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),
  status: "completed",
  total: { $gte: 100 }
})
.sort({ createdAt: -1 })
.explain("executionStats");

console.log("Execution Stage:", stats.executionStats.executionStages.stage); // IXSCAN
console.log("Docs Examined:", stats.executionStats.totalDocsExamined);
console.log("Keys Examined:", stats.executionStats.totalKeysExamined);
```

> [!WARNING]
> Every additional index slows down write operations (`insertOne`, `updateOne`, `deleteOne`) because WiredTiger must update all corresponding B-trees. Audit unused indexes periodically via `db.collection.aggregate([{ $indexStats: {} }])`.

---

## 12. Aggregation Framework

🔗 **Full Lesson:** [12_Aggregation_Framework.md](./12_Aggregation_Framework.md)

* **What**: A multi-stage data processing pipeline that transforms, groups, calculates, and reshapes documents sequentially (replacing SQL `GROUP BY`, `HAVING`, window functions, and subqueries).
* **Why It Exists**: Allows complex data analytics, financial rollups, and document reshaping to execute natively in database memory without pulling raw datasets into application code.
* **Key Concepts**:
  * **Pipeline Mechanics**: Data flows sequentially through stages: `Input Docs → Stage 1 ($match) → Stage 2 ($group) → Stage 3 ($sort) → Output`.
  * **Core Pipeline Stages**:
    * `$match`: Filters documents (analogous to SQL `WHERE` when placed first; uses indexes).
    * `$group`: Groups documents by an `_id` key and computes accumulator metrics (`$sum`, `$avg`, `$min`, `$max`, `$push`, `$addToSet`). Set `_id: null` to aggregate the entire collection.
    * `$project` / `$addFields`: Adds computed properties, casts types (`$toDouble`, `$toString`), and reshapes output.
    * `$sort`, `$limit`, `$skip`: Orders and paginates pipeline streams.
    * `$unwind`: Deconstructs an array field from input documents to output one document for every array element (analogous to SQL `LATERAL JOIN` / `UNNEST`).
    * `$facet`: Executes multiple independent aggregation pipelines in parallel over the exact same input stream (ideal for e-commerce search results with facets, counts, and price stats).
  * **Field References (`$fieldName`)**: Field values inside expressions are referenced with a `$` prefix (e.g., `"$price"`).
  * **100MB RAM Stage Limit**: Each pipeline stage has a strict 100MB RAM limit. Pass `{ allowDiskUse: true }` to allow spilling to temporary disk storage for massive datasets.

### Key Commands / Code Example:

```javascript
// Comprehensive Sales Analytics Pipeline with $facet for parallel processing
db.orders.aggregate([
  // Stage 1: Filter completed orders in 2024 (uses index)
  { $match: {
    status: "completed",
    createdAt: { $gte: new Date("2024-01-01") }
  }},

  // Stage 2: Parallel execution of multiple analytic streams
  { $facet: {
    // Pipeline Stream A: Monthly revenue rollup
    monthlyRevenue: [
      { $group: {
        _id: { $dateToString: { format: "%Y-%m", date: "$createdAt" } },
        revenue: { $sum: { $toDouble: "$total" } },
        orderCount: { $sum: 1 }
      }},
      { $sort: { _id: 1 } }
    ],

    // Pipeline Stream B: Top 5 selling products by quantity
    topProducts: [
      { $unwind: "$items" },
      { $group: {
        _id: "$items.productId",
        productName: { $first: "$items.name" },
        totalQuantity: { $sum: "$items.quantity" },
        totalRevenue: { $sum: { $toDouble: "$items.subtotal" } }
      }},
      { $sort: { totalQuantity: -1 } },
      { $limit: 5 }
    ]
  }}
], { allowDiskUse: true });
```

> [!IMPORTANT]
> Always place `$match` and `$sort` stages at the **very beginning** of the aggregation pipeline. Only early `$match` and `$sort` stages can leverage database indexes; once data passes through `$group` or `$project`, indexes can no longer be used.

---

## 13. $lookup & Relations

🔗 **Full Lesson:** [13_Lookup_And_Relations.md](./13_Lookup_And_Relations.md)

* **What**: An aggregation stage that performs a left outer join between two collections within the same database.
* **Why It Exists**: Enables querying referenced relationships (1:Many, Many:Many) when full document embedding would cause unbounded document growth or excessive data duplication.
* **Key Concepts**:
  * **Basic `$lookup` Syntax**: Joins based on equality between `localField` and `foreignField`, outputting matched documents as an array field (`as: "joinedArray"`).
  * **Unwinding Joined Arrays**: `$lookup` always returns an array even for 1:1 relationships. Use `{ $unwind: "$customer" }` to flatten the joined array into a single object.
  * **Pipeline `$lookup` (Correlated Subqueries)**: Uses `let` variables and a nested `pipeline` to perform complex joins with custom filtering, projections, and sorting on the target collection.
  * **Performance Reality Check**: `$lookup` uses nested-loop execution. It is 5–50x slower than SQL relational joins. It must only be used on cold paths (e.g., admin panels, monthly reporting) and NEVER on hot user-facing read paths.
  * **Database Boundary**: `$lookup` cannot join across different MongoDB databases or across different sharded clusters.
  * **Application-Level Joins**: Fetching root documents, collecting foreign IDs, and querying related collections via `Promise.all([ ... ])` with `{ _id: { $in: ids } }` is frequently faster than complex multi-stage `$lookup` pipelines.

### Key Commands / Code Example:

```javascript
// Pipeline $lookup with variable passing and projection
db.orders.aggregate([
  { $match: { status: "pending" } },
  {
    $lookup: {
      from: "customers",
      let: { orderCustomerId: "$customerId" }, // Pass local field as variable
      pipeline: [
        { $match: {
          $expr: { $eq: ["$_id", "$$orderCustomerId"] } // Match with $$ prefix
        }},
        { $project: { name: 1, email: 1, phone: 1, _id: 0 } } // Project only needed fields
      ],
      as: "customer"
    }
  },
  { $unwind: "$customer" } // Flatten 1-element array to an object
]);
```

> [!WARNING]
> Always create an index on the `foreignField` of the target collection being joined. Running `$lookup` without an index on the foreign collection causes a full collection scan on every single incoming document!

---

## 14. Embedding vs Referencing

🔗 **Full Lesson:** [14_Embedding_Vs_Referencing.md](./14_Embedding_Vs_Referencing.md)

* **What**: The core architectural decision in MongoDB data modeling: storing related data inside the same parent document (Embedding) versus storing it in a separate collection linked by `ObjectId` (Referencing).
* **Why It Exists**: Choosing the wrong model results in either catastrophic 16MB document overflows (unbounded embedding) or excessive slow joins that destroy application latency (over-referencing).
* **Key Concepts**:
  * **When to Embed (Denormalize)**:
    * Data is always read together (e.g., Product Specifications).
    * 1:1 or 1:Few bounded relationships (e.g., User with max 5 shipping addresses).
    * Data belongs strictly to one parent with no independent lifecycle.
    * Point-in-time historical snapshots (e.g., Order items freezing product price at checkout).
  * **When to Reference (Normalize)**:
    * Unbounded 1:Many relationships (e.g., E-commerce product with 50,000+ reviews, IoT sensor logs).
    * Shared, frequently updated entity data (e.g., Category names shared across 10,000 products).
    * Many-to-Many relationships (e.g., Students enrolled in Courses).
    * Related data accessed independently (e.g., Blog comments moderated in an admin dashboard).
  * **The Hybrid Pattern (Best of Both Worlds)**: Store an `ObjectId` reference to maintain relational integrity, alongside a denormalized cache/snapshot of display fields (e.g., storing `customerId` plus `{ name, email }` inside the order).
  * **The Subset Pattern**: Embed the top 10 most recent reviews inside the main product document for instant UI rendering, and store the remaining 50,000 reviews in a separate `reviews` collection.

### Key Commands / Code Example:

```javascript
// Hybrid & Subset Pattern: E-Commerce Product Document
{
  _id: ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),
  name: "MacBook Pro 16",
  price: NumberDecimal("2499.99"),

  // 1. Embedded: Bounded, read together
  specs: { cpu: "M3 Max", ram: "36GB", storage: "1TB SSD" },

  // 2. Hybrid Reference: Category ID reference + cached display name
  categoryId: ObjectId("65a1b2c3d4e5f6a7b8c9d0aa"),
  categoryName: "Laptops", // Cached for fast UI display

  // 3. Computed Pattern: Pre-aggregated review metrics
  ratings: { average: 4.8, count: 1420 },

  // 4. Subset Pattern: Only top 3 recent reviews embedded; full reviews in separate collection
  recentReviews: [
    { user: "Alice", rating: 5, comment: "Incredible speed!", date: ISODate("2024-01-10") },
    { user: "Bob", rating: 4, comment: "Great display.", date: ISODate("2024-01-08") }
  ]
}
```

> [!IMPORTANT]
> The **16MB Document Limit** is your primary boundary check. If an array can grow indefinitely over time (e.g., `user.activityLogs`), it **must** be stored in a separate collection with references.

---

## 15. Schema Design Strategies

🔗 **Full Lesson:** [15_Schema_Design_Strategies.md](./15_Schema_Design_Strategies.md)

* **What**: Specialized architectural design patterns for solving common data modeling challenges in production MongoDB systems.
* **Why It Exists**: Relational normalization fails for polymorphic entities, time-series metrics, and high-frequency real-time counters; these patterns optimize storage footprint and query performance.
* **Key Concepts**:
  * **1. Attribute Pattern**: Solves polymorphic products with hundreds of sparse attributes. Converts varied top-level keys into an array of uniform key-value pairs (`attributes: [{ key: "ram", value: "16GB" }]`), allowing a single index `{ "attributes.key": 1, "attributes.value": 1 }` to serve all search filters.
  * **2. Bucket Pattern**: Solves high-frequency time-series IoT data. Groups thousands of individual log readings into a single document per hour/day with pre-aggregated statistics (`min`, `max`, `avg`), reducing index size by 99%.
  * **3. Computed Pattern**: Pre-computes and stores rollup metrics (e.g., rating averages, revenue totals) at write time using `$inc` rather than calculating expensive `$group` aggregations on every user read.
  * **4. Outlier Pattern**: Optimizes for the 99% standard use case while handling extreme exceptions (e.g., storing typical review counts directly in the product, but setting an `hasOverflow: true` flag to redirect extreme celebrity products to an overflow collection).
  * **5. Schema Versioning Pattern**: Adds a `schemaVersion: 1` field to every document. Applications maintain backward-compatible shape normalizers, enabling zero-downtime, continuous schema migrations without running locking database-wide migration scripts.
  * **6. Polymorphic Pattern**: Stores different entity types in the same collection using a `type` discriminator (e.g., `type: "article"`, `type: "video"`), leveraging partial indexes for type-specific lookups.

### Key Commands / Code Example:

```javascript
// 1. Attribute Pattern for Dynamic E-Commerce Specifications
{
  name: "Industrial Drill",
  sku: "TOOL-098",
  attributes: [
    { key: "voltage", value: "20V" },
    { key: "chuckSize", value: "0.5in" },
    { key: "brushless", value: "true" }
  ]
}
// Single Compound Index serves searches across all dynamic attributes:
db.products.createIndex({ "attributes.key": 1, "attributes.value": 1 });

// 2. Schema Versioning Pattern
function normalizeCustomer(doc) {
  if (doc.schemaVersion === 1) {
    // Upgrade legacy flat address string to structured subdocument in memory
    return { ...doc, address: { street: doc.legacyAddress, city: "Unknown" } };
  }
  return doc;
}
```

> [!NOTE]
> MongoDB 5.0+ introduced native **Time-Series Collections** (`timeseries: { timeField, metaField }`), which implement the Bucket Pattern automatically at the storage engine level with optimized columnar compression.

---

## 16. Transactions

🔗 **Full Lesson:** [16_Transactions.md](./16_Transactions.md)

* **What**: Multi-document ACID transactions that guarantee snapshot isolation across multiple documents, collections, and shards.
* **Why It Exists**: Provides all-or-nothing atomicity and consistency guarantees for multi-entity business workflows (e.g., bank transfers, cross-collection balance updates) where document embedding alone cannot prevent partial failures.
* **Key Concepts**:
  * **Single-Document vs Multi-Document ACID**: Single-document operations in MongoDB are **always atomic and ACID-compliant** by default without opening transactions. Multi-document transactions are reserved for operations spanning multiple separate documents.
  * **Performance Overhead**: Multi-document transactions incur a 10–40x latency penalty compared to single-document writes due to lock acquisitions, snapshot tracking, and WiredTiger storage engine checkpoint pressure.
  * **Prerequisites & Constraints**:
    * Requires a **Replica Set** (transactions fail on standalone `mongod` instances).
    * Maximum transaction execution lifetime is **60 seconds** (default).
    * Transaction oplog payload size cannot exceed 16MB.
    * Cannot execute DDL operations (e.g., `createCollection`, `createIndex`) inside a transaction.
  * **Callback API (`session.withTransaction`)**: The recommended production approach in Node.js. Automatically handles transient network errors (`TransientTransactionError`) and commit uncertainties (`UnknownTransactionCommitResult`) by retrying the entire transaction block.

### Key Commands / Code Example:

```javascript
const { MongoClient } = require('mongodb');

// Production-Grade Money Transfer using withTransaction Callback API
async function transferFunds(fromAccountId, toAccountId, amount) {
  const client = new MongoClient(process.env.MONGO_URI);
  await client.connect();
  const session = client.startSession();

  try {
    // withTransaction automatically retries on transient network/lock failures
    await session.withTransaction(async () => {
      const accounts = client.db('bank').collection('accounts');
      const transfers = client.db('bank').collection('transfers');

      // 1. Debit source account (with guard)
      const debitRes = await accounts.updateOne(
        { _id: fromAccountId, balance: { $gte: amount } },
        { $inc: { balance: -amount } },
        { session }
      );
      if (debitRes.modifiedCount === 0) {
        throw new Error("Insufficient balance or source account not found");
      }

      // 2. Credit destination account
      await accounts.updateOne(
        { _id: toAccountId },
        { $inc: { balance: amount } },
        { session }
      );

      // 3. Insert audit log
      await transfers.insertOne({
        from: fromAccountId,
        to: toAccountId,
        amount,
        status: "completed",
        timestamp: new Date()
      }, { session });
    });

    console.log("Transaction successfully committed!");
  } finally {
    await session.endSession();
    await client.close();
  }
}
```

> [!WARNING]
> Every database operation inside a transaction MUST receive the `{ session }` options object (e.g., `collection.updateOne(filter, update, { session })`). Omitting `{ session }` executes the operation outside the transaction, breaking atomicity!

---

## 17. Validation & Schema

🔗 **Full Lesson:** [17_Validation_And_Schema.md](./17_Validation_And_Schema.md)

* **What**: Database-level constraint enforcement using JSON Schema (`$jsonSchema`) and application-level validation via ODM models (Mongoose).
* **Why It Exists**: Protects database collections from corrupted data, invalid types, missing required fields, and malformed inputs while preserving flexible schema evolution.
* **Key Concepts**:
  * **Server-Level Validation (`$jsonSchema`)**: Configured directly on the collection via `db.createCollection` or `collMod`. Cannot be bypassed by any client (scripts, admin tools, native drivers).
  * **Validation Levels**:
    * `validationLevel: "strict"` (default): Validates all inserts and updates.
    * `validationLevel: "moderate"`: Validates new inserts and updates to *already-valid* documents, but skips checking legacy invalid documents (ideal for gradual migrations).
  * **Validation Actions**: `validationAction: "error"` (rejects write) vs `"warn"` (allows write but records a warning in server logs for testing rules).
  * **Two-Tier Validation Architecture**:
    * *Tier 1 (Application / Mongoose)*: Handles business logic, virtuals, default values, string trimming, and password hashing.
    * *Tier 2 (Database / JSON Schema)*: Serves as an unbypassable safety net at the storage engine level.
  * **Limitations Compared to SQL**: MongoDB JSON Schema does not support DB-level default values, auto-incrementing serials, or foreign key referential integrity checks.

### Key Commands / Code Example:

```javascript
// Modifying an existing collection with JSON Schema Validation
db.runCommand({
  collMod: "users",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "passwordHash", "role"],
      properties: {
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
          description: "Must be a valid email string"
        },
        passwordHash: {
          bsonType: "string",
          minLength: 60,
          description: "Bcrypt hash required"
        },
        age: {
          bsonType: "int",
          minimum: 18,
          maximum: 120,
          description: "Age must be an integer between 18 and 120"
        },
        role: {
          enum: ["customer", "admin", "vendor"],
          description: "Role can only be customer, admin, or vendor"
        }
      },
      additionalProperties: true // Allow new fields for schema evolution
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
});
```

> [!TIP]
> Avoid setting `additionalProperties: false` in `$jsonSchema` unless you require rigid structures. Setting it to `false` disables MongoDB's dynamic schema flexibility and makes schema evolution difficult.

---

## 18. Mongoose Deep Dive

🔗 **Full Lesson:** [18_Mongoose_Deep_Dive.md](./18_Mongoose_Deep_Dive.md)

* **What**: Mongoose is an Object Document Mapper (ODM) for Node.js providing strict schema definitions, validation, middleware hooks, virtuals, and reference population.
* **Why It Exists**: Simplifies application development by providing schema guardrails, automated timestamps, query builders, and business lifecycle hooks on top of the raw MongoDB driver.
* **Key Concepts**:
  * **Schema Definition**: Defines strong property types, custom regex validators, enums, nested subdocuments, and automatic timestamps (`{ timestamps: true }`).
  * **Virtual Properties**: Computed attributes accessible on document instances that are never persisted to disk (e.g., `fullName` derived from `firstName + lastName`).
  * **Virtual Populate**: Performs reverse reference joins without storing child arrays on the parent document.
  * **Middleware (Hooks)**:
    * `pre('save')`: Runs before saving (ideal for hashing passwords or generating URL slugs).
    * `pre('find')` / `pre('findOne')`: Automatically appends filters (e.g., soft-delete `{ deletedAt: { $exists: false } }`).
    * `post('save')`: Triggers external side-effects (e.g., sending emails, cache invalidation).
  * **Static vs Instance Methods**:
    * `schema.statics.findByEmail`: Custom query method attached directly to the `Model`.
    * `schema.methods.comparePassword`: Custom business logic method attached to a single document instance.
  * **Population (`populate()`)**: Replaces an `ObjectId` reference with the full referenced document by executing an automated `$in` query under the hood.
  * **The `.lean()` Optimization**: Skips hydrating full Mongoose document instances (getters, setters, change tracking), returning plain JavaScript objects. Yields a **5–10x speedup** on read-only queries.

### Key Commands / Code Example:

```javascript
const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
  name: { type: String, required: true, trim: true },
  slug: { type: String, unique: true, lowercase: true },
  price: { type: mongoose.Types.Decimal128, required: true },
  stock: { type: Number, required: true, min: 0 }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Virtual Field: Not saved in MongoDB, calculated on the fly
productSchema.virtual('isAvailable').get(function() {
  return this.stock > 0;
});

// Pre-save Middleware: Auto-generate slug from product name
productSchema.pre('save', function(next) {
  if (this.isModified('name')) {
    this.slug = this.name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  }
  next();
});

// Custom Static Helper Method
productSchema.statics.findInStock = function() {
  return this.find({ stock: { $gt: 0 } }).lean(); // Use .lean() for read performance
};

const Product = mongoose.model('Product', productSchema);
```

> [!IMPORTANT]
> Never use `.lean()` if you intend to modify the document and call `.save()`. `.lean()` returns a plain JavaScript object without Mongoose change-tracking or `.save()` methods.

---

## 19. Performance Optimization

🔗 **Full Lesson:** [19_Performance_Optimization.md](./19_Performance_Optimization.md)

* **What**: Strategies to minimize query latency, manage working set memory, optimize connection pools, and eliminate CPU bottlenecks.
* **Why It Exists**: Misconfigured queries, missing compound indexes, and oversized documents cause high disk I/O, cache thrashing, and database saturation under load.
* **Key Concepts**:
  * **The 5-Level Optimization Pyramid**:
    1. *Level 1 (Schema Design)*: Embedding vs referencing, bounding arrays, pre-aggregating data.
    2. *Level 2 (Indexing)*: Applying ESR rule, covered queries, eliminating unused indexes.
    3. *Level 3 (Query Optimization)*: Field projections, keyset pagination, `.lean()`.
    4. *Level 4 (Application Layer)*: Connection pooling, Redis caching, secondary reads.
    5. *Level 5 (Infrastructure)*: Sizing RAM to exceed working set, fast SSD storage, sharding.
  * **Working Set Sizing**: The working set (all actively accessed documents + all index B-trees) must fit within the WiredTiger RAM cache (typically 50–60% of total system RAM). When the working set exceeds RAM, page faults force disk reads, causing latency spikes from <1ms to 50ms+.
  * **Database Profiler**: Logs slow queries (`db.setProfilingLevel(1, { slowms: 100 })`) into the `system.profile` capped collection.
  * **Connection Pool Tuning**: Driver default pool size (100) can exhaust server memory under microservice architectures. Set `maxPoolSize: 10-20` per Node.js instance.
  * **Read Preferences for Secondary Nodes**: Route analytics or reporting workloads to secondary replica set nodes via `.readPreference(ReadPreference.SECONDARY_PREFERRED)` to protect the primary node from heavy reporting queries.

### Key Commands / Code Example:

```javascript
// 1. Enable Slow Query Profiler for queries exceeding 100ms
db.setProfilingLevel(1, { slowms: 100 });

// View top 5 slowest recent queries
db.system.profile.find().sort({ millis: -1 }).limit(5);

// 2. Production Connection Pool Configuration (Node.js)
const client = new MongoClient(process.env.MONGO_URI, {
  maxPoolSize: 20,              // Limit concurrent sockets per Node container
  minPoolSize: 5,               // Keep idle sockets warm
  maxIdleTimeMS: 30000,         // Clean up idle connections
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000
});

// 3. Cache-Aside Pattern with Redis
async function getCachedProduct(productId) {
  const cacheKey = `product:${productId}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const product = await db.collection('products')
    .findOne({ _id: new ObjectId(productId) });

  if (product) {
    await redis.set(cacheKey, JSON.stringify(product), 'EX', 300); // 5-minute TTL
  }
  return product;
}
```

> [!NOTE]
> Check index memory footprint using `db.collection.stats().totalIndexSize`. If total index size approaches available RAM, drop redundant indexes immediately to prevent WiredTiger cache thrashing.

---

## 20. When to Use MongoDB vs SQL

🔗 **Full Lesson:** [20_When_To_Use_MongoDB_Vs_SQL.md](./20_When_To_Use_MongoDB_Vs_SQL.md)

* **What**: A comprehensive technical evaluation matrix comparing MongoDB with relational SQL databases (PostgreSQL, MySQL).
* **Why It Exists**: Choosing the wrong database engine leads to either complex manual code workarounds or costly rewrites; production systems benefit most from **Polyglot Persistence**.
* **Key Concepts**:
  * **When MongoDB Wins**:
    * Hierarchical/nested document structures (Catalog, User Profiles, Content Management).
    * Dynamic, rapidly evolving schemas with frequent feature iterations.
    * High write throughput where relational table-locking DDL slows deployments.
    * Native horizontal sharding across distributed geographic regions.
    * Native Time-Series and Geospatial query workloads.
  * **When SQL Wins**:
    * Banking, financial ledgers, and payment systems requiring strict multi-table ACID guarantees.
    * Complex enterprise ERP/inventory systems with deep many-to-many relationships.
    * Heavy analytical reporting requiring complex multi-table joins, CTEs, and window functions.
    * Workloads requiring database-enforced foreign key referential integrity.
  * **Polyglot Persistence Architecture**: Real-world enterprise systems combine database strengths:
    * **MongoDB**: Product catalog, user profiles, content, real-time analytics.
    * **PostgreSQL**: Orders, payment ledgers, financial reporting.
    * **Redis**: Session storage, rate limiting, volatile cache.
    * **Elasticsearch**: Full-text fuzzy search and autocomplete.

### Key Commands / Code Example:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Enterprise Polyglot Persistence                   │
├──────────────────────────────────────────────────────────────────────┤
│  [ Client Requests ] ──► API Gateway / Node.js Backend              │
│                              │                                       │
│    ├──► MongoDB:       Product Catalog, User Profiles, Reviews       │
│    │                   (Dynamic Schema, High Read Locality)          │
│    │                                                                 │
│    ├──► PostgreSQL:    Orders, Invoices, Payment Ledger              │
│    │                   (Strict ACID, Foreign Key Constraints)        │
│    │                                                                 │
│    ├──► Redis:         Session Tokens, Rate Limiting, Feed Cache     │
│    │                   (Ultra-low Latency In-Memory KV)              │
│    │                                                                 │
│    └──► Elasticsearch: Catalog Search, Fuzzy Autocomplete, Logs     │
│                        (Inverted Index, Text Ranking)                │
└──────────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> The database decision is never binary. Avoid forcing an entire enterprise platform into a single database technology. Use MongoDB where data locality and schema flexibility excel, and SQL where multi-table relational integrity is paramount.

---

## 21. Real-World Architecture

🔗 **Full Lesson:** [21_Real_World_Architecture.md](./21_Real_World_Architecture.md)

* **What**: Production-ready architectural design for a Node.js/Express and MongoDB backend, encompassing modular layer separation, global error handling, JWT auth, Change Streams, and in-memory integration testing.
* **Why It Exists**: Moves beyond isolated code snippets to demonstrate how real enterprise backends structure services, manage connection lifecycles, and push real-time updates.
* **Key Concepts**:
  * **Layered Architectural Slicing**:
    * `models/`: Mongoose schemas, virtuals, and indexes.
    * `services/`: Business logic, calculations, and multi-document transactions.
    * `routes/` / `controllers/`: HTTP parsing, status codes, and input extraction.
    * `middleware/`: Auth guards, schema validators, rate limiters, global error interceptor.
  * **Centralized Error Handling**: Custom `ApiError` class mapped to an Express error handler that converts Mongoose `ValidationError`, `CastError` (bad ObjectId), and `11000` (duplicate key) into structured JSON responses.
  * **Authentication Architecture**: Password hashing with `bcrypt` in `pre('save')`, `select: false` on password fields, JWT access tokens (15m), and rotating refresh tokens (7d).
  * **Change Streams**: Real-time event streams that listen to database insertions, updates, and deletes (powered by the replica set oplog), pushing events to WebSockets (Socket.IO).
  * **Automated Integration Testing**: Testing against `mongodb-memory-server` to run isolated unit and integration test suites without hitting external staging databases.

### Key Commands / Code Example:

```javascript
// 1. Real-Time Order Notifications via Change Streams & Socket.IO
const changeStream = db.collection('orders').watch([
  { $match: {
    operationType: { $in: ['insert', 'update'] },
    'fullDocument.status': 'shipped'
  }}
], { fullDocument: 'updateLookup' });

changeStream.on('change', (change) => {
  const order = change.fullDocument;
  // Push live update to connected WebSocket client
  io.to(`user:${order.customerId}`).emit('orderShipped', {
    orderId: order._id,
    trackingNumber: order.trackingNumber
  });
});

// 2. In-Memory Database Test Setup (Jest + mongodb-memory-server)
const { MongoMemoryServer } = require('mongodb-memory-server');
let mongoServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  await mongoose.connect(mongoServer.getUri());
});

afterEach(async () => {
  // Clean all collections between tests
  const collections = mongoose.connection.collections;
  for (const key in collections) {
    await collections[key].deleteMany({});
  }
});

afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});
```

> [!TIP]
> Always mark sensitive fields (like passwords, MFA secrets, internal notes) with `select: false` in your Mongoose schema. This ensures they are never leaked in general queries unless explicitly retrieved via `.select('+password')`.

---

## 22. Deployment & Scaling

🔗 **Full Lesson:** [22_Deployment_And_Scaling.md](./22_Deployment_And_Scaling.md)

* **What**: Production deployment strategies for MongoDB, covering self-hosted EC2 configuration, MongoDB Atlas managed hosting, Replica Set high availability, horizontal Sharding, security hardening, and backup strategies.
* **Why It Exists**: Ensures the database cluster achieves 99.999% uptime, zero unauthorized data exposure, automatic failover recovery, and continuous scalability.
* **Key Concepts**:
  * **Replica Sets (Minimum 3 Nodes)**: 1 Primary (handles all writes and default reads) + 2 Secondaries (asynchronously replicate data via oplog). If Primary fails, an automated consensus election elects a new Primary in 10–30 seconds.
  * **Sharded Clusters (Horizontal Scaling)**:
    * `mongos` (Query Routers): Stateless gateway directing application queries to the correct shard.
    * `Config Servers`: 3-node replica set storing cluster metadata and chunk distribution ranges.
    * `Shards`: Independent replica sets holding partitioned data chunks.
  * **Shard Key Selection Criteria**: Must have high cardinality, even write distribution (avoid monotonic auto-incrementing timestamps as sole key to prevent hot shards), and support common query patterns.
  * **Security Hardening**: Enable `security.authorization: enabled`, create dedicated least-privilege users, enforce TLS/SSL encryption on the wire, bind to private VPC IPs, and never expose port `27017` to the public internet (`0.0.0.0/0`).
  * **Backup Strategies**:
    * `mongodump` / `mongorestore`: Logical binary backups for small-to-medium datasets.
    * Atlas Continuous Backups / Oplog PITR: Point-in-time recovery to any second within the retention window.
  * **Nginx Reverse Proxy & PM2**: Run Node.js applications in cluster mode under PM2, reverse proxied through Nginx with SSL termination, Gzip compression, and rate limiting.

### Key Commands / Code Example:

```bash
# 1. Automated Compressed Backup Script with 30-Day Retention Policy
mongodump --uri="mongodb://appuser:SecretPass@10.0.1.5:27017/ecommerce?authSource=ecommerce" \
  --gzip --archive="/backups/ecommerce_$(date +%Y%m%d_%H%M%S).gz"

# Restore from compressed archive
mongorestore --uri="mongodb://appuser:SecretPass@10.0.1.5:27017/ecommerce?authSource=ecommerce" \
  --gzip --archive="/backups/ecommerce_20240115_020000.gz"

# 2. Production PM2 Cluster Configuration (ecosystem.config.js)
module.exports = {
  apps: [{
    name: 'ecommerce-api',
    script: 'server.js',
    instances: 'max',       // Utilize all available CPU cores
    exec_mode: 'cluster',   // Zero-downtime reloads and internal load balancing
    max_memory_restart: '500M',
    env_production: {
      NODE_ENV: 'production',
      PORT: 3000,
      MONGO_URI: 'mongodb://appuser:pass@10.0.1.5:27017/ecommerce?authSource=ecommerce&replicaSet=rs0'
    }
  }]
};
```

> [!WARNING]
> Never deploy MongoDB without authentication (`security.authorization: enabled`) or with port `27017` open to `0.0.0.0/0`. Unsecured databases exposed to the public internet are continuously targeted by automated ransomware bots that drop collections and demand ransom.

---

Previous : [00_index.md](./00_index.md) | Index : [00_index.md](./00_index.md) | Next : [01_Introduction_And_Setup.md](./01_Introduction_And_Setup.md)
