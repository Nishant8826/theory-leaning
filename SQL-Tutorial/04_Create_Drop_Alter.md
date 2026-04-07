# Create, Drop, Alter

> 📌 **File:** 04_Create_Drop_Alter.md | **Level:** Beginner → MERN Developer

---

## What is it?
These commands are part of DDL (Data Definition Language). They shape the structural skeleton of your database tables, completely separate from the data inside them.

## MERN Parallel — You Already Know This!
- `CREATE` → Mongoose `new Schema(...)`
- `DROP` → Db delete (`db.dropCollection()`)
- `ALTER` → Modifying your Mongoose JS schema file and restarting the app.

## Why does it matter?
Schemas change over time. You'll need to add an `email` field to an existing `customers` table without deleting their current records, handled safely by `ALTER`.

## How does it work?
You tell the database exactly what structural adjustment to make.

## Visual Diagram
```ascii
[Table V1]                  [ALTER]                   [Table V2]
| id | name |    --ADD COLUMN email VARCHAR(255)-->   | id | name | email |
```

## Syntax
```sql
-- Fully commented SQL syntax
CREATE TABLE staff (id INT PRIMARY KEY);
ALTER TABLE staff ADD COLUMN role VARCHAR(50);
ALTER TABLE staff DROP COLUMN role;
DROP TABLE staff; -- DESTROYS entire table and all data!
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose (How to "alter" a schema)
// Just add property to mongoose model
const StaffSchema = new Schema({ id: Number, role: String });

// SQL
-- ALTER TABLE staff ADD COLUMN role VARCHAR(50);

// Node.js using mysql2/promise (REQUIRED)
await pool.query('ALTER TABLE staff ADD COLUMN role VARCHAR(50)');

// ORM Equivalent (IMPORTANT)
// Prisma migration tool automatically does this based on prisma.schema changes.
```

### Raw SQL vs ORM
- **Raw SQL:** Excellent for doing on-the-fly hotfixes to database columns, but scary to run directly on production.
- **ORM:** Standardizes DDL through specific migration folders so teams can share database changes via Git.

### Real-World Scenario + Full Stack Code
**Scenario:** Rolling out a generic profile picture feature by altering the `customers` table manually through an admin utility route.

```sql
-- SQL query
ALTER TABLE customers ADD COLUMN avatar_url VARCHAR(255) DEFAULT 'default.png';
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.post('/api/admin/add-avatar-feature', async (req, res) => {
  try {
    const query = `ALTER TABLE customers ADD COLUMN avatar_url VARCHAR(255) DEFAULT 'default.png'`;
    await pool.query(query); // No parameterized inputs for schema columns
    res.json({ message: 'Migration deployed successfully.' });
  } catch(e) {
    if (e.code === 'ER_DUP_FIELDNAME') {
      return res.status(400).json({ error: 'Column already exists' });
    }
    res.status(500).send(e.message);
  }
});

// React component using Axios
function MigrateBtn() {
  return <button onClick={() => axios.post('/api/admin/add-avatar-feature')}>Run Avatar Migration</button>
}
```

**Output:**
```json
{
  "message": "Migration deployed successfully."
}
```

## Impact
Running `DROP TABLE` is catastrophic data loss. Running `ALTER TABLE` locks the table for writes on massive databases until the migration finishes, causing downtime.

## Practice Exercises
- **Easy (SQL)**: Create a table, alter it to have an `age` column, then drop the table entirely.
- **Medium (SQL + Node.js)**: Write a Node script that wraps an ALTER table around a `try/catch` to gracefully fail if the table doesn't exist.
- **Hard (Full stack)**: Create a React dropdown list of DB Tables. Pushing "Delete Drop" calls an API running `DROP TABLE ?` (Note: DB identifiers can't be safely parameterized using `?`, they must be validated string concatenations!)

## Interview Q&A
1. **Core SQL:** What's the difference between DELETE and DROP?
   *DELETE removes rows (DML). DROP removes the whole table architecture (DDL).*
2. **MERN integration:** Should we run ALTER queries from Express controllers?
   *Historically, no. Migrations belong in CI/CD chains using CLI tools (like knex/prisma).*
3. **SQL vs MongoDB:** Why is ALTER risky compared to updating a Mongoose JS schema?
   *Mongoose schemas are just application logic checking data on its way in/out. ALTER physically locks the physical disk table while making changes.*
4. **Scenario-based:** Can I parameterize a table name? `DROP TABLE ?`
   *No. Prepared statements (`?`) only work for values, not structural identifiers (table/column names).*
5. **Advanced/tricky:** How to safely add a column if it doesn't already exist?
   *Advanced procedural SQL/checking `information_schema` is required in MySQL, unlike postgres `ADD COLUMN IF NOT EXISTS`.*

| Previous: [03_Data_Types.md](./03_Data_Types.md) | Next: [05_Insert_Update_Delete.md](./05_Insert_Update_Delete.md) |
