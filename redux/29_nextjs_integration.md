# Next.js Integration (SSR & Hydration)

---

## 1. What

Integrating Redux with Next.js involves ensuring that Redux works smoothly within a Server-Side Rendering (SSR) environment. This requires configuring a separate Redux store for the server and client, and synchronizing (hydrating) the server's initial state onto the client.

Next.js has two routing paradigms: **Pages Router** and **App Router**.

---

## 2. Why

If you instantiate a global `export const store = configureStore(...)` in a standard Next.js application, that single store instance will be shared across **every user hitting the server**. 
User A logs in, and User B (hitting the same Node.js server instance) suddenly sees User A's data!

In Next.js, **you must create a fresh store per request on the server**.

---

## 3. How

### In the Pages Router:
You use a library called `next-redux-wrapper`. It handles creating store instances per request and dispatches a special `HYDRATE` action to sync server state to the client.

### In the App Router (Next 13+):
`next-redux-wrapper` is no longer recommended. Because the App Router fundamentally separates Server Components and Client Components, Server Components cannot interact with Redux Context. You instead fetch data natively in server components, pass it via props to Client Components, and let the Client components hydrate the Redux store on initialization using a `useRef` based Provider.

---

## 4. Implementation

### The App Router Setup (Modern Recommended Approach)

**1. Create a `makeStore` Factory**
```ts
// lib/store.ts
import { configureStore } from '@reduxjs/toolkit';
import rootReducer from './rootReducer';

// Creates a brand new store
export const makeStore = () => {
  return configureStore({
    reducer: rootReducer,
  });
};

// Types
export type AppStore = ReturnType<typeof makeStore>;
export type RootState = ReturnType<AppStore['getState']>;
export type AppDispatch = AppStore['dispatch'];
```

**2. Create a Client Provider**
```tsx
// app/StoreProvider.tsx
'use client';
import { useRef } from 'react';
import { Provider } from 'react-redux';
import { makeStore, AppStore } from '../lib/store';

export default function StoreProvider({ count, children }: { count: number, children: React.ReactNode }) {
  // Ensure the store is only created ONCE per client session
  const storeRef = useRef<AppStore | null>(null);
  if (!storeRef.current) {
    storeRef.current = makeStore();
    
    // OPTIONAL: Hydrate initial state directly on creation
    // storeRef.current.dispatch(initializeCount(count));
  }

  return <Provider store={storeRef.current}>{children}</Provider>;
}
```

**3. Wrap the Layout**
```tsx
// app/layout.tsx
import StoreProvider from './StoreProvider';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <StoreProvider count={0}>{children}</StoreProvider>
      </body>
    </html>
  );
}
```

### RTK Query Hydration in App Router:
If you want to fetch data in a React Server Component (RSC), and hydrate RTK Query so client hooks don't refetch:

```tsx
// ServerComponent.tsx
import { makeStore } from '@/lib/store';
import { apiSlice } from '@/lib/apiSlice';
import ClientComponent from './ClientComponent';

export default async function Page() {
  const store = makeStore();
  
  // Initiate the query on the SERVER
  await store.dispatch(apiSlice.endpoints.getPosts.initiate());

  // Extract the raw cached state
  const initialData = store.getState().api;

  // Pass it to the client
  return <ClientComponent initialData={initialData} />;
}
```

---

## 5. React Integration

Because standard React (Vite/CRA) runs purely in the client browser, you don't face these SSR leak issues. You just `export const store = ...` universally. Next.js enforces stricter rules.

---

## 6. Impact

### Why this structure?
- Eliminates "Cross-Request State Leaking" (a severe security flaw where server memory is shared between users).
- Improves SEO: Search engines see the fully populated HTML generated from the server store.
- Reduces Cumulative Layout Shift (CLS): Users do not see flickering loading spinners, as the data is already pre-loaded into the store during hydration.

---

## 7. Summary

- **Never** export a singleton `store` object in an SSR environment.
- Create a `makeStore()` factory that returns a fresh instance.
- In App Router, utilize `useRef` in a `'use client'` Provider to persist the store between client renders but avoid cross-server bounds.
- If pre-fetching RTK Query on the server, `store.dispatch(endpoint.initiate())` kicks off the request, which can then be passed to the client.

---

**Prev:** [28_typescript_with_redux.md](./28_typescript_with_redux.md) | **Next:** [30_advanced_topics.md](./30_advanced_topics.md)
