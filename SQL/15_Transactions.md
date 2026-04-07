# Transactions

> 📌 **File:** `15_Transactions.md` | **Level:** Beginner → MERN Developer

---

## What is it?

A **transaction** is a group of SQL operations that either ALL succeed or ALL fail together. It's an "all-or-nothing" guarantee. If any operation fails, everything is rolled back to the original state — as if nothing happened.

Classic example: Transferring money. Debit from Account A AND credit to Account B must both succeed. If the credit fails after the debit, you'd lose money! Transactions prevent this.

---

## MERN Parallel — You Already Know This!

| MongoDB/Mongoose (You Know)                       | MySQL Transaction (You'll Learn)                |
|---------------------------------------------------|-------------------------------------------------|
| `const session = await mongoose.startSession()`   | `const conn = await pool.getConnection()`       |
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
const pool = require('./db');

async function placeOrder(customerId, items) {
  // Get a connection from the pool (MUST use same connection for all queries)
  const connection = await pool.getConnection();
  
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
  const connection = await pool.getConnection();
  
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

```js
// React — Checkout Component
function Checkout({ cart, customerId }) {
  const [loading, setLoading] = useState(false);

  const placeOrder = async () => {
    setLoading(true);
    try {
      const items = cart.map(item => ({
        productId: item.id,
        quantity: item.quantity
      }));
      
      const { data } = await axios.post('/api/orders', { customerId, items });
      alert(`Order #${data.order.id} placed! Total: ₹${data.order.totalAmount}`);
    } catch (error) {
      alert(error.response?.data?.error || 'Order failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Your Cart</h2>
      {cart.map(item => (
        <div key={item.id}>{item.name} × {item.quantity} — ₹{item.price * item.quantity}</div>
      ))}
      <p><strong>Total: ₹{cart.reduce((sum, i) => sum + i.price * i.quantity, 0)}</strong></p>
      <button onClick={placeOrder} disabled={loading}>
        {loading ? 'Placing Order...' : 'Place Order'}
      </button>
    </div>
  );
}
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

## Practice Exercises

### Easy (SQL)
1. Write a transaction that inserts a customer and then their first order
2. Write a transaction that transfers ₹500 from customer A to customer B (using a balance column)
3. Practice ROLLBACK: start a transaction, insert a row, verify it exists, rollback, verify it's gone

### Medium (SQL + Node.js)
4. Implement the `placeOrder` function with full transaction support
5. Add stock validation with `FOR UPDATE` to prevent race conditions
6. Implement an order cancellation endpoint that reverses the order within a transaction (restore stock + update status)

### Hard (Full Stack)
7. Build a complete checkout flow with cart, order placement, and error handling
8. Simulate 100 concurrent orders for the last item in stock — verify that only one succeeds with transactions

---

## Real-World Q&A

**Q1:** MongoDB doesn't need transactions for most operations because of embedded documents. Why does MySQL always need them?
**A:** In MongoDB, updating an order with embedded items is a single document update — atomic by default. In MySQL, creating an order involves INSERT into `orders` + multiple INSERTs into `order_items` + UPDATE on `products` — multiple tables, multiple operations. Transactions tie them together.

**Q2:** What is `FOR UPDATE` and why is it important?
**A:** `SELECT ... FOR UPDATE` locks the selected rows, preventing other transactions from modifying them until the current transaction commits or rolls back. Without it, two users could simultaneously read stock=1, both see it's sufficient, and both deduct — resulting in stock = -1.

**Q3:** What happens if a transaction runs for too long?
**A:** Long transactions hold locks, blocking other operations and potentially causing timeouts or deadlocks. MySQL has `innodb_lock_wait_timeout` (default 50 seconds). Keep transactions as short as possible — do prep work outside the transaction.

---

## Interview Q&A

**Q1: What is a transaction? Explain ACID.**
A transaction is a unit of work that groups multiple operations into an atomic unit. ACID: Atomicity (all or nothing), Consistency (valid state to valid state), Isolation (concurrent transactions don't interfere), Durability (committed data survives crashes).

**Q2: What is a deadlock and how do you prevent it?**
A deadlock occurs when two transactions each hold a lock the other needs. Transaction A locks row 1, waits for row 2. Transaction B locks row 2, waits for row 1. Neither can proceed. MySQL detects deadlocks and rolls back one transaction. Prevention: always access tables/rows in the same order, keep transactions short, use appropriate isolation levels.

**Q3: What are isolation levels in MySQL?**
READ UNCOMMITTED (dirty reads possible), READ COMMITTED (reads only committed data), REPEATABLE READ (default — consistent reads within transaction), SERIALIZABLE (full isolation, like single-threaded). Higher isolation = more correct but slower due to locking.

**Q4: What is the difference between COMMIT and ROLLBACK?**
COMMIT permanently saves all changes made in the current transaction. ROLLBACK undoes all changes since the last BEGIN/START TRANSACTION. After COMMIT, changes cannot be undone. After ROLLBACK, the database is exactly as it was before the transaction started.

**Q5: How do you handle transactions in a connection pool scenario?**
Always get a dedicated connection from the pool (`pool.getConnection()`), use that single connection for all transaction queries, and release it in a `finally` block. Never use `pool.query()` for transactions — it may use different connections for each query!

---

| [← Previous: Indexes](./14_Indexes.md) | [Next: Stored Procedures →](./16_Stored_Procedures.md) |
|---|---|
