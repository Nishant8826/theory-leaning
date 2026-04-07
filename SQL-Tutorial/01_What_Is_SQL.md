# What Is SQL

> 📌 **File:** 01_What_Is_SQL.md | **Level:** Beginner → MERN Developer

---

## What is it?
SQL (Structured Query Language) is the standard language to communicate with relational databases. It reads, writes, and manipulates strongly-structured tabular data.

## MERN Parallel — You Already Know This!
- MongoDB JSON queries → SQL standard syntax
- MongoDB Driver (BSON) → SQL Text Queries
- unstructured → Highly structured / strict schema
- `db.collection.find({age: 20})` → `SELECT * FROM table WHERE age = 20;`

## Why does it matter?
SQL powers the majority of mature enterprise systems, financial tech, and large-scale applications where data relationships are complex and need strict integrity. 

## How does it work?
Unlike NoSQL where you pass JSON objects to functions to retrieve data, in SQL you write raw string commands (like telling the DB exactly what to do using English-like syntax).

## Visual Diagram
```ascii
[JSON based MERN]               [SQL based MERN]
JS Object                         SQL String
{ "name": "John" }      ->        "SELECT * FROM users WHERE name='John';"
      |                                  |
   Mongo DB                           MySQL DB
```

## Syntax
```sql
-- Fully commented SQL syntax
SELECT * FROM table_name; -- The universal "find all" command
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
const users = await User.find({});

// SQL
-- SELECT * FROM users;

// Node.js using mysql2/promise (REQUIRED)
const [rows] = await pool.query('SELECT * FROM users');

// ORM Equivalent (IMPORTANT)
// Sequelize
const users = await User.findAll();
```

### Raw SQL vs ORM
- **Raw SQL:** Teaches you the actual underlying language. Better for debugging and complex reports.
- **ORM:** Abstracts SQL strings to JS functions (like Mongoose), making simple CRUD faster but hiding database mechanics.

### Real-World Scenario + Full Stack Code
**Scenario:** Returning an introductory test payload to the React frontend.

```sql
-- SQL query
SELECT 'Hello World' AS message;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.get('/api/hello', async (req, res) => {
  const [rows] = await pool.query('SELECT ? AS message', ['Hello World']);
  res.json(rows[0]);
});

// ORM version (Sequelize/Prisma)
app.get('/api/hello', async (req, res) => {
  const obj = await Model.findOne(); // Overkill for a simple string
  res.json(obj);
});

// React component using Axios
useEffect(() => {
  axios.get('/api/hello').then(res => console.log(res.data.message));
}, []);
```

**Output:**
```json
{
  "message": "Hello World"
}
```

## Impact
If you don't understand basic SQL, debugging slow ORM queries in production is impossible. ORMs can sometimes generate incredibly inefficient SQL.

## Practice Exercises
- **Easy (SQL)**: Write a query selecting the number `100` as `score`.
- **Medium (SQL + Node.js)**: Send a `SELECT 'SQL is cool'` query via Node and return it.
- **Hard (Full stack)**: Create a React button that requests a random number generated purely by MySQL `SELECT RAND()`.

## Interview Q&A
1. **Core SQL:** What does SQL stand for?
   *Structured Query Language.*
2. **MERN integration:** Do we pass JSON to `mysql2` to find records?
   *No, we pass strings of SQL statements mixed with parameterized values.*
3. **SQL vs MongoDB:** Which is more flexible?
   *MongoDB (schema-less), but SQL provides rigid data safety.*
4. **Scenario-based:** You want a quick script to update 1,000,000 rows. Use ORM or raw SQL?
   *Raw SQL. ORMs will instantiate 1,000,000 JS objects, destroying Node's memory heap.*
5. **Advanced/tricky:** Is SQL declarative or imperative?
   *Declarative. You tell it WHAT you want (`SELECT`), not HOW to get it (it figures out the tree traversal).*

| Previous: [00_Introduction_And_Setup.md](./00_Introduction_And_Setup.md) | Next: [02_Databases_And_Tables.md](./02_Databases_And_Tables.md) |
