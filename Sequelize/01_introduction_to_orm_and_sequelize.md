# 01. Introduction to ORM and Sequelize

## 🎯 Goal of This Chapter
By the end of this chapter, you will understand what an Object-Relational Mapper (ORM) is, the problems it solves, how it differs from writing raw SQL queries, and why Sequelize is one of the most popular ORM choices for Node.js and Express applications.

---

## 🤔 Why This Topic Matters
When building web applications, you almost always need to store data in a database. Traditionally, developers wrote raw SQL queries in their backend code to communicate with databases. However, raw SQL strings inside JavaScript code lead to:
1. **High Boilerplate**: Manually writing connection code, mapping query result arrays back into JavaScript objects, and handling errors.
2. **Security Vulnerabilities**: High risk of SQL Injection attacks if inputs are not sanitized perfectly.
3. **Dialect Lock-in**: If you write PostgreSQL-specific SQL queries and later want to migrate to MySQL, you have to rewrite large portions of your codebase.

An ORM like Sequelize acts as a translation layer, allowing you to interact with databases using clean JavaScript code instead of raw SQL strings.

---

## 🧠 Core Concept
An **ORM (Object-Relational Mapper)** is a library that maps the concepts of Object-Oriented Programming (OOP) in your code to the concepts of Relational Databases (RDBMS).

| Relational Database Concept | OOP / JavaScript Concept |
| :--- | :--- |
| **Table** (e.g., `users` table) | **Model** (a JavaScript Class `User`) |
| **Row / Record** (a single user row in the table) | **Instance** of the Class (a specific `user` object) |
| **Column** (e.g., `email`, `age`) | **Property** / Attribute of the class (`user.email`, `user.age`) |
| **SQL Query** (e.g., `SELECT * FROM users`) | **Method call** (e.g., `User.findAll()`) |

Instead of writing SQL queries, you interact with your database using standard JavaScript classes, objects, and methods.

---

## 🏗 Mental Model / Internal Working
When you execute a command in Sequelize, a multi-step translation occurs:

1. **JavaScript Call**: You call a Sequelize method, such as `User.findByPk(1)`.
2. **Dynamic Generation**: Sequelize's internal engine translates this Javascript call into a parameterized SQL string: `SELECT id, name, email FROM users WHERE id = ?;`.
3. **Database Driver execution**: Sequelize sends the parameterized query and the parameters `[1]` to the low-level database driver (e.g., `mysql2` for MySQL, `pg` for PostgreSQL) over a network socket.
4. **Data Deserialization (Hydration)**: The database returns a raw row format (e.g. array of row-arrays or raw JSON). Sequelize wraps this raw data into rich JavaScript objects (Model instances) containing helper methods (like `.update()` or `.destroy()`) and returns it to your application.

---

## 🌍 Real-World Analogy
Imagine you are at an international restaurant. The Chef only speaks **SQL**. You only speak **JavaScript**. 
Instead of trying to speak a language you aren't fluent in (and risking miscommunication), you hire a Translator: the **ORM**.

* You say to the translator: *"Give me the record of user 5."*
* The translator turns around and tells the Chef in SQL: `SELECT * FROM users WHERE id = 5;`
* The Chef hands a tray of raw ingredients (raw database rows) to the translator.
* The translator formats the food beautifully on a plate with clean utensils (JavaScript object with helper methods) and hands it back to you.

---

## ⚙️ Syntax / API / Core Usage

### Raw SQL vs. Sequelize Comparison

Here is how code looks when querying a user from a database using raw SQL vs. Sequelize.

#### Approach A: Raw SQL (using `mysql2` driver)
```javascript
const mysql = require('mysql2/promise');

async function getUser(userId) {
  const connection = await mysql.createConnection(process.env.DATABASE_URL);
  // We must use parameterized inputs (?) to avoid SQL injection
  const query = 'SELECT id, username, email FROM users WHERE id = ?';
  const [rows] = await connection.execute(query, [userId]);
  
  if (rows.length === 0) return null;
  
  // Returns a plain JavaScript object representing the row
  const rawUser = rows[0]; 
  await connection.end();
  return rawUser;
}
```

#### Approach B: Sequelize ORM
```javascript
const User = require('./models/User');

async function getUser(userId) {
  // 1. Clean, readable method call
  // 2. Automatically sanitized to prevent SQL injection
  // 3. Connection is managed automatically via an internal pool
  const user = await User.findByPk(userId); 
  return user; // Returns a rich model instance
}
```

---

## 💻 Practical Examples

### Comparing Common Operations
Let's compare everyday operations to see the benefits of Sequelize.

#### 1. Creating a Record
* **Raw SQL**:
  ```sql
  INSERT INTO users (username, email, created_at, updated_at) 
  VALUES ('john_doe', 'john@example.com', NOW(), NOW());
  ```
* **Sequelize**:
  ```javascript
  const newUser = await User.create({
    username: 'john_doe',
    email: 'john@example.com'
  });
  ```

#### 2. Updating a Record
* **Raw SQL**:
  ```sql
  UPDATE users 
  SET email = 'john.new@example.com', updated_at = NOW() 
  WHERE id = 5;
  ```
* **Sequelize**:
  ```javascript
  const user = await User.findByPk(5);
  if (user) {
    user.email = 'john.new@example.com';
    await user.save(); // Sequelize generates and executes the UPDATE statement
  }
  ```

---

## 🔄 Flow Diagram

The diagram below shows the flow of an HTTP Request fetching data through Express and Sequelize:

```text
+-----------------------+
|  Client HTTP Request  |
+-----------+-----------+
            |
            v
+-----------------------+
|   Express Controller  |
|  Calls: User.findAll()|
+-----------+-----------+
            |
            v
+-----------------------+
|     Sequelize ORM     |
| Generates SQL Query   |
| "SELECT * FROM users;"|
+-----------+-----------+
            |
            v
+-----------------------+
|   DB Dialect Driver   |
|   (pg / mysql2 / etc) |
+-----------+-----------+
            |
            v
+-----------------------+
|    Database Server    |
|   (Postgres / MySQL)  |
+-----------------------+
```

---

## 🧪 Common Interview Questions

### Q1: What is the main difference between Active Record and Data Mapper patterns in ORMs?
* **Answer**: 
  * In the **Active Record** pattern (used by **Sequelize**), the model class represents both the data and the database behavior. The model instances contain operational database methods (e.g., `user.save()`, `user.destroy()`).
  * In the **Data Mapper** pattern (used by **Prisma** or **TypeORM**), models represent only the data structures (schemas). Database operations are performed using a separate manager/repository class (e.g., `db.user.save(user)`).

### Q2: Why would you choose Sequelize over a query builder like Knex.js?
* **Answer**: Sequelize provides a complete object layer out of the box, including schemas, data validations, lifecycle hooks, automatic handling of table associations (relationships), and database migrations. A query builder like Knex.js only helps write programmatic SQL strings, leaving the mapping, hooks, and relationships for you to implement manually.

### Q3: What is "Dialect" in Sequelize?
* **Answer**: A dialect represents the specific relational database system you are connecting to (such as `postgres`, `mysql`, `sqlite`, or `mssql`). Sequelize is written to be dialect-agnostic, meaning the core code is the same, but you configure a specific "dialect" so that Sequelize knows how to compile Javascript methods into the exact SQL grammar of your database.

---

## ⚠️ Common Mistakes / Pitfalls
* **Performance Overhead**: Sequelize adds a translation layer. For simple SELECT queries, raw SQL will always be slightly faster. For extremely performance-critical or high-throughput reporting, Sequelize can become a bottleneck due to the memory overhead of hydrating thousands of model instances.
* **Treating ORM as Magic**: Many beginners think that using an ORM means they don't need to learn SQL. This is a trap. Without understanding SQL, it is easy to write Sequelize queries that trigger hundreds of database calls in the background (known as the N+1 query problem).

---

## ✅ Best Practices
* **Keep SQL knowledge sharp**: Use Sequelize for standard CRUD, transactions, validation, and relationships, but do not hesitate to write optimized raw SQL queries (using `sequelize.query()`) for complex reporting, bulk operations, or heavy analytical queries.
* **Always check logs in development**: Enable SQL query logging (`logging: console.log`) in your local development config. This helps you monitor exactly what SQL Sequelize is generating in the background.

---

## 📝 Quick Recap
* An ORM (Object-Relational Mapper) translates object-oriented JavaScript code into relational database SQL queries.
* Sequelize maps Tables to Classes (Models), and Rows to Object Instances.
* Sequelize supports multiple databases (Postgres, MySQL, SQLite, etc.) using pluggable database drivers called "dialects".
* In development, always monitor the generated SQL query logs to prevent hidden performance issues.

---

## 🔗 Navigation
Previous : [00_index.md](./00_index.md) | Index : [00_index.md](./00_index.md) | Next : [02_sequelize_architecture_and_mental_model.md](./02_sequelize_architecture_and_mental_model.md)
