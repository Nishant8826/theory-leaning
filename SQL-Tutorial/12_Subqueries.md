# Subqueries

> 📌 **File:** `12_Subqueries.md` | **Level:** Beginner → MERN Developer

---

## What is it?

A subquery is a query nested inside another query. It's like calling an async function inside another async function — the inner one executes first, and its result is used by the outer query.

Subqueries can appear in SELECT, FROM, WHERE, and HAVING clauses.

---

## MERN Parallel — You Already Know This!

| JavaScript/Mongoose (You Know)                     | SQL Subquery (You'll Learn)                     |
|----------------------------------------------------|-------------------------------------------------|
| `const maxPrice = await Product.findOne().sort({price:-1})` then use `maxPrice` in another query | `WHERE price = (SELECT MAX(price) FROM products)` |
| Nested `.find()` calls                             | Subquery in WHERE                               |
| `$lookup` + `$match` pipeline                      | JOIN with subquery                              |
| Callback/Promise chaining                          | Nested SELECTs                                  |
| `array.filter(item => relatedArray.includes(...))`  | `WHERE id IN (SELECT ...)`                     |

---

## Why does it matter?

- Some queries are impossible without subqueries (e.g., "find products priced above average")
- Subqueries break complex problems into smaller steps (like decomposing functions)
- Understanding subqueries vs JOINs helps you choose the optimal approach
- Correlated subqueries enable row-by-row comparisons
- Common in interview questions: "find the second highest salary"

---

## How does it work?

### Subquery Execution

```
Outer Query:  SELECT * FROM products WHERE price > (__________)
                                                       │
Inner Query:                              SELECT AVG(price) FROM products
                                                       │
                                                       ▼
                                               Returns: 44519.40
                                                       │
                                                       ▼
Final Query:  SELECT * FROM products WHERE price > 44519.40
```

### Types of Subqueries

```
┌──────────────────────────────────────────────────────────────┐
│                    SUBQUERY TYPES                            │
├────────────────┬─────────────────────────────────────────────┤
│ Scalar         │ Returns single value (one row, one column)  │
│                │ WHERE price = (SELECT MAX(price) FROM ...)  │
├────────────────┼─────────────────────────────────────────────┤
│ Row            │ Returns single row with multiple columns    │
│                │ WHERE (name, age) = (SELECT ...)            │
├────────────────┼─────────────────────────────────────────────┤
│ Table          │ Returns multiple rows and columns           │
│                │ FROM (SELECT ... ) AS subquery              │
├────────────────┼─────────────────────────────────────────────┤
│ Correlated     │ References outer query (runs per row)       │
│                │ WHERE price > (SELECT AVG(...) WHERE cat=..)│
└────────────────┴─────────────────────────────────────────────┘
```

---

## Visual Diagram

```
Scalar Subquery:                    Table Subquery (Derived Table):
┌─────────────────────┐            ┌──────────────────────────────┐
│ SELECT * FROM prods │            │ SELECT * FROM                │
│ WHERE price = (     │            │   (SELECT cat_id,            │
│   ┌───────────────┐ │            │    AVG(price) AS avg         │
│   │ SELECT MAX()  │ │            │    FROM products             │
│   │ Returns: 114900│ │            │    GROUP BY cat_id) AS stats │
│   └───────────────┘ │            │ WHERE avg > 10000            │
│ )                   │            └──────────────────────────────┘
└─────────────────────┘

IN Subquery:                        EXISTS Subquery:
┌─────────────────────┐            ┌──────────────────────────────┐
│ SELECT * FROM custs │            │ SELECT * FROM customers c    │
│ WHERE id IN (       │            │ WHERE EXISTS (               │
│   ┌───────────────┐ │            │   ┌───────────────────────┐  │
│   │ SELECT cust_id│ │            │   │ SELECT 1 FROM orders  │  │
│   │ FROM orders   │ │            │   │ WHERE customer_id =   │  │
│   │ Returns:1,2,3 │ │            │   │ c.id  ← References   │  │
│   └───────────────┘ │            │   │    outer query!       │  │
│ )                   │            │   └───────────────────────┘  │
└─────────────────────┘            └──────────────────────────────┘
```

---

## Syntax

```sql
-- ============================================
-- SCALAR SUBQUERY (returns single value)
-- ============================================

-- Product with the highest price
SELECT * FROM products WHERE price = (SELECT MAX(price) FROM products);

-- Products priced above average
SELECT * FROM products WHERE price > (SELECT AVG(price) FROM products);

-- Customer who placed the most recent order
SELECT * FROM customers WHERE id = (
  SELECT customer_id FROM orders ORDER BY order_date DESC LIMIT 1
);

-- ============================================
-- IN SUBQUERY (returns a list of values)
-- ============================================

-- Customers who have placed orders
SELECT * FROM customers WHERE id IN (
  SELECT DISTINCT customer_id FROM orders
);

-- Products that have been ordered
SELECT * FROM products WHERE id IN (
  SELECT DISTINCT product_id FROM order_items
);

-- Products in categories that have more than 3 products
SELECT * FROM products WHERE category_id IN (
  SELECT category_id FROM products GROUP BY category_id HAVING COUNT(*) > 3
);

-- NOT IN — customers who have NEVER ordered
SELECT * FROM customers WHERE id NOT IN (
  SELECT DISTINCT customer_id FROM orders
);

-- ============================================
-- EXISTS SUBQUERY (checks if rows exist)
-- ============================================

-- Customers who have at least one order (same as IN but often faster)
SELECT * FROM customers c WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.id
);

-- Customers without orders
SELECT * FROM customers c WHERE NOT EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.id
);

-- ============================================
-- DERIVED TABLE (subquery in FROM)
-- ============================================

-- Average of category averages
SELECT ROUND(AVG(avg_price), 2) AS avg_of_averages
FROM (
  SELECT category_id, AVG(price) AS avg_price
  FROM products
  GROUP BY category_id
) AS category_stats;

-- Top spending customers
SELECT * FROM (
  SELECT 
    c.name,
    SUM(o.total_amount) AS total_spent,
    COUNT(o.id) AS order_count
  FROM customers c
  JOIN orders o ON c.id = o.customer_id
  GROUP BY c.id, c.name
) AS customer_spending
WHERE total_spent > 50000
ORDER BY total_spent DESC;

-- ============================================
-- CORRELATED SUBQUERY (references outer query)
-- ============================================

-- Products priced above their category average
SELECT p.name, p.price, p.category_id
FROM products p
WHERE p.price > (
  SELECT AVG(p2.price) FROM products p2 WHERE p2.category_id = p.category_id
);
-- This runs the inner query once per row in the outer query!

-- Most expensive product in each category
SELECT p.name, p.price, p.category_id
FROM products p
WHERE p.price = (
  SELECT MAX(p2.price) FROM products p2 WHERE p2.category_id = p.category_id
);

-- ============================================
-- SUBQUERY in SELECT (scalar subquery in column list)
-- ============================================
SELECT 
  c.name,
  c.email,
  (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS order_count,
  (SELECT COALESCE(SUM(o.total_amount), 0) FROM orders o WHERE o.customer_id = c.id) AS total_spent
FROM customers c;
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Mongoose (What You Know) ==========

// Products priced above average (2 queries)
const avgResult = await Product.aggregate([
  { $group: { _id: null, avg: { $avg: '$price' } } }
]);
const avgPrice = avgResult[0].avg;
const expensiveProducts = await Product.find({ price: { $gt: avgPrice } });

// Customers who have ordered (2 queries + filter)
const customerIdsWithOrders = await Order.distinct('customerId');
const activeCustomers = await Customer.find({ _id: { $in: customerIdsWithOrders } });
```

```sql
-- ========== MySQL (Single Query!) ==========

-- Products priced above average (1 query)
SELECT * FROM products WHERE price > (SELECT AVG(price) FROM products);

-- Customers who have ordered (1 query)
SELECT * FROM customers WHERE id IN (SELECT DISTINCT customer_id FROM orders);
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Products above average price
const [aboveAvg] = await pool.query(`
  SELECT name, price,
    (SELECT ROUND(AVG(price), 2) FROM products) AS avg_price
  FROM products
  WHERE price > (SELECT AVG(price) FROM products)
  ORDER BY price DESC
`);

// Customers with no orders
const [inactiveCustomers] = await pool.query(`
  SELECT c.id, c.name, c.email
  FROM customers c
  WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
  )
`);

// Customer stats using subqueries in SELECT
const [customerStats] = await pool.query(`
  SELECT 
    c.name,
    c.email,
    (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.id) AS order_count,
    (SELECT COALESCE(SUM(o.total_amount), 0) FROM orders o WHERE o.customer_id = c.id) AS total_spent
  FROM customers c
  ORDER BY total_spent DESC
`);
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize ==========
const { Op, literal } = require('sequelize');

// Products above average — using literal subquery
const products = await Product.findAll({
  where: {
    price: { [Op.gt]: literal('(SELECT AVG(price) FROM products)') }
  }
});

// Customers with orders — using subquery
const activeCustomers = await Customer.findAll({
  where: {
    id: { [Op.in]: literal('(SELECT DISTINCT customer_id FROM orders)') }
  }
});

// Note: Complex subqueries in Sequelize often require literal() or raw queries
// This is one area where raw SQL is cleaner than ORM
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Product recommendations — "Products frequently bought together"

```sql
-- SQL: Find products bought by customers who bought product X
SELECT p.id, p.name, p.price, COUNT(*) AS co_purchase_count
FROM products p
JOIN order_items oi ON p.id = oi.product_id
WHERE oi.order_id IN (
  -- Orders that contain the target product
  SELECT order_id FROM order_items WHERE product_id = ?
)
AND p.id != ?   -- Exclude the target product itself
GROUP BY p.id, p.name, p.price
ORDER BY co_purchase_count DESC
LIMIT 5;
```

```js
// Node.js + Express
app.get('/api/products/:id/recommendations', async (req, res) => {
  try {
    const productId = req.params.id;
    
    const [recommendations] = await pool.query(`
      SELECT p.id, p.name, p.price, COUNT(*) AS co_purchase_count
      FROM products p
      JOIN order_items oi ON p.id = oi.product_id
      WHERE oi.order_id IN (
        SELECT order_id FROM order_items WHERE product_id = ?
      )
      AND p.id != ?
      GROUP BY p.id, p.name, p.price
      ORDER BY co_purchase_count DESC
      LIMIT 5
    `, [productId, productId]);
    
    res.json({ productId, recommendations });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// React Component
function ProductRecommendations({ productId }) {
  const [recs, setRecs] = useState([]);

  useEffect(() => {
    axios.get(`/api/products/${productId}/recommendations`)
      .then(({ data }) => setRecs(data.recommendations));
  }, [productId]);

  return (
    <div>
      <h3>Frequently Bought Together</h3>
      {recs.map(p => (
        <div key={p.id}>
          <strong>{p.name}</strong> — ₹{p.price}
          <small> ({p.co_purchase_count} co-purchases)</small>
        </div>
      ))}
    </div>
  );
}
```

**Output:**
```json
{
  "productId": "1",
  "recommendations": [
    { "id": 5, "name": "AirPods Pro", "price": "24900.00", "co_purchase_count": 15 },
    { "id": 2, "name": "MacBook Air M3", "price": "114900.00", "co_purchase_count": 8 }
  ]
}
```

---

## Impact

| If You Don't Understand Subqueries...    | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| Use multiple round-trip queries          | 3x slower — subquery does it in one call         |
| Use correlated subquery when JOIN works  | N× slower — subquery runs per row                |
| Forget NOT IN handles NULLs differently  | Wrong results — NOT IN with NULL returns empty!  |
| Don't know when to use EXISTS vs IN     | Performance issues on large datasets              |

### NOT IN Trap With NULLs

```sql
-- ⚠️ DANGEROUS: If subquery returns any NULL, NOT IN returns empty!
SELECT * FROM customers WHERE id NOT IN (SELECT customer_id FROM orders);
-- If any order has customer_id = NULL, this returns NO ROWS!

-- ✅ SAFE: Use NOT EXISTS instead
SELECT * FROM customers c WHERE NOT EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

---

## Practice Exercises

### Easy (SQL)
1. Find the most expensive product using a subquery
2. Find all products priced above the average
3. Find customers who have placed at least one order (using IN subquery)

### Medium (SQL + Node.js)
4. Build an API that finds products that have never been ordered
5. Write a query to find the second most expensive product using a subquery
6. Get each customer's latest order using a correlated subquery

### Hard (Full Stack)
7. Build a "Customers Also Bought" recommendation engine using subqueries
8. Implement a leaderboard: rank customers by total spending, show percentile using subqueries

---

## Real-World Q&A

**Q1:** When should I use a subquery vs a JOIN?
**A:** Use JOINs when you need columns from both tables. Use subqueries when you need a value/list from one table to filter another. JOINs are usually faster for related-data retrieval. Subqueries are cleaner for "find rows where condition depends on aggregate of another table."

**Q2:** Are correlated subqueries always slow?
**A:** They run once per outer row, so they can be O(n²). But MySQL's optimizer can sometimes convert them to JOINs. For small tables, the difference is negligible. For large tables, rewrite as a JOIN if possible.

**Q3:** Can I nest subqueries inside subqueries?
**A:** Yes, MySQL supports deep nesting. But deeply nested subqueries are hard to read and optimize. If you go beyond 2 levels deep, consider using CTEs (`WITH` clause) or temporary tables for clarity.

---

## Interview Q&A

**Q1: What is a subquery? Give types.**
A subquery is a query nested inside another SQL statement. Types: Scalar (returns single value), Row (returns single row), Table/Derived (returns result set, used in FROM), Correlated (references outer query, runs per row), Non-correlated (independent, runs once).

**Q2: What is the difference between a correlated and non-correlated subquery?**
Non-correlated: independent of outer query, executes once, result is reused. Example: `WHERE price > (SELECT AVG(price) FROM products)`. Correlated: references outer query columns, executes once per outer row. Example: `WHERE price > (SELECT AVG(price) FROM products p2 WHERE p2.category_id = p.category_id)`. Correlated is slower but more powerful.

**Q3: When would you choose EXISTS over IN?**
EXISTS is better when checking for existence in large tables (stops at first match). IN is better for small lists. EXISTS handles NULLs correctly; NOT IN with NULLs can return empty results unexpectedly. Rule of thumb: use EXISTS for correlated checks, IN for value lists.

**Q4: Write a query to find the Nth highest salary.**
`SELECT DISTINCT salary FROM employees e1 WHERE N-1 = (SELECT COUNT(DISTINCT salary) FROM employees e2 WHERE e2.salary > e1.salary);` Or simpler: `SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET N-1;`

**Q5: Can a subquery in SELECT return multiple rows?**
No — a scalar subquery in SELECT must return exactly one value. `SELECT (SELECT name FROM products)` would error if products has multiple rows. Use `LIMIT 1` or ensure the subquery filters to one row.

---

| [← Previous: Joins](./11_Joins.md) | [Next: Views →](./13_Views.md) |
|---|---|
