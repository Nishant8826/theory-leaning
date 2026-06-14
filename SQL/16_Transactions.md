# Transactions

> 📌 **File:** `16_Transactions.md` | **Level:** Beginner → MERN Developer

---

## What is it?

A **transaction** is a group of SQL operations that either ALL succeed or ALL fail together. It's an "all-or-nothing" guarantee. If any operation fails, everything is rolled back to the original state — as if nothing happened.

Classic example: Transferring money. Debit from Account A AND credit to Account B must both succeed. If the credit fails after the debit, you'd lose money! Transactions prevent this.

---

## MERN Parallel — You Already Know This!

| MongoDB/Mongoose (You Know)                       | MySQL Transaction (You'll Learn)                |
|---------------------------------------------------|-------------------------------------------------|
| `const session = await mongoose.startSession()`   | `const conn = await db.getConnection()`       |
| `session.startTransaction()`                      | `await conn.beginTransaction()`                 |
| `await Model.create([doc], { session })`          | `await conn.query('INSERT...', params)`         |
| `await session.commitTransaction()`               | `await conn.commit()`                           |
| `await session.abortTransaction()`                | `await conn.rollback()`                         |
| `session.endSession()`                            | `conn.release()`                                |

### Key Difference
MongoDB only supports multi-document transactions since v4.0, and they're less common because embedded documents handle most cases. In MySQL, transactions are fundamental — you use them for **any** operation that involves multiple queries.

---

## Why does it matter?

- **Data consistency**: Without transactions, partial failures corrupt your data
- **Financial operations**: Orders, payments, refunds MUST be atomic
- **E-commerce**: Deducting stock AND creating an order must happen together
- **ACID compliance**: MySQL guarantees Atomicity, Consistency, Isolation, Durability
- **Production requirement**: Every multi-step operation needs a transaction

---

## How does it work?

### ACID Properties

```
┌──────────────────────────────────────────────────────────────┐
│                     ACID PROPERTIES                          │
├──────────────┬───────────────────────────────────────────────┤
│ Atomicity    │ All operations succeed or all fail together   │
│              │ "All or nothing"                              │
├──────────────┼───────────────────────────────────────────────┤
│ Consistency  │ Database moves from one valid state to another│
│              │ Constraints are never violated                │
├──────────────┼───────────────────────────────────────────────┤
│ Isolation    │ Concurrent transactions don't interfere       │
│              │ Each transaction sees a consistent snapshot   │
├──────────────┼───────────────────────────────────────────────┤
│ Durability   │ Once committed, data survives server crashes  │
│              │ Written to disk, not just memory              │
└──────────────┴───────────────────────────────────────────────┘
```

Let's dive deeper into what these four pillars mean in practice, especially under the hood in MySQL:

---

#### 1. Atomicity ("All-or-Nothing Execution")
* **What it means:** A transaction is treated as a single, indivisible unit of work. It is physically impossible for the database to apply only half of the queries in a transaction. Either 100% of the queries are permanently applied, or 0% are.
* **Under-the-Hood Mechanism:**
  * MySQL's InnoDB storage engine uses a structure called the **Undo Log**.
  * Before modifying any data, InnoDB writes the *reverse action* to the Undo Log. For instance, if you update a balance from `$100` to `$80`, InnoDB logs: *"If rollback happens, update it back to `$100`"*. If you insert a row, it logs: *"If rollback happens, delete this row by ID"*.
  * If a query fails or you execute `ROLLBACK`, MySQL reads the Undo Log backward to revert all modifications, returning the database to its exact pre-transaction state.
* **Real-World E-Commerce Example:** Creating an order and deducting stock. If stock is deducted but the payment fails, the stock deduction is rolled back.
* **MERN Parallel:** Similar to MongoDB's multi-document transactions using Sessions. If you call `session.abortTransaction()`, the operations staged in the oplog are discarded.

#### 2. Consistency ("Preserving Database Integrity Rules")
* **What it means:** A transaction must transition the database from one valid state to another, strictly adhering to all defined rules, schemas, constraints, and foreign key relations. If any rule is violated, the transaction is rejected.
* **Under-the-Hood Mechanism:**
  * MySQL enforces integrity constraints at the database engine level (e.g., `NOT NULL`, `UNIQUE`, `CHECK` constraints, and `FOREIGN KEY` referential integrity).
  * If a transaction tries to insert a duplicate email on a `UNIQUE` column, or references a non-existent `customer_id` on a foreign key, MySQL instantly throws an error and marks the transaction as failed, forcing a rollback.
* **Real-World E-Commerce Examples:**
  * **Stock Check:** If your `products` table has a `CHECK (stock >= 0)` constraint, any transaction that attempts to buy more items than available in stock will immediately fail.
  * **Wallet Balance Check:** If your `users` table has a `CHECK (wallet_balance >= 0)` constraint, you can safely deduct funds during checkout. If a user tries to place an order costing `$500` but only has `$300` in their wallet, the update query (`UPDATE users SET wallet_balance = wallet_balance - 500 WHERE id = 1`) violates the consistency constraint. The database immediately aborts the query, forcing a rollback of any prior stock deductions or order records.
    ```sql
    -- Enforced via Check Constraint:
    ALTER TABLE users ADD CONSTRAINT chk_positive_wallet CHECK (wallet_balance >= 0);
    ```
* **MERN Parallel:** In MongoDB, schema validation is typically handled by Mongoose at the application level. If a user bypasses Mongoose and writes directly to MongoDB, invalid data can easily be saved. In MySQL, the database engine itself guarantees consistency, making it impossible to bypass.

#### 3. Isolation ("Managing Concurrent Operations")
* **What it means:** Multiple transactions running concurrently must not interfere with each other. If User A and User B are executing transactions at the exact same time, the system guarantees that their executions are isolated.
* **Under-the-Hood Mechanism:**
  * Uses **MVCC (Multi-Version Concurrency Control)** and the **InnoDB Lock Manager**.
  * **MVCC:** To prevent read operations from blocking write operations (and vice versa), InnoDB maintains multiple versions of a row. When Transaction A updates a row, Transaction B can still read the previous state of the row from the **Undo Log** without waiting!
  * **Locks:** InnoDB uses row-level locking (`SELECT ... FOR UPDATE` locks the selected rows; shared locks block updates, exclusive locks block both reads and updates).
  * **Isolation Levels:** You can configure how isolated queries are (e.g., default `REPEATABLE READ` prevents dirty reads and non-repeatable reads).
* **Real-World E-Commerce Example:** Two users click "Buy Now" on the last remaining concert ticket at the exact same millisecond. Isolation (via row locks) serializes their access, ensuring the first user completes their purchase and the second user gets a "Sold Out" message, rather than both being charged.
* **MERN Parallel:** MongoDB uses document-level locks. However, managing complex isolation scenarios (like avoiding phantom reads across multiple collections) in MongoDB requires deliberate setup, whereas MySQL has built-in transaction isolation levels.

#### 4. Durability ("Surviving Crashes")
* **What it means:** Once a transaction is committed, its changes are permanently written to non-volatile storage (disk). Even if the server crashes, suffers a power failure, or the operating system halts a millisecond later, the data is guaranteed to survive.
* **Under-the-Hood Mechanism:**
  * Uses the **Redo Log** (Write-Ahead Logging / WAL) and the **Doublewrite Buffer**.
  * Writing updates directly to random sectors on a hard drive/SSD is slow. Instead, when you commit, InnoDB writes the changes sequentially to the **Redo Log** on disk (which is extremely fast because it is sequential write).
  * Only after the Redo Log is flushed to disk does MySQL confirm success. In the background, it updates the actual data files. If a crash occurs, MySQL's startup recovery process replays the **Redo Log** to reconstruct any lost updates.
* **Real-World E-Commerce Example:** The database server crashes immediately after confirming an order. When the server restarts, the order is still safely recorded in the database.
* **MERN Parallel:** Matches MongoDB’s **Journaling** system. When you use the write concern `{ w: 'majority', j: true }`, MongoDB ensures the write is recorded in the journal file on disk before returning success.

---

### Transaction Flow

```
START TRANSACTION
       │
       ├── Query 1: Deduct stock   ✅ Success
       │
       ├── Query 2: Create order   ✅ Success
       │
       ├── Query 3: Add items      ✅ Success
       │
       ├── Query 4: Charge payment ❌ FAILS!
       │
       └── ROLLBACK ← All 3 previous queries are UNDONE!
           Stock restored, order removed, items removed
           Database is exactly as before

vs. Without Transaction:
       ├── Query 1: Deduct stock   ✅ Done (stock reduced)
       ├── Query 2: Create order   ✅ Done (order exists)
       ├── Query 3: Add items      ✅ Done (items exist)
       ├── Query 4: Charge payment ❌ FAILS!
       └── 😱 Stock deducted but order is incomplete!
           Customer charged nothing but stock is gone!
```

---

## Visual Diagram

```
Transaction Lifecycle:
┌──────────────────────────────────────────┐
│                                          │
│   BEGIN ──── Operations ──── COMMIT      │
│     │                          │         │
│     │    Query 1               │         │
│     │    Query 2               │ ✅ Save │
│     │    Query 3               │         │
│     │                          │         │
│     │    If error ──── ROLLBACK│         │
│     │                    │     │         │
│     │               ❌ Undo    │         │
│     │                  All     │         │
│                                          │
└──────────────────────────────────────────┘

Savepoints (partial rollback):
BEGIN
  │
  ├── Query 1 ✅
  │
  ├── SAVEPOINT sp1
  │     │
  │     ├── Query 2 ✅
  │     ├── Query 3 ❌
  │     │
  │     └── ROLLBACK TO sp1  ← Only undo Query 2 & 3
  │
  ├── Query 4 ✅
  │
  └── COMMIT  ← Query 1 and 4 are saved
```

---

## Syntax

```sql
-- ============================================
-- BASIC TRANSACTION
-- ============================================

-- Start a transaction
START TRANSACTION;
-- or: BEGIN;

-- Run your queries
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;  -- Debit
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;  -- Credit

-- If everything is OK → save permanently
COMMIT;

-- If something went wrong → undo everything
ROLLBACK;


-- ============================================
-- SAVEPOINT (partial rollback)
-- ============================================

START TRANSACTION;
INSERT INTO orders (customer_id, total_amount) VALUES (1, 5000);
SAVEPOINT order_created;

INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 1, 2);
-- Oops, something wrong with this item
ROLLBACK TO order_created;  -- Only undo the order_items insert

-- Continue with correct data
INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 2, 1);
COMMIT;


-- ============================================
-- ISOLATION LEVELS
-- ============================================

-- Check current isolation level
SELECT @@transaction_isolation;

-- Set isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;  -- MySQL default
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Levels (from least to most strict):
-- READ UNCOMMITTED: Can see uncommitted changes (dirty reads)
-- READ COMMITTED: Only sees committed changes
-- REPEATABLE READ: Same read returns same results within transaction (default)
-- SERIALIZABLE: Full isolation (slowest, like single-threaded)
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Mongoose Transaction (What You Know) ==========
const session = await mongoose.startSession();
session.startTransaction();

try {
  // Deduct stock
  await Product.updateOne(
    { _id: productId, stock: { $gte: quantity } },
    { $inc: { stock: -quantity } },
    { session }
  );
  
  // Create order
  const order = await Order.create([{
    customerId, totalAmount
  }], { session });
  
  // If all good → commit
  await session.commitTransaction();
} catch (error) {
  // If anything fails → rollback
  await session.abortTransaction();
  throw error;
} finally {
  session.endSession();
}
```

```sql
-- ========== MySQL Transaction ==========
START TRANSACTION;

-- Deduct stock
UPDATE products SET stock = stock - 2 WHERE id = 1 AND stock >= 2;

-- Create order
INSERT INTO orders (customer_id, total_amount, status) VALUES (1, 159998, 'pending');

-- Add order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (LAST_INSERT_ID(), 1, 2, 79999);

COMMIT;
-- If any statement fails, run ROLLBACK instead
```

```js
// ========== Node.js using mysql2/promise ==========
const db = require('./db');

async function placeOrder(customerId, items) {
  // Get a connection from the pool (MUST use same connection for all queries)
  const connection = await db.getConnection();
  
  try {
    // Start transaction
    await connection.beginTransaction();
    
    // Calculate total
    let totalAmount = 0;
    for (const item of items) {
      totalAmount += item.price * item.quantity;
    }
    
    // 1. Create order
    const [orderResult] = await connection.query(
      'INSERT INTO orders (customer_id, total_amount, status) VALUES (?, ?, ?)',
      [customerId, totalAmount, 'pending']
    );
    const orderId = orderResult.insertId;
    
    // 2. Add order items and deduct stock
    for (const item of items) {
      // Check and deduct stock (atomic check)
      const [stockResult] = await connection.query(
        'UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?',
        [item.quantity, item.productId, item.quantity]
      );
      
      if (stockResult.affectedRows === 0) {
        throw new Error(`Insufficient stock for product ${item.productId}`);
      }
      
      // Add order item
      await connection.query(
        'INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
        [orderId, item.productId, item.quantity, item.price]
      );
    }
    
    // All good → commit
    await connection.commit();
    
    return { orderId, totalAmount, status: 'pending' };
    
  } catch (error) {
    // Something failed → rollback everything
    await connection.rollback();
    throw error;
    
  } finally {
    // ALWAYS release the connection back to the pool
    connection.release();
  }
}
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize Transaction ==========

// Option 1: Managed transaction (auto commit/rollback)
const result = await sequelize.transaction(async (t) => {
  const order = await Order.create(
    { customerId, totalAmount: 0, status: 'pending' },
    { transaction: t }
  );
  
  for (const item of items) {
    const [updated] = await Product.update(
      { stock: sequelize.literal(`stock - ${item.quantity}`) },
      { where: { id: item.productId, stock: { [Op.gte]: item.quantity } }, transaction: t }
    );
    
    if (updated === 0) throw new Error('Insufficient stock');
    
    await OrderItem.create(
      { orderId: order.id, productId: item.productId, quantity: item.quantity, unitPrice: item.price },
      { transaction: t }
    );
  }
  
  return order;
});
// Auto-commits if no error, auto-rollbacks if error thrown
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Complete order placement with stock validation and payment

```js
// Node.js + Express — Place Order API (with transaction)
app.post('/api/orders', async (req, res) => {
  const connection = await db.getConnection();
  
  try {
    const { customerId, items } = req.body;
    // items: [{ productId, quantity }]
    
    await connection.beginTransaction();
    
    // 1. Validate and calculate
    let totalAmount = 0;
    const orderItems = [];
    
    for (const item of items) {
      // Get product price and check stock
      const [products] = await connection.query(
        'SELECT id, name, price, stock FROM products WHERE id = ? FOR UPDATE',
        [item.productId]
      );
      // FOR UPDATE: locks the row, preventing other transactions from modifying it
      
      if (products.length === 0) {
        throw new Error(`Product ${item.productId} not found`);
      }
      
      const product = products[0];
      
      if (product.stock < item.quantity) {
        throw new Error(`Insufficient stock for ${product.name}. Available: ${product.stock}`);
      }
      
      totalAmount += product.price * item.quantity;
      orderItems.push({
        productId: product.id,
        quantity: item.quantity,
        unitPrice: product.price
      });
    }
    
    // 2. Create order
    const [orderResult] = await connection.query(
      'INSERT INTO orders (customer_id, total_amount, status) VALUES (?, ?, ?)',
      [customerId, totalAmount, 'pending']
    );
    const orderId = orderResult.insertId;
    
    // 3. Add items and deduct stock
    for (const item of orderItems) {
      await connection.query(
        'INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
        [orderId, item.productId, item.quantity, item.unitPrice]
      );
      
      await connection.query(
        'UPDATE products SET stock = stock - ? WHERE id = ?',
        [item.quantity, item.productId]
      );
    }
    
    // 4. All good → commit
    await connection.commit();
    
    res.status(201).json({
      message: 'Order placed successfully',
      order: { id: orderId, totalAmount, status: 'pending', items: orderItems }
    });
    
  } catch (error) {
    await connection.rollback();
    res.status(400).json({ error: error.message });
  } finally {
    connection.release();
  }
});
```

**Output (Success):**
```json
{
  "message": "Order placed successfully",
  "order": {
    "id": 15,
    "totalAmount": 82498,
    "status": "pending",
    "items": [
      { "productId": 1, "quantity": 1, "unitPrice": "79999.00" },
      { "productId": 3, "quantity": 1, "unitPrice": "2499.00" }
    ]
  }
}
```

---

## Impact

| If You Don't Use Transactions...         | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| Stock deducted but order creation fails  | Stock is lost — product appears sold but no order exists |
| Money debited but credit fails           | Customer loses money — financial disaster        |
| Order created but items not added        | Empty order in the system — confusing reports    |
| Two users buy last item simultaneously   | Both succeed → negative stock (overselling!)     |
| Don't use `FOR UPDATE` locks             | Race conditions in concurrent operations         |
| Forget `connection.release()`            | Connection leak → app hangs after pool exhausted |



---

## Real-World Q&A

### ❓ Q1: MongoDB doesn't need transactions for most operations because of embedded documents. Why does MySQL always need them?
> **💡 Answer:** In MongoDB, updating an order with embedded items is a single document update — atomic by default. In MySQL, creating an order involves INSERT into `orders` + multiple INSERTs into `order_items` + UPDATE on `products` — multiple tables, multiple operations. Transactions tie them together.

### ❓ Q2: What is `FOR UPDATE` and why is it important?
> **💡 Answer:** `SELECT ... FOR UPDATE` locks the selected rows, preventing other transactions from modifying them until the current transaction commits or rolls back. Without it, two users could simultaneously read stock=1, both see it's sufficient, and both deduct — resulting in stock = -1.

### ❓ Q3: What happens if a transaction runs for too long?
> **💡 Answer:** Long transactions hold locks, blocking other operations and potentially causing timeouts or deadlocks. MySQL has `innodb_lock_wait_timeout` (default 50 seconds). Keep transactions as short as possible — do prep work outside the transaction.

---

## Interview Q&A

### ❓ Q1: What is a transaction? Explain ACID.
> **💡 Answer:** A transaction is a unit of work that groups multiple operations into an atomic unit. ACID: Atomicity (all or nothing), Consistency (valid state to valid state), Isolation (concurrent transactions don't interfere), Durability (committed data survives crashes).

### ❓ Q2: What is a deadlock and how do you prevent it?
> **💡 Answer:** A deadlock occurs when two transactions each hold a lock the other needs. Transaction A locks row 1, waits for row 2. Transaction B locks row 2, waits for row 1. Neither can proceed. MySQL detects deadlocks and rolls back one transaction. Prevention: always access tables/rows in the same order, keep transactions short, use appropriate isolation levels.

### ❓ Q3: What are isolation levels in MySQL?
> **💡 Answer:** READ UNCOMMITTED (dirty reads possible), READ COMMITTED (reads only committed data), REPEATABLE READ (default — consistent reads within transaction), SERIALIZABLE (full isolation, like single-threaded). Higher isolation = more correct but slower due to locking.

### ❓ Q4: What is the difference between COMMIT and ROLLBACK?
> **💡 Answer:** COMMIT permanently saves all changes made in the current transaction. ROLLBACK undoes all changes since the last BEGIN/START TRANSACTION. After COMMIT, changes cannot be undone. After ROLLBACK, the database is exactly as it was before the transaction started.

### ❓ Q5: How do you handle transactions in a connection pool scenario?
> **💡 Answer:** Always get a dedicated connection from the pool (`db.getConnection()`), use that single connection for all transaction queries, and release it in a `finally` block. Never use `db.query()` for transactions — it may use different connections for each query!

---

| [← Previous: Indexes](./15_Indexes.md) | [Index](./00_index.md) | [Next: Stored Procedures →](./17_Stored_Procedures.md) |
|---|---|---|
