# Transactions

> 📌 **File:** 15_Transactions.md | **Level:** Beginner → MERN Developer

---

## What is it?
A Transaction bundles multiple SQL commands into one atomic unit of work. If step 1 succeeds but step 2 fails, the entire transaction "Rolls back" (undoes) step 1, leaving the database perfectly safe.

## MERN Parallel — You Already Know This!
- MongoDB Sessions `session.startTransaction()`, `session.commitTransaction()`
- Exactly equivalent to SQL Transactions (`START TRANSACTION`, `COMMIT`, `ROLLBACK`)

## Why does it matter?
**Money.** If you process a cart checkout: Step A charges their card. Step B removes inventory. If Step B crashes, their card was charged, but you didn't mark inventory. They sue you. Transactions guarantee either ALL steps happen, or NONE happen.

## How does it work?
You tell the connection to `START TRANSACTION`. Use the connection `pool.getConnection()` to lock down one thread. Run your queries. If all succeed, run `COMMIT`. If any `catch(e)` errors, run `ROLLBACK`.

## Visual Diagram
```ascii
[ START TRANSACTION ]
   |
   +-- INSERT order_id 1
   |
   +-- UPDATE user wallet (-$50) --> CRASH!
   |
[ ROLLBACK ] --> INSERT order_id 1 is erased as if it never occurred.
```

## Syntax
```sql
-- Fully commented SQL syntax
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT; -- Or ROLLBACK if failing.
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose (Replicaset required for Mongo Transactions)
const session = await mongoose.startSession();
session.startTransaction();
try {
  await A.save({ session });
  await session.commitTransaction();
} catch (e) { await session.abortTransaction(); }

// Node.js using mysql2/promise (REQUIRED)
const connection = await pool.getConnection(); // Grab 1 physical line
await connection.beginTransaction();
try {
  await connection.query('UPDATE ..');
  await connection.commit();
} catch (e) {
  await connection.rollback();
} finally {
  connection.release(); // Put line back in pool
}

// ORM Equivalent (IMPORTANT)
// Prisma
await prisma.$transaction([
  prisma.user.update(...),
  prisma.post.create(...)
])
```

### Raw SQL vs ORM
- **Raw SQL:** Requires careful locking and releasing logic over HTTP API endpoints. Manually forgetting to `.release()` locks out your database connection pool immediately.
- **ORM:** Handles the commit/rollback cycle inherently over arrays of queries cleanly. 

### Real-World Scenario + Full Stack Code
**Scenario:** Safely checking out a cart product. Deduping inventory and inserting the order record natively.

```sql
-- SQL query conceptual
START TRANSACTION;
INSERT INTO orders ...;
UPDATE products SET stock = stock - 1;
COMMIT;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.post('/api/checkout', async (req, res) => {
  const { userId, productId } = req.body;
  const connection = await pool.getConnection(); 

  try {
    await connection.beginTransaction();

    // 1. Insert order
    await connection.query('INSERT INTO orders (user_id, product_id) VALUES (?, ?)', [userId, productId]);

    // 2. Decrement stock
    await connection.query('UPDATE products SET stock = stock - 1 WHERE id = ?', [productId]);

    // 3. Optional intentional error simulation
    // throw new Error("Simulated Crash");
    
    await connection.commit(); // Push all code finally
    res.json({ success: true, msg: 'Checkout Complete' });
  } catch (err) {
    await connection.rollback(); // Undo insert
    res.status(500).json({ error: err.message });
  } finally {
    connection.release(); // CRITICAL! Free up for the next API hit!
  }
});
```

**Output:**
```json
{
  "success": true,
  "msg": "Checkout Complete"
}
```

## Impact
If your Node API crashes mid-flow without a Transaction, data goes physically out of sync immediately. Conversely, keeping a Transaction open too long (e.g., waiting for an external Axios API call mid-transaction) physically LOCKS those rows blocking every other user on the internet. Keep transactions millisecond-fast.

## Practice Exercises
- **Easy (SQL)**: Write a literal `START TRANSACTION; UPDATE.. ROLLBACK;` script. Notice changes disappear.
- **Medium (SQL + Node.js)**: Implement a bank transfer Express route safely moving money from account A to B using `.getConnection()`.
- **Hard (Full stack)**: Build a React interface that triggers a transaction intentionally designed to fail halfway, and verify the frontend shows original DB states haven't altered.

## Interview Q&A
1. **Core SQL:** What does ACID stand for?
   *Atomicity, Consistency, Isolation, Durability. Transactions handle Atomicity (All or Nothing).*
2. **MERN integration:** Why do we use `pool.getConnection()` instead of `pool.query()` for transactions?
   *`pool.query()` pulls a random temporary connection line per query. Thus, Step 2 might hit an entirely different DB line. `getConnection()` locks onto ONE persistent thread for the whole journey.*
3. **SQL vs MongoDB:** Why are transactions harder/less common in MongoDB?
   *Because MongoDB clusters documents. Updating 1 embedded array (all data in 1 document) is natively atomic. SQL requires updating dozens of normalized tables, demanding transactions everywhere.*
4. **Scenario-based:** You called `beginTransaction`, but forgot `commit()`. Result?
   *The DB locks rows forever until timeout. App dies.*
5. **Advanced/tricky:** What is Isolation Level?
   *Defines how visible in-progress (uncommitted) transaction changes are to other parallel connections. Usually set to "READ COMMITTED".*

| Previous: [14_Indexes.md](./14_Indexes.md) | Next: [16_Stored_Procedures.md](./16_Stored_Procedures.md) |
