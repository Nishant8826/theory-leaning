# Advanced Topics

---

## 1. What

This section covers Redux features that you won't use every day, but are crucial for building enterprise-grade applications.
Topics include **Custom Middleware**, **Code Splitting (Dynamic Reducers)**, and **Listener Middleware**.

---

## 2. Why

As your application grows to hundreds of endpoints or encounters specific edge cases (e.g. logging every action to an analytics tracker, intercepting actions based on authentication, loading specific slices only when a widget is mounted), basic standard setup limits your scaling capabilities.

---

## 3. How

### Custom Middleware
Middleware forms a pipeline between dispatching an action, and the action reaching the reducer.
```
Action Dispatched -> Middleware 1 -> Middleware 2 -> Reducer -> State Updated
```

### Code Splitting (Dynamic Reducers)
Instead of importing all reducers into `store.ts` upfront (creating a massive JS bundle), we inject them asynchronously only when a specific component mounts.

### Listener Middleware 
RTK's modern alternative to Redux Saga or Redux Observable. It lets you "listen" to specific actions and trigger side effects without writing giant Thunks.

---

## 4. Implementation

### 1. Custom Middleware (e.g., Error Logger)

```ts
import { Middleware, isRejectedWithValue } from '@reduxjs/toolkit';

// Middleware Signature: (store) => (next) => (action)
export const rtkQueryErrorLogger: Middleware = (api) => (next) => (action) => {
  // If this action represents a rejected promise/thunk/rtk query
  if (isRejectedWithValue(action)) {
    console.warn('An API request failed!', action.payload);
    // You could trigger a Toast notification right here
    // alert(action.payload.data.message);
  }

  return next(action);
};

// store.ts implementation:
// middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(rtkQueryErrorLogger)
```

### 2. Code Splitting (Redux Toolkit specific method)

RTK provides `injectEndpoints` for code splitting API slices.

```ts
// 1. emptyApiSlice.ts
// Define this at the root of the app
export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/' }),
  endpoints: () => ({}),
});

// 2. features/posts/postsApi.ts
// This file is lazy loaded. When executed, it attaches to the main api instance.
const extendedApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getPosts: builder.query<Post[], void>({ query: () => '/posts' }),
  }),
  overrideExisting: false, 
});

export const { useGetPostsQuery } = extendedApi;
```

### 3. RTK Listener Middleware (Replacing Redux-Saga)

If you need a side effect: "When the user clears their cart, show a specialized modal and ping an analytics server."

```ts
import { createListenerMiddleware } from '@reduxjs/toolkit';
import { clearCart } from '../features/cart/cartSlice';

const listenerMiddleware = createListenerMiddleware();

listenerMiddleware.startListening({
  actionCreator: clearCart,
  effect: async (action, listenerApi) => {
    // This runs AFTER the reducer processes 'clearCart'
    console.log('Cart was cleared. Current State:', listenerApi.getState());
    
    // Ping analytics
    await fetch('/analytics/track', { method: 'POST', body: 'CART_CLEARED' });
  },
});

// store.ts
// middleware: (gDM) => gDM().prepend(listenerMiddleware.middleware)
```

---

## 5. React Integration

Advanced configurations sit almost entirely inside the store layer. Your React components remain clean and do not know or care that an analytics middleware just intercepted their dispatch.

---

## 6. Next.js Integration

Be cautious. `injectEndpoints` and runtime dynamic reducer injections must be configured correctly in Next.js Server environments so they don't leak across requests. Middleware will execute on both the Server (during SSR dispatches) and Client.

---

## 7. Impact

Advanced architecture:
- Lowers main bundle sizes (`injectEndpoints`).
- Decouples side-effects from UI logic (`ListenerMiddleware`).
- Centralizes error handling and logging (`Custom Middleware`).

---

## 8. Summary

- **Custom Middleware**: Intercepts actions before they hit reducers. Perfect for logging and global error handling.
- **Code Splitting (`injectEndpoints`)**: Attaches queries and mutations dynamically to reduce initial JS payload sizes.
- **Listener Middleware**: The modern, built-in RTK replacement for complex side-effects (saga/observable), acting as an event-listener for specific Redux Actions.

---

**Prev:** [29_nextjs_integration.md](./29_nextjs_integration.md) | **Next:** [31_common_mistakes_and_debugging.md](./31_common_mistakes_and_debugging.md)
