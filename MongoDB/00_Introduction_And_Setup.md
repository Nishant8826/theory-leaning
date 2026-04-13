# Introduction & Setup

> 📌 **File:** 00_Introduction_And_Setup.md | **Level:** SQL Expert → MongoDB

---

## What is it?

MongoDB is a **document-oriented NoSQL database** that stores data as flexible JSON-like documents (BSON internally). Unlike SQL databases where you define rigid schemas upfront, MongoDB lets you store heterogeneous documents in the same collection. It was built for **horizontal scalability**, **flexible schema evolution**, and **developer productivity** — not as a replacement for SQL, but as a different tool for different problems.

**You already know:** Tables, rows, columns, foreign keys, JOINs, ACID transactions, normalization.
**What changes:** No tables — collections. No rows — documents. No rigid schema — flexible structure. No JOINs by default — embed or reference.

---

## SQL Parallel — Think of it like this

```
┌──────────────────────────────────────────────────────┐
│              SQL World → MongoDB World               │
├──────────────────┬───────────────────────────────────┤
│  Database        │  Database                         │
│  Table           │  Collection                       │
│  Row             │  Document                         │
│  Column          │  Field                            │
│  PRIMARY KEY     │  _id (auto-generated ObjectId)    │
│  JOIN            │  $lookup / Embedding              │
│  Schema (DDL)    │  Schema-less (or validated)       │
│  mysqld / pg     │  mongod                           │
│  mysql / psql    │  mongosh                          │
│  MySQL WB / pgA  │  MongoDB Compass                  │
│  ORM (Sequelize) │  ODM (Mongoose)                   │
└──────────────────┴───────────────────────────────────┘
```

---

## Why MongoDB Exists (Not a beginner pitch)

As an SQL expert, you know that relational databases excel at:
- **Structured, predictable data** (banking, ERP, inventory)
- **Complex relationships** (many-to-many, self-referencing)
- **ACID guarantees** across multiple tables

MongoDB was created because certain workloads **fight against** the relational model:

| Problem                          | SQL Pain Point                    | MongoDB Advantage                     |
|----------------------------------|-----------------------------------|---------------------------------------|
| Rapidly evolving schemas         | ALTER TABLE on 100M rows = pain   | Add/remove fields instantly           |
| Deeply nested / hierarchical     | Multiple JOINs, N+1 queries      | Single document read                  |
| High write throughput            | Vertical scaling limits           | Horizontal sharding built-in          |
| Geographically distributed       | Complex replication               | Native replica sets & zones           |
| Semi-structured data (logs, IoT) | Awkward EAV or JSON columns       | Natural document fit                  |

---

## Installation — MongoDB Community Server

### Windows

```powershell
# Option 1: Download MSI installer from
# https://www.mongodb.com/try/download/community

# Option 2: Using winget
winget install MongoDB.Server

# Option 3: Using Chocolatey
choco install mongodb
```

After installation:
1. MongoDB installs as a Windows service (`MongoDB Server`)
2. Default data directory: `C:\Program Files\MongoDB\Server\7.0\data\`
3. Default port: `27017`

### Verify Installation

```powershell
# Check if mongod is running
mongosh --version

# Connect to MongoDB
mongosh
```

### macOS

```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

### Linux (Ubuntu)

```bash
# Import MongoDB GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

# Add repository
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

---

## Install MongoDB Compass (GUI)

Download from: https://www.mongodb.com/try/download/compass

```
Compass = pgAdmin / MySQL Workbench equivalent
- Visual query builder
- Index analysis
- Schema visualization
- Performance profiling
```

Connection string: `mongodb://localhost:27017`

---

## Install mongosh (MongoDB Shell)

```powershell
# Usually included with server install
# Or install separately:
winget install MongoDB.Shell
```

### First Commands (SQL Equivalents)

```javascript
// Connect
mongosh

// Show all databases (SHOW DATABASES;)
show dbs

// Switch to database (USE ecommerce;)
use ecommerce

// Show collections (SHOW TABLES;)
show collections

// Create collection implicitly by inserting
db.products.insertOne({
  name: "Laptop",
  price: 1000,
  category: { name: "Electronics" }
})

// Verify
db.products.find()
```

---

## Create the `ecommerce` Database with Sample Data

```javascript
// Switch to ecommerce database (created on first write)
use ecommerce

// Insert sample products
db.products.insertMany([
  {
    name: "Laptop",
    price: 999.99,
    brand: "Dell",
    category: { name: "Electronics", slug: "electronics" },
    specs: { ram: "16GB", storage: "512GB SSD", cpu: "i7-12700H" },
    tags: ["computer", "portable", "work"],
    stock: 45,
    ratings: { average: 4.5, count: 234 },
    createdAt: new Date()
  },
  {
    name: "Running Shoes",
    price: 129.99,
    brand: "Nike",
    category: { name: "Footwear", slug: "footwear" },
    sizes: [7, 8, 9, 10, 11, 12],
    color: "Black/Red",
    stock: 120,
    ratings: { average: 4.2, count: 89 },
    createdAt: new Date()
  },
  {
    name: "Coffee Maker",
    price: 79.99,
    brand: "Breville",
    category: { name: "Kitchen", slug: "kitchen" },
    features: ["programmable", "12-cup", "auto-shutoff"],
    stock: 67,
    ratings: { average: 4.7, count: 412 },
    createdAt: new Date()
  }
])

// Insert sample customers
db.customers.insertMany([
  {
    firstName: "John",
    lastName: "Doe",
    email: "john@example.com",
    address: {
      street: "123 Main St",
      city: "New York",
      state: "NY",
      zip: "10001"
    },
    orders: [],
    createdAt: new Date()
  },
  {
    firstName: "Jane",
    lastName: "Smith",
    email: "jane@example.com",
    address: {
      street: "456 Oak Ave",
      city: "San Francisco",
      state: "CA",
      zip: "94102"
    },
    orders: [],
    createdAt: new Date()
  }
])

// Insert sample categories
db.categories.insertMany([
  { name: "Electronics", slug: "electronics", description: "Electronic devices and accessories" },
  { name: "Footwear", slug: "footwear", description: "Shoes and sandals" },
  { name: "Kitchen", slug: "kitchen", description: "Kitchen appliances and tools" }
])

// Verify
db.products.countDocuments()   // 3
db.customers.countDocuments()  // 2
db.categories.countDocuments() // 3
```

---

## Node.js Project Setup

```powershell
mkdir mongodb-ecommerce-api
cd mongodb-ecommerce-api
npm init -y
npm install mongodb mongoose express dotenv
npm install -D nodemon
```

### Project Structure

```
mongodb-ecommerce-api/
├── config/
│   └── db.js
├── routes/
│   └── products.js
├── models/
│   └── Product.js
├── .env
├── server.js
└── package.json
```

### `.env`

```env
MONGO_URI=mongodb://localhost:27017/ecommerce
PORT=3000
```

### `config/db.js` — Native Driver Connection

```javascript
const { MongoClient } = require('mongodb');

let db;

async function connectDB() {
  const client = new MongoClient(process.env.MONGO_URI);
  await client.connect();
  db = client.db(); // Uses database from URI
  console.log(`✅ MongoDB connected: ${db.databaseName}`);
  return db;
}

function getDB() {
  if (!db) throw new Error('Database not initialized. Call connectDB() first.');
  return db;
}

module.exports = { connectDB, getDB };
```

### `config/mongoose.js` — Mongoose Connection

```javascript
const mongoose = require('mongoose');

async function connectMongoose() {
  await mongoose.connect(process.env.MONGO_URI);
  console.log(`✅ Mongoose connected: ${mongoose.connection.name}`);
}

module.exports = { connectMongoose };
```

### `server.js`

```javascript
require('dotenv').config();
const express = require('express');
const { connectDB } = require('./config/db');

const app = express();
app.use(express.json());

// Test route
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', database: 'MongoDB', timestamp: new Date() });
});

// Products route — native driver
app.get('/api/products', async (req, res) => {
  try {
    const { getDB } = require('./config/db');
    const db = getDB();
    const products = await db.collection('products').find({}).toArray();
    res.json(products);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Start server
const PORT = process.env.PORT || 3000;

async function start() {
  await connectDB();
  app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
}

start();
```

### `package.json` — Add scripts

```json
{
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  }
}
```

### Test

```powershell
npm run dev

# In another terminal:
curl http://localhost:3000/api/health
curl http://localhost:3000/api/products
```

---

## Verification Checklist

```
✅ MongoDB server running (mongod)
✅ mongosh connects successfully
✅ ecommerce database created
✅ products, customers, categories collections exist
✅ MongoDB Compass connects to localhost:27017
✅ Node.js server starts and returns products
✅ Both native driver and Mongoose connections work
```

---

## SQL vs MongoDB — Connection Comparison

```
┌─────────────────────────────────────────────────────────┐
│                    SQL (PostgreSQL)                      │
├─────────────────────────────────────────────────────────┤
│  const pool = new Pool({                                │
│    host: 'localhost',                                   │
│    port: 5432,                                          │
│    database: 'ecommerce',                               │
│    user: 'postgres',                                    │
│    password: 'secret'                                   │
│  });                                                    │
│  const res = await pool.query('SELECT * FROM products');│
├─────────────────────────────────────────────────────────┤
│                    MongoDB (Native)                     │
├─────────────────────────────────────────────────────────┤
│  const client = new MongoClient(uri);                   │
│  await client.connect();                                │
│  const db = client.db('ecommerce');                     │
│  const res = await db.collection('products')            │
│    .find({}).toArray();                                  │
├─────────────────────────────────────────────────────────┤
│                    MongoDB (Mongoose)                   │
├─────────────────────────────────────────────────────────┤
│  await mongoose.connect(uri);                           │
│  const res = await Product.find({});                    │
└─────────────────────────────────────────────────────────┘
```

---

## What's Next?

In the next file, we'll dive into the **mental model shift** from relational thinking to document thinking — the single most important concept you need to internalize before writing any MongoDB code.
