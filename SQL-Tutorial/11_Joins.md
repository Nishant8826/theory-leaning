# Joins

> 📌 **File:** 11_Joins.md | **Level:** Beginner → MERN Developer

---

## What is it?
A `JOIN` merges columns from entirely different tables based on matching overlapping keys (usually Primary/Foreign Keys).

## MERN Parallel — You Already Know This!
- Mongoose `.populate('user')` → `LEFT JOIN`
- MongoDB pipeline `$lookup` → `LEFT JOIN`
- Foreign Key (`user_id`) → Mongoose explicit `Schema.Types.ObjectId` ref.
- Array of Subdocuments → Normalized `1-to-Many` Table Joins.

## Why does it matter?
Unlike Mongo, where you can stuff huge arrays into JSON fields, in SQL you break everything apart for strict integrity (Normalization). `JOIN` is the mechanism that stitches your database back together upon query.

## How does it work?
You tell SQL the tables involved, and use `ON` to specify which column equals which column. (e.g. `users.id = orders.user_id`).

## Visual Diagram
```ascii
Users Table       Orders Table
id | name         id | user_id | item
1  | Bob          99 | 1       | Pen

JOIN ON users.id = orders.user_id

Combined Result:
name | item
Bob  | Pen
```

## Syntax
```sql
-- Fully commented SQL syntax
-- INNER JOIN guarantees both row sides must exist.
SELECT orders.id, users.name 
FROM orders
INNER JOIN users ON orders.user_id = users.id;

-- LEFT JOIN keeps left table rows even if the right table is NULL.
SELECT users.name, orders.id
FROM users
LEFT JOIN orders ON users.id = orders.user_id;
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
const order = await Order.findById(1).populate('userId', 'name');

// SQL
-- SELECT orders.id, users.name FROM orders 
-- JOIN users ON orders.user_id = users.id WHERE orders.id = 1;

// Node.js using mysql2/promise (REQUIRED)
const query = `
  SELECT o.id, u.name 
  FROM orders o 
  JOIN users u ON o.user_id = u.id 
  WHERE o.id = ?
`;
const [rows] = await pool.query(query, [1]);

// ORM Equivalent (IMPORTANT)
// Prisma
await prisma.order.findUnique({ where: { id: 1 }, include: { user: true } });
```

### Raw SQL vs ORM
- **Raw SQL:** Creates flat response rows (if a user has 5 orders, user data is duplicated 5 times). You manually reshape data into tree objects if needed.
- **ORM:** Behind the scenes, ORMs run massive joins and seamlessly shape the returned result into nested JS Objects mimicking Mongoose `populate()`.

### Real-World Scenario + Full Stack Code
**Scenario:** User profile page that displays their info along with their recent order history.

```sql
-- SQL query
SELECT 
  u.id AS user_id, u.name, 
  o.id AS order_id, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.id = ?;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.get('/api/users/:id/orders', async (req, res) => {
  const query = `
    SELECT u.name, u.email, o.id as orderId, o.total 
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.id = ?
  `;
  try {
    const [rows] = await pool.query(query, [req.params.id]);
    
    // Manually format raw flat SQL rows into nested JSON (similar to Mongoose output)
    if (rows.length === 0) return res.status(404).send('Not Found');
    const response = {
      name: rows[0].name,
      email: rows[0].email,
      orders: rows.map(r => ({ id: r.orderId, total: r.total })).filter(o => o.id) // keep valid
    };
    res.json(response);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
function ProfileOrders({ userId }) {
  const [data, setData] = useState(null);
  useEffect(() => { axios.get(`/api/users/${userId}/orders`).then(res => setData(res.data)) }, [userId]);
  if(!data) return <div>Loading...</div>;
  return <div>{data.name} has {data.orders.length} orders.</div>;
}
```

**Output:**
```json
{
  "name": "Jane",
  "email": "jane@me.com",
  "orders": [
    { "id": 105, "total": "55.00" },
    { "id": 106, "total": "12.50" }
  ]
}
```

## Impact
Heavy JOINS without indexing your foreign keys will trigger massive full-table cross-scans driving millions of calculations recursively causing complete database lockups.

## Practice Exercises
- **Easy (SQL)**: Write a basic JOIN querying what category ID 1 name is.
- **Medium (SQL + Node.js)**: Send a flattened response containing Order IDs alongside product names using `INNER JOIN`.
- **Hard (Full stack)**: Create an API returning nested React data displaying Authors and their embedded array of Book objects mapped manually from raw flat SQL output.

## Interview Q&A
1. **Core SQL:** Diff between INNER and LEFT JOIN?
   *INNER keeps only matches. LEFT keeps everything on left table, injecting NULLs if right side has no match.*
2. **MERN integration:** How does SQL JOIN output differ from Mongoose populate?
   *Mongoose `.populate()` builds a tree structure `[ { user: {..} } ]`. SQL JOIN returns flat rows spanning columns `[ { user_id, user_name, ... } ]`.*
3. **SQL vs MongoDB:** Can I just put arrays in a SQL column?
   *You can put comma-separated IDs via strings or JSON, but that completely defeats Relational Database indexing performance. Use explicit joins.*
4. **Scenario-based:** I want a list of all products, and IF they are out of stock, list their backorder date.
   *Use a `LEFT JOIN` starting with Products, linking to backorder stock table.*
5. **Advanced/tricky:** What is an N+1 Query problem?
   *Running 1 query for Users, looping the result in Node, and firing an individual db query per user to get orders. Anti-pattern. Solve via 1 JOIN query.*

| Previous: [10_Group_By_And_Having.md](./10_Group_By_And_Having.md) | Next: [12_Subqueries.md](./12_Subqueries.md) |
