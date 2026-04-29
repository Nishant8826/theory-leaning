# 📌 12 — Execution Order Deep Dive

## 🧠 Concept Explanation (Deep Technical Narrative)

Understanding JavaScript execution order requires synthesizing everything: the EC stack, microtask queue, macrotask queue, rendering pipeline, and host-specific behaviors. This file is the capstone of the Fundamentals module — a complete reference for predicting execution order in complex scenarios.

The complete execution model:

```
1. Parse and evaluate the script (initial task)
2. Synchronous code runs to completion on the call stack
3. Microtask queue drained to exhaustion
4. If rendering opportunity: rAF → layout → paint
5. Next task from task queue
6. Repeat
```

But the devil is in the details — particularly around:
- How nested async functions interact with microtask timing
- How browser rendering interleaves with JS execution
- How Node.js phases differ from browser phases
- How `await` introduces asymmetric tick counts depending on what's awaited
- How Promise chaining depth affects microtask burst size

---

## 🔬 Internal Mechanics (Complete View)

### The Complete Priority Order

```
PRIORITY (highest → lowest):
════════════════════════════

1. SYNCHRONOUS CODE (current call stack)
   └─ Currently executing function to completion

2. MICROTASKS (after every task/microtask)
   ├─ process.nextTick (Node.js ONLY — before promises)
   ├─ Promise callbacks (PromiseReactionJob)
   ├─ queueMicrotask()
   └─ MutationObserver callbacks (browsers)

3. RENDERING (browsers — before next task, at frame boundary)
   ├─ requestAnimationFrame callbacks
   ├─ ResizeObserver callbacks
   ├─ IntersectionObserver callbacks
   └─ Style/Layout/Paint/Composite

4. MACROTASKS (one per event loop iteration)
   ├─ setImmediate (Node.js — after I/O phase)
   ├─ MessageChannel.port.onmessage
   ├─ setTimeout / setInterval
   ├─ I/O callbacks (fetch, XHR, file I/O)
   └─ DOM events (click, keydown, etc.)
```

### V8's Microtask Scope

V8 tracks "microtask scope depth". The microtask queue is drained when:
- The scope depth returns to 0 (after each JavaScript entry point)
- The host explicitly calls `v8::MicrotasksScope::PerformCheckpoint()`

In browsers, the host calls the checkpoint after every task. In Node.js, libuv calls it at the boundaries of each phase.

---

## 🔁 Execution Flow — Master Trace

```javascript
// Complete scenario: browser environment
const log = (s) => console.log(s)

// SETUP: before script runs
// State: call stack empty, all queues empty

log('01: script start')

// Macrotask scheduling
setTimeout(() => {
  log('10: setTimeout(0)')
  Promise.resolve().then(() => log('11: promise in setTimeout'))
}, 0)

setTimeout(() => log('12: setTimeout(0) #2'), 0)

// Microtask scheduling  
Promise.resolve()
  .then(() => {
    log('06: promise 1')
    return new Promise(resolve => {
      log('07: sync in promise')
      resolve()
    })
  })
  .then(() => log('08: promise 2'))
  .then(() => log('09: promise 3'))

queueMicrotask(() => log('05: queueMicrotask'))

// Async function
async function asyncFn() {
  log('03: async fn start')
  await null
  log('04: async fn after await')
}
asyncFn()

log('02: script end')

/*
SYNC PHASE:
  '01: script start'
  setTimeout(cb1, 0) → enqueue cb1 in timer task queue
  setTimeout(cb2, 0) → enqueue cb2 in timer task queue
  Promise chain → schedules microtask for promise1.then
  queueMicrotask → schedules microtask for '05'
  asyncFn() called:
    '03: async fn start'
    `await null` → schedules microtask to resume asyncFn (Promise.resolve(null).then)
    asyncFn() returns pending promise
  '02: script end'

MICROTASK DRAIN (after initial script task):
  Queue state: [promise1.then, queueMicrotask('05'), asyncFn_resume]
  
  1. promise1.then fires:
     '06: promise 1'
     `return new Promise(...)` executes executor synchronously:
       '07: sync in promise'  
       resolve() called → inner promise resolves
     PromiseResolveThenableJob scheduled (to forward to promise2)
     Queue: [queueMicrotask('05'), asyncFn_resume, PromiseResolveThenableJob]
  
  2. queueMicrotask fires: '05: queueMicrotask'
  
  3. asyncFn resumes: '04: async fn after await'
  
  4. PromiseResolveThenableJob runs → promise2 resolves → schedule promise2.then
  
  5. promise2.then fires: '08: promise 2'
     → promise3 resolves → schedule promise3.then
  
  6. promise3.then fires: '09: promise 3'

[Microtask queue empty]
[Rendering opportunity: probably not yet at 60fps]

MACROTASK: setTimeout cb1
  '10: setTimeout(0)'
  Promise.resolve().then → schedules microtask
  
  MICROTASK DRAIN:
    '11: promise in setTimeout'

MACROTASK: setTimeout cb2
  '12: setTimeout(0) #2'

FINAL OUTPUT:
01, 03, 02, 06, 07, 05, 04, 08, 09, 10, 11, 12
*/
```

---

## 🧠 Memory Behavior

```
Object lifecycle across execution phases:

SCRIPT TASK (Phase 1):
  - All declared closures allocated
  - Promise chains: each .then() creates JSPromise + PromiseReaction
  - setTimeout closures retained by timer queue

MICROTASK DRAIN (Phase 2):
  - Promise reaction jobs are small, short-lived
  - Each resolved promise's [[PromiseFulfillReactions]] cleared
  - Promise objects become eligible for GC as chain progresses

RENDERING (Phase 3):
  - Layout tree rebuilt incrementally
  - Paint records allocated for changed regions
  - GPU textures updated

MACROTASK (Phase 4):
  - Timer closure now on call stack (promoted from timer queue)
  - After callback runs: closure eligible for GC
```

---

## 📐 ASCII Diagram — Complete Timeline

```
Time →

0ms  [SCRIPT TASK STARTS]
     ┌────────────────────────────────────────────────────┐
     │ Synchronous code: 01, 03, 02                       │
     │ Schedule: setTimeout×2, Promise chain, asyncFn     │
     └────────────────────────────────────────────────────┘
     
     [MICROTASK DRAIN]
     ┌────────────────────────────────────────────────────┐
     │ 06: promise1.then                                  │
     │   07: sync inside new Promise                      │
     │   → schedules PromiseResolveThenableJob            │
     │ 05: queueMicrotask                                 │
     │ 04: asyncFn resumes                                │
     │ PromiseResolveThenableJob → resolves promise2      │
     │   → schedules promise2.then                        │
     │ 08: promise2.then                                  │
     │   → schedules promise3.then                        │
     │ 09: promise3.then                                  │
     └────────────────────────────────────────────────────┘
     
~1ms [RENDERING CHECK - skipped if <16.67ms since last paint]
     
     [MACROTASK: setTimeout(0) #1]
     ┌────────────────────────────────────────────────────┐
     │ 10: setTimeout callback                            │
     │   → schedules Promise.then                         │
     └────────────────────────────────────────────────────┘
     
     [MICROTASK DRAIN]
     ┌────────────────────────────────────────────────────┐
     │ 11: promise in setTimeout                          │
     └────────────────────────────────────────────────────┘
     
     [MACROTASK: setTimeout(0) #2]
     ┌────────────────────────────────────────────────────┐
     │ 12: setTimeout callback #2                         │
     └────────────────────────────────────────────────────┘

~16ms [RENDERING FRAME]
     rAF callbacks → style → layout → paint → composite
```

---

## 🔍 Code Examples

### Example 1 — Execution Order with Real async/await Chain

```javascript
async function A() {
  console.log('A1')
  await B()
  console.log('A2')
}

async function B() {
  console.log('B1')
  await C()
  console.log('B2')
}

async function C() {
  console.log('C1')
}

console.log('before')
A()
console.log('after')

/* Step-by-step:
SYNC:
  'before'
  A() called:
    'A1'
    B() called:
      'B1'  
      C() called:
        'C1'
        C returns (resolves C's promise)
      `await C()` → schedule microtask to resume B (after C resolves)
      B suspends → B's promise still pending
    `await B()` → schedule microtask to resume A (after B resolves)
    A suspends → A's promise still pending
  'after'

MICROTASK DRAIN:
  Resume B (after C resolved):
    'B2'
    B returns → B's promise resolves
    → schedule microtask to resume A
  Resume A (after B resolved):
    'A2'
    A returns → A's promise resolves

OUTPUT: before, A1, B1, C1, after, B2, A2
*/
```

### Example 2 — Promise.all Microtask Burst

```javascript
// How many microtask ticks does Promise.all with N promises take?
const start = performance.now()
let ticks = 0

// Instrument microtask counting
const origThen = Promise.prototype.then
Promise.prototype.then = function(...args) {
  return origThen.call(this, (...a) => { ticks++; return args[0]?.(...a) }, args[1])
}

const promises = Array.from({ length: 100 }, (_, i) => Promise.resolve(i))
await Promise.all(promises)

console.log(`Ticks: ${ticks}`)  // ~100 + overhead
// Each promise settlement → reaction job (microtask)
// Promise.all tracks count → when all done, resolves all-promise → more microtasks
// For 100 promises: burst of ~100 microtasks before .then() of Promise.all runs
```

### Example 3 — Node.js Phase-Specific Execution

```javascript
// Demonstrates Node.js event loop phases
// Run with: node example.js

const fs = require('fs')

fs.readFile(__filename, () => {  // I/O callback (poll phase)
  console.log('I/O callback')
  
  setImmediate(() => console.log('setImmediate inside I/O'))
  setTimeout(() => console.log('setTimeout inside I/O'), 0)
  
  process.nextTick(() => console.log('nextTick inside I/O'))
  Promise.resolve().then(() => console.log('Promise inside I/O'))
})

setImmediate(() => console.log('setImmediate outside I/O'))
setTimeout(() => console.log('setTimeout outside I/O'), 0)

// Inside I/O callback: nextTick → Promise → setImmediate BEFORE setTimeout
// Outside I/O callback: setTimeout vs setImmediate order is UNDEFINED
// (depends on system timer resolution at startup)
```

### Example 4 — rAF Timing vs Microtasks

```javascript
// Demonstrates that rAF runs AFTER microtasks but BEFORE next task
// (in the rendering phase of the event loop)

button.addEventListener('click', () => {
  // This is a TASK
  
  requestAnimationFrame(() => {
    // This runs in the RENDERING PHASE after this task's microtasks drain
    element.style.color = 'red'  // Applied in this render frame
  })
  
  Promise.resolve().then(() => {
    // This runs in MICROTASK DRAIN (before rAF)
    console.log('microtask ran first')
  })
  
  // Note: any DOM mutations here are NOT yet reflected visually
  // The rendering phase hasn't happened yet
  element.style.background = 'blue'  // Will render in same frame as the rAF red
})

// Timeline in click handler's iteration:
// [click task] → sync code → [microtask drain] → [rAF] → [rendering] → [next task]
```

---

## 💥 Production Failures & Debugging

### Failure 1 — Race Between Promise and DOM Event

```javascript
// Production bug at a financial services company
// User clicked "Submit" twice rapidly

let processing = false

submitButton.addEventListener('click', async () => {
  if (processing) return
  processing = true  // Set synchronously
  
  try {
    const result = await submitOrder()
    // After await: we're in a MICROTASK
    // During this microtask, no other click events can fire
    // (click events are tasks, not microtasks)
    // BUT: if submitOrder takes time, another click CAN fire before await resumes
    // because between the current task and the next task (network response),
    // the event loop is free to process other events
    
    showSuccess(result)
    processing = false  // WRONG: race if another click happened while awaiting
  } catch(e) {
    processing = false
    showError(e)
  }
})

// Fix: Use AbortController + server-side idempotency keys
// NOT just a boolean flag that can be violated between async gaps
```

### Failure 2 — Unintended Batching Assumption

```javascript
// React 17 behavior (NOT React 18):
// State updates outside React event handlers are NOT batched

setTimeout(() => {
  setState({ a: 1 }) // Triggers render
  setState({ b: 2 }) // Triggers another render
  // TWO renders! May cause visual flicker or inconsistent UI
}, 1000)

// React 18 with automatic batching:
// Both updates are batched into ONE render, using the scheduler

// If you need to opt out of batching in React 18:
import { flushSync } from 'react-dom'
setTimeout(() => {
  flushSync(() => setState({ a: 1 })) // Render now
  flushSync(() => setState({ b: 2 })) // Render now
}, 1000)
```

### Complete DevTools Workflow for Execution Order Debugging

```
1. Open Chrome DevTools → Performance tab
2. Click "Record" 
3. Trigger the interaction
4. Click "Stop"
5. In the flame chart:
   - Wide colored blocks = Tasks
   - Narrow sections between blocks = microtask drains + rendering
   - "Rendering" section = style/layout/paint
   - Look for "Animation Frame Fired" = rAF callback

6. Click on any JS block to see call stack
7. Use "Timings" row to see LCP, FCP, FID markers

For Node.js:
$ clinic flame -- node app.js
$ clinic bubbleprof -- node app.js  # Shows async context timing
```

---

## ⚠️ Edge Cases — Tricky Execution Orders

### Edge Case 1 — Resolved Promise Before .then()

```javascript
// Common misconception: "Promise.resolve() should be synchronous"
const p = Promise.resolve(42)
p.then(v => console.log('async:', v))
console.log('sync')

// Output: 'sync', 'async: 42'
// Even though p is ALREADY resolved, .then() always schedules a microtask
// Promises NEVER call handlers synchronously — always via microtask
```

### Edge Case 2 — Multiple await Ticks

```javascript
async function countTicks() {
  const start = await Promise.resolve('start')  // 1 tick
  const middle = await fetch('/api')             // 1 tick (when fetch resolves, could be much later)
  const end = await start + 'end'               // 1 tick
  return end
}
// Each `await` is at minimum 1 microtask tick
// `await fetch(...)` is actually much more complex:
// - Returns to event loop (fetch is I/O)
// - Network request goes through browser's network stack
// - When response arrives: I/O callback fires (task)
// - Promise resolves → microtask to resume async fn
// Total: many event loop iterations happen between second and third log
```

### Edge Case 3 — async constructor pattern (anti-pattern)

```javascript
// Classes cannot have async constructors — constructor is sync
class DataLoader {
  constructor() {
    this.data = null
    this.load()  // Fire and forget async — BAD
  }
  async load() {
    this.data = await fetchData()
  }
}

const loader = new DataLoader()
console.log(loader.data)  // null — async hasn't completed yet

// Pattern: async factory function
class DataLoader {
  static async create() {
    const instance = new DataLoader()
    instance.data = await fetchData()
    return instance
  }
  constructor() { this.data = null }
}

const loader = await DataLoader.create()
console.log(loader.data)  // actual data ✓
```

---

## 🏢 Industry Best Practices

1. **Draw execution order diagrams for complex async flows** — Before implementing multi-promise workflows, sketch the timeline. Bugs in ordering are only visible when you trace the full path.

2. **Test execution order with automated timing tests** — Use `jest.useFakeTimers()` and `await Promise.resolve()` (to flush microtasks) in tests that verify ordering.

3. **Document async boundaries explicitly** — In production code, comment where async gaps occur. "Below this await, multiple event loop iterations may have passed" is important for reasoning about state.

4. **Use AsyncLocalStorage (Node.js) or Zone.js (Angular)** for request-scoped context that survives async boundaries.

5. **Don't rely on execution order between unrelated async operations** — Two concurrent `fetch()` calls will complete in network order, not registration order.

---

## ⚖️ Complete Execution Order Reference Table

| What | When | Notes |
|------|------|-------|
| Synchronous code | Immediately | On call stack |
| Promise executor | Synchronously when `new Promise(exec)` is called | Before `.then()` reactions |
| `process.nextTick` | Before microtasks | Node.js only |
| `Promise.then` | Next microtask checkpoint | Always async |
| `queueMicrotask` | Next microtask checkpoint | Cross-platform |
| `MutationObserver` | Microtask checkpoint | Browsers only |
| `requestAnimationFrame` | Before next paint | Skipped in hidden tabs |
| `MessageChannel` | Next task | Faster than setTimeout |
| `setTimeout(0)` | Next task, ≥0ms | Subject to 4ms clamp |
| `setImmediate` | After I/O phase | Node.js only |
| I/O callbacks | After I/O completes | Network/file system |

---

## 💼 Interview Questions (With Solutions)

**Q1: What is the output of Promise.resolve(Promise.resolve(42)).then(console.log)?**

> `42`. `Promise.resolve` called with a native Promise returns the SAME promise — no unwrapping occurs. So `Promise.resolve(Promise.resolve(42))` is the same promise as `Promise.resolve(42)`. The `.then(console.log)` then runs as a microtask with value `42`. Only 1 extra tick.

**Q2: In Node.js, if both `process.nextTick` and `Promise.resolve().then()` are scheduled inside a `setImmediate` callback, which runs first?**

> `process.nextTick`. Inside any callback (including `setImmediate`), V8 drains the nextTick queue first, then the promise microtask queue. Both run before the next task, but nextTick always precedes promise reactions. This is Node.js-specific behavior — browsers have no nextTick.

**Q3: Can two `requestAnimationFrame` callbacks from the same frame see each other's DOM mutations?**

> Only if they're called in order. rAF callbacks registered in the same frame run sequentially. If callback A mutates the DOM, callback B (registered later, same frame) sees the mutation. However, neither callback sees the RENDERED result — rendering happens after all rAF callbacks complete. Both mutations will be visible in the NEXT frame's paint.

---

## 🧩 Practice Problem — Ultimate Execution Order Test

```javascript
// Node.js environment. Predict complete output:

const { promisify } = require('util')
const sleep = promisify(setTimeout)

async function main() {
  console.log('1')
  
  setImmediate(() => console.log('2'))
  process.nextTick(() => console.log('3'))
  
  await sleep(0)
  
  console.log('4')
  process.nextTick(() => console.log('5'))
  Promise.resolve().then(() => console.log('6'))
  setImmediate(() => console.log('7'))
}

main()
process.nextTick(() => console.log('8'))
```

**Solution:**
```
1, 8, 3, 2, 4, 5, 6, 7

Explanation:
SYNC: '1'
nextTick queue: [8, 3 (registered inside async before first await)]

Wait — actually:
- main() runs sync code:
  '1'
  setImmediate('2') → scheduled  
  nextTick('3') → nextTick queue: [3]
  `await sleep(0)` → setTimeout(resolve, 0) scheduled → main suspends
- outer nextTick('8') → nextTick queue: [3, 8]

NEXTTICK: '3', '8' (node runs nextTick before returning to event loop)

MACROTASK: setImmediate('2')
  nextTick drain: (empty)
  '2'

MACROTASK: setTimeout resolves → main() resumes (promise microtask)
  NEXTTICK drain first: (empty)
  PROMISE MICROTASK: main resumes:
    '4'
    nextTick('5') → next tick queue
    Promise.resolve('6') → microtask queue
    setImmediate('7') → scheduled

NEXTTICK: '5'
PROMISE MICROTASK: '6'

MACROTASK: setImmediate('7')

Final: 1, 3, 8, 2, 4, 5, 6, 7
```

---

## 🔗 Navigation

**Prev:** [11_Microtasks_vs_Macrotasks.md](11_Microtasks_vs_Macrotasks.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [../Advanced/01_Deep_vs_Shallow_Copy.md](../Advanced/01_Deep_vs_Shallow_Copy.md)
