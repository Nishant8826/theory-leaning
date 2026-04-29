# 📌 04 — Scope & Lexical Environment

## 🌟 Introduction

**Scope** is the area where a variable is accessible. If you try to use a variable outside its scope, JavaScript will throw an error saying it's "not defined."

**Lexical Environment** is the technical term for the internal structure that manages scope. It consists of the variables in the current "box" plus a reference to the **outer** "box".

---

## 🏗️ The Scope Chain (The "Search")

When you look for a variable, JavaScript starts in the **current scope**. If it's not there, it looks in the **parent scope**. It keeps going up until it reaches the **Global Scope**. This path is called the **Scope Chain**.

> [!TIP]
> **Lexical** means "determined at write-time." Your scope is defined by where you **wrote** the code, not where you **called** it.

---

## 📚 Types of Scope

1.  **Global Scope:** Accessible everywhere.
2.  **Function Scope:** Variables (`var`, `let`, `const`) defined inside a function.
3.  **Block Scope:** Variables (`let`/`const`) defined inside `{ }`.

---

## 📐 Visualizing the Scope Chain

```text
 [ GLOBAL SCOPE ] (Root)
        │
        ▼
 [ OUTER FUNCTION ] ──────────┐
        │                     │
        ▼                     ▼
 [ INNER FUNCTION ]     [ ANOTHER FUNCTION ]
        │
        ▼
 [ LOOKUP PATH ] (Checks Inner -> Outer -> Global)
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: "Variable is not defined" even though I see it in the file.**
> **Problem:** `ReferenceError: x is not defined`.
> **Reason:** You are likely trying to access a variable that is defined inside a function or a block from the outside. Scope only flows **down** (inward), not **up** (outward).
> **Fix:** Move the variable to a common parent scope or return the value from the function.

**P2: "Shadowing" bugs.**
> **Problem:** I updated `x` in my `if` block, but the `x` outside didn't change.
> **Reason:** You used `let` or `const` inside the block with the same name as the outer variable. This created a **new** variable that "shadowed" the original.
> **Fix:** Avoid reusing variable names in nested scopes, or be intentional about whether you are creating a new variable or updating an existing one.

**P3: Global Namespace Pollution.**
> **Problem:** My third-party library is crashing because it's using the same global variable name as my app.
> **Reason:** You defined too many variables in the **Global Scope**.
> **Fix:** Wrap your code in an IIFE (Immediately Invoked Function Expression) or use ES Modules to create private local scopes.

---

## 🔍 Code Walkthrough: The Search

```javascript
var a = "Global";

function outer() {
  var b = "Outer";
  
  function inner() {
    var c = "Inner";
    console.log(a, b, c); // "Global Outer Inner"
  }
  
  inner();
}

outer();
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Environment Records
V8 doesn't just "look up" names dynamically every time. At compile-time, V8's parser calculates exactly how many "hops" up the scope chain are needed to find a variable. It then uses a direct memory index (O(1) access).

---

## 💼 Interview Questions

**Q1: What is the difference between Scope and Context?**
> **Ans:** **Scope** is about the visibility of variables. **Context** is about the value of `this`.

**Q2: What is "Lexical Scope"?**
> **Ans:** It means that the scope of a variable is determined by its position in the source code. It is locked in when the function is defined.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Global Scope** | Shared data. | Namespace pollution; hard-to-track bugs. |
| **Block Scope** | Prevents variable leakage. | None (best practice). |

---

## 🔗 Navigation

**Prev:** [03_Hoisting.md](03_Hoisting.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [05_Closures.md](05_Closures.md)
