# Redux Toolkit (RTK) — Introduction

---

## 1. What

**Redux Toolkit (RTK)** is the **official, recommended way** to write Redux code. It's like Redux, but with all the boilerplate stripped away and best practices built in.

Think of it this way:
- **Legacy Redux** = building a car from scratch (engine, chassis, wiring, everything)
- **Redux Toolkit** = buying a car that's already assembled with everything you need

RTK is NOT a different library — it IS Redux, just with better tools and defaults.

### What RTK Includes:
| Tool | Purpose |
|------|---------|
| `configureStore` | Creates the store with good defaults |
| `createSlice` | Creates reducer + actions in one step |
| `createAsyncThunk` | Handles async logic (API calls) |
| `createApi` (RTK Query) | Complete data fetching & caching solution |
| Immer | Write "mutating" code that's actually immutable |
| Redux DevTools | Auto-configured for debugging |
| Middleware | Thunk middleware included by default |

---

## 2. Why

### The Problem with Legacy Redux:

```ts
// ❌ Legacy Redux — TOO MUCH BOILERPLATE!

// Step 1: Define action type constants
const INCREMENT = "counter/INCREMENT";
const DECREMENT = "counter/DECREMENT";
const INCREMENT_BY = "counter/INCREMENT_BY";

// Step 2: Define action creator functions
function increment() {
  return { type: INCREMENT };
}

function decrement() {
  return { type: DECREMENT };
}

function incrementBy(amount: number) {
  return { type: INCREMENT_BY, payload: amount };
}

// Step 3: Define the reducer with immutable updates
function counterReducer(state = { count: 0 }, action: any) {
  switch (action.type) {
    case INCREMENT:
      return { ...state, count: state.count + 1 }; // Must spread manually
    case DECREMENT:
      return { ...state, count: state.count - 1 };
    case INCREMENT_BY:
      return { ...state, count: state.count + action.payload };
    default:
      return state;
  }
}

// Step 4: Configure the store manually
import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import { composeWithDevTools } from "redux-devtools-extension";

const rootReducer = combineReducers({
  counter: counterReducer,
});

const store = createStore(
  rootReducer,
  composeWithDevTools(applyMiddleware(thunk))
);
```

**That's 40+ lines just for a counter!** 😩

### The Solution with Redux Toolkit:

```ts
// ✅ Redux Toolkit — Clean and Simple!

// Step 1: Create a slice (reducer + actions in one!)
import { createSlice, PayloadAction, configureStore } from "@reduxjs/toolkit";

const counterSlice = createSlice({
  name: "counter",
  initialState: { count: 0 },
  reducers: {
    increment(state) {
      state.count += 1; // "Mutation" is safe, thanks to Immer!
    },
    decrement(state) {
      state.count -= 1;
    },
    incrementBy(state, action: PayloadAction<number>) {
      state.count += action.payload;
    },
  },
});

export const { increment, decrement, incrementBy } = counterSlice.actions;

// Step 2: Create the store (DevTools + thunk middleware auto-configured!)
const store = configureStore({
  reducer: {
    counter: counterSlice.reducer,
  },
});
```

**That's 20 lines!** And it includes DevTools, middleware, and immutability — ALL automatically! 🎉

---

## 3. How

### How RTK Improves Every Part of Redux:

### 1. `configureStore` replaces `createStore`
```ts
// ❌ Legacy
import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import { composeWithDevTools } from "redux-devtools-extension";

const store = createStore(
  combineReducers({ counter: counterReducer }),
  composeWithDevTools(applyMiddleware(thunk))
);

// ✅ RTK — all of the above in one line!
import { configureStore } from "@reduxjs/toolkit";

const store = configureStore({
  reducer: { counter: counterReducer },
  // DevTools: ✅ auto-enabled
  // Thunk middleware: ✅ auto-included
  // Serialization checks: ✅ auto-enabled
});
```

### 2. `createSlice` replaces action types + creators + reducer
```ts
// ❌ Legacy: 3 separate files/concepts
// - actionTypes.ts (constants)
// - actions.ts (creator functions)
// - reducer.ts (switch statement)

// ✅ RTK: Everything in one place
const slice = createSlice({
  name: "feature",
  initialState: {},
  reducers: {
    // Each function here is BOTH a reducer case AND an action creator
    doSomething(state, action) { /* ... */ }
  }
});
```

### 3. Immer replaces manual spreading
```ts
// ❌ Legacy: Must spread manually for immutability
return {
  ...state,
  nested: {
    ...state.nested,
    deep: {
      ...state.nested.deep,
      value: action.payload, // 😩 This is painful!
    },
  },
};

// ✅ RTK: Just "mutate" directly (Immer handles immutability)
state.nested.deep.value = action.payload; // 🎉 So clean!
```

---

## 4. Implementation

### Complete RTK Setup:

```ts
// features/user/userSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user";
}

interface UserState {
  currentUser: User | null;
  isAuthenticated: boolean;
  preferences: {
    theme: "light" | "dark";
    language: string;
    notifications: boolean;
  };
}

const initialState: UserState = {
  currentUser: null,
  isAuthenticated: false,
  preferences: {
    theme: "dark",
    language: "en",
    notifications: true,
  },
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    // Simple action — no payload
    logout(state) {
      state.currentUser = null;
      state.isAuthenticated = false;
    },

    // Action with payload
    login(state, action: PayloadAction<User>) {
      state.currentUser = action.payload;
      state.isAuthenticated = true;
    },

    // Updating nested state — painless with Immer!
    setTheme(state, action: PayloadAction<"light" | "dark">) {
      state.preferences.theme = action.payload;
    },

    setLanguage(state, action: PayloadAction<string>) {
      state.preferences.language = action.payload;
    },

    toggleNotifications(state) {
      state.preferences.notifications = !state.preferences.notifications;
    },

    // Update multiple nested fields at once
    updatePreferences(
      state,
      action: PayloadAction<Partial<UserState["preferences"]>>
    ) {
      // Object.assign with Immer — works perfectly!
      Object.assign(state.preferences, action.payload);
    },
  },
});

export const {
  logout,
  login,
  setTheme,
  setLanguage,
  toggleNotifications,
  updatePreferences,
} = userSlice.actions;

export default userSlice.reducer;
```

```ts
// store.ts
import { configureStore } from "@reduxjs/toolkit";
import userReducer from "./features/user/userSlice";
import counterReducer from "./features/counter/counterSlice";

const store = configureStore({
  reducer: {
    user: userReducer,
    counter: counterReducer,
  },
  // Optional: customize middleware
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: true, // Warns if non-serializable data enters the store
    }),
  // DevTools are enabled automatically in development
  devTools: process.env.NODE_ENV !== "production",
});

// Infer types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
```

---

## 5. React Integration

```tsx
// App.tsx
import { useSelector, useDispatch } from "react-redux";
import { RootState, AppDispatch } from "./store";
import { login, logout, setTheme, toggleNotifications } from "./features/user/userSlice";

function UserDashboard() {
  const user = useSelector((state: RootState) => state.user.currentUser);
  const isAuth = useSelector((state: RootState) => state.user.isAuthenticated);
  const theme = useSelector((state: RootState) => state.user.preferences.theme);
  const dispatch = useDispatch<AppDispatch>();

  if (!isAuth) {
    return (
      <button
        onClick={() =>
          dispatch(
            login({
              id: "1",
              name: "Nishant",
              email: "nishant@example.com",
              role: "admin",
            })
          )
        }
      >
        Log In
      </button>
    );
  }

  return (
    <div>
      <h1>Welcome, {user?.name}!</h1>
      <p>Theme: {theme}</p>
      <button onClick={() => dispatch(setTheme(theme === "dark" ? "light" : "dark"))}>
        Toggle Theme
      </button>
      <button onClick={() => dispatch(toggleNotifications())}>
        Toggle Notifications
      </button>
      <button onClick={() => dispatch(logout())}>Log Out</button>
    </div>
  );
}
```

---

## 6. Next.js Integration

### App Router:

```tsx
// lib/store.ts — Same store setup as above

// app/StoreProvider.tsx
"use client";
import { Provider } from "react-redux";
import store from "@/lib/store";

export default function StoreProvider({ children }: { children: React.ReactNode }) {
  return <Provider store={store}>{children}</Provider>;
}

// app/layout.tsx
import StoreProvider from "./StoreProvider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
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

### Why RTK is the Standard:
- **Official recommendation** — the Redux team says "use RTK, always"
- **90% less boilerplate** compared to legacy Redux
- **Built-in best practices** — DevTools, middleware, serialization checks
- **Immer** — no more manual spreading for immutability
- **RTK Query** — built-in data fetching that rivals React Query
- **TypeScript support** — first-class type inference

### Migration Path:
- If you have a legacy Redux app, you can adopt RTK **incrementally**
- Replace `createStore` with `configureStore` first
- Then convert reducers to `createSlice` one at a time

---

## 8. Summary

- **Redux Toolkit (RTK)** is the official, recommended way to write Redux
- `configureStore` = creates store with DevTools + middleware automatically
- `createSlice` = creates reducer + actions in one step
- **Immer** = write "mutating" code that's actually immutable
- RTK reduces boilerplate by **~90%** compared to legacy Redux
- Always use RTK for new projects — there's no reason to use legacy Redux
- RTK includes `createAsyncThunk` for async logic and `createApi` for data fetching

---

**Prev:** [04_data_flow.md](./04_data_flow.md) | **Next:** [06_configure_store.md](./06_configure_store.md)
