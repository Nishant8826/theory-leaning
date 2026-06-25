# 06. Basic CRUD Operations

## 🎯 Goal of This Chapter
By the end of this chapter, you will be able to perform standard Create, Read, Update, and Delete (CRUD) operations in database tables using Sequelize. You will learn the difference between class-level and instance-level operations and how to build functional Express controllers for REST APIs.

---

## 🤔 Why This Topic Matters
Almost all web applications spend the majority of their lifecycle executing CRUD operations: adding users, fetching blog posts, updating profile details, or deleting files. 

If you write CRUD operations poorly, you risk introducing bugs like:
* Sending incorrect HTTP status codes (e.g., returning 200 OK when a user was not found).
* Writing inefficient updates that overwrite columns with stale data.
* Writing unsafe code that throws unhandled promise rejections, crashing the Node process.

---

## 🧠 Core Concept
In Sequelize, CRUD operations are mapped directly to static Class methods on the Model, or instance methods on returned objects.

| CRUD Operation | Sequelize API Method | SQL Translation |
| :--- | :--- | :--- |
| **Create** | `Model.create({ data })` | `INSERT INTO ...` |
| **Read (All)** | `Model.findAll()` | `SELECT * FROM ...` |
| **Read (One)** | `Model.findByPk(id)` or `Model.findOne({ where })` | `SELECT ... LIMIT 1;` |
| **Update (Direct)** | `Model.update({ fields }, { where })` | `UPDATE ... WHERE ...` |
| **Update (Instance)**| `instance.save()` | `UPDATE ... WHERE id = ...` |
| **Delete (Direct)** | `Model.destroy({ where })` | `DELETE FROM ... WHERE ...` |
| **Delete (Instance)**| `instance.destroy()` | `DELETE FROM ... WHERE id = ...` |

---

## 🏗 Mental Model / Internal Working

### Hydration vs. Plain Data
When you run a read query like `User.findByPk(1)`:
1. Sequelize executes the SELECT query in SQL.
2. The database returns raw row data: `{ id: 1, name: "Alice", email: "alice@example.com" }`.
3. **Hydration Phase**: Sequelize instantiates a new `User` class object. It injects the raw database properties and appends special helper functions (like `.save()`, `.destroy()`, `.toJSON()`) onto the prototype of this object.
4. If you write `{ raw: true }` in the query options, Sequelize skips the hydration phase and returns a plain JavaScript object. This is faster and uses less memory, but the object won't have methods like `.save()`.

---

## 🌍 Real-World Analogy
Think of database records as **Rental Cars**:
* `Model.create()` is ordering a brand-new car to be built and delivered to the garage.
* `Model.findAll()` is getting a list of all active rentals.
* `Model.findByPk(id)` is requesting a specific car key. When you get the key, you get a fully functional car (a hydrated instance) with a steering wheel and pedals (`.save()`, `.destroy()`).
* If you ask for a **"raw"** car key (using `{ raw: true }`), they only show you a printed photograph of the car. You can see what it looks like, but you can't drive it (`.save()` will fail).

---

## ⚙️ Syntax / API / Core Usage

### Creating Records
`Model.create()` builds a new model instance and saves it to the database in one step.

```javascript
const user = await User.create({
  username: 'john_doe',
  email: 'john@example.com',
  password: 'hashedpassword123'
});
// 'user' is a fully hydrated Model instance
```

### Reading Records
```javascript
// Find all users
const users = await User.findAll(); // returns array []

// Find one user by Primary Key
const user = await User.findByPk(1); // returns instance or null

// Find user matching specific conditions
const userByEmail = await User.findOne({ where: { email: 'john@example.com' } });
```

### Updating Records
There are two ways to perform updates:

#### Approach A: Direct Model Update (Class Level)
Good for bulk updates or quick edits when you don't need the object data in code.

```javascript
const [affectedRows] = await User.update(
  { isActive: false },
  { where: { role: 'guest' } }
);
// Returns an array containing the number of affected rows.
// Does NOT return the modified user objects by default.
```

#### Approach B: Fetch and Save (Instance Level)
Best when you need to inspect the data, run validations, or trigger hooks before saving.

```javascript
const user = await User.findByPk(1);
if (user) {
  user.username = 'new_username';
  await user.save(); // Generates and runs UPDATE sql
}
```

### Deleting Records
```javascript
// Bulk / Direct delete
await User.destroy({ where: { isActive: false } });

// Instance-level delete
const user = await User.findByPk(1);
if (user) {
  await user.destroy();
}
```

---

## 💻 Practical Examples

### Creating an Express CRUD Controller
Here is how you write a clean, production-ready controller using Express and Sequelize models.

```javascript
// src/controllers/userController.js
const User = require('../models/User');

module.exports = {
  // 1. CREATE
  createUser: async (req, res) => {
    try {
      const { username, email, password } = req.body;
      const user = await User.create({ username, email, password });
      return res.status(201).json(user);
    } catch (error) {
      return res.status(400).json({ error: error.message });
    }
  },

  // 2. READ ALL
  getAllUsers: async (req, res) => {
    try {
      // Use raw: true for read-only index endpoints to boost performance
      const users = await User.findAll({ raw: true });
      return res.status(200).json(users);
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  },

  // 3. READ ONE
  getUserById: async (req, res) => {
    try {
      const user = await User.findByPk(req.params.id);
      if (!user) {
        return res.status(404).json({ message: 'User not found' });
      }
      return res.status(200).json(user);
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  },

  // 4. UPDATE
  updateUser: async (req, res) => {
    try {
      const user = await User.findByPk(req.params.id);
      if (!user) {
        return res.status(404).json({ message: 'User not found' });
      }
      // Update instance attributes dynamically
      await user.update(req.body); 
      return res.status(200).json(user);
    } catch (error) {
      return res.status(400).json({ error: error.message });
    }
  },

  // 5. DELETE
  deleteUser: async (req, res) => {
    try {
      const user = await User.findByPk(req.params.id);
      if (!user) {
        return res.status(404).json({ message: 'User not found' });
      }
      await user.destroy();
      return res.status(200).json({ message: 'User deleted successfully' });
    } catch (error) {
      return res.status(500).json({ error: error.message });
    }
  }
};
```

---

## 🔄 Flow Diagram

### CRUD Controller Execution Flow (READ ONE)

```text
 Client Request              Express Router          User Controller           Sequelize ORM           Database
 (GET /users/5)
       │                           │                        │                        │                     │
       │─────── HTTP GET ─────────>│                        │                        │                     │
       │                           │────── Call method ────>│                        │                     │
       │                           │       getUserById()    │─── User.findByPk(5) ──>│                     │
       │                           │                        │                        │─── SQL SELECT ─────>│
       │                           │                        │                        │    WHERE id = 5     │
       │                           │                        │                        │                     │
       │                           │                        │                        │<── Raw Row data ────│
       │                           │                        │                        │    {id: 5, ...}     │
       │                           │                        │<─ Hydrated Instance ───│                     │
       │                           │                        │   (User model object)  │                     │
       │                           │<──── Send JSON 200 ────│                        │                     │
       │                           │      { id: 5, ... }    │                        │                     │
       │<────── HTTP 200 OK ───────│                        │                        │                     │
```

---

## 🧪 Common Interview Questions

### Q1: What is the difference between `Model.update()` and `instance.update()`?
* **Answer**: 
  * `Model.update()` is a class method that performs a direct SQL update on the database without fetching records first. It returns only the number of affected rows and **does not trigger instance-level hooks** unless explicitly configured.
  * `instance.update()` runs on an already retrieved model instance, updates its local values, executes validations, triggers instance lifecycle hooks, saves to the database, and leaves the model instance updated in memory.

### Q2: What does `Model.findAll()` return if no records match the criteria?
* **Answer**: It returns an empty array `[]`. It does **not** return `null`. Therefore, you should check for empty arrays using `if (results.length === 0)` rather than simple truthy checks like `if (!results)`.

### Q3: How do you bypass model hydration in read operations?
* **Answer**: Pass the `{ raw: true }` option in the query configuration block. For example: `User.findAll({ raw: true })`. This returns plain database row objects rather than class instances, reducing CPU usage and memory footprint.

---

## ⚠️ Common Mistakes / Pitfalls
* **Wrong Truthy Checks for Arrays**: Writing `if (!users) { return 404; }` after calling `User.findAll()`. Since an empty array `[]` is truthy in JavaScript, the condition will be skipped, and the server will return an empty list with a 200 OK status instead of indicating no data exists.
* **Expecting Model.update to Return Data**: Expecting `const updatedUser = await User.update(...)` to return the updated record object. In MySQL (and SQLite), bulk updates do not support the `returning: true` option; it only returns the number of affected rows. If you need the updated object properties, you must query the record again.

---

## ✅ Best Practices
* **Use `{ raw: true }` for read-only listings**: If your endpoint simply lists data (e.g. products listing index) without editing it, use `raw: true` to optimize performance.
* **Return correct HTTP status codes**: 
  * `201 Created` for successful creations.
  * `404 Not Found` when a request target ID is missing.
  * `400 Bad Request` on validation errors.

---

## 📝 Quick Recap
* CRUD functions map directly to Sequelize class methods (`create`, `findAll`, `update`, `destroy`).
* Query results are hydrated into active model objects containing helper methods like `.save()` and `.destroy()`.
* `{ raw: true }` skips model hydration, improving performance for read-only endpoints.
* Class-level updates (`Model.update`) run direct queries and return count stats, whereas instance-level updates (`instance.update`) execute hooks and validate inputs before saving.

---

## 🔗 Navigation
Previous : [05_migrations_and_seeders_in_depth.md](./05_migrations_and_seeders_in_depth.md) | Index : [00_index.md](./00_index.md) | Next : [07_advanced_querying_filtering_and_operators.md](./07_advanced_querying_filtering_and_operators.md)
