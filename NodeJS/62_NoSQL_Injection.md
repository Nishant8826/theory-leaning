# NoSQL Injection

Many developers assume NoSQL databases are safe from injection because they do not use SQL strings. This is false. MongoDB queries use JavaScript objects. If you pass client-provided objects directly into your query parameters, attackers can inject query operators (like `$ne` - "not equal") to bypass authentication checks or extract private data. Understanding NoSQL validation is critical for securing document databases.

### What is NoSQL Injection?
**NoSQL Injection** occurs when untrusted user input is parsed directly into NoSQL query objects, allowing attackers to inject query operators that alter the query structure.

### MongoDB Operator Injection
MongoDB queries are structured as JSON-like objects. Attackers can inject operators to alter query logic:
* **`$ne` (Not Equal)**: Bypasses checks (e.g., checking if password is not equal to empty string).
* **`$gt` (Greater Than)**: Bypasses validation (e.g., querying for IDs greater than 0).
* **`$regex` (Regular Expression)**: Extracts data by checking values character-by-character (e.g., searching if a password starts with `"a"`, then `"b"`, and so on).

## Deep Dive

### Mitigation Strategies

#### 1. Input Sanitization
Attackers inject operators by passing keys that start with a dollar sign (`$`). You can strip out these keys by sanitizing input payloads using middleware:
* **`mongo-sanitize`**: A utility library that recursively strips out keys starting with a dollar sign (`$`) from objects, preventing operator injection.

#### 2. Enforcing Schema Types with Mongoose
Using an ODM like Mongoose provides a built-in defense layer. Mongoose casts values strictly based on the schema definition:
* If a schema field is defined as a `String` (e.g. `password: String`), and the client sends an object (e.g. `{ "$ne": "" }`), Mongoose converts the object to a literal string: `"{ '$ne': '' }"`.
* The database queries for that literal string, causing the attack to fail safely.

*Caution*: Mongoose only protects fields that have defined schema types. If you query using dynamic schemas, mixed types, or raw MongoDB driver commands, you must sanitize inputs manually.

## Visual Explanation

### Password Extraction using $regex
```text
Attack Goal: Extract the admin's password.
Attack Query sent by Client:
POST /api/login
{
  "username": "admin",
  "password": { "$regex": "^a" }  (Checks if password starts with 'a')
}

Server execution path:
1. Server queries: User.findOne({ username: "admin", password: { $regex: "^a" } })
2. If the query returns a user record, the server returns 200 OK. The attacker learns the password starts with 'a'.
3. If the query fails, the attacker tries "^b", "^c", and so on.
4. By iterating through characters, the attacker extracts the complete password hash!
```

## Real-World Example
Consider an API endpoint `/api/users`. If you pass request query parameters directly to the search query `User.find(req.query)`, an attacker can send a request: `GET /api/users?role[$ne]=user`. This compiles to `User.find({ role: { $ne: "user" } })`, exposing administrator profiles. You prevent this by validating inputs using Zod schemas.

## Code Examples

### Custom Sanitization Middleware and Mongoose Type Defense

```javascript
// middleware/sanitize.js
const AppError = require('../utils/AppError');

// 1. Custom NoSQL Sanitization Middleware
// Recursively deletes any object keys starting with a dollar sign ($)
const sanitizeNoSql = (req, res, next) => {
  const clean = (obj) => {
    if (obj && typeof obj === 'object') {
      for (const key in obj) {
        if (key.startsWith('$')) {
          delete obj[key]; // Strip injection keys
        } else {
          clean(obj[key]); // Recursively check nested objects
        }
      }
    }
    return obj;
  };

  if (req.body) clean(req.body);
  if (req.query) clean(req.query);
  if (req.params) clean(req.params);

  next();
};

module.exports = sanitizeNoSql;
```

```javascript
// app.js
const express = require('express');
const mongoose = require('mongoose');
const sanitizeNoSql = require('./middleware/sanitize');

const app = express();
app.use(express.json());

// Bind database schema
const UserSchema = new mongoose.Schema({
  username: String,
  passwordHash: String
});
const User = mongoose.model('User', UserSchema);

// Apply NoSQL sanitization globally
app.use(sanitizeNoSql);

// Safe Route: Protected by sanitization and Mongoose type casting
app.post('/api/login', async (req, res, next) => {
  const { username, password } = req.body;

  try {
    // If the attacker bypassed 'sanitizeNoSql' and sent: { password: { $ne: '' } }
    // Mongoose casts 'password' to a literal string, query executes safely
    const user = await User.findOne({
      username: username,
      passwordHash: password 
    });

    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    res.json({ message: 'Login successful' });
  } catch (err) {
    next(err);
  }
});

app.listen(3000, () => console.log('NoSQL secure server running on port 3000'));
```

## Best Practices
* **Enforce Strict Types**: Always validate and cast client inputs to the correct types (strings, numbers, booleans) before using them in database queries.
* **Use Sanitization Middleware**: Apply sanitization middleware (like `mongo-sanitize`) globally to strip out keys starting with `$` from all incoming requests.
* **Avoid Raw Queries**: Avoid passing unchecked client objects directly into raw MongoDB driver commands (like `db.collection('users').find(req.body)`).
* **Use Zod for Validation**: Enforce schemas on all request input boundaries using validation libraries like Zod, rejecting objects when strings are expected.

## Interview Questions

**Q:** Can NoSQL databases suffer from injection attacks?

> **Answer:**
> Yes. NoSQL databases are vulnerable to operator injection attacks, where attackers inject query operators (like `$ne` or `$regex` in MongoDB) inside query objects to bypass authentication or extract private data.

**Q:** How does utilizing Mongoose help defend against NoSQL injection?

> **Answer:**
> Mongoose enforces schema definitions. When a query is executed, Mongoose automatically casts incoming values to the types defined in the schema. If a schema field is defined as a `String` and an attacker passes an object containing operators (like `{ "$ne": "" }`), Mongoose casts the object to a literal string, neutralizing the query operator.

**Q:** Explain how an attacker can extract user passwords from a MongoDB database using the `$regex` operator, and how you prevent it.

> **Answer:**
> An attacker can send login requests containing a regex pattern: `{ "username": "admin", "password": { "$regex": "^a" } }`. If the query succeeds, the attacker learns the password starts with "a". By iterating through characters, they can extract the complete password.
> To prevent this:
> 1. Enforce strict input validation using schema libraries (like Zod) to ensure that the password parameter is strictly a string, rejecting objects.
> 2. Apply sanitization middleware (like `mongo-sanitize`) to strip out any keys starting with `$` from the request payload.

**Q:** How would you secure a high-throughput Node.js API that uses a combination of MongoDB and PostgreSQL against both SQL and NoSQL injection attacks, ensuring minimum latency overhead?

> **Answer:**
> To secure a hybrid SQL/NoSQL API with minimal latency:
> 1. **Validation at Boundary**: Use Zod validation middleware at the API boundary to enforce strict schemas for all inputs. Reject invalid formats (such as objects where strings are expected) before they reach controllers. Zod schemas compile validations quickly, minimizing latency.
> 2. **Automatic Parameterization**: Use query builders (like Knex or Kysely) for PostgreSQL queries, which use parameterized queries automatically.
> 3. **Schema Enforcement**: Use Mongoose for MongoDB queries, leveraging its built-in schema casting. For raw MongoDB driver commands, apply `mongo-sanitize` to strip out operator keys.
> 4. **Least Privilege**: Configure separate, restricted database users for MongoDB and PostgreSQL. Limit permissions to the minimum tables and collections required, containing the impact if a vulnerability is compromised.

---
Previous : [61_SQL_Injection.md](61_SQL_Injection.md) | Index : [00_index.md](00_index.md) | Next : [63_Testing_Fundamentals.md](63_Testing_Fundamentals.md)
