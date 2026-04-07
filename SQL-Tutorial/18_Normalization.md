# Normalization

> 📌 **File:** 18_Normalization.md | **Level:** Beginner → MERN Developer

---

## What is it?
Normalization is the fundamental architectural philosophy of SQL. You break data down into tiny interconnected tables to utterly destroy data duplication (redundancy).

## MERN Parallel — You Already Know This!
- MongoDB Embedded Array of `{ addresses }` → **DE-NORMALIZED** (NoSQL way)
- Splitting collections and using `populate()` → **NORMALIZATION** (SQL way)
- DRY code (Don't Repeat Yourself) principle applied to database rows.

## Why does it matter?
If John's email is stored in an `Orders` table 50 times alongside his 50 orders, updating his email requires 50 updates. If you use Normalization (foreign key `user_id`), his email exists strictly ONCE in the `Users` table. Changing it updates the whole system implicitly.

## How does it work?
Follow the "Normal Forms" (1NF, 2NF, 3NF):
1. **1NF:** Each column holds ONE value (No comma separated arrays `tags: "cool, new"`).
2. **2NF:** Remove partial dependencies. Use Primary Keys.
3. **3NF:** "Every column must depend on the primary key, the whole primary key, and nothing but the primary key". No calculated fields.

## Visual Diagram
```ascii
BAD (Denormalized MERN Array Style)
Table: Orders
id | user_name | user_email | items
1  | Bob       | b@m.com    | Hat, Shoe
2  | Bob       | b@m.com    | Socks

GOOD (3NF Normalized SQL Style)
Table Users        Table Orders        Table Order_Items
id | name | email  id | user_id        order_id | item
1  | Bob  | b@m.   1  | 1              1        | Hat
                   2  | 1              1        | Shoe
                                       2        | Socks
```

## Syntax
```sql
-- Fully commented SQL syntax
-- Setting up normalized keys
CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose (Often embraces Denormalization)
new Schema({ 
  user: { name: String, email: String }, // duplicates info!
  items: [ { name: String } ] 
});

// SQL (Forces explicit structural integrity)
-- CREATE TABLE order_items ( order_id INT, product_id INT ... Foreign keys linked );

// Node.js using mysql2/promise (REQUIRED)
// Node must handle building data natively over multiple INSERTs
await pool.query('INSERT INTO orders (user_id) VALUES (?)', [uId]);
await pool.query('INSERT INTO order_items (order_id, product_id) VALUES (?, ?)', [oId, pId]);

// ORM Equivalent (IMPORTANT)
// Prisma provides incredibly clean nested creates bridging the gap!
await prisma.order.create({ data: { userId: 1, items: { create: [{ productId: 5 }] } } });
```

### Raw SQL vs ORM
- **Raw SQL:** Requires deep Transactional logic to properly map relational ids dynamically upon normalized insertions.
- **ORM:** ORMs were built entirely to hide the pain of writing multi-table Normalized `INSERT` chains.

### Real-World Scenario + Full Stack Code
**Scenario:** Deleting a user causes all their orders to cleanly wipe implicitly via `ON DELETE CASCADE`.

```sql
-- SQL query
-- Normalization rule: Child tables reference parents.
ALTER TABLE orders 
ADD CONSTRAINT fk_user 
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
// If our database is cleanly normalized with Cascading Foreign Keys:
app.delete('/api/users/:id', async (req, res) => {
  try {
    // Because of Normalize FK rules, deleting the user physically 
    // erases all their orders, items, and carts instantly automatically.
    await pool.query('DELETE FROM users WHERE id = ?', [req.params.id]);
    res.json({ msg: "User completely expunged based on relational keys." });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
function ClearAccountButton({id}) {
  return <button onClick={() => axios.delete(`/api/users/${id}`)}>Cancel My Account</button>
}
```

**Output:**
```json
{
  "msg": "User completely expunged based on relational keys."
}
```

## Impact
Over-normalization causes "Join Hell". If retrieving a user profile requires 12 `JOIN`s scaling across 12 hyper-fragmented tables, reads become incredibly slow. Balance structure with performance.

## Practice Exercises
- **Easy (SQL)**: Identify the 1NF violation in: `categories = "shoes, hats, boots"`.
- **Medium (SQL + Node.js)**: Build the SQL definitions separating an `authors` table with a `books` table using Foreign keys.
- **Hard (Full stack)**: Create a Many-to-Many architecture schema for `students` and `classes` using a junction table `student_classes`. Route an API to fetch a student's schedule explicitly via JOIN.

## Interview Q&A
1. **Core SQL:** What is the rule of 3NF intuitively?
   *Columns must belong directly to the primary key. If a table `orders` has a column `user_address`, address belongs to User, not the Order ID. Rip it out.*
2. **MERN integration:** In Mongo, why is denormalization okay?
   *Reads are prioritized. Grabbing one massive JSON document is faster than piecing together IDs.*
3. **SQL vs MongoDB:** How is Many-to-Many handled?
   *MongoDB: Arrays of IDs `students: [id1, id2]`. MySQL: A normalized bridge "Junction" table containing solely `[student_id, class_id]` pairs.*
4. **Scenario-based:** We calculate "Total Revenue". Should we store `total = col A + col B`?
   *No. 3NF prohibits calculated derived values. Compute it dynamically using `SELECT` or `Views`.*
5. **Advanced/tricky:** Would you ever denormalize a SQL database intentionally?
   *Yes. Data warehousing/reporting databases severely denormalize to "Star Schemas" to optimize mathematical heavy READ speeds over WRITES.*

| Previous: [17_Triggers.md](./17_Triggers.md) | Next: [19_SQL_Vs_NoSQL.md](./19_SQL_Vs_NoSQL.md) |
