# configureStore

---

## 1. What

`configureStore` is the **RTK function that creates your Redux store**. It's a wrapper around the legacy `createStore` that automatically sets up:

- ✅ **Redux DevTools** — for debugging
- ✅ **Thunk middleware** — for async operations
- ✅ **Serialization checks** — warns you about non-serializable data
- ✅ **Immutability checks** — catches accidental state mutations
- ✅ **Reducer combination** — automatically calls `combineReducers` for you

In simple terms: **one function call gives you a fully configured, production-ready store.**

---

## 2. Why

### Legacy Store Setup Was Painful:

```ts
// ❌ Legacy — so many packages and config!
import { createStore, combineReducers, applyMiddleware, compose } from "redux";
import thunk from "redux-thunk";                     // Extra package
import logger from "redux-logger";                    // Extra package
import { composeWithDevTools } from "redux-devtools-extension"; // Extra package

const rootReducer = combineReducers({
  auth: authReducer,
  cart: cartReducer,
  products: productsReducer,
});

const middleware = [thunk, logger];

const store = createStore(
  rootReducer,
  composeWithDevTools(applyMiddleware(...middleware))
);
```

### RTK Makes It Simple:

```ts
// ✅ RTK — one function, everything included!
import { configureStore } from "@reduxjs/toolkit";

const store = configureStore({
  reducer: {
    auth: authReducer,
    cart: cartReducer,
    products: productsReducer,
  },
});
// DevTools: ✅ auto-enabled
// Thunk: ✅ auto-included
// Type safety: ✅ auto-inferred
```

---

## 3. How

### How `configureStore` Works Internally:

```
configureStore({
  reducer: { ... },          ─→ Calls combineReducers automatically
  middleware: (default) => ..., ─→ Adds thunk + dev checks by default
  devTools: true,             ─→ Enables Redux DevTools
  preloadedState: { ... },    ─→ Sets initial state (for SSR hydration)
  enhancers: [],              ─→ Additional store enhancers (rarely needed)
})
```

### API Reference:

```ts
import { configureStore } from "@reduxjs/toolkit";

const store = configureStore({
  // REQUIRED: Your reducers
  reducer: {
    sliceName: sliceReducer,
    // ... more reducers
  },

  // OPTIONAL: Customize middleware
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(customMiddleware),

  // OPTIONAL: Enable/disable DevTools (default: true in dev)
  devTools: process.env.NODE_ENV !== "production",

  // OPTIONAL: Preloaded state (for SSR)
  preloadedState: {},

  // OPTIONAL: Store enhancers
  enhancers: (getDefaultEnhancers) =>
    getDefaultEnhancers().concat(customEnhancer),
});
```

---

## 4. Implementation

### Basic Store:

```ts
// store.ts
import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./features/counter/counterSlice";
import authReducer from "./features/auth/authSlice";

const store = configureStore({
  reducer: {
    counter: counterReducer,
    auth: authReducer,
  },
});

// These two type exports are CRITICAL for TypeScript
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;
```

### Store with Custom Middleware:

```ts
// store.ts
import { configureStore, Middleware } from "@reduxjs/toolkit";
import counterReducer from "./features/counter/counterSlice";

// Custom logging middleware
const loggerMiddleware: Middleware = (storeAPI) => (next) => (action) => {
  console.log("Dispatching:", action);
  const result = next(action);
  console.log("Next State:", storeAPI.getState());
  return result;
};

const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(loggerMiddleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
```

### Store with Preloaded State (for SSR):

```ts
// store.ts
import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./features/counter/counterSlice";

// Factory function — creates a new store each time (important for SSR!)
export function makeStore(preloadedState?: Partial<RootState>) {
  return configureStore({
    reducer: {
      counter: counterReducer,
    },
    preloadedState,
  });
}

// For client-side, create a single store
const store = makeStore();

export type RootState = ReturnType<ReturnType<typeof makeStore>["getState"]>;
export type AppDispatch = ReturnType<typeof makeStore>["dispatch"];
export default store;
```

### Store with Disabled Checks (for Performance):

```ts
// store.ts
const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      // These checks run in development only
      serializableCheck: false,   // Disable if storing non-serializable data
      immutableCheck: false,       // Disable if you have large state
    }),
});
```

### Store with Multiple Middleware:

```ts
import { configureStore } from "@reduxjs/toolkit";
import createSagaMiddleware from "redux-saga"; // If using sagas

const sagaMiddleware = createSagaMiddleware();

const store = configureStore({
  reducer: {
    // ... reducers
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      thunk: true, // Keep thunk (default)
    }).concat(sagaMiddleware),
});

// Run sagas after store creation
// sagaMiddleware.run(rootSaga);
```

---

## 5. React Integration

```tsx
// main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import store from "./store";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>
);
```

---

## 6. Next.js Integration

### App Router (Recommended for Next.js 13+):

```ts
// lib/store.ts
import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./features/counter/counterSlice";

// Use a makeStore function for SSR compatibility
export const makeStore = () => {
  return configureStore({
    reducer: {
      counter: counterReducer,
    },
  });
};

export type AppStore = ReturnType<typeof makeStore>;
export type RootState = ReturnType<AppStore["getState"]>;
export type AppDispatch = AppStore["dispatch"];
```

```tsx
// app/StoreProvider.tsx
"use client";

import { useRef } from "react";
import { Provider } from "react-redux";
import { makeStore, AppStore } from "@/lib/store";

export default function StoreProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  // Create the store ONCE per client-side lifecycle
  const storeRef = useRef<AppStore | null>(null);
  if (!storeRef.current) {
    storeRef.current = makeStore();
  }

  return <Provider store={storeRef.current}>{children}</Provider>;
}
```

```tsx
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
import { Provider } from "react-redux";
import store from "@/lib/store";
import type { AppProps } from "next/app";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Provider store={store}>
      <Component {...pageProps} />
    </Provider>
  );
}
```

---

## 7. Impact

### What `configureStore` Gives You for Free:
1. **DevTools** — inspect state, actions, and diffs in the browser
2. **Thunk middleware** — handle async logic out of the box
3. **Immutability detection** — caught accidental mutations during development
4. **Serialization checks** — warns if you store things like `Date` objects or class instances
5. **Type inference** — `RootState` and `AppDispatch` are auto-inferred

### Common Gotchas:
- **Don't create multiple stores** (except for SSR)
- **Don't disable DevTools in production** — `configureStore` automatically disables them
- **Export `RootState` and `AppDispatch` types** — you'll need them everywhere

---

## 8. Summary

- `configureStore` is the **only way** you should create a Redux store
- It auto-includes **DevTools**, **thunk middleware**, and **development checks**
- Pass an object of **slice reducers** — it auto-calls `combineReducers`
- Export `RootState` and `AppDispatch` types for TypeScript
- Use `makeStore` factory pattern for **SSR/Next.js** compatibility
- Customize middleware with `getDefaultMiddleware().concat()`
- Default middleware includes: thunk, serializable check, immutable check

---

**Prev:** [05_redux_toolkit_introduction.md](./05_redux_toolkit_introduction.md) | **Next:** [07_create_slice.md](./07_create_slice.md)
