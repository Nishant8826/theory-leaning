# 📌 02 — Reflow & Repaint

## 🧠 Concept Explanation

(See also Browser/05_Rendering_Pipeline.md)

**Reflow (Layout):** Recalculating the position and geometry of all elements. Expensive — affects all descendants and ancestors. Triggered by: DOM structure changes, CSS geometry changes (width, height, padding), reading layout properties after writes.

**Repaint (Paint):** Redrawing pixels for elements whose geometry hasn't changed but appearance has (color, background, border-radius). Less expensive than reflow but still costly.

**Composite:** GPU layers composited without touching layout or paint. Essentially free.

## 🔬 Internal Mechanics

### What Triggers Each Phase

```
Layout triggers (reflow everything in the tree):
  Adding/removing DOM elements
  display, position, width, height, padding, margin, font-size, border
  Reading: offsetWidth, offsetHeight, clientWidth, scrollWidth, getBoundingClientRect()
  
Paint triggers (repaint affected elements):
  color, background, box-shadow, border-color, visibility
  outline, text-shadow
  
Composite only (cheapest):
  transform: translateX/Y/Z, rotate, scale
  opacity
  filter (with GPU-accelerated filters)
  will-change (promotes to own layer)
```

### The Invalidation Chain

```
Write: element.style.width = '100px'
  → Style recalculation (needs new computed styles)
  → Layout (geometry changed)
  → Paint (element appearance changed)
  → Composite

Read: element.offsetWidth (after above write)
  → FORCED SYNCHRONOUS layout! Browser cannot return stale value
  → Must complete layout before returning
  → This is the layout thrash pattern
```

## 🔍 Code Examples

### Layout Thrash Detection Tool

```javascript
// Detect layout thrash in development
function detectThrash() {
  let writePhase = false
  let thrashCount = 0
  
  const observer = new MutationObserver(() => {
    writePhase = true
    requestAnimationFrame(() => { writePhase = false })
  })
  
  observer.observe(document.body, { 
    subtree: true, 
    attributes: true,
    attributeFilter: ['style', 'class']
  })
  
  // Proxy expensive reads to detect thrash
  const layoutProps = ['offsetWidth', 'offsetHeight', 'offsetTop', 'offsetLeft', 
                       'scrollWidth', 'scrollHeight', 'clientWidth', 'clientHeight']
  
  layoutProps.forEach(prop => {
    const original = Object.getOwnPropertyDescriptor(HTMLElement.prototype, prop)
    Object.defineProperty(HTMLElement.prototype, prop, {
      get() {
        if (writePhase) {
          thrashCount++
          console.warn(`Layout thrash: reading ${prop} after write`, new Error().stack)
        }
        return original.get.call(this)
      }
    })
  })
}

// Only in development!
if (process.env.NODE_ENV === 'development') detectThrash()
```

### FastDOM Pattern

```javascript
// FastDOM: batch DOM reads and writes
class FastDOM {
  constructor() {
    this.reads = []
    this.writes = []
    this.scheduled = false
  }
  
  measure(fn) {
    this.reads.push(fn)
    this.schedule()
  }
  
  mutate(fn) {
    this.writes.push(fn)
    this.schedule()
  }
  
  schedule() {
    if (this.scheduled) return
    this.scheduled = true
    requestAnimationFrame(() => this.flush())
  }
  
  flush() {
    // ALL reads first (no write-read interleaving!)
    const reads = this.reads.splice(0)
    reads.forEach(fn => fn())
    
    // THEN all writes
    const writes = this.writes.splice(0)
    writes.forEach(fn => fn())
    
    this.scheduled = false
    
    // If new tasks were added during flush:
    if (this.reads.length || this.writes.length) this.schedule()
  }
}

const fastDOM = new FastDOM()

// Usage:
fastDOM.measure(() => {
  const height = element.offsetHeight
  fastDOM.mutate(() => {
    element.style.height = height + 10 + 'px'
  })
})
```

## 💥 Production Failure — Infinite Scroll Layout Thrash

```javascript
// Anti-pattern: common in lazy infinite scroll implementations
function updatePositions(items) {
  items.forEach((item, i) => {
    const rect = item.getBoundingClientRect()  // READ
    item.style.top = rect.top + window.scrollY + 'px'  // WRITE
    // Next iteration: READ after WRITE → forced layout per item
    // 100 items = 100 forced layouts per scroll event
  })
}

// Fix: separate reads from writes
function updatePositions(items) {
  const rects = items.map(item => item.getBoundingClientRect())  // ALL reads
  items.forEach((item, i) => {
    item.style.top = rects[i].top + window.scrollY + 'px'  // ALL writes
  })
}
```

## 🏢 Industry Best Practices

1. **Use Chrome Performance tab** — "Recalculate Style", "Layout", "Paint" events show cost.
2. **Use FastDOM or batch manually** — All reads then all writes.
3. **CSS class toggle over inline styles** — One invalidation instead of N.
4. **virtual-dom/key reconciliation** — Frameworks minimize DOM mutations.
5. **Use CSS `contain`** — `contain: layout` tells browser: changes inside don't affect outside.

## 💼 Interview Questions

**Q1: What CSS property prevents a container's layout changes from affecting the rest of the page?**
> `contain: layout` (CSS Containment). This tells the browser that changes inside the element don't affect layout outside it, and vice versa. This allows the browser to scope layout recalculations to just the contained element's subtree. It's very effective for independent widgets, infinite scroll containers, and dynamic list items. `contain: strict` provides the strongest isolation (layout + paint + style + size).

## 🔗 Navigation

**Prev:** [01_Code_Optimization.md](01_Code_Optimization.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Memory_Leaks.md](03_Memory_Leaks.md)
