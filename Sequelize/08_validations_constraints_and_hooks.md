# 08. Validations, Constraints, and Hooks

## 🎯 Goal of This Chapter
By the end of this chapter, you will understand the difference between database-level constraints and model-level validations in Sequelize. You will learn to implement custom validations and use model lifecycle hooks (triggers) to automate database tasks, such as hashing passwords with `bcrypt`.

---

## 🤔 Why This Topic Matters
Ensuring data integrity is one of the most critical responsibilities of a backend engineer. If invalid data enters your database (like a missing email address or a plain-text password), your application will suffer from logic errors, security breaches, and analytical inaccuracies.

Additionally, backend development involves recurring actions: whenever a user registers, we must hash their password, format their email to lowercase, or log their activity. Manually repeating this logic in every controller introduces boilerplate and risks. **Hooks** automate these actions at the database lifecycle level.

---

## 🧠 Core Concept

### 1. Model-Level Validations (JavaScript Level)
* These are checks executed in **Node.js** memory **before** Sequelize compiles or sends any SQL query to the database.
* Examples: Checking if a string is a valid email format, verifying a password length, or ensuring a string doesn't contain forbidden words.
* If a model validation fails, Sequelize stops execution immediately, throws an error, and **never sends a query to the database**. This saves network and database resources.

### 2. Database-Level Constraints (Database Level)
* These are rules enforced by the **RDBMS (MySQL / PostgreSQL)** server itself.
* Examples: `allowNull: false` (NOT NULL constraint), `unique: true` (Unique index constraint), or foreign keys.
* The query is sent to the database. If a rule is violated, the database rejects the write, rolls back the change, and sends an error back, which Sequelize wraps in a JavaScript error class (like `UniqueConstraintError`).

### 3. Model Lifecycle Hooks
* **Hooks** (also known as database triggers) are callback functions that run before or after specific events occur in a model instance's lifecycle (e.g. before validating, after creating, before saving).

---

## 🏗 Mental Model / Internal Working

### The Model Lifecycle Execution Order
When you save a model instance (`user.save()`), Sequelize follows a strict, sequential pipeline:

```text
1. User calls user.save()
       │
       ▼
2. Trigger: beforeValidate()
       │
       ▼
3. Execution: Run Model-Level Validations
       │
       ├─ [Validation Fails] ──> Throw ValidationError (Process Stops)
       └─ [Validation Passes] 
       │
       ▼
4. Trigger: afterValidate()
       │
       ▼
5. Trigger: beforeCreate() / beforeUpdate()  <-- (e.g., Hash Password here)
       │
       ▼
6. Execution: Run Database-Level Constraints (Not Null, Unique, etc.)
       │
       ├─ [Constraint Fails] ──> DB Rolls Back ──> Throw UniqueConstraintError
       └─ [Constraint Passes]
       │
       ▼
7. Trigger: afterCreate() / afterUpdate()    <-- (e.g., Send confirmation email)
```

---

## 🌍 Real-World Analogy
Think of data verification as entering a **High-Security Building**:
* **Model-Level Validations** are the **Security Guards at the entrance gate**. They verify that you have a badge and are wearing proper clothes before letting you step onto the property. If you fail, they send you away before you even walk through the door.
* **Database-Level Constraints** are the **Biometric Scanners at the vault door** inside. They verify that your fingerprints match the registry index. If it fails, the alarms sound, and you are locked out of the vault.
* **Hooks** are the **Smart Sensors** in the hallway: as you pass through the gate, the lights turn on automatically (`beforeValidate`), and when you successfully open the vault, a log is written to the system registry (`afterCreate`).

---

## ⚙️ Syntax / API / Core Usage

### Field Validations and Custom Validators
You define validations under the `validate` key inside the attribute definition block.

```javascript
const { Model, DataTypes } = require('sequelize');
const sequelize = require('../config/database');

class User extends Model {}

User.init({
  email: {
    type: DataTypes.STRING,
    allowNull: false, // Database-level constraint
    validate: {
      isEmail: true, // Model-level validator (verifies format)
    }
  },
  username: {
    type: DataTypes.STRING,
    validate: {
      // Custom inline validator function
      isNotBlacklisted(value) {
        const blacklist = ['admin', 'root', 'superuser'];
        if (blacklist.includes(value.toLowerCase())) {
          throw new Error('This username is not allowed.');
        }
      }
    }
  }
}, { sequelize, modelName: 'User' });
```

---

## 💻 Practical Examples

### Example: Auto-Hashing Passwords with Lifecycle Hooks
Here is how you use `bcrypt` to hash passwords automatically before they are saved to the database. We use the `beforeSave` hook, which triggers on both `create` and `update` events.

```javascript
// src/models/User.js
const { Model, DataTypes } = require('sequelize');
const bcrypt = require('bcrypt');
const sequelize = require('../config/database');

class User extends Model {}

User.init({
  username: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      len: {
        args: [8, 100],
        msg: 'Password must be at least 8 characters long.'
      }
    }
  }
}, {
  sequelize,
  modelName: 'User',
  tableName: 'users',
  
  // Register lifecycle hooks here
  hooks: {
    beforeSave: async (user, options) => {
      // Only hash password if it has been modified or is new
      if (user.changed('password')) {
        const salt = await bcrypt.genSalt(10);
        user.password = await bcrypt.hash(user.password, salt);
      }
    }
  }
});

module.exports = User;
```

---

## 🧪 Common Interview Questions

### Q1: What is the difference between `allowNull: false` and the `notNull` validator in Sequelize?
* **Answer**: 
  * `allowNull: false` is a database-level configuration. It generates a `NOT NULL` constraint on the SQL table, meaning the database server itself will reject queries containing null values.
  * The `notNull` validator is a model-level Javascript validator. If used, Sequelize runs a check in memory. To run correctly, `allowNull: false` should be set alongside it so that Sequelize generates both the DB constraint and the JS check.

### Q2: Why won't single-instance hooks (like `beforeCreate` or `beforeUpdate`) run during bulk queries like `User.update()`?
* **Answer**: By default, bulk operations (like `User.update()` or `User.destroy()`) run as a single direct SQL query across the database to optimize performance. Since individual records are not loaded/hydrated in memory, Sequelize cannot run individual instance callbacks. To run hooks for bulk queries, you must set `{ individualHooks: true }` in the query options, which forces Sequelize to fetch each instance individually and run its hooks (which degrades performance).

### Q3: What is the purpose of `user.changed('columnName')` inside a hook?
* **Answer**: It is a utility method that checks whether the value of a column was modified since the record was last fetched. In password hashing hooks, checking `user.changed('password')` prevents the app from hashing an already-hashed password hash again during routine profile updates (such as changing an email or username).

---

## ⚠️ Common Mistakes / Pitfalls
* **Ignoring Asynchronous Behavior in Hooks**: Writing `beforeCreate: (user) => { bcrypt.hash(user.password, 10).then(h => user.password = h) }` without using `async/await` or returning the promise chain. Because the function returns immediately, Sequelize proceeds to write the user record to the database before the asynchronous hashing task completes, saving the password as plain text!
* **Overusing hooks for external services**: Initiating external HTTP requests (like sending welcome emails or stripe checkouts) inside database hooks. If the database transaction rolls back due to a constraint error, your external request has already been sent, leading to database inconsistencies.

---

## ✅ Best Practices
* **Use hooks only for database operations**: Keep database hooks focused on modifying and formatting data (like hashing passwords, downcasing emails, or auto-generating slugs). Send emails or process payments in your Express service layers, **after** the database transaction has successfully committed.
* **Write custom validations for business logic**: Use the `validate` block for field-specific format checks, keeping your Express controller code clean and readable.

---

## 📝 Quick Recap
* Model-level validations run in JS memory before SQL is sent. If they fail, no queries hit the database.
* Database-level constraints are rules checked by the RDBMS itself during query execution.
* Hooks are callbacks that automate tasks at specific lifecycle events (like `beforeSave`).
* Bulk queries (like `User.update`) bypass individual instance hooks unless you explicitly configure `{ individualHooks: true }`.

---

## 🔗 Navigation
Previous : [07_advanced_querying_filtering_and_operators.md](./07_advanced_querying_filtering_and_operators.md) | Index : [00_index.md](./00_index.md) | Next : [09_associations_and_relationships.md](./09_associations_and_relationships.md)
