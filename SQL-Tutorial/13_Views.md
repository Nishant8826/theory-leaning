# Views

> 📌 **File:** 13_Views.md | **Level:** Beginner → MERN Developer

---

## What is it?
A View is a stored, virtual table mapped directly to the result of a predefined SQL query. It lets you encapsulate complex JOINS and calculations so they behave exactly like a real table.

## MERN Parallel — You Already Know This!
- Mongoose Virtuals (`schema.virtual('fullName').get(...)`) → `CREATE VIEW`
- Mongoose pre-packaged `.aggregate()` wrappers → `VIEW`

## Why does it matter?
Security and repetition. If an analyst team needs access to "Users", but they shouldn't see `password_hashes`, you create a View `SafeUsersTable` stripping bad columns. Also reduces repeating complex `JOIN` code everywhere.

## How does it work?
Run `CREATE VIEW Name AS (SELECT ...)` once. Afterward, you simply run `SELECT * FROM Name;` inside your Express routes.

## Visual Diagram
```ascii
Physical Data:                    VIRTUAL VIEW: 'public_users_view'
Table: Users                      -----------
id | name | password_hash         User ID | User Name
1  | Bob  | $2b$10...      ====>  1       | Bob 
2  | Sue  | $2b$10...             2       | Sue
```

## Syntax
```sql
-- Fully commented SQL syntax
-- 1. Create the persistent view table
CREATE VIEW active_customer_orders AS
SELECT u.name, o.total, o.created_at
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.is_active = 1;

-- 2. Query the view like a normal table forever
SELECT * FROM active_customer_orders;
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
userSchema.virtual('publicProfile').get(function() {
  return { name: this.name, email: this.email }; // computed on server logic
});

// SQL
-- CREATE VIEW public_profile AS SELECT name, email FROM users;

// Node.js using mysql2/promise (REQUIRED)
const [rows] = await pool.query('SELECT * FROM active_customer_orders');

// ORM Equivalent (IMPORTANT)
// Prisma
// Introspect DB, map Views manually to models with `@@map("view_name")` allowing standard findMany.
```

### Raw SQL vs ORM
- **Raw SQL:** Creates and queries Views effortlessly natively on the engine.
- **ORM:** ORMs struggle out-the-box making Views since they don't have explicit Model primary tables; they usually require raw SQL executions or custom DB-level migrations.

### Real-World Scenario + Full Stack Code
**Scenario:** A front-end admin dashboard needing secure revenue reporting. Complex joins are hidden by DB architect; Node just queries a View.

```sql
-- SQL query (Ran ONCE on DB setup)
CREATE VIEW daily_revenue AS
SELECT DATE(created_at) as order_date, SUM(total) as revenue
FROM orders
GROUP BY order_date;

-- Your query
SELECT * FROM daily_revenue LIMIT 7;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.get('/api/reports/revenue', async (req, res) => {
  try {
    // Looks like fetching a basic table, but triggers complex dynamic db calculations
    const [rows] = await pool.query(`
      SELECT order_date, revenue
      FROM daily_revenue 
      ORDER BY order_date DESC LIMIT 7
    `);
    res.json(rows);
  } catch(err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
function RevenueReport() {
  const [rep, setRep] = useState([]);
  useEffect(() => { axios.get('/api/reports/revenue').then(r => setRep(r.data)) }, []);
  return <div>{rep.map(r => <div key={r.order_date}>{r.revenue}</div>)}</div>;
}
```

**Output:**
```json
[
  { "order_date": "2026-04-01", "revenue": "4500.00" }
]
```

## Impact
Views dynamically calculate the underlying payload EVERY time they're called (creating latency for huge calculations) unless they are strictly defined as "Materialized Views" (which cache snapshot results).

## Practice Exercises
- **Easy (SQL)**: Create a View for `discounted_products` where price < 20. Select from it.
- **Medium (SQL + Node.js)**: Send view data using a parameter `WHERE id= ?` against the view.
- **Hard (Full stack)**: Create an admin panel fetching live dashboard charts from a Virtual Database View combining Orders/Products.

## Interview Q&A
1. **Core SQL:** Can you UPDATE data inside a view?
   *Sometimes. "Updatable Views" are allowed only if the view connects directly to a 1:1 table without grouping. Otherwise, they are Read-Only.*
2. **MERN integration:** If Mongoose Virtuals are free, why use DB Views?
   *Speed & Security. Sending unneeded data over Wi-Fi to a Node.js server container wastes processing cycles.*
3. **SQL vs MongoDB:** Can I make a view in Mongo?
   *Yes, MongoDB 3.4+ added Read-Only Views mapped to aggregation pipelines.*
4. **Scenario-based:** Hide salaries from junior devs querying the DB directly.
   *Create `public_employee_view` omitting `salary`. Revoke base table permission, explicitly grant SELECT access to the View only.*
5. **Advanced/tricky:** Difference vs Materialized View?
   *Normal View executes the query query live. Materialized stores the physical row copies on disk for instant reading, requiring background refreshes.*

| Previous: [12_Subqueries.md](./12_Subqueries.md) | Next: [14_Indexes.md](./14_Indexes.md) |
