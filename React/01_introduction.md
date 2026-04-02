# 01 - Introduction to React ⚛️


---

## 🤔 What is React?

React is a **JavaScript library** made by Facebook (Meta) that helps you build **user interfaces** — basically the part of a website/app that users see and click on.

---

## 🌍 Real-World Analogy

| Concept | Real-World Example |
|---|---|
| React App | A news website like BBC |
| Component | Navbar, Article Card, Footer |
| State | Number of likes that updates live |
| Props | Article title passed to the card |

---

## ✨ Why React? (React vs Vanilla JS)

### Without React (Vanilla JS):
```html
<!-- HTML -->
<div id="counter">0</div>
<button onclick="increment()">Click Me</button>

<script>
  let count = 0;
  function increment() {
    count++;
    document.getElementById("counter").innerText = count;
  }
</script>
```

### With React:
```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(count + 1)}>Click Me</button>
    </div>
  );
}
```

- **What:** This is a basic React Component using the `useState` hook to manage dynamic data.
- **Why:** React handles DOM updates automatically instead of writing tedious `document.getElementById` queries.
- **How:** `useState(0)` initializes state, and `setCount` updates it. React automatically detects the state change and re-renders only the changed DOM node.
- **Impact:** Less boilerplate code, fewer bugs, and highly maintainable components for large-scale applications.

**Difference:** In React, you don't manually update the DOM. React does it automatically when data changes. 🎉

---

## 🆚 React vs Angular vs Vue (Quick Overview)

| Feature | React | Angular | Vue |
|---|---|---|---|
| Type | Library | Full Framework | Framework |
| Made by | Meta | Google | Community |
| Language | JavaScript/JSX | TypeScript | JavaScript |
| Learning Curve | Easy | Steep | Easy |
| Flexibility | High | Low | Medium |
| DOM | Virtual DOM | Real DOM | Virtual DOM |

---

## 🏗️ How React Works (Big Picture)

```
Your Code (React Components)
        ↓
   Virtual DOM (React's copy of the DOM)
        ↓
   React compares old vs new (Diffing)
        ↓
   Only updates what changed (Real DOM)
```

This process is called **Reconciliation** and it makes React very fast!

---

## 🔑 Key Concepts You'll Learn

- **Component** — Building block of any React app
- **JSX** — HTML-like syntax inside JavaScript
- **Props** — Passing data between components
- **State** — Data that changes over time
- **Hooks** — Functions that power your components (useState, useEffect, etc.)

---

## ❌ Common Mistakes / Tips

- ❌ Don't think React is a full framework — it's just a **UI library**
- ✅ React only handles the **View** layer (what users see)
- ❌ Don't manipulate the DOM directly with `document.getElementById` in React
- ✅ Let React manage the DOM for you

---

## 📝 Summary

- React is a **JavaScript library** for building UIs
- It uses **components** — reusable pieces of UI
- React uses a **Virtual DOM** for performance
- Way simpler than Vanilla JS once you get the hang of it
- Made by **Meta**, used by companies like Netflix, Airbnb, Twitter

---

## 🎯 Practice Tasks

1. Go to [react.dev](https://react.dev) and read the "Quick Start" page
2. Visit a website you use daily. Try to identify what the "components" might be (navbar, card, sidebar, etc.)
3. Write down: What problem do you think React solves compared to plain HTML + JS?
4. Bookmark this folder — you'll be coming back to it a lot! 😄

---

## 🎤 Interview Questions

**Q1: What is the Virtual DOM and how does it differ from the Real DOM?**
**Answer:** The Virtual DOM is a lightweight memory representation of the Real DOM. React compares the new Virtual DOM with the old one (Diffing) and updates only the changed parts in the Real DOM (Reconciliation), making it much faster.

**Q2: What is the difference between a Library and a Framework? Why is React considered a library?**
**Answer:** A framework (like Angular) dictates how you write the application and comes with built-in routing, HTTP modules, etc. React is a library because it only handles the UI (the View layer) and leaves routing and data management to other packages you choose.

**Q3: What are React Components?**
**Answer:** Components are independent, reusable building blocks of a React application. They accept inputs (props) and return React elements describing what should appear on the screen.

---

← Previous: []() | Next: [02_setup_react.md](02_setup_react.md) →
