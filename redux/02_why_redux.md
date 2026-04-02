# Why Redux?

---

## 1. What

"Why Redux?" is the question every beginner asks — and it's a great one. Redux is a **state management tool** that solves specific problems that arise when your application grows in size and complexity.

Before understanding Redux, you need to understand the **problems** it was designed to fix.

---

## 2. Why

### The Problems That Led to Redux:

### Problem 1: Prop Drilling

When components are deeply nested and a child component needs data from a distant ancestor, you must pass props through every intermediate component.

```tsx
// ❌ Without Redux — Prop Drilling
function App() {
  const [user, setUser] = useState({ name: "Nishant" });
  return <Dashboard user={user} />;
}

function Dashboard({ user }: { user: User }) {
  // Dashboard doesn't even USE user, just passes it down
  return <Sidebar user={user} />;
}

function Sidebar({ user }: { user: User }) {
  // Sidebar doesn't USE user either
  return <UserProfile user={user} />;
}

function UserProfile({ user }: { user: User }) {
  // Finally! This component actually uses the data
  return <h1>{user.name}</h1>;
}
```

```tsx
// ✅ With Redux — Direct Access
function UserProfile() {
  // Read directly from the store — no prop drilling!
  const user = useSelector((state: RootState) => state.auth.user);
  return <h1>{user.name}</h1>;
}
```

### Problem 2: Shared State Between Unrelated Components

```
Header (shows cart count)         ←→         CartPage (shows cart items)
    ↑                                              ↑
    └── Both need the SAME "cart" state ───────────┘
```

Without Redux, you'd have to **lift state up** to a common ancestor and pass it down — which creates more prop drilling.

With Redux, both components simply **read from the same store**.

### Problem 3: Complex State Logic

When state updates depend on multiple conditions, multiple sources, or involve async operations, managing it with `useState` alone becomes chaotic.

```tsx
// ❌ Messy state management without Redux
const [user, setUser] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
const [isAuthenticated, setIsAuthenticated] = useState(false);
const [notifications, setNotifications] = useState([]);
const [theme, setTheme] = useState("dark");
// ... it keeps growing and growing
```

```ts
// ✅ With Redux — organized in slices
// authSlice handles: user, loading, error, isAuthenticated
// notificationSlice handles: notifications
// themeSlice handles: theme
```

### Problem 4: Unpredictable State Changes

Without Redux, any component can change state in any way. This makes it nearly impossible to debug:
- **What** changed the state?
- **When** did it change?
- **Why** did it change?

Redux enforces that **every change goes through an action + reducer**, making the entire state history traceable.

### Problem 5: No Time-Travel Debugging

With React's built-in state, once state changes, the old state is gone. Redux DevTools lets you:
- See **every action** that was dispatched
- **Jump back** to any previous state
- **Replay** actions step by step
- **Export/import** state for bug reports

---

## 3. How

### How Redux Solves These Problems:

| Problem | Redux Solution |
|---------|---------------|
| Prop Drilling | Components read directly from the store using `useSelector` |
| Shared State | Single store — any component can access any state |
| Complex Logic | Organized into slices with clear reducers |
| Unpredictable Changes | Actions describe what happened; reducers are pure functions |
| Debugging | Redux DevTools with time-travel debugging |

### The Redux Mental Model:

```
Think of Redux like a bank:
- The VAULT (Store) = holds all the money (state)
- A DEPOSIT SLIP (Action) = describes what you want to do
- The BANK TELLER (Reducer) = processes the slip and updates the vault
- Your BANK APP (UI) = shows you the updated balance

You can't just walk into the vault and grab money.
You MUST fill out a slip, give it to the teller, and they handle it.
```

---

## 4. Implementation

### Before Redux (React Only):

```tsx
// App.tsx — Managing state with just React
import { useState, createContext, useContext } from "react";

// Step 1: Create context
interface AppState {
  user: { name: string; email: string } | null;
  theme: "light" | "dark";
  cartItems: string[];
}

const AppContext = createContext<{
  state: AppState;
  setState: React.Dispatch<React.SetStateAction<AppState>>;
} | null>(null);

// Step 2: Provider component
function AppProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AppState>({
    user: null,
    theme: "dark",
    cartItems: [],
  });

  return (
    <AppContext.Provider value={{ state, setState }}>
      {children}
    </AppContext.Provider>
  );
}

// Step 3: Custom hook
function useAppState() {
  const context = useContext(AppContext);
  if (!context) throw new Error("Must be inside AppProvider");
  return context;
}

// Problem: This re-renders EVERY consumer when ANY state changes!
// If theme changes, cart-related components ALSO re-render unnecessarily.
```

### After Redux:

```ts
// store.ts
import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./features/auth/authSlice";
import themeReducer from "./features/theme/themeSlice";
import cartReducer from "./features/cart/cartSlice";

const store = configureStore({
  reducer: {
    auth: authReducer,    // Only auth-related components re-render on auth changes
    theme: themeReducer,  // Only theme-related components re-render on theme changes
    cart: cartReducer,    // Only cart-related components re-render on cart changes
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
```

```ts
// features/auth/authSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface User {
  name: string;
  email: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    login(state, action: PayloadAction<User>) {
      state.user = action.payload;
      state.isAuthenticated = true;
    },
    logout(state) {
      state.user = null;
      state.isAuthenticated = false;
    },
  },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;
```

```tsx
// components/Header.tsx — Only re-renders when auth state changes
import { useSelector } from "react-redux";
import { RootState } from "../store";

function Header() {
  const user = useSelector((state: RootState) => state.auth.user);

  return (
    <header>
      {user ? <span>Welcome, {user.name}</span> : <span>Please log in</span>}
    </header>
  );
}
```

---

## 5. React Integration

Redux seamlessly integrates with React using the `react-redux` library:

```tsx
// main.tsx
import { Provider } from "react-redux";
import store from "./store";

// Wrap your entire app with Provider
// This makes the store available to ALL components
<Provider store={store}>
  <App />
</Provider>

// Then in ANY component, no matter how deep:
import { useSelector, useDispatch } from "react-redux";

function AnyComponent() {
  const data = useSelector((state: RootState) => state.someSlice.data);
  const dispatch = useDispatch();

  // Read state ↑ and dispatch actions ↓
  dispatch(someAction());
}
```

---

## 6. Next.js Integration

### App Router:

```tsx
// app/providers.tsx
"use client";

import { Provider } from "react-redux";
import store from "@/lib/store";

export function Providers({ children }: { children: React.ReactNode }) {
  return <Provider store={store}>{children}</Provider>;
}
```

### Pages Router:

```tsx
// pages/_app.tsx
import { Provider } from "react-redux";
import store from "@/lib/store";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Provider store={store}>
      <Component {...pageProps} />
    </Provider>
  );
}
```

---

## 7. Redux vs Alternatives

| Feature | Redux | Context API | Zustand | Jotai |
|---------|-------|------------|---------|-------|
| Learning Curve | Medium | Easy | Easy | Easy |
| Boilerplate | Low (with RTK) | Very Low | Very Low | Very Low |
| DevTools | Excellent | None | Good | Good |
| Performance | Great (selective re-renders) | Poor (all consumers re-render) | Great | Great |
| Middleware | Yes | No | Yes | Limited |
| Time Travel | Yes | No | No | No |
| Community | Huge | Built-in | Growing | Growing |
| Best For | Large apps | Small apps | Medium apps | Atomic state |

---

## 8. Impact

### When to Choose Redux:
- ✅ **Large teams** — standardized patterns help everyone follow the same approach
- ✅ **Complex state logic** — when state depends on multiple factors
- ✅ **Need for debugging tools** — Redux DevTools are unmatched
- ✅ **Server state + client state** — RTK Query handles server state beautifully
- ✅ **Enterprise applications** — battle-tested at scale

### When NOT to Choose Redux:
- ❌ **Simple apps** — a todo app doesn't need Redux
- ❌ **Only server state** — React Query / TanStack Query might be simpler
- ❌ **Small amount of shared state** — Context API or Zustand might suffice

---

## 9. Summary

- Redux solves **prop drilling**, **shared state**, **complex logic**, and **debugging** problems
- It provides a **single source of truth** with a predictable update pattern
- **Redux Toolkit** dramatically reduces boilerplate compared to legacy Redux
- Redux shines in **large, complex applications** with many developers
- For simple apps, consider lighter alternatives like Context API or Zustand
- Redux DevTools provide **unmatched debugging capabilities** including time-travel
- `useSelector` enables **selective re-renders** — only components that use changed state re-render

---

**Prev:** [01_what_is_redux.md](./01_what_is_redux.md) | **Next:** [03_core_concepts.md](./03_core_concepts.md)
