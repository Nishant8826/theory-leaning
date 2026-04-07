# Joins

> 📌 **File:** `11_Joins.md` | **Level:** Beginner → MERN Developer

---

## What is it?

A JOIN combines rows from two or more tables based on a related column. In MongoDB, you either embed data inside documents or use `populate()` (Mongoose) / `$lookup` (aggregation) to connect collections. In SQL, data is split into separate tables by design, and JOINs are how you bring it back together.

JOINs are the **most important** SQL concept. Master JOINs and you've mastered relational databases.

---

## MERN Parallel — You Already Know This!

| Mongoose (You Know)                               | SQL JOIN (You'll Learn)                          |
|----------------------------------------------------|--------------------------------------------------|
| `Order.find().populate('customer')`                | `SELECT * FROM orders JOIN customers ON ...`     |
| `Product.find().populate('category')`              | `LEFT JOIN categories ON p.category_id = c.id`   |
| `$lookup` in aggregation pipeline                  | `JOIN` in SQL                                    |
| Embedded subdocuments `{ address: {...} }`         | Separate `addresses` table + JOIN                |
| `ref: 'Category'` in schema                       | `FOREIGN KEY (category_id) REFERENCES categories(id)` |
| Application-level joining (multiple queries)       | Database-level joining (single query)            |

### The Core Difference
```
MongoDB approach:                    SQL approach:
┌─────────────────────┐             ┌──────────┐   ┌──────────┐
│ Order Document      │             │ orders   │   │customers │
│ {                   │             │ ────────── │   │ ──────── │
│   customer: {       │      vs     │ id       │──▶│ id       │
│     name: "Ali",    │             │ cust_id  │   │ name     │
│     email: "..."    │             │ total    │   │ email    │
│   },                │             └──────────┘   └──────────┘
│   total: 5000       │             
│ }                   │             Data is SPLIT → JOIN to combine
└─────────────────────┘             
Data is EMBEDDED together           SELECT * FROM orders 
                                     JOIN customers ON ...
```

---

## Why does it matter?

- In SQL, related data lives in separate tables — JOINs are the ONLY way to combine them
- A single JOIN query replaces what would be 2+ separate MongoDB queries + application-level merging
- JOINs are performed by the database engine (optimized, fast) vs Mongoose populate (multiple round-trips)
- **Every SQL interview will test JOINs** — it's the #1 topic
- Understanding JOINs helps you design better database schemas

---

## How does it work?

### The 4 Types of JOINs

```
Given two tables: A and B

INNER JOIN:          LEFT JOIN:           RIGHT JOIN:         FULL OUTER JOIN:
Only matching        All from A +         All from B +        All from both
rows from both       matching from B      matching from A

  ┌───┬───┐           ┌───┬───┐           ┌───┬───┐          ┌───┬───┐
  │ A │ B │           │ A │ B │           │ A │ B │          │ A │ B │
  │   ┼───┤           │───┼───┤           ├───┼───│          │───┼───│
  │   │███│           │███│███│           │███│███│          │███│███│
  │   ┼───┤           │───┼───┤           ├───┼───│          │───┼───│
  │   │   │           │███│   │           │   │███│          │███│███│
  └───┴───┘           └───┴───┘           └───┴───┘          └───┴───┘
  
█ = Included in result
```

---

## Visual Diagram

### JOIN Example With Data

```
customers table:                    orders table:
┌────┬─────────┬──────────────┐    ┌────┬─────────────┬──────────┬─────────┐
│ id │ name    │ email        │    │ id │ customer_id │ total    │ status  │
├────┼─────────┼──────────────┤    ├────┼─────────────┼──────────┼─────────┤
│ 1  │ Nishant │ n@test.com   │    │ 1  │ 1           │ 79999    │ shipped │
│ 2  │ Priya   │ p@test.com   │    │ 2  │ 1           │ 2499     │ pending │
│ 3  │ Rahul   │ r@test.com   │    │ 3  │ 3           │ 299      │ shipped │
│ 4  │ Sneha   │ s@test.com   │    └────┴─────────────┴──────────┴─────────┘
└────┴─────────┴──────────────┘    
                                    Note: Customer 2 (Priya) has NO orders
                                    Note: Customer 4 (Sneha) has NO orders

INNER JOIN: (only customers WITH orders)
┌─────────┬──────────┬─────────┐
│ name    │ total    │ status  │  ← Only Nishant (2 orders) and Rahul (1 order)
├─────────┼──────────┼─────────┤  ← Priya and Sneha are EXCLUDED
│ Nishant │ 79999    │ shipped │
│ Nishant │ 2499     │ pending │
│ Rahul   │ 299      │ shipped │
└─────────┴──────────┴─────────┘

LEFT JOIN: (all customers, even without orders)
┌─────────┬──────────┬─────────┐
│ name    │ total    │ status  │  ← ALL customers included
├─────────┼──────────┼─────────┤  ← Priya and Sneha show NULL
│ Nishant │ 79999    │ shipped │
│ Nishant │ 2499     │ pending │
│ Priya   │ NULL     │ NULL    │  ← No orders → NULL
│ Rahul   │ 299      │ shipped │
│ Sneha   │ NULL     │ NULL    │  ← No orders → NULL
└─────────┴──────────┴─────────┘
```

### E-Commerce Schema Relationships

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│ categories │     │  products  │     │order_items │
│ ──────────── │     │ ──────────── │     │ ──────────── │
│ id ◄───────│─────│ category_id│     │ product_id │──▶ products.id
│ name       │     │ id         │◄────│ order_id   │──▶ orders.id
│            │     │ name       │     │ quantity   │
│            │     │ price      │     │ unit_price │
└────────────┘     └────────────┘     └────────────┘
                                             │
┌────────────┐     ┌────────────┐            │
│ customers  │     │   orders   │            │
│ ──────────── │     │ ──────────── │            │
│ id ◄───────│─────│ customer_id│            │
│ name       │     │ id ◄───────│────────────┘
│ email      │     │ total      │
│            │     │ status     │
└────────────┘     └────────────┘
```

---

## Syntax

```sql
-- ============================================
-- INNER JOIN (most common)
-- Returns only rows with matches in BOTH tables
-- ============================================

-- Products with their category names
SELECT p.name, p.price, c.name AS category
FROM products p
INNER JOIN categories c ON p.category_id = c.id;

-- Orders with customer info
SELECT o.id, o.total_amount, o.status, c.name AS customer, c.email
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;

-- Short form (JOIN = INNER JOIN)
SELECT p.name, c.name AS category
FROM products p
JOIN categories c ON p.category_id = c.id;


-- ============================================
-- LEFT JOIN (LEFT OUTER JOIN)
-- Returns ALL rows from left table + matching from right
-- ============================================

-- All products, even without a category
SELECT p.name, p.price, c.name AS category
FROM products p
LEFT JOIN categories c ON p.category_id = c.id;
-- Products without a category show NULL for category

-- All customers and their order count (including those with 0 orders)
SELECT c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;


-- ============================================
-- RIGHT JOIN (RIGHT OUTER JOIN)
-- Returns ALL rows from right table + matching from left
-- ============================================

-- All categories, even those without products
SELECT c.name AS category, p.name AS product
FROM products p
RIGHT JOIN categories c ON p.category_id = c.id;


-- ============================================
-- CROSS JOIN (Cartesian product)
-- Every row from A combined with every row from B
-- ============================================
SELECT c.name AS customer, p.name AS product
FROM customers c
CROSS JOIN products p;
-- 4 customers × 5 products = 20 rows!
-- Rarely used, but useful for generating combinations


-- ============================================
-- SELF JOIN (join a table with itself)
-- ============================================

-- Find employees and their managers (if employees table had manager_id)
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;


-- ============================================
-- MULTI-TABLE JOINS (3+ tables)
-- ============================================

-- Order details: customer + products + quantities
SELECT 
  o.id AS order_id,
  c.name AS customer,
  p.name AS product,
  oi.quantity,
  oi.unit_price,
  oi.quantity * oi.unit_price AS line_total
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.status = 'shipped'
ORDER BY o.id, p.name;


-- Full order with category
SELECT 
  o.id AS order_id,
  c.name AS customer,
  p.name AS product,
  cat.name AS category,
  oi.quantity,
  oi.unit_price,
  o.total_amount,
  o.status
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
LEFT JOIN categories cat ON p.category_id = cat.id
ORDER BY o.order_date DESC;
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Mongoose populate (What You Know) ==========

// Populate one level
const orders = await Order.find()
  .populate('customer', 'name email')  // Like LEFT JOIN
  .populate('items.product', 'name price');

// Multiple queries approach
const order = await Order.findById(orderId);
const customer = await Customer.findById(order.customerId);
const items = await OrderItem.find({ orderId }).populate('product');

// $lookup in aggregation
const result = await Order.aggregate([
  { $lookup: {
    from: 'customers',
    localField: 'customerId',
    foreignField: '_id',
    as: 'customer'
  }},
  { $unwind: '$customer' }
]);
```

```sql
-- ========== MySQL JOIN ==========

-- Single query does it all!
SELECT 
  o.id, o.total_amount, o.status,
  c.name AS customer_name, c.email,
  p.name AS product_name, p.price,
  oi.quantity
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;

-- vs MongoDB that needs:
-- 1. Find order
-- 2. Find customer by customerId  
-- 3. Find order items
-- 4. Find products for each item
-- = 4 database calls vs 1 SQL query!
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Get order with all details (single query!)
app.get('/api/orders/:id', async (req, res) => {
  try {
    const [rows] = await pool.query(`
      SELECT 
        o.id AS order_id,
        o.order_date,
        o.status,
        o.total_amount,
        c.id AS customer_id,
        c.name AS customer_name,
        c.email AS customer_email,
        p.id AS product_id,
        p.name AS product_name,
        oi.quantity,
        oi.unit_price,
        oi.quantity * oi.unit_price AS line_total,
        cat.name AS category
      FROM orders o
      JOIN customers c ON o.customer_id = c.id
      JOIN order_items oi ON o.id = oi.order_id
      JOIN products p ON oi.product_id = p.id
      LEFT JOIN categories cat ON p.category_id = cat.id
      WHERE o.id = ?
    `, [req.params.id]);

    if (rows.length === 0) {
      return res.status(404).json({ error: 'Order not found' });
    }

    // Reshape flat rows into nested JSON (like Mongoose populate output)
    const order = {
      id: rows[0].order_id,
      orderDate: rows[0].order_date,
      status: rows[0].status,
      totalAmount: rows[0].total_amount,
      customer: {
        id: rows[0].customer_id,
        name: rows[0].customer_name,
        email: rows[0].customer_email
      },
      items: rows.map(row => ({
        product: {
          id: row.product_id,
          name: row.product_name,
          category: row.category
        },
        quantity: row.quantity,
        unitPrice: row.unit_price,
        lineTotal: row.line_total
      }))
    };

    res.json(order);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize (almost identical to Mongoose) ==========

// Define associations first (like Mongoose refs)
Customer.hasMany(Order, { foreignKey: 'customer_id' });
Order.belongsTo(Customer, { foreignKey: 'customer_id' });
Order.hasMany(OrderItem, { foreignKey: 'order_id' });
OrderItem.belongsTo(Order, { foreignKey: 'order_id' });
OrderItem.belongsTo(Product, { foreignKey: 'product_id' });
Product.belongsTo(Category, { foreignKey: 'category_id' });

// Then use include (like populate!)
const order = await Order.findByPk(1, {
  include: [
    { model: Customer, attributes: ['name', 'email'] },
    { 
      model: OrderItem,
      include: [
        { 
          model: Product, 
          attributes: ['name', 'price'],
          include: [{ model: Category, attributes: ['name'] }]
        }
      ]
    }
  ]
});
// Sequelize generates the JOIN SQL automatically!
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Customer order history page

```sql
-- SQL: Get order history for a customer
SELECT 
  o.id AS order_id,
  o.order_date,
  o.status,
  o.total_amount,
  GROUP_CONCAT(p.name SEPARATOR ', ') AS products,
  SUM(oi.quantity) AS total_items
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.customer_id = ?
GROUP BY o.id, o.order_date, o.status, o.total_amount
ORDER BY o.order_date DESC;
```

```js
// Express API — Customer order history
app.get('/api/customers/:id/orders', async (req, res) => {
  try {
    const [orders] = await pool.query(`
      SELECT 
        o.id AS order_id,
        o.order_date,
        o.status,
        o.total_amount,
        GROUP_CONCAT(p.name SEPARATOR ', ') AS products,
        SUM(oi.quantity) AS total_items
      FROM orders o
      JOIN order_items oi ON o.id = oi.order_id
      JOIN products p ON oi.product_id = p.id
      WHERE o.customer_id = ?
      GROUP BY o.id, o.order_date, o.status, o.total_amount
      ORDER BY o.order_date DESC
    `, [req.params.id]);
    
    res.json({ orders });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// React — Order History Component
import { useState, useEffect } from 'react';
import axios from 'axios';

function OrderHistory({ customerId }) {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    axios.get(`/api/customers/${customerId}/orders`)
      .then(({ data }) => setOrders(data.orders));
  }, [customerId]);

  const statusColors = {
    pending: '#f39c12', processing: '#3498db',
    shipped: '#9b59b6', delivered: '#2ecc71', cancelled: '#e74c3c'
  };

  return (
    <div>
      <h2>Order History</h2>
      {orders.length === 0 ? <p>No orders yet.</p> : (
        orders.map(order => (
          <div key={order.order_id} style={{
            border: '1px solid #ddd', padding: '16px', marginBottom: '12px', borderRadius: '8px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <strong>Order #{order.order_id}</strong>
              <span style={{ color: statusColors[order.status], fontWeight: 'bold' }}>
                {order.status.toUpperCase()}
              </span>
            </div>
            <p>Date: {new Date(order.order_date).toLocaleDateString()}</p>
            <p>Items: {order.products} ({order.total_items} items)</p>
            <p><strong>Total: ₹{order.total_amount}</strong></p>
          </div>
        ))
      )}
    </div>
  );
}
```

**Output:**
```json
{
  "orders": [
    {
      "order_id": 1,
      "order_date": "2024-01-15T00:00:00.000Z",
      "status": "shipped",
      "total_amount": "82498.00",
      "products": "iPhone 15, Levi's Jeans",
      "total_items": 2
    }
  ]
}
```

---

## Impact

| If You Don't Understand JOINs...         | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| Use multiple queries instead of JOINs    | N+1 problem — 100 orders = 101 queries          |
| Use wrong JOIN type                      | Missing data (INNER) or unexpected NULLs (LEFT) |
| Forget ON condition                      | Cartesian product — millions of useless rows     |
| JOIN without indexes on FK columns       | Extremely slow queries on large tables           |
| Don't alias tables in multi-JOIN         | Ambiguous column errors, unreadable queries      |

### N+1 Query Problem (Common in MongoDB, solved by JOINs)

```
MongoDB approach (N+1 problem):
Query 1: Get all orders       → 1 query
Query 2-101: Get each customer → 100 queries
Total: 101 database calls!

SQL approach (JOIN):
Query 1: SELECT ... FROM orders JOIN customers ON ...
Total: 1 database call!

JOINs solve the N+1 problem by design.
```

---

## Practice Exercises

### Easy (SQL)
1. Write a query to get all products with their category names using INNER JOIN
2. Get all customers and their order count using LEFT JOIN + GROUP BY
3. Find orders that have no order items (using LEFT JOIN + WHERE IS NULL)

### Medium (SQL + Node.js)
4. Build a `/api/orders/:id` endpoint that returns order details with customer info and item list using JOINs
5. Write a query that shows every customer and their total spending (including $0 for those with no orders)
6. Get the top 5 best-selling products using JOINs with order_items

### Hard (Full Stack)
7. Build a complete order management page:
   - List orders with customer names and product previews
   - Click an order to see full details (customer, items, totals)
   - Filter by status, date range, customer
8. Implement a "Customers who bought X also bought Y" recommendation system using self-JOIN on order_items

---

## Real-World Q&A

**Q1:** Mongoose's `populate()` does multiple queries behind the scenes. Are SQL JOINs faster?
**A:** Yes, significantly. `populate()` sends N+1 queries to MongoDB. A SQL JOIN runs as a single query with the database engine optimizing the join algorithm (hash join, merge join, nested loop). For 100 orders with customer data: Mongoose = 101 queries, SQL = 1 query.

**Q2:** When should I use LEFT JOIN vs INNER JOIN?
**A:** Use INNER JOIN when you only want rows that have matches in both tables (e.g., orders with customers). Use LEFT JOIN when you want ALL rows from the left table, even without matches (e.g., all customers, including those with 0 orders). In API development, LEFT JOIN is safer because it doesn't silently drop data.

**Q3:** Can I JOIN more than 2 tables?
**A:** Yes! You can chain as many JOINs as needed. The e-commerce query joining orders → customers → order_items → products → categories uses 4 JOINs. Each JOIN adds more data. Performance degrades with many JOINs on large tables — use indexes on all FK columns.

---

## Interview Q&A

**Q1: Explain the different types of JOINs with examples.**
INNER JOIN returns only matching rows from both tables. LEFT JOIN returns all rows from the left table plus matching from right (NULLs for non-matching). RIGHT JOIN is the opposite. FULL OUTER JOIN returns all rows from both tables (MySQL doesn't support it natively — use UNION of LEFT and RIGHT JOIN). CROSS JOIN returns the Cartesian product.

**Q2: What is the N+1 query problem and how do JOINs solve it?**
N+1 occurs when you query a list (1 query) then query related data for each item (N queries). Example: 100 orders + 100 customer lookups = 101 queries. A JOIN solves this with a single query: `SELECT * FROM orders JOIN customers ON...`. In Mongoose, `populate()` causes N+1; in SQL, JOINs are the default solution.

**Q3: Write a query to find customers who have never placed an order.**
`SELECT c.* FROM customers c LEFT JOIN orders o ON c.id = o.customer_id WHERE o.id IS NULL;` LEFT JOIN includes all customers, and WHERE IS NULL filters to only those without matching orders.

**Q4: What happens if you forget the ON clause in a JOIN?**
Without ON, it becomes a CROSS JOIN (Cartesian product): every row from table A combines with every row from table B. 1000 customers × 1000 orders = 1,000,000 rows! Always specify the join condition.

**Q5: How would you optimize a slow JOIN query?**
(1) Add indexes on all columns used in ON conditions (foreign keys). (2) Select only needed columns instead of SELECT *. (3) Add WHERE conditions to filter early. (4) Use EXPLAIN to see the query plan. (5) For very large tables, consider denormalization or materialized views. (6) Ensure the join order is optimal (MySQL usually optimizes this automatically).

---

| [← Previous: Group By & Having](./10_Group_By_And_Having.md) | [Next: Subqueries →](./12_Subqueries.md) |
|---|---|
