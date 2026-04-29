# 📌 01 — Deep vs Shallow Copy

## 🌟 Introduction

In JavaScript, when you "copy" an object or an array, you might only be copying the **reference** (the address) to that object, not the actual data. This is where the difference between **Shallow** and **Deep** copy comes in.

-   **Shallow Copy:** Copies the top-level properties. If there are nested objects, they still point to the same memory location as the original.
-   **Deep Copy:** Copies everything, including nested objects.

---

## 🏗️ Shallow Copy

A shallow copy is fast and easy, but it **only goes one level deep**.

```javascript
const user = { name: "Nishant", address: { city: "Delhi" } };
const copy = { ...user };

copy.address.city = "Mumbai"; // 💥 Affects BOTH 'user' and 'copy'!
```

---

## 🏗️ Deep Copy

A deep copy creates a completely new copy of every nested object.

```javascript
const user = { name: "Nishant", address: { city: "Delhi" } };
const copy = structuredClone(user);

copy.address.city = "Mumbai"; // Only affects 'copy'
```

---

## 📐 Visualizing the Memory Reference

```text
 SHALLOW COPY (Shared Nesting)
 Original ──▶ [ name: "A", address: * ] ──┐
                                          │
                                          ▼
 Copy     ──▶ [ name: "B", address: * ] ──▶ { city: "Delhi" }
                                            (Shared Object)

 ──────────────────────────────────────────────────────────

 DEEP COPY (Independent Nesting)
 Original ──▶ [ name: "A", address: * ] ──▶ { city: "Delhi" }
 
 Copy     ──▶ [ name: "B", address: * ] ──▶ { city: "Delhi" }
                                            (Separate Object)
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: Unexpected "state mutation" in React or Redux.**
> **Problem:** I updated a copy of my state, but my UI didn't re-render, or other parts of the app changed unexpectedly.
> **Reason:** You used a **Shallow Copy** on a nested object. React only checks if the top-level object reference changed. If you mutated a nested property, React might not detect it, or you might have accidentally changed the original state.
> **Fix:** Use the spread operator at every level of nesting `{...state, user: {...state.user, name: 'New'}}` or use `structuredClone`.

**P2: "Data Loss" when using the JSON stringify trick.**
> **Problem:** My object had a date and a function, but after `JSON.parse(JSON.stringify(obj))`, the function is gone and the date is a string.
> **Reason:** JSON does not support functions, undefined, or Date objects. It is a "lossy" format.
> **Fix:** Use `structuredClone()` which is the modern, native way to deep copy while preserving Dates, Maps, Sets, etc.

**P3: "Data Clone Error" when using `structuredClone`.**
> **Problem:** `Uncaught DOMException: ... could not be cloned.`
> **Reason:** You tried to deep copy an object that contains a **Function**, a **DOM Node**, or an **Error object**. `structuredClone` only works for data.
> **Fix:** If you need to copy logic (functions), you shouldn't be "cloning" the object; you should probably be using a Class or a Factory function to create a new instance.

---

## 🔬 Deep Technical Dive (V8 Internals)

### Memory Pointers
In V8, an object property doesn't always "hold" the object. It holds a **Pointer** (memory address). When you perform a shallow copy, you are just copying the pointer (the address), not the house at that address.

---

## 💼 Interview Questions

**Q1: What is the main drawback of using `JSON.stringify` for deep copying?**
> **Ans:** It's "lossy." It cannot copy functions, `undefined`, or circular references.

**Q2: When should you use a shallow copy?**
> **Ans:** Use it when the object is "flat" or when you want to share state for performance reasons.

---

## ⚖️ Trade-offs

| Feature | Shallow Copy | Deep Copy |
| :--- | :--- | :--- |
| **Speed** | Very Fast | Slower (recursive) |
| **Memory** | Low usage | Higher usage |

---

## 🔗 Navigation

**Prev:** [../Fundamentals/12_Execution_Order_Deep_Dive.md](../Fundamentals/12_Execution_Order_Deep_Dive.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [02_Memory_Management.md](02_Memory_Management.md)
