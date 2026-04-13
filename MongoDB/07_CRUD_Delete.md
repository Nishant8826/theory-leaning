# CRUD — Delete

> 📌 **File:** 07_CRUD_Delete.md | **Level:** SQL Expert → MongoDB

---

## What is it?

Delete operations remove documents from collections. MongoDB provides `deleteOne()`, `deleteMany()`, and `findOneAndDelete()`. Unlike SQL, there's no `CASCADE` delete — if you delete a document that other documents reference, those references become orphaned. Referential integrity is **your responsibility**.

---

## SQL Parallel — Think of it like this

```
SQL:                                         MongoDB:
DELETE FROM t WHERE id = 5                 → db.t.deleteOne({ _id: 5 })
DELETE FROM t WHERE x > 10                → db.t.deleteMany({ x: { $gt: 10 } })
DELETE FROM t                              → db.t.deleteMany({})
TRUNCATE TABLE t                           → db.t.drop() + db.createCollection('t')
DROP TABLE t                               → db.t.drop()
DELETE ... RETURNING *                     → db.t.findOneAndDelete(filter)
DELETE ... CASCADE                         → ❌ Not supported — manual cleanup
```

---

## Why this is different from SQL (CRITICAL)

### 1. No CASCADE Deletes

```sql
-- SQL: Foreign key with CASCADE
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(id) ON DELETE CASCADE
);
-- Deleting a customer automatically deletes their orders
DELETE FROM customers WHERE id = 42;  -- Orders with customer_id=42 also deleted
```

```javascript
// MongoDB: No foreign keys, no CASCADE
// Deleting a customer does NOT delete their orders
await db.collection('customers').deleteOne({ _id: new ObjectId('...') });
// Orders still reference this customer — orphaned references!

// YOU must handle this manually:
const customerId = new ObjectId('...');
await db.collection('orders').deleteMany({ customerId });           // Delete orders
await db.collection('reviews').deleteMany({ 'author.id': customerId }); // Delete reviews
await db.collection('customers').deleteOne({ _id: customerId });    // Finally delete customer
```

### 2. Soft Delete is More Common in MongoDB

Because there's no CASCADE and cleanup is manual, many MongoDB applications prefer **soft deletes**:

```javascript
// Soft delete — mark as deleted instead of removing
await db.collection('products').updateOne(
  { _id: new ObjectId('...') },
  { $set: { deletedAt: new Date(), isActive: false } }
);

// All queries must filter out soft-deleted documents
db.products.find({ deletedAt: { $exists: false } })

// With Mongoose, this can be automated via middleware
```

### 3. Embedded Data is Deleted Automatically

```javascript
// When you delete a document, ALL embedded data is gone — no orphans
await db.collection('orders').deleteOne({ _id: orderId });
// The embedded customer info, items array, shipping address — all deleted
// This is actually BETTER than SQL (no orphan rows in join tables)
```

---

## How does it work?

### Delete Flow (Internal)

```
Client                       MongoDB (WiredTiger)
  │                                │
  │  deleteOne(filter)             │
  │ ──────────────────────────►    │
  │                                │  1. Find document (index or scan)
  │                                │  2. Acquire write lock
  │                                │  3. Mark document as deleted
  │                                │  4. Remove index entries
  │                                │  5. Write to journal (WAL)
  │                                │  6. Space is reusable (not freed to OS)
  │  { deletedCount: 1 }          │
  │ ◄──────────────────────────    │
  │                                │
  Note: Disk space is NOT returned to the OS.
  MongoDB reuses the space for new documents.
  To reclaim: db.collection.compact() or rebuild.
```

---

## Syntax

### deleteOne()

```javascript
// SQL: DELETE FROM products WHERE _id = 42;
db.products.deleteOne({ _id: ObjectId("65a1b2c3d4e5f6a7b8c9d0e1") })

// Result: { acknowledged: true, deletedCount: 1 }
// deletedCount: 0 means no document matched the filter
```

### deleteMany()

```javascript
// SQL: DELETE FROM products WHERE stock = 0 AND isActive = false;
db.products.deleteMany({ stock: 0, isActive: false })

// Result: { acknowledged: true, deletedCount: 47 }

// Delete ALL documents (like TRUNCATE but slower)
db.products.deleteMany({})
// ⚠️ This scans the entire collection. Use drop() instead for full wipe.
```

### findOneAndDelete()

```javascript
// SQL: DELETE FROM products WHERE id = 42 RETURNING *;
const deleted = db.products.findOneAndDelete(
  { _id: ObjectId("...") }
)
// Returns the full document that was deleted
// Useful for: audit logs, undo functionality, moving to archive

// With sort — delete the oldest/cheapest/etc.
const cheapest = db.products.findOneAndDelete(
  { stock: 0 },
  { sort: { price: 1 } }  // Delete the cheapest out-of-stock product
)
```

### drop() — Drop Entire Collection

```javascript
// SQL: DROP TABLE products;
db.products.drop()
// Removes collection, all documents, and all indexes
// Much faster than deleteMany({}) for full collection wipe

// SQL: TRUNCATE TABLE products;
// MongoDB equivalent:
db.products.drop()
db.createCollection('products')
// Or just drop — collection recreates on next insert
```

---

## SQL vs MongoDB — Side-by-Side

```sql
-- SQL: Delete with subquery and cascade
BEGIN;
-- Delete order items first (or rely on CASCADE)
DELETE FROM order_items WHERE order_id IN (
  SELECT id FROM orders WHERE customer_id = 42
);
-- Delete orders
DELETE FROM orders WHERE customer_id = 42;
-- Delete customer
DELETE FROM customers WHERE id = 42;
COMMIT;
-- 3 DELETEs, transaction needed for consistency
```

```javascript
// MongoDB: If data is embedded, one delete handles everything
await db.collection('orders').deleteMany({ 'customer._id': customerId })
// Each order document contained its items and customer info — all gone

// If using references, must delete manually
const session = client.startSession();
session.startTransaction();
try {
  await db.collection('orders').deleteMany({ customerId }, { session });
  await db.collection('reviews').deleteMany({ userId: customerId }, { session });
  await db.collection('customers').deleteOne({ _id: customerId }, { session });
  await session.commitTransaction();
} catch (err) {
  await session.abortTransaction();
  throw err;
} finally {
  session.endSession();
}
```

---

## Node.js Using MongoDB Driver (REQUIRED)

```javascript
const { MongoClient, ObjectId } = require('mongodb');

async function deleteOperations() {
  const client = new MongoClient('mongodb://localhost:27017');
  await client.connect();
  const db = client.db('ecommerce');

  // ──── deleteOne ────
  const result = await db.collection('products').deleteOne({
    _id: new ObjectId('65a1b2c3d4e5f6a7b8c9d0e1')
  });
  console.log('Deleted:', result.deletedCount);

  // ──── deleteMany ────
  const cleaned = await db.collection('products').deleteMany({
    stock: 0,
    isActive: false,
    updatedAt: { $lt: new Date('2023-01-01') }
  });
  console.log('Cleaned up:', cleaned.deletedCount, 'stale products');

  // ──── findOneAndDelete (with archive) ────
  const archived = await db.collection('orders').findOneAndDelete(
    { status: 'cancelled', createdAt: { $lt: new Date('2023-01-01') } },
    { sort: { createdAt: 1 } }
  );
  if (archived) {
    // Move to archive collection
    await db.collection('orders_archive').insertOne({
      ...archived,
      archivedAt: new Date()
    });
    console.log('Archived order:', archived._id);
  }

  // ──── Soft Delete Pattern ────
  await db.collection('customers').updateOne(
    { _id: new ObjectId('...') },
    {
      $set: {
        deletedAt: new Date(),
        deletedBy: 'admin',
        isActive: false
      }
    }
  );

  // ──── Bulk Delete ────
  const bulkResult = await db.collection('logs').bulkWrite([
    { deleteMany: { filter: { level: 'debug', createdAt: { $lt: new Date('2023-06-01') } } } },
    { deleteMany: { filter: { level: 'info', createdAt: { $lt: new Date('2023-01-01') } } } }
  ]);
  console.log('Bulk deleted:', bulkResult.deletedCount);

  await client.close();
}
```

### Express API — Delete Endpoints

```javascript
// DELETE /api/products/:id
app.delete('/api/products/:id', async (req, res) => {
  try {
    const result = await db.collection('products').findOneAndDelete({
      _id: new ObjectId(req.params.id)
    });

    if (!result) {
      return res.status(404).json({ error: 'Product not found' });
    }

    // Log deletion for audit
    await db.collection('audit_log').insertOne({
      action: 'DELETE',
      collection: 'products',
      documentId: result._id,
      document: result,
      deletedBy: req.user?.id,
      deletedAt: new Date()
    });

    res.json({ message: 'Product deleted', product: result });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// DELETE /api/products/:id (soft delete version)
app.delete('/api/products/:id/soft', async (req, res) => {
  const result = await db.collection('products').findOneAndUpdate(
    { _id: new ObjectId(req.params.id), deletedAt: { $exists: false } },
    { $set: { deletedAt: new Date(), isActive: false } },
    { returnDocument: 'after' }
  );

  if (!result) return res.status(404).json({ error: 'Product not found' });
  res.json({ message: 'Product soft-deleted' });
});
```

---

## Real-World Scenario — Data Retention / TTL

### MongoDB TTL Indexes (Auto-Delete)

```javascript
// SQL: Scheduled cron job to DELETE old records
// MongoDB: TTL (Time To Live) index — automatic expiration

// Create TTL index — delete documents 30 days after createdAt
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 2592000 }  // 30 days in seconds
)

// MongoDB automatically deletes expired documents every 60 seconds
// No cron job, no application code, no manual cleanup

// Insert a session — it auto-deletes after 30 days
db.sessions.insertOne({
  userId: ObjectId("..."),
  token: "abc123",
  createdAt: new Date()  // TTL timer starts from this timestamp
})

// Per-document expiry (custom TTL per document)
db.sessions.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 })
// Now expiresAt IS the deletion time
db.sessions.insertOne({
  userId: ObjectId("..."),
  token: "abc123",
  expiresAt: new Date(Date.now() + 3600000)  // Expires in 1 hour
})
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────┐
│  Delete Operation                │ Performance           │
├──────────────────────────────────┼───────────────────────┤
│  deleteOne by _id                │ ⚡ <1ms (index)       │
│  deleteOne by indexed field      │ ⚡ <1ms (index)       │
│  deleteOne by unindexed field    │ 🐌 Full scan          │
│  deleteMany (1000 docs)          │ ~50ms                 │
│  deleteMany (1M docs)            │ ⚠️ Minutes + locks   │
│  drop() entire collection        │ ⚡ <1ms (metadata)    │
│  TTL auto-delete                 │ Background, 60s cycle │
├──────────────────────────────────┴───────────────────────┤
│  Key insight: drop() is instant. deleteMany({}) is slow. │
│  For full collection wipes, ALWAYS use drop().           │
│                                                          │
│  ⚠️ Deleted space is NOT returned to OS. The space is    │
│  reused by new inserts. To truly reclaim disk space,     │
│  run db.collection.compact() (locks the collection).     │
└──────────────────────────────────────────────────────────┘
```

---

## Common Mistakes (SQL Developers Make)

### ❌ Mistake 1: Forgetting Orphaned References

```javascript
// Deleted the customer but orders still reference them
await db.collection('customers').deleteOne({ _id: customerId });
// db.orders.find({ customerId }) still returns results!
// Solution: Always clean up references or use soft deletes
```

### ❌ Mistake 2: Using deleteMany({}) Instead of drop()

```javascript
// ❌ Slow: Scans and deletes every document one by one
await db.collection('logs').deleteMany({});  // Could take hours on large collection

// ✅ Fast: Drops the collection metadata (instant)
await db.collection('logs').drop();
```

### ❌ Mistake 3: Not Using TTL for Temporary Data

```javascript
// ❌ Manual cleanup with scheduled job
cron.schedule('0 * * * *', async () => {
  const cutoff = new Date(Date.now() - 86400000);
  await db.collection('sessions').deleteMany({ createdAt: { $lt: cutoff } });
});

// ✅ Let MongoDB handle it
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 86400 });
// Automatic, no code needed, no cron, no maintenance
```

---

## Practice Exercises

### Exercise 1: Delete Operations

1. Delete a single product by `_id`
2. Delete all products where `stock` is 0 and `isActive` is false
3. Delete the oldest order (by `createdAt`) and return it
4. Implement a soft-delete for customers that sets `deletedAt` and `isActive: false`

### Exercise 2: Cascade Cleanup

Write a function that deletes a customer and cleans up all references:
- Delete all orders for the customer
- Delete all reviews by the customer
- Delete all wishlist items
- Finally delete the customer
- Wrap in a transaction

### Exercise 3: TTL Implementation

1. Create a `sessions` collection with TTL of 24 hours
2. Create a `verification_tokens` collection with per-document TTL
3. Verify that expired documents are automatically removed

---

## Interview Q&A

**Q1: How does MongoDB handle cascading deletes?**
> It doesn't. There are no foreign key constraints, so there are no cascade deletes. The application must manually delete dependent documents. This is why embedded documents are preferred — deleting the parent automatically deletes embedded children. For referenced data, use application-level cleanup or soft deletes.

**Q2: What is a TTL index and when would you use it?**
> A TTL index automatically deletes documents after a specified time has elapsed since a date field value. Used for sessions, cache entries, temporary tokens, audit logs with retention policies. MongoDB's background TTL thread runs every 60 seconds. No SQL equivalent — SQL requires scheduled jobs or partitioned tables.

**Q3: Why is `drop()` faster than `deleteMany({})`?**
> `drop()` removes the collection metadata (instant operation). `deleteMany({})` scans every document, removes it individually, and updates all indexes — O(n) with n being document count. For a 10M document collection, `deleteMany({})` could take minutes; `drop()` takes milliseconds.

**Q4: What happens to disk space after deleting documents?**
> Deleted space is NOT returned to the operating system. MongoDB reuses the space for new inserts. To reclaim disk space, use `db.collection.compact()` (requires lock) or the `--repair` server option (requires downtime). This is similar to SQL's table bloat.

**Q5: How do you implement undo/restore for deleted documents?**
> Options: (1) Soft deletes with `deletedAt` timestamp — easiest to restore. (2) Archive collection — `findOneAndDelete` followed by `insertOne` to an archive collection. (3) Change Streams — capture delete events in real-time and store in a separate collection. (4) Backup and point-in-time recovery.
