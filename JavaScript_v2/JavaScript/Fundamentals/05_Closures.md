# 📌 05 — Closures

## 🧠 Concept Explanation (Deep Technical Narrative)

A closure is a **function that retains a live reference to its enclosing lexical environment** — the Environment Records that existed at the time of the function's creation. The function carries these references (via its `[[Environment]]` internal slot) even after the enclosing function has returned and its stack frame has been destroyed.

The key insight: **closures are not a "feature" V8 added — they are a direct consequence of lexical scoping combined with first-class functions.** If functions can be passed around (first-class) and scoping is lexical, then the runtime must keep the lexical environment alive as long as any function references it. The heap-allocated Context object is the mechanism.

In V8's implementation:
- `[[Environment]]` in the spec maps to the `context` field of a `JSFunction` object
- The `context` field points to a `Context` object on the V8 heap
- The Context has a `previous` pointer forming a chain (the scope chain)
- The GC keeps a Context alive as long as any JSFunction references it

---

## 🔬 Internal Mechanics (Engine-Level — V8)

### Scope Analysis: Who Gets a Context Slot?

V8's scope analyzer makes per-variable decisions:

```
For each variable in a function:
  if captured_by_inner_function → heap-allocate in Context object
  else if function_has_no_eval  → stack-allocate in register file
  else → dynamic lookup (for eval-contaminated functions)
```

This decision is made statically (parse time). V8 cannot defer this decision — by the time a function runs, the bytecode is already generated with fixed slot assignments.

### V8 Context Object Layout

```
Context object (heap-allocated, managed by GC):
┌──────────────────────────────────┐
│  [0] Map (hidden class)          │
│  [1] Length                      │
│  [2] JSFunction (closure ref)    │  ← The function that owns this context
│  [3] previous Context (parent)   │  ← Scope chain link
│  [4] native_context              │  ← Realm's built-ins
│  [5..N] variable slots           │  ← Captured variables live here
└──────────────────────────────────┘
```

When multiple closures share the same enclosing scope, they ALL point to the SAME Context object. There is exactly ONE Context per scope level — not one per closure.

### What V8 Cannot Eliminate

V8's escape analysis in TurboFan can sometimes eliminate heap allocations (scalar replacement). But for closures, V8 currently **does not** eliminate Context object allocation when a closure might escape. The reasoning: if the closure is passed to unknown code, V8 conservatively assumes it could be called at any time — the Context must stay alive.

---

## 🔁 Execution Flow (Step-by-Step)

```javascript
function outer() {
  let count = 0                    // Line A
  const increment = () => ++count  // Line B — closure created
  const decrement = () => --count  // Line C — another closure created
  return { increment, decrement }  // Line D — closures escape
}

const obj = outer()                // outer's stack frame destroyed
obj.increment()                    // count lives on!
```

**Step-by-step V8 execution:**

```
1. outer() called:
   - V8 creates stack frame for outer
   - Scope analysis determined 'count' is captured → allocate Context slot
   - V8 emits: CreateBlockContext, LdaSmi 0, Star contextSlot[0]
   
2. Line A: count = 0
   - Stored in Context object slot, NOT on the stack
   
3. Line B: increment arrow function created
   - V8 emits: CreateClosure [bytecode_for_increment, context]
   - A new JSFunction object is allocated on heap
   - Its [[Environment]] (context field) points to outer's Context
   
4. Line C: Same as B for decrement
   - SAME Context object pointed to — NOT a copy!
   
5. Line D: { increment, decrement } object created and returned
   
6. outer() returns, stack frame destroyed
   - BUT: outer's Context object is still referenced by increment and decrement JSFunctions
   - GC CANNOT collect the Context
   - count (= 0) persists in heap
   
7. obj.increment():
   - V8 loads JSFunction (increment), loads its context
   - LdaContextSlot [0] → 0
   - Increment: 1
   - StaContextSlot [0] → 1
   - count in shared Context is now 1
   
8. obj.decrement():
   - Same Context, same slot
   - LdaContextSlot [0] → 1
   - Decrement: 0
```

---

## 🧠 Memory Behavior

```
GC Object Graph After outer() Returns:

  [Root: obj]
      │
  [JS Object: { increment, decrement }]
      │              │
      │         [JSFunction: decrement]
      │              │
  [JSFunction: increment]
      │              │
      └──────────────┘
               │ context field
               ▼
      [Context: { count: 0, prev: GlobalCtx }]
               │
               ▼
      [Context: GlobalContext]
               │
               ▼
      [NativeContext (Realm)]

GC retention chain:
obj → JSFunction → Context → (kept alive)
```

**Retained size vs Shallow size:**
- Shallow size of `increment` function: ~40-50 bytes (JSFunction fields only)
- **Retained size**: 40 + size of Context + all objects the Context references

This is why heap snapshots show closures with surprisingly large retained sizes — they drag along their entire scope chain.

---

## 📐 ASCII Diagram — Closure Memory Retention

```
BEFORE outer() returns:          AFTER outer() returns:

Stack:                           Stack:
┌─────────────┐                  ┌─────────────┐
│ outer frame │                  │ (destroyed) │
│  count→ctx  │                  └─────────────┘
└─────────────┘                  
      │                          Heap (still alive):
      ▼                          
Heap: Context                    ┌──────────────────────┐
┌───────────────┐                │ obj = {              │
│ count: 0      │◄───────────────│   increment: fn,     │
│ prev: global  │                │   decrement: fn      │
└───────────────┘                │ }                    │
                                 └──────────────────────┘
                                        │          │
                                        ▼          ▼
                                 [fn increment] [fn decrement]
                                        │          │
                                        └────┬─────┘
                                             ▼
                                      [Context: count=0]
                                 ← GC cannot collect this
```

---

## 🔍 Code Examples

### Example 1 — Module Pattern via Closure

```javascript
function createUserStore() {
  // Private state — heap-allocated in Context
  const users = new Map()
  let nextId = 0
  
  // These closures share ONE Context containing {users, nextId}
  return {
    addUser(name) {
      const id = ++nextId
      users.set(id, { id, name, createdAt: Date.now() })
      return id
    },
    getUser(id) {
      return users.get(id)
    },
    deleteUser(id) {
      return users.delete(id)
    },
    // DANGER: This exposes the internal Map reference
    // Callers can mutate users directly, bypassing the store's logic
    // Never expose internal data structures
    [Symbol.iterator]() {
      return users.values()
    }
  }
}
```

### Example 2 — Partial Application with Closure

```javascript
// Each call to curry creates a new JSFunction with its own Context
function curry(fn) {
  const arity = fn.length
  return function curried(...args) {
    if (args.length >= arity) {
      return fn(...args)
    }
    // New closure created — Context captures fn, arity, args
    return function(...moreArgs) {
      return curried(...args, ...moreArgs)
    }
  }
}

const add = curry((a, b, c) => a + b + c)
const add5 = add(5)     // Context: { fn, arity:3, args:[5] }
const add5and3 = add5(3) // Context: { fn, arity:3, args:[5,3] }
add5and3(1)              // 9 — calls fn(5, 3, 1)

// Memory: Each partial application creates:
// 1 JSFunction + 1 Context + 1 args array
// For deep currying chains this can add up — profile if used heavily
```

### Example 3 — Closure Over Loop Variable (let semantics)

```javascript
// Each for-let iteration creates a NEW binding
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0) // 0, 1, 2
}

// V8 implementation: At each iteration boundary, V8 creates a NEW
// block-level LexicalEnvironment and copies the current i value into it.
// Conceptually equivalent to:
{
  let i_0 = 0  // New Context per iteration
  setTimeout(() => console.log(i_0), 0)
}
{
  let i_1 = 1
  setTimeout(() => console.log(i_1), 0)
}
// etc.

// This is described in the spec (14.7.4.2 ForLoopEvaluation)
// V8 emits CreateBlockContext at each iteration for captured loop vars
```

### Example 4 — Closure Memory Leak (React)

```javascript
class Cache {
  static instance = null
  static getInstance() {
    if (!Cache.instance) Cache.instance = new Cache()
    return Cache.instance
  }
  
  constructor() {
    this.handlers = []
  }
  
  subscribe(fn) {
    // fn closes over the entire component scope
    this.handlers.push(fn)
    // No way to unsubscribe!
  }
}

// In React component:
function Component() {
  const [state, setState] = useState({ largeArray: new Array(10000).fill({}) })
  
  // This closure captures `state` (via setState closure in hook)
  // AND the entire component's scope chain
  Cache.getInstance().subscribe(() => {
    setState(prev => ({ ...prev, updated: true }))
  })
  
  // When component unmounts, handler is STILL in Cache.handlers
  // The closure holds a reference to:
  // - setState (which holds a reference to the fiber)
  // - state (the large array)
  // - The entire component's Context
  // LEAK: grows with every mount
}
```

---

## 💥 Production Failures & Debugging

### Debugging Closure Memory Leaks

```
Strategy 1: Chrome DevTools Heap Snapshot
1. DevTools → Memory → Heap Snapshot → Take Snapshot
2. Take snapshot again after multiple navigations  
3. Click "Comparison" view
4. Sort by "# Delta" (net new objects)
5. Look for: (closure), Context, JSFunction with large retained sizes
6. Click a closure → see "Retainers" pane → trace why it's kept alive

Strategy 2: DevTools Memory Allocation Timeline
1. DevTools → Memory → Allocation Instrumentation on Timeline
2. Record the suspected memory-leaking action
3. Look for blue bars that don't turn gray (gray = collected, blue = retained)
4. Click retained allocations → "Allocation Stack" shows where created

Strategy 3: Node.js Heap Dump
```
```bash
node --heap-prof app.js  # Creates heap profile
# OR
node -e "
const v8 = require('v8')
const stream = v8.writeHeapSnapshot()
console.log('Written to', stream)
"
```

### WeakRef + FinalizationRegistry for Optional Closure Retention

```javascript
// Pattern for closures that shouldn't prevent GC
const cache = new Map()

function expensiveOperation(input) {
  const key = JSON.stringify(input)
  const cached = cache.get(key)
  if (cached) {
    const value = cached.deref()
    if (value !== undefined) return value
  }
  
  const result = /* expensive computation */{}
  // WeakRef allows GC to collect `result` if memory pressure is high
  cache.set(key, new WeakRef(result))
  
  // FinalizationRegistry cleans up the cache entry after GC
  const registry = new FinalizationRegistry(key => cache.delete(key))
  registry.register(result, key)
  
  return result
}
```

---

## ⚠️ Edge Cases & Undefined Behaviors

### Closure Over `arguments`

```javascript
function outer() {
  const args = arguments // Capture arguments object
  return function inner() {
    // 'arguments' here is INNER's arguments, not outer's!
    // To access outer's arguments, must use the captured 'args' variable
    console.log(arguments) // inner's args
    console.log(args)      // outer's args
  }
}

// Arrow functions do NOT have their own 'arguments'
function outer2() {
  const inner = () => {
    console.log(arguments) // outer2's arguments (lexical)
  }
  inner('ignored')  // 'ignored' is NOT in arguments here
}
```

### Closure and Prototype Chain Interaction

```javascript
function createClass() {
  let privateState = 0  // Captured in Context
  
  // Method on prototype — shared across instances
  // But it closes over the SAME privateState for all instances!
  function MyClass() {}
  MyClass.prototype.increment = function() { return ++privateState }
  
  return MyClass
}

const C = createClass()
const c1 = new C()
const c2 = new C()
c1.increment() // 1
c2.increment() // 2 — they SHARE privateState!
// This is a bug — private state is per-class not per-instance
```

---

## 🏢 Industry Best Practices

1. **Capture minimal scope** — Destructure only what the closure needs: `const { id, name } = user` instead of capturing the whole `user` object.

2. **Always provide cleanup for event listeners, subscriptions** — Any callback registered as a listener or subscriber must have a corresponding removal mechanism. React's `useEffect` cleanup function is the standard pattern.

3. **WeakMap for closures over DOM nodes** — If you need to associate closure-based state with DOM elements, use `WeakMap<DOMNode, State>` — allows GC when the DOM element is removed.

4. **Use DevTools Allocation Timeline** in development to detect growing retained closures before they reach production.

5. **Profile closure creation count** in tight loops — Creating closures inside hot loops generates GC pressure. Pre-allocate or use class methods instead.

---

## ⚖️ Trade-offs

| Design | Benefit | Cost |
|--------|---------|------|
| Heap-allocated Context for captures | Enables closures | GC, cache-miss risk |
| Shared Context across sibling closures | Memory efficiency | Shared mutation can surprise |
| `let` in for-loop creates new Context per iteration | Correct closure semantics | More Context allocations |
| WeakRef for closure-held objects | Optional GC retention | Non-deterministic lifetime |
| Class private fields (#) vs closures | Native encapsulation | Private fields require class syntax |

---

## 💼 Interview Questions (With Solutions)

**Q1: What is the memory cost of a closure in V8?**

> Direct cost: 1 JSFunction object (~50 bytes) + 1 Context object (size proportional to number of captured variables, ~40 + 8 bytes per slot). Indirect cost: the entire retained size — all objects referenced by captured variables are kept alive. A closure capturing a 10MB cache keeps that 10MB alive. This is why retained size (shown in heap snapshots) is more important than shallow size for closures.

**Q2: Do arrow functions create closures?**

> Yes. Arrow functions capture `this`, `arguments`, and all outer-scope variables through the same Context mechanism as regular functions. The difference is that arrow functions do NOT create their own `this` binding, `arguments` object, or `prototype`. Their `[[Environment]]` still points to the enclosing scope's Context — they close over outer variables in exactly the same way.

**Q3: How does React's `useCallback` relate to closure mechanics?**

> `useCallback(fn, [deps])` memoizes the function reference. Without it, every render creates a NEW JSFunction pointing to a NEW closure over the current render's scope. With it, the same JSFunction (and Context) is reused across renders until a dependency changes. The benefit: stable function references for `memo`-wrapped children, preventing unnecessary re-renders. The cost: the previous render's Context is retained in memory longer (until the dependency changes).

---

## 🧩 Practice Problems (With Solutions)

**Problem:** Implement `memoize` — a function that caches results of expensive computations:

```javascript
function memoize(fn) {
  // Your implementation here
}

const expensiveFn = memoize((n) => {
  // expensive computation
  return n * n
})
```

**Solution:**

```javascript
function memoize(fn) {
  const cache = new Map() // Captured in closure — persists across calls
  
  return function memoized(...args) {
    // Cache key — works for primitive args
    // For objects, use a serialization strategy
    const key = JSON.stringify(args)
    
    if (cache.has(key)) {
      return cache.get(key)
    }
    
    const result = fn.apply(this, args)
    cache.set(key, result)
    return result
  }
}

// Production-grade version with WeakMap for object args:
function memoizeAdvanced(fn) {
  const primitiveCache = new Map()
  const objectCache = new WeakMap()
  
  return function memoized(arg) {
    if (arg !== null && typeof arg === 'object') {
      if (objectCache.has(arg)) return objectCache.get(arg)
      const result = fn.call(this, arg)
      objectCache.set(arg, result)  // WeakMap → GC-friendly
      return result
    }
    
    if (primitiveCache.has(arg)) return primitiveCache.get(arg)
    const result = fn.call(this, arg)
    primitiveCache.set(arg, result)
    return result
  }
}

// Analysis: memoize closure retains:
// - fn (reference to original function)
// - cache (Map — grows unboundedly for unique args!)
// Production concern: cache must have eviction strategy (LRU, TTL)
// or it will cause memory leaks for functions called with many unique args
```

---

## 🔗 Navigation

**Prev:** [04_Scope_and_Lexical_Environment.md](04_Scope_and_Lexical_Environment.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [06_This_Keyword.md](06_This_Keyword.md)
