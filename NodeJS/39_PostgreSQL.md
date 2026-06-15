# PostgreSQL

## What You Will Learn
* The core principles of Relational Databases (SQL, Schemas, Tables, Joins).
* Understanding the ACID transaction properties (Atomicity, Consistency, Isolation, Durability).
* Initializing database connection pools in Node.js using the native `pg` driver.
* Preventing SQL Injection vulnerabilities using Parameterized Queries.
* Executing basic SQL CRUD operations in Node.js.

## Why This Matters
While NoSQL databases like MongoDB are popular, relational databases like PostgreSQL are the standard choice for applications requiring complex query joins, strong data consistency, and transactional guarantees. Understanding how to manage PostgreSQL connection pools and write secure, parameterized SQL queries is essential for building secure, enterprise-grade backend systems.

## Theory

### Relational Databases and SQL
Relational databases organize data into rigid, pre-defined tables. Tables are linked together using **Foreign Keys**, allowing you to combine data from multiple tables using `JOIN` statements. You query the data using **SQL (Structured Query Language)**.

### ACID Properties
PostgreSQL guarantees that all transactions adhere to the **ACID** properties, ensuring database reliability:
* **Atomicity**: "All or nothing." If any part of a multi-step transaction fails, the entire transaction is rolled back, leaving the database unchanged.
* **Consistency**: Ensures that data written to the database complies with all schema rules, constraints, and triggers.
* **Isolation**: Concurrently running transactions execute independently without interfering with each other's state.
* **Durability**: Once a transaction commits, the changes are written to disk and will not be lost even if the system loses power.

## Deep Dive

### Connection Pooling with the `pg` Driver
Connecting to a PostgreSQL database requires a TCP handshake and user authentication, which takes time. To keep queries fast, the Node.js `pg` module uses a **`Pool`** class.
* The `Pool` maintains a set of active, reusable connections to the database server.
* When you run `pool.query()`, the pool automatically borrows a client, executes the query, and returns the client to the pool.
* Never call `pg.Client` directly inside route handlers; always use the `Pool` class to manage database connections.

### SQL Injection Vulnerability
SQL Injection occurs when untrusted user input is concatenated directly into a SQL query string:

```sql
-- DANGEROUS: concat string input
SELECT * FROM users WHERE email = '` + req.query.email + `';
```

If a user inputs `' OR '1'='1`, the compiled query becomes:
```sql
SELECT * FROM users WHERE email = '' OR '1'='1';
```
This returns every record in the database, bypassing authentication.

To prevent this, always use **Parameterized Queries** (also called Prepared Statements). The values are passed separately from the query template, ensuring the database engine treats client inputs strictly as parameters, not executable code.

## Visual Explanation

### Concatenated Query (Insecure) vs. Parameterized Query (Secure)
```text
Insecure Approach (String Concatenation):
Input: "test@db.com'; DROP TABLE users; --"
Query compiled by Node:
SELECT * FROM users WHERE email = 'test@db.com'; DROP TABLE users; --';
Result: Database executes the read query, then executes the malicious DROP TABLE command!

Secure Approach (Parameterized Query):
Query Template: SELECT * FROM users WHERE email = $1;
Parameters sent separately: ["test@db.com'; DROP TABLE users; --"]
Result: Database treats the entire input strictly as a text string lookup value for email, executing safely.
```

## Real-World Example
Consider a bank transfer transaction. You need to debit one account and credit another. This requires a transaction: if the debit succeeds but the credit fails, the database rolls back the debit, keeping the data consistent. Using the `pg` pool, you run `BEGIN`, execute the SQL statements, and run `COMMIT`. If any statement fails, you run `ROLLBACK` to revert changes.

## Code Examples

### PostgreSQL Connection Pool and Parameterized CRUD Operations

```javascript
// db/pgPool.js
// Dependency required: npm install pg
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.PGHOST || 'localhost',
  port: process.env.PGPORT || 5432,
  database: process.env.PGDATABASE || 'mastery_db',
  user: process.env.PGUSER || 'postgres',
  password: process.env.PGPASSWORD || 'secret',
  max: 20,                  // Max active connections in the pool
  idleTimeoutMillis: 30000, // Close idle connections after 30 seconds
  connectionTimeoutMillis: 2000 // Return connection error after 2 seconds
});

// Test connection on startup
pool.on('connect', () => {
  console.log('PostgreSQL client acquired from pool.');
});

pool.on('error', (err) => {
  console.error('Unexpected error on idle pg client:', err.message);
});

module.exports = pool;
```

```javascript
// user-repository.js
const pool = require('./db/pgPool');

// 1. CREATE Table schema setup (Simulated schema initialization)
async function initializeSchema() {
  const queryText = `
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      email VARCHAR(255) UNIQUE NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `;
  await pool.query(queryText);
  console.log('Users table checked/created.');
}

// 2. CRUD: Insert User (Parameterized)
async function createUser(name, email) {
  const queryText = 'INSERT INTO users(name, email) VALUES($1, $2) RETURNING *;';
  const values = [name, email]; // Passed separately to prevent SQL Injection

  const res = await pool.query(queryText, values);
  return res.rows[0];
}

// 3. CRUD: Find User by Email
async function findUserByEmail(email) {
  const queryText = 'SELECT * FROM users WHERE email = $1;';
  const res = await pool.query(queryText, [email]);
  return res.rows[0] || null;
}

async function runDemo() {
  await initializeSchema();
  try {
    const newUser = await createUser('Alice', 'alice@postgres.com');
    console.log('Created user record:', newUser);

    const user = await findUserByEmail('alice@postgres.com');
    console.log('Found user record:', user);
  } catch (err) {
    console.error('Database query error:', err.message);
  } finally {
    // End the pool connection during script termination
    await pool.end();
  }
}
runDemo();
```

## Best Practices
* **Always Use Parameterized Queries**: Never construct SQL query strings using string interpolation (`${value}`) or string concatenation. Use placeholders (`$1`, `$2`) to pass inputs safely.
* **Release Clients in Manual checkouts**: If you check out a client from the pool manually (using `pool.connect()`) to run a multi-query transaction, always call `client.release()` inside a `finally` block to return the connection to the pool.
* **Tune Pool Sizes for Hardware**: Set your pool size based on your database server capacity. Setting it too high will overwhelm the database server CPU, while setting it too low will block the Node.js application.

## Interview Questions

### Beginner
* **What does ACID stand for in database transactions?**
  *Answer*: ACID stands for:
  * **Atomicity**: Guarantees that all operations within a transaction succeed or all fail together.
  * **Consistency**: Ensures the database remains in a valid state after updates.
  * **Isolation**: Prevents concurrent transactions from interfering with each other.
  * **Durability**: Guarantees that changes are saved to disk once committed, surviving server crashes.

### Intermediate
* **What is SQL Injection, and how do parameterized queries prevent it?**
  *Answer*: SQL Injection occurs when untrusted user input is concatenated directly into a SQL query string, allowing attackers to execute arbitrary database commands. Parameterized queries prevent this by separating the query template from the parameter values. The database engine pre-compiles the query template, and then treats the parameters strictly as lookup values, preventing them from being executed as code.

### Advanced
* **Why should you use a connection Pool instead of individual client instances in a production web application?**
  *Answer*: Opening a new database connection for every query requires a full TCP handshake, SSL negotiation, and database user authentication, which takes time and resources. 
  A connection `Pool` keeps a set of persistent database connections open in memory. The application can borrow an active connection, execute the query, and return it to the pool instantly. This reduces connection overhead and improves response times.

### Senior Architect
* **How would you implement a secure multi-query transaction in Node.js using the `pg` pool, ensuring that resources are cleaned up safely if an error occurs halfway through execution?**
  *Answer*: To run a secure transaction:
  1. Borrow a single client from the pool using `pool.connect()`. Do not use `pool.query()` directly, as that runs queries on separate connections.
  2. Implement a try/catch block. Inside the `try` block, run `BEGIN` to start the transaction, execute the queries using the client instance, and run `COMMIT` to save changes.
  3. Inside the `catch` block, run `ROLLBACK` to revert any changes if an error occurred.
  4. Inside the `finally` block, call `client.release()` to return the connection back to the pool, preventing connection leaks.
  
  ```javascript
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    await client.query('UPDATE accounts SET balance = balance - $1 WHERE id = $2', [100, 1]);
    await client.query('UPDATE accounts SET balance = balance + $1 WHERE id = $2', [100, 2]);
    await client.query('COMMIT');
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release(); // Crucial!
  }
  ```

---
Previous : [38_Mongoose.md] | Index : [00_index.md] | Next : [40_ORM_Concepts.md]
