# Group By And Having

> 📌 **File:** `10_Group_By_And_Having.md` | **Level:** Beginner → MERN Developer

---

## What is it?

**GROUP BY** groups rows with the same values into summary rows and lets you apply aggregate functions (COUNT, SUM, AVG) to each group. **HAVING** filters those groups after aggregation.

It's the SQL equivalent of MongoDB's `$group` stage in the aggregation pipeline.

---

## MERN Parallel — You Already Know This!

| MongoDB Aggregation (You Know)                        | SQL GROUP BY (You'll Learn)                     |
|-------------------------------------------------------|-------------------------------------------------|
| `{ $group: { _id: "$category" } }`                   | `GROUP BY category_id`                          |
| `{ $group: { _id: "$status", count: {$sum: 1} } }`   | `SELECT status, COUNT(*) GROUP BY status`       |
| `{ $group: { _id: "$cat", total: {$sum: "$price"} }}`| `SELECT cat, SUM(price) GROUP BY cat`           |
| `{ $match: { count: { $gte: 5 } } }` (after $group)  | `HAVING COUNT(*) >= 5`                          |
| `{ $match: { status: "active" } }` (before $group)    | `WHERE status = 'active'`                       |

### Key Insight
```
MongoDB Pipeline:          SQL Equivalent:
$match (before grouping) → WHERE (filter rows first)
$group                   → GROUP BY + aggregate functions
$match (after grouping)  → HAVING (filter groups)
$sort                    → ORDER BY
$limit                   → LIMIT
```

---

## Why does it matter?

- "Sales by category", "Orders per customer", "Revenue by month" — all need GROUP BY
- HAVING lets you filter aggregated results (e.g., "customers with more than 5 orders")
- Essential for reports, analytics dashboards, and business intelligence
- Without GROUP BY, you'd need multiple queries or complex JavaScript processing
- One of the most tested SQL topics in interviews

---

## How does it work?

```
Step 1: FROM — Get all rows
Step 2: WHERE — Filter individual rows
Step 3: GROUP BY — Group rows by column(s)
Step 4: Aggregate functions run on each group
Step 5: HAVING — Filter groups based on aggregate results
Step 6: SELECT — Choose columns to display
Step 7: ORDER BY — Sort results
Step 8: LIMIT — Restrict output
```

---

## Visual Diagram

### GROUP BY Visualization

```
Original Data:                          After GROUP BY category_id:
┌────┬──────────┬────────┬──────────┐  ┌────────────┬────────┬──────────┬──────────┐
│ id │ name     │ cat_id │ price    │  │ category_id│ COUNT  │ SUM      │ AVG      │
├────┼──────────┼────────┼──────────┤  ├────────────┼────────┼──────────┼──────────┤
│ 1  │ iPhone   │   1    │ 79999    │  │     1      │   3    │ 219799   │ 73266.33 │
│ 2  │ MacBook  │   1    │ 114900   │  │     2      │   1    │ 2499     │ 2499.00  │
│ 3  │ Jeans    │   2    │ 2499     │  │     3      │   1    │ 299      │ 299.00   │
│ 4  │ Alchemist│   3    │ 299      │  └────────────┴────────┴──────────┴──────────┘
│ 5  │ AirPods  │   1    │ 24900    │     3 groups from 5 rows
└────┴──────────┴────────┴──────────┘

GROUP BY takes 5 rows → produces 3 groups
Each group gets its own COUNT, SUM, AVG
```

### WHERE vs HAVING

```
WHERE (before grouping):
┌──────────────────────────┐
│ All rows in table        │
│ ┌──────────────────────┐ │
│ │ WHERE price > 1000   │ │ ← Filters individual rows
│ │ (removes Alchemist)  │ │
│ └──────────────────────┘ │
│         │                │
│         ▼                │
│ ┌──────────────────────┐ │
│ │ GROUP BY category_id │ │ ← Groups remaining rows
│ └──────────────────────┘ │
│         │                │
│         ▼                │
│ ┌──────────────────────┐ │
│ │ HAVING COUNT(*) > 1  │ │ ← Filters groups
│ │ (removes groups with │ │
│ │  only 1 product)     │ │
│ └──────────────────────┘ │
└──────────────────────────┘
```

---

## Syntax

```sql
-- ============================================
-- BASIC GROUP BY
-- ============================================

-- Count products per category
SELECT category_id, COUNT(*) AS product_count
FROM products
GROUP BY category_id;

-- Total revenue per order status
SELECT status, COUNT(*) AS order_count, SUM(total_amount) AS total_revenue
FROM orders
GROUP BY status;

-- Average price per category
SELECT 
  c.name AS category,
  COUNT(p.id) AS product_count,
  ROUND(AVG(p.price), 2) AS avg_price,
  MIN(p.price) AS cheapest,
  MAX(p.price) AS most_expensive
FROM products p
JOIN categories c ON p.category_id = c.id
GROUP BY c.name;


-- ============================================
-- GROUP BY with HAVING
-- ============================================

-- Categories with more than 2 products
SELECT category_id, COUNT(*) AS product_count
FROM products
GROUP BY category_id
HAVING COUNT(*) > 2;

-- Customers who spent more than ₹50,000
SELECT 
  c.name,
  COUNT(o.id) AS order_count,
  SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
HAVING SUM(o.total_amount) > 50000
ORDER BY total_spent DESC;


-- ============================================
-- GROUP BY with WHERE + HAVING
-- ============================================

-- Active categories with more than 5 published products averaging over ₹1000
SELECT 
  c.name AS category,
  COUNT(*) AS product_count,
  ROUND(AVG(p.price), 2) AS avg_price
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.status = 'published'           -- WHERE: filter rows first
GROUP BY c.name                        -- GROUP BY: then group
HAVING COUNT(*) > 5                    -- HAVING: filter groups
   AND AVG(p.price) > 1000
ORDER BY avg_price DESC;               -- ORDER BY: sort results


-- ============================================
-- GROUP BY with DATE functions (time-based reports)
-- ============================================

-- Monthly revenue
SELECT 
  DATE_FORMAT(order_date, '%Y-%m') AS month,
  COUNT(*) AS order_count,
  ROUND(SUM(total_amount), 2) AS revenue
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month DESC;

-- Daily orders for the last 7 days
SELECT 
  DATE(order_date) AS date,
  COUNT(*) AS orders,
  ROUND(SUM(total_amount), 2) AS revenue
FROM orders
WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY DATE(order_date)
ORDER BY date;

-- Revenue by day of week
SELECT 
  DAYNAME(order_date) AS day_of_week,
  COUNT(*) AS order_count,
  ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
GROUP BY DAYNAME(order_date), DAYOFWEEK(order_date)
ORDER BY DAYOFWEEK(order_date);


-- ============================================
-- GROUP BY with ROLLUP (subtotals and grand total)
-- ============================================
SELECT 
  COALESCE(c.name, 'GRAND TOTAL') AS category,
  COUNT(*) AS product_count,
  ROUND(SUM(p.price), 2) AS total_value
FROM products p
JOIN categories c ON p.category_id = c.id
GROUP BY c.name WITH ROLLUP;
-- Adds a summary row at the bottom with totals
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== MongoDB Aggregation (What You Know) ==========

// Products per category
const result = await Product.aggregate([
  { $group: {
    _id: '$category',
    count: { $sum: 1 },
    avgPrice: { $avg: '$price' },
    totalValue: { $sum: '$price' }
  }},
  { $sort: { count: -1 } }
]);

// Monthly revenue
const result = await Order.aggregate([
  { $group: {
    _id: { $dateToString: { format: '%Y-%m', date: '$orderDate' } },
    count: { $sum: 1 },
    revenue: { $sum: '$totalAmount' }
  }},
  { $sort: { _id: -1 } }
]);

// Customers with >5 orders
const result = await Order.aggregate([
  { $group: { _id: '$customerId', orderCount: { $sum: 1 } } },
  { $match: { orderCount: { $gt: 5 } } }
]);
```

```sql
-- ========== MySQL ==========

-- Products per category
SELECT category_id, COUNT(*) AS count,
  ROUND(AVG(price), 2) AS avg_price, SUM(price) AS total_value
FROM products
GROUP BY category_id
ORDER BY count DESC;

-- Monthly revenue
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
  COUNT(*) AS count, SUM(total_amount) AS revenue
FROM orders
GROUP BY month
ORDER BY month DESC;

-- Customers with >5 orders
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING order_count > 5;
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Products per category with category name
const [categoryStats] = await pool.query(`
  SELECT 
    c.name AS category,
    COUNT(*) AS product_count,
    ROUND(AVG(p.price), 2) AS avg_price,
    ROUND(SUM(p.price), 2) AS total_value
  FROM products p
  JOIN categories c ON p.category_id = c.id
  GROUP BY c.id, c.name
  ORDER BY product_count DESC
`);

// Monthly revenue (parameterized year)
const [monthlyRevenue] = await pool.query(`
  SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(*) AS order_count,
    ROUND(SUM(total_amount), 2) AS revenue
  FROM orders
  WHERE YEAR(order_date) = ?
  GROUP BY month
  ORDER BY month
`, [2024]);
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize ==========
const { fn, col, literal } = require('sequelize');

// Products per category
const stats = await Product.findAll({
  attributes: [
    'categoryId',
    [fn('COUNT', '*'), 'productCount'],
    [fn('ROUND', fn('AVG', col('price')), 2), 'avgPrice'],
    [fn('SUM', col('price')), 'totalValue']
  ],
  group: ['categoryId'],
  order: [[literal('productCount'), 'DESC']],
  include: [{ model: Category, attributes: ['name'] }]
});

// Monthly revenue
const monthlyRevenue = await Order.findAll({
  attributes: [
    [fn('DATE_FORMAT', col('order_date'), '%Y-%m'), 'month'],
    [fn('COUNT', '*'), 'orderCount'],
    [fn('ROUND', fn('SUM', col('total_amount')), 2), 'revenue']
  ],
  group: [literal("DATE_FORMAT(order_date, '%Y-%m')")],
  order: [[literal('month'), 'DESC']]
});
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Sales analytics report

```sql
-- SQL: Comprehensive sales analytics
-- Category-wise sales
SELECT 
  c.name AS category,
  COUNT(DISTINCT p.id) AS products,
  COUNT(oi.id) AS items_sold,
  ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
  ROUND(AVG(oi.unit_price), 2) AS avg_selling_price
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'cancelled'
GROUP BY c.id, c.name
ORDER BY revenue DESC;
```

```js
// Node.js + Express — Analytics API
app.get('/api/analytics/sales', async (req, res) => {
  try {
    const { period = 'month' } = req.query;
    
    // Format string based on period
    const dateFormats = {
      day: '%Y-%m-%d',
      week: '%Y-W%u',
      month: '%Y-%m',
      year: '%Y'
    };
    const dateFormat = dateFormats[period] || dateFormats.month;
    
    // Revenue over time
    const [revenueTimeline] = await pool.query(`
      SELECT 
        DATE_FORMAT(o.order_date, ?) AS period,
        COUNT(DISTINCT o.id) AS orders,
        ROUND(SUM(o.total_amount), 2) AS revenue,
        ROUND(AVG(o.total_amount), 2) AS avg_order_value
      FROM orders o
      WHERE o.status != 'cancelled'
      GROUP BY period
      ORDER BY period DESC
      LIMIT 12
    `, [dateFormat]);
    
    // Top selling products
    const [topProducts] = await pool.query(`
      SELECT 
        p.name,
        SUM(oi.quantity) AS units_sold,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
      FROM order_items oi
      JOIN products p ON oi.product_id = p.id
      JOIN orders o ON oi.order_id = o.id
      WHERE o.status != 'cancelled'
      GROUP BY p.id, p.name
      ORDER BY revenue DESC
      LIMIT 10
    `);
    
    // Category breakdown
    const [categoryBreakdown] = await pool.query(`
      SELECT 
        c.name AS category,
        COUNT(DISTINCT o.id) AS orders,
        SUM(oi.quantity) AS units_sold,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
      FROM categories c
      JOIN products p ON c.id = p.category_id
      JOIN order_items oi ON p.id = oi.product_id
      JOIN orders o ON oi.order_id = o.id
      WHERE o.status != 'cancelled'
      GROUP BY c.id, c.name
      ORDER BY revenue DESC
    `);
    
    res.json({ revenueTimeline, topProducts, categoryBreakdown });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// React — Sales Analytics Component
import { useState, useEffect } from 'react';
import axios from 'axios';

function SalesAnalytics() {
  const [data, setData] = useState(null);
  const [period, setPeriod] = useState('month');

  useEffect(() => {
    axios.get(`/api/analytics/sales?period=${period}`)
      .then(({ data }) => setData(data));
  }, [period]);

  if (!data) return <p>Loading analytics...</p>;

  return (
    <div>
      <h1>Sales Analytics</h1>
      
      <select value={period} onChange={e => setPeriod(e.target.value)}>
        <option value="day">Daily</option>
        <option value="week">Weekly</option>
        <option value="month">Monthly</option>
        <option value="year">Yearly</option>
      </select>

      <h2>Revenue Timeline</h2>
      <table>
        <thead>
          <tr><th>Period</th><th>Orders</th><th>Revenue</th><th>Avg Order</th></tr>
        </thead>
        <tbody>
          {data.revenueTimeline.map((r, i) => (
            <tr key={i}>
              <td>{r.period}</td><td>{r.orders}</td>
              <td>₹{r.revenue}</td><td>₹{r.avg_order_value}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Top Products</h2>
      {data.topProducts.map((p, i) => (
        <div key={i}>
          <strong>#{i + 1}</strong> {p.name} — {p.units_sold} sold — ₹{p.revenue}
        </div>
      ))}

      <h2>Category Breakdown</h2>
      {data.categoryBreakdown.map((c, i) => (
        <div key={i}>
          <strong>{c.category}</strong>: {c.orders} orders, ₹{c.revenue} revenue
        </div>
      ))}
    </div>
  );
}
```

**Output:**
```json
{
  "revenueTimeline": [
    { "period": "2024-01", "orders": 45, "revenue": "750000.00", "avg_order_value": "16666.67" },
    { "period": "2023-12", "orders": 52, "revenue": "890000.00", "avg_order_value": "17115.38" }
  ],
  "topProducts": [
    { "name": "iPhone 15", "units_sold": 120, "revenue": "9599880.00" },
    { "name": "MacBook Air M3", "units_sold": 45, "revenue": "5170500.00" }
  ],
  "categoryBreakdown": [
    { "category": "Electronics", "orders": 200, "units_sold": 350, "revenue": "15000000.00" },
    { "category": "Books", "orders": 150, "units_sold": 500, "revenue": "149500.00" }
  ]
}
```

---

## Impact

| If You Don't Understand GROUP BY...      | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| SELECT non-grouped column without aggregate | Error: "not in GROUP BY clause"             |
| Use WHERE instead of HAVING              | `WHERE COUNT(*) > 5` → ERROR!                   |
| Don't include GROUP BY columns in SELECT | Confusing results — can't tell which group is which |
| Group by wrong column                    | Incorrect aggregations, misleading reports       |
| Forget GROUP BY with aggregate + normal columns | MySQL may return random non-grouped values (ONLY_FULL_GROUP_BY mode) |

### The ONLY_FULL_GROUP_BY Rule

```sql
-- ❌ INVALID (in strict mode — default in MySQL 8.0)
SELECT name, category_id, COUNT(*)
FROM products
GROUP BY category_id;
-- Error: 'name' is not in GROUP BY or an aggregate function
-- Which NAME should MySQL pick from each group? It can't decide!

-- ✅ VALID options:
-- Option 1: Include in GROUP BY
SELECT name, category_id, COUNT(*) FROM products GROUP BY category_id, name;

-- Option 2: Use aggregate function on non-grouped column
SELECT MAX(name), category_id, COUNT(*) FROM products GROUP BY category_id;

-- Option 3: Remove from SELECT
SELECT category_id, COUNT(*) FROM products GROUP BY category_id;
```

---

## Practice Exercises

### Easy (SQL)
1. Count the number of products in each category
2. Find the total revenue for each order status (pending, shipped, delivered)
3. Calculate the average product price per category
4. Find the number of orders placed each month

### Medium (SQL + Node.js)
5. Build a `/api/analytics/categories` endpoint returning product count, avg price, and total value per category
6. Find customers who have placed more than 3 orders using GROUP BY + HAVING
7. Create a monthly revenue report for the current year

### Hard (Full Stack)
8. Build an analytics dashboard with:
   - Revenue chart (group by month/week/day)
   - Category breakdown pie chart data
   - Top 10 customers by total spending
   - Period selector (this week, this month, this year)
9. Implement a "cohort analysis": group customers by registration month, then show their purchasing behavior over time

---

## Real-World Q&A

**Q1:** In MongoDB's aggregation pipeline, I can use `$match` both before and after `$group`. What's the SQL equivalent?
**A:** `WHERE` is `$match` before grouping (filters individual rows). `HAVING` is `$match` after grouping (filters aggregated groups). Example: `WHERE status = 'active'` filters rows, `HAVING COUNT(*) > 5` filters groups.

**Q2:** Can I GROUP BY a computed column or alias?
**A:** In MySQL, yes! You can `GROUP BY YEAR(order_date)` or even `GROUP BY 1` (first SELECT column). You can also use column aliases in GROUP BY and HAVING in MySQL (this doesn't work in all databases).

**Q3:** What's the performance impact of GROUP BY?
**A:** GROUP BY creates temporary result sets and can be expensive on large tables. Adding an index on the GROUP BY column helps significantly. For very large datasets, consider materialized views or pre-aggregated summary tables that are updated periodically.

---

## Interview Q&A

**Q1: What is the difference between WHERE and HAVING?**
WHERE filters individual rows before grouping. HAVING filters groups after aggregation. WHERE cannot use aggregate functions; HAVING can. Example: `WHERE price > 100` is valid; `WHERE COUNT(*) > 5` is invalid (use HAVING instead). Both can coexist: `WHERE status='active' GROUP BY cat HAVING COUNT(*)>5`.

**Q2: Can you use GROUP BY without aggregate functions?**
Yes — it acts like SELECT DISTINCT. `SELECT city FROM customers GROUP BY city` is equivalent to `SELECT DISTINCT city FROM customers`. However, using DISTINCT is more readable for this purpose.

**Q3: What is GROUP BY WITH ROLLUP?**
ROLLUP adds summary rows (subtotals and grand total) to GROUP BY results. `GROUP BY category WITH ROLLUP` adds an extra row with NULL for category that shows the grand total. It's like adding a "Total" row at the bottom of a spreadsheet.

**Q4: Write a query to find duplicate emails in a customers table.**
`SELECT email, COUNT(*) AS count FROM customers GROUP BY email HAVING COUNT(*) > 1;` This groups by email, counts occurrences, and filters for groups with more than one occurrence — i.e., duplicates.

**Q5: How would you get the top 3 customers by total spending?**
`SELECT c.name, SUM(o.total_amount) AS total_spent FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name ORDER BY total_spent DESC LIMIT 3;` This joins customers with orders, groups by customer, sums their spending, sorts descending, and takes top 3.

---

| [← Previous: Aggregate Functions](./09_Aggregate_Functions.md) | [Next: Joins →](./11_Joins.md) |
|---|---|
