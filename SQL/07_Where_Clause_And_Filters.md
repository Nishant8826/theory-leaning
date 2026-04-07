# WHERE Clause And Filters

> 📌 **File:** `07_Where_Clause_And_Filters.md` | **Level:** Beginner → MERN Developer

---

## What is it?

The WHERE clause filters rows based on conditions — it's the SQL equivalent of the filter object you pass to Mongoose's `.find()`. Just like `User.find({ age: { $gte: 18 } })` returns only adults, `SELECT * FROM users WHERE age >= 18` does the same thing.

WHERE is used with SELECT, UPDATE, and DELETE to specify which rows to affect.

---

## MERN Parallel — You Already Know This!

| Mongoose Query Filter                         | SQL WHERE Clause                              |
|-----------------------------------------------|-----------------------------------------------|
| `{ age: 25 }`                                 | `WHERE age = 25`                              |
| `{ age: { $gt: 25 } }`                        | `WHERE age > 25`                              |
| `{ age: { $gte: 18, $lte: 30 } }`            | `WHERE age >= 18 AND age <= 30`               |
| `{ age: { $ne: 0 } }`                         | `WHERE age != 0` or `WHERE age <> 0`          |
| `{ $or: [{ city: 'Delhi' }, { city: 'Mumbai' }] }` | `WHERE city = 'Delhi' OR city = 'Mumbai'`  |
| `{ city: { $in: ['Delhi', 'Mumbai'] } }`      | `WHERE city IN ('Delhi', 'Mumbai')`           |
| `{ city: { $nin: ['Delhi'] } }`               | `WHERE city NOT IN ('Delhi')`                 |
| `{ name: /^Ni/i }`                            | `WHERE name LIKE 'Ni%'`                       |
| `{ phone: { $exists: true } }`                | `WHERE phone IS NOT NULL`                     |
| `{ phone: { $exists: false } }`               | `WHERE phone IS NULL`                         |
| `{ age: { $gte: 18 }, city: 'Delhi' }`        | `WHERE age >= 18 AND city = 'Delhi'`          |
| `{ $and: [condition1, condition2] }`           | `WHERE condition1 AND condition2`             |

---

## Why does it matter?

- Without WHERE, UPDATE changes ALL rows and DELETE removes ALL rows
- WHERE is used in 90%+ of all real-world queries
- Proper filtering at the database level is 100x faster than filtering in JavaScript
- WHERE conditions determine whether indexes are used (performance critical)
- SQL injection attacks specifically target WHERE clauses

---

## How does it work?

### WHERE Evaluation

```
SELECT * FROM products WHERE price > 1000 AND category_id = 1;

Step 1: MySQL scans the products table
Step 2: For EACH row, evaluates: is price > 1000?
Step 3: For matching rows, evaluates: is category_id = 1?
Step 4: Only rows where BOTH conditions are TRUE are returned

Row 1: price=79999, cat=1 → TRUE AND TRUE → ✅ Returned
Row 2: price=299, cat=3   → FALSE AND TRUE → ❌ Skipped
Row 3: price=24900, cat=1 → TRUE AND TRUE → ✅ Returned
Row 4: price=12999, cat=2 → TRUE AND FALSE → ❌ Skipped
```

---

## Visual Diagram

### Comparison Operators

```
┌──────────┬───────────────┬──────────────────────────┬──────────────────────┐
│ Operator │ Meaning       │ SQL Example              │ Mongoose Equivalent  │
├──────────┼───────────────┼──────────────────────────┼──────────────────────┤
│ =        │ Equal         │ WHERE age = 25           │ { age: 25 }          │
│ != or <> │ Not equal     │ WHERE status != 'draft'  │ { status: {$ne:..} } │
│ >        │ Greater than  │ WHERE price > 1000       │ { price: {$gt:1000}} │
│ <        │ Less than     │ WHERE stock < 10         │ { stock: {$lt:10} }  │
│ >=       │ Greater/equal │ WHERE age >= 18          │ { age: {$gte:18} }   │
│ <=       │ Less/equal    │ WHERE rating <= 5        │ { rating:{$lte:5} }  │
└──────────┴───────────────┴──────────────────────────┴──────────────────────┘
```

### Logical Operators

```
┌──────────┬────────────────────────────────────────────────────────┐
│ AND      │ Both conditions must be true                          │
│          │ WHERE age >= 18 AND city = 'Delhi'                    │
│          │ Mongoose: { age: {$gte:18}, city: 'Delhi' }           │
├──────────┼────────────────────────────────────────────────────────┤
│ OR       │ At least one condition must be true                   │
│          │ WHERE city = 'Delhi' OR city = 'Mumbai'               │
│          │ Mongoose: { $or: [{city:'Delhi'},{city:'Mumbai'}] }    │
├──────────┼────────────────────────────────────────────────────────┤
│ NOT      │ Negates a condition                                   │
│          │ WHERE NOT (status = 'cancelled')                      │
│          │ Mongoose: { status: {$ne: 'cancelled'} }              │
├──────────┼────────────────────────────────────────────────────────┤
│ IN       │ Matches any value in a list                           │
│          │ WHERE city IN ('Delhi', 'Mumbai', 'Bangalore')        │
│          │ Mongoose: { city: {$in: ['Delhi','Mumbai','Bang..']} } │
├──────────┼────────────────────────────────────────────────────────┤
│ BETWEEN  │ Range check (inclusive)                               │
│          │ WHERE price BETWEEN 1000 AND 5000                     │
│          │ Mongoose: { price: {$gte:1000, $lte:5000} }           │
├──────────┼────────────────────────────────────────────────────────┤
│ LIKE     │ Pattern matching (% = any chars, _ = one char)        │
│          │ WHERE name LIKE 'Ni%'                                 │
│          │ Mongoose: { name: /^Ni/i }                            │
├──────────┼────────────────────────────────────────────────────────┤
│ IS NULL  │ Check for NULL (can't use = NULL!)                    │
│          │ WHERE phone IS NULL                                   │
│          │ Mongoose: { phone: {$exists: false} }                  │
└──────────┴────────────────────────────────────────────────────────┘
```

### LIKE Patterns

```
LIKE 'A%'      → Starts with 'A'       (Amit, Asha, Arun)
LIKE '%a'      → Ends with 'a'         (Priya, Sneha, Asha)
LIKE '%kumar%' → Contains 'kumar'      (Raj Kumar, Kumar Singh)
LIKE 'A__'     → 'A' + exactly 2 chars (Ash, Ami, Amu)
LIKE '_a%'     → 2nd character is 'a'  (Raj, Sam, Jas)

_ = exactly one character
% = zero or more characters
```

---

## Syntax

```sql
-- ============================================
-- COMPARISON OPERATORS
-- ============================================
SELECT * FROM products WHERE price = 79999;
SELECT * FROM products WHERE price > 10000;
SELECT * FROM products WHERE price >= 10000;
SELECT * FROM products WHERE price < 5000;
SELECT * FROM products WHERE stock <= 0;
SELECT * FROM products WHERE status != 'draft';
SELECT * FROM products WHERE status <> 'draft';  -- Same as !=

-- ============================================
-- LOGICAL OPERATORS
-- ============================================

-- AND — all conditions must be true
SELECT * FROM products 
WHERE price > 1000 AND stock > 0 AND status = 'published';

-- OR — at least one condition must be true
SELECT * FROM products 
WHERE category_id = 1 OR category_id = 2;

-- NOT — negate a condition
SELECT * FROM products WHERE NOT (status = 'draft');

-- Combined (use parentheses for clarity!)
SELECT * FROM products
WHERE (category_id = 1 OR category_id = 2) 
  AND price > 5000 
  AND status = 'published';

-- ============================================
-- IN — Match against a list
-- ============================================
SELECT * FROM customers WHERE city IN ('Delhi', 'Mumbai', 'Bangalore');
SELECT * FROM orders WHERE status IN ('pending', 'processing');
SELECT * FROM products WHERE category_id NOT IN (1, 2);

-- ============================================
-- BETWEEN — Range (inclusive on both ends)
-- ============================================
SELECT * FROM products WHERE price BETWEEN 1000 AND 10000;
-- Same as: WHERE price >= 1000 AND price <= 10000;

SELECT * FROM orders 
WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- ============================================
-- LIKE — Pattern matching
-- ============================================
SELECT * FROM customers WHERE name LIKE 'N%';          -- Starts with N
SELECT * FROM customers WHERE email LIKE '%@gmail.com'; -- Gmail users
SELECT * FROM products WHERE name LIKE '%phone%';       -- Contains 'phone'
SELECT * FROM customers WHERE phone LIKE '98%';         -- Phone starts with 98

-- Case-insensitive by default in MySQL (depends on collation)
SELECT * FROM customers WHERE name LIKE '%nishant%';    -- Finds 'Nishant' too

-- ============================================
-- IS NULL / IS NOT NULL
-- ============================================
SELECT * FROM customers WHERE phone IS NULL;        -- No phone number
SELECT * FROM customers WHERE phone IS NOT NULL;    -- Has phone number

-- ⚠️ WRONG: WHERE phone = NULL   (always returns empty!)
-- ✅ RIGHT: WHERE phone IS NULL

-- ============================================
-- EXISTS (check if subquery returns any rows)
-- ============================================
SELECT * FROM customers c WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
-- Returns customers who have at least one order
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Mongoose (What You Know) ==========

// Simple filter
const products = await Product.find({ category: 'Electronics' });

// Multiple conditions (AND)
const products = await Product.find({
  price: { $gte: 1000, $lte: 50000 },
  status: 'published',
  stock: { $gt: 0 }
});

// OR condition
const products = await Product.find({
  $or: [
    { category: 'Electronics' },
    { category: 'Books' }
  ]
});

// Regex search
const products = await Product.find({
  name: { $regex: 'iphone', $options: 'i' }
});

// Null check
const customers = await Customer.find({
  phone: { $exists: true, $ne: null }
});
```

```sql
-- ========== MySQL ==========

-- Simple filter
SELECT * FROM products WHERE category_id = 1;

-- Multiple conditions (AND)
SELECT * FROM products
WHERE price >= 1000 AND price <= 50000
  AND status = 'published'
  AND stock > 0;

-- OR condition
SELECT * FROM products
WHERE category_id IN (1, 3);

-- Pattern search (like regex)
SELECT * FROM products WHERE name LIKE '%iphone%';

-- Null check
SELECT * FROM customers WHERE phone IS NOT NULL;
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Simple filter with parameterized query
const [products] = await pool.query(
  'SELECT * FROM products WHERE category_id = ?',
  [1]
);

// Multiple conditions
const [products] = await pool.query(
  `SELECT * FROM products
   WHERE price >= ? AND price <= ?
     AND status = ?
     AND stock > 0`,
  [1000, 50000, 'published']
);

// Dynamic filters (common in search APIs)
async function searchProducts(filters) {
  let sql = 'SELECT * FROM products WHERE 1=1';  // 1=1 is always true (base)
  const params = [];

  if (filters.minPrice) {
    sql += ' AND price >= ?';
    params.push(filters.minPrice);
  }
  if (filters.maxPrice) {
    sql += ' AND price <= ?';
    params.push(filters.maxPrice);
  }
  if (filters.category) {
    sql += ' AND category_id = ?';
    params.push(filters.category);
  }
  if (filters.search) {
    sql += ' AND name LIKE ?';
    params.push(`%${filters.search}%`);
  }
  if (filters.status) {
    sql += ' AND status = ?';
    params.push(filters.status);
  }

  const [products] = await pool.query(sql, params);
  return products;
}
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize ==========
const { Op } = require('sequelize');

// Simple filter
const products = await Product.findAll({
  where: { categoryId: 1 }
});

// Multiple conditions (AND — default)
const products = await Product.findAll({
  where: {
    price: { [Op.between]: [1000, 50000] },
    status: 'published',
    stock: { [Op.gt]: 0 }
  }
});

// OR condition
const products = await Product.findAll({
  where: {
    [Op.or]: [
      { categoryId: 1 },
      { categoryId: 3 }
    ]
  }
});

// LIKE search
const products = await Product.findAll({
  where: {
    name: { [Op.like]: '%iphone%' }
  }
});

// NULL check
const customers = await Customer.findAll({
  where: {
    phone: { [Op.not]: null }
  }
});

// IN
const products = await Product.findAll({
  where: {
    status: { [Op.in]: ['published', 'draft'] }
  }
});
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Product search and filter API (like an e-commerce filter sidebar)

```sql
-- SQL: Complex product search with filters
SELECT 
  p.id, p.name, p.price, p.stock,
  c.name AS category,
  p.status
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.status = 'published'
  AND p.price BETWEEN 500 AND 100000
  AND p.stock > 0
  AND (p.name LIKE '%phone%' OR p.description LIKE '%phone%')
  AND p.category_id IN (1, 2)
ORDER BY p.price ASC
LIMIT 20;
```

```js
// Node.js + Express — Search API with dynamic filters
app.get('/api/products/search', async (req, res) => {
  try {
    const { search, minPrice, maxPrice, categories, status, inStock, sort, limit } = req.query;
    
    let sql = `
      SELECT p.id, p.name, p.price, p.stock, c.name AS category, p.status
      FROM products p
      LEFT JOIN categories c ON p.category_id = c.id
      WHERE 1=1
    `;
    const params = [];
    
    // Search by name or description
    if (search) {
      sql += ' AND (p.name LIKE ? OR p.description LIKE ?)';
      params.push(`%${search}%`, `%${search}%`);
    }
    
    // Price range
    if (minPrice) {
      sql += ' AND p.price >= ?';
      params.push(Number(minPrice));
    }
    if (maxPrice) {
      sql += ' AND p.price <= ?';
      params.push(Number(maxPrice));
    }
    
    // Category filter (comma-separated IDs)
    if (categories) {
      const catIds = categories.split(',').map(Number);
      sql += ` AND p.category_id IN (${catIds.map(() => '?').join(',')})`;
      params.push(...catIds);
    }
    
    // Status filter
    if (status) {
      sql += ' AND p.status = ?';
      params.push(status);
    }
    
    // In-stock only
    if (inStock === 'true') {
      sql += ' AND p.stock > 0';
    }
    
    // Sorting
    const sortOptions = {
      'price_asc': 'p.price ASC',
      'price_desc': 'p.price DESC',
      'newest': 'p.created_at DESC',
      'name': 'p.name ASC'
    };
    sql += ` ORDER BY ${sortOptions[sort] || 'p.created_at DESC'}`;
    
    // Pagination
    sql += ' LIMIT ?';
    params.push(Number(limit) || 20);
    
    const [products] = await pool.query(sql, params);
    
    res.json({ count: products.length, products });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// React — Search & Filter Component
import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

function ProductSearch() {
  const [products, setProducts] = useState([]);
  const [filters, setFilters] = useState({
    search: '', minPrice: '', maxPrice: '',
    categories: '', inStock: true, sort: 'newest'
  });

  const fetchProducts = useCallback(async () => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, val]) => {
      if (val !== '' && val !== undefined) params.set(key, val);
    });
    
    const { data } = await axios.get(`/api/products/search?${params}`);
    setProducts(data.products);
  }, [filters]);

  useEffect(() => {
    const timer = setTimeout(fetchProducts, 300); // Debounce
    return () => clearTimeout(timer);
  }, [fetchProducts]);

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      {/* Filter Sidebar */}
      <div style={{ width: '250px' }}>
        <h3>Filters</h3>
        <input placeholder="Search..." value={filters.search}
          onChange={e => setFilters({...filters, search: e.target.value})} />
        
        <h4>Price Range</h4>
        <input type="number" placeholder="Min" value={filters.minPrice}
          onChange={e => setFilters({...filters, minPrice: e.target.value})} />
        <input type="number" placeholder="Max" value={filters.maxPrice}
          onChange={e => setFilters({...filters, maxPrice: e.target.value})} />
        
        <h4>Sort By</h4>
        <select value={filters.sort}
          onChange={e => setFilters({...filters, sort: e.target.value})}>
          <option value="newest">Newest First</option>
          <option value="price_asc">Price: Low to High</option>
          <option value="price_desc">Price: High to Low</option>
          <option value="name">Name A-Z</option>
        </select>
        
        <label>
          <input type="checkbox" checked={filters.inStock}
            onChange={e => setFilters({...filters, inStock: e.target.checked})} />
          In Stock Only
        </label>
      </div>

      {/* Product Grid */}
      <div>
        <p>{products.length} products found</p>
        {products.map(p => (
          <div key={p.id} style={{ border: '1px solid #ddd', padding: '10px', marginBottom: '10px' }}>
            <h3>{p.name}</h3>
            <p>₹{p.price} | {p.category} | Stock: {p.stock}</p>
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
  "count": 2,
  "products": [
    { "id": 1, "name": "iPhone 15", "price": "79999.00", "stock": 50, "category": "Electronics", "status": "published" },
    { "id": 5, "name": "AirPods Pro", "price": "24900.00", "stock": 100, "category": "Electronics", "status": "published" }
  ]
}
```

---

## Impact

| If You Don't Understand WHERE...        | What Happens                                    |
|-----------------------------------------|-------------------------------------------------|
| Forget WHERE in UPDATE/DELETE            | ALL rows affected — data disaster                |
| Use `= NULL` instead of `IS NULL`        | Query returns empty — silent bug                 |
| Don't parameterize WHERE values          | SQL injection vulnerability                      |
| Filter in JavaScript instead of SQL      | 10x slower — fetching all rows then filtering    |
| Wrong operator precedence (AND/OR)       | Wrong results — use parentheses!                 |
| Use LIKE '%value%' on large tables       | Full table scan — extremely slow without index   |

### Operator Precedence Trap

```sql
-- ⚠️ WRONG — AND has higher precedence than OR!
SELECT * FROM products
WHERE category_id = 1 OR category_id = 2 AND price > 10000;
-- This means: category_id = 1 OR (category_id = 2 AND price > 10000)
-- Returns ALL Electronics + only expensive Clothing

-- ✅ CORRECT — Use parentheses!
SELECT * FROM products
WHERE (category_id = 1 OR category_id = 2) AND price > 10000;
-- Returns expensive products from either category
```

---

## Practice Exercises

### Easy (SQL)
1. Select all products with price greater than 5000
2. Select customers whose name starts with 'N'
3. Select orders with status 'pending' or 'processing'
4. Select products where stock is NULL

### Medium (SQL + Node.js)
5. Build a search API that accepts `?search=`, `?minPrice=`, `?maxPrice=` query params
6. Write a query to find customers who registered in the last 30 days
7. Find products that are published, in stock, and in the price range 1000-50000

### Hard (Full Stack)
8. Build a complete filter sidebar with: search box, price range slider, category checkboxes, sort dropdown, in-stock toggle — all connected to the search API
9. Implement full-text search using MySQL's FULLTEXT index and `MATCH ... AGAINST` syntax

---

## Real-World Q&A

**Q1:** I used `WHERE phone = NULL` and got no results even though some customers have NULL phone. Why?
**A:** In SQL, NULL is not a value — it's the absence of a value. You cannot compare with `=`. Use `IS NULL` or `IS NOT NULL`. Think of it like JavaScript's `undefined` — `undefined === undefined` evaluates to true in JS, but SQL's `NULL = NULL` evaluates to NULL (unknown), not TRUE.

**Q2:** Is the WHERE `1=1` pattern a security risk?
**A:** No, `1=1` is always TRUE and acts as a convenient base for dynamically adding AND conditions. Without it, you'd need special logic for the first condition (no AND prefix). It has zero performance impact — the optimizer removes it. It's a common pattern in query builders.

**Q3:** How do I search across multiple columns efficiently?
**A:** For simple searches, use `WHERE name LIKE '%term%' OR description LIKE '%term%'`. For production, use MySQL's FULLTEXT index: `ALTER TABLE products ADD FULLTEXT(name, description)` then query with `WHERE MATCH(name, description) AGAINST('search term')`. FULLTEXT is much faster on large datasets.

---

## Interview Q&A

**Q1: What is the difference between WHERE and HAVING?**
WHERE filters rows BEFORE grouping (applied to individual rows). HAVING filters groups AFTER grouping (applied after GROUP BY). WHERE cannot use aggregate functions; HAVING can. Example: `WHERE price > 100` filters rows; `HAVING COUNT(*) > 5` filters groups.

**Q2: Why can't you use `= NULL` to check for NULL values?**
NULL represents unknown/missing data. Any comparison with NULL returns NULL (unknown), not TRUE or FALSE. `NULL = NULL` is NULL, not TRUE. SQL provides IS NULL and IS NOT NULL specifically for NULL checks. This is called three-valued logic (TRUE, FALSE, NULL).

**Q3: What is the difference between IN and EXISTS?**
`IN` checks if a value matches any value in a list or subquery result. `EXISTS` checks if a subquery returns any rows. EXISTS is generally faster for correlated subqueries on large datasets because it stops at the first match. IN is simpler and better for small lists.

**Q4: How does LIKE differ from regular expressions in MySQL?**
LIKE uses simple patterns: `%` (any characters) and `_` (one character). For complex patterns, use `REGEXP`: `WHERE name REGEXP '^[A-Z]'`. LIKE is faster and sufficient for most cases. REGEXP is more powerful but slower. In MongoDB terms, LIKE is a simplified regex.

**Q5: You have a products table with 10 million rows. A query using `WHERE name LIKE '%phone%'` is slow. How would you fix it?**
Leading wildcard `%phone%` prevents index usage, causing a full table scan. Solutions: (1) Add a FULLTEXT index and use `MATCH...AGAINST`. (2) Use an external search engine like Elasticsearch. (3) If prefix search is sufficient, use `LIKE 'phone%'` which can use a regular index. (4) Create a generated column with a reversed name for suffix searches a. (5) Implement application-level caching for common searches.

---

| [← Previous: SELECT Basics](./06_Select_Basics.md) | [Next: Sorting & Limiting →](./08_Sorting_And_Limiting.md) |
|---|---|
