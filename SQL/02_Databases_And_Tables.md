# Databases And Tables

> 📌 **File:** `02_Databases_And_Tables.md` | **Level:** Beginner → MERN Developer

---

## What is it?

A **database** in MySQL is a container that holds related tables — exactly like a MongoDB database holds collections. A **table** is a structured collection of rows and columns — where every row has the same columns (unlike MongoDB documents which can have different fields).

Think of it this way:
- **Database** = A folder on your computer
- **Table** = A spreadsheet file inside that folder
- **Row** = One row in the spreadsheet
- **Column** = One column header in the spreadsheet

---

## MERN Parallel — You Already Know This!

| MongoDB (You Know)                    | MySQL (You'll Learn)                     |
|---------------------------------------|------------------------------------------|
| `use ecommerce` (switch database)     | `USE ecommerce;`                         |
| `show dbs` (list databases)           | `SHOW DATABASES;`                        |
| `show collections`                    | `SHOW TABLES;`                           |
| `db.createCollection('users')`        | `CREATE TABLE users (...);`              |
| `db.users.drop()`                     | `DROP TABLE users;`                      |
| `db.dropDatabase()`                   | `DROP DATABASE ecommerce;`               |
| Collection has no fixed structure     | Table has fixed columns defined at creation |
| Documents can have different fields   | Every row MUST have the same columns     |
| `db.users.stats()`                    | `DESCRIBE users;`                        |

### The Key Difference

```js
// MongoDB — Each document can be different (flexible schema)
db.users.insertOne({ name: "Nishant", age: 24 });
db.users.insertOne({ name: "Priya", hobbies: ["reading"] }); // ← Different fields!
// ✅ MongoDB allows this — no error
```

```sql
-- MySQL — Every row MUST follow the table structure
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  age INT
);

INSERT INTO users (id, name, age) VALUES (1, 'Nishant', 24);  -- ✅ Works
INSERT INTO users (id, name, hobbies) VALUES (2, 'Priya', 'reading');  -- ❌ ERROR! 
-- Column 'hobbies' doesn't exist in this table
```

---

## Why does it matter?

- You MUST create a database and tables before storing any data in MySQL
- Table structure (schema) is enforced at the database level — not optional
- Understanding database/table hierarchy is fundamental to every SQL operation
- Bad table design leads to slow queries, data duplication, and maintenance nightmares
- In production, database and table creation is usually done through migrations (like Mongoose schemas)

---

## How does it work?

### Step-by-Step: Creating Our E-Commerce Database

```
Step 1: Create Database
       │
       ▼
Step 2: Switch to Database (USE)
       │
       ▼
Step 3: Create Tables (with columns & types)
       │
       ▼
Step 4: Verify Structure (DESCRIBE)
       │
       ▼
Step 5: Start inserting data
```

---

## Visual Diagram

### Database Hierarchy

```
MySQL Server (like mongod process)
│
├── ecommerce (database)    ← USE ecommerce;
│   ├── customers (table)
│   │   ├── id       (column)
│   │   ├── name     (column)
│   │   ├── email    (column)
│   │   └── phone    (column)
│   │
│   ├── products (table)
│   │   ├── id       (column)
│   │   ├── name     (column)
│   │   ├── price    (column)
│   │   └── category_id (column)  ← Foreign Key (like ref in Mongoose)
│   │
│   ├── categories (table)
│   ├── orders (table)
│   └── order_items (table)
│
├── information_schema (system DB)
├── mysql (system DB)
├── performance_schema (system DB)
└── sys (system DB)
```

### MongoDB vs MySQL — Data Organization

```
MongoDB:                              MySQL:
┌──────────────────────┐             ┌──────────────────────┐
│ ecommerce (database) │             │ ecommerce (database) │
│                      │             │                      │
│ ┌──────────────────┐ │             │ ┌──────────────────┐ │
│ │ users (collection)│ │             │ │ users (table)    │ │
│ │                  │ │             │ │                  │ │
│ │ { name, age,     │ │             │ │ id | name | age  │ │
│ │   hobbies: [...] │ │             │ │ 1  | Ali  | 25   │ │
│ │   address: {     │ │             │ │ 2  | Sara | 22   │ │
│ │     city: "..."  │ │             │ │                  │ │
│ │   }              │ │             │ │ addresses (table) │ │
│ │ }                │ │             │ │ id|user_id|city   │ │
│ └──────────────────┘ │             │ │ 1 | 1     |Delhi  │ │
│                      │             │ └──────────────────┘ │
│ Nested/embedded data │             │ Separate tables +    │
│                      │             │ relationships (JOIN)  │
└──────────────────────┘             └──────────────────────┘
```

---

## Syntax

```sql
-- ============================================
-- DATABASE OPERATIONS
-- ============================================

-- Create a new database
CREATE DATABASE ecommerce;

-- Create only if it doesn't exist (prevents error)
CREATE DATABASE IF NOT EXISTS ecommerce;

-- Create with specific character set (for international characters)
CREATE DATABASE ecommerce
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Show all databases
SHOW DATABASES;

-- Switch to a database (MUST do before working with tables)
USE ecommerce;

-- Show current database
SELECT DATABASE();

-- Delete a database (⚠️ PERMANENT — no undo!)
DROP DATABASE ecommerce;

-- Safe delete
DROP DATABASE IF EXISTS ecommerce;


-- ============================================
-- TABLE OPERATIONS
-- ============================================

-- Create a table with columns and types
CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,    -- Like MongoDB's _id
  name VARCHAR(100) NOT NULL,           -- String, max 100 chars, required
  email VARCHAR(150) UNIQUE NOT NULL,   -- Must be unique, required
  phone VARCHAR(15),                    -- Optional (nullable)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Auto-set on insert
);

-- Show all tables in current database
SHOW TABLES;

-- Show table structure (column names, types, constraints)
DESCRIBE customers;
-- or
SHOW COLUMNS FROM customers;

-- Show the CREATE TABLE statement used to create the table
SHOW CREATE TABLE customers;

-- Delete a table (⚠️ PERMANENT)
DROP TABLE customers;

-- Safe delete
DROP TABLE IF EXISTS customers;

-- Delete ALL rows but keep table structure
TRUNCATE TABLE customers;
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== MongoDB / Mongoose ==========

// Define a schema (optional in raw MongoDB)
const customerSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  phone: String,
  createdAt: { type: Date, default: Date.now }
});

const Customer = mongoose.model('Customer', customerSchema);
// Collection 'customers' is auto-created when first document is inserted
```

```sql
-- ========== MySQL (SQL) ==========

-- Create the database
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

-- Create the table (MUST do before inserting)
CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  phone VARCHAR(15),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Create the database
await pool.query('CREATE DATABASE IF NOT EXISTS ecommerce');

// Create the customers table
await pool.query(`
  CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
`);

// Check table structure
const [columns] = await pool.query('DESCRIBE customers');
console.log(columns);

// List all tables
const [tables] = await pool.query('SHOW TABLES');
console.log(tables);
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize (like Mongoose) ==========
const { DataTypes } = require('sequelize');
const sequelize = require('./sequelizeDb');

// Define model — generates CREATE TABLE automatically
const Customer = sequelize.define('Customer', {
  // id is auto-created by Sequelize (like _id in Mongoose)
  name: {
    type: DataTypes.STRING(100),
    allowNull: false          // Like required: true in Mongoose
  },
  email: {
    type: DataTypes.STRING(150),
    allowNull: false,
    unique: true              // Like unique: true in Mongoose
  },
  phone: {
    type: DataTypes.STRING(15),
    allowNull: true           // Optional field
  }
  // createdAt and updatedAt are auto-added by Sequelize (like timestamps: true in Mongoose)
}, {
  tableName: 'customers'     // Explicit table name (like collection: 'customers' in Mongoose)
});

// Sync model with database (creates table if not exists)
// Like mongoose.model() + first insert
await Customer.sync();

// Force recreate table (drops and recreates — like db.collection.drop())
await Customer.sync({ force: true });
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Initialize the e-commerce database with all tables

```sql
-- SQL: Create all tables for our e-commerce app
CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table (references categories)
CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL,
  stock INT DEFAULT 0,
  category_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  phone VARCHAR(15),
  address TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table (references customers)
CREATE TABLE IF NOT EXISTS orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  total_amount DECIMAL(10, 2) DEFAULT 0,
  status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
  order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Order Items table (references orders and products)
CREATE TABLE IF NOT EXISTS order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  unit_price DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);
```

```js
// Node.js — Database initialization script (run once)
// initDb.js
const pool = require('./db');

async function initDatabase() {
  try {
    // Create categories table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✅ categories table created');

    // Create products table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL,
        stock INT DEFAULT 0,
        category_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(id)
      )
    `);
    console.log('✅ products table created');

    // Create customers table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        phone VARCHAR(15),
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✅ customers table created');

    // Create orders table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT NOT NULL,
        total_amount DECIMAL(10, 2) DEFAULT 0,
        status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
      )
    `);
    console.log('✅ orders table created');

    // Create order_items table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS order_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL DEFAULT 1,
        unit_price DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
      )
    `);
    console.log('✅ order_items table created');

    // Verify all tables
    const [tables] = await pool.query('SHOW TABLES');
    console.log('\n📋 All tables:', tables.map(t => Object.values(t)[0]));
    
  } catch (error) {
    console.error('❌ Database initialization failed:', error.message);
  } finally {
    process.exit(0);
  }
}

initDatabase();
```

```js
// Express route to list tables
app.get('/api/schema', async (req, res) => {
  try {
    const [tables] = await pool.query('SHOW TABLES');
    const tableNames = tables.map(t => Object.values(t)[0]);
    
    // Get structure of each table
    const schema = {};
    for (const table of tableNames) {
      const [columns] = await pool.query(`DESCRIBE ${table}`);
      schema[table] = columns;
    }
    
    res.json({ database: 'ecommerce', tables: schema });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// React component — Display database schema
import { useState, useEffect } from 'react';
import axios from 'axios';

function DatabaseSchema() {
  const [schema, setSchema] = useState(null);

  useEffect(() => {
    axios.get('/api/schema')
      .then(({ data }) => setSchema(data))
      .catch(err => console.error(err));
  }, []);

  if (!schema) return <p>Loading schema...</p>;

  return (
    <div>
      <h2>Database: {schema.database}</h2>
      {Object.entries(schema.tables).map(([tableName, columns]) => (
        <div key={tableName}>
          <h3>📋 {tableName}</h3>
          <table border="1" cellPadding="8">
            <thead>
              <tr>
                <th>Column</th>
                <th>Type</th>
                <th>Nullable</th>
                <th>Key</th>
                <th>Default</th>
              </tr>
            </thead>
            <tbody>
              {columns.map((col, i) => (
                <tr key={i}>
                  <td>{col.Field}</td>
                  <td>{col.Type}</td>
                  <td>{col.Null}</td>
                  <td>{col.Key}</td>
                  <td>{col.Default || 'NULL'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}
```

**Output (DESCRIBE customers):**
```
+------------+--------------+------+-----+-------------------+-------------------+
| Field      | Type         | Null | Key | Default           | Extra             |
+------------+--------------+------+-----+-------------------+-------------------+
| id         | int          | NO   | PRI | NULL              | auto_increment    |
| name       | varchar(100) | NO   |     | NULL              |                   |
| email      | varchar(150) | NO   | UNI | NULL              |                   |
| phone      | varchar(15)  | YES  |     | NULL              |                   |
| created_at | timestamp    | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+------------+--------------+------+-----+-------------------+-------------------+
```

---

## Impact

| If You Don't Understand This...       | What Happens                                    |
|---------------------------------------|-------------------------------------------------|
| Don't create tables before inserting   | `ERROR 1146: Table doesn't exist`               |
| Forget `IF NOT EXISTS`                | Script crashes on second run                     |
| Use DROP instead of TRUNCATE          | Lose table structure + data (vs. just data)      |
| Don't define column types properly     | Data truncation, wrong calculations              |
| Forget FOREIGN KEY relationships       | Orphaned data, no referential integrity          |
| Don't use UTF8MB4 charset             | Emojis and special characters break              |

---

## Practice Exercises

### Easy (SQL)
1. Create a database called `test_shop` and verify it with `SHOW DATABASES`
2. Switch to `test_shop` and create a table called `items` with columns: `id`, `name`, `price`
3. Run `DESCRIBE items` and understand each column in the output
4. Drop the `items` table, then drop the `test_shop` database

### Medium (SQL + Node.js)
5. Write a Node.js script that creates the `ecommerce` database and all 5 tables
6. Create an Express route `GET /api/tables` that returns all table names in the database
7. Create an Express route `GET /api/tables/:name` that returns the column structure of a specific table

### Hard (Full Stack)
8. Build a React UI that:
   - Fetches and displays all tables in the database
   - Click a table name to see its column structure
   - Has a "Create Table" form that lets you specify columns and creates the table via API
9. Create a database migration system:
   - Version-numbered SQL files in a `migrations/` folder
   - A script that runs pending migrations in order
   - Track which migrations have been applied (hint: use a `migrations` table)

---

## Real-World Q&A

**Q1:** In MongoDB, collections are auto-created when I insert data. Why do I need to manually create tables in MySQL?
**A:** Because MySQL enforces a schema. It needs to know the exact columns, their data types, and constraints BEFORE you insert data. This prevents inconsistent data. Think of it like TypeScript interfaces — you define the shape first, then the data must match.

**Q2:** What's the difference between DROP and TRUNCATE?
**A:** `DROP TABLE users` deletes the table AND all its data — the table is gone completely. `TRUNCATE TABLE users` deletes all rows but keeps the table structure intact (like `db.users.deleteMany({})`). `DELETE FROM users` also deletes all rows but is slower because it logs each deletion for potential rollback.

**Q3:** How do I add a new column to an existing table? In MongoDB, I just add a new field to my document.
**A:** Use `ALTER TABLE`: `ALTER TABLE users ADD COLUMN age INT AFTER name;`. We'll cover this in detail in file 04. In MongoDB, there's no equivalent because fields are dynamic. In SQL, you must explicitly modify the table structure.

---

## Interview Q&A

**Q1: What is the difference between a database and a table in MySQL?**
A database is a container/namespace that holds related tables. A table is a structured set of data organized in rows and columns. A MySQL server can have multiple databases, and each database can have multiple tables. This is analogous to MongoDB where a database holds multiple collections.

**Q2: What is the difference between DROP, TRUNCATE, and DELETE?**
DROP removes the entire table (structure + data). TRUNCATE removes all rows but keeps the table structure; it's fast because it doesn't log individual row deletions. DELETE removes specific rows (or all if no WHERE clause); it's slower but can be rolled back in a transaction and triggers ON DELETE events.

**Q3: What is AUTO_INCREMENT and how does it compare to MongoDB's _id?**
AUTO_INCREMENT automatically generates a unique integer for each new row, incrementing by 1. MongoDB's `_id` is similar but uses ObjectId (a 12-byte unique identifier). AUTO_INCREMENT is sequential and predictable; ObjectId encodes timestamp, machine ID, and a counter, making it globally unique across distributed systems.

**Q4: What are FOREIGN KEYS and why don't MongoDB collections have them?**
Foreign keys create a link between two tables, ensuring that a value in one table must exist in another. For example, `orders.customer_id` must reference a valid `customers.id`. MongoDB doesn't have foreign keys because it uses embedded documents or manual references (`populate()` in Mongoose). SQL foreign keys are enforced by the database engine; MongoDB references are enforced by application code.

**Q5: You're designing a MySQL database for a social media app. What tables would you create and how would they relate?**
Core tables: `users` (id, name, email), `posts` (id, user_id FK→users, content, created_at), `comments` (id, post_id FK→posts, user_id FK→users, text), `likes` (id, post_id FK→posts, user_id FK→users), `followers` (follower_id FK→users, following_id FK→users). The `likes` and `followers` tables are junction tables that represent many-to-many relationships. In MongoDB, you might embed comments in posts, but in SQL, each entity gets its own table.

---

| [← Previous: What Is SQL](./01_What_Is_SQL.md) | [Next: Data Types →](./03_Data_Types.md) |
|---|---|
