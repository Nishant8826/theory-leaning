# 📌 03 — Input Validation and Sanitization: Hardening the Entry

## 🧠 Concept Explanation

### Basic → Intermediate
Input Validation is checking if the data provided by the user matches the expected format (e.g. "Is this an email?"). Sanitization is cleaning the data to remove dangerous parts (e.g. "Remove `<script>` tags").

### Advanced → Expert
At a staff level, we treat the API boundary as a **Zero-Trust Zone**.
1. **Validation (Structural)**: Ensuring the payload has the right keys, types, and constraints (length, range).
2. **Sanitization (Content)**: Removing potential XSS or SQL characters.
3. **Coercion**: Safely converting types (e.g. "123" string to 123 number).

The goal is to ensure that **no malformed data ever reaches your business logic.**

---

## 🏗️ Common Mental Model
"I'll just use a few `if` statements for validation."
**Correction**: Manual validation is prone to errors and bypasses. Use a **Schema-based Validator** like **Zod** or **Joi**. They provide a declarative way to define data shapes that also act as documentation and TypeScript types.

---

## ⚡ Actual Behavior: Fail-Fast
Validation should happen as the **first step** in your middleware chain. If the input is invalid, you should return a `400 Bad Request` immediately, preventing any expensive database calls or logic execution.

---

## 🔬 Internal Mechanics (V8 + Validation)

### Prototype Pollution Defense
Validators like Zod automatically ignore extra keys (Strip mode) by default. This prevents an attacker from sending a `__proto__` key in the JSON payload, as the validator will simply discard it before it reaches your application code.

---

## 📐 ASCII Diagrams

### The Validation Shield
```text
  INCOMING REQUEST (Untrusted)
     │
     ▼
  ┌───────────────────────────┐
  │   ZOD SCHEMA VALIDATION   │ ──▶ Invalid ──▶ [ 400 Bad Request ]
  └─────────────┬─────────────┘
                │
                ▼ (Guaranteed Shape)
  ┌───────────────────────────┐
  │      BUSINESS LOGIC       │
  └───────────────────────────┘
```

---

## 🔍 Code Example: Strict Validation with Zod
```javascript
const { z } = require('zod');

// 1. Define the Schema
const createUserSchema = z.object({
  username: z.string().min(3).max(20).regex(/^[a-zA-Z0-9_]+$/),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
  bio: z.string().max(500).transform(val => val.trim()) // Sanitization
});

app.post('/users', (req, res) => {
  try {
    // 2. Validate and Parse
    const validatedData = createUserSchema.parse(req.body);
    
    // validatedData is now safe and typed
    db.save(validatedData);
    res.status(201).send();
  } catch (e) {
    res.status(400).json({ errors: e.errors });
  }
});
```

---

## 💥 Production Failures & Debugging

### Scenario: The Hidden ReDoS
**Problem**: You have a validation regex for usernames: `^(([a-z])+.)+[A-Z]([a-z])+$`.
**Reason**: This is a "catastrophic backtracking" regex. An attacker sends a 50-character string that almost matches but fails at the end. The CPU hits 100% for minutes.
**Fix**: Use simple regexes or built-in validators like `z.string().email()`. Use `node-re2` for safe regular expressions.

### Scenario: Mass Assignment Vulnerability
**Problem**: A user updates their profile and includes `"role": "admin"` in the JSON. The server saves the whole object to the DB.
**Reason**: You are doing `db.users.update(req.body)`.
**Fix**: Only pick the fields you want to update. Schema validators like Zod handle this by "stripping" unknown keys.

---

## 🧪 Real-time Production Q&A

**Q: "Should I sanitize on input or output?"**
**A**: **Both, but for different reasons.** Validate and Sanitize on **Input** to protect your database and business logic. Sanitize on **Output** (Encoding) to protect the user from XSS when displaying the data.

---

## 🏢 Industry Best Practices
- **Never Trust req.body**: Or `req.query`, or `req.params`. Validate everything.
- **Dry (Don't Repeat Yourself)**: Use your validation schema to generate your TypeScript interfaces to ensure consistency.

---

## 💼 Interview Questions
**Q: What is the difference between Validation and Sanitization?**
**A**: Validation is **Rejecting** bad data (e.g. "This is not a number"). Sanitization is **Cleaning** bad data so it becomes safe (e.g. "Remove `<script>` tags from this string").

---

## 🧩 Practice Problems
1. Create a Zod schema for a "Search" endpoint that accepts a query string, a numeric limit, and an optional sort order. Handle the case where the limit is passed as a string `"10"`.
2. Build a middleware that uses `dompurify` to sanitize every string field in `req.body`.

---

**Prev:** [02_Authentication_JWT_OAuth.md](./02_Authentication_JWT_OAuth.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [04_Cryptography_and_Hashing.md](./04_Cryptography_and_Hashing.md)
