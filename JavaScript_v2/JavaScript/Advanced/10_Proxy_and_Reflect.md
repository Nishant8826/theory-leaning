# 📌 10 — Proxy & Reflect

## 🧠 Concept Explanation

Proxy creates a meta-programming layer around an object, intercepting fundamental operations (get, set, has, deleteProperty, apply, construct) via "traps". Reflect provides the default implementations of those same operations as first-class functions.

## 🔬 Internal Mechanics (V8)

### IC Invalidation by Proxy

Proxies are the most significant IC killer in V8. When V8's IC encounters an object backed by a Proxy, it CANNOT cache property access:
- Every property access on a Proxy goes through the trap system
- V8 cannot predict what a trap will return → no caching
- Property access on proxied objects degrades to slow path (dictionary mode)

`javascript
const p = new Proxy({}, { get: () => Math.random() })
p.x  // Goes through: IC miss → trap call → runtime lookup EVERY TIME
`

### Proxy Trap Cost

Each trap invocation:
1. V8 identifies object as Proxy (via internal type flag)
2. Jumps to Proxy handler lookup in C++ runtime
3. Calls handler.trap() via JS function call
4. Returns result (possibly doing type checking)

This is significantly slower than normal property access (~10-50x for simple cases).

## 🔁 Execution Flow — get Trap

`javascript
const handler = {
  get(target, prop, receiver) {
    // target = original object
    // prop = property name (string or Symbol)
    // receiver = the Proxy (or object that initiated the access)
    
    console.log(Getting: )
    return Reflect.get(target, prop, receiver)  // Default behavior
  }
}

const proxy = new Proxy({ x: 1 }, handler)
proxy.x
// 1. V8: detects Proxy type
// 2. Calls handler.get(target, 'x', proxy)
// 3. Logs "Getting: x"
// 4. Reflect.get(target, 'x', proxy) → returns 1
`

## 📐 ASCII Diagram — Proxy Architecture

`
Consumer Code
     │ proxy.property
     ▼
┌─────────────────┐
│     PROXY       │ ← transparent wrapper
│  get trap       │ ── calls ──► Handler.get(target, prop, receiver)
│  set trap       │ ── calls ──► Handler.set(target, prop, value, receiver)
│  has trap       │ ── calls ──► Handler.has(target, prop)
└─────────────────┘
     │ Reflect.get() / target[prop]
     ▼
┌─────────────────┐
│     TARGET      │ ← real object
└─────────────────┘
`

## 🔍 Code Examples

### Example 1 — Validation Proxy

`javascript
function createTypedObject(schema) {
  return new Proxy({}, {
    set(target, prop, value) {
      if (prop in schema) {
        const expectedType = schema[prop]
        if (typeof value !== expectedType) {
          throw new TypeError(${prop} must be , got )
        }
      }
      return Reflect.set(target, prop, value)
    },
    get(target, prop) {
      if (!(prop in target) && !(prop in schema)) {
        throw new ReferenceError(Unknown property: )
      }
      return Reflect.get(target, prop)
    }
  })
}

const user = createTypedObject({ name: 'string', age: 'number' })
user.name = 'Alice'  // OK
user.age = 'thirty'  // TypeError: age must be number
`

### Example 2 — Reactive Proxy (Vue 3 Internals)

`javascript
// Simplified Vue 3 reactivity (actual implementation in @vue/reactivity)
const trackMap = new WeakMap()
let activeEffect = null

function reactive(obj) {
  return new Proxy(obj, {
    get(target, key, receiver) {
      // Track this dependency
      if (activeEffect) {
        let deps = trackMap.get(target)
        if (!deps) { deps = new Map(); trackMap.set(target, deps) }
        let dep = deps.get(key)
        if (!dep) { dep = new Set(); deps.set(key, dep) }
        dep.add(activeEffect)
      }
      const value = Reflect.get(target, key, receiver)
      // If value is object: make it reactive too (lazy)
      return typeof value === 'object' && value !== null ? reactive(value) : value
    },
    
    set(target, key, value, receiver) {
      const result = Reflect.set(target, key, value, receiver)
      // Trigger effects that depend on this key
      const deps = trackMap.get(target)
      if (deps) {
        const dep = deps.get(key)
        if (dep) dep.forEach(effect => effect())
      }
      return result
    }
  })
}
`

### Example 3 — Proxy for Logging/Monitoring

`javascript
function createMonitoredAPI(api, logger) {
  return new Proxy(api, {
    apply(target, thisArg, args) {
      const start = performance.now()
      try {
        const result = Reflect.apply(target, thisArg, args)
        if (result instanceof Promise) {
          return result
            .then(v => { logger.info(${target.name} resolved in ms); return v })
            .catch(e => { logger.error(${target.name} rejected:, e); throw e })
        }
        logger.info(${target.name} returned in ms)
        return result
      } catch(e) {
        logger.error(${target.name} threw:, e)
        throw e
      }
    }
  })
}

const monitoredFetch = createMonitoredAPI(fetch, console)
`

## 💥 Production Failure — Proxy Performance in Hot Loops

`javascript
// Anti-pattern: Proxy in inner loop
const reactive = new Proxy(largeObject, complexHandler)

for (let i = 0; i < 1000000; i++) {
  result += reactive.value  // Each access goes through trap — very slow!
}

// Fix: Extract value outside the loop
const value = reactive.value  // One trap call
for (let i = 0; i < 1000000; i++) {
  result += value  // Direct read — fast!
}

// Vue 3 addresses this: reactive() creates proxies lazily
// and deactivated proxies don't intercept accesses in background computations
`

## ⚠️ Edge Cases

### Proxy vs Reflect for 	his forwarding

`javascript
class MyClass {
  constructor() { this.value = 42 }
  getValue() { return this.value }
}

const obj = new MyClass()
const proxy = new Proxy(obj, {
  get(target, prop, receiver) {
    const value = Reflect.get(target, prop, receiver)
    // CRITICAL: pass eceiver to Reflect.get
    // This ensures 	his in getValue() = proxy (not target)
    // Matters when subclasses or other proxies are involved
    return typeof value === 'function' ? value.bind(receiver) : value
  }
})
`

## 🏢 Industry Best Practices

1. **Never use Proxy in hot performance paths** — IC miss on every access.
2. **Use Proxy at boundaries** — API validation, logging, feature flags.
3. **Always use Reflect.* in traps** — Provides correct default semantics with receiver forwarding.
4. **Cache Proxy targets** — Don't create new Proxy objects for each access.

## 💼 Interview Questions

**Q1: Why do Proxies invalidate V8's inline caches?**
> V8's ICs cache property access patterns keyed on object shape (hidden class). A Proxy's "shape" is fundamentally dynamic — the same property access could return different values or invoke arbitrary code. V8 cannot make any static assumptions about Proxy behavior, so it bypasses the IC system and always uses the slow-path runtime dispatch for proxied objects.

**Q2: What is the difference between Proxy and Object.defineProperty for interception?**
> Object.defineProperty with a getter/setter intercepts only specific property accesses by name. It's cheaper (no IC invalidation) but limited. Proxy intercepts ALL operations (any property, prototype access, function calls, instanceof, in operator, spread, destructuring) dynamically. Proxy is more powerful but significantly more expensive. Use defineProperty for specific computed properties; use Proxy for meta-programming like validation frameworks.

## 🔗 Navigation

**Prev:** [09_Modules_System.md](09_Modules_System.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [11_Symbols_and_Iterators.md](11_Symbols_and_Iterators.md)
