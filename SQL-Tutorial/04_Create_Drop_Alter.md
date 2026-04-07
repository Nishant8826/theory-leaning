# Create, Drop & Alter

> 📌 **File:** `04_Create_Drop_Alter.md` | **Level:** Beginner → MERN Developer

---

## What is it?

**CREATE**, **DROP**, and **ALTER** are DDL (Data Definition Language) commands that define and modify the structure of your database and tables. They're the SQL equivalent of defining Mongoose schemas and modifying them over time.

- **CREATE** — Build new databases, tables, indexes (like writing a Mongoose schema)
- **DROP** — Delete databases, tables permanently (like `db.collection.drop()`)
- **ALTER** — Modify existing tables: add/remove/change columns (like changing your Mongoose schema and redeploying)

---

## MERN Parallel — You Already Know This!

| Mongoose / MongoDB (You Know)                    | MySQL DDL (You'll Learn)                        |
|--------------------------------------------------|-------------------------------------------------|
| `new mongoose.Schema({ name: String })`          | `CREATE TABLE users (name VARCHAR(100))`        |
| `mongoose.model('User', schema)`                 | Table is ready after CREATE                     |
| `db.collection.drop()`                           | `DROP TABLE users;`                             |
| `db.dropDatabase()`                              | `DROP DATABASE ecommerce;`                      |
| Edit schema file + redeploy                      | `ALTER TABLE users ADD COLUMN age INT;`         |
| `schema.index({ email: 1 }, { unique: true })`  | `ALTER TABLE users ADD UNIQUE (email);`         |
| `required: true` in schema                       | `NOT NULL` constraint                           |
| `default: 0` in schema                           | `DEFAULT 0` in column definition                |
| Schema middleware (pre/post)                      | Happens at table level (triggers)               |

### The Key Difference
In MongoDB, changing a schema means editing a file and redeploying your Node.js app. Existing documents are unaffected — they keep their old structure. In MySQL, **ALTER TABLE actually modifies the table in the database**. Every existing row is updated to match the new structure.

---

## Why does it matter?

- Every SQL application starts with CREATE TABLE
- Schema changes in production (ALTER) can lock tables and cause downtime if done wrong
- Dropping the wrong table or database is irreversible (no undo, no recycle bin)
- Understanding these commands is essential for database migrations
- Job interviews test your ability to modify database structures

---

## How does it work?

```
CREATE → Build the structure
           │
           ▼
     Table exists with columns,
     types, and constraints
           │
           ▼
ALTER → Modify the structure
   ├── ADD COLUMN
   ├── DROP COLUMN
   ├── MODIFY COLUMN (change type)
   ├── RENAME COLUMN
   ├── ADD CONSTRAINT
   └── ADD INDEX
           │
           ▼
DROP → Destroy the structure
     (permanent, no recovery)
```

---

## Visual Diagram

### ALTER TABLE Operations

```
Original Table: customers
┌────┬────────┬──────────────┐
│ id │ name   │ email        │
├────┼────────┼──────────────┤
│ 1  │Nishant │ n@test.com   │
│ 2  │ Priya  │ p@test.com   │
└────┴────────┴──────────────┘

After: ALTER TABLE customers ADD COLUMN phone VARCHAR(15);
┌────┬────────┬──────────────┬─────────┐
│ id │ name   │ email        │ phone   │
├────┼────────┼──────────────┼─────────┤
│ 1  │Nishant │ n@test.com   │ NULL    │  ← Existing rows get NULL
│ 2  │ Priya  │ p@test.com   │ NULL    │  ← for the new column
└────┴────────┴──────────────┴─────────┘

After: ALTER TABLE customers DROP COLUMN phone;
┌────┬────────┬──────────────┐
│ id │ name   │ email        │  ← Back to original
├────┼────────┼──────────────┤  ← phone column & data GONE
│ 1  │Nishant │ n@test.com   │
│ 2  │ Priya  │ p@test.com   │
└────┴────────┴──────────────┘

After: ALTER TABLE customers MODIFY COLUMN name VARCHAR(200);
┌────┬────────┬──────────────┐
│ id │ name   │ email        │  ← Same data, but name column
├────┼────────┼──────────────┤  ← now allows up to 200 chars
│ 1  │Nishant │ n@test.com   │  ← (was VARCHAR(100))
│ 2  │ Priya  │ p@test.com   │
└────┴────────┴──────────────┘
```

---

## Syntax

```sql
-- ============================================
-- CREATE DATABASE
-- ============================================
CREATE DATABASE ecommerce;
CREATE DATABASE IF NOT EXISTS ecommerce
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- ============================================
-- CREATE TABLE (Full Example)
-- ============================================
CREATE TABLE IF NOT EXISTS products (
  -- Primary Key (auto-incrementing ID)
  id INT AUTO_INCREMENT PRIMARY KEY,
  
  -- Regular columns with constraints
  name VARCHAR(200) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
  stock INT UNSIGNED DEFAULT 0,
  
  -- Foreign key reference
  category_id INT,
  
  -- Enum type
  status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
  
  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  -- Constraints at table level
  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
  INDEX idx_price (price),          -- Create index for faster price queries
  INDEX idx_status (status)         -- Create index for status filtering
);


-- ============================================
-- DROP (Delete permanently)
-- ============================================
DROP TABLE products;                -- Error if doesn't exist
DROP TABLE IF EXISTS products;      -- Safe delete
DROP DATABASE ecommerce;
DROP DATABASE IF EXISTS ecommerce;


-- ============================================
-- TRUNCATE (Delete all rows, keep structure)
-- ============================================
TRUNCATE TABLE products;  -- Faster than DELETE FROM products


-- ============================================
-- ALTER TABLE — Add Columns
-- ============================================
ALTER TABLE customers ADD COLUMN phone VARCHAR(15);
ALTER TABLE customers ADD COLUMN age INT AFTER name;       -- Add after specific column
ALTER TABLE customers ADD COLUMN prefix VARCHAR(5) FIRST;  -- Add as first column

-- Add multiple columns at once
ALTER TABLE customers
  ADD COLUMN city VARCHAR(100),
  ADD COLUMN state VARCHAR(50),
  ADD COLUMN pincode CHAR(6);


-- ============================================
-- ALTER TABLE — Modify Columns
-- ============================================
-- Change data type
ALTER TABLE customers MODIFY COLUMN name VARCHAR(200);

-- Change data type + constraints
ALTER TABLE customers MODIFY COLUMN email VARCHAR(255) NOT NULL UNIQUE;

-- Rename column (MySQL 8.0+)
ALTER TABLE customers RENAME COLUMN phone TO mobile_number;

-- Change column definition completely
ALTER TABLE customers CHANGE COLUMN old_name new_name VARCHAR(200) NOT NULL;


-- ============================================
-- ALTER TABLE — Drop Columns
-- ============================================
ALTER TABLE customers DROP COLUMN age;

-- Drop multiple columns
ALTER TABLE customers
  DROP COLUMN city,
  DROP COLUMN state;


-- ============================================
-- ALTER TABLE — Constraints
-- ============================================
-- Add unique constraint
ALTER TABLE customers ADD UNIQUE (email);

-- Add foreign key
ALTER TABLE orders ADD FOREIGN KEY (customer_id) REFERENCES customers(id);

-- Drop foreign key (need constraint name)
ALTER TABLE orders DROP FOREIGN KEY orders_ibfk_1;

-- Add/Drop index
ALTER TABLE products ADD INDEX idx_name (name);
ALTER TABLE products DROP INDEX idx_name;


-- ============================================
-- ALTER TABLE — Rename Table
-- ============================================
ALTER TABLE customers RENAME TO clients;
-- or
RENAME TABLE customers TO clients;
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Mongoose (What You Know) ==========

// "Creating a table" = Defining a schema + model
const customerSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true }
});
const Customer = mongoose.model('Customer', customerSchema);

// "Altering a table" = Just edit the schema file and redeploy
// Old documents keep old structure — MongoDB doesn't care!
customerSchema.add({ phone: String }); // Add field

// "Dropping a table" 
await mongoose.connection.dropCollection('customers');
```

```sql
-- ========== MySQL (What You'll Use) ==========

-- Creating a table
CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL
);

-- Altering — ACTUALLY changes the table
ALTER TABLE customers ADD COLUMN phone VARCHAR(15);

-- Dropping — permanent deletion
DROP TABLE customers;
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Create table
async function createCustomersTable() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS customers (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      email VARCHAR(150) UNIQUE NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);
  console.log('✅ Customers table created');
}

// Alter table — add column
async function addPhoneColumn() {
  try {
    await pool.query('ALTER TABLE customers ADD COLUMN phone VARCHAR(15)');
    console.log('✅ Phone column added');
  } catch (error) {
    if (error.code === 'ER_DUP_FIELDNAME') {
      console.log('ℹ️ Phone column already exists');
    } else {
      throw error;
    }
  }
}

// Drop table (with confirmation — good practice)
async function dropTable(tableName) {
  await pool.query(`DROP TABLE IF EXISTS ${tableName}`);
  console.log(`✅ Table ${tableName} dropped`);
}

// Get table structure (like viewing your Mongoose schema)
async function describeTable(tableName) {
  const [columns] = await pool.query(`DESCRIBE ${tableName}`);
  console.table(columns);
  return columns;
}
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize ==========
const { DataTypes } = require('sequelize');

// CREATE TABLE → Define model
const Customer = sequelize.define('Customer', {
  name: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  email: {
    type: DataTypes.STRING(150),
    allowNull: false,
    unique: true
  }
}, { tableName: 'customers' });

// sync() → CREATE TABLE IF NOT EXISTS
await Customer.sync();

// sync({ force: true }) → DROP TABLE + CREATE TABLE
await Customer.sync({ force: true });  // ⚠️ Destroys all data!

// sync({ alter: true }) → ALTER TABLE (adds/modifies columns to match model)
await Customer.sync({ alter: true });   // ⚠️ Safer but can still lose data

// Migrations (proper way — like version control for schema)
// Using sequelize-cli:
// npx sequelize-cli migration:generate --name add-phone-to-customers
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('customers', 'phone', {
      type: Sequelize.STRING(15),
      allowNull: true
    });
  },
  down: async (queryInterface) => {
    await queryInterface.removeColumn('customers', 'phone');
  }
};
```

### Sequelize Migrations vs Raw ALTER TABLE

| Sequelize Migrations                | Raw ALTER TABLE                    |
|-------------------------------------|------------------------------------|
| Version-controlled (git trackable)  | One-off commands                   |
| Can rollback (`down` function)      | No built-in rollback               |
| Team-friendly (everyone runs same)  | Must communicate manually          |
| `npx sequelize-cli db:migrate`      | Run SQL in Workbench or script     |

---

## Real-World Scenario + Full Stack Code

### Scenario: Your e-commerce app needs to add a `loyalty_points` column to existing customers table

```sql
-- Step 1: Check current structure
DESCRIBE customers;

-- Step 2: Add loyalty_points column with default 0
ALTER TABLE customers ADD COLUMN loyalty_points INT UNSIGNED DEFAULT 0 AFTER email;

-- Step 3: Verify the change
DESCRIBE customers;

-- Step 4: Update existing customers with initial points
UPDATE customers SET loyalty_points = 100;  -- All existing customers get 100 points
```

```js
// Node.js — Migration script
const pool = require('./db');

async function addLoyaltyPoints() {
  try {
    // Check if column already exists
    const [columns] = await pool.query('DESCRIBE customers');
    const hasColumn = columns.some(col => col.Field === 'loyalty_points');
    
    if (hasColumn) {
      console.log('ℹ️ loyalty_points column already exists');
      return;
    }
    
    // Add the column
    await pool.query(`
      ALTER TABLE customers 
      ADD COLUMN loyalty_points INT UNSIGNED DEFAULT 0 AFTER email
    `);
    console.log('✅ loyalty_points column added');
    
    // Give existing customers 100 points
    const [result] = await pool.query(
      'UPDATE customers SET loyalty_points = 100'
    );
    console.log(`✅ Updated ${result.affectedRows} customers with 100 points`);
    
  } catch (error) {
    console.error('❌ Migration failed:', error.message);
  }
}

addLoyaltyPoints();
```

```js
// Express API — Update loyalty points
app.patch('/api/customers/:id/loyalty', async (req, res) => {
  try {
    const { points } = req.body;
    const [result] = await pool.query(
      'UPDATE customers SET loyalty_points = loyalty_points + ? WHERE id = ?',
      [points, req.params.id]
    );
    
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: 'Customer not found' });
    }
    
    // Get updated customer
    const [rows] = await pool.query(
      'SELECT id, name, loyalty_points FROM customers WHERE id = ?',
      [req.params.id]
    );
    
    res.json(rows[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

```js
// React — Display and update loyalty points
import { useState, useEffect } from 'react';
import axios from 'axios';

function LoyaltyDashboard({ customerId }) {
  const [customer, setCustomer] = useState(null);
  const [points, setPoints] = useState(0);

  useEffect(() => {
    axios.get(`/api/customers/${customerId}`)
      .then(({ data }) => setCustomer(data));
  }, [customerId]);

  const addPoints = async () => {
    const { data } = await axios.patch(`/api/customers/${customerId}/loyalty`, {
      points: parseInt(points)
    });
    setCustomer(data);
    setPoints(0);
  };

  if (!customer) return <p>Loading...</p>;

  return (
    <div>
      <h2>{customer.name}</h2>
      <p>Loyalty Points: <strong>{customer.loyalty_points}</strong></p>
      <input 
        type="number" 
        value={points} 
        onChange={e => setPoints(e.target.value)}
        placeholder="Points to add"
      />
      <button onClick={addPoints}>Add Points</button>
    </div>
  );
}
```

**Output:**
```json
{
  "id": 1,
  "name": "Nishant",
  "loyalty_points": 150
}
```

---

## Impact

| If You Don't Understand This...          | What Happens                                    |
|------------------------------------------|-------------------------------------------------|
| Use DROP instead of TRUNCATE             | Lose the entire table structure, not just data   |
| ALTER TABLE on a big production table     | Table locks → app goes down for minutes/hours    |
| Forget IF NOT EXISTS on CREATE           | Script crashes on second run                     |
| Don't plan schema before CREATE          | Endless ALTER TABLE migrations                   |
| Drop a column without checking data      | Permanently lose that data (no undo!)            |
| Forget foreign key ON DELETE behavior     | Orphaned rows or cascade deletions               |

### Production Warning: ALTER TABLE Locks

```
Small Table (< 1M rows):
ALTER TABLE → instant, no issue

Big Table (10M+ rows):
ALTER TABLE → MySQL COPIES the entire table!
             → Table is LOCKED during copy
             → All reads/writes BLOCKED
             → Could take minutes or hours

Solutions:
1. Use pt-online-schema-change (Percona tool)
2. Use gh-ost (GitHub's tool)
3. Schedule during low-traffic periods
4. MySQL 8.0+ has INSTANT ALTER for some operations
```

---

## Practice Exercises

### Easy (SQL)
1. Create a table `employees` with columns: id, name, department, salary, hire_date
2. Add a column `email` to the employees table
3. Rename the `salary` column to `monthly_salary`
4. Drop the employees table safely

### Medium (SQL + Node.js)
5. Write a Node.js migration script that:
   - Creates all 5 e-commerce tables if they don't exist
   - Checks `DESCRIBE` before running each CREATE
   - Logs the result of each operation
6. Write an Express route that accepts a table name and returns its column structure
7. Write a migration that adds `updated_at` column to all tables that don't have it

### Hard (Full Stack)
8. Build a database migration system:
   - Each migration is a numbered SQL file: `001_create_users.sql`, `002_add_phone.sql`
   - Track applied migrations in a `migrations` table
   - Express route: `POST /api/migrate` runs all pending migrations
   - React UI shows migration status and has "Run Migrations" button
9. Create a "Schema Designer" React app:
   - Form to create new tables (specify columns, types, constraints)
   - Calls Express API which runs `CREATE TABLE`
   - Displays current schema for all tables
   - Supports adding/dropping columns via ALTER TABLE

---

## Real-World Q&A

**Q1:** In MongoDB, I never worry about schema changes. Why is ALTER TABLE such a big deal in MySQL?
**A:** Because ALTER TABLE physically restructures the data on disk. If your table has 50 million rows, MySQL has to read every row, apply the change, and write it back. During this time, the table is locked. This is why production schema changes are planned carefully, often using tools like `pt-online-schema-change` that do it gradually without locking.

**Q2:** What happens if I DROP a FOREIGN KEY referenced by another table?
**A:** You'll get an error: `Cannot drop table 'categories' referenced by a foreign key constraint`. You must drop the dependent table first (or the foreign key constraint). This is actually a safety feature — it prevents you from accidentally breaking relationships.

**Q3:** Can I undo a DROP TABLE?
**A:** No. There is no `UNDO` in SQL. Once you DROP a table, it's gone forever unless you have a backup. This is why you should ALWAYS have database backups. In production, use `DROP TABLE IF EXISTS` and test in a staging environment first.

---

## Interview Q&A

**Q1: What is DDL? Give examples.**
DDL (Data Definition Language) includes commands that define or modify database structure: CREATE (creates databases, tables, indexes), ALTER (modifies existing tables), DROP (deletes tables/databases), TRUNCATE (removes all rows). DDL commands auto-commit — they cannot be rolled back.

**Q2: What is the difference between DROP, TRUNCATE, and DELETE?**
DROP removes the table completely (structure + data). TRUNCATE removes all rows but keeps the table structure; it resets AUTO_INCREMENT and is faster because it deallocates pages without logging individual row deletions. DELETE removes specific rows (with WHERE) or all rows; it's logged, can be rolled back, and doesn't reset AUTO_INCREMENT.

**Q3: What are constraints in MySQL? Name the types.**
Constraints are rules enforced on columns: NOT NULL (must have a value), UNIQUE (no duplicates), PRIMARY KEY (NOT NULL + UNIQUE, identifies each row), FOREIGN KEY (links to another table), CHECK (validates values, e.g., price >= 0), DEFAULT (sets default value). In Mongoose, these are like `required`, `unique`, `ref`, `validate`, and `default`.

**Q4: How does ON DELETE CASCADE work with FOREIGN KEYS?**
When you define a foreign key with `ON DELETE CASCADE`, deleting a row in the parent table automatically deletes all related rows in the child table. Example: `FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE` — deleting a customer also deletes all their orders. Other options: SET NULL (sets FK to NULL), RESTRICT (prevents deletion), NO ACTION (same as RESTRICT).

**Q5: In production, a table with 100 million rows needs a new column. How would you approach this?**
Direct ALTER TABLE would lock the table for a long time. Solutions: (1) Use MySQL 8.0+ INSTANT algorithm: `ALTER TABLE t ADD COLUMN col INT, ALGORITHM=INSTANT` for operations that support it. (2) Use pt-online-schema-change or gh-ost — these create a shadow table, copy data gradually, then swap. (3) Add with a default migration window during low traffic. (4) Consider blue-green deployment: add column to replica, swap primary. Always test on a staging environment first.

---

| [← Previous: Data Types](./03_Data_Types.md) | [Next: Insert, Update & Delete →](./05_Insert_Update_Delete.md) |
|---|---|
