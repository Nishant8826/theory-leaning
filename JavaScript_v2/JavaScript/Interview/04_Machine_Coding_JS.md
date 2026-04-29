# 📌 04 — Machine Coding (JS System Design)

## 🧠 Overview

Machine coding rounds require building small but complete systems in 30-60 minutes. These test architecture, API design, edge case handling, and production-readiness thinking.

---

## System 1 — Build a Pub/Sub System

```javascript
class PubSub {
  constructor() {
    this.topics = new Map()
    this.subId = 0
  }
  
  subscribe(topic, callback) {
    if (!this.topics.has(topic)) this.topics.set(topic, new Map())
    
    const id = ++this.subId
    this.topics.get(topic).set(id, callback)
    
    // Return unsubscribe function
    return () => {
      const subs = this.topics.get(topic)
      subs?.delete(id)
      if (subs?.size === 0) this.topics.delete(topic)
    }
  }
  
  publish(topic, data) {
    if (!this.topics.has(topic)) return 0
    
    let count = 0
    this.topics.get(topic).forEach(callback => {
      try { callback(data); count++ } catch(e) { console.error(e) }
    })
    return count
  }
  
  unsubscribeAll(topic) {
    if (topic) this.topics.delete(topic)
    else this.topics.clear()
  }
  
  getSubscriberCount(topic) {
    return this.topics.get(topic)?.size ?? 0
  }
}
```

---

## System 2 — Build a Request Queue with Concurrency Limit

```javascript
class RequestQueue {
  constructor(concurrency = 3) {
    this.concurrency = concurrency
    this.running = 0
    this.queue = []
  }
  
  add(requestFn) {
    return new Promise((resolve, reject) => {
      this.queue.push({ requestFn, resolve, reject })
      this.process()
    })
  }
  
  process() {
    while (this.running < this.concurrency && this.queue.length > 0) {
      const { requestFn, resolve, reject } = this.queue.shift()
      this.running++
      
      Promise.resolve()
        .then(() => requestFn())
        .then(result => { resolve(result); this.running--; this.process() })
        .catch(err => { reject(err); this.running--; this.process() })
    }
  }
  
  get pending() { return this.queue.length }
  get active() { return this.running }
}

// Usage:
const queue = new RequestQueue(3)
const results = await Promise.all(
  urls.map(url => queue.add(() => fetch(url).then(r => r.json())))
)
```

---

## System 3 — Build a Memoize Function

```javascript
function memoize(fn, { 
  maxSize = Infinity,
  keySerializer = JSON.stringify,
  ttl = null
} = {}) {
  const cache = new Map()
  
  function memoized(...args) {
    const key = keySerializer(args)
    
    if (cache.has(key)) {
      const { value, expiry } = cache.get(key)
      if (!expiry || Date.now() < expiry) {
        return value
      }
      cache.delete(key)
    }
    
    const value = fn.apply(this, args)
    
    // Enforce size limit (evict oldest)
    if (cache.size >= maxSize) {
      cache.delete(cache.keys().next().value)
    }
    
    cache.set(key, {
      value,
      expiry: ttl ? Date.now() + ttl : null
    })
    
    return value
  }
  
  memoized.cache = cache
  memoized.clear = () => cache.clear()
  memoized.delete = (...args) => cache.delete(keySerializer(args))
  memoized.size = () => cache.size
  
  return memoized
}

// Async memoize
function memoizeAsync(fn, options = {}) {
  const inFlight = new Map()
  const memoized = memoize((...args) => {
    const key = JSON.stringify(args)
    if (!inFlight.has(key)) {
      const promise = fn(...args).finally(() => inFlight.delete(key))
      inFlight.set(key, promise)
    }
    return inFlight.get(key)
  }, options)
  return memoized
}
```

---

## System 4 — Build a State Machine

```javascript
class StateMachine {
  constructor(config) {
    this.config = config
    this.state = config.initial
    this.context = config.context || {}
    this.listeners = []
  }
  
  send(event, payload) {
    const stateConfig = this.config.states[this.state]
    const transition = stateConfig?.on?.[event]
    
    if (!transition) return this
    
    const target = typeof transition === 'string' ? transition : transition.target
    const action = typeof transition === 'object' ? transition.action : null
    
    // Guard check
    if (transition.guard && !transition.guard(this.context, payload)) {
      return this  // Transition rejected by guard
    }
    
    // Exit current state
    stateConfig.exit?.(this.context, payload)
    
    // Execute transition action
    if (action) this.context = action(this.context, payload) || this.context
    
    const prevState = this.state
    this.state = target
    
    // Enter new state
    this.config.states[target]?.entry?.(this.context, payload)
    
    // Notify listeners
    this.listeners.forEach(l => l({ prev: prevState, next: target, event, payload }))
    
    return this
  }
  
  matches(state) { return this.state === state }
  
  onChange(fn) {
    this.listeners.push(fn)
    return () => { this.listeners = this.listeners.filter(l => l !== fn) }
  }
}
```

---

## 💼 Machine Coding Evaluation Criteria

1. **Correctness** — Does it handle the happy path?
2. **Edge cases** — Empty inputs, null, concurrent calls
3. **Error handling** — Throws? Returns null? Propagates?
4. **API design** — Is it intuitive and consistent?
5. **Memory safety** — Any leaks? Does cleanup work?
6. **Testability** — Can each part be tested independently?

---

## 🔗 Navigation

**Prev:** [03_Coding_Problems.md](03_Coding_Problems.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [../Projects/01_Build_Event_Emitter.md](../Projects/01_Build_Event_Emitter.md)
