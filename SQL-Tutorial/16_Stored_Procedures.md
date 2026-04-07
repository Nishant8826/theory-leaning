# Stored Procedures

> 📌 **File:** 16_Stored_Procedures.md | **Level:** Beginner → MERN Developer

---

## What is it?
A Stored Procedure is essentially an executable JavaScript function... written entirely in SQL code, stored natively inside the Database itself. You can pass it arguments, and it executes deep multi-step IF/ELSE transactional logic on its own.

## MERN Parallel — You Already Know This!
- Cloud Functions (AWS Lambda / Firebase Functions)
- Node.js thick controllers containing massive `await/if/try` database calculation logic
- MongoDB stored javascript functions (deprecated)

## Why does it matter?
If you need to process 1,000,000 orders at midnight to calculate affiliate payouts, pulling that data over TCP/HTTP into a Node Event Loop will crash your backend. Letting the Database execute it internally via a Procedure is instantaneous.

## How does it work?
You write a `CREATE PROCEDURE` block containing parameters `IN` and `OUT` and internal SQL state logic. Inside your Express code, you simply execute `CALL procedure_name(?)`.

## Visual Diagram
```ascii
Standard Controller Logic     vs      Stored Procedure Logic
Express Node                          Express Node
   | [Req DB array]                      | ["CALL pay_affiliates()"]
   v                                     v
   [Wait 5s]                             [Done in 0.1s]
   v                                     
   [For loop.. if/else..]             MySQL Hardware
   v                                  [Loop, Check, Update, Insert securely inside RAM.]
   [Send DB Update list]
```

## Syntax
```sql
-- Fully commented SQL syntax
DELIMITER //

CREATE PROCEDURE AddUser(IN p_name VARCHAR(50), OUT p_id INT)
BEGIN
  -- We can use standard IF/ELSE and variable declaration logic here!
  INSERT INTO users (name) VALUES (p_name);
  SET p_id = LAST_INSERT_ID();
END //

DELIMITER ;

-- Execution
CALL AddUser('Alice', @outID);
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
// Logic usually implemented as static methods on models.
userSchema.statics.archiveOldAccounts = async function() {
  const users = await this.find({ is_active: false });
  // heavy loop... saving...
};

// SQL
-- CREATE PROCEDURE archive_old_accounts() BEGIN ... END;

// Node.js using mysql2/promise (REQUIRED)
const [rows] = await pool.query('CALL archive_old_accounts()');

// ORM Equivalent (IMPORTANT)
// Prisma
// Does not natively support defining procedures. Just queries them via $executeRaw.
await prisma.$executeRaw`CALL archive_old_accounts()`;
```

### Raw SQL vs ORM
- **Raw SQL:** Perfect environment to execute procedures since it accepts raw `CALL` syntax.
- **ORM:** ORMs actively discourage logic living inside the database. They prefer "Thick Controllers" inside API code logic for Git-trackable maintenance.

### Real-World Scenario + Full Stack Code
**Scenario:** Admin panel running massive heavy nightly cleanup routines over clicking a single button.

```sql
-- SQL query (Ran ONCE on DB setup)
-- Creates procedure to wipe old orders and log it
CREATE PROCEDURE ArchiveOrders(IN cutoff_days INT)
BEGIN
    INSERT INTO archived_logs (task, amount)
    SELECT 'orders_wiped', COUNT(*) FROM orders WHERE created_at < NOW() - INTERVAL cutoff_days DAY;
    
    DELETE FROM orders WHERE created_at < NOW() - INTERVAL cutoff_days DAY;
END;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.post('/api/admin/run-archive', async (req, res) => {
  const cutoff = parseInt(req.body.days) || 30; // Clean older than 30 days
  try {
    // Calling the function natively on the DB hardware
    await pool.query('CALL ArchiveOrders(?)', [cutoff]);
    res.json({ success: true, msg: "Database cleanup triggered." });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
function ArchiveBtn() {
  return <button onClick={() => axios.post('/api/admin/run-archive', { days: 60 })}>Wipe Old Data</button>
}
```

**Output:**
```json
{
  "success": true,
  "msg": "Database cleanup triggered."
}
```

## Impact
Stored procedures cannot be easily tracked by Git (unless via strictly disciplined migration scripts). They fragment your business logic: half lives in Node Express Controllers, half lives black-boxed inside MySQL memory. Debugging becomes very hard.

## Practice Exercises
- **Easy (SQL)**: Write a procedure `GetCount(OUT total INT)` that returns total users.
- **Medium (SQL + Node.js)**: Build an Express endpoint invoking a procedure that accepts a `customer_id` and securely resets their state.
- **Hard (Full stack)**: Create an admin React page that lists all stored procedures in the database (use `SHOW PROCEDURE STATUS`).

## Interview Q&A
1. **Core SQL:** What does `DELIMITER //` do?
   *Since procedure bodies contain lots of semicolons `;`, we must temporarily change SQL's end-command character so it doesn't break prematurely.*
2. **MERN integration:** Where does business logic belong? Express or MySQL Procedures?
   *Modern architecture favors Express (Microservices/Git control). Legacy/Fintech heavily use Procedures (Speed/Security).*
3. **SQL vs MongoDB:** Can MongoDB run procedures?
   *Historically it had server-side JS functions, but it's heavily deprecated.*
4. **Scenario-based:** We need to update 5,000,000 rows overnight.
   *Write it as a Procedure. Hook it up to a MySQL `EVENT` (Cronjob) entirely skipping Node.*
5. **Advanced/tricky:** Difference between Procedure and Function in SQL?
   *FUNCTIONS must return precisely 1 value and are used in `SELECT` statements (e.g. `UPPER(str)`). PROCEDURES run workflows via `CALL`, returning nothing or multiple result sets.*

| Previous: [15_Transactions.md](./15_Transactions.md) | Next: [17_Triggers.md](./17_Triggers.md) |
