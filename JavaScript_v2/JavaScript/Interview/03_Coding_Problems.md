# 📌 03 — Coding Interview Problems

## 🧠 Overview

Coding problems that appear in senior JavaScript interviews. Each problem tests not just algorithmic thinking but also JavaScript-specific knowledge (closures, async, prototype, etc.).

---

## Problem 1 — Implement Promise.all

```javascript
function promiseAll(promises) {
  return new Promise((resolve, reject) => {
    if (!promises.length) return resolve([])
    
    const results = new Array(promises.length)
    let completed = 0
    
    promises.forEach((promise, index) => {
      Promise.resolve(promise).then(value => {
        results[index] = value  // Preserve order!
        completed++
        if (completed === promises.length) resolve(results)
      }).catch(reject)
    })
  })
}

// Test:
promiseAll([
  Promise.resolve(1),
  Promise.resolve(2),
  Promise.resolve(3)
]).then(console.log)  // [1, 2, 3]

promiseAll([
  Promise.resolve(1),
  Promise.reject('error'),
]).catch(console.error)  // 'error'
```

---

## Problem 2 — Implement Debounce

```javascript
function debounce(fn, delay, { leading = false, trailing = true } = {}) {
  let timer = null
  let lastArgs = null
  let lastThis = null
  let lastResult
  
  function invoke() {
    lastResult = fn.apply(lastThis, lastArgs)
    lastThis = lastArgs = null
  }
  
  function debounced(...args) {
    lastArgs = args
    lastThis = this
    
    const isFirstCall = !timer
    
    if (leading && isFirstCall) {
      invoke()
    }
    
    clearTimeout(timer)
    timer = setTimeout(() => {
      timer = null
      if (trailing && lastArgs) {
        invoke()
      }
    }, delay)
    
    return lastResult
  }
  
  debounced.cancel = () => {
    clearTimeout(timer)
    timer = lastArgs = lastThis = null
  }
  
  debounced.flush = () => {
    if (timer) {
      clearTimeout(timer)
      timer = null
      invoke()
    }
    return lastResult
  }
  
  return debounced
}
```

---

## Problem 3 — Implement LRU Cache

```javascript
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity
    this.cache = new Map()
  }
  
  get(key) {
    if (!this.cache.has(key)) return -1
    
    const value = this.cache.get(key)
    // Move to end (most recently used)
    this.cache.delete(key)
    this.cache.set(key, value)
    return value
  }
  
  put(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key)
    } else if (this.cache.size >= this.capacity) {
      // Delete oldest (first in Map iteration order)
      this.cache.delete(this.cache.keys().next().value)
    }
    this.cache.set(key, value)
  }
}

// Test:
const lru = new LRUCache(3)
lru.put(1, 'a')
lru.put(2, 'b')
lru.put(3, 'c')
lru.get(1)      // 'a', moves 1 to front
lru.put(4, 'd') // Evicts 2 (oldest unused)
lru.get(2)      // -1 (evicted)
```

---

## Problem 4 — Deep Clone (Production-Grade)

```javascript
function deepClone(value, seen = new Map()) {
  if (value === null || typeof value !== 'object') return value
  if (typeof value === 'function') return value
  
  // Circular reference detection
  if (seen.has(value)) return seen.get(value)
  
  // Special types
  if (value instanceof Date) return new Date(value.getTime())
  if (value instanceof RegExp) return new RegExp(value.source, value.flags)
  if (value instanceof Map) {
    const cloned = new Map()
    seen.set(value, cloned)
    value.forEach((v, k) => cloned.set(deepClone(k, seen), deepClone(v, seen)))
    return cloned
  }
  if (value instanceof Set) {
    const cloned = new Set()
    seen.set(value, cloned)
    value.forEach(v => cloned.add(deepClone(v, seen)))
    return cloned
  }
  if (ArrayBuffer.isView(value)) {
    const cloned = new value.constructor(value.buffer.slice(0))
    seen.set(value, cloned)
    return cloned
  }
  
  const cloned = Array.isArray(value) ? [] : Object.create(Object.getPrototypeOf(value))
  seen.set(value, cloned)
  
  for (const key of Reflect.ownKeys(value)) {
    const desc = Object.getOwnPropertyDescriptor(value, key)
    if (desc.get || desc.set) {
      Object.defineProperty(cloned, key, desc)
    } else {
      cloned[key] = deepClone(value[key], seen)
    }
  }
  
  return cloned
}
```

---

## Problem 5 — Event Emitter (Complete)

```javascript
class EventEmitter {
  constructor() {
    this._events = Object.create(null)
    this._maxListeners = 10
  }
  
  on(event, listener) {
    if (!this._events[event]) this._events[event] = []
    if (this._events[event].length >= this._maxListeners) {
      console.warn(`MaxListeners exceeded for event: ${event}`)
    }
    this._events[event].push(listener)
    return this
  }
  
  once(event, listener) {
    const wrapper = (...args) => {
      listener.apply(this, args)
      this.off(event, wrapper)
    }
    wrapper._original = listener
    return this.on(event, wrapper)
  }
  
  off(event, listener) {
    if (!this._events[event]) return this
    this._events[event] = this._events[event].filter(
      l => l !== listener && l._original !== listener
    )
    return this
  }
  
  emit(event, ...args) {
    if (!this._events[event]) return false
    this._events[event].slice().forEach(listener => {
      try { listener.apply(this, args) } catch(e) { this.emit('error', e) }
    })
    return true
  }
  
  removeAllListeners(event) {
    if (event) delete this._events[event]
    else this._events = Object.create(null)
    return this
  }
  
  listenerCount(event) {
    return this._events[event]?.length ?? 0
  }
}
```

---

## Problem 6 — Flatten Nested Array

```javascript
// Multiple approaches:
function flatten(arr, depth = Infinity) {
  // Method 1: recursive
  if (depth === 0) return arr.slice()
  return arr.reduce((acc, val) => {
    if (Array.isArray(val)) {
      acc.push(...flatten(val, depth - 1))
    } else {
      acc.push(val)
    }
    return acc
  }, [])
}

// Method 2: iterative with stack (avoids stack overflow for deep nesting)
function flattenIterative(arr) {
  const result = []
  const stack = [[...arr]]
  
  while (stack.length) {
    const item = stack.pop()
    if (Array.isArray(item)) {
      stack.push(...item)  // Push each element
    } else {
      result.unshift(item)
    }
  }
  
  return result
}

// Method 3: generator (memory efficient, lazy)
function* flattenGen(arr, depth = Infinity) {
  for (const item of arr) {
    if (Array.isArray(item) && depth > 0) {
      yield* flattenGen(item, depth - 1)
    } else {
      yield item
    }
  }
}
```

---

## 🔗 Navigation

**Prev:** [02_Tricky_Questions.md](02_Tricky_Questions.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Machine_Coding_JS.md](04_Machine_Coding_JS.md)
