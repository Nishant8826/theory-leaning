# 📌 01 — Module Pattern

## 🧠 Concept Explanation

The Module Pattern uses closures to create private encapsulation in JavaScript. Before ES6 modules, this was the primary way to achieve information hiding. It remains relevant for understanding IIFE-based SDKs and older codebases.

## 🔍 Code Examples

### IIFE Module
```javascript
const Counter = (() => {
  let count = 0  // Private
  
  return {
    increment() { count++ },
    decrement() { count-- },
    getCount() { return count },
    reset() { count = 0 }
  }
})()

Counter.increment()
Counter.increment()
Counter.getCount()  // 2
Counter.count       // undefined (private!)
```

### Revealing Module
```javascript
const UserModule = (() => {
  const users = new Map()
  
  function create(data) {
    const id = generateId()
    users.set(id, { ...data, id, createdAt: Date.now() })
    return id
  }
  
  function getById(id) { return users.get(id) }
  function getAll() { return [...users.values()] }
  function remove(id) { return users.delete(id) }
  
  // Reveal only what's needed
  return { create, getById, getAll, remove }
})()
```

### Augmented Module (Splitting Across Files)

```javascript
// core.js
let Module = (() => {
  let state = {}
  return { getState: () => state, setState: s => { state = { ...state, ...s } } }
})()

// feature.js (augments Module)
Module = ((mod) => {
  mod.featureX = () => {
    // Has access to original mod's methods
    const state = mod.getState()
    return processFeatureX(state)
  }
  return mod
})(Module)
```

## ⚖️ Module Pattern vs ES6 Modules

| Aspect | IIFE Module | ES6 Module |
|--------|-------------|------------|
| Scope | Closure | File scope |
| Exports | Explicit object | `export` keyword |
| Tree-shaking | No | Yes |
| Live bindings | No | Yes |
| Browser support | Universal | Modern + bundler |

## 💼 Interview Questions

**Q1: Why was the Module Pattern necessary before ES6?**
> JavaScript had no native module system until ES6. All code shared a global scope. The IIFE pattern creates a closure that acts as a private scope — variables inside the IIFE are not accessible from outside. The returned object acts as the public API. This pattern enabled large applications to avoid global namespace pollution before CommonJS/AMD/ESM.

## 🔗 Navigation

**Prev:** [../NodeJS/08_Backpressure_Deep_Dive.md](../NodeJS/08_Backpressure_Deep_Dive.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [02_Factory_Pattern.md](02_Factory_Pattern.md)
