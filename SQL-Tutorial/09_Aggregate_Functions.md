# Aggregate Functions

> 📌 **File:** `09_Aggregate_Functions.md` | **Level:** Beginner → MERN Developer

---

## What is it?

Aggregate functions perform calculations across multiple rows and return a single result. They're the SQL equivalent of MongoDB's aggregation pipeline stages like `$sum`, `$avg`, `$count`, `$min`, `$max`.

The five core aggregates: **COUNT**, **SUM**, **AVG**, **MIN**, **MAX**.

---

## MERN Parallel — You Already Know This!

| MongoDB Aggregation (You Know)                    | SQL Aggregate (You'll Learn)                |
|---------------------------------------------------|---------------------------------------------|
| `db.orders.countDocuments()`                      | `SELECT COUNT(*) FROM orders;`              |
| `{ $group: { _id: null, total: { $sum: "$price" }}}` | `SELECT SUM(price) FROM products;`     |
| `{ $group: { _id: null, avg: { $avg: "$price" }}}` | `SELECT AVG(price) FROM products;`       |
| `{ $group: { _id: null, min: { $min: "$price" }}}` | `SELECT MIN(price) FROM products;`       |
| `{ $group: { _id: null, max: { $max: "$price" }}}` | `SELECT MAX(price) FROM products;`       |
| `{ $count: "total" }`                             | `SELECT COUNT(*) AS total`                  |
| Model.countDocuments(filter)                       | `SELECT COUNT(*) FROM t WHERE ...`          |

---

## Why does it matter?

- Dashboards, reports, and analytics rely entirely on aggregate functions
- Business questions: "How many orders today?", "What's the total revenue?", "What's the average order value?"
- Much faster than fetching all rows and calculating in JavaScript
- Interview questions frequently test aggregate function knowledge
- Foundation for GROUP BY (next chapter)

---

## How does it work?

```
Table: products (5 rows)
┌────┬──────────┬──────────┬───────┐
│ id │ name     │ price    │ stock │
├────┼──────────┼──────────┼───────┤
│ 1  │ iPhone   │ 79999.00 │ 50    │
│ 2  │ MacBook  │ 114900.00│ 30    │
│ 3  │ Jeans    │ 2499.00  │ 200   │
│ 4  │ Alchemist│ 299.00   │ 500   │
│ 5  │ AirPods  │ 24900.00 │ 100   │
└────┴──────────┴──────────┴───────┘

COUNT(*) = 5                    (number of rows)
SUM(price) = 222597.00          (total of all prices)
AVG(price) = 44519.40           (average price)
MIN(price) = 299.00             (cheapest)
MAX(price) = 114900.00          (most expensive)
SUM(price * stock) = 16,144,800 (total inventory value)
```

---

## Visual Diagram

### How Aggregates Process Data

```
Input Rows:                          Aggregate Results:
┌──────────┐                        ┌──────────────────────┐
│ 79999.00 │──┐                     │ COUNT = 5            │
│114900.00 │──┤                     │ SUM   = 222,597.00   │
│  2499.00 │──┼── Aggregate ──────▶ │ AVG   = 44,519.40    │
│   299.00 │──┤   Functions         │ MIN   = 299.00       │
│ 24900.00 │──┘                     │ MAX   = 114,900.00   │
└──────────┘                        └──────────────────────┘
 5 input rows                        1 output row
```

### COUNT Variants

```
COUNT(*)           → Counts ALL rows (including NULLs)
COUNT(column)      → Counts rows where column IS NOT NULL
COUNT(DISTINCT col)→ Counts unique non-NULL values

Example with NULL phones:
┌────┬────────┬───────────┐
│ id │ name   │ phone     │
├────┼────────┼───────────┤
│ 1  │Nishant │ 987654321 │
│ 2  │ Priya  │ NULL      │
│ 3  │ Rahul  │ 987654321 │  ← Same as Nishant
│ 4  │ Sneha  │ 123456789 │
│ 5  │ Amit   │ NULL      │
└────┴────────┴───────────┘

COUNT(*)              = 5  (all rows)
COUNT(phone)          = 3  (non-NULL phones)
COUNT(DISTINCT phone) = 2  (unique phone numbers)
```

---

## Syntax

```sql
-- ============================================
-- COUNT — How many rows?
-- ============================================
SELECT COUNT(*) FROM products;                    -- All rows: 5
SELECT COUNT(*) AS total_products FROM products;  -- With alias
SELECT COUNT(phone) FROM customers;               -- Non-NULL phones only
SELECT COUNT(DISTINCT category_id) FROM products; -- Unique categories
SELECT COUNT(*) FROM orders WHERE status = 'pending'; -- Filtered count

-- ============================================
-- SUM — Total of a column
-- ============================================
SELECT SUM(price) AS total_price FROM products;
SELECT SUM(stock) AS total_inventory FROM products;
SELECT SUM(quantity * unit_price) AS total_revenue FROM order_items;

-- ============================================
-- AVG — Average value
-- ============================================
SELECT AVG(price) AS avg_price FROM products;
SELECT ROUND(AVG(price), 2) AS avg_price FROM products;  -- Rounded to 2 decimals
SELECT AVG(DATEDIFF(NOW(), created_at)) AS avg_account_age_days FROM customers;

-- ============================================
-- MIN / MAX — Smallest / Largest
-- ============================================
SELECT MIN(price) AS cheapest FROM products;
SELECT MAX(price) AS most_expensive FROM products;
SELECT MIN(order_date) AS first_order, MAX(order_date) AS last_order FROM orders;

-- ============================================
-- COMBINING AGGREGATES
-- ============================================
SELECT 
  COUNT(*) AS total_products,
  SUM(price) AS total_value,
  ROUND(AVG(price), 2) AS avg_price,
  MIN(price) AS min_price,
  MAX(price) AS max_price,
  SUM(stock) AS total_stock,
  SUM(price * stock) AS inventory_value
FROM products
WHERE status = 'published';

-- ============================================
-- AGGREGATE with EXPRESSIONS
-- ============================================
SELECT 
  COUNT(CASE WHEN stock = 0 THEN 1 END) AS out_of_stock,
  COUNT(CASE WHEN stock > 0 AND stock < 10 THEN 1 END) AS low_stock,
  COUNT(CASE WHEN stock >= 10 THEN 1 END) AS in_stock
FROM products;
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== MongoDB Aggregation (What You Know) ==========

// Count
const count = await Product.countDocuments();

// Sum
const result = await Product.aggregate([
  { $group: { _id: null, total: { $sum: '$price' } } }
]);
const total = result[0].total;

// Average
const result = await Product.aggregate([
  { $group: { _id: null, avg: { $avg: '$price' } } }
]);

// Min/Max
const result = await Product.aggregate([
  { $group: { _id: null, min: { $min: '$price' }, max: { $max: '$price' } } }
]);

// Dashboard stats
const stats = await Product.aggregate([
  { $group: {
    _id: null,
    count: { $sum: 1 },
    totalValue: { $sum: '$price' },
    avgPrice: { $avg: '$price' },
    minPrice: { $min: '$price' },
    maxPrice: { $max: '$price' }
  }}
]);
```

```sql
-- ========== MySQL ==========

-- Count
SELECT COUNT(*) AS count FROM products;

-- Sum
SELECT SUM(price) AS total FROM products;

-- Average
SELECT ROUND(AVG(price), 2) AS avg FROM products;

-- Min/Max
SELECT MIN(price) AS min, MAX(price) AS max FROM products;

-- Dashboard stats (all in one query!)
SELECT 
  COUNT(*) AS count,
  SUM(price) AS total_value,
  ROUND(AVG(price), 2) AS avg_price,
  MIN(price) AS min_price,
  MAX(price) AS max_price
FROM products;
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Dashboard stats in one query
const [stats] = await pool.query(`
  SELECT 
    COUNT(*) AS total_products,
    ROUND(SUM(price), 2) AS total_value,
    ROUND(AVG(price), 2) AS avg_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price,
    SUM(stock) AS total_stock,
    ROUND(SUM(price * stock), 2) AS inventory_value
  FROM products
  WHERE status = 'published'
`);
console.log(stats[0]);  // Single row with all stats
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize ==========
const { fn, col } = require('sequelize');

// Count
const count = await Product.count();
const publishedCount = await Product.count({ where: { status: 'published' } });

// Sum
const total = await Product.sum('price');

// Avg
const avg = await Product.aggregate('price', 'avg');

// Min/Max
const min = await Product.min('price');
const max = await Product.max('price');

// All stats with findAll + aggregate functions
const stats = await Product.findAll({
  attributes: [
    [fn('COUNT', '*'), 'total_products'],
    [fn('SUM', col('price')), 'total_value'],
    [fn('ROUND', fn('AVG', col('price')), 2), 'avg_price'],
    [fn('MIN', col('price')), 'min_price'],
    [fn('MAX', col('price')), 'max_price']
  ],
  where: { status: 'published' },
  raw: true
});
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Admin dashboard with key business metrics

```sql
-- SQL: E-commerce dashboard stats
-- Product stats
SELECT 
  COUNT(*) AS total_products,
  COUNT(CASE WHEN stock = 0 THEN 1 END) AS out_of_stock,
  COUNT(CASE WHEN status = 'published' THEN 1 END) AS published,
  ROUND(AVG(price), 2) AS avg_price,
  ROUND(SUM(price * stock), 2) AS inventory_value
FROM products;

-- Order stats
SELECT 
  COUNT(*) AS total_orders,
  ROUND(SUM(total_amount), 2) AS total_revenue,
  ROUND(AVG(total_amount), 2) AS avg_order_value,
  COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending_orders,
  COUNT(CASE WHEN status = 'delivered' THEN 1 END) AS delivered_orders
FROM orders;

-- Customer stats
SELECT 
  COUNT(*) AS total_customers,
  COUNT(CASE WHEN created_at > DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) AS new_this_month
FROM customers;

-- Today's stats
SELECT 
  COUNT(*) AS orders_today,
  COALESCE(SUM(total_amount), 0) AS revenue_today
FROM orders 
WHERE DATE(order_date) = CURDATE();
```

```js
// Node.js + Express — Dashboard API
app.get('/api/dashboard', async (req, res) => {
  try {
    // Run all queries in parallel for speed
    const [productStats] = await pool.query(`
      SELECT 
        COUNT(*) AS total_products,
        COUNT(CASE WHEN stock = 0 THEN 1 END) AS out_of_stock,
        COUNT(CASE WHEN status = 'published' THEN 1 END) AS published,
        ROUND(AVG(price), 2) AS avg_price,
        ROUND(SUM(price * stock), 2) AS inventory_value
      FROM products
    `);

    const [orderStats] = await pool.query(`
      SELECT 
        COUNT(*) AS total_orders,
        ROUND(COALESCE(SUM(total_amount), 0), 2) AS total_revenue,
        ROUND(COALESCE(AVG(total_amount), 0), 2) AS avg_order_value,
        COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending_orders,
        COUNT(CASE WHEN status = 'delivered' THEN 1 END) AS delivered_orders
      FROM orders
    `);

    const [customerStats] = await pool.query(`
      SELECT 
        COUNT(*) AS total_customers,
        COUNT(CASE WHEN created_at > DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) AS new_this_month
      FROM customers
    `);

    const [todayStats] = await pool.query(`
      SELECT 
        COUNT(*) AS orders_today,
        COALESCE(SUM(total_amount), 0) AS revenue_today
      FROM orders 
      WHERE DATE(order_date) = CURDATE()
    `);

    res.json({
      products: productStats[0],
      orders: orderStats[0],
      customers: customerStats[0],
      today: todayStats[0]
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// React — Dashboard Component
import { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axios.get('/api/dashboard').then(({ data }) => setStats(data));
  }, []);

  if (!stats) return <p>Loading dashboard...</p>;

  const cards = [
    { title: 'Total Products', value: stats.products.total_products, color: '#3498db' },
    { title: 'Total Revenue', value: `₹${stats.orders.total_revenue}`, color: '#2ecc71' },
    { title: 'Total Orders', value: stats.orders.total_orders, color: '#e74c3c' },
    { title: 'Total Customers', value: stats.customers.total_customers, color: '#f39c12' },
    { title: 'Avg Order Value', value: `₹${stats.orders.avg_order_value}`, color: '#9b59b6' },
    { title: 'Revenue Today', value: `₹${stats.today.revenue_today}`, color: '#1abc9c' },
    { title: 'Pending Orders', value: stats.orders.pending_orders, color: '#e67e22' },
    { title: 'Out of Stock', value: stats.products.out_of_stock, color: '#e74c3c' }
  ];

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
        {cards.map((card, i) => (
          <div key={i} style={{
            backgroundColor: card.color, color: 'white',
            padding: '20px', borderRadius: '8px', textAlign: 'center'
          }}>
            <h3>{card.title}</h3>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{card.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

**Output:**
```json
{
  "products": {
    "total_products": 5,
    "out_of_stock": 0,
    "published": 4,
    "avg_price": "44519.40",
    "inventory_value": "16144800.00"
  },
  "orders": {
    "total_orders": 150,
    "total_revenue": "2500000.00",
    "avg_order_value": "16666.67",
    "pending_orders": 23,
    "delivered_orders": 95
  },
  "customers": {
    "total_customers": 75,
    "new_this_month": 12
  },
  "today": {
    "orders_today": 8,
    "revenue_today": "125000.00"
  }
}
```

---

## Impact

| If You Don't Understand Aggregates...    | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| Fetch all rows and count in JS           | 1000x slower — database does it in milliseconds  |
| Use COUNT(*) on huge tables without index | Slow query — consider approximate counts         |
| Forget ROUND on AVG                      | Display ₹44519.4000000001 to users               |
| Don't use COALESCE with SUM              | SUM returns NULL if no rows match (not 0)         |
| Mix aggregate and non-aggregate columns  | Error or wrong results (must use GROUP BY)        |

---

## Practice Exercises

### Easy (SQL)
1. Count the total number of customers
2. Find the most expensive and cheapest product
3. Calculate the total value of all products in stock (price × stock)
4. Find the average price of products in the 'Electronics' category

### Medium (SQL + Node.js)
5. Build a `/api/stats` endpoint that returns product, order, and customer counts
6. Write a query that counts products by stock level: out_of_stock, low (<10), normal (10-100), high (>100)
7. Calculate the total revenue and order count for the current month

### Hard (Full Stack)
8. Build a complete admin dashboard with:
   - KPI cards (revenue, orders, customers, products)
   - Mini charts (daily revenue for last 7 days using aggregates)
   - Real-time counters (auto-refresh every 30 seconds)
9. Create a reports API that returns aggregate data for a date range (custom period)

---

## Real-World Q&A

**Q1:** In MongoDB, I use `countDocuments()` which is simple. Why is SQL COUNT more confusing with COUNT(*) vs COUNT(column)?
**A:** `COUNT(*)` counts all rows regardless of NULL values — like `countDocuments()`. `COUNT(column)` counts only non-NULL values in that column. `COUNT(DISTINCT column)` counts unique non-NULL values. MongoDB's `countDocuments()` is always equivalent to `COUNT(*)`.

**Q2:** Why does SUM return NULL instead of 0 when no rows match?
**A:** SQL aggregates return NULL when operating on an empty set (no rows). This is by design — NULL means "no data to aggregate." Use `COALESCE(SUM(amount), 0)` to convert NULL to 0. It's a common gotcha that breaks JavaScript code: `null + 100 = 100` in JS but `NULL + 100 = NULL` in SQL.

**Q3:** Should I calculate averages in SQL or JavaScript?
**A:** Always in SQL. The database processes millions of rows and returns a single number. Fetching all rows to JavaScript and calling `.reduce()` transfers massive data and is orders of magnitude slower.

---

## Interview Q&A

**Q1: What is the difference between COUNT(*), COUNT(column), and COUNT(DISTINCT column)?**
COUNT(*) counts all rows including those with NULLs. COUNT(column) counts only rows where that column is not NULL. COUNT(DISTINCT column) counts unique non-NULL values. Example: with values [1, 2, 2, NULL], COUNT(*)=4, COUNT(col)=3, COUNT(DISTINCT col)=2.

**Q2: What does SUM return when there are no matching rows?**
NULL, not 0. Use `COALESCE(SUM(column), 0)` to get 0 instead. This applies to AVG, MIN, and MAX too — they all return NULL for empty sets. COUNT is the exception — COUNT(*) returns 0 for empty sets.

**Q3: Can you use WHERE with aggregate functions?**
No. WHERE filters rows BEFORE aggregation. To filter based on aggregate results, use HAVING (after GROUP BY). Example: `WHERE price > 100` works, but `WHERE AVG(price) > 100` is invalid. Use `HAVING AVG(price) > 100` instead.

**Q4: Write a query to find the second highest price in the products table.**
`SELECT MAX(price) FROM products WHERE price < (SELECT MAX(price) FROM products);` Or: `SELECT DISTINCT price FROM products ORDER BY price DESC LIMIT 1 OFFSET 1;`

**Q5: How would you get a running total (cumulative sum) in SQL?**
Using window functions: `SELECT name, price, SUM(price) OVER (ORDER BY id) AS running_total FROM products;` Window functions (OVER clause) perform calculations across rows related to the current row without collapsing them — like aggregates but preserving individual rows.

---

| [← Previous: Sorting & Limiting](./08_Sorting_And_Limiting.md) | [Next: Group By & Having →](./10_Group_By_And_Having.md) |
|---|---|
