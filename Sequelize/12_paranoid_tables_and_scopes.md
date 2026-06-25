# 12. Paranoid Tables and Scopes

## 🎯 Goal of This Chapter
By the end of this chapter, you will know how to implement soft deletes using Sequelize **Paranoid tables**, query and restore deleted records, and define reusable query configurations called **Scopes** (including default and named scopes).

---

## 🤔 Why This Topic Matters
In production apps, permanently deleting data using raw `DELETE` queries is highly risky. If a user accidentally deletes a project or an admin deletes an invoice, there is no way to recover it. Furthermore, deleting records breaks database relationships and analytic histories. **Soft deletes** solve this by hiding records from normal view while retaining them in the database.

Additionally, you often write the same query filters repeatedly, such as only fetching "active" products or "verified" users. Writing this logic in every controller violates the DRY (Don't Repeat Yourself) principle. **Scopes** let you package and reuse query logic cleanly inside the model itself.

---

## 🧠 Core Concept

### 1. Paranoid Tables (Soft Delete)
* When you call `instance.destroy()` on a paranoid model, Sequelize does **not** delete the row. Instead, it records a timestamp in a special **`deletedAt`** column.
* Standard select queries automatically ignore soft-deleted rows.
* You can bypass this filter using `{ paranoid: false }` or restore records using `instance.restore()`.

### 2. Scopes
* A **Scope** is a pre-defined set of query options (like `where`, `include`, `attributes`, or `limit`) configured inside the model definitions.
* **Default Scope**: Automatically merged into **every** query run on that model (unless bypassed).
* **Named Scopes**: Custom, named filter blocks applied programmatically using `.scope('scopeName')`.

---

## 🏗 Mental Model / Internal Working

### How Paranoid Queries Compile to SQL
When `paranoid: true` is enabled on the model:
* Calling `post.destroy()` compiles to:
  ```sql
  UPDATE posts SET deletedAt = NOW() WHERE id = 1;
  ```
* Calling `Post.findAll()` compiles to:
  ```sql
  SELECT id, title FROM posts WHERE deletedAt IS NULL;
  ```
* Calling `Post.findAll({ paranoid: false })` compiles to:
  ```sql
  SELECT id, title FROM posts; -- Includes deleted records
  ```

---

## 🌍 Real-World Analogy
* **Soft Delete** is like throwing a paper document into the **Office Recycle Bin**. It is no longer on your desk (hidden from normal work queries), but it still exists. If you change your mind, you can reach into the bin and put it back on your desk (restore it). A **Hard Delete** is putting that paper document into an **Incinerator** (permanent loss).
* **Scopes** are like **Pre-Configured Instagram Filters**: instead of manually adjusting brightness, contrast, and warmth (writing `where`, `limit`, `order`) for every photo you take, you press the "Vintage" button (custom scope), and it applies all settings instantly.

---

## ⚙️ Syntax / API / Core Usage

### Configuring Paranoid and Scopes in Models

```javascript
// src/models/Post.js
const { Model, DataTypes } = require('sequelize');
const sequelize = require('../config/database');

class Post extends Model {}

Post.init({
  title: DataTypes.STRING,
  content: DataTypes.TEXT,
  status: DataTypes.ENUM('draft', 'published'),
  views: DataTypes.INTEGER
}, {
  sequelize,
  modelName: 'Post',
  tableName: 'posts',
  
  // 1. Enable Soft Deletes (Requires timestamps: true)
  timestamps: true,
  paranoid: true, // Automatically manages a 'deletedAt' column
  
  // 2. Define Scopes
  defaultScope: {
    where: {
      status: 'published' // By default, only query published posts
    }
  },
  scopes: {
    popular: {
      where: {
        views: { [sequelize.Sequelize.Op.gt]: 1000 }
      }
    },
    recent: {
      order: [['createdAt', 'DESC']]
    }
  }
});

module.exports = Post;
```

---

## 💻 Practical Examples

### Example 1: Soft Delete, Querying, and Restoring
Let's see how paranoid records are created, queried, and restored.

```javascript
// src/demo.js
const Post = require('./models/Post');

async function runDemo() {
  // 1. Create a post (Default scope will find it because it is published)
  const post = await Post.create({ title: 'Sequelize Tips', status: 'published', views: 50 });
  
  // 2. Soft delete the post
  await post.destroy(); // Sets deletedAt to current timestamp
  
  // 3. Normal queries will NOT find it
  const foundPost = await Post.findByPk(post.id);
  console.log(foundPost); // null
  
  // 4. Query including deleted records
  const deletedPost = await Post.findByPk(post.id, { paranoid: false });
  console.log(deletedPost.title); // 'Sequelize Tips'
  
  // 5. Restore the soft-deleted post
  await deletedPost.restore(); // Sets deletedAt back to null
  
  const restoredPost = await Post.findByPk(post.id);
  console.log(restoredPost !== null); // true (It is back!)
}
```

### Example 2: Querying with Scopes
Let's look at combining named scopes to build cleaner query patterns.

```javascript
// 1. Queries only published posts (due to defaultScope)
const published = await Post.findAll();

// 2. Bypass defaultScope to fetch draft posts too
const allPosts = await Post.unscoped().findAll();

// 3. Use a named scope
const popularPosts = await Post.scope('popular').findAll();

// 4. Chain multiple named scopes together
// Fetch posts that are both popular AND ordered from newest to oldest
const popularAndRecent = await Post.scope(['popular', 'recent']).findAll();
```

---

## 🔄 Flow Diagram

### Scope Query Resolution Flow

```text
                     Call: Post.scope('popular').findAll()
                                       │
                                       ▼
                             Lookup Scopes Metadata:
                             - Merge 'defaultScope' where properties
                             - Merge 'popular' scope where properties
                                       │
                                       ▼
                             Combine Query Objects:
                             where: { 
                               status: 'published',  <-- (Default scope)
                               views: { [Op.gt]: 1000 } <-- (Popular scope)
                             }
                                       │
                                       ▼
                               Add Paranoid Filter:
                               deletedAt IS NULL     <-- (Auto paranoid filter)
                                       │
                                       ▼
                              Compile SQL Query:
                     "SELECT * FROM posts WHERE status='published' 
                      AND views > 1000 AND deletedAt IS NULL;"
```

---

## 🧪 Common Interview Questions

### Q1: What column must be present in the database table to support paranoid models?
* **Answer**: The database table must contain a nullable datetime/timestamp column named `deletedAt` (case-sensitive by default). This must be declared in both the Sequelize model configuration and the corresponding database migration files.

### Q2: How do you perform a permanent (hard) delete on a paranoid model?
* **Answer**: Pass the `{ force: true }` option inside the destroy configuration block. For example: `await post.destroy({ force: true })` or `await Post.destroy({ where: { id: 1 }, force: true })`. This generates a raw SQL `DELETE FROM` query instead of an `UPDATE` statement.

### Q3: How do you bypass all scopes (including defaultScope) on a model query?
* **Answer**: Call the static class method `.unscoped()` before your query execution. For example: `const users = await User.unscoped().findAll();`.

---

## ⚠️ Common Mistakes / Pitfalls
* **Missing Migration Column**: Enabling `paranoid: true` on a model, but forgetting to define the `deletedAt` column in the migration file. When you try to delete a record, Sequelize attempts to update a non-existent column, throwing an SQL syntax error.
* **DefaultScope Side-Effects**: Over-complicating `defaultScope` (e.g. including relations or ordering by default). This default scope also applies to update, delete, and find queries inside your associations. If you try to update a record that is filtered out by the defaultScope, Sequelize will throw a "Record not found" error.

---

## ✅ Best Practices
* **Keep `defaultScope` Simple**: Limit `defaultScope` to basic status filtering (like `isActive: true` or `isDeleted: false`). Avoid adding ordering or eager loads (`include`) in default scopes, as it makes customization and overrides extremely difficult in complex endpoints.
* **Use Paranoid for Auditable Data**: Apply soft deletes to critical business records (Users, Transactions, Invoices) but avoid them on temporary records or simple junction tables to prevent bloated database tables.

---

## 📝 Quick Recap
* Paranoid tables enable soft deletes, setting a `deletedAt` timestamp instead of deleting rows.
* Normal read queries automatically filter out soft-deleted records.
* Query paranoid records using `{ paranoid: false }` and restore them using `instance.restore()`.
* Scopes encapsulate reusable query logic. `defaultScope` runs automatically, while named scopes are called using `.scope('name')`.

---

## 🔗 Navigation
Previous : [11_transactions_in_depth.md](./11_transactions_in_depth.md) | Index : [00_index.md](./00_index.md) | Next : [13_model_methods_and_advanced_patterns.md](./13_model_methods_and_advanced_patterns.md)
