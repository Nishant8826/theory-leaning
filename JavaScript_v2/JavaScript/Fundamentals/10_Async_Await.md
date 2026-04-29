# 📌 10 — Async/Await

## 🧠 Concept Explanation (Deep Technical Narrative)

`async/await` is **syntactic sugar over generators and promises**, implemented by V8 at the bytecode level rather than being transpiled to generators at the JavaScript level. An `async function` is fundamentally a function that returns a Promise and can be suspended at `await` points, with the suspension and resumption orchestrated by the microtask queue.

The spec describes `async functions` using the `AsyncFunctionStart` abstract operation and represents suspension via an **AsyncContext** (not the same as a scope context). When an `await` is encountered, V8 suspends the current bytecode execution, saves the current register state (effectively the async function's "local variables") into a heap-allocated **JSPromise** and registers a microtask to resume when the awaited promise settles.

**Key insight:** Each `await` creates exactly one microtask checkpoint. The async function body between two consecutive `await` expressions runs synchronously (as a single task/microtask unit) — only `await` introduces asynchronous gaps.

---

## 🔬 Internal Mechanics (Engine-Level — V8)

### The V8 Async Function Implementation

V8 compiles async functions to use a **continuation-passing style** internally. The bytecode for an async function includes:

```
SuspendGenerator [register_file_snapshot]
ResumeGenerator [restore_register_file]
```

These instructions save/restore the entire register file to/from the heap-allocated **JSGeneratorObject** (for async functions, it's technically an async generator object). The suspension stores:
- All live local variables (register file)
- Current bytecode offset (where to resume)
- The context (scope chain)

### `await` Desugaring

```javascript
async function fetchUser(id) {
  const user = await getUser(id)
  return user.name
}
```

V8 conceptually transforms this to:

```javascript
function fetchUser(id) {
  const __result_promise = new Promise((resolve, reject) => {
    // PromiseReactionJob scheduled when getUser(id) settles
    getUser(id).then(
      (__resumed_value) => {
        // This is the "resumption" — runs as a microtask
        try {
          const user = __resumed_value
          resolve(user.name) // Resolves the outer promise
        } catch(e) {
          reject(e)
        }
      },
      reject  // If getUser rejects, propagate
    )
  })
  return __result_promise
}
```

**V8 Optimization (zero-cost `await` for native Promises):**

In V8 7.2+ (Node.js 12+), when `await`ing a **native Promise** (not a thenable), V8 optimizes the path to avoid creating intermediate `PromiseResolveThenableJob`. The reaction is directly scheduled, reducing latency from 2 microtask ticks to 1 tick per `await`.

This was a contentious optimization that required a spec change. The "extra tick" was observable behavior that some code relied on — fixing it broke compatibility temporarily.

---

## 🔁 Execution Flow (Step-by-Step)

```javascript
async function outer() {
  console.log('A')
  const result = await inner()
  console.log('C:', result)
  return result
}

async function inner() {
  console.log('B')
  return 42
}

outer().then(() => console.log('D'))
console.log('E')
```

**Detailed trace:**

```
SYNC:
  outer() called:
    → JSPromise for outer created
    → 'A' logged
    → inner() called (synchronously):
        → JSPromise for inner created
        → 'B' logged
        → `return 42` → resolves inner's promise
        → schedules PromiseReactionJob for outer's await (microtask)
    → outer() SUSPENDS at `await inner()`
    → returns outer's (still pending) JSPromise
  .then(() => 'D') → registers reaction on outer's promise
  'E' logged

MICROTASK 1:
  PromiseReactionJob resumes outer() at the `await` point:
    → result = 42
    → 'C: 42' logged
    → `return result` → resolves outer's promise with 42
    → schedules PromiseReactionJob for .then(() => 'D')

MICROTASK 2:
  PromiseReactionJob runs .then(() => 'D'):
    → 'D' logged

Output: A, B, E, C: 42, D
```

---

## 🧠 Memory Behavior

```
During async function suspension:

Stack (when outer() is suspended at await):
┌───────────────────────────────────┐
│  (empty — async fn not on stack)  │
└───────────────────────────────────┘

Heap (live objects):
┌─────────────────────────────────────────────────────┐
│  JSAsyncFunctionObject (outer's state)              │
│  - bytecode_offset: [at await point]                │
│  - register_file_snapshot: { id, result=pending }  │
│  - context: outer's scope chain                     │
└─────────────────────────────────────────────────────┘
          │ referenced by
┌─────────────────────────────────────────────────────┐
│  JSPromise (outer's return value)                   │
│  - [[PromiseState]]: kPending                       │
│  - [[PromiseFulfillReactions]]: [.then(() => 'D')]  │
└─────────────────────────────────────────────────────┘

Memory leak risk: If outer's promise is held alive (e.g., in a Set),
the entire JSAsyncFunctionObject (with all captured locals) stays alive
even after the async function would naturally have completed.
```

---

## 📐 ASCII Diagram — Async Function Lifecycle

```
async function foo() {
                    
START: foo() called
       │
       ▼
  [RUNNING on call stack]
  code before first `await`
       │
       ▼ await somePromise
       
  SUSPEND: save registers to JSAsyncFunctionObject
           register reaction on somePromise
           return pending JSPromise
       │
       │ ← call stack now empty (event loop runs)
       │
       ▼ somePromise settles → PromiseReactionJob scheduled
       
  RESUME: PromiseReactionJob runs
          restore registers from JSAsyncFunctionObject
          [RUNNING on call stack again — as a microtask]
          code after `await`
       │
       ▼ (another await OR return)
       
  COMPLETE: resolve/reject outer JSPromise
            JSAsyncFunctionObject eligible for GC
```

---

## 🔍 Code Examples

### Example 1 — Error Handling Mechanics

```javascript
async function fetchWithRetry(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      return await response.json()
    } catch (error) {
      if (i === retries - 1) throw error // Last retry — propagate
      await sleep(1000 * Math.pow(2, i))  // Exponential backoff
    }
  }
}

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

// Key behavior: Each `await` is a potential rejection point
// `await fetch(url)` throws if network error
// `await response.json()` throws if body is malformed JSON
// The try/catch block catches ALL of these — any await can throw
```

### Example 2 — Sequential vs Concurrent Awaits

```javascript
// SEQUENTIAL: each await waits for completion before starting next
// Total time: t1 + t2 + t3
async function sequential(ids) {
  const results = []
  for (const id of ids) {
    results.push(await fetchItem(id))  // One at a time
  }
  return results
}

// CONCURRENT: all started simultaneously, awaited at end
// Total time: max(t1, t2, t3)
async function concurrent(ids) {
  const promises = ids.map(id => fetchItem(id))  // All start NOW
  return Promise.all(promises)                   // Wait for all
}

// BOUNDED CONCURRENCY: max N in-flight at once
async function bounded(ids, limit = 3) {
  const results = []
  const queue = [...ids]
  
  async function worker() {
    while (queue.length) {
      const id = queue.shift()
      results.push(await fetchItem(id))
    }
  }
  
  await Promise.all(Array.from({ length: limit }, worker))
  return results
}
```

### Example 3 — Async Generators (Streaming Pattern)

```javascript
async function* paginate(url) {
  let page = 1
  while (true) {
    const response = await fetch(`${url}?page=${page}`)
    const data = await response.json()
    
    if (!data.items.length) break
    
    yield* data.items  // Yield each item from the page
    
    if (!data.hasNextPage) break
    page++
  }
}

// Consumer: uses `for await...of`
async function processAll(url) {
  for await (const item of paginate(url)) {
    await processItem(item)
    // Each item processed sequentially, pages fetched on demand
  }
}

// V8 internals: `yield` in async generator suspends AND yields a value
// The async generator has TWO state machines: the async (microtask-based)
// AND the generator (value-yielding) aspects combined
```

### Example 4 — Async Stack Traces

```javascript
// V8 7.3+ (Node 12+): --async-stack-traces enabled by default
// Without: Error thrown in deep async chain only shows current microtask
// With: Shows full async causation chain

async function level3() {
  throw new Error('deep error')
}

async function level2() {
  await level3()
}

async function level1() {
  await level2()
}

// With async stack traces:
level1().catch(e => console.log(e.stack))
// Error: deep error
//     at level3 (app.js:2)
//     at async level2 (app.js:6)    ← async stack trace!
//     at async level1 (app.js:10)   ← and this one!

// Implementation: V8 stores the async continuation stack in the JSPromise
// and reconstructs it when building Error.stack
// Cost: ~20% memory overhead per JSPromise (stores stack frame references)
// Trade-off: Disable in performance-critical code via --no-async-stack-traces
```

---

## 💥 Production Failures & Debugging

### Failure 1 — Async Function Not Awaited

```javascript
// Classic production bug: forgetting await inside async function
async function saveUser(userData) {
  db.transaction(async (trx) => {  // ← NOT awaited!
    await trx.insert('users', userData)
    await trx.insert('audit_log', { action: 'create', userId: userData.id })
  })
  // saveUser resolves IMMEDIATELY — transaction may not have run yet!
  // Error: transaction may be committed without all inserts
}

// Fix:
async function saveUser(userData) {
  await db.transaction(async (trx) => {  // ← await!
    await trx.insert('users', userData)
    await trx.insert('audit_log', { action: 'create', userId: userData.id })
  })
}

// ESLint rule: @typescript-eslint/no-floating-promises
// Catches unawaited async function calls at lint time
```

### Failure 2 — Unintentional Sequential Execution

```javascript
// Performance regression: appears parallel but is sequential
async function loadDashboard(userId) {
  const profile = await fetchProfile(userId)   // Wait...
  const settings = await fetchSettings(userId) // Then wait...
  const notifications = await fetchNotifications(userId) // Then wait...
  // Total: ~900ms (300ms each)
  return { profile, settings, notifications }
}

// Fix — truly parallel:
async function loadDashboard(userId) {
  const [profile, settings, notifications] = await Promise.all([
    fetchProfile(userId),
    fetchSettings(userId),
    fetchNotifications(userId)
  ])
  // Total: ~300ms (parallel)
  return { profile, settings, notifications }
}
```

### Debugging Async Functions

```javascript
// Node.js async hooks for tracking async context
const async_hooks = require('async_hooks')

const hooks = async_hooks.createHook({
  init(asyncId, type, triggerAsyncId) {
    if (type === 'PROMISE') {
      console.log(`Promise ${asyncId} created by ${triggerAsyncId}`)
    }
  },
  resolve(asyncId) {
    console.log(`Promise ${asyncId} resolved`)
  }
})
hooks.enable()

// Shows the async causation chain for every promise
// Use async_hooks + AsyncLocalStorage for request context propagation in Node.js
```

---

## ⚠️ Edge Cases & Undefined Behaviors

### `await` on Non-Promise Values

```javascript
async function test() {
  const x = await 42          // Wraps in Promise.resolve(42)
  const y = await null        // Promise.resolve(null)
  const z = await undefined   // Promise.resolve(undefined)
  
  // All schedule exactly 1 microtask tick
  // Same as: await Promise.resolve(value)
}

// await on a thenable — extra tick!
const thenable = { then(resolve) { resolve(99) } }
async function thenableTest() {
  const x = await thenable  // 2 microtask ticks (PromiseResolveThenableJob + resume)
}
```

### Returning a Promise from Async Function

```javascript
async function example() {
  return Promise.resolve(42)
  // Is the return value resolved by the function?
}

const p = example()
// p is a Promise<number>
// The returned Promise.resolve(42) causes an extra microtask tick
// (because async functions call PromiseResolveThenableJob on returned promises)

// Compare with:
async function example2() {
  return 42  // Direct value — no extra tick
}
```

### Top-Level Await (ESM Only)

```javascript
// Only valid in ESM modules (type="module" in browser, .mjs in Node)
const data = await fetch('/api').then(r => r.json())
// Module evaluation is async — dependent modules wait for this to complete
// V8 implements this via module graph async evaluation
// Can cause circular dependency deadlocks if two modules await each other
```

---

## 🏢 Industry Best Practices

1. **`await` in parallel, not in series** — Use `Promise.all` for independent operations. Sequential awaits are a common performance antipattern.

2. **Always handle rejection** — Either `try/catch` around `await`, or `.catch()` on the async function's returned promise. ESLint: `@typescript-eslint/no-floating-promises`.

3. **Use `await` for cleanup in finally** — `async function` with `try/finally` properly handles async cleanup: `finally { await cleanup() }`.

4. **Be careful with `await` in loops** — `for...of` with `await` = sequential. Use `Promise.all(array.map(...))` for parallel.

5. **Enable async stack traces** in production (default in Node.js 12+). The memory overhead is worth the debuggability. Use `--no-async-stack-traces` only if profiled to be a bottleneck.

---

## ⚖️ Trade-offs

| Approach | Benefit | Cost |
|----------|---------|------|
| `async/await` | Readable, debuggable | Extra microtask per `await` vs raw promises |
| Promise chains | Lower overhead | Harder to read, error handling verbose |
| Sequential `await` | Simple ordering | Performance: no parallelism |
| `Promise.all` | Max parallelism | One rejection cancels all |
| Async generators | Streaming large datasets | Complex state machine |
| Top-level await | Simple module initialization | Can block module graph |

---

## 💼 Interview Questions (With Solutions)

**Q1: How many microtask ticks does a single `await` cost?**

> With V8's optimization for native promises (V8 7.2+, Node.js 12+): **1 tick**. The awaited promise's reaction is directly scheduled without an intermediate `PromiseResolveThenableJob`. For thenables (non-native): **2 ticks**. Without the optimization (older V8): always 2 ticks. This was actually a breaking change in V8 that required a spec amendment because the observable tick count changed.

**Q2: What's the difference between `async function foo() { return bar() }` and `async function foo() { return await bar() }`?**

> Both ultimately return a promise. The difference is in the async stack trace and error handling. Without `await`: if `bar()` returns a promise that rejects, the rejection bypasses `foo`'s context — foo's name won't appear in the stack trace. With `await`: the rejection is observed inside `foo`, so `foo` appears in the stack trace. Also, with `return await bar()`, a `try/catch` in `foo` can catch the rejection. With `return bar()` (no await), a try/catch in `foo` cannot catch the rejection.

**Q3: Why does V8 store the async function's register file on the heap during suspension?**

> Because when an async function is suspended at `await`, its call stack frame is destroyed — the function returns to the event loop. But the function needs to resume later with its local variable state intact. V8 heap-allocates a `JSGeneratorObject` (the mechanism underlying async functions) that contains a snapshot of the register file. When the awaited promise settles and the continuation microtask runs, V8 restores the register file from the heap object, allowing the function to continue as if it never stopped.

---

## 🧩 Practice Problems (With Solutions)

**Problem:** Implement an `asyncPool` function that limits concurrency:

```javascript
async function asyncPool(concurrency, iterable, iteratorFn) {
  const results = []
  const executing = new Set()
  
  for (const item of iterable) {
    // Create promise for this item
    const promise = Promise.resolve(item).then(value => iteratorFn(value))
    results.push(promise)
    
    // Track executing promises
    executing.add(promise)
    const cleanup = () => executing.delete(promise)
    promise.then(cleanup, cleanup)
    
    // If at concurrency limit, wait for one to complete
    if (executing.size >= concurrency) {
      await Promise.race(executing)
    }
  }
  
  return Promise.all(results)
}

// Usage:
const urls = ['url1', 'url2', 'url3', 'url4', 'url5']
const results = await asyncPool(2, urls, async (url) => {
  const response = await fetch(url)
  return response.json()
})
// At most 2 fetches in flight at any time
// Fetches url1+url2, then as each completes, starts url3, url4, url5
```

---

## 🔗 Navigation

**Prev:** [09_Promises.md](09_Promises.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [11_Microtasks_vs_Macrotasks.md](11_Microtasks_vs_Macrotasks.md)
