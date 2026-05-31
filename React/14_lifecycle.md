# 14 - Component Lifecycle 🔄

> [!NOTE]
> ### 💡 Topic Quick Overview (For Beginners)
> - **What is it?** Component lifecycle refers to the sequence of stages a React component goes through: mounting (creation), updating (re-rendering), and unmounting (destruction).
> - **Why do we use it?** Understanding lifecycle is vital for timing actions correctly, such as fetching data when a page loads or clearing memory when a component leaves the screen.
> - **How does it work?** In class components, use lifecycle methods (`componentDidMount`, `componentDidUpdate`, `componentWillUnmount`). In functional components, use `useEffect` configurations.

---

## 🤔 What is the Component Lifecycle?

Every React component goes through a **lifecycle** — it gets created, shows on screen, updates when data changes, and eventually gets removed.

> **Real-world analogy:**
> Think of a plant's life cycle — 🌱 Seed (mount) → 🌿 Growing (update) → 🍂 Dying (unmount). React components follow the same pattern!

---

## 🔄 Three Lifecycle Phases

```
1. MOUNTING   → Component is created and added to the DOM
2. UPDATING   → Component re-renders (state or props changed)
3. UNMOUNTING → Component is removed from the DOM
```

---

## 🏗️ Lifecycle in Functional Components (with useEffect)

In modern React, you handle lifecycle with `useEffect`:

```jsx
import { useState, useEffect } from "react";

function MyComponent() {
  const [count, setCount] = useState(0);

  // 1. MOUNT — runs once when component appears
  useEffect(() => {
    console.log("✅ Component Mounted!");

    // 3. UNMOUNT — cleanup runs when component disappears
    return () => {
      console.log("❌ Component Unmounted!");
    };
  }, []); // empty array = only on mount/unmount

  // 2. UPDATE — runs when `count` changes
  useEffect(() => {
    console.log("🔄 Count updated to:", count);
  }, [count]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
}
```

---

## 📜 Lifecycle in Class Components (for reference)

Even though class components are old, you might encounter them in legacy code:

```jsx
import React, { Component } from "react";

class MyComponent extends Component {
  // 1. MOUNTING
  constructor(props) {
    super(props);
    this.state = { count: 0 };
    console.log("🌱 Constructor called");
  }

  componentDidMount() {
    console.log("✅ Mounted! API calls go here.");
  }

  // 2. UPDATING
  componentDidUpdate(prevProps, prevState) {
    if (prevState.count !== this.state.count) {
      console.log("🔄 Count changed to:", this.state.count);
    }
  }

  // 3. UNMOUNTING
  componentWillUnmount() {
    console.log("❌ Unmounted! Cleanup goes here.");
  }

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={() => this.setState({ count: this.state.count + 1 })}>
          +1
        </button>
      </div>
    );
  }
}
```

---

## 🗺️ Lifecycle Phase Mapping

| Class Method | Functional Hook Equivalent |
|---|---|
| `componentDidMount` | `useEffect(() => {...}, [])` |
| `componentDidUpdate` | `useEffect(() => {...}, [dep])` |
| `componentWillUnmount` | Return cleanup from `useEffect` |
| `constructor` + `this.state` | `useState()` |
| `shouldComponentUpdate` | `React.memo` |

---

## 🌍 Real-World Lifecycle Examples

### Example 1: Real Mounting/Unmounting

```jsx
function Parent() {
  const [showChild, setShowChild] = useState(true);

  return (
    <div>
      <button onClick={() => setShowChild(!showChild)}>
        {showChild ? "Remove Component" : "Add Component"}
      </button>

      {showChild && <ChildWithLifecycle />}
    </div>
  );
}

function ChildWithLifecycle() {
  useEffect(() => {
    console.log("Child mounted ✅");

    return () => {
      console.log("Child unmounted ❌ — cleanup done!");
    };
  }, []);

  return <div>👋 I'm the child component!</div>;
}
```

### Example 2: Data Fetching on Mount

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Mount or userId changes → fetch new user
    console.log(`Fetching user ${userId}...`);

    fetch(`https://jsonplaceholder.typicode.com/users/${userId}`)
      .then((res) => res.json())
      .then((data) => setUser(data));

    return () => {
      console.log("Cleanup: cancelling old request...");
    };
  }, [userId]); // Re-runs when userId changes (like navigating profiles)

  if (!user) return <p>Loading...</p>;

  return (
    <div>
      <h2>{user.name}</h2>
      <p>Email: {user.email}</p>
    </div>
  );
}
```

### Example 3: WebSocket Connection

```jsx
function ChatRoom({ roomId }) {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // MOUNT: Connect to chat room
    const socket = connectToRoom(roomId);
    socket.on("message", (msg) => setMessages((prev) => [...prev, msg]));
    console.log(`Connected to room: ${roomId}`);

    // UNMOUNT: Disconnect when leaving
    return () => {
      socket.disconnect();
      console.log(`Disconnected from room: ${roomId}`);
    };
  }, [roomId]);

  return (
    <div>
      <h2>Room: {roomId}</h2>
      {messages.map((msg, i) => <p key={i}>{msg}</p>)}
    </div>
  );
}
```

---

## 🔄 Every Render Flow

```
User action (click / type)
    ↓
State / Props updates
    ↓
React re-renders component
    ↓
useEffect cleanup (from previous render)
    ↓
New useEffect runs
```

---

## ❌ Common Mistakes / Tips

- ❌ Forgetting cleanup in `useEffect` → memory leaks (open sockets, timers, listeners)
- ❌ Putting API calls in render body instead of `useEffect`
- ✅ Mount = component appears, Unmount = component disappears
- ✅ `useEffect` with `[]` = componentDidMount
- ✅ Return from `useEffect` = componentWillUnmount
- 💡 In `React.StrictMode` (development), effects run TWICE intentionally — this is normal!

---

## 📝 Summary

| Phase | When | useEffect Pattern |
|---|---|---|
| Mount | Component appears | `useEffect(() => {...}, [])` |
| Update | State/props change | `useEffect(() => {...}, [dep])` |
| Unmount | Component removed | Return cleanup function |

---

← Previous: [13_useMemo_useCallback.md](13_useMemo_useCallback.md) | Index: [00_Index.md](00_Index.md) | Next: [15_lifting_state_up.md](15_lifting_state_up.md) →
