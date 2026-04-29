# 📌 08 — Intersection Observer & Performance

## 🧠 Concept Explanation

IntersectionObserver (IO) solves the classic "is this element visible?" problem without polling or scroll event layout thrashing. It uses the browser's compositor knowledge to detect element-viewport intersections asynchronously, off the main thread.

Before IO: developers polled `getBoundingClientRect()` in scroll handlers — forcing synchronous layout calculations every scroll event. IO eliminates this by delegating intersection detection to the browser's compositor thread.

## 🔬 Internal Mechanics

IntersectionObserver callbacks are **NOT microtasks** — they're delivered as a step in the event loop after layout and before paint (after rAF, part of the "update the rendering" algorithm). This timing ensures the intersection ratios are accurate for the current frame.

**Root margin:** The observation area can be expanded/contracted relative to the viewport (like CSS margin). Useful for pre-loading content just before it enters view.

**Threshold:** An array of ratios at which callbacks fire. `[0, 0.25, 0.5, 0.75, 1]` fires 5 times as an element scrolls into/out of view.

## 🔍 Code Examples

### Example 1 — Lazy Image Loading

```javascript
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return
    
    const img = entry.target
    img.src = img.dataset.src  // Replace placeholder with real src
    img.removeAttribute('data-src')
    imageObserver.unobserve(img)  // Stop watching after loading
  })
}, {
  root: null,           // Viewport
  rootMargin: '200px',  // Start loading 200px before entering view
  threshold: 0          // Fire as soon as ANY part enters view
})

document.querySelectorAll('img[data-src]').forEach(img => {
  imageObserver.observe(img)
})
```

### Example 2 — Infinite Scroll (Virtualized)

```javascript
class InfiniteList {
  constructor(container, fetchMore) {
    this.container = container
    this.fetchMore = fetchMore
    this.loading = false
    
    // Sentinel element at bottom of list
    this.sentinel = document.createElement('div')
    this.sentinel.style.height = '1px'
    container.appendChild(this.sentinel)
    
    const observer = new IntersectionObserver(async ([entry]) => {
      if (!entry.isIntersecting || this.loading) return
      this.loading = true
      await this.fetchMore()
      this.loading = false
    }, {
      root: container.scrollable,
      rootMargin: '300px',  // Pre-load 300px before sentinel is visible
      threshold: 0
    })
    
    observer.observe(this.sentinel)
  }
}
```

### Example 3 — Analytics Impression Tracking

```javascript
// Track when elements are viewed (50% visible for 1+ second)
class ImpressionTracker {
  constructor() {
    this.viewTimers = new Map()
    
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const el = entry.target
        const adId = el.dataset.adId
        
        if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
          // Element is 50%+ visible — start timer
          const timer = setTimeout(() => {
            this.trackImpression(adId, entry)
          }, 1000)  // Must stay visible for 1 second
          this.viewTimers.set(adId, timer)
        } else {
          // Element left view — cancel timer
          clearTimeout(this.viewTimers.get(adId))
          this.viewTimers.delete(adId)
        }
      })
    }, {
      threshold: [0, 0.5, 1.0]  // Callbacks at 0%, 50%, 100% visibility
    })
  }
  
  observe(el) { this.observer.observe(el) }
  
  trackImpression(adId, entry) {
    fetch('/api/impressions', {
      method: 'POST',
      body: JSON.stringify({
        adId,
        ratio: entry.intersectionRatio,
        timestamp: Date.now()
      })
    })
  }
}
```

## 💥 Production Failure — ResizeObserver Loop

```javascript
// ResizeObserver loop error: "ResizeObserver loop limit exceeded"
// Occurs when: resize callback changes element size → triggers resize → infinite loop

const ro = new ResizeObserver(entries => {
  entries.forEach(entry => {
    const { width } = entry.contentRect
    // BUG: Changing width triggers another resize observation → loop!
    entry.target.style.height = width + 'px'
  })
})

// Fix: Use rAF to break the synchronous loop
const ro2 = new ResizeObserver(entries => {
  requestAnimationFrame(() => {
    entries.forEach(entry => {
      const { width } = entry.contentRect
      entry.target.style.height = width + 'px'  // Now deferred, no loop
    })
  })
})
```

## 🏢 Industry Best Practices

1. **Use IO instead of scroll event + getBoundingClientRect** — Orders of magnitude more efficient.
2. **Unobserve after action** — For one-time events (lazy load), always `unobserve()`.
3. **Use rootMargin for pre-loading** — Trigger loading 200-300px before element enters view.
4. **Disconnect when done** — `observer.disconnect()` when the observing component unmounts.
5. **Batch multiple thresholds** — One observer can watch multiple elements efficiently.

## 💼 Interview Questions

**Q1: Why is IntersectionObserver more performant than scroll event + getBoundingClientRect?**
> `getBoundingClientRect()` forces a synchronous layout recalculation — the browser must compute geometry before returning. In a scroll handler (which may fire at 60fps+), this means forced layout every 16ms or more. IntersectionObserver works at the compositor level, using the browser's already-computed intersection data. Callbacks fire asynchronously after layout, at the browser's chosen timing — never blocking the main thread mid-scroll.

## 🔗 Navigation

**Prev:** [07_Web_Workers.md](07_Web_Workers.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [09_Animation_and_Frame_Budget.md](09_Animation_and_Frame_Budget.md)
