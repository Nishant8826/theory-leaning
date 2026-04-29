# 📌 02 — Reflow & Repaint

## 🌟 Introduction

When you change something on a website (like making a button bigger or changing its color), the browser has to do a lot of work to update the screen.

Think of it like **Building a House**:
1.  **Reflow (Layout):** The Architect. You decide to move a wall. Now you have to recalculate the size of every room, the plumbing, and the wiring. This is the **slowest** and hardest work.
2.  **Repaint (Paint):** The Painter. You just want to change the color of the wall. The rooms stay the same size; you just apply new paint. This is faster but still takes time.
3.  **Composite:** The Mover. You just want to move a chair. You don't change the wall or the paint; you just slide an object around. This is the **fastest** work (handled by the GPU).

---

## 🏗️ What Triggers Each Phase?

| Action | Phase | Cost |
| :--- | :--- | :--- |
| **Geometry:** `width`, `height`, `margin`, `padding`, `top`, `left`, `font-size`. | **Reflow** | 🔴 High |
| **Appearance:** `color`, `background-color`, `visibility`, `box-shadow`. | **Repaint** | 🟡 Medium |
| **Layers:** `transform` (scale, rotate, translate), `opacity`. | **Composite** | 🟢 Low |

---

## 🚀 The Performance Killer: Layout Thrashing

**Layout Thrashing** happens when you "Write" to the DOM and then "Read" from it immediately after in a loop.

```javascript
// ❌ SLOW: Layout Thrashing
// Every time we read 'offsetWidth', the browser is FORCED to stop and 
// recalculate everything because we just changed the width in the previous line.
for (let i = 0; i < boxes.length; i++) {
  const width = boxes[i].offsetWidth; // READ
  boxes[i].style.width = (width + 10) + 'px'; // WRITE
}

// ✅ FAST: Batching
// We read everything first, then we write everything. 
// The browser only has to do the math ONCE.
const widths = boxes.map(b => b.offsetWidth); // ALL READS
boxes.forEach((b, i) => {
  b.style.width = (widths[i] + 10) + 'px'; // ALL WRITES
});
```

---

## 🏗️ Pro Tip: Use CSS Transforms

If you want to animate a ball moving across the screen:
-   **Don't** use `top` and `left`. These trigger **Reflow** 60 times a second.
-   **Do** use `transform: translate()`. This only triggers **Composite**. It’s handled by the graphics card (GPU) and is buttery smooth.

---

## 📐 Visualizing the Pipeline

```text
 [ JAVASCRIPT ] ──▶ [ LAYOUT ] ──▶ [ PAINT ] ──▶ [ COMPOSITE ]
    (Change)         (Math)        (Pixels)       (GPU Magic)
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Forced Synchronous Layout
Normally, the browser is "lazy." When you change a style, it waits for the end of the frame to calculate the math. But if you call a property like `getBoundingClientRect()` or `offsetTop`, you are demanding an answer **now**. The browser has to stop everything, run the layout engine, and give you the number. If you do this many times, your app will feel "janky" (low FPS).

---

## 💼 Interview Questions

**Q1: What is the difference between Reflow and Repaint?**
> **Ans:** Reflow happens when an element's geometry (size or position) changes. It affects the layout of the whole page. Repaint happens when an element's appearance (color, visibility) changes but its geometry stays the same. Reflow is much more expensive than Repaint.

**Q2: Why are animations using `transform` faster than `margin-left`?**
> **Ans:** `margin-left` triggers a Reflow, which requires the CPU to do heavy math. `transform` triggers a Composite, which is handled by the GPU. The GPU is specially designed to move pixels around extremely fast.

**Q3: How do you detect Layout Thrashing?**
> **Ans:** Use the **Chrome DevTools Performance Tab**. Look for red bars or "Recalculate Style" events that happen many times in a single frame.

---

## ⚖️ Trade-offs

| Property | Benefit | Cost |
| :--- | :--- | :--- |
| **Transforms** | Super smooth (60fps); GPU accelerated. | Can cause blurriness if not used correctly. |
| **Geometry (Width/Height)**| Easiest to understand and use. | Heavy performance cost on every change. |
| **Visibility** | Easy to toggle elements. | Triggers a Repaint (not a Reflow). |

---

## 🔗 Navigation

**Prev:** [01_Code_Optimization.md](01_Code_Optimization.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [03_Memory_Leaks.md](03_Memory_Leaks.md)
