# 12 - useRef Hook 🎯


---

## 🤔 What is useRef?

`useRef` is a hook that gives you a **reference** to a DOM element or a **persistent value** that doesn't cause re-renders when it changes.

Think of it as a secret variable that React doesn't watch.

---

## 🔧 Two Main Uses of useRef

1. **Access DOM elements directly** (focus, scroll, measure)
2. **Store a value** that persists between renders without re-rendering

---

## 📌 Syntax

```jsx
import { useRef } from "react";

const myRef = useRef(initialValue);

// Access the value/element with:
myRef.current
```

---

## 🖱️ Use Case 1: Accessing DOM Elements

### Example: Auto-focus an input

```jsx
function AutoFocusInput() {
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current.focus(); // Focus the input when component mounts
  }, []);

  return <input ref={inputRef} placeholder="I'm auto-focused! 🎯" />;
}
```

### Example: Scroll to element

```jsx
function ScrollToSection() {
  const sectionRef = useRef(null);

  const scrollToSection = () => {
    sectionRef.current.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div>
      <button onClick={scrollToSection}>Go to Section ↓</button>

      <div style={{ height: "100vh" }}>Content above...</div>

      <div ref={sectionRef} style={{ background: "lightblue", padding: "20px" }}>
        <h2>🎯 You Scrolled Here!</h2>
      </div>
    </div>
  );
}
```

### Example: Read input value without controlled component

```jsx
function UncontrolledInput() {
  const inputRef = useRef();

  const handleSubmit = () => {
    alert(`You typed: ${inputRef.current.value}`);
  };

  return (
    <div>
      <input ref={inputRef} placeholder="Type something..." />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}
```

---

## 💾 Use Case 2: Persisting Values Without Re-rendering

### Example: Count renders (without causing infinite loop)

```jsx
function RenderCounter() {
  const [count, setCount] = useState(0);
  const renderCount = useRef(0);

  // This runs every render but doesn't CAUSE a render!
  renderCount.current += 1;

  return (
    <div>
      <p>State count: {count}</p>
      <p>Total renders: {renderCount.current}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

> If you used `useState` for `renderCount`, updating it would cause infinite renders!

### Example: Store previous value

```jsx
function PreviousValue() {
  const [count, setCount] = useState(0);
  const prevCount = useRef(0);

  useEffect(() => {
    prevCount.current = count; // Save current count after render
  });

  return (
    <div>
      <p>Current: {count}</p>
      <p>Previous: {prevCount.current}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
}
```

### Example: Store a timer ID

```jsx
function StopwatchApp() {
  const [time, setTime] = useState(0);
  const [running, setRunning] = useState(false);
  const intervalRef = useRef(null); // Store interval ID

  const start = () => {
    if (!running) {
      setRunning(true);
      intervalRef.current = setInterval(() => {
        setTime((prev) => prev + 1);
      }, 1000);
    }
  };

  const stop = () => {
    clearInterval(intervalRef.current); // Use ref to clear it
    setRunning(false);
  };

  const reset = () => {
    clearInterval(intervalRef.current);
    setRunning(false);
    setTime(0);
  };

  return (
    <div>
      <h2>⏱️ {time}s</h2>
      <button onClick={start}>▶️ Start</button>
      <button onClick={stop}>⏸️ Stop</button>
      <button onClick={reset}>🔄 Reset</button>
    </div>
  );
}
```

---

## 🆚 useRef vs useState

| Feature | `useRef` | `useState` |
|---|---|---|
| Causes re-render? | ❌ No | ✅ Yes |
| Value persists? | ✅ Yes | ✅ Yes |
| Use for DOM? | ✅ Yes | ❌ No |
| Sync/Async | Sync (immediate) | Async (batched) |
| Best for | DOM refs, timers, prev values | UI data that should update screen |

---

## 🆚 useRef vs Variables

```jsx
// Normal variable — RESETS to 0 on every render!
let count = 0;

// useRef — PERSISTS between renders!
const countRef = useRef(0);
```

---

## ❌ Common Mistakes / Tips

- ❌ Using `useRef` for data that should update the UI (use `useState` for that!)
- ❌ Accessing `ref.current` before the component mounts (it'll be `null`)
- ✅ `useRef` for: DOM access, timer IDs, previous values, any mutable data that doesn't affect UI
- ✅ Always check `if (ref.current)` before using it to avoid null errors
- 💡 `ref.current` is mutable — you can assign to it directly

---

## 📝 Summary

- `useRef` stores a **mutable value** or **DOM reference**
- Changing `ref.current` does **NOT trigger a re-render**
- Use for: focusing inputs, scrolling, measuring, storing timer IDs, previous values
- Attach to elements using `ref={myRef}` attribute
- Access value/element via `myRef.current`

---

## 🎯 Practice Tasks

1. Build an input that **auto-focuses** when the page loads
2. Build a **stopwatch** (start, stop, reset) using `useRef` for the interval
3. Build a "Go to Top" button that **smoothly scrolls** to the top of the page
4. Display the **previous value** of a counter alongside the current value
5. Build a video player component — use `useRef` to call `.play()` and `.pause()` on a `<video>` element

---

← Previous: [11_useEffect.md](11_useEffect.md) | Next: [13_useMemo_useCallback.md](13_useMemo_useCallback.md) →
