# 02. Sequelize Architecture and Mental Model

## 🎯 Goal of This Chapter
By the end of this chapter, you will understand the internal architecture of Sequelize. You will learn how query generation works, what connection pooling is, and how Sequelize manages database connections using the Active Record pattern.

---

## 🤔 Why This Topic Matters
Many developers treat ORMs as "black boxes" — writing code and hoping it works. When the application scales, this lack of understanding leads to critical issues like:
* **Connection Leaks**: Running out of database connections under load, causing the application to freeze.
* **Slow Queries**: Not knowing how Sequelize compiles your Javascript queries into raw SQL.
* **Memory Bloat**: Hydrating too many model instances.

Understanding the internal architecture helps you build highly performant backends and debug connection issues confidently.

---

## 🧠 Core Concept
Sequelize is organized into distinct internal layers, each handling a specific part of the database lifecycle:

```text
+-------------------------------------------------+
|               Your Application                  |
|        (Express Controllers & Services)         |
+------------------------+------------------------+
                         |
                         v
+-------------------------------------------------+
|             Models & Active Record              |
|   (User.create(), user.save(), validations)     |
+------------------------+------------------------+
                         |
                         v
+-------------------------------------------------+
|                 Query Generator                 |
|   (Converts Javascript objects to raw SQL strings) |
+------------------------+------------------------+
                         |
                         v
+-------------------------------------------------+
|                 Connection Pool                 |
| (Manages & reuses database connection sockets)  |
+------------------------+------------------------+
                         |
                         v
+-------------------------------------------------+
|                 Dialect Adapter                 |
|      (Translates SQL into pg / mysql2 format)   |
+------------------------+------------------------+
                         |
                         v
+-------------------------------------------------+
|                 Database Server                 |
+-------------------------------------------------+
```

Let's look at the key parts:
1. **Active Record Layer**: The interface you write. Every database table is mapped to a Model class, and every row in a table is mapped to a Model instance.
2. **Query Generator**: A compiler inside Sequelize. It reads your options (like `{ where: { id: 1 } }`) and outputs dialect-specific SQL strings.
3. **Connection Pool**: A manager that keeps a specific number of database connections open so that queries don't waste time establishing new TCP connections.
4. **Dialect Adapter**: Translates and communicates using low-level drivers (`pg` for Postgres, `mysql2` for MySQL, etc.).

---

## 🏗 Mental Model / Internal Working

### 1. The Lifecycle of a Query
When you call `User.findAll({ where: { role: 'admin' } })`:
1. **Model Validation**: Sequelize checks if the attributes in the query match the model's defined columns.
2. **SQL Compilation**: The Query Generator compiles the inputs into `SELECT id, username, role FROM users WHERE role = $1;`.
3. **Connection Leasing**: The query engine asks the **Connection Pool** for an available open socket connection.
4. **Driver Execution**: The connection executes the query on the database.
5. **Hydration**: The database returns raw binary rows. Sequelize parses these rows, initializes a new `User` class instance for each row, binds helper methods (like `.update()`, `.save()`), and returns the array of instances.

### 2. Connection Pooling
Creating a connection to a database is expensive because it requires a network handshake (TCP + SSL/TLS).
* Without pooling: Each query creates a connection, executes, and closes it. This is very slow and can crash the database due to connection limits.
* With pooling: Sequelize keeps a group of active, open connections. A query leases a connection, uses it for a fraction of a millisecond, and immediately returns it to the pool.

---

## 🌍 Real-World Analogy
Think of a **Taxi Dispatch Service** (Connection Pool).
* The **Taxis** are database connection sockets.
* The **Passengers** are queries waiting to run.
* Instead of building a brand-new taxi from scratch (establishing a new connection socket) every time a passenger calls, and destroying the taxi after the ride, the dispatch office keeps 10 taxis parked in a garage (the pool).
* When a passenger calls (query runs), they hop into an idle taxi, get driven to the database destination, and the taxi drives back to the garage to wait for the next passenger.

---

## ⚙️ Syntax / API / Core Usage

### Configuring Connection Pooling
You configure the connection pool inside the main Sequelize initialization settings.

```javascript
const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('my_database', 'user', 'password', {
  host: 'localhost',
  dialect: 'mysql',
  
  // Connection Pool configuration
  pool: {
    max: 10,       // Maximum number of active connections in the pool
    min: 0,        // Minimum number of connections to keep open when idle
    acquire: 30000, // Maximum time (ms) Sequelize will try to get connection before throwing error
    idle: 10000    // Time (ms) a connection can remain idle before being released
  }
});
```

---

## 💻 Practical Examples

### Understanding Active Record Instances
Let's see how Active Record objects work in code.

```javascript
// db/sequelize.js setup
const { Sequelize, DataTypes, Model } = require('sequelize');
const sequelize = new Sequelize('sqlite::memory:'); // Using memory database for speed

class Product extends Model {}
Product.init({
  name: DataTypes.STRING,
  price: DataTypes.INTEGER
}, { sequelize, modelName: 'Product' });

async function runDemo() {
  await sequelize.sync({ force: true });

  // 1. Class Method: Creates a record in the database
  const item = await Product.create({ name: 'Laptop', price: 999 });
  
  // item is now a Model Instance (Active Record object)
  console.log(item instanceof Product); // true
  console.log(item.name); // 'Laptop'
  
  // 2. Instance Method: Modify properties and persist them directly
  item.price = 1050; 
  await item.save(); // Directly saves to DB. Under the hood, runs UPDATE query.
  
  // 3. Instance Method: Deletes the record
  await item.destroy(); // Under the hood, runs DELETE query.
}

runDemo();
```

---

## 🔄 Flow Diagram

### Connection Leasing Lifecycle
```text
                  Query is requested
                          │
                          ▼
             Is there an idle connection
                  in the pool?
                 /            \
               YES             NO
               /                 \
              v                   v
     Lease connection      Are active connections
      from the pool          less than max limit?
                                /             \
                              YES              NO
                              /                 \
                             v                   v
                     Create new socket    Wait for release 
                        connection        (Timeout: acquire ms)
                             │                      │
                             └──────────┬───────────┘
                                        │
                                        ▼
                                 Run SQL Query
                                        │
                                        ▼
                              Return connection to
                               pool for reuse
```

---

## 🧪 Common Interview Questions

### Q1: What is a Singleton connection pattern, and why is it important in Sequelize?
* **Answer**: The Singleton pattern ensures that only one instance of the `Sequelize` class is created throughout the application lifecycle. If we create new Sequelize instances inside different model files or express routing files, each instance creates its own connection pool, quickly exceeding the database's maximum allowed connection limit.

### Q2: What happens when the database connection pool is exhausted?
* **Answer**: If all connections in the pool are busy executing long-running queries, subsequent queries must wait in a queue. If a query waits longer than the `pool.acquire` timeout setting (default: 30 seconds), Sequelize throws a `ConnectionAcquireTimeoutError`.

### Q3: What is "hydration" in Sequelize?
* **Answer**: Hydration is the process where Sequelize takes the raw database rows (simple key-value JSON or arrays) and wraps them inside instances of the corresponding Sequelize Model class. This turns raw data back into active objects with built-in database methods like `.update()` or `.destroy()`.

---

## ⚠️ Common Mistakes / Pitfalls
* **Creating Multiple Instances**: Initializing `new Sequelize(...)` in multiple files instead of exporting a single instance from a configuration file.
* **Ignoring the `acquire` Timeout**: Setting a very low `acquire` time (e.g. 1000ms) on slow databases, which causes transaction queries to fail during network spikes.

---

## ✅ Best Practices
* **Share a single Sequelize Instance**: Export one `sequelize` instance from a centralized database config file (e.g., `src/config/database.js`) and import it wherever models are defined.
* **Keep `min` pool size low**: In environments that scale up and down dynamically (like containerized Express apps), keeping `pool.min` to 0 or 1 ensures that idle instances do not consume database connections unnecessarily when traffic is low.

---

## 📝 Quick Recap
* Sequelize uses the **Active Record** pattern: Models represent tables, instances represent rows, and databases are modified by calling methods on those instances.
* **Connection Pooling** avoids the overhead of opening and closing network connections for every query by keeping a pool of active connection sockets open.
* Always export a single connection instance from a database file to prevent database connection limit exhaustions.

---

## 🔗 Navigation
Previous : [01_introduction_to_orm_and_sequelize.md](./01_introduction_to_orm_and_sequelize.md) | Index : [00_index.md](./00_index.md) | Next : [03_project_setup_and_configuration.md](./03_project_setup_and_configuration.md)
