# Indexes

> 📌 **File:** 14_Indexes.md | **Level:** Beginner → MERN Developer

---

## What is it?
Indexes are hidden B-Tree data structures built on specific columns to drastically accelerate search `WHERE` lookup speeds, from O(n) table scans to O(log n) tree traversals.

## MERN Parallel — You Already Know This!
- Mongoose `index: true` → `CREATE INDEX`
- Mongoose `{ email: 1 }` → `CREATE INDEX idx_email ON users(email)`
- Required indexing for fast `Model.find({ email: 'bob@me' })`

## Why does it matter?
If you have 10,000,000 users and you run `WHERE email='bob@me'`, an unindexed database sequentially reads every single row until it finds Bob. Your CPU hits 100%, and the Node API times out. Indexes make lookup nearly instant.

## How does it work?
You manually create an index pointing to a particular column. The database automatically maintains a separate sorted physical b-tree map for that column pointing directly to the real row memory offsets.

## Visual Diagram
```ascii
Without Index (Full Table Scan)
[Row1..Row2............................Row 1,000,000 (Found! Time: 2sec) ]

With Index (Binary Tree)
Is it > M?  -> right
Is it > S?  -> right
Is it < W?  -> left
[Found in 3 steps! Time: 0.001sec]
```

## Syntax
```sql
-- Fully commented SQL syntax
-- PRIMARY KEYs are automatically indexed!
CREATE INDEX idx_user_email ON users(email);

-- Composite Index (For multi-where checks)
CREATE INDEX idx_category_price ON products(category, price);

-- Unique index
CREATE UNIQUE INDEX idx_user_username ON users(username);
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
const schema = new Schema({ email: { type: String, unique: true, index: true } });

// SQL
-- ALTER TABLE users ADD UNIQUE INDEX idx_email (email);

// Node.js using mysql2/promise (REQUIRED)
// Note: Indexes are infrastructure. Usually you don't run them in runtime code.
await pool.query('CREATE INDEX idx_price ON products(price)');

// ORM Equivalent (IMPORTANT)
// Prisma
model User {
  email String @unique
  @@index([email])
}
```

### Raw SQL vs ORM
- **Raw SQL:** Using `EXPLAIN SELECT ...` helps you physically evaluate whether the DB optimized the query plan using the index.
- **ORM:** ORM documentation typically uses basic schema decorations to build them during migration syncs automatically.

### Real-World Scenario + Full Stack Code
**Scenario:** A high-traffic REST API endpoint logging in users. If `email` checking scans linearly, the auth server dies under DDOS easily. Primary Keys (`id`) are auto-indexed, but custom columns (`email`) are not.

```sql
-- SQL query
EXPLAIN SELECT id, hash FROM users WHERE email = ?;
-- The EXPLAIN checks if it used the tree or did a full table scan
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
// Ensure `CREATE INDEX idx_email ON users(email);` ran once during setup.

app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;

  try {
    // Thanks to the index, this lookup is O(log n)
    const [rows] = await pool.query('SELECT id, password FROM users WHERE email = ?', [email]);
    if (rows.length === 0) return res.status(401).send('No user');

    res.json({ success: true /* password compare logic */ });
  } catch(e) {
    res.status(500).send('Error');
  }
});

// React component using Axios
// Normal fetch code.. 
axios.post('/api/login', { email: 'x', password: 'y' });
```

**Output:**
```json
{
  "success": true
}
```

## Impact
Indexes massively SPEED UP `READS` (SELECT) but SLOW DOWN `WRITES` (INSERT/UPDATE). For every INSERT, the Database must re-balance and physically update the B-Tree graph. Do not index every column. Only index columns heavily used in `WHERE`, `JOIN`, or `ORDER BY` operations.

## Practice Exercises
- **Easy (SQL)**: Create an index on the `category` column in products.
- **Medium (SQL + Node.js)**: Send `EXPLAIN SELECT...` query and `console.log()` the rows in Node to view query efficiency structures. 
- **Hard (Full stack)**: Build a setup endpoint that seeds 10,000 rows, tests a read speed via `console.time()`, adds an index, and tests read speed again showing difference.

## Interview Q&A
1. **Core SQL:** What data structure backs standard indexes?
   *B-Trees (Balanced Trees).*
2. **MERN integration:** If Mongoose handles indexes, why care in MySQL?
   *You design indexes in Mongoose models. In relational logic, it's manually crafted via SQL commands based exactly on expected app bottlenecks.*
3. **SQL vs MongoDB:** Can I run a text-search on a normal index?
   *A normal B-Tree index speeds up strict equality `='word'` or prefix `LIKE 'word%'`. It FAILS for `LIKE '%word%'`. You need explicitly a `FULLTEXT INDEX`.*
4. **Scenario-based:** We indexed price, but `WHERE price + 5 > 10` is slow.
   *Indexes become ignored if wrapped in mathematical functions dynamically. Query MUST be written `WHERE price > 5` linearly.*
5. **Advanced/tricky:** What is a covering index?
   *When all requested SELECT columns exist intimately inside the Index tree itself, the DB never fetches the physical table row at all! Insanely fast.*

| Previous: [13_Views.md](./13_Views.md) | Next: [15_Transactions.md](./15_Transactions.md) |
