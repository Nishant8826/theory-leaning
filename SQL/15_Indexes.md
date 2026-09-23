# Indexes

> 📌 **File:** `15_Indexes.md` | **Level:** Beginner → MERN Developer

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

### Types of Indexes Explained

To optimize queries effectively, you must choose the right type of index:

#### 1. Primary Key Index (Clustered Index)
* **What it is:** The physical table data on disk is physically sorted and stored in the order of the Primary Key. Because table records can only be stored in one physical order, there is **only one clustered index** per table.
* **How it works:** When you query by the Primary Key, MySQL doesn't look up pointers — it lands directly on the actual row data.
* **MERN Parallel:** Matches the automatically generated `_id` index in MongoDB.
* **SQL Query Syntax:**
  ```sql
  -- Defined during table creation:
  CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
  );
  -- Or added to an existing table:
  ALTER TABLE users ADD PRIMARY KEY (id);

  -- How to query (utilizes Clustered Index):
  SELECT * FROM users WHERE id = 42;
  ```

#### 2. Unique Index
* **What it is:** A non-clustered index that enforces a uniqueness constraint. It prevents duplicate values from being inserted.
* **How it works:** Before inserting a row, MySQL checks the B-tree. If the key exists, it rejects the insert with a duplicate key error.
* **MERN Parallel:** Matches the `{ unique: true }` option on Mongoose fields.
* **SQL Query Syntax:**
  ```sql
  -- Create Unique Index:
  CREATE UNIQUE INDEX idx_unique_email ON customers(email);

  -- How to query (utilizes Unique Index):
  SELECT * FROM customers WHERE email = 'n@test.com';
  ```

#### 3. Single-Column (Regular) Index
* **What it is:** A standard non-clustered index on a single column (e.g. `status` or `price`). It contains a sorted list of column values, and each entry points back to the Primary Key of the matching row.
* **How it works:** MySQL searches the B-tree to find the column value, gets the Primary Key ID, and then uses that ID to fetch the actual row (called a "Key Lookup" or "Bookmark Lookup").
* **MERN Parallel:** Matches `schema.index({ status: 1 })`.
* **SQL Query Syntax:**
  ```sql
  -- Create Regular Index:
  CREATE INDEX idx_status ON orders(status);

  -- How to query (utilizes Single-Column Index):
  SELECT * FROM orders WHERE status = 'pending';
  ```

#### 4. Composite (Compound) Index
* **What it is:** An index built on multiple columns in a specific order, e.g., `INDEX (category_id, price)`.
* **The Leftmost Prefix Rule:** The order of columns in the index declaration is critical. An index on `(A, B, C)` can only be used if the query filters by:
  * `WHERE A = ...`
  * `WHERE A = ... AND B = ...`
  * `WHERE A = ... AND B = ... AND C = ...`
  * *It CANNOT be used for `WHERE B = ...` or `WHERE C = ...` because the leftmost column `A` is missing.*
* **MERN Parallel:** Matches compound indexes like `schema.index({ category_id: 1, price: 1 })`.
* **SQL Query Syntax:**
  ```sql
  -- Create Composite Index:
  CREATE INDEX idx_cat_price ON products(category_id, price);

  -- How to query (utilizes Composite Index):
  -- 1. Querying by leftmost column only (Uses Index):
  SELECT * FROM products WHERE category_id = 5;

  -- 2. Querying by leftmost + second column (Uses Index):
  SELECT * FROM products WHERE category_id = 5 AND price > 1500;

  -- ❌ Querying by second column only (Does NOT use this index - leftmost prefix violation!):
  SELECT * FROM products WHERE price > 1500;
  ```

#### 5. Full-Text Index (`FULLTEXT`)
* **What it is:** Specifically designed for searching large blocks of natural language text. Instead of storing the exact string value, it builds an "inverted index" mapping words to rows.
* **How it works:** Rather than using slow wildcard filters (`LIKE '%query%'`), you run `MATCH(name, desc) AGAINST('query')`. This is incredibly fast and supports search rankings.
* **MERN Parallel:** Matches MongoDB’s `{ name: 'text' }` text indexing capabilities.
* **SQL Query Syntax:**
  ```sql
  -- Create FULLTEXT Index:
  ALTER TABLE products ADD FULLTEXT INDEX ft_name_desc (name, description);

  -- How to query (utilizes FULLTEXT Index):
  SELECT * FROM products 
  WHERE MATCH(name, description) AGAINST('iphone' IN BOOLEAN MODE);
  ```

#### 6. Prefix (Partial) Index
* **What it is:** An index built only on the first $N$ characters of a long string column (like a `VARCHAR(500)` or `TEXT`).
* **Why it matters:** Indexing long strings wastes massive disk space and RAM. Creating a prefix index like `INDEX idx_desc (description(20))` index only the first 20 characters, which is usually selective enough to find rows while keeping the index size tiny.
* **SQL Query Syntax:**
  ```sql
  -- Create Prefix Index:
  CREATE INDEX idx_name_prefix ON users(name(20)); -- Index only first 20 characters

  -- How to query (utilizes Prefix Index):
  SELECT * FROM users WHERE name LIKE 'Nish%';
  ```

#### 7. Spatial Index
* **What it is:** Built for geometric/geographic data coordinates (`POINT`, `POLYGON`, etc.).
* **Why it matters:** Enables location-based queries (e.g. "find properties within 5 miles"). Uses R-tree indexing structure.
* **SQL Query Syntax:**
  ```sql
  -- Create Table with SPATIAL Index (spatial columns must be NOT NULL):
  CREATE TABLE stores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    coordinates POINT NOT NULL,
    SPATIAL INDEX idx_location (coordinates)
  );

  -- How to query (utilizes Spatial Index for bounding box search):
  SELECT * FROM stores 
  WHERE MBRContains(ST_GeomFromText('POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))'), coordinates);

  -- How to query (finds nearest store within a sphere distance):
  SELECT id, name, ST_Distance_Sphere(coordinates, ST_GeomFromText('POINT(77.2090 28.6139)')) AS distance_meters
  FROM stores
  ORDER BY distance_meters ASC;
  ```

---

### Under-the-Hood Technical Deep Dive

#### 1. B+Tree Fan-Out Math & Page Geometry
Why is a B+Tree so blisteringly fast?
* In MySQL InnoDB, all disk data is stored in **16 KB Pages**.
* In a non-leaf index node page, an entry consists of a column key (e.g. 8-byte `BIGINT`) + a child page pointer (6 bytes) $\approx 14$ bytes.
* A single 16 KB page can hold $\approx 16,384 / 14 \approx \mathbf{1,170\text{ child pointers}}$ (the **Fan-Out**).
* **Tree Capacity Calculations:**
  * **Level 1 (Root):** 1 Page $\approx 1,170$ pointers.
  * **Level 2 (Branch):** $1,170 \times 1,170 \approx 1.36\text{ Million pointers}$.
  * **Level 3 (Leaf):** If each leaf page holds 100 table rows: $1.36\text{M} \times 100 \approx \mathbf{136\text{ Million rows}}$!
* 🚀 **Impact:** A table with **136 million rows** requires only **3 disk page reads** to locate any random row!

#### 2. Covering Index vs Secondary Bookmark Lookup
* **Secondary Bookmark Lookup (🐢 Standard):** An index on `(email)` stores `(email, id)`. If you query `SELECT name FROM users WHERE email = 'test@example.com'`, MySQL traverses the B+Tree to find `id`, then performs a **second random disk lookup** on the Clustered Index to retrieve `name`.
* **Covering Index (⚡ Ultra Fast):** If you create a composite index on `(email, name)`, all requested columns exist inside the index tree! MySQL retrieves `name` directly from the leaf node without touching the main table storage (`Using index` in `EXPLAIN`).

#### 3. Index Condition Pushdown (ICP - `Using index condition`)
In older MySQL, if a query filtered on non-leading index columns, InnoDB read full table rows into the SQL Server layer before evaluating the filter. In modern MySQL, the storage engine filters rows at the index level before fetching rows from disk, drastically reducing I/O.

#### 4. The Master `EXPLAIN` Type Hierarchy (Fastest to Slowest)
```
system > const > eq_ref > ref > fulltext > ref_or_null > index_merge > unique_subquery > index_subquery > range > index > ALL
```
* **`const` / `system`:** Single row lookup via Primary Key or Unique Index ($O(1)$).
* **`eq_ref`:** 1-to-1 join using Primary Key or Unique Index.
* **`ref`:** Non-unique index lookup (multiple matching rows).
* **`range`:** Index range scan using `>`, `<`, `BETWEEN`, `IN()`.
* **`index`:** Full Index Scan (scans entire index tree without using keys).
* **`ALL`:** ⚠️ **Full Table Scan!** (Scans entire disk table from start to finish).

#### 5. Index Selectivity & Cardinality Math
**Selectivity** measures how uniquely an index filters data:
$$\text{Selectivity} = \frac{\text{Cardinality (Number of Unique Values)}}{\text{Total Rows in Table}}$$
* **High Selectivity ($\approx 1.0$ / $100\%$):** E.g., `email`, `user_id`, `ssn`. The index is extremely fast; MySQL uses it instantly.
* **Low Selectivity ($< 0.15$ / $< 15\%$):** E.g., `gender`, `is_active`, `status` (`'pending'/'completed'`). 
* ⚠️ **The 20% Threshold Trap:** If MySQL estimates that an index query will match more than $20\%-30\%$ of total table rows, the Cost-Based Optimizer **intentionally ignores the index** and performs a Full Table Scan because sequential disk reads are faster than thousands of random B+Tree secondary index bookmark lookups!

#### 6. The Range Column Index-Killer Rule
In a composite index on `(A, B, C)`:
```sql
-- Query 1: All 3 columns use the index!
SELECT * FROM orders WHERE a = 10 AND b = 20 AND c = 30;

-- Query 2: Range column 'b' TERMINATES index usage for 'c'!
SELECT * FROM orders WHERE a = 10 AND b > 20 AND c = 30;
```
* **Why column `c` fails:** Inside the B+Tree, rows are ordered by `A`, then by `B`, then by `C`. Once column `b` matches a range (`b > 20`), the values of `c` across different `b` values are no longer in sorted order! MySQL can use the index to locate `a = 10` and filter the range `b > 20`, but it **cannot use the index to seek `c = 30`**.
* 💡 **Golden Rule of Index Ordering:** Place exact equality columns **first**, and range filter columns **last** in your composite index: `INDEX(a, c, b)`.

#### 7. Loose Index Scan (`Using index for group-by`)
When running `SELECT DISTINCT category_id FROM products;` or `SELECT category_id, MIN(price) FROM products GROUP BY category_id;`:
* **Tight Index Scan:** MySQL scans all index entries for the category.
* **Loose Index Scan (⚡ Blazing Fast):** MySQL jumps directly from the first key of Category 1 to the first key of Category 2 without reading intermediate rows, executing in $O(\text{number of groups})$ rather than $O(\text{number of rows})$.

#### 8. Modern `EXPLAIN ANALYZE` (MySQL 8.0+)
While standard `EXPLAIN` gives optimizer estimates, `EXPLAIN ANALYZE` physically executes the query using the Volcano iterator model and outputs exact runtime metrics:
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42;
```
* **Output breakdown:**
  `-> Index lookup on orders using idx_customer (customer_id=42) (cost=0.35 rows=1) (actual time=0.041..0.043 rows=1 loops=1)`
  * `cost=0.35`: Estimated I/O + CPU cost.
  * `actual time=0.041..0.043`: Time to first row and time to all rows in milliseconds.
  * `loops=1`: Number of times the iterator was executed.

#### 9. Optimizer Index Hints
If the optimizer chooses the wrong execution plan:
```sql
-- Force MySQL to use a specific index
SELECT * FROM orders FORCE INDEX (idx_customer_date) WHERE customer_id = 42;

-- Ignore an inefficient index
SELECT * FROM orders IGNORE INDEX (idx_status) WHERE status = 'pending';
```

---

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
const db = require('./db');

// Create index
await db.query('CREATE INDEX idx_email ON customers(email)');

// Explain a query to check performance
const [explanation] = await db.query(
  'EXPLAIN SELECT * FROM products WHERE price > ? AND status = ?',
  [10000, 'published']
);
console.table(explanation);

// Show all indexes on a table
const [indexes] = await db.query('SHOW INDEX FROM products');
console.table(indexes);

// Fulltext search (after adding FULLTEXT index)
const [results] = await db.query(
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
      const [plan] = await db.query('EXPLAIN ' + sql, params);
      return res.json({ queryPlan: plan, sql });
    }
    
    const [products] = await db.query(sql, params);
    res.json({ count: products.length, products });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Index management route (admin only)
app.get('/api/admin/indexes/:table', async (req, res) => {
  try {
    const [indexes] = await db.query('SHOW INDEX FROM ??', [req.params.table]);
    res.json({ table: req.params.table, indexes });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
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

## Real-World Q&A

### ❓ Q1: In MongoDB, `_id` is auto-indexed. What about MySQL?
> **💡 Answer:** The PRIMARY KEY column is auto-indexed (clustered index). UNIQUE columns are also auto-indexed. But foreign keys (`customer_id`, `category_id`) are NOT auto-indexed in MySQL — you must add them manually! This is a common optimization miss.

### ❓ Q2: How many indexes should a table have?
> **💡 Answer:** No fixed rule, but guidelines: Index every foreign key column. Index columns frequently used in WHERE, JOIN ON, and ORDER BY. Don't index columns with low cardinality (e.g., boolean/status with only 2-3 values). A typical table might have 3-7 indexes. Monitor and adjust based on EXPLAIN results.

### ❓ Q3: Does having an index guarantee MySQL will use it?
> **💡 Answer:** No! MySQL's optimizer decides whether to use an index based on cardinality, data distribution, and query structure. If an index would return >30% of the table rows, MySQL may prefer a full table scan. Use EXPLAIN to verify.

---

## Interview Q&A

### ❓ Q1: What is an index and why is it important?
> **💡 Answer:** An index is a data structure (B-tree) that allows the database to find rows quickly without scanning the entire table. Like a book's index — instead of reading every page, you look up the topic and go directly to the page. Indexes are crucial for performance; a query on 1M rows can go from seconds to milliseconds.

### ❓ Q2: What are the disadvantages of indexes?
> **💡 Answer:** (1) Extra storage space. (2) Slower INSERT/UPDATE/DELETE because indexes must be updated. (3) Index maintenance overhead. The tradeoff: faster reads vs slower writes. For read-heavy apps (most web apps), the tradeoff is worth it.

### ❓ Q3: What is a composite index and how does the leftmost prefix rule work?
> **💡 Answer:** A composite index is on multiple columns: `INDEX(a, b, c)`. The leftmost prefix rule means the index can be used for queries on (a), (a,b), or (a,b,c) but NOT (b), (c), or (b,c) alone. Column order matters — put the most selective (highest cardinality) column first.

### ❓ Q4: What is the difference between clustered and non-clustered indexes?
> **💡 Answer:** Clustered index: the table data is physically ordered by this index. MySQL's PRIMARY KEY is the clustered index — only one per table. Non-clustered index: a separate structure that points to the actual rows. You can have multiple non-clustered indexes. Think: clustered = the book itself (ordered by chapters), non-clustered = the book's back index.

### ❓ Q5: How would you find and fix slow queries in a production MySQL database?
> **💡 Answer:** (1) Enable slow query log: `SET GLOBAL slow_query_log = 'ON'`. (2) Check queries with `EXPLAIN ANALYZE`. (3) Look for type=ALL (full scan) and key=NULL. (4) Add indexes on columns in WHERE, JOIN, ORDER BY. (5) Monitor with `SHOW PROCESSLIST`. (6) Use tools like `pt-query-digest`. (7) Consider query rewrites, denormalization, or caching for genuinely complex queries.

### ❓ Q6: Why does a range condition on column B prevent column C from utilizing a composite index `(A, B, C)`?
> **💡 Answer:** In a B+Tree, index records are sorted in strict lexicographical order: first by `A`, then by `B` within the same `A`, then by `C` within the same `B`. Once a query applies a range filter on `B` (`WHERE a = 1 AND b > 10 AND c = 5`), multiple distinct `B` values match. Because `C` is only sorted *relative to a single fixed value of B*, across multiple distinct `B` values the values of `C` are no longer in continuous sorted order. The engine must scan the index range for `(A=1, B>10)` and manually filter `C=5` using Index Condition Pushdown (ICP).

### ❓ Q7: What is a Covering Index and how do you confirm it in `EXPLAIN`?
> **💡 Answer:** A Covering Index contains 100% of the columns requested in the query's `SELECT`, `WHERE`, `JOIN`, and `ORDER BY` clauses within its own leaf pages. When used, the database retrieves all requested data directly from the index tree without making a second random I/O hop to the Clustered Index (Bookmark Lookup). You confirm it when `EXPLAIN` shows `Using index` in the `Extra` column.

---

| [← Previous: Views](./14_Views.md) | [Index](./00_index.md) | [Next: Transactions →](./16_Transactions.md) |
|---|---|---|
