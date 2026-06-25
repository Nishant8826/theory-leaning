# 10. Eager and Lazy Loading

## 🎯 Goal of This Chapter
By the end of this chapter, you will understand the difference between Eager Loading and Lazy Loading. You will learn how to query associated tables using the `include` option, handle nested includes, filter associations, and analyze and resolve the performance-killing **N+1 query problem**.

---

## 🤔 Why This Topic Matters
When querying database associations (like articles and their comments), how you fetch data determines your application's performance. 

If you use **Lazy Loading** inside a loop, your application will execute one query to fetch the articles, and then *separate queries for every single article* to fetch its comments. If you have 100 articles, this triggers **101 database queries** (N+1 query problem), which slows down your database server and increases API latency. Knowing how and when to use **Eager Loading** is essential for backend optimization.

---

## 🧠 Core Concept

### 1. Lazy Loading (Fetch Later)
* Lazy loading fetches the primary data first. Associated data is loaded **only when you explicitly request it** by calling generated helper methods (like `user.getPosts()`).
* It runs multiple SQL queries sequentially.

### 2. Eager Loading (Fetch Together)
* Eager loading fetches the primary data and the associated data **together in a single query** using SQL `JOIN` statements.
* In Sequelize, this is achieved using the **`include`** option inside the query settings block.

### 3. The N+1 Query Problem
* This occurs when an application runs 1 query to fetch parent records (N records), and then runs N individual sub-queries to fetch child records for each parent.
* **Formula**: 1 initial query + N child queries = N+1 total queries.

---

## 🏗 Mental Model / Internal Working

### SQL Joins Behind the Scenes
* When you call `User.findAll({ include: [Post] })` (Eager Loading), Sequelize generates a single SQL query using a `LEFT OUTER JOIN`:
  ```sql
  SELECT users.id, posts.id AS "posts.id", posts.title AS "posts.title"
  FROM users
  LEFT OUTER JOIN posts ON users.id = posts.userId;
  ```
* The database returns a single combined dataset. Sequelize parses this set and nests the posts inside their corresponding user object array in memory.

---

## 🌍 Real-World Analogy
Think of ordering **Fast Food**:
* **Eager Loading**: You order a Burger, Fries, and a Soda together at the register. The cashier hands you everything on one single tray (one trip).
* **Lazy Loading / N+1**: You order a Burger. You sit down, realize you want Fries, so you walk back to the register and order them. You sit down again, realize you are thirsty, so you walk back a third time to order a Soda. 
  If you are ordering food for 10 friends (N = 10) and do this for each friend individually, you will walk back and forth to the counter 11 times (N+1 trips), frustrating the cashier and wasting time.

---

## ⚙️ Syntax / API / Core Usage

### Eager Loading with `include`
To retrieve posts written by a user in one query:

```javascript
const User = require('./models/User');
const Post = require('./models/Post');

const users = await User.findAll({
  include: [{
    model: Post,
    as: 'posts', // Matches the alias declared in model associations
    attributes: ['id', 'title'] // Projection: Fetch only ID and title
  }]
});
```

### Lazy Loading with Getters
Retrieve a user, and then retrieve their posts later:

```javascript
const user = await User.findByPk(1);

// Lazy load posts when needed
const posts = await user.getPosts(); // Triggers a separate SQL SELECT query
```

---

## 💻 Practical Examples

### 1. Triggering the N+1 Query Problem (Bad Code)
Here is code that triggers the N+1 query problem during an API call.

```javascript
// src/controllers/userController.js (INCORRECT / SLOW PATTERN)
const User = require('../models/User');

module.exports = {
  getUsersAndPostsSlow: async (req, res) => {
    // 1 Query executed: SELECT * FROM users;
    const users = await User.findAll(); 

    // N Queries executed in loop: SELECT * FROM posts WHERE userId = ...;
    const formattedData = await Promise.all(
      users.map(async (user) => {
        const posts = await user.getPosts(); // Triggers a separate query for EVERY user!
        return {
          id: user.id,
          username: user.username,
          posts: posts.map(p => p.title)
        };
      })
    );
    
    // If you have 50 users, this executes 51 SQL queries!
    return res.status(200).json(formattedData);
  }
};
```

### 2. Fixing with Eager Loading (Optimized Code)
Here is the corrected code. It achieves the exact same output but executes **only 1 query**:

```javascript
// src/controllers/userController.js (OPTIMIZED / FAST PATTERN)
const User = require('../models/User');
const Post = require('../models/Post');

module.exports = {
  getUsersAndPostsFast: async (req, res) => {
    // Executes 1 Query using LEFT OUTER JOIN
    const users = await User.findAll({
      include: [{
        model: Post,
        as: 'posts',
        attributes: ['title']
      }]
    });

    // Formatting data in JS memory is extremely fast
    const formattedData = users.map(user => ({
      id: user.id,
      username: user.username,
      posts: user.posts.map(p => p.title)
    }));

    return res.status(200).json(formattedData);
  }
};
```

### 3. Nested Includes (Deep Joins)
You can nest `include` arrays to join multiple levels (e.g. Fetch Users -> their Posts -> the Comments on those posts):

```javascript
const users = await User.findAll({
  include: [{
    model: Post,
    as: 'posts',
    include: [{
      model: Comment,
      as: 'comments',
      attributes: ['id', 'content']
    }]
  }]
});
```

---

## 🔄 Flow Diagram

### Eager vs Lazy Execution Comparison

```text
EAGER LOADING (1 Query):
User Controller             Sequelize ORM                  Database
      │                           │                           │
      │── User.findAll(include) ─>│── LEFT OUTER JOIN SQL ───>│
      │                           │<─ Combined Result Rows ───│
      │<─ Hydrated nested array ──│                           │

LAZY LOADING (N+1 Queries):
User Controller             Sequelize ORM                  Database
      │                           │                           │
      │── User.findAll() ────────>│── SELECT * FROM users ───>│ (Query 1)
      │                           │<─ Users Array (Length 3) ─│
      │                           │                           │
      │── Loop 1: user.getPosts() ─>│── SELECT WHERE userId=1 ─>│ (Query 2)
      │                           │<─ Posts user 1 ───────────│
      │                           │                           │
      │── Loop 2: user.getPosts() ─>│── SELECT WHERE userId=2 ─>│ (Query 3)
      │                           │<─ Posts user 2 ───────────│
      │                           │                           │
      │── Loop 3: user.getPosts() ─>│── SELECT WHERE userId=3 ─>│ (Query 4)
      │                           │<─ Posts user 3 ───────────│
```

---

## 🧪 Common Interview Questions

### Q1: What is the N+1 query problem, and how do you resolve it in Sequelize?
* **Answer**: The N+1 query problem occurs when the application executes 1 query to fetch parent records, and then executes N subsequent queries to fetch associated child records for each parent. It is resolved by replacing lazy loading (getters inside loops) with eager loading using the `include` option, which combines the parent and child tables in a single SQL query using Joins.

### Q2: What is the role of the `required: true` option in Sequelize includes?
* **Answer**: By default, Sequelize uses `LEFT OUTER JOIN` for includes, which returns parent records even if they have no matching child records (e.g. users without posts). Setting `required: true` forces Sequelize to use an `INNER JOIN`, returning only parent records that have at least one matching child record (e.g. only users who have written posts).

### Q3: How do you filter parent records based on child values?
* **Answer**: To filter parent records based on nested association values, you must define a where clause on the nested model inside the include block, and set `required: true`. For example:
  ```javascript
  User.findAll({
    include: [{ model: Post, as: 'posts', where: { title: { [Op.like]: '%Sequelize%' } }, required: true }]
  });
  ```

---

## ⚠️ Common Mistakes / Pitfalls
* **Lazy Loading in Loops**: Fetching relations by calling `await instance.getRelations()` inside `.map()`, `.forEach()`, or `for...of` loops. Always check your development logs. If you see multiple SELECT statements firing for a single request, you have an N+1 bug.
* **Massive Payload Joins**: Eagerly loading multiple large tables (e.g., loading Users with Profiles, Posts, Comments, and Tags all at once). The database returns cartesian product rows, generating massive network payloads that slow down both the database and Node memory.

---

## ✅ Best Practices
* **Filter child columns**: When using `include`, always limit the fields fetched using `attributes: [...]`. Do not fetch entire child rows if you only need the ID or Title.
* **Set `nest: true` for raw queries**: When using `{ raw: true }` with `include` statements, Sequelize flats the keys into names like `"posts.title"`. Add `nest: true` to get structured nested objects:
  ```javascript
  User.findAll({ include: [Post], raw: true, nest: true });
  ```

---

## 📝 Quick Recap
* Lazy loading fetches parent records first and uses getters (like `.getPosts()`) to query child records later.
* Eager loading fetches parent and child records in a single query using SQL `JOIN` statements.
* The N+1 query problem occurs when lazy loading runs queries inside loops, slowing down database interactions.
* Use `include` to eager-load records, and apply `attributes` to limit the returned columns.

---

## 🔗 Navigation
Previous : [09_associations_and_relationships.md](./09_associations_and_relationships.md) | Index : [00_index.md](./00_index.md) | Next : [11_transactions_in_depth.md](./11_transactions_in_depth.md)
