# 📌 06 — Currying

## 🧠 Concept Explanation

Currying transforms a function that takes multiple arguments into a chain of functions that each take one argument. It's a functional programming technique rooted in lambda calculus. `f(a, b, c)` becomes `f(a)(b)(c)`.

Partial application is related but different: it pre-fills some arguments but doesn't necessarily reduce to unary functions. `f(a, b, c)` → `f(a)(b, c)` is partial application.

## 🔬 Internal Mechanics (V8)

Each curried invocation creates a new JSFunction (closure) that captures the accumulated arguments. The closure chain grows with each application:

```
curry(fn)(a) → new closure { fn, args: [a] }
              (b) → new closure { fn, args: [a, b] }
                    (c) → fn(a, b, c) — finally called
```

**IC implications:** If `curry(fn)` is called with different function types, the returned curried function becomes polymorphic. V8's IC at the call site sees different shapes → potential megamorphic IC. For performance-critical curried functions, call them monomorphically.

## 🔁 Execution Flow

```javascript
function curry(fn) {
  const arity = fn.length  // fn.length = number of declared params
  
  return function curried(...args) {
    if (args.length >= arity) {
      return fn.apply(this, args)
    }
    return function(...moreArgs) {
      return curried.apply(this, args.concat(moreArgs))
    }
  }
}

const add = curry((a, b, c) => a + b + c)
// add has arity 3 (fn.length = 3)

const step1 = add(1)       // args.length(1) < 3 → new closure { args: [1] }
const step2 = step1(2)     // args.length(2) < 3 → new closure { args: [1,2] }
const result = step2(3)    // args.length(3) >= 3 → fn(1, 2, 3) = 6
```

## 🧠 Memory Behavior

```
Heap allocations per curry application:
step1: JSFunction + Context { fn, args:[1] }        ≈ 150 bytes
step2: JSFunction + Context { fn, args:[1,2] }      ≈ 170 bytes
result: No new allocation (fn called directly)

For N applications: N JSFunction + N Context objects
GC: step1 and step2 eligible for GC after step2 and result are computed
    (no external reference to step1 after step2 = step1(2))
```

## 📐 ASCII Diagram — Curry Chain

```
curry(add3)
   │
   └─ curried function (captures: fn=add3, arity=3)
         │
         │ curried(1)
         └─ closure (captures: curried, args=[1])
               │
               │ (2)
               └─ closure (captures: curried, args=[1,2])
                     │
                     │ (3)
                     └─ fn(1, 2, 3) = 6  ← direct execution
```

## 🔍 Code Examples

### Example 1 — Practical Currying

```javascript
// Curried API call builder
const apiCall = curry((method, endpoint, data) =>
  fetch(endpoint, { method, body: JSON.stringify(data) })
)

const get = apiCall('GET')
const post = apiCall('POST')
const postUsers = post('/api/users')

// Usage:
await get('/api/users')()     // GET /api/users
await postUsers({ name: 'Alice' }) // POST /api/users with body
```

### Example 2 — Partial Application for Event Handlers

```javascript
// Curried event handler avoids creating closures inside loops
const handleItemClick = curry((dispatch, itemId, event) => {
  event.preventDefault()
  dispatch({ type: 'SELECT_ITEM', payload: itemId })
})

const dispatchBound = handleItemClick(dispatch)

// In template/JSX:
items.map(item => (
  <button onClick={dispatchBound(item.id)}>
    {item.name}
  </button>
))

// Each button gets a partially applied function
// Only ONE closure created per item (not a new arrow function per render)
```

### Example 3 — Point-Free Style with Curry

```javascript
const map = curry((fn, arr) => arr.map(fn))
const filter = curry((pred, arr) => arr.filter(pred))
const reduce = curry((fn, initial, arr) => arr.reduce(fn, initial))
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x)

// Point-free: no explicit data argument
const processUsers = pipe(
  filter(user => user.active),
  map(user => ({ id: user.id, name: user.name })),
  reduce((acc, user) => ({ ...acc, [user.id]: user }), {})
)

// processUsers(rawUsers) → { id1: {id, name}, id2: {id, name}, ... }
```

## 💥 Production Failures

### Failure — fn.length vs Rest Parameters

```javascript
// curry relies on fn.length (declared parameter count)
const broken = curry((...args) => args.reduce((a,b) => a+b, 0))
// broken.length === 0 (rest params don't count!)
// curry immediately calls fn with 0 args

// Fix: explicit arity parameter
const fixedCurry = (fn, arity = fn.length) => {
  return function curried(...args) {
    return args.length >= arity
      ? fn.apply(this, args)
      : (...more) => curried(...args, ...more)
  }
}

const sum = fixedCurry((...args) => args.reduce((a,b) => a+b, 0), 3)
sum(1)(2)(3)  // 6 ✓
```

## ⚠️ Edge Cases

```javascript
// Default parameters don't count in fn.length
const f = (a, b = 0, c) => a + b + c
f.length  // 1 (only 'a' counts — before first default)

// Destructured params count as 1 regardless of shape
const g = ({ x, y, z }) => x + y + z
g.length  // 1

// These edge cases make auto-currying unreliable
// Prefer explicit arity specification
```

## 🏢 Industry Best Practices

1. **Prefer explicit arity** — Don't rely on `fn.length` for currying. Pass arity explicitly.
2. **Use libraries** — `ramda.curry`, `lodash/fp` handle all edge cases.
3. **Curry for composition, not performance** — Curried closures have allocation cost.
4. **Avoid deep curry chains in hot paths** — Each application creates a closure.

## ⚖️ Trade-offs

| Approach | Composability | Performance | Readability |
|----------|--------------|-------------|-------------|
| Manual currying | High | Lower (closures) | Low |
| Partial application | Medium | Medium | High |
| Explicit functions | Low | Highest | Highest |
| Ramda/fp-ts | High | Medium | Medium |

## 💼 Interview Questions

**Q1: What is the difference between currying and partial application?**
> Currying always produces unary functions: `f(a,b,c)` → `f(a)(b)(c)`. Partial application pre-fills some arguments but the resulting function may still take multiple arguments: `f(a,b,c)` → `f(a)(b,c)`. All curried functions use partial application, but not all partial application is currying. JavaScript's `Function.prototype.bind` is partial application, not currying.

**Q2: How does `fn.length` interact with default parameters?**
> `fn.length` only counts parameters before the first default parameter. `(a, b=0, c)` has length 1. This makes auto-currying unreliable for functions with defaults. The spec specifies this behavior so that `length` reflects the minimum number of required arguments, not the total.

## 🧩 Practice Problem

Implement `pipe` and `compose` using currying:
```javascript
const pipe = (...fns) => (x) => fns.reduce((v, f) => f(v), x)
const compose = (...fns) => (x) => fns.reduceRight((v, f) => f(v), x)

// Async pipe
const pipeAsync = (...fns) => (x) => fns.reduce(
  async (promise, fn) => fn(await promise), 
  Promise.resolve(x)
)
```

## 🔗 Navigation

**Prev:** [05_Debouncing_vs_Throttling.md](05_Debouncing_vs_Throttling.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [07_Composition_vs_Inheritance.md](07_Composition_vs_Inheritance.md)
