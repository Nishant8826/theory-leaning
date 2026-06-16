# MongoDB

MongoDB is the most popular NoSQL database in the Node.js ecosystem. While ODMs like Mongoose are widely used, they add layer overhead. Understanding how to use the native MongoDB driver allows you to write high-performance database queries, manage connection pools directly, and design optimal indexes to prevent slow queries in production.

### NoSQL Documents vs. Relational Tables
* **Relational Databases (e.g. PostgreSQL)**: Store data in rigid, tabular rows and columns. They require pre-defined schemas and use foreign keys to join tables together.
* **Document Databases (e.g. MongoDB)**: Store data in flexible, semi-structured documents. Related data is often embedded inside a single document (nested arrays and objects) instead of being split across tables, reducing the need for join queries.

### JSON and BSON
MongoDB represents documents using JSON-like structures. Internally, however, MongoDB stores data in **BSON (Binary JSON)** format:
* **JSON**: A text-based format supporting limited data types (strings, numbers, booleans, null, arrays, objects).
* **BSON**: A binary serialization format that extends JSON to support additional data types (like `Date`, `ObjectId`, `Decimal128`, and raw binary buffers). BSON is optimized for space efficiency and fast parsing speed.

## Deep Dive

### Connection Pooling
Opening and closing database connections for every request adds network and CPU latency. The native MongoDB driver automatically manages a **Connection Pool**.
* When you call `MongoClient.connect()`, the driver opens a pool of persistent TCP connections (defaulting to 100 connections).
* When a query is executed, the driver borrows an active connection from the pool, runs the query, and returns the connection to the pool.
* You should initialize the `MongoClient` once during application startup and reuse the client instance across all files.

### Write Concerns
**Write Concern** controls how MongoDB confirms write operations:
* **`w: 1`** (Default): The database confirms the write as soon as it is written to the primary node's memory.
* **`w: majority`**: The database confirms the write only after it has been replicated to a majority of the replica set nodes. This provides high data durability but increases write latency.

## Visual Explanation

### Connection Pool Lifecycle
```text
  [ Express App Bootstrap ] ── Instantiates ──> [ MongoClient ]
                                                       │
                                                       ▼ (Opens TCP Connections)
+---------------------------------------------------------------------------------+
| [ Connection Pool ]                                                             |
|   ├── Connection 1  <── Active (Processing User A query)                        |
|   ├── Connection 2  <── Idle (Waiting in pool)                                  |
|   └── Connection 3  <── Idle (Waiting in pool)                                  |
+---------------------------------------------------------------------------------+
                                                       ▲
                                                       │ (Borrow & Return)
  [ HTTP Request Client ] ─── Triggers ───> [ runDatabaseQuery() ]
```

## Real-World Example
Consider building a real-time analytics engine. You need to write thousands of log metrics per second. Using the native MongoDB driver, you configure a connection pool of 50 connections and set write concern to `w: 1` to keep write operations fast. This allows the application to handle high-throughput log ingestion without blocking the event loop.

## Code Examples

### Native MongoDB Driver Setup, CRUD, and Index Configuration

```javascript
// db/mongoClient.js
// Dependency required: npm install mongodb
const { MongoClient } = require('mongodb');

const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017';
const DB_NAME = process.env.DB_NAME || 'mastery_db';

let dbInstance = null;
let clientInstance = null;

async function connectToDatabase() {
  if (dbInstance) return dbInstance;

  try {
    // 1. Initialize MongoClient with pool configurations
    clientInstance = new MongoClient(MONGO_URI, {
      maxPoolSize: 50,      // Max concurrent socket connections in the pool
      minPoolSize: 10,      // Keep at least 10 sockets open
      connectTimeoutMS: 5000 // Timeout after 5 seconds during startup
    });

    await clientInstance.connect();
    console.log('Successfully connected to MongoDB server.');
    
    dbInstance = clientInstance.db(DB_NAME);
    return dbInstance;
  } catch (err) {
    console.error('Failed to establish MongoDB connection:', err.message);
    process.exit(1);
  }
}

function getDb() {
  if (!dbInstance) {
    throw new Error('Database connection has not been initialized.');
  }
  return dbInstance;
}

module.exports = { connectToDatabase, getDb, clientInstance };
```

```javascript
// crud-operations.js
const { connectToDatabase, getDb } = require('./db/mongoClient');

async function executeCrudDemo() {
  // Initialize connection
  await connectToDatabase();
  const db = getDb();
  
  const usersCollection = db.collection('users');

  // 1. Optimize collections using Indexes
  // Create an index on the 'email' field to ensure fast lookups
  await usersCollection.createIndex({ email: 1 }, { unique: true });
  console.log('Index successfully created on "email" field.');

  try {
    // 2. CREATE (Insert Document)
    const newUser = {
      name: 'Charlie',
      email: 'charlie@db.com',
      createdAt: new Date(),
      metadata: { loginCount: 1 }
    };
    const insertResult = await usersCollection.insertOne(newUser);
    console.log('Document inserted. ID:', insertResult.insertedId);

    // 3. READ (Find Document)
    const user = await usersCollection.findOne({ email: 'charlie@db.com' });
    console.log('Found user document:', user);

    // 4. UPDATE (Modify Document)
    const updateResult = await usersCollection.updateOne(
      { email: 'charlie@db.com' },
      {
        $inc: { 'metadata.loginCount': 1 }, // Increment nested value
        $set: { updatedAt: new Date() }
      }
    );
    console.log('Updated documents count:', updateResult.modifiedCount);

    // 5. DELETE (Remove Document)
    const deleteResult = await usersCollection.deleteOne({ email: 'charlie@db.com' });
    console.log('Deleted documents count:', deleteResult.deletedCount);

  } catch (err) {
    console.error('Error during CRUD operations:', err.message);
  }
}
executeCrudDemo();
```

## Best Practices
* **Reuse the Database Instance**: Never call `MongoClient.connect()` inside your route handlers. Initialize the client once during application startup and reuse the database instance globally.
* **Always Index Query Fields**: Identify which fields are queried frequently (e.g. emails, usernames, or status fields) and create indexes for them to prevent MongoDB from performing slow full-collection scans (`COLLSCAN`).
* **Handle Connection Drops**: Register event listeners on the `MongoClient` instance (like `'close'` or `'error'`) to handle database connection drops gracefully in production.

## Interview Questions

**Q:** What is BSON and how does it relate to JSON in MongoDB?

> **Answer:**
> BSON stands for Binary JSON. It is the binary serialization format MongoDB uses internally to store documents. BSON extends JSON by supporting additional data types (like `Date`, `ObjectId`, and raw binary buffers) and is optimized for fast parsing and space efficiency.

**Q:** Why should you use a connection pool, and how do you configure it in the native MongoDB driver?

> **Answer:**
> A connection pool maintains a set of persistent TCP connections to the database. This allows the application to reuse connections across multiple queries, eliminating the latency of opening and closing connections for each query. In the native MongoDB driver, you configure the pool size by passing `maxPoolSize` and `minPoolSize` settings in the `MongoClient` options during initialization.

**Q:** Explain the difference between a Collection Scan (COLLSCAN) and an Index Scan (IXSCAN) in MongoDB. How do you identify which one a query is using?

> **Answer:**
> A Collection Scan (COLLSCAN) occurs when MongoDB must search through every document in a collection to find a match. This is slow and CPU-intensive for large collections. An Index Scan (IXSCAN) occurs when MongoDB uses an index to locate documents quickly, similar to using an index in a textbook.
> You can identify which scan a query uses by appending `.explain('executionStats')` to your query chain. The output details the query plan and shows either `COLLSCAN` or `IXSCAN` in the winning plan stage.

**Q:** Discuss how Write Concerns (`w: 1` vs `w: majority`) and Journaling (`j: true`) impact data durability and write performance in a MongoDB Replica Set.

> **Answer:**
> 

**Q:** `w: 1`

> **Answer:**
> 

**Q:** `w: majority`

> **Answer:**
> 

**Q:** `j: true`

> **Answer:**
> For high-availability transactions, use `w: majority` and `j: true` to guarantee durability. For high-volume log ingestion where occasional data loss is acceptable, use `w: 1` and disable disk journaling confirmations to maximize write throughput.

---
Previous : [36_Sessions.md](36_Sessions.md) | Index : [00_index.md](00_index.md) | Next : [38_Mongoose.md](38_Mongoose.md)
