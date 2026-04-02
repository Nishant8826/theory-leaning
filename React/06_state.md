# 06 - State 🔄


---

## 🤔 What is State?

**State** is data that **changes over time** inside a component. When state changes, React automatically **re-renders** the component to reflect the new data.

> **Real-world analogy:**
> Think of a scoreboard at a cricket match. The score **changes** as runs are scored — that changing score is "state". Every time it changes, the board updates automatically. React does the same for your UI!

---

## 🆚 State vs Props Quick Recap

| | Props | State |
|---|---|---|
| Who controls? | Parent | The component itself |
| Can change? | ❌ No | ✅ Yes |
| Example | movie title | like count, toggle, input value |

---

## 🧰 useState Hook

To use state in a functional component, use the `useState` hook:

```tsx
import { useState } from "react";

function Counter() {
  // [currentValue, functionToUpdate] = useState(initialValue)
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>➕ Increment</button>
      <button onClick={() => setCount(count - 1)}>➖ Decrement</button>
      <button onClick={() => setCount(0)}>🔄 Reset</button>
    </div>
  );
}
```

### Breakdown:
- `count` — the current value of state
- `setCount` — the function to **update** the state
- `useState(0)` — initial value is `0`

---

## 🌍 Real-World Examples

### Example 1: Toggle (Show/Hide)

```tsx
function FAQ() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? "Hide Answer ▲" : "Show Answer ▼"}
      </button>

      {isOpen && (
        <p>React is a JavaScript library for building UIs! 🎉</p>
      )}
    </div>
  );
}
```

### Example 2: Like Button

```tsx
function LikeButton() {
  const [likes, setLikes] = useState(0);
  const [liked, setLiked] = useState(false);

  const handleLike = () => {
    if (!liked) {
      setLikes(likes + 1);
      setLiked(true);
    } else {
      setLikes(likes - 1);
      setLiked(false);
    }
  };

  return (
    <button onClick={handleLike} style={{ color: liked ? "red" : "gray" }}>
      ❤️ {likes} {liked ? "Liked" : "Like"}
    </button>
  );
}
```

### Example 3: Input Field (Text State)

```tsx
function NameInput() {
  const [name, setName] = useState("");

  return (
    <div>
      <input
        type="text"
        placeholder="Enter your name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <p>Hello, {name || "Stranger"}! 👋</p>
    </div>
  );
}
```

---

## 📦 State with Objects

You can store objects in state too, but always **spread** the old values when updating:

```tsx
function UserForm() {
  const [user, setUser] = useState({
    name: "",
    email: "",
  });

  return (
    <div>
      <input
        placeholder="Name"
        value={user.name}
        onChange={(e) => setUser({ ...user, name: e.target.value })}
        // ↑ spread old values, then override the one that changed
      />
      <input
        placeholder="Email"
        value={user.email}
        onChange={(e) => setUser({ ...user, email: e.target.value })}
      />
      <p>{user.name} — {user.email}</p>
    </div>
  );
}
```

---

## 📋 State with Arrays

```tsx
function TodoList() {
  const [todos, setTodos] = useState(["Buy milk", "Go gym"]);
  const [input, setInput] = useState("");

  const addTodo = () => {
    if (input.trim()) {
      setTodos([...todos, input]);  // spread old todos + new one
      setInput("");
    }
  };

  const removeTodo = (index) => {
    setTodos(todos.filter((_, i) => i !== index));
  };

  return (
    <div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={addTodo}>Add</button>
      <ul>
        {todos.map((todo, index) => (
          <li key={index}>
            {todo} <button onClick={() => removeTodo(index)}>❌</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## ⚠️ Important Rules of State

### 1. NEVER mutate state directly
```tsx
// ❌ WRONG - modifying state directly won't trigger re-render
count = count + 1;
todos.push("New item");

// ✅ CORRECT - always use the setter function
setCount(count + 1);
setTodos([...todos, "New item"]);
```

### 2. State updates may be asynchronous
```tsx
// ❌ May cause bugs when relying on previous value
setCount(count + 1);
setCount(count + 1);  // second one uses stale count!

// ✅ Use functional update for previous value
setCount(prev => prev + 1);
setCount(prev => prev + 1);  // works correctly!
```

---

## ❌ Common Mistakes / Tips

- ❌ Mutating state directly (`state.value = newValue`)
- ❌ Forgetting to spread objects/arrays when updating
- ❌ Defining state outside a component
- ✅ Always use the setter function (`setState(...)`)
- ✅ Use functional updates `setState(prev => prev + 1)` when depending on previous value
- 💡 Multiple `useState` = totally fine! Use one per piece of data

---

## 📝 Summary

- **State** is data that changes and lives inside a component
- Use `useState(initialValue)` to create state
- Returns `[value, setter]` — update state only with the setter
- State change → React **re-renders** the component automatically
- Never mutate state directly — always use the setter
- Use spread `...` when updating objects or arrays

---

## 🎯 Practice Tasks

1. Build a **counter** with increment, decrement, and reset buttons
2. Build a **toggle** component (like a dark/light mode switch)
3. Build an **input** that shows what you're typing in real-time below it
4. Build a simple **Todo list** (add and remove todos)
5. Build a **traffic light** component: clicking cycles through 🔴 → 🟡 → 🟢

---

← Previous: [05_props.md](05_props.md) | Next: [07_event_handling.md](07_event_handling.md) →
