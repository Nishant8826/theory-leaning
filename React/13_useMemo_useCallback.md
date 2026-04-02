# 13 - useMemo and useCallback ⚡


---

## 🤔 The Problem: Unnecessary Re-calculations

In React, every time a component re-renders, **every function is re-created** and **every calculation is re-run** from scratch — even if the data hasn't changed.

> **Real-world analogy:**
> Imagine you're at a restaurant. Every time a new customer walks in, the chef re-bakes ALL the cakes, even if the same ones are already ready. That's wasteful! `useMemo` and `useCallback` are like a caching tray — you only re-bake when the recipe changes.

---

## 🧮 useMemo — Cache a Computed Value

`useMemo` stores (memoizes) the **result of a calculation** and only re-calculates it when the specified dependencies change.

### Syntax:
```tsx
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
```

### Without useMemo (Problem):
```tsx
function App() {
  const [count, setCount] = useState(0);
  const [input, setInput] = useState("");

  // This runs EVERY render — even when only `input` changes!
  const expensiveResult = heavyCalculation(count);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <p>Result: {expensiveResult}</p>
    </div>
  );
}
```

### With useMemo (Solution):
```tsx
function App() {
  const [count, setCount] = useState(0);
  const [input, setInput] = useState("");

  // Only re-calculates when `count` changes!
  const expensiveResult = useMemo(() => {
    console.log("🔄 Re-calculating...");
    return heavyCalculation(count);
  }, [count]);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <p>Result: {expensiveResult}</p>
    </div>
  );
}
```

---

## 🌍 Real-World useMemo Examples

### Example 1: Expensive Filter

```tsx
function ProductSearch() {
  const [search, setSearch] = useState("");
  const [darkMode, setDarkMode] = useState(false);

  const products = [
    { id: 1, name: "iPhone", category: "Phone" },
    { id: 2, name: "MacBook", category: "Laptop" },
    { id: 3, name: "iPad", category: "Tablet" },
    { id: 4, name: "AirPods", category: "Audio" },
    // ... imagine 10,000 more items
  ];

  // Without useMemo: re-filters ALL items on EVERY render (even dark mode toggle)
  // With useMemo: only re-filters when `search` changes!
  const filteredProducts = useMemo(() => {
    console.log("Filtering...");
    return products.filter((p) =>
      p.name.toLowerCase().includes(search.toLowerCase())
    );
  }, [search]);

  return (
    <div style={{ background: darkMode ? "#333" : "#fff", color: darkMode ? "#fff" : "#000" }}>
      <button onClick={() => setDarkMode(!darkMode)}>Toggle Dark Mode</button>
      <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search..." />
      <ul>
        {filteredProducts.map((p) => <li key={p.id}>{p.name}</li>)}
      </ul>
    </div>
  );
}
```

---

## 🔁 useCallback — Cache a Function

`useCallback` stores (memoizes) a **function** and only re-creates it when dependencies change.

### Why? Because in React, functions are re-created on every render!

```tsx
// Every render creates a NEW handleClick function
const handleClick = () => {
  console.log("Clicked!");
};
// Next render → a different handleClick in memory, even if it does the same thing!
```

### Syntax:
```tsx
const memoizedFn = useCallback(() => {
  doSomething(a, b);
}, [a, b]);
```

---

## 🌍 Real-World useCallback Example

### Without useCallback:

```tsx
function Parent() {
  const [count, setCount] = useState(0);

  // New function on every render → Child re-renders unnecessarily!
  const handleClick = () => {
    console.log("Button clicked");
  };

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Parent count: {count}</button>
      <Child onClick={handleClick} />
    </div>
  );
}

const Child = React.memo(({ onClick }) => {
  console.log("Child rendered! 🔄");
  return <button onClick={onClick}>Child Button</button>;
});
```

> Even with `React.memo` on Child, it still re-renders because `handleClick` is a new function reference every render!

### With useCallback:

```tsx
function Parent() {
  const [count, setCount] = useState(0);

  // Same function reference — Child won't re-render!
  const handleClick = useCallback(() => {
    console.log("Button clicked");
  }, []); // No dependencies = only created once

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Parent count: {count}</button>
      <Child onClick={handleClick} />
    </div>
  );
}

const Child = React.memo(({ onClick }) => {
  console.log("Child rendered! 🔄");
  return <button onClick={onClick}>Child Button</button>;
});
// Now Child ONLY re-renders when handleClick changes!
```

---

## 🆚 useMemo vs useCallback

| | `useMemo` | `useCallback` |
|---|---|---|
| Returns | A **value** (result of a function) | A **function** |
| Use for | Expensive computations | Stable function references |
| Example | Filtered list, calculated total | Event handlers passed to children |

```tsx
// useMemo → caches the RESULT
const total = useMemo(() => items.reduce((sum, i) => sum + i.price, 0), [items]);

// useCallback → caches the FUNCTION ITSELF
const handleAdd = useCallback(() => {
  setItems([...items, newItem]);
}, [items, newItem]);
```

---

## ⚠️ When to Use Them (Don't Over-Optimize!)

> 🚨 **STOP** — Don't use `useMemo` / `useCallback` everywhere!

Use them **only** when:
1. The computation is **truly expensive** (filtering/sorting 10k+ items)
2. You're passing functions to **deeply nested children** wrapped in `React.memo`
3. You notice **real performance issues** in DevTools

For most small/medium apps, they're **unnecessary** and add complexity!

---

## ❌ Common Mistakes / Tips

- ❌ Using `useMemo`/`useCallback` on simple calculations — more overhead than benefit
- ❌ Forgetting the dependency array — misses re-calculation when data changes
- ✅ Measure first with React DevTools Profiler, optimize later
- ✅ `useMemo` is for values, `useCallback` is for functions
- 💡 Rule: Premature optimization is the root of all evil. Profile first!

---

## 📝 Summary

- `useMemo` = **cache a computed value**, only re-compute when dependencies change
- `useCallback` = **cache a function**, only re-create when dependencies change
- Use when: expensive calculations, functions passed to `React.memo` children
- Don't use everywhere — measure first!

---

## 🎯 Practice Tasks

1. Create a list of 1000 items. Use `useMemo` to filter them by a search term. Open console to see when re-filtering happens
2. Use `useCallback` on a function passed to a child component to prevent unnecessary re-renders
3. Try using React DevTools **Profiler** to measure render times before and after
4. Build a cart with items. Use `useMemo` to calculate the total price only when items change

---

← Previous: [12_useRef.md](12_useRef.md) | Next: [14_lifecycle.md](14_lifecycle.md) →
