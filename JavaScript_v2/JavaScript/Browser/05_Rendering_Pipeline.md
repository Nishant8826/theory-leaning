# 📌 05 — Rendering Pipeline

## 🧠 Concept Explanation

The browser's rendering pipeline converts HTML/CSS/JS into pixels on the screen. Understanding it is essential for achieving smooth 60fps animations, avoiding layout thrashing, and knowing which CSS properties are "free" (GPU-composited) vs "expensive" (trigger layout).

The pipeline (Critical Rendering Path):
```
Parse HTML → DOM Tree
Parse CSS  → CSSOM Tree
              ↓
DOM + CSSOM → Render Tree (only visible elements)
              ↓
          Layout (calculate geometry: position, size)
              ↓
          Paint (generate draw records: colors, borders, shadows)
              ↓
          Composite (GPU assembles layers into final image)
```

## 🔬 Internal Mechanics (Blink + Compositor Thread)

### Thread Architecture

The browser uses multiple threads for rendering:

```
Main Thread (JS + Style + Layout + Paint):
  JavaScript execution
  Style recalculation (CSS matching)
  Layout tree construction
  Paint record generation

Compositor Thread (GPU-accelerated):
  Layer management
  Scroll (can be compositor-only = no main thread involvement!)
  CSS transform animations (can run on compositor!)
  Rasterization (converting paint records to pixels)

GPU Process:
  Texture upload
  Final composition to display
```

**Key insight:** Animations/scrolling that run on the **compositor thread** never block on JavaScript — they're butter-smooth even if the main thread is busy.

### Layer Promotion

Elements can be "promoted" to their own compositor layer:
```css
/* Promotes to own layer: */
transform: translateZ(0)
will-change: transform
will-change: opacity
```

Layer promotion:
- Creates a separate GPU texture for the element
- Compositor can transform/animate without re-painting
- BUT: each layer uses GPU memory — don't promote everything!

## 🔁 Execution Flow — A Single Frame

```
Frame budget: ~16.67ms (60fps) or ~11.1ms (90fps) or ~8.33ms (120fps)

[1. Input event handling] ~0-5ms
[2. JavaScript execution] ~0-10ms (includes requestAnimationFrame callbacks)
[3. Style recalculation] ~0-2ms (CSS selector matching, computed values)
[4. Layout] ~0-5ms (geometry calculation for dirty elements)
[5. Paint] ~0-2ms (generating draw records — not actual pixel drawing!)
[6. Composite] ~0-2ms (GPU layer composition)

Total budget: 16.67ms
If any step exceeds budget → JANK (dropped frame)
```

## 📐 ASCII Diagram — Pipeline Stages

```
HTML bytes → Tokens → DOM nodes
CSS bytes  → Tokens → CSSOM nodes
                  ↓ (both complete)
             Render Tree (visible nodes with computed styles)
                  ↓
         Layout (x, y, width, height of each node)
                  ↓
         Paint (ordered list of drawing instructions)
                  ↓ Layers separated here
         Composite (GPU assembles layers)
                  ↓
              Screen pixels

What invalidates what:
  DOM mutation → Render Tree + Layout + Paint + Composite
  CSS class change → Style + Layout + Paint + Composite (maybe less)
  CSS transform only → Composite ONLY! (cheapest)
  CSS opacity only → Composite ONLY! (cheapest)
```

## 🔍 Code Examples

### Example 1 — CSS Properties Cost (Compositor vs Layout vs Paint)

```javascript
// CHEAPEST: Compositor-only properties (no layout, no paint)
element.style.transform = 'translateX(100px)'   // GPU: free!
element.style.opacity = 0.5                      // GPU: free!

// EXPENSIVE: Layout-triggering properties (full pipeline)
element.style.width = '100px'         // Triggers layout + paint + composite
element.style.height = '100px'        // Layout
element.style.padding = '10px'        // Layout
element.style.margin = '10px'         // Layout
element.style.fontSize = '16px'       // Layout
element.style.display = 'block'       // Layout

// MEDIUM: Paint-triggering (no layout, but still CPU work)
element.style.color = 'red'           // Paint (no geometry change)
element.style.background = 'blue'    // Paint
element.style.boxShadow = '0 2px 4px rgba(0,0,0,0.5)' // Paint (expensive!)

// ANIMATION RULE: Always animate transform and opacity, not width/height
```

### Example 2 — Forced Synchronous Layout Detection

```javascript
// Chrome DevTools: Performance tab will show "Layout" events
// Look for "Forced reflow while executing JavaScript" warning

// Anti-pattern (triggers forced layout on each iteration):
function badResize(elements) {
  elements.forEach(el => {
    el.style.width = el.offsetWidth + 10 + 'px'  // READ then WRITE per element
  })
}

// Good (reads then writes):
function goodResize(elements) {
  const widths = elements.map(el => el.offsetWidth)  // All reads
  elements.forEach((el, i) => {
    el.style.width = widths[i] + 10 + 'px'           // All writes
  })
}

// Alternatively: use CSS only (no JS)
elements.forEach(el => el.classList.add('wider'))
/* CSS: .wider { width: calc(100% + 10px) } */
```

### Example 3 — will-change and Layer Promotion

```javascript
// Promote before animation, demote after
function animateElement(el) {
  el.style.willChange = 'transform'  // Hint to browser: promote now
  
  el.animate([
    { transform: 'translateX(0)' },
    { transform: 'translateX(200px)' }
  ], {
    duration: 500,
    easing: 'ease-in-out'
  }).addEventListener('finish', () => {
    el.style.willChange = 'auto'  // Remove promotion after animation
  })
}

// WARNING: will-change is NOT free
// It allocates a GPU texture layer immediately
// Only use for elements ABOUT TO animate
// Overusing will-change exhausts GPU memory
```

### Example 4 — GPU Layer Debugging

```javascript
// Chrome DevTools: Layers panel shows all compositor layers
// Rendering tab: "Layer borders" checkbox shows layer boundaries
// "Scrolling performance issues" checkbox shows non-composited layers

// Programmatic layer inspection:
// Use Performance tab → Record → Look at "Layers" in frame details

// Measure layout/paint cost:
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log(entry.name, entry.startTime, entry.duration)
  }
})
observer.observe({ entryTypes: ['layout-shift', 'paint'] })
```

## 💥 Production Failures

### Failure 1 — Scroll Jank from Non-Composited Scroll

```javascript
// Problem: scroll listener doing layout work
window.addEventListener('scroll', () => {
  // Reading scrollY + layout property = main thread work during scroll
  const offset = window.scrollY
  const parallaxEl = document.querySelector('.parallax')
  parallaxEl.style.transform = `translateY(${offset * 0.5}px)`
  
  // If browser can't run this on compositor thread:
  // Scroll is NOT smooth — jank every frame!
})

// Fix: CSS-only parallax (compositor-thread scroll)
// Requires overflow: hidden on container + perspective
// Or: use Intersection Observer for scroll-triggered effects
```

### Failure 2 — CLS (Cumulative Layout Shift) from Late Content

```javascript
// Loading image without dimensions causes layout shift:
// Before: <img src="logo.png"> (no width/height)
// Page renders → img loads → EVERYTHING reflows to make room

// Fix 1: Always set width/height on images
// <img width="400" height="300" src="logo.png">
// Browser reserves space before image loads

// Fix 2: aspect-ratio CSS
// img { aspect-ratio: 4/3; width: 100%; }

// Measure CLS:
new PerformanceObserver((list) => {
  let cls = 0
  list.getEntries().forEach(entry => {
    if (!entry.hadRecentInput) cls += entry.value
  })
  console.log('CLS:', cls)
}).observe({ entryTypes: ['layout-shift'] })
```

## ⚠️ Edge Cases

### `requestAnimationFrame` is NOT always called at 60fps

```javascript
// rAF fires at the DISPLAY refresh rate:
// Desktop: usually 60Hz (16.67ms)
// Gaming monitors: 144Hz, 165Hz, 240Hz (less time per frame!)
// Mobile: 60Hz or 120Hz (ProMotion, High Refresh Rate)
// Hidden/background tabs: 0Hz (paused!)
// Low-power mode: may reduce to 30Hz

// Use DOMHighResTimeStamp from rAF for delta time:
let lastTime = 0
function animate(timestamp) {
  const delta = timestamp - lastTime  // Actual ms since last frame
  lastTime = timestamp
  
  // Move at 100px/second regardless of refresh rate
  element.style.transform = `translateX(${position}px)`
  position += 100 * (delta / 1000)  // pixels per second × seconds per frame
  
  requestAnimationFrame(animate)
}
```

## 🏢 Industry Best Practices

1. **Only animate `transform` and `opacity`** — All other properties trigger layout or paint.
2. **Avoid forced synchronous layout** — Batch reads, then writes.
3. **Use `will-change` sparingly** — Only for elements about to animate. Remove after.
4. **Measure with Performance tab** — Real data beats intuition.
5. **Target 60fps** — Budget: 16ms total, ~10ms for JS, ~6ms for render pipeline.
6. **Use `content-visibility: auto`** — Skip rendering for off-screen content.

## ⚖️ Trade-offs

| Approach | Performance | Flexibility | Complexity |
|----------|------------|-------------|-----------|
| CSS animations | Best (compositor) | Limited | Low |
| Web Animations API | Good | Medium | Medium |
| JS `style.transform` + rAF | Good | High | Medium |
| JS `style.left/top/width` | Poor (layout) | High | Low |
| Canvas/WebGL | Best for complex | Very High | Very High |

## 💼 Interview Questions

**Q1: What is the Critical Rendering Path and how do you optimize it?**
> The CRP is the sequence: HTML parsing → DOM, CSS parsing → CSSOM, DOM+CSSOM → Render Tree, Layout, Paint, Composite. Blocking the CRP means the page doesn't become visible until all steps complete. Optimizations: (1) Reduce render-blocking resources (defer non-critical CSS/JS); (2) Minimize render tree size (remove hidden elements); (3) Minimize layout scope (prefer compositor-only properties); (4) Use `link rel=preload` for critical fonts/images.

**Q2: Why is `transform: translateX()` cheaper than `left: 100px`?**
> `left` is a layout property — changing it invalidates the layout tree, requiring style recalculation, layout, paint, and composite. `transform` is a compositor property — it doesn't affect the document flow or layout. The browser handles transforms entirely on the compositor thread using GPU matrix multiplication on the pre-rasterized layer texture. No main thread work, no layout or paint — just a cheap GPU operation.

## 🔗 Navigation

**Prev:** [04_Service_Workers.md](04_Service_Workers.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [06_CORS.md](06_CORS.md)
