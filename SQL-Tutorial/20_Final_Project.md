# Final Project

> 📌 **File:** 20_Final_Project.md | **Level:** Beginner → MERN Developer

---

## What is it?
This is the capstone project. You will synthesize all SQL concepts by building a complete backend API for the `ecommerce` database using Node.js, Express, `mysql2`, React, and raw parameterized Queries.

## MERN Parallel — You Already Know This!
- Replicating a full-stack Mongoose portfolio project purely using raw SQL strings and relations.

## Why does it matter?
Tutorials don't cement knowledge; building from scratch does. Wiring complex `JOIN`s to React hooks solves real 3D architecture problems.

## How does it work?
Follow the structural steps to build the E-Commerce API Server.

## Visual Diagram
```ascii
[ React Client ]
       | GET /api/storefront
[ Node Server ]
       | pool.query("SELECT ... JOIN ... GROUP BY")
[ MySQL Schema ] -> Customers, Categories, Products, Invoices.
```

## System Requirements

### 1. Database Schema
Copy and execute this script locally via MySQL Workbench.
```sql
CREATE DATABASE storefront;
USE storefront;

CREATE TABLE categories (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL
);

CREATE TABLE products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  category_id INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  price DECIMAL(10, 2) NOT NULL,
  stock INT DEFAULT 0,
  FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  status VARCHAR(50) DEFAULT 'PENDING',
  total DECIMAL(10,2) DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 2. Node.js Boilerplate
```javascript
// db.js
const mysql = require('mysql2/promise');
module.exports = mysql.createPool({ 
  host: 'localhost', user: 'root', password: 'pwd', database: 'storefront' 
});
```

### 3. API Challenges to Build

**Goal 1: Pagination & Joins (Select Basics, Joins, Limits)**
```javascript
// GET /api/products
// Must return List of products with their raw Category NAME (requires JOIN).
// Must support ?page=x offsets.
app.get('/api/products', async (req, res) => {
  // YOUR RAW SQL: SELECT title, price, name AS category FROM products
  // JOIN categories ON products.category_id = categories.id LIMIT ? OFFSET ?
});
```

**Goal 2: Complex Aggregation (Group By, Where, Having)**
```javascript
// GET /api/analytics/categories
// Must return category names and TOTAL inventory value (stock * price),
// ONLY for categories with total > 1000.
```

**Goal 3: Transactions (Insert, Update, Transactions)**
```javascript
// POST /api/checkout
// Must wrap in transaction: 
// 1. Create order for user
// 2. Reduce product stock
// 3. Commit.
```

### Real-World Scenario + Full Stack Code
**Scenario:** The Frontend React dashboard mapping the above APIs.

```javascript
// React component using Axios
import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function StoreAdmin() {
  const [analytics, setAnalytics] = useState([]);
  
  const checkout = async () => {
    try {
      await axios.post('/api/checkout', { userId: 1, productId: 5 });
      alert('Atomic Transaction Success!');
    } catch (e) { alert('Rollback Fired!'); }
  }

  useEffect(() => {
    axios.get('/api/analytics/categories').then(r => setAnalytics(r.data));
  }, []);

  return (
     <div>
       <h2>Top Categories Value</h2>
       {analytics.map(a => <div key={a.name}>{a.name}: ${a.total_value}</div>)}
       <button onClick={checkout}>Test Checkout</button>
     </div>
  )
}
```

## Impact
Successfully passing this test means you are ready to architect scalable relational business applications without relying primarily on ORMs for abstraction.

## Advanced Extensions
- Build an `AFTER UPDATE` trigger that logs low-stock warnings when an item falls below 5.
- Create a `Subquery` returning users who haven't ordered anything in exactly 1 week.

| Previous: [19_SQL_Vs_NoSQL.md](./19_SQL_Vs_NoSQL.md) | Next: [21_Deployment_On_EC2.md](./21_Deployment_On_EC2.md) |
