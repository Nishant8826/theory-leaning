# Transactions

> 📌 **File:** 15_Transactions.md | **Level:** SQL Expert → MongoDB

---

## What is it?

MongoDB supports multi-document ACID transactions (since v4.0 for replica sets, v4.2 for sharded clusters). However, unlike SQL where transactions are a core design pattern used in virtually every write operation, MongoDB transactions are a **safety net for exceptional cases** — not the default approach.

**SQL mindset:** "Every multi-table write goes in a transaction."
**MongoDB mindset:** "Design documents so single-document writes don't need transactions. Use transactions only when absolutely necessary."

---

## SQL Parallel — Think of it like this

```
SQL:                              MongoDB:
BEGIN / START TRANSACTION       → session.startTransaction()
COMMIT                          → session.commitTransaction()
ROLLBACK                        → session.abortTransaction()
SAVEPOINT                       → ❌ Not supported
Nested transactions             → ❌ Not supported
Implicit transactions           → Single-document ops are always atomic
READ COMMITTED                  → Read concern "local" (default)
REPEATABLE READ                 → Read concern "snapshot"
SERIALIZABLE                    → ❌ Not directly available
```

---

## Why this is different from SQL (CRITICAL)

### 1. Single-Document Operations Are Already Atomic

```javascript
// In SQL, even a simple update might need a transaction
// if it involves multiple tables

// In MongoDB, single-document operations are ACID by default:
db.orders.updateOne(
  { _id: orderId },
  {
    $set: { status: "shipped" },
    $push: { statusHistory: { status: "shipped", date: new Date() } },
    $inc: { "metrics.updates": 1 }
  }
)
// This updates 3 things atomically WITHOUT a transaction
// Because they're all in the SAME document
```

### 2. Transactions Have Performance Costs

```
┌─────────────────────────────────────────────────────────────────┐
│  Transaction Overhead in MongoDB                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Without transaction (single-document):                         │
│  ├── Latency: ~1ms                                              │
│  ├── Lock: Document-level only                                  │
│  └── Retry: Automatic (retryable writes)                       │
│                                                                 │
│  With transaction:                                              │
│  ├── Latency: ~5-20ms (overhead)                               │
│  ├── Lock: All involved documents                               │
│  ├── Retry: Manual retry logic needed                           │
│  ├── Timeout: 60s default (configurable)                       │
│  ├── Memory: State held in memory until commit                 │
│  └── WiredTiger: Checkpoint pressure on long transactions      │
│                                                                 │
│  SQL comparison:                                                │
│  PostgreSQL transaction: ~0.5ms overhead                        │
│  MongoDB transaction: ~5-20ms overhead (10-40x more)           │
│                                                                 │
│  If your application needs transactions for most writes,        │
│  MongoDB is the WRONG database choice.                          │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Design to Avoid Transactions

```javascript
// ❌ SQL approach: Needs transaction for order creation
// BEGIN;
// INSERT INTO orders (...);
// INSERT INTO order_items (...), (...);
// UPDATE products SET stock = stock - 1 WHERE id = ?;
// COMMIT;

// ✅ MongoDB approach: Embed to avoid transaction
// Single insertOne with all order data embedded
db.orders.insertOne({
  customer: { name: "John", email: "john@example.com" },
  items: [
    { product: "Laptop", price: 999, quantity: 1 },
    { product: "Mouse", price: 29, quantity: 2 }
  ],
  total: 1057,
  status: "pending"
})
// ONE write, ONE document, ZERO transactions needed

// Stock update is separate:
db.products.updateOne(
  { _id: productId, stock: { $gte: quantity } },
  { $inc: { stock: -quantity } }
)
// Atomic by itself, no transaction needed for THIS operation
```

---

## Syntax

### Basic Transaction

```javascript
// mongosh
const session = db.getMongo().startSession();
session.startTransaction();

try {
  const orders = session.getDatabase("ecommerce").orders;
  const products = session.getDatabase("ecommerce").products;

  // Create order
  orders.insertOne({
    customerId: ObjectId("..."),
    items: [{ productId: ObjectId("p1"), quantity: 2 }],
    total: 59.98,
    status: "pending"
  }, { session });

  // Decrement stock
  const result = products.updateOne(
    { _id: ObjectId("p1"), stock: { $gte: 2 } },
    { $inc: { stock: -2 } },
    { session }
  );

  if (result.modifiedCount === 0) {
    throw new Error("Insufficient stock");
  }

  session.commitTransaction();
} catch (error) {
  session.abortTransaction();
  throw error;
} finally {
  session.endSession();
}
```

### Node.js Transaction (with Callback API — Recommended)

```javascript
const { MongoClient } = require('mongodb');

async function transferFunds(fromAccountId, toAccountId, amount) {
  const client = new MongoClient('mongodb://localhost:27017/?replicaSet=rs0');
  await client.connect();

  const session = client.startSession();

  try {
    // Callback API — handles retry automatically
    await session.withTransaction(async () => {
      const accounts = client.db('bank').collection('accounts');

      // Debit source account
      const debit = await accounts.updateOne(
        { _id: fromAccountId, balance: { $gte: amount } },
        { $inc: { balance: -amount } },
        { session }
      );

      if (debit.modifiedCount === 0) {
        throw new Error('Insufficient funds');
      }

      // Credit destination account
      await accounts.updateOne(
        { _id: toAccountId },
        { $inc: { balance: amount } },
        { session }
      );

      // Log the transfer
      await client.db('bank').collection('transfers').insertOne({
        from: fromAccountId,
        to: toAccountId,
        amount,
        status: 'completed',
        createdAt: new Date()
      }, { session });
    });

    console.log('Transfer successful');
  } catch (error) {
    console.error('Transfer failed:', error.message);
  } finally {
    await session.endSession();
    await client.close();
  }
}
```

### Node.js Transaction (Core API — Manual Retry)

```javascript
async function runTransactionWithRetry(session, txnFunc) {
  while (true) {
    try {
      await txnFunc(session);
      break;
    } catch (error) {
      if (error.hasErrorLabel('TransientTransactionError')) {
        console.log('Transient error, retrying...');
        continue;
      }
      throw error;
    }
  }
}

async function commitWithRetry(session) {
  while (true) {
    try {
      await session.commitTransaction();
      break;
    } catch (error) {
      if (error.hasErrorLabel('UnknownTransactionCommitResult')) {
        console.log('Commit error, retrying...');
        continue;
      }
      throw error;
    }
  }
}

async function placeOrder(client, orderData) {
  const session = client.startSession();

  try {
    session.startTransaction({
      readConcern: { level: 'snapshot' },
      writeConcern: { w: 'majority' },
      readPreference: 'primary'
    });

    const db = client.db('ecommerce');

    // All operations pass { session }
    await db.collection('orders').insertOne(orderData, { session });

    for (const item of orderData.items) {
      const result = await db.collection('products').updateOne(
        { _id: item.productId, stock: { $gte: item.quantity } },
        { $inc: { stock: -item.quantity } },
        { session }
      );

      if (result.modifiedCount === 0) {
        throw new Error(`Insufficient stock for ${item.name}`);
      }
    }

    await commitWithRetry(session);
  } catch (error) {
    await session.abortTransaction();
    throw error;
  } finally {
    await session.endSession();
  }
}
```

---

## When Transactions ARE Needed

### 1. Financial Operations

```javascript
// Money transfer — MUST be atomic across documents
await session.withTransaction(async () => {
  await accounts.updateOne({ _id: from }, { $inc: { balance: -amount } }, { session });
  await accounts.updateOne({ _id: to }, { $inc: { balance: amount } }, { session });
  await transactions.insertOne({ from, to, amount, date: new Date() }, { session });
});
```

### 2. Inventory Reservation (Cross-Document)

```javascript
// Reserve inventory + create order atomically
await session.withTransaction(async () => {
  // Check and decrement all product stocks
  for (const item of items) {
    const result = await products.updateOne(
      { _id: item.productId, stock: { $gte: item.quantity } },
      { $inc: { stock: -item.quantity } },
      { session }
    );
    if (result.modifiedCount === 0) throw new Error('Stock unavailable');
  }
  // Create order only if all stock decrements succeeded
  await orders.insertOne(orderData, { session });
});
```

### 3. User Registration (Unique Constraints Across Collections)

```javascript
// Create user + profile + settings atomically
await session.withTransaction(async () => {
  const user = await users.insertOne({ email, password: hash }, { session });
  await profiles.insertOne({ userId: user.insertedId, name, avatar: null }, { session });
  await settings.insertOne({ userId: user.insertedId, theme: 'light' }, { session });
});
```

---

## SQL vs MongoDB Transaction Comparison

```sql
-- SQL: Natural, cheap, ubiquitous
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
  INSERT INTO transfers (from_id, to_id, amount) VALUES (1, 2, 100);
COMMIT;
-- ~1ms overhead. Used in every write path.
```

```javascript
// MongoDB: Works but has overhead
const session = client.startSession();
await session.withTransaction(async () => {
  await accounts.updateOne({ _id: 1 }, { $inc: { balance: -100 } }, { session });
  await accounts.updateOne({ _id: 2 }, { $inc: { balance: 100 } }, { session });
  await transfers.insertOne({ from: 1, to: 2, amount: 100 }, { session });
});
// ~10-20ms overhead. Use sparingly.
```

---

## Transaction Limitations

```
┌──────────────────────────────────────────────────────────────────┐
│  Limitation                              │ Impact               │
├──────────────────────────────────────────┼──────────────────────┤
│  Requires replica set                    │ No transactions on   │
│                                          │ standalone mongod    │
│  60-second timeout (default)             │ Long transactions    │
│                                          │ are aborted          │
│  16MB oplog entry limit per transaction  │ Can't modify too    │
│                                          │ many documents       │
│  No savepoints                           │ All or nothing       │
│  No nested transactions                  │ Flat only            │
│  Cannot create/drop collections          │ DDL not in txns     │
│  Performance degradation under contention│ If many transactions │
│                                          │ touch same documents│
│  No cross-database on sharded clusters   │ Shard-aware only     │
│  Snapshot isolation level only            │ No READ UNCOMMITTED  │
└──────────────────────────────────────────┴──────────────────────┘
```

---

## Real-World Scenario — E-Commerce Checkout

```javascript
// Express API: Place order with transaction
app.post('/api/checkout', async (req, res) => {
  const { customerId, items, shippingAddress, paymentMethod } = req.body;
  const session = client.startSession();

  try {
    let orderId;

    await session.withTransaction(async () => {
      const db = client.db('ecommerce');

      // 1. Validate and decrement stock
      for (const item of items) {
        const result = await db.collection('products').findOneAndUpdate(
          { _id: new ObjectId(item.productId), stock: { $gte: item.quantity } },
          { $inc: { stock: -item.quantity } },
          { session, returnDocument: 'after' }
        );

        if (!result) {
          throw new Error(`Product ${item.productId} is out of stock`);
        }

        // Capture current price snapshot
        item.name = result.name;
        item.price = result.price;
        item.subtotal = parseFloat(result.price.toString()) * item.quantity;
      }

      // 2. Calculate total
      const total = items.reduce((sum, i) => sum + i.subtotal, 0);

      // 3. Create order
      const customer = await db.collection('customers').findOne(
        { _id: new ObjectId(customerId) },
        { projection: { name: 1, email: 1 }, session }
      );

      const order = await db.collection('orders').insertOne({
        customerId: new ObjectId(customerId),
        customer: { name: customer.name, email: customer.email },
        items,
        shippingAddress,
        payment: { method: paymentMethod },
        total,
        status: 'pending',
        createdAt: new Date()
      }, { session });

      orderId = order.insertedId;

      // 4. Update customer stats
      await db.collection('customers').updateOne(
        { _id: new ObjectId(customerId) },
        {
          $inc: { 'orderStats.totalOrders': 1, 'orderStats.totalSpent': total },
          $set: { 'orderStats.lastOrderDate': new Date() }
        },
        { session }
      );
    });

    res.status(201).json({ orderId, message: 'Order placed successfully' });
  } catch (error) {
    res.status(400).json({ error: error.message });
  } finally {
    await session.endSession();
  }
});
```

---

## Performance Insight

```
┌──────────────────────────────────────────────────────────────────┐
│  Transaction Best Practices                                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Keep transactions SHORT — under 1 second                    │
│  2. Minimize the number of documents modified                    │
│  3. Avoid long-running queries inside transactions              │
│  4. Don't fetch data you don't need (use projection)            │
│  5. Retry transient errors automatically                         │
│  6. Use the callback API (withTransaction) for auto-retry       │
│  7. Set appropriate write/read concerns                          │
│  8. Index all fields used in transaction queries                 │
│  9. Avoid transactions on hot documents (high contention)       │
│ 10. Design documents to minimize transaction usage               │
│                                                                  │
│  If > 10% of your writes use transactions,                      │
│  reconsider if MongoDB is the right database.                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes

### ❌ Using Transactions for Everything

```javascript
// ❌ Transaction for single-document update (unnecessary)
const session = client.startSession();
await session.withTransaction(async () => {
  await products.updateOne({ _id: id }, { $set: { price: 99 } }, { session });
});
// Single-document ops are already atomic!

// ✅ Just update directly
await products.updateOne({ _id: id }, { $set: { price: 99 } });
```

### ❌ Forgetting Replica Set Requirement

```javascript
// Transactions require a replica set
// Standalone mongod → TransactionError

// For local development, use a single-node replica set:
// mongod --replSet rs0
// then: rs.initiate()
```

---

## Practice Exercises

### Exercise 1: Convert a SQL Transaction

Convert this SQL transaction to MongoDB:
```sql
BEGIN;
INSERT INTO orders (customer_id, total) VALUES (1, 99.99);
UPDATE customers SET total_orders = total_orders + 1 WHERE id = 1;
UPDATE products SET stock = stock - 1 WHERE id = 42;
INSERT INTO audit_log (action, entity_id) VALUES ('order_created', LASTVAL());
COMMIT;
```

### Exercise 2: Design Without Transactions

Redesign the above scenario so that it can work WITHOUT a transaction by using embedded documents.

### Exercise 3: Retry Logic

Implement a `withRetry` wrapper that handles `TransientTransactionError` and `UnknownTransactionCommitResult` errors.

---

## Interview Q&A

**Q1: Does MongoDB support ACID transactions?**
> Yes, since v4.0 (replica sets) and v4.2 (sharded clusters). They provide snapshot isolation across multiple documents and collections. However, they have higher overhead than SQL transactions (10-40x) and should be used sparingly. Single-document operations are always ACID without transactions.

**Q2: Why should you minimize transaction usage in MongoDB?**
> MongoDB transactions have higher overhead (locking, snapshot management, WiredTiger checkpoint pressure), 60s timeout, 16MB oplog limit, and only work on replica sets. MongoDB's document model is designed to avoid transactions by embedding related data — if you need transactions frequently, your schema needs redesign or SQL may be a better fit.

**Q3: What's the difference between the callback API and core API for transactions?**
> Callback API (`session.withTransaction()`) automatically retries on transient errors and unknown commit results. Core API requires manual retry logic with `startTransaction()` / `commitTransaction()` / `abortTransaction()`. Always prefer the callback API for production code.

**Q4: What read/write concerns should you use for transactions?**
> `readConcern: "snapshot"` for consistent reads. `writeConcern: { w: "majority" }` for durable writes. `readPreference: "primary"` (required). These ensure data consistency within the transaction.

**Q5: Can MongoDB transactions span multiple databases?**
> Yes, on replica sets (same `mongod`). On sharded clusters, transactions can span multiple shards within the same database. Cross-database transactions on sharded clusters have limitations. This is more restrictive than SQL's cross-database transactions.
