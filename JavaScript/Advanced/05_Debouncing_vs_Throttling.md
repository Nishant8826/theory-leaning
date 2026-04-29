# 📌 05 — Debouncing vs Throttling

## 🌟 Introduction

Some browser events, like **scrolling, resizing, or typing**, fire hundreds of times per second. If you attach a heavy function (like an API call) to these events, your app will lag or crash.

**Debouncing** and **Throttling** are techniques used to control (rate-limit) how many times a function is executed over time.

---

## 🏗️ Debouncing (The "Wait for Silence")

Debouncing ensures that a function is only called **after** a certain amount of time has passed since the last time it was triggered.

**Analogy:** An Elevator.
The elevator door doesn't close as soon as you step in. It waits for 5 seconds of silence. If someone else steps in, the 5-second timer **resets**. The door only closes when there has been 5 seconds of nobody entering.

-   **Use Case:** Search bar (Wait for the user to stop typing before calling the API).

```javascript
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer); // Reset the timer every time the event fires
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
```

---

## 🏗️ Throttling (The "Speed Limit")

Throttling ensures that a function is called **at most once** every X milliseconds, no matter how many times the event fires.

**Analogy:** A Water Tap.
No matter how hard you turn the handle, the water only drips out at a steady rate. If you set it to drip once per second, it won't drip faster even if you shake it.

-   **Use Case:** Scroll events (Update the UI every 100ms while the user scrolls).

```javascript
function throttle(fn, limit) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      fn.apply(this, args); // Run the function
      inThrottle = true; // Block further calls
      setTimeout(() => (inThrottle = false), limit); // Unblock after 'limit'
    }
  };
}
```

---

## 📐 Visualizing the Difference

```text
Events:    |||||||||||||||| (Rapid firing)

DEBOUNCE:  ----------------- [FIRE] (Wait for silence)

THROTTLE:  [FIRE] --- [FIRE] --- [FIRE] (Steady rhythm)
```

---

## ⚡ Comparison Table

| Feature | Debouncing | Throttling |
| :--- | :--- | :--- |
| **Strategy** | Group multiple events into one. | Spread events over time. |
| **Execution** | Fires **after** the events stop. | Fires **during** the events at intervals. |
| **Goal** | Do it once when finished. | Do it at a steady rate. |
| **Best For** | Search inputs, form validation. | Scrolling, resizing, game firing. |

---

## 🔬 Deep Technical Dive (V8 Internals)

### Timer Heap
In V8 (and Node.js), `setTimeout` doesn't create a separate thread for every timer. Instead, it uses a **Timer Heap** (a priority queue). The engine checks the top of the heap to see which timer is due next. Debouncing works by constantly removing and re-inserting items into this heap.

---

## 💼 Interview Questions

**Q1: What is the main difference between Debouncing and Throttling?**
> **Ans:** Debouncing waits for a "quiet period" before executing, while Throttling ensures execution happens at regular intervals during a busy period.

**Q2: Which one is better for a "Resize" event?**
> **Ans:** **Throttling** is usually better because you want the UI to update smoothly *while* the user is resizing, not just at the very end.

**Q3: How do you handle "Leading" vs "Trailing" edge?**
> **Ans:** Leading edge means the function runs at the **start** of the burst. Trailing edge means it runs at the **end**. Most implementations allow you to toggle these behaviors.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Debounce** | Saves the most resources (only 1 call). | The user has to wait for the "silence" to see results. |
| **Throttle** | Keeps the UI feeling responsive during action. | Still executes the function multiple times (more CPU usage). |
| **Lodash/Underscore** | Battle-tested and handles edge cases. | Adds external dependency to your project. |

---

## 🔗 Navigation

**Prev:** [04_Concurrency_Model.md](04_Concurrency_Model.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [06_Currying.md](06_Currying.md)
