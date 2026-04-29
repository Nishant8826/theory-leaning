# 📌 02 — EventEmitter

## 🧠 Concept Explanation

Node.js EventEmitter is the observer pattern as a core primitive. It's the backbone of Node.js's async model: streams, HTTP servers, sockets, child processes — all extend EventEmitter. Understanding its internals is essential for building reliable event-driven systems.

## 🔬 Internal Mechanics

EventEmitter maintains a `_events` object (plain JS object, not Map) mapping event names to listeners. Listeners are stored as functions or arrays of functions. For performance, the single-listener case stores the function directly; the multi-listener case stores an array.

```javascript
// Internal structure:
emitter._events = {
  'data': [fn1, fn2, fn3],  // Multiple listeners
  'end': fn4,               // Single listener (stored directly, not in array)
  'error': fn5              // Special: if no error listener, throws!
}
```

**MaxListeners:** Default 10. Adding more emits a warning (potential memory leak detection). Not a hard limit.

**`once()` internals:** Creates a wrapper function that calls the original handler then removes itself. The wrapper is what's actually registered — which is why `removeListener(event, originalFn)` doesn't work for `once()`-registered listeners!

## 🔍 Code Examples

### Example 1 — Building a Production EventEmitter

```javascript
const EventEmitter = require('events')

class OrderSystem extends EventEmitter {
  constructor() {
    super()
    this.setMaxListeners(20)  // Increase limit for high-subscription scenarios
    
    // Always handle errors to prevent crashes
    this.on('error', (err) => {
      console.error('OrderSystem error:', err)
      // Re-emit to monitoring system
      monitoring.captureException(err)
    })
  }
  
  createOrder(data) {
    try {
      const order = processOrderData(data)
      this.emit('order:created', order)
      return order
    } catch (err) {
      this.emit('error', err)
    }
  }
  
  // Memory-safe event subscription with cleanup
  subscribe(event, handler, signal) {
    this.on(event, handler)
    
    // AbortSignal for automatic cleanup
    if (signal) {
      signal.addEventListener('abort', () => {
        this.off(event, handler)
      }, { once: true })
    }
    
    return () => this.off(event, handler)  // Manual cleanup function
  }
}
```

### Example 2 — AsyncEmitter Pattern

```javascript
// Standard EventEmitter doesn't await async listeners
class AsyncEmitter extends EventEmitter {
  async emitAsync(event, ...args) {
    const listeners = this.rawListeners(event)
    const results = []
    
    for (const listener of listeners) {
      try {
        const result = await Promise.resolve(
          listener.apply(this, args)
        )
        results.push(result)
      } catch (err) {
        this.emit('error', err)
      }
    }
    
    return results
  }
}

// Usage:
const emitter = new AsyncEmitter()
emitter.on('process', async (data) => {
  await saveToDatabase(data)
})
await emitter.emitAsync('process', userData)
// Waits for async listener to complete
```

### Example 3 — Memory Leak via Listener Accumulation

```javascript
// BUG: Each request adds a listener, never removed
http.createServer(async (req, res) => {
  // This creates a new closure per request:
  db.on('query', () => {
    // Never removed! Memory leak — each request adds a listener
  })
  
  // After 1000 requests: 1000 listeners on db's 'query' event
  // Node.js MaxListeners warning fires at 10 listeners
})

// Fix: Use once, or explicit cleanup
http.createServer(async (req, res) => {
  const handler = () => { ... }
  db.once('query', handler)  // Auto-removes after first event
  // OR:
  db.on('query', handler)
  req.on('close', () => db.off('query', handler))  // Cleanup on request close
})
```

## 💥 Production Failure — Missing Error Handler

```javascript
// CRASH: EventEmitter throws if 'error' is emitted without listener
const emitter = new EventEmitter()
emitter.emit('error', new Error('Unhandled!'))
// Process CRASHES with "Unhandled 'error' event"
// Unlike other events: 'error' with no listener = synchronous throw

// ALWAYS add error handler:
emitter.on('error', (err) => {
  console.error('Handled:', err)
})

// For streams (which extend EventEmitter):
stream.on('error', (err) => { /* handle */ })
// Missing stream error handler = process crash on pipe failure!
```

## 🏢 Industry Best Practices

1. **Always handle `error` events** — Missing error handler = process crash.
2. **Use `once()` for one-time events** — Prevents listener accumulation.
3. **Return cleanup functions** — Make it easy to remove subscriptions.
4. **Monitor listener counts** — Alert if `emitter.listenerCount(event) > threshold`.
5. **Use AbortSignal for lifecycle-bound subscriptions** — Natural cleanup with component/request lifecycle.

## 💼 Interview Questions

**Q1: Why does emitting 'error' without a listener crash the process?**
> EventEmitter has a special case for the 'error' event: if it fires with no listeners, EventEmitter throws the error synchronously. Since this happens in the event loop, an uncaught throw becomes an uncaught exception, crashing the process. This design reflects the philosophy that unhandled errors are bugs. In production, always attach error listeners to all EventEmitter instances.

**Q2: Why doesn't `removeListener` work for functions registered with `once()`?**
> `once()` internally wraps your function in a new wrapper function (which removes itself after one call). The wrapper is what's actually stored in `_events`. When you call `removeListener(event, originalFn)`, it looks for `originalFn` in the listener array — but only finds the wrapper. Fix: save the return value of `once()` (which returns the emitter for chaining) and use `emitter.rawListeners(event)` to find wrappers. Or use `AbortSignal` for lifecycle-based cleanup.

## 🔗 Navigation

**Prev:** [01_Node_Architecture.md](01_Node_Architecture.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Streams.md](03_Streams.md)
