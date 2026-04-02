# 21 - Performance Optimization 🚀


---

## 🤔 Why Optimize?

React is fast by default, but as apps grow, they can become slow if you're not careful. Optimization means making your app **faster, smoother, and more efficient**.

---

## 🔍 The First Rule of Optimization

**> "Don't optimize prematurely!"**

First, **measure** if there's actually a problem. Then optimize.
Use the **React DevTools Profiler** to see which components re-render and how long they take.

---

## 🧰 Optimization Techniques

---

### 1. `React.memo` — Prevent Unnecessary Re-renders

Wrapping a component in `React.memo` makes React **skip re-rendering** it if its props haven't changed.

```jsx
// Without memo — re-renders even when nothing changed
function MovieCard({ title, rating }) {
  console.log("Rendering:", title);
  return <div>{title} ⭐{rating}</div>;
}

// With memo — only re-renders if `title` or `rating` changes
const MovieCard = React.memo(function MovieCard({ title, rating }) {
  console.log("Rendering:", title);
  return <div>{title} ⭐{rating}</div>;
});

// In parent — if parent re-renders, MovieCard won't unless props change!
function App() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Click: {count}</button>
      <MovieCard title="Inception" rating={9} />  {/* Won't re-render on button click! */}
    </div>
  );
}
```

---

### 2. `useMemo` — Cache Expensive Calculations

(Covered in detail in `13_useMemo_useCallback.md`)

```jsx
// Re-calculates only when `products` or `filter` changes
const filteredProducts = useMemo(() => {
  return products.filter((p) => p.category === filter);
}, [products, filter]);
```

---

### 3. `useCallback` — Stable Function References

(Covered in detail in `13_useMemo_useCallback.md`)

```jsx
// Same function reference between renders — prevents child re-renders
const handleDelete = useCallback((id) => {
  setItems((prev) => prev.filter((item) => item.id !== id));
}, []); // No deps = always the same function
```

---

### 4. Code Splitting — Load Only What's Needed

Instead of loading the entire app upfront, **lazy load** components only when needed:

```jsx
import { lazy, Suspense } from "react";

// Load these components only when the route is visited!
const Dashboard = lazy(() => import("./pages/Dashboard"));
const Settings = lazy(() => import("./pages/Settings"));

function App() {
  return (
    <Suspense fallback={<div>Loading page... ⏳</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

> 💡 The initial bundle is smaller → app loads faster for users!

---

### 5. List Virtualization — Render Only Visible Items

If you have a list of 10,000 items, don't render all 10,000 at once! Render only the ones visible on screen:

```bash
npm install react-window
```

```jsx
import { FixedSizeList } from "react-window";

function HugeList({ items }) {
  return (
    <FixedSizeList
      height={500}      // Container height
      itemCount={items.length}
      itemSize={50}     // Each row height
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          {items[index].name}
        </div>
      )}
    </FixedSizeList>
  );
}
```

---

### 6. Image Optimization

```jsx
// ❌ BAD — loads huge image, slow
<img src="hero-photo.jpg" alt="Hero" />

// ✅ GOOD — specify dimensions, lazy load
<img
  src="hero-photo.jpg"
  alt="Hero"
  width={800}
  height={400}
  loading="lazy"     // Browser loads only when scrolled into view!
/>
```

---

### 7. Avoid Anonymous Functions in JSX

```jsx
// ❌ BAD — new function on every render
<button onClick={() => handleDelete(item.id)}>Delete</button>

// ✅ BETTER — pre-bound function
const handleDeleteItem = useCallback(() => handleDelete(item.id), [item.id]);
<button onClick={handleDeleteItem}>Delete</button>
```

> Note: For simple cases, the performance difference is tiny. Only worry about this in very long lists.

---

### 8. `useReducer` for Complex State

When you have complex state with many updates, `useReducer` can be more efficient than many `useState` calls:

```jsx
const initialState = { count: 0, step: 1, history: [] };

function reducer(state, action) {
  switch (action.type) {
    case "increment":
      return { ...state, count: state.count + state.step, history: [...state.history, state.count] };
    case "decrement":
      return { ...state, count: state.count - state.step };
    case "setStep":
      return { ...state, step: action.payload };
    case "reset":
      return initialState;
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <div>
      <p>Count: {state.count} (step: {state.step})</p>
      <button onClick={() => dispatch({ type: "increment" })}>+</button>
      <button onClick={() => dispatch({ type: "decrement" })}>-</button>
      <button onClick={() => dispatch({ type: "reset" })}>Reset</button>
    </div>
  );
}
```

---

### 9. Debounce Expensive Operations

```jsx
// Debounce search — don't call API on every keystroke
const debouncedSearch = useDebounce(searchQuery, 500);

useEffect(() => {
  if (debouncedSearch) {
    searchAPI(debouncedSearch);
  }
}, [debouncedSearch]);
```

---

### 10. React DevTools Profiler

1. Install **React Developer Tools** browser extension
2. Open DevTools → "Profiler" tab
3. Click Record → interact with your app → Stop
4. See which components took longest to render → optimize those!

---

## 🆚 Optimization Summary Table

| Technique | Solves |
|---|---|
| `React.memo` | Prevents unnecessary re-renders of child components |
| `useMemo` | Caches expensive calculations |
| `useCallback` | Stable function references for child components |
| Code Splitting (lazy) | Smaller initial bundle, faster load |
| Virtualization | Rendering large lists efficiently |
| `loading="lazy"` on images | Faster image loading |
| Debouncing | Reduce API calls for search/input |

---

## ❌ Common Mistakes / Tips

- ❌ Over-optimizing everything — adds complexity without benefit
- ❌ Using `React.memo` on every component — only helps if parent re-renders frequently
- ✅ Profile first with React DevTools Profiler, then optimize
- ✅ The biggest wins: lazy loading, virtualization, proper keys in lists
- 💡 Code splitting alone can cut initial load time by 40-60%!

---

## 📝 Summary

- Measure before optimizing — use React DevTools Profiler
- `React.memo` → skip re-renders | `useMemo/useCallback` → cache values/functions
- Lazy loading reduces initial bundle size
- Virtualize large lists with `react-window`
- Debounce search inputs and expensive operations
- Don't over-optimize — only fix what profiling shows is slow!

---

## 🎯 Practice Tasks

1. Wrap a component in `React.memo` and verify it stops re-rendering with React DevTools
2. Use `React.lazy` and `Suspense` to lazy-load a heavy component like a Dashboard
3. Install `react-window` and render a virtualized list of 5000 items
4. Open React DevTools → Profiler → record interactions → identify slow components
5. Implement debounced search (type in input → API called only after 500ms pause)

---

← Previous: [20_custom_hooks.md](20_custom_hooks.md) | Next: [22_folder_structure.md](22_folder_structure.md) →
