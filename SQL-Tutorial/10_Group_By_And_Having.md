# Group By and Having

> 📌 **File:** 10_Group_By_And_Having.md | **Level:** Beginner → MERN Developer

---

## What is it?
`GROUP BY` splits data into categories before running aggregate mathematical functions on them. `HAVING` filters the results but applies *after* `GROUP BY` executes, unlike `WHERE`.

## MERN Parallel — You Already Know This!
- Aggregate pipeline `$group: { _id: "$category" }` → `GROUP BY category`
- Pipeline `$match` after `$group` → `HAVING`
- Pipeline `$match` before `$group` → `WHERE`

## Why does it matter?
Crucial for generating detailed aggregated charts. Example: Fetching total sales per category, active vs inactive user totals, or finding duplicate records.

## How does it work?
In `SELECT`, define the grouping column AND an aggregate function. Run `GROUP BY grouping_column`. Use `HAVING` to filter out any aggregated results that don't match conditions.

## Visual Diagram
```ascii
Table Items
Category | Price
Shoes    | 10
Shoes    | 20
Hats     | 5

SELECT Category, SUM(Price) FROM items GROUP BY Category;

Grouped Results:
Category | SUM(Price)
Shoes    | 30
Hats     | 5
```

## Syntax
```sql
-- Fully commented SQL syntax
-- 1. Select the grouped column AND the aggregated math
SELECT category, COUNT(id) AS total_items 
FROM products 
GROUP BY category; -- 2. Dictate the splitting rule

-- 3. Use HAVING to filter groups AFTER the math runs
SELECT category, SUM(price) AS value
FROM products
GROUP BY category
HAVING value > 1000;
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
await Product.aggregate([
  { $group: { _id: "$category", count: { $sum: 1 } } },
  { $match: { count: { $gt: 5 } } }
]);

// SQL
-- SELECT category, COUNT(*) AS count FROM products 
-- GROUP BY category HAVING count > 5;

// Node.js using mysql2/promise (REQUIRED)
const [rows] = await pool.query('SELECT category, COUNT(*) AS c FROM products GROUP BY category');

// ORM Equivalent (IMPORTANT)
// Sequelize
await Product.findAll({
  attributes: ['category', [sequelize.fn('COUNT', 'id'), 'c']],
  group: 'category'
});
```

### Raw SQL vs ORM
- **Raw SQL:** Simple mapping using standard `GROUP BY` keywords makes statistical queries significantly easier to construct than ORM.
- **ORM:** Doing multi-field GROUP BY requires passing complex, database-specific query generation strings back into the Javascript ORM.

### Real-World Scenario + Full Stack Code
**Scenario:** A front-end Pie Chart needs to know total revenue grouped by category.

```sql
-- SQL query
SELECT category, SUM(price) AS segment_revenue FROM products GROUP BY category;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.get('/api/charts/category-revenue', async (req, res) => {
  try {
    const [rows] = await pool.query(`
      SELECT category, SUM(price) AS revenue 
      FROM products 
      GROUP BY category
    `);
    res.json(rows); 
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
function RevenueChart() {
  const [data, setData] = useState([]);
  useEffect(() => {
    axios.get('/api/charts/category-revenue').then(res => setData(res.data));
  }, []);
  
  return (
    <ul>
      {data.map(d => <li key={d.category}>{d.category}: ${d.revenue}</li>)}
    </ul>
  );
}
```

**Output:**
```json
[
  { "category": "Electronics", "revenue": "15000.00" },
  { "category": "Apparel", "revenue": "1200.00" }
]
```

## Impact
Using `WHERE` instead of `HAVING` for a `SUM()` value throws a syntax error crashing your API, as `WHERE` evaluates lines before group math is computed.

## Practice Exercises
- **Easy (SQL)**: Group customers by city and show `COUNT(id)`. 
- **Medium (SQL + Node.js)**: Send JSON indicating total salaries grouped by company department.
- **Hard (Full stack)**: Build a bar chart interface. Fetch groups via API, and only render categories with `HAVING total > 10`.

## Interview Q&A
1. **Core SQL:** What's the main difference between `WHERE` and `HAVING`?
   *`WHERE` filters individual rows BEFORE they are grouped. `HAVING` filters aggregated values AFTER they are grouped.*
2. **MERN integration:** Can you group by multiple columns?
   *Yes. `GROUP BY month, category` makes distinct bucket pairs.*
3. **SQL vs MongoDB:** Which grouping logic is easier?
   *SQL reads linearly (`SELECT > FROM > WHERE > GROUP BY`). Mongo pipeline ordering dictates the data processing sequentially.*
4. **Scenario-based:** I want `category` and `name`, but I want to group by `category`. What happens?
   *Error. Explicit `ONLY_FULL_GROUP_BY` SQL laws prohibit mixing ungrouped and unaggregated columns.*
5. **Advanced/tricky:** Can I use `WHERE` and `HAVING` in the same query?
   *Yes. `WHERE is_active=1 GROUP BY department HAVING SUM(salary) > 100`.*

| Previous: [09_Aggregate_Functions.md](./09_Aggregate_Functions.md) | Next: [11_Joins.md](./11_Joins.md) |
