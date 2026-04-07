# Sorting And Limiting

> 📌 **File:** `08_Sorting_And_Limiting.md` | **Level:** Beginner → MERN Developer

---

## What is it?

**ORDER BY** sorts query results (like Mongoose's `.sort()`), and **LIMIT** restricts how many rows are returned (like Mongoose's `.limit()`). Together with **OFFSET**, they enable pagination — the backbone of any list/feed in your app.

---

## MERN Parallel — You Already Know This!

| Mongoose (You Know)                           | MySQL (You'll Learn)                            |
|-----------------------------------------------|-------------------------------------------------|
| `.sort({ price: 1 })`                        | `ORDER BY price ASC`                            |
| `.sort({ price: -1 })`                       | `ORDER BY price DESC`                           |
| `.sort({ category: 1, price: -1 })`          | `ORDER BY category ASC, price DESC`             |
| `.limit(10)`                                  | `LIMIT 10`                                      |
| `.skip(20)`                                   | `OFFSET 20` (or `LIMIT 10 OFFSET 20`)          |
| `.skip(20).limit(10)`                         | `LIMIT 10 OFFSET 20`                           |
| Page 3 with 10/page: `.skip(20).limit(10)`   | `LIMIT 10 OFFSET 20`                           |

---

## Why does it matter?

- Every list page needs sorting (newest first, price low-to-high, etc.)
- Pagination is essential — you can't send 1 million products to the frontend
- Proper LIMIT prevents memory issues and slow responses
- Understanding OFFSET helps build infinite scroll and page-based navigation
- ORDER BY without an index causes expensive sorting operations

---

## How does it work?

### Pagination Formula

```
Page 1: LIMIT 10 OFFSET 0   → Rows 1-10
Page 2: LIMIT 10 OFFSET 10  → Rows 11-20
Page 3: LIMIT 10 OFFSET 20  → Rows 21-30

Formula: OFFSET = (page - 1) × limit

In Mongoose: .skip((page - 1) * limit).limit(limit)
In MySQL:    LIMIT limit OFFSET (page - 1) * limit
```

---

## Visual Diagram

### ORDER BY Visualization

```
Original (unordered):              ORDER BY price ASC:
┌────┬──────────┬─────────┐       ┌────┬──────────┬─────────┐
│ id │ name     │ price   │       │ id │ name     │ price   │
├────┼──────────┼─────────┤       ├────┼──────────┼─────────┤
│ 1  │ iPhone   │ 79999   │       │ 4  │ Alchemist│ 299     │ ↑
│ 2  │ MacBook  │ 114900  │       │ 3  │ Jeans    │ 2499    │ │
│ 3  │ Jeans    │ 2499    │       │ 5  │ AirPods  │ 24900   │ │ ASC
│ 4  │ Alchemist│ 299     │       │ 1  │ iPhone   │ 79999   │ │
│ 5  │ AirPods  │ 24900   │       │ 2  │ MacBook  │ 114900  │ │
└────┴──────────┴─────────┘       └────┴──────────┴─────────┘

ORDER BY price DESC:               ORDER BY price DESC LIMIT 3:
┌────┬──────────┬─────────┐       ┌────┬──────────┬─────────┐
│ id │ name     │ price   │       │ id │ name     │ price   │
├────┼──────────┼─────────┤       ├────┼──────────┼─────────┤
│ 2  │ MacBook  │ 114900  │ ↓     │ 2  │ MacBook  │ 114900  │  Only
│ 1  │ iPhone   │ 79999   │ │     │ 1  │ iPhone   │ 79999   │  top 3
│ 5  │ AirPods  │ 24900   │ DESC  │ 5  │ AirPods  │ 24900   │  rows!
│ 3  │ Jeans    │ 2499    │ │     └────┴──────────┴─────────┘
│ 4  │ Alchemist│ 299     │ │
└────┴──────────┴─────────┘
```

### Pagination

```
Total: 50 products, 10 per page

Page 1: LIMIT 10 OFFSET 0    → Products 1-10
Page 2: LIMIT 10 OFFSET 10   → Products 11-20
Page 3: LIMIT 10 OFFSET 20   → Products 21-30
Page 4: LIMIT 10 OFFSET 30   → Products 31-40
Page 5: LIMIT 10 OFFSET 40   → Products 41-50

┌──────────────────────────────────────────────────────┐
│  [1]  [2]  [3]  [4]  [5]    ← Pagination buttons    │
│   ↑                                                  │
│  OFFSET=0                                            │
│  LIMIT=10                                            │
│                                                      │
│  « Previous  Page 2 of 5  Next »                     │
└──────────────────────────────────────────────────────┘
```

---

## Syntax

```sql
-- ============================================
-- ORDER BY — Sorting
-- ============================================

-- Sort ascending (default)
SELECT * FROM products ORDER BY price;       -- ASC is default
SELECT * FROM products ORDER BY price ASC;   -- Explicit ascending

-- Sort descending
SELECT * FROM products ORDER BY price DESC;

-- Sort by multiple columns
SELECT * FROM products ORDER BY category_id ASC, price DESC;
-- First sorts by category, then within each category, by price descending

-- Sort by column position (not recommended but valid)
SELECT name, price FROM products ORDER BY 2 DESC;  -- 2 = second column (price)

-- Sort by alias
SELECT name, price * stock AS total_value 
FROM products 
ORDER BY total_value DESC;

-- Sort by expression
SELECT * FROM products ORDER BY price * stock DESC;

-- NULL values in sort (NULLs appear first in ASC, last in DESC)
SELECT * FROM customers ORDER BY phone ASC;  -- NULLs first
SELECT * FROM customers ORDER BY phone DESC; -- NULLs last


-- ============================================
-- LIMIT — Restrict rows returned
-- ============================================

-- Get top 5 products
SELECT * FROM products LIMIT 5;

-- Get top 3 most expensive products
SELECT * FROM products ORDER BY price DESC LIMIT 3;

-- Cheapest product
SELECT * FROM products ORDER BY price ASC LIMIT 1;

-- LIMIT with OFFSET — Pagination
SELECT * FROM products LIMIT 10 OFFSET 0;   -- Page 1 (rows 1-10)
SELECT * FROM products LIMIT 10 OFFSET 10;  -- Page 2 (rows 11-20)
SELECT * FROM products LIMIT 10 OFFSET 20;  -- Page 3 (rows 21-30)

-- Short syntax (LIMIT offset, count)
SELECT * FROM products LIMIT 0, 10;   -- Same as LIMIT 10 OFFSET 0
SELECT * FROM products LIMIT 10, 10;  -- Same as LIMIT 10 OFFSET 10
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Mongoose ==========

// Sort by price ascending
const products = await Product.find().sort({ price: 1 });

// Sort descending, limit 5
const top5 = await Product.find().sort({ price: -1 }).limit(5);

// Pagination
const page = 2, limit = 10;
const products = await Product.find()
  .sort({ createdAt: -1 })
  .skip((page - 1) * limit)
  .limit(limit);

const total = await Product.countDocuments();
```

```sql
-- ========== MySQL ==========

-- Sort by price ascending
SELECT * FROM products ORDER BY price ASC;

-- Sort descending, limit 5
SELECT * FROM products ORDER BY price DESC LIMIT 5;

-- Pagination (page 2, 10 per page)
SELECT * FROM products
ORDER BY created_at DESC
LIMIT 10 OFFSET 10;

-- Total count
SELECT COUNT(*) AS total FROM products;
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Sort by price ascending
const [products] = await pool.query(
  'SELECT * FROM products ORDER BY price ASC'
);

// Top 5 most expensive
const [top5] = await pool.query(
  'SELECT * FROM products ORDER BY price DESC LIMIT 5'
);

// Pagination function
async function getProducts(page = 1, limit = 10, sortBy = 'created_at', order = 'DESC') {
  const offset = (page - 1) * limit;
  
  // Whitelist allowed sort columns (prevent SQL injection!)
  const allowedSorts = ['price', 'name', 'created_at', 'stock'];
  const sortColumn = allowedSorts.includes(sortBy) ? sortBy : 'created_at';
  const sortOrder = order.toUpperCase() === 'ASC' ? 'ASC' : 'DESC';
  
  // Get paginated results
  const [products] = await pool.query(
    `SELECT * FROM products ORDER BY ${sortColumn} ${sortOrder} LIMIT ? OFFSET ?`,
    [limit, offset]
  );
  
  // Get total count for pagination metadata
  const [countResult] = await pool.query('SELECT COUNT(*) AS total FROM products');
  const total = countResult[0].total;
  
  return {
    products,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
      hasNext: page * limit < total,
      hasPrev: page > 1
    }
  };
}
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize ==========

// Sort + Limit
const products = await Product.findAll({
  order: [['price', 'DESC']],  // Like sort({ price: -1 })
  limit: 5
});

// Multiple sorts
const products = await Product.findAll({
  order: [
    ['categoryId', 'ASC'],
    ['price', 'DESC']
  ]
});

// Pagination with metadata
const { count, rows: products } = await Product.findAndCountAll({
  order: [['createdAt', 'DESC']],
  limit: 10,
  offset: 10  // Page 2
});
// count = total number of records
// rows = this page's records
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Paginated product listing with sorting

```sql
-- SQL: Products with pagination and sorting
SELECT 
  p.id, p.name, p.price, p.stock,
  c.name AS category
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.status = 'published'
ORDER BY p.price ASC
LIMIT 10 OFFSET 0;

-- Total count for pagination
SELECT COUNT(*) AS total 
FROM products 
WHERE status = 'published';
```

```js
// Node.js + Express — Paginated Products API
app.get('/api/products', async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = Math.min(parseInt(req.query.limit) || 10, 100); // Max 100
    const offset = (page - 1) * limit;
    const sortBy = req.query.sortBy || 'created_at';
    const order = req.query.order || 'DESC';
    const search = req.query.search || '';
    
    // Whitelist sort columns
    const allowedSorts = { price: 'p.price', name: 'p.name', created_at: 'p.created_at', stock: 'p.stock' };
    const sortColumn = allowedSorts[sortBy] || 'p.created_at';
    const sortOrder = order.toUpperCase() === 'ASC' ? 'ASC' : 'DESC';
    
    // Build WHERE clause
    let whereClause = "WHERE p.status = 'published'";
    const params = [];
    
    if (search) {
      whereClause += ' AND (p.name LIKE ? OR p.description LIKE ?)';
      params.push(`%${search}%`, `%${search}%`);
    }
    
    // Get paginated results
    const [products] = await pool.query(`
      SELECT p.id, p.name, p.price, p.stock, c.name AS category
      FROM products p
      LEFT JOIN categories c ON p.category_id = c.id
      ${whereClause}
      ORDER BY ${sortColumn} ${sortOrder}
      LIMIT ? OFFSET ?
    `, [...params, limit, offset]);
    
    // Get total count
    const [countResult] = await pool.query(
      `SELECT COUNT(*) AS total FROM products p ${whereClause}`,
      params
    );
    const total = countResult[0].total;
    
    res.json({
      products,
      pagination: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
        hasNext: page * limit < total,
        hasPrev: page > 1
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// React — Paginated Product List
import { useState, useEffect } from 'react';
import axios from 'axios';

function PaginatedProducts() {
  const [products, setProducts] = useState([]);
  const [pagination, setPagination] = useState({});
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState('created_at');
  const [order, setOrder] = useState('DESC');

  useEffect(() => {
    axios.get(`/api/products?page=${page}&limit=10&sortBy=${sortBy}&order=${order}`)
      .then(({ data }) => {
        setProducts(data.products);
        setPagination(data.pagination);
      });
  }, [page, sortBy, order]);

  return (
    <div>
      {/* Sort Controls */}
      <div>
        <select value={sortBy} onChange={e => { setSortBy(e.target.value); setPage(1); }}>
          <option value="created_at">Newest</option>
          <option value="price">Price</option>
          <option value="name">Name</option>
        </select>
        <button onClick={() => setOrder(o => o === 'ASC' ? 'DESC' : 'ASC')}>
          {order === 'ASC' ? '↑' : '↓'}
        </button>
      </div>

      {/* Product List */}
      {products.map(p => (
        <div key={p.id}>
          <strong>{p.name}</strong> — ₹{p.price} ({p.category})
        </div>
      ))}

      {/* Pagination Controls */}
      <div>
        <button disabled={!pagination.hasPrev} onClick={() => setPage(p => p - 1)}>
          ← Previous
        </button>
        <span> Page {pagination.page} of {pagination.totalPages} </span>
        <button disabled={!pagination.hasNext} onClick={() => setPage(p => p + 1)}>
          Next →
        </button>
      </div>
      <p>Total: {pagination.total} products</p>
    </div>
  );
}
```

**Output:**
```json
{
  "products": [
    { "id": 4, "name": "The Alchemist", "price": "299.00", "stock": 500, "category": "Books" },
    { "id": 3, "name": "Levi's Jeans", "price": "2499.00", "stock": 200, "category": "Clothing" }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 5,
    "totalPages": 1,
    "hasNext": false,
    "hasPrev": false
  }
}
```

---

## Impact

| If You Don't Understand This...           | What Happens                                    |
|-------------------------------------------|-------------------------------------------------|
| Don't use LIMIT                           | API returns 1M rows → crashes browser/server     |
| Wrong OFFSET calculation                  | Users see duplicate or missing items              |
| Sort by unindexed column on large table   | Slow query — MySQL sorts all rows in temp table  |
| Don't whitelist sort columns              | SQL injection through sort parameter              |
| Forget total count query                  | Can't show "Page X of Y" or disable Next button  |
| Use large OFFSET (e.g., OFFSET 1000000)  | Very slow — MySQL still scans 1M rows            |

### The Large OFFSET Problem

```sql
-- Page 1: Fast ✅
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 0;
-- MySQL reads 10 rows

-- Page 100,000: SLOW! ❌
SELECT * FROM products ORDER BY id LIMIT 10 OFFSET 999990;
-- MySQL reads 1,000,000 rows, then discards 999,990!

-- Solution: Cursor-based pagination (keyset pagination)
-- Instead of OFFSET, use the last seen ID:
SELECT * FROM products WHERE id > 999990 ORDER BY id LIMIT 10;
-- MySQL uses the index to jump directly to id 999990 ✅
```

---

## Practice Exercises

### Easy (SQL)
1. Select all products sorted by price (cheapest first)
2. Get the 3 most expensive products
3. Get products on page 2 (10 per page), sorted by name

### Medium (SQL + Node.js)
4. Build a pagination API that returns `{ data, pagination }` with hasNext/hasPrev
5. Implement cursor-based pagination using `WHERE id > ?` instead of OFFSET
6. Add sort parameter validation (whitelist allowed columns)

### Hard (Full Stack)
7. Build a data table component with:
   - Clickable column headers for sorting (toggle ASC/DESC)
   - Page navigation (first, prev, next, last)
   - Items per page selector (10, 25, 50, 100)
   - "Showing 11-20 of 157" text
8. Implement infinite scroll using cursor-based pagination

---

## Real-World Q&A

**Q1:** In Mongoose, `.sort('-createdAt')` is simple. Why is SQL ORDER BY more verbose?
**A:** SQL is explicit by design. `ORDER BY created_at DESC` clearly states the direction. The verbosity helps readability in complex queries with multiple sort columns. The trade-off is clarity over brevity.

**Q2:** What's the performance difference between OFFSET-based and cursor-based pagination?
**A:** OFFSET 100000 means MySQL scans 100,010 rows and discards 100,000. Cursor-based (`WHERE id > last_id LIMIT 10`) jumps directly to the right spot using the index — constant time regardless of page number. For large datasets (>10K pages), always use cursor-based.

**Q3:** Can I sort by a computed/alias column?
**A:** Yes! `SELECT price * stock AS total_value FROM products ORDER BY total_value DESC` works. MySQL evaluates the alias in ORDER BY. However, you CANNOT use aliases in WHERE (because WHERE runs before SELECT).

---

## Interview Q&A

**Q1: What is the difference between LIMIT and FETCH FIRST?**
LIMIT is MySQL-specific syntax. FETCH FIRST is the ANSI SQL standard (`SELECT * FROM products FETCH FIRST 10 ROWS ONLY`). Both limit result rows. MySQL supports LIMIT; PostgreSQL and Oracle support FETCH FIRST. For portability, know both.

**Q2: Explain OFFSET-based vs cursor-based pagination.**
OFFSET-based: `LIMIT 10 OFFSET 1000` — simple but slow for large offsets because the DB scans and discards rows. Cursor-based: `WHERE id > 1000 LIMIT 10` — uses indexes, constant performance. Tradeoff: cursor-based can't jump to arbitrary pages, only next/previous.

**Q3: What happens if ORDER BY is not specified? Is the result order guaranteed?**
No! Without ORDER BY, MySQL returns rows in an undefined order that may vary between executions. It often follows insertion order or index order, but this is NOT guaranteed. Always use ORDER BY if order matters.

**Q4: Can you ORDER BY a column not in the SELECT list?**
Yes. `SELECT name FROM products ORDER BY price DESC` is valid — products are sorted by price even though price isn't displayed. Exception: when using DISTINCT, you can only ORDER BY columns in the SELECT list.

**Q5: How would you get the Nth highest salary without using LIMIT?**
Using a subquery: `SELECT DISTINCT salary FROM employees e1 WHERE N-1 = (SELECT COUNT(DISTINCT salary) FROM employees e2 WHERE e2.salary > e1.salary)`. With LIMIT: `SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET N-1`. The LIMIT approach is simpler and faster.

---

| [← Previous: WHERE Clause & Filters](./07_Where_Clause_And_Filters.md) | [Next: Aggregate Functions →](./09_Aggregate_Functions.md) |
|---|---|
