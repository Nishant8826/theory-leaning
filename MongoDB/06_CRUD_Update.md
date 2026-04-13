# CRUD — Update

> 📌 **File:** 06_CRUD_Update.md | **Level:** SQL Expert → MongoDB

---

## What is it?

Update operations modify existing documents in collections. MongoDB provides granular update operators (`$set`, `$inc`, `$push`, etc.) that modify specific fields **without rewriting the entire document** — something SQL's `UPDATE SET` always does conceptually. This is MongoDB's hidden superpower for high-concurrency workloads.

---

## SQL Parallel — Think of it like this

```
SQL:                                          MongoDB:
UPDATE t SET x = 1 WHERE id = 5             → db.t.updateOne({ _id: 5 }, { $set: { x: 1 } })
UPDATE t SET x = x + 1 WHERE id = 5        → db.t.updateOne({ _id: 5 }, { $inc: { x: 1 } })
UPDATE t SET x = 1                          → db.t.updateMany({}, { $set: { x: 1 } })
UPDATE t SET x = 1 WHERE y > 10            → db.t.updateMany({ y: { $gt: 10 } }, { $set: { x: 1 } })
REPLACE INTO t VALUES (...)                 → db.t.replaceOne({ _id: 5 }, { ... })
UPDATE ... RETURNING *                      → db.t.findOneAndUpdate(filter, update, { returnDocument: 'after' })
INSERT ... ON DUPLICATE KEY UPDATE          → db.t.updateOne(filter, update, { upsert: true })
```

---

## Why this is different from SQL (CRITICAL)

### 1. Atomic Field-Level Updates

```sql
-- SQL: Even changing one column rewrites the entire row
UPDATE products SET stock = stock - 1 WHERE id = 42;
-- Internally: Read row → modify → write entire row
```

```javascript
// MongoDB: $inc modifies ONLY the stock field in-place
db.products.updateOne(
  { _id: ObjectId("...") },
  { $inc: { stock: -1 } }
)
// Internally: Navigate to field → modify in-place → done
// No read-modify-write cycle. Atomic at the document level.
```

### 2. Update Operators (No SQL Equivalent)

```
┌──────────────────────────────────────────────────────────────────┐
│  MongoDB Update Operators — Things SQL Can't Do Natively        │
├──────────────────────────────────────────────────────────────────┤
│  $set        → Set field value (closest to SQL UPDATE SET)      │
│  $unset      → Remove a field entirely (no ALTER TABLE needed)  │
│  $inc        → Atomic increment/decrement                       │
│  $mul        → Atomic multiply                                  │
│  $min / $max → Set to min/max of current and given value        │
│  $push       → Append to array                                  │
│  $pull       → Remove from array by value                       │
│  $addToSet   → Append to array only if not already present      │
│  $pop        → Remove first/last element of array               │
│  $rename     → Rename a field (no ALTER TABLE RENAME COLUMN)    │
│  $currentDate→ Set to current date                              │
└──────────────────────────────────────────────────────────────────┘
```

### 3. Updating Nested Fields and Arrays

```javascript
// SQL: Updating a value in a JSON column or related table
// UPDATE products SET specs = jsonb_set(specs, '{ram}', '"32GB"') WHERE id = 42;

// MongoDB: Dot notation — natural and readable
db.products.updateOne(
  { _id: ObjectId("...") },
  { $set: { "specs.ram": "32GB" } }
)

// Update specific array element by index
db.products.updateOne(
  { _id: ObjectId("...") },
  { $set: { "tags.0": "laptop" } }  // Update first tag
)

// Update array element matching condition (positional $ operator)
db.orders.updateOne(
  { _id: ObjectId("..."), "items.productId": ObjectId("...") },
  { $set: { "items.$.quantity": 5 } }  // Update matched item's quantity
)
```

---

## How does it work?

### Update Flow (Internal)

```
Client                         MongoDB (WiredTiger)
  │                                  │
  │  updateOne(filter, update)       │
  │ ────────────────────────────►    │
  │                                  │  1. Find document (using index or scan)
  │                                  │  2. Acquire write lock on document
  │                                  │  3. Apply update operators in-place
  │                                  │  4. Update affected indexes
  │                                  │  5. Write to journal (WAL)
  │                                  │  6. Release lock
  │  { matchedCount: 1,             │
  │    modifiedCount: 1 }           │
  │ ◄────────────────────────────    │
```

**Key insight:** MongoDB applies all update operators **atomically** within a single document. There's no intermediate state visible to other operations. This is equivalent to row-level locking in SQL.

---

## Syntax

### updateOne() — Update First Matching Document

```javascript
// SQL: UPDATE products SET price = 899.99 WHERE name = 'Laptop';

db.products.updateOne(
  { name: "Laptop" },                    // Filter (WHERE clause)
  { $set: { price: NumberDecimal("899.99") } }  // Update
)

// Result:
{ acknowledged: true, matchedCount: 1, modifiedCount: 1 }
// matchedCount = found the document
// modifiedCount = actually changed (0 if value was already 899.99)
```

### updateMany() — Update All Matching Documents

```javascript
// SQL: UPDATE products SET stock = 0 WHERE category_name = 'Discontinued';

db.products.updateMany(
  { "category.name": "Discontinued" },
  { $set: { stock: 0, isActive: false, updatedAt: new Date() } }
)

// Result:
{ acknowledged: true, matchedCount: 15, modifiedCount: 15 }
```

### replaceOne() — Replace Entire Document

```javascript
// SQL: DELETE then INSERT (conceptually)
// ⚠️ Replaces the ENTIRE document (except _id)

db.products.replaceOne(
  { _id: ObjectId("...") },
  {
    name: "New Laptop",
    price: NumberDecimal("1099.99"),
    brand: "Dell",
    // All other fields are GONE if not included here
  }
)
// Use updateOne + $set instead in most cases
```

### findOneAndUpdate() — Update and Return Document

```javascript
// SQL: UPDATE products SET stock = stock - 1 WHERE id = 42 RETURNING *;

const result = db.products.findOneAndUpdate(
  { _id: ObjectId("..."), stock: { $gt: 0 } },
  { $inc: { stock: -1 }, $set: { updatedAt: new Date() } },
  { returnDocument: "after" }  // "before" = original, "after" = modified
)
// Returns the full document (before or after modification)
// Atomic — no race condition between find and update
```

---

## Update Operators Deep Dive

### $set — Set Field Values

```javascript
// Set single field
db.products.updateOne({ _id: id }, { $set: { price: 899 } })

// Set multiple fields
db.products.updateOne({ _id: id }, {
  $set: {
    price: 899,
    brand: "Dell",
    "specs.ram": "32GB",            // Nested field
    updatedAt: new Date()
  }
})

// Set creates the field if it doesn't exist
db.products.updateOne({ _id: id }, { $set: { discount: 10 } })
// Adds "discount" field to document — no ALTER TABLE needed
```

### $unset — Remove Fields

```javascript
// SQL: ALTER TABLE products DROP COLUMN discount;
// MongoDB: Per-document field removal

db.products.updateOne({ _id: id }, { $unset: { discount: "" } })
// Removes "discount" field from this specific document

// Remove from all documents
db.products.updateMany({}, { $unset: { temporaryField: "" } })
```

### $inc — Atomic Increment/Decrement

```javascript
// SQL: UPDATE products SET stock = stock - 1, sold = sold + 1 WHERE id = 42;

db.products.updateOne(
  { _id: ObjectId("...") },
  { $inc: { stock: -1, sold: 1, "stats.views": 1 } }
)
// Atomic — safe for concurrent access. No read-modify-write needed.
```

### $push — Append to Array

```javascript
// SQL: INSERT INTO product_tags (product_id, tag) VALUES (42, 'sale');

db.products.updateOne(
  { _id: ObjectId("...") },
  { $push: { tags: "sale" } }
)

// Push with modifiers
db.products.updateOne(
  { _id: ObjectId("...") },
  {
    $push: {
      reviews: {
        $each: [                     // Add multiple items
          { user: "John", rating: 5, text: "Amazing!" },
          { user: "Jane", rating: 4, text: "Good value" }
        ],
        $sort: { rating: -1 },       // Sort array after push
        $slice: -50                   // Keep only last 50 reviews
      }
    }
  }
)
// This single operation: adds reviews, sorts them, and caps at 50
// SQL would need: INSERT + subquery/trigger for sorting + DELETE for capping
```

### $pull — Remove from Array

```javascript
// SQL: DELETE FROM product_tags WHERE product_id = 42 AND tag = 'sale';

db.products.updateOne(
  { _id: ObjectId("...") },
  { $pull: { tags: "sale" } }
)

// Pull with condition (remove all reviews with rating < 3)
db.products.updateOne(
  { _id: ObjectId("...") },
  { $pull: { reviews: { rating: { $lt: 3 } } } }
)
```

### $addToSet — Add to Array Only if Unique

```javascript
// SQL: INSERT INTO product_tags (product_id, tag) VALUES (42, 'sale')
//      ON CONFLICT DO NOTHING;

db.products.updateOne(
  { _id: ObjectId("...") },
  { $addToSet: { tags: "sale" } }
)
// If "sale" already in tags → no change
// If not → adds it

// Add multiple unique values
db.products.updateOne(
  { _id: ObjectId("...") },
  { $addToSet: { tags: { $each: ["sale", "featured", "new"] } } }
)
```

### Positional Operators ($ and $[])

```javascript
// Update a specific array element that matches a condition
// "Update the price of the item whose productId matches"

db.orders.updateOne(
  { _id: ObjectId("..."), "items.productId": ObjectId("prod123") },
  { $set: { "items.$.price": 29.99 } }
  //                 ^ positional operator — refers to matched array element
)

// Update ALL array elements
db.orders.updateMany(
  {},
  { $inc: { "items.$[].price": 5 } }
  //              ^^ all positional — applies to every element
)

// Update array elements matching a condition (arrayFilters)
db.orders.updateMany(
  {},
  { $set: { "items.$[elem].discounted": true } },
  { arrayFilters: [{ "elem.price": { $lt: 50 } }] }
  // Updates only items where price < 50
)
```

### $rename — Rename Fields

```javascript
// SQL: ALTER TABLE products RENAME COLUMN old_name TO new_name;

db.products.updateMany(
  {},
  { $rename: { "category_name": "category.name" } }
)
// Renames field "category_name" to nested "category.name"
// Individual documents, no DDL, no migration needed
```

---

## SQL vs MongoDB — Side-by-Side

```sql
-- SQL: Multiple updates in a transaction
BEGIN;
UPDATE products SET price = 899.99, updated_at = NOW() WHERE id = 42;
UPDATE products SET stock = stock - 1 WHERE id = 42;
UPDATE order_items SET unit_price = 899.99 WHERE product_id = 42 AND order_id = 100;
COMMIT;
```

```javascript
// MongoDB: Single atomic update (within one document)
db.products.updateOne(
  { _id: ObjectId("...") },
  {
    $set: { price: NumberDecimal("899.99"), updatedAt: new Date() },
    $inc: { stock: -1 }
  }
)
// For cross-document updates, you need a transaction (see file 15)
```

---

## Node.js Using MongoDB Driver (REQUIRED)

```javascript
const { MongoClient, ObjectId, Decimal128 } = require('mongodb');

async function updateOperations() {
  const client = new MongoClient('mongodb://localhost:27017');
  await client.connect();
  const db = client.db('ecommerce');

  // ──── Basic updateOne ────
  const updateResult = await db.collection('products').updateOne(
    { name: 'Laptop' },
    {
      $set: { price: Decimal128.fromString('899.99'), updatedAt: new Date() },
      $inc: { 'stats.views': 1 }
    }
  );
  console.log('Matched:', updateResult.matchedCount, 'Modified:', updateResult.modifiedCount);

  // ──── updateMany ────
  const bulkUpdate = await db.collection('products').updateMany(
    { stock: { $lte: 5 } },
    { $set: { lowStock: true, updatedAt: new Date() } }
  );
  console.log('Low stock flagged:', bulkUpdate.modifiedCount);

  // ──── findOneAndUpdate (atomic get-and-modify) ────
  const decremented = await db.collection('products').findOneAndUpdate(
    { _id: new ObjectId('...'), stock: { $gt: 0 } },
    {
      $inc: { stock: -1 },
      $set: { updatedAt: new Date() }
    },
    { returnDocument: 'after' }
  );
  if (decremented) {
    console.log('New stock:', decremented.stock);
  } else {
    console.log('Product not found or out of stock');
  }

  // ──── Push to array ────
  await db.collection('products').updateOne(
    { _id: new ObjectId('...') },
    {
      $push: {
        reviews: {
          $each: [{
            userId: new ObjectId('...'),
            userName: 'John',
            rating: 5,
            text: 'Excellent product!',
            createdAt: new Date()
          }],
          $slice: -100     // Keep last 100 reviews
        }
      },
      $inc: { 'ratings.count': 1 }
    }
  );

  // ──── Upsert ────
  const upserted = await db.collection('products').updateOne(
    { sku: 'WIDGET-X100' },
    {
      $set: { name: 'Widget X100', price: Decimal128.fromString('24.99') },
      $setOnInsert: { stock: 100, createdAt: new Date() }
    },
    { upsert: true }
  );

  // ──── Bulk Write (mixed operations) ────
  const bulk = await db.collection('products').bulkWrite([
    { updateOne: { filter: { sku: 'A' }, update: { $inc: { stock: -1 } } } },
    { updateOne: { filter: { sku: 'B' }, update: { $inc: { stock: -2 } } } },
    { updateMany: { filter: { stock: 0 }, update: { $set: { isActive: false } } } }
  ], { ordered: false });

  await client.close();
}
```

### Express API — Update Product

```javascript
// PATCH /api/products/:id
app.patch('/api/products/:id', async (req, res) => {
  try {
    const allowedFields = ['name', 'price', 'brand', 'stock', 'specs', 'tags'];
    const updates = {};

    for (const [key, value] of Object.entries(req.body)) {
      if (allowedFields.includes(key)) {
        updates[key] = key === 'price' ? Decimal128.fromString(String(value)) : value;
      }
    }

    if (Object.keys(updates).length === 0) {
      return res.status(400).json({ error: 'No valid fields to update' });
    }

    updates.updatedAt = new Date();

    const result = await db.collection('products').findOneAndUpdate(
      { _id: new ObjectId(req.params.id) },
      { $set: updates },
      { returnDocument: 'after' }
    );

    if (!result) return res.status(404).json({ error: 'Product not found' });
    res.json(result);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});
```

---

## Real-World Scenario — Inventory Management

### SQL Approach (Race Condition Risk)

```sql
-- Thread 1 & Thread 2 both trying to buy the last item
-- Without proper locking:
SELECT stock FROM products WHERE id = 42;  -- Both see stock = 1
UPDATE products SET stock = stock - 1 WHERE id = 42;  -- Both execute
-- stock = -1 (oversold!)

-- Fix: Use SELECT ... FOR UPDATE
BEGIN;
SELECT stock FROM products WHERE id = 42 FOR UPDATE;
-- If stock > 0:
UPDATE products SET stock = stock - 1 WHERE id = 42;
COMMIT;
```

### MongoDB Approach (Atomic by Design)

```javascript
// findOneAndUpdate is atomic — no race condition possible
const result = await db.collection('products').findOneAndUpdate(
  {
    _id: new ObjectId(productId),
    stock: { $gte: quantity }    // Only if enough stock
  },
  {
    $inc: { stock: -quantity },
    $set: { updatedAt: new Date() }
  },
  { returnDocument: 'after' }
);

if (!result) {
  // Either product not found OR insufficient stock
  throw new Error('Product unavailable or insufficient stock');
}
// No race condition — filter + update are atomic
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────┐
│  Update Operation                │ Performance Impact        │
├──────────────────────────────────┼───────────────────────────┤
│  $set on indexed field           │ Index update required     │
│  $set on non-indexed field       │ Fast — no index update    │
│  $inc (counter)                  │ Very fast — in-place      │
│  $push to small array            │ Fast                      │
│  $push to large array (10K+)    │ ⚠️ Slow — document growth │
│  $pull from large array          │ ⚠️ Slow — scan + shift   │
│  updateMany on 1M docs           │ ⚠️ Slow — no bulk opt.    │
│  replaceOne                      │ Rewrites full document    │
├──────────────────────────────────┴───────────────────────────┤
│  Key rule: $inc and $set on non-indexed, non-array fields   │
│  are the fastest operations in MongoDB.                     │
│                                                             │
│  ⚠️ Document growth: If an update makes a document larger   │
│  than its allocated space, WiredTiger moves it to a new     │
│  location and updates all indexes. Avoid unbounded growth.  │
└─────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes (SQL Developers Make)

### ❌ Mistake 1: Replacing Instead of Updating

```javascript
// ❌ WRONG — overwrites entire document (loses all other fields!)
db.products.updateOne(
  { _id: ObjectId("...") },
  { name: "New Name", price: 999 }  // No $set!
)
// This is actually a replaceOne disguised as updateOne
// In modern MongoDB, this throws an error. Always use $set.

// ✅ RIGHT
db.products.updateOne(
  { _id: ObjectId("...") },
  { $set: { name: "New Name", price: 999 } }
)
```

### ❌ Mistake 2: Using Read-Modify-Write Instead of Atomic Operators

```javascript
// ❌ WRONG — race condition!
const product = await products.findOne({ _id: id });
product.stock -= 1;
await products.updateOne({ _id: id }, { $set: { stock: product.stock } });

// ✅ RIGHT — atomic
await products.updateOne({ _id: id }, { $inc: { stock: -1 } });
```

### ❌ Mistake 3: Unbounded Array Growth

```javascript
// ❌ Reviews array grows forever
db.products.updateOne({ _id: id }, { $push: { reviews: newReview } })

// ✅ Cap the array
db.products.updateOne({ _id: id }, {
  $push: { reviews: { $each: [newReview], $slice: -100 } }
})
// Or move reviews to a separate collection when they reach a threshold
```

---

## Practice Exercises

### Exercise 1: Update Operations

Write MongoDB update commands for:
1. Change a product's price to $799.99
2. Increment view count by 1 and decrement stock by 2 atomically
3. Add "featured" to tags array (only if not already present)
4. Remove all tags matching "clearance"
5. Rename field "category_name" to "categoryName" across all documents

### Exercise 2: Array Operations

Given an order document with an items array:
1. Update the quantity of a specific item (by productId)
2. Add a new item to the order and update the total
3. Remove an item from the order and recalculate total

### Exercise 3: Concurrent Stock Management

Build a `/api/products/:id/purchase` endpoint that:
- Atomically decrements stock
- Returns the updated product
- Returns 409 Conflict if insufficient stock
- Uses `findOneAndUpdate` with stock check in filter

---

## Interview Q&A

**Q1: Why is `$inc` preferred over read-modify-write for counters?**
> `$inc` is atomic at the document level — no lock or transaction needed. Read-modify-write creates a race condition where two concurrent requests read the same value, both decrement, and write the same result (losing one update). `$inc` guarantees correct behavior under concurrency.

**Q2: What's the difference between `updateOne` and `findOneAndUpdate`?**
> `updateOne` returns `{ matchedCount, modifiedCount }` — it tells you IF the update happened but not the document itself. `findOneAndUpdate` returns the actual document (before or after modification). Use it when you need the document (e.g., to return it in an API response) or for atomic read-and-modify operations.

**Q3: How do you update a specific element in an array?**
> Use the positional `$` operator: `{ "items.$.field": value }` matches the first array element that matches the query filter. For all elements, use `$[]`. For filtered elements, use `$[identifier]` with `arrayFilters`.

**Q4: What happens if you `$push` to a non-existent field?**
> MongoDB creates the field as an array and pushes the value. Same as `$set` creating a field. No `ALTER TABLE` needed.

**Q5: How does MongoDB handle concurrent updates to the same document?**
> MongoDB uses document-level locking (WiredTiger storage engine). Concurrent updates to the SAME document are serialized. Concurrent updates to DIFFERENT documents execute in parallel. This is more granular than SQL's row-level locking because the "row" (document) contains related data that would be across multiple tables in SQL.
