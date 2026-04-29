# 📌 09 — Promises

## 🧠 Concept Explanation (Deep Technical Narrative)

A Promise is a **state machine** that represents the eventual result of an asynchronous operation. Its three states (`pending`, `fulfilled`, `rejected`) are internal slots in the specification, and transitions are one-way and irrevocable. The critical engineering insight: **Promise settlement scheduling is done via the microtask queue**, meaning promise reactions run before the next task but after the current synchronous execution completes.

In V8's implementation, Promises are implemented as **JSPromise objects** — a subtype of JSObject with special internal slots:
- `[[PromiseState]]`: `kPending`, `kFulfilled`, `kRejected`
- `[[PromiseResult]]`: the settled value
- `[[PromiseFulfillReactions]]`: list of reactions when fulfilled
- `[[PromiseRejectReactions]]`: list of reactions when rejected
- `[[PromiseIsHandled]]`: flag for unhandled rejection tracking

The V8 `PromiseReactionJob` is the unit of work scheduled to the microtask queue when a promise settles.

---

## 🔬 Internal Mechanics (Engine-Level — V8)

### Promise Creation and Resolution

```javascript
new Promise((resolve, reject) => {
  // The executor runs SYNCHRONOUSLY — immediately, in the current task
  resolve(42)
})
```

V8 execution:
1. Allocates `JSPromise` object on heap
2. Creates `resolve` and `reject` functions (BuiltinFunction objects)
3. Calls executor synchronously with `(resolve, reject)`
4. `resolve(42)` → calls V8's `PromiseResolveFunction`:
   - Checks if value is a thenable (duck-type check)
   - If not: transitions `[[PromiseState]]` → `kFulfilled`, `[[PromiseResult]]` → 42
   - Schedules `PromiseReactionJob` for each registered `.then()` handler
5. Executor returns → Promise object returned to caller

### `.then()` Chaining Internals

```javascript
promise.then(onFulfilled, onRejected)
```

V8 creates a **PromiseReaction** object: `{ capability, handler }` where:
- `capability` wraps the new promise created by `.then()`
- `handler` is the provided callback

This reaction is either:
- Scheduled immediately to microtask queue (if promise already settled)
- Stored in `[[PromiseFulfillReactions]]` (if pending)

**The chaining mechanism:** When `onFulfilled` completes, V8 takes its return value and calls `PromiseResolveThenableJob` on the next promise in the chain — scheduling ANOTHER microtask. This is why deep `.then()` chains add microtask overhead per hop.

### Thenable Resolution — The Hidden Async

```javascript
Promise.resolve(thenable)
// where thenable = { then: function(resolve, reject) {...} }
```

V8 **does not** immediately resolve. It must call `thenable.then(resolve, reject)` to get the actual value. This is done via `PromiseResolveThenableJob` — a microtask! This means:

```javascript
const thenable = { then(resolve) { resolve(42) } }
Promise.resolve(thenable).then(v => console.log(v))
// Requires 2 microtask ticks: 1 for PromiseResolveThenableJob, 1 for .then()
// Compare: Promise.resolve(42).then(v => ...) — only 1 microtask tick
```

This is a non-obvious performance implication when returning thenables from `.then()` handlers.

---

## 🔁 Execution Flow (Step-by-Step)

```javascript
const p = new Promise(resolve => {
  console.log('1')  // Sync: executor runs immediately
  resolve('value')
  console.log('2')  // Sync: still in executor
})

p.then(v => {
  console.log('3:', v)  // Microtask
  return 'chained'
}).then(v => {
  console.log('4:', v)  // Microtask
})

console.log('5')  // Sync
```

**Execution trace:**

```
SYNC execution:
  new Promise executor → logs '1'
  resolve('value') → schedules PromiseReactionJob in microtask queue
                   → reaction for handler '3' queued
  logs '2'
  .then(handler3) → p already settled → schedule PromiseReactionJob immediately
                  → BUT: handler3 was registered WHILE reaction was being scheduled
                  → Result: handler3 IS the scheduled reaction
  .then(handler4) → p2 (result of first .then) is still pending → store handler4
  logs '5'

MICROTASK DRAIN:
  Run PromiseReactionJob for handler3:
    logs '3: value'
    returns 'chained'
    → p2 resolved with 'chained'
    → schedules PromiseReactionJob for handler4
  
  Run PromiseReactionJob for handler4:
    logs '4: chained'

Output: 1, 2, 5, 3: value, 4: chained
```

---

## 🧠 Memory Behavior

```
Promise chain memory model:

p ──────────────────────────────────────────────────────────┐
  [[PromiseState]]: kFulfilled                              │
  [[PromiseResult]]: 'value'                                │
  [[PromiseFulfillReactions]]: [] (cleared after settling)  │
                                                            │
p.then() creates p2 ─────────────────────────────────────┐ │
  [[PromiseState]]: kFulfilled (after reaction runs)       │ │
  [[PromiseResult]]: 'chained'                             │ │
                                                           │ │
p2.then() creates p3 ──────────────────────────────────┐  │ │
  [[PromiseState]]: kFulfilled                          │  │ │
  [[PromiseResult]]: undefined                          │  │ │
                                                        │  │ │
GC: p3, p2, p are all eligible for collection           │  │ │
ONLY if no external references hold them                │  │ │
                                                        │  │ │
const chain = p.then(...).then(...)                     │  │ │
`chain` keeps p3 alive, but p3's ref to p2 keeps p2,   │  │ │
and p2's reaction keeps a ref to p... NOT retained once │  │ │
settled. Only the FINAL promise in chain needs keeping. └──┘ ┘
```

**Memory optimization:** V8 clears `[[PromiseFulfillReactions]]` and `[[PromiseRejectReactions]]` after the promise settles and reactions are scheduled. The settled value in `[[PromiseResult]]` is retained until the promise is GC'd.

---

## 📐 ASCII Diagram — Promise State Machine

```
             ┌─────────────────────────┐
             │        PENDING          │
             │  [[PromiseState]]:      │
             │    kPending             │
             │  [[PromiseResult]]:     │
             │    undefined            │
             └─────────────────────────┘
                   │           │
            resolve(v)      reject(e)
                   │           │
                   ▼           ▼
    ┌─────────────────┐   ┌─────────────────┐
    │   FULFILLED     │   │    REJECTED     │
    │ kFulfilled      │   │  kRejected      │
    │ result: v       │   │  result: e      │
    └─────────────────┘   └─────────────────┘
           │                      │
    PromiseReactionJob      PromiseReactionJob
    (microtask)             (microtask)
           │                      │
     onFulfilled             onRejected
     handler runs            handler runs
```

---

## 🔍 Code Examples

### Example 1 — Promise.all vs Promise.allSettled vs Promise.race

```javascript
const slow = new Promise(r => setTimeout(() => r('slow'), 100))
const fast = new Promise(r => setTimeout(() => r('fast'), 10))
const fail = Promise.reject(new Error('failed'))

// Promise.all: ALL must succeed, fails fast on first rejection
await Promise.all([slow, fast, fail])
// Rejects immediately with Error('failed')
// 'slow' and 'fast' promises still run but results are ignored

// Promise.allSettled: waits for ALL, gives results as {status, value/reason}
await Promise.allSettled([slow, fast, fail])
// [
//   { status: 'fulfilled', value: 'slow' },
//   { status: 'fulfilled', value: 'fast' },
//   { status: 'rejected', reason: Error('failed') }
// ]

// Promise.race: first settled wins (fulfill OR reject)
await Promise.race([slow, fast])
// 'fast' — settles first

// Promise.any: first FULFILLED wins, rejects if ALL reject
await Promise.any([fast, fail])
// 'fast' — ignores the rejection

// V8 optimization: Promise.all registers reactions on each promise.
// When one settles, it decrements an internal counter.
// When counter reaches 0 (all settled), the all-promise resolves.
// No polling — purely reaction-based.
```

### Example 2 — Unhandled Promise Rejection

```javascript
// V8/Node.js tracks unhandled rejections via PromiseIsHandled flag
const p = Promise.reject(new Error('unhandled'))

// At this point: [[PromiseIsHandled]] = false
// V8 schedules a microtask to check if a rejection handler is added

// If no .catch() or onRejected handler is added before the check:
// Browser: window.onunhandledrejection event fires
// Node.js: process.on('unhandledRejection') fires

// Adding a handler AFTER rejection:
setTimeout(() => {
  p.catch(e => console.log('caught late:', e))
  // Browser: still fires unhandledrejection (already past microtask check)
  // Node.js: fires unhandledRejection, then rejectionHandled when caught
}, 0)

// Best practice: always .catch() or use try/catch in async/await
// Production monitoring: UnhandledPromiseRejection = bug that silently swallowed errors
```

### Example 3 — Promise Cancellation (Missing Feature)

```javascript
// Promises have no native cancellation (AbortController fills this gap for fetch)
// Pattern: CancellablePromise wrapper

class CancellablePromise {
  constructor(executor) {
    this._cancelled = false
    this.promise = new Promise((resolve, reject) => {
      executor(
        value => { if (!this._cancelled) resolve(value) },
        reason => { if (!this._cancelled) reject(reason) }
      )
    })
  }
  
  cancel() {
    this._cancelled = true
  }
  
  then(...args) { return this.promise.then(...args) }
  catch(...args) { return this.promise.catch(...args) }
}

// Usage:
const cancellable = new CancellablePromise(resolve => {
  setTimeout(() => resolve('done'), 5000)
})

cancellable.then(v => console.log(v))
cancellable.cancel() // 'done' never logs

// Better: AbortController for fetch operations
const controller = new AbortController()
fetch('/api/data', { signal: controller.signal })
controller.abort() // Cancels the fetch
```

### Example 4 — Promise Performance Anti-pattern

```javascript
// SLOW: Unnecessary Promise wrapping
async function fetchData(url) {
  return new Promise((resolve, reject) => {
    fetch(url)
      .then(resolve)
      .catch(reject)
  })
}
// Creates extra Promise allocation, extra microtask hop

// FAST: Just await directly
async function fetchData(url) {
  return fetch(url) // async fn auto-wraps return value in promise
}

// Or even simpler if just returning:
const fetchData = (url) => fetch(url)
// No async overhead at all — fetch already returns a Promise
```

---

## 💥 Production Failures & Debugging

### Failure 1 — Promise Chain Error Swallowing

```javascript
// Classic production bug: uncaught rejection in the middle of a chain
function processOrder(orderId) {
  return fetchOrder(orderId)
    .then(order => {
      if (!order.items.length) throw new Error('Empty order')
      return processItems(order.items)  // Returns a Promise
    })
    .then(result => {
      // If processItems rejects, this .then() is skipped
      // But the rejection propagates to...
      return saveResult(result)
    })
    // NO .catch() HERE
    // Unhandled rejection: processItems failure silently swallowed
}

// Fix:
function processOrder(orderId) {
  return fetchOrder(orderId)
    .then(order => {
      if (!order.items.length) throw new Error('Empty order')
      return processItems(order.items)
    })
    .then(result => saveResult(result))
    .catch(error => {
      logger.error('Order processing failed', { orderId, error })
      throw error  // Re-throw to let caller handle
    })
}
```

### Failure 2 — Concurrent Mutation Without Coordination

```javascript
// Race condition: multiple promises mutating shared state
const cache = {}

async function getOrFetch(key) {
  if (cache[key]) return cache[key]
  
  // If two calls arrive before either completes:
  const data = await fetch(`/api/${key}`)  // Both start fetch
  cache[key] = await data.json()            // Both write cache
  return cache[key]
  // Result: two fetches for same key, race on cache write
}

// Fix: In-flight deduplication
const inflight = {}

async function getOrFetchSafe(key) {
  if (cache[key]) return cache[key]
  if (inflight[key]) return inflight[key] // Return same promise!
  
  inflight[key] = fetch(`/api/${key}`)
    .then(r => r.json())
    .then(data => {
      cache[key] = data
      delete inflight[key]
      return data
    })
    .catch(err => {
      delete inflight[key]
      throw err
    })
  
  return inflight[key]
}
```

### Debugging Promises

```javascript
// Track promise creation for debugging
const originalThen = Promise.prototype.then
Promise.prototype.then = function patchedThen(onFulfilled, onRejected) {
  const stack = new Error().stack
  return originalThen.call(this, onFulfilled, reason => {
    if (onRejected) return onRejected(reason)
    console.error('Unhandled in chain:', reason, '\nChain created at:', stack)
    throw reason
  })
}
// WARNING: Performance overhead — only in development

// Better: Use DevTools Promise debugging
// Chrome: DevTools → Sources → Pause on caught exceptions
// async_hooks in Node.js for async context tracking
```

---

## ⚠️ Edge Cases & Undefined Behaviors

### Promise.resolve with a Promise argument

```javascript
const p1 = Promise.resolve(42)
const p2 = Promise.resolve(p1)

p1 === p2  // TRUE — Promise.resolve(promise) returns the SAME promise
           // if it's a native Promise from the same realm

// But:
const p3 = new Promise(resolve => resolve(p1))
p3 === p1  // false — different promise object
// p3 "follows" p1: when p1 fulfills, p3 also fulfills with the same value
// Requires an extra microtask tick (PromiseResolveThenableJob)
```

### Synchronous vs Asynchronous Executor

```javascript
// Executor runs synchronously, but resolution SCHEDULES microtask
let resolveFunc
const p = new Promise(resolve => {
  resolveFunc = resolve
})

resolveFunc(42) // Resolve synchronously
// Promise is NOW fulfilled in [[PromiseState]]
// But .then() handlers run ASYNCHRONOUSLY (microtask)

p.then(v => console.log(v)) // Scheduled as microtask
console.log('sync after resolve')

// Output: 'sync after resolve', then 42
// Even though p was resolved before .then() was called,
// the handler still runs asynchronously
```

---

## 🏢 Industry Best Practices

1. **Always handle promise rejections** — Use `.catch()` at the chain end or `try/catch` with async/await. Set up `process.on('unhandledRejection')` as a safety net in Node.js.

2. **Use `Promise.allSettled` for fanout operations** — When launching multiple parallel operations where individual failures shouldn't abort others.

3. **Deduplicate in-flight requests** — Maintain an inflight Map keyed on request identity. Return the same Promise for identical concurrent requests.

4. **Avoid `new Promise()` wrapping** — If a function already returns a Promise, don't wrap it in `new Promise()`. Use `async/await` or chain directly.

5. **Limit concurrent Promises** — `Promise.all([...1000 fetches])` can overwhelm the server. Use a semaphore or batching to limit concurrency.

---

## ⚖️ Trade-offs

| Pattern | Benefit | Cost |
|---------|---------|------|
| `.then()` chains | Composable, lazy | Extra microtask per hop |
| `async/await` | Readable, debuggable | Transpiles to generator in older targets |
| `Promise.all` | Parallel execution | One rejection cancels all |
| `Promise.allSettled` | All results collected | Must check status per result |
| Custom cancellation | Control over in-flight work | Complex, no native support |

---

## 💼 Interview Questions (With Solutions)

**Q1: How many microtask ticks does `Promise.resolve(thenable).then(fn)` take?**

> Two ticks. First tick: `Promise.resolve(thenable)` schedules a `PromiseResolveThenableJob` to call `thenable.then(resolve, reject)` — this is a microtask. Second tick: once `thenable.then` calls `resolve`, the promise resolves and schedules `fn` as a `PromiseReactionJob`. Compare to `Promise.resolve(42).then(fn)` — only one tick since 42 is not a thenable.

**Q2: Why can't you cancel a Promise?**

> Promises represent already-initiated operations. The Promise itself is just a notification mechanism — the actual work (I/O, timers) is managed outside the Promise. Cancelling the notification doesn't stop the work. Additionally, the spec intentionally kept Promises simple — no cancellation logic means no cancellation propagation edge cases in chains. AbortController was introduced to handle HTTP request cancellation at the network level, and it can be threaded through promise-based APIs.

**Q3: What is the difference between `reject(new Error())` and `throw new Error()` inside a Promise executor?**

> In the executor, both have the same effect — the promise is rejected with the error. But `throw` in the executor is caught by the Promise constructor machinery and converted to a rejection. Outside an executor (in a `.then()` callback), `throw` propagates through the chain. The key difference: `throw` works in both sync and async contexts inside `.then()`; `reject()` is only available in the executor.

---

## 🧩 Practice Problems (With Solutions)

**Problem:** Implement `Promise.any` from scratch:

```javascript
function promiseAny(promises) {
  return new Promise((resolve, reject) => {
    if (!promises.length) {
      return reject(new AggregateError([], 'All promises were rejected'))
    }
    
    let rejectedCount = 0
    const errors = []
    
    promises.forEach((promise, index) => {
      Promise.resolve(promise).then(
        value => resolve(value),  // First fulfillment wins
        reason => {
          errors[index] = reason
          rejectedCount++
          if (rejectedCount === promises.length) {
            reject(new AggregateError(errors, 'All promises were rejected'))
          }
        }
      )
    })
  })
}

// Test:
promiseAny([Promise.reject(1), Promise.resolve(2), Promise.resolve(3)])
  .then(v => console.log(v)) // 2
  
promiseAny([Promise.reject('a'), Promise.reject('b')])
  .catch(e => console.log(e instanceof AggregateError, e.errors)) // true, ['a', 'b']
```

---

## 🔗 Navigation

**Prev:** [08_Event_Loop.md](08_Event_Loop.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [10_Async_Await.md](10_Async_Await.md)
