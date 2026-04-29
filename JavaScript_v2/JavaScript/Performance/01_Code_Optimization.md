# 📌 01 — Code Optimization

## 🧠 Concept Explanation

JavaScript code optimization at the V8 level involves understanding how the compiler pipeline (Ignition bytecode interpreter → TurboFan JIT compiler) optimizes code, what causes deoptimizations, and how to write code that stays in the "fast path."

Key optimization levers:
1. **Monomorphic code** — Same types at the same callsites (ICs stay fast)
2. **Predictable object shapes** — Hidden classes don't change after construction
3. **Loop optimization** — Avoid object allocations in hot loops
4. **Avoid deoptimizing patterns** — arguments object, eval, try/catch in loops

## 🔬 V8 Optimization Pipeline

```
Source → Parsing → AST → Ignition (bytecode) → Execute
                                    ↓ (hot function detected: 30+ calls)
                              TurboFan (JIT compile to machine code)
                                    ↓ (type assumption violated)
                              DEOPTIMIZE → back to Ignition
```

**Inline caching (IC) states:**
- **Uninitialized** — Never executed
- **Monomorphic** — One type seen → fastest
- **Polymorphic** — 2-4 types seen → fast (polymorphic IC)
- **Megamorphic** — 5+ types seen → slow (generic handler, no IC)

## 🔍 Code Examples

### Example 1 — Maintaining Monomorphic ICs

```javascript
// GOOD: Always call with same type → monomorphic IC
function processUser(user) {
  return user.name + ':' + user.age
}

// If called with:
processUser({ name: 'Alice', age: 30 })   // V8: IC = "shape A"
processUser({ name: 'Bob', age: 25 })     // V8: IC = "shape A" (same!) → monomorphic

// BAD: Called with different shapes → polymorphic/megamorphic
processUser({ name: 'Alice', age: 30 })         // shape A
processUser({ age: 25, name: 'Bob' })             // shape B (different order → different hidden class!)
processUser({ name: 'Carol', age: 20, email: '' }) // shape C
// After 5+ shapes: IC = megamorphic → slow lookup every call
```

### Example 2 — Object Shape Consistency

```javascript
// BAD: Adding properties after construction creates new hidden classes
function makeUser(name, email) {
  const user = {}  // Hidden class M0: {}
  user.name = name  // M1: {name}
  user.email = email  // M2: {name, email}
  if (email.endsWith('@gmail.com')) {
    user.isGmail = true  // M3: {name, email, isGmail} -- some users only
  }
  return user
}

// After 1000 users: 3/4 have shape M2, 1/4 have shape M3 → polymorphic ICs everywhere

// GOOD: Initialize all properties in constructor
function makeUser(name, email) {
  return {
    name,
    email,
    isGmail: email.endsWith('@gmail.com')  // Always present
    // ALL users have same shape → monomorphic ICs everywhere
  }
}
```

### Example 3 — Avoid Hidden Allocations in Hot Loops

```javascript
// BAD: allocations in hot loop
function processItems(items) {
  for (let i = 0; i < items.length; i++) {
    const temp = { value: items[i] }  // NEW OBJECT every iteration!
    processItem(temp)
    // temp becomes garbage immediately → GC pressure
  }
}

// GOOD: Reuse object or pass primitive
function processItems(items) {
  for (let i = 0; i < items.length; i++) {
    processItem(items[i])  // Pass primitive directly
  }
}

// Or: object pool
const pool = { value: null }
function processItems(items) {
  for (let i = 0; i < items.length; i++) {
    pool.value = items[i]
    processItem(pool)  // Always same object → IC stays monomorphic
  }
}
```

### Example 4 — Arguments Object vs Rest Parameters

```javascript
// BAD: arguments object prevents V8 optimizations
function badSum() {
  let sum = 0
  for (let i = 0; i < arguments.length; i++) {
    sum += arguments[i]  // `arguments` allocation prevents optimization
  }
  return sum
}

// GOOD: Rest parameters (optimizable by TurboFan)
function goodSum(...nums) {
  let sum = 0
  for (let i = 0; i < nums.length; i++) {
    sum += nums[i]  // nums is a real Array — can be optimized
  }
  return sum
}

// Even better for simple cases:
const sum = (nums) => nums.reduce((a, b) => a + b, 0)
```

## 💥 Production Failure — Accidental Deoptimization

```javascript
// try/catch prevents optimization of the entire surrounding function
function processOrders(orders) {
  // TurboFan WON'T optimize this function because of the try/catch!
  for (const order of orders) {
    try {
      processOrder(order)  // Even if this is hot
    } catch(e) {
      logError(e)
    }
  }
}

// Fix: move try/catch to a separate function
function safeProcessOrder(order) {
  try {
    processOrder(order)
  } catch(e) {
    logError(e)
  }
}

function processOrders(orders) {
  // This function CAN be optimized by TurboFan
  for (const order of orders) {
    safeProcessOrder(order)  // Calls optimized inner path
  }
}
```

## ⚠️ Measuring Optimization

```javascript
// Use V8 flags to observe optimization status
// node --trace-opt --trace-deopt app.js

// Programmatically check if function is optimized (dev only):
// node --allow-natives-syntax
function checkOptimized(fn) {
  %OptimizeFunctionOnNextCall(fn)
  fn()
  return %GetOptimizationStatus(fn)
}

// Benchmark with proper methodology:
const { performance } = require('perf_hooks')

function benchmark(name, fn, iterations = 1000000) {
  // Warm-up: run to trigger JIT
  for (let i = 0; i < 10000; i++) fn()
  
  const start = performance.now()
  for (let i = 0; i < iterations; i++) fn()
  const end = performance.now()
  
  console.log(`${name}: ${((end-start)/iterations*1000).toFixed(3)}μs/op`)
}
```

## 🏢 Industry Best Practices

1. **Profile before optimizing** — Don't guess; measure.
2. **Keep object shapes consistent** — Always initialize all properties.
3. **Avoid `delete` on objects** — Makes object go to dictionary mode (slow).
4. **Use TypedArrays for numeric computation** — Float64Array is MUCH faster than Array for numbers.
5. **Avoid `arguments`** — Use rest parameters.
6. **Keep hot functions small** — TurboFan works better with focused functions.

## ⚖️ Trade-offs

| Optimization | Benefit | Complexity | Risk |
|-------------|---------|------------|------|
| Object pooling | Reduces GC pressure | Medium | Shape pollution |
| Monomorphic types | Faster IC | Medium | Premature specialization |
| TypedArrays | 10-100x faster | Medium | Type constraints |
| Avoiding allocation | Less GC | High | Mutation bugs |

## 💼 Interview Questions

**Q1: What is deoptimization and what triggers it?**
> V8 speculatively optimizes functions (TurboFan) based on observed types. If a type assumption is violated (different shape object received, function receives unexpected type), V8 deoptimizes — throws away the compiled machine code and falls back to Ignition bytecode interpretation. Common triggers: changing object shape after construction, using `arguments` object, `eval`, `with`, `try/catch` in hot code, deleting properties, receiving objects of different shapes at the same callsite.

## 🔗 Navigation

**Prev:** [../Patterns/08_State_Management_Patterns.md](../Patterns/08_State_Management_Patterns.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [02_Reflow_and_Repaint.md](02_Reflow_and_Repaint.md)
