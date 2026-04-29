# 📌 02 — Event Delegation

## 🧠 Concept Explanation

Event delegation is a pattern where a single event listener on a parent element handles events for all its children, using the **event bubbling** mechanism. Instead of attaching `N` listeners for `N` children, you attach 1 listener to an ancestor.

The event model in browsers has three phases:
1. **Capture phase** — Event travels from `window` → `document` → ... → target
2. **Target phase** — Event is at the target element
3. **Bubble phase** — Event travels back up from target → ... → `document` → `window`

Delegation exploits the bubble phase.

## 🔬 Internal Mechanics (Blink)

### Event Dispatch Cost

Each event listener registration creates a C++ `EventListener` object and adds it to the element's `EventListenerList`. The memory cost scales linearly with listener count.

**1000 buttons with individual listeners:**
- 1000 EventListener objects
- 1000 closure objects (JS closures capturing handler state)
- V8 must GC all 1000 closures when buttons are removed

**1 delegated listener:**
- 1 EventListener object
- 1 closure

### `event.target` vs `event.currentTarget`

```
event.target        = the element that ORIGINALLY received the event (deepest element clicked)
event.currentTarget = the element whose listener is currently executing (where delegation is set up)
```

## 🔁 Execution Flow

```javascript
document.getElementById('list').addEventListener('click', handler)

// User clicks on a <button> inside a <li> inside the list

// Capture phase: window → document → html → body → list → li → button
// Target phase: button (target)
// Bubble phase: button → li → list (← HANDLER FIRES HERE) → body → html → document → window
```

## 📐 ASCII Diagram

```
┌─────────────────────────────────────────────┐
│  ul#list ← Single listener here             │
│  ┌────────┐ ┌────────┐ ┌────────┐           │
│  │  li    │ │  li    │ │  li    │           │
│  │ ┌────┐ │ │ ┌────┐ │ │ ┌────┐ │           │
│  │ │btn │ │ │ │btn │ │ │ │btn │ │           │
│  │ └────┘ │ │ └────┘ │ │ └────┘ │           │
│  └────────┘ └────────┘ └────────┘           │
│                                              │
│  Click bubbles up → caught at #list          │
└─────────────────────────────────────────────┘
```

## 🔍 Code Examples

### Example 1 — Basic Delegation Pattern

```javascript
const list = document.getElementById('todo-list')

list.addEventListener('click', function(event) {
  // event.target = the element actually clicked
  // We need to find the relevant ancestor
  
  const item = event.target.closest('.todo-item')  // Traverse up to find target
  if (!item) return  // Clicked outside any todo-item
  
  const action = event.target.dataset.action
  
  switch(action) {
    case 'delete':
      item.remove()
      break
    case 'complete':
      item.classList.toggle('done')
      break
    case 'edit':
      item.contentEditable = 'true'
      item.focus()
      break
  }
})
```

### Example 2 — Delegation with Dynamic Content

```javascript
// The key benefit: new items added to list are automatically handled
class TodoList {
  constructor(container) {
    this.container = container
    this.items = []
    
    // ONE listener handles ALL items, past and future
    this.container.addEventListener('click', this.handleClick.bind(this))
    this.container.addEventListener('change', this.handleChange.bind(this))
    this.container.addEventListener('input', this.handleInput.bind(this))
  }
  
  handleClick(e) {
    const btn = e.target.closest('[data-action]')
    if (!btn) return
    
    const item = btn.closest('[data-id]')
    const id = item?.dataset.id
    const action = btn.dataset.action
    
    if (action === 'delete') this.deleteItem(id)
    if (action === 'toggle') this.toggleItem(id)
  }
  
  addItem(item) {
    this.items.push(item)
    // No new event listener needed — delegation handles it!
    this.container.insertAdjacentHTML('beforeend', this.renderItem(item))
  }
  
  renderItem(item) {
    return `
      <div class="todo" data-id="${item.id}">
        <span>${item.text}</span>
        <button data-action="toggle">✓</button>
        <button data-action="delete">✗</button>
      </div>
    `
  }
}
```

### Example 3 — Capture vs Bubble Phase

```javascript
// Capture phase: useful for intercepting events before target
document.addEventListener('click', function(e) {
  console.log('Capture: document')
}, true)  // ← true = capture phase

document.addEventListener('click', function(e) {
  console.log('Bubble: document')
}, false)  // ← false (default) = bubble phase

// For: click on button inside div inside document
// Output: 
// Capture: document (capture, top-down)
// [Any capture listeners on intermediate elements]
// [Target phase listeners]
// Bubble: document (bubble, bottom-up)

// Use capture for:
// - Focus events (don't bubble naturally)
// - Implementing "click outside to close" patterns correctly
// - Intercepting events before they reach targets
```

### Example 4 — `stopPropagation` vs `stopImmediatePropagation`

```javascript
button.addEventListener('click', function(e) {
  e.stopPropagation()  // Stops bubbling — parent delegation WON'T see this click
  // Other listeners on THIS button still run
})

button.addEventListener('click', function(e) {
  e.stopImmediatePropagation()  // Stops bubbling + other listeners on this element
  // Subsequent listeners on the same button DON'T run
})

// Performance note: stopPropagation() aborts the bubbling phase early
// Slightly cheaper (no further event dispatch needed) but breaks delegation!
```

## 💥 Production Failures

### Failure 1 — Memory Leak via Unremoved Listeners

```javascript
// Each component adds listeners but never removes them
class Component {
  mount() {
    this.el = document.createElement('div')
    document.body.appendChild(this.el)
    
    // WRONG: References 'this' → prevents GC of this component
    document.addEventListener('keydown', this.handleKey.bind(this))
    // 'bind' creates a NEW function each time!
    // document holds reference → this component never GC'd even after unmount
  }
  
  unmount() {
    document.body.removeChild(this.el)
    // WRONG: Removed from DOM but listener still in document!
    // document.removeEventListener needs the SAME function reference
  }
}

// Fix:
class ComponentFixed {
  mount() {
    this.el = document.createElement('div')
    document.body.appendChild(this.el)
    this._handleKey = this.handleKey.bind(this)  // Save reference
    document.addEventListener('keydown', this._handleKey)
  }
  
  unmount() {
    document.body.removeChild(this.el)
    document.removeEventListener('keydown', this._handleKey)  // Same reference
  }
}
```

### Failure 2 — Delegation Breaks with `stopPropagation`

```javascript
// Third-party widget uses stopPropagation:
widget.querySelector('.item').addEventListener('click', function(e) {
  e.stopPropagation()  // "Isolate" the widget
  // But now: YOUR delegation handler on parent NEVER sees these clicks!
})

// Your delegation:
container.addEventListener('click', function(e) {
  // This NEVER fires for clicks inside widget — stopPropagation killed bubbling
})

// Fix: Use capture phase for your delegation
container.addEventListener('click', function(e) {
  // Capture fires BEFORE stopPropagation in bubble phase
  // You intercept the event on the way DOWN
}, true)  // ← capture phase
```

## ⚠️ Edge Cases

### `closest()` Performance

```javascript
// element.closest() walks UP the DOM tree
// O(depth) where depth = distance from target to delegating ancestor
// For very deep DOMs: could be slow if called frequently

// Alternative: check tagName or dataset directly
list.addEventListener('click', function(e) {
  // Fast: direct check on target
  if (e.target.tagName === 'BUTTON' && e.target.classList.contains('delete')) {
    handleDelete(e.target)
  }
})
```

### Event Delegation and SVG

```javascript
// SVG elements have different event models
// SVG text/path elements ARE event targets
// .closest() works but tagName is lowercase in SVG ('circle' not 'CIRCLE')

svgElement.addEventListener('click', function(e) {
  const circle = e.target.closest('circle')  // lowercase for SVG
  if (circle) handleCircleClick(circle)
})
```

## 🏢 Industry Best Practices

1. **Always use delegation for list-like UI** — Todo lists, data tables, menus.
2. **Save bound function references** — `this.handler = fn.bind(this)` before addEventListener.
3. **Always remove listeners in cleanup** — React useEffect cleanup, Angular ngOnDestroy.
4. **Use `{ once: true }` for one-time listeners** — Auto-removes after first fire.
5. **Use `{ passive: true }` for scroll/touch** — Tells browser you won't call preventDefault, enabling GPU scroll optimization.

## ⚖️ Trade-offs

| Approach | Memory | Flexibility | Dynamic Content | stopPropagation Safe |
|----------|--------|-------------|-----------------|----------------------|
| Direct listeners | High | High | No (manual add) | Yes |
| Delegation (bubble) | Low | Medium | Yes | No |
| Delegation (capture) | Low | High | Yes | Yes |

## 💼 Interview Questions

**Q1: Why does `removeEventListener` fail if you pass an anonymous function?**
> `removeEventListener` requires the EXACT SAME function reference as was passed to `addEventListener`. Anonymous functions create a new function object each time they're evaluated, so the reference is always different. The browser can't match it to any registered listener. Always save the function reference if you need to remove it later.

**Q2: When would you choose capture phase over bubble phase for delegation?**
> Use capture phase when: (1) the target element or its children call `stopPropagation()` preventing bubbling; (2) you need to intercept events before the target handles them; (3) for events that don't bubble (`focus`, `blur`, `mouseenter`, `mouseleave`) — though `focusin`/`focusout` DO bubble and are better for delegation.

## 🔗 Navigation

**Prev:** [01_DOM_Manipulation.md](01_DOM_Manipulation.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Browser_Storage.md](03_Browser_Storage.md)
