# 📌 06 — Middleware Design

## 🌟 Introduction

In a Node.js server (like Express), a request doesn't just hit a function and get an answer. It travels through a series of "stations" called **Middleware**.

Think of it like an **Airport Security Check**:
1.  **Station 1 (Passport Control):** Checks if you are allowed in (Auth).
2.  **Station 2 (Security Scan):** Checks if you are carrying anything dangerous (Data Validation).
3.  **Station 3 (Boarding):** You finally reach your plane (The Route Handler).

Each station can either **allow you to move forward** using `next()`, or **stop you** and send you home with an error.

---

## 🏗️ How it Works: The Linear Model (Express)

In Express, middleware functions run one after another in a straight line.

```javascript
app.use((req, res, next) => {
  console.log("Station 1: Logging...");
  next(); // Pass to the next station
});

app.use((req, res, next) => {
  if (req.user) {
    next(); // Authenticated! Move on.
  } else {
    res.status(401).send("Stop! You are not logged in.");
  }
});
```

---

## 🏗️ The Onion Model (Koa)

Koa uses a more advanced "Onion" model. The request goes **in** through the layers and **out** back through the same layers. This is great for tasks like measuring how long a request took.

```javascript
app.use(async (ctx, next) => {
  const start = Date.now(); // 1. Going in...
  await next();             // 2. Wait for all other middlewares to finish
  const ms = Date.now() - start; // 3. Coming back out!
  console.log(`Request took ${ms}ms`);
});
```

---

## 🚀 Common Use Cases

1.  **Logger:** Record every request in a file or database.
2.  **Body Parser:** Convert raw text from a form into a JS object (`req.body`).
3.  **Authentication:** Block unauthorized users from private routes.
4.  **Error Handling:** Catch any crashes and send a "friendly" error message to the user.

---

## 🔍 Code Walkthrough: Simple Auth & Logger

```javascript
const express = require('express');
const app = express();

// Middleware 1: A simple logger
const logger = (req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
};

// Middleware 2: A fake Auth check
const checkAdmin = (req, res, next) => {
  if (req.query.admin === 'true') {
    next();
  } else {
    res.status(403).send('Access Denied: Admins Only');
  }
};

app.use(logger); // Runs for every request

app.get('/dashboard', checkAdmin, (req, res) => {
  res.send('Welcome to the Secret Dashboard!');
});

app.listen(3000);
```

---

## 📐 Visualizing the Onion Model

```text
       REQUEST
          │
    ┌─────▼─────┐
    │  Layer 1  │ (Start Timer)
    │ ┌───▼───┐ │
    │ │Layer 2│ │ (Auth Check)
    │ │ ┌─▼─┐ │ │
    │ │ │APP│ │ │ (The actual code)
    │ │ └─┬─┘ │ │
    │ │Layer 2│ │ (Add Headers)
    │ └───┬───┘ │
    │  Layer 1  │ (End Timer)
    └─────┬─────┘
          │
       RESPONSE
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### The `next()` Callback
In the Express source code, `next()` is basically just a pointer to the next function in an internal array. When you call `next()`, Express just calls `stack[index++]()`. If you forget to call `next()`, the request will stay "Hanging" forever, and the browser will eventually timeout. This is why you should always either `res.send()` or call `next()`.

---

## 💼 Interview Questions

**Q1: What is the difference between `app.use()` and `app.get()`?**
> **Ans:** `app.use()` applies the middleware to **all** requests (GET, POST, etc.) and all paths. `app.get()` only applies to a specific path and only for GET requests.

**Q2: How do you handle errors in middleware?**
> **Ans:** Express has special **Error Middleware**. It is a function with **4 arguments** instead of 3: `(err, req, res, next)`. If you call `next(error)` in any previous middleware, Express will skip everything else and jump straight to this error handler.

**Q3: What happens if you don't call `next()`?**
> **Ans:** The request will hang. The client (browser) will keep waiting for a response until it eventually times out.

---

## ⚖️ Trade-offs

| Model | Benefit | Cost |
| :--- | :--- | :--- |
| **Linear (Express)** | Very simple to understand and write. | Hard to do "post-processing" after the response is sent. |
| **Onion (Koa)** | Extremely powerful for logging and cleanup. | Requires understanding of `async/await`. |
| **Custom Composition**| Fully flexible. | Hard to maintain and debug for new team members. |

---

## 🔗 Navigation

**Prev:** [05_Worker_Threads.md](05_Worker_Threads.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [07_Event_Loop_Node_vs_Browser.md](07_Event_Loop_Node_vs_Browser.md)
