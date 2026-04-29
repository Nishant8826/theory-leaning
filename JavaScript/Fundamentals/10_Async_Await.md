# 📌 10 — Async/Await

## 🌟 Introduction

**Async/Await** is a special syntax that allows you to work with Promises in a way that looks and behaves like synchronous code. It is essentially **"Syntactic Sugar"** built on top of Promises.

-   **`async`**: Used to define a function that will always return a Promise.
-   **`await`**: Used inside an `async` function to "pause" execution until a Promise is resolved.

---

## 🏗️ How it Works

When the JavaScript engine hits an `await` line, it doesn't "freeze" the whole program. Instead:
1.  It **suspends** the execution of that specific `async` function.
2.  It moves the function out of the **Call Stack**.
3.  The engine continues running other code (like event listeners or other timers).
4.  Once the awaited Promise is ready, the function is pushed back onto the **Call Stack** and resumes exactly where it left off.

---

## 📐 Visualizing the Execution Suspension

```text
 CALL STACK                WEB APIs / HEAP             MICROTASK QUEUE
 ──────────────────        ───────────────────         ───────────────────
 [ asyncFunc() ] ──▶ await ──▶ [ Promise ] 
       │                         │
       ▼ (POPPED)                ▼ (Waiting...)
 [ (Other Code) ]                                      ┌────────────────┐
                                 │                     │ [ asyncFunc ]  │
                                 └──── (Resolved) ───▶ │ [  Resume   ]  │
                                                       └────────────────┘
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: The "Async Waterfall" (Performance bottleneck).**
> **Problem:** My page takes 5 seconds to load, even though each API call only takes 1 second.
> **Reason:** You are `await`ing three independent API calls one by one. `await A(); await B(); await C();` Each one waits for the previous one to finish.
> **Fix:** Start all promises at once and then await them together: `await Promise.all([A(), B(), C()])`.

**P2: Forgotten `await` bug.**
> **Problem:** My variable `data` is a Promise object instead of the actual data.
> **Reason:** You called an `async` function but forgot the `await` keyword. JavaScript continued to the next line immediately.
> **Fix:** Always check if the function you are calling is `async`. Use a linter (like ESLint) to warn you about un-awaited promises.

**P3: `try-catch` not catching errors.**
> **Problem:** An error happened, but my `catch` block didn't run.
> **Reason:** You likely forgot to `await` the promise inside the `try` block. If you just `return` a promise without `await`ing it, the error will bypass the local `catch` and bubble up to whoever called the function.
> **Fix:** Use `return await myPromise()` if you want the local `try-catch` to handle the error.

---

## 🛡️ Error Handling with `try...catch`

```javascript
async function safeFetch() {
  try {
    const response = await fetch("https://api.example.com");
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Oops! Something went wrong:", error);
  }
}
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Generators Under the Hood
Internally, V8 implements `async/await` using **Generators**. When you `await`, V8 effectively calls `.next()` on an internal generator. The "local variables" of your async function are saved into a **JSGeneratorObject** on the heap while the function is suspended.

---

## 💼 Interview Questions

**Q1: What does an `async` function return?**
> **Ans:** It always returns a **Promise**.

**Q2: Can you use `await` in the global scope?**
> **Ans:** Only in **ES Modules** (Top-Level Await).

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Readability** | Looks like synchronous code. | Can lead to "Waterfall" performance bugs. |
| **Error Handling** | Uses standard `try...catch`. | Forgotten `await` keywords cause bugs. |

---

## 🔗 Navigation

**Prev:** [09_Promises.md](09_Promises.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [11_Microtasks_vs_Macrotasks.md](11_Microtasks_vs_Macrotasks.md)
