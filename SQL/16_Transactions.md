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
| `const session = await mongoose.startSession()`   | `const conn = await db.getConnection()`         |
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

---

### Under-the-Hood Technical Deep Dive: ACID Mechanics

#### 1. Atomicity ("All-or-Nothing Execution")
* **What it means:** A transaction is treated as a single, indivisible unit of work. Either 100% of the queries are permanently applied, or 0% are.
* **Under-the-Hood Mechanism:**
  * MySQL's InnoDB storage engine uses the **Undo Log**.
  * Before modifying any data, InnoDB writes the reverse action to the Undo Log. For instance, if you update a balance from `$100` to `$80`, InnoDB logs: *"If rollback happens, update it back to `$100`"*. If you insert a row, it logs: *"If rollback happens, delete this row by ID"*.
  * If a query fails or you execute `ROLLBACK`, MySQL reads the Undo Log backward to revert all modifications, returning the database to its exact pre-transaction state.

#### 2. Consistency ("Preserving Database Integrity Rules")
* **What it means:** A transaction must transition the database from one valid state to another, strictly adhering to all defined schemas, constraints, and foreign key relations.
* **Under-the-Hood Mechanism:**
  * Enforced via `NOT NULL`, `UNIQUE`, `CHECK` constraints, and `FOREIGN KEY` referential integrity.
  * If a transaction violates a constraint (e.g. `CHECK (wallet_balance >= 0)`), MySQL immediately throws a fatal SQL error and forces a rollback.

#### 3. Isolation ("Managing Concurrent Operations")
* **What it means:** Concurrent transactions execute without stepping on each other's data modifications.
* **Under-the-Hood Physical Mechanics:**
  * **3 Hidden Clustered Record Columns:**
    1. `DB_TRX_ID` (6 Bytes): The transaction ID of the last transaction that modified this row.
    2. `DB_ROLL_PTR` (7 Bytes): Pointer to the **Undo Log** historical version chain.
    3. `DB_ROW_ID` (6 Bytes): Fallback clustered row identifier.
  * **Read View Generation (MVCC Snapshot):** In `REPEATABLE READ`, InnoDB generates a **Read View** `[m_ids: min_trx_id, max_trx_id]`. If a row's `DB_TRX_ID` is uncommitted or created after the Read View, InnoDB traverses the Undo Log chain via `DB_ROLL_PTR` to read the historical committed snapshot.
  * **Snapshot Read vs Current Read:**
    * *Snapshot Read (Non-locking):* Plain `SELECT` reads historical undo versions without acquiring locks.
    * *Current Read (Locking):* `UPDATE`, `DELETE`, `SELECT ... FOR UPDATE` read the latest physical disk state and place row/gap locks.
  * **Write Skew Anomaly:** Occurs under `REPEATABLE READ` when two concurrent transactions read valid overlapping state (e.g., both check `COUNT(*) WHERE on_call = 1` which returns 2) and modify separate rows (both set `on_call = 0`), resulting in 0 on-call doctors! Prevented via `SELECT ... FOR UPDATE` or `SERIALIZABLE`.
  * **Two-Phase Locking (2PL):** Growing phase (acquire locks) $\rightarrow$ Shrinking phase (release locks upon `COMMIT`/`ROLLBACK`).

#### 4. Durability ("Surviving Crashes")
* **What it means:** Once committed, changes survive server crashes, power failures, and OS crashes.
* **Under-the-Hood Mechanism:**
  * InnoDB uses the **Redo Log** (Write-Ahead Logging / WAL) and the **Doublewrite Buffer**.
  * On `COMMIT`, changes are written sequentially to the append-only Redo Log on disk. On restart, InnoDB replays the Redo Log during crash recovery.

---

## 🏷️ Types of Database Transactions & Architectures

In modern database systems, transactions are classified across multiple dimensions:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 TYPES OF DATABASE TRANSACTIONS                                   │
├──────────────────────┬──────────────────────────────────────────────┬────────────────────────────┤
│ Transaction Type     │ How it Works & Engine Behavior               │ Practical Production Use   │
├──────────────────────┼──────────────────────────────────────────────┼────────────────────────────┤
│ 1. Explicit          │ Manually demarcated with `START TRANSACTION` │ High-value multi-step API  │
│    Transactions      │ and finalized with `COMMIT` or `ROLLBACK`.   │ operations (checkout/order)│
├──────────────────────┼──────────────────────────────────────────────┼────────────────────────────┤
│ 2. Implicit          │ Every standalone query auto-commits instantly│ Default for simple single  │
│    (Autocommit)      │ by default (`@@autocommit = 1`).             │ read/write API endpoints.  │
├──────────────────────┼──────────────────────────────────────────────┼────────────────────────────┤
│ 3. Read-Only         │ Declared via `START TRANSACTION READ ONLY`.  │ High-throughput analytical │
│    Transactions      │ Engine skips `DB_TRX_ID` & Undo Log memory.  │ reporting & Read Replicas. │
├──────────────────────┼──────────────────────────────────────────────┼────────────────────────────┤
│ 4. Chained           │ `COMMIT AND CHAIN` commits current work and  │ High-throughput batching   │
│    Transactions      │ immediately opens a new transaction in 0ms.  │ without connection hops.   │
├──────────────────────┼──────────────────────────────────────────────┼────────────────────────────┤
│ 5. Savepoint         │ Sets internal checkpoints (`SAVEPOINT sp1`)  │ Resilient workflows with   │
│    (Flat + Nested)   │ allowing partial rollback without aborting.  │ optional sub-operations.   │
├──────────────────────┼──────────────────────────────────────────────┼────────────────────────────┤
│ 6. Distributed / XA  │ Multi-server Two-Phase Commit (2PC)          │ Cross-database banking and │
│    Transactions      │ coordinated via `XA START`, `PREPARE`, `COMMIT`│ enterprise micro-shards.   │
├──────────────────────┼──────────────────────────────────────────────┼────────────────────────────┤
│ 7. Compensating      │ Application-level Saga pattern with forward  │ Asynchronous distributed   │
│    (Sagas)           │ actions and reverse compensating API calls.  │ event-driven microservices.│
└──────────────────────┴──────────────────────────────────────────────┴────────────────────────────┘
```

---

### 1. Read-Only vs Read-Write Transactions
* **`START TRANSACTION READ WRITE` (Default):** Prepares for modifications, allocates transaction IDs, and writes to undo logs.
* **`START TRANSACTION READ ONLY` (Engine Performance Optimization):**
  - Informs InnoDB that only `SELECT` statements will run.
  - **The Optimization:** InnoDB **completely bypasses** allocating a unique transaction ID (`DB_TRX_ID`), avoids allocating Undo Log memory structures, and skips transaction list tracking in the internal engine lock manager.
  - **Impact:** Drastically reduces CPU cache line contention and lock manager memory thrashing on read replicas and analytics dashboards.

---

### 2. Distributed Transactions: XA & Two-Phase Commit (2PC)
When a single business transaction spans multiple independent database nodes (e.g., Shard 1 and Shard 2):

```
Coordinator (Node.js App / Proxy)          Shard A (MySQL 1)            Shard B (MySQL 2)
       │                                          │                            │
       ├──── Phase 1: XA PREPARE ────────────────▶│                            │
       ├──── Phase 1: XA PREPARE ─────────────────────────────────────────────▶│
       │                                          │                            │
       │◀─── Vote: "YES (Prepared)" ──────────────┤                            │
       │◀─── Vote: "YES (Prepared)" ───────────────────────────────────────────┤
       │                                          │                            │
       │   (If all nodes vote YES, Coordinator sends COMMIT. Else ROLLBACK)    │
       │                                          │                            │
       ├──── Phase 2: XA COMMIT ─────────────────▶│                            │
       ├──── Phase 2: XA COMMIT ──────────────────────────────────────────────▶│
       ▼                                          ▼                            ▼
```

* **MySQL XA Syntax:**
  ```sql
  XA START 'order_tx_001';
  UPDATE user_wallet SET balance = balance - 100 WHERE user_id = 42;
  XA END 'order_tx_001';
  XA PREPARE 'order_tx_001'; -- Node writes Redo Log and holds locks
  -- When coordinator confirms all nodes prepared:
  XA COMMIT 'order_tx_001';
  ```

---

### 3. ⚠️ The Silent Implicit Commit Trap (DDL & Schema Invalidation)

In MySQL, executing certain statements inside an active transaction causes the engine to **silently and automatically issue an immediate `COMMIT`**, destroying your ability to `ROLLBACK`!

```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 1000 WHERE id = 1; -- Deducted $1000

-- ⚠️ DISASTER: Running DDL triggers an IMPLICIT COMMIT!
ALTER TABLE logs ADD COLUMN client_ip VARCHAR(45);

-- ❌ THIS ROLLBACK DOES NOTHING! The $1000 deduction is already permanently committed!
ROLLBACK;
```

#### Statements That Trigger Silent Implicit Commits:
1. **Data Definition Language (DDL):** `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, `TRUNCATE TABLE`, `RENAME TABLE`, `CREATE INDEX`, `DROP INDEX`.
2. **User & Security Management:** `CREATE USER`, `DROP USER`, `GRANT`, `REVOKE`, `SET PASSWORD`.
3. **Table Maintenance & Locking:** `LOCK TABLES`, `UNLOCK TABLES`, `OPTIMIZE TABLE`, `ANALYZE TABLE`, `CHECK TABLE`.
4. **Nested Transaction Starts:** Invoking `START TRANSACTION` or `BEGIN` while a transaction is already active automatically commits the previous one!

---

### 🔒 Complete InnoDB Lock Types & Granularity Hierarchy

InnoDB uses a multi-granularity locking hierarchy to balance maximum concurrency with strict isolation:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              INNODB LOCK TYPE HIERARCHY                                │
├─────────────────────────┬──────────────┬───────────────────────────────────────────────┤
│ Lock Type               │ Granularity  │ What it Locks & Purpose                       │
├─────────────────────────┼──────────────┼───────────────────────────────────────────────┤
│ **Shared (S)**          │ Row-level    │ Read lock (`FOR SHARE`). Multiple transactions │
│                         │              │ can read; blocks all Exclusive (X) writes.    │
├─────────────────────────┼──────────────┼───────────────────────────────────────────────┤
│ **Exclusive (X)**       │ Row-level    │ Write lock (`FOR UPDATE`, `UPDATE`, `DELETE`). │
│                         │              │ Only 1 transaction can hold; blocks all S & X.│
├─────────────────────────┼──────────────┼───────────────────────────────────────────────┤
│ **Intention Shared (IS)**│ Table-level │ Indicates a transaction intends to set an S   │
│                         │              │ lock on individual rows. Allows $O(1)$ table  │
│                         │              │ lock conflict checks without scanning rows.   │
├─────────────────────────┼──────────────┼───────────────────────────────────────────────┤
│ **Intention Exclusive** │ Table-level  │ Indicates a transaction intends to set an X   │
│ **(IX)**                │              │ lock on individual rows.                      │
├─────────────────────────┼──────────────┼───────────────────────────────────────────────┤
│ **Record Lock**         │ Index Record │ Locks the exact physical B+Tree index entry.   │
├─────────────────────────┼──────────────┼───────────────────────────────────────────────┤
│ **Gap Lock**            │ Index Gap    │ Locks the space *between* index records (or   │
│                         │              │ before first / after last). Stops Phantoms!   │
├─────────────────────────┼──────────────┼───────────────────────────────────────────────┤
│ **Next-Key Lock**       │ Record + Gap │ Combination: Locks record AND the gap before  │
│                         │              │ it. Default row lock in `REPEATABLE READ`.    │
├─────────────────────────┼──────────────┼───────────────────────────────────────────────┤
│ **Insert Intention**    │ Gap subtype  │ Special gap lock set before inserting a row   │
│                         │              │ so concurrent inserts in different positions  │
│                         │              │ of the same gap don't block each other.       │
├─────────────────────────┼──────────────┼───────────────────────────────────────────────┤
│ **AUTO-INC Lock**       │ Table-level  │ Special lock held during auto-increment inserts│
│                         │              │ (tuned via `innodb_autoinc_lock_mode`).       │
└─────────────────────────┴──────────────┴───────────────────────────────────────────────┘
```

#### Why are Intention Locks (`IS`/`IX`) Critical?
If Transaction A holds an Exclusive (X) row lock on row 5,000, and Transaction B requests a full table lock (`LOCK TABLES users WRITE`):
- Without Intention Locks, Transaction B would have to scan all 10,000,000 rows in the table to check if any row is locked!
- With Intention Locks, Transaction A automatically placed an `IX` lock on the `users` table header when it locked row 5,000. Transaction B checks the table header in **$O(1)$ constant time**, sees the `IX` lock, and immediately waits!

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
  ├── Query 2 ✅
  ├── Query 3 ❌
  │     │
  └── ROLLBACK TO sp1  ← Only undo Query 2 & 3
  │
  ├── Query 4 ✅
  │
  └── COMMIT  ← Query 1 and 4 are saved
```

---

## Syntax

```sql
-- ============================================
-- 1. BASIC EXPLICIT TRANSACTION
-- ============================================

-- Start a standard Read-Write transaction
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
-- 2. READ-ONLY OPTIMIZED TRANSACTION
-- ============================================

-- Skips DB_TRX_ID allocation & Undo Log memory overhead for high-speed reporting
START TRANSACTION READ ONLY;
SELECT customer_id, SUM(total_amount) FROM orders GROUP BY customer_id;
COMMIT;


-- ============================================
-- 3. CHAINED TRANSACTIONS
-- ============================================

START TRANSACTION;
INSERT INTO audit_logs (event) VALUES ('batch_step_1');
-- Atomically commits step 1 and immediately begins step 2 in 0ms:
COMMIT AND CHAIN;
INSERT INTO audit_logs (event) VALUES ('batch_step_2');
COMMIT;


-- ============================================
-- 4. SAVEPOINTS (Partial Rollbacks)
-- ============================================

START TRANSACTION;
INSERT INTO orders (customer_id, total_amount) VALUES (1, 5000);
SAVEPOINT order_created;

INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 1, 2);
-- Oops, something wrong with this item
ROLLBACK TO order_created;  -- Only undo the order_items insert, order remains intact!

-- Continue with correct data
INSERT INTO order_items (order_id, product_id, quantity) VALUES (1, 2, 1);
COMMIT;


-- ============================================
-- 5. ISOLATION LEVELS & CONCURRENCY ANOMALIES
-- ============================================

-- Check current isolation level
SELECT @@transaction_isolation;

-- Set isolation level (Session or Global)
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;  -- MySQL default

/*
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ISOLATION LEVEL & ANOMALY MATRIX                                │
├──────────────────┬────────────┬────────────────────┬──────────────┬────────────────────┤
│ Isolation Level  │ Dirty Read │ Non-Repeatable Read│ Phantom Read │ Concurrency Perf   │
├──────────────────┼────────────┼────────────────────┼──────────────┼────────────────────┤
│ READ UNCOMMITTED │ ❌ Yes     │ ❌ Yes             │ ❌ Yes       │ ⚡ Fastest         │
│ READ COMMITTED   │ ✅ No      │ ❌ Yes             │ ❌ Yes       │ ⏱️ Fast (Web apps) │
│ REPEATABLE READ  │ ✅ No      │ ✅ No              │ ✅ No (InnoDB│ ⚖️ Default (MVCC)  │
│ (MySQL Default)  │            │                    │ Next-Key Lock│                    │
│ SERIALIZABLE     │ ✅ No      │ ✅ No              │ ✅ No        │ 🐢 Slowest (Locks) │
└──────────────────┴────────────┴────────────────────┴──────────────┴────────────────────┘
*/


-- ============================================
-- 6. INNODB LOCK TYPES
-- ============================================

-- Shared Read Lock (Allows others to read, blocks writes):
SELECT * FROM products WHERE id = 10 FOR SHARE;

-- Exclusive Write Lock (Blocks others from reading/writing until COMMIT):
SELECT * FROM products WHERE id = 10 FOR UPDATE;

-- Next-Key Lock (Record Lock + Gap Lock):
SELECT * FROM products WHERE id BETWEEN 10 AND 20 FOR UPDATE;
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

## Real-World Scenario + Full Stack Code

### Scenario: E-Commerce Checkout with Balance & Inventory Validation

```sql
-- Schema setup
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  wallet_balance DECIMAL(10,2) NOT NULL,
  CONSTRAINT chk_wallet CHECK (wallet_balance >= 0)
);

CREATE TABLE products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  stock INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  CONSTRAINT chk_stock CHECK (stock >= 0)
);

CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT,
  total_amount DECIMAL(10,2),
  status VARCHAR(20) DEFAULT 'completed',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

```js
// Express API Endpoint: POST /api/checkout
const express = require('express');
const router = express.Router();
const pool = require('./db');

router.post('/checkout', async (req, res) => {
  const { userId, productId, quantity } = req.body;
  
  // 1. Acquire dedicated connection from the connection pool
  const connection = await pool.getConnection();

  try {
    // 2. Start Explicit Transaction
    await connection.beginTransaction();

    // 3. Lock product row exclusively to prevent concurrent race conditions
    const [products] = await connection.query(
      'SELECT id, name, price, stock FROM products WHERE id = ? FOR UPDATE',
      [productId]
    );

    if (products.length === 0) {
      throw new Error('Product not found');
    }

    const product = products[0];
    if (product.stock < quantity) {
      throw new Error(`Insufficient stock! Only ${product.stock} left.`);
    }

    const totalCost = product.price * quantity;

    // 4. Lock user row exclusively to verify wallet balance
    const [users] = await connection.query(
      'SELECT id, wallet_balance FROM users WHERE id = ? FOR UPDATE',
      [userId]
    );

    const user = users[0];
    if (user.wallet_balance < totalCost) {
      throw new Error(`Insufficient wallet balance! Cost: $${totalCost}, Balance: $${user.wallet_balance}`);
    }

    // 5. Deduct wallet balance
    await connection.query(
      'UPDATE users SET wallet_balance = wallet_balance - ? WHERE id = ?',
      [totalCost, userId]
    );

    // 6. Deduct inventory stock
    await connection.query(
      'UPDATE products SET stock = stock - ? WHERE id = ?',
      [quantity, productId]
    );

    // 7. Create finalized Order record
    const [orderResult] = await connection.query(
      'INSERT INTO orders (user_id, total_amount, status) VALUES (?, ?, ?)',
      [userId, totalCost, 'completed']
    );

    // 8. Permanent Atomic Commit
    await connection.commit();

    res.status(200).json({
      success: true,
      message: 'Checkout completed successfully!',
      orderId: orderResult.insertId,
      debited: totalCost,
      remainingBalance: user.wallet_balance - totalCost
    });

  } catch (err) {
    // 9. Atomic Rollback: Reverts wallet deductions, stock changes, and order creation
    await connection.rollback();
    console.error('Transaction Failed -> Rolled Back:', err.message);

    res.status(400).json({
      success: false,
      error: err.message
    });

  } finally {
    // 10. ALWAYS release connection back to pool
    connection.release();
  }
});

module.exports = router;
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
> **💡 Answer:** A transaction is a unit of work that groups multiple operations into an atomic unit. ACID: Atomicity (all or nothing via Undo Log), Consistency (valid state transitions via constraints), Isolation (concurrency management via MVCC snapshots and locks), Durability (crash survival via Redo Log and WAL).

### ❓ Q2: What is a deadlock and how do you prevent it?
> **💡 Answer:** A deadlock occurs when two transactions each hold a lock the other needs. Transaction A locks row 1, waits for row 2. Transaction B locks row 2, waits for row 1. MySQL detects deadlocks and rolls back the transaction with the fewest row modifications. Prevention: access tables/rows in a globally consistent order, keep transactions short, and use optimistic locking or `SELECT ... FOR UPDATE` consistently.

### ❓ Q3: What are isolation levels in MySQL?
> **💡 Answer:** READ UNCOMMITTED (dirty reads possible), READ COMMITTED (reads only committed data), REPEATABLE READ (default — consistent reads within transaction), SERIALIZABLE (full isolation, locks all reads). Higher isolation = more correct but slower due to locking.

### ❓ Q4: What is the difference between COMMIT and ROLLBACK?
> **💡 Answer:** COMMIT permanently saves all changes made in the current transaction to disk via the Redo Log. ROLLBACK undoes all modifications using the Undo Log. After COMMIT, changes are permanent. After ROLLBACK, the database is restored to its exact pre-transaction state.

### ❓ Q5: How do you handle transactions in a connection pool scenario?
> **💡 Answer:** Always get a dedicated connection from the pool (`db.getConnection()`), use that single connection for all transaction queries, and release it in a `finally` block. Never use `db.query()` for transactions — it acquires and releases different pool connections for each query!

### ❓ Q6: How does InnoDB implement MVCC under the hood?
> **💡 Answer:** Every clustered index row in InnoDB contains two hidden record header fields: `DB_TRX_ID` (the 6-byte transaction ID that modified the row) and `DB_ROLL_PTR` (a 7-byte pointer to the Undo Log segment containing the previous row version). When a query runs in `REPEATABLE READ`, InnoDB creates a Read View containing active transaction IDs. If a row's `DB_TRX_ID` is active or was committed after the Read View creation, InnoDB follows `DB_ROLL_PTR` down the Undo Log history chain until it finds a row version committed *before* the transaction began.

### ❓ Q7: What is the difference between a Consistent Snapshot Read and a Current Read?
> **💡 Answer:** A **Consistent Snapshot Read** (plain `SELECT`) reads historical data versions from the Undo Log without acquiring locks, providing non-blocking read scalability. A **Current Read** (`UPDATE`, `DELETE`, `INSERT`, `SELECT ... FOR UPDATE`) reads the *latest committed physical row* directly from the table and places row/gap locks (Next-Key locks) on index records to prevent concurrent write interference.

### ❓ Q8: What is Write Skew and why does REPEATABLE READ fail to prevent it?
> **💡 Answer:** Write Skew occurs when two concurrent transactions read overlapping data, make disjoint modifications based on what they read, and commit — resulting in an end state that violates a business constraint (e.g. the hospital on-call doctor dilemma). It happens under `REPEATABLE READ` because both transactions perform non-locking Snapshot Reads (both see valid states) and update different rows. It can only be prevented using explicit locking (`SELECT ... FOR UPDATE`) or `SERIALIZABLE` isolation.

### ❓ Q9: What are the different types of database transactions, and when would you use a Read-Only Transaction?
> **💡 Answer:** 
> 1. **Explicit Transactions:** Manually started with `START TRANSACTION` and ended with `COMMIT`/`ROLLBACK`.
> 2. **Implicit / Autocommit Transactions:** Single statements committed automatically.
> 3. **Read-Only Transactions (`START TRANSACTION READ ONLY`):** Used for analytics and read replicas. InnoDB optimizes these by completely skipping transaction ID (`DB_TRX_ID`) allocation and Undo Log memory buffers, minimizing lock manager CPU overhead.
> 4. **Chained Transactions (`COMMIT AND CHAIN`):** Commits the current transaction and immediately opens a new one with zero network overhead.
> 5. **Distributed / XA Transactions:** Two-Phase Commit (2PC) transactions coordinated across multiple physical database nodes (`XA START`, `PREPARE`, `COMMIT`).
> 6. **Compensating Transactions (Sagas):** Application-level forward and undo API workflows used in distributed microservices.

### ❓ Q10: What is an Intention Lock (`IS`/`IX`) in InnoDB and why does it exist?
> **💡 Answer:** Intention Locks are **table-level locks** that declare what type of lock (Shared `IS` or Exclusive `IX`) a transaction intends to acquire on individual rows. They exist to allow table-level lock requests (such as `LOCK TABLES users WRITE` or `ALTER TABLE`) to detect row-level lock conflicts in **$O(1)$ constant time** by checking the table header, eliminating the need to scan millions of individual row locks.

### ❓ Q11: What is an "Implicit Commit" in MySQL, and what statements cause it?
> **💡 Answer:** An Implicit Commit occurs when MySQL **silently and automatically commits** an active transaction before executing certain non-transactional statements, permanently preventing any subsequent `ROLLBACK`. It is triggered by **DDL statements** (`ALTER TABLE`, `CREATE TABLE`, `DROP TABLE`, `TRUNCATE`), **security statements** (`CREATE USER`, `GRANT`), **table locking** (`LOCK TABLES`), and starting a new transaction with `START TRANSACTION` without committing the previous one.

---

| [← Previous: Indexes](./15_Indexes.md) | [Index](./00_index.md) | [Next: Stored Procedures →](./17_Stored_Procedures.md) |
|---|---|---|
