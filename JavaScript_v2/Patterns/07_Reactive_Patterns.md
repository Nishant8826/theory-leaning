# 📌 07 — Reactive Patterns

## 🧠 Concept Explanation

Reactive programming is programming with asynchronous data streams. Everything can be a stream: events, promises, arrays, HTTP requests. You compose transformations on these streams using operators.

RxJS operationalizes this in JavaScript with Observables. Vue 3's reactivity and MobX use similar reactive primitives under the hood.

## 🔍 Code Examples

### RxJS Operators

```javascript
import { fromEvent, timer, combineLatest, merge } from 'rxjs'
import { debounceTime, distinctUntilChanged, switchMap, catchError, retry } from 'rxjs/operators'
import { EMPTY } from 'rxjs'

// Reactive search with autocomplete
const search$ = fromEvent(searchInput, 'input').pipe(
  debounceTime(300),          // Wait 300ms after last keypress
  map(event => event.target.value),
  distinctUntilChanged(),     // Skip if same value
  filter(query => query.length >= 2),
  switchMap(query =>          // Cancel previous, start new
    fetchResults(query).pipe(
      catchError(err => {
        console.error('Search failed:', err)
        return EMPTY           // Don't break the stream
      })
    )
  )
)

const subscription = search$.subscribe({
  next: results => updateResults(results),
  error: err => showError(err),
  complete: () => console.log('Search stream complete')
})

// Cleanup:
subscription.unsubscribe()
```

### Reactive State Management (MobX-inspired)

```javascript
class ReactiveStore {
  constructor(initialState) {
    this._state = initialState
    this._observers = new Map()
    this._computeds = new Map()
    this._tracking = null
    
    return new Proxy(this, {
      get: (target, prop) => {
        if (prop in target) return target[prop]
        return this._trackAccess(prop)
      },
      set: (target, prop, value) => {
        target._state[prop] = value
        this._notify(prop, value)
        return true
      }
    })
  }
  
  _trackAccess(prop) {
    if (this._tracking) {
      this._tracking.dependencies.add(prop)
    }
    return this._state[prop]
  }
  
  _notify(prop, value) {
    const observers = this._observers.get(prop) || new Set()
    observers.forEach(fn => fn(value))
  }
  
  observe(prop, fn) {
    if (!this._observers.has(prop)) this._observers.set(prop, new Set())
    this._observers.get(prop).add(fn)
    return () => this._observers.get(prop).delete(fn)
  }
  
  computed(name, fn) {
    const recompute = () => {
      const deps = new Set()
      this._tracking = { dependencies: deps }
      const result = fn()
      this._tracking = null
      
      // Subscribe to all accessed properties
      deps.forEach(dep => this.observe(dep, recompute))
      this._computeds.set(name, result)
    }
    recompute()
    return () => this._computeds.get(name)
  }
}
```

## 🏢 Industry Best Practices

1. **Unsubscribe on cleanup** — All Observable subscriptions must be unsubscribed.
2. **Use `switchMap` for search** — Cancels previous request when new query arrives.
3. **Use `catchError` to prevent stream termination** — Errors complete Observables by default.
4. **Prefer `combineLatest` over zip** — For combining latest values from multiple streams.

## 🔗 Navigation

**Prev:** [06_Middleware_Pattern.md](06_Middleware_Pattern.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [08_State_Management_Patterns.md](08_State_Management_Patterns.md)
