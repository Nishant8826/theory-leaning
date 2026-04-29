# 📌 02 — Factory Pattern

## 🌟 Introduction

In JavaScript, you can create objects using `new Class()` or `{}`. But sometimes, creating an object is complicated. You might need to check certain conditions, set default values, or choose between different types of objects.

The **Factory Pattern** is a function that handles all this complexity for you. It "manufactures" objects and hands them to you.

Think of it like a **Vending Machine**:
-   You don't need to know how to brew coffee or mix soda.
-   You just press a button ("Coffee" or "Soda").
-   The machine does the work and gives you the final product.

---

## 🏗️ Basic Factory Example

Instead of using a `class`, we use a simple function that returns an object.

```javascript
function createUser(role, name) {
  const commonData = {
    name,
    createdAt: new Date(),
    sayHello: function() {
      console.log(`Hello, I am ${this.name} (${this.role})`);
    }
  };

  if (role === 'admin') {
    return { ...commonData, role: 'admin', canDelete: true };
  } else {
    return { ...commonData, role: 'user', canDelete: false };
  }
}

const admin = createUser('admin', 'Nishant');
const user = createUser('user', 'Rahul');

admin.sayHello(); // "Hello, I am Nishant (admin)"
```

---

## 🚀 Why Use a Factory?

1.  **Decoupling:** Your main code doesn't need to know the internal details of how a `User` or a `Product` is built.
2.  **No `new` Keyword:** You don't have to worry about forgetting `new` and breaking your code.
3.  **Privacy:** You can use **Closures** inside the factory to create variables that are truly private and cannot be changed from the outside.
4.  **Conditional Creation:** A single factory can return different types of objects depending on the input.

---

## 🏗️ The "Abstract" Factory

An Abstract Factory is basically a **Factory for Factories**. It’s used in very large apps where you need to create "families" of related objects (like a "Database Factory" that can create either a "MySQL Connection" or a "MongoDB Connection").

---

## 📐 Visualizing the Factory

```text
    [ INPUT: "Admin" ]
            │
            ▼
    ┌───────────────┐
    │  THE FACTORY  │ (Logic: Should I add admin permissions?)
    └───────┬───────┘
            │
            ▼
    [ OUTPUT: Admin Object ]
```

---

## ⚡ Comparison Table

| Feature | Factory Function | Class / Constructor |
| :--- | :--- | :--- |
| **`new` Keyword** | Not required. | **Required.** |
| **Privacy** | Uses Closures (Very strong). | Uses `#` prefix (Recent addition). |
| **`this` Binding**| Rare; usually not needed. | **Critical;** easy to break. |
| **Return Type** | Can return **any** type of object. | Must return an **instance** of the class. |

---

## 🔬 Deep Technical Dive (V8 Internals)

### Prototype Sharing
One downside of simple factory functions is that every object you create gets its own **copy** of the methods (functions). In a `class`, all instances share the same method on the `.prototype`. If you are creating 100,000 objects, a class might use less memory. However, for most apps, the memory difference is tiny, and the flexibility of the Factory is often worth the cost.

---

## 💼 Interview Questions

**Q1: When would you use a Factory instead of a Class?**
> **Ans:** Use a Factory when the object creation logic is complex, when you want true private variables using closures, or when you need to return different types of objects based on a parameter.

**Q2: Does the Factory Pattern support inheritance?**
> **Ans:** Not in the traditional `extends` way. Factories use **Composition**. You can build a small object and then "mix" it into a larger object. This is often seen as more flexible than class-based inheritance.

**Q3: Can a Factory return an object with private data?**
> **Ans:** Yes! By defining variables inside the factory function and only exposing functions that use them, those variables become "private" and cannot be accessed directly from outside the object.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Factory** | Extremely flexible; private state. | Slightly higher memory (no prototype sharing). |
| **Class** | Familiar to Java/C++ devs; memory-efficient. | `this` binding is confusing; rigid structure. |
| **Object Literal** | Simple and fast. | No logic; cannot create private data. |

---

## 🔗 Navigation

**Prev:** [01_Module_Pattern.md](01_Module_Pattern.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Singleton_Pattern.md](03_Singleton_Pattern.md)
