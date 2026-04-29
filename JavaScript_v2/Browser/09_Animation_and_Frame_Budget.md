# 📌 09 — Animation & Frame Budget

## 🧠 Concept Explanation

Smooth animation requires consistently delivering frames within the display's refresh interval. At 60fps: 16.67ms per frame. At 120fps: 8.33ms. Missing this deadline causes **jank** — visible stuttering.

The 16ms frame budget is split:
- ~10ms for JavaScript (including rAF callbacks)
- ~6ms for style, layout, paint, composite

Going over budget in any phase drops the frame.

## 🔬 Internal Mechanics

### requestAnimationFrame Scheduling

`rAF` callbacks run in the "update the rendering" step of the event loop:
1. After tasks and microtasks complete
2. Before style/layout/paint
3. The browser may batch multiple callbacks if it decides to skip a frame

The timestamp passed to rAF is the **expected frame time** (DOMHighResTimeStamp), not the actual current time. This ensures animation calculations use consistent frame timing.

### FLIP Animation Technique

**F**irst, **L**ast, **I**nvert, **P**lay — enables smooth animations of expensive layout changes:

```javascript
function flipAnimation(el, newPosition) {
  // FIRST: Record initial state
  const first = el.getBoundingClientRect()
  
  // LAST: Apply final state (even if it causes layout)
  el.classList.add('new-position')
  const last = el.getBoundingClientRect()
  
  // INVERT: Apply inverse transform (makes element appear at FIRST position)
  const deltaX = first.left - last.left
  const deltaY = first.top - last.top
  el.style.transform = `translate(${deltaX}px, ${deltaY}px)`
  el.style.transition = 'none'
  
  // PLAY: Animate to identity transform (compositor-only = smooth!)
  requestAnimationFrame(() => {
    el.style.transition = 'transform 300ms ease'
    el.style.transform = ''  // Back to final position — compositor handles this
  })
}
```

## 🔍 Code Examples

### Example 1 — Smooth rAF Loop

```javascript
class AnimationLoop {
  constructor(updateFn) {
    this.updateFn = updateFn
    this.rafId = null
    this.lastTime = null
    this.paused = false
  }
  
  start() {
    if (this.rafId) return
    const frame = (timestamp) => {
      if (this.paused) { this.rafId = null; return }
      
      const delta = this.lastTime ? timestamp - this.lastTime : 0
      this.lastTime = timestamp
      
      this.updateFn(delta, timestamp)
      this.rafId = requestAnimationFrame(frame)
    }
    this.rafId = requestAnimationFrame(frame)
  }
  
  pause() { this.paused = true }
  resume() { if (!this.rafId) { this.paused = false; this.start() } }
  stop() { cancelAnimationFrame(this.rafId); this.rafId = null; this.lastTime = null }
}

// Usage:
const loop = new AnimationLoop((delta, timestamp) => {
  // delta = milliseconds since last frame
  // Move at 200px/second regardless of frame rate
  position.x += 200 * (delta / 1000)
  el.style.transform = `translateX(${position.x}px)`
})
loop.start()
```

### Example 2 — Long Task Detection and Yielding

```javascript
// Detect long tasks and yield during heavy computation
async function processHeavyWork(items) {
  const BUDGET = 10  // ms per chunk (leave 6ms for rendering)
  
  for (let i = 0; i < items.length; i++) {
    processItem(items[i])
    
    // Check frame budget
    if (i % 100 === 0) {  // Check every 100 items
      // Yield to allow rendering
      await new Promise(resolve => {
        // scheduler.yield() is the modern API (Chrome 129+)
        if ('scheduler' in globalThis && 'yield' in scheduler) {
          scheduler.yield().then(resolve)
        } else {
          setTimeout(resolve, 0)  // Fallback
        }
      })
    }
  }
}
```

### Example 3 — CSS Animation vs JS Animation

```javascript
// CSS animation: runs on compositor thread (60fps even if JS is busy)
el.style.animation = 'spin 1s linear infinite'
// @keyframes spin { to { transform: rotate(360deg) } }

// Web Animations API: also compositor-eligible
const anim = el.animate([
  { transform: 'rotate(0deg)' },
  { transform: 'rotate(360deg)' }
], {
  duration: 1000,
  iterations: Infinity,
  easing: 'linear'
})

// JS animation (rAF): main thread, can be interrupted by long tasks
function rotate() {
  angle += 2
  el.style.transform = `rotate(${angle}deg)`
  requestAnimationFrame(rotate)  // Blocked if JS is busy!
}
```

## 💥 Production Failure — Jank from Main Thread Blocking

```javascript
// Heavy JSON processing in rAF callback → frame drop
requestAnimationFrame(() => {
  const data = JSON.parse(hugeJSON)  // 50ms! Blocks this entire frame
  updateChart(data)
  // Browser: misses frame → 16ms delay becomes 66ms → visible stutter
})

// Fix 1: Move parsing to Worker
const worker = new Worker('./json-parser.js')
worker.onmessage = ({ data }) => {
  requestAnimationFrame(() => {
    updateChart(data)  // Parsed already, rAF callback is fast
  })
}
worker.postMessage(hugeJSON)

// Fix 2: Process during idle time
requestIdleCallback(() => {
  parsedData = JSON.parse(hugeJSON)
}, { timeout: 2000 })
```

## 🏢 Industry Best Practices

1. **Only transform and opacity** in rAF for animations.
2. **Use Web Animations API** instead of JS rAF loops when possible.
3. **Measure with Performance tab** — Identify long tasks causing jank.
4. **Target 60fps** — 10ms JS budget, 6ms render budget.
5. **Use `scheduler.yield()`** to break up long synchronous work.
6. **Profile on low-end devices** — Desktop CPU can hide problems mobile users face.

## 💼 Interview Questions

**Q1: What is the 16ms frame budget and how should it be divided?**
> At 60fps, each frame has 16.67ms total. Breakdown: ~10ms for JavaScript (DOM manipulation, business logic, rAF callbacks), ~2ms for style recalculation and layout, ~2ms for paint, ~2ms for composite. In practice, any single JavaScript task exceeding ~10ms risks dropping a frame. Long tasks (>50ms) are particularly noticeable as jank. Use the Performance panel's "Main" track to identify blocking tasks.

**Q2: What is the FLIP technique and why is it needed?**
> FLIP (First-Last-Invert-Play) enables animating expensive layout changes smoothly. Directly animating properties like `width`, `height`, or `top` triggers layout on every frame. FLIP: record initial position (First), apply final state instantly (Last), invert the transform to make it appear at the initial position (Invert), then animate the transform back to zero (Play). Since only `transform` is animated in the Play phase, it runs on the compositor thread — smooth at 60fps.

## 🔗 Navigation

**Prev:** [08_Intersection_Observer_and_Performance.md](08_Intersection_Observer_and_Performance.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [../NodeJS/01_Node_Architecture.md](../NodeJS/01_Node_Architecture.md)
