# createAction & createReducer

---

## 1. What

`createAction` and `createReducer` are **lower-level RTK utilities** that `createSlice` is built on top of. Think of them as the building blocks:

- **`createAction`** — creates an action creator function with a specific type
- **`createReducer`** — creates a reducer using a builder pattern (with Immer support)

### The Hierarchy:
```
createSlice (recommended — uses both under the hood)
   ├── createAction (creates individual action creators)
   └── createReducer (creates individual reducers with builder pattern)
```

> **Note:** In most cases, you should use `createSlice` instead. These are useful when you need more control or need to share actions between slices.

---

## 2. Why

### When to Use createAction:
- When you need an action that **multiple slices** respond to
- When you need to define actions **separately** from reducers
- When building a **shared action** (like `logout` that resets multiple slices)

### When to Use createReducer:
- When you need a reducer **without** a slice
- When migrating legacy code **incrementally**
- For **edge cases** where `createSlice` doesn't fit

### 99% of the time → Use `createSlice`
### The 1% edge case → Use `createAction` + `createReducer`

---

## 3. How

### createAction:

```ts
import { createAction } from "@reduxjs/toolkit";

// Create an action with no payload
const increment = createAction("counter/increment");
increment(); // { type: "counter/increment" }

// Create an action with a typed payload
const incrementBy = createAction<number>("counter/incrementBy");
incrementBy(5); // { type: "counter/incrementBy", payload: 5 }

// Create an action with a prepare callback
const addTodo = createAction("todos/add", (text: string) => ({
  payload: {
    id: crypto.randomUUID(),
    text,
    completed: false,
  },
}));
addTodo("Learn Redux");
// { type: "todos/add", payload: { id: "abc-123", text: "Learn Redux", completed: false } }
```

### createReducer:

```ts
import { createReducer } from "@reduxjs/toolkit";

const initialState = { count: 0 };

const counterReducer = createReducer(initialState, (builder) => {
  builder
    .addCase(increment, (state) => {
      state.count += 1; // Immer enabled!
    })
    .addCase(incrementBy, (state, action) => {
      state.count += action.payload;
    })
    .addDefaultCase((state) => {
      // Handle unknown actions (optional)
      return state;
    });
});
```

---

## 4. Implementation

### Shared Actions Between Slices:

```ts
// actions/sharedActions.ts
import { createAction } from "@reduxjs/toolkit";

// This action will be handled by MULTIPLE slices
export const logout = createAction("auth/logout");
export const resetApp = createAction("app/reset");
```

```ts
// features/auth/authSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { logout } from "../../actions/sharedActions";

interface AuthState {
  user: { name: string; email: string } | null;
  token: string | null;
  isAuthenticated: boolean;
}

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    login(
      state,
      action: PayloadAction<{ user: AuthState["user"]; token: string }>
    ) {
      state.user = action.payload.user;
      state.token = action.payload.token;
      state.isAuthenticated = true;
    },
  },
  // Handle the shared logout action
  extraReducers: (builder) => {
    builder.addCase(logout, (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
    });
  },
});

export const { login } = authSlice.actions;
export default authSlice.reducer;
```

```ts
// features/cart/cartSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { logout } from "../../actions/sharedActions";

interface CartState {
  items: Array<{ id: string; name: string; quantity: number }>;
}

const initialState: CartState = {
  items: [],
};

const cartSlice = createSlice({
  name: "cart",
  initialState,
  reducers: {
    addItem(
      state,
      action: PayloadAction<{ id: string; name: string }>
    ) {
      const existing = state.items.find((i) => i.id === action.payload.id);
      if (existing) {
        existing.quantity += 1;
      } else {
        state.items.push({ ...action.payload, quantity: 1 });
      }
    },
  },
  // Also handle logout — clear the cart!
  extraReducers: (builder) => {
    builder.addCase(logout, (state) => {
      state.items = []; // Clear cart on logout
    });
  },
});

export const { addItem } = cartSlice.actions;
export default cartSlice.reducer;
```

```tsx
// Usage: One dispatch clears BOTH auth AND cart
import { useDispatch } from "react-redux";
import { logout } from "./actions/sharedActions";

function LogoutButton() {
  const dispatch = useDispatch();

  return (
    <button onClick={() => dispatch(logout())}>
      {/* This single dispatch triggers BOTH authSlice and cartSlice reducers! */}
      Logout
    </button>
  );
}
```

### Standalone createReducer Example:

```ts
// Sometimes useful for legacy migration
import { createAction, createReducer } from "@reduxjs/toolkit";

// Define actions separately
const setTheme = createAction<"light" | "dark">("theme/set");
const toggleTheme = createAction("theme/toggle");
const setFontSize = createAction<number>("theme/setFontSize");

interface ThemeState {
  mode: "light" | "dark";
  fontSize: number;
}

const initialState: ThemeState = {
  mode: "dark",
  fontSize: 16,
};

// Create a reducer that handles these actions
const themeReducer = createReducer(initialState, (builder) => {
  builder
    .addCase(setTheme, (state, action) => {
      state.mode = action.payload;
    })
    .addCase(toggleTheme, (state) => {
      state.mode = state.mode === "dark" ? "light" : "dark";
    })
    .addCase(setFontSize, (state, action) => {
      state.fontSize = action.payload;
    })
    // addMatcher: handle actions that match a condition
    .addMatcher(
      (action) => action.type.startsWith("theme/"),
      (state) => {
        // Log or handle ALL theme actions
        console.log("Theme action fired");
      }
    );
});
```

---

## 5. React Integration

Works the same as any other Redux code:

```tsx
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "./store";
import { logout } from "./actions/sharedActions";

function Header() {
  const isAuth = useSelector((state: RootState) => state.auth.isAuthenticated);
  const cartCount = useSelector((state: RootState) => state.cart.items.length);
  const dispatch = useDispatch();

  return (
    <header>
      <span>Cart: {cartCount}</span>
      {isAuth && (
        <button onClick={() => dispatch(logout())}>Logout</button>
      )}
    </header>
  );
}
```

---

## 6. Next.js Integration

No special Next.js handling needed. `createAction` and `createReducer` are store-level logic — they work the same regardless of the framew framework.

---

## 7. Impact

### When createAction Shines:
- **Shared actions** — one action triggers multiple slice reducers
- **Action matching** — `addMatcher` in `extraReducers` can match patterns
- **TypeScript** — creates strongly typed action creators

### Key Insight:
`createSlice` uses `createAction` internally. When you write:
```ts
const slice = createSlice({
  name: "counter",
  initialState: { count: 0 },
  reducers: {
    increment(state) { state.count += 1; }
  }
});
```
RTK internally calls `createAction("counter/increment")` to create the action creator.

---

## 8. Summary

- **`createAction`** creates typed action creators with a specific type string
- **`createReducer`** creates a reducer using the builder pattern with Immer support
- **`createSlice`** uses BOTH internally — prefer `createSlice` for most cases
- Use `createAction` for **shared actions** that multiple slices handle
- Use `extraReducers` with `builder.addCase()` to handle external actions
- `addMatcher` lets you handle actions based on **conditions** (not exact types)
- The `prepare` callback in `createAction` customizes how the payload is created

---

**Prev:** [07_create_slice.md](./07_create_slice.md) | **Next:** [09_immer_and_immutability.md](./09_immer_and_immutability.md)
