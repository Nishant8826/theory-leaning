# Introduction and Setup

> 📌 **File:** 00_Introduction_And_Setup.md | **Level:** Beginner → MERN Developer

---

## What is it?
This is the foundational setup for learning SQL as a MERN developer. We'll install a relational database (MySQL) and connect it to a Node.js Express backend, replacing the typical MongoDB connection.

## MERN Parallel — You Already Know This!
- MongoDB → MySQL
- MongoDB Atlas / Compass → MySQL Community Server / Workbench
- `mongoose.connect()` → `mysql.createPool()`
- `npm i mongoose` → `npm i mysql2`

## Why does it matter?
Without an environment, you can't run queries. In the real world, SQL databases require strict setup (users, databases, host names) compared to schema-less document DBs.

## How does it work?
We install the SQL server locally, create an admin user, define our database `ecommerce`, and write a Node.js connection file to safely handle queries via connection pooling.

## Visual Diagram
```ascii
[React Frontend] (Axios)
      |
      v
[Node.js / Express] (mysql2/promise)
      |
      v
[MySQL Connection Pool]
      |
      v
[MySQL Server (ecommerce DB)]
```

## Setup Instructions & Syntax

### 1. MySQL Installation (Windows)
1. Download **MySQL Installer for Windows**.
2. Choose **Developer Default** or **Custom** (we just need MySQL Server and Node connectors).
3. Set the `root` password. Keep port `3306` default.
4. Download and setup **MySQL Workbench** (visual UI like MongoDB Compass).

### 2. Creating the Database
Open MySQL Workbench, connect to `127.0.0.1:3306`, and run:
```sql
SELECT VERSION();
CREATE DATABASE ecommerce;
```

### 3. Node.js Integration
```bash
npm init -y
npm install express mysql2 dotenv cors
```

### MERN vs SQL — Side-by-Side Code
```javascript
// MongoDB / Mongoose (db.js)
const mongoose = require('mongoose');
mongoose.connect(process.env.MONGO_URI);

// Node.js using mysql2/promise (REQUIRED) (db.js)
const mysql = require('mysql2/promise');
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'yourpassword',
  database: 'ecommerce',
  waitForConnections: true,
  connectionLimit: 10
});
module.exports = pool;

// ORM Equivalent (Sequelize)
const { Sequelize } = require('sequelize');
const sequelize = new Sequelize('ecommerce', 'root', 'yourpassword', {
  host: 'localhost',
  dialect: 'mysql'
});
```

### Raw SQL vs ORM
- **Raw SQL**: Best for learning and complex queries with maximum performance.
- **ORM**: Faster development for standard CRUD apps.

### Real-World Scenario + Full Stack Code
**Scenario**: Testing our database connection with a simple Express API route.

```sql
-- SQL query sent behind the scenes
SELECT 1 + 1 AS result;
```

```javascript
// Node.js + Express using mysql2
const express = require('express');
const pool = require('./db');
const app = express();

app.get('/api/test-connection', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT 1 + 1 AS sum');
    res.json({ success: true, message: 'Connected!', data: rows });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
app.listen(3000, () => console.log('Server open on 3000'));
```

```javascript
// React component using Axios
import { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);
  useEffect(() => {
    axios.get('/api/test-connection').then(res => setData(res.data));
  }, []);
  return <div>{data?.message}</div>;
}
```

**Output:**
```json
{
  "success": true,
  "message": "Connected!",
  "data": [{ "sum": 2 }]
}
```

## Impact
If connection pooling isn't used, your Express app may crash under load because MySQL limits maximum concurrent connections. Mongoose handles pooling implicitly; in MySQL, you must configure a `Pool`.

## Practice Exercises
- **Easy (SQL)**: Write `SHOW DATABASES;` in MySQL Workbench.
- **Medium (SQL + Node.js)**: Setup `db.js` and successfully console.log a query result on startup.
- **Hard (Full stack)**: Build a React page that queries the Express test route and shows a green checkmark if the MySQL DB is connected.

## Interview Q&A
1. **Core SQL**: What is connection pooling?
   *It reuses existing active DB connections rather than opening a new one for every request, improving performance.*
2. **MERN integration**: How differs `mysql2/promise` from `mysql2`?
   *It uses `async/await` which aligns perfectly with modern Express controllers, avoiding callback hell.*
3. **SQL vs MongoDB**: Why do SQL databases use ports like 3306 instead of 27017?
   *Default IANA assigned ports differ; 3306 is standard MySQL, 27017 is standard Mongo.*
4. **Scenario-based**: Express app crashes under heavy load with DB connection errors. Why?
   *Likely using `createConnection` instead of `createPool`.*
5. **Advanced/tricky**: What is the equivalent of a Node `ENV` URI string for MySQL?
   *A connection string like `mysql://user:pass@localhost:3306/db_name`.*

| Previous: None | Next: [01_What_Is_SQL.md](./01_What_Is_SQL.md) |
