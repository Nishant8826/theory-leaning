# Custom Hooks — useAppDispatch & useAppSelector

---

## 1. What

Custom Redux hooks are **typed wrappers** around `useDispatch` and `useSelector` that save you from typing `RootState` and `AppDispatch` in every component.

```ts
// Instead of this in EVERY component:
const dispatch = useDispatch<AppDispatch>();
const count = useSelector((state: RootState) => state.counter.count);

// You write this ONCE and use everywhere:
const dispatch = useAppDispatch();
const count = useAppSelector((state) => state.counter.count);
// Type inference works automatically! ✨
```

---

## 2. Why

### The Problem:
```tsx
// ❌ Repeating types in every component is tedious and error-prone
import { useSelector, useDispatch } from "react-redux";
import { RootState, AppDispatch } from "../store";

function ComponentA() {
  const dispatch = useDispatch<AppDispatch>();     // Same generic every time
  const data = useSelector((state: RootState) => state.something); // Same type every time
}

function ComponentB() {
  const dispatch = useDispatch<AppDispatch>();     // Again!
  const data = useSelector((state: RootState) => state.other);     // Again!
}

// Multiply this by 50+ components...
```

### The Solution:
```tsx
// ✅ Define once, use everywhere
import { useAppDispatch, useAppSelector } from "../hooks";

function ComponentA() {
  const dispatch = useAppDispatch();          // Typed!
  const data = useAppSelector((state) => state.something); // Auto-typed!
}

function ComponentB() {
  const dispatch = useAppDispatch();
  const data = useAppSelector((state) => state.other);
}
```

---

## 3. How

### Creating the Custom Hooks:

```ts
// hooks.ts (or hooks/redux.ts)
import { useDispatch, useSelector, TypedUseSelectorHook } from "react-redux";
import type { RootState, AppDispatch } from "./store";

// Typed dispatch hook — supports thunks!
export const useAppDispatch = () => useDispatch<AppDispatch>();

// Typed selector hook — auto-infers state type!
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

That's it! Two lines of code that save you hundreds of type annotations.

---

## 4. Implementation

### Complete Setup:

```ts
// lib/store.ts
import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./features/counter/counterSlice";
import authReducer from "./features/auth/authSlice";
import todoReducer from "./features/todos/todoSlice";

const store = configureStore({
  reducer: {
    counter: counterReducer,
    auth: authReducer,
    todos: todoReducer,
  },
});

// These types are the foundation
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
```

```ts
// lib/hooks.ts
import { useDispatch, useSelector, TypedUseSelectorHook } from "react-redux";
import type { RootState, AppDispatch } from "./store";

// Use throughout your app instead of plain useDispatch and useSelector
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

### Usage in Components:

```tsx
// components/Counter.tsx
import { useAppDispatch, useAppSelector } from "../lib/hooks";
import { increment, decrement } from "../lib/features/counter/counterSlice";

function Counter() {
  const dispatch = useAppDispatch(); // ← Typed! Supports thunks!
  const count = useAppSelector((state) => state.counter.count);
  //                                      ↑ Full autocomplete!

  return (
    <div>
      <h1>{count}</h1>
      <button onClick={() => dispatch(increment())}>+</button>
      <button onClick={() => dispatch(decrement())}>-</button>
    </div>
  );
}
```

### Building More Custom Hooks:

```ts
// hooks/useAuth.ts
import { useAppSelector, useAppDispatch } from "../lib/hooks";
import { login, logout } from "../lib/features/auth/authSlice";

export function useAuth() {
  const dispatch = useAppDispatch();
  const user = useAppSelector((state) => state.auth.user);
  const isAuthenticated = useAppSelector((state) => state.auth.isAuthenticated);

  return {
    user,
    isAuthenticated,
    login: (credentials: { email: string; password: string }) =>
      dispatch(login(credentials)),
    logout: () => dispatch(logout()),
  };
}

// Usage:
function Header() {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <header>
      {isAuthenticated ? (
        <>
          <span>Welcome, {user?.name}</span>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <span>Please log in</span>
      )}
    </header>
  );
}
```

```ts
// hooks/useTodos.ts
import { useAppSelector, useAppDispatch } from "../lib/hooks";
import {
  addTodo,
  toggleTodo,
  deleteTodo,
  selectFilteredTodos,
} from "../lib/features/todos/todoSlice";

export function useTodos() {
  const dispatch = useAppDispatch();
  const todos = useAppSelector(selectFilteredTodos);
  const filter = useAppSelector((state) => state.todos.filter);

  return {
    todos,
    filter,
    addTodo: (text: string) =>
      dispatch(addTodo({ text, priority: "medium" })),
    toggleTodo: (id: string) => dispatch(toggleTodo(id)),
    deleteTodo: (id: string) => dispatch(deleteTodo(id)),
  };
}

// Usage — super clean!
function TodoList() {
  const { todos, addTodo, toggleTodo, deleteTodo } = useTodos();

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => toggleTodo(todo.id)}
          />
          {todo.text}
          <button onClick={() => deleteTodo(todo.id)}>❌</button>
        </li>
      ))}
    </ul>
  );
}
```

```ts
// hooks/useProducts.ts — With async operations
import { useEffect } from "react";
import { useAppSelector, useAppDispatch } from "../lib/hooks";
import {
  fetchProducts,
  createProduct,
  deleteProduct,
} from "../lib/features/products/productSlice";

export function useProducts() {
  const dispatch = useAppDispatch();
  const products = useAppSelector((state) => state.products.products);
  const loading = useAppSelector((state) => state.products.productsLoading);
  const error = useAppSelector((state) => state.products.productsError);

  // Auto-fetch on mount
  useEffect(() => {
    if (products.length === 0 && !loading) {
      dispatch(fetchProducts());
    }
  }, [dispatch, products.length, loading]);

  return {
    products,
    loading,
    error,
    refresh: () => dispatch(fetchProducts()),
    create: (data: { title: string; price: number }) =>
      dispatch(createProduct(data)).unwrap(),
    remove: (id: number) => dispatch(deleteProduct(id)).unwrap(),
  };
}

// Usage:
function ProductPage() {
  const { products, loading, error, refresh, remove } = useProducts();

  if (loading) return <p>Loading...</p>;
  if (error) return <button onClick={refresh}>Retry</button>;

  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>
          {p.title} - ${p.price}
          <button onClick={() => remove(p.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}
```

---

## 5. React Integration

Custom hooks are the **recommended pattern** for React + Redux apps:

```
📁 src/
├── lib/
│   ├── store.ts          ← Store + types
│   ├── hooks.ts          ← useAppDispatch, useAppSelector
│   └── features/
│       ├── auth/
│       │   └── authSlice.ts
│       └── todos/
│           └── todoSlice.ts
├── hooks/
│   ├── useAuth.ts        ← Feature-specific custom hooks
│   ├── useTodos.ts
│   └── useProducts.ts
└── components/
    ├── Header.tsx         ← Uses useAuth()
    ├── TodoList.tsx       ← Uses useTodos()
    └── ProductList.tsx    ← Uses useProducts()
```

---

## 6. Next.js Integration

### App Router:

```ts
// lib/hooks.ts — Same as React
import { useDispatch, useSelector, TypedUseSelectorHook } from "react-redux";
import type { RootState, AppDispatch } from "./store";

export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

```tsx
// app/todos/page.tsx
"use client";

import { useTodos } from "@/hooks/useTodos";

export default function TodosPage() {
  const { todos, addTodo, toggleTodo } = useTodos();
  // Works perfectly in Next.js client components!

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id} onClick={() => toggleTodo(todo.id)}>
          {todo.text}
        </li>
      ))}
    </ul>
  );
}
```

---

## 7. Impact

### Benefits of Custom Hooks:
1. **Type safety** — types are inferred automatically
2. **Less boilerplate** — no `RootState` or `AppDispatch` in components
3. **Encapsulation** — feature logic is contained in hooks
4. **Reusability** — share logic across components
5. **Testability** — hooks can be tested independently
6. **Clean components** — components focus on rendering, not Redux logic

### This is the Official Recommendation:
From the [Redux docs](https://redux.js.org/usage/usage-with-typescript):
> "We recommend creating typed versions of useDispatch and useSelector hooks."

---

## 8. Summary

- Create `useAppDispatch` and `useAppSelector` in a `hooks.ts` file
- These provide **automatic type inference** — no more manual typing
- Build **feature-specific hooks** that encapsulate Redux logic (e.g., `useAuth`, `useTodos`)
- Custom hooks make components **cleaner** — they just consume data, not manage it
- This is the **officially recommended pattern** by the Redux team
- Works identically in React and Next.js (client components only)

---

**Prev:** [15_use_dispatch.md](./15_use_dispatch.md) | **Next:** [17_rtk_query_introduction.md](./17_rtk_query_introduction.md)
