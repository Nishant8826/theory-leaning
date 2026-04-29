# 📌 11 — Microtasks vs Macrotasks

## 🧠 Concept Explanation (Deep Technical Narrative)

The distinction between microtasks and macrotasks (tasks) is fundamental to understanding JavaScript's scheduling model. They answer the question: **in what order does the runtime decide to execute callbacks?**

- **Macrotask (Task):** A unit of work in the **Task Queue**. The event loop picks exactly ONE per iteration. After it completes, the microtask queue is fully drained before any next task runs.
- **Microtask:** A unit of work in the **Microtask Queue**. Runs after the current task (or microtask) completes but before the next task. Multiple microtasks can run per event loop iteration — they are drained to exhaustion.

This two-queue model is defined in the **HTML Living Standard** (for browsers) and implemented separately in **libuv** (for Node.js). V8 itself manages only the microtask queue; the host environment (browser or Node.js) manages the task queue.

---

## 🔬 Internal Mechanics (Engine-Level)

### Microtask Queue — V8's Domain

V8 maintains the microtask queue internally as part of its **microtask scope**. The queue is:
- Per-Isolate (per JS thread) — not shared between workers
- Drained synchronously within V8 after each `RunMicrotasks()` call
- The host calls `RunMicrotasks()` at the appropriate points in the event loop

**Sources of microtasks:**
| Source | Mechanism |
|--------|-----------|
| `Promise.then()` | `PromiseReactionJob` scheduled by V8 |
| `async/await` | `PromiseReactionJob` at each await resumption |
| `queueMicrotask(fn)` | Direct microtask queue insertion |
| `MutationObserver` callbacks | Browser enqueues as microtask |

### Task Queue — Host Environment's Domain

The browser has **multiple task queues** with different priorities:
- User interaction queue (click, keypress) — highest priority
- Networking queue (fetch, XHR callbacks)
- Timer queue (setTimeout, setInterval)
- Rendering tasks (internal)

Node.js has its own phases (see `07_Event_Loop_Node_vs_Browser.md` for full coverage).

**Sources of macrotasks:**
| Source | Notes |
|--------|-------|
| `setTimeout(fn, delay)` | ≥0ms delay |
| `setInterval(fn, period)` | Periodic |
| `MessageChannel.port.onmessage` | Faster than setTimeout(0) |
| `fetch`/`XHR` completion | I/O task |
| DOM event handlers | click, keydown, etc. |
| `<script>` parsing | Initial execution |

---

## 🔁 Execution Flow (Step-by-Step)

```javascript
// Complete execution order demonstration
console.log('1: sync start')

setTimeout(() => console.log('2: macrotask 1'), 0)
setTimeout(() => console.log('3: macrotask 2'), 0)

Promise.resolve()
  .then(() => {
    console.log('4: microtask 1')
    queueMicrotask(() => console.log('5: microtask 3 (nested)'))
    return Promise.resolve()
  })
  .then(() => console.log('6: microtask 2'))

queueMicrotask(() => console.log('7: microtask 0 (direct)'))

console.log('8: sync end')
```

**Output trace:**

```
1: sync start       ← Synchronous
8: sync end         ← Synchronous

Task ends → drain microtask queue:

7: microtask 0      ← queueMicrotask (enqueued first among microtasks)
4: microtask 1      ← Promise.then (runs, schedules nested microtask + returns promise)
5: microtask 3      ← nested queueMicrotask from microtask 1 (enqueued during drain)
6: microtask 2      ← Promise.then chained after microtask 1 resolved

Microtask queue empty → rendering opportunity check → next task:

2: macrotask 1      ← setTimeout (first registered)
3: macrotask 2      ← setTimeout (second registered)
```

---

## 🧠 Memory Behavior

```
Task Queue entries:
  Each task: function pointer + closure context
  Pending tasks keep closures alive (and all their captured vars)
  
  setTimeout callback waiting 5 seconds:
  → Its closure is retained for 5 seconds
  → All captured variables in the closure are retained 5 seconds
  → If the closure captures a large object: memory held for timer duration

Microtask Queue entries:
  PromiseReactionJob: { handler: JSFunction, capability: JSPromise }
  → Cleared immediately after running
  → Short-lived compared to task queue entries

Implication: Long-lived timers holding large closures = memory pressure
Fix: Avoid capturing large objects in setTimeout callbacks
```

---

## 📐 ASCII Diagram — Queue Priority Model

```
                     EVENT LOOP ITERATION
                     
┌─────────────────────────────────────────────────────────────────┐
│  TASK QUEUE (pick ONE task per iteration)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ onClick  │ │setTimeout│ │ fetch cb │ │ msgChan  │  ...      │
│  └────┬─────┘ └──────────┘ └──────────┘ └──────────┘          │
│       │ Execute this one task                                    │
└───────┼──────────────────────────────────────────────────────────┘
        │
        ▼ Task completes
        
┌─────────────────────────────────────────────────────────────────┐
│  MICROTASK QUEUE (drain ALL before next task)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                        │
│  │promise.  │ │queueMicro│ │mutation  │  ← can add more!       │
│  │then cb   │ │task cb   │ │observer  │                        │
│  └──────────┘ └──────────┘ └──────────┘                        │
│  ↓ (if microtask adds microtask) ↓                              │
│  ┌──────────┐                                                   │
│  │ nested   │  ← added DURING drain, still runs THIS iteration  │
│  └──────────┘                                                   │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼ All microtasks complete
        
┌─────────────────────────────────────────────────────────────────┐
│  RENDERING (if time budget allows)                               │
│  rAF → layout → paint → composite                               │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼ Next iteration
```

---

## 🔍 Code Examples

### Example 1 — Starvation Scenario

```javascript
// Microtask starvation: infinite microtask loop blocks all tasks
function starveTasks() {
  let count = 0
  
  function microtaskLoop() {
    count++
    if (count < 1e6) {
      queueMicrotask(microtaskLoop) // Add another microtask
    }
  }
  
  queueMicrotask(microtaskLoop)
  
  setTimeout(() => {
    console.log('This never runs until microtask loop finishes')
  }, 0)
}

// During microtask starvation:
// - No UI events processed
// - No timers fire
// - No network responses handled
// - No rendering updates
// Browser: page is frozen for the duration
```

### Example 2 — Node.js `process.nextTick` vs `Promise`

```javascript
// Node.js has THREE priority levels:
// 1. process.nextTick → "nextTick queue" (BEFORE promises in Node.js)
// 2. Promise microtasks → microtask queue
// 3. setImmediate/setTimeout → task queue (I/O phases)

setImmediate(() => console.log('A: setImmediate'))
setTimeout(() => console.log('B: setTimeout'), 0)
Promise.resolve().then(() => console.log('C: promise'))
process.nextTick(() => console.log('D: nextTick'))
console.log('E: sync')

// Node.js output: E, D, C, A or B, B or A
// (A vs B order depends on event loop timing, typically setImmediate after setTimeout)
// Always: sync → nextTick → promises → setImmediate/setTimeout

// WARNING: process.nextTick can also starve the event loop
// if callbacks add more nextTick callbacks
```

### Example 3 — MutationObserver Microtask Timing

```javascript
// MutationObserver callbacks fire as microtasks
// This is important for React's DOM batching strategy

const observer = new MutationObserver(mutations => {
  console.log('DOM changed:', mutations.length, 'mutations')
  // This runs as a MICROTASK after the current task
  // NOT after each individual DOM mutation
})

observer.observe(document.body, { childList: true, subtree: true })

// These mutations are BATCHED — observer fires ONCE with all changes
document.body.append(document.createElement('div'))
document.body.append(document.createElement('div'))
document.body.append(document.createElement('div'))
// MutationObserver fires ONCE with 3 mutations (after task completes)
// Compare: if observer fired synchronously, it would run 3 times
```

### Example 4 — Ordering Guarantees

```javascript
// What can you rely on?
// 1. Microtasks run AFTER the current synchronous code
// 2. Microtasks run BEFORE the next task (timer, I/O callback)
// 3. All microtasks run before rendering
// 4. Microtasks are drained to completion (including dynamically added ones)

// What you CANNOT rely on:
// 1. Order of macrotasks across different sources (OS-dependent)
// 2. setTimeout(0) firing before/after setImmediate (in Node.js)
// 3. Whether rendering happens between two consecutive tasks

// Example of reliable vs unreliable ordering:
setTimeout(() => console.log('A'), 0)
setTimeout(() => console.log('B'), 0)
// A ALWAYS before B (same queue, FIFO) ✓ Reliable

setTimeout(() => console.log('C'), 0)
setImmediate(() => console.log('D'))
// C vs D order in Node.js: UNRELIABLE (depends on event loop timing)
```

---

## 💥 Production Failures & Debugging

### Failure 1 — Race Condition via Microtask Assumption

```javascript
// Production bug: assuming microtask fires before DOM event
let state = 'initial'

button.addEventListener('click', () => {
  // This is a TASK (DOM event)
  state = 'clicked'
})

Promise.resolve().then(() => {
  // This is a microtask WITHIN the click handler's task
  // IF the promise was created before the click, this may have
  // already run before the click task executes
  console.log(state) // 'initial' — the click task hasn't run yet!
})

// The bug: Developer thought microtask fires "after" click
// Reality: if microtask was scheduled in a PREVIOUS task,
// it already ran before the click handler task
```

### Failure 2 — Missing Re-render Due to Microtask

```javascript
// React state updates batch differently in different contexts

// In React event handler (task): batched automatically
button.addEventListener('click', () => {
  setState({ a: 1 })  // Batched
  setState({ b: 2 })  // Batched
  // ONE render after both state updates
})

// In setTimeout (before React 18): NOT batched
setTimeout(() => {
  setState({ a: 1 })  // Renders immediately
  setState({ b: 2 })  // Renders again (double render!)
})

// React 18 "automatic batching" fixes this using scheduler:
// Uses queueMicrotask to defer re-renders within the same "work"
// Unifies behavior across events, timeouts, promises
```

### Debugging Queue Ordering

```javascript
// DevTools trick: Log with timestamps
const t0 = performance.now()
const log = (label) => {
  const delta = (performance.now() - t0).toFixed(3)
  console.log(`[+${delta}ms] ${label}`)
}

setTimeout(() => log('setTimeout'), 0)
Promise.resolve().then(() => log('Promise.then'))
queueMicrotask(() => log('queueMicrotask'))
log('sync')

// Output shows exact timing:
// [+0.000ms] sync
// [+0.002ms] queueMicrotask
// [+0.003ms] Promise.then
// [+0.112ms] setTimeout  ← note the gap: task queue delay
```

---

## ⚠️ Edge Cases & Undefined Behaviors

### `queueMicrotask` during Microtask Drain

```javascript
queueMicrotask(() => {
  console.log('micro 1')
  queueMicrotask(() => console.log('micro 2 (nested)'))
})
queueMicrotask(() => console.log('micro 3'))

// Output: micro 1, micro 3, micro 2
// WHY: When micro 1 runs, micro 2 is enqueued
// At that point, micro 3 is already in the queue AHEAD of micro 2
// Queue at time of micro 1 execution: [micro 3]
// After micro 1 adds micro 2: [micro 3, micro 2]
// Run micro 3 → run micro 2
```

### Browser vs Node.js `Promise` Queue Position

```javascript
// Browser: Promise microtasks are standard microtasks
// Node.js: process.nextTick runs BEFORE promise callbacks
// (nextTick has a separate, higher-priority queue)

// This causes subtle bugs when:
// 1. Code uses process.nextTick expecting Promise-level timing
// 2. Code is ported between browser and Node.js

// Node.js 11+: process.nextTick fires between each I/O phase AND
// before promise microtasks within the same phase
```

---

## 🏢 Industry Best Practices

1. **Use microtasks for state updates** — If you need to defer work until "after current code but before next event", use `queueMicrotask` or `Promise.resolve().then()`.

2. **Never create infinite microtask loops** — Always have a termination condition for recursive microtask scheduling.

3. **Understand Node.js nextTick priority** — `process.nextTick` fires before promises. Use `setImmediate` if you want to defer until after I/O in the same tick.

4. **Test timing assumptions explicitly** — Don't assume ordering between different async sources without a diagram. Write tests that verify the execution order.

5. **React 18 automatic batching** — Understand that React 18 uses scheduler's microtask-based batching to unify state update behavior. Your custom render schedulers should not fight this.

---

## ⚖️ Trade-offs

| Queue | Priority | Use Case | Risk |
|-------|----------|----------|------|
| Microtask | Highest async | DOM-consistent state, promise chains | Can starve event loop |
| process.nextTick | Above promises (Node) | Node.js error propagation | Starvation, not portable |
| rAF | Before render | Animation, visual updates | Skipped in hidden tabs |
| MessageChannel | Task (fast) | Scheduling yielding | Not synchronized with rendering |
| setTimeout(0) | Task (slow) | Non-critical deferral | 4ms clamp, drift |

---

## 💼 Interview Questions (With Solutions)

**Q1: If a Promise rejection handler throws, where does the error go?**

> It creates a rejected promise for the next `.then()` or `.catch()` in the chain. This is scheduled as another `PromiseReactionJob` in the microtask queue. If there is no subsequent handler, it becomes an unhandled rejection, triggering `unhandledrejection` event in browsers or `process.on('unhandledRejection')` in Node.js.

**Q2: What is the difference between `process.nextTick` and `queueMicrotask` in Node.js?**

> Both run before the next event loop phase (before I/O tasks), but `process.nextTick` callbacks are executed from a separate **nextTick queue** that is drained BEFORE the promise microtask queue. This means `nextTick` callbacks always run before `Promise.then` callbacks, even if the promise was resolved before the `nextTick` was registered. `queueMicrotask` is cross-platform (browser and Node.js) and uses the standard microtask queue.

**Q3: Can a microtask cause a layout thrash?**

> Yes. If a MutationObserver microtask (or a Promise `.then()`) reads layout properties (like `offsetHeight`) after a style mutation was queued but before the browser has a chance to update the layout, it forces a **synchronous style recalculation and layout**. This is layout thrashing within the microtask context. The fact that microtasks run before rendering means every microtask runs in the "post-task, pre-render" window — ideal for batching state but risky for layout reads.

---

## 🧩 Practice Problems (With Solutions)

**Problem:** Predict the complete output and explain:

```javascript
async function main() {
  console.log('1')
  
  await Promise.resolve()
  console.log('2')
  
  await new Promise(resolve => setTimeout(resolve, 0))
  console.log('3')
  
  await Promise.resolve()
  console.log('4')
}

main()
console.log('5')
setTimeout(() => console.log('6'), 0)
Promise.resolve().then(() => console.log('7'))
```

**Solution:**
```
Output: 1, 5, 2, 7, 3, 4, 6

Explanation:
1 → sync (before first await)
5 → sync (after main() returns pending promise)

Microtask drain 1:
  - main() resumes at first await → '2'
  - main() hits second await (setTimeout) → suspends, schedules setTimeout
  - '7' → Promise.resolve().then() callback

[Rendering check]

Task: setTimeout from second await fires → main() resumes → '3'
  - main() hits third await (Promise.resolve) → schedules microtask

Microtask drain 2:
  - main() resumes → '4'

Task: setTimeout(() => '6', 0) fires (was registered at same time as await's setTimeout,
but await's setTimeout was registered first — however, await's setTimeout resolves main,
which then awaits another Promise, then the outer '6' setTimeout fires)
```

---

## 🔗 Navigation

**Prev:** [10_Async_Await.md](10_Async_Await.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [12_Execution_Order_Deep_Dive.md](12_Execution_Order_Deep_Dive.md)
