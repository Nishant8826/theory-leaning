# 📌 09 — Promises

## 🌟 Introduction

A **Promise** is an object representing the eventual completion (or failure) of an asynchronous operation and its resulting value.

Think of it like a **"Receipt"** at a fast-food restaurant.
1.  You order a burger (start an async task).
2.  The cashier gives you a **receipt** (the Promise).
3.  The receipt is **Pending** while your burger is being cooked.
4.  Eventually, your burger is ready (**Fulfilled**) or they ran out of meat (**Rejected**).

---

## 🏗️ The 3 States of a Promise

1.  **Pending:** Initial state.
2.  **Fulfilled:** Operation completed successfully.
3.  **Rejected:** Operation failed.

---

## 📐 Visualizing the Promise Lifecycle

```text
       ┌───────────────┐
       │   PENDING     │ (ORDER PLACED)
       └───────┬───────┘
               │
       ┌───────┴───────┐
       ▼               ▼
 ┌───────────┐   ┌───────────┐
 │ FULFILLED │   │ REJECTED  │ (BURGER READY vs OUT OF MEAT)
 └─────┬─────┘   └─────┬─────┘
       │               │
    .then()         .catch()
       │               │
       └───────┬───────┘
               ▼
         ┌───────────┐
         │  FINALLY  │ (LEAVING COUNTER)
         └───────────┘
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: "Unhandled Promise Rejection" error.**
> **Problem:** Your server crashes or logs a warning about unhandled rejections.
> **Reason:** You have a promise that failed (Rejected), but you didn't attach a `.catch()` block or a `try-catch` to handle the error.
> **Fix:** Always ensure every promise chain ends with a `.catch()`, or wrap `await` calls in `try-catch`.

**P2: The "Floating" Promise bug.**
> **Problem:** Your code continues to the next line before the async task is done, even though you used a promise.
> **Reason:** You forgot to `return` the promise in a function or a `.then()` block, or you forgot to `await` it. The code "fires and forgets" the task.
> **Fix:** Ensure you return promises in chains and use `await` consistently in async functions.

**P3: `Promise.all` fails too early.**
> **Problem:** I am fetching 100 images, and because 1 failed, I got NO data back at all.
> **Reason:** `Promise.all` is "All or Nothing." It rejects as soon as the first promise fails.
> **Fix:** Use `Promise.allSettled`. It waits for everything to finish (even failures) and returns an array of results telling you which ones worked and which ones didn't.

---

## 🔄 Consuming a Promise

We use "Handlers" to deal with the result of a Promise.

```javascript
fetch("https://api.example.com/data")
  .then((response) => response.json()) // Success
  .then((data) => console.log(data))
  .catch((error) => console.error("Failed:", error)) // Failure
  .finally(() => console.log("Operation Complete")); // Cleanup
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### JSPromise Object
In V8, a Promise is a `JSPromise` object. It contains internal slots like `[[PromiseState]]` and `[[PromiseResult]]`. When you call `resolve()`, V8 updates these slots and then checks the `[[PromiseFulfillReactions]]` list to schedule the `.then()` callbacks.

---

## 💼 Interview Questions

**Q1: What is the benefit of using Promises over Callbacks?**
> **Ans:** Promises solve "Callback Hell" by allowing you to chain operations. They also provide a standardized way to handle errors.

**Q2: What is the output of `Promise.resolve(5)`?**
> **Ans:** It returns a Promise that is already in the **Fulfilled** state with a value of `5`.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Chaining** | Avoids nested callback hell. | Memory overhead for each `.then()`. |
| **Error Propagation** | Standardized error handling. | Errors can be swallowed if you forget `.catch()`. |

---

## 🔗 Navigation

**Prev:** [08_Event_Loop.md](08_Event_Loop.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [10_Async_Await.md](10_Async_Await.md)
