# Introduction & Setup

> 📌 **File:** `00_Introduction_And_Setup.md` | **Level:** Beginner → MERN Developer

---

## What is it?

This is your starting point for learning SQL as a MERN stack developer. We'll install MySQL (the database engine), MySQL Workbench (the GUI tool), and connect everything to Node.js using the `mysql2` library — the same way you currently connect to MongoDB with Mongoose.

By the end of this file, you'll have a working MySQL environment and a running Express API that talks to a MySQL database.

---

## MERN Parallel — You Already Know This!

| MERN (What You Know)            | SQL (What You'll Learn)          |
|---------------------------------|----------------------------------|
| MongoDB (database engine)       | MySQL (database engine)          |
| MongoDB Compass (GUI)           | MySQL Workbench (GUI)            |
| `mongoose` (ODM library)        | `mysql2` (driver) / Sequelize (ORM) |
| `mongoose.connect(uri)`         | `mysql.createPool({...})`        |
| `mongodb://localhost:27017`     | `localhost:3306`                 |
| JSON documents                  | Rows in tables                   |
| Collections                     | Tables                           |
| No schema required              | Schema is mandatory              |
| `mongod` (server process)       | `mysqld` (server process)        |

**Key Difference:** MongoDB lets you throw any JSON into a collection. MySQL requires you to define the exact shape of your data (columns, types, constraints) BEFORE inserting anything. Think of it like TypeScript vs plain JavaScript — MySQL enforces structure.

---

## Why does it matter?

- **80%+ of production apps** use relational databases (PostgreSQL, MySQL, SQL Server)
- **Job interviews** almost always test SQL knowledge
- **MERN + SQL** makes you a full-stack developer who can work with ANY database
- Understanding SQL helps you design better MongoDB schemas too
- Most enterprise applications, banking systems, and e-commerce platforms run on SQL databases

---

## How does it work?

### Architecture Comparison

```
MERN Stack (Current):
Browser → React → Express API → Mongoose → MongoDB
                                    ↓
                              mongodb://localhost:27017

SQL Stack (New):
Browser → React → Express API → mysql2 → MySQL
                                    ↓
                              localhost:3306
```

The flow is identical! Only the database layer changes.

---

## Visual Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR DEVELOPMENT STACK                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐  │
│  │  React    │───▶│ Express  │───▶│  MySQL Server    │  │
│  │  (Front)  │    │ (API)    │    │  (Port 3306)     │  │
│  │  :3000    │    │ :5000    │    │                  │  │
│  └──────────┘    └──────────┘    └──────────────────┘  │
│       │               │                   │             │
│       │               │                   │             │
│  Axios/Fetch    mysql2/promise      MySQL Workbench     │
│                                     (GUI Client)        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Step 1: Install MySQL Community Server (Windows)

### Download
1. Go to: https://dev.mysql.com/downloads/mysql/
2. Select **Windows (x86, 64-bit)**
3. Download the **MSI Installer** (larger file, includes everything)

### Install
1. Run the MSI installer
2. Choose **Custom** installation type
3. Select these components:
   - MySQL Server
   - MySQL Workbench
   - MySQL Shell (optional but useful)
4. Click **Next** through the configuration:
   - **Type:** Development Computer
   - **Port:** 3306 (default — keep it)
   - **Authentication:** Use Strong Password Encryption (recommended)
5. **Set Root Password:**
   - Choose a password you'll remember (e.g., `root123` for development)
   - ⚠️ **NEVER use a simple password in production**
6. **Windows Service:**
   - Check "Configure MySQL Server as a Windows Service"
   - Check "Start the MySQL Server at System Startup"
   - Service Name: `MySQL80` (default)
7. Click **Execute** → **Finish**

### Verify Installation
Open **Command Prompt** and run:
```bash
mysql --version
# Expected output: mysql  Ver 8.x.x for Win64 on x86_64
```

If `mysql` is not recognized, add MySQL to your PATH:
```
C:\Program Files\MySQL\MySQL Server 8.0\bin
```

### Connect via Command Line
```bash
mysql -u root -p
# Enter your password when prompted
```

You should see:
```
Welcome to the MySQL monitor.  Commands end with ; or \g.
mysql>
```

---

## Step 2: MySQL Workbench Setup

### Open MySQL Workbench
1. Launch MySQL Workbench from Start Menu
2. You'll see a home screen with **MySQL Connections**

### Create Your First Connection
1. Click the **+** button next to "MySQL Connections"
2. Fill in:
   - **Connection Name:** `Local MySQL`
   - **Hostname:** `127.0.0.1`
   - **Port:** `3306`
   - **Username:** `root`
3. Click **Test Connection** → Enter your root password
4. Click **OK** if successful

### Your First SQL Commands
Double-click your connection to open a query tab. Run these:

```sql
-- Check MySQL version (like running node --version)
SELECT VERSION();

-- Show all databases (like show dbs in MongoDB shell)
SHOW DATABASES;

-- Create our project database
CREATE DATABASE ecommerce;

-- Verify it was created
SHOW DATABASES;

-- Switch to our database (like use ecommerce in MongoDB)
USE ecommerce;

-- Show tables (will be empty for now)
SHOW TABLES;
```

**Expected Output for `SELECT VERSION()`:**
```
+-----------+
| VERSION() |
+-----------+
| 8.0.xx    |
+-----------+
```

**Expected Output for `SHOW DATABASES`:**
```
+--------------------+
| Database           |
+--------------------+
| ecommerce          |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
```

---

## Step 3: Node.js Integration with mysql2

### Why mysql2?

| Library    | Role              | MERN Equivalent      |
|------------|-------------------|----------------------|
| `mysql2`   | Raw SQL driver    | Native MongoDB driver|
| Sequelize  | ORM (abstraction) | Mongoose             |
| Prisma     | Modern ORM        | Mongoose (modern)    |

We use `mysql2` as our PRIMARY tool because:
- It teaches you real SQL (not abstractions)
- It's the fastest MySQL driver for Node.js
- It supports Promises (`mysql2/promise`)
- Parameterized queries prevent SQL injection

### Install

```bash
# Create a new project
mkdir sql-ecommerce-api
cd sql-ecommerce-api
npm init -y

# Install dependencies
npm install express mysql2 dotenv cors
npm install -D nodemon
```

### Create Connection Pool — `db.js`

```js
// db.js — Database connection pool
// Think of this as your mongoose.connect() equivalent

const mysql = require('mysql2/promise');
require('dotenv').config();

// A "pool" reuses connections instead of creating new ones each time
// MongoDB does this automatically; in MySQL, we set it up explicitly
const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || 'root123',
  database: process.env.DB_NAME || 'ecommerce',
  port: process.env.DB_PORT || 3306,
  
  // Pool configuration
  waitForConnections: true,   // Wait if all connections are busy
  connectionLimit: 10,         // Max 10 simultaneous connections
  queueLimit: 0                // Unlimited waiting queue
});

// Test the connection (like mongoose connection event handlers)
async function testConnection() {
  try {
    const connection = await pool.getConnection();
    console.log('✅ MySQL connected successfully!');
    console.log(`📦 Database: ${process.env.DB_NAME || 'ecommerce'}`);
    connection.release(); // Always release connections back to pool!
  } catch (error) {
    console.error('❌ MySQL connection failed:', error.message);
    process.exit(1);
  }
}

testConnection();

module.exports = pool;
```

### Create `.env` file

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root123
DB_NAME=ecommerce
DB_PORT=3306
PORT=5000
```

### MERN vs SQL — Connection Comparison

```js
// ========== MONGODB (What you know) ==========
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/ecommerce')
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error(err));

// ========== MYSQL (What you're learning) ==========
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'root123',
  database: 'ecommerce'
});

// Test connection
const [rows] = await pool.query('SELECT 1');
console.log('MySQL connected');
```

---

## Step 4: Create Test Express API Route

### `server.js`

```js
// server.js — Express server with MySQL
const express = require('express');
const cors = require('cors');
const pool = require('./db');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json()); // Like body-parser (you already know this)

// =========================================
// Health Check Route
// =========================================
app.get('/api/health', async (req, res) => {
  try {
    // Run a simple query to check if DB is alive
    const [rows] = await pool.query('SELECT VERSION() AS version, NOW() AS serverTime');
    
    res.json({
      status: 'ok',
      database: 'MySQL',
      version: rows[0].version,
      serverTime: rows[0].serverTime,
      message: '🎉 MySQL is connected and working!'
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

// =========================================
// List All Databases (like show dbs)
// =========================================
app.get('/api/databases', async (req, res) => {
  try {
    const [rows] = await pool.query('SHOW DATABASES');
    res.json({
      count: rows.length,
      databases: rows.map(row => row.Database)
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// =========================================
// List All Tables in Current Database
// =========================================
app.get('/api/tables', async (req, res) => {
  try {
    const [rows] = await pool.query('SHOW TABLES');
    res.json({
      database: 'ecommerce',
      tables: rows
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// =========================================
// Parameterized Query Example (IMPORTANT!)
// =========================================
app.get('/api/test/:id', async (req, res) => {
  try {
    // ❌ NEVER do this (SQL injection vulnerability):
    // const [rows] = await pool.query(`SELECT * FROM users WHERE id = ${req.params.id}`);
    
    // ✅ ALWAYS use parameterized queries:
    const [rows] = await pool.query(
      'SELECT ? AS receivedId, NOW() AS timestamp',
      [req.params.id]
    );
    
    res.json(rows[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log(`📡 Health check: http://localhost:${PORT}/api/health`);
});
```

### Add Script to `package.json`

```json
{
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  }
}
```

### Run It!

```bash
npm run dev
```

### Test with Browser or curl

Visit: `http://localhost:5000/api/health`

**Expected Output:**
```json
{
  "status": "ok",
  "database": "MySQL",
  "version": "8.0.35",
  "serverTime": "2024-01-15T10:30:00.000Z",
  "message": "🎉 MySQL is connected and working!"
}
```

---

## Syntax — SQL Basics You Just Used

```sql
-- Comments in SQL use double dashes
-- Every SQL statement ends with a semicolon ;

-- Show MySQL version
SELECT VERSION();

-- List all databases
SHOW DATABASES;

-- Create a new database
CREATE DATABASE database_name;

-- Switch to a database
USE database_name;

-- List all tables in current database
SHOW TABLES;

-- Delete a database (careful!)
DROP DATABASE database_name;
```

---

## ORM Equivalent (Sequelize)

```js
// For comparison — this is the Sequelize way (like Mongoose)
// We'll use this as secondary reference throughout the tutorial

const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('ecommerce', 'root', 'root123', {
  host: 'localhost',
  dialect: 'mysql',
  logging: false  // Set to console.log to see generated SQL
});

// Test connection
async function testDB() {
  try {
    await sequelize.authenticate();
    console.log('Sequelize connected to MySQL!');
  } catch (error) {
    console.error('Connection failed:', error);
  }
}

testDB();
```

### Why We Use Raw SQL First

| Approach        | Pros                              | Cons                              |
|-----------------|-----------------------------------|-----------------------------------|
| Raw SQL (mysql2) | Full control, learn real SQL      | More verbose, manual mapping      |
| ORM (Sequelize) | Less code, auto-migrations        | Hides SQL, slower for complex ops |

**Rule of thumb:** Learn raw SQL first, then use an ORM when you understand what it's doing under the hood.

---

## Impact

| If You Skip This...                    | What Happens                                    |
|----------------------------------------|-------------------------------------------------|
| Don't set up connection pool           | App crashes under load (too many connections)    |
| Use string concatenation in queries    | SQL injection → database gets hacked             |
| Forget to release pool connections     | Connection leak → app hangs after a few requests |
| Don't set password for root            | Anyone can access your database                  |
| Skip `.env` for credentials            | Passwords get committed to GitHub                |

---

## Practice Exercises

### Easy
1. Install MySQL and run `SELECT VERSION();` in MySQL Workbench
2. Create a database called `test_db` and then drop it
3. Run `SHOW DATABASES` and identify the system databases

### Medium
4. Create the `db.js` connection pool and verify it works with `node db.js`
5. Create an Express route that returns the current MySQL time using `SELECT NOW()`
6. Modify the health check to also return the current database name using `SELECT DATABASE()`

### Hard
7. Create a full Express app with these routes:
   - `GET /api/health` — returns MySQL version and status
   - `GET /api/databases` — lists all databases
   - `GET /api/time` — returns current server time
   - `POST /api/query` — accepts a `{ query }` body and runs it (⚠️ development only!)
8. Add error handling middleware that catches MySQL connection errors

---

## Real-World Q&A

**Q1:** I'm getting `ECONNREFUSED` when connecting to MySQL from Node.js. What's wrong?
**A:** MySQL server isn't running. Check Windows Services (`services.msc`) → find `MySQL80` → Start it. Also verify the port (3306) and credentials in your `.env` file.

**Q2:** Should I use `mysql` or `mysql2` package?
**A:** Always use `mysql2`. It's faster, supports Promises natively (`mysql2/promise`), and is actively maintained. The original `mysql` package is outdated.

**Q3:** Why use a connection pool instead of a single connection?
**A:** Same reason MongoDB uses connection pooling internally — if 100 users hit your API simultaneously, a single connection would queue all requests. A pool of 10 connections can handle 10 queries in parallel. It's like having 10 checkout lanes instead of 1.

---

## Interview Q&A

**Q1: What is MySQL and how does it differ from MongoDB?**
MySQL is a relational database that stores data in structured tables with predefined schemas. MongoDB is a document database that stores flexible JSON-like documents. MySQL uses SQL for queries; MongoDB uses its own query language. MySQL enforces relationships through foreign keys; MongoDB embeds data or uses references.

**Q2: How do you connect Node.js to MySQL?**
Using the `mysql2/promise` package. You create a connection pool with `mysql.createPool({host, user, password, database})` and use `pool.query()` with async/await to execute queries. Always use parameterized queries to prevent SQL injection.

**Q3: What is a connection pool and why is it important?**
A connection pool is a cache of database connections that can be reused. Instead of opening/closing connections for every query (expensive), the pool maintains a set of open connections. When a query needs to run, it borrows a connection from the pool and returns it when done. This dramatically improves performance under load.

**Q4: What is SQL injection and how do you prevent it?**
SQL injection is when an attacker inserts malicious SQL code through user input. For example, inputting `'; DROP TABLE users; --` could delete your entire table. Prevent it by ALWAYS using parameterized queries: `pool.query('SELECT * FROM users WHERE id = ?', [userId])`. Never concatenate user input into SQL strings.

**Q5: Compare `mysql2` vs Sequelize. When would you use each?**
`mysql2` is a raw driver — you write SQL directly. Use it when you need full control, complex queries, or maximum performance. Sequelize is an ORM that generates SQL from JavaScript methods (like Mongoose for MongoDB). Use it when you want faster development, auto-migrations, and don't need complex SQL. In production, many teams use both: ORM for CRUD, raw SQL for reports and complex queries.

---

| | [Next: What Is SQL →](./01_What_Is_SQL.md) |
|---|---|
