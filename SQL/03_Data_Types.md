# Data Types

> 📌 **File:** `03_Data_Types.md` | **Level:** Beginner → MERN Developer

---

## What is it?

Data types in MySQL define exactly what kind of data a column can hold — numbers, text, dates, etc. In MongoDB/Mongoose, you specify types like `String`, `Number`, `Date` in your schema. MySQL does the same thing but with much more granularity.

In Mongoose, `Number` covers everything. In MySQL, you choose between `TINYINT`, `SMALLINT`, `INT`, `BIGINT`, `FLOAT`, `DOUBLE`, `DECIMAL` — each with different storage sizes and precision. This precision is how MySQL keeps data small and fast.

---

## MERN Parallel — You Already Know This!

| Mongoose Type        | MySQL Type(s)                    | Notes                           |
|----------------------|----------------------------------|---------------------------------|
| `String`             | `VARCHAR(n)`, `TEXT`, `CHAR(n)` | Must specify max length for VARCHAR |
| `Number` (integer)   | `INT`, `SMALLINT`, `BIGINT`     | Choose based on range needed    |
| `Number` (decimal)   | `DECIMAL(p,s)`, `FLOAT`, `DOUBLE` | DECIMAL for money, FLOAT for science |
| `Boolean`            | `BOOLEAN` / `TINYINT(1)`        | Stored as 0 or 1 (not true/false) |
| `Date`               | `DATE`, `DATETIME`, `TIMESTAMP` | Multiple date types available   |
| `Buffer`             | `BLOB`, `BINARY`                | Binary data storage             |
| `Array`              | ❌ No direct equivalent          | Use separate table or JSON column |
| `Object` (nested)    | ❌ No direct equivalent          | Use separate table or JSON column |
| `ObjectId` (ref)     | `INT` (Foreign Key)             | References another table's ID   |
| `Mixed`              | `JSON`                          | Stores any JSON (use sparingly) |
| `enum: [...]`        | `ENUM('a','b','c')`             | Built into the column definition |

---

## Why does it matter?

- **Wrong data type = wrong results**: Storing prices as `FLOAT` causes rounding errors (₹199.99 becomes ₹199.98999)
- **Storage efficiency**: `TINYINT` uses 1 byte, `BIGINT` uses 8 bytes — multiply by millions of rows
- **Query performance**: Comparing integers is faster than comparing strings
- **Data integrity**: MySQL rejects data that doesn't match the column type
- **Interview essential**: "What data type would you use for..." is a common question

---

## How does it work?

MySQL data types are grouped into 4 categories:

```
┌──────────────────────────────────────────────────────────────┐
│                    MySQL Data Types                          │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   Numeric    │    String    │  Date/Time   │    Other       │
├──────────────┼──────────────┼──────────────┼────────────────┤
│ TINYINT      │ CHAR(n)      │ DATE         │ JSON           │
│ SMALLINT     │ VARCHAR(n)   │ TIME         │ BLOB           │
│ MEDIUMINT    │ TEXT         │ DATETIME     │ ENUM           │
│ INT          │ MEDIUMTEXT   │ TIMESTAMP    │ SET            │
│ BIGINT       │ LONGTEXT     │ YEAR         │ BINARY         │
│ FLOAT        │              │              │ VARBINARY      │
│ DOUBLE       │              │              │ BOOLEAN        │
│ DECIMAL(p,s) │              │              │                │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

---

## Visual Diagram

### Numeric Types — Size Comparison

```
Type        Bytes   Min Value              Max Value
─────────── ─────── ────────────────────── ──────────────────────
TINYINT     1       -128                   127
SMALLINT    2       -32,768                32,767
MEDIUMINT   3       -8,388,608             8,388,607
INT         4       -2,147,483,648         2,147,483,647
BIGINT      8       -9.2 quintillion       9.2 quintillion

UNSIGNED versions double the positive range (no negatives):
TINYINT UNSIGNED    0 → 255
INT UNSIGNED        0 → 4,294,967,295

FLOAT       4       ~7 decimal digits precision
DOUBLE      8       ~15 decimal digits precision
DECIMAL(10,2) varies Exact precision! (use for money)
```

### String Types — When to Use What

```
┌──────────────────────────────────────────────────────────────┐
│                     STRING TYPES                             │
├──────────────┬─────────────┬─────────────────────────────────┤
│    Type      │  Max Length  │  Use Case                      │
├──────────────┼─────────────┼─────────────────────────────────┤
│ CHAR(10)     │ 10 chars    │ Fixed-length: country code, PIN │
│ VARCHAR(255) │ 255 chars   │ Variable: name, email, title   │
│ TEXT         │ 65,535 chars│ Descriptions, comments         │
│ MEDIUMTEXT   │ 16 MB       │ Blog posts, articles           │
│ LONGTEXT     │ 4 GB        │ Books, large HTML content      │
├──────────────┼─────────────┼─────────────────────────────────┤
│ CHAR vs VARCHAR:                                              │
│ CHAR(10) 'hi' → 'hi        ' (padded to 10 chars — wastes) │
│ VARCHAR(10) 'hi' → 'hi' (stores only 2 chars — efficient)  │
└──────────────────────────────────────────────────────────────┘
```

### Date/Time Types

```
Type        Format               Example                Storage
─────────── ──────────────────── ────────────────────── ───────
DATE        YYYY-MM-DD           2024-01-15             3 bytes
TIME        HH:MM:SS             14:30:00               3 bytes
DATETIME    YYYY-MM-DD HH:MM:SS 2024-01-15 14:30:00    8 bytes
TIMESTAMP   YYYY-MM-DD HH:MM:SS 2024-01-15 14:30:00    4 bytes
YEAR        YYYY                 2024                   1 byte

TIMESTAMP vs DATETIME:
- TIMESTAMP: Stores as UTC, converts to local time → good for global apps
- DATETIME: Stores as-is, no timezone conversion → good for fixed dates
- TIMESTAMP range: 1970-2038 (Y2K38 problem!)
- DATETIME range: 1000-9999
```

---

## Syntax

```sql
-- ============================================
-- NUMERIC TYPES
-- ============================================

-- Integer for IDs (auto increment)
id INT AUTO_INCREMENT PRIMARY KEY

-- Small numbers (age, quantity)
age TINYINT UNSIGNED          -- 0 to 255
stock SMALLINT UNSIGNED       -- 0 to 65,535

-- Money (ALWAYS use DECIMAL for currency!)
price DECIMAL(10, 2)          -- 10 digits total, 2 after decimal
                              -- Range: -99999999.99 to 99999999.99
                              -- Example: 79999.00, 299.50

-- Ratings (floating point — OK for non-financial)
rating FLOAT                  -- 4.5, 3.7, etc.

-- Boolean (true/false)
is_active BOOLEAN             -- Actually stored as TINYINT(1): 0=false, 1=true


-- ============================================
-- STRING TYPES
-- ============================================

-- Name, email, title (known max length)
name VARCHAR(100)
email VARCHAR(150)
phone VARCHAR(15)

-- Fixed-length codes
country_code CHAR(2)          -- 'IN', 'US', 'UK' (always 2 chars)
pin_code CHAR(6)              -- '110001' (always 6 digits)

-- Long text content
description TEXT
blog_content MEDIUMTEXT

-- Predefined choices (like Mongoose enum)
status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled')
gender ENUM('male', 'female', 'other')


-- ============================================
-- DATE/TIME TYPES
-- ============================================

-- Date only (birthdays, events)
birth_date DATE               -- '2000-05-15'

-- Date + Time (orders, logs)
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

-- Specific date+time without timezone
event_date DATETIME           -- '2024-12-31 23:59:59'


-- ============================================
-- SPECIAL TYPES
-- ============================================

-- JSON (store flexible data — like MongoDB subdocuments)
metadata JSON                 -- '{"color": "red", "size": "XL"}'

-- Binary data
profile_picture BLOB          -- Images, files (usually stored externally though)
```

---

## MERN vs SQL — Side-by-Side Code

```js
// ========== Mongoose Schema (What You Know) ==========
const productSchema = new mongoose.Schema({
  name:        { type: String, required: true, maxlength: 200 },
  description: { type: String },
  price:       { type: Number, required: true },
  stock:       { type: Number, default: 0 },
  rating:      { type: Number, min: 0, max: 5 },
  is_active:   { type: Boolean, default: true },
  tags:        [String],                        // Array of strings
  metadata:    { type: Object },                // Nested object
  category:    { type: mongoose.Schema.Types.ObjectId, ref: 'Category' },
  status:      { type: String, enum: ['draft', 'published', 'archived'] },
  created_at:  { type: Date, default: Date.now }
});
```

```sql
-- ========== MySQL Table (What You'll Use) ==========
CREATE TABLE products (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(200) NOT NULL,
  description TEXT,
  price       DECIMAL(10, 2) NOT NULL,          -- Not Number, use DECIMAL for money!
  stock       INT DEFAULT 0,
  rating      FLOAT,                            -- FLOAT is OK for ratings
  is_active   BOOLEAN DEFAULT TRUE,             -- Stored as 0/1
  tags        JSON,                             -- '["tech", "sale"]' — or use a tags table
  metadata    JSON,                             -- '{"color": "red"}'
  category_id INT,                              -- FK instead of ObjectId ref
  status      ENUM('draft', 'published', 'archived') DEFAULT 'draft',
  created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

```js
// ========== Node.js using mysql2/promise ==========
const pool = require('./db');

// Create products table
await pool.query(`
  CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    rating FLOAT,
    is_active BOOLEAN DEFAULT TRUE,
    tags JSON,
    metadata JSON,
    category_id INT,
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
  )
`);

// Insert with correct types
await pool.query(`
  INSERT INTO products (name, price, stock, tags, metadata, category_id, status)
  VALUES (?, ?, ?, ?, ?, ?, ?)
`, [
  'iPhone 15',                                    // VARCHAR
  79999.00,                                       // DECIMAL
  50,                                             // INT
  JSON.stringify(['electronics', 'smartphone']),  // JSON
  JSON.stringify({ color: 'black', storage: '128GB' }), // JSON
  1,                                              // INT (FK)
  'published'                                     // ENUM
]);
```

---

## ORM Equivalent (Sequelize)

```js
// ========== Sequelize Model ==========
const { DataTypes } = require('sequelize');

const Product = sequelize.define('Product', {
  name: {
    type: DataTypes.STRING(200),     // → VARCHAR(200)
    allowNull: false
  },
  description: {
    type: DataTypes.TEXT             // → TEXT
  },
  price: {
    type: DataTypes.DECIMAL(10, 2), // → DECIMAL(10,2)
    allowNull: false
  },
  stock: {
    type: DataTypes.INTEGER,         // → INT
    defaultValue: 0
  },
  rating: {
    type: DataTypes.FLOAT            // → FLOAT
  },
  isActive: {
    type: DataTypes.BOOLEAN,         // → TINYINT(1)
    defaultValue: true
  },
  tags: {
    type: DataTypes.JSON             // → JSON
  },
  metadata: {
    type: DataTypes.JSON             // → JSON
  },
  status: {
    type: DataTypes.ENUM('draft', 'published', 'archived'), // → ENUM
    defaultValue: 'draft'
  }
}, {
  tableName: 'products',
  underscored: true  // Uses snake_case columns (like created_at instead of createdAt)
});

// Association (like Mongoose ref + populate)
Product.belongsTo(Category, { foreignKey: 'category_id' });
```

---

## Real-World Scenario + Full Stack Code

### Scenario: Creating a customer registration form with proper data types

```sql
-- SQL: Customer table with carefully chosen data types
CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,       -- Names rarely exceed 50 chars
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,    -- Emails can be long (RFC allows 254)
  password_hash CHAR(60) NOT NULL,       -- bcrypt always outputs 60 chars → CHAR, not VARCHAR
  phone VARCHAR(15),                     -- International: +91-9876543210
  date_of_birth DATE,                    -- DATE, not DATETIME (no time needed)
  gender ENUM('male', 'female', 'other'),
  address TEXT,                          -- Addresses vary wildly in length
  pincode CHAR(6),                       -- Indian PIN: exactly 6 digits
  is_verified BOOLEAN DEFAULT FALSE,
  balance DECIMAL(12, 2) DEFAULT 0.00,   -- Wallet balance: up to 9,999,999,999.99
  profile JSON,                          -- Flexible metadata
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

```js
// Node.js + Express — Customer Registration API
const bcrypt = require('bcrypt');
const pool = require('./db');

app.post('/api/customers/register', async (req, res) => {
  try {
    const { firstName, lastName, email, password, phone, dateOfBirth, gender } = req.body;
    
    // Hash password (bcrypt always outputs 60 chars → matches CHAR(60))
    const passwordHash = await bcrypt.hash(password, 10);
    
    // Parameterized query — prevents SQL injection
    const [result] = await pool.query(`
      INSERT INTO customers (first_name, last_name, email, password_hash, phone, date_of_birth, gender)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `, [firstName, lastName, email, passwordHash, phone, dateOfBirth, gender]);
    
    res.status(201).json({
      message: 'Customer registered successfully',
      customerId: result.insertId  // Like MongoDB's insertedId
    });
  } catch (error) {
    if (error.code === 'ER_DUP_ENTRY') {
      return res.status(409).json({ error: 'Email already exists' });
    }
    res.status(500).json({ error: error.message });
  }
});
```

```js
// React Registration Form
import { useState } from 'react';
import axios from 'axios';

function RegisterForm() {
  const [form, setForm] = useState({
    firstName: '', lastName: '', email: '',
    password: '', phone: '', dateOfBirth: '', gender: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await axios.post('/api/customers/register', form);
      alert(`Registered! Customer ID: ${data.customerId}`);
    } catch (error) {
      alert(error.response?.data?.error || 'Registration failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input placeholder="First Name" maxLength={50}
        onChange={e => setForm({...form, firstName: e.target.value})} />
      <input placeholder="Last Name" maxLength={50}
        onChange={e => setForm({...form, lastName: e.target.value})} />
      <input type="email" placeholder="Email" maxLength={150}
        onChange={e => setForm({...form, email: e.target.value})} />
      <input type="password" placeholder="Password"
        onChange={e => setForm({...form, password: e.target.value})} />
      <input placeholder="Phone" maxLength={15}
        onChange={e => setForm({...form, phone: e.target.value})} />
      <input type="date"
        onChange={e => setForm({...form, dateOfBirth: e.target.value})} />
      <select onChange={e => setForm({...form, gender: e.target.value})}>
        <option value="">Select Gender</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
      </select>
      <button type="submit">Register</button>
    </form>
  );
}
```

**Output:**
```json
{
  "message": "Customer registered successfully",
  "customerId": 1
}
```

---

## Impact

| If You Choose Wrong Data Type...       | What Happens                                    |
|----------------------------------------|-------------------------------------------------|
| Use `FLOAT` for money                  | ₹199.99 × 3 = ₹599.96999... (rounding error!)  |
| Use `VARCHAR(255)` for everything      | Wasted storage, slower queries on millions of rows |
| Use `INT` for phone numbers            | Leading zeros are lost: 0991234567 → 991234567  |
| Use `DATETIME` for timestamps          | No timezone awareness → wrong times globally     |
| Use `TEXT` instead of `VARCHAR`        | Can't index TEXT columns efficiently             |
| Store arrays as comma-separated strings| Can't query individual values, joins become impossible |
| Use `INT` for an ID that might exceed 2B | Overflow error when your app goes viral        |

### The FLOAT vs DECIMAL Problem (Critical!)

```sql
-- FLOAT stores approximate values (binary floating point)
SELECT CAST(0.1 + 0.2 AS FLOAT);  -- Returns: 0.30000001192092896

-- DECIMAL stores exact values
SELECT CAST(0.1 AS DECIMAL(10,2)) + CAST(0.2 AS DECIMAL(10,2));  -- Returns: 0.30

-- For money, ALWAYS use DECIMAL!
```

This is the same problem as JavaScript's `0.1 + 0.2 === 0.30000000000000004`.

---

## Practice Exercises

### Easy (SQL)
1. Create a table `students` with columns: `id` (INT), `name` (VARCHAR), `grade` (CHAR(1)), `gpa` (DECIMAL), `enrolled_date` (DATE)
2. What's the difference between `CHAR(10)` and `VARCHAR(10)`? When would you use each?
3. Create an ENUM column `status` with values: `active`, `inactive`, `suspended`

### Medium (SQL + Node.js)
4. Create the full `products` table using mysql2 with appropriate types for: name, price, description, stock, rating, is_active
5. Write an Express POST route that inserts a product with all the correct data types
6. Store product tags as JSON and write a query to find products that have a specific tag

### Hard (Full Stack)
7. Build a product creation form in React with:
   - Input validation matching MySQL constraints (maxLength, number ranges)
   - Proper `type` attributes on inputs (number, date, etc.)
   - Error handling for MySQL type mismatches
8. Create a data type comparison chart that queries `INFORMATION_SCHEMA.COLUMNS` and displays all columns, their types, and constraints for a given table

---

## Real-World Q&A

**Q1:** In Mongoose, I just use `Number` for everything. Why does MySQL have so many number types?
**A:** Storage and performance. A `TINYINT` uses 1 byte per row, `BIGINT` uses 8 bytes. With 10 million rows, that's the difference between 10 MB and 80 MB just for one column. Also, MySQL enforces ranges — `TINYINT` won't accept 999, preventing bad data.

**Q2:** Should I use `JSON` columns to store arrays and objects like MongoDB?
**A:** Use JSON sparingly. It's useful for flexible metadata but don't abuse it. If you're querying by JSON fields frequently, extract them into separate columns or tables. SQL databases are optimized for structured columns, not JSON parsing. If you find yourself using JSON for everything, you might as well stay with MongoDB.

**Q3:** What data type should I use for passwords?
**A:** NEVER store plain-text passwords. Store bcrypt hashes which are always exactly 60 characters. Use `CHAR(60)` — not `VARCHAR` — because CHAR is faster for fixed-length data. The predictable length also serves as a sanity check that the hash was generated correctly.

---

## Interview Q&A

**Q1: What is the difference between CHAR and VARCHAR?**
CHAR is fixed-length: `CHAR(10)` always stores exactly 10 characters, padding with spaces if needed. VARCHAR is variable-length: `VARCHAR(10)` stores only the characters used (plus 1-2 bytes for length). Use CHAR for fixed-length data (country codes, PINs), VARCHAR for variable-length data (names, emails). CHAR is slightly faster for fixed-length data due to predictable storage.

**Q2: Why should you use DECIMAL instead of FLOAT for monetary values?**
FLOAT uses binary floating-point representation which cannot exactly represent many decimal fractions (like 0.1). This leads to rounding errors in calculations. DECIMAL stores exact decimal values, making it essential for financial calculations where precision matters. Example: `0.1 + 0.2 = 0.3` with DECIMAL, but `0.30000001` with FLOAT.

**Q3: What is the difference between DATETIME and TIMESTAMP?**
Both store date and time. TIMESTAMP stores in UTC and converts to the session timezone on retrieval (good for global apps). DATETIME stores the exact value with no conversion (good for fixed dates like birthdays). TIMESTAMP range is 1970-2038; DATETIME range is 1000-9999. TIMESTAMP uses 4 bytes; DATETIME uses 8 bytes.

**Q4: How would you store a list of tags for a product in MySQL?**
Three approaches: (1) JSON column: `tags JSON` — stores `["tag1","tag2"]`, simple but hard to query. (2) Separate tags table with a junction table: `product_tags(product_id, tag_id)` — normalized, queryable, best practice. (3) Comma-separated string: `tags VARCHAR(500)` — worst approach, impossible to query efficiently.

**Q5: A column defined as `INT UNSIGNED` can store values from 0 to 4,294,967,295. When would you use this over a regular `INT`?**
When the column should never have negative values — like `age`, `quantity`, `price` (in whole numbers), or `views_count`. The UNSIGNED modifier doubles the positive range by eliminating negative values. However, be careful with operations that could produce negative results (e.g., subtraction) — they'll cause errors with UNSIGNED columns.

---

| [← Previous: Databases & Tables](./02_Databases_And_Tables.md) | [Next: Create, Drop & Alter →](./04_Create_Drop_Alter.md) |
|---|---|
