# Select Basics

> 📌 **File:** 06_Select_Basics.md | **Level:** Beginner → MERN Developer

---

## What is it?
`SELECT` reads data from tables. It is analogous to fetching.

## MERN Parallel — You Already Know This!
- `Model.find()` → `SELECT * FROM table`
- `Model.find().select('name price')` → `SELECT name, price FROM table`
- Projection → Explicit SELECT columns

## Why does it matter?
`SELECT` accounts for ~80% of database interactions in modern web apps. Fetching only what you need improves app performance drastically.

## How does it work?
You specify columns to retrieve, then `FROM` which table. `*` fetches everything.

## Visual Diagram
```ascii
Database Table
id | name | price
1  | shoe | 10
2  | hat  | 5

SELECT name FROM table --> Returns purely
name
----
shoe
hat
```

## Syntax
```sql
-- Fully commented SQL syntax
SELECT * FROM products; -- Fetch ALL columns
SELECT name, price FROM products; -- Fetch ONLY specific columns (Projection)
SELECT price AS cost FROM products; -- Aliasing (Renaming keys in JS response)
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
const getProds = await Product.find({}, 'name price');

// SQL
-- SELECT name, price FROM products;

// Node.js using mysql2/promise (REQUIRED)
const [rows] = await pool.query('SELECT name, price FROM products');

// ORM Equivalent (IMPORTANT)
// Prisma
await prisma.product.findMany({ select: { name: true, price: true } });
```

### Raw SQL vs ORM
- **Raw SQL:** Provides incredibly precise control over what fields come over the network.
- **ORM:** Tends to do `SELECT *` under the hood if not explicitly configured, bloating memory.

### Real-World Scenario + Full Stack Code
**Scenario:** Building an online store catalog to display products to users, returning minimal data.

```sql
-- SQL query
SELECT id, name, price FROM products;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.get('/api/catalog', async (req, res) => {
  try {
    // Only fetching id, name, price (ignoring heavy stuff like descriptions/blobs)
    const [rows] = await pool.query('SELECT id, name, price FROM products');
    res.json(rows); // sends array of objects
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// React component using Axios
function Catalog() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    axios.get('/api/catalog').then(res => setItems(res.data));
  }, []);
  
  return (
    <ul>
      {items.map(i => <li key={i.id}>{i.name} - ${i.price}</li>)}
    </ul>
  );
}
```

**Output:**
```json
[
  { "id": 1, "name": "Shoe", "price": "10.00" },
  { "id": 2, "name": "Hat", "price": "5.00" }
]
```

## Impact
Using `SELECT *` on massive tables containing long `TEXT` or `BLOB` columns will consume massive Node.js RAM and crush network bandwidth between the backend and DB. Always specify needed fields.

## Practice Exercises
- **Easy (SQL)**: Select ONLY the emails from the `customers` table.
- **Medium (SQL + Node.js)**: Send a response formatting a product price using Alias (`SELECT price AS usdCost`).
- **Hard (Full stack)**: Create an API that grabs everything from products EXCEPT the stock count, and display it in a React grid.

## Interview Q&A
1. **Core SQL:** Why is `SELECT *` considered bad practice in production?
   *It wastes bandwidth, slows DB reads, and can introduce app errors if schema columns change unexpectedly.*
2. **MERN integration:** What data structure does `SELECT` return in Node.js?
   *An Array of Objects. `[{col1: val1, col2: val2}]`.*
3. **SQL vs MongoDB:** How is aliasing done in Mongo vs SQL?
   *SQL uses the `AS` keyword securely on DB level. MongoDB handles via aggregations or JS manipulation.*
4. **Scenario-based:** Table has 5 million rows, doing `SELECT *` blows up Node heap memory. Why?
   *Node loads the entire massive array into JS memory before resolving. (Must use limits or streams).*
5. **Advanced/tricky:** Can I select fields that don't exist in the table?
   *Yes, constants. `SELECT 1 AS flag, name FROM products`.*

| Previous: [05_Insert_Update_Delete.md](./05_Insert_Update_Delete.md) | Next: [07_Where_Clause_And_Filters.md](./07_Where_Clause_And_Filters.md) |
