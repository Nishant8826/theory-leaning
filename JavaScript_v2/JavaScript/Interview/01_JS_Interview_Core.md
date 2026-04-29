# 📌 01 — JS Interview Core Concepts

## 🧠 Overview

This file covers the most frequently asked JavaScript interview questions at senior/principal engineer level, with answers that demonstrate engine internals knowledge. These go far beyond "what is a closure" — they expect systems-level thinking.

---

## 📋 Core Questions & Definitive Answers

### Q1: Explain the JavaScript runtime model

**Expected answer for senior level:**

JavaScript has a single-threaded execution model based on an event loop. V8 provides the JS engine (call stack + microtask queue). The host environment (browser or Node.js/libuv) provides the task queue and I/O abstractions.

Execution priority (highest to lowest):
1. Synchronous code (call stack)
2. Microtasks (Promise callbacks, queueMicrotask, MutationObserver)
3. Rendering (browser only: rAF, style, layout, paint)
4. Tasks (setTimeout, setInterval, I/O callbacks, DOM events)

**Deeper (engine-level):** V8's call stack is a LIFO stack of stack frames. Each frame includes local variables, arguments, and a pointer to the bytecode instruction. When a function returns, its frame is popped. Stack overflow occurs when the stack exceeds V8's stack size limit (~984 frames by default).

---

### Q2: What is a closure at the engine level?

**Surface answer:** A closure is a function that retains access to variables from its outer scope after that scope has closed.

**Engine-level answer (expected for senior+):**

V8 heap-allocates a **Context object** for each function invocation that has variables captured by inner functions. The Context contains the captured variable slots. The inner function holds a reference to this Context object via its `[[Environment]]` internal slot. As long as any inner function is reachable, the Context (and all its captured variables) remain reachable by the GC.

```javascript
function outer() {
  const x = { largeData: new Array(1e6) }  // Allocated on heap
  
  return function inner() {
    return x.largeData[0]  // inner's [[Environment]] → outer's Context → x
  }
}

const fn = outer()
// outer() has returned, but:
// fn → inner function → Context → x → largeData (1M element array)
// ALL of this is kept alive by fn
fn = null  // NOW everything is eligible for GC
```

---

### Q3: What is the difference between `==` and `===` at the spec level?

**`===` (Strict Equality — Abstract Equality Comparison):**
1. If types differ → `false`
2. If both undefined or both null → `true`
3. If NaN → `false` (NaN ≠ NaN)
4. If same primitive value → `true`
5. If same object reference → `true`

**`==` (Abstract Equality Comparison):**
Performs type coercion via a complex algorithm:
- `null == undefined` → `true` (both sides checked)
- `number == string` → convert string to number, then compare
- `boolean == anything` → convert boolean to number first
- `object == primitive` → call `ToPrimitive(object)`, then compare

```javascript
// Tricky coercions:
'' == false        // true ('' → 0, false → 0, 0 == 0)
0 == '0'          // true ('0' → 0)
0 == ''           // true ('' → 0)
'0' == false      // true ('0' → 0, false → 0, 0 == 0)
null == undefined  // true (spec special case)
null == 0         // false (null only == undefined)
[] == false       // true ([] → '' → 0, false → 0)
[] == ![]         // true (![] = false, [] == false → true)
```

---

### Q4: Explain prototype chain lookup in V8

When `obj.property` is accessed, V8 follows:

1. Check `obj`'s own properties (via hidden class + property backing store)
2. If not found: follow `obj.__proto__` (the prototype pointer in the object's Map)
3. Repeat until `Object.prototype` (whose `__proto__` is null)
4. If not found anywhere: return `undefined`

**IC optimization:** V8's IC remembers: "for objects with hidden class M, property 'x' is at offset 8 bytes." The next access with the same hidden class is a direct memory read — no chain traversal.

**IC invalidation:** If `Object.prototype` is modified (`Object.prototype.x = 1`), V8 must invalidate ALL monomorphic ICs that might now need to return this new property — a potentially catastrophic global invalidation.

---

### Q5: How does `async/await` differ from Promises?

`async/await` is syntactic sugar over Promises, but with important behavioral differences:

**Stack traces:** Async/await creates better stack traces because V8 links the async causation chain. Promise chains only show the current microtask's stack.

**Error handling:** `await` allows try/catch to catch async errors synchronously. Promise chains require `.catch()`.

**Debugging:** Async functions appear in the call stack in DevTools when suspended at `await`. Promise callback chains show only the current handler.

**Performance (V8 specific):** In V8 7.2+ (Node.js 12+), `await`ing a native Promise costs 1 microtask tick. Awaiting a thenable costs 2 ticks (PromiseResolveThenableJob). Without the optimization (older V8): always 2 ticks per await.

**Sequential vs parallel:**
```javascript
// Sequential (common mistake)
const a = await fetchA()  // Waits for A to complete
const b = await fetchB()  // Then waits for B

// Parallel (correct for independent operations)
const [a, b] = await Promise.all([fetchA(), fetchB()])
```

---

### Q6: What causes V8 to deoptimize a function?

V8 speculatively compiles (TurboFan) functions based on observed types. Deoptimization occurs when assumptions are violated:

1. **Type mismatch:** Function optimized for `number` arguments receives `string`
2. **Shape change:** Object shape changes after optimization (property added/deleted)
3. **Overflow:** SMI (small integer) arithmetic overflows to floating point
4. **`arguments` object escape:** Using `arguments` in ways that prevent optimization
5. **`eval` / `with`:** Dynamic scope prevents variable lookup optimization
6. **`try/catch` in hot path:** TurboFan doesn't fully optimize functions with try/catch
7. **Class changes:** Modifying `Array.prototype` or `Object.prototype`

After deoptimization, V8 re-enters Ignition bytecode mode and may re-optimize with new type observations.

---

### Q7: Explain WeakMap vs Map for memory management

**Map:** Strong references. Both keys and values are strongly referenced. A Map entry prevents both key and value from being GC'd.

**WeakMap:** Weak keys. The key must be an object. The WeakMap does NOT prevent the key object from being GC'd. When the key is GC'd, the entry is automatically removed.

**When to use WeakMap:**
- Associating metadata with objects without preventing their GC
- Caches where cache entries should expire when the key is no longer needed
- Private data associated with DOM elements or class instances

```javascript
// DOM element metadata (no memory leak):
const elementMeta = new WeakMap()
const el = document.createElement('div')
elementMeta.set(el, { clicks: 0, firstSeen: Date.now() })

el.remove()  // Remove from DOM
// If no other reference to el: el can be GC'd
// elementMeta entry also gone (key is the el object)

// Compare to Map: elementMeta.set(el, ...) with Map
// el.remove() does NOT allow GC — Map holds el reference!
```

---

### Q8: How does the V8 hidden class system work?

Every JavaScript object in V8 has an associated **Map** (called "hidden class" by the documentation). The Map describes:
- The object's structure (property names and their offsets)
- The object's prototype
- What type of object it is

When a property is added, V8 creates a **new Map** via a **transition**:

```
{} → Map M0 (empty object)
{ x: 1 } → Map M1 (has 'x' at offset 0)
{ x: 1, y: 2 } → Map M2 (has 'x' at offset 0, 'y' at offset 8)
```

Objects with the same structure share the same Map. ICs cache operations based on Map identity — "for Map M2, accessing 'x' returns the value at offset 0."

**Property addition order matters:**
```javascript
const a = {}; a.x = 1; a.y = 2  // Map: x→0, y→8
const b = {}; b.y = 2; b.x = 1  // Map: y→0, x→8 (DIFFERENT MAP!)
// a and b have different hidden classes — ICs see 2 shapes → polymorphic
```

---

### Q9: What is the Temporal Dead Zone (TDZ)?

The TDZ is the period between entering a scope and the initialization of a `let` or `const` variable. During the TDZ, accessing the variable throws a `ReferenceError`.

**Why it exists:** `let/const` variables ARE hoisted (the binding is created at scope entry), but they're placed in an "uninitialized" state. V8 internally uses a special "the hole" sentinel value. Accessing "the hole" triggers a TDZ check.

**V8 internals:** The bytecode for `let x = 5` in a block scope:
1. `CreateBlockContext` — creates scope with slot for `x`
2. `LdaTheHole` — load the "hole" sentinel
3. `StaCurrentContextSlot x` — initialize slot to hole (= TDZ starts)
4. ... (code before `let x = 5`) ...
5. `LdaSmi 5` — load value 5
6. `StaCurrentContextSlot x` — initialize to 5 (= TDZ ends)

Any `LdaContextSlot x` before step 6 → V8 sees "the hole" → `ReferenceError`.

---

### Q10: Explain how `this` binding works in V8

`this` is determined at call time, not at function definition time (except arrow functions):

| Call pattern | `this` value |
|-------------|--------------|
| `fn()` | undefined (strict) / global (non-strict) |
| `obj.fn()` | `obj` |
| `new Fn()` | new object |
| `fn.call(ctx, ...)` | `ctx` |
| `fn.apply(ctx, [...])` | `ctx` |
| `fn.bind(ctx)` | `ctx` (permanent) |
| Arrow `() => {}` | Lexical `this` from enclosing scope |

**V8 call dispatch:** When a method is called (`obj.fn()`), V8 passes `obj` as the implicit `this` parameter via the "receiver" slot in the call frame. For plain function calls, the receiver is `undefined` (strict) or the global object (non-strict).

---

## 💼 Rapid-Fire Questions

**Q: What outputs `typeof null`?**
> `"object"` — a historical bug in JavaScript. `null` is a primitive but `typeof null === "object"` due to the original C implementation using a null pointer (which was type-tagged as 'object').

**Q: Why does `0.1 + 0.2 !== 0.3`?**
> IEEE 754 double-precision floating point cannot represent 0.1 or 0.2 exactly. They're stored as approximations. The addition of two approximations results in 0.30000000000000004, not exactly 0.3. Use `Math.abs(a - b) < Number.EPSILON` for float comparison.

**Q: What does `new` actually do?**
> (1) Creates a new empty object, (2) sets its `[[Prototype]]` to `Constructor.prototype`, (3) calls the constructor with `this` = new object, (4) returns the new object (unless constructor explicitly returns a non-primitive).

**Q: Can you add properties to a primitive?**
> No. `"string".foo = 1` silently fails (non-strict) or throws (strict). Accessing a property on a primitive temporarily wraps it in a wrapper object (String, Number, Boolean), accesses the property, then discards the wrapper. The primitive is never mutated.

---

## 🔗 Navigation

**Prev:** [../Performance/08_GC_Performance_Tuning.md](../Performance/08_GC_Performance_Tuning.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [02_Tricky_Questions.md](02_Tricky_Questions.md)
