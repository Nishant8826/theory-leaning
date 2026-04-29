# 📌 03 — Garbage Collection

## 🌟 Introduction

**Garbage Collection (GC)** is the automated process of finding memory that is no longer being used by the application and reclaiming it so it can be reused.

In JavaScript, you don't have to manually "delete" objects. Instead, the engine has an **Invisible Janitor** that periodically walks through your memory and throws away the "trash."

---

## 🏗️ The Core Concept: Reachability

How does the janitor know what is trash? It uses a concept called **Reachability**. An object is "reachable" if it is accessible or usable in some way.

### 🌳 1. The Roots (The Starting Points)
Roots are objects that are considered inherently reachable by the engine. The Garbage Collector starts its search from these:
-   **Global Variables:** Any variable defined in the global scope (e.g., `window` in browsers, `global` in Node.js).
-   **Call Stack:** Local variables and parameters of the currently executing functions.
-   **Active Closures:** Variables in the scope of functions that are still "alive" or can be called.

### 🔗 2. The Reference Chain
An object is reachable if:
-   It is a **Root**.
-   It is referenced by a **Root**.
-   It is referenced by another **Reachable** object (creating a chain).

### 🏝️ 3. The "Island of Isolation" (Circular References)
A common misconception is that if an object has *any* reference to it, it won't be deleted. This was true for old **Reference Counting** algorithms, but NOT for modern **Reachability**.

If two objects reference each other but are **not** reachable from any Root, they form an "Island of Isolation." The engine will delete the entire island.

```javascript
function marry(man, woman) {
  woman.husband = man;
  man.wife = woman;
  return { father: man, mother: woman };
}

let family = marry({ name: "John" }, { name: "Ann" });

// If we cut the reference from the root:
family = null; 

// Now, John and Ann still point to each other, but the ROOT (family) 
// can no longer reach them. They are now an Island of Isolation 
// and will be Garbage Collected.
```

#### 🖼️ Island Visualization:
```text
[ Root ] 
   │
   X  <-- (Connection severed)
   │
[ John ] <────▶ [ Ann ]   <-- (Still linked to each other, but Root can't see them!)
```


---

## 🔄 The "Mark & Sweep" Algorithm

Most modern engines (like V8) use this 2-step process:

1.  **Mark:** The GC starts at the Roots and "marks" (tags) every object it can find.
2.  **Sweep:** It then looks at all objects in memory. Any object that **doesn't** have a mark is deleted.

---

## 📐 Visualizing the Process

```text
[ Global Root ] 
      │
      ▼
   [ User ] ──▶ [ Profile ] ──▶ [ Image ]  <-- (MARK: Keep these!)
      │
      X (Reference broken)
      │
      ▼
   [ OldData ] ──▶ [ HugeArray ]           <-- (SWEEP: Delete these!)
```

---

## ⚡ Generational Collection (Optimization)

V8 is smart. It knows that **most objects die young** (e.g., variables inside a short function). It splits the heap into two areas:

1.  **Young Generation:** Where new objects are born. The janitor cleans this area very frequently and very fast.
2.  **Old Generation:** If an object survives multiple cleanups in the Young Generation, it gets "promoted" to the Old Generation. The janitor cleans this area less often.

---

## 🔍 Code Walkthrough: `Map` vs `WeakMap`

A common cause of "Memory Leaks" is keeping objects in a `Map` after you're done with them.

```javascript
// ❌ With Map:
let obj = { name: "Nishant" };
let myMap = new Map();
myMap.set(obj, "some data");

obj = null; 
// Even though we set obj to null, the object is STILL in myMap.
// The Janitor CANNOT delete it. (This is a leak!)

// ✅ With WeakMap:
let obj2 = { name: "Rahul" };
let myWeakMap = new WeakMap();
myWeakMap.set(obj2, "some data");

obj2 = null;
// Because it's a WeakMap, the Janitor is allowed to delete the object
// as soon as there are no other references to it. (No leak!)
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Orinoco Engine
V8's GC system is called **Orinoco**. It uses **Parallel**, **Incremental**, and **Concurrent** marking.
-   **Incremental:** Instead of stopping your code for 100ms, it breaks the work into tiny 1ms chunks so you don't notice any "jank" or lag in your app.

---

## 💼 Interview Questions

**Q1: What is the main algorithm used for Garbage Collection in JS?**
> **Ans:** The **Mark & Sweep** algorithm. It marks reachable objects from roots and sweeps away the unreachable ones.

**Q2: What is "Stop-The-World" in GC?**
> **Ans:** It refers to the moment when the JavaScript engine completely pauses the execution of your code to perform garbage collection. Modern engines minimize this using incremental marking.

**Q3: Can we force Garbage Collection to run?**
> **Ans:** In a standard browser environment, **no**. The engine decides when to run it. In Node.js, you can enable it using the `--expose-gc` flag and calling `global.gc()`, but this is only recommended for testing.

---

## ⚖️ Trade-offs

| Feature | Benefit | Cost |
| :--- | :--- | :--- |
| **Automation** | No manual "memory free" bugs. | You have no control over *when* cleanup happens. |
| **Mark & Sweep** | Very reliable at finding all garbage. | Requires some CPU time to "walk the tree" of objects. |
| **WeakMap** | Prevents memory leaks automatically. | You cannot iterate over a WeakMap or see its size. |

---

## 🔗 Navigation

**Prev:** [02_Memory_Management.md](02_Memory_Management.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Concurrency_Model.md](04_Concurrency_Model.md)
