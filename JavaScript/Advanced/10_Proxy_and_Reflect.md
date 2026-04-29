# 📌 10 — Proxy & Reflect

## 🌟 Introduction

**Proxy** and **Reflect** are tools for **Metaprogramming** (writing code that manages other code).

-   **Proxy:** Think of it as a **Security Guard** standing in front of an object. Every time you try to read or change the object, the guard intercepts you and decides what to do.
-   **Reflect:** Think of it as the **Master Key**. It's a built-in object that provides methods for interceptable JavaScript tasks.

---

## 🏗️ The Proxy Pattern

A Proxy is created with two things:
1.  **Target:** The original object you want to wrap.
2.  **Handler:** An object containing "Traps" (functions that intercept actions).

```javascript
const target = { name: "Nishant", age: 25 };

const handler = {
  // The "get" trap intercepts reading a property
  get: (obj, prop) => {
    console.log(`Reading property: ${prop}`);
    return obj[prop];
  }
};

const proxy = new Proxy(target, handler);

console.log(proxy.name); 
// Output: 
// Reading property: name
// Nishant
```

---

## 🏗️ Reflect: The Companion

Inside a Proxy trap, you often want to perform the original action. You *could* do it manually, but using `Reflect` is safer and cleaner.

```javascript
const handler = {
  set: (obj, prop, value) => {
    if (prop === "age" && value < 0) {
      console.error("Age cannot be negative!");
      return false;
    }
    // Use Reflect to perform the actual setting
    return Reflect.set(obj, prop, value);
  }
};
```

---

## 🚀 Common Use Cases

1.  **Validation:** Ensure data follows certain rules before saving it to an object.
2.  **Logging:** Track who accessed what data and when (great for debugging).
3.  **Reactivity:** Automatically update the UI when an object changes (this is how **Vue 3** works!).
4.  **Security:** Hide certain properties or make an object read-only.

---

## 📐 Visualizing the Interception

```text
CODE ──▶ [ PROXY (Guard) ] ──▶ [ TARGET (Object) ]
           │    ▲
           │    │
           └────┴── Traps (get, set, delete...)
```

---

## ⚡ Comparison Table

| Feature | Regular Object | Proxy Object |
| :--- | :--- | :--- |
| **Access** | Direct and fast. | Indirect (goes through handler). |
| **Control** | None (public by default). | High (can intercept everything). |
| **Performance** | Best. | Slight overhead due to trap calls. |
| **Use Case** | Most standard coding tasks. | Frameworks, validation, logging. |

---

## 🔬 Deep Technical Dive (V8 Internals)

### Inline Cache (IC) Invalidation
V8 uses **Inline Caching** to speed up property lookups. However, because a Proxy can return *anything* dynamically, V8 **cannot cache** property lookups for Proxies. This is why property access on a Proxy is significantly slower than on a regular object. **Avoid using Proxies in high-frequency loops.**

---

## 💼 Interview Questions

**Q1: What is a "Trap" in a Proxy?**
> **Ans:** A trap is a method in the handler object that intercepts a specific operation, such as `get`, `set`, `has`, or `deleteProperty`.

**Q2: Why should we use `Reflect` instead of just using `target[prop]`?**
> **Ans:** `Reflect` methods return a boolean (true/false) indicating if the operation succeeded, whereas direct assignment might fail silently. It also handles edge cases with `this` binding and inherited properties more correctly.

**Q3: How does Vue 3 use Proxies?**
> **Ans:** Vue 3 wraps your data in a Proxy. When you read a value (`get`), it records that the current component depends on that value. When you change a value (`set`), it automatically triggers a re-render of all components that used that value.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Proxy** | Powerful control over object behavior. | Slower performance than regular objects. |
| **Reflect** | Clean, standardized way to handle objects. | Requires learning a new set of API methods. |
| **Object.defineProperty** | Faster for specific properties. | Cannot intercept "new" properties or deletions. |

---

## 🔗 Navigation

**Prev:** [09_Modules_System.md](09_Modules_System.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [11_Symbols_and_Iterators.md](11_Symbols_and_Iterators.md)
