# useSelector — Reading State from the Store

---

## 1. What

`useSelector` is a React-Redux hook that lets you **read data from the Redux store** inside a component. Think of it as a **window into the store** — you tell it what you want to see, and it shows you.

```tsx
const value = useSelector((state: RootState) => state.counter.count);
// "Hey Redux, give me the counter's count value"
```

### Key Behavior:
- It runs your **selector function** after every dispatched action
- It **compares** the new value with the old value
- If the value **changed**, the component **re-renders**
- If the value **didn't change**, the component **skips** re-rendering

---

## 2. Why

### Without useSelector:
In legacy Redux, you had to use `connect()` — a higher-order component (HOC) that was verbose and confusing:

```tsx
// ❌ Legacy connect — verbose!
const mapStateToProps = (state) => ({
  count: state.counter.count,
  user: state.auth.user,
});

export default connect(mapStateToProps)(MyComponent);
```

### With useSelector:
```tsx
// ✅ Modern hook — clean and simple!
function MyComponent() {
  const count = useSelector((state: RootState) => state.counter.count);
  const user = useSelector((state: RootState) => state.auth.user);
}
```

---

## 3. How

### How useSelector Works Internally:

```
1. Component mounts → useSelector runs the selector function
2. Selector returns a value → this is the "current" value
3. An action is dispatched somewhere
4. useSelector runs the selector AGAIN
5. Compares new value with old value using === (strict equality)
6. If different → re-render the component
7. If same → skip re-render (performance optimization!)
```

### Important: Reference Equality (===)

```ts
// Primitive values — works great!
const count = useSelector((state: RootState) => state.counter.count);
// 5 === 5 → true → no re-render ✅
// 5 === 6 → false → re-render ✅

// Objects — be careful!
const user = useSelector((state: RootState) => state.auth.user);
// If user object reference changes → re-render (even if contents are same)

// ❌ DANGER: Creating new objects in selector
const data = useSelector((state: RootState) => ({
  count: state.counter.count,
  name: state.auth.user?.name,
}));
// This creates a NEW object every time → ALWAYS re-renders! 😱
```

---

## 4. Implementation

### Basic Selectors:

```tsx
import { useSelector } from "react-redux";
import { RootState } from "../store";

function Dashboard() {
  // ─── Simple value selector ───
  const count = useSelector((state: RootState) => state.counter.count);

  // ─── Nested value selector ───
  const userName = useSelector((state: RootState) => state.auth.user?.name);

  // ─── Boolean selector ───
  const isAuthenticated = useSelector(
    (state: RootState) => state.auth.isAuthenticated
  );

  // ─── Array selector ───
  const todos = useSelector((state: RootState) => state.todos.items);

  // ─── Computed value selector ───
  const completedCount = useSelector(
    (state: RootState) =>
      state.todos.items.filter((t) => t.completed).length
  );

  return (
    <div>
      <p>Count: {count}</p>
      <p>User: {userName ?? "Guest"}</p>
      <p>{isAuthenticated ? "Logged in" : "Not logged in"}</p>
      <p>Todos: {todos.length}</p>
      <p>Completed: {completedCount}</p>
    </div>
  );
}
```

### Pre-Defined Selectors (Recommended):

```ts
// features/todos/todoSlice.ts
// Co-locate selectors with the slice!

export const selectAllTodos = (state: RootState) => state.todos.items;

export const selectTodoById = (state: RootState, id: string) =>
  state.todos.items.find((t) => t.id === id);

export const selectCompletedTodos = (state: RootState) =>
  state.todos.items.filter((t) => t.completed);

export const selectActiveTodos = (state: RootState) =>
  state.todos.items.filter((t) => !t.completed);

export const selectTodoCount = (state: RootState) => state.todos.items.length;

// Usage in components:
function TodoList() {
  const todos = useSelector(selectAllTodos);
  const completedTodos = useSelector(selectCompletedTodos);
  // Much cleaner!
}
```

### Memoized Selectors with createSelector:

```ts
import { createSelector } from "@reduxjs/toolkit";

// Problem: filter creates a new array every time → unnecessary re-renders
// Solution: createSelector memoizes the result

const selectTodos = (state: RootState) => state.todos.items;
const selectFilter = (state: RootState) => state.todos.filter;

// This only recomputes when selectTodos or selectFilter return new values
export const selectFilteredTodos = createSelector(
  [selectTodos, selectFilter],
  (todos, filter) => {
    // This computation only runs if todos or filter changed
    switch (filter) {
      case "active":
        return todos.filter((t) => !t.completed);
      case "completed":
        return todos.filter((t) => t.completed);
      default:
        return todos;
    }
  }
);

// More complex memoized selector
export const selectTodoStats = createSelector([selectTodos], (todos) => ({
  total: todos.length,
  completed: todos.filter((t) => t.completed).length,
  active: todos.filter((t) => !t.completed).length,
  // This object is only recreated when todos actually change
}));

// Usage:
function TodoStats() {
  const stats = useSelector(selectTodoStats);
  // Only re-renders when todos actually change!
  return (
    <div>
      Total: {stats.total} | Done: {stats.completed} | Active: {stats.active}
    </div>
  );
}
```

### Common Mistakes and Fixes:

```tsx
// ❌ MISTAKE 1: Creating new objects/arrays inline
function BadComponent() {
  const data = useSelector((state: RootState) => ({
    count: state.counter.count,
    name: state.auth.user?.name,
  }));
  // NEW object every time → always re-renders!
}

// ✅ FIX 1: Separate selectors
function GoodComponent() {
  const count = useSelector((state: RootState) => state.counter.count);
  const name = useSelector((state: RootState) => state.auth.user?.name);
  // Each selector returns a primitive → efficient!
}

// ✅ FIX 2: Use createSelector for derived data
const selectDashboardData = createSelector(
  [(state: RootState) => state.counter.count, (state: RootState) => state.auth.user?.name],
  (count, name) => ({ count, name })
);

function BetterComponent() {
  const data = useSelector(selectDashboardData);
  // Only recomputes when count or name changes!
}

// ❌ MISTAKE 2: Using useSelector in a loop
function BadList() {
  const ids = useSelector((state: RootState) => state.todos.items.map((t) => t.id));
  // .map creates a new array every time → always re-renders!
}

// ✅ FIX: Memoize with createSelector
const selectTodoIds = createSelector(
  [(state: RootState) => state.todos.items],
  (items) => items.map((t) => t.id)
);
```

---

## 5. React Integration

### useSelector with TypeScript:

```tsx
import { useSelector, TypedUseSelectorHook } from "react-redux";
import { RootState } from "../store";

// Create a typed version (recommended!)
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// Now you get full type inference without typing RootState every time:
function MyComponent() {
  const count = useAppSelector((state) => state.counter.count);
  //                                      ↑ fully typed!
}
```

### Equality Function:

```tsx
import { useSelector, shallowEqual } from "react-redux";

// Use shallowEqual when selecting objects or arrays
function UserProfile() {
  const user = useSelector(
    (state: RootState) => state.auth.user,
    shallowEqual // Compare by shallow equality instead of reference
  );
  // Only re-renders if user properties actually changed
}
```

---

## 6. Next.js Integration

Works identically — `useSelector` is a client-side hook:

```tsx
// app/dashboard/page.tsx
"use client"; // Must be a client component!

import { useSelector } from "react-redux";
import { RootState } from "@/lib/store";

export default function DashboardPage() {
  const count = useSelector((state: RootState) => state.counter.count);
  return <h1>Count: {count}</h1>;
}
```

> **Important:** Server Components in Next.js **cannot** use `useSelector`. Only Client Components can.

---

## 7. Impact

### Performance Rules:
1. **Select the smallest piece of state** you need
2. **Never create new objects/arrays** inside the selector function
3. **Use createSelector** for derived/computed data
4. **Use shallowEqual** when you must select objects
5. **Multiple small selectors** > one large selector

### useSelector vs Other Approaches:

| Approach | Re-render Trigger |
|----------|-------------------|
| `useSelector(s => s.counter.count)` | Only when count changes ✅ |
| `useSelector(s => s.counter)` | When ANY counter field changes |
| `useSelector(s => ({ ...s.counter }))` | EVERY dispatch ❌ |
| `useSelector(s => s.counter, shallowEqual)` | When any top-level property changes |

---

## 8. Summary

- `useSelector` reads data from the Redux store
- It accepts a **selector function**: `(state) => value`
- Uses **strict equality** (`===`) to decide if a re-render is needed
- **Never create new objects/arrays** inside the selector (causes unnecessary re-renders)
- Use **createSelector** from RTK for memoized/computed selectors
- Use **shallowEqual** as a second argument for object comparisons
- Define selectors in the **slice file** and export them (co-location)
- Create a **typed useAppSelector** hook for TypeScript projects
- In Next.js, only **Client Components** can use `useSelector`

---

**Prev:** [13_provider.md](./13_provider.md) | **Next:** [15_use_dispatch.md](./15_use_dispatch.md)
