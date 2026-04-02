# 20 - Custom Hooks 🎣


---

## 🤔 What are Custom Hooks?

A **custom hook** is a function that you create yourself that uses built-in React hooks (like `useState`, `useEffect`) to **extract and reuse logic** across multiple components.

> **Real-world analogy:**
> Instead of re-explaining how to make coffee every time someone asks, you write a recipe (custom hook). Now anyone can just follow the recipe — no need to reinvent the wheel every time!

---

## 🔑 Rules of Custom Hooks

1. The name **must start with `use`** — e.g., `useCounter`, `useFetch`, `useAuth`
2. You can call other hooks inside them (useState, useEffect, etc.)
3. They are just **regular JavaScript functions** — no magic!
4. They can return **anything** — values, functions, objects, arrays

---

## 🔧 Why Create Custom Hooks?

Without custom hooks:
```jsx
// ❌ Repeating the same fetch logic in every component!
function UserList() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/users").then(r => r.json()).then(setData).catch(setError).finally(() => setLoading(false));
  }, []);
  // ... same pattern copy-pasted in 10 other components
}
```

With custom hooks:
```jsx
// ✅ Extract to hook, use anywhere!
const { data, loading, error } = useFetch("/api/users");
```

---

## 🌍 Real-World Custom Hook Examples

### Hook 1: `useFetch` — Reusable Data Fetching

```jsx
// hooks/useFetch.js
import { useState, useEffect } from "react";

function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error(`Error: ${res.status}`);
        return res.json();
      })
      .then((result) => {
        if (!cancelled) setData(result);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => { cancelled = true; }; // Cleanup!
  }, [url]);

  return { data, loading, error };
}

export default useFetch;
```

```jsx
// Usage — SO CLEAN!
function UserList() {
  const { data: users, loading, error } = useFetch("https://jsonplaceholder.typicode.com/users");

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

function PostList() {
  const { data: posts, loading } = useFetch("https://jsonplaceholder.typicode.com/posts");
  // Same hook, different URL!
}
```

---

### Hook 2: `useLocalStorage` — Persist State in Browser

```jsx
// hooks/useLocalStorage.js
import { useState } from "react";

function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      const val = value instanceof Function ? value(storedValue) : value;
      setStoredValue(val);
      localStorage.setItem(key, JSON.stringify(val));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}

export default useLocalStorage;
```

```jsx
// Usage — works like useState but persists after refresh!
function ThemeToggle() {
  const [theme, setTheme] = useLocalStorage("theme", "light");

  return (
    <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>
      {theme === "light" ? "🌙 Dark Mode" : "☀️ Light Mode"}
    </button>
  );
}
```

---

### Hook 3: `useDebounce` — Delay Input Actions

```jsx
// hooks/useDebounce.js
import { useState, useEffect } from "react";

function useDebounce(value, delay = 500) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

export default useDebounce;
```

```jsx
// Usage
function SearchBar() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, 400); // Only update after 400ms

  useEffect(() => {
    if (debouncedQuery) {
      console.log("Searching for:", debouncedQuery); // API call here
    }
  }, [debouncedQuery]);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search..." />;
}
```

---

### Hook 4: `useCounter` — Reusable Counter Logic

```jsx
// hooks/useCounter.js
import { useState } from "react";

function useCounter(initialValue = 0, step = 1) {
  const [count, setCount] = useState(initialValue);

  const increment = () => setCount((prev) => prev + step);
  const decrement = () => setCount((prev) => prev - step);
  const reset = () => setCount(initialValue);

  return { count, increment, decrement, reset };
}

export default useCounter;
```

```jsx
// Usage
function Counter() {
  const { count, increment, decrement, reset } = useCounter(0, 5);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+5</button>
      <button onClick={decrement}>-5</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}
```

---

### Hook 5: `useWindowSize` — Track Window Dimensions

```jsx
// hooks/useWindowSize.js
import { useState, useEffect } from "react";

function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () =>
      setSize({ width: window.innerWidth, height: window.innerHeight });

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return size;
}

export default useWindowSize;
```

```jsx
function ResponsiveLayout() {
  const { width } = useWindowSize();

  return (
    <div>
      {width < 768 ? (
        <MobileLayout />
      ) : (
        <DesktopLayout />
      )}
    </div>
  );
}
```

---

## 📁 Custom Hooks Folder Structure

```
src/
├── hooks/
│   ├── useFetch.js
│   ├── useLocalStorage.js
│   ├── useDebounce.js
│   ├── useCounter.js
│   └── useWindowSize.js
├── components/
└── App.jsx
```

---

## ❌ Common Mistakes / Tips

- ❌ Not starting the hook name with `use` — React won't treat it as a hook!
- ❌ Calling hooks conditionally inside a custom hook — hooks must be at top level
- ✅ Custom hooks are just **regular functions** — no React magic, just convention
- ✅ Return what the component needs (values + functions)
- ✅ Put all custom hooks in a `hooks/` folder
- 💡 If you find yourself copying the same hook logic in 3+ components — it's time for a custom hook!

---

## 📝 Summary

- Custom hooks = **extract reusable logic** from components
- Always name them starting with `use`
- Can use any other hooks inside (useState, useEffect, etc.)
- Return values and functions the component needs
- Common custom hooks: `useFetch`, `useLocalStorage`, `useDebounce`, `useAuth`, `useForm`

---

## 🎯 Practice Tasks

1. Create a `useFetch(url)` hook and use it in 3 different components
2. Create a `useToggle(initialValue)` hook that returns `[value, toggle]`
3. Create a `useForm(initialValues)` hook that handles form state and onChange
4. Create a `useWindowSize()` hook and use it to show different layouts
5. Create a `useOnClickOutside(ref, callback)` hook that closes a dropdown when clicking outside

---

← Previous: [19_error_handling.md](19_error_handling.md) | Next: [21_performance_optimization.md](21_performance_optimization.md) →
