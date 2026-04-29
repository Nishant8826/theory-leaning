# 📌 03 — Coding Interview Problems

## 🌟 Introduction

In senior interviews, you won't just be asked definitions; you'll be asked to **build** core JavaScript features from scratch.

This file provides the most common coding challenges and the "Senior Level" way to solve them.

---

## 🏗️ 1. Implement `Promise.all()`

**Goal:** Create a function that takes an array of promises and returns a single promise that resolves with an array of all results (preserving the order).

```javascript
function myPromiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let completed = 0;

    if (promises.length === 0) return resolve([]);

    promises.forEach((promise, index) => {
      // Wrap in Promise.resolve in case it's a raw value
      Promise.resolve(promise)
        .then((value) => {
          results[index] = value; // Keep the original order!
          completed++;

          if (completed === promises.length) {
            resolve(results);
          }
        })
        .catch(reject); // If one fails, they all fail
    });
  });
}
```

---

## 🏗️ 2. Implement `debounce()`

**Goal:** Create a function that delays execution until a certain amount of "quiet time" has passed.

```javascript
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    const context = this; // Preserve the 'this' context
    clearTimeout(timer);
    timer = setTimeout(() => {
      fn.apply(context, args);
    }, delay);
  };
}
```

---

## 🏗️ 3. Implement Deep Clone

**Goal:** Create a copy of an object that is 100% independent (no shared references).

```javascript
function deepClone(obj) {
  // Handle primitives and null
  if (obj === null || typeof obj !== "object") return obj;

  // Handle Arrays
  if (Array.isArray(obj)) {
    return obj.map(item => deepClone(item));
  }

  // Handle Objects
  const clone = {};
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      clone[key] = deepClone(obj[key]);
    }
  }
  return clone;
}
```

---

## 🏗️ 4. Flatten a Nested Array

**Goal:** Turn `[1, [2, [3, 4]], 5]` into `[1, 2, 3, 4, 5]`.

```javascript
function flatten(arr) {
  return arr.reduce((acc, item) => {
    if (Array.isArray(item)) {
      acc.push(...flatten(item)); // Recursively flatten
    } else {
      acc.push(item);
    }
    return acc;
  }, []);
}
```

---

## 🏗️ 5. LRU Cache (Least Recently Used)

**Goal:** Build a cache that stores a maximum number of items. When it's full, it removes the item that hasn't been used for the longest time.

```javascript
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.cache = new Map(); // Map preserves insertion order
  }

  get(key) {
    if (!this.cache.has(key)) return -1;
    const val = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, val); // Move to the "front" (end of map)
    return val;
  }

  put(key, value) {
    if (this.cache.has(key)) this.cache.delete(key);
    this.cache.set(key, value);
    if (this.cache.size > this.capacity) {
      // Remove the oldest item (first item in the map)
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
  }
}
```

---

## 📐 Decision Table: Which Logic to Use?

| Problem | Key Concept to Mention | Edge Case to Watch |
| :--- | :--- | :--- |
| **Promise.all** | Synchronization. | Preserve index order. |
| **Debounce** | Closures & Timers. | `this` binding context. |
| **Deep Clone** | Recursion. | Circular references (A points to B, B points to A). |
| **Flatten** | Recursive Reduce. | Non-array elements. |
| **LRU Cache** | Map insertion order. | Capacity limits. |

---

## 💼 Interview Tip: Edge Cases First

Before you start typing, always ask the interviewer about edge cases:
-   "What if the input is `null` or `undefined`?"
-   "Does the clone need to handle Dates or Regex objects?"
-   "Should the debounce have a 'leading edge' option?"

This makes you look like an architect who thinks before they code.

---

## 🔗 Navigation

**Prev:** [02_Tricky_Questions.md](02_Tricky_Questions.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Machine_Coding_JS.md](04_Machine_Coding_JS.md)
