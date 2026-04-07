# SELECT Basics

> 📌 **File:** `06_Select_Basics.md` | **Level:** Beginner → MERN Developer

---

## What is it?

SELECT is the most-used SQL command. It retrieves data from tables — the SQL equivalent of Mongoose's `.find()`, `.findOne()`, and `.select()`. Every time your React app fetches data from an API, there's a SELECT query behind it.

SELECT is part of DQL (Data Query Language) — the only command that reads data without modifying it.

---

## MERN Parallel — You Already Know This!

| Mongoose (You Know)                          | SQL SELECT (You'll Learn)                       |
|----------------------------------------------|-------------------------------------------------|
| `User.find()`                                | `SELECT * FROM users;`                          |
| `User.find().select('name email')`           | `SELECT name, email FROM users;`                |
| `User.find().select('-password')`            | `SELECT name, email, phone FROM users;` (list all except password) |
| `User.findOne({ email: 'x' })`              | `SELECT * FROM users WHERE email='x' LIMIT 1;` |
| `User.findById(id)`                          | `SELECT * FROM users WHERE id = ?;`             |
| `User.distinct('city')`                      | `SELECT DISTINCT city FROM users;`              |
| `User.countDocuments()`                      | `SELECT COUNT(*) FROM users;`                   |
| `User.find().lean()`                         | SELECT always returns plain objects              |

---

## Why does it matter?

- SELECT represents 80%+ of all database operations in most apps
- Selecting only needed columns (not `SELECT *`) improves performance significantly
- Understanding aliases, expressions, and DISTINCT prevents data redundancy
- Proper SELECT queries make your API responses clean and efficient
- Interview questions heavily test SELECT skills

---

## How does it work?

### SELECT Execution Order

```
What you WRITE:                What MySQL EXECUTES:
──────────────                 ────────────────────
SELECT columns         5th     FROM table              1st
FROM table             1st     WHERE condition          2nd
WHERE condition        2nd     GROUP BY columns         3rd
GROUP BY columns       3rd     HAVING condition         4th
HAVING condition       4th     SELECT columns           5th
ORDER BY columns       6th     ORDER BY columns         6th
LIMIT count            7th     LIMIT count              7th

The order you write SQL ≠ the order MySQL runs it!
This matters when understanding aliases and column availability.
```

---

## Visual Diagram

### SELECT * vs SELECT specific columns

```
Table: customers
┌────┬────────┬──────────────┬───────────┬────────────┐
│ id │ name   │ email        │ phone     │ created_at │
├────┼────────┼──────────────┼───────────┼────────────┤
│ 1  │Nishant │ n@test.com   │ 987654321 │ 2024-01-15 │
│ 2  │ Priya  │ p@test.com   │ 876543210 │ 2024-01-16 │
│ 3  │ Rahul  │ r@test.com   │ 765432109 │ 2024-01-17 │
└────┴────────┴──────────────┴───────────┴────────────┘

SELECT * FROM customers;           → Returns ALL 5 columns
SELECT name, email FROM customers; → Returns only 2 columns:

┌────────┬──────────────┐
│ name   │ email        │
├────────┼──────────────┤
│Nishant │ n@test.com   │
│ Priya  │ p@test.com   │
│ Rahul  │ r@test.com   │
└────────┴──────────────┘

LESS data transferred = FASTER response
```

### DISTINCT

```
Table: orders
┌────┬───────────┬──────────┐
│ id │ city      │ status   │
├────┼───────────┼──────────┤
│ 1  │ Delhi     │ pending  │
│ 2  │ Mumbai    │ shipped  │
│ 3  │ Delhi     │ shipped  │
│ 4  │ Bangalore │ pending  │
│ 5  │ Delhi     │ delivered│
└────┴───────────┴──────────┘

SELECT city FROM orders;           → Delhi, Mumbai, Delhi, Bangalore, Delhi
SELECT DISTINCT city FROM orders;  → Delhi, Mumbai, Bangalore (unique only!)
```

---

## Syntax

```sql
-- ============================================
-- BASIC SELECT
-- ============================================

-- Select all columns from a table
SELECT * FROM customers;

-- Select specific columns
SELECT name, email FROM customers;

-- Select with a calculated column
SELECT name, price, price * 0.18 AS gst FROM products;

-- Select with string functions
SELECT name, UPPER(email) AS email_upper FROM customers;



-- ============================================
-- ALIASES (AS) — Rename columns in output
-- ============================================

-- Column alias
SELECT 
  name AS customer_name,
  email AS contact_email,
  phone AS mobile
FROM customers;

-- Table alias (for shorter references in JOINs)
SELECT c.name, c.email
FROM customers AS c;

-- Calculated alias
SELECT 
  name,
  price,
  price * 1.18 AS price_with_gst,
  stock * price AS inventory_value
FROM products;

-- String alias with spaces (use quotes)
SELECT name AS "Customer Name", email AS "Email Address"
FROM customers;


-- ============================================
-- DISTINCT — Remove duplicates
-- ============================================

-- Unique cities
SELECT DISTINCT city FROM customers;

-- Unique combinations
SELECT DISTINCT city, state FROM customers;

-- Count distinct values
SELECT COUNT(DISTINCT city) AS unique_cities FROM customers;


-- ============================================
-- EXPRESSIONS AND FUNCTIONS in SELECT
-- ============================================

-- Math in SELECT
SELECT 
  name,
  price,
  stock,
  price * stock AS total_value,
  ROUND(price * 0.1, 2) AS discount_10pct
FROM products;

-- String functions
SELECT 
  CONCAT(first_name, ' ', last_name) AS full_name,
  LENGTH(email) AS email_length,
  SUBSTRING(phone, 1, 3) AS area_code
FROM customers;

-- Date functions
SELECT 
  name,
  created_at,
  DATE_FORMAT(created_at, '%d %b %Y') AS formatted_date,
  DATEDIFF(NOW(), created_at) AS days_since_joined
FROM customers;

-- Conditional (CASE — like ternary operator)
SELECT 
  name,
  price,
  CASE 
    WHEN price > 50000 THEN 'Premium'
    WHEN price > 10000 THEN 'Mid-Range'
    ELSE 'Budget'
  END AS price_category
FROM products;

-- NULL handling
SELECT 
  name,
  IFNULL(phone, 'Not Provided') AS phone,      -- Like || 'default' in JS
  COALESCE(phone, email, 'No Contact') AS contact  -- First non-null value
FROM customers;
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Mongoose / MongoDB ==========

// Select all
const users = await User.find();

// Select specific fields
const users = await User.find().select('name email');

// Select with exclusion
const users = await User.find().select('-password -__v');

// Find distinct values
const cities = await User.distinct('city');

// Count
const count = await User.countDocuments();

// Computed field (using aggregation)
const products = await Product.aggregate([
  { $project: { name: 1, price: 1, totalValue: { $multiply: ['$price', '$stock'] } } }
]);
```

```sql
-- ========== MySQL (SQL) ==========

-- Select all
SELECT * FROM users;

-- Select specific fields
SELECT name, email FROM users;

-- Select with exclusion (no shortcut — list all columns you want)
SELECT name, email, phone, created_at FROM users;

-- Find distinct values
SELECT DISTINCT city FROM users;

-- Count
SELECT COUNT(*) AS count FROM users;

-- Computed field (direct in SELECT)
SELECT name, price, price * stock AS total_value FROM products;
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Select all
const [customers] = await pool.query('SELECT * FROM customers');

// Select specific fields
const [customers] = await pool.query('SELECT name, email FROM customers');

// Select one by ID
const [rows] = await pool.query('SELECT * FROM customers WHERE id = ?', [1]);
const customer = rows[0]; // mysql2 always returns array

// Distinct values
const [cities] = await pool.query('SELECT DISTINCT city FROM customers');

// Count
const [result] = await pool.query('SELECT COUNT(*) AS total FROM customers');
const count = result[0].total;

// Computed columns
const [products] = await pool.query(`
  SELECT 
    name, 
    price, 
    stock,
    price * stock AS inventory_value,
    CASE 
      WHEN stock = 0 THEN 'Out of Stock'
      WHEN stock < 10 THEN 'Low Stock'
      ELSE 'In Stock'
    END AS stock_status
  FROM products
`);
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize ==========
const { Op, fn, col, literal } = require('sequelize');

// Select all — generates: SELECT * FROM customers;
const customers = await Customer.findAll();

// Select specific fields — generates: SELECT name, email FROM customers;
const customers = await Customer.findAll({
  attributes: ['name', 'email']
});

// Exclude fields — generates: SELECT name, email, phone FROM customers;
const customers = await Customer.findAll({
  attributes: { exclude: ['password', 'createdAt'] }
});

// Computed column
const products = await Product.findAll({
  attributes: [
    'name', 'price', 'stock',
    [literal('price * stock'), 'inventory_value']
  ]
});

// Distinct — generates: SELECT DISTINCT city FROM customers;
const cities = await Customer.findAll({
  attributes: [[fn('DISTINCT', col('city')), 'city']]
});

// Count — generates: SELECT COUNT(*) AS count FROM customers;
const count = await Customer.count();
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Product listing page with dynamic columns and computed fields

```sql
-- SQL: Product listing with all useful computed fields
SELECT 
  p.id,
  p.name,
  p.price,
  p.stock,
  c.name AS category,
  ROUND(p.price * 0.18, 2) AS gst_amount,
  ROUND(p.price * 1.18, 2) AS price_with_gst,
  p.price * p.stock AS inventory_value,
  CASE 
    WHEN p.stock = 0 THEN 'Out of Stock'
    WHEN p.stock < 10 THEN 'Low Stock'
    WHEN p.stock < 50 THEN 'In Stock'
    ELSE 'Well Stocked'
  END AS stock_status,
  DATEDIFF(NOW(), p.created_at) AS days_listed,
  p.status
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.status = 'published';
```

```js
// Node.js + Express API
app.get('/api/products/listing', async (req, res) => {
  try {
    const [products] = await pool.query(`
      SELECT 
        p.id,
        p.name,
        p.price,
        p.stock,
        c.name AS category,
        ROUND(p.price * 0.18, 2) AS gst_amount,
        ROUND(p.price * 1.18, 2) AS price_with_gst,
        p.price * p.stock AS inventory_value,
        CASE 
          WHEN p.stock = 0 THEN 'Out of Stock'
          WHEN p.stock < 10 THEN 'Low Stock'
          WHEN p.stock < 50 THEN 'In Stock'
          ELSE 'Well Stocked'
        END AS stock_status,
        DATEDIFF(NOW(), p.created_at) AS days_listed,
        p.status
      FROM products p
      LEFT JOIN categories c ON p.category_id = c.id
      WHERE p.status = 'published'
    `);
    
    res.json({
      count: products.length,
      products
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// ORM version (Sequelize)
app.get('/api/products/listing', async (req, res) => {
  const products = await Product.findAll({
    attributes: [
      'id', 'name', 'price', 'stock', 'status',
      [literal('ROUND(price * 0.18, 2)'), 'gst_amount'],
      [literal('ROUND(price * 1.18, 2)'), 'price_with_gst'],
      [literal('price * stock'), 'inventory_value'],
      [literal(`CASE 
        WHEN stock = 0 THEN 'Out of Stock'
        WHEN stock < 10 THEN 'Low Stock'
        ELSE 'In Stock'
      END`), 'stock_status']
    ],
    include: [{ model: Category, attributes: ['name'] }],
    where: { status: 'published' }
  });
  
  res.json({ count: products.length, products });
});
```

```js
// React Component
import { useState, useEffect } from 'react';
import axios from 'axios';

function ProductListing() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/products/listing')
      .then(({ data }) => setProducts(data.products))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2>Products ({products.length})</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Price</th>
            <th>GST</th>
            <th>Total</th>
            <th>Stock</th>
            <th>Status</th>
            <th>Category</th>
          </tr>
        </thead>
        <tbody>
          {products.map(p => (
            <tr key={p.id}>
              <td>{p.name}</td>
              <td>₹{p.price}</td>
              <td>₹{p.gst_amount}</td>
              <td>₹{p.price_with_gst}</td>
              <td>{p.stock}</td>
              <td style={{ 
                color: p.stock_status === 'Out of Stock' ? 'red' : 
                       p.stock_status === 'Low Stock' ? 'orange' : 'green'
              }}>
                {p.stock_status}
              </td>
              <td>{p.category}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

**Output:**
```json
{
  "count": 4,
  "products": [
    {
      "id": 1,
      "name": "iPhone 15",
      "price": "79999.00",
      "stock": 50,
      "category": "Electronics",
      "gst_amount": "14399.82",
      "price_with_gst": "94398.82",
      "inventory_value": "3999950.00",
      "stock_status": "Well Stocked",
      "days_listed": 15,
      "status": "published"
    }
  ]
}
```

---

## Impact

| If You Don't Understand This...         | What Happens                                    |
|-----------------------------------------|-------------------------------------------------|
| Always use `SELECT *`                   | Transfer unnecessary data, slower queries        |
| Don't use aliases                       | Confusing column names in API responses          |
| Don't understand NULL handling          | NullPointerException in your JavaScript code     |
| Ignore DISTINCT                         | Duplicate data in dropdowns/filters              |
| Don't use CASE expressions              | More logic in JavaScript instead of database     |
| Skip computed columns                   | Calculate in JS for every row — much slower      |

### Performance: SELECT * vs SELECT columns

```
SELECT * FROM products;
→ Transfers: id + name + description + price + stock + metadata + images + ...
→ Data size: ~2 KB per row × 10,000 rows = ~20 MB

SELECT name, price FROM products;
→ Transfers: name + price only
→ Data size: ~50 bytes per row × 10,000 rows = ~500 KB

That's 40x less data! On a mobile connection, this is the difference
between a 0.1s and 4s load time.
```

---

## Practice Exercises

### Easy (SQL)
1. Select only the `name` and `price` from products
2. Select all customers and add an alias "Customer Email" for the email column
3. Get all unique statuses from the orders table
4. Select products with a computed column `price_after_discount` (10% off)

### Medium (SQL + Node.js)
5. Write an Express route `/api/products/summary` that returns: name, price, gst (18%), final_price, stock_status (CASE)
6. Create a `/api/stats` route using SELECT with COUNT, DISTINCT, and computed columns
7. Implement field selection via query params: `/api/products?fields=name,price,stock`

### Hard (Full Stack)
8. Build a dynamic data table component in React:
   - Column toggler (show/hide columns)
   - Computed columns (total value = price × stock)
   - Conditional cell coloring based on CASE expressions
9. Create a SQL query builder UI where users select columns and see the generated SQL + results

---

## Real-World Q&A

**Q1:** In Mongoose, I use `.select('-password')` to exclude fields. What's the MySQL equivalent?
**A:** MySQL doesn't have a built-in "exclude" syntax. You must list all columns you want. For APIs, define a constant with "safe" columns: `const SAFE_COLS = 'id, name, email, phone'` and use it in queries. Or use a view: `CREATE VIEW safe_users AS SELECT id, name, email FROM users;`

**Q2:** Why does mysql2 always return an array even for one row?
**A:** Because SELECT can return 0, 1, or many rows. mysql2 always returns `[rows, fields]` where `rows` is an array. For single-row queries, access `rows[0]`. In Mongoose, `findOne()` returns a single document — this is a convenience method that SQL drivers don't provide.

**Q3:** Should I compute values in SQL (CASE, calculations) or in JavaScript?
**A:** In SQL when possible. The database is optimized for data operations and returns exactly what the frontend needs. Computing in JS means: (1) Transferring extra data over the network, (2) Processing on the Node.js server instead of the database, (3) Doing it per-request instead of once. Exception: Complex business logic is better in JS for readability.

---

## Interview Q&A

**Q1: What is the difference between SELECT * and SELECT specific columns?**
SELECT * retrieves all columns; SELECT with specific columns retrieves only named ones. SELECT * is convenient for development but bad for production: it transfers unnecessary data, breaks if columns are added/removed, and prevents index-only scans. Always select only the columns you need.

**Q2: What does SELECT DISTINCT do?**
DISTINCT eliminates duplicate rows from the result set. `SELECT DISTINCT city FROM users` returns each unique city once. It applies to the entire row when multiple columns are listed: `SELECT DISTINCT city, state` returns unique city+state combinations.

**Q3: What is the purpose of column aliases (AS)?**
Aliases rename columns in the output without changing the table. Uses: (1) Give readable names to computed columns: `price * 1.18 AS price_with_gst`, (2) Shorten long column names, (3) Resolve naming conflicts in JOINs: `c.name AS customer_name, p.name AS product_name`.

**Q4: Explain the CASE expression in SQL with a real-world example.**
CASE is SQL's equivalent of if-else or switch. Example: categorizing products by price range: `CASE WHEN price > 50000 THEN 'Premium' WHEN price > 10000 THEN 'Mid' ELSE 'Budget' END AS category`. It works inside SELECT, WHERE, ORDER BY, and UPDATE SET clauses.

**Q5: How would you write a query that shows NULL values as a default string?**
Use `IFNULL(column, 'default')` or `COALESCE(col1, col2, 'default')`. IFNULL takes exactly 2 arguments and returns the second if the first is NULL. COALESCE takes N arguments and returns the first non-NULL value. In JavaScript terms: IFNULL is like `col ?? 'default'`; COALESCE is like `col1 ?? col2 ?? 'default'`.

---

| [← Previous: Insert, Update & Delete](./05_Insert_Update_Delete.md) | [Next: WHERE Clause & Filters →](./07_Where_Clause_And_Filters.md) |
|---|---|
