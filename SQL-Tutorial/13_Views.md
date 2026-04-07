# Views

> 📌 **File:** `13_Views.md` | **Level:** Beginner → MERN Developer

---

## What is it?

A **view** is a saved SQL query that acts like a virtual table. It doesn't store data — it runs the underlying query every time you access it. Think of it as a **reusable function** that returns a result set.

In MERN terms, it's like creating a Mongoose static method or a middleware that always returns a pre-shaped version of data.

---

## MERN Parallel — You Already Know This!

| MERN (You Know)                                    | SQL View (You'll Learn)                         |
|----------------------------------------------------|-------------------------------------------------|
| Mongoose static: `UserSchema.statics.findActive`   | `CREATE VIEW active_users AS SELECT ... WHERE active=1` |
| Mongoose virtual: `schema.virtual('fullName')`     | View with computed columns                      |
| Express middleware that filters requests            | View with WHERE clause                          |
| A service function that joins & shapes data         | View with JOINs                                 |
| GraphQL resolver returning shaped data              | View as a pre-shaped result set                 |

---

## Why does it matter?

- **Simplify complex queries** — Write the JOIN once, query the view by name
- **Security** — Expose only certain columns (hide passwords, sensitive data)
- **Abstraction** — Application code queries the view, DBA changes the underlying query
- **Consistency** — All team members use the same query/business logic
- **Access control** — Grant users access to views instead of base tables

---

## How does it work?

```
Without View:                        With View:
Every time you need this data:       Create once:
  SELECT p.name, p.price,             CREATE VIEW product_listing AS
    c.name AS category                 SELECT p.name, p.price, c.name...
  FROM products p
  JOIN categories c ON ...             Then query simply:
  WHERE p.status = 'published'         SELECT * FROM product_listing;
                                       
Repeat in 10 different routes  →     Use in all routes like a regular table
```

---

## Visual Diagram

```
Base Tables:                    View (Virtual Table):
┌──────────┐  ┌──────────┐    ┌──────────────────────────────┐
│ products │  │categories│    │ product_listing (VIEW)       │
│ ──────── │  │ ──────── │    │ ────────────────────────────── │
│ id       │  │ id       │    │ SELECT p.name, p.price,      │
│ name     │──│ name     │───▶│   c.name AS category         │
│ price    │  │          │    │ FROM products p               │
│ cat_id   │  └──────────┘    │ JOIN categories c ON ...      │
│ status   │                  │ WHERE status = 'published'    │
└──────────┘                  └──────────────────────────────┘
  Actual data                   No data stored — runs query
  on disk                       when accessed

Query: SELECT * FROM product_listing WHERE price > 10000;
       ↓
MySQL internally runs the view's query + your WHERE condition
```

---

## Syntax

```sql
-- ============================================
-- CREATE VIEW
-- ============================================

-- Simple view — published products with category
CREATE VIEW product_listing AS
SELECT 
  p.id,
  p.name,
  p.price,
  p.stock,
  c.name AS category,
  p.status,
  p.created_at
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.status = 'published';

-- Now query it like a regular table!
SELECT * FROM product_listing;
SELECT * FROM product_listing WHERE price > 10000;
SELECT * FROM product_listing WHERE category = 'Electronics';
SELECT name, price FROM product_listing ORDER BY price DESC LIMIT 5;

-- View with computed columns
CREATE VIEW product_analytics AS
SELECT 
  p.id,
  p.name,
  p.price,
  p.stock,
  p.price * p.stock AS inventory_value,
  CASE WHEN p.stock = 0 THEN 'Out of Stock'
       WHEN p.stock < 10 THEN 'Low Stock'
       ELSE 'In Stock'
  END AS stock_status,
  c.name AS category
FROM products p
LEFT JOIN categories c ON p.category_id = c.id;

-- View for customer safety (hide sensitive data)
CREATE VIEW safe_customers AS
SELECT id, name, email, created_at
FROM customers;
-- Password hash, phone, address are hidden!

-- View for order summaries
CREATE VIEW order_summary AS
SELECT 
  o.id AS order_id,
  c.name AS customer,
  c.email,
  o.total_amount,
  o.status,
  o.order_date,
  COUNT(oi.id) AS item_count,
  SUM(oi.quantity) AS total_items
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, c.name, c.email, o.total_amount, o.status, o.order_date;


-- ============================================
-- ALTER / REPLACE VIEW
-- ============================================

-- Replace (update) an existing view
CREATE OR REPLACE VIEW product_listing AS
SELECT 
  p.id, p.name, p.price, p.stock,
  c.name AS category,
  p.status,
  ROUND(p.price * 1.18, 2) AS price_with_gst  -- Added new column
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.status = 'published';


-- ============================================
-- DROP VIEW
-- ============================================
DROP VIEW product_listing;
DROP VIEW IF EXISTS product_listing;


-- ============================================
-- SHOW VIEWS
-- ============================================
SHOW FULL TABLES WHERE Table_type = 'VIEW';
SHOW CREATE VIEW product_listing;
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== MERN — Creating reusable query patterns ==========

// Mongoose Static Method (like a View)
productSchema.statics.getListing = function() {
  return this.find({ status: 'published' })
    .populate('category', 'name')
    .select('name price stock category status');
};

// Usage in route:
const products = await Product.getListing();

// Service function (another pattern)
async function getProductListing() {
  return Product.find({ status: 'published' })
    .populate('category', 'name')
    .select('name price stock');
}
```

```sql
-- ========== MySQL — Create View once, use everywhere ==========

CREATE VIEW product_listing AS
SELECT p.name, p.price, p.stock, c.name AS category
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.status = 'published';

-- Usage (just like a table!):
SELECT * FROM product_listing;
SELECT * FROM product_listing WHERE price > 10000;
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Create the view (run once, usually in migration)
await pool.query(`
  CREATE OR REPLACE VIEW product_listing AS
  SELECT 
    p.id, p.name, p.price, p.stock,
    c.name AS category,
    ROUND(p.price * 1.18, 2) AS price_with_gst
  FROM products p
  LEFT JOIN categories c ON p.category_id = c.id
  WHERE p.status = 'published'
`);

// Now use the view in all API routes (clean and simple!)
app.get('/api/products', async (req, res) => {
  const [products] = await pool.query('SELECT * FROM product_listing');
  res.json(products);
});

app.get('/api/products/expensive', async (req, res) => {
  const [products] = await pool.query(
    'SELECT * FROM product_listing WHERE price > ? ORDER BY price DESC',
    [10000]
  );
  res.json(products);
});
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize ==========

// Sequelize doesn't have native view support
// But you can define a model that maps to a view:

const ProductListing = sequelize.define('ProductListing', {
  id: { type: DataTypes.INTEGER, primaryKey: true },
  name: DataTypes.STRING,
  price: DataTypes.DECIMAL(10, 2),
  stock: DataTypes.INTEGER,
  category: DataTypes.STRING,
  priceWithGst: DataTypes.DECIMAL(10, 2)
}, {
  tableName: 'product_listing',  // Points to the VIEW
  timestamps: false,              // Views don't have timestamps
  freezeTableName: true           // Don't pluralize
});

// Usage (same as any model):
const products = await ProductListing.findAll({
  where: { price: { [Op.gt]: 10000 } }
});

// Note: You can't INSERT/UPDATE/DELETE through most views
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Dashboard views for different user roles

```sql
-- Admin view — sees everything
CREATE VIEW admin_dashboard AS
SELECT 
  o.id AS order_id,
  c.name AS customer,
  c.email,
  o.total_amount,
  o.status,
  o.order_date,
  GROUP_CONCAT(p.name SEPARATOR ', ') AS products,
  SUM(oi.quantity) AS total_items
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
GROUP BY o.id, c.name, c.email, o.total_amount, o.status, o.order_date
ORDER BY o.order_date DESC;

-- Customer view — sees only their orders (parameterized in route)
CREATE VIEW customer_order_view AS
SELECT 
  o.id AS order_id,
  o.total_amount,
  o.status,
  o.order_date,
  COUNT(oi.id) AS item_count
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, o.total_amount, o.status, o.order_date;
```

```js
// Node.js + Express — Using views
app.get('/api/admin/orders', async (req, res) => {
  // Admin sees all orders with customer details
  const [orders] = await pool.query('SELECT * FROM admin_dashboard');
  res.json({ orders });
});

app.get('/api/my-orders', async (req, res) => {
  // Customer sees only their orders
  const customerId = req.user.id; // From auth middleware
  const [orders] = await pool.query(
    `SELECT * FROM customer_order_view co
     JOIN orders o ON co.order_id = o.id
     WHERE o.customer_id = ?`,
    [customerId]
  );
  res.json({ orders });
});
```

```js
// React — Admin Dashboard using view
function AdminOrders() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    axios.get('/api/admin/orders').then(({ data }) => setOrders(data.orders));
  }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>Order ID</th><th>Customer</th><th>Email</th>
          <th>Products</th><th>Items</th><th>Total</th><th>Status</th>
        </tr>
      </thead>
      <tbody>
        {orders.map(o => (
          <tr key={o.order_id}>
            <td>#{o.order_id}</td>
            <td>{o.customer}</td>
            <td>{o.email}</td>
            <td>{o.products}</td>
            <td>{o.total_items}</td>
            <td>₹{o.total_amount}</td>
            <td>{o.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

**Output:**
```json
{
  "orders": [
    {
      "order_id": 1,
      "customer": "Nishant",
      "email": "n@test.com",
      "total_amount": "82498.00",
      "status": "shipped",
      "products": "iPhone 15, Levi's Jeans",
      "total_items": 2
    }
  ]
}
```

---

## Impact

| If You Don't Understand Views...         | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| Repeat complex JOINs in every route      | Code duplication, inconsistent results           |
| Expose base tables to all users          | Security risk — users see passwords, internal IDs |
| Change table structure without views     | Must update every query that references the table |
| Don't use views for reporting            | Reports break when schema changes                |

---

## Practice Exercises

### Easy (SQL)
1. Create a view `active_products` that shows only published products with stock > 0
2. Create a view `customer_list` that hides the password_hash column
3. Query the view with additional WHERE and ORDER BY

### Medium (SQL + Node.js)
4. Create views for your e-commerce app: `product_listing`, `order_summary`, `customer_stats`
5. Build Express routes that query views instead of writing complex JOINs
6. Create a view that shows monthly revenue summary

### Hard (Full Stack)
7. Implement role-based views: admin sees all data, customer sees only their own
8. Build a view management UI: create, modify, and drop views through the interface

---

## Real-World Q&A

**Q1:** Are views slow because they run the query every time?
**A:** Regular views re-execute on every access, but MySQL's optimizer often merges the view query with your outer query for good performance. For truly expensive queries, use **materialized views** (MySQL doesn't support natively — simulate with a table + scheduled refresh).

**Q2:** Can I INSERT/UPDATE/DELETE through a view?
**A:** Yes, for simple views (single table, no aggregates, no GROUP BY). Complex views with JOINs are usually read-only. This is a key difference from MongoDB where you always write to the base collection.

**Q3:** When should I use a view vs a stored procedure?
**A:** Views are best for read-only queries that shape data (like SELECT statements). Stored procedures are for operations with logic, parameters, variables, and flow control (IF/ELSE, loops). Views = data shaping, Procedures = business logic.

---

## Interview Q&A

**Q1: What is a view and what are its advantages?**
A view is a virtual table based on a stored SELECT query. Advantages: simplifies complex queries, provides security by hiding columns, ensures consistency across the application, and enables abstraction (change underlying query without changing application code).

**Q2: What is the difference between a view and a table?**
A table stores actual data on disk. A view stores only the query definition — data is computed on access. Tables can be INSERT/UPDATE/DELETE directly. Most views are read-only (especially complex ones). Tables use storage; views use negligible storage.

**Q3: Can you create an index on a view?**
In MySQL, no. Views don't store data, so indexes don't apply. Index the underlying base tables instead to improve view performance. Some databases (SQL Server) support indexed/materialized views.

**Q4: What is a materialized view?**
A materialized view stores the query result physically on disk (like a cached table). It provides fast reads but needs periodic refresh to stay current. MySQL doesn't support them natively — simulate by creating a table and refreshing it with a scheduled event or cron job.

**Q5: Can views be nested (view built on another view)?**
Yes, you can build views on top of other views. However, deep nesting makes debugging harder and can cause performance issues because MySQL merges and runs all underlying queries. Keep nesting to 2-3 levels maximum.

---

| [← Previous: Subqueries](./12_Subqueries.md) | [Next: Indexes →](./14_Indexes.md) |
|---|---|
