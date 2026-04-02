# Provider — Connecting Redux to React

---

## 1. What

The **`Provider`** component from `react-redux` is the **bridge between Redux and React**. It makes the Redux store available to every component in your application.

Think of it as a **power outlet** — it supplies the "electricity" (store) to every "device" (component) in your "house" (app).

```tsx
<Provider store={store}>
  {/* Every component inside here can access the Redux store */}
  <App />
</Provider>
```

Without `Provider`, your components **cannot** use `useSelector` or `useDispatch` — they simply won't have access to the store.

---

## 2. Why

### The Problem:
Redux's store is a plain JavaScript object. React components don't know about it unless you explicitly connect them.

```ts
// store.ts
const store = configureStore({ reducer: { ... } });

// Without Provider:
// ❌ useSelector → Error: "Could not find the store..."
// ❌ useDispatch → Error: "Could not find the store..."
```

### The Solution:
`Provider` uses **React Context** internally to pass the store down through the component tree.

```tsx
// With Provider:
<Provider store={store}>
  <App /> {/* ✅ useSelector works! ✅ useDispatch works! */}
</Provider>
```

---

## 3. How

### How Provider Works Internally:

```
1. Provider creates a React Context
2. It puts the Redux store in that context
3. Any child component can access the context
4. useSelector reads from the context's store
5. useDispatch gets dispatch from the context's store

Provider
  └── Context (holds the store)
       ├── ComponentA → useSelector reads from store
       ├── ComponentB → useDispatch sends to store
       └── ComponentC → useSelector reads from store
```

### Key Point:
Provider should **wrap your entire app** — typically at the very top level.

---

## 4. Implementation

### Basic Setup (React / Vite):

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

### With Multiple Providers (if needed):

```tsx
// Sometimes you might have other providers too
import { Provider } from "react-redux";
import { ThemeProvider } from "./ThemeContext";
import { BrowserRouter } from "react-router-dom";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <ThemeProvider>
          <App />
        </ThemeProvider>
      </BrowserRouter>
    </Provider>
  </React.StrictMode>
);
```

---

## 5. React Integration

Once `Provider` wraps your app, every component can use Redux hooks:

```tsx
// components/Header.tsx — works because it's inside Provider!
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "../store";

function Header() {
  const userName = useSelector((state: RootState) => state.auth.user?.name);
  const dispatch = useDispatch();

  return <header>Welcome, {userName ?? "Guest"}</header>;
}
```

```tsx
// components/deeply/nested/Footer.tsx — ALSO works! No prop drilling!
function Footer() {
  const theme = useSelector((state: RootState) => state.theme.mode);
  return <footer className={theme}>© 2026</footer>;
}
```

---

## 6. Next.js Integration

### App Router (Next.js 13+):

In Next.js App Router, you need a **client component** for Provider because hooks don't work in Server Components.

```tsx
// app/StoreProvider.tsx
"use client"; // ← MUST be a client component!

import { useRef } from "react";
import { Provider } from "react-redux";
import { makeStore, AppStore } from "@/lib/store";

export default function StoreProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const storeRef = useRef<AppStore | null>(null);
  if (!storeRef.current) {
    storeRef.current = makeStore();
  }

  return <Provider store={storeRef.current}>{children}</Provider>;
}
```

```tsx
// app/layout.tsx — Server Component (default)
import StoreProvider from "./StoreProvider";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {/* StoreProvider is a client component boundary */}
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

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Provider store={store}>
      <Component {...pageProps} />
    </Provider>
  );
}
```

### Important Next.js Considerations:
1. **Server Components CANNOT use Redux hooks** — only Client Components can
2. **Create store per request** in SSR to avoid sharing state between users
3. Use `useRef` to ensure the store is created only once on the client

---

## 7. Impact

### Provider is Simple but Critical:
- Without it, **nothing works** — no hooks, no state, no dispatch
- It should be placed at the **highest level** of your app
- It's a **one-time setup** — you set it and forget it

### Common Mistakes:
```tsx
// ❌ Mistake: Using hooks OUTSIDE Provider
function App() {
  const count = useSelector((state) => state.counter.count); // ❌ Error!
  return (
    <Provider store={store}>
      <div>{count}</div>
    </Provider>
  );
}

// ✅ Correct: Using hooks INSIDE Provider
function Counter() {
  const count = useSelector((state: RootState) => state.counter.count); // ✅
  return <div>{count}</div>;
}

function App() {
  return (
    <Provider store={store}>
      <Counter />
    </Provider>
  );
}
```

---

## 8. Summary

- `Provider` is the **bridge** between Redux store and React components
- It uses **React Context** internally to share the store
- Wrap your **entire app** with `<Provider store={store}>`
- In Next.js App Router, Provider must be in a **client component** (`"use client"`)
- In Next.js Pages Router, place it in `_app.tsx`
- All `useSelector` and `useDispatch` calls must be **inside** the Provider tree
- It's a **one-time setup** that enables all Redux functionality in React

---

**Prev:** [12_async_state_handling.md](./12_async_state_handling.md) | **Next:** [14_use_selector.md](./14_use_selector.md)
