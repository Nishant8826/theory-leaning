# 📌 08 — Immutability

## 🌟 Introduction

**Immutability** means that once a piece of data is created, it **cannot be changed**.

If you want to modify an immutable object, you don't edit the original. Instead, you create a **new copy** with the changes you want.

Think of it like a **Photograph**:
-   You can't change the person's pose in a photo after it's taken.
-   If you want a different pose, you take a **new photo**.

---

## 🏗️ Why Use Immutability?

1.  **Predictability:** You never have to worry about a function accidentally changing your data.
2.  **Tracking Changes:** In frameworks like React, it's very fast to check if data has changed by comparing the "address" (reference) of the object (`oldData === newData`).
3.  **Time Travel:** It makes features like "Undo/Redo" very easy because you have a history of all previous states.

---

## 🛠️ Immutability in JavaScript

### 1. `const` (The Weakest)
`const` prevents you from **reassigning** a variable, but it does **not** stop you from changing the contents of an object.
```javascript
const user = { name: "Nishant" };
user.name = "Rahul"; // ✅ This works! (Not truly immutable)
```

### 2. `Object.freeze()` (Shallow)
`Object.freeze()` stops you from changing properties, but it **only goes one level deep**.
```javascript
const user = { name: "Nishant", address: { city: "Delhi" } };
Object.freeze(user);

user.name = "Rahul"; // ❌ Fails silently (or throws error in strict mode)
user.address.city = "Mumbai"; // ✅ This STILL works! (Nested object not frozen)
```

---

## 🚀 The Modern Way: Structural Sharing

When we "copy" an object to make a change, we don't copy everything. We reuse the parts that didn't change to save memory. This is called **Structural Sharing**.

```javascript
const state = {
  user: { name: "Nishant" },
  posts: [1, 2, 3]
};

// We want to change the name:
const nextState = {
  ...state, // Copy existing state
  user: { name: "Rahul" } // Overwrite only the user
};

// Verification:
console.log(state.user === nextState.user);   // false (User changed)
console.log(state.posts === nextState.posts); // true (Posts are SHARED!)
```

---

## 📐 Visualizing Structural Sharing

```text
STATE V1: [ USER ] ──▶ { name: "Nishant" }
             │
          [ POSTS ] ──┐
                      │
STATE V2: [ USER ] ───┼──▶ { name: "Rahul" } (New object)
             │        │
          [ POSTS ] ──┘ (Same memory as V1!)
```

---

## ⚡ Comparison Table

| Feature | Mutation (Mutable) | Immutability |
| :--- | :--- | :--- |
| **Logic** | Change the original data. | Create new data for every change. |
| **Performance** | Faster for small, simple apps. | Faster for complex apps (Change detection). |
| **Bugs** | Higher risk (Side effects). | Lower risk (Predictable). |
| **Memory** | Low (reused). | Slightly higher (new objects created). |

---

## 🔬 Deep Technical Dive (V8 Internals)

### Inline Caching (IC)
When an object is frozen using `Object.freeze()`, V8 knows that its properties will never change. This allows the engine to perform **aggressive optimizations** because it can "hardcode" the location of properties in memory without worrying they might move or disappear later.

---

## 💼 Interview Questions

**Q1: Is `const` sufficient for immutability?**
> **Ans:** No. `const` only prevents reassignment. To make an object truly immutable, you need `Object.freeze()` or use immutable patterns like the spread operator.

**Q2: What are the benefits of Immutability in React?**
> **Ans:** React uses "Shallow Comparison" to decide if a component should re-render. If you mutate an object, the reference stays the same, and React might not see the change. If you use immutability, the reference changes, and React updates correctly.

**Q3: Does immutability waste memory?**
> **Ans:** A little bit, but modern engines and techniques like **Structural Sharing** ensure that only the changed parts are newly allocated. Most of the data is reused between the old and new versions.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Spread `...`** | Simple and native to JS. | Can be verbose for very deep objects. |
| **`Object.freeze`** | Built-in protection. | Shallow only; requires a recursive function for deep freeze. |
| **Immer.js** | Best developer experience; write "mutable" code that becomes immutable. | Adds a small library dependency. |

---

## 🔗 Navigation

**Prev:** [07_Composition_vs_Inheritance.md](07_Composition_vs_Inheritance.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [09_Modules_System.md](09_Modules_System.md)
