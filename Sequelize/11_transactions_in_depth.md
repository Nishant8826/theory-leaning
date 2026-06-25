# 11. Transactions in Depth

## 🎯 Goal of This Chapter
By the end of this chapter, you will understand what database transactions are, how they enforce ACID compliance, the difference between Managed and Unmanaged transactions in Sequelize, and how to write reliable multi-step write operations.

---

## 🤔 Why This Topic Matters
Imagine running an E-commerce store. A customer purchases an item:
1. Step 1: Your backend creates an invoice record in the `Orders` table.
2. Step 2: Your backend decrements the stock quantity in the `Products` table.

What happens if Step 1 succeeds, but the database connection drops or the server crashes before Step 2 executes? 
You have sold a product but failed to update stock, leading to overselling. 

**Transactions** group multiple database operations into a single unit of work. Either all operations succeed (Commit), or all operations are cancelled (Rollback), keeping your database consistent.

---

## 🧠 Core Concept

### ACID Properties
A transaction guarantees four properties to keep your database safe:
* **Atomicity** (All or Nothing): Either the entire transaction succeeds, or the database is reverted to its original state.
* **Consistency**: A transaction can only transition the database from one valid state to another, maintaining constraints.
* **Isolation**: Transactions running concurrently cannot see each other's partial, uncommitted changes.
* **Durability**: Once a transaction commits, the written data is permanently written to disk, surviving server crashes.

### Managed vs. Unmanaged Transactions
Sequelize supports two approaches for writing transactions:

| Feature | Managed Transactions (Recommended) | Unmanaged Transactions |
| :--- | :--- | :--- |
| **Control** | Sequelize handles commits and rollbacks automatically. | The developer must manually call commit and rollback. |
| **Code Safety** | High. Safe from forgetting to rollback during exceptions. | Low. If you forget to call rollback on error, connections lock up. |
| **Implementation** | Uses a callback function wrapper. | Uses manual variables and try-catch blocks. |

---

## 🏗 Mental Model / Internal Working

### Connection Isolation & Locks
When you start a transaction:
1. Sequelize leases a dedicated database connection socket from the pool.
2. It sends `BEGIN TRANSACTION;` to the database.
3. During the transaction, the database locks the affected rows (e.g. locks the product inventory row) so other concurrent requests cannot edit the same row until your transaction is done.
4. If successful, Sequelize sends `COMMIT;`, updating the database and releasing locks.
5. If an error is thrown, Sequelize sends `ROLLBACK;`, reverting modifications and releasing locks.

---

## 🌍 Real-World Analogy
Think of a **Vending Machine**:
* A purchase is a transaction.
* Step 1: You insert money.
* Step 2: You press the button.
* Step 3: The machine drops the soda.
* If the soda gets stuck on the shelf (Step 3 fails), the machine does not keep your money. It rolls back the transaction by returning your coins. You do not end up in an intermediate state where you lost money and got no drink.

---

## ⚙️ Syntax / API / Core Usage

### 1. Managed Transactions (Recommended Syntax)
You pass a callback function to `sequelize.transaction()`. If the callback runs without throwing an error, Sequelize commits the transaction. If an error is thrown, it rolls back the transaction.

```javascript
try {
  await sequelize.transaction(async (t) => {
    // You MUST pass { transaction: t } to every query
    const user = await User.create({ username: 'alice' }, { transaction: t });
    
    await Profile.create({ 
      userId: user.id, 
      bio: 'Developer' 
    }, { transaction: t });
  });
  // If execution reaches here, the transaction has been committed successfully!
} catch (error) {
  // If execution reaches here, the transaction has been rolled back automatically!
  console.error('Transaction failed:', error.message);
}
```

### 2. Unmanaged Transactions (Manual Syntax)
You manually call `.commit()` and `.rollback()`:

```javascript
// Start the transaction
const t = await sequelize.transaction();

try {
  const user = await User.create({ username: 'bob' }, { transaction: t });
  await Profile.create({ userId: user.id, bio: 'Designer' }, { transaction: t });
  
  // Manually commit
  await t.commit();
} catch (error) {
  // Manually rollback on failure
  await t.rollback();
}
```

---

## 💻 Practical Examples

### E-commerce Checkout Transaction
Here is a complete checkout controller executing order creation and inventory reduction within a managed transaction.

```javascript
// src/controllers/orderController.js
const sequelize = require('../config/database');
const Product = require('../models/Product');
const Order = require('../models/Order');

module.exports = {
  createOrder: async (req, res) => {
    const { productId, quantity, userId } = req.body;

    try {
      // Execute all database writes inside a managed transaction
      const result = await sequelize.transaction(async (transaction) => {
        // 1. Fetch the product and lock the row for update (prevents race conditions)
        const product = await Product.findByPk(productId, {
          transaction,
          lock: transaction.LOCK.UPDATE // Locks row until transaction commits
        });

        if (!product) {
          throw new Error('Product not found.');
        }

        if (product.stock < quantity) {
          throw new Error('Insufficient product stock available.');
        }

        // 2. Reduce the product inventory stock
        product.stock -= quantity;
        await product.save({ transaction });

        // 3. Create the order invoice record
        const totalAmount = product.price * quantity;
        const order = await Order.create({
          userId,
          productId,
          quantity,
          totalAmount,
          status: 'pending'
        }, { transaction });

        // Return data to controller parent scope
        return order;
      });

      // Commit happens here automatically
      return res.status(201).json({ status: 'success', order: result });
    } catch (error) {
      // Rollback happens here automatically
      return res.status(400).json({ status: 'fail', error: error.message });
    }
  }
};
```

---

## 🔄 Flow Diagram

### Managed Transaction Lifecycle

```text
                  Call: sequelize.transaction()
                               │
                               ▼
                    Lease DB Connection Socket
                     & send "BEGIN" command
                               │
                               ▼
                     Execute Callback block
                               │
                All queries pass { transaction: t }?
                      /                 \
                    YES                  NO
                    /                     \
                   v                       v
          Executes on leased         Executes on different
          socket connection          connection (Dangerous!)
                   │                       │
                   └───────────┬───────────┘
                               │
                     Does callback throw error?
                      /                 \
                    YES                  NO
                    /                     \
                   v                       v
            Send "ROLLBACK"            Send "COMMIT"
          Revert table changes       Persist table changes
                   │                       │
                   └───────────┬───────────┘
                               │
                               ▼
                     Return DB Connection Socket
                            to the pool
```

---

## 🧪 Common Interview Questions

### Q1: Why is it critical to pass the `{ transaction: t }` object to every query within a transaction block?
* **Answer**: If you omit `{ transaction: t }` from a query, that query executes outside the transaction, using a separate connection socket from the pool. It will not see the uncommitted changes made inside the transaction, and if the transaction rolls back, this unjoined query's writes will **not** be reverted, leading to database inconsistencies.

### Q2: What is row locking (`lock: transaction.LOCK.UPDATE`) and when should you use it?
* **Answer**: Row locking prevents race conditions where two concurrent requests try to modify the same database row simultaneously. For example, if two customers buy the last item at the exact same millisecond, row locking forces the second query to block and wait until the first transaction commits or rolls back, ensuring stock checks remain accurate.

### Q3: What is the difference between Managed and Unmanaged transactions?
* **Answer**: 
  * A managed transaction takes a callback. If the callback succeeds, it auto-commits; if it throws an error, it auto-rolls back.
  * An unmanaged transaction requires the developer to store a transaction variable and manually call `t.commit()` and `t.rollback()` in try-catch blocks.

---

## ⚠️ Common Mistakes / Pitfalls
* **Forgetting the Transaction Argument**: Omitting `{ transaction: t }` from one of the update queries, leading to partial writes that bypass the rollback system.
* **Non-Database Side Effects inside Transactions**: Executing irreversible API calls (like calling a payment gateway or sending a SMS notification) *inside* the transaction block. If the database write fails, the SMS is still sent, creating confusion.

---

## ✅ Best Practices
* **Keep Transactions Short**: Run database transactions as fast as possible. Long transactions hold row locks, causing other client requests to queue, lag, and eventually time out.
* **Perform external side effects AFTER transaction commits**: Always process payments or trigger notification emails after the `sequelize.transaction` callback block has resolved successfully.

---

## 📝 Quick Recap
* Transactions guarantee ACID operations, ensuring multi-step updates succeed or fail together.
* Use managed transactions (`sequelize.transaction(callback)`) to automate commits and rollbacks.
* Always pass `{ transaction: t }` to every query executed inside a transaction.
* Lock inventory rows using `lock: transaction.LOCK.UPDATE` to prevent double-spending race conditions.

---

## 🔗 Navigation
Previous : [10_eager_and_lazy_loading.md](./10_eager_and_lazy_loading.md) | Index : [00_index.md](./00_index.md) | Next : [12_paranoid_tables_and_scopes.md](./12_paranoid_tables_and_scopes.md)
