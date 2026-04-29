# 📌 Project 02 — Build a Promise from Scratch

## 🌟 Introduction

Building a **Promise** is the "Final Boss" of JavaScript interviews. It requires you to understand closures, classes, state machines, and the event loop all at once.

A Promise is like an **"I Owe You" (IOU) note**:
-   **Pending:** You have the note, but you haven't received the money yet.
-   **Fulfilled:** You got the money! (Success).
-   **Rejected:** The person who gave you the note disappeared. (Error).

---

## 🏗️ 1. The Core Structure

A Promise needs to store its **State**, its **Value**, and a list of **Followers** (the `then` callbacks).

```javascript
class MyPromise {
  constructor(executor) {
    this.state = 'pending';
    this.value = undefined;
    this.callbacks = []; // Functions to run when fulfilled

    const resolve = (val) => {
      if (this.state !== 'pending') return;
      this.state = 'fulfilled';
      this.value = val;
      
      // Run all 'then' functions LATER (as a microtask)
      this.callbacks.forEach(callback => callback(val));
    };

    const reject = (err) => {
      if (this.state !== 'pending') return;
      this.state = 'rejected';
      this.value = err;
    };

    // Run the user's code immediately
    try {
      executor(resolve, reject);
    } catch (e) {
      reject(e);
    }
  }

  then(onFulfilled) {
    // If already finished, run immediately (but async)
    if (this.state === 'fulfilled') {
      onFulfilled(this.value);
    } else {
      // Otherwise, save it for later
      this.callbacks.push(onFulfilled);
    }
    return this; // Allow chaining (simplified)
  }
}
```

---

## 🏗️ 2. The Secret: `queueMicrotask`

In real JavaScript, Promises are **Microtasks**. This means they run *after* the current script finishes, but *before* the browser paints the next frame.

To make our `MyPromise` truly accurate, we should wrap the callback execution in `queueMicrotask()`:

```javascript
const resolve = (val) => {
  this.state = 'fulfilled';
  this.value = val;
  
  queueMicrotask(() => {
    this.callbacks.forEach(cb => cb(val));
  });
};
```

---

## 🚀 3. Testing Your Promise

```javascript
console.log("1. Start");

const p = new MyPromise((resolve) => {
  setTimeout(() => resolve("3. Success!"), 1000);
});

p.then(data => console.log(data));

console.log("2. End");

// Expected Output: 
// 1. Start
// 2. End
// (1 second delay)
// 3. Success!
```

---

## 📐 Visualizing the State Machine

```text
       [ EXECUTOR ]
            │
            ▼
     ┌──────────────┐
     │   PENDING    │
     └──────┬───────┘
            │
    ┌───────┴───────┐
    ▼               ▼
 [ FULFILLED ]   [ REJECTED ]
 (Value)         (Reason)
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Promise Capability
In V8, creating a Promise creates a "Promise Capability" object. This object holds the hidden "Result" and "State" fields. When you call `.then()`, V8 creates a **"PromiseReaction"** object and attaches it to the original promise. If the promise is already resolved, V8 schedules a microtask to run that reaction. If not, it waits. This is why `.then()` can be called multiple times on the same promise—it just adds more reactions to the list.

---

## 💼 Interview Tips

-   **Can a promise change state twice?** No. Once it is Fulfilled or Rejected, it is "Settled" forever.
-   **Why is `then` asynchronous?** To ensure consistency. You don't want your code to be sync sometimes and async other times. `then` is *always* async.
-   **What is "Thenable"?** Any object that has a `.then()` method is considered a "thenable" (like our `MyPromise` class). Real Promises can interact with thenables automatically.

---

## ⚖️ Trade-offs

| Feature | Our Version | Native Promise |
| :--- | :--- | :--- |
| **Chaining** | Basic (returns `this`). | Advanced (returns a *new* promise). |
| **Async Timing** | Uses `queueMicrotask`. | Highly optimized in V8 C++. |
| **Methods** | `on`, `then`. | `all`, `race`, `any`, `allSettled`. |

---

## 🔗 Navigation

**Prev:** [01_Build_Event_Emitter.md](01_Build_Event_Emitter.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Build_LRU_Cache.md](03_Build_LRU_Cache.md)
