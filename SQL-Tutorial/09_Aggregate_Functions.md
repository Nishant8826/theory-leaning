# Aggregate Functions

> 📌 **File:** 09_Aggregate_Functions.md | **Level:** Beginner → MERN Developer

---

## What is it?
Aggregate functions perform a calculation on a set of values in a column, squashing them down into a single returned row result (like calculating a sum or fetching the total count).

## MERN Parallel — You Already Know This!
- `Model.countDocuments()` → `COUNT(*)`
- MongoDB Aggregation `$sum` → `SUM(column)`
- MongoDB Aggregation `$avg` → `AVG(column)`
- `$max` / `$min` → `MAX(column)` / `MIN(column)`

## Why does it matter?
Essential for analytics dashboards. Displaying "Total Revenue", "Active Users", "Average Rating". You don't want Node.js doing that math using `reduce()`. Let the fast Database hardware engine do it.

## How does it work?
Wrap the target column name inside the function keywords `COUNT(), SUM(), AVG(), MIN(), MAX()` within the `SELECT` clause.

## Visual Diagram
```ascii
Rows:
price
-----
10
20
30

SELECT SUM(price) FROM products;  --> Returns single row: 60
SELECT AVG(price) FROM products;  --> Returns single row: 20
```

## Syntax
```sql
-- Fully commented SQL syntax
SELECT COUNT(id) FROM users;           -- Number of users
SELECT SUM(price) FROM order_items;    -- Total gross revenue
SELECT MIN(price), MAX(price) FROM products; -- Cheapest and Most Expensive
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
const count = await User.countDocuments();
const res = await Order.aggregate([{ $group: { _id: null, total: { $sum: "$amount" } } }]);

// SQL
-- SELECT COUNT(*) AS total_users FROM users;
-- SELECT SUM(amount) AS total FROM orders;

// Node.js using mysql2/promise (REQUIRED)
const [rows] = await pool.query('SELECT SUM(price) AS revenue FROM order_items');

// ORM Equivalent (IMPORTANT)
// Sequelize
const total = await OrderItem.sum('price');
```

### Raw SQL vs ORM
- **Raw SQL:** Simple `SUM(y)` beats complex array brackets syntax of Mongo/ORM aggregates heavily in readability.
- **ORM:** ORMs provide basic `count()` out of the box, but complex combined aggregates often force developers back entirely into executing raw queries.

### Real-World Scenario + Full Stack Code
**Scenario:** Admin dashboard fetching total active users and their average wallet balance.

```sql
-- SQL query
SELECT COUNT(id) AS active_users, AVG(wallet_balance) AS avg_bal
FROM users WHERE is_active = 1;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.get('/api/admin/metrics', async (req, res) => {
  try {
    const [rows] = await pool.query(`
      SELECT 
        COUNT(id) AS totalUsers, 
        AVG(wallet) AS avgBalance 
      FROM users 
      WHERE is_active = ?
    `, [1]);
    
    // Rows always returns an array, even if query guarantees 1 aggregated row
    res.json(rows[0]); 
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
function Dashboard() {
  const [metrics, setMetrics] = useState({ totalUsers: 0, avgBalance: 0 });
  useEffect(() => {
    axios.get('/api/admin/metrics').then(res => setMetrics(res.data));
  }, []);
  
  return <div>Active Users: {metrics.totalUsers} Average Funds: ${metrics.avgBalance}</div>
}
```

**Output:**
```json
{
  "totalUsers": 140,
  "avgBalance": "50.450"
}
```

## Impact
Pulling 10,000 array objects into your Node.js server and using `array.reduce((a, b) => a + b)` will block the asynchronous Node Event Loop. It freezes your entire API for all users. SQL `SUM()` executes directly on the database machine's C++ core highly efficiently. 

## Practice Exercises
- **Easy (SQL)**: Find the sheer number of users using `COUNT(*)`.
- **Medium (SQL + Node.js)**: Send total money generated (`SUM(price)`) from all orders belonging to user ID 5.
- **Hard (Full stack)**: Build a cart summary that shows the minimum price item, the max price item, and total cost of the user's cart items.

## Interview Q&A
1. **Core SQL:** What does `COUNT(*)` vs `COUNT(column)` do?
   *`COUNT(*)` counts total rows. `COUNT(column)` counts rows ignoring NULLs in that column.*
2. **MERN integration:** Aggregate returns `[ { "revenue": "100.50" } ]`. Why format is string?
   *`mysql2` returns DECIMAL types as strings to prevent native JS `FLOAT` precision loss.*
3. **SQL vs MongoDB:** Which is faster for sums?
   *SQL is highly optimized row-wise mathematics.*
4. **Scenario-based:** We need the total amount ignoring refunded statuses. 
   *`SELECT SUM(amount) FROM orders WHERE status != 'refunded'`.*
5. **Advanced/tricky:** Can I select non-aggregated columns next to aggregates? `SELECT name, SUM(price)`
   *Without grouping (see next chapter), this returns invalid or unpredictable results in SQL strict mode.*

| Previous: [08_Sorting_And_Limiting.md](./08_Sorting_And_Limiting.md) | Next: [10_Group_By_And_Having.md](./10_Group_By_And_Having.md) |
