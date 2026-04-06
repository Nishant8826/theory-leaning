# Data Flow in Redux

---

## 1. What

Redux data flow is the **predictable, one-way cycle** that every piece of state goes through when it changes. Unlike two-way data binding (like in Angular), Redux enforces a **strict unidirectional flow** — data always moves in one direction.

This is often called the **"Redux Cycle"** or **"Unidirectional Data Flow"**.

```
┌─────────────────────────────────────────────────┐
│                                                 │
│   UI ──dispatch──▶ Action ──▶ Reducer ──▶ Store │
│   ▲                                        │    │
│   └────────────── Re-render ◀──────────────┘    │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 2. Why

### Why is One-Way Flow Important?

**Two-way data flow (the problem):**
```
Component A changes state → State changes Component B → Component B changes state → 
State changes Component C → Component C changes state → ??? → 🔥 Chaos
```

When data flows in multiple directions, you get:
- **Cascading updates** — one change triggers another, triggering another...
- **Unpredictable behavior** — you can't tell what caused a specific change
- **Impossible debugging** — where did this value come from? Nobody knows.

**One-way data flow (the solution):**
```
User clicks button → Action dispatched → Reducer computes new state → 
Store updates → UI re-renders → Done ✅
```

Benefits:
- **Traceable** — you can follow the flow from trigger to result
- **Predictable** — same actions + same state = same result
- **Debuggable** — Redux DevTools show every step

---

## 3. How

### The Complete Redux Data Flow (Step-by-Step):

### Step 1: Something Happens in the UI
A user clicks a button, submits a form, or a timer fires.

```tsx
<button onClick={() => dispatch(increment())}>+1</button>
```

### Step 2: An Action is Dispatched
The component calls `dispatch()` with an action object.

```ts
// The action object that gets dispatched:
{
  type: "counter/increment",  // Created by createSlice
  payload: undefined           // No data needed for simple increment
}
```

### Step 3: The Store Receives the Action
The store passes the action to the **root reducer**.

```ts
// Internally, the store does something like:
const newState = rootReducer(currentState, action);
```

### Step 4: The Root Reducer Delegates to Slice Reducers
If you have multiple slices, each slice reducer gets called with its own portion of state.

```ts
// configureStore creates a root reducer that does this:
function rootReducer(state, action) {
  return {
    counter: counterReducer(state.counter, action),
    auth: authReducer(state.auth, action),
    cart: cartReducer(state.cart, action),
  };
}
```

### Step 5: The Matching Reducer Computes New State
Only the reducer that handles this action type will produce a different state.

```ts
// counterReducer handles "counter/increment"
case "counter/increment":
  state.count += 1; // Immer makes this safe
```

### Step 6: The Store Saves the New State
The store replaces its state with the new state returned by the root reducer.

### Step 7: Subscribed Components Re-Render
Components using `useSelector` check if their selected value changed. If it did, they re-render.

```tsx
// This component re-renders ONLY if state.counter.count changed
const count = useSelector((state: RootState) => state.counter.count);
```

### Complete Visual:

```
┌──────────────────────────────────────────────────────────────┐
│                    REDUX DATA FLOW                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. EVENT                                                    │
│     User interacts (clicks button / loads page)              │
│       ↓                                                      │
│  2. DISPATCH                                                 │
│     Sends action → dispatch(action / asyncThunk)             │
│       ↓                                                      │
│  3. ACTION                                                   │
│     Plain object OR async function                           │
│     { type, payload }                                        │
│       ↓                                                      │
│  4. MIDDLEWARE ⭐                                            │
│     Handles SIDE EFFECTS:                                    │
│     - API calls (fetch / axios)                              │
│     - Async logic (thunk / saga)                             │
│     - Logging / debugging                                    │
│     → Dispatches new actions (success/failure)               │
│       ↓                                                      │
│  5. REDUCER                                                  │
│     Pure function → updates state based on action            │
│       ↓                                                      │
│  6. NEW STATE                                                │
│     Updated immutable state object                           │
│       ↓                                                      │
│  7. STORE                                                    │
│     Central place that saves state                           │
│       ↓                                                      │
│  8. SELECTORS                                                │
│     useSelector reads updated state                          │
│       ↓                                                      │
│  9. RE-RENDER                                                │
│     UI updates automatically                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Implementation

### Full Working Example:

```ts
// counterSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface CounterState {
  count: number;
  lastAction: string;
  history: number[];
}

const initialState: CounterState = {
  count: 0,
  lastAction: "none",
  history: [0],
};

const counterSlice = createSlice({
  name: "counter",
  initialState,
  reducers: {
    increment(state) {
      state.count += 1;
      state.lastAction = "increment";
      state.history.push(state.count);
    },
    decrement(state) {
      state.count -= 1;
      state.lastAction = "decrement";
      state.history.push(state.count);
    },
    incrementBy(state, action: PayloadAction<number>) {
      state.count += action.payload;
      state.lastAction = `incrementBy(${action.payload})`;
      state.history.push(state.count);
    },
    reset(state) {
      state.count = 0;
      state.lastAction = "reset";
      state.history = [0];
    },
  },
});

export const { increment, decrement, incrementBy, reset } =
  counterSlice.actions;
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

```tsx
// Counter.tsx — Observe the data flow in action
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "./store";
import { increment, decrement, incrementBy, reset } from "./counterSlice";

function Counter() {
  // Step 8: SELECTOR — reads from the store
  const count = useSelector((state: RootState) => state.counter.count);
  const lastAction = useSelector(
    (state: RootState) => state.counter.lastAction
  );
  const history = useSelector((state: RootState) => state.counter.history);

  // Step 2: DISPATCH — the function that triggers the flow
  const dispatch = useDispatch();

  return (
    <div>
      {/* Step 9: UI renders based on current state */}
      <h1>Count: {count}</h1>
      <p>Last action: {lastAction}</p>
      <p>History: {history.join(" → ")}</p>

      {/* Step 1: User interaction triggers dispatch */}
      <button onClick={() => dispatch(increment())}>+1</button>
      <button onClick={() => dispatch(decrement())}>-1</button>
      <button onClick={() => dispatch(incrementBy(5))}>+5</button>
      <button onClick={() => dispatch(reset())}>Reset</button>
    </div>
  );
}

export default Counter;
```

### Tracing the Flow:

```
User clicks "+5"
  ↓
dispatch(incrementBy(5))
  ↓
Action created: { type: "counter/incrementBy", payload: 5 }
  ↓
Store passes to counterReducer:
  state = { count: 0, lastAction: "none", history: [0] }
  action = { type: "counter/incrementBy", payload: 5 }
  ↓
Reducer computes new state (via Immer):
  newState = { count: 5, lastAction: "incrementBy(5)", history: [0, 5] }
  ↓
Store updates: state.counter = newState
  ↓
useSelector detects change:
  - count: 0 → 5 ✅ (changed — re-render)
  - lastAction: "none" → "incrementBy(5)" ✅ (changed)
  - history: [0] → [0, 5] ✅ (changed)
  ↓
Component re-renders with new values
```

---

## 5. React Integration

### How React-Redux Hooks Fit Into the Data Flow:

```tsx
import { useSelector, useDispatch } from "react-redux";

function MyComponent() {
  // useSelector: SUBSCRIBES to the store
  // - Called after every dispatch
  // - Compares old value vs new value
  // - Re-renders ONLY if the selected value changed
  const value = useSelector((state: RootState) => state.slice.value);

  // useDispatch: Returns the store's dispatch function
  // - Used to send actions to the store
  // - Triggers the entire Redux cycle
  const dispatch = useDispatch();

  // The cycle:
  // 1. dispatch(action) → 2. reducer → 3. new state → 4. useSelector re-checks → 5. re-render
}
```

### Important: Selective Re-Rendering

```tsx
function ComponentA() {
  // Only re-renders when counter.count changes
  const count = useSelector((state: RootState) => state.counter.count);
  return <div>{count}</div>;
}

function ComponentB() {
  // Only re-renders when auth.user changes
  const user = useSelector((state: RootState) => state.auth.user);
  return <div>{user?.name}</div>;
}

// If you dispatch increment(), only ComponentA re-renders!
// ComponentB is unaffected because auth.user didn't change.
```

---

## 6. Next.js Integration

The data flow is identical in Next.js. The only difference is **where you initialize the store** and how **server-side rendering (SSR)** affects the initial state.

### App Router:
```tsx
// The flow is the same — Provider wraps everything
// Client components use useSelector/useDispatch as normal
// Server components CANNOT use Redux hooks (they don't have access to the store)
```

### Pages Router with SSR:
```tsx
// pages/index.tsx
import { GetServerSideProps } from "next";

export const getServerSideProps: GetServerSideProps = async () => {
  // Fetch initial data on the server
  const data = await fetchSomeData();

  return {
    props: {
      initialData: data,
    },
  };
};

// Then hydrate the store with this initial data
// (covered in detail in the SSR chapter)
```

---

## 7. Impact

### Why Understanding Data Flow Matters:

- **Debugging:** When something goes wrong, you can trace the flow:
  - What action was dispatched?
  - What did the reducer produce?
  - Did the selector select the right data?
- **Performance:** Understanding the flow helps you optimize:
  - Move expensive computations into selectors (memoized with `createSelector`)
  - Avoid unnecessary re-renders by selecting only what you need
- **Architecture:** The unidirectional flow scales to any size application

### Redux DevTools Shows the Entire Flow:
1. **Actions tab** — every action that was dispatched
2. **State tab** — the complete state after each action
3. **Diff tab** — what exactly changed in the state
4. **Time-travel** — jump to any point in the action history

---

## 8. Summary

- Redux uses **unidirectional (one-way) data flow**
- The cycle: **UI → dispatch → action → middleware → reducer → store → UI**
- Only **dispatching an action** can trigger a state change
- Each **slice reducer** handles its own portion of state
- `useSelector` causes re-renders **only when selected data changes**
- Redux DevTools visualize the entire flow for debugging
- The same flow works in React, Next.js, and any other framework

---

**Prev:** [03_core_concepts.md](./03_core_concepts.md) | **Next:** [05_redux_toolkit_introduction.md](./05_redux_toolkit_introduction.md)
