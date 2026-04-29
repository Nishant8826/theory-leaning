# 📌 08 — Event Loop

## 🧠 Concept Explanation (Deep Technical Narrative)

The Event Loop is the scheduling mechanism that coordinates JavaScript's single-threaded execution with asynchronous I/O operations, timers, and UI rendering. Despite JavaScript being single-threaded, the system achieves apparent concurrency by interleaving execution of callbacks queued from various async operations.

Understanding the Event Loop requires understanding **three different systems** working together:

1. **The JavaScript Engine (V8)** — Executes synchronous code, microtasks
2. **The Runtime (libuv in Node / Browser C++ core)** — Manages async operations (timers, I/O, network)
3. **The Task Scheduler** — Decides what to run next on the JS thread

The Event Loop's central role is: *when the JS call stack is empty, what should run next?*

---

## 🔬 Internal Mechanics (Engine-Level — V8 + Browser)

### Browser Event Loop Architecture

The HTML specification (not ECMA) defines the browser's event loop. The browser's event loop runs in the **main thread** which is shared by:
- JavaScript execution
- Style calculation
- Layout
- Paint
- Compositor communication

```
Browser Event Loop (simplified from HTML spec):

1. Run one "task" from the oldest task in the task queue
2. Drain the microtask queue completely
3. If a rendering opportunity exists (≥ 16.67ms since last render):
   a. Run requestAnimationFrame callbacks
   b. Run IntersectionObserver callbacks  
   c. Update rendering (style → layout → paint → composite)
4. If task queue is empty: wait
5. Repeat
```

### What Constitutes a "Task"

Tasks are placed in the **Task Queue** (macrotask queue) by:
- `setTimeout(fn, delay)` — minimum delay, not guaranteed
- `setInterval(fn, interval)` — periodic timer
- `MessageChannel.port.onmessage` — message passing
- `requestAnimationFrame` — rendering-aligned (special status)
- I/O callbacks (fetch completion, XHR, IndexedDB)
- User events (click, keydown) — from the UI event queue
- `<script>` tag parsing — initial script execution task

**Critical:** The event loop picks ONE task per iteration, then drains ALL microtasks before picking the next task.

### Microtask Queue — The High Priority Queue

The Microtask Queue is drained **to exhaustion** after every task (and after every microtask that adds more microtasks). Sources:
- `Promise.resolve().then(fn)` — PromiseReactionJob
- `queueMicrotask(fn)` — direct microtask scheduling
- `MutationObserver` callbacks
- `await` resumption (each `await` schedules a microtask)

```
AFTER every task → drain ALL microtasks:
  while (microtaskQueue.length) {
    runMicrotask(microtaskQueue.shift())
    // If this microtask adds more microtasks, those run too!
  }
```

**Starvation risk:** If microtasks add microtasks infinitely, the event loop NEVER processes another task — the page freezes.

```javascript
// Starvation example (don't do this)
function starve() {
  Promise.resolve().then(starve) // Infinite microtask loop
}
starve()
// Browser: page becomes completely unresponsive
// No user events, no rendering, no setTimeout callbacks
```

---

## 🔁 Execution Flow (Step-by-Step)

```javascript
console.log('A')

setTimeout(() => console.log('B'), 0)

Promise.resolve()
  .then(() => console.log('C'))
  .then(() => console.log('D'))

console.log('E')
```

**Complete execution trace:**

```
CALL STACK          MICROTASK QUEUE     TASK QUEUE
────────────        ───────────────     ──────────
[script task]
  log('A')          []                  [setTimeout cb]
  
  → 'A' printed
  
  setTimeout called → schedules B in task queue (after ≥0ms)
  
  Promise.resolve().then(C) → schedules C in microtask queue
  
  .then(D) → schedules D AFTER C resolves (pending)
  
  log('E') → 'E' printed
  
[script task ends]
                    [C pending]         [B in task queue]
                    
↓ Script task complete → drain microtasks
  
  Run C:
    log('C') → 'C' printed
    C's promise resolves → schedules D in microtask queue
  
  Run D:
    log('D') → 'D' printed

↓ Microtask queue empty

  [Rendering opportunity? Check if ≥16.67ms since last frame]
  → Probably not yet (everything ran in <1ms)

↓ Pick next task: setTimeout callback B

  log('B') → 'B' printed

Output: A, E, C, D, B
```

---

## 🧠 Memory Behavior

```
Event Loop Memory Model:

Task Queue entries:
  Each entry: pointer to callback function + closure context
  Memory: shallow (just the function pointer + args)
  Retention: callback's closure is kept alive until the task runs

Microtask Queue entries:
  Promise reactions: { onFulfilled, onRejected, resultCapability }
  These are small objects; the reaction holds a reference to the
  next promise in the chain — this is how .then() chains don't leak

Rendering:
  Layout tree: retained across frames (incremental updates)
  Paint records: GPU command buffer (can be large for complex scenes)
```

---

## 📐 ASCII Diagram — Full Browser Event Loop

```
                    ┌──────────────────────────────────────────────────────┐
                    │                  EVENT LOOP ITERATION                │
                    └──────────────────────────────────────────────────────┘
                                              │
                         ┌────────────────────┘
                         ▼
              ┌─────────────────────┐
              │  Pick 1 Task from   │◄──────────────────────────────────────┐
              │  Oldest Task Queue  │                                        │
              └─────────────────────┘                                        │
                         │                                                   │
                         ▼                                                   │
              ┌─────────────────────┐                                        │
              │  Run Task on        │                                        │
              │  Call Stack         │                                        │
              └─────────────────────┘                                        │
                         │                                                   │
                         ▼                                                   │
              ┌─────────────────────────────────────────────────────┐       │
              │  DRAIN MICROTASK QUEUE (until empty)                │       │
              │  ┌──────────────────────────────────────────────┐   │       │
              │  │  Run microtask → may add more microtasks     │   │       │
              │  │  Loop until queue is completely empty        │   │       │
              │  └──────────────────────────────────────────────┘   │       │
              └─────────────────────────────────────────────────────┘       │
                         │                                                   │
                         ▼                                                   │
              ┌─────────────────────────────┐                               │
              │  Rendering Opportunity?     │                               │
              │  (Time since last frame     │                               │
              │   ≥ 1 / display_hz seconds) │                               │
              └─────────────────────────────┘                               │
                    │           │                                            │
                   YES          NO                                           │
                    │           └────────────────────────────────────────────┘
                    ▼
              ┌─────────────────────────────────────┐
              │  1. requestAnimationFrame callbacks  │
              │  2. ResizeObserver callbacks         │
              │  3. IntersectionObserver callbacks   │
              │  4. Style recalculation              │
              │  5. Layout                           │
              │  6. Paint                            │
              │  7. Composite (GPU thread)           │
              └─────────────────────────────────────┘
                         │
                         └────────────────────────────────────────────────────┘
```

---

## 🔍 Code Examples

### Example 1 — Timer Clamping

```javascript
// Browsers clamp setTimeout to minimum 4ms after 5 nested levels
// AND clamp to minimum 1000ms for inactive tabs (Chrome)

let depth = 0
function nestedTimer() {
  depth++
  if (depth < 10) {
    console.time(`level-${depth}`)
    setTimeout(() => {
      console.timeEnd(`level-${depth}`)
      nestedTimer()
    }, 0)
  }
}
nestedTimer()

// Output: level-1: 1ms, level-2: 1ms, ... level-5: 4ms, level-6: 4ms...
// After 5 levels of nesting: clamped to 4ms minimum

// Node.js: no 4ms clamping (libuv timers have 1ms resolution)
// Mobile Chrome: additional clamping when battery saver active
```

### Example 2 — requestAnimationFrame vs setTimeout

```javascript
// setTimeout: not synchronized with rendering
// Can fire mid-frame, causing visual tearing or double-paint

// BAD for animation:
let pos = 0
function animateBad() {
  pos += 5
  element.style.left = pos + 'px'
  if (pos < 300) setTimeout(animateBad, 16)
}

// GOOD: rAF fires at the START of each frame
// Browser will skip calls if rendering is behind
function animateGood() {
  pos += 5
  element.style.left = pos + 'px'
  if (pos < 300) requestAnimationFrame(animateGood)
}

// rAF callbacks:
// - Always called before the browser paints
// - Receive a high-resolution timestamp (DOMHighResTimeStamp)
// - Automatically paused in hidden tabs (saves battery)
// - Can be cancelled with cancelAnimationFrame(id)
```

### Example 3 — Rendering & Event Loop Coordination

```javascript
// Layout thrashing: forces synchronous layout computation
// Each read of layout property after a write forces layout

function thrash() {
  const elements = document.querySelectorAll('.item')
  
  elements.forEach(el => {
    const height = el.offsetHeight  // READ: forces layout!
    el.style.height = height + 10 + 'px'  // WRITE: invalidates layout
    // Next iteration's READ forces layout again → thrashing
  })
}

// Fix: Batch reads, then batch writes
function optimized() {
  const elements = document.querySelectorAll('.item')
  
  // All reads first
  const heights = Array.from(elements).map(el => el.offsetHeight)
  
  // All writes after (one layout recalculation total)
  elements.forEach((el, i) => {
    el.style.height = heights[i] + 10 + 'px'
  })
}
```

### Example 4 — MessageChannel for High-Priority Task Scheduling

```javascript
// MessageChannel gives a task priority between setTimeout and microtasks
// Used internally by React's scheduler

const { port1, port2 } = new MessageChannel()
const taskQueue = []

port2.onmessage = function() {
  const task = taskQueue.shift()
  if (task) task()
}

function scheduleTask(fn) {
  taskQueue.push(fn)
  port1.postMessage(null)
}

// MessageChannel tasks are tasks (not microtasks) but fire faster than
// setTimeout(0) which can have 4ms clamping.
// React's scheduler uses this to schedule work between frames.
```

---

## 💥 Production Failures & Debugging

### Failure 1 — Infinite Microtask Loop (Page Freeze)

```javascript
// Production incident: RxJS observable subscribing to itself
// via promise-based transform

observable
  .pipe(
    switchMap(val => of(val).pipe(delay(0))) // Uses Promise under the hood
    // delay(0) in RxJS 6 uses Promise.resolve().then()
    // switchMap re-subscribes synchronously
    // Creates infinite microtask loop in some configurations
  )
  .subscribe(console.log)

// Symptom: Page completely freezes, no user interaction possible
// DevTools shows: "Page Unresponsive" or long "Scripting" bar in Performance
// Flame graph: microtask after microtask with no gaps
```

### Failure 2 — Timer Drift in Real-Time Applications

```javascript
// setInterval drifts because each callback takes time
// Example: 100ms interval, callback takes 20ms
// Actual intervals: 120ms, 118ms, 122ms... (drift accumulates)

// Fix: Self-correcting timer
function preciseInterval(fn, interval) {
  let expected = Date.now() + interval
  
  function step() {
    const drift = Date.now() - expected
    fn()
    expected += interval
    setTimeout(step, Math.max(0, interval - drift))
  }
  
  setTimeout(step, interval)
}

// Used in: stock tickers, game loops, WebRTC timing, music sequencers
```

### Debugging Event Loop Issues

```javascript
// Measure task duration using PerformanceObserver
const observer = new PerformanceObserver(list => {
  list.getEntries().forEach(entry => {
    if (entry.duration > 50) { // Long task > 50ms
      console.warn(`Long Task: ${entry.duration}ms`, entry)
    }
  })
})
observer.observe({ entryTypes: ['longtask'] })

// Chrome DevTools:
// Performance tab → Record → look for long red blocks in Main thread
// Each block = one task
// The grey gaps between blocks = microtask drain + rendering
// Filter: "Show native frames" to see V8 internal calls
```

---

## ⚠️ Edge Cases & Undefined Behaviors

### `queueMicrotask` vs `Promise.resolve().then`

```javascript
// Both queue a microtask. Subtle difference:
// Promise.resolve().then() wraps in PromiseReactionJob which has
// extra overhead (checking fulfillment state, handling rejection)

// queueMicrotask is lighter — direct microtask queue insert
queueMicrotask(() => console.log('microtask'))
Promise.resolve().then(() => console.log('promise microtask'))

// Both run in same iteration, queueMicrotask first
// (it was enqueued first in this example)
```

### `setTimeout(fn, 0)` is NOT immediate

```javascript
// Even with delay=0, timer fires AFTER microtasks AND possibly AFTER rendering
// Real minimum delay: browser-dependent (0-4ms)
// In practice: 0-1ms in Node.js, 4ms+ in nested browser timers

console.log('sync')
setTimeout(() => console.log('macro'), 0)
Promise.resolve().then(() => console.log('micro'))
// Always: sync → micro → macro
```

### Rendering Opportunity Timing

```javascript
// The browser decides IF and WHEN to render
// A single event loop iteration may or may not include rendering
// Factors: display refresh rate, vsync, tab visibility, GPU availability

// This means two consecutive tasks may be in the SAME rendered frame
// or in DIFFERENT frames — implementation defined

// Implication for animations:
// Code between two tasks is NOT necessarily visible to the user
// Only RAF callbacks happen BEFORE the next paint
```

---

## 🏢 Industry Best Practices

1. **Never block the event loop** — Any synchronous operation >16ms on the main thread causes frame drop. Move heavy computation to Web Workers or use the Scheduler API's `scheduler.yield()`.

2. **Use rAF for visual updates, not setTimeout** — rAF fires at the right time in the frame budget. setTimeout can fire at any point in the frame.

3. **Monitor long tasks** with `PerformanceObserver({ entryTypes: ['longtask'] })` in production. Any task >50ms is a long task per spec.

4. **Batch DOM reads and writes** — Use `requestAnimationFrame` to batch writes, read properties before writing in the same function.

5. **Use `queueMicrotask` for high-priority ordering** within the same task — it's cleaner than `Promise.resolve().then()` for scheduling microtasks without the Promise overhead.

---

## ⚖️ Trade-offs

| Mechanism | Scheduling Priority | Use Case |
|-----------|--------------------|----|
| Synchronous code | Immediate | Current execution |
| `queueMicrotask` | After current task, before next task | High-priority async work |
| `Promise.then` | Microtask (same as above) | Promise chains |
| `requestAnimationFrame` | Before next paint | Visual updates |
| `MessageChannel` | Task (faster than setTimeout) | High-frequency task scheduling |
| `setTimeout(0)` | Task (≥1-4ms) | Deferring non-critical work |
| `setInterval` | Periodic task | Polling |

---

## 💼 Interview Questions (With Solutions)

**Q1: What happens if a microtask adds another microtask? Does it run before the next task?**

> Yes. The microtask queue is drained to **complete exhaustion** after each task. If a microtask adds a new microtask, that new microtask runs immediately in the same drain cycle — before any tasks in the task queue. This can cause starvation: if microtasks continuously add microtasks, the event loop never advances to the next task, freezing the page.

**Q2: Why is `requestAnimationFrame` preferred over `setTimeout` for animations?**

> `setTimeout` is a task — it fires at an arbitrary point in the event loop, potentially mid-frame or before a frame is due. `rAF` callbacks are invoked by the browser at precisely the right time: just before the rendering update in that frame's budget. This means rAF animations are synchronized with the display refresh rate, preventing visual tearing and unnecessary double-paints. rAF is also automatically paused in hidden tabs, saving CPU/battery.

**Q3: How does React's scheduler use the Event Loop to achieve interruptible rendering?**

> React Fiber's scheduler uses `MessageChannel` (or `setTimeout(0)` as fallback) to schedule work in tasks. Each task runs a chunk of Fiber reconciliation work, then yields back to the event loop. Before yielding, it checks if the frame budget (usually 5ms per chunk) is exhausted using `performance.now()`. If more work remains, it schedules another task via `MessageChannel`. This allows the browser to process user input events between React's work chunks, preventing "jank" from React blocking the main thread.

---

## 🧩 Practice Problems (With Solutions)

**Problem:** Implement a scheduler that runs tasks in the background without blocking UI:

```javascript
class CooperativeScheduler {
  constructor(framebudgetMs = 5) {
    this.queue = []
    this.running = false
    this.budget = framebudgetMs
  }
  
  schedule(task) {
    this.queue.push(task)
    if (!this.running) this._run()
  }
  
  _run() {
    this.running = true
    const { port1, port2 } = new MessageChannel()
    
    port2.onmessage = () => {
      const deadline = performance.now() + this.budget
      
      while (this.queue.length && performance.now() < deadline) {
        const task = this.queue.shift()
        task()
      }
      
      if (this.queue.length) {
        port1.postMessage(null) // Schedule next chunk
      } else {
        this.running = false
      }
    }
    
    port1.postMessage(null) // Start first chunk
  }
}

const scheduler = new CooperativeScheduler(5)
for (let i = 0; i < 1000; i++) {
  scheduler.schedule(() => {
    // Process item i — won't block UI
    processItem(i)
  })
}
```

---

## 🔗 Navigation

**Prev:** [07_Prototype_and_Inheritance.md](07_Prototype_and_Inheritance.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [09_Promises.md](09_Promises.md)
