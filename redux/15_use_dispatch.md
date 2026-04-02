# useDispatch — Dispatching Actions to the Store

---

## 1. What

`useDispatch` is a React-Redux hook that gives you the **dispatch function**. This function is the **only way** to send actions to the Redux store and trigger state changes.

```tsx
const dispatch = useDispatch();
dispatch(increment()); // Send an action to the store
```

Think of `dispatch` as a **mailbox** — you put your "letter" (action) in it, and Redux delivers it to the right "department" (reducer).

---

## 2. Why

### Without useDispatch (Legacy):
```tsx
// ❌ Legacy connect — verbose!
const mapDispatchToProps = {
  increment,
  decrement,
  addTodo,
};

export default connect(null, mapDispatchToProps)(MyComponent);
```

### With useDispatch:
```tsx
// ✅ Modern hook — simple and direct!
function MyComponent() {
  const dispatch = useDispatch();
  dispatch(increment()); // Done!
}
```

---

## 3. How

### How useDispatch Works:

```
1. useDispatch() returns the store's dispatch function
2. You call dispatch(action) with an action object
3. The action goes through middleware (thunks, etc.)
4. Then the action reaches the reducer
5. Reducer computes new state
6. Store updates
7. useSelector detects changes → re-renders
```

### What Can You Dispatch?

```ts
// 1. Regular action objects (from createSlice)
dispatch(increment());                  // { type: "counter/increment" }
dispatch(addTodo("Learn Redux"));       // { type: "todos/addTodo", payload: "Learn Redux" }

// 2. Thunk functions (for async logic)
dispatch(fetchUsers());                  // Function → handled by thunk middleware

// 3. createAsyncThunk actions
dispatch(fetchPosts());                  // Dispatches pending/fulfilled/rejected

// 4. RTK Query hook calls handle dispatch internally
// You don't dispatch manually with RTK Query hooks
```

---

## 4. Implementation

### Basic Usage:

```tsx
import { useDispatch } from "react-redux";
import { increment, decrement, incrementBy } from "../features/counter/counterSlice";
import { AppDispatch } from "../store";

function Counter() {
  // Basic dispatch
  const dispatch = useDispatch();

  // Better: Typed dispatch for async thunks
  const typedDispatch = useDispatch<AppDispatch>();

  return (
    <div>
      {/* Dispatch simple actions */}
      <button onClick={() => dispatch(increment())}>+1</button>
      <button onClick={() => dispatch(decrement())}>-1</button>

      {/* Dispatch action with payload */}
      <button onClick={() => dispatch(incrementBy(10))}>+10</button>
    </div>
  );
}
```

### Dispatching in Event Handlers:

```tsx
import { useDispatch } from "react-redux";
import { AppDispatch } from "../store";
import { login, logout } from "../features/auth/authSlice";
import { addTodo, deleteTodo } from "../features/todos/todoSlice";
import { useState, FormEvent } from "react";

function TodoForm() {
  const [text, setText] = useState("");
  const dispatch = useDispatch<AppDispatch>();

  // ─── Form Submit ───
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (text.trim()) {
      dispatch(addTodo({ text: text.trim(), priority: "medium" }));
      setText("");
    }
  };

  // ─── Click Handler ───
  const handleDelete = (id: string) => {
    dispatch(deleteTodo(id));
  };

  // ─── Conditional Dispatch ───
  const handleLogin = () => {
    const user = { name: "Nishant", email: "nishant@example.com" };
    dispatch(login({ user, token: "abc123" }));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Add todo..."
      />
      <button type="submit">Add</button>
      <button type="button" onClick={handleLogin}>Login</button>
    </form>
  );
}
```

### Dispatching Async Thunks:

```tsx
import { useDispatch } from "react-redux";
import { AppDispatch } from "../store";
import { fetchPosts, createPost, deletePost } from "../features/posts/postSlice";
import { useEffect } from "react";

function PostManager() {
  const dispatch = useDispatch<AppDispatch>();

  // ─── Dispatch on mount ───
  useEffect(() => {
    dispatch(fetchPosts());
  }, [dispatch]);

  // ─── Dispatch with .unwrap() for error handling ───
  const handleCreate = async () => {
    try {
      const newPost = await dispatch(
        createPost({ title: "New Post", body: "Content", userId: 1 })
      ).unwrap(); // unwrap() throws if rejected!

      console.log("Created:", newPost);
    } catch (error) {
      console.error("Failed:", error);
    }
  };

  // ─── Dispatch with confirmation ───
  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure?")) return;

    try {
      await dispatch(deletePost(id)).unwrap();
      alert("Deleted!");
    } catch (error) {
      alert("Delete failed!");
    }
  };

  return (
    <div>
      <button onClick={handleCreate}>Create Post</button>
    </div>
  );
}
```

### Dispatching Multiple Actions:

```tsx
function UserDashboard() {
  const dispatch = useDispatch<AppDispatch>();

  // Dispatch multiple actions in sequence
  const handleLogout = () => {
    dispatch(clearCart());         // Clear cart
    dispatch(clearNotifications()); // Clear notifications
    dispatch(logout());            // Log out
    dispatch(resetTheme());        // Reset theme
  };

  // Better: Use a shared action (covered in file 08)
  const handleLogoutBetter = () => {
    dispatch(logout()); // One action, multiple slices handle it via extraReducers
  };

  return <button onClick={handleLogoutBetter}>Logout</button>;
}
```

---

## 5. React Integration

### Passing dispatch to Child Components:

```tsx
// ❌ Don't pass dispatch as a prop (anti-pattern)
function Parent() {
  const dispatch = useDispatch();
  return <Child dispatch={dispatch} />; // ❌
}

// ✅ Let each component call useDispatch
function Child() {
  const dispatch = useDispatch(); // ✅ Each component gets its own
  return <button onClick={() => dispatch(increment())}>+1</button>;
}
```

### Using dispatch in useCallback:

```tsx
import { useCallback } from "react";
import { useDispatch } from "react-redux";
import { AppDispatch } from "../store";
import { deleteTodo } from "../features/todos/todoSlice";

function TodoItem({ id, text }: { id: string; text: string }) {
  const dispatch = useDispatch<AppDispatch>();

  // Memoize the handler to prevent unnecessary re-renders of children
  const handleDelete = useCallback(() => {
    dispatch(deleteTodo(id));
  }, [dispatch, id]);

  return (
    <li>
      {text}
      <button onClick={handleDelete}>Delete</button>
    </li>
  );
}
```

---

## 6. Next.js Integration

### App Router:

```tsx
// app/counter/page.tsx
"use client"; // Required for hooks!

import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "@/lib/store";
import { increment } from "@/lib/features/counter/counterSlice";

export default function CounterPage() {
  const dispatch = useDispatch<AppDispatch>();
  const count = useSelector((state: RootState) => state.counter.count);

  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={() => dispatch(increment())}>+1</button>
    </div>
  );
}
```

### Pages Router:
```tsx
// pages/counter.tsx
// Works the same — no "use client" needed in Pages Router
```

---

## 7. Impact

### dispatch Rules:
1. **Always type it** as `AppDispatch` for async thunk support
2. **Never call it conditionally** inside hooks (React rules of hooks)
3. **Use .unwrap()** when you need to handle async results in components
4. **dispatch is stable** — its reference never changes, so it's safe in dependency arrays

### Common Pattern — Action + Feedback:

```tsx
const handleSave = async () => {
  setIsSaving(true);
  try {
    await dispatch(saveData(formData)).unwrap();
    toast.success("Saved successfully!");
    navigate("/dashboard");
  } catch (error) {
    toast.error("Save failed. Please try again.");
  } finally {
    setIsSaving(false);
  }
};
```

---

## 8. Summary

- `useDispatch` returns the store's **dispatch function**
- Use it to send **actions** (sync or async) to the store
- Type it as `useDispatch<AppDispatch>()` for TypeScript support
- Use `.unwrap()` on async thunks for component-level error handling
- **dispatch is stable** — safe to include in `useEffect` / `useCallback` dependency arrays
- Each component should call `useDispatch` directly — don't pass it as a prop
- In Next.js, only **Client Components** can use `useDispatch`
- Prefer dispatching **one shared action** over multiple separate actions for related state changes

---

**Prev:** [14_use_selector.md](./14_use_selector.md) | **Next:** [16_custom_hooks.md](./16_custom_hooks.md)
