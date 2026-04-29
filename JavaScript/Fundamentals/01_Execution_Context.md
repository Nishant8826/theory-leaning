# 📌 01 — Execution Context

## 🌟 Introduction

In JavaScript, **Execution Context** is the most fundamental concept to understand. Think of it as an **environment** or a **box** that contains everything needed to execute a piece of code.

Whenever you run a JavaScript program, the engine creates these "boxes" to keep track of variables, functions, and the value of `this`.

---

## 🏗️ The Two Main Types

1.  **Global Execution Context (GEC):** 
    - Created when you start running your script.
    - There is only **one** GEC.
    - It creates the `window` object (in browsers) and sets `this` to it.
2.  **Function Execution Context (FEC):**
    - Created every time a function is **invoked** (called).
    - Each function call gets its own brand new context.

---

## 🔄 The Life Cycle (The "Two Phases")

This is where the magic happens. Every Execution Context is created in two distinct phases:

### Phase 1: Creation Phase (Memory Allocation)
Before a single line of code runs, the JS engine scans the code and:
-   **Allocates memory** for variables and functions.
-   **Hoisting:** Variables are set to `undefined` (if declared with `var`) or left uninitialized (if `let`/`const`).
-   **Functions:** The entire function body is stored in memory.
-   **Scope Chain:** It determines which variables the context has access to.
-   **`this` Binding:** The value of `this` is determined.

### Phase 2: Execution Phase (Code Running)
The engine starts executing the code line-by-line:
-   Assigns actual values to variables.
-   Executes function calls.

> [!IMPORTANT]
> **Hoisting** is simply the result of Phase 1. JavaScript doesn't physically move your code to the top; it just sets aside memory for it before running.

---

## 📚 The Execution Context Stack (Call Stack)

JavaScript is **single-threaded**, meaning it can only do one thing at a time. To manage multiple Execution Contexts, it uses a **Call Stack** (a LIFO - Last In, First Out structure).

---

## 📐 Visualizing the Execution Context (The "Box" Model)

```text
 ┌──────────────────────────────────────────────────────────┐
 │                  EXECUTION CONTEXT                       │
 ├──────────────────────────┬───────────────────────────────┤
 │     MEMORY COMPONENT     │        CODE COMPONENT         │
 │     (Variable Env)       │      (Thread of Execution)    │
 ├──────────────────────────┼───────────────────────────────┤
 │ a: 10                    │ var a = 10;                   │
 │ square: { ... }          │ function square(n) { ... }    │
 │ ans: undefined           │ var ans = square(a);          │
 └──────────────────────────┴───────────────────────────────┘
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: "Cannot access 'x' before initialization"**
> **Problem:** Your code crashes with a `ReferenceError` when using `let` or `const`.
> **Reason:** You are in the **Temporal Dead Zone (TDZ)**. During the Creation Phase, `let` and `const` are allocated memory but NOT initialized. Accessing them before the line where they are defined is forbidden.
> **Fix:** Always declare your `let` and `const` variables at the very top of their scope.

**P2: "Uncaught RangeError: Maximum call stack size exceeded"**
> **Problem:** The app crashes when running a recursive function.
> **Reason:** You have created too many **Function Execution Contexts** without closing any. The Call Stack has a limited size (usually ~10,000 frames).
> **Fix:** Check your recursion base case or use an iterative `while` loop to avoid pushing too many boxes onto the stack.

**P3: `this` is returning `window` instead of my Object.**
> **Problem:** Inside a function, `this.name` is undefined or points to the global object.
> **Reason:** The **`this` binding** happened during the Creation Phase based on *how* the function was called. If called as a regular function `fn()`, `this` defaults to the Global Context.
> **Fix:** Use `.bind()`, `.call()`, or Arrow Functions to ensure the Execution Context has the correct `this` reference.

---

## 🔍 Code Walkthrough

```javascript
var a = 10;
function square(n) {
  var ans = n * n;
  return ans;
}
var square2 = square(a);
```

### What happens inside the "Box"?

1.  **Global Context (Phase 1):** 
    - `a`: `undefined`
    - `square`: `fn { ... }` (stored entirely)
    - `square2`: `undefined`
2.  **Global Context (Phase 2):**
    - `a` becomes `10`.
    - `square(a)` is called $\rightarrow$ Creates **Function Context**.
3.  **Function Context (Phase 1):**
    - `n`: `10` (parameter)
    - `ans`: `undefined`
4.  **Function Context (Phase 2):**
    - `ans` becomes `100`.
    - Returns `100` $\rightarrow$ Function Context is destroyed.
5.  **Global Context (Phase 2 resumed):**
    - `square2` becomes `100`.

---

## 🔬 Deep Technical Dive (Spec & V8 Internals)

### The Internal Record
An Execution Context is a record that holds:
1.  **LexicalEnvironment:** Where `let`, `const`, and function declarations live.
2.  **VariableEnvironment:** Where `var` declarations live.
3.  **PrivateEnvironment:** For class private fields (ES2022+).
4.  **Realm:** The set of built-in objects (Array, Object, etc.).

### V8 Parsing Phase: Scope Analysis
Before execution, V8's **parser** performs a pass to decide if variables live on the **stack** (fast) or the **heap** (slow).
- **Stack-allocated:** Local variables that aren't captured by closures.
- **Context-allocated (Heap):** Variables captured by closures. V8 creates a **Context object** on the heap to ensure they persist even after the function returns.

---

## 💼 Interview Questions

**Q1: What is the difference between LexicalEnvironment and VariableEnvironment?**
> **Ans:** They are both environment records. `var` declarations are stored in `VariableEnvironment`, while `let` and `const` go into `LexicalEnvironment`. This separation is what allows `let`/`const` to have block scope while `var` remains function-scoped.

**Q2: Explain the Temporal Dead Zone (TDZ).**
> **Ans:** In the Creation Phase, `let` and `const` are recognized by the engine but **not initialized**. Accessing them before their declaration line in the Execution Phase throws a `ReferenceError`. This "period" of unreachability is the TDZ.

**Q3: Does every function call create a new Execution Context?**
> **Ans:** Yes. Every time you invoke a function, a brand new Function Execution Context is created and pushed onto the Call Stack.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Hoisting** | Functions can be used before they are defined. | Can lead to confusion/bugs with `var` being `undefined`. |
| **Closures** | Functions remember their Lexical Environment. | Memory overhead (heap allocation for captured variables). |
| **Call Stack** | Predictable execution flow. | Risk of `RangeError: Maximum call stack size exceeded` (Stack Overflow). |

---

## 🔗 Navigation

**Prev:** [00_Index.md](../00_Index.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [02_Call_Stack.md](02_Call_Stack.md)
