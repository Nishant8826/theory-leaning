# Final Project

> 📌 **File:** `20_Final_Project.md` | **Level:** Beginner → MERN Developer

---

## What is it?

This is your capstone project — a full-stack **E-Commerce REST API** built with Node.js, Express, MySQL (mysql2/promise), and React. It brings together EVERY concept from the tutorial: tables, relationships, CRUD, JOINs, aggregations, transactions, indexes, views, stored procedures, and triggers.

---

## Project Overview

### E-Commerce Application: "ShopSQL"

```
┌─────────────────────────────────────────────────────────────────┐
│                         ShopSQL                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Frontend (React)           Backend (Express)      Database     │
│  ┌───────────────┐         ┌──────────────┐       ┌──────────┐│
│  │ Product List  │────────▶│ GET /products│──────▶│ products ││
│  │ Cart          │────────▶│ POST /orders │──────▶│ orders   ││
│  │ Checkout      │────────▶│ POST /pay    │──────▶│ payments ││
│  │ Order History │────────▶│ GET /orders  │──────▶│ o_items  ││
│  │ Admin Panel   │────────▶│ CRUD all     │──────▶│ customers││
│  │ Dashboard     │────────▶│ GET /stats   │──────▶│ views    ││
│  └───────────────┘         └──────────────┘       └──────────┘│
│                                                                 │
│  Port: 3000                Port: 5000              Port: 3306  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Database Schema

```sql
-- ============================================
-- Complete E-Commerce Database Schema
-- ============================================

CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

-- Categories
CREATE TABLE categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  image_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products
CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
  cost_price DECIMAL(10, 2),
  stock INT UNSIGNED DEFAULT 0,
  sku VARCHAR(50) UNIQUE,
  category_id INT,
  status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
  image_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
  INDEX idx_category (category_id),
  INDEX idx_status (status),
  INDEX idx_price (price),
  FULLTEXT INDEX ft_search (name, description)
);

-- Customers
CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  password_hash CHAR(60) NOT NULL,
  phone VARCHAR(15),
  address TEXT,
  city VARCHAR(50),
  state VARCHAR(50),
  pincode CHAR(6),
  is_active BOOLEAN DEFAULT TRUE,
  loyalty_points INT UNSIGNED DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_email (email)
);

-- Orders
CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  subtotal DECIMAL(10, 2) NOT NULL DEFAULT 0,
  tax_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
  shipping_amount DECIMAL(10, 2) DEFAULT 0,
  total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
  status ENUM('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded') DEFAULT 'pending',
  shipping_address TEXT,
  payment_method ENUM('cod', 'upi', 'card', 'netbanking') DEFAULT 'cod',
  payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'pending',
  order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  delivered_at TIMESTAMP NULL,
  notes TEXT,
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  INDEX idx_customer (customer_id),
  INDEX idx_status (status),
  INDEX idx_date (order_date)
);

-- Order Items
CREATE TABLE order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
  unit_price DECIMAL(10, 2) NOT NULL,
  total_price DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id),
  INDEX idx_order (order_id),
  INDEX idx_product (product_id)
);

-- Audit Log
CREATE TABLE audit_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  table_name VARCHAR(50),
  record_id INT,
  action ENUM('INSERT', 'UPDATE', 'DELETE'),
  old_data JSON,
  new_data JSON,
  changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_table_record (table_name, record_id)
);
```

---

## Step 2: Seed Data

```sql
-- Categories
INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices, gadgets, and accessories'),
('Clothing', 'Fashion, apparel, and accessories'),
('Books', 'Books, eBooks, and literature'),
('Home & Kitchen', 'Home decor, kitchen appliances, and essentials'),
('Sports', 'Sports equipment and fitness accessories');

-- Products
INSERT INTO products (name, description, price, cost_price, stock, sku, category_id, status) VALUES
('iPhone 15 Pro', '256GB, Natural Titanium, A17 Pro chip', 134900.00, 95000.00, 50, 'ELEC-IP15P-256', 1, 'published'),
('MacBook Air M3', '8GB RAM, 256GB SSD, 13.6" Display', 114900.00, 80000.00, 30, 'ELEC-MBA-M3', 1, 'published'),
('AirPods Pro 2', 'Active Noise Cancellation, USB-C', 24900.00, 15000.00, 100, 'ELEC-APP2', 1, 'published'),
('Samsung Galaxy S24', '128GB, Phantom Black', 69999.00, 48000.00, 75, 'ELEC-SGS24', 1, 'published'),
('Levis 511 Slim Jeans', 'Blue denim, slim fit, stretch', 2999.00, 1200.00, 200, 'CLO-LV511-BLU', 2, 'published'),
('Nike Air Max 90', 'White/Black, running shoes', 12999.00, 6500.00, 150, 'CLO-NAM90-WB', 2, 'published'),
('The Alchemist', 'Paulo Coelho, Paperback', 299.00, 100.00, 500, 'BOOK-ALC-PB', 3, 'published'),
('Atomic Habits', 'James Clear, Hardcover', 599.00, 250.00, 300, 'BOOK-AH-HC', 3, 'published'),
('Prestige Pressure Cooker', '5L, Stainless Steel', 2499.00, 1200.00, 80, 'HOME-PPC-5L', 4, 'published'),
('Yoga Mat', 'Anti-slip, 6mm, Blue', 999.00, 400.00, 200, 'SPORT-YM-6BL', 5, 'published');

-- Customers
INSERT INTO customers (first_name, last_name, email, password_hash, phone, city, state, pincode) VALUES
('Nishant', 'Kumar', 'nishant@test.com', '$2b$10$dummyhash1234567890abcdefghijklmnopqrstuvwx', '9876543210', 'Delhi', 'Delhi', '110001'),
('Priya', 'Sharma', 'priya@test.com', '$2b$10$dummyhash1234567890abcdefghijklmnopqrstuvwx', '8765432109', 'Mumbai', 'Maharashtra', '400001'),
('Rahul', 'Verma', 'rahul@test.com', '$2b$10$dummyhash1234567890abcdefghijklmnopqrstuvwx', '7654321098', 'Bangalore', 'Karnataka', '560001'),
('Sneha', 'Patel', 'sneha@test.com', '$2b$10$dummyhash1234567890abcdefghijklmnopqrstuvwx', '6543210987', 'Ahmedabad', 'Gujarat', '380001'),
('Amit', 'Singh', 'amit@test.com', '$2b$10$dummyhash1234567890abcdefghijklmnopqrstuvwx', '5432109876', 'Jaipur', 'Rajasthan', '302001');
```

---

## Step 3: Views

```sql
-- Product listing view (used by frontend)
CREATE OR REPLACE VIEW v_product_listing AS
SELECT 
  p.id, p.name, p.description, p.price, p.stock, p.sku,
  p.image_url, p.status,
  c.name AS category,
  c.id AS category_id,
  ROUND(p.price * 1.18, 2) AS price_with_gst,
  CASE 
    WHEN p.stock = 0 THEN 'out_of_stock'
    WHEN p.stock < 10 THEN 'low_stock'
    ELSE 'in_stock'
  END AS availability,
  p.created_at
FROM products p
LEFT JOIN categories c ON p.category_id = c.id;

-- Order summary view
CREATE OR REPLACE VIEW v_order_summary AS
SELECT 
  o.id AS order_id,
  CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
  c.email,
  o.total_amount,
  o.status,
  o.payment_status,
  o.order_date,
  COUNT(oi.id) AS item_count,
  SUM(oi.quantity) AS total_units
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, c.first_name, c.last_name, c.email, 
         o.total_amount, o.status, o.payment_status, o.order_date;

-- Dashboard stats view
CREATE OR REPLACE VIEW v_dashboard AS
SELECT
  (SELECT COUNT(*) FROM products WHERE status = 'published') AS total_products,
  (SELECT COUNT(*) FROM customers WHERE is_active = TRUE) AS total_customers,
  (SELECT COUNT(*) FROM orders) AS total_orders,
  (SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status != 'cancelled') AS total_revenue,
  (SELECT COUNT(*) FROM orders WHERE status = 'pending') AS pending_orders,
  (SELECT COUNT(*) FROM products WHERE stock = 0) AS out_of_stock;
```

---

## Step 4: Triggers

```sql
DELIMITER //

-- Audit log trigger for products
CREATE TRIGGER trg_product_audit_update
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
  IF OLD.price != NEW.price OR OLD.stock != NEW.stock OR OLD.status != NEW.status THEN
    INSERT INTO audit_log (table_name, record_id, action, old_data, new_data)
    VALUES ('products', NEW.id, 'UPDATE',
      JSON_OBJECT('price', OLD.price, 'stock', OLD.stock, 'status', OLD.status),
      JSON_OBJECT('price', NEW.price, 'stock', NEW.stock, 'status', NEW.status)
    );
  END IF;
END //

-- Auto-calculate order totals
CREATE TRIGGER trg_order_item_after_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
  DECLARE v_subtotal DECIMAL(10,2);
  SELECT SUM(quantity * unit_price) INTO v_subtotal
  FROM order_items WHERE order_id = NEW.order_id;
  
  UPDATE orders SET 
    subtotal = v_subtotal,
    tax_amount = ROUND(v_subtotal * 0.18, 2),
    total_amount = ROUND(v_subtotal * 1.18, 2)
  WHERE id = NEW.order_id;
END //

DELIMITER ;
```

---

## Step 5: Stored Procedure

```sql
DELIMITER //

CREATE PROCEDURE sp_place_order(
  IN p_customer_id INT,
  IN p_items JSON,
  IN p_shipping_address TEXT,
  IN p_payment_method VARCHAR(20),
  OUT p_order_id INT,
  OUT p_total DECIMAL(10,2),
  OUT p_message VARCHAR(255)
)
BEGIN
  DECLARE v_i INT DEFAULT 0;
  DECLARE v_count INT;
  DECLARE v_product_id INT;
  DECLARE v_quantity INT;
  DECLARE v_price DECIMAL(10,2);
  DECLARE v_stock INT;
  
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    SET p_order_id = NULL;
    SET p_total = 0;
    SET p_message = 'Transaction failed. All changes rolled back.';
  END;
  
  SET v_count = JSON_LENGTH(p_items);
  START TRANSACTION;
  
  -- Create order
  INSERT INTO orders (customer_id, shipping_address, payment_method, status)
  VALUES (p_customer_id, p_shipping_address, p_payment_method, 'pending');
  SET p_order_id = LAST_INSERT_ID();
  
  -- Process each item
  WHILE v_i < v_count DO
    SET v_product_id = JSON_EXTRACT(p_items, CONCAT('$[', v_i, '].productId'));
    SET v_quantity = JSON_EXTRACT(p_items, CONCAT('$[', v_i, '].quantity'));
    
    -- Check stock with lock
    SELECT price, stock INTO v_price, v_stock
    FROM products WHERE id = v_product_id FOR UPDATE;
    
    IF v_stock < v_quantity THEN
      SET p_message = CONCAT('Insufficient stock for product ID ', v_product_id);
      ROLLBACK;
      SET p_order_id = NULL;
      SET p_total = 0;
      LEAVE;
    END IF;
    
    -- Add item
    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
    VALUES (p_order_id, v_product_id, v_quantity, v_price);
    
    -- Deduct stock
    UPDATE products SET stock = stock - v_quantity WHERE id = v_product_id;
    
    -- Award loyalty points (1 point per ₹100 spent)
    UPDATE customers 
    SET loyalty_points = loyalty_points + FLOOR((v_price * v_quantity) / 100)
    WHERE id = p_customer_id;
    
    SET v_i = v_i + 1;
  END WHILE;
  
  IF p_order_id IS NOT NULL THEN
    -- Get total (calculated by trigger)
    SELECT total_amount INTO p_total FROM orders WHERE id = p_order_id;
    SET p_message = CONCAT('Order #', p_order_id, ' placed. Total: ₹', p_total);
    COMMIT;
  END IF;
END //

DELIMITER ;
```

---

## Step 6: Express API (Key Routes)

```js
// server.js
const express = require('express');
const cors = require('cors');
const pool = require('./db');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// ==================== PRODUCTS ====================

// Search & Filter Products
app.get('/api/products', async (req, res) => {
  try {
    const { search, category, minPrice, maxPrice, sort, page = 1, limit = 12 } = req.query;
    const offset = (parseInt(page) - 1) * parseInt(limit);
    
    let sql = 'SELECT * FROM v_product_listing WHERE status = ?';
    const params = ['published'];
    
    if (search) {
      sql += ' AND (name LIKE ? OR description LIKE ?)';
      params.push(`%${search}%`, `%${search}%`);
    }
    if (category) { sql += ' AND category_id = ?'; params.push(category); }
    if (minPrice) { sql += ' AND price >= ?'; params.push(minPrice); }
    if (maxPrice) { sql += ' AND price <= ?'; params.push(maxPrice); }
    
    const sortMap = {
      'price_asc': 'price ASC', 'price_desc': 'price DESC',
      'newest': 'created_at DESC', 'name': 'name ASC'
    };
    sql += ` ORDER BY ${sortMap[sort] || 'created_at DESC'} LIMIT ? OFFSET ?`;
    params.push(parseInt(limit), offset);
    
    const [products] = await pool.query(sql, params);
    
    // Get total for pagination
    let countSql = 'SELECT COUNT(*) AS total FROM v_product_listing WHERE status = ?';
    const countParams = ['published'];
    if (search) { countSql += ' AND (name LIKE ? OR description LIKE ?)'; countParams.push(`%${search}%`, `%${search}%`); }
    if (category) { countSql += ' AND category_id = ?'; countParams.push(category); }
    
    const [countResult] = await pool.query(countSql, countParams);
    
    res.json({
      products,
      pagination: {
        page: parseInt(page), limit: parseInt(limit),
        total: countResult[0].total,
        totalPages: Math.ceil(countResult[0].total / parseInt(limit))
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== ORDERS ====================

// Place Order (uses stored procedure)
app.post('/api/orders', async (req, res) => {
  try {
    const { customerId, items, shippingAddress, paymentMethod } = req.body;
    
    await pool.query(
      'CALL sp_place_order(?, ?, ?, ?, @orderId, @total, @msg)',
      [customerId, JSON.stringify(items), shippingAddress, paymentMethod || 'cod']
    );
    
    const [result] = await pool.query('SELECT @orderId AS orderId, @total AS total, @msg AS message');
    
    if (result[0].orderId) {
      res.status(201).json({
        orderId: result[0].orderId,
        total: result[0].total,
        message: result[0].message
      });
    } else {
      res.status(400).json({ error: result[0].message });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get Order Details
app.get('/api/orders/:id', async (req, res) => {
  try {
    const [orderRows] = await pool.query(
      `SELECT o.*, CONCAT(c.first_name, ' ', c.last_name) AS customer_name, c.email
       FROM orders o JOIN customers c ON o.customer_id = c.id WHERE o.id = ?`,
      [req.params.id]
    );
    if (orderRows.length === 0) return res.status(404).json({ error: 'Not found' });
    
    const [items] = await pool.query(
      `SELECT oi.*, p.name AS product_name, p.image_url
       FROM order_items oi JOIN products p ON oi.product_id = p.id
       WHERE oi.order_id = ?`,
      [req.params.id]
    );
    
    res.json({ ...orderRows[0], items });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ==================== DASHBOARD ====================

app.get('/api/dashboard', async (req, res) => {
  try {
    const [stats] = await pool.query('SELECT * FROM v_dashboard');
    
    const [recentOrders] = await pool.query(
      'SELECT * FROM v_order_summary ORDER BY order_date DESC LIMIT 5'
    );
    
    const [monthlyRevenue] = await pool.query(`
      SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
        COUNT(*) AS orders, ROUND(SUM(total_amount), 2) AS revenue
      FROM orders WHERE status != 'cancelled'
      GROUP BY month ORDER BY month DESC LIMIT 6
    `);
    
    const [topProducts] = await pool.query(`
      SELECT p.name, SUM(oi.quantity) AS sold, ROUND(SUM(oi.total_price), 2) AS revenue
      FROM order_items oi JOIN products p ON oi.product_id = p.id
      JOIN orders o ON oi.order_id = o.id WHERE o.status != 'cancelled'
      GROUP BY p.id, p.name ORDER BY revenue DESC LIMIT 5
    `);
    
    res.json({ stats: stats[0], recentOrders, monthlyRevenue, topProducts });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
```

---

## Step 7: React Frontend (Key Components)

```js
// App.js — Main application with routing
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ProductList from './components/ProductList';
import ProductDetail from './components/ProductDetail';
import Cart from './components/Cart';
import Checkout from './components/Checkout';
import OrderHistory from './components/OrderHistory';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <nav>
        <a href="/">Shop</a>
        <a href="/cart">Cart</a>
        <a href="/orders">Orders</a>
        <a href="/admin">Dashboard</a>
      </nav>
      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path="/products/:id" element={<ProductDetail />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="/orders" element={<OrderHistory />} />
        <Route path="/admin" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
```

---

## Concepts Applied

| Tutorial Chapter       | Applied In Project                              |
|------------------------|-------------------------------------------------|
| 02: Databases & Tables | Full schema with 6 tables                       |
| 03: Data Types         | DECIMAL for money, ENUM for status, JSON params |
| 04: CREATE/ALTER       | Schema with constraints, foreign keys           |
| 05: INSERT/UPDATE/DEL  | Full CRUD API                                   |
| 06: SELECT             | Aliases, computed columns, CASE                 |
| 07: WHERE              | Dynamic filters, search, parameterized queries  |
| 08: ORDER BY/LIMIT     | Sorting, pagination                             |
| 09: Aggregates         | Dashboard stats (COUNT, SUM, AVG)               |
| 10: GROUP BY           | Monthly revenue, top products                   |
| 11: JOINs              | Multi-table queries (4+ JOINs)                  |
| 12: Subqueries         | Complex filtered queries                        |
| 13: Views              | product_listing, order_summary, dashboard       |
| 14: Indexes            | FK indexes, FULLTEXT search, price index        |
| 15: Transactions       | Order placement with stock deduction            |
| 16: Stored Procedures  | sp_place_order with error handling               |
| 17: Triggers           | Audit log, auto-calculate totals                |
| 18: Normalization      | Fully normalized schema (3NF)                   |

---

## Practice: Extend the Project

1. **Authentication**: Add JWT-based auth with bcrypt password hashing
2. **Cart System**: Store cart in MySQL (persistent cart) or localStorage
3. **Payment Integration**: Add Razorpay/Stripe mock payment flow
4. **Admin Panel**: CRUD for products, categories, and order management
5. **Search**: Implement FULLTEXT search with relevance scoring
6. **Reviews**: Add product reviews with rating aggregation
7. **Coupons**: Discount codes with validation stored procedure
8. **Email Notifications**: Trigger-based order confirmation emails
9. **Analytics**: Build a full analytics dashboard with date range filters
10. **API Documentation**: Add Swagger/OpenAPI documentation

---

| [← Previous: SQL vs NoSQL](./19_SQL_Vs_NoSQL.md) | [Next: Deployment on EC2 →](./21_Deployment_On_EC2.md) |
|---|---|
