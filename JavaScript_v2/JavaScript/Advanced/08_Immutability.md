# 📌 08 — Immutability

## 🧠 Concept Explanation

Immutability means objects cannot be modified after creation. In JavaScript, it's enforced either by language mechanisms (`Object.freeze`, `const`) or by convention + libraries (Immer, Immutable.js). True immutability in JS is shallow by default — `Object.freeze` only freezes one level.

The value proposition of immutability:
- **Predictability:** No hidden state mutations
- **Change detection:** Reference equality (`===`) is sufficient to detect changes
- **Concurrency safety:** Immutable values can be shared across threads/workers safely
- **Time-travel debugging:** Snapshots of immutable state are trivial

## 🔬 Internal Mechanics (V8)

### `Object.freeze` Internals

```javascript
Object.freeze(obj)
```

V8 sets the object's hidden class to one marked **not extensible** and all property descriptors to `writable: false, configurable: false`. Internally:
1. `[[Preventextensions]]` called → hidden class becomes "non-extensible variant"
2. For each own property: descriptor updated to non-writable + non-configurable
3. V8 caches this as a separate hidden class state

**Performance:** Frozen objects can actually be FASTER in some cases — V8 knows properties won't change, enabling more aggressive inline caching. TurboFan can treat frozen object property accesses as constants.

### Structural Sharing (Persistent Data Structures)

Libraries like Immutable.js and Immer implement structural sharing:
- When you "modify" an immutable object, they create a NEW object sharing unchanged sub-trees
- Uses hash array mapped tries (HAMT) or similar persistent data structures
- Memory cost: O(log n) new nodes per update (not O(n) full copy)

```
Original tree:        After update(key='c', val=99):
    root                    newRoot
   /    \                  /       \
  a      b               a        newB
 / \    / \             / \       /  \
1   2  3   4           1   2    3   newC
                                      \
                                       99
Shared: a, 1, 2, 3 nodes
New: newRoot, newB, newC
```

## 📐 ASCII Diagram — Freeze vs Deep Freeze

```
Object.freeze(obj):
obj = { a: 1, nested: { b: 2 } }
       ↑ frozen (can't add/change/delete 'a' or 'nested')
              ↑ NOT frozen! nested.b can still be mutated

Deep freeze:
obj = { a: 1, nested: { b: 2 } }
       ↑ frozen                
              ↑ ALSO frozen — recursive freeze
```

## 🔍 Code Examples

### Example 1 — Object.freeze Deep

```javascript
function deepFreeze(obj) {
  if (obj === null || typeof obj !== 'object') return obj
  
  Object.keys(obj).forEach(key => deepFreeze(obj[key]))
  return Object.freeze(obj)
}

const config = deepFreeze({
  api: { baseUrl: 'https://api.example.com', timeout: 5000 },
  features: { darkMode: true, analytics: false }
})

config.api.timeout = 9999  // Silently fails (strict: TypeError)
config.api.timeout         // Still 5000
```

### Example 2 — Immer Structural Sharing

```javascript
import produce from 'immer'

const state = {
  users: [
    { id: 1, name: 'Alice', settings: { theme: 'dark' } },
    { id: 2, name: 'Bob', settings: { theme: 'light' } }
  ],
  meta: { version: 1 }
}

// Update only Alice's theme
const nextState = produce(state, draft => {
  draft.users[0].settings.theme = 'light'
})

// Verification:
nextState === state              // false (new root)
nextState.users === state.users  // false (new array — path changed)
nextState.users[0] === state.users[0]  // false (new user object)
nextState.users[0].settings === state.users[0].settings  // false (new settings)
nextState.users[1] === state.users[1]  // TRUE — Bob unchanged, same reference!
nextState.meta === state.meta    // TRUE — meta unchanged, same reference!

// Change detection: O(1) reference equality
if (nextState.users[1] !== state.users[1]) { /* Bob changed */ }
```

### Example 3 — Immutable.js vs Plain JS

```javascript
import { Map, List } from 'immutable'

// Immutable.js: persistent data structures (HAMT internally)
const map1 = Map({ a: 1, b: 2 })
const map2 = map1.set('c', 3)  // Returns NEW Map, shares a and b

map1.toJS()  // { a: 1, b: 2 }
map2.toJS()  // { a: 1, b: 2, c: 3 }
map1 === map2  // false
map1.get('a') === map2.get('a')  // Internally shares the value

// Performance profile:
// map.get(key): O(log32 n) — HAMT tree traversal
// Plain object: O(1) — IC direct property access
// Immutable.js is slower for individual gets but faster for structural sharing
// Use when: deep state trees, frequent partial updates, React optimization
```

### Example 4 — Record and Tuple (Stage 2 Proposal)

```javascript
// Upcoming: primitively immutable by nature
const record = #{ x: 1, y: 2, nested: #{ z: 3 } }
const tuple = #[1, 2, 3]

// Records and Tuples are PRIMITIVES (like strings) — compared by VALUE
#{ x: 1 } === #{ x: 1 }  // TRUE (value comparison, not reference!)

// Current workaround until proposal lands:
// Use Immer + memoized selectors for structural equality
```

## 💥 Production Failures

### Failure — Mutating Shared State in Redux

```javascript
// BUG: Reducer mutates existing state
function reducer(state = [], action) {
  switch (action.type) {
    case 'ADD':
      state.push(action.item)  // MUTATION!
      return state              // Same reference → React doesn't re-render
    case 'ADD_CORRECT':
      return [...state, action.item]  // New array → re-renders correctly
  }
}

// Detection: Redux DevTools shows action dispatched but state appears unchanged
// Debugger: prev state === next state (same reference)
```

### Failure — Object.freeze Performance Cliff

```javascript
// Freezing very large objects at module load time
const HUGE_CONFIG = Object.freeze(generateConfig())  // 10MB config object
// This freezes 50,000 nested properties
// Cost: O(N) where N = all nested properties = seconds of blocking!

// Fix: Lazy freeze
const createFrozenConfig = (() => {
  let frozen = null
  return () => {
    if (!frozen) frozen = Object.freeze(generateConfig())
    return frozen
  }
})()
```

## ⚠️ Edge Cases

### `const` is NOT immutability

```javascript
const obj = { x: 1 }
obj.x = 2  // Works! const binds the reference, not the value
obj = {}   // TypeError: Assignment to constant variable

// const = immutable binding (cannot rebind)
// Object.freeze = immutable value (cannot mutate)
```

### Frozen Prototype Method Conflicts

```javascript
const frozen = Object.freeze({ hasOwnProperty: null })
frozen.hasOwnProperty('key')  // TypeError — we "overrode" Object.prototype method!
// Frozen doesn't prevent prototype method shadowing by own properties
Object.prototype.hasOwnProperty.call(frozen, 'key')  // Safe alternative
```

## 🏢 Industry Best Practices

1. **Use Immer for state management** — Structural sharing without Immutable.js API overhead.
2. **Freeze configuration objects** — API keys, feature flags, routing config.
3. **Never mutate function parameters** — Treat all parameters as immutable.
4. **Use `const` for all declarations** — Forces intentionality on rebinding.
5. **Memoize derived state** — With immutable state, `useMemo` dependencies are simple reference checks.

## 💼 Interview Questions

**Q1: Why does `Object.freeze` not deep-freeze?**
> `Object.freeze` was designed to be a single operation on one object — making it recursive would have unpredictable performance characteristics (cycles, very deep trees). The spec keeps it shallow and lets developers decide how to handle nested structures. Deep freezing is trivially composable on top of the shallow API.

**Q2: How does structural sharing enable O(1) change detection in React?**
> With structural sharing (Immer/Immutable.js), unchanged parts of the state tree reuse the exact same object references. A component subscribed to `state.users[1]` can check `prevState.users[1] === nextState.users[1]` — if true, the slice didn't change (even if other parts of state did). This makes `React.memo` and `PureComponent` highly effective because their default shallow comparison correctly identifies unchanged components.

## 🔗 Navigation

**Prev:** [07_Composition_vs_Inheritance.md](07_Composition_vs_Inheritance.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [09_Modules_System.md](09_Modules_System.md)
