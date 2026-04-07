# Stored Procedures

> 📌 **File:** `16_Stored_Procedures.md` | **Level:** Beginner → MERN Developer

---

## What is it?

A **stored procedure** is a saved set of SQL statements that you can call by name — like a function in JavaScript. Instead of sending multiple queries from your Node.js app, you call one procedure and the database executes the entire logic internally.

Think of it as moving your business logic from Express routes into the database itself.

---

## MERN Parallel — You Already Know This!

| MERN (You Know)                               | MySQL Stored Procedure (You'll Learn)           |
|------------------------------------------------|-------------------------------------------------|
| `async function placeOrder(customerId) {...}`  | `CREATE PROCEDURE PlaceOrder(IN p_cust_id INT)` |
| Function parameters                           | `IN`, `OUT`, `INOUT` parameters                 |
| `return result`                                | `OUT` parameter or `SELECT` result              |
| Express controller function                    | Stored procedure                                |
| Middleware chain                               | Procedure calling other procedures              |
| `try/catch` error handling                     | `DECLARE ... HANDLER` for errors                |

---

## Why does it matter?

- **Performance**: Multiple queries run inside the database — no network round-trips
- **Security**: Application only needs EXECUTE permission, not direct table access
- **Consistency**: Same business logic enforced regardless of which app calls it
- **Reduced network traffic**: One CALL replaces multiple queries
- **Encapsulation**: Change the procedure without changing application code

---

## How does it work?

```
Without Stored Procedure:             With Stored Procedure:
App → Query 1 → DB → Result          App → CALL PlaceOrder(1, items)
App → Query 2 → DB → Result                      │
App → Query 3 → DB → Result                      ▼
App → Query 4 → DB → Result          DB internally runs:
                                        Query 1 → Query 2 →
4 network round trips                  Query 3 → Query 4
                                      → Returns final result
                                      
                                      1 network round trip!
```

---

## Visual Diagram

```
Stored Procedure Structure:
┌──────────────────────────────────────────────┐
│ PROCEDURE PlaceOrder                         │
│ ┌──────────────────────────────────────────┐ │
│ │ Parameters:                              │ │
│ │   IN  p_customer_id INT                  │ │
│ │   IN  p_product_id  INT                  │ │
│ │   IN  p_quantity    INT                  │ │
│ │   OUT p_order_id    INT                  │ │
│ │   OUT p_message     VARCHAR(255)         │ │
│ ├──────────────────────────────────────────┤ │
│ │ Body:                                    │ │
│ │   DECLARE variables                      │ │
│ │   START TRANSACTION                      │ │
│ │   Check stock                            │ │
│ │   IF sufficient THEN                     │ │
│ │     INSERT order                         │ │
│ │     INSERT order_item                    │ │
│ │     UPDATE stock                         │ │
│ │     COMMIT                               │ │
│ │   ELSE                                   │ │
│ │     ROLLBACK                             │ │
│ │   END IF                                 │ │
│ └──────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘

IN  = Input parameter (like function argument)
OUT = Output parameter (like return value)
INOUT = Both input and output
```

---

## Syntax

```sql
-- ============================================
-- BASIC STORED PROCEDURE
-- ============================================

-- Change delimiter (procedures contain semicolons internally)
DELIMITER //

CREATE PROCEDURE GetAllProducts()
BEGIN
  SELECT id, name, price, stock FROM products WHERE status = 'published';
END //

DELIMITER ;

-- Call it
CALL GetAllProducts();


-- ============================================
-- PROCEDURE WITH INPUT PARAMETERS
-- ============================================

DELIMITER //

CREATE PROCEDURE GetProductsByCategory(IN p_category_id INT)
BEGIN
  SELECT p.name, p.price, c.name AS category
  FROM products p
  JOIN categories c ON p.category_id = c.id
  WHERE p.category_id = p_category_id;
END //

DELIMITER ;

CALL GetProductsByCategory(1);  -- Get electronics


-- ============================================
-- PROCEDURE WITH OUTPUT PARAMETERS
-- ============================================

DELIMITER //

CREATE PROCEDURE GetProductStats(
  IN p_category_id INT,
  OUT p_count INT,
  OUT p_avg_price DECIMAL(10,2),
  OUT p_total_value DECIMAL(12,2)
)
BEGIN
  SELECT COUNT(*), ROUND(AVG(price), 2), ROUND(SUM(price * stock), 2)
  INTO p_count, p_avg_price, p_total_value
  FROM products
  WHERE category_id = p_category_id;
END //

DELIMITER ;

-- Call with output variables
CALL GetProductStats(1, @count, @avg, @total);
SELECT @count AS product_count, @avg AS avg_price, @total AS total_value;


-- ============================================
-- PROCEDURE WITH CONTROL FLOW
-- ============================================

DELIMITER //

CREATE PROCEDURE PlaceOrder(
  IN p_customer_id INT,
  IN p_product_id INT,
  IN p_quantity INT,
  OUT p_order_id INT,
  OUT p_message VARCHAR(255)
)
BEGIN
  DECLARE v_stock INT;
  DECLARE v_price DECIMAL(10,2);
  DECLARE v_total DECIMAL(10,2);
  
  -- Error handler
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    SET p_order_id = NULL;
    SET p_message = 'Error occurred. Transaction rolled back.';
  END;
  
  START TRANSACTION;
  
  -- Check stock
  SELECT stock, price INTO v_stock, v_price
  FROM products WHERE id = p_product_id FOR UPDATE;
  
  IF v_stock IS NULL THEN
    SET p_message = 'Product not found';
    ROLLBACK;
  ELSEIF v_stock < p_quantity THEN
    SET p_message = CONCAT('Insufficient stock. Available: ', v_stock);
    ROLLBACK;
  ELSE
    SET v_total = v_price * p_quantity;
    
    -- Create order
    INSERT INTO orders (customer_id, total_amount, status)
    VALUES (p_customer_id, v_total, 'pending');
    SET p_order_id = LAST_INSERT_ID();
    
    -- Add order item
    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
    VALUES (p_order_id, p_product_id, p_quantity, v_price);
    
    -- Deduct stock
    UPDATE products SET stock = stock - p_quantity WHERE id = p_product_id;
    
    COMMIT;
    SET p_message = CONCAT('Order #', p_order_id, ' placed successfully. Total: ', v_total);
  END IF;
END //

DELIMITER ;

-- Call it
CALL PlaceOrder(1, 1, 2, @orderId, @msg);
SELECT @orderId AS order_id, @msg AS message;


-- ============================================
-- DROP / SHOW PROCEDURES
-- ============================================
DROP PROCEDURE IF EXISTS GetAllProducts;
SHOW PROCEDURE STATUS WHERE Db = 'ecommerce';
SHOW CREATE PROCEDURE PlaceOrder;
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Express Controller (What You Know) ==========
async function placeOrder(req, res) {
  const { customerId, productId, quantity } = req.body;
  const connection = await pool.getConnection();
  try {
    await connection.beginTransaction();
    // ... 4 queries ...
    await connection.commit();
  } catch (err) {
    await connection.rollback();
  } finally {
    connection.release();
  }
}
```

```js
// ========== Node.js calling Stored Procedure ==========
app.post('/api/orders', async (req, res) => {
  const { customerId, productId, quantity } = req.body;
  
  try {
    // One call replaces all the transaction logic!
    await pool.query(
      'CALL PlaceOrder(?, ?, ?, @orderId, @msg)',
      [customerId, productId, quantity]
    );
    
    const [result] = await pool.query('SELECT @orderId AS orderId, @msg AS message');
    
    if (result[0].orderId) {
      res.status(201).json({
        orderId: result[0].orderId,
        message: result[0].message
      });
    } else {
      res.status(400).json({ error: result[0].message });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

---

## ORM Equivalent (Sequelize)

```js
// Sequelize doesn't have native stored procedure support
// Use raw query:
const [results] = await sequelize.query(
  'CALL PlaceOrder(:customerId, :productId, :quantity, @orderId, @msg)',
  { replacements: { customerId: 1, productId: 1, quantity: 2 } }
);

const [output] = await sequelize.query('SELECT @orderId AS orderId, @msg AS message');
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Monthly sales report procedure

```sql
DELIMITER //

CREATE PROCEDURE MonthlySalesReport(
  IN p_year INT,
  IN p_month INT
)
BEGIN
  -- Summary stats
  SELECT 
    COUNT(DISTINCT o.id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    ROUND(SUM(o.total_amount), 2) AS total_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
  FROM orders o
  WHERE YEAR(o.order_date) = p_year AND MONTH(o.order_date) = p_month
    AND o.status != 'cancelled';
  
  -- Top products
  SELECT 
    p.name,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
  FROM order_items oi
  JOIN orders o ON oi.order_id = o.id
  JOIN products p ON oi.product_id = p.id
  WHERE YEAR(o.order_date) = p_year AND MONTH(o.order_date) = p_month
    AND o.status != 'cancelled'
  GROUP BY p.id, p.name
  ORDER BY revenue DESC
  LIMIT 10;
  
  -- Category breakdown
  SELECT 
    c.name AS category,
    COUNT(DISTINCT o.id) AS orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
  FROM categories c
  JOIN products p ON c.id = p.category_id
  JOIN order_items oi ON p.id = oi.product_id
  JOIN orders o ON oi.order_id = o.id
  WHERE YEAR(o.order_date) = p_year AND MONTH(o.order_date) = p_month
    AND o.status != 'cancelled'
  GROUP BY c.id, c.name
  ORDER BY revenue DESC;
END //

DELIMITER ;
```

```js
// Node.js — Call the report procedure
app.get('/api/reports/monthly', async (req, res) => {
  const year = parseInt(req.query.year) || new Date().getFullYear();
  const month = parseInt(req.query.month) || new Date().getMonth() + 1;
  
  try {
    // Procedure returns multiple result sets
    const [results] = await pool.query('CALL MonthlySalesReport(?, ?)', [year, month]);
    
    res.json({
      period: `${year}-${String(month).padStart(2, '0')}`,
      summary: results[0][0],       // First result set
      topProducts: results[1],      // Second result set
      categoryBreakdown: results[2] // Third result set
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// React — Monthly Report Component
function MonthlyReport() {
  const [report, setReport] = useState(null);
  const [year, setYear] = useState(new Date().getFullYear());
  const [month, setMonth] = useState(new Date().getMonth() + 1);

  const loadReport = () => {
    axios.get(`/api/reports/monthly?year=${year}&month=${month}`)
      .then(({ data }) => setReport(data));
  };

  useEffect(loadReport, [year, month]);

  if (!report) return <p>Loading report...</p>;

  return (
    <div>
      <h1>Sales Report: {report.period}</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
        <div><h3>Orders</h3><p>{report.summary.total_orders}</p></div>
        <div><h3>Customers</h3><p>{report.summary.unique_customers}</p></div>
        <div><h3>Revenue</h3><p>₹{report.summary.total_revenue}</p></div>
        <div><h3>Avg Order</h3><p>₹{report.summary.avg_order_value}</p></div>
      </div>
      
      <h2>Top Products</h2>
      {report.topProducts.map((p, i) => (
        <div key={i}>#{i+1} {p.name} — {p.units_sold} sold — ₹{p.revenue}</div>
      ))}
    </div>
  );
}
```

**Output:**
```json
{
  "period": "2024-01",
  "summary": { "total_orders": 150, "unique_customers": 85, "total_revenue": "2500000.00", "avg_order_value": "16666.67" },
  "topProducts": [{ "name": "iPhone 15", "units_sold": 45, "revenue": "3599955.00" }],
  "categoryBreakdown": [{ "category": "Electronics", "orders": 120, "revenue": "2000000.00" }]
}
```

---

## Impact

| If You Don't Understand Procedures...    | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| Run 5 queries from Node.js instead of 1  | 5× network latency + can't share transaction    |
| Business logic only in Express           | Different apps may implement it differently      |
| Don't use error handlers                 | Procedure crashes without cleanup                |

---

## Practice Exercises

### Easy (SQL)
1. Create a procedure `GetCustomerById` that accepts a customer ID and returns their details
2. Create a procedure `CountProducts` with an OUT parameter for the total count
3. Call both procedures and verify the results

### Medium (SQL + Node.js)
4. Create and call the `PlaceOrder` procedure from an Express route
5. Create a `CancelOrder` procedure that restores stock and updates status
6. Create a `GetDashboardStats` procedure that returns multiple result sets

### Hard (Full Stack)
7. Build a reporting dashboard powered entirely by stored procedures
8. Compare performance: raw queries vs stored procedure for 1000 order placements

---

## Interview Q&A

**Q1: What is a stored procedure and what are its advantages?**
A stored procedure is a precompiled set of SQL statements stored in the database. Advantages: reduced network traffic, consistent business logic, security (EXECUTE permission only), performance (precompiled execution plan), and code reuse.

**Q2: What is the difference between a stored procedure and a function?**
Procedure: called with CALL, can have IN/OUT/INOUT parameters, can return multiple result sets, can use DML (INSERT/UPDATE/DELETE). Function: called in SQL expressions, MUST return a single value, can be used in SELECT/WHERE, generally read-only.

**Q3: Should business logic be in the application or in stored procedures?**
Hybrid approach is best. Use procedures for: data-intensive operations, transactions, shared logic across apps. Use application code for: HTTP handling, authentication, complex business rules, testing (procedures are harder to unit test). Most modern apps lean toward application-side logic with raw SQL or ORMs.

**Q4: What are the disadvantages of stored procedures?**
Hard to version control (not in git by default), difficult to debug, database-specific (not portable), harder to test, can become complex and unmaintainable, less familiar to JavaScript developers.

**Q5: How do you handle errors in stored procedures?**
Use `DECLARE ... HANDLER`: `DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; SET p_error = 'Error occurred'; END;`. EXIT handler stops procedure, CONTINUE handler continues. Check `SQLSTATE` for specific error types.

---

| [← Previous: Transactions](./15_Transactions.md) | [Next: Triggers →](./17_Triggers.md) |
|---|---|
