# 📌 03 — Singleton Pattern

## 🌟 Introduction

In some cases, you only want **one single copy** of an object to exist in your entire application.

Think of it like a **President**:
-   A country can only have one President at a time.
-   Anyone who wants to talk to the President talks to the **same person**.
-   If the President changes their mind, everyone sees the change.

In software, we use the **Singleton Pattern** for things like Database Connections, App Configurations, or Loggers.

---

## 🏗️ The Node.js Way (Module Caching)

The easiest way to create a Singleton in Node.js is to leverage the module system. Node.js **caches** modules. The first time you `require` a file, it runs. Every time after that, it just returns the result of the first run.

```javascript
// config.js
const settings = {
  theme: 'dark',
  apiKey: '12345-ABCDE'
};

// We export the OBJECT, not the class/function
module.exports = settings;

// main.js
const config1 = require('./config');
const config2 = require('./config');

config1.theme = 'light';
console.log(config2.theme); // "light" (They are the SAME object!)
```

---

## 🏗️ The Class-Based Way (Lazy Initialization)

If you aren't using Node.js modules or you want more control, you can use a static property.

```javascript
class Database {
  constructor() {
    if (Database.instance) {
      return Database.instance;
    }
    this.connection = "Connected to DB";
    Database.instance = this;
  }
}

const db1 = new Database();
const db2 = new Database();

console.log(db1 === db2); // true
```

---

## 🚀 Why Use a Singleton?

1.  **Saves Resources:** You don't want to open 100 database connections if one will do.
2.  **Global Point of Access:** It’s easy to get the app's configuration from anywhere without passing it through 10 functions.
3.  **Consistency:** Ensures that everyone is looking at the exact same data.

---

## ⚠️ The Danger: Global State

Singletons are basically **Global Variables**.
-   **Hard to Test:** If one test changes the singleton, it might break other tests that run later.
-   **Hidden Dependencies:** It’s not always obvious that a function depends on a global singleton.

---

## 📐 Visualizing the Singleton

```text
 [ FILE A ] ──┐
              │
 [ FILE B ] ──┼──▶ [ THE SINGLETON INSTANCE ] (Shared Memory)
              │
 [ FILE C ] ──┘
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### require.cache
When you call `require('./db')`, Node.js looks in an internal object called `require.cache`. If the file path exists as a key, it returns the cached value. This is why singletons are so performant in Node—there is zero overhead after the first load. If you absolutely need a **new** instance, you have to manually delete the key from `require.cache` before calling `require` again.

---

## 💼 Interview Questions

**Q1: How does the Singleton pattern work in Node.js?**
> **Ans:** Node.js uses module caching. When you `module.exports` an object (an instance), Node stores that object in memory. Any other file that `require`s it gets a reference to that same object.

**Q2: What is "Lazy Initialization"?**
> **Ans:** It means the singleton instance is not created until the very moment someone asks for it. This saves memory if the singleton is never actually used during the app's lifecycle.

**Q3: Are Singletons thread-safe in Node.js?**
> **Ans:** Since Node.js JavaScript runs on a single thread, you don't have to worry about two threads creating the singleton at the same time. However, in multi-process systems (like using the Cluster module), **each process will have its own singleton**.

---

## ⚖️ Trade-offs

| Feature | Singleton | Global Variable |
| :--- | :--- | :--- |
| **Organization** | Encapsulated in a class/module. | Messy and unorganized. |
| **Creation** | Created when needed (Lazy). | Created as soon as the script loads. |
| **Testing** | Hard to test (Shared state). | Also hard to test. |

---

## 🔗 Navigation

**Prev:** [02_Factory_Pattern.md](02_Factory_Pattern.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Observer_Pattern.md](04_Observer_Pattern.md)
