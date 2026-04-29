# 📌 08 — Garbage Collection (GC) Performance

## 🌟 Introduction

In JavaScript, there is an invisible "Janitor" called the **Garbage Collector (GC)**. Its job is to walk around your app's memory and throw away any data that you aren't using anymore.

Most of the time, the Janitor is so fast you don't even notice. But if you create **thousands of objects every second**, the Janitor has to work overtime. While the Janitor is working, the entire app has to **STOP**.

These "Stops" are called **GC Pauses**, and they are the #1 cause of "stuttering" or "jank" in web apps and games.

---

## 🏗️ 1. The Allocation Rate

The **Allocation Rate** is how fast you are creating "trash."

-   **Low Rate:** You create a few objects. The Janitor cleans once an hour. No lag.
-   **High Rate:** You create 10,000 objects in a loop. The Janitor has to clean every 10 milliseconds. Your app feels like it's lagging.

---

## 🏗️ 2. Strategy: Object Pooling

In high-performance apps (like games), we avoid creating new objects. Instead, we create a **Pool** of objects and reuse them over and over.

```javascript
// ❌ SLOW: Creating a new object 60 times a second
function gameLoop() {
  const position = { x: 10, y: 20 }; // New object every frame!
  updatePlayer(position);
}

// ✅ FAST: Reusing the same object
const playerPos = { x: 0, y: 0 }; // Created ONCE

function gameLoop() {
  playerPos.x = 10;
  playerPos.y = 20;
  updatePlayer(playerPos); // Same object, just updated
}
```

---

## 🏗️ 3. "Young" vs. "Old" Objects

V8 uses a trick called **Generational Collection**:
-   **New Space (The Nursery):** Most objects die here. Cleaning this space is **instant**.
-   **Old Space (The Warehouse):** If an object survives long enough, it moves here. Cleaning this space is **slow and heavy**.

**Rule of Thumb:** Try to keep your objects "short-lived." If they die quickly, they stay in the Nursery and never slow down the app.

---

## 🚀 How to Tune for Node.js

In Node.js, you can tell the Janitor how much memory he is allowed to use before he starts a heavy clean.

```bash
# Set the memory limit to 4GB
node --max-old-space-size=4096 app.js
```

---

## 📐 Visualizing the "Stop-the-World" Event

During a Major GC (Mark-Compact), the main thread is completely paused.

```text
 TIME LINE:
 
 ──────────────────────────────────────────────────────────▶
 [ RUNNING CODE ] [████ MAJOR GC PAUSE ████] [ RUNNING CODE ]
                      (Stop-the-World)
 
 INTERNAL ACTIONS:
 1. Mark: Find all objects still in use (Roots -> Reachable).
 2. Sweep: Identify "Dead" objects.
 3. Compact: Move live objects together to save space (Fragmentation).
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: Node.js App Crashing with "FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed - JavaScript heap out of memory".**
> **Problem:** The Janitor is cleaning as hard as possible, but he can't find enough trash to throw away. Your app is literally full of "Live" objects (a Memory Leak).
> **Fix:** Profile the heap using `--heap-prof` to find who is holding onto the data. Increase `--max-old-space-size` ONLY if your app legitimately needs that much RAM.

**P2: Micro-stuttering in a Web Game.**
> **Problem:** Every few seconds, the frame rate drops from 60fps to 40fps for a split second.
> **Reason:** You are likely creating "Temporary" objects (like Vectors or Math objects) inside the `requestAnimationFrame` loop.
> **Fix:** Use **Object Pooling** to reuse math objects instead of creating new ones in the hot loop.

**P3: High CPU usage but low traffic.**
> **Problem:** The server is at 100% CPU even with 1 user.
> **Reason:** The heap is 99% full, so the Janitor is running **continuously** to try and find even 1KB of free space.
> **Fix:** Check for a memory leak that is pushing the heap to its absolute limit.

---

## 🔬 Deep Technical Dive (V8 Internals)

### Scavenging vs. Mark-Compact
V8 uses a **"Scavenger"** algorithm for the New Space. it simply copies "live" objects to a new area and wipes the old area completely. It's incredibly fast. For the Old Space, it uses **"Mark-Compact,"** which has to walk through every single object in your app to see if it's still connected to anything. This is why "Memory Leaks" in the Old Space are so much more dangerous than in the New Space.

---

## 💼 Interview Questions

**Q1: What is a "Stop-the-World" pause?**
> **Ans:** It is a moment during Garbage Collection where the JavaScript engine pauses all code execution to safely move and delete objects in memory. If these pauses are too long, the user experiences "Jank."

**Q2: What is "Object Pooling"?**
> **Ans:** It is a performance pattern where you pre-allocate a set of objects and reuse them instead of creating and destroying them constantly. This significantly reduces the workload on the Garbage Collector.

**Q3: Why is a larger `max-old-space-size` not always better?**
> **Ans:** While it allows the app to hold more data, it also makes the GC pauses **longer** when they finally happen. A larger warehouse takes longer to clean than a smaller one!

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Object Pooling** | Zero GC pauses; maximum speed. | Harder to write; can lead to bugs. |
| **Generational GC** | Handles most apps automatically. | Unpredictable pauses in heavy apps. |
| **Manual Cleanup (nulling)** | Helps the Janitor find trash faster. | Verbose; usually not necessary. |

---

## 🔗 Navigation

**Prev:** [07_Event_Loop_Blocking_UI.md](07_Event_Loop_Blocking_UI.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [../Interview/01_JS_Interview_Core.md](../Interview/01_JS_Interview_Core.md)
