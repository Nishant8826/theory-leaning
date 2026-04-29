# 📌 01 — Deep vs Shallow Copy

## 🧠 Concept Explanation (Deep Technical Narrative)

Copying objects in JavaScript is not a language-level operation with a single implementation — it's a spectrum of techniques with fundamentally different semantics, performance profiles, and correctness trade-offs. The core distinction:

- **Shallow copy:** Creates a new top-level object with references to the same nested objects. Mutations to nested objects are shared between original and copy.
- **Deep copy:** Creates a fully independent object graph where every nested object is also a new object. Mutations are never shared.

The critical insight: JavaScript has no built-in deep copy for arbitrary objects (until `structuredClone` in 2022). Every pre-`structuredClone` deep copy mechanism was either incomplete, slow, or both.

At the V8 level, "copying" means creating new heap allocations. Understanding which allocations are shared vs independent is essential for reasoning about correctness and performance.

---

## 🔬 Internal Mechanics (Engine-Level — V8)

### Object Layout in V8 Memory

```
JSObject (shallow copy makes a new JSObject, but...)
┌─────────────────────────────────────────────────────┐
│  Map pointer (hidden class)                         │
│  Property backing store pointer                     │ ← New array
│  In-object slot 0: primitive (42) — COPIED          │ ← Value copy
│  In-object slot 1: pointer to HeapObject ───────────┼──→ shared HeapObject!
│  In-object slot 2: pointer to Array ────────────────┼──→ shared Array!
└─────────────────────────────────────────────────────┘
```

For a shallow copy:
- Primitives (numbers, booleans, strings) stored as SMI (small integer) or pointer to heap string — value copied
- Object references — pointer copied (both original and copy point to same heap object)

### Copy-on-Write (COW) in V8

V8 implements COW for **array literal elements**:
```javascript
const arr = [1, 2, 3] // V8: elements stored in COW buffer
const arr2 = arr.slice() // Initially shares the COW buffer
arr2[0] = 99 // COW: triggers copy of buffer for arr2
```

This is an internal V8 optimization — invisible to JavaScript code but relevant for understanding why `Array.slice()` doesn't immediately double memory usage.

### `structuredClone` Algorithm (V8 Implementation)

`structuredClone` uses the **structured clone algorithm** defined in the HTML spec. V8 implements this as a C++ traversal:

1. Maintains a "transfer map" for circular reference detection
2. For each supported type (Object, Array, Date, Map, Set, RegExp, TypedArray, Blob, etc.): copies recursively
3. Uses V8's `ValueSerializer/ValueDeserializer` — the same mechanism used for postMessage

Unsupported types: Functions, DOM nodes, class instances with prototype methods (methods not copied), WeakMap/WeakSet, Error (partial).

---

## 🔁 Execution Flow (Step-by-Step)

```javascript
const original = {
  a: 1,                           // Primitive
  b: { nested: 'object' },        // Nested object
  c: [1, 2, 3],                   // Array
  d: new Date(),                  // Date object
}

// Method 1: Object spread (shallow)
const spread = { ...original }

// Method 2: Object.assign (shallow)
const assigned = Object.assign({}, original)

// Method 3: JSON (deep, but lossy)
const json = JSON.parse(JSON.stringify(original))

// Method 4: structuredClone (deep, complete)
const clone = structuredClone(original)
```

**V8 operations for spread:**
```
1. CreateObject {} (new JSObject on heap)
2. For each property of original:
   - Read property value (may be primitive or pointer)
   - Copy value into new object's property backing store
   - For 'b': copies the POINTER to the nested object
   - For 'c': copies the POINTER to the array
3. Return new JSObject
Time: O(n) where n = number of own properties
```

**V8 operations for structuredClone:**
```
1. ValueSerializer: walks entire object graph depth-first
   - Creates serialized byte stream
2. ValueDeserializer: reconstructs from byte stream
   - Creates new heap objects for everything
Time: O(total nodes in object graph)
Memory: peak = original + serialized buffer + clone
```

---

## 🧠 Memory Behavior

```
SHALLOW COPY memory:
                                        
original   ──→  { a:1, b:──→[nested:obj], c:──→[1,2,3] }
                              ↑                 ↑
spread     ──→  { a:1, b:────┘            c:───┘        }

Two JSObject headers, ONE nested object, ONE array.
Mutations to original.b or spread.b affect the SAME heap object.

DEEP COPY memory:

original   ──→  { a:1, b:──→[nested:obj1], c:──→[arr1] }
                              
clone      ──→  { a:1, b:──→[nested:obj2], c:──→[arr2] }

Two independent object graphs. Total memory: ~2x.

STRUCTURAL SHARING (used by immutable libraries):
original   ──→  { a:1, b:──→[nested:obj], c:──→[arr] }
                              ↑                 
withA      ──→  { a:2, b:────┘            c:──→[arr]  }

Only the changed path is new. Unchanged subtrees are SHARED.
Immer.js, Immutable.js, Redux Toolkit use this pattern.
```

---

## 📐 ASCII Diagram — Copy Semantics

```
SHALLOW COPY:
  [original] ─── a: 1 (primitive, copied by value)
                 b: ───────────────────────────┐
                 c: ─────────────────────┐     │
                                         │     │
  [shallow] ──── a: 1 (own copy)         │     │
                 b: ──────────────────── │─────┘ (SAME object!)
                 c: ──────────────────── ┘ (SAME array!)

DEEP COPY:
  [original] ─── a: 1
                 b: ──→ { nested: 'object' }
                 c: ──→ [1, 2, 3]

  [deep] ──────── a: 1
                  b: ──→ { nested: 'object' } (NEW object)
                  c: ──→ [1, 2, 3] (NEW array)
```

---

## 🔍 Code Examples

### Example 1 — Shallow Copy Methods Compared

```javascript
const obj = { x: 1, inner: { y: 2 }, arr: [3, 4] }

// Method A: Spread
const a = { ...obj }

// Method B: Object.assign
const b = Object.assign({}, obj)

// Method C: Array destructuring for arrays
const arrCopy = [...obj.arr]

// Verify shallow:
a.inner === obj.inner   // true — same reference
a.arr === obj.arr       // true — same reference
a.x === obj.x           // true (same value, but x is primitive)

// Mutation test:
a.inner.y = 99
console.log(obj.inner.y)  // 99 — shared reference!

// Spread does NOT spread getters (converts to values)
const withGetter = Object.create({}, {
  computed: { get() { return Math.random() }, enumerable: true }
})
const spread = { ...withGetter }
spread.computed // Fixed value (getter called once during spread)
// withGetter.computed would call getter each time
```

### Example 2 — JSON Deep Copy Limitations

```javascript
const obj = {
  str: 'hello',            // ✓ copied
  num: 42,                 // ✓ copied
  bool: true,              // ✓ copied
  arr: [1, 2],             // ✓ copied
  nested: { a: 1 },        // ✓ copied
  
  undef: undefined,        // ✗ key removed (JSON has no undefined)
  fn: () => {},            // ✗ key removed (functions not serializable)
  symbol: Symbol('key'),   // ✗ key removed (symbols not JSON)
  date: new Date(),        // ✗ becomes string (not Date object!)
  nan: NaN,                // ✗ becomes null
  inf: Infinity,           // ✗ becomes null
  regexp: /pattern/gi,     // ✗ becomes {}
  map: new Map([[1, 2]]),  // ✗ becomes {}
  set: new Set([1, 2]),    // ✗ becomes {}
  bigint: 42n,             // ✗ throws TypeError!
}

const jsonCopy = JSON.parse(JSON.stringify(obj))
// jsonCopy has lost: undef, fn, symbol
// jsonCopy.date is a STRING, not a Date
// jsonCopy.nan === null
// jsonCopy.regexp is {}
// Never use JSON deep copy in production for arbitrary objects!
```

### Example 3 — structuredClone (2022+)

```javascript
const obj = {
  date: new Date(),         // ✓ cloned as Date object
  regexp: /pattern/gi,      // ✓ cloned as RegExp
  map: new Map([[1, 2]]),   // ✓ cloned as Map
  set: new Set([1, 2, 3]), // ✓ cloned as Set
  typed: new Uint8Array(4), // ✓ cloned (new buffer)
  error: new Error('oops'), // ✓ cloned (partial)
}

// Circular references handled!
const circular = { a: 1 }
circular.self = circular
const cloned = structuredClone(circular)
cloned.self === cloned  // true — circular ref preserved!

// What structuredClone CANNOT clone:
const bad = {
  fn: () => {},           // ✗ DataCloneError: functions
  symbol: Symbol('key'), // ✗ DataCloneError: symbols
  domNode: document.body, // ✗ DataCloneError: DOM nodes
  proxy: new Proxy({}, {}), // ✗ DataCloneError: Proxies
}
structuredClone(bad) // Throws DOMException: Failed to execute 'structuredClone'
```

### Example 4 — Structural Sharing (Immer Pattern)

```javascript
import produce from 'immer'

const state = {
  users: [
    { id: 1, name: 'Alice', posts: [{ id: 1, title: 'Hello' }] },
    { id: 2, name: 'Bob', posts: [] },
  ],
  ui: { loading: false, error: null }
}

// Immer: only creates new objects along the MUTATION path
const nextState = produce(state, draft => {
  draft.users[0].name = 'Alicia'  // Mutate via Proxy
})

// Memory analysis:
// nextState.users !== state.users          (new array - path mutated)
// nextState.users[0] !== state.users[0]   (new object - mutated)
// nextState.users[0].posts === state.users[0].posts  (SAME array! not in mutation path)
// nextState.users[1] === state.users[1]   (SAME object! Bob not touched)
// nextState.ui === state.ui               (SAME object! UI not touched)

// This is structural sharing: only O(depth of change) new allocations
// Full deep clone would be O(total nodes)
```

---

## 💥 Production Failures & Debugging

### Failure 1 — Redux State Mutation via Shallow Copy

```javascript
// Classic Redux bug: reducer modifies state instead of returning new state
function reducer(state = initialState, action) {
  switch (action.type) {
    case 'ADD_ITEM':
      state.items.push(action.item)  // MUTATES state.items!
      return state  // Same reference → React/Redux sees no change!
      
    case 'ADD_ITEM_CORRECT':
      return {
        ...state,
        items: [...state.items, action.item]  // New array, new state object
      }
  }
}

// Symptom: UI doesn't update even though state changed
// Because: === comparison finds state unchanged (same reference)
// Detection: Redux DevTools shows action dispatched but state unchanged
// Fix: Use Immer (produce) or always return new objects
```

### Failure 2 — Date Object Corruption via JSON Clone

```javascript
// API response processing bug
async function getUserData(id) {
  const data = await fetch(`/api/user/${id}`).then(r => r.json())
  // data.createdAt is already a STRING from JSON parsing!
  
  const user = JSON.parse(JSON.stringify(data)) // "deep clone"
  // user.createdAt is STILL a string — not a Date object
  
  // Later code expects Date:
  const daysSince = (Date.now() - user.createdAt) / 86400000
  // NaN! Because "2023-01-01T00:00:00.000Z" - Date.now() = NaN
}

// Fix: Use structuredClone + proper Date handling
// OR: Use a schema validator like Zod that constructs proper types
```

---

## ⚠️ Edge Cases & Undefined Behaviors

### Prototype Not Copied

```javascript
class Point {
  constructor(x, y) { this.x = x; this.y = y }
  distanceTo(other) { return Math.sqrt((this.x - other.x)**2 + (this.y - other.y)**2) }
}

const p = new Point(1, 2)

// Spread loses prototype
const copy = { ...p }
copy instanceof Point  // false
copy.distanceTo        // undefined

// JSON loses prototype AND methods
const jsonCopy = JSON.parse(JSON.stringify(p))
jsonCopy instanceof Point  // false

// Only structuredClone... also doesn't preserve prototype for custom classes!
const sc = structuredClone(p)
sc instanceof Point  // false — structuredClone treats as plain object

// To preserve prototype with deep copy:
function deepCloneWithProto(obj) {
  return Object.assign(Object.create(Object.getPrototypeOf(obj)), 
    structuredClone(obj))
}
```

### Getter/Setter Behavior During Copy

```javascript
const reactive = {
  _x: 0,
  get x() { 
    console.log('getter called')
    return this._x 
  },
  set x(v) { this._x = v }
}

// Spread: calls getter, copies the VALUE (not the getter/setter!)
const copy = { ...reactive }
// "getter called" logs during spread
// copy.x is a plain property (value: 0), NOT a getter
// copy.x = 5 just sets a value — original._x unchanged

// To preserve getters/setters:
const withAccessors = Object.defineProperties(
  {},
  Object.getOwnPropertyDescriptors(reactive)
)
// withAccessors.x is a getter — calling it triggers original's getter
```

---

## 🏢 Industry Best Practices

1. **Use `structuredClone` as the default deep copy** (2022+, available in Node.js 17+, Chrome 98+, Firefox 94+). Fall back to `lodash.cloneDeep` for environments lacking support.

2. **Use Immer for immutable state updates** — It's structurally sharing-aware, handles circular refs, and has V8-optimized Proxy implementation.

3. **Never use JSON.parse(JSON.stringify)** in production for deep copy — silently loses dates, functions, undefined, NaN, and infinite values.

4. **Profile clone operations in hot paths** — `structuredClone` on large objects (>10MB) adds measurable latency. Cache clones or use structural sharing.

5. **For Redux/state management**: Use RTK's `createSlice` with Immer built-in. Manual spread-heavy reducers are error-prone and verbose.

---

## ⚖️ Trade-offs

| Method | Depth | Speed | Preserves Types | Handles Circular |
|--------|-------|-------|-----------------|-----------------|
| Spread `{...}` | Shallow | Fastest | Yes (pointer) | N/A |
| `Object.assign` | Shallow | Fast | Yes (pointer) | N/A |
| JSON round-trip | Deep | Slow | No (Date→string) | No (throws) |
| `structuredClone` | Deep | Medium | Most types | Yes |
| `lodash.cloneDeep` | Deep | Medium | Most types | Yes |
| Immer `produce` | Structural | Fast (COW) | Proxied | Yes |

---

## 💼 Interview Questions (With Solutions)

**Q1: Why does `JSON.parse(JSON.stringify(date))` produce a string, not a Date?**

> `JSON.stringify` calls `date.toISOString()` (via the Date object's `toJSON` method), producing a string. `JSON.parse` sees a string and has no knowledge that it was originally a Date — it remains a string. JSON's type system has no Date type. `structuredClone` avoids this by using a separate serialization format that preserves type tags.

**Q2: How does Immer implement structural sharing without full deep copy?**

> Immer wraps the state in a recursive Proxy. When the draft function reads a property, Immer gives a Proxy that tracks access. When the draft function WRITES a property, Immer creates a new object for that level and marks all ancestors for recreation. On `produce()` completion, Immer walks the tree: nodes that were written get new objects; nodes that weren't written reuse the original object's reference. Only the path from the root to the mutation gets new allocations — all other subtrees are shared.

**Q3: What is the V8-level difference between `[...arr]` and `arr.slice()`?**

> Both produce a shallow copy. `Array.slice()` is a built-in that V8 can inline and optimize with COW semantics. Spread (`[...arr]`) goes through the iterator protocol (`Symbol.iterator`), which is slower for standard arrays but allows copying any iterable (not just arrays). For plain dense arrays, `slice()` is typically faster. For sparse arrays or custom iterables, spread handles them correctly while slice may produce holes.

---

## 🧩 Practice Problems (With Solutions)

**Problem:** Implement a production-grade deep clone:

```javascript
function deepClone(value, refs = new Map()) {
  // Primitives
  if (value === null || typeof value !== 'object') return value
  if (typeof value === 'function') return value  // Functions: reference copy
  
  // Circular reference
  if (refs.has(value)) return refs.get(value)
  
  // Special types
  if (value instanceof Date) return new Date(value)
  if (value instanceof RegExp) return new RegExp(value.source, value.flags)
  if (value instanceof Map) {
    const cloneMap = new Map()
    refs.set(value, cloneMap)
    value.forEach((v, k) => cloneMap.set(deepClone(k, refs), deepClone(v, refs)))
    return cloneMap
  }
  if (value instanceof Set) {
    const cloneSet = new Set()
    refs.set(value, cloneSet)
    value.forEach(v => cloneSet.add(deepClone(v, refs)))
    return cloneSet
  }
  if (ArrayBuffer.isView(value)) {
    return new value.constructor(value.buffer.slice(0), value.byteOffset, value.length)
  }
  
  // Objects and Arrays
  const clone = Array.isArray(value) ? [] : Object.create(Object.getPrototypeOf(value))
  refs.set(value, clone)
  
  for (const key of Reflect.ownKeys(value)) {
    const descriptor = Object.getOwnPropertyDescriptor(value, key)
    if (descriptor.get || descriptor.set) {
      Object.defineProperty(clone, key, descriptor)  // Preserve accessors
    } else {
      clone[key] = deepClone(value[key], refs)
    }
  }
  
  return clone
}
```

---

## 🔗 Navigation

**Prev:** [../Fundamentals/12_Execution_Order_Deep_Dive.md](../Fundamentals/12_Execution_Order_Deep_Dive.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [02_Memory_Management.md](02_Memory_Management.md)
