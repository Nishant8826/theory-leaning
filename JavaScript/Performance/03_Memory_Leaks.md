# 📌 03 — Memory Leaks

## 🌟 Introduction

In JavaScript, you don't have to manually delete objects when you're done with them. A "Garbage Collector" (GC) does it for you automatically.

However, a **Memory Leak** happens when you accidentally keep a "link" or "reference" to an object that you don't need anymore. Because that link exists, the Garbage Collector is afraid to delete it, thinking you might still need it.

Think of it like **Trash Collection**:
-   **Normal:** you put your trash in the bin, and the truck takes it away.
-   **Memory Leak:** You keep your trash in your pocket. The truck can't take it because you are still holding onto it. Eventually, your pockets get so full you can't move!

---

## 🏗️ The 4 Most Common Leaks

### 1. Forgotten Event Listeners
If you add an event listener to the `window` or `document` inside a component, you **must** remove it when that component is destroyed.

```javascript
// ❌ LEAK: The 'resize' listener stays forever!
function startApp() {
  const largeData = new Array(1000000).fill("DATA");
  window.addEventListener('resize', () => {
    console.log(largeData.length);
  });
}

// ✅ FIXED: Remove it when done
function startApp() {
  const largeData = new Array(1000000).fill("DATA");
  const onResize = () => console.log(largeData.length);
  
  window.addEventListener('resize', onResize);
  
  // Later...
  window.removeEventListener('resize', onResize);
}
```

### 2. Uncleared Timers
`setInterval` will run forever until you tell it to stop. If the code inside the timer refers to a large object, that object can never be deleted.

```javascript
// ❌ LEAK: Timer runs forever
let user = { name: 'Nishant', data: new Array(1000000) };
setInterval(() => {
  console.log(user.name);
}, 1000);

// ✅ FIXED: Clear the interval
const intervalId = setInterval(() => { ... }, 1000);
clearInterval(intervalId);
```

### 3. Detached DOM Nodes
This happens when you remove an element from the HTML, but you still have a variable pointing to it in your JavaScript.

```javascript
// ❌ LEAK: Button is gone from screen, but still in 'myBtn' variable
let myBtn = document.getElementById('button-1');
document.body.removeChild(myBtn); 

// ✅ FIXED: Null out the variable
myBtn = null;
```

### 4. Global Variables
Anything you attach to `window` (in the browser) or `global` (in Node.js) will **never** be deleted until the page is refreshed or the server is restarted.

---

## 🚀 How to Detect a Leak

1.  Open **Chrome DevTools**.
2.  Go to the **Memory** tab.
3.  Take a **Heap Snapshot**.
4.  Perform the action you think is leaking (e.g., open and close a modal 10 times).
5.  Take another **Heap Snapshot**.
6.  Compare the two. If the "Total Heap Size" keeps going up and never comes back down, you have a leak!

---

## 📐 Visualizing the Leak

```text
 [ GLOBAL SCOPE ] ────────── (Link/Reference) ─────────┐
                                                       │
                                                       ▼
 [ TRASH CAN ] ◀──(GC tries to take)── [ OBJECT (100MB) ]
      ┃                                                ┃
      ┗━━━━━━━━━━━━━ (NOT ALLOWED!) ━━━━━━━━━━━━━━━━━━━┛
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Mark-and-Sweep Algorithm
V8 uses an algorithm called "Mark-and-Sweep." It starts at the "Roots" (like the `window` object) and "Marks" every object it can reach. Then, it "Sweeps" away everything that was NOT marked. A memory leak is simply an object that is still reachable from the Roots, even if your app logic says it should be gone.

---

## 💼 Interview Questions

**Q1: What is a "Detached DOM Node"?**
> **Ans:** It’s a DOM element that has been removed from the document tree (the screen) but is still being referenced by a JavaScript variable. Because JS is still "holding" it, the browser cannot free up the memory used by that element and its children.

**Q2: How do `WeakMap` and `WeakSet` help with memory?**
> **Ans:** They hold "Weak" references. This means if the object they are pointing to is deleted everywhere else, the `WeakMap` will also let go of it. It doesn't prevent the Garbage Collector from doing its job.

**Q3: Does setting a variable to `null` trigger the Garbage Collector?**
> **Ans:** Not immediately. It just "cuts the link." The Garbage Collector runs periodically. When it next runs, it will see that the object no longer has any links and will then delete it.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Automatic GC** | No need to manually manage memory. | Can cause tiny "pauses" in your app (Jank). |
| **Manual Nulling** | Guaranteed to free up memory faster. | Verbose; easy to forget. |
| **WeakMap** | Automatic cleanup of metadata. | Harder to use than a regular Map. |

---

## 🔗 Navigation

**Prev:** [02_Reflow_and_Repaint.md](02_Reflow_and_Repaint.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Lazy_Loading.md](04_Lazy_Loading.md)
