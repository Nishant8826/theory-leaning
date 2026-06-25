# 13. Model Methods and Advanced Patterns

## 🎯 Goal of This Chapter
By the end of this chapter, you will understand how to encapsulate business logic inside models using custom **Instance Methods** and **Class Methods**. You will also learn how to structure large-scale Express applications using the **Service and Repository Patterns** to decouple database operations from HTTP routing controllers.

---

## 🤔 Why This Topic Matters
In basic applications, developers call Sequelize methods (like `User.findOne`) directly inside Express controllers. As applications grow, this causes:
1. **Fat Controllers**: Controllers contain HTTP routing logic, database queries, and business calculations, making them long and hard to test.
2. **Coupled Code**: If you change how you fetch a user, you must modify multiple controllers.
3. **Leaked Secrets**: Forgetting to manually delete passwords from query results before sending responses.

Encapsulating logic in custom model methods and separating your architecture into Service/Repository layers keeps your code clean, modular, and easy to unit test.

---

## 🧠 Core Concept

### 1. Custom Model Methods

#### Instance Methods (Row Level)
* Functions that operate on a specific instance (a single database row).
* They have access to **`this`**, which points to the current object's data values.
* Examples: Generating full names, comparing password hashes, or formatting responses.

#### Class Methods (Table Level)
* Static functions defined on the model class itself.
* They have access to the class context, allowing you to run queries.
* Examples: Finding all admins, searching records by customized scopes, or batch creations.

### 2. Service and Repository Architecture

```text
+---------------------+
|    HTTP Request     |
+----------+----------+
           |
           v
+---------------------+
|  Express Controller |  <-- Validates HTTP inputs, handles status codes
+----------+----------+
           |
           v
+---------------------+
|    Service Layer    |  <-- Enforces business rules (transactions, emails)
+----------+----------+
           |
           v
+---------------------+
|  Repository Layer   |  <-- Executes raw database operations via Sequelize
+----------+----------+
           |
           v
+---------------------+
|   Sequelize Model   |  <-- Model definitions, validations, hooks
+---------------------+
```

---

## 🏗 Mental Model / Internal Working
* **Instance Methods** are added to the prototype of the Model class. When Sequelize hydrates raw rows into instances, these methods become available on the returned object.
* **Class Methods** are defined as static class methods. Inside a static method, `this` refers to the class itself, so calling `this.findOne` executes Sequelize's standard querying engine.
* **The Service/Repository split**:
  * The Repository does not care about Express, req, res, or business logic. It only translates inputs into queries (e.g. `UserRepository.getById(id)`).
  * The Service does not care about SQL. It handles business flows (e.g., check if user exists -> hash password -> register -> send email).

---

## ⚙️ Syntax / API / Core Usage

### Custom Methods with ES6 Class syntax
```javascript
const { Model, DataTypes } = require('sequelize');
const bcrypt = require('bcrypt');
const sequelize = require('../config/database');

class User extends Model {
  // 1. Class Method (static keyword)
  static async findActiveAdmins() {
    return await this.findAll({
      where: { role: 'admin', isActive: true }
    });
  }

  // 2. Instance Method (standard class method)
  // CRITICAL: NEVER use arrow functions here, as they do not bind 'this'
  async comparePassword(plainPassword) {
    return await bcrypt.compare(plainPassword, this.password);
  }

  // 3. Overriding default JSON serialization (Instance Method override)
  // Automatically called when res.json() serialization occurs
  toJSON() {
    const values = { ...this.get() };
    delete values.password; // Strip the sensitive password field automatically!
    return values;
  }
}
```

---

## 💻 Practical Examples

### Building a Service + Repository Pipeline
Let's build a clean user registration flow.

#### Step 1: The Repository Layer
Handles direct database interactions.

```javascript
// src/repositories/userRepository.js
const User = require('../models/User');

class UserRepository {
  async findByEmail(email) {
    return await User.findOne({ where: { email } });
  }

  async findById(id) {
    return await User.findByPk(id);
  }

  async create(userData) {
    return await User.create(userData);
  }
}

module.exports = new UserRepository();
```

#### Step 2: The Service Layer
Contains core business rules. Free of HTTP inputs (`req.body`).

```javascript
// src/services/userService.js
const userRepository = require('../repositories/userRepository');

class UserService {
  async registerUser(userData) {
    // 1. Enforce business rule: Email uniqueness check
    const existingUser = await userRepository.findByEmail(userData.email);
    if (existingUser) {
      throw new Error('Email is already registered.');
    }

    // 2. Persist user via repository
    const user = await userRepository.create(userData);

    // 3. Perform external actions (safe from transactions)
    // await emailService.sendWelcomeEmail(user.email);

    return user;
  }
}

module.exports = new UserService();
```

#### Step 3: The Controller Layer
Interacts with Express routes, processes status codes, and parses parameters.

```javascript
// src/controllers/userController.js
const userService = require('../services/userService');

module.exports = {
  register: async (req, res) => {
    try {
      const { username, email, password } = req.body;
      
      // Delegate all business logic to the service
      const user = await userService.registerUser({ username, email, password });
      
      // user.toJSON() is automatically invoked inside res.json()
      return res.status(201).json({ status: 'success', data: user });
    } catch (error) {
      return res.status(400).json({ status: 'fail', message: error.message });
    }
  }
};
```

---

## 🔄 Flow Diagram

### Service/Repository Flow Chart

```text
HTTP Client              Controller                Service                 Repository                 Database
    │                        │                        │                        │                         │
    │─── POST /register ────>│                        │                        │                         │
    │    {email, ...}        │─── registerUser() ────>│                        │                         │
    │                        │    (Business checks)   │─── findByEmail() ─────>│                         │
    │                        │                        │                        │─── SQL SELECT ─────────>│
    │                        │                        │                        │<── null (not exists) ───│
    │                        │                        │<── null ───────────────│                         │
    │                        │                        │─── create() ──────────>│                         │
    │                        │                        │                        │─── SQL INSERT ─────────>│
    │                        │                        │                        │<── Hydrated User Row ───│
    │                        │                        │<── User Instance ──────│                         │
    │                        │<── User Instance ──────│                        │                         │
    │                        │    (Strip password via │                        │                         │
    │                        │     toJSON serialization)                       │                         │
    │<── Response 201 ───────│                        │                        │                         │
```

---

## 🧪 Common Interview Questions

### Q1: What is the main difference between an instance method and a class method?
* **Answer**: 
  * An **instance method** is defined on the class prototype and runs on a single retrieved database record (e.g. `user.comparePassword()`). Inside, `this` refers to the specific instance's columns.
  * A **class method** is defined as static and runs on the model class itself without loading a specific record first (e.g., `User.findActiveAdmins()`). Inside, `this` refers to the model class, allowing queries like `this.findAll()`.

### Q2: Why shouldn't you use arrow functions `() => {}` when writing model methods?
* **Answer**: Arrow functions do not bind their own `this` context. Instead, they capture the `this` value of the enclosing lexical scope. If you use an arrow function for an instance method, `this` will be undefined or point to the global exports object, making it impossible to access instance variables like `this.password` or `this.email`.

### Q3: What is the benefit of overriding the `toJSON` method inside a model?
* **Answer**: Overriding `toJSON` centralizes response security. Whenever an Express controller sends a model instance back to a client using `res.json(user)`, Express automatically stringifies the object, calling `toJSON()`. Stripping sensitive fields (like `password`, `salt`, or `verificationToken`) inside `toJSON` ensures you never leak secrets in API responses, even if a developer forgets to exclude them in controllers.

---

## ⚠️ Common Mistakes / Pitfalls
* **Arrow Functions**: Defining instance methods using arrow functions, causing `this.attribute` to throw runtime undefined errors.
* **Leaking Database Secrets**: Forgetting to strip password fields from models. Always override `toJSON` on models holding sensitive data.

---

## ✅ Best Practices
* **Keep Repositories Focused on Queries**: Do not write business logic inside repository files. Repositories should only receive variables, execute queries, and return raw or hydrated data.
* **Keep Services Free of HTTP Concepts**: Never pass Express `req`, `res`, or `next` objects into service methods. Services should only receive plain JS inputs, allowing them to be run inside CLI tasks, test suites, or cron jobs without HTTP mock frameworks.

---

## 📝 Quick Recap
* Class methods (static) operate on the entire table; instance methods operate on individual rows.
* Never use arrow functions for model methods because they don't bind `this`.
* Override `toJSON()` in models to automatically remove sensitive fields (like passwords) from API responses.
* Decouple large apps: Route -> Controller (HTTP validation) -> Service (business logic) -> Repository (Sequelize queries) -> Database.

---

## 🔗 Navigation
Previous : [12_paranoid_tables_and_scopes.md](./12_paranoid_tables_and_scopes.md) | Index : [00_index.md](./00_index.md) | Next : [14_error_handling_and_production_practices.md](./14_error_handling_and_production_practices.md)
