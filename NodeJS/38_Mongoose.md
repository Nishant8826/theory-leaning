# Mongoose

## What You Will Learn
* What an Object Document Mapper (ODM) is and its performance overhead.
* Defining Mongoose Schemas, Models, and validation rules.
* Working with Mongoose Hooks (pre-save, post-save, pre-validate).
* Optimizing query performance using `.lean()` and select projections.
* Relational joins in MongoDB using `.populate()`.

## Why This Matters
Mongoose is the standard ODM for MongoDB in Node.js. It simplifies development by enforcing schemas and validation. However, Mongoose wraps query results in complex JavaScript Document objects containing virtuals, getters, setters, and state tracking. This overhead can slow down read operations. Knowing when to use optimizations like `.lean()` is key to building high-performance APIs.

## Theory

### What is an ODM?
An **Object Document Mapper (ODM)** is an abstraction layer that maps application objects (like JavaScript classes) to database documents. Mongoose provides:
* **Schema Enforcement**: Enforces consistent fields and types on MongoDB's schema-less collections.
* **Built-in Validation**: Validates fields (like email formats or string lengths) before writing to the database.
* **Middleware Hooks**: Runs custom functions automatically before or after database actions (e.g. hashing a password before saving a user).

### Mongoose Document Wrapping Overhead
When you execute a query (like `User.find()`), Mongoose does not return raw JSON data. It returns an array of complex **Mongoose Documents**. Each document contains internal state properties, getters, setters, and change-tracking systems. 
This wrapping process consumes CPU cycles and memory. For read-heavy API routes where you only need to return JSON to the client, wrapping documents is unnecessary overhead.

## Deep Dive

### Optimizing with `.lean()`
The `.lean()` method tells Mongoose to bypass the Document wrapping step and return raw, plain JavaScript objects directly from the MongoDB driver.
* **Performance**: Lean queries are up to **4x faster** and consume significantly less memory.
* **Trade-off**: Plain JavaScript objects do not support Mongoose features like virtuals, custom methods, or `.save()`. Use `.lean()` for read-only query paths (like GET routes), and standard Mongoose queries when you need to update or save documents.

### Mongoose Middleware (Hooks)
Hooks allow you to execute logic at specific stages of a document's lifecycle:
* **`pre('save')`**: Runs before a document is written to the database. Ideal for hashing passwords or generating slugs.
* **`pre('validate')`**: Runs before validation rules are evaluated.

## Visual Explanation

### Mongoose Query Pipeline: Standard vs. Lean Query
```text
  [ Client Request: User.find() ]
                 │
                 ▼
     [ Fetch BSON from MongoDB ]
                 │
                 ├─────────── Using .lean()?
                 │                 │
                 │                 ├── YES ──> [ Plain JavaScript Object ] ──> res.json() (Fast!)
                 │                 │
                 │                 └── NO  ──> [ Instantiate Mongoose Document ] (High Memory Cost)
                 ▼                                  │ (Appends virtuals, change-trackers, hooks)
  [ Mongoose Document Array ] ──────────────────────┘
```

## Real-World Example
Consider a user registration schema. You define validation rules to ensure usernames are required and passwords are at least 8 characters. You write a `pre('save')` hook to automatically hash the user's password before writing the record to the database. This ensures passwords are encrypted without cluttering the registration controller code.

## Code Examples

### Schemas, Validation, Hooks, and Lean Query Performance

```javascript
// models/User.js
// Dependency required: npm install mongoose bcrypt
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const UserSchema = new mongoose.Schema({
  username: {
    type: String,
    required: [true, 'Username is required'],
    trim: true,
    minlength: [3, 'Username must be at least 3 characters']
  },
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    match: [/^\S+@\S+\.\S+$/, 'Please use a valid email address']
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: 8
  }
}, {
  timestamps: true // Automatically manages 'createdAt' and 'updatedAt'
});

// 1. Pre-Save Hook (Hash password automatically before saving)
UserSchema.pre('save', async function(next) {
  // Only hash the password if it has been modified or is new
  if (!this.isModified('password')) return next();

  try {
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (err) {
    next(err);
  }
});

// 2. Custom instance method on the Document
UserSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', UserSchema);
```

```javascript
// controllers/userController.js
const User = require('../models/User');

// GET /users - High-performance read-only query
exports.getUsers = async (req, res, next) => {
  try {
    const users = await User.find()
      .select('-password') // Exclude password field (projection)
      .lean();             // Return plain JavaScript objects for maximum speed

    res.status(200).json(users);
  } catch (err) {
    next(err);
  }
};
```

## Best Practices
* **Always Use `.lean()` for Reads**: Always append `.lean()` to queries inside read-only GET routes to improve response speeds and reduce memory usage.
* **Use Projections**: Use `.select()` to exclude fields you do not need (like passwords or heavy metadata arrays) from database queries.
* **Handle Index Errors**: Mongoose's `unique` validator relies on MongoDB unique indexes. Listen for MongoDB code `11000` (duplicate key error) inside your error handlers to return clean validation responses to the client.

## Interview Questions

### Beginner
* **What is Mongoose and why is it used?**
  *Answer*: Mongoose is an Object Document Mapper (ODM) for MongoDB and Node.js. It is used to enforce schema validation, define model constraints, and run lifecycle hooks (like pre-save logic) on MongoDB's schema-less collections.

### Intermediate
* **What is Mongoose middleware (hooks), and when would you use a `pre('save')` hook?**
  *Answer*: Mongoose hooks are functions that run automatically before or after specific lifecycle events (like save, validate, or delete). You use a `pre('save')` hook to perform tasks automatically before writing data to the database, such as hashing passwords or generating slug fields.

### Advanced
* **Explain how Mongoose's `.lean()` option improves application performance. What are the limitations of using it?**
  *Answer*: By default, Mongoose wraps query results in complex Document objects containing virtuals, change-trackers, and custom methods. The `.lean()` method bypasses this wrapping step, returning plain JavaScript objects instead. This improves query performance up to 4x and reduces memory overhead. 
  The limitation is that the returned objects are read-only; they do not support Mongoose features like virtuals, custom methods, change tracking, or calling `.save()`.

### Senior Architect
* **In a high-throughput read-heavy API, explain why Mongoose's `.populate()` method can cause severe database bottlenecks, and discuss how you optimize relational querying in MongoDB.**
  *Answer*: Mongoose's `.populate()` method does not perform join operations at the database level (since MongoDB lacks native relational joins). Instead, Mongoose executes a separate `find()` query behind the scenes for every populated reference ID returned in the original query. If you query 100 documents and populate 2 fields on each, Mongoose can execute up to 201 database queries, degrading API latency.
  
  To optimize relational queries:
  1. Use MongoDB's native **Aggregation Pipeline** with the `$lookup` operator. This performs the join operation on the database server in a single query, which is much faster.
  2. **Denormalize Data**: Embed frequently accessed relational data directly inside the document (e.g. storing a user's name directly in the order document) if the data does not change frequently, eliminating the need to query or populate it.
  3. Cache populated results in a fast key-value store like Redis to avoid hitting the database for duplicate requests.

---
Previous : [37_MongoDB.md] | Index : [00_index.md] | Next : [39_PostgreSQL.md]
