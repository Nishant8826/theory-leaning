# Insert, Update & Delete

> 📌 **File:** `05_Insert_Update_Delete.md` | **Level:** Beginner → MERN Developer

---

## What is it?

INSERT, UPDATE, and DELETE are DML (Data Manipulation Language) commands — they modify the data inside tables. These are the SQL equivalent of Mongoose's `.save()`, `.updateOne()`, and `.deleteOne()` methods.

- **INSERT** — Add new rows to a table (like `Model.create()` or `.save()`)
- **UPDATE** — Modify existing rows (like `Model.updateOne()` or `.findByIdAndUpdate()`)
- **DELETE** — Remove rows from a table (like `Model.deleteOne()` or `.findByIdAndDelete()`)

---

## MERN Parallel — You Already Know This!

| Mongoose (You Know)                                 | MySQL (You'll Learn)                                |
|-----------------------------------------------------|-----------------------------------------------------|
| `Model.create({ name: 'Ali' })`                    | `INSERT INTO users (name) VALUES ('Ali')`           |
| `new Model({...}).save()`                           | Same INSERT                                         |
| `Model.insertMany([{...}, {...}])`                  | `INSERT INTO users (...) VALUES (...), (...)`       |
| `Model.updateOne({ _id: id }, { $set: {...} })`    | `UPDATE users SET name='Ali' WHERE id=1`            |
| `Model.updateMany({ city: 'Delhi' }, {...})`        | `UPDATE users SET ... WHERE city='Delhi'`           |
| `Model.findByIdAndUpdate(id, {...})`                | `UPDATE ... WHERE id=?` + `SELECT ... WHERE id=?`  |
| `Model.deleteOne({ _id: id })`                     | `DELETE FROM users WHERE id = 1`                    |
| `Model.deleteMany({ age: { $lt: 18 } })`           | `DELETE FROM users WHERE age < 18`                  |
| `result.nModified`                                  | `result.affectedRows`                               |
| `result.insertedId`                                 | `result.insertId`                                   |

---

## Why does it matter?

- INSERT, UPDATE, DELETE are the bread and butter of any CRUD application
- Every REST API endpoint maps to one of these operations
- Wrong UPDATE/DELETE without WHERE clause = data disaster
- Understanding `affectedRows` and `insertId` is essential for API responses
- Parameterized queries here prevent SQL injection attacks

---

## How does it work?

### CRUD Mapping: REST → SQL

```
HTTP Method    REST Route              Mongoose              SQL
──────────── ─────────────────── ──────────────────── ──────────────────────
POST         /api/users           User.create()        INSERT INTO users ...
GET          /api/users           User.find()          SELECT * FROM users
GET          /api/users/:id       User.findById()      SELECT * WHERE id = ?
PUT/PATCH    /api/users/:id       User.updateOne()     UPDATE users SET ... WHERE id = ?
DELETE       /api/users/:id       User.deleteOne()     DELETE FROM users WHERE id = ?
```

---

## Visual Diagram

### INSERT Flow

```
Before INSERT:
┌────┬────────┬──────────────┐
│ id │ name   │ email        │
├────┼────────┼──────────────┤
│ 1  │Nishant │ n@test.com   │
│ 2  │ Priya  │ p@test.com   │
└────┴────────┴──────────────┘

INSERT INTO customers (name, email) VALUES ('Rahul', 'r@test.com');

After INSERT:
┌────┬────────┬──────────────┐
│ id │ name   │ email        │
├────┼────────┼──────────────┤
│ 1  │Nishant │ n@test.com   │
│ 2  │ Priya  │ p@test.com   │
│ 3  │ Rahul  │ r@test.com   │  ← New row (id auto-generated)
└────┴────────┴──────────────┘
```

### UPDATE Flow

```
Before UPDATE:
┌────┬────────┬──────────────┐
│ id │ name   │ email        │
├────┼────────┼──────────────┤
│ 1  │Nishant │ n@test.com   │
│ 2  │ Priya  │ p@test.com   │
│ 3  │ Rahul  │ r@test.com   │
└────┴────────┴──────────────┘

UPDATE customers SET email = 'nishant@gmail.com' WHERE id = 1;

After UPDATE:
┌────┬────────┬──────────────────┐
│ id │ name   │ email            │
├────┼────────┼──────────────────┤
│ 1  │Nishant │ nishant@gmail.com│  ← Only this row changed
│ 2  │ Priya  │ p@test.com       │
│ 3  │ Rahul  │ r@test.com       │
└────┴────────┴──────────────────┘
```

### DELETE Flow

```
Before DELETE:
┌────┬────────┬──────────────┐
│ id │ name   │ email        │
├────┼────────┼──────────────┤
│ 1  │Nishant │ n@test.com   │
│ 2  │ Priya  │ p@test.com   │
│ 3  │ Rahul  │ r@test.com   │
└────┴────────┴──────────────┘

DELETE FROM customers WHERE id = 2;

After DELETE:
┌────┬────────┬──────────────┐
│ id │ name   │ email        │
├────┼────────┼──────────────┤
│ 1  │Nishant │ n@test.com   │
│ 3  │ Rahul  │ r@test.com   │  ← id 2 is GONE (not reassigned!)
└────┴────────┴──────────────┘
```

---

## Syntax

```sql
-- ============================================
-- INSERT — Adding New Rows
-- ============================================

-- Insert a single row
INSERT INTO customers (name, email, phone)
VALUES ('Nishant', 'n@test.com', '9876543210');

-- Insert with all columns (order must match table definition)
INSERT INTO customers
VALUES (NULL, 'Priya', 'p@test.com', '9876543211', NOW());
-- NULL for auto_increment id

-- Insert multiple rows at once (like insertMany)
INSERT INTO customers (name, email, phone) VALUES
  ('Rahul', 'r@test.com', '9876543212'),
  ('Sneha', 's@test.com', '9876543213'),
  ('Amit', 'a@test.com', '9876543214');

-- Insert with SELECT (copy from another table)
INSERT INTO vip_customers (name, email)
SELECT name, email FROM customers WHERE loyalty_points > 1000;

-- INSERT IGNORE — Skip rows that violate constraints (like upsert)
INSERT IGNORE INTO customers (name, email) VALUES ('Nishant', 'n@test.com');
-- If email already exists → silently skips instead of error

-- INSERT ... ON DUPLICATE KEY UPDATE (upsert)
INSERT INTO products (name, price, stock)
VALUES ('iPhone 15', 79999, 50)
ON DUPLICATE KEY UPDATE stock = stock + 50;


-- ============================================
-- UPDATE — Modifying Existing Rows
-- ============================================

-- Update specific row
UPDATE customers SET email = 'nishant@gmail.com' WHERE id = 1;

-- Update multiple columns
UPDATE customers
SET name = 'Nishant Kumar', phone = '9999999999', loyalty_points = 200
WHERE id = 1;

-- Update with calculation
UPDATE products SET price = price * 0.9 WHERE category_id = 1;  -- 10% discount
UPDATE products SET stock = stock - 1 WHERE id = 5;              -- Reduce stock

-- Update multiple rows (like updateMany)
UPDATE orders SET status = 'cancelled' WHERE status = 'pending' AND order_date < '2024-01-01';

-- ⚠️ UPDATE without WHERE — Updates ALL ROWS!
UPDATE products SET price = 0;  -- DANGER: All products are now free!


-- ============================================
-- DELETE — Removing Rows
-- ============================================

-- Delete specific row
DELETE FROM customers WHERE id = 3;

-- Delete with condition
DELETE FROM orders WHERE status = 'cancelled';

-- Delete rows older than 30 days
DELETE FROM logs WHERE created_at < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- ⚠️ DELETE without WHERE — Deletes ALL ROWS!
DELETE FROM customers;  -- DANGER: All customers gone!

-- TRUNCATE vs DELETE (both remove all rows)
TRUNCATE TABLE logs;    -- Faster, resets auto_increment, can't rollback
DELETE FROM logs;       -- Slower, keeps auto_increment, can rollback
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Mongoose (What You Know) ==========

// INSERT
const customer = await Customer.create({
  name: 'Nishant',
  email: 'n@test.com',
  phone: '9876543210'
});
console.log(customer._id); // ObjectId

// UPDATE
const result = await Customer.updateOne(
  { _id: id },
  { $set: { email: 'new@test.com' } }
);
console.log(result.modifiedCount); // 1

// DELETE
const result = await Customer.deleteOne({ _id: id });
console.log(result.deletedCount); // 1
```

```sql
-- ========== MySQL (SQL) ==========

-- INSERT
INSERT INTO customers (name, email, phone)
VALUES ('Nishant', 'n@test.com', '9876543210');
-- Returns: insertId

-- UPDATE
UPDATE customers SET email = 'new@test.com' WHERE id = 1;
-- Returns: affectedRows, changedRows

-- DELETE
DELETE FROM customers WHERE id = 1;
-- Returns: affectedRows
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// INSERT
const [result] = await pool.query(
  'INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)',
  ['Nishant', 'n@test.com', '9876543210']
);
console.log(result.insertId);      // 1 (auto-generated ID)
console.log(result.affectedRows);  // 1

// UPDATE
const [result] = await pool.query(
  'UPDATE customers SET email = ? WHERE id = ?',
  ['new@test.com', 1]
);
console.log(result.affectedRows);  // 1 (rows matched)
console.log(result.changedRows);   // 1 (rows actually changed)

// DELETE
const [result] = await pool.query(
  'DELETE FROM customers WHERE id = ?',
  [1]
);
console.log(result.affectedRows);  // 1

// INSERT MANY (multiple rows)
const customers = [
  ['Rahul', 'r@test.com', '1111111111'],
  ['Sneha', 's@test.com', '2222222222'],
  ['Amit', 'a@test.com', '3333333333']
];
const [result] = await pool.query(
  'INSERT INTO customers (name, email, phone) VALUES ?',
  [customers]  // Note: double array wrapping
);
console.log(result.affectedRows); // 3
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize (Like Mongoose) ==========

// INSERT — create
const customer = await Customer.create({
  name: 'Nishant',
  email: 'n@test.com',
  phone: '9876543210'
});
// Generated SQL: INSERT INTO customers (name,email,phone,created_at,updated_at)
//                VALUES ('Nishant','n@test.com','9876543210',NOW(),NOW())

// INSERT MANY — bulkCreate
await Customer.bulkCreate([
  { name: 'Rahul', email: 'r@test.com' },
  { name: 'Sneha', email: 's@test.com' }
]);

// UPDATE — update
const [affectedCount] = await Customer.update(
  { email: 'new@test.com' },        // What to change ($set equivalent)
  { where: { id: 1 } }              // Which rows
);
// Generated SQL: UPDATE customers SET email='new@test.com' WHERE id=1

// DELETE — destroy
const deletedCount = await Customer.destroy({
  where: { id: 1 }
});
// Generated SQL: DELETE FROM customers WHERE id=1

// UPSERT — upsert
await Customer.upsert({
  email: 'n@test.com',  // unique key
  name: 'Nishant Updated',
  phone: '9999999999'
});
// Generated SQL: INSERT ... ON DUPLICATE KEY UPDATE
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Complete CRUD API for products

```sql
-- Seed data for products
INSERT INTO categories (name, description) VALUES
  ('Electronics', 'Electronic devices and gadgets'),
  ('Clothing', 'Fashion and apparel'),
  ('Books', 'Books and literature');

INSERT INTO products (name, description, price, stock, category_id, status) VALUES
  ('iPhone 15', '128GB, Black', 79999.00, 50, 1, 'published'),
  ('MacBook Air M3', '8GB RAM, 256GB SSD', 114900.00, 30, 1, 'published'),
  ('Levi''s Jeans', 'Blue denim, slim fit', 2499.00, 200, 2, 'published'),
  ('The Alchemist', 'By Paulo Coelho', 299.00, 500, 3, 'published'),
  ('AirPods Pro', 'Active Noise Cancellation', 24900.00, 100, 1, 'draft');
```

```js
// Node.js + Express — Full CRUD API for products
const express = require('express');
const pool = require('./db');
const router = express.Router();

// ==========================================
// CREATE — POST /api/products
// ==========================================
router.post('/', async (req, res) => {
  try {
    const { name, description, price, stock, categoryId, status } = req.body;
    
    // Validate required fields
    if (!name || !price) {
      return res.status(400).json({ error: 'Name and price are required' });
    }
    
    const [result] = await pool.query(
      `INSERT INTO products (name, description, price, stock, category_id, status)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [name, description || null, price, stock || 0, categoryId || null, status || 'draft']
    );
    
    // Fetch the created product (like Mongoose's { new: true })
    const [rows] = await pool.query('SELECT * FROM products WHERE id = ?', [result.insertId]);
    
    res.status(201).json({
      message: 'Product created',
      product: rows[0]
    });
  } catch (error) {
    if (error.code === 'ER_DUP_ENTRY') {
      return res.status(409).json({ error: 'Product already exists' });
    }
    res.status(500).json({ error: error.message });
  }
});

// ==========================================
// READ — GET /api/products
// ==========================================
router.get('/', async (req, res) => {
  try {
    const [products] = await pool.query(`
      SELECT p.*, c.name AS category_name
      FROM products p
      LEFT JOIN categories c ON p.category_id = c.id
      ORDER BY p.created_at DESC
    `);
    
    res.json({ count: products.length, products });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==========================================
// READ ONE — GET /api/products/:id
// ==========================================
router.get('/:id', async (req, res) => {
  try {
    const [rows] = await pool.query(
      `SELECT p.*, c.name AS category_name
       FROM products p
       LEFT JOIN categories c ON p.category_id = c.id
       WHERE p.id = ?`,
      [req.params.id]
    );
    
    if (rows.length === 0) {
      return res.status(404).json({ error: 'Product not found' });
    }
    
    res.json(rows[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==========================================
// UPDATE — PUT /api/products/:id
// ==========================================
router.put('/:id', async (req, res) => {
  try {
    const { name, description, price, stock, categoryId, status } = req.body;
    
    const [result] = await pool.query(
      `UPDATE products
       SET name = ?, description = ?, price = ?, stock = ?, category_id = ?, status = ?
       WHERE id = ?`,
      [name, description, price, stock, categoryId, status, req.params.id]
    );
    
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: 'Product not found' });
    }
    
    // Fetch updated product
    const [rows] = await pool.query('SELECT * FROM products WHERE id = ?', [req.params.id]);
    
    res.json({
      message: 'Product updated',
      product: rows[0]
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==========================================
// DELETE — DELETE /api/products/:id
// ==========================================
router.delete('/:id', async (req, res) => {
  try {
    // Check if product exists first
    const [rows] = await pool.query('SELECT * FROM products WHERE id = ?', [req.params.id]);
    
    if (rows.length === 0) {
      return res.status(404).json({ error: 'Product not found' });
    }
    
    await pool.query('DELETE FROM products WHERE id = ?', [req.params.id]);
    
    res.json({
      message: 'Product deleted',
      product: rows[0]
    });
  } catch (error) {
    // Foreign key constraint violation
    if (error.code === 'ER_ROW_IS_REFERENCED_2') {
      return res.status(409).json({ 
        error: 'Cannot delete product. It has associated order items.' 
      });
    }
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
```

```js
// React — Product Management Component
import { useState, useEffect } from 'react';
import axios from 'axios';

function ProductManager() {
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ name: '', price: '', stock: '' });
  const [editId, setEditId] = useState(null);

  const fetchProducts = async () => {
    const { data } = await axios.get('/api/products');
    setProducts(data.products);
  };

  useEffect(() => { fetchProducts(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editId) {
        await axios.put(`/api/products/${editId}`, form);
      } else {
        await axios.post('/api/products', form);
      }
      setForm({ name: '', price: '', stock: '' });
      setEditId(null);
      fetchProducts();
    } catch (error) {
      alert(error.response?.data?.error || 'Operation failed');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this product?')) return;
    try {
      await axios.delete(`/api/products/${id}`);
      fetchProducts();
    } catch (error) {
      alert(error.response?.data?.error || 'Delete failed');
    }
  };

  const handleEdit = (product) => {
    setForm({ name: product.name, price: product.price, stock: product.stock });
    setEditId(product.id);
  };

  return (
    <div>
      <h2>Product Manager</h2>
      
      <form onSubmit={handleSubmit}>
        <input placeholder="Name" value={form.name}
          onChange={e => setForm({...form, name: e.target.value})} />
        <input type="number" placeholder="Price" value={form.price}
          onChange={e => setForm({...form, price: e.target.value})} />
        <input type="number" placeholder="Stock" value={form.stock}
          onChange={e => setForm({...form, stock: e.target.value})} />
        <button type="submit">{editId ? 'Update' : 'Create'}</button>
        {editId && <button type="button" onClick={() => setEditId(null)}>Cancel</button>}
      </form>

      <table>
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Price</th><th>Stock</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map(p => (
            <tr key={p.id}>
              <td>{p.id}</td>
              <td>{p.name}</td>
              <td>₹{p.price}</td>
              <td>{p.stock}</td>
              <td>
                <button onClick={() => handleEdit(p)}>Edit</button>
                <button onClick={() => handleDelete(p.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

**Output (POST /api/products):**
```json
{
  "message": "Product created",
  "product": {
    "id": 6,
    "name": "Samsung Galaxy S24",
    "description": "256GB, Phantom Black",
    "price": "69999.00",
    "stock": 75,
    "category_id": 1,
    "status": "draft",
    "created_at": "2024-01-15T10:30:00.000Z",
    "updated_at": "2024-01-15T10:30:00.000Z"
  }
}
```

---

## Impact

| If You Don't Understand This...         | What Happens                                    |
|-----------------------------------------|-------------------------------------------------|
| UPDATE without WHERE clause             | ALL rows are updated — every product's price is now 0 |
| DELETE without WHERE clause             | ALL rows are deleted — entire table emptied      |
| Don't check `affectedRows`             | Silent failures — user thinks delete worked but it didn't |
| Don't use parameterized queries         | SQL injection: `'; DROP TABLE users; --`         |
| Don't handle duplicate key errors       | App crashes on duplicate email/username           |
| INSERT without specifying columns       | Columns shift if table is altered later           |
| Forget foreign key constraints          | Delete parent row → orphaned children             |

### The Deadliest Mistake in SQL

```sql
-- ⚠️ These are the most dangerous SQL statements:

UPDATE products SET price = 0;      -- Forgot WHERE → all products free!
DELETE FROM orders;                  -- Forgot WHERE → all orders gone!

-- ALWAYS add WHERE first, then write the rest:
-- Step 1: SELECT first to preview affected rows
SELECT * FROM products WHERE category_id = 3;

-- Step 2: If results look right, change SELECT to UPDATE/DELETE
UPDATE products SET price = 0 WHERE category_id = 3;

-- Pro tip: Use LIMIT as a safety net
DELETE FROM orders WHERE status = 'cancelled' LIMIT 100;
-- Deletes at most 100 rows — prevents catastrophic mistakes
```

---

## Practice Exercises

### Easy (SQL)
1. Insert 5 customers into the customers table
2. Update customer with id=3 to change their email
3. Delete customer with id=5
4. Insert a product with NULL description (optional field)

### Medium (SQL + Node.js)
5. Build a complete CRUD API for customers with:
   - POST /api/customers (create)
   - GET /api/customers (list all)
   - GET /api/customers/:id (get one)
   - PUT /api/customers/:id (update)
   - DELETE /api/customers/:id (delete)
6. Add input validation to the POST route (check email format, required fields)
7. Handle the `ER_DUP_ENTRY` error and return a user-friendly message

### Hard (Full Stack)
8. Build a product management dashboard:
   - React form for creating/editing products
   - Table showing all products with Edit/Delete buttons
   - Confirmation dialog before delete
   - Toast notifications for success/error
   - Real-time stock update (decrease stock on order)
9. Implement soft delete: Instead of actually deleting rows, add a `deleted_at` column and set it on delete. Modify all queries to exclude soft-deleted rows.

---

## Real-World Q&A

**Q1:** In MongoDB, `updateOne()` returns `modifiedCount`. What's the MySQL equivalent?
**A:** MySQL's `pool.query('UPDATE...')` returns a result object with `affectedRows` (rows that matched the WHERE clause) and `changedRows` (rows where data actually changed). The difference matters: if you UPDATE a row setting name='Ali' but it was already 'Ali', `affectedRows = 1` but `changedRows = 0`.

**Q2:** How do I do an "upsert" in MySQL (insert if not exists, update if exists)?
**A:** Use `INSERT ... ON DUPLICATE KEY UPDATE`: 
```sql
INSERT INTO products (name, price) VALUES ('iPhone', 79999)
ON DUPLICATE KEY UPDATE price = 79999;
```
This requires a UNIQUE constraint on the column being checked. In Mongoose, this is like `Model.findOneAndUpdate({...}, {...}, { upsert: true })`.

**Q3:** What happens to AUTO_INCREMENT id when I delete a row?
**A:** The ID is NOT reused. If you insert ids 1,2,3 and delete id=2, the next insert will be id=4, not id=2. This is by design — IDs should be permanently unique. If you TRUNCATE the table, AUTO_INCREMENT resets to 1.

---

## Interview Q&A

**Q1: What is the difference between DELETE and TRUNCATE?**
DELETE removes specific rows (or all if no WHERE), logs each deletion, can be rolled back, fires triggers, and doesn't reset AUTO_INCREMENT. TRUNCATE removes all rows instantly, can't be rolled back, doesn't fire triggers, and resets AUTO_INCREMENT. TRUNCATE is DDL (structural), DELETE is DML (data).

**Q2: How do you prevent SQL injection in INSERT/UPDATE/DELETE?**
Always use parameterized queries (prepared statements). In mysql2: `pool.query('INSERT INTO users (name) VALUES (?)', [userInput])`. The `?` placeholder ensures user input is never executed as SQL. Never concatenate user input into SQL strings: `'INSERT INTO users (name) VALUES ("' + userInput + '")'` is dangerous.

**Q3: What is the difference between `affectedRows` and `changedRows`?**
`affectedRows` counts rows that matched the WHERE clause. `changedRows` counts rows where the data actually changed. Example: `UPDATE users SET name='Ali' WHERE id=1` — if user 1's name was already 'Ali', `affectedRows=1, changedRows=0`. If name was 'Bob', both are 1.

**Q4: How would you implement a "soft delete" in MySQL?**
Add a `deleted_at TIMESTAMP NULL DEFAULT NULL` column. Instead of DELETE, run UPDATE: `UPDATE users SET deleted_at = NOW() WHERE id = ?`. All SELECT queries add `WHERE deleted_at IS NULL`. Create a view for convenience: `CREATE VIEW active_users AS SELECT * FROM users WHERE deleted_at IS NULL`. To permanently delete: run actual DELETE later.

**Q5: A user calls your API to delete their account, but they have orders. What happens?**
If there's a FOREIGN KEY constraint on `orders.customer_id → customers.id`, the delete fails with `ER_ROW_IS_REFERENCED_2`. Solutions depend on business logic: (1) `ON DELETE CASCADE` — delete customer AND their orders (usually bad). (2) `ON DELETE SET NULL` — keep orders but set customer_id to NULL. (3) Soft delete — mark customer as deleted but keep data. (4) Delete orders first, then customer. Best practice: soft delete + data anonymization (GDPR compliance).

---

| [← Previous: Create, Drop & Alter](./04_Create_Drop_Alter.md) | [Next: SELECT Basics →](./06_Select_Basics.md) |
|---|---|
