# Data Types

> 📌 **File:** 03_Data_Types.md | **Level:** Beginner → MERN Developer

---

## What is it?
SQL has specific, granular data types. Every column must be assigned a type before any data is inserted.

## MERN Parallel — You Already Know This!
- `String` → `VARCHAR(255)` or `TEXT`
- `Number` → `INT`, `FLOAT`, or `DECIMAL(10,2)`
- `Boolean` → `BOOLEAN` (or `TINYINT(1)`)
- `Date` → `DATETIME` or `TIMESTAMP`
- Arrays/Objects → Must be broken into separate relational tables (or saved as `JSON` columns in modern MySQL)

## Why does it matter?
Proper data types optimize disk storage speed and maintain data fidelity. In JS, `0.1 + 0.2` has floating point errors. In MySQL, `DECIMAL` stores monetary values perfectly.

## How does it work?
When creating a table or modifying it, you attach the data type keywords exactly against the column name.

## Visual Diagram
```ascii
Mongoose Number    --->    MySQL Needs Context
{ price: Number }          - INT (Whole Numbers)
                           - FLOAT (Science / approximation)
                           - DECIMAL (Money / Exact)
```

## Syntax
```sql
-- Fully commented SQL syntax
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50),      -- Max 50 chars, saves space
  bio TEXT,                  -- Long text block
  is_active BOOLEAN,         -- Under the hood, this is a TINYINT(1)
  wallet DECIMAL(10,2),      -- 10 total digits, 2 after decimal (99999999.99)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### MERN vs SQL — Side-by-Side Code

```javascript
// MongoDB / Mongoose
new Schema({ isActive: { type: Boolean, default: true } });

// SQL
-- is_active BOOLEAN DEFAULT 1;

// Node.js using mysql2/promise (REQUIRED)
const [rows] = await pool.query('SELECT CAST(1 AS BOOLEAN) AS result');

// ORM Equivalent (IMPORTANT)
// Prisma
model User {
  isActive Boolean @default(true)
}
```

### Raw SQL vs ORM
- **Raw SQL:** Forces you to learn the exact limits of MySQL storage.
- **ORM:** Automatically maps JS primitives to DB types (e.g. `String` to `VARCHAR(255)` automatically).

### Real-World Scenario + Full Stack Code
**Scenario:** Handling boolean logic which MySQL returns as `1` or `0` instead of `true`/`false`.

```sql
-- SQL query
SELECT is_active FROM users WHERE id = ?;
```

```javascript
// Node.js + Express using mysql2 (ALWAYS parameterized queries)
app.get('/api/users/:id', async (req, res) => {
  const [rows] = await pool.query('SELECT is_active FROM users WHERE id=?', [req.params.id]);
  
  // Convert tinyint to JS boolean before sending
  const user = rows[0];
  user.is_active = user.is_active === 1;
  res.json(user);
});

// ORM version (Sequelize/Prisma)
app.get('/api/users/:id', async (req, res) => {
  const user = await User.findByPk(req.params.id);
  // ORM does the 1 to True conversion automatically
  res.json(user);
});

// React component using Axios
function Profile({ id }) {
  const [active, setActive] = useState(false);
  useEffect(() => {
    axios.get(`/api/users/${id}`).then(res => setActive(res.data.is_active));
  }, [id]);
  return <div>{active ? 'Active User' : 'Inactive User'}</div>;
}
```

**Output:**
```json
{
  "is_active": true
}
```

## Impact
If you use `FLOAT` for financial data, tax calculations will experience rounding errors causing huge bugs. Always use `DECIMAL(10,2)` for money.

## Practice Exercises
- **Easy (SQL)**: Design a simple table command using VARCHAR, INT, and BOOLEAN.
- **Medium (SQL + Node.js)**: Build an API that accepts `{ price: 34.55 }` and accurately stores it in a `DECIMAL` column.
- **Hard (Full stack)**: Create a React form for a user profile with text inputs and a checkbox toggle, mapped perfectly to DB types.

## Interview Q&A
1. **Core SQL:** What's the difference between VARCHAR and TEXT?
   *VARCHAR has a strict max length defined (e.g., 255) and is faster for small things. TEXT is for long paragraphs.*
2. **MERN integration:** How does JS handle MySQL DATE fields?
   *`mysql2` converts them natively into JavaScript `Date` objects.*
3. **SQL vs MongoDB:** Can I store arrays natively in a MySQL column?
   *Historically no (needs a separate table). Modern MySQL allows JSON type columns, but relations are better.*
4. **Scenario-based:** We are losing fractions of cents on purchases. Issue?
   *The DB uses FLOAT. It must be migrated to DECIMAL.*
5. **Advanced/tricky:** What is TINYINT(1)?
   *It's a one-byte integer. MySQL aliases the word BOOLEAN to this. 0 is false, everything else true.*

| Previous: [02_Databases_And_Tables.md](./02_Databases_And_Tables.md) | Next: [04_Create_Drop_Alter.md](./04_Create_Drop_Alter.md) |
