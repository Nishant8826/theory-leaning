# 04 - Components (Functional vs Class) 🧩


---

## 🤔 What is a Component?

A component is a **reusable piece of UI**. Think of it like a LEGO block — you build small blocks and combine them to make something big.

> **Real-world analogy:** A YouTube page has:
> - A **Navbar** component (top bar with search)
> - A **VideoCard** component (each video thumbnail)
> - A **Sidebar** component (left menu)
> - A **Footer** component
>
> All of these are separate components assembled together on one page!

---

## 🏗️ Two Types of Components

### 1. Functional Components (✅ Modern — Use This!)

A simple JavaScript function that returns JSX.

```jsx
// Simple functional component
function Greeting() {
  return <h1>Hello, World! 👋</h1>;
}

// Arrow function style (same thing)
const Greeting = () => {
  return <h1>Hello, World! 👋</h1>;
};
```

### 2. Class Components (❌ Old — Avoid for new code)

A class that extends `React.Component` and has a `render()` method.

```jsx
import React, { Component } from "react";

class Greeting extends Component {
  render() {
    return <h1>Hello, World! 👋</h1>;
  }
}
```

---

## 🆚 Functional vs Class Components

| Feature | Functional | Class |
|---|---|---|
| Syntax | Simple function | Extends `Component` |
| State | `useState()` hook | `this.state` |
| Lifecycle | `useEffect()` hook | Lifecycle methods |
| `this` keyword | ❌ Not needed | ✅ Required |
| Code amount | Less | More (boilerplate) |
| Modern? | ✅ Yes | ❌ Outdated |
| Performance | ✅ Slightly better | Slightly heavier |

> 🎯 **Rule of thumb**: Always use **Functional Components** in modern React (2019+)

---

## 📋 Rules for Components

1. **Component name MUST start with a Capital letter**

```jsx
// ❌ WRONG - React will treat it as HTML tag
function mybutton() { return <button>Click</button>; }

// ✅ CORRECT
function MyButton() { return <button>Click</button>; }
```

2. **One component per file** (best practice)

```
src/
├── components/
│   ├── Navbar.jsx
│   ├── Footer.jsx
│   └── Button.jsx
├── App.jsx
```

3. **Always export your component**

```jsx
// Named export
export function Greeting() {
  return <h1>Hello!</h1>;
}

// Default export (most common)
function Greeting() {
  return <h1>Hello!</h1>;
}
export default Greeting;
```

---

## 🌍 Real-World Component Example

### App.jsx (assembles everything)
```jsx
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Footer from "./components/Footer";

function App() {
  return (
    <div>
      <Navbar />
      <Hero />
      <Footer />
    </div>
  );
}

export default App;
```

### Navbar.jsx
```jsx
function Navbar() {
  return (
    <nav className="navbar">
      <h1>My Website 🚀</h1>
      <ul>
        <li>Home</li>
        <li>About</li>
        <li>Contact</li>
      </ul>
    </nav>
  );
}

export default Navbar;
```

### Footer.jsx
```jsx
function Footer() {
  return (
    <footer>
      <p>© 2025 My Website. All rights reserved.</p>
    </footer>
  );
}

export default Footer;
```

---

## 🔄 Component Composition

You can nest components inside other components — this is called **composition**.

```jsx
function Button() {
  return <button className="btn">Click Me</button>;
}

function Card() {
  return (
    <div className="card">
      <h2>Product Name</h2>
      <p>₹999</p>
      <Button />   {/* Using Button inside Card! */}
    </div>
  );
}

function App() {
  return (
    <div>
      <Card />   {/* Using Card inside App! */}
      <Card />   {/* Reusing the same component! */}
      <Card />
    </div>
  );
}
```

---

## ❌ Common Mistakes / Tips

- ❌ Naming components starting with lowercase (`button` → ❌, `Button` → ✅)
- ❌ Returning multiple root-level elements without a wrapper
- ❌ Writing all components in one file (for large apps)
- ✅ One component = one file
- ✅ Put components in a `components/` folder
- 💡 Use the snippet `rafce` in VS Code (ES7 React Snippets extension) to quickly generate a component

---

## 📝 Summary

- Components are **reusable UI pieces**
- Use **Functional Components** — class components are old
- Component names **must start with uppercase**
- Components can be **nested** inside each other (composition)
- Each component should be in its **own file** in the `components/` folder

---

## 🎯 Practice Tasks

1. Create a `Header` component that shows a website name and a navigation bar
2. Create a `Card` component that shows a product name, image placeholder, and price
3. Create an `App` that uses `Header` + 3 `Card` components
4. Try making a `Button` component and reuse it in multiple places
5. Refactor: Take any HTML page you have and convert it into React components

---

← Previous: [03_jsx.md](03_jsx.md) | Next: [05_props.md](05_props.md) →
