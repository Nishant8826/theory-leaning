# Sorting and Limiting

> 📌 **File:** 08_Sorting_And_Limiting.md | **Level:** Beginner → MERN Developer

---

## What is it?
Sorting orders results ascending or descending. Limiting restricts the number of rows returned, powering offset-based pagination.

## MERN Parallel — You Already Know This!
- `sort({ price: -1 })` → `ORDER BY price DESC`
- `sort({ price: 1 })` → `ORDER BY price ASC`
- `limit(10)` → `LIMIT 10`
- `skip(20)` → `OFFSET 20`

## Why does it matter?
Essential for UX features like "Top 10 Rated", "Newest Arrivals", and preventing overloaded API responses via Pagination pages.

## How does it work?
Append `ORDER BY colName [ASC|DESC]` and `LIMIT [amount] OFFSET [amount]` at the end of the query string.

## Visual Diagram
```ascii
SELECT * FROM list ORDER BY price DESC LIMIT 2;

Original      Sorted DESC        LIMIT 2
$5            $25                $25
$1            $10     ====>      $10
$10           $5                 ---
$25           $1                 ---
```

## Syntax
```sql
-- Fully commented SQL syntax
SELECT * FROM products ORDER BY price DESC; -- Highest price first
SELECT * FROM products ORDER BY category ASC, price DESC; -- Multi-sort
SELECT * FROM products LIMIT 5; -- Top 5 only
SELECT * FROM products LIMIT 10 OFFSET 20; -- Page 3 (skips first 20)
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
await Product.find().sort({ price: -1 }).skip(10).limit(10);

// SQL
-- SELECT * FROM products ORDER BY price DESC LIMIT 10 OFFSET 10;

// Node.js using mysql2/promise (REQUIRED)
await pool.query('SELECT * FROM products ORDER BY price DESC LIMIT 10 OFFSET ?', [10]);

// ORM Equivalent (IMPORTANT)
// Prisma
await prisma.product.findMany({ orderBy: { price: 'desc' }, skip: 10, take: 10 });
```

### Raw SQL vs ORM
- **Raw SQL:** Requires careful math in JS to calculate the `OFFSET` from a frontend `page` query.
- **ORM:** Provides simpler logical bindings natively mapping page limits.

### Real-World Scenario + Full Stack Code
**Scenario:** A paginated Product API endpoint for React data grids.

```sql
-- SQL query
SELECT id, name, price FROM products ORDER BY created_at DESC LIMIT ? OFFSET ?;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.get('/api/products', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const offset = (page - 1) * limit;

  try {
    // Note: limit/offset parameters MUST be sent strictly as INTEGERS
    // mysql2 handles numeric parameterization automatically
    const [rows] = await pool.query(
      'SELECT id, name, price FROM products ORDER BY id DESC LIMIT ? OFFSET ?',
      [limit, offset]
    );
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
function Pagination() {
  const [page, setPage] = useState(1);
  const getPage = (p) => axios.get(`/api/products?page=${p}&limit=5`);
  return <button onClick={() => getPage(page + 1)}>Next Page</button>;
}
```

**Output:**
```json
[
  { "id": 99, "name": "Latest Item", "price": "99.99" },
  { "id": 98, "name": "Older Item", "price": "19.99" }
]
```

## Impact
Using `OFFSET 100000` is notoriously slow in SQL because it physically reads and discards the first 100,000 rows. Apps with infinite scrolling often use "cursor-based pagination" (`WHERE id > lastId LIMIT 10`) for massive performance gains.

## Practice Exercises
- **Easy (SQL)**: Find the single cheapest product. `ORDER BY ... LIMIT 1`.
- **Medium (SQL + Node.js)**: Implement a "Sort By Price (High/Low)" feature via API query. 
- **Hard (Full stack)**: Build a fully working React data table with Pagination & server-side sorting.

## Interview Q&A
1. **Core SQL:** What order is default without `ORDER BY`?
   *No guaranteed order. Never rely on default insertion sequence.*
2. **MERN integration:** Can you pass `ASC`/`DESC` strings into a parameter `?` block?
   *No. Sorting directions/column names cannot be parameterized. Use string interpolation `ORDER BY ${col} ${dir}`. BUT validate carefully against a whitelist to avoid injection.*
3. **SQL vs MongoDB:** Is offset pagination slow in Mongo too?
   *Yes, `skip(10000)` is slow in both DBs. Cursor pagination is universally better for big data.*
4. **Scenario-based:** We want top 10 most expensive shoes.
   *`SELECT * FROM products WHERE category='shoes' ORDER BY price DESC LIMIT 10`.*
5. **Advanced/tricky:** Does multi-column sorting work?
   *Yes, `ORDER BY last_name ASC, first_name ASC` sorts alphabetically by last name, then breaks ties via first name.*

| Previous: [07_Where_Clause_And_Filters.md](./07_Where_Clause_And_Filters.md) | Next: [09_Aggregate_Functions.md](./09_Aggregate_Functions.md) |
