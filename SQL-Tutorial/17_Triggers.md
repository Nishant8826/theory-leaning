# Triggers

> 📌 **File:** 17_Triggers.md | **Level:** Beginner → MERN Developer

---

## What is it?
A Trigger is database logic that automatically executes "in reaction" to an event (`INSERT`, `UPDATE`, `DELETE`) on a specific table.

## MERN Parallel — You Already Know This!
- Mongoose Middlewares
- `schema.pre('save', function...)`
- `schema.post('remove', function...)`

## Why does it matter?
Ensures bullet-proof data integrity. Example: If an admin deletes a `user`, a Trigger can automatically move them to a `deleted_users` audit log table. No Node.js Express code is ever required to remember to do this.

## How does it work?
You define `CREATE TRIGGER`, state `BEFORE` or `AFTER` an action (`UPDATE/DELETE/INSERT`) `ON table_name`. Inside, you use `NEW` and `OLD` pointers to access the row data.

## Visual Diagram
```ascii
Node App: "UPDATE products SET price = 80 WHERE id = 1"
   |
   V
MySQL:
[ BEFORE UPDATE TRIGGER fires ] -- Checks if NEW.price < 0? Rejects if true.
[ UPDATE Executes on Table ] -- Price becomes 80
[ AFTER UPDATE TRIGGER fires ] -- Logs OLD.price(100) and NEW.price(80) to PriceHistory table.
```

## Syntax
```sql
-- Fully commented SQL syntax
DELIMITER //

CREATE TRIGGER before_product_update
BEFORE UPDATE ON products
FOR EACH ROW -- Run loop for every single row hit by the query
BEGIN
  -- If new incoming price is negative, force it to 0
  IF NEW.price < 0 THEN
    SET NEW.price = 0;
  END IF;
END //

DELIMITER ;
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
productSchema.pre('save', function(next) {
  if (this.price < 0) this.price = 0;
  next();
});

// SQL
-- CREATE TRIGGER before_product_insert BEFORE INSERT ON products ...

// Node.js using mysql2/promise (REQUIRED)
// You do absolutely NOTHING in Node! The trigger automatically fires invisibly.
await pool.query('UPDATE products SET price = -5 WHERE id=1'); // DB intercepts and fixes it!

// ORM Equivalent (IMPORTANT)
// Prisma / Sequelize
// Sequelize has logical application-level hooks (`beforeUpdate`, `afterCreate`), but DB Triggers bypass the ORM completely.
```

### Raw SQL vs ORM
- **Raw SQL:** Creates physical DB-level locks that ensure NO CLIENT (not even via terminal) can insert bad data.
- **ORM:** ORM `pre-save` hooks only protect edits coming through the Node Express API.

### Real-World Scenario + Full Stack Code
**Scenario:** Maintaining a bulletproof audit history log of password changes without polluting Express routes.

```sql
-- SQL query (Setup Trigger on DB)
CREATE TRIGGER after_user_update
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
   -- If password hash changed, log it.
   IF NEW.password != OLD.password THEN
      INSERT INTO audit_logs (user_id, action) VALUES (NEW.id, 'PASSWORD_CHANGED');
   END IF;
END;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.put('/api/users/:id/password', async (req, res) => {
  const { newHash } = req.body;
  try {
    // Normal update code.
    // We NEVER explicitly write code to insert an audit log here. 
    // The Database's AFTER UPDATE trigger handles our audit logging implicitly.
    await pool.query('UPDATE users SET password = ? WHERE id = ?', [newHash, req.params.id]);
    res.json({ msg: "Password updated successfully" });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
// Normal PUT request
```

**Output:**
```json
{
  "msg": "Password updated successfully"
}
```

## Impact
Triggers run invisibly. If a junior developer tries to update an order, and a Trigger automatically deletes matching items without their knowledge, debugging takes hours because "nothing in the Node.js source code did it." Document your triggers extensively.

## Practice Exercises
- **Easy (SQL)**: Build an `AFTER DELETE` trigger that records deeply deleted user IDs into a backup table.
- **Medium (SQL + Node.js)**: Send a `DELETE` query from Express. Fetch the backup table to prove the DB moved it.
- **Hard (Full stack)**: Create an `updated_at` visual system where a row is updated in React, and the DB trigger automatically overwrites `updated_at = NOW()` internally.

## Interview Q&A
1. **Core SQL:** What are `NEW` and `OLD` records?
   *`NEW` maps to incoming data. `OLD` maps to the row's existing pre-modification data.*
2. **MERN integration:** If Mongoose `pre('save')` exists, why use MySQL Triggers?
   *If an admin opens MySQL workbench and manually updates a bad price, Mongoose isn't running to stop them. Triggers exist strictly at the metal.*
3. **SQL vs MongoDB:** Can I use `OLD` on an `INSERT` trigger?
   *No. `OLD` doesn't exist on INSERTS. `NEW` doesn't exist on DELETES.*
4. **Scenario-based:** We need `updated_at` to auto-bump to the current time on edit.
   *Write a `BEFORE UPDATE` trigger setting `NEW.updated_at = CURRENT_TIMESTAMP()`.*
5. **Advanced/tricky:** Can a trigger update the very table it activated on? (Mutating table error?)
   *Usually NO. E.g., An update on Products triggering a `SELECT/UPDATE` on that same Products table creates infinite loop recursive locks.*

| Previous: [16_Stored_Procedures.md](./16_Stored_Procedures.md) | Next: [18_Normalization.md](./18_Normalization.md) |
