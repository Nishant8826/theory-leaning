# 📌 02 — ORM vs Query Builder: Abstraction vs Performance

## 🧠 Concept Explanation

### Basic → Intermediate
- **ORM (Object-Relational Mapping)**: (e.g. Sequelize, TypeORM, Prisma) Maps database tables to JavaScript objects/classes. High abstraction, easy to use.
- **Query Builder**: (e.g. Knex) Provides a programmatic way to write SQL queries. Mid abstraction.
- **Raw SQL**: Direct queries. Zero abstraction, maximum control.

### Advanced → Expert
At a staff level, the choice depends on the **Complexity of the Schema** vs the **Performance Requirements**.
1. **ORM**: Great for productivity and complex relationships. But it often hides the **N+1 Problem** and generates inefficient SQL (unnecessary JOINs or `SELECT *`).
2. **Query Builder**: Provides the perfect balance. It prevents SQL injection and helps with dynamic query building, but you still "think in SQL."
3. **The "Data Mapping" Cost**: ORMs have high CPU overhead because they must instantiate hundreds of class instances and perform complex property mapping for every row returned.

---

## 🏗️ Common Mental Model
"Prisma is an ORM."
**Correction**: Prisma is technically a **Data Mapper**. It uses a separate Rust-based engine to handle the heavy lifting of query generation and result mapping, which is different from "Active Record" ORMs like Sequelize where the logic is in JS classes.

---

## ⚡ Actual Behavior: The N+1 Problem
An ORM makes it too easy to write code that performs one query to get 10 users and then **10 separate queries** to get the posts for each user.
```javascript
const users = await User.findAll(); // 1 query
for (const user of users) {
  const posts = await user.getPosts(); // 10 more queries!
}
```
In a high-traffic system, this is a death sentence for the database.

---

## 🔬 Internal Mechanics (Performance)

### JSON Serialization Cost
ORMs often return "rich" objects with methods like `.save()` and `.update()`. When you send these to `res.json()`, Node.js has to strip all the methods and internal metadata, which consumes CPU and memory.

### Lean Queries
Most modern ORMs offer a "lean" or "raw" mode (e.g. Mongoose's `.lean()`) that returns plain JS objects instead of class instances. This can improve performance by 2x-5x for read-only operations.

---

## 📐 ASCII Diagrams

### Abstraction Layers
```text
  ┌─────────────────────────┐
  │   APP LOGIC (JS)        │
  ├─────────────────────────┤
  │   ORM / DATA MAPPER     │ (Sequelize / Prisma)
  ├─────────────────────────┤
  │   QUERY BUILDER         │ (Knex)
  ├─────────────────────────┤
  │   DATABASE DRIVER       │ (pg / mysql2)
  └─────────────────────────┘
```

---

## 🔍 Code Example: Knex vs Prisma
```javascript
// KNEX (Query Builder) - Explicit control
const posts = await knex('posts')
  .where('user_id', 1)
  .select('title', 'created_at'); // Only the fields we need

// PRISMA (ORM/Data Mapper) - Type-safe and Clean
const posts = await prisma.post.findMany({
  where: { userId: 1 },
  select: { title: true, createdAt: true }
});
```

---

## 💥 Production Failures & Debugging

### Scenario: The "Selective Over-fetching"
**Problem**: The user profile page is slow and the server uses 100% CPU.
**Reason**: You are using `User.findOne()` without a `select` clause. The DB table has a `bio_long` column with 500KB of text. The ORM is loading 500KB of data for every user just to show their username.
**Fix**: Always specify which columns you need.

### Scenario: The Hidden Join
**Problem**: A simple query to list users is taking 500ms.
**Reason**: The ORM is configured to "Eager Load" relationships. It is performing a massive JOIN across 5 tables in the background.
**Fix**: Use **Lazy Loading** or manual JOINs when performance is critical.

---

## 🧪 Real-time Production Q&A

**Q: "Is it okay to use Raw SQL in a modern Node.js app?"**
**A**: **Yes**, especially for complex analytical queries or performance-critical paths. Many teams use an ORM for 90% of the app (CRUD) and raw SQL for the remaining 10% (reports/optimization).

---

## 🏢 Industry Best Practices
- **Use an ORM with a Schema**: (like Prisma) It provides type-safety that reduces bugs in large teams.
- **Always log the generated SQL**: During development, look at what your ORM is actually sending to the database.

---

## 💼 Interview Questions
**Q: What is the difference between an "Active Record" and "Data Mapper" pattern?**
**A**: In **Active Record** (Sequelize), the model object contains both the data and the logic to save itself (e.g. `user.save()`). In **Data Mapper** (Prisma/TypeORM), the data is in a plain object and a separate "repository" or "client" handles the database operations (e.g. `client.user.save(user)`).

---

## 🧩 Practice Problems
1. Implement the same query in Sequelize, Knex, and Raw SQL. Compare the execution time for 10,000 rows.
2. Use Prisma's `$on('query')` to log and measure the execution time of every database call.

---

**Prev:** [01_Database_Connections.md](./01_Database_Connections.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [03_Caching_Strategies_Redis.md](./03_Caching_Strategies_Redis.md)
