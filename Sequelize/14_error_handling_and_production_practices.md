# 14. Error Handling and Production Practices

## 🎯 Goal of This Chapter
By the end of this chapter, you will be able to implement centralized error-handling middleware in Express to catch Sequelize-specific errors, map validation and constraint failures to clean JSON responses, write index migrations, and configure production-grade logging and connection pooling.

---

## 🤔 Why This Topic Matters
Uncaught database errors are a major source of security leaks and server crashes. If your database connection fails and you do not handle the error:
* The Node process will crash, causing downtime for all users.
* Express might return the raw database error stack to the client, exposing your database schema, column names, or local directory paths to hackers.

Additionally, production databases handle heavy concurrent traffic. Without **indexing** and **pool optimization**, database operations slow down, locking tables and causing connection bottlenecks.

---

## 🧠 Core Concept

### 1. Sequelize Error Hierarchy
Sequelize inherits all its database errors from a base class: **`SequelizeBaseError`**. Understanding this hierarchy lets you handle errors selectively.

* **`SequelizeValidationError`**: Triggered when model-level validations fail.
* **`SequelizeUniqueConstraintError`**: Triggered when a unique DB constraint is violated (e.g. duplicating an email).
* **`SequelizeForeignKeyConstraintError`**: Triggered when trying to write a foreign key that doesn't exist in the parent table.
* **`SequelizeConnectionAcquireTimeoutError`**: Triggered when the pool is empty and a query times out waiting for a connection socket.

### 2. Indexes in Migrations
An **Index** is a data structure (usually a B-Tree) that the database uses to find rows quickly. Without indexes, the database must scan every single row in a table (Full Table Scan) to find matches, which is incredibly slow for large tables.

---

## 🏗 Mental Model / Internal Working

### Indexing: Sequential Scan vs. Index Scan
Imagine a `users` table with 1,000,000 rows.
* **Query**: `SELECT * FROM users WHERE email = 'alice@example.com';`
* **Without Index (Sequential Scan)**: The database reads row 1, then row 2, then row 3... all the way to row 1,000,000. This uses heavy CPU and disk reading.
* **With Index (Index Scan)**: The database checks the index B-Tree (which is ordered). It finds the email location in 3 or 4 index checks, retrieves the row directly, and stops. This takes less than a millisecond.

---

## 🌍 Real-World Analogy
* **Centralized Error Handling** is like having an **Office PR Officer**: instead of letting the internal construction workers scream technical build errors directly to visitors outside the gate, the PR officer catches the issue, formats a polite explanation, and presents it in a clear, friendly announcement (clean JSON response).
* **Indexing** is like a **Phone Book**: if you want to find "John Smith", you go directly to the "S" section. You do not read every single page of the phone book from start to finish.

---

## ⚙️ Syntax / API / Core Usage

### 1. Centralized Express Error Middleware
In Express, error-handling middleware is defined using four arguments: `(err, req, res, next)`.

```javascript
// src/middlewares/errorHandler.js
const { ValidationError, UniqueConstraintError, ForeignKeyConstraintError } = require('sequelize');

module.exports = (err, req, res, next) => {
  // Log the full error internally for developers (use a logger like Winston in production)
  console.error('SYSTEM ERROR:', err);

  // 1. Handle Model Validation Errors
  if (err instanceof ValidationError) {
    const messages = err.errors.map(e => ({ field: e.path, message: e.message }));
    return res.status(400).json({
      status: 'fail',
      error: 'ValidationError',
      details: messages
    });
  }

  // 2. Handle Unique Constraint Errors (e.g., duplicated email)
  if (err instanceof UniqueConstraintError) {
    return res.status(409).json({
      status: 'fail',
      error: 'ConflictError',
      message: err.errors[0].message || 'Data conflict occurred.'
    });
  }

  // 3. Handle Foreign Key Failures
  if (err instanceof ForeignKeyConstraintError) {
    return res.status(400).json({
      status: 'fail',
      error: 'ForeignKeyError',
      message: 'Referenced parent record does not exist.'
    });
  }

  // 4. Default Fallback for generic errors (hide stack traces in production!)
  const isProduction = process.env.NODE_ENV === 'production';
  return res.status(500).json({
    status: 'error',
    message: isProduction ? 'An internal server error occurred.' : err.message,
    ...(isProduction ? {} : { stack: err.stack })
  });
};
```

### 2. Registering Indexes in Migrations
You can add indexes to tables inside migration files using the `queryInterface.addIndex()` method:

```javascript
// src/migrations/[timestamp]-add-indexes-to-posts.js
module.exports = {
  up: async (queryInterface, Sequelize) => {
    // 1. Add single column index
    await queryInterface.addIndex('posts', ['userId']);

    // 2. Add composite index (ordering by userId and creation date)
    await queryInterface.addIndex('posts', ['userId', 'createdAt'], {
      name: 'posts_user_created_idx' // Explicit index name
    });
  },

  down: async (queryInterface) => {
    await queryInterface.removeIndex('posts', 'posts_user_created_idx');
    await queryInterface.removeIndex('posts', ['userId']);
  }
};
```

---

## 💻 Practical Examples

### Using the Error Handler in an Express App
To use the centralized error handler, import it and place it at the **very bottom** of your middleware definitions in `app.js`.

```javascript
// src/app.js
const express = require('express');
const userRouter = require('./routes/userRoutes');
const errorHandler = require('./middlewares/errorHandler');

const app = express();

app.use(express.json());

// Routes
app.use('/users', userRouter);

// Global Error Handler (MUST be defined last)
app.use(errorHandler);

module.exports = app;
```

Inside your controllers, wrap async code in try-catch and forward errors to the handler using `next(error)`:

```javascript
// src/controllers/userController.js
const User = require('../models/User');

module.exports = {
  create: async (req, res, next) => {
    try {
      const user = await User.create(req.body);
      return res.status(201).json(user);
    } catch (error) {
      // Forward the error to our centralized errorHandler middleware
      next(error);
    }
  }
};
```

---

## 🔄 Flow Diagram

### Error Propagation Flow

```text
       Controller Try Block              Sequelize ORM                  Database
                │                              │                           │
                │── User.create(req.body) ────>│                           │
                │                              │─── SQL INSERT Query ─────>│ (Violates Unique)
                │                              │                           │  [Duplicate Key]
                │                              │<── SQL Constraint Error ──│
                │                              │ (Parse error code)
                │<── UniqueConstraintError ────│
                │
     Catch block catches error
                │
                v
           next(error)
                │
                v
      Express Error Middleware (errorHandler.js)
                │
                ├─ Identifies error instance
                ├─ Formats standard JSON payload
                └─ Sends: HTTP 409 Conflict Response
```

---

## 🧪 Common Interview Questions

### Q1: What is the benefit of registering error middleware at the bottom of the Express middleware stack?
* **Answer**: Express executes middlewares and routing handlers in the order they are defined. For error-handling middleware to intercept errors thrown inside routes or controller functions, it must be declared after all other route bindings so that any unhandled exceptions are caught and passed down the `next(err)` pipeline.

### Q2: Why is it bad to log raw SQL statements in production?
* **Answer**: 
  1. **Log Bloat**: Production logs handle high volumes of queries. Logging every SQL statement degrades IO performance and increases hosting storage costs.
  2. **Security Leak**: Raw query logs contain sensitive values in plaintext (e.g. password hashes, user emails, or bank transaction details), violating security regulations like GDPR and PCI-DSS.

### Q3: Do databases automatically index foreign keys?
* **Answer**: No. While databases automatically create indexes for Primary Keys (`id`) and Unique constraints, they do **not** automatically index foreign key columns in child tables (e.g. `userId` in `posts`). Developers must explicitly add indexes on foreign keys to prevent slow queries during join operations.

---

## ⚠️ Common Mistakes / Pitfalls
* **Leaking Stack Traces**: Returning `res.json(error)` or `res.json(err.stack)` to client users in production, exposing database vulnerabilities to attackers.
* **Forgetting `next(error)` in Controllers**: Writing a try-catch block inside an Express controller but forgetting to call `next(error)` inside the catch block. This leaves the HTTP request hanging, eventually timing out and degrading performance.

---

## ✅ Best Practices
* **Separate environments for SQL logging**: Set the `logging` parameter in Sequelize settings conditionally based on `process.env.NODE_ENV` (e.g., enable query logging in local development but disable it in production).
* **Index fields in `WHERE` and `JOIN` clauses**: Always index foreign key columns and any fields regularly used to filter queries (like `isActive` or `status`) or sort records (like `createdAt`).

---

## 📝 Quick Recap
* Handle database exceptions centrally in Express using global error-handling middleware `(err, req, res, next)`.
* Catch Sequelize validation and unique constraint errors separately to return clean messages to users.
* Disable SQL logging in production config to maintain performance and secure logs.
* Explicitly create indexes for foreign keys and query search fields in migration scripts.

---

## 🔗 Navigation
Previous : [13_model_methods_and_advanced_patterns.md](./13_model_methods_and_advanced_patterns.md) | Index : [00_index.md](./00_index.md) | Next : [15_common_mistakes_and_interview_prep.md](./15_common_mistakes_and_interview_prep.md)
