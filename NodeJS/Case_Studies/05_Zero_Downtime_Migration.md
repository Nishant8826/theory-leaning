# 📌 Case Study 05 — Zero-Downtime Schema Migration

## 🛠️ The Scenario
A social media app needs to rename the `user_handle` column to `username` in a table with 50 million rows. The site must stay online throughout the process.

**The Risk**:
- Running `RENAME COLUMN` locks the table for minutes.
- Existing code will crash because it expects `user_handle`.
- New code will crash because it expects `username`.

---

## 🔍 Step 1: The Plan (Expand and Contract)
We will perform this change in **4 separate deployments**.

---

## 🚀 Deployment 1: The "Expand" Phase
We add the new column and update the code to write to **both** columns.

**Database**:
```sql
ALTER TABLE users ADD COLUMN username VARCHAR(255);
```

**Code**:
```javascript
// ✅ Dual-Write logic
async function updateUser(id, name) {
  return await db('users').where({ id }).update({
    user_handle: name, // Old column
    username: name     // New column
  });
}
```
**Status**: All new data is in both columns. Old data is still only in `user_handle`.

---

## 🧪 Step 2: The "Migration" Phase (Background)
We run a background script to copy the data from the old column to the new one for all existing rows. We do this in small batches (e.g. 1000 rows at a time) to avoid locking the database.

```javascript
// Background Script
while (rowsPending) {
  await db.raw(`
    UPDATE users 
    SET username = user_handle 
    WHERE username IS NULL 
    LIMIT 1000
  `);
  await sleep(100); // Breathe
}
```

---

## 💡 Step 3: The "Switch" Phase
We update the code to **Read** from the new column and stop writing to the old one.

**Code**:
```javascript
// ✅ Switch to new column
async function getUser(id) {
  const user = await db('users').where({ id }).first();
  return user.username; // Reading from the new column
}
```
**Status**: The app is now fully using `username`. `user_handle` is stale and unused.

---

## 🔬 Step 4: The "Contract" Phase
After 24 hours of monitoring to ensure no bugs, we delete the old column.

**Database**:
```sql
ALTER TABLE users DROP COLUMN user_handle;
```

---

## ✅ Results
- **Downtime**: 0 seconds.
- **Errors**: 0.
- **Database Load**: Minimal (due to batching).

---

## 🏢 Lessons Learned
1. **Never rename columns in-place**: It is a recipe for disaster in a high-traffic app.
2. **Dual-Writing is your friend**: It provides a bridge between the old and new schemas.
3. **Batch your background updates**: Protect the database CPU by moving data in small, controlled chunks.

---

## 🏁 Curriculum Conclusion
Congratulations! You have completed the **Node.js Systems Engineering & Runtime Internals** curriculum. You now have the architectural knowledge and the production-grade toolset to design, scale, and debug world-class Node.js applications.

**Next Steps**: 
- Apply these patterns to your current projects.
- Master the profiling tools (`clinic`, `0x`).
- Deep dive into the Node.js source code for specific modules.

---

**Prev:** [04_Microservices_Failure_Chain.md](./04_Microservices_Failure_Chain.md) | **Index:** [00_Index.md](../00_Index.md)
