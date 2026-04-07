# Where Clause And Filters

> 📌 **File:** 07_Where_Clause_And_Filters.md | **Level:** Beginner → MERN Developer

---

## What is it?
The `WHERE` clause filters data based on specific conditions, ensuring you only retrieve (or modify) the specific rows you want.

## MERN Parallel — You Already Know This!
- `Model.find({ category: 'shoes' })` → `WHERE category = 'shoes'`
- `{ price: { $gt: 50 } }` → `WHERE price > 50`
- `{ $or: [ ... ] }` → `WHERE cond1 OR cond2`
- `{ name: /regex/i }` → `WHERE name LIKE '%text%'`

## Why does it matter?
Querying without `WHERE` gets massive payloads. For any search bar, category filter, or user authentication system, `WHERE` is strictly required.

## How does it work?
Append `WHERE` followed by logical expressions (`=`, `>`, `<`, `AND`, `OR`, `LIKE`, `IN()`) to filter out falsy rows.

## Visual Diagram
```ascii
Rows
id | category | price
1  | Shoes    | 120
2  | Hats     | 30
3  | Shoes    | 40

SELECT id FROM table WHERE category='Shoes' AND price > 100;
Result: id 1 gets returned.
```

## Syntax
```sql
-- Fully commented SQL syntax
SELECT * FROM products WHERE id = 5;
SELECT * FROM products WHERE price > 100 AND category = 'electronics';
SELECT * FROM products WHERE category IN ('shoes', 'hats');
SELECT * FROM products WHERE name LIKE '%nike%'; -- Contains "nike" anywhere
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
const items = await Product.find({ 
  price: { $gt: 100 }, 
  name: /nike/i 
});

// SQL
-- SELECT * FROM products WHERE price > 100 AND name LIKE '%nike%';

// Node.js using mysql2/promise (REQUIRED)
const [rows] = await pool.query(
  'SELECT * FROM products WHERE price > ? AND name LIKE ?',
  [100, '%nike%']
);

// ORM Equivalent (IMPORTANT)
// Prisma
await prisma.product.findMany({ 
  where: { price: { gt: 100 }, name: { contains: 'nike' } } 
});
```

### Raw SQL vs ORM
- **Raw SQL:** Complex chained `AND`/`OR` conditions are easier to read sequentially in SQL than deeply-nested JS objects.
- **ORM:** Generates the WHERE logic dynamically based on JS objects securely.

### Real-World Scenario + Full Stack Code
**Scenario:** E-commerce product search endpoint with text filter and price floor.

```sql
-- SQL query
SELECT * FROM products WHERE price >= ? AND name LIKE ?;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.get('/api/search', async (req, res) => {
  const { minPrice, q } = req.query;
  
  // Format the LIKE wildcard variable cleanly
  const searchQuery = `%${q}%`; 

  try {
    const [rows] = await pool.query(
      'SELECT id, name, price FROM products WHERE price >= ? AND name LIKE ?',
      [minPrice || 0, searchQuery]
    );
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
function SearchBar() {
  const handleSearch = () => {
    axios.get('/api/search?q=shirt&minPrice=20').then(res => console.log(res.data));
  };
  return <button onClick={handleSearch}>Search</button>;
}
```

**Output:**
```json
[
  { "id": 15, "name": "Red T-Shirt", "price": "25.00" }
]
```

## Impact
Using `LIKE '%term%'` forces MySQL to scan the entire table ignoring indexes, leading to catastrophic slowdowns on big tables. Use full-text search indexes for major text fields. ALWAYS use prepared statement `?` for user variables in `WHERE` to prevent injected bypassing (e.g. `1=1`).

## Practice Exercises
- **Easy (SQL)**: Find all users where `isActive = 1`.
- **Medium (SQL + Node.js)**: Create a login route translating `WHERE email = ? AND password = ?`. 
- **Hard (Full stack)**: Create a multi-filter side-panel matching SQL conditions (Min Price, Max Price, Category list).

## Interview Q&A
1. **Core SQL:** How do you test for NULL in SQL?
   *You must use `IS NULL` or `IS NOT NULL`, regular `=` operator fails for NULL values.*
2. **MERN integration:** Are MongoDB ranges `$in`/`$nin` equivalent to SQL `IN`?
   *Yes, `WHERE id IN (1, 2, 3)`.*
3. **SQL vs MongoDB:** Is `LIKE` case sensitive?
   *Usually not in MySQL (depends on collation). In MongoDB regex is needed for case-insensitivity.*
4. **Scenario-based:** User wants search results strictly starting with 'A'.
   *Use `WHERE name LIKE 'A%'`.*
5. **Advanced/tricky:** Difference between `WHERE` and `HAVING`?
   *`WHERE` filters rows BEFORE aggregation. `HAVING` filters grouped rows AFTER aggregation.*

| Previous: [06_Select_Basics.md](./06_Select_Basics.md) | Next: [08_Sorting_And_Limiting.md](./08_Sorting_And_Limiting.md) |
