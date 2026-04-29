# 📌 05 — Database Migrations: Zero-Downtime Schema Evolution

## 🧠 Concept Explanation

### Basic → Intermediate
Migrations are version-controlled changes to your database schema (e.g. adding a column, creating a table). They allow you to keep your database in sync with your code across different environments.

### Advanced → Expert
At a staff level, the challenge is **Zero-Downtime Migrations**. In a production environment, you cannot just run `DROP COLUMN` while the app is running, as the existing code will crash. You must use the **Expand and Contract** (or Parallel Change) pattern.

The stages are:
1. **Expand**: Add the new column/table, but keep the old one. Code writes to both but reads from the old one.
2. **Migrate**: Copy the existing data from the old column to the new one (Background Job).
3. **Switch**: Update the code to read from the new column.
4. **Contract**: Delete the old column once you are sure the new code is stable.

---

## 🏗️ Common Mental Model
"I'll just put the site in 'Maintenance Mode' while I run migrations."
**Correction**: For high-availability systems, maintenance mode is unacceptable. You must design your migrations to be **Backward Compatible**.

---

## ⚡ Actual Behavior: Locking and Table Size
Running `ALTER TABLE` on a table with 100 million rows can **lock the table** for minutes or hours, preventing all writes and effectively causing a total outage.
**Fix**: Use tools like **gh-ost** or **pt-online-schema-change** for MySQL, or use the "Expand and Contract" pattern to avoid heavy locks.

---

## 🔬 Internal Mechanics (SQL + Migrations)

### Transactional Migrations
Most modern migration tools (like Knex or Prisma) wrap each migration in a database transaction. If the migration fails halfway, it rolls back, preventing a partially updated schema. 
**Note**: Some operations (like creating an index in Postgres without `CONCURRENTLY`) cannot be undone easily if they cause a lock.

### The Migration Table
Migration tools create a hidden table (e.g. `knex_migrations`) in your database to keep track of which migration files have already been executed.

---

## 📐 ASCII Diagrams

### Expand and Contract Pattern
```text
  STATE 1: [ Column: OldName ]
             │
  STATE 2: [ Column: OldName, Column: NewName ]  <─── (Expand)
             │   (App writes to both)
             ▼
  STATE 3: [ Column: OldName, Column: NewName ]
             │   (App reads from NewName)
             ▼
  STATE 4: [ Column: NewName ]                   <─── (Contract)
```

---

## 🔍 Code Example: Safer Migration with Knex
```javascript
exports.up = async function(knex) {
  // ❌ Dangerous: Renaming a column in a live app
  // await knex.schema.table('users', t => t.renameColumn('name', 'full_name'));

  // ✅ Safe (Expand): Add the new column
  await knex.schema.table('users', t => {
    t.string('full_name').nullable();
  });
};

exports.down = async function(knex) {
  await knex.schema.table('users', t => {
    t.dropColumn('full_name');
  });
};
```

---

## 💥 Production Failures & Debugging

### Scenario: The Migration Timeout
**Problem**: You run `npm run migrate` in your CI/CD pipeline. It runs for 60 seconds and then is killed by the deployment agent.
**Reason**: The database is performing a large index creation. The migration tool is waiting, but the CI/CD has a timeout. The database is now in an unknown state.
**Fix**: Run long migrations (like index creation) separately from your application deployment, or use `CONCURRENTLY` in Postgres.

### Scenario: The Deployment Mismatch
**Problem**: You deploy new code that expects the new schema, but the migration hasn't finished yet. The code crashes.
**Reason**: Race condition between deployment and migration.
**Fix**: Always run migrations **before** deploying code, and ensure migrations are backward-compatible so old code doesn't crash.

---

## 🧪 Real-time Production Q&A

**Q: "Should I use `db push` or migrations?"**
**A**: **Use Migrations.** Tools like `prisma db push` are great for prototyping but dangerous for production because they don't provide a historical record of changes and can perform destructive operations without warning.

---

## 🏢 Industry Best Practices
- **Never modify a migration file**: Once it is committed and run in production, it is immutable. If you need to make a change, create a *new* migration.
- **Test Rollbacks**: Always ensure your `down` migration works correctly before deploying.

---

## 💼 Interview Questions
**Q: How do you handle migrations in a system with 100 microservices?**
**A**: Each microservice owns its own database and its own migrations. Never have a "Global Migration" that spans multiple services.

---

## 🧩 Practice Problems
1. Implement a 3-stage deployment (Expand, Switch, Contract) for renaming a `username` field to `email`.
2. Use Postgres `EXPLAIN` to see if adding an index to a table will require a full table scan.

---

**Prev:** [04_Consistency_vs_Availability.md](./04_Consistency_vs_Availability.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [../Performance/01_Profiling_and_Analysis.md](../Performance/01_Profiling_and_Analysis.md)
