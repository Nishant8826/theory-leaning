# RTK Query — Introduction

---

## 1. What

**RTK Query** is a **powerful data fetching and caching tool** built into Redux Toolkit. It eliminates the need to write thunks, loading states, and caching logic by hand. Think of it as Redux's answer to React Query / TanStack Query.

### What RTK Query Does:
- **Fetches data** from APIs automatically
- **Caches results** — no duplicate requests
- **Tracks loading/error/success** states automatically
- **Generates React hooks** for each endpoint
- **Manages cache invalidation** — knows when to refetch
- **Supports mutations** (POST, PUT, DELETE) with cache updates
- **Supports polling**, lazy queries, and optimistic updates

### The Analogy:
```
Without RTK Query:
You = Chef who buys ingredients, cooks, serves, washes dishes, stores leftovers

With RTK Query:
You = Customer at a restaurant — just ORDER, the kitchen handles everything
```

---

## 2. Why

### The Problem (Without RTK Query):

For EVERY API call, you had to write:

```ts
// 1. Define the types ......... (5 lines)
// 2. Create async thunk ........ (10 lines)
// 3. Add loading/error state ... (5 lines)
// 4. Handle pending ............. (3 lines)
// 5. Handle fulfilled ........... (3 lines)
// 6. Handle rejected ............ (3 lines)
// 7. Write useEffect in component (5 lines)
// 8. Handle cache manually ....... (10 lines)
// 9. Handle stale data ........... (5 lines)
// 10. Handle refetching .......... (5 lines)
// ────────────────────────────────────
// Total: ~55 lines per API endpoint! 😩
```

### The Solution (With RTK Query):

```ts
// Define your API with endpoints — EVERYTHING is handled
const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  endpoints: (builder) => ({
    getUsers: builder.query<User[], void>({
      query: () => "/users",
    }),
  }),
});

// Auto-generated hook — loading, error, caching, ALL included!
const { data, isLoading, error } = useGetUsersQuery();
// That's it. ~10 lines total. 🎉
```

### RTK Query vs Manual Approach:

| Feature | createAsyncThunk | RTK Query |
|---------|------------------|-----------|
| Boilerplate | ~55 lines/endpoint | ~5 lines/endpoint |
| Loading states | Manual | Automatic |
| Error handling | Manual | Automatic |
| Caching | Manual | Automatic |
| Deduplication | Manual | Automatic |
| Refetching | Manual | Automatic |
| Polling | Manual | Built-in |
| Optimistic updates | Manual | Built-in |
| Cache invalidation | Manual | Tag-based |
| Generated hooks | No | Yes |

---

## 3. How

### How RTK Query Works:

```
1. You define an API slice with endpoints (queries & mutations)
2. RTK Query auto-generates React hooks for each endpoint
3. When a component uses a hook, RTK Query:
   a. Checks if data is already cached
   b. If cached & fresh → returns cached data (no API call!)
   c. If not cached → makes the API call
   d. Stores the response in the Redux store
   e. Provides { data, isLoading, error } to the component
4. When the component unmounts, a countdown starts
5. If no other component uses this data within 60 seconds,
   the cache entry is removed (garbage collected)
```

### Architecture:

```
┌──────────────────────────────────────────────┐
│                 RTK Query                     │
├──────────────────────────────────────────────┤
│  createApi({                                  │
│    baseQuery: fetchBaseQuery(...)              │
│    endpoints: {                               │
│      getUsers: query<User[], void>            │
│      createUser: mutation<User, NewUser>      │
│    }                                          │
│  })                                           │
├──────────────────────────────────────────────┤
│  Auto-generated:                              │
│  ├── useGetUsersQuery()     ← React Hook     │
│  ├── useCreateUserMutation() ← React Hook    │
│  ├── Reducer                 ← For the store │
│  └── Middleware              ← For caching   │
└──────────────────────────────────────────────┘
```

---

## 4. Implementation

### Step 1: Create the API Slice

```ts
// features/api/apiSlice.ts
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

// Define your data types
interface User {
  id: number;
  name: string;
  email: string;
}

interface CreateUserPayload {
  name: string;
  email: string;
}

// Create the API slice
export const apiSlice = createApi({
  // Unique key for this API in the Redux store
  reducerPath: "api",

  // Base URL for all requests
  baseQuery: fetchBaseQuery({
    baseUrl: "https://jsonplaceholder.typicode.com",
  }),

  // Tag types for cache invalidation (we'll cover this in detail later)
  tagTypes: ["User", "Post"],

  // Define your endpoints
  endpoints: (builder) => ({
    // ── QUERY: GET request ──
    getUsers: builder.query<User[], void>({
      query: () => "/users",
      providesTags: ["User"],
    }),

    // ── QUERY with parameter ──
    getUserById: builder.query<User, number>({
      query: (id) => `/users/${id}`,
      providesTags: (result, error, id) => [{ type: "User", id }],
    }),

    // ── MUTATION: POST request ──
    createUser: builder.mutation<User, CreateUserPayload>({
      query: (newUser) => ({
        url: "/users",
        method: "POST",
        body: newUser,
      }),
      invalidatesTags: ["User"], // Refetch all users after creating one
    }),

    // ── MUTATION: PUT request ──
    updateUser: builder.mutation<User, { id: number } & Partial<User>>({
      query: ({ id, ...patch }) => ({
        url: `/users/${id}`,
        method: "PUT",
        body: patch,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: "User", id }],
    }),

    // ── MUTATION: DELETE request ──
    deleteUser: builder.mutation<void, number>({
      query: (id) => ({
        url: `/users/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: ["User"],
    }),
  }),
});

// Auto-generated hooks! ✨
export const {
  useGetUsersQuery,
  useGetUserByIdQuery,
  useCreateUserMutation,
  useUpdateUserMutation,
  useDeleteUserMutation,
} = apiSlice;
```

### Step 2: Add to Store

```ts
// store.ts
import { configureStore } from "@reduxjs/toolkit";
import { apiSlice } from "./features/api/apiSlice";

const store = configureStore({
  reducer: {
    // Add the API slice reducer
    [apiSlice.reducerPath]: apiSlice.reducer,
  },
  // Add the API middleware (handles caching, invalidation, polling)
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(apiSlice.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
```

---

## 5. React Integration

```tsx
// components/UserList.tsx
import {
  useGetUsersQuery,
  useCreateUserMutation,
  useDeleteUserMutation,
} from "../features/api/apiSlice";

function UserList() {
  // ── Query: Fetch users ──
  const {
    data: users,       // The fetched data
    isLoading,         // First load
    isFetching,        // Any fetch (including refetch)
    isError,           // Did it fail?
    error,             // Error details
    refetch,           // Manual refetch function
  } = useGetUsersQuery();

  // ── Mutation: Create user ──
  const [createUser, { isLoading: isCreating }] = useCreateUserMutation();

  // ── Mutation: Delete user ──
  const [deleteUser, { isLoading: isDeleting }] = useDeleteUserMutation();

  // ── Loading state ──
  if (isLoading) return <div>Loading users...</div>;

  // ── Error state ──
  if (isError) {
    return (
      <div>
        <p>Error loading users</p>
        <button onClick={refetch}>Retry</button>
      </div>
    );
  }

  return (
    <div>
      <h1>Users ({users?.length})</h1>

      <button
        onClick={() => createUser({ name: "New User", email: "new@test.com" })}
        disabled={isCreating}
      >
        {isCreating ? "Creating..." : "Add User"}
      </button>

      <ul>
        {users?.map((user) => (
          <li key={user.id}>
            {user.name} — {user.email}
            <button
              onClick={() => deleteUser(user.id)}
              disabled={isDeleting}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>

      {isFetching && <p>Refreshing...</p>}
    </div>
  );
}

export default UserList;
```

---

## 6. Next.js Integration

### App Router:

```tsx
// app/users/page.tsx
"use client";

import { useGetUsersQuery } from "@/lib/features/api/apiSlice";

export default function UsersPage() {
  const { data: users, isLoading, isError } = useGetUsersQuery();

  if (isLoading) return <p>Loading...</p>;
  if (isError) return <p>Error!</p>;

  return (
    <ul>
      {users?.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Pages Router:

```tsx
// pages/users.tsx
import { useGetUsersQuery } from "@/lib/features/api/apiSlice";

export default function UsersPage() {
  const { data: users, isLoading } = useGetUsersQuery();

  if (isLoading) return <p>Loading...</p>;

  return (
    <ul>
      {users?.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

> **RTK Query SSR** is covered in detail in chapter 37.

---

## 7. Impact

### RTK Query Changes Everything:
- **10x less code** for data fetching
- **Automatic caching** — no duplicate requests
- **Automatic refetching** — when cache is invalidated
- **Type-safe hooks** — generated automatically
- **Built into RTK** — no extra library needed

### When to Use RTK Query:
- ✅ Any API interaction (CRUD operations)
- ✅ When you need caching
- ✅ When you need automatic refetching
- ✅ When using Redux already

### When to Use createAsyncThunk Instead:
- Custom business logic beyond simple API calls
- When you need to dispatch multiple actions from one operation
- Complex conditional logic during the async operation

---

## 8. Summary

- **RTK Query** is a data fetching and caching solution built into Redux Toolkit
- Use `createApi` to define your API with **queries** (GET) and **mutations** (POST/PUT/DELETE)
- RTK Query auto-generates **React hooks** for each endpoint
- It handles **loading**, **error**, **caching**, and **refetching** automatically
- Add the API's **reducer** and **middleware** to your store
- Hooks provide `data`, `isLoading`, `isError`, `refetch`, and more
- **Cache invalidation** with tags ensures data stays fresh
- RTK Query replaces manual thunks for 90%+ of data fetching scenarios

---

**Prev:** [16_custom_hooks.md](./16_custom_hooks.md) | **Next:** [18_create_api_and_fetch_base_query.md](./18_create_api_and_fetch_base_query.md)
