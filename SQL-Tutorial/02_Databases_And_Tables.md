# Databases and Tables

> 📌 **File:** 02_Databases_And_Tables.md | **Level:** Beginner → MERN Developer

---

## What is it?
In SQL, a database is a container for tables. Tables are rigorous grids (rows and columns) that strictly hold data of predefined types.

## MERN Parallel — You Already Know This!
- database → database
- collection → table (e.g. `products`)
- Mongoose Schema Definition → Table Creation (`CREATE TABLE`)
- document → row
- fields → columns

## Why does it matter?
Properly structuring tables prevents bad data from ever entering your database. If Mongoose misses validation, bad JSON gets saved to MongoDB. In MySQL, the database fundamentally rejects bad data types at the hardware level.

## How does it work?
You write a `CREATE TABLE` statement defining all columns and their specific properties (like string max length, default values, and primary keys) before you can push any data into it.

## Visual Diagram
```ascii
MongoDB (Flexible)             MySQL (Strict Table)
{                              +----+-------+-------+
  "name": "Shoes"              | id | name  | price |
}                              +----+-------+-------+
{                              | 1  | Shoes | 39.99 |
  "name": "Hat",               | 2  | Hat   | 15.00 |
  "color": "Red" <--(Messy)    +----+-------+-------+
}                                   NO 'color' COLUMN ALLOWED
```

## Syntax
```sql
-- Fully commented SQL syntax
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY, -- Like Mongoose's default _id
  name VARCHAR(100) NOT NULL,        -- required string
  price DECIMAL(10, 2) DEFAULT 0.00  -- Price format
);
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
const productSchema = new mongoose.Schema({
  name: { type: String, required: true },
  price: { type: Number, default: 0 }
});

// SQL
-- CREATE TABLE products (
--   id INT PRIMARY KEY AUTO_INCREMENT,
--   name VARCHAR(255) NOT NULL,
--   price DECIMAL(10,2) DEFAULT 0
-- );

// Node.js using mysql2/promise (REQUIRED)
await pool.query(`CREATE TABLE products (...)`);

// ORM Equivalent (IMPORTANT)
// Sequelize (Creates the table automatically via db.sync())
const Product = sequelize.define('Product', {
  name: { type: DataTypes.STRING, allowNull: false },
  price: { type: DataTypes.DECIMAL, defaultValue: 0 }
});
```

### Raw SQL vs ORM
- **Raw SQL:** Great for learning migration logic and understanding exact DB constraints.
- **ORM:** ORMs use methods like `sequelize.sync()` to auto-generate `CREATE TABLE` commands. Best in production via "Migration Files".

### Real-World Scenario + Full Stack Code
**Scenario:** Admin panel button that initializes the tables on first run.

```sql
-- SQL query
CREATE TABLE IF NOT EXISTS categories (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL
);
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.post('/api/init-db', async (req, res) => {
  const query = `
    CREATE TABLE IF NOT EXISTS categories (
      id INT PRIMARY KEY AUTO_INCREMENT,
      name VARCHAR(50) NOT NULL
    )
  `;
  await pool.query(query); // No params needed for purely DDL queries
  res.json({ success: true });
});

// ORM version (Sequelize/Prisma)
app.post('/api/init-db', async (req, res) => {
  await sequelize.sync();
  res.json({ success: true });
});

// React component using Axios
function InitDBButton() {
  return <button onClick={() => axios.post('/api/init-db')}>Init DB</button>;
}
```

**Output:**
```json
{
  "success": true
}
```

## Impact
Creating tables manually from the application code is rare in real life (often done via migration frameworks like Knex or Prisma). If a table structure is flawed (e.g. `VARCHAR(5)` for an email), production inserts will instantly crash.

## Practice Exercises
- **Easy (SQL)**: Write a CREATE TABLE for `customers` with `id`, `name`, and `email`.
- **Medium (SQL + Node.js)**: Trigger the creation of a `customers` table via an Express route if it doesn't already exist.
- **Hard (Full stack)**: Build a setup page in React that lists tables existing in the DB (use Node.js `SHOW TABLES` query).

## Interview Q&A
1. **Core SQL:** What does `PRIMARY KEY` mean?
   *It uniquely identifies a row. Like `_id` in Mongo, it automatically gets indexed.*
2. **MERN integration:** Where do we put table creations?
   *Usually in separate migration scripts, not in the main API flow.*
3. **SQL vs MongoDB:** Can I insert a row with an unknown column?
   *No, MySQL will fail safely. MongoDB would accept and store it.*
4. **Scenario-based:** You need a table for orders. What's the best primary key representation?
   *`INT AUTO_INCREMENT` or `VARCHAR(36)` if storing UUIDs.*
5. **Advanced/tricky:** What is the difference between DDL and DML?
   *DDL (Data Definition Language) creates tables (CREATE). DML (Data Manipulation Language) edits rows (INSERT/UPDATE).*

| Previous: [01_What_Is_SQL.md](./01_What_Is_SQL.md) | Next: [03_Data_Types.md](./03_Data_Types.md) |
