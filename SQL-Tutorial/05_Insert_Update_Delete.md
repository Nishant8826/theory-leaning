# Insert, Update, Delete

> 📌 **File:** 05_Insert_Update_Delete.md | **Level:** Beginner → MERN Developer

---

## What is it?
These are DML (Data Manipulation Language) commands. They modify the actual row data inside pre-existing tables.

## MERN Parallel — You Already Know This!
- `Model.create()`/`insertOne()` → `INSERT INTO`
- `Model.updateOne()`/`findByIdAndUpdate()` → `UPDATE SET`
- `Model.deleteOne()`/`findByIdAndDelete()` → `DELETE FROM`

## Why does it matter?
This is how CRUD functionality works. You will write these commands continuously inside your API routes.

## How does it work?
You write string queries containing placeholders `?`, and `mysql2` safely injects your dynamic variable values into real SQL.

## Visual Diagram
```ascii
[Client Data] --> Express Node --> pool.query("INSERT", [data]) --> [MySQL Row]
```

## Syntax
```sql
-- Fully commented SQL syntax
INSERT INTO products (name, price) VALUES ('Book', 15.99);

UPDATE products SET price = 12.99 WHERE id = 1;

DELETE FROM products WHERE id = 1;
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
await Product.create({ name: 'Book', price: 15.99 });
await Product.updateOne({ _id: 1 }, { price: 12.99 });
await Product.deleteOne({ _id: 1 });

// SQL
-- INSERT INTO products ...
-- UPDATE products SET ...
-- DELETE FROM products ...

// Node.js using mysql2/promise (REQUIRED)
await pool.query('INSERT INTO products (name, price) VALUES (?, ?)', ['Book', 15.99]);

// ORM Equivalent (IMPORTANT)
// Prisma
await prisma.product.create({ data: { name: 'Book', price: 15.99 }});
```

### Raw SQL vs ORM
- **Raw SQL:** Explicitly handles bulk inserts incredibly fast. Highly legible.
- **ORM:** Protects you automatically from SQL injection and parses result structures nicely.

### Real-World Scenario + Full Stack Code
**Scenario:** Submitting a new category from a React admin panel.

```sql
-- SQL query
INSERT INTO categories (name) VALUES (?);
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.post('/api/categories', async (req, res) => {
  const { name } = req.body;
  if (!name) return res.status(400).json({ error: "Missing name" });

  try {
    // Parameterized queries (?) PREVENT SQL INJECTION
    const [result] = await pool.query(
      'INSERT INTO categories (name) VALUES (?)', 
      [name]
    );
    res.json({ success: true, insertId: result.insertId });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
function AddCategory() {
  const [name, setName] = useState('');
  
  const handleSave = async () => {
    const res = await axios.post('/api/categories', { name });
    alert(`Category created with ID: ${res.data.insertId}`);
  };

  return <input onChange={e => setName(e.target.value)} onBlur={handleSave} />;
}
```

**Output:**
```json
{
  "success": true,
  "insertId": 4
}
```

## Impact
FORGETTING THE `WHERE` CLAUSE ON AN UPDATE OR DELETE WILL AFFECT THE ENTIRE TABLE. Running `UPDATE products SET price = 0;` will instantly make everything free.

## Practice Exercises
- **Easy (SQL)**: Write SQL strings to insert 2 rows, then update 1 of them.
- **Medium (SQL + Node.js)**: Build a PUT endpoint that updates a product's price based on its ID via URL param. 
- **Hard (Full stack)**: Create a React list showing items with "Approve", "Edit Price", and "Delete" buttons triggering those exact queries.

## Interview Q&A
1. **Core SQL:** What happens if `UPDATE` has no `WHERE` clause?
   *It modifies every single row in the table.*
2. **MERN integration:** How do I get the new item's ID immediately after an `INSERT` using `mysql2`?
   *The `[result]` array has an object containing `result.insertId`.*
3. **SQL vs MongoDB:** Can `INSERT` create missing columns on the fly like Mongoose?
   *No. It will throw a strict standard SQL error.*
4. **Scenario-based:** A user submits a name `John'; DROP TABLE users;--`. What happens?
   *If you use string interpolation (`${name}`), it destroys the table (SQL Injection). Using `?` parameters safely sanitizes it into text.*
5. **Advanced/tricky:** Can I insert multiple rows at once?
   *Yes, `INSERT INTO t (col) VALUES (?),(?),(?)`.*

| Previous: [04_Create_Drop_Alter.md](./04_Create_Drop_Alter.md) | Next: [06_Select_Basics.md](./06_Select_Basics.md) |
