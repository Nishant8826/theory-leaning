# 📌 01 — DOM Manipulation

## 🧠 Concept Explanation

DOM manipulation is the performance-critical boundary between JavaScript and the browser's rendering engine. Every DOM access crosses the **C++/JavaScript bridge** — V8 executes JS but the DOM lives in Blink/WebKit's C++ heap. This crossing has measurable overhead.

## 🔬 Internal Mechanics (Blink + V8)

### The JS ↔ DOM Bridge

The DOM binding layer (called "Bindings" in Blink) creates V8 wrapper objects (JSObjects) that delegate to C++ DOM objects. When you access element.style, V8:
1. Calls the generated binding code (auto-generated from Web IDL)
2. Extracts the underlying C++ DOM node pointer from the JS wrapper
3. Calls the C++ getter on the DOM node
4. Wraps the result in another JS wrapper (or converts to primitive)

This is why element.offsetHeight is significantly slower than reading a plain JS property.

### Layout Invalidation

DOM mutations that affect layout (changing className, style, adding/removing children) mark the layout tree as "dirty." The browser does NOT recalculate layout immediately — it batches changes and recalculates before the next paint.

**Forced synchronous layout (Layout Thrashing):** If you READ a layout property (offsetWidth, getBoundingClientRect) AFTER writing to a property that invalidates layout, the browser must synchronously recalculate layout right then — even in the middle of your JavaScript.

`javascript
// Layout thrashing:
element.style.width = '100px'  // Write: invalidates layout
element.offsetWidth            // READ: forces synchronous layout NOW!
element.style.height = '100px' // Write: invalidates again
element.offsetHeight           // READ: forces synchronous layout AGAIN!
`

## 📐 ASCII Diagram — Rendering Pipeline

`
JS Code
  │ DOM mutations
  ▼
DOM Tree (C++ in Blink)
  │ computed style recalculation
  ▼
Render Tree / Layout Tree
  │ layout (geometry calculation)
  ▼
Paint records (what to draw)
  │ compositing
  ▼
GPU (display)
`

## 🔍 Code Examples

### Example 1 — DocumentFragment Batching

`javascript
// WRONG: Each append causes layout invalidation
const list = document.getElementById('list')
items.forEach(item => {
  const li = document.createElement('li')
  li.textContent = item.name
  list.appendChild(li)  // 1000 layout invalidations!
})

// CORRECT: DocumentFragment — one insertion
const fragment = document.createDocumentFragment()
items.forEach(item => {
  const li = document.createElement('li')
  li.textContent = item.name
  fragment.appendChild(li)  // Off-screen, no layout
})
list.appendChild(fragment)  // ONE insertion, ONE layout invalidation
`

### Example 2 — Batch Reads and Writes

`javascript
// Read-Write-Read pattern = layout thrashing
function layoutThrash(elements) {
  elements.forEach(el => {
    const height = el.offsetHeight  // READ (may force layout)
    el.style.height = height + 10 + 'px'  // WRITE (invalidates)
    // Next iteration's READ forces another layout
  })
}

// Read all, then write all
function neatLayout(elements) {
  const heights = elements.map(el => el.offsetHeight)  // All reads
  elements.forEach((el, i) => {
    el.style.height = heights[i] + 10 + 'px'            // All writes
  })
  // Only ONE potential forced layout (the reads batch)
}
`

### Example 3 — Efficient Style Manipulation

`javascript
// WRONG: Multiple style.property assignments
el.style.width = '200px'
el.style.height = '100px'
el.style.background = '#000'
el.style.border = '1px solid red'
// 4 style property writes — may trigger multiple style invalidations

// BETTER: className (one invalidation)
el.className = 'active expanded featured'

// BEST: classList for incremental changes
el.classList.add('active')     // Minimal invalidation
el.classList.toggle('hidden')

// For complex dynamic styles: cssText
el.style.cssText = 'width:200px;height:100px;background:#000'
`

## 💥 Production Failures

### Failure — Infinite Scroll Layout Thrashing

`javascript
// Infinite scroll with unvirtualized height calculation
function onScroll() {
  items.forEach((item, i) => {
    const rect = item.getBoundingClientRect()  // Forces layout every call!
    if (rect.top < window.innerHeight) {
      item.classList.add('visible')
    }
  })
}
// With 10,000 items: 10,000 layout recalculations per scroll event
// Fix: Use IntersectionObserver (see Browser/08_Intersection_Observer)
`

## ⚠️ Edge Cases

### cloneNode Deep vs Shallow

`javascript
const original = document.querySelector('.template')
const shallow = original.cloneNode(false)  // Clone element only, no children
const deep = original.cloneNode(true)      // Clone entire subtree
// Event listeners are NOT cloned by either
// Data attributes ARE cloned
// Inline styles ARE cloned
`

## 🏢 Industry Best Practices

1. **Batch DOM reads before writes** — Never interleave reads and writes.
2. **Use DocumentFragment** for bulk insertions.
3. **Use IntersectionObserver** instead of getBoundingClientRect in loops.
4. **Avoid layout properties in loops** — offsetWidth, offsetHeight, getBoundingClientRect.
5. **Use CSS classes** for style changes, not inline style properties.

## 💼 Interview Questions

**Q1: What is forced synchronous layout and how do you prevent it?**
> Forced synchronous layout occurs when JavaScript reads a layout-dependent property (offsetWidth, scrollTop, getBoundingClientRect) after writing a property that invalidates layout, before the browser has had a chance to batch-recalculate. The browser must synchronously compute layout in the middle of your JS to return an accurate value. Prevent it by batching all writes before all reads within the same task. Use rAF to separate write-then-read cycles across frames.

**Q2: Why is innerHTML faster than createElement for bulk insertion?**
> innerHTML parsing uses the browser's highly optimized HTML parser (written in C++) which can process many elements in a single parse pass. createElement creates elements one-by-one through the V8↔DOM bridge. For large amounts of HTML, innerHTML can be 10-100x faster. Trade-off: innerHTML has XSS risk (must sanitize), destroys existing DOM structure, and removes event listeners. Use it only with trusted content.

## 🔗 Navigation

**Prev:** [../Advanced/12_TypedArrays_and_ArrayBuffers.md](../Advanced/12_TypedArrays_and_ArrayBuffers.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [02_Event_Delegation.md](02_Event_Delegation.md)
