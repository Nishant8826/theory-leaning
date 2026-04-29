# 📌 07 — Reactive Patterns

## 🌟 Introduction

In traditional programming, you tell the computer: "Add 10 to X." In **Reactive Programming**, you tell the computer: "Whenever X changes, automatically update Y."

Think of it like an **Excel Spreadsheet**:
-   You have a formula in cell B1: `=A1 * 2`.
-   You don't have to manually tell B1 to update.
-   As soon as you type a new number in A1, B1 **reacts** and updates instantly.

---

## 🏗️ The Reactive Tools

There are two main ways we achieve this in JavaScript:

1.  **Observables (RxJS):** You treat events like a "Stream of Water." You can filter the water, color it, or combine it with another stream.
2.  **Proxies:** You wrap an object in a "Shield" (Proxy) that detects every time a property is read or changed.

---

## 🏗️ Why Use Reactive Patterns?

The best example is a **Search Autocomplete** box:
-   **Problem:** If the user types "apple" very fast, you don't want to send 5 separate API requests (a, ap, app, appl, apple).
-   **Reactive Solution:**
    1.  **Debounce:** Wait 300ms for the user to stop typing.
    2.  **Filter:** Only search if they typed more than 2 characters.
    3.  **SwitchMap:** If a new search starts, cancel the previous one immediately.

---

## 🔍 Code Walkthrough: Simple Proxy Reactivity

This is how modern frameworks like **Vue 3** work under the hood.

```javascript
const data = { price: 10, quantity: 2 };

// Create a reactive proxy
const reactiveData = new Proxy(data, {
  set(target, key, value) {
    console.log(`Property "${key}" changed to: ${value}`);
    target[key] = value;
    
    // Auto-update the total whenever price or quantity changes
    updateTotal();
    return true;
  }
});

function updateTotal() {
  const total = reactiveData.price * reactiveData.quantity;
  console.log(`Total is now: ${total}`);
}

reactiveData.price = 20; 
// Output: Property "price" changed to: 20
// Output: Total is now: 40
```

---

## 📐 Visualizing the Data Stream

```text
 [ KEYBOARD CLICKS ] ──▶ [ DEBOUNCE (300ms) ] ──▶ [ FILTER (len > 2) ] ──▶ [ API REQUEST ]
    "a", "p", "p"             (Wait...)              (Passed!)             (Searching...)
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Proxy Traps
V8 handles **Proxies** differently than regular objects. When you access a property on a Proxy, V8 has to pause and run the "Trap" function (like `get` or `set`). This used to be very slow, but modern V8 engines have optimized this using **"JIT (Just-In-Time) compilation."** If you use the same proxy pattern many times, V8 can "inline" the trap logic directly into the machine code, making reactivity incredibly fast.

---

## 💼 Interview Questions

**Q1: What is the difference between Imperative and Reactive programming?**
> **Ans:** Imperative is "Step-by-step" (do this, then that). Reactive is "Declaration of relationship" (whenever this happens, that should happen too).

**Q2: What is "Debouncing" in reactive programming?**
> **Ans:** It’s a technique to limit how often a function is called. It waits for a period of "silence" before firing. This is crucial for performance in search boxes or window resizing.

**Q3: How does a Proxy work?**
> **Ans:** A Proxy is a wrapper around an object. It allows you to "intercept" operations like reading a property, writing a property, or deleting one. It’s the engine behind modern reactive state management.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Reactive (Proxies)** | Clean code; automatic updates. | Can be hard to debug (who triggered this change?). |
| **Manual Updates** | Total control; easy to trace. | Leads to "Spaghetti Code" as the app grows. |
| **RxJS (Observables)** | Extremely powerful for complex events. | Very steep learning curve. |

---

## 🔗 Navigation

**Prev:** [06_Middleware_Pattern.md](06_Middleware_Pattern.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [08_State_Management_Patterns.md](08_State_Management_Patterns.md)
