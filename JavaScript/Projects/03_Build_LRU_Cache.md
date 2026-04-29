# 📌 Project 03 — Build an LRU Cache

## 🌟 Introduction

**LRU** stands for **Least Recently Used**. It is a smart memory system that has a limited size. When the cache is full and you want to add something new, it automatically deletes the item that was used the **longest time ago**.

Think of it like a **Stack of Books**:
-   Every time you read a book, you put it on the **Top**.
-   The books you haven't touched in a long time stay at the **Bottom**.
-   If your shelf is full and you buy a new book, you throw away the book at the very bottom.

---

## 🏗️ 1. The Strategy

In JavaScript, we can build a perfect LRU Cache using just a **`Map`**. 

Wait, why a Map? Because in modern JavaScript, `Map` objects **remember the order** in which keys were inserted. If we delete a key and re-insert it, it moves to the "End" (the most recent position).

---

## 🏗️ 2. The Implementation

```javascript
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.cache = new Map(); // Remembers order!
  }

  get(key) {
    if (!this.cache.has(key)) return -1;

    // To make it "Most Recently Used", we delete and re-add it
    const val = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, val);
    
    return val;
  }

  put(key, value) {
    // If it exists, delete the old version first
    if (this.cache.has(key)) {
      this.cache.delete(key);
    }

    this.cache.set(key, value);

    // If we are over capacity, remove the OLDEST item
    // The oldest item is always the FIRST item in the Map
    if (this.cache.size > this.capacity) {
      const oldestKey = this.cache.keys().next().value;
      this.cache.delete(oldestKey);
    }
  }
}
```

---

## 🚀 3. Testing Your Cache

```javascript
const cache = new LRUCache(2); // Only space for 2 items

cache.put(1, "Data 1");
cache.put(2, "Data 2");
console.log(cache.get(1)); // "Data 1" (Now 1 is most recent)

cache.put(3, "Data 3"); // 2 was least recent, so it gets DELETED
console.log(cache.get(2)); // -1 (Not found)
```

---

## 📐 Visualizing the Internal Map Structure

Inside V8, the Map looks like a mix of a Hash Table and a Doubly Linked List.

```text
 HEAD (Oldest/LRU)                                     TAIL (Newest/MRU)
      │                                                       │
      ▼                                                       ▼
 ┌───────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐
 │ Key: 1    │ ◀───▶ │ Key: 5    │ ◀───▶ │ Key: 2    │ ◀───▶ │ Key: 9    │
 └───────────┘       └───────────┘       └───────────┘       └───────────┘
      ▲                                                       ▲
      │                                                       │
  [ EVICT ]                                               [ RECENT ]
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: Memory Usage keeps growing despite the Cache Limit.**
> **Problem:** You are storing massive objects as values in the cache. Even if you limit the *number* of keys (e.g., 1000 keys), if each object is 1MB, the cache will take 1GB of RAM.
> **Fix:** Calculate the "Size" of the cache in bytes, not just key count, or use a `WeakMap` if you only want to cache objects that are stored elsewhere.

**P2: Performance bottleneck on `put()` operations.**
> **Problem:** If you are doing thousands of `put()` operations per second, the constant `delete` and `set` calls in a standard `Map` can cause Garbage Collection pressure.
> **Fix:** For ultra-high performance, use a custom Doubly Linked List + a plain Object to avoid the overhead of the `Map` iterator.

**P3: Cache Inconsistency.**
> **Problem:** The data in the source (database) changed, but the cache still has the old data.
> **Fix:** Implement a **TTL (Time to Live)**. Add a timestamp to each entry and delete it if it's older than e.g. 60 seconds.

---

## 🔬 Deep Technical Dive (V8 Internals)

### Map Ordering
In V8, `Map` is implemented using a **Deterministic Hash Table**. It uses a linked list internally to maintain the order of insertion. This is why `this.cache.keys().next().value` is an $O(1)$ operation—V8 just looks at the "Head" pointer of its internal linked list. If we used a regular `Object`, the order would be unpredictable, and finding the oldest key would take $O(N)$ time.

---

## 💼 Interview Tips

-   **Why use Map over Object?** Objects don't guarantee the order of keys (especially with numeric keys). Maps always maintain insertion order and have better performance for frequent additions/deletions.
-   **What is the Time Complexity?** Both `get` and `put` are **O(1)**. This means they are incredibly fast regardless of how many items are in the cache.
-   **Real-world use case:** Database connection pools, Image caching in browsers, or "Recently Opened Files" in your code editor.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Map-based LRU** | Very easy to write; built into JS. | Harder to implement custom eviction logic. |
| **Linked List + Object** | Classic computer science way; maximum control. | Lots of "Pointer" code (`node.next`, `node.prev`). |
| **Simple Object** | Fast for small data. | No order; grows forever (memory leak risk). |

---

## 🔗 Navigation

**Prev:** [02_Build_Promise.md](02_Build_Promise.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Build_React_Like_State.md](04_Build_React_Like_State.md)
