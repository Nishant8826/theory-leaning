# SQL Injection

SQL Injection is one of the most destructive security vulnerabilities in backend applications. If an attacker can inject SQL commands into your queries, they can bypass login screens, read your entire database (including passwords and credit cards), modify data, or drop entire tables. Parameterizing your queries is critical for database security.

### What is SQL Injection?
**SQL Injection (SQLi)** occurs when untrusted user input is concatenated directly into a SQL query string instead of being passed as a parameter. This allows the database engine to interpret the input as SQL command instructions rather than text data.

### Common SQLi Attack Vectors
1. **Authentication Bypass**: Injecting characters like `' OR '1'='1` to force queries (like user lookups) to return true, bypassing login checks without credentials.
2. **UNION-Based SQLi**: Appending `UNION SELECT` commands to normal queries to merge and extract sensitive data from other tables (like passwords or configuration settings).
3. **Data Modification/Deletion**: Appending command separators (like `;`) followed by destructive SQL commands (such as `DROP TABLE users;`).

## Deep Dive

### Parameterized Queries vs. String Concatenation
* **String Concatenation (Insecure)**: The query and parameters are sent to the database engine as a single string. The database compiles and executes the string, executing any injected SQL commands:
  ```javascript
  const sql = `SELECT * FROM users WHERE email = '${email}';`;
  ```
* **Parameterized Queries (Secure)**: The database query template is sent to the database engine first. The engine compiles the query template, establishing the execution plan. The parameters are sent separately:
  ```javascript
  const sql = 'SELECT * FROM users WHERE email = $1;';
  const values = [email];
  ```
  The database engine treats the parameters strictly as variables, preventing them from altering the query structure.

### Database User Permissions (Least Privilege)
To limit the impact if a vulnerability exists, restrict your database user permissions:
* Create a dedicated database user for your application.
* Grant only the permissions needed (e.g. `SELECT`, `INSERT`, `UPDATE`, `DELETE` on specific tables). Do not grant admin privileges (like `SUPERUSER` or `CREATE TABLE`).
* Use a read-only database user for reporting or analytical queries, preventing data modifications.

## Visual Explanation

### SQL Injection Authentication Bypass Flow
```mermaid
graph TD
    subgraph Flow ["SQL Injection Authentication Bypass Flow"]
        Input["Attack Input:<br/>email = admin@app.com<br/>password = ' OR '1'='1"] --> Compilation["Compiled SQL String Execution:<br/>SELECT * FROM users WHERE email = 'admin@app.com' AND password = '' OR '1'='1';"]
        Compilation --> Eval1{Step 1: Evaluate AND}
        Eval1 -->|'admin@app.com' AND ''| False["False"]
        False --> Eval2{Step 2: Evaluate OR}
        Eval2 -->|False OR '1'='1'| True["True"]
        True --> Bypass([Authentication Bypassed - Logged in as Admin!])
    end

    style Input fill:#fff3cd,stroke:#ffc107
    style Compilation fill:#f8d7da,stroke:#dc3545
    style Bypass fill:#f8d7da,stroke:#dc3545,stroke-width:2px
```

## Real-World Example
Consider an endpoint `/api/search` that allows users to search items by name. If the query concatenates the input string directly, an attacker can append a UNION command: `?name=shoe' UNION SELECT username, password FROM users; --`. The database will merge the user records into the search results, leaking passwords to the client. Using parameterized queries blocks the attack.

## Code Examples

### Vulnerable Concatenation and Secure SQL Resolution in Node.js

```javascript
// sqli-prevention.js
const { Pool } = require('pg');
const AppError = require('./utils/AppError');

const pool = new Pool({
  host: 'localhost',
  database: 'mastery_db',
  user: 'postgres',
  password: 'password'
});

// 1. DANGEROUS: String Concatenation (Vulnerable to SQLi)
async function vulnerableLogin(req, res, next) {
  const { email, password } = req.body;
  
  // If attacker passes password: ' OR '1'='1
  const sqlQuery = `SELECT * FROM users WHERE email = '${email}' AND password = '${password}';`;
  
  try {
    const result = await pool.query(sqlQuery);
    res.json(result.rows);
  } catch (err) {
    next(err);
  }
}

// 2. SECURE: Parameterized Query (SQLi Proof)
async function secureLogin(req, res, next) {
  const { email, password } = req.body;

  // Use placeholders ($1, $2) to separate query logic from parameters
  const sqlQuery = 'SELECT * FROM users WHERE email = $1 AND password = $2;';
  const values = [email, password];

  try {
    const result = await pool.query(sqlQuery, values);
    
    if (result.rows.length === 0) {
      return next(new AppError('Unauthorized: Invalid email or password.', 401));
    }
    
    res.json(result.rows[0]);
  } catch (err) {
    next(err);
  }
}

// 3. SECURE: Validating Input Type before querying
async function fetchUserById(req, res, next) {
  const userId = req.params.id;

  // Ensure parameter is a number to prevent string injection
  const numericId = parseInt(userId, 10);
  if (isNaN(numericId)) {
    return next(new AppError('Bad Request: Invalid numeric ID.', 400));
  }

  try {
    const sqlQuery = 'SELECT * FROM users WHERE id = $1;';
    const result = await pool.query(sqlQuery, [numericId]);
    res.json(result.rows[0]);
  } catch (err) {
    next(err);
  }
}
```

## Best Practices
* **Never Concatenate Inputs in SQL**: Always use parameterized queries (prepared statements) for all database transactions.
* **Use Query Builders or ORMs**: Use query builders (like Knex) or ORMs (like Prisma or Sequelize) that handle input parameterization automatically.
* **Validate and Cast Input Types**: Validate and cast incoming route parameters (e.g. converting ID strings to numbers using `parseInt`) before executing queries.
* **Apply Least Privilege to DB Users**: Restrict application database user permissions to block admin operations like `DROP TABLE` in production.

## Interview Questions

**Q:** What is SQL Injection (SQLi)?

> **Answer:**
> SQL Injection is a vulnerability that occurs when untrusted user input is concatenated directly into a SQL query string, allowing the database engine to execute the input as SQL commands.

**Q:** How do parameterized queries prevent SQL Injection?

> **Answer:**
> Parameterized queries (prepared statements) separate the query template from the parameter values. The database engine compiles the query template first to establish the execution plan, and then inserts the parameters strictly as text or data values, preventing them from altering the query structure.

**Q:** What is a UNION-based SQL Injection attack, and what does the attacker require to execute it successfully?

> **Answer:**
> A UNION-based SQL Injection attack occurs when an attacker appends a `UNION SELECT` command to a normal query to merge and return results from other tables.
> To execute it successfully, the attacker must:
> 1. Determine the number of columns returned by the original query (often by appending `ORDER BY` commands).
> 2. Match the data types of the columns in the `UNION` query with those of the original query.
> If successful, the query returns the requested data (such as passwords or configuration settings) directly in the search results.

**Q:** How would you architecture a database security strategy in an enterprise Node.js microservices fleet to mitigate the impact if a SQL Injection vulnerability is compromised in one of the services?

> **Answer:**
> To mitigate the impact of a database compromise:
> 1. **Least Privilege Users**: Create unique database credentials for each microservice. Limit permissions strictly to the tables that specific service needs to access (e.g., the billing service cannot access the user credentials table).
> 2. **Row-Level Security (RLS)**: Enable Row-Level Security in the database (e.g. in PostgreSQL) to restrict queries to return only records associated with the active tenant or user context.
> 3. **Network Isolation**: Deploy database instances inside a private virtual network (VPC), allowing access only from authenticated application containers and blocking direct external connections.
> 4. **Encryption at Rest**: Encrypt sensitive data columns (like credit cards or passwords) using AES-256-GCM. This ensures that even if an attacker extracts raw table rows via SQLi, the data remains encrypted and unreadable.

---
Previous : [60_XSS.md](60_XSS.md) | Index : [00_index.md](00_index.md) | Next : [62_NoSQL_Injection.md](62_NoSQL_Injection.md)
