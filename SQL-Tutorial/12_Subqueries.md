# Subqueries

> 📌 **File:** 12_Subqueries.md | **Level:** Beginner → MERN Developer

---

## What is it?
A subquery is a SQL query nested inside another SQL query (using parentheses). The outer query depends on the calculated dynamic output of the inner query.

## MERN Parallel — You Already Know This!
- Await result A `const A = await Model1.find()` then use it `await Model2.find({A.id})`. Subqueries do this entirely on the database side without round-tripping to Node.js.

## Why does it matter?
Sometimes you don't know the `WHERE` value beforehand. (Example: "Find all products priced higher than the average price.") You must compute the average using a subquery before you can filter.

## How does it work?
You write your outer query as normal, but under the `WHERE` or `FROM` or `SELECT` clauses, you wrap a complete inner `(SELECT...)` returning temporary row datasets.

## Visual Diagram
```ascii
Goal: Find all users buying a $100+ product.

SELECT * FROM users WHERE id IN (
   [ Inner Subquery computes Product threshold returns array: (1, 5, 10)]
);

Final Result matched against [1, 5, 10].
```

## Syntax
```sql
-- Fully commented SQL syntax
-- Filtering based on calculated output
SELECT * FROM products 
WHERE price > (SELECT AVG(price) FROM products);

-- Creating a temporary column selection
SELECT name, (SELECT COUNT(id) FROM orders WHERE orders.user_id = users.id) AS count
FROM users;
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
const average = (await Product.aggregate([{ $group: { _id: null, avg: { $avg: '$price' } } }]))[0].avg;
const result = await Product.find({ price: { $gt: average } });

// SQL (One trip to the server)
-- SELECT * FROM products WHERE price > (SELECT AVG(price) FROM products);

// Node.js using mysql2/promise (REQUIRED)
const query = 'SELECT name FROM products WHERE price > (SELECT AVG(price) FROM products)';
const [rows] = await pool.query(query);

// ORM Equivalent (IMPORTANT)
// Prisma mapping varies drastically for nested subqueries. Often RAW SQL is utilized here.
```

### Raw SQL vs ORM
- **Raw SQL:** Simple to wrap in parenthesis. Highly advanced calculation flows are possible.
- **ORM:** ORMs struggle significantly with correlating deep subqueries. Prisma heavily suggests raw parameterized SQL for complex comparative aggregations.

### Real-World Scenario + Full Stack Code
**Scenario:** Returning "Elite" tier items where pricing is higher than the overall store average to populate a specialized React marquee banner.

```sql
-- SQL query
SELECT id, name, price 
FROM products 
WHERE price > (SELECT AVG(price) FROM products);
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.get('/api/products/elite', async (req, res) => {
  try {
    const query = `
      SELECT id, name, price 
      FROM products 
      WHERE price > (SELECT AVG(price) FROM products)
    `;
    const [rows] = await pool.query(query); // no parameters needed for internal math
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
function EliteBanner() {
  const [premium, setPremium] = useState([]);
  useEffect(() => { axios.get('/api/products/elite').then(res => setPremium(res.data))}, []);
  
  return (
    <div className="marquee">
      {premium.map(item => <span key={item.id}>🔥 {item.name}: ${item.price} </span>)}
    </div>
  )
}
```

**Output:**
```json
[
  { "id": 4, "name": "Rolex", "price": "10000.00" }
]
```

## Impact
Using "Correlated Subqueries" (where the inner query depends on the outer query's row value e.g., checking user ID) evaluates the subquery row-by-row like a `for` loop. On millions of rows, it exponentially degrades performance. Usually, `JOIN`s resolve faster.

## Practice Exercises
- **Easy (SQL)**: Find all orders belonging to user Jane using her name as a subquery constraint.
- **Medium (SQL + Node.js)**: Return users whose `id` exists `IN (SELECT user_id FROM orders)`.
- **Hard (Full stack)**: Create an Express endpoint showing departments that have fewer than average active total users.

## Interview Q&A
1. **Core SQL:** When would you use a Subquery vs a JOIN?
   *JOINs combine columns horizontally. Subqueries act internally as isolated step-calculations before returning results vertically.*
2. **MERN integration:** In MERN we fetch ID arrays in Node and pass them to Mongoose `{$in: ids}`. Do we do this in SQL?
   *No! Use `WHERE id IN (SELECT id FROM ...)` inside one DB query to save network trips.*
3. **SQL vs MongoDB:** Which handles nested mathematical data queries better?
   *SQL entirely dominates nested set-based computations mathematically natively.*
4. **Scenario-based:** I want `category_name`, but only categories holding >10 products.
   *Subquery on `WHERE id IN (SELECT category_id FROM prods GROUP BY ID HAVING COUNT > 10)`.*
5. **Advanced/tricky:** Can subqueries return more than 1 column?
   *If it's inside `IN()`, or used as a derived table `FROM (SELECT...) as Temp`, yes. If used under `= (SELECT...)`, NO, it must return precisely 1 row/1 column.*

| Previous: [11_Joins.md](./11_Joins.md) | Next: [13_Views.md](./13_Views.md) |
