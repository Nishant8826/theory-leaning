# Indexes

> 📌 **File:** `14_Indexes.md` | **Level:** Beginner → MERN Developer

---

## What is it?

An **index** is a data structure (usually a B-tree) that speeds up data retrieval. It's like the index at the back of a textbook — instead of reading every page to find "SQL", you look up "SQL" in the index and jump directly to page 142.

Without indexes, MySQL performs a **full table scan** — reading every single row. With an index on the searched column, MySQL jumps directly to matching rows.

---

## MERN Parallel — You Already Know This!

| MongoDB/Mongoose (You Know)                        | MySQL Index (You'll Learn)                      |
|----------------------------------------------------|-------------------------------------------------|
| `schema.index({ email: 1 })`                      | `CREATE INDEX idx_email ON users(email)`        |
| `{ unique: true }` in schema                      | `CREATE UNIQUE INDEX ...` or `UNIQUE` constraint|
| `schema.index({ name: 'text' })`                  | `ALTER TABLE ADD FULLTEXT(name)`                |
| `schema.index({ price: 1, category: 1 })`         | `CREATE INDEX idx_price_cat ON products(price, category_id)` |
| `db.collection.getIndexes()`                       | `SHOW INDEX FROM table_name`                    |
| `explain()` to analyze query                       | `EXPLAIN SELECT ...`                            |
| `_id` index (automatic)                            | PRIMARY KEY index (automatic)                   |

---

## Why does it matter?

- A query on 1 million rows: **Without index = 2 seconds, With index = 2 milliseconds** (1000× faster)
- Indexes are the #1 way to improve query performance
- Missing indexes are the #1 cause of slow queries in production
- Too many indexes slow down INSERT/UPDATE/DELETE operations
- Understanding the EXPLAIN plan is essential for query optimization

---

## How does it work?

### Without Index (Full Table Scan)

```
Query: SELECT * FROM customers WHERE email = 'n@test.com';

Without Index:
Row 1: email = 'a@test.com' → No match
Row 2: email = 'b@test.com' → No match
Row 3: email = 'c@test.com' → No match
...
Row 999: email = 'n@test.com' → MATCH! ✅
...
Row 1000000: email = 'z@test.com' → checked unnecessarily
→ Scanned ALL 1,000,000 rows to find 1 result!
```

### With Index (B-tree Lookup)

```
Query: SELECT * FROM customers WHERE email = 'n@test.com';

With Index on email:
          ┌─────────┐
          │  m-r    │
          └─┬───┬───┘
            │   │
    ┌───────┘   └───────┐
    │                   │
┌───┴───┐         ┌────┴──┐
│ m-o   │         │ p-r   │
└──┬────┘         └───────┘
   │
┌──┴──┐
│n@..  │ → FOUND! Points to row 999
└─────┘

→ Checked only ~3 levels of the tree (log₂ of 1M ≈ 20 comparisons)
  instead of 1,000,000!
```

---

## Visual Diagram

### Index Types

```
┌──────────────────────────────────────────────────────────────┐
│                       INDEX TYPES                            │
├─────────────────┬────────────────────────────────────────────┤
│ PRIMARY KEY     │ Auto-created on primary key column         │
│                 │ Unique, non-null, one per table            │
│                 │ Clustered index (data sorted by PK)        │
├─────────────────┼────────────────────────────────────────────┤
│ UNIQUE          │ Prevents duplicate values                  │
│                 │ Like MongoDB's unique: true                │
│                 │ Can have multiple per table                │
├─────────────────┼────────────────────────────────────────────┤
│ INDEX (Regular) │ Speeds up lookups, no uniqueness constraint│
│                 │ Most common type                           │
├─────────────────┼────────────────────────────────────────────┤
│ COMPOSITE       │ Index on multiple columns                  │
│                 │ ORDER MATTERS: (price, category) ≠         │
│                 │ (category, price)                          │
├─────────────────┼────────────────────────────────────────────┤
│ FULLTEXT        │ For text search (MATCH ... AGAINST)        │
│                 │ Like MongoDB's text index                  │
├─────────────────┼────────────────────────────────────────────┤
│ SPATIAL         │ For geographic data (rarely used)          │
└─────────────────┴────────────────────────────────────────────┘
```

### Write Speed vs Read Speed Tradeoff

```
                    Few Indexes          Many Indexes
                   ┌──────────┐         ┌──────────┐
  SELECT (Read)    │ SLOW ❌   │         │ FAST ✅   │
  INSERT (Write)   │ FAST ✅   │         │ SLOW ❌   │
  UPDATE (Write)   │ FAST ✅   │         │ SLOW ❌   │
  DELETE (Write)   │ FAST ✅   │         │ SLOW ❌   │
  Storage          │ SMALL ✅  │         │ LARGE ❌  │
                   └──────────┘         └──────────┘
  
  Balance: Index columns used in WHERE, JOIN, ORDER BY
           Don't index columns rarely searched
```

---

## Syntax

```sql
-- ============================================
-- CREATE INDEX
-- ============================================

-- Regular index
CREATE INDEX idx_email ON customers(email);
CREATE INDEX idx_category ON products(category_id);
CREATE INDEX idx_status ON orders(status);

-- Unique index (prevents duplicates)
CREATE UNIQUE INDEX idx_unique_email ON customers(email);

-- Composite index (multiple columns)
CREATE INDEX idx_price_status ON products(price, status);
-- Works for: WHERE price > 1000
-- Works for: WHERE price > 1000 AND status = 'published'
-- Does NOT work for: WHERE status = 'published' (leftmost column missing!)

-- Index in CREATE TABLE
CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,    -- PRIMARY KEY = auto index
  email VARCHAR(150) UNIQUE NOT NULL,   -- UNIQUE = auto index
  name VARCHAR(100),
  city VARCHAR(50),
  INDEX idx_name (name),                -- Regular index
  INDEX idx_city (city)                 -- Regular index
);

-- Fulltext index (for text search)
ALTER TABLE products ADD FULLTEXT INDEX ft_search (name, description);

-- Prefix index (index only first N characters)
CREATE INDEX idx_name_prefix ON customers(name(20));  -- First 20 chars only


-- ============================================
-- DROP INDEX
-- ============================================
DROP INDEX idx_email ON customers;
ALTER TABLE customers DROP INDEX idx_email;


-- ============================================
-- SHOW INDEXES
-- ============================================
SHOW INDEX FROM customers;
SHOW INDEX FROM products;


-- ============================================
-- EXPLAIN — Analyze query performance
-- ============================================
EXPLAIN SELECT * FROM customers WHERE email = 'n@test.com';
EXPLAIN SELECT * FROM products WHERE price > 10000 AND status = 'published';
EXPLAIN SELECT * FROM orders o JOIN customers c ON o.customer_id = c.id;

-- Key fields in EXPLAIN output:
-- type: ALL (full scan 😱), index, range, ref, eq_ref, const (best)
-- key: Which index is used (NULL = no index! 😱)
-- rows: Estimated rows scanned (lower = better)
-- Extra: Using index, Using where, Using filesort
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Mongoose (What You Know) ==========

// Create index in schema
const customerSchema = new mongoose.Schema({
  name: String,
  email: { type: String, unique: true, index: true },
  phone: String,
  city: String
});

// Compound index
customerSchema.index({ city: 1, name: 1 });

// Text index
customerSchema.index({ name: 'text', email: 'text' });

// Get indexes
const indexes = await Customer.collection.getIndexes();

// Explain a query
const explanation = await Customer.find({ email: 'n@test.com' }).explain();
```

```sql
-- ========== MySQL ==========

CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(150) UNIQUE NOT NULL,  -- Auto-indexed
  phone VARCHAR(15),
  city VARCHAR(50)
);

-- Add indexes
CREATE INDEX idx_city_name ON customers(city, name);
ALTER TABLE customers ADD FULLTEXT(name, email);

-- Show indexes
SHOW INDEX FROM customers;

-- Explain query
EXPLAIN SELECT * FROM customers WHERE email = 'n@test.com';
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Create index
await pool.query('CREATE INDEX idx_email ON customers(email)');

// Explain a query to check performance
const [explanation] = await pool.query(
  'EXPLAIN SELECT * FROM products WHERE price > ? AND status = ?',
  [10000, 'published']
);
console.table(explanation);

// Show all indexes on a table
const [indexes] = await pool.query('SHOW INDEX FROM products');
console.table(indexes);

// Fulltext search (after adding FULLTEXT index)
const [results] = await pool.query(
  `SELECT *, MATCH(name, description) AGAINST(? IN BOOLEAN MODE) AS relevance
   FROM products
   WHERE MATCH(name, description) AGAINST(? IN BOOLEAN MODE)
   ORDER BY relevance DESC`,
  [searchTerm, searchTerm]
);
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize ==========

const Product = sequelize.define('Product', {
  name: DataTypes.STRING,
  price: DataTypes.DECIMAL(10, 2),
  status: DataTypes.STRING
}, {
  indexes: [
    { fields: ['price'] },
    { fields: ['status'] },
    { fields: ['price', 'status'], name: 'idx_price_status' },
    { unique: true, fields: ['name'] },
    { type: 'FULLTEXT', fields: ['name', 'description'] }
  ]
});
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Optimizing the product search API that's running slow

```sql
-- Before optimization — EXPLAIN shows full table scan
EXPLAIN SELECT * FROM products WHERE name LIKE '%iphone%' AND price > 10000;
-- type: ALL, rows: 1000000, key: NULL  ← FULL SCAN!

-- Step 1: Add indexes
CREATE INDEX idx_price ON products(price);
ALTER TABLE products ADD FULLTEXT INDEX ft_name_desc (name, description);

-- After optimization — EXPLAIN shows index usage
EXPLAIN SELECT * FROM products 
WHERE MATCH(name, description) AGAINST('iphone' IN BOOLEAN MODE) 
AND price > 10000;
-- type: fulltext, rows: 15, key: ft_name_desc ← INDEX USED!
```

```js
// Node.js + Express — Optimized search with EXPLAIN endpoint
app.get('/api/products/search', async (req, res) => {
  try {
    const { q, minPrice, maxPrice, explain } = req.query;
    
    let sql = `
      SELECT p.id, p.name, p.price, p.stock, c.name AS category
      FROM products p
      LEFT JOIN categories c ON p.category_id = c.id
      WHERE 1=1
    `;
    const params = [];
    
    if (q) {
      sql += ' AND MATCH(p.name, p.description) AGAINST(? IN BOOLEAN MODE)';
      params.push(q);
    }
    if (minPrice) {
      sql += ' AND p.price >= ?';
      params.push(Number(minPrice));
    }
    if (maxPrice) {
      sql += ' AND p.price <= ?';
      params.push(Number(maxPrice));
    }
    
    sql += ' ORDER BY p.price ASC LIMIT 20';
    
    // Debug mode — return query plan
    if (explain === 'true') {
      const [plan] = await pool.query('EXPLAIN ' + sql, params);
      return res.json({ queryPlan: plan, sql });
    }
    
    const [products] = await pool.query(sql, params);
    res.json({ count: products.length, products });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Index management route (admin only)
app.get('/api/admin/indexes/:table', async (req, res) => {
  try {
    const [indexes] = await pool.query('SHOW INDEX FROM ??', [req.params.table]);
    res.json({ table: req.params.table, indexes });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// React — Query analyzer component
function QueryAnalyzer() {
  const [query, setQuery] = useState('');
  const [plan, setPlan] = useState(null);

  const analyze = async () => {
    const { data } = await axios.get(`/api/products/search?q=${query}&explain=true`);
    setPlan(data.queryPlan);
  };

  return (
    <div>
      <h2>Query Performance Analyzer</h2>
      <input value={query} onChange={e => setQuery(e.target.value)}
        placeholder="Search products..." />
      <button onClick={analyze}>Analyze</button>
      
      {plan && (
        <table>
          <thead>
            <tr>
              <th>Type</th><th>Table</th><th>Key</th>
              <th>Rows Scanned</th><th>Extra</th>
            </tr>
          </thead>
          <tbody>
            {plan.map((row, i) => (
              <tr key={i} style={{
                backgroundColor: row.type === 'ALL' ? '#ffcccc' : '#ccffcc'
              }}>
                <td>{row.type}</td>
                <td>{row.table}</td>
                <td>{row.key || '❌ NONE'}</td>
                <td>{row.rows}</td>
                <td>{row.Extra}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
```

**Output (EXPLAIN):**
```json
{
  "queryPlan": [
    {
      "id": 1,
      "select_type": "SIMPLE",
      "table": "p",
      "type": "fulltext",
      "possible_keys": "ft_name_desc,idx_price",
      "key": "ft_name_desc",
      "rows": 1,
      "Extra": "Using where"
    }
  ]
}
```

---

## Impact

| If You Don't Understand Indexes...       | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| No index on email column                 | Login query scans entire users table every time  |
| No index on foreign key columns          | JOINs become extremely slow                      |
| Too many indexes                         | INSERT/UPDATE become slow (index maintenance)    |
| Wrong composite index order              | Index not used — still full table scan            |
| Don't use EXPLAIN                        | Can't diagnose slow queries                      |
| LIKE '%search%' without FULLTEXT         | Always full table scan — can't use regular index |

### Composite Index Leftmost Prefix Rule

```
Index: (category_id, price, status)

✅ Uses index: WHERE category_id = 1
✅ Uses index: WHERE category_id = 1 AND price > 1000
✅ Uses index: WHERE category_id = 1 AND price > 1000 AND status = 'active'

❌ Cannot use index: WHERE price > 1000 (category_id missing!)
❌ Cannot use index: WHERE status = 'active' (category_id missing!)
❌ Cannot use index: WHERE price > 1000 AND status = 'active' (category_id missing!)

The leftmost column(s) MUST be in the WHERE clause!
Think of it like a phone book: sorted by last name, then first name.
You can look up "Kumar" or "Kumar, Nishant" but NOT just "Nishant".
```

---

## Practice Exercises

### Easy (SQL)
1. Create an index on the `email` column of the customers table
2. Run EXPLAIN on a SELECT query and identify if an index is being used
3. Show all indexes on the products table

### Medium (SQL + Node.js)
4. Add appropriate indexes to all foreign key columns in your e-commerce schema
5. Write a fulltext search for products and build an Express route for it
6. Create a `/api/admin/slow-queries` route that shows queries with type='ALL' using EXPLAIN

### Hard (Full Stack)
7. Build an index management dashboard:
   - List all tables and their indexes
   - Run EXPLAIN on custom queries
   - Get recommendations for missing indexes
8. Benchmark: insert 100,000 products and compare query times with and without indexes

---

## Real-World Q&A

**Q1:** In MongoDB, `_id` is auto-indexed. What about MySQL?
**A:** The PRIMARY KEY column is auto-indexed (clustered index). UNIQUE columns are also auto-indexed. But foreign keys (`customer_id`, `category_id`) are NOT auto-indexed in MySQL — you must add them manually! This is a common optimization miss.

**Q2:** How many indexes should a table have?
**A:** No fixed rule, but guidelines: Index every foreign key column. Index columns frequently used in WHERE, JOIN ON, and ORDER BY. Don't index columns with low cardinality (e.g., boolean/status with only 2-3 values). A typical table might have 3-7 indexes. Monitor and adjust based on EXPLAIN results.

**Q3:** Does having an index guarantee MySQL will use it?
**A:** No! MySQL's optimizer decides whether to use an index based on cardinality, data distribution, and query structure. If an index would return >30% of the table rows, MySQL may prefer a full table scan. Use EXPLAIN to verify.

---

## Interview Q&A

**Q1: What is an index and why is it important?**
An index is a data structure (B-tree) that allows the database to find rows quickly without scanning the entire table. Like a book's index — instead of reading every page, you look up the topic and go directly to the page. Indexes are crucial for performance; a query on 1M rows can go from seconds to milliseconds.

**Q2: What are the disadvantages of indexes?**
(1) Extra storage space. (2) Slower INSERT/UPDATE/DELETE because indexes must be updated. (3) Index maintenance overhead. The tradeoff: faster reads vs slower writes. For read-heavy apps (most web apps), the tradeoff is worth it.

**Q3: What is a composite index and how does the leftmost prefix rule work?**
A composite index is on multiple columns: `INDEX(a, b, c)`. The leftmost prefix rule means the index can be used for queries on (a), (a,b), or (a,b,c) but NOT (b), (c), or (b,c) alone. Column order matters — put the most selective (highest cardinality) column first.

**Q4: What is the difference between clustered and non-clustered indexes?**
Clustered index: the table data is physically ordered by this index. MySQL's PRIMARY KEY is the clustered index — only one per table. Non-clustered index: a separate structure that points to the actual rows. You can have multiple non-clustered indexes. Think: clustered = the book itself (ordered by chapters), non-clustered = the book's back index.

**Q5: How would you find and fix slow queries in a production MySQL database?**
(1) Enable slow query log: `SET GLOBAL slow_query_log = 'ON'`. (2) Check queries with `EXPLAIN`. (3) Look for type=ALL (full scan) and key=NULL. (4) Add indexes on columns in WHERE, JOIN, ORDER BY. (5) Monitor with `SHOW PROCESSLIST`. (6) Use tools like `pt-query-digest`. (7) Consider query rewrites, denormalization, or caching for genuinely complex queries.

---

| [← Previous: Views](./13_Views.md) | [Next: Transactions →](./15_Transactions.md) |
|---|---|
