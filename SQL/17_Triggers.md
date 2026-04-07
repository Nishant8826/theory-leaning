# Triggers

> 📌 **File:** `17_Triggers.md` | **Level:** Beginner → MERN Developer

---

## What is it?

A **trigger** is a piece of SQL code that automatically runs when a specific event (INSERT, UPDATE, DELETE) happens on a table. It's the SQL equivalent of Mongoose **middleware** (`pre`/`post` hooks).

Just like `schema.pre('save', function() {...})` runs before saving a document, a MySQL trigger runs before or after a row is inserted, updated, or deleted.

---

## MERN Parallel — You Already Know This!

| Mongoose Middleware (You Know)                     | MySQL Trigger (You'll Learn)                    |
|----------------------------------------------------|-------------------------------------------------|
| `schema.pre('save', fn)`                           | `BEFORE INSERT` trigger                         |
| `schema.post('save', fn)`                          | `AFTER INSERT` trigger                          |
| `schema.pre('remove', fn)`                         | `BEFORE DELETE` trigger                         |
| `schema.post('findOneAndUpdate', fn)`              | `AFTER UPDATE` trigger                          |
| `this.modifiedPaths()`                             | `NEW.column` vs `OLD.column`                    |
| `this.isNew`                                       | `BEFORE INSERT` (row doesn't exist yet)         |
| `next()` in middleware                             | Trigger completes automatically                 |

---

## Why does it matter?

- **Automatic audit logging**: Track what changed, when, and by whom
- **Data validation**: Enforce rules the application layer might miss
- **Cascading updates**: Automatically update related data
- **Business rule enforcement**: Regardless of which app modifies the table
- **Data consistency**: Rules enforced at database level, not application level

---

## How does it work?

```
Trigger Timing × Event Matrix:
┌─────────────┬──────────┬──────────┬──────────┐
│             │ INSERT   │ UPDATE   │ DELETE   │
├─────────────┼──────────┼──────────┼──────────┤
│ BEFORE      │ ✅       │ ✅       │ ✅       │
│             │ Validate │ Validate │ Check    │
│             │ new data │ changes  │ deps     │
├─────────────┼──────────┼──────────┼──────────┤
│ AFTER       │ ✅       │ ✅       │ ✅       │
│             │ Log      │ Log      │ Cleanup  │
│             │ creation │ changes  │ log      │
└─────────────┴──────────┴──────────┴──────────┘

NEW = the new row being inserted/updated
OLD = the existing row being updated/deleted

INSERT: NEW only (no OLD — row doesn't exist yet)
UPDATE: Both NEW and OLD (can compare changes)
DELETE: OLD only (no NEW — row is being removed)
```

---

## Visual Diagram

```
BEFORE INSERT trigger:
┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│ INSERT INTO  │───▶│ TRIGGER fires │───▶│ Row actually │
│ products ... │    │ Can modify    │    │ inserted     │
│              │    │ NEW values    │    │              │
└──────────────┘    │ Can SIGNAL    │    └──────────────┘
                    │ error to stop │
                    └───────────────┘

AFTER UPDATE trigger:
┌──────────────┐    ┌──────────────┐    ┌───────────────┐
│ UPDATE       │───▶│ Row actually │───▶│ TRIGGER fires │
│ products ... │    │ updated      │    │ Can INSERT    │
│              │    │              │    │ into log table│
└──────────────┘    └──────────────┘    │ Has OLD & NEW │
                                        └───────────────┘

Audit Log Example:
products table:                    product_audit_log table:
UPDATE products                    AFTER UPDATE trigger automatically
SET price = 89999                  INSERTs:
WHERE id = 1;                      ┌─────┬──────────┬───────────┬────────┐
                                   │ id  │ old_price│ new_price │ time   │
                                   ├─────┼──────────┼───────────┼────────┤
                                   │ 1   │ 79999    │ 89999     │ NOW()  │
                                   └─────┴──────────┴───────────┴────────┘
```

---

## Syntax

```sql
-- ============================================
-- BEFORE INSERT — Validate/modify before saving
-- ============================================

DELIMITER //

-- Auto-set timestamps (like Mongoose timestamps: true)
CREATE TRIGGER before_product_insert
BEFORE INSERT ON products
FOR EACH ROW
BEGIN
  -- Ensure price is not negative
  IF NEW.price < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Price cannot be negative';
  END IF;
  
  -- Ensure stock is not negative
  IF NEW.stock < 0 THEN
    SET NEW.stock = 0;
  END IF;
  
  -- Auto-format name (capitalize first letter)
  SET NEW.name = CONCAT(UPPER(SUBSTRING(NEW.name, 1, 1)), SUBSTRING(NEW.name, 2));
END //

DELIMITER ;


-- ============================================
-- AFTER INSERT — Log new records
-- ============================================

-- First, create the audit table
CREATE TABLE product_audit (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT,
  action VARCHAR(10),
  old_price DECIMAL(10,2),
  new_price DECIMAL(10,2),
  old_stock INT,
  new_stock INT,
  changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  changed_by VARCHAR(100)
);

DELIMITER //

CREATE TRIGGER after_product_insert
AFTER INSERT ON products
FOR EACH ROW
BEGIN
  INSERT INTO product_audit (product_id, action, new_price, new_stock)
  VALUES (NEW.id, 'INSERT', NEW.price, NEW.stock);
END //

DELIMITER ;


-- ============================================
-- AFTER UPDATE — Track changes
-- ============================================

DELIMITER //

CREATE TRIGGER after_product_update
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
  -- Only log if price or stock actually changed
  IF OLD.price != NEW.price OR OLD.stock != NEW.stock THEN
    INSERT INTO product_audit (product_id, action, old_price, new_price, old_stock, new_stock)
    VALUES (NEW.id, 'UPDATE', OLD.price, NEW.price, OLD.stock, NEW.stock);
  END IF;
END //

DELIMITER ;


-- ============================================
-- BEFORE DELETE — Prevent or validate deletion
-- ============================================

DELIMITER //

CREATE TRIGGER before_product_delete
BEFORE DELETE ON products
FOR EACH ROW
BEGIN
  -- Prevent deletion of products with active orders
  DECLARE v_order_count INT;
  SELECT COUNT(*) INTO v_order_count
  FROM order_items WHERE product_id = OLD.id;
  
  IF v_order_count > 0 THEN
    SIGNAL SQLSTATE '45000' 
    SET MESSAGE_TEXT = 'Cannot delete product with existing orders';
  END IF;
  
  -- Log the deletion
  INSERT INTO product_audit (product_id, action, old_price, old_stock)
  VALUES (OLD.id, 'DELETE', OLD.price, OLD.stock);
END //

DELIMITER ;


-- ============================================
-- Auto-update order total when items change
-- ============================================

DELIMITER //

CREATE TRIGGER after_order_item_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
  UPDATE orders 
  SET total_amount = (
    SELECT SUM(quantity * unit_price) FROM order_items WHERE order_id = NEW.order_id
  )
  WHERE id = NEW.order_id;
END //

DELIMITER ;


-- ============================================
-- DROP / SHOW TRIGGERS
-- ============================================
DROP TRIGGER IF EXISTS before_product_insert;
SHOW TRIGGERS;
SHOW TRIGGERS FROM ecommerce;
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Mongoose Middleware (What You Know) ==========

// Pre-save validation
productSchema.pre('save', function(next) {
  if (this.price < 0) {
    return next(new Error('Price cannot be negative'));
  }
  if (this.stock < 0) {
    this.stock = 0;
  }
  next();
});

// Post-save audit log
productSchema.post('save', async function(doc) {
  await AuditLog.create({
    productId: doc._id,
    action: doc.isNew ? 'INSERT' : 'UPDATE',
    newPrice: doc.price,
    changedAt: new Date()
  });
});

// Pre-remove check
productSchema.pre('remove', async function(next) {
  const orderCount = await OrderItem.countDocuments({ productId: this._id });
  if (orderCount > 0) {
    return next(new Error('Cannot delete product with existing orders'));
  }
  next();
});
```

```sql
-- ========== MySQL Triggers (same behavior!) ==========

-- Pre-save validation
CREATE TRIGGER before_product_insert BEFORE INSERT ON products
FOR EACH ROW BEGIN
  IF NEW.price < 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Price cannot be negative';
  END IF;
  IF NEW.stock < 0 THEN SET NEW.stock = 0; END IF;
END;

-- Post-save audit log
CREATE TRIGGER after_product_insert AFTER INSERT ON products
FOR EACH ROW BEGIN
  INSERT INTO product_audit (product_id, action, new_price)
  VALUES (NEW.id, 'INSERT', NEW.price);
END;

-- Pre-remove check
CREATE TRIGGER before_product_delete BEFORE DELETE ON products
FOR EACH ROW BEGIN
  IF (SELECT COUNT(*) FROM order_items WHERE product_id = OLD.id) > 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete product with orders';
  END IF;
END;
```

```js
// ========== Node.js — Triggers work automatically! ==========
const pool = require('./db');

// Just do normal operations — triggers fire automatically
app.post('/api/products', async (req, res) => {
  try {
    const { name, price, stock, categoryId } = req.body;
    
    // The BEFORE INSERT trigger will:
    // 1. Validate price (throw error if negative)
    // 2. Fix negative stock to 0
    // 3. Capitalize the name
    
    const [result] = await pool.query(
      'INSERT INTO products (name, price, stock, category_id) VALUES (?, ?, ?, ?)',
      [name, price, stock, categoryId]
    );
    
    // The AFTER INSERT trigger automatically logs this to product_audit!
    
    const [product] = await pool.query('SELECT * FROM products WHERE id = ?', [result.insertId]);
    res.status(201).json(product[0]);
  } catch (error) {
    // If trigger SIGNAL'd an error, it'll be caught here
    if (error.sqlState === '45000') {
      return res.status(400).json({ error: error.message });
    }
    res.status(500).json({ error: error.message });
  }
});

// View audit log
app.get('/api/products/:id/audit', async (req, res) => {
  const [logs] = await pool.query(
    'SELECT * FROM product_audit WHERE product_id = ? ORDER BY changed_at DESC',
    [req.params.id]
  );
  res.json({ productId: req.params.id, auditLog: logs });
});
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize Hooks (like triggers but app-side) ==========

Product.beforeCreate((product) => {
  if (product.price < 0) throw new Error('Price cannot be negative');
  if (product.stock < 0) product.stock = 0;
});

Product.afterCreate(async (product) => {
  await ProductAudit.create({
    productId: product.id,
    action: 'INSERT',
    newPrice: product.price
  });
});

// Note: Sequelize hooks only fire when using Sequelize methods
// Raw SQL queries bypass them. Database triggers fire on ALL changes.
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Automatic stock alerts — trigger when stock drops below threshold

```sql
-- Stock alert table
CREATE TABLE stock_alerts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT,
  product_name VARCHAR(200),
  current_stock INT,
  alert_type ENUM('low_stock', 'out_of_stock'),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  resolved BOOLEAN DEFAULT FALSE
);

DELIMITER //

CREATE TRIGGER after_stock_update
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
  -- Only check if stock decreased
  IF NEW.stock < OLD.stock THEN
    IF NEW.stock = 0 THEN
      INSERT INTO stock_alerts (product_id, product_name, current_stock, alert_type)
      VALUES (NEW.id, NEW.name, NEW.stock, 'out_of_stock');
    ELSEIF NEW.stock < 10 AND OLD.stock >= 10 THEN
      INSERT INTO stock_alerts (product_id, product_name, current_stock, alert_type)
      VALUES (NEW.id, NEW.name, NEW.stock, 'low_stock');
    END IF;
  END IF;
END //

DELIMITER ;
```

```js
// Express — Stock alerts API
app.get('/api/admin/stock-alerts', async (req, res) => {
  const [alerts] = await pool.query(`
    SELECT * FROM stock_alerts 
    WHERE resolved = FALSE 
    ORDER BY created_at DESC
  `);
  res.json({ alerts });
});

app.patch('/api/admin/stock-alerts/:id/resolve', async (req, res) => {
  await pool.query('UPDATE stock_alerts SET resolved = TRUE WHERE id = ?', [req.params.id]);
  res.json({ message: 'Alert resolved' });
});
```

```js
// React — Stock Alert Dashboard
function StockAlerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      axios.get('/api/admin/stock-alerts').then(({ data }) => setAlerts(data.alerts));
    }, 10000); // Check every 10 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2>⚠️ Stock Alerts ({alerts.length})</h2>
      {alerts.map(alert => (
        <div key={alert.id} style={{
          padding: '12px', marginBottom: '8px', borderRadius: '8px',
          backgroundColor: alert.alert_type === 'out_of_stock' ? '#ffdddd' : '#fff3cd'
        }}>
          <strong>{alert.product_name}</strong>
          <span> — Stock: {alert.current_stock}</span>
          <span style={{ fontWeight: 'bold', color: alert.alert_type === 'out_of_stock' ? 'red' : 'orange' }}>
            {' '}{alert.alert_type === 'out_of_stock' ? '🔴 OUT OF STOCK' : '🟡 LOW STOCK'}
          </span>
          <button onClick={() => axios.patch(`/api/admin/stock-alerts/${alert.id}/resolve`)
            .then(() => setAlerts(prev => prev.filter(a => a.id !== alert.id)))}>
            Resolve
          </button>
        </div>
      ))}
    </div>
  );
}
```

**Output:**
```json
{
  "alerts": [
    {
      "id": 1, "product_id": 5, "product_name": "AirPods Pro",
      "current_stock": 3, "alert_type": "low_stock",
      "created_at": "2024-01-15T10:30:00.000Z", "resolved": false
    }
  ]
}
```

---

## Impact

| If You Don't Understand Triggers...      | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| No audit logging                         | Can't track who changed what and when            |
| Validation only in Express               | Direct database queries bypass validation        |
| No stock alerts                          | Products go out of stock without anyone knowing  |
| Don't know triggers exist                | Debug for hours wondering where data came from   |
| Too many complex triggers                | Slow INSERT/UPDATE operations, hard to debug     |

---

## Practice Exercises

### Easy (SQL)
1. Create a trigger that logs all new customer registrations to a `customer_audit` table
2. Create a BEFORE INSERT trigger that prevents inserting products with price = 0
3. Show all triggers for the products table

### Medium (SQL + Node.js)
4. Implement an audit log system with triggers for all CRUD operations on products
5. Create a trigger that auto-calculates order totals when order items change
6. Build an API that queries the audit log for a specific product's change history

### Hard (Full Stack)
7. Build a complete audit dashboard showing all database changes across all tables
8. Implement a "soft delete" trigger that moves deleted records to an archive table instead of removing them

---

## Interview Q&A

**Q1: What is a trigger and when would you use one?**
A trigger is stored SQL code that auto-executes on INSERT, UPDATE, or DELETE events. Use cases: audit logging, data validation, cascading updates, maintaining derived data, enforcing business rules at the database level. Like Mongoose pre/post middleware but at the database level.

**Q2: What is the difference between BEFORE and AFTER triggers?**
BEFORE: runs before the operation, can modify NEW values or prevent the operation (using SIGNAL). AFTER: runs after the operation, used for logging and cascading changes. BEFORE can set `NEW.column = value`; AFTER cannot modify the row.

**Q3: What are NEW and OLD in triggers?**
NEW refers to the row being inserted/updated (new values). OLD refers to the existing row being updated/deleted (previous values). INSERT has only NEW, DELETE has only OLD, UPDATE has both. In Mongoose terms: `this` (new) and checking `isModified()` for changes.

**Q4: Can a trigger call another trigger?**
Yes — this is called cascading triggers. If trigger A on table X inserts into table Y, and table Y has its own trigger, it fires too. Be careful: cascading triggers can cause infinite loops and are hard to debug.

**Q5: Should business logic be in triggers or application code?**
Keep triggers simple: validation, audit logging, simple cascading. Complex business logic should stay in the application for testability, readability, and portability. Triggers are invisible to developers and hard to debug. Use them for rules that must be enforced regardless of which application accesses the database.

---

| [← Previous: Stored Procedures](./16_Stored_Procedures.md) | [Next: Normalization →](./18_Normalization.md) |
|---|---|
