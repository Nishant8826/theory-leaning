# 11 - useEffect Hook 🔁

> **Previous: [10_forms.md](./10_forms.md)** | **Next: [12_useRef.md](./12_useRef.md)**

---

## 🤔 What is useEffect?

`useEffect` lets you perform **side effects** in your component — things that happen **after** the component renders.

> **Real-world analogy:**
> When you open WhatsApp (component mounts), your phone automatically checks for new messages (side effect). When you close WhatsApp (component unmounts), it stops checking. `useEffect` works the same way!

**Side effects include:**
- Fetching data from an API
- Setting up timers / intervals
- Subscribing to events
- Updating the document title
- Connecting to a WebSocket

---

## 🔧 Basic Syntax

```jsx
import { useEffect } from "react";

useEffect(() => {
  // Your side effect code here
  console.log("Component rendered!");

  // Optional cleanup function
  return () => {
    console.log("Component unmounted / cleanup!");
  };
}, [/* dependency array */]);
```

---

## ⚙️ The Dependency Array — The Most Important Part!

The **dependency array** (second argument) controls **when** the effect runs:

| Dependency Array | When Effect Runs |
|---|---|
| Not provided | After **every** render |
| `[]` (empty) | **Once** — when component mounts |
| `[value]` | When component mounts **AND** every time `value` changes |

---

## 📋 Three Common Patterns

### Pattern 1: Run ONCE (on mount) — `[]`

```jsx
function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    console.log("Component mounted! Fetch data...");
    // API call here
    setData("Hello from API!");
  }, []); // ← empty array = run once!

  return <p>{data}</p>;
}
```

### Pattern 2: Run when value changes — `[value]`

```jsx
function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (query) {
      console.log("Searching for:", query);
      // Imagine an API call here
      setResults([`Result for "${query}"`]);
    }
  }, [query]); // ← runs every time `query` changes

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search..." />
      <ul>{results.map((r, i) => <li key={i}>{r}</li>)}</ul>
    </div>
  );
}
```

### Pattern 3: Cleanup (on unmount)

```jsx
function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSeconds((prev) => prev + 1);
    }, 1000);

    // Cleanup: runs when component is removed
    return () => {
      clearInterval(interval); // ← Stop the timer!
      console.log("Timer cleaned up!");
    };
  }, []);

  return <p>⏱️ Timer: {seconds}s</p>;
}
```

---

## 🌍 Real-World Examples

### Example 1: Fetch API Data

```jsx
function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/users")
      .then((res) => res.json())
      .then((data) => {
        setUsers(data);
        setLoading(false);
      });
  }, []); // Only fetch once when component mounts

  if (loading) return <p>Loading... ⏳</p>;

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name} — {user.email}</li>
      ))}
    </ul>
  );
}
```

### Example 2: Update Document Title

```jsx
function PageTitle() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `You clicked ${count} times`;
  }, [count]); // Updates title whenever count changes

  return <button onClick={() => setCount(count + 1)}>Clicked: {count}</button>;
}
```

### Example 3: Window Resize Listener

```jsx
function WindowSize() {
  const [size, setSize] = useState({ width: window.innerWidth, height: window.innerHeight });

  useEffect(() => {
    const handleResize = () => {
      setSize({ width: window.innerWidth, height: window.innerHeight });
    };

    window.addEventListener("resize", handleResize);

    // Cleanup: remove listener when component unmounts
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return <p>Window: {size.width} x {size.height}</p>;
}
```

### Example 4: Debounced Search (Advanced but Practical)

```jsx
function DebouncedSearch() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState("");

  useEffect(() => {
    // Wait 500ms after user stops typing before searching
    const timer = setTimeout(() => {
      if (query) {
        setResult(`Searching for: "${query}"`);
      }
    }, 500);

    return () => clearTimeout(timer); // Cancel if query changes before 500ms
  }, [query]);

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Type to search..." />
      <p>{result}</p>
    </div>
  );
}
```

---

## ⚡ Multiple useEffects

You can have multiple `useEffect` hooks — each handles a different concern:

```jsx
function Dashboard() {
  useEffect(() => {
    // Fetch user data
    fetchUser();
  }, []);

  useEffect(() => {
    // Set page title
    document.title = "Dashboard";
  }, []);

  useEffect(() => {
    // Setup analytics
    trackPageView("dashboard");
  }, []);

  // ...
}
```

---

## ❌ Common Mistakes / Tips

- ❌ Missing the dependency array — effect runs after every render (usually a bug!)
- ❌ Infinite loop: using `setState` inside effect + putting that state in dependency array
- ❌ Forgetting cleanup for intervals, event listeners, subscriptions → **memory leaks!**
- ✅ Always clean up timers, listeners, subscriptions in the return function
- ✅ Use `async/await` inside useEffect with a wrapper function:

```jsx
useEffect(() => {
  const fetchData = async () => {
    const res = await fetch("/api/data");
    const data = await res.json();
    setData(data);
  };

  fetchData(); // Can't make useEffect itself async!
}, []);
```

---

## 📝 Summary

- `useEffect` runs **after** rendering — for side effects
- `[]` = run once (mount), `[value]` = run on change, no array = every render
- Return a cleanup function to avoid **memory leaks**
- Use for: API calls, timers, event listeners, subscriptions, DOM updates
- Never make the `useEffect` callback itself `async` — use an inner async function

---

## 🎯 Practice Tasks

1. Fetch users from `https://jsonplaceholder.typicode.com/users` and display them
2. Build a **live clock** that shows time and updates every second
3. Build a **scroll position tracker** that shows how far down the page you've scrolled
4. Build a **debounced search** input (wait 500ms after user stops typing)
5. Update the browser tab title dynamically based on what page you're "on"

---

> **Previous: [10_forms.md](./10_forms.md)** | **Next: [12_useRef.md](./12_useRef.md)**
