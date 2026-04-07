# What Is SQL?

> 📌 **File:** `01_What_Is_SQL.md` | **Level:** Beginner → MERN Developer

---

## What is it?

SQL (Structured Query Language) is the standard language used to communicate with relational databases. Just like you use JavaScript to talk to MongoDB through Mongoose methods like `find()`, `insertOne()`, and `updateMany()`, you use SQL statements like `SELECT`, `INSERT`, and `UPDATE` to talk to MySQL.

SQL is NOT a programming language — it's a **query language**. You don't write loops or functions in SQL (well, mostly). You tell the database **what** data you want, and it figures out **how** to get it.

---

## MERN Parallel — You Already Know This!

| Mongoose / MongoDB (You Know)         | SQL / MySQL (You'll Learn)          |
|---------------------------------------|-------------------------------------|
| `db.users.find()`                     | `SELECT * FROM users;`              |
| `db.users.find({ age: 25 })`         | `SELECT * FROM users WHERE age=25;` |
| `db.users.insertOne({ name: 'Ali' })`| `INSERT INTO users (name) VALUES ('Ali');` |
| `db.users.updateOne({...}, {...})`    | `UPDATE users SET name='Ali' WHERE id=1;`  |
| `db.users.deleteOne({ _id: id })`    | `DELETE FROM users WHERE id = 1;`   |
| `db.users.countDocuments()`           | `SELECT COUNT(*) FROM users;`       |
| `db.users.distinct('city')`          | `SELECT DISTINCT city FROM users;`  |
| MongoDB Query Language (MQL)          | SQL (Structured Query Language)     |

### The Core Insight

In MongoDB, you write queries as **JavaScript objects**:
```js
// MongoDB — query is a JS object
db.users.find({ age: { $gte: 18 }, city: 'Delhi' })
```

In SQL, you write queries as **English-like sentences**:
```sql
-- SQL — query is an English sentence
SELECT * FROM users WHERE age >= 18 AND city = 'Delhi';
```

**Same result, different syntax.** That's it.

---

## Why does it matter?

- **SQL is universal** — MySQL, PostgreSQL, SQLite, Oracle, SQL Server all use SQL
- **SQL is 50+ years old** and still the #1 database language
- **Most job postings** require SQL knowledge, even for frontend developers
- **Data analysis, business intelligence, and reporting** all rely on SQL
- Once you learn SQL for MySQL, you can use it with ANY relational database

---

## How does it work?

### SQL Statement Categories

SQL statements are grouped into sublanguages based on what they do:

```
┌──────────────────────────────────────────────────────────────┐
│                     SQL SUBLANGUAGES                         │
├──────────────┬──────────────┬──────────────┬────────────────┤
│     DDL      │     DML      │     DQL      │     DCL        │
│ Data Defn.   │ Data Manip.  │ Data Query   │ Data Control   │
├──────────────┼──────────────┼──────────────┼────────────────┤
│ CREATE       │ INSERT       │ SELECT       │ GRANT          │
│ ALTER        │ UPDATE       │              │ REVOKE         │
│ DROP         │ DELETE       │              │                │
│ TRUNCATE     │              │              │                │
├──────────────┼──────────────┼──────────────┼────────────────┤
│ Mongoose:    │ Mongoose:    │ Mongoose:    │ MongoDB:       │
│ new Schema() │ .save()      │ .find()      │ db.createUser()│
│              │ .updateOne() │ .findOne()   │                │
│              │ .deleteOne() │ .aggregate() │                │
└──────────────┴──────────────┴──────────────┴────────────────┘

TCL (Transaction Control): COMMIT, ROLLBACK, SAVEPOINT
→ MongoDB equivalent: session.startTransaction()
```

### How a SQL Query Executes

```
                     Your SQL Query
                          │
                          ▼
                   ┌──────────────┐
                   │    Parser    │  ← Checks syntax (like JS linter)
                   └──────┬───────┘
                          │
                          ▼
                   ┌──────────────┐
                   │  Optimizer   │  ← Finds the fastest way to get data
                   └──────┬───────┘
                          │
                          ▼
                   ┌──────────────┐
                   │  Executor    │  ← Actually runs the query
                   └──────┬───────┘
                          │
                          ▼
                   ┌──────────────┐
                   │   Result     │  ← Returns rows (like JSON array)
                   └──────────────┘
```

---

## Visual Diagram

### SQL vs MongoDB — Terminology Map

```
┌─────────────────────────────────────────────────────────────┐
│              TERMINOLOGY MAPPING                            │
├─────────────────────────┬───────────────────────────────────┤
│     MongoDB             │           MySQL                   │
├─────────────────────────┼───────────────────────────────────┤
│  Database               │  Database                         │
│  Collection (users)     │  Table (users)                    │
│  Document { ... }       │  Row (record/tuple)               │
│  Field (name, age)      │  Column (name, age)               │
│  _id (ObjectId)         │  PRIMARY KEY (usually `id`)       │
│  Embedded document      │  Related table + JOIN             │
│  $lookup                │  JOIN                             │
│  .find()                │  SELECT                           │
│  .insertOne()           │  INSERT INTO                      │
│  .updateOne()           │  UPDATE ... SET                   │
│  .deleteOne()           │  DELETE FROM                      │
│  .aggregate()           │  GROUP BY                         │
│  Schema validation      │  Column constraints               │
│  No fixed schema        │  Fixed schema (columns + types)   │
└─────────────────────────┴───────────────────────────────────┘
```

### Table Structure (How Data Looks in SQL)

```
MongoDB Document:                    MySQL Table Row:
{                                    ┌────┬───────┬──────┬────────────┐
  _id: ObjectId("abc123"),           │ id │ name  │ age  │ email      │
  name: "Nishant",                   ├────┼───────┼──────┼────────────┤
  age: 24,                           │ 1  │Nishant│  24  │ n@test.com │
  email: "n@test.com"                │ 2  │ Priya │  22  │ p@test.com │
}                                    │ 3  │ Rahul │  28  │ r@test.com │
                                     └────┴───────┴──────┴────────────┘
                                     ↑ Every row has SAME columns
```

---

## Syntax

```sql
-- ============================================
-- SQL statements are case-INSENSITIVE
-- These are all identical:
-- ============================================

SELECT * FROM users;
select * from users;
Select * From Users;

-- Convention: Write SQL keywords in UPPERCASE
-- This is just style — not required

-- ============================================
-- Every statement ends with a semicolon ;
-- ============================================

SELECT NOW();    -- Returns current date/time
SELECT 1 + 1;    -- Returns 2 (SQL can do math!)
SELECT 'Hello';  -- Returns the string 'Hello'

-- ============================================
-- Comments
-- ============================================

-- This is a single-line comment
# This also works in MySQL (but not standard SQL)

/*
   This is a
   multi-line comment
*/
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== MONGODB (Mongoose) ==========
// Get all users
const users = await User.find();

// Get users older than 18
const adults = await User.find({ age: { $gte: 18 } });

// Get one user by ID
const user = await User.findById('abc123');

// Count all users
const count = await User.countDocuments();
```

```sql
-- ========== MySQL (SQL) ==========
-- Get all users
SELECT * FROM users;

-- Get users older than 18
SELECT * FROM users WHERE age >= 18;

-- Get one user by ID
SELECT * FROM users WHERE id = 1;

-- Count all users
SELECT COUNT(*) FROM users;
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Get all users
const [users] = await pool.query('SELECT * FROM users');

// Get users older than 18
const [adults] = await pool.query('SELECT * FROM users WHERE age >= ?', [18]);

// Get one user by ID
const [rows] = await pool.query('SELECT * FROM users WHERE id = ?', [1]);
const user = rows[0];  // First row (like findOne)

// Count all users
const [result] = await pool.query('SELECT COUNT(*) AS total FROM users');
const count = result[0].total;
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize (like Mongoose) ==========
const { User } = require('./models');

// Get all users — generates: SELECT * FROM users;
const users = await User.findAll();

// Get users older than 18 — generates: SELECT * FROM users WHERE age >= 18;
const adults = await User.findAll({ where: { age: { [Op.gte]: 18 } } });

// Get one user by ID — generates: SELECT * FROM users WHERE id = 1;
const user = await User.findByPk(1);

// Count all users — generates: SELECT COUNT(*) AS count FROM users;
const count = await User.count();
```

**Notice how Sequelize syntax looks almost identical to Mongoose?** That's intentional — ORMs abstract away the database differences.

---

## Real-World Scenario + Full Stack Code

### Scenario: Display all products on an e-commerce homepage

```sql
-- SQL Query: Get all products with their category names
SELECT p.id, p.name, p.price, c.name AS category
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.price > 0
ORDER BY p.created_at DESC
LIMIT 20;
```

```js
// Node.js + Express using mysql2 (parameterized)
app.get('/api/products', async (req, res) => {
  try {
    const [products] = await pool.query(`
      SELECT p.id, p.name, p.price, c.name AS category
      FROM products p
      JOIN categories c ON p.category_id = c.id
      WHERE p.price > 0
      ORDER BY p.created_at DESC
      LIMIT 20
    `);
    
    res.json({ count: products.length, products });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// ORM version (Sequelize)
app.get('/api/products', async (req, res) => {
  const products = await Product.findAll({
    include: [{ model: Category, attributes: ['name'] }],
    where: { price: { [Op.gt]: 0 } },
    order: [['createdAt', 'DESC']],
    limit: 20
  });
  
  res.json({ count: products.length, products });
});
```

```js
// React Component using Axios
import { useState, useEffect } from 'react';
import axios from 'axios';

function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchProducts() {
      try {
        const { data } = await axios.get('/api/products');
        setProducts(data.products);
      } catch (error) {
        console.error('Failed to fetch products:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchProducts();
  }, []);

  if (loading) return <p>Loading products...</p>;

  return (
    <div className="product-grid">
      {products.map(product => (
        <div key={product.id} className="product-card">
          <h3>{product.name}</h3>
          <p>₹{product.price}</p>
          <span>{product.category}</span>
        </div>
      ))}
    </div>
  );
}
```

**Output:**
```json
{
  "count": 3,
  "products": [
    { "id": 1, "name": "iPhone 15", "price": 79999, "category": "Electronics" },
    { "id": 2, "name": "Nike Air Max", "price": 12999, "category": "Footwear" },
    { "id": 3, "name": "The Alchemist", "price": 299, "category": "Books" }
  ]
}
```

---

## Impact

| If You Don't Understand SQL...          | What Happens                                    |
|-----------------------------------------|-------------------------------------------------|
| Write queries without understanding     | ORM generates slow/wrong queries in production  |
| Don't know SQL sublanguages             | Accidentally DROP a table thinking it's DELETE   |
| Ignore SQL syntax rules                 | Spend hours debugging missing semicolons         |
| Think MongoDB knowledge is enough       | Fail SQL-heavy interviews at 80% of companies   |

---

## Practice Exercises

### Easy (SQL Only)
1. Write a SQL statement that returns today's date
2. Write a SQL statement that adds two numbers: 100 + 200
3. Write a comment in SQL (both single-line and multi-line)

### Medium (SQL + Node.js)
4. Write a Node.js route that runs `SELECT VERSION()` and returns the result as JSON
5. Translate this Mongoose query to raw SQL: `User.find({ city: 'Mumbai' }).select('name email')`
6. Write the SQL equivalent of `db.products.find().sort({ price: -1 }).limit(5)`

### Hard (Full Stack)
7. Create a React + Express app that:
   - Has a text input where users can type a SQL query
   - Sends the query to Express backend
   - Displays the result in a table format
   - (⚠️ This is for learning only — NEVER allow arbitrary SQL in production!)
8. Compare the same query in MongoDB, raw SQL, and Sequelize — note the output format differences

---

## Real-World Q&A

**Q1:** If SQL and MongoDB both store data, why do most companies prefer SQL?
**A:** SQL databases enforce data integrity through schemas, constraints, and relationships. When you're dealing with financial data, user accounts, or inventory — you CANNOT afford inconsistent data. MongoDB is great for flexibility, but SQL guarantees that every row follows the rules.

**Q2:** Can I use SQL and MongoDB together in one app?
**A:** Absolutely! Many apps use both. For example: MySQL for user accounts and transactions (needs strict consistency), MongoDB for chat messages and logs (needs flexibility and speed). This is called **polyglot persistence**.

**Q3:** Is SQL harder than MongoDB queries?
**A:** Different, not harder. SQL is actually more readable — it reads like English: `SELECT name FROM users WHERE age > 18 ORDER BY name`. MongoDB's JSON-based queries can be harder to read for complex operations like JOINs (which require `$lookup` in MongoDB but are native in SQL).

---

## Interview Q&A

**Q1: What is SQL?**
SQL stands for Structured Query Language. It's the standard language for managing and querying relational databases. It allows you to create, read, update, and delete data (CRUD), define database schemas, control access, and manage transactions.

**Q2: What are the different types of SQL commands?**
DDL (Data Definition Language): CREATE, ALTER, DROP — defines structure. DML (Data Manipulation Language): INSERT, UPDATE, DELETE — modifies data. DQL (Data Query Language): SELECT — reads data. DCL (Data Control Language): GRANT, REVOKE — manages permissions. TCL (Transaction Control Language): COMMIT, ROLLBACK — manages transactions.

**Q3: What is the difference between SQL and MySQL?**
SQL is a language (like JavaScript). MySQL is a database management system that uses SQL (like Node.js runs JavaScript). Other DBMS that use SQL include PostgreSQL, Oracle, SQL Server, and SQLite. Each has slight syntax differences but the core SQL is the same.

**Q4: How is querying data different in SQL vs MongoDB?**
SQL uses declarative text-based queries: `SELECT * FROM users WHERE age > 18`. MongoDB uses method chaining with JSON objects: `db.users.find({ age: { $gt: 18 } })`. SQL has powerful built-in JOINs for combining tables; MongoDB uses `$lookup` (aggregate pipeline) or application-level joins via `populate()` in Mongoose.

**Q5: If you have an existing MERN app and need to migrate from MongoDB to MySQL, what are the key challenges?**
Schema design: MongoDB's nested documents must be normalized into separate tables. Relationships: Embedded arrays become junction/join tables. Queries: All Mongoose queries must be rewritten as SQL. Data migration: Documents must be transformed into flat rows. Transactions: MongoDB's multi-document transactions work differently than SQL transactions. ORMs like Sequelize can ease the transition by providing a Mongoose-like API.

---

| [← Previous: Introduction & Setup](./00_Introduction_And_Setup.md) | [Next: Databases & Tables →](./02_Databases_And_Tables.md) |
|---|---|
