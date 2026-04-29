# 📌 Project 04 — Build a "React-Like" State

## 🌟 Introduction

React Hooks like `useState` seem like magic. How does a function "remember" its state between renders even though it starts from scratch every time?

The secret is simple: **Arrays**.

Think of a **Pill Organizer**:
-   Each slot in the organizer is a piece of state.
-   React fills the slots in order: Slot 1, then Slot 2, then Slot 3.
-   On the next render, it goes back to Slot 1 and says: "Ah, here is the value from last time!"

---

## 🏗️ 1. The Strategy

We need three things:
1.  **An Array (`hooks`):** To store the data.
2.  **An Index (`cursor`):** To know which "slot" we are currently reading.
3.  **A Render Function:** To clear the index and restart the process.

---

## 🏗️ 2. The Implementation

```javascript
let hooks = []; // Our storage
let cursor = 0; // Our "Which slot am I in?" counter

function useState(initialValue) {
  const currentCursor = cursor; // Capture the current slot
  
  // If this is the FIRST time, save the initial value
  if (hooks[currentCursor] === undefined) {
    hooks[currentCursor] = initialValue;
  }

  const setState = (newValue) => {
    hooks[currentCursor] = newValue; // Update the storage
    render(); // Re-run the whole app!
  };

  cursor++; // Move to the NEXT slot for the next hook
  return [hooks[currentCursor], setState];
}

function render() {
  cursor = 0; // RESET the counter before we start
  App(); // Run the component
}
```

---

## 🚀 3. Testing Your Hook

```javascript
function App() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState("Nishant");

  console.log(`State: ${count}, Name: ${name}`);

  // Simulate a user click
  if (count === 0) {
    setTimeout(() => setCount(1), 1000);
  }
}

render();
// Output: State: 0, Name: Nishant
// (1 second later)
// Output: State: 1, Name: Nishant
```

---

## 📐 Visualizing the Re-render Cycle

When `setState` is called, the entire function runs again. The `cursor` is the key to connecting the old state to the new run.

```text
 INITIAL RENDER:
 1. useState(0)     ──▶ hooks[0] = 0, cursor = 1
 2. useState("N")   ──▶ hooks[1] = "N", cursor = 2
 
 [ USER CLICKS SETCOUNT(1) ]
 
 RE-RENDER:
 1. cursor = 0      (Reset!)
 2. useState(0)     ──▶ returns hooks[0] (which is now 1), cursor = 1
 3. useState("N")   ──▶ returns hooks[1] (which is still "N"), cursor = 2
```

---

## 🛠️ Real-World Troubleshooting (Q&A)

**P1: Infinite Loops with `useEffect`.**
> **Problem:** My component keeps re-rendering thousands of times a second.
> **Reason:** You are updating a piece of state inside a `useEffect` that also depends on that same state.
> **Fix:** Check your dependency array. Only include variables that *should* trigger the effect. Never update state that is in the dependency array unless you have a strict condition.

**P2: "Stale Closures" in `setState`.**
> **Problem:** `setCount(count + 1)` called three times in a row only increments by 1.
> **Reason:** The `count` variable is "captured" from the old render. All three calls are seeing the same old value.
> **Fix:** Use the functional update pattern: `setCount(prevCount => prevCount + 1)`. This ensures you are always working with the most recent data.

**P3: Hooks Rule Violation.**
> **Problem:** `Error: Rendered fewer hooks than expected.`
> **Reason:** You put a `useState` inside a conditional `if` block.
> **Fix:** Hooks MUST be called at the top level, in the exact same order, every single time.

---

## 🔬 Deep Technical Dive (V8 Internals)

### Call Stack vs. Persistence
When a function finishes running, its local variables are usually deleted from the **Call Stack**. However, because our `hooks` array is defined **outside** the function, it lives in the **Heap** (the permanent memory). The `setState` function is a "Closure"—it carries a reference to the specific index (the `currentCursor`) forever. This is how the value survives even though the `App` function "dies" at the end of every render.

---

## 💼 Interview Tips

-   **Why can't hooks be in `if` statements?** Because the `cursor` depends on the order. If an `if` statement skips a hook, the cursor will point to the wrong slot in the array, and your data will be corrupted!
-   **What happens on a re-render?** We reset the `cursor` to 0. This is the most important part—it ensures that the first `useState` call always maps to `hooks[0]`.
-   **Is this how React actually works?** Yes! React uses a more complex version called a **Linked List** instead of an array, but the logic of "Order Matters" is exactly the same.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Hooks (Ordered)** | Very clean; no boilerplate. | "Rules of Hooks" are confusing for beginners. |
| **Class State (Object)** | No order rules; safer. | Very verbose; `this` binding is annoying. |
| **Global Store** | State is accessible everywhere. | Overkill for simple components. |

---

## 🔗 Navigation

**Prev:** [03_Build_LRU_Cache.md](03_Build_LRU_Cache.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [05_Build_Rate_Limiter.md](05_Build_Rate_Limiter.md)
