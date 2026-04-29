# 📌 05 — Debouncing vs Throttling

## 🧠 Concept Explanation (Deep Technical Narrative)

Debouncing and throttling are rate-limiting patterns that control how frequently a function can be invoked. They're critical for managing user events (resize, scroll, input) that fire far more frequently than useful work can be done.

- **Debouncing:** Delays invocation until the event stream has *stopped* for a specified duration. The function runs ONCE after a "quiet period."
- **Throttling:** Guarantees the function runs AT MOST once per specified interval, regardless of how many events fire.

They solve different problems: debounce for "wait until user stops typing" (autocomplete), throttle for "update at most 60fps" (scroll position).

The subtle distinction: debounce collapses a burst into ONE call; throttle spreads calls evenly across time.

---

## 🔬 Internal Mechanics

### Debounce — Timer Reset Pattern

```javascript
function debounce(fn, delay, options = {}) {
  let timer = null
  let lastArgs = null
  const { leading = false, trailing = true } = options
  
  function debounced(...args) {
    lastArgs = args
    
    // Leading edge: call immediately on first event
    if (leading && !timer) fn.apply(this, args)
    
    // Reset timer on every call
    clearTimeout(timer)
    timer = setTimeout(() => {
      timer = null
      if (trailing) fn.apply(this, lastArgs)  // Call with LAST args
    }, delay)
  }
  
  debounced.cancel = () => { clearTimeout(timer); timer = null }
  debounced.flush = () => { if (timer) { clearTimeout(timer); fn.apply(this, lastArgs) } }
  
  return debounced
}
```

V8 behavior: Each `setTimeout` creates a timer handle in libuv's heap (Node.js) or the browser's timer system. `clearTimeout` marks the timer as cancelled. The closure captures `timer`, `lastArgs`, and `fn` — all heap-allocated. For frequently-created debounced functions (anti-pattern), each creates a new closure on the heap.

### Throttle — Leading/Trailing Edge Pattern

```javascript
function throttle(fn, interval, options = { leading: true, trailing: true }) {
  let lastCallTime = 0
  let timer = null
  let lastArgs = null
  
  function throttled(...args) {
    const now = Date.now()
    lastArgs = args
    
    if (!lastCallTime && !options.leading) {
      lastCallTime = now  // Skip first call
    }
    
    const remaining = interval - (now - lastCallTime)
    
    if (remaining <= 0) {
      // Time to execute
      if (timer) { clearTimeout(timer); timer = null }
      lastCallTime = now
      fn.apply(this, args)
    } else if (options.trailing) {
      // Schedule trailing call
      clearTimeout(timer)
      timer = setTimeout(() => {
        lastCallTime = options.leading ? Date.now() : 0
        timer = null
        fn.apply(this, lastArgs)
      }, remaining)
    }
  }
  
  throttled.cancel = () => { clearTimeout(timer); timer = null; lastCallTime = 0 }
  
  return throttled
}
```

### requestAnimationFrame-Based Throttle

```javascript
// For visual updates: throttle to display refresh rate naturally
function rafThrottle(fn) {
  let rafId = null
  let lastArgs = null
  
  function throttled(...args) {
    lastArgs = args
    if (!rafId) {
      rafId = requestAnimationFrame((timestamp) => {
        rafId = null
        fn.apply(this, [...lastArgs, timestamp])
      })
    }
  }
  
  throttled.cancel = () => { cancelAnimationFrame(rafId); rafId = null }
  return throttled
}

// Better than throttle(fn, 16) because:
// 1. Automatically adjusts to actual display refresh rate (60Hz, 90Hz, 120Hz)
// 2. Pauses in hidden tabs (saves battery)
// 3. Synchronized with browser's rendering pipeline
```

---

## 🔁 Execution Flow

```
DEBOUNCE (delay=300ms):
Events:  ↓  ↓  ↓  ↓          ↓  ↓
         0  100 200 300       700 800ms
         
Timer:   [─300ms─]reset[─300ms─]reset[─300ms─]reset[─300ms─]  [─300ms─]
                                               ↑              ↑
Fires:                                      NEVER      FIRES at 1100ms

THROTTLE (interval=300ms):
Events:  ↓  ↓  ↓  ↓    ↓  ↓
         0  100 200 300 500 600ms
         
Fires:   ↓           ↓         ↓
         0           300        600ms
         (leading)   (trailing) (trailing)
```

---

## 🧠 Memory Behavior

```
Closure allocations per debounce/throttle:

Single debounce() call:
- 1 JSFunction (debounced) — ~50 bytes
- 1 Context { timer, lastArgs, fn, delay, leading, trailing } — ~80 bytes
- Total: ~130 bytes (persists as long as debounced fn is referenced)

Timer while pending:
- 1 timer handle in browser/libuv timer heap — small
- The timer's callback closure captures 'debounced' context
- lastArgs captured: retains last event args until debounce fires

Anti-pattern: creating debounce inside render function
function Component() {
  const handleInput = debounce(fn, 300)  // NEW closure EVERY render!
  // Each render: old closure leaked until GC
  // Fix: use useMemo or useCallback
}
```

---

## 📐 ASCII Diagram — Debounce vs Throttle Timeline

```
User events (resize): █ █ █ █ █ █ █ █ █ █ █ █ █ (continuous)

DEBOUNCE (300ms): Fires ONCE after stream ends
                  ────────────────────────────────[FIRE]───

THROTTLE (300ms): Fires every 300ms regardless
                  [FIRE]──────────[FIRE]──────────[FIRE]───

rAF THROTTLE: Fires every frame (16.7ms)
              [F][F][F][F][F][F][F][F][F][F][F][F] (60fps)
```

---

## 🔍 Code Examples

### Example 1 — Production Debounce for Search

```javascript
// React search input with debounce
function SearchComponent() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  
  // CORRECT: useMemo to avoid recreating debounce on every render
  const debouncedSearch = useMemo(
    () => debounce(async (q) => {
      if (!q.trim()) { setResults([]); return }
      try {
        const data = await fetch(`/api/search?q=${encodeURIComponent(q)}`)
        const json = await data.json()
        setResults(json.results)
      } catch (e) {
        console.error('Search failed', e)
      }
    }, 300, { leading: false, trailing: true }),
    [] // Empty deps: create once
  )
  
  // IMPORTANT: Cancel pending debounce on unmount
  useEffect(() => () => debouncedSearch.cancel(), [debouncedSearch])
  
  return (
    <input
      onChange={e => {
        const q = e.target.value
        setQuery(q)
        debouncedSearch(q)
      }}
      value={query}
    />
  )
}
```

### Example 2 — Scroll Throttle with rAF

```javascript
function useScrollPosition(onScroll) {
  const rafId = useRef(null)
  const lastPosition = useRef({ x: 0, y: 0 })
  
  useEffect(() => {
    function handleScroll() {
      if (rafId.current) return  // Already scheduled
      
      rafId.current = requestAnimationFrame(() => {
        rafId.current = null
        const position = { x: window.scrollX, y: window.scrollY }
        
        // Only call if position actually changed
        if (position.x !== lastPosition.current.x || 
            position.y !== lastPosition.current.y) {
          lastPosition.current = position
          onScroll(position)
        }
      })
    }
    
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => {
      window.removeEventListener('scroll', handleScroll)
      cancelAnimationFrame(rafId.current)
    }
  }, [onScroll])
}
```

### Example 3 — Timer Drift Issue with setInterval

```javascript
// setInterval drift in real-time applications
class PreciseTimer {
  constructor(callback, intervalMs) {
    this.callback = callback
    this.intervalMs = intervalMs
    this.expected = null
    this.timeout = null
  }
  
  start() {
    this.expected = Date.now() + this.intervalMs
    this.timeout = setTimeout(this._step.bind(this), this.intervalMs)
  }
  
  _step() {
    const drift = Date.now() - this.expected
    this.callback(drift)
    
    this.expected += this.intervalMs
    // Adjust next timeout by drift
    const nextDelay = Math.max(0, this.intervalMs - drift)
    this.timeout = setTimeout(this._step.bind(this), nextDelay)
  }
  
  stop() {
    clearTimeout(this.timeout)
  }
}

// Usage: stock price ticker, audio scheduler, WebRTC keepalive
const timer = new PreciseTimer(() => sendHeartbeat(), 1000)
timer.start()
```

---

## 💥 Production Failures

### Failure 1 — Debounce Not Cancelled on Unmount (React)

```javascript
// Memory leak + stale state update after unmount
function DataFetcher({ searchTerm }) {
  const [data, setData] = useState(null)
  
  // BUG: If component unmounts while debounce is pending,
  // the callback fires after unmount and calls setData
  // → React warning: "Can't perform a React state update on an unmounted component"
  
  const debouncedFetch = debounce(async (term) => {
    const result = await fetch(`/api?q=${term}`)
    setData(await result.json())  // This may fire after unmount!
  }, 500)
  
  useEffect(() => {
    debouncedFetch(searchTerm)
    // MISSING: return () => debouncedFetch.cancel()
  }, [searchTerm])
}
```

### Failure 2 — Throttle Too Aggressive on Mobile

```javascript
// Desktop: 60fps resize events every 16ms → throttle at 100ms = good
// Mobile: resize fires differently, throttle at 100ms may miss important changes
// Touch scroll on iOS: events fire at 60fps but can be batched

// Fix: Adaptive throttling based on device capability
const THROTTLE_INTERVAL = navigator.hardwareConcurrency > 4 ? 16 : 33
const handleResize = throttle(updateLayout, THROTTLE_INTERVAL)
```

---

## ⚠️ Edge Cases

### `this` Context in Debounced Methods

```javascript
class SearchEngine {
  constructor() {
    this.results = []
    // Arrow function debounce to preserve `this`
    this.debouncedSearch = debounce((...args) => this.search(...args), 300)
    
    // OR: bind before debouncing
    this.debouncedSearch2 = debounce(this.search.bind(this), 300)
  }
  
  search(query) {
    // `this` = SearchEngine instance
    this.results = performSearch(query)
  }
}

// Don't debounce like this — `this` context lost:
const engine = new SearchEngine()
const broken = debounce(engine.search, 300)  // `this` = undefined
```

---

## 🏢 Industry Best Practices

1. **Use rAF throttle for visual updates** — More accurate than `throttle(fn, 16)`.
2. **Always cancel on component unmount** — Memory leak prevention.
3. **Consider leading edge** — For UX, leading-edge debounce gives immediate feedback.
4. **Use lodash implementations** — Battle-tested, handles edge cases like flush/cancel.
5. **Monitor throttle effectiveness** — Log how many events were throttled vs executed.

## ⚖️ Trade-offs

| Pattern | Responsiveness | Call Frequency | Use Case |
|---------|---------------|----------------|---------|
| Debounce (trailing) | Delayed | Once (after pause) | Autocomplete, form validation |
| Debounce (leading) | Immediate | Once (then pauses) | Submit button, click |
| Throttle | Immediate | Periodic | Scroll, resize, mousemove |
| rAF Throttle | Immediate | 60fps max | Animations, visual updates |

## 💼 Interview Questions (With Solutions)

**Q1: What's the difference between leading and trailing edge debounce?**
> Leading edge: calls immediately on the first event, then ignores subsequent events until the quiet period ends. Trailing edge: waits for the quiet period, then calls with the LAST event's arguments. Leading is better for UX responsiveness; trailing is better for "process final state" use cases like autocomplete where you want the complete typed query.

**Q2: Why might `throttle(fn, 1000/60)` not produce exactly 60fps?**
> `setTimeout` has minimum resolution (~1ms) and is subject to timer clamping (4ms after 5 nesting levels). It's not synchronized with the browser's rendering pipeline. On a 120Hz display, `throttle(fn, 16)` would fire twice per rendered frame. `requestAnimationFrame` is the correct solution for display-synchronized throttling.

## 🧩 Practice Problem

Implement `debounce` with `maxWait` (lodash behavior):
```javascript
function debounce(fn, delay, { maxWait } = {}) {
  let timer = null
  let lastArgs = null
  let firstCallTime = null
  
  return function debounced(...args) {
    const now = Date.now()
    lastArgs = args
    
    if (!firstCallTime) firstCallTime = now
    
    clearTimeout(timer)
    
    const timeSinceFirst = now - firstCallTime
    const remainingMaxWait = maxWait ? maxWait - timeSinceFirst : Infinity
    const timeoutDelay = Math.min(delay, remainingMaxWait)
    
    timer = setTimeout(() => {
      timer = null
      firstCallTime = null
      fn.apply(this, lastArgs)
    }, timeoutDelay)
  }
}
```

## 🔗 Navigation

**Prev:** [04_Concurrency_Model.md](04_Concurrency_Model.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [06_Currying.md](06_Currying.md)
