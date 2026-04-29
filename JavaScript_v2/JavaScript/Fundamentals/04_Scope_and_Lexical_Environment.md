# 📌 04 — Scope & Lexical Environment

## 🧠 Concept Explanation (Deep Technical Narrative)

The **Lexical Environment** is the ECMAScript specification's formal data structure for scope. It consists of two components:

1. **Environment Record** — A table mapping identifier names to their values and metadata (initialized/uninitialized, mutable/immutable)
2. **Outer reference** — A pointer to the enclosing LexicalEnvironment, forming the scope chain

"Lexical" means *determined at write time* — the scope chain is fixed by the source code structure, not by runtime call patterns. This is the defining property that makes JavaScript's scoping predictable and optimizable.

There are several Environment Record types, each with specific behaviors:
- **DeclarativeEnvironmentRecord** — `let`, `const`, `function`, `class` in function/block scopes
- **ObjectEnvironmentRecord** — `with` statements; uses an actual JS object as the record
- **GlobalEnvironmentRecord** — Composite: outer ObjectEnvironmentRecord (window/global) + inner DeclarativeEnvironmentRecord
- **FunctionEnvironmentRecord** — Extends Declarative; adds `this`, `super`, `arguments`
- **ModuleEnvironmentRecord** — Like Declarative but supports live bindings (ESM imports)

---

## 🔬 Internal Mechanics (Engine-Level — V8)

### Scope Resolution at the IC Level

V8's Ignition bytecode includes two main variable access patterns:

**1. Stack/register access (uncontested locals):**
```
LdaImmutableCurrentContextSlot [slot_index]
```
Direct indexed access into the Context object — O(1), similar to array access.

**2. Context chain walk (outer scope variables):**
```
LdaContextSlot [context_depth, slot_index]
```
V8 computes at compile time how many `outer_` pointer hops are needed and emits the depth as a constant. This is NOT a dynamic walk at runtime — it's a known offset.

**3. Global access:**
```
LdaGlobal [name_index]
LdaGlobalInsideTypeof [name_index]
```
V8 uses an inline cache (IC) for global property lookups — it caches the offset in the global object's hidden class.

### V8 Scope Analysis Output

When V8's parser analyzes scope, each variable gets assigned:
- `IsContextAllocated()` — goes in heap Context (captured by closure)
- `IsStackAllocated()` — goes in stack register (fast)
- `IsGlobalSlot()` — global scope, IC lookup
- `IsLookupSlot()` — dynamic lookup (eval/with present — slow!)

```bash
# Visualize V8's scope analysis:
node --print-scopes script.js
# Shows the scope tree with each variable's allocation decision
```

### Block Scopes and Scope Objects

For block-level scopes (`if`, `for`, `{}`), V8 creates a new Environment Record but does NOT always create a new Context object. If the block's variables are not captured by closures, V8 allocates them in the parent function's register file — no heap allocation needed.

Only when a block variable is captured does V8 create a `BlockContext` — a heap-allocated Context object with the captured slots.

---

## 🔁 Execution Flow (Step-by-Step)

```javascript
const globalConst = 'global'

function outer(param) {
  let outerLet = 'outer'
  
  {
    const blockConst = 'block'
    
    function inner() {
      console.log(globalConst, outerLet, blockConst)
    }
    
    inner()
  }
}

outer('test')
```

**Scope chain at `inner()` call time:**

```
inner's FunctionEnvironmentRecord {
  this: undefined (strict) / global (sloppy)
  arguments: []
  outer → outer's DeclarativeEnvironmentRecord {
    param: 'test'
    outerLet: 'outer'
    outer → block's DeclarativeEnvironmentRecord {
      blockConst: 'block'
      outer → GlobalEnvironmentRecord {
        globalConst: 'global'
        outer → null
      }
    }
  }
}
```

**Variable resolution for `blockConst`:**
1. Check inner's FunctionEnvironmentRecord → not found
2. Walk `outer` pointer → outer's record → not found
3. Walk `outer` pointer → block's record → **found: 'block'**

V8 knows this at compile time: `LdaContextSlot [depth=2, slot=0]`

---

## 🧠 Memory Behavior

```
HEAP allocations (V8 Context objects):
                          
GlobalEnvironmentRecord ──────────── (always heap, shared by all code)
         │
BlockContext { blockConst } ───────── (heap ONLY if inner captures it)
         │                            (stack register if not captured)
FunctionContext { param, outerLet } ─ (heap because inner captures outerLet)
         │
inner's own context ──────────────── (minimal if inner captures nothing itself)
```

**Key optimization:** If `inner` didn't close over any outer variables, V8 wouldn't create Context objects for outer scopes — all locals would be stack-allocated registers. The **decision is made per-variable**, not per-function.

---

## 📐 ASCII Diagram — Scope Chain

```
┌──────────────────────────────────────────────────────────────┐
│  GlobalEnvRecord                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  ObjectEnvRecord (window/global)                      │    │
│  │  - window, document, fetch, ...                       │    │
│  └──────────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  DeclarativeEnvRecord                                 │    │
│  │  - globalConst: 'global'                              │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
         ▲ outer
┌──────────────────────────────────────────────────────────────┐
│  FunctionEnvRecord (outer)                                    │
│  - param: 'test'                                              │
│  - outerLet: 'outer'                        [heap Context]    │
└──────────────────────────────────────────────────────────────┘
         ▲ outer
┌──────────────────────────────────────────────────────────────┐
│  BlockEnvRecord ({} block)                                    │
│  - blockConst: 'block'                      [heap Context]    │
└──────────────────────────────────────────────────────────────┘
         ▲ outer
┌──────────────────────────────────────────────────────────────┐
│  FunctionEnvRecord (inner)                                    │
│  - [no own variables]                                         │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔍 Code Examples

### Example 1 — IIFE for Scope Isolation (Pre-ES6 Pattern)

```javascript
// Classic module pattern using IIFE to create a scope boundary
const counter = (function() {
  let count = 0  // Private to this IIFE scope
  
  return {
    increment() { return ++count },
    decrement() { return --count },
    reset() { count = 0 }
  }
})()

// WHY IIFEs: Before let/const, var always leaked to function scope.
// IIFE creates a FunctionEnvironmentRecord boundary.
// Modern code uses blocks with let/const or ESM for the same isolation.
```

### Example 2 — Dynamic Lookup Cost with eval

```javascript
function withEval(x) {
  eval('var dynamic = x * 2') // Modifies VE at runtime
  return dynamic
}

// V8 marks withEval as having eval:
// - All variable accesses use LdaLookupSlot (runtime lookup) instead of
//   LdaContextSlot (compile-time indexed access)
// - This is 5-10x slower per access
// - V8 cannot inline this function into callers
// - TurboFan refuses to optimize it

// Node.js performance test shows:
// Normal function with x: ~50M ops/sec
// Same function with unused eval: ~5M ops/sec
// The mere presence of eval degrades ALL variables, not just dynamic ones
```

### Example 3 — Module Environment Record (ESM Live Bindings)

```javascript
// counter.js (ESM)
export let count = 0
export function increment() { count++ }

// main.js
import { count, increment } from './counter.js'
console.log(count) // 0
increment()
increment()
console.log(count) // 2 — live binding! count is NOT a copy

// WHY: ESM imports are live bindings into the exporting module's
// ModuleEnvironmentRecord. You're reading the actual slot, not a copy.
// CJS: const { count } = require('./counter') → copy, always 0
// ESM: import { count } → live reference into exporting module's env record

// This enables:
// - Tree-shaking (live bindings mean unused exports can be elided)
// - Circular dep resolution (bindings exist before values are set)
// - But also: you CANNOT reassign an import:
// count = 5 // TypeError: Assignment to constant variable
```

### Example 4 — Scope Chain Walk Performance

```javascript
// Variable resolution cost increases with scope chain depth
const global = 0

function depth1() {
  const d1 = 1
  function depth2() {
    const d2 = 2
    function depth3() {
      const d3 = 3
      function depth4() {
        // Accessing global requires walking 4 scope chain links
        // V8 emits: LdaContextSlot [depth=4, slot=0]
        // Each link is a pointer dereference (potential cache miss)
        return global + d1 + d2 + d3
      }
      return depth4
    }
    return depth3
  }
  return depth2
}

// Performance implication: HOT code should capture frequently-used
// outer-scope variables into local variables:
function optimized() {
  const g = global // Local reference — depth=0, fastest access
  // ... use g instead of global in tight loops
}
```

---

## 💥 Production Failures & Debugging

### Failure 1 — `with` Statement Scope Poisoning

```javascript
// Legacy codebases (template engines, old libraries) sometimes use `with`
function renderTemplate(data) {
  with (data) {
    // All variable lookups now check data first
    return `Hello ${name}, you have ${messages.length} messages`
    // But: what if data = { constructor: null, hasOwnProperty: null }?
    // The `with` injects an ObjectEnvironmentRecord at the FRONT of the chain
    // Prototype chain of `data` is also searched!
    // data.__proto__.name would be found if data.name doesn't exist
  }
}

// Production bug: Template injection via prototype pollution:
// Object.prototype.name = 'HACKED'
// renderTemplate({}) → "Hello HACKED, ..."
```

### Failure 2 — Closure Scope Leak in React (useEffect)

```javascript
function Component({ userId }) {
  const [data, setData] = useState(null)
  
  useEffect(() => {
    // This closure captures userId from the FunctionEnvRecord of Component
    // If userId changes and the effect re-runs, a NEW closure is created
    // But the OLD fetch may still be in flight with the OLD userId!
    fetch(`/api/user/${userId}`)
      .then(res => res.json())
      .then(data => setData(data)) // Could set stale data
  }, [userId])
}

// Fix: Use AbortController + cleanup
useEffect(() => {
  const controller = new AbortController()
  fetch(`/api/user/${userId}`, { signal: controller.signal })
    .then(res => res.json())
    .then(data => setData(data))
    .catch(err => { if (err.name !== 'AbortError') throw err })
  return () => controller.abort() // Cleanup cancels previous request
}, [userId])
```

---

## ⚠️ Edge Cases & Undefined Behaviors

### Scope of catch Binding

```javascript
try {
  throw new Error('test')
} catch (e) {
  // 'e' exists only in catch block — DeclarativeEnvironmentRecord
  var inCatch = true  // 'var' goes to function/global scope (escapes catch!)
}
console.log(typeof e)       // "undefined" — catch binding is scoped
console.log(inCatch)        // true — var escaped

// ES2019: Optional catch binding
try {
  mightThrow()
} catch {
  // No binding created at all — no catch variable
}
```

### Named Function Expression Scope

```javascript
const outer = function inner() {
  // 'inner' is in scope here — bound in a special scope wrapping the function
  // 'outer' is NOT in scope here (it's in the outer environment)
  typeof inner // "function"
  typeof outer // depends on outer scope
  
  inner.name  // "inner"
}

outer.name   // "inner"
typeof inner // "undefined" — inner is NOT in outer scope
```

---

## 🏢 Industry Best Practices

1. **Never use `with`** — It makes all variable access in the block dynamic, destroys IC effectiveness, and is forbidden in strict mode for exactly these reasons.

2. **Minimize scope chain depth for hot paths** — Deep closure chains have chain-walking cost. Cache outer-scope variables in locals for tight loops.

3. **Use ESM live bindings deliberately** — In library code, exported mutable bindings (like a `version` counter) are live. Make sure consumers understand the binding is live, not a snapshot.

4. **Avoid `eval` in any function on a hot path** — Its presence disables optimization for the entire containing function, even if `eval` is never actually called.

5. **Structure scopes to minimize captured variables** — Capture only what closures need. Use parameter passing instead of outer-scope capture for better GC and V8 optimization.

---

## ⚖️ Trade-offs

| Mechanism | Benefit | Cost |
|-----------|---------|------|
| Lexical scoping | Predictable, optimizable | Less flexible than dynamic scoping |
| Context objects for captures | Enables closures | Heap allocation, GC pressure |
| Stack allocation for locals | Near-zero overhead | Destroyed on function return |
| ESM live bindings | Circular deps, tree-shaking | Cannot reassign import |
| eval/with dynamic lookup | Runtime dynamism | Disables all static optimizations |

---

## 💼 Interview Questions (With Solutions)

**Q1: What is the difference between scope and closure?**

> Scope is the static mapping of identifier names to environment records — it's determined at parse time. A closure is a *function* paired with its captured environment (the enclosing environment records at the time of function creation). The scope defines which environments a function can access; the closure is the runtime pairing of the function with those environments when the function is created.

**Q2: Why does ESM use live bindings instead of value copies?**

> Live bindings enable: (1) circular dependency resolution — two modules can import each other; the binding slot exists even before the exporting module's initialization runs, so by the time the imported value is actually *used*, it's initialized; (2) tree-shaking — bundlers can statically analyze which exports are consumed; (3) singleton-like behavior for shared state. Value copies would break circular deps and prevent mutable shared state from propagating.

**Q3: Explain how V8 avoids runtime scope chain walking for most variable accesses.**

> V8's scope analyzer determines at parse time exactly which Environment Record (at what chain depth) each variable lives in. It emits `LdaContextSlot [depth, slot]` — a compile-time constant lookup. There is no runtime name-based search; it's a direct indexed access at a known depth. The only exceptions are `eval`/`with` (where the chain is dynamic) and true global lookups (which use ICs, not chain walking).

---

## 🧩 Practice Problems (With Solutions)

**Problem:** Explain why this logs different values:

```javascript
function makeAdder(x) {
  return function(y) { return x + y }
}
const add5 = makeAdder(5)
const add10 = makeAdder(10)
console.log(add5(3))   // ?
console.log(add10(3))  // ?
console.log(add5(3))   // ?
```

**Solution:**
```
8, 13, 8

Each call to makeAdder creates a new FunctionEnvironmentRecord with its own x slot.
add5's closure captured the record where x=5.
add10's closure captured a DIFFERENT record where x=10.
They are independent Context objects on the heap.
add5 always adds to its own x=5, regardless of add10 existing.
```

---

## 🔗 Navigation

**Prev:** [03_Hoisting.md](03_Hoisting.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [05_Closures.md](05_Closures.md)
