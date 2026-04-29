# 📌 04 — Observer Pattern

## 🧠 Concept Explanation

The Observer pattern (Pub/Sub) defines a one-to-many dependency where when one object (subject/publisher) changes state, all dependents (observers/subscribers) are notified automatically. It's the foundation of event-driven programming.

Variants:
- **Observer** — Subject holds direct references to observers (tighter coupling)
- **Pub/Sub** — Event broker decouples publisher and subscriber (looser coupling)

## 🔍 Code Examples

### Production-Grade EventBus

```javascript
class EventBus {
  constructor() {
    this.events = new Map()
    this.onceEvents = new Map()
    this.wildcardHandlers = []
  }
  
  on(event, handler, { priority = 0 } = {}) {
    if (!this.events.has(event)) this.events.set(event, [])
    const handlers = this.events.get(event)
    handlers.push({ handler, priority })
    handlers.sort((a, b) => b.priority - a.priority)  // Higher priority first
    
    return () => this.off(event, handler)
  }
  
  once(event, handler) {
    const wrapper = (...args) => {
      handler(...args)
      this.off(event, wrapper)
    }
    return this.on(event, wrapper)
  }
  
  off(event, handler) {
    if (!this.events.has(event)) return
    const handlers = this.events.get(event)
    const index = handlers.findIndex(h => h.handler === handler)
    if (index !== -1) handlers.splice(index, 1)
  }
  
  emit(event, data) {
    const handlers = this.events.get(event) || []
    handlers.forEach(({ handler }) => {
      try {
        handler(data)
      } catch(err) {
        this.emit('error', { event, error: err })
      }
    })
    
    this.wildcardHandlers.forEach(handler => {
      try { handler(event, data) } catch(e) {}
    })
  }
  
  onAny(handler) {
    this.wildcardHandlers.push(handler)
    return () => {
      this.wildcardHandlers = this.wildcardHandlers.filter(h => h !== handler)
    }
  }
  
  clear(event) {
    if (event) this.events.delete(event)
    else { this.events.clear(); this.wildcardHandlers = [] }
  }
}

const bus = new EventBus()

// Middleware-style (typed events)
const off = bus.on('user:created', (user) => {
  sendWelcomeEmail(user)
}, { priority: 10 })

bus.on('user:created', async (user) => {
  await updateAnalytics(user)
}, { priority: 5 })

bus.emit('user:created', { id: 1, email: 'alice@example.com' })
```

### RxJS-Inspired Observable

```javascript
class Observable {
  constructor(subscriber) {
    this._subscriber = subscriber
  }
  
  static fromEvent(element, event) {
    return new Observable(observer => {
      const handler = (e) => observer.next(e)
      element.addEventListener(event, handler)
      return () => element.removeEventListener(event, handler)
    })
  }
  
  static interval(ms) {
    return new Observable(observer => {
      let id = 0
      const timer = setInterval(() => observer.next(id++), ms)
      return () => clearInterval(timer)
    })
  }
  
  pipe(...operators) {
    return operators.reduce((obs, op) => op(obs), this)
  }
  
  map(fn) {
    return new Observable(observer => {
      return this.subscribe({
        next: (v) => observer.next(fn(v)),
        error: (e) => observer.error(e),
        complete: () => observer.complete()
      })
    })
  }
  
  filter(pred) {
    return new Observable(observer => {
      return this.subscribe({
        next: (v) => pred(v) && observer.next(v),
        error: (e) => observer.error(e),
        complete: () => observer.complete()
      })
    })
  }
  
  subscribe(observer) {
    const cleanup = this._subscriber(observer)
    return { unsubscribe: cleanup || (() => {}) }
  }
}
```

## 💥 Production Failure — Event Listener Accumulation in SPA

```javascript
// React component adding global event listeners without cleanup
function SearchComponent() {
  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown)
    bus.on('search:results', handleResults)
    // No cleanup!
    // Unmounting adds listener, never removes it
    // After 100 mounts/unmounts: 100 handlers for same event
  }, [])
  
  // Fix:
  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown)
    const off = bus.on('search:results', handleResults)
    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      off()
    }
  }, [])
}
```

## 🏢 Industry Best Practices

1. **Return unsubscribe functions** — Every subscription should be cancellable.
2. **Handle errors in handlers** — A throwing handler shouldn't stop other handlers.
3. **Use typed events** — TypeScript discriminated unions for event data.
4. **WeakRef for optional observers** — If observers shouldn't prevent GC.
5. **Test with multiple subscribers** — Verify ordering, error isolation, cleanup.

## 💼 Interview Questions

**Q1: What is the difference between Observer and Pub/Sub patterns?**
> Observer: the subject (observable) directly holds references to its observers and calls them directly. Tight coupling — observers know about the subject, subject knows about observers. Pub/Sub: introduces an event broker/message bus between publisher and subscriber. Neither knows about each other — they communicate through the broker. Pub/Sub is looser coupling and allows for cross-component communication without direct references.

## 🔗 Navigation

**Prev:** [03_Singleton_Pattern.md](03_Singleton_Pattern.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [05_Strategy_Pattern.md](05_Strategy_Pattern.md)
