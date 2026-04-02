# What is Redux?

---

## 1. What

**Redux** is a **predictable state management library** for JavaScript applications. Think of it as a **single, centralized place** where all your application's data (state) lives.

Imagine your app is a big office building. Instead of every room (component) keeping its own notes and files scattered everywhere, Redux is like having **one central filing cabinet** that everyone reads from and writes to — in an organized, traceable way.

### Key Points:
- Redux is **not** tied to React — it can work with any UI framework or even vanilla JavaScript.
- Redux stores **all your app's state** in one JavaScript object called the **store**.
- State can only be changed by sending a description of what happened (called an **action**).
- A pure function (called a **reducer**) takes the current state + action and returns a new state.

### Simple Analogy:
```
You (User) → Send a request (Action) → Office clerk processes it (Reducer) → Filing cabinet updates (Store) → Everyone sees the update (UI re-renders)
```

---

## 2. Why

### Problems Redux Solves:

**Problem 1: Prop Drilling**
Without Redux, if a deeply nested component needs data from a top-level component, you have to pass that data through every component in between — even if those middle components don't need it.

```
App → Dashboard → Sidebar → UserProfile → Avatar (needs user data)
// Without Redux: pass "user" through ALL 4 levels
// With Redux: Avatar directly reads from the store
```

**Problem 2: Shared State Between Unrelated Components**
When two components that are far apart in the component tree need the same data, managing that state becomes messy.

**Problem 3: Unpredictable State Changes**
When multiple components can update state in different ways, it becomes hard to track **what changed**, **when**, and **why**.

**Problem 4: Debugging Nightmares**
Without a centralized system, tracking down bugs related to state is extremely difficult.

### Redux Solves These By:
- **Single source of truth** — one store holds everything
- **Predictable updates** — only reducers can change state, and they follow strict rules
- **Time-travel debugging** — you can replay every state change step by step
- **Traceable changes** — every change has a named action describing what happened

---

## 3. How

### How Redux Works Internally (Step-by-Step):

```
1. The STORE holds the entire state of your application
2. A component wants to change something → it DISPATCHES an ACTION
3. The ACTION is a plain object: { type: "ADD_TODO", payload: "Learn Redux" }
4. The REDUCER receives (currentState, action) and returns a NEW state
5. The STORE updates with the new state
6. All subscribed components RE-RENDER with the new data
```

### Visual Flow:
```
UI Component
    ↓ dispatch(action)
Action { type: "INCREMENT" }
    ↓
Reducer(state, action) → newState
    ↓
Store (updated)
    ↓
UI Component (re-renders)
```

### Core Rules:
1. **State is read-only** — you can never directly mutate it
2. **Changes are made with pure functions** — reducers must be predictable (same input = same output)
3. **Single source of truth** — one store for the entire app

---

## 4. Implementation

### Legacy Redux (For Understanding — Don't Use in Production):

```ts
// types.ts
interface CounterState {
  count: number;
}

interface IncrementAction {
  type: "INCREMENT";
}

interface DecrementAction {
  type: "DECREMENT";
}

interface IncrementByAction {
  type: "INCREMENT_BY";
  payload: number;
}

type CounterAction = IncrementAction | DecrementAction | IncrementByAction;

// reducer.ts
const initialState: CounterState = { count: 0 };

function counterReducer(
  state: CounterState = initialState,
  action: CounterAction
): CounterState {
  switch (action.type) {
    case "INCREMENT":
      // Return a NEW object — never mutate the old state
      return { ...state, count: state.count + 1 };
    case "DECREMENT":
      return { ...state, count: state.count - 1 };
    case "INCREMENT_BY":
      return { ...state, count: state.count + action.payload };
    default:
      return state;
  }
}

// store.ts
import { createStore } from "redux";

const store = createStore(counterReducer);

// Usage
store.dispatch({ type: "INCREMENT" });
console.log(store.getState()); // { count: 1 }

store.dispatch({ type: "INCREMENT_BY", payload: 5 });
console.log(store.getState()); // { count: 6 }
```

### Modern Redux Toolkit (Recommended):

```ts
// counterSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface CounterState {
  count: number;
}

const initialState: CounterState = { count: 0 };

const counterSlice = createSlice({
  name: "counter",           // A unique name for this slice
  initialState,              // The starting state
  reducers: {
    increment(state) {
      state.count += 1;      // Looks like mutation, but Immer handles it safely
    },
    decrement(state) {
      state.count -= 1;
    },
    incrementBy(state, action: PayloadAction<number>) {
      state.count += action.payload;
    },
  },
});

// Export actions (auto-generated)
export const { increment, decrement, incrementBy } = counterSlice.actions;

// Export reducer
export default counterSlice.reducer;
```

```ts
// store.ts
import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./counterSlice";

const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;
```

---

## 5. React Integration

### Setting Up Redux with React:

```tsx
// main.tsx (or index.tsx)
import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import store from "./store";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    {/* Provider makes the store available to ALL components */}
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);
```

```tsx
// Counter.tsx
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "./store";
import { increment, decrement, incrementBy } from "./counterSlice";

function Counter() {
  // Read state from the store
  const count = useSelector((state: RootState) => state.counter.count);

  // Get the dispatch function
  const dispatch = useDispatch();

  return (
    <div>
      <h1>Count: {count}</h1>
      <button onClick={() => dispatch(increment())}>+1</button>
      <button onClick={() => dispatch(decrement())}>-1</button>
      <button onClick={() => dispatch(incrementBy(10))}>+10</button>
    </div>
  );
}

export default Counter;
```

---

## 6. Next.js Integration

### App Router:

```tsx
// app/StoreProvider.tsx
"use client";

import { Provider } from "react-redux";
import store from "@/lib/store";

export default function StoreProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return <Provider store={store}>{children}</Provider>;
}

// app/layout.tsx
import StoreProvider from "./StoreProvider";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <StoreProvider>{children}</StoreProvider>
      </body>
    </html>
  );
}
```

### Pages Router:

```tsx
// pages/_app.tsx
import type { AppProps } from "next/app";
import { Provider } from "react-redux";
import store from "@/lib/store";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <Provider store={store}>
      <Component {...pageProps} />
    </Provider>
  );
}
```

---

## 7. Impact

### Real-World Impact:
- **Used by millions** of developers worldwide — it's the most popular state management solution for React
- **Predictable debugging** — Redux DevTools let you inspect every action and state change
- **Team collaboration** — clear, standardized patterns make it easy for teams to work together
- **Scalability** — from small apps to enterprise-level applications

### When to Use Redux:
- ✅ Large applications with lots of shared state
- ✅ When multiple components need the same data
- ✅ When you need to track state changes over time
- ✅ Complex state logic with many interactions

### When NOT to Use Redux:
- ❌ Small apps with simple state (use `useState` / `useContext`)
- ❌ State that only one component uses (keep it local)
- ❌ When React Query / RTK Query handles your server state

---

## 8. Summary

- **Redux** is a predictable state management library
- It uses a **single store** to hold all application state
- State changes happen through **actions** (what happened) and **reducers** (how state changes)
- **Redux Toolkit (RTK)** is the modern, recommended way to write Redux
- Redux integrates with React via the **react-redux** library (`Provider`, `useSelector`, `useDispatch`)
- It solves **prop drilling**, **shared state**, and **debugging** problems
- Use Redux for **complex, shared state** — not for every piece of state

---

**Prev:** None | **Next:** [02_why_redux.md](./02_why_redux.md)
