# 📌 01 — OWASP Top 10 in Node.js: Defensive Engineering

## 🧠 Concept Explanation

### Basic → Intermediate
The OWASP Top 10 is a list of the most critical web application security risks. In Node.js, we must implement specific defenses against these risks to ensure our applications are production-ready.

### Advanced → Expert
At a staff level, security is about **Defense in Depth**.
1. **Injection**: SQL/NoSQL injection. Prevent by using parameterized queries (Knex/Prisma).
2. **Broken Authentication**: Session hijacking or weak passwords. Prevent by using JWTs with short TTLs and secure `httpOnly` cookies.
3. **Sensitive Data Exposure**: Leaking passwords or PII. Prevent by hashing with `bcrypt` (high cost) and using TLS.
4. **Broken Access Control**: Users accessing data they shouldn't. Prevent by using **RBAC (Role-Based Access Control)** or **ABAC (Attribute-Based Access Control)**.

---

## 🏗️ Common Mental Model
"I use an ORM, so I'm safe from SQL injection."
**Correction**: ORMs can be bypassed. For example, passing an object instead of a string to a `where` clause in Sequelize can sometimes trigger unintended behavior (NoSQL-style injection). Always validate input types using **Zod** or **Joi**.

---

## ⚡ Actual Behavior: Prototype Pollution
A risk unique to JavaScript. If you merge a user-provided object into a system object without sanitization, an attacker can modify `Object.prototype`, affecting the behavior of the entire application (e.g. changing an `isAdmin` check from `false` to `true`).

---

## 🔬 Internal Mechanics (V8 + Networking)

### Serialization Security
`JSON.parse()` is generally safe, but `eval()` or `new Function()` with user data is a critical vulnerability. Additionally, insecurely deserializing objects in older libraries (like `node-serialize`) can lead to **Remote Code Execution (RCE)**.

---

## 📐 ASCII Diagrams

### Prototype Pollution Attack
```text
  1. Attack Payload: { "__proto__": { "isAdmin": true } }
     │
     ▼
  2. Unsafe Merge: Object.assign(systemObj, payload)
     │
     ▼
  3. IMPACT: Every object in the app now has .isAdmin = true
     (Object.prototype has been poisoned)
```

---

## 🔍 Code Example: Defending against NoSQL Injection
```javascript
const express = require('express');
const app = express();

// ❌ VULNERABLE: User can send { "password": { "$ne": null } }
app.post('/login', async (req, res) => {
  const user = await db.users.findOne({
    username: req.body.username,
    password: req.body.password 
  });
  // ...
});

// ✅ SECURE: Strict Type Validation
const { z } = require('zod');
const loginSchema = z.object({
  username: z.string(),
  password: z.string() // Forces input to be a string
});

app.post('/login', async (req, res) => {
  const { username, password } = loginSchema.parse(req.body);
  // Now password is guaranteed to be a literal string
});
```

---

## 💥 Production Failures & Debugging

### Scenario: The XSS in JSON
**Problem**: An attacker puts `<script>alert(1)</script>` in their username. When another user views the profile, the script executes.
**Reason**: You are injecting the username directly into the HTML on the server (Server-Side Rendering) or the client is using `.innerHTML`.
**Fix**: Use `.textContent` instead of `.innerHTML`. Set the `Content-Security-Policy` (CSP) header.

### Scenario: ReDoS (Regular Expression Denial of Service)
**Problem**: The server CPU hits 100% and stops responding to all users when one user submits a specific string to a search field.
**Reason**: You are using a vulnerable Regex (Evil Regex) that has exponential complexity for certain inputs.
**Fix**: Use `safe-regex` to scan your patterns. Avoid nested quantifiers (e.g. `(a+)+`).

---

## 🧪 Real-time Production Q&A

**Q: "Should I use Helmet.js?"**
**A**: **Yes.** `helmet` is a collection of middleware that sets important security headers (XSS Filter, HSTS, CSP) automatically. It is a "quick win" for basic security.

---

## 🏢 Industry Best Practices
- **Least Privilege**: The database user for your app should only have access to the tables and actions (Select/Insert/Update) it actually needs.
- **Secret Management**: Never hardcode keys. Use AWS Secrets Manager or Vault.

---

## 💼 Interview Questions
**Q: What is a CSRF attack and how does Node.js prevent it?**
**A**: Cross-Site Request Forgery. An attacker tricks a logged-in user's browser into sending a request to your server (e.g. a hidden form). Prevent it using **Anti-CSRF tokens** or the `SameSite=Strict` attribute on cookies.

---

## 🧩 Practice Problems
1. Implement a middleware that recursively sanitizes any `__proto__` keys from `req.body` to prevent Prototype Pollution.
2. Use `npm audit` on a project and fix one critical vulnerability.

---

**Prev:** [../Performance/05_Benchmarking_NodeJS.md](../Performance/05_Benchmarking_NodeJS.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [02_Authentication_JWT_OAuth.md](./02_Authentication_JWT_OAuth.md)
