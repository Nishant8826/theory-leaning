# 📌 01 — Execution Context

## 🧠 Concept Explanation (Deep Technical Narrative)

The Execution Context (EC) is the foundational abstraction that the ECMAScript specification uses to track code evaluation. Every time JavaScript evaluates code — a script, a module, a function, or `eval()` — the engine creates an Execution Context and pushes it onto the **Running Execution Context Stack** (what developers call "the call stack").

But the EC is far more than a stack frame. It is a composite record that holds:

1. **Code Evaluation State** — Used to suspend and resume async generators
2. **Function** — The function object being evaluated (null for scripts/modules)
3. **Realm** — The set of built-in objects (Array, Object, etc.) associated with this context
4. **LexicalEnvironment** — Where `let`, `const`, and function declarations live
5. **VariableEnvironment** — Where `var` declarations live
6. **PrivateEnvironment** — For class private fields (ES2022+)

In V8's implementation, this maps to a **stack frame** on the native call stack with associated objects heap-allocated for the environments.

---

## 🏗️ Common Mental Model vs Actual Behavior

**Common model:** "Each function gets its own scope" — technically correct but misses the spec structure.

**Actual behavior:** Each function invocation creates an EC with **two** environment records. `var` declarations go into `VariableEnvironment`, while `let`/`const` and inner functions go into `LexicalEnvironment`. For most functions these point to the same record, but for `catch` blocks and `with` statements they diverge — which is why:

```javascript
try {
  throw new Error()
} catch (e) {
  var x = 1  // Goes to VariableEnvironment (outer function scope)
  let y = 2  // Goes to catch's LexicalEnvironment (disappears after catch)
}
console.log(x) // 1 — var escapes catch block
console.log(y) // ReferenceError — let does not
```

---

## 🔬 Internal Mechanics (Engine-Level — V8)

### V8 Parsing Phase: Scope Analysis

Before any code executes, V8's **parser** performs a **scope analysis pass** that:
1. Identifies all variable declarations in each function
2. Determines if a variable is captured by an inner closure
3. Decides whether the variable lives on the **stack** (fast) or the **heap** (slow, context object)

```
Source Code
    │
    ▼
[Scanner/Tokenizer]
    │
    ▼
[Parser → AST]
    │
    ▼
[Scope Analyzer] ← Determines: stack-allocated vs context-allocated
    │
    ▼
[Bytecode Generator (Ignition)]
    │
    ▼
[BytecodeArray] ← What actually runs
```

### V8 Context Objects

When a function *closes over* a variable, V8 cannot store that variable on the native stack (it would be destroyed on function return). Instead, V8 heap-allocates a **Context object** — a fixed-size array with slots for each captured variable.

The `JSFunction` object in V8 holds a pointer to its **outer context**, forming a linked list — the scope chain.

```
[ JSFunction: inner ]
        │ context pointer
        ▼
[ Context: { x: 42, __parent__: ... } ]
        │ parent pointer
        ▼
[ Context: { outerVar: 'hello', __parent__: null } ]
```

**Key insight for performance:** If a variable is only used locally and never captured, it stays on the C++ native stack (register or stack slot). The moment it's captured, it gets boxed into a heap-allocated Context — adding GC pressure and cache-miss risk.

### Creation vs Execution Phase

The EC lifecycle has two phases:

**Phase 1 — Creation (Binding Instantiation):**
- `var` declarations → bound to `undefined` in VariableEnvironment
- `function` declarations → fully initialized (the function object exists)
- `let`/`const` → bound but **uninitialized** (TDZ — accessing throws ReferenceError)
- Arguments object created (non-strict mode)
- `this` binding established

**Phase 2 — Execution:**
- Code runs line by line
- Assignments update binding values
- `let`/`const` bindings become initialized at their declaration line

---

## 🔁 Execution Flow (Step-by-Step)

```javascript
// Example
const globalVar = 'global'

function outer(x) {
  const captured = x * 2
  
  function inner() {
    return captured + globalVar.length
  }
  
  return inner()
}

outer(5)
```

**Step 1:** Global EC created
- Realm: default realm
- LexicalEnvironment: GlobalEnvironmentRecord
  - `globalVar` → uninitialized (TDZ)
  - `outer` → function object (hoisted)
- VariableEnvironment: same as Lexical for global

**Step 2:** Global code executes
- `globalVar` initialized to `'global'`

**Step 3:** `outer(5)` called → New EC pushed
- LexicalEnvironment created with outer binding
  - `x` → 5 (parameter)
  - `captured` → uninitialized
  - `inner` → function object
- V8 detects `captured` is captured by `inner` → allocates Context object on heap

**Step 4:** `captured` initialized to `10`

**Step 5:** `inner()` called → New EC pushed
- `inner`'s LexicalEnvironment has outer pointer to `outer`'s Context
- `captured` lookup: not local → walk scope chain → found in outer's Context (10)
- `globalVar` lookup: walk chain to GlobalEnvironmentRecord → found

**Step 6:** `inner` EC popped, `outer` EC popped, control returns to global EC

---

## 🧠 Memory Behavior

```
STACK (native C++ stack)                HEAP (V8 managed)
┌─────────────────────┐                ┌────────────────────────────────┐
│  inner() frame      │                │  Context { captured: 10 }      │
│  [return addr]      │                │  ↑                             │
│  [scope ref] ───────┼────────────────┘  Context { x: 5 }            │
├─────────────────────┤                   ↑                             │
│  outer() frame      │────────────────── JSFunction: inner            │
│  [return addr]      │                                                 │
│  [scope ref]        │                   JSFunction: outer             │
├─────────────────────┤                                                 │
│  global frame       │                   GlobalEnvironmentRecord       │
└─────────────────────┘                └────────────────────────────────┘
```

**GC implication:** The `inner` function object holds a reference to `outer`'s Context. If `inner` is returned and kept alive (closure), V8's GC cannot collect the Context — even if `outer` itself has returned. The entire Context chain stays alive as long as *any* function that closed over it remains reachable.

---

## 📐 ASCII Diagram — EC Stack Lifecycle

```
EC Stack (grows upward)
                    ┌──────────────────┐
          inner()   │  EC: inner       │ ← Running EC
                    │  LE → outer ctx  │
                    ├──────────────────┤
          outer()   │  EC: outer       │
                    │  LE → global ctx │
                    │  VE → global ctx │
                    ├──────────────────┤
          global    │  EC: global      │ ← initial EC
                    │  LE → GlobalEnv  │
                    └──────────────────┘
```

---

## 🔍 Code Examples

### Example 1 — TDZ vs Hoisting

```javascript
console.log(typeof undeclared) // "undefined" — no binding at all
console.log(typeof letVar)     // ReferenceError — binding exists but TDZ
let letVar = 1

// WHY: In the creation phase, letVar is bound but marked "uninitialized".
// The typeof operator does NOT bypass TDZ (unlike undeclared variables).
```

### Example 2 — Context object allocation

```javascript
function createContext() {
  let count = 0  // Will V8 heap-allocate this?
  
  return function() { return ++count } // YES — count is captured
}

function noContext() {
  let count = 0  // V8 keeps this on the stack
  count++
  return count   // No closure — no heap allocation
}

// You can verify with: node --allow-natives-syntax
// %DebugPrint(createContext()) — look for "context" in output
```

### Example 3 — Multiple closures sharing Context

```javascript
function makeCounter() {
  let count = 0
  // Both functions share the SAME Context object
  return {
    increment: () => ++count,
    decrement: () => --count,
    value: () => count
  }
}

const c = makeCounter()
c.increment()
c.increment()
c.decrement()
console.log(c.value()) // 1
// count is ONE shared heap location — not three copies
```

### Example 4 — Realm isolation

```javascript
// In browser: iframes have separate Realms
const iframe = document.createElement('iframe')
document.body.appendChild(iframe)

const IframeArray = iframe.contentWindow.Array

const arr = new IframeArray(1, 2, 3)
console.log(arr instanceof Array)        // false — different Realm
console.log(arr instanceof IframeArray)  // true

// This breaks React's Children.toArray and similar instanceof checks
// Production bug: shared libraries passed cross-frame objects
```

---

## 💥 Production Failures & Debugging

### Failure 1 — Memory leak via retained EC

```javascript
// Anti-pattern seen in large SPAs
class EventBus {
  constructor() {
    this.handlers = []
  }
  
  subscribe(handler) {
    // handler closes over the subscribing component's entire state
    this.handlers.push(handler)
    // NEVER calls unsubscribe → component unmounts but its entire
    // closure context (including setState, refs, child components)
    // stays alive via the EventBus.handlers array
  }
}

// Production symptom: memory grows by ~2-5MB per route navigation
// Heap snapshot shows: EventBus → Function → Context → Component state chain
```

**Debugging:**
```
Chrome DevTools → Memory → Take Heap Snapshot
Filter by: "Detached" 
Look for: EventBus → [array] → JSFunction → Context
```

### Failure 2 — Unexpected shared context mutation

```javascript
// Classic interview trap, real production bug
const fns = []
for (var i = 0; i < 5; i++) {
  fns.push(function() { return i })
}
fns.map(f => f()) // [5, 5, 5, 5, 5]

// WHY: All 5 functions share ONE variable environment (the function scope
// containing the for loop). var declares i in that shared VE.
// By the time any function runs, the loop has completed: i === 5.

// Fix: IIFE per iteration (creates new EC per iteration)
for (var i = 0; i < 5; i++) {
  fns.push((function(i) { return function() { return i } })(i))
}
// OR: use let (creates new LexicalEnvironment binding per iteration)
for (let i = 0; i < 5; i++) {
  fns.push(function() { return i })
}
```

---

## ⚠️ Edge Cases & Undefined Behaviors

### eval() Creates a New EC Mid-Execution

```javascript
function test() {
  eval('var dynamicVar = 42') // Injects into current VariableEnvironment
  console.log(dynamicVar)    // 42 — accessible because eval uses current EC
}
// V8 CANNOT optimize functions containing eval() — it must assume any
// variable could be modified. V8 marks these as "has_eval" and disables:
// - Inline caching for variable access
// - Context slot analysis (must use slower lookup)
```

### `with` Statement — Scope Chain Injection

```javascript
const obj = { x: 10 }
with (obj) {
  // V8 inserts an ObjectEnvironmentRecord at the front of the scope chain
  console.log(x) // 10 — found in obj first
}
// Result: ALL variable lookups inside `with` become dynamic
// V8 cannot cache any slot positions → megamorphic ICs everywhere
// Strict mode forbids `with` precisely for this reason
```

### Module EC vs Script EC

```javascript
// script.js (classic) — global EC, var leaks to window
var leaked = true
window.leaked // true

// module.js (ESM) — module EC, top-level bindings are module-private
var notLeaked = true
window.notLeaked // undefined — module has its own top-level environment
```

---

## 🏢 Industry Best Practices

1. **Avoid `eval()` and `with`** — They disable V8's static scope analysis and inline caches. Use Function constructor sparingly; it has the same penalty.

2. **Minimize closure scope** — Only capture what you need. Capturing large objects in closures prevents GC of the entire object graph.

3. **Prefer `let`/`const` over `var`** — Block-scoped bindings create smaller Environment Records, and their TDZ behavior catches use-before-init bugs at development time.

4. **Cross-frame instanceof checks** — Use `Array.isArray()` instead of `instanceof Array` because it checks the `@@toStringTag` internal, not the Realm-specific constructor.

5. **Profile context allocation** — Use `node --trace-opt` and look for "context" in allocation output. Heavy context allocation in hot paths is a GC bottleneck.

---

## ⚖️ Trade-offs

| Design Decision | Benefit | Cost |
|----------------|---------|------|
| Heap-allocate captured vars | Enables closures | GC pressure, cache misses |
| TDZ for let/const | Catches use-before-init | Runtime check overhead |
| `var` hoisting | Simpler semantics historically | Confusing behavior, shared scope bugs |
| Realm isolation | Security (iframes, workers) | instanceof breaks across realms |
| eval() dynamic scope | Runtime code generation | Disables all V8 optimizations in function |

---

## 💼 Interview Questions (With Solutions)

**Q1: What is the difference between LexicalEnvironment and VariableEnvironment in an EC?**

> Both are Environment Records. For most functions they reference the same record. They differ in `catch` blocks and `with` statements — `var` always goes to VariableEnvironment (which is the function's outer environment), while `let`/`const` go to the LexicalEnvironment (which may be a block scope). This is why `var` in a `catch` block escapes to the function scope.

**Q2: Why does `typeof` on an undeclared variable return `"undefined"` but `typeof` on a TDZ variable throw?**

> `typeof` on an undeclared variable checks if the binding *exists* in any environment record in the scope chain. It doesn't — so the spec says return `"undefined"`. For a TDZ variable, the binding *does exist* (it was created in the creation phase) but is marked "uninitialized". Accessing an uninitialized binding throws ReferenceError, and `typeof` does NOT get special treatment for TDZ bindings.

**Q3: Explain the V8 optimization tradeoff for captured variables.**

> V8's scope analyzer identifies which variables are captured. Captured variables are allocated in heap-based Context objects (a fixed array). Non-captured variables stay on the native C++ stack as register variables or stack slots — much faster to access. Closures pay a heap allocation cost + potential GC cost in exchange for persistence beyond stack frame lifetime.

**Q4: What happens when two closures share a context, and one mutates the shared variable?**

> They share ONE Context object. Mutation by one function is immediately visible to all others. This is because closures capture the binding (the memory location in the Context), not the value. Counter objects and generators rely on this — it's a feature. The classic `for-var-loop` bug is a misuse of this behavior.

---

## 🧩 Practice Problems (With Solutions)

**Problem 1:** Predict the output and explain with EC internals:

```javascript
let x = 'global'
function outer() {
  let x = 'outer'
  function inner() {
    console.log(x) // What prints?
    let x = 'inner'
    console.log(x) // What prints?
  }
  inner()
}
outer()
```

**Solution:**
```
ReferenceError — TDZ
```
The first `console.log(x)` inside `inner` throws ReferenceError. Even though `x = 'outer'` exists in the outer scope, the `let x = 'inner'` declaration causes the engine (during scope analysis) to create a new binding for `x` in `inner`'s lexical environment. This binding is **uninitialized** (TDZ) at the point of the first `console.log`. The outer `x` is **shadowed** — it's unreachable. This is a critical V8 scope analysis behavior.

---

**Problem 2:** Fix this without using `let`:

```javascript
const timers = []
for (var i = 0; i < 3; i++) {
  timers.push(setTimeout(function() { console.log(i) }, 100 * i))
}
// Currently prints: 3, 3, 3
```

**Solution:**
```javascript
// Option A: IIFE (creates new EC per iteration, capturing current i)
for (var i = 0; i < 3; i++) {
  (function(capturedI) {
    timers.push(setTimeout(function() { console.log(capturedI) }, 100 * capturedI))
  })(i)
}

// Option B: .bind (binds value at call time)
for (var i = 0; i < 3; i++) {
  timers.push(setTimeout(console.log.bind(null, i), 100 * i))
}

// Explanation: IIFE creates a new VariableEnvironment for each iteration.
// capturedI in each IIFE's EC gets the value of i AT THAT MOMENT (0, 1, 2).
```

---

## 🔗 Navigation

**Prev:** [00_Index.md](../00_Index.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [02_Call_Stack.md](02_Call_Stack.md)
