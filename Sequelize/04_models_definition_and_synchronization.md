# 04. Model Definition and Synchronization

## 🎯 Goal of This Chapter
By the end of this chapter, you will understand how to define database tables as Javascript classes (Models) in Sequelize. You will learn about various data types, constraints, and how model synchronization works using `sequelize.sync()`, along with the limits and dangers of synchronization in production.

---

## 🤔 Why This Topic Matters
Models are the blueprints of your application. Defining incorrect data types or constraints in your model definitions leads to invalid data entering your database, broken calculations, or silent query failures. 

Furthermore, Sequelize offers a quick way to create tables: `sequelize.sync()`. If a developer does not understand how `sync()` works and runs it in production with options like `{ force: true }`, **it will immediately drop all database tables and erase all production customer data**. Knowing how to safely synchronize schemas is critical.

---

## 🧠 Core Concept

### What is a Sequelize Model?
A **Model** is a class that represents a table in your database. An instance of that class represents a single row in that table.

In modern Sequelize, models are defined by extending the ES6 `Model` class and calling its static `init()` method to declare attributes (columns) and options (like indices, database connection, and table names).

### Common Attributes Options
When defining column fields, we can attach options to customize database behavior:
* `allowNull`: Set to `false` to make a column NOT NULL.
* `defaultValue`: Assigns a default fallback value if none is provided.
* `unique`: Enforces unique values (e.g., usernames or emails).
* `primaryKey`: Designates the column as the primary key.
* `autoIncrement`: Automatically increments integer values (typically used for IDs).

---

## 🏗 Mental Model / Internal Working
Model definition is a two-step process:

1. **Definition (In-Memory Configuration)**:
   When you write `User.init({ ... })`, Sequelize does **not** touch your database yet. It simply registers the metadata of your schema into its internal memory registry.
2. **Synchronization (Database Execution)**:
   When you call `sequelize.sync()` or `Model.sync()`, Sequelize translates this registered in-memory schema into raw SQL `CREATE TABLE` queries and executes them against the database.

---

## 🌍 Real-World Analogy
Think of a model definition as a **Blueprint for a House**:
* Writing the JavaScript code defining columns is like drawing lines on blueprints. The house does not exist yet.
* Running `sequelize.sync()` is like calling a **Construction Crew** to build the house according to that blueprint.
  * `sync()`: Builds the house if there is empty land. If a house is already there, it does nothing.
  * `sync({ force: true })`: **Bulldozes the existing house** (losing all furniture/data inside!) and builds a brand-new house.
  * `sync({ alter: true })`: Tries to expand/remodel the existing house while people are living in it (e.g., knocking down walls dynamically). This is risky and might cause structural collapse if the layout changes are too complex.

---

## ⚙️ Syntax / API / Core Usage

### Defining a Model
Here is the modern class syntax to define a model:

```javascript
const { Model, DataTypes } = require('sequelize');
const sequelize = require('../config/database'); // Single shared instance

class User extends Model {}

User.init({
  // Column definitions
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  username: {
    type: DataTypes.STRING(50), // limits VARCHAR length to 50
    allowNull: false,
    unique: true
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false
  },
  role: {
    type: DataTypes.ENUM('admin', 'user', 'manager'),
    defaultValue: 'user'
  },
  isActive: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  }
}, {
  sequelize,          // Pass the database connection instance
  modelName: 'User',  // The model name (used in associations)
  tableName: 'users', // Explicit table name in the DB
  timestamps: true,   // Auto adds 'createdAt' and 'updatedAt' fields
});

module.exports = User;
```

---

## 💻 Practical Examples

### Schema Synchronization Modes
Let's see how the three synchronization options behave when executed in a script.

```javascript
// sync-demo.js
const sequelize = require('./config/database');
const User = require('./models/User');

async function syncDatabase() {
  try {
    // ----------------------------------------------------
    // Option 1: Standard Sync
    // Checks if table exists. If no, runs CREATE TABLE.
    // If yes, does nothing. Safe for dev, but won't update columns.
    // ----------------------------------------------------
    await sequelize.sync();
    console.log('Database synced successfully (Default).');

    // ----------------------------------------------------
    // Option 2: Force Sync (DANGEROUS)
    // Runs DROP TABLE IF EXISTS users; followed by CREATE TABLE users;
    // Useful in local development/testing to get a clean state.
    // ----------------------------------------------------
    // await sequelize.sync({ force: true });
    // console.log('Database synced with force: true (Dropped tables!).');

    // ----------------------------------------------------
    // Option 3: Alter Sync (USE WITH CAUTION)
    // Compares model attributes with DB columns.
    // Generates ALTER TABLE commands to add/remove fields.
    // ----------------------------------------------------
    // await sequelize.sync({ alter: true });
    // console.log('Database columns altered to match models.');

  } catch (error) {
    console.error('Failed to sync database:', error);
  } finally {
    await sequelize.close();
  }
}

syncDatabase();
```

---

## 🔄 Flow Diagram

### Synchronization Mechanics

```text
                  Model.sync() is called
                            │
                            ▼
              Does table exist in database?
                     /             \
                   YES              NO
                   /                 \
                  v                   v
      Options check:              Execute SQL:
      - force? ──────────> YES ──> DROP TABLE IF EXISTS
      - alter? ──> YES             CREATE TABLE
      - None   ──> Do nothing         
                     │
                     v
            Alter check (alter: true)
            - Compare DB schema metadata
            - Generate ALTER TABLE queries
            - Run migrations
```

---

## 🧪 Common Interview Questions

### Q1: What is the difference between `force: true` and `alter: true`?
* **Answer**: 
  * `force: true` runs a destructive SQL query `DROP TABLE IF EXISTS` and then recreates the table. All data in that table is permanently deleted.
  * `alter: true` attempts to update the existing table schema. It reads the current columns and executes `ALTER TABLE` statements to match the new model definitions without deleting the current rows, though it can still fail if data conflicts arise (e.g. changing a column from nullable to not-null when empty cells exist).

### Q2: Why is running `sequelize.sync()` discouraged in production environments?
* **Answer**: 
  1. **Data Loss Risk**: Accidentally calling `sync({ force: true })` wipes out production databases.
  2. **Lack of Version Control**: Sync does not leave a history log of schema changes. It is impossible to rollback schema updates safely if a deployment fails.
  3. **Locks and Downtime**: On large tables, running auto-alter checks can block databases, locking write access for tables and crashing live applications.

### Q3: What fields are automatically created if `timestamps: true` is configured?
* **Answer**: Sequelize automatically appends two datetime fields: `createdAt` (populated when a record is created) and `updatedAt` (automatically updated whenever an instance property is changed and saved).

---

## ⚠️ Common Mistakes / Pitfalls
* **Accidental `force: true` in Production**: Having `sequelize.sync({ force: true })` in your startup code block without setting environmental guards.
* **Mismatched Pluralization**: Sequelize automatically pluralizes model names to generate table names (e.g., model `User` maps to table `Users`). If you define queries on singular table names manually, your SQL will break unless you explicitly define `tableName: 'users'` in model options.

---

## ✅ Best Practices
* **Use Environment Guards**: Lock synchronization behind development-only conditional blocks in your initialization code:
  ```javascript
  if (process.env.NODE_ENV === 'development') {
    // Only allow sync in local development
    sequelize.sync({ alter: true });
  }
  ```
* **Explicit table names**: Always define the `tableName` key inside your model configuration to prevent Sequelize from automatically guessing and naming tables using default English plural rules.

---

## 📝 Quick Recap
* Sequelize models are defined as JavaScript classes extending the `Model` superclass.
* `DataTypes` map Javascript primitive types to specific database-supported formats (VARCHAR, INT, UUID, ENUM, etc.).
* `sequelize.sync()` maps defined models to SQL tables. 
* Never run `sync({ force: true })` in production, as it deletes tables before recreating them. Use database migrations for production environments instead.

---

## 🔗 Navigation
Previous : [03_project_setup_and_configuration.md](./03_project_setup_and_configuration.md) | Index : [00_index.md](./00_index.md) | Next : [05_migrations_and_seeders_in_depth.md](./05_migrations_and_seeders_in_depth.md)
