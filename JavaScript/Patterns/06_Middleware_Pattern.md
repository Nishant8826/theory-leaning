# 📌 06 — Middleware Pattern

## 🌟 Introduction

You might have seen **Middleware** in Node.js (Express), but it is actually a universal design pattern used in many places, like Redux, GraphQL, and even data processing pipelines.

Think of it like a **Baton Race**:
-   Each runner (Function) carries the baton (The Data).
-   They can do something while they have the baton (like log it or clean it).
-   When they are done, they hand the baton to the next runner using `next()`.
-   The race ends when the last runner reaches the finish line (The Response).

---

## 🏗️ How it Works: The Chained Pipeline

The heart of this pattern is a "stack" of functions that execute in order.

```javascript
class Pipeline {
  constructor() {
    this.stack = [];
  }

  // Add a new "Station" to the pipeline
  use(fn) {
    this.stack.push(fn);
  }

  // Run the whole pipeline
  run(data) {
    let index = 0;

    const next = () => {
      if (index < this.stack.length) {
        const currentFunction = this.stack[index++];
        currentFunction(data, next); // Pass data and the 'next' trigger
      }
    };

    next(); // Start the first function
  }
}

const p = new Pipeline();

p.use((data, next) => {
  data.value += 10;
  console.log("Added 10");
  next();
});

p.use((data, next) => {
  data.value *= 2;
  console.log("Multiplied by 2");
  next();
});

const myData = { value: 5 };
p.run(myData);
console.log(myData.value); // 30
```

---

## 🚀 Common Use Cases

1.  **Redux Middleware:** Intercepting actions to log them or handle async API calls (like Redux Thunk).
2.  **Data Cleaning:** A pipeline where Step 1 removes whitespace, Step 2 removes HTML tags, and Step 3 converts to lowercase.
3.  **Command Validation:** Checking if a user has permission at different levels (e.g., "Is logged in?" -> "Is Admin?" -> "Has enough balance?").

---

## 📐 Visualizing the Pipeline (The "Onion" Model)

In many systems (like Koa), middleware isn't just a straight line; it's an **Onion**. You go **IN** through the layers, and then you come back **OUT**.

```text
    REQUEST PHASE (IN)              RESPONSE PHASE (OUT)
    ──────────────────▶            ◀──────────────────
    
    ┌──────────────────────────────────────────────────┐
    │  Middleware 1 (Logger)                           │
    │  ┌────────────────────────────────────────────┐  │
    │  │  Middleware 2 (Auth)                       │  │
    │  │  ┌──────────────────────────────────────┐  │  │
    │  │  │  Middleware 3 (Router)               │  │  │
    │  │  │  ┌────────────────────────────────┐  │  │  │
    │  │  │  │      CORE LOGIC / HANDLER      │  │  │  │
    │  │  │  └────────────────────────────────┘  │  │  │
    │  │  └──────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────┘  │
    └──────────────────────────────────────────────────┘
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: The "Hanging" Request**
> **Problem:** My application just stops responding, and the browser loading spinner spins forever.
> **Reason:** Someone forgot to call `next()`. If a middleware doesn't call `next()` and doesn't send a response, the pipeline is broken, and the "baton" is dropped.
> **Fix:** Always ensure every logical path in your middleware either calls `next()` or finishes the request (e.g., `res.send()`).

**P2: "Heads Already Sent" Error**
> **Problem:** `Error [ERR_HTTP_HEADERS_SENT]: Cannot set headers after they are sent to the client.`
> **Reason:** You called `next()` but *also* tried to send a response in the same middleware, or a later middleware sent a response and the current one tried to send another.
> **Fix:** Use `return next()` to ensure you stop executing the current function after handing over the baton.

**P3: Middleware Ordering Bugs**
> **Problem:** My `req.user` is undefined even though I have Auth middleware.
> **Reason:** The middleware that uses `req.user` is defined *before* the Auth middleware in the stack.
> **Fix:** Order matters! Always place "Data Population" middleware (Auth, BodyParser) at the very top of the stack.

---

## 🔬 Deep Technical Dive (V8 Internals)

### Recursive Depth
Most middleware engines use recursion to implement `next()`. In V8, every function call adds a frame to the **Call Stack**. If you have a pipeline with 1,000 middlewares, you might hit a `RangeError: Maximum call stack size exceeded`. This is why high-performance engines (like Fastify) use optimized loops instead of pure recursion to keep the memory footprint low.

---

## 💼 Interview Questions

**Q1: Why use Middleware instead of just calling 5 functions in a row?**
> **Ans:** Flexibility. With the Middleware pattern, the functions don't need to know about each other. You can dynamically add or remove "stations" in the pipeline without changing the code inside the functions themselves.

**Q2: How does Redux middleware differ from Express middleware?**
> **Ans:** They are very similar, but Redux uses a more "functional" approach (currying): `store => next => action => { ... }`. Express uses the more traditional `(req, res, next) => { ... }` style.

**Q3: What is "Error-First" middleware?**
> **Ans:** It’s a convention where if something goes wrong, you call `next(error)`. The pipeline then skips all normal stations and jumps straight to the "Error Handler" station at the end.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Middleware Pattern** | Highly decoupled and reusable. | Can be hard to debug if the pipeline is too long. |
| **Simple Chain** | Easy to follow. | Rigid; hard to change the order at runtime. |
| **Events (Pub/Sub)** | Total isolation. | No guaranteed order of execution. |

---

## 🔗 Navigation

**Prev:** [05_Strategy_Pattern.md](05_Strategy_Pattern.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [07_Reactive_Patterns.md](07_Reactive_Patterns.md)
