# 📌 07 — Prototype & Inheritance

## 🌟 Introduction

In JavaScript, **Inheritance** is handled differently than in languages like Java or C++. Instead of "copying" methods from a class to an object, JavaScript uses **Prototypal Inheritance**.

Every object has a hidden property called `[[Prototype]]` (accessible via `__proto__`) that points to another object. This "parent" object is called its **Prototype**.

---

## 🏗️ The Prototype Chain (The "Delegation")

When you try to access a property on an object:
1.  JS looks at the **object itself**.
2.  If not found, it looks at the **object's prototype**.
3.  If still not found, it looks at the **prototype's prototype**.
4.  It keeps going until it reaches `null`. This is the **Prototype Chain**.

---

## 📚 `__proto__` vs `prototype`

1.  **`__proto__` (The Link):** Exists on **every object**.
2.  **`prototype` (The Blueprint):** Exists only on **Constructor Functions**.

---

## 📐 Visualizing the Prototype Hierarchy

```text
 [ CONSTRUCTOR FUNCTION ]         [ PROTOTYPE OBJECT ]
        │                                 ▲
        │ (.prototype) ───────────────────┘
        │
        ▼ (new)
 [ INSTANCE OBJECT ]
        │
        │ (__proto__) ────────────────────┘
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: "Property shadowing" leads to unexpected values.**
> **Problem:** I added `name` to my object, but the prototype also has a `name`. Which one wins?
> **Reason:** The Prototype Chain search stops at the **first match**. If the object has the property, it never looks at the prototype.
> **Fix:** Be careful when using property names that might conflict with prototype methods (like `toString` or `valueOf`).

**P2: Prototype Pollution (Security Risk).**
> **Problem:** An attacker sends a malicious JSON object `{ "__proto__": { "admin": true } }`.
> **Reason:** If you merge this object into your app's config without sanitizing, you might accidentally update `Object.prototype`, making *every* object in your app have `admin: true`.
> **Fix:** Use `Object.create(null)` for plain data objects, or use `Map` which doesn't have a prototype chain.

**P3: Performance lag on very deep chains.**
> **Problem:** Accessing a method is slow.
> **Reason:** Your inheritance chain is 10 levels deep. Every lookup has to walk all 10 steps to find the method.
> **Fix:** Keep your inheritance hierarchies shallow. Favor "Composition" over "Inheritance" (mixins or simple object merging).

---

## 🔄 Classes: The "Sugar"

In modern JavaScript (ES6+), we use the `class` keyword. However, under the hood, it is still using the **Prototype Chain**.

---

## 🔬 Deep Technical Dive (V8 Internals)

### Hidden Classes (Maps)
V8 uses "Hidden Classes" to optimize property access. If two objects have the same properties in the same order, they share the same Hidden Class. Mutating the prototype of an object at runtime is very expensive because it forces V8 to throw away these optimizations.

---

## 💼 Interview Questions

**Q1: What is a Prototype?**
> **Ans:** A prototype is an object from which other objects inherit properties and methods.

**Q2: How do you create an object without a prototype?**
> **Ans:** Use `Object.create(null)`.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Delegation** | Huge memory savings. | Slight performance hit for deep chains. |
| **Class Syntax** | Easier readability. | Hides the reality of prototypes. |

---

## 🔗 Navigation

**Prev:** [06_This_Keyword.md](06_This_Keyword.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [08_Event_Loop.md](08_Event_Loop.md)
