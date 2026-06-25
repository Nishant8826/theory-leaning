# 15. Common Mistakes and Interview Prep

## 🎯 Goal of This Chapter
By the end of this chapter, you will be prepared for senior backend interviews. You will study common Sequelize anti-patterns and their corrections, review 15+ detailed scenario-based interview questions, and understand the final recommended directory architecture for professional Express + Sequelize applications.

---

## 🤔 Why This Topic Matters
Many developers can write basic CRUD queries. However, in production environments and during backend interviews, you are judged on your ability to handle complex scenarios: troubleshooting performance drops, preventing concurrency errors, scaling databases under heavy loads, and structuring code clean-architecture systems. This chapter bridges the gap between learning syntax and writing production-ready code.

---

## 🏗 Recommended Final Project Architecture
For medium-to-large production applications, organize your code into a layered structure to separate HTTP transport, business logic, data queries, and database models.

```text
src/
├── config/
│   └── database.js       # Sequelize configuration and environment settings
├── constants/
│   └── roles.js          # Predefined application constants (role types)
├── controllers/
│   └── userController.js # Handles req/res boundary, validates HTTP requests
├── middlewares/
│   ├── auth.js           # JWT authentication middleware
│   └── errorHandler.js   # Centralized error mapping and formatting
├── migrations/           # Database migration files (immutable)
├── models/
│   ├── index.js          # Core database bootstrapping and association loader
│   ├── User.js           # User model class
│   └── Post.js           # Post model class
├── repositories/
│   └── userRepository.js # Wraps Sequelize operations (Data Access Layer)
├── routes/
│   └── userRoutes.js     # Express route definitions
├── seeders/              # Mock and default database seed files
├── services/
│   └── userService.js    # Enforces business rules and triggers external logic
├── app.js                # Express app setup and middleware configuration
└── server.js             # Starts the HTTP listener and validates DB connection
```

---

## ⚠️ Common Mistakes / Pitfalls and Corrections

### 1. The Async-Inside-Loop Anti-pattern (N+1 Query)
* **Bad**:
  ```javascript
  const posts = await Post.findAll();
  const data = await Promise.all(posts.map(async (post) => {
    const comments = await post.getComments(); // Triggers queries in a loop!
    return { ...post.toJSON(), comments };
  }));
  ```
* **Good**:
  ```javascript
  const posts = await Post.findAll({
    include: [{ model: Comment, as: 'comments' }] // Executes 1 Join query
  });
  ```

### 2. Forgetting Arrow Function Limitations on Model Methods
* **Bad**:
  ```javascript
  User.prototype.getFullName = () => {
    return `${this.firstName} ${this.lastName}`; // 'this' is undefined here!
  };
  ```
* **Good**:
  ```javascript
  User.prototype.getFullName = function() {
    return `${this.firstName} ${this.lastName}`; // 'this' correctly binds to the user instance
  };
  ```

### 3. Exposing Password Hashes in API Outputs
* **Bad**:
  ```javascript
  const user = await User.findByPk(req.params.id);
  res.json(user); // Sends password hashes to the client!
  ```
* **Good**:
  ```javascript
  // Inside src/models/User.js:
  toJSON() {
    const values = { ...this.get() };
    delete values.password; // Auto-removes password from all res.json() calls
    return values;
  }
  ```

---

## 🧪 15 Scenario-Based Interview Questions & Answers

### Q1: A client says that their database connection limit is exhausted in production every day. How do you troubleshoot?
* **Answer**: 
  1. **Singleton Check**: Verify if the application initializes `new Sequelize()` inside multiple files instead of exporting a single instance from a configuration file.
  2. **Serverless Configuration**: If deployed on AWS Lambda, check the connection pool. Serverless functions scale by running multiple isolated containers. If each container opens a pool of 10 connections, they will quickly crash the database connection limit. In serverless, pool sizes should be set to `max: 1` or `max: 2` with idle timeouts configured low.
  3. **Connection Leaks**: Ensure all connection-testing scripts close sockets correctly when running background cron tasks.

### Q2: You need to migrate database schemas from SQLite in development to MySQL in production. What issues do you expect and how do you handle them?
* **Answer**: SQLite is dynamically typed and forgiving, while MySQL enforces schemas strictly (especially in Strict SQL Mode) and behaves differently regarding table casing depending on the host operating system.
  * **Issues**:
    1. **Table Casing**: SQLite treats table names as case-insensitive. In MySQL, table casing is dependent on the host Operating System. Windows is case-insensitive, but Linux servers (where most production code is deployed) enforce case-sensitive table checks. A query to `users` works on Windows but crashes on Linux if the table was created as `Users`.
    2. **Data Constraints**: SQLite allows writing a long string into a VARCHAR(50) field without error, but MySQL strict mode will reject the query and throw a DataTruncation error.
  * **Solution**: Always standardize table naming conventions (explicit lowercase pluralized tables, e.g. `'users'`), set strict SQL constraints locally, and run developer integration tests using a local MySQL Docker container instance instead of SQLite to catch configuration errors early.

### Q3: A bulk update like `User.update({ isActive: false }, { where: { id: [1, 2] } })` is not hashing passwords. Why?
* **Answer**: Bulk queries inside Sequelize run as a single SQL query directly on the database to maximize performance. They bypass the instantiation phase, meaning individual model records are never loaded in memory. Consequently, instance-level hooks like `beforeCreate` or `beforeSave` (where password hashing is configured) are never triggered. To fix this, you must pass `{ individualHooks: true }` in the options array.

### Q4: How do you implement cursor-based pagination instead of offset pagination, and why?
* **Answer**:
  * **Why**: Offset pagination (`LIMIT 10 OFFSET 100000`) degrades database performance because the database must scan and throw away the first 100,000 records before returning the final 10. Offset pagination also suffers from "page drift" (skipping or duplicating records if items are added or deleted while paginating).
  * **How**: Cursor pagination queries records relative to the last retrieved ID:
    ```javascript
    const products = await Product.findAll({
      where: {
        id: { [Op.lt]: lastSeenId } // Uses index on PK
      },
      order: [['id', 'DESC']],
      limit: 10
    });
    ```

### Q5: How do you handle concurrent edits on the same bank account balance to prevent double-spending?
* **Answer**: Use **Pessimistic Locking** inside a transaction to lock the balance row:
  ```javascript
  await sequelize.transaction(async (transaction) => {
    const account = await Account.findByPk(accountId, {
      transaction,
      lock: transaction.LOCK.UPDATE // Locks row until commit
    });
    account.balance += amount;
    await account.save({ transaction });
  });
  ```
  This forces concurrent requests attempting to read/update the same row to wait in a queue, preventing race conditions.

### Q6: Can you explain the difference between `validation` and `constraints` and which runs first?
* **Answer**: `validation` is a JavaScript-level check running in Node.js memory. `constraints` are SQL-level rules checked by the RDBMS engine. Validations run first. If validation fails, Sequelize stops the execution and never sends the SQL query to the database, saving network and database resources.

### Q7: If you define a `defaultScope` that filters out inactive posts, how do you query inactive posts for an admin panel?
* **Answer**: Use the static `.unscoped()` method to bypass all scopes:
  ```javascript
  const allPosts = await Post.unscoped().findAll();
  ```

### Q8: What does `{ raw: true, nest: true }` do when querying associations?
* **Answer**: By default, eager loading returns a nested array of hydrated model instances, which has a performance overhead. `{ raw: true }` flats query keys (e.g. `"comments.content"`). Adding `nest: true` formats these flat keys back into nested JSON objects (e.g. `{ comments: { content: '...' } }`) as plain JavaScript objects, skipping the performance cost of model hydration.

### Q9: Why is editing an already executed migration file dangerous, and what is the correct approach to edit a column schema?
* **Answer**: If you edit a migration file that has already run in development, Sequelize will not execute it again on staging or production servers because the filename is already stamped inside the `SequelizeMeta` table. This creates database drift between servers. The correct approach is to generate a new migration file (e.g., `npx sequelize-cli migration:generate --name modify-users-email`) that applies the specific schema modifications.

### Q10: How do you perform database transactions across multiple microservices?
* **Answer**: Standard database transactions (ACID) only work on a single database. For microservices, you must implement the **Saga Pattern**: breaking the operation into a series of local database transactions. Each step executes its own write, and if a subsequent step fails, you must execute "compensating transactions" (rollback actions) manually across the preceding microservices to restore consistency.

### Q11: What is the risk of utilizing `sync({ alter: true })` in production, and why should migrations be preferred?
* **Answer**: `sync({ alter: true })` runs dynamic checks and attempts to alter columns programmatically. If a column contains data that conflicts with new constraints (e.g. turning a field to NOT NULL when empty cells exist), the query fails, leaving the database partially altered and locked. Migrations are controlled, version-controlled scripts that can be tested locally, verified in PR reviews, and safely rolled back.

### Q12: How do you optimize Sequelize performance when bulk inserting 50,000 records?
* **Answer**: Do not run loops calling `Model.create()`, as it executes 50,000 individual SQL insert statements. Use the bulk helper:
  ```javascript
  await User.bulkCreate(largeUserArray, { 
    validate: false,  // Skip validation checks to boost speed
    hooks: false      // Disable hooks to prevent execution overhead
  });
  ```
  This combines the records into a single optimized multi-value INSERT statement.

### Q13: How does Sequelize handle database read-replicas?
* **Answer**: Sequelize supports read/write replication out of the box in connection configurations:
  ```javascript
  const sequelize = new Sequelize('db', 'user', 'pass', {
    replication: {
      write: { host: 'master-db-endpoint' },
      read: [{ host: 'replica-db-1' }, { host: 'replica-db-2' }]
    }
  });
  ```
  Sequelize automatically routes write operations (like `create`, `update`, `destroy`) to the master database, and load-balances read operations (like `findAll`, `findOne`) across the replica array.

### Q14: How do you write a custom validator that checks database values (e.g., checking if a code exists in another table)?
* **Answer**: You write an asynchronous custom validation function:
  ```javascript
  validate: {
    async checkCodeExists(value) {
      const match = await Coupon.findOne({ where: { code: value } });
      if (!match) {
        throw new Error('This coupon code is invalid.');
      }
    }
  }
  ```

### Q15: How do you prevent SQL Injection attacks when writing raw SQL queries in Sequelize?
* **Answer**: Never concatenate user inputs directly into query strings (e.g. do not write `... WHERE id = ` + req.query.id). Always use bind parameters or replacement options:
  ```javascript
  await sequelize.query(
    'SELECT * FROM users WHERE id = :userId',
    {
      replacements: { userId: req.query.id },
      type: QueryTypes.SELECT
    }
  );
  ```

---

## 🔄 Flow Diagram

### Clean-Architecture Request Lifecycle

```text
 Client Request
       │
       ▼
┌──────────────┐
│ Express Route│  --> Path mapping (e.g. /users/register)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Controller  │  --> Parses req.body, validates inputs, forwards parameters
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Service    │  --> Runs business checks, manages database transactions
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Repository  │  --> Wraps database logic, executes Sequelize Model methods
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Sequelize   │  --> Compiles queries to SQL, validates schemas, executes on DB
└──────────────┘
```

---

## 📝 Quick Recap
* Organize professional applications using the Controller -> Service -> Repository design pattern.
* Bulk queries (like `update` and `bulkCreate`) bypass instance hooks unless configured with individual hooks.
* Always use Pessimistic locking (`LOCK.UPDATE`) inside transactions to handle concurrent financial writes safely.
* SQLite in local environments behaves differently than MySQL in production; always use matching database drivers during testing.

---

## 🔗 Navigation
Previous : [14_error_handling_and_production_practices.md](./14_error_handling_and_production_practices.md) | Index : [00_index.md](./00_index.md) | Next : [00_index.md](./00_index.md)
