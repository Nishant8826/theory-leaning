# 📌 06 — Currying

## 🌟 Introduction

**Currying** is a functional programming technique where a function with multiple arguments is transformed into a series of nesting functions, each taking a **single argument**.

Instead of calling `add(1, 2, 3)`, you call `add(1)(2)(3)`.

Think of it like a **Vending Machine**:
-   You don't put in all the money at once.
-   You put in one coin (argument).
-   The machine waits.
-   You put in another coin.
-   Once the total price is met, you get your snack (the result).

---

## 🏗️ How it Works

Currying relies on **Closures**. Each inner function "remembers" the arguments passed to its parent.

```javascript
// Normal function
function add(a, b) {
  return a + b;
}

// Curried function
function curriedAdd(a) {
  return function(b) {
    return a + b;
  };
}

const addFive = curriedAdd(5); // 'a' is remembered as 5
console.log(addFive(10)); // 15
console.log(addFive(20)); // 25
```

---

## 🚀 Practical Use Case: Specialized Loggers

Currying is great for creating "presets" or specialized versions of a general function.

```javascript
const logger = (level) => (message) => {
  console.log(`[${level.toUpperCase()}] ${message}`);
};

// Create specialized loggers
const infoLog = logger("info");
const errorLog = logger("error");

infoLog("App started");   // [INFO] App started
errorLog("Failed to connect"); // [ERROR] Failed to connect
```

---

## 📐 Visualizing the Chain

```text
curriedAdd(5)
   │
   └── returns a function(b) { return 5 + b }
          │
          └── called with (10)
                 │
                 └── returns 15
```

---

## ⚡ Currying vs. Partial Application

They are often confused, but they are slightly different:
-   **Currying:** Always breaks a function down into steps of **exactly one** argument.
-   **Partial Application:** Pre-fills some arguments but can return a function that takes **multiple** arguments.

---

## 🔍 Code Walkthrough: Advanced Auto-Curry

In real projects, we use a utility to turn any normal function into a curried one.

```javascript
function curry(fn) {
  return function curried(...args) {
    // If we have enough arguments, run the original function
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    // Otherwise, return a new function to collect more arguments
    return function (...moreArgs) {
      return curried.apply(this, args.concat(moreArgs));
    };
  };
}

const sum = (a, b, c) => a + b + c;
const curriedSum = curry(sum);

console.log(curriedSum(1)(2)(3)); // 6
console.log(curriedSum(1, 2)(3)); // 6 (Hybrid approach)
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Arity (`fn.length`)
In JavaScript, every function has a `length` property that tells you how many arguments it expects. A currying utility uses this to know when to stop returning functions and finally execute the result.

### Memory Overhead
Every step of a curried function creates a new **Closure** and a new **Function Object** in the Heap. While this is fine for most apps, using deep currying chains in high-performance game loops might add pressure to the Garbage Collector.

---

## 💼 Interview Questions

**Q1: What is Currying?**
> **Ans:** It is a technique of evaluating a function with multiple arguments into a sequence of functions with a single argument.

**Q2: What is the main benefit of Currying?**
> **Ans:** It helps in **Function Composition** and **Reusability**. It allows you to create specialized functions from generic ones by pre-filling some arguments.

**Q3: How does Currying use Closures?**
> **Ans:** Each function in the chain "closes over" the arguments of the previous functions, keeping them in memory until the final calculation is made.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Reusability** | Create "pre-configured" functions easily. | Can make code harder to read for beginners. |
| **Composition** | Perfect for functional programming pipelines. | Slight memory overhead due to multiple closures. |
| **Cleanliness** | Avoids passing the same arguments repeatedly. | Debugging can be trickier (multiple stack frames). |

---

## 🔗 Navigation

**Prev:** [05_Debouncing_vs_Throttling.md](05_Debouncing_vs_Throttling.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [07_Composition_vs_Inheritance.md](07_Composition_vs_Inheritance.md)
