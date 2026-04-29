# 📌 04 — Machine Coding (JS System Design)

## 🌟 Introduction

A **Machine Coding Round** is a live session where you are asked to build a small, working system (like a "To-Do List" or an "Event Bus") in 45-60 minutes.

It's not just about getting it to work; it's about **Clean Code**, **API Design**, and handling **Edge Cases**.

---

## 🏗️ 1. Build a Pub/Sub System (Event Bus)

**Goal:** Create a system where different parts of an app can "Subscribe" to events and "Publish" data without talking directly to each other.

```javascript
class PubSub {
  constructor() {
    this.events = {}; // Store callbacks: { 'click': [fn1, fn2] }
  }

  // Subscribe to an event
  subscribe(eventName, callback) {
    if (!this.events[eventName]) {
      this.events[eventName] = [];
    }
    this.events[eventName].push(callback);

    // Return an "unsubscribe" function
    return () => {
      this.events[eventName] = this.events[eventName].filter(fn => fn !== callback);
    };
  }

  // Fire an event
  publish(eventName, data) {
    if (!this.events[eventName]) return;
    this.events[eventName].forEach(callback => callback(data));
  }
}
```

---

## 🏗️ 2. Concurrency Limiter (Task Queue)

**Goal:** Imagine you have 100 images to download, but you only want to download **3 at a time** to avoid crashing the browser.

```javascript
class TaskQueue {
  constructor(limit) {
    this.limit = limit;
    this.running = 0;
    this.queue = [];
  }

  add(task) {
    this.queue.push(task);
    this.runNext();
  }

  runNext() {
    if (this.running >= this.limit || this.queue.length === 0) return;

    const task = this.queue.shift();
    this.running++;

    task().then(() => {
      this.running--;
      this.runNext(); // Run the next task in the queue
    });
  }
}
```

---

## 🏗️ 3. Build a Simple State Machine

**Goal:** Manage a UI that moves between states like `IDLE`, `LOADING`, and `SUCCESS`.

```javascript
class UIState {
  constructor() {
    this.state = 'IDLE';
  }

  transition(action) {
    switch (this.state) {
      case 'IDLE':
        if (action === 'FETCH') this.state = 'LOADING';
        break;
      case 'LOADING':
        if (action === 'RESOLVE') this.state = 'SUCCESS';
        if (action === 'REJECT') this.state = 'ERROR';
        break;
      case 'SUCCESS':
      case 'ERROR':
        if (action === 'RETRY') this.state = 'LOADING';
        break;
    }
    console.log(`Current State: ${this.state}`);
  }
}
```

---

## 📐 Evaluation Checklist

When you finish your machine coding, check these 4 things:

1.  **Correctness:** Does it actually solve the main problem?
2.  **Memory Cleanup:** Did you provide an `unsubscribe` or `clear` function?
3.  **Error Handling:** What if a callback crashes? Does the whole system stop? (Use `try...catch`).
4.  **Privacy:** Use `#privateVariables` or `WeakMap` to hide internal data from the user.

---

## 🔬 Deep Technical Dive (V8 Internals)

### Hidden Classes & Map Usage
When building a Pub/Sub system, using a **`Map`** is often better than a plain **`Object`**. In V8, `Object` keys are optimized for specific "Hidden Classes." If you add and remove keys frequently (like with subscribers), V8 might move the object to "Dictionary Mode," which is slower. `Map` is designed specifically for frequent additions/removals and maintains performance regardless of how many subscribers you have.

---

## 💼 Interview Tip: Talk While You Type

Don't code in silence for 40 minutes.
-   "I'm using a `Map` here because we'll be adding/removing subscribers often..."
-   "I'm returning an unsubscribe function so the user doesn't have to pass the original function back..."
-   "I'll add a `try...catch` here so one broken subscriber doesn't break the whole app..."

---

## 🔗 Navigation

**Prev:** [03_Coding_Problems.md](03_Coding_Problems.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [../Projects/01_Build_Event_Emitter.md](../Projects/01_Build_Event_Emitter.md)
