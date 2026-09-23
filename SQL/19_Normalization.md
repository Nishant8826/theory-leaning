# Normalization

> 📌 **File:** `19_Normalization.md` | **Level:** Beginner → MERN Developer

---

## What is it?

**Normalization** is the process of organizing database tables to reduce data redundancy and improve data integrity. It's the fundamental design philosophy of relational databases — splitting data into separate, related tables instead of duplicating it.

Think of it as the opposite of MongoDB's embedding pattern. In MongoDB, you embed related data inside a document. In normalized SQL, you split it into separate tables and JOIN them back together.

---

## MERN Parallel — You Already Know This!

| MongoDB Pattern (You Know)              | SQL Normalization (You'll Learn)                |
|-----------------------------------------|-------------------------------------------------|
| Embedding: `{ order: { items: [...] }}` | Separate `orders` + `order_items` tables        |
| Denormalized (duplicate data)           | Normalized (no duplicates)                      |
| Flexible schema per document            | Strict schema per table                         |
| Store category name WITH product        | Store category_id → lookup in categories table  |
| `ref + populate()` for references       | Foreign keys + JOIN                             |
| Trade storage for speed                 | Trade speed for data integrity                  |

### The MongoDB Dilemma You've Faced

```js
// MongoDB — You've probably done this:
const orderSchema = new Schema({
  customer: {
    name: 'Nishant',    // ← Copied from customers collection
    email: 'n@test.com' // ← What if customer updates email? Data is stale!
  },
  items: [{
    productName: 'iPhone', // ← Copied from products collection
    price: 79999          // ← What if price changes? Orders show old price
  }]
});
// Problem: Customer changes email → old orders still show old email
// This IS acceptable for orders (historical accuracy)
// But NOT acceptable for customer profiles, product catalogs, etc.
```

---

## Why does it matter?

- **Data integrity**: No contradictory copies of the same data
- **Storage efficiency**: Store each fact exactly once
- **Easy updates**: Change a customer's email in ONE place, reflected everywhere
- **Prevents anomalies**: Insert, update, and delete anomalies are eliminated
- **Interview essential**: Normalization forms (1NF, 2NF, 3NF) are very commonly tested

---

## How does it work?

### Normal Forms Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    NORMAL FORMS                              │
├────────┬─────────────────────────────────────────────────────┤
│  UNF   │ Unnormalized: duplicate data, repeating groups     │
│        │ Like a messy MongoDB document with embedded arrays  │
├────────┼─────────────────────────────────────────────────────┤
│  1NF   │ Each column has atomic (single) values              │
│        │ No repeating groups or arrays in a single cell      │
├────────┼─────────────────────────────────────────────────────┤
│  2NF   │ 1NF + every non-key column depends on ENTIRE PK    │
│        │ Remove partial dependencies                        │
├────────┼─────────────────────────────────────────────────────┤
│  3NF   │ 2NF + no transitive dependencies                   │
│        │ Non-key columns don't depend on other non-key cols  │
├────────┼─────────────────────────────────────────────────────┤
│  BCNF  │ Stricter 3NF: for every X → Y, X MUST be a super key│
│        │ Eliminates anomalies with overlapping candidate keys│
├────────┼─────────────────────────────────────────────────────┤
│4NF/5NF │ Removes multi-valued & join projection dependencies │
└────────┴─────────────────────────────────────────────────────┘
```

---

### Under-the-Hood Technical Deep Dive

#### 1. Functional Dependencies ($X \rightarrow Y$) & Armstrong's Axioms
A functional dependency $X \rightarrow Y$ means: *If you know the value of column $X$, there is only one possible value for column $Y$*.
* $X$ is the **Determinant** and $Y$ is the **Dependent**.
* If `email` determines `user_id` ($email \rightarrow user\_id$), `email` is a candidate key.

##### The 6 Armstrong's Axioms (Sound and Complete Inference Rules):
1. **Reflexivity Rule:** If $Y \subseteq X$, then $X \rightarrow Y$ (e.g. `{student_id, email} \rightarrow student_id`).
2. **Augmentation Rule:** If $X \rightarrow Y$, then $XZ \rightarrow YZ$ for any attribute set $Z$.
3. **Transitivity Rule:** If $X \rightarrow Y$ and $Y \rightarrow Z$, then $X \rightarrow Z$.
4. **Union Rule:** If $X \rightarrow Y$ and $X \rightarrow Z$, then $X \rightarrow YZ$.
5. **Decomposition Rule:** If $X \rightarrow YZ$, then $X \rightarrow Y$ and $X \rightarrow Z$.
6. **Pseudotransitivity Rule:** If $X \rightarrow Y$ and $WY \rightarrow Z$, then $WX \rightarrow Z$.

---

#### 2. Lossless Join vs Dependency Preservation Theorems
When decomposing a large table $R$ into smaller tables $R_1$ and $R_2$:
* **Lossless Join (Non-negotiable requirement):** Natural join $R_1 \bowtie R_2$ must equal $R$ exactly without generating phantom/spurious tuples. Mathematically guaranteed if:
  $$(R_1 \cap R_2) \rightarrow R_1 \quad \text{OR} \quad (R_1 \cap R_2) \rightarrow R_2$$
  *(i.e., the common attributes must form a Super Key in at least one decomposed table).*
* **Dependency Preservation:** Every functional dependency in $R$ can be verified by inspecting individual decomposed tables without running expensive cross-table `JOIN` constraints.
* **The Fundamental Trade-off:**
  - **3NF** ALWAYS guarantees both **Lossless Join** AND **Dependency Preservation**.
  - **BCNF** guarantees **Lossless Join** and eliminates ALL single-valued redundancy, but MAY SOMETIMES sacrifice **Dependency Preservation**!

---

#### 3. Boyce-Codd Normal Form (BCNF) Deep Dive
A table is in **BCNF** if and only if: **For every non-trivial functional dependency $X \rightarrow Y$, $X$ is a Super Key** (a primary or candidate key).

##### 🥊 3NF vs BCNF Classic Example:
Suppose a university consulting platform has table `StudentAdvising(student_id, major, advisor)`:
* **Rule 1:** A student can have multiple majors (each with one advisor).
* **Rule 2:** Each advisor advises only ONE major ($advisor \rightarrow major$).
* **Rule 3:** For a given student and major, there is only one advisor ($(student\_id, major) \rightarrow advisor$).
* **Candidate Keys:** $(student\_id, major)$ and $(student\_id, advisor)$.
* **Is it in 3NF?** YES! Because in $advisor \rightarrow major$, $major$ is part of a candidate key (prime attribute).
* **Is it in BCNF?** NO! Because $advisor$ is NOT a super key by itself!
* **The Anomaly:** If advisor Dr. Smith changes department/major, we must update multiple student rows. If no students are assigned to Dr. Smith, we can't record which major he advises!
* **BCNF Decomposition:**
  1. `AdvisorDept(advisor, major)` — Key: `advisor` (BCNF satisfied!).
  2. `StudentAdvisor(student_id, advisor)` — Key: `(student_id, advisor)` (BCNF satisfied!).

---

#### 4. Strategic Denormalization in Production
While 3NF eliminates all data redundancy, extreme normalization requires joining 8+ tables for every page load.
* **When to Denormalize:** Read-heavy dashboards where join latency is unacceptable (e.g., storing `order_total` in the `orders` table instead of calculating `SUM(price * quantity)` across 5 million `order_items` on every page refresh).
* **Guarding Denormalized Consistency:** Maintain pre-computed totals using atomic database triggers, background cron workers, or cached summaries in **Redis**.

---

---

## Visual Diagram

### Unnormalized → 1NF → 2NF → 3NF

```
UNNORMALIZED (one messy table):
┌────┬─────────┬──────────────┬──────────────────┬────────────────┬──────────┐
│ id │ cust    │ cust_email   │ items            │ item_prices    │ city     │
├────┼─────────┼──────────────┼──────────────────┼────────────────┼──────────┤
│ 1  │ Nishant │ n@test.com   │ iPhone, AirPods  │ 79999, 24900   │ Delhi    │
│ 2  │ Priya   │ p@test.com   │ Jeans            │ 2499           │ Mumbai   │
└────┴─────────┴──────────────┴──────────────────┴────────────────┴──────────┘
Problems: ❌ Multiple values in one cell (items, prices)
          ❌ Customer data repeated if they order again
          ❌ Can't query individual items easily

═══════════════════════════════════════════════════════════════════

1NF (atomic values — no arrays in cells):
┌────┬─────────┬──────────────┬──────────┬──────────┬──────────┐
│ id │ cust    │ cust_email   │ item     │ price    │ city     │
├────┼─────────┼──────────────┼──────────┼──────────┼──────────┤
│ 1  │ Nishant │ n@test.com   │ iPhone   │ 79999    │ Delhi    │
│ 1  │ Nishant │ n@test.com   │ AirPods  │ 24900    │ Delhi    │
│ 2  │ Priya   │ p@test.com   │ Jeans    │ 2499     │ Mumbai   │
└────┴─────────┴──────────────┴──────────┴──────────┴──────────┘
Fixed: ✅ Each cell has one value
Still: ❌ Customer data duplicated (Nishant appears twice)

═══════════════════════════════════════════════════════════════════

2NF (remove partial dependencies → separate tables):
┌──────────────────┐     ┌──────────────────────────┐
│ orders           │     │ order_items               │
│ ──────────────── │     │ ────────────────────────── │
│ id | cust | email│     │ order_id | item   | price │
│ 1  │Nishant│n@.. │     │ 1       │ iPhone │ 79999 │
│ 2  │ Priya │p@.. │     │ 1       │ AirPods│ 24900 │
└──────────────────┘     │ 2       │ Jeans  │ 2499  │
                         └──────────────────────────┘
Fixed: ✅ Customer data not duplicated per item
Still: ❌ If Nishant orders again, his name/email is duplicated

═══════════════════════════════════════════════════════════════════

3NF (remove transitive dependencies → more tables):
┌──────────┐  ┌────────────────┐  ┌──────────────────┐  ┌──────────┐
│customers │  │ orders         │  │ order_items       │  │ products │
│ ──────── │  │ ────────────── │  │ ──────────────── │  │ ──────── │
│ id       │  │ id             │  │ order_id         │  │ id       │
│ name     │  │ customer_id ──▶│  │ product_id ──────▶│  │ name     │
│ email    │  │ order_date     │  │ quantity         │  │ price    │
│ city     │  │ total          │  │ unit_price       │  │          │
└──────────┘  └────────────────┘  └──────────────────┘  └──────────┘
Fixed: ✅ No data duplication
       ✅ Update customer email in ONE place
       ✅ Each fact stored exactly once
```

---

## Syntax

```sql
-- ============================================
-- UNNORMALIZED (bad design)
-- ============================================

-- Don't do this!
CREATE TABLE orders_bad (
  id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_email VARCHAR(150),
  customer_city VARCHAR(50),
  product1_name VARCHAR(200),
  product1_price DECIMAL(10,2),
  product1_qty INT,
  product2_name VARCHAR(200),   -- What if 3 products? 10? 100?
  product2_price DECIMAL(10,2),
  product2_qty INT
);


-- ============================================
-- NORMALIZED (good design — our e-commerce schema!)
-- ============================================

-- Each entity gets its own table
CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  city VARCHAR(50)
);

CREATE TABLE categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  stock INT DEFAULT 0,
  category_id INT,
  FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  total_amount DECIMAL(10, 2),
  status ENUM('pending', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
  order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  unit_price DECIMAL(10, 2) NOT NULL,  -- Price at time of order (historical)
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);


-- ============================================
-- STRATEGIC DENORMALIZATION (intentional duplication)
-- ============================================

-- unit_price in order_items is INTENTIONALLY denormalized
-- We store the price at the time of purchase, not reference the current price
-- If product price changes, order history should NOT change!

-- Similarly, you might denormalize for performance:
ALTER TABLE orders ADD COLUMN customer_name VARCHAR(100);
-- Avoids a JOIN for display-only purposes
-- But now you must keep it in sync!
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== MongoDB — Denormalized Approach ==========

// Embedding (denormalized — common in MongoDB)
const orderSchema = new Schema({
  customer: {
    _id: ObjectId,
    name: String,  // Copied from customer document
    email: String  // Copied from customer document
  },
  items: [{
    product: {
      _id: ObjectId,
      name: String,  // Copied from product document
    },
    quantity: Number,
    price: Number    // Price at time of purchase
  }],
  total: Number
});

// Pro: Single document read — very fast
// Con: Customer email update doesn't reflect in old orders
```

```sql
-- ========== MySQL — Normalized Approach ==========

-- Data split across tables with foreign keys
-- To get a full order, you JOIN:
SELECT 
  o.id, o.order_date, o.total_amount,
  c.name AS customer, c.email,
  p.name AS product, oi.quantity, oi.unit_price
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.id = 1;

-- Pro: Change customer email once → reflected everywhere
-- Pro: No data duplication
-- Con: Requires JOINs (slight performance cost)
```

```js
// ========== Node.js — Working with normalized data ==========
const db = require('./db');

// The query gets data from 4 tables in 1 call (normalized but efficient)
app.get('/api/orders/:id', async (req, res) => {
  const [rows] = await db.query(`
    SELECT 
      o.id AS order_id,
      c.name AS customer,
      c.email,
      o.total_amount,
      o.status,
      p.name AS product,
      oi.quantity,
      oi.unit_price
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE o.id = ?
  `, [req.params.id]);
  
  // Reshape flat rows into nested structure (like MongoDB's embedded format)
  if (rows.length === 0) return res.status(404).json({ error: 'Not found' });
  
  const order = {
    id: rows[0].order_id,
    customer: { name: rows[0].customer, email: rows[0].email },
    totalAmount: rows[0].total_amount,
    status: rows[0].status,
    items: rows.map(r => ({
      product: r.product,
      quantity: r.quantity,
      unitPrice: r.unit_price
    }))
  };
  
  res.json(order);
});
```

---

## ORM Equivalent (Sequelize)

```js
// Sequelize handles normalization naturally through associations
const order = await Order.findByPk(1, {
  include: [
    { model: Customer, attributes: ['name', 'email'] },
    { 
      model: OrderItem,
      include: [{ model: Product, attributes: ['name'] }]
    }
  ]
});

// Output looks like MongoDB embedded documents:
// { id: 1, Customer: { name: '...' }, OrderItems: [{ Product: { name: '...' } }] }
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Demonstrating data anomalies in unnormalized designs

```sql
-- ❌ BAD: Unnormalized orders table
CREATE TABLE orders_flat (
  order_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  customer_email VARCHAR(150),
  product_name VARCHAR(200),
  product_price DECIMAL(10,2),
  quantity INT
);

INSERT INTO orders_flat VALUES
(1, 'Nishant', 'n@test.com', 'iPhone', 79999, 1),
(2, 'Nishant', 'n@test.com', 'AirPods', 24900, 1),
(3, 'Priya', 'p@test.com', 'iPhone', 79999, 2);

-- UPDATE ANOMALY: Nishant changes email
-- Must update EVERY row where customer_name = 'Nishant'
UPDATE orders_flat SET customer_email = 'new@test.com' WHERE customer_name = 'Nishant';
-- What if you miss one? Inconsistent data!

-- INSERT ANOMALY: New customer with no orders
-- Can't add a customer who hasn't ordered yet!
-- In normalized design, just INSERT INTO customers

-- DELETE ANOMALY: Delete the only order for 'Priya'
DELETE FROM orders_flat WHERE order_id = 3;
-- We just lost Priya's customer information entirely!
```

```js
// Node.js — Demonstrating normalization benefits
app.get('/api/demo/anomalies', async (req, res) => {
  // Normalized: update email in ONE place
  await db.query('UPDATE customers SET email = ? WHERE id = ?', ['newemail@test.com', 1]);
  
  // Now EVERY query that JOINs customers will see the new email
  const [orders] = await db.query(`
    SELECT o.id, c.email FROM orders o
    JOIN customers c ON o.customer_id = c.id
    WHERE o.customer_id = 1
  `);
  // All orders show the updated email! No anomalies!
  
  res.json({ message: 'All orders reflect updated email', orders });
});
```

**Output:**
```json
{
  "message": "All orders reflect updated email",
  "orders": [
    { "id": 1, "email": "newemail@test.com" },
    { "id": 2, "email": "newemail@test.com" }
  ]
}
```

---

## Impact

| If You Don't Normalize...                | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| Store customer name in orders table       | Customer renames → old orders show old name      |
| Store category name with every product    | Category renames → must update every product row |
| Store product list as comma-separated     | Can't query individual products, no JOINs        |
| No foreign keys between tables            | Orphaned data, broken relationships              |
| Over-normalize (too many tables)          | Too many JOINs, slow queries, complex code       |

### When to Denormalize (Intentionally)

```
Denormalize when:
✅ Read performance is critical (dashboard, feeds)
✅ Data is historical (order prices shouldn't change)
✅ Joins are too slow on very large tables
✅ Data rarely changes (country names, zip codes)

Keep normalized when:
✅ Data changes frequently (user profiles, product details)
✅ Data integrity is critical (financial records)
✅ Storage efficiency matters
✅ Multiple applications access the same database
```



---

## Interview Q&A

### ❓ Q1: What is normalization and what are the normal forms?
> **💡 Answer:** Normalization organizes data to reduce redundancy and improve integrity. 1NF: atomic values, no repeating groups. 2NF: 1NF + no partial dependencies on composite key. 3NF: 2NF + no transitive dependencies (non-key columns don't depend on other non-key columns). BCNF: stricter 3NF. Most apps target 3NF.

### ❓ Q2: What is denormalization and when would you use it?
> **💡 Answer:** Denormalization intentionally adds redundancy for read performance. Use when: read-heavy workloads, complex JOINs are too slow, data rarely changes. Example: storing product name in order_items alongside product_id. Trade-off: faster reads but harder updates and risk of inconsistency.

### ❓ Q3: Explain the three types of data anomalies.
> **💡 Answer:** Insert anomaly: can't add data without unrelated data (can't add customer without an order). Update anomaly: must update duplicate data in multiple places (change email in every order row). Delete anomaly: losing data when deleting other data (deleting last order loses customer info). Normalization eliminates all three.

### ❓ Q4: What is the difference between 2NF and 3NF?
> **💡 Answer:** 2NF eliminates partial dependencies: in a table with composite key (A, B), every non-key column must depend on BOTH A and B together, not just A or B alone. 3NF eliminates transitive dependencies: non-key columns must depend directly on the primary key, not through another non-key column. Example: city depends on zip_code, which depends on customer_id — city should be in a separate zip_codes table.

### ❓ Q5: In MongoDB, we use embedded documents. How does that relate to normalization?
> **💡 Answer:** Embedded documents are denormalized by design — data is duplicated for read performance. In SQL, the same data would live in separate tables (normalized) and be JOINed. MongoDB trades consistency for speed; SQL trades speed for consistency. The best approach depends on read/write patterns, data change frequency, and consistency requirements.

### ❓ Q6: When is 3NF preferred over BCNF in real-world database design?
> **💡 Answer:** When decomposing a table into BCNF causes a **loss of Functional Dependency Preservation**. In 3NF, all functional dependencies can be enforced natively using simple single-table unique constraints or primary keys. Decomposing into BCNF can split a dependency across two tables, meaning the database cannot enforce the rule without expensive multi-table triggers or serialized locks during every insert/update. In practice, engineers accept 3NF with minor redundancy to preserve dependency checking performance.

### ❓ Q7: What mathematical condition guarantees that a table decomposition is "Lossless"?
> **💡 Answer:** By the **Lossless Join Theorem**, a decomposition of relation $R$ into $R_1$ and $R_2$ is lossless if and only if the intersection of their attributes $(R_1 \cap R_2)$ forms a **Super Key** for either $R_1$ or $R_2$ (i.e. $(R_1 \cap R_2) \rightarrow R_1$ or $(R_1 \cap R_2) \rightarrow R_2$). This ensures that joining $R_1 \bowtie R_2$ reconstructs the exact original relation without producing phantom (fake) rows.

---

| [← Previous: Triggers](./18_Triggers.md) | [Index](./00_index.md) | [Next: SQL vs NoSQL →](./20_SQL_Vs_NoSQL.md) |
|---|---|---|

