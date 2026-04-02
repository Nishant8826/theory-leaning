# createApi & fetchBaseQuery

---

## 1. What

### createApi
`createApi` is the **core function** of RTK Query. It defines your entire API — the base URL, endpoints, caching rules, and more. Think of it as a **blueprint** for all your API interactions.

### fetchBaseQuery
`fetchBaseQuery` is a **lightweight wrapper** around the native `fetch` API. It handles:
- Setting headers (like `Content-Type` and `Authorization`)
- Serializing request bodies to JSON
- Parsing response bodies from JSON
- Error handling

### Together:
```ts
createApi = WHAT endpoints exist and HOW they behave
fetchBaseQuery = HOW to make the actual HTTP requests
```

---

## 2. Why

### Without RTK Query:
```ts
// For EVERY endpoint, you write:
const fetchUsers = async () => {
  const token = getToken();
  const response = await fetch("https://api.example.com/users", {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) throw new Error("Failed");
  return response.json();
};
// Repeat this for EVERY single endpoint... 😩
```

### With createApi + fetchBaseQuery:
```ts
// Configure ONCE, use everywhere
const api = createApi({
  baseQuery: fetchBaseQuery({
    baseUrl: "https://api.example.com",
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) headers.set("Authorization", `Bearer ${token}`);
      return headers;
    },
  }),
  endpoints: (builder) => ({
    getUsers: builder.query({ query: () => "/users" }),
    getPosts: builder.query({ query: () => "/posts" }),
    // Add as many endpoints as you need!
  }),
});
```

---

## 3. How

### createApi Configuration:

```ts
createApi({
  // 1. reducerPath: unique key in Redux store
  reducerPath: "api",

  // 2. baseQuery: how to make HTTP requests
  baseQuery: fetchBaseQuery({ baseUrl: "..." }),

  // 3. tagTypes: cache invalidation tags
  tagTypes: ["User", "Post", "Comment"],

  // 4. endpoints: your API endpoints
  endpoints: (builder) => ({
    // queries (GET) and mutations (POST/PUT/DELETE)
  }),

  // 5. keepUnusedDataFor: seconds to keep unused cache (default: 60)
  keepUnusedDataFor: 60,

  // 6. refetchOnFocus: refetch when window gains focus
  refetchOnFocus: false,

  // 7. refetchOnReconnect: refetch when network reconnects
  refetchOnReconnect: false,

  // 8. refetchOnMountOrArgChange: refetch when component mounts
  refetchOnMountOrArgChange: false,
});
```

### fetchBaseQuery Configuration:

```ts
fetchBaseQuery({
  // Base URL for all requests
  baseUrl: "https://api.example.com",

  // Prepare headers for every request
  prepareHeaders: (headers, { getState, endpoint }) => {
    const token = (getState() as RootState).auth.token;
    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }
    headers.set("Accept", "application/json");
    return headers;
  },

  // Credentials for cookies
  credentials: "include", // "same-origin" | "include" | "omit"

  // Custom fetch function (optional)
  fetchFn: customFetch,

  // Timeout (optional)
  timeout: 10000, // 10 seconds
});
```

---

## 4. Implementation

### Complete API Slice:

```ts
// features/api/apiSlice.ts
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type { RootState } from "../../store";

// ─── Types ───
interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "user";
}

interface Post {
  id: number;
  title: string;
  body: string;
  userId: number;
}

interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}

interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  user: User;
  token: string;
}

// ─── API Slice ───
export const apiSlice = createApi({
  reducerPath: "api",

  baseQuery: fetchBaseQuery({
    baseUrl: "https://api.example.com/v1",

    // Auto-attach auth token to every request
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.token;
      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }
      return headers;
    },

    // Include cookies
    credentials: "include",
  }),

  tagTypes: ["User", "Post"],

  // Keep unused cache for 5 minutes
  keepUnusedDataFor: 300,

  endpoints: (builder) => ({
    // ── AUTH ──
    login: builder.mutation<LoginResponse, LoginRequest>({
      query: (credentials) => ({
        url: "/auth/login",
        method: "POST",
        body: credentials,
      }),
    }),

    // ── USERS ──
    getUsers: builder.query<User[], void>({
      query: () => "/users",
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: "User" as const, id })),
              { type: "User", id: "LIST" },
            ]
          : [{ type: "User", id: "LIST" }],
    }),

    getUserById: builder.query<User, number>({
      query: (id) => `/users/${id}`,
      providesTags: (result, error, id) => [{ type: "User", id }],
    }),

    createUser: builder.mutation<User, Omit<User, "id">>({
      query: (newUser) => ({
        url: "/users",
        method: "POST",
        body: newUser,
      }),
      invalidatesTags: [{ type: "User", id: "LIST" }],
    }),

    updateUser: builder.mutation<User, Partial<User> & Pick<User, "id">>({
      query: ({ id, ...patch }) => ({
        url: `/users/${id}`,
        method: "PATCH",
        body: patch,
      }),
      invalidatesTags: (result, error, { id }) => [
        { type: "User", id },
        { type: "User", id: "LIST" },
      ],
    }),

    deleteUser: builder.mutation<void, number>({
      query: (id) => ({
        url: `/users/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: (result, error, id) => [
        { type: "User", id },
        { type: "User", id: "LIST" },
      ],
    }),

    // ── POSTS (with pagination) ──
    getPosts: builder.query<PaginatedResponse<Post>, { page: number; limit: number }>({
      query: ({ page, limit }) => `/posts?page=${page}&limit=${limit}`,
      providesTags: (result) =>
        result
          ? [
              ...result.data.map(({ id }) => ({ type: "Post" as const, id })),
              { type: "Post", id: "LIST" },
            ]
          : [{ type: "Post", id: "LIST" }],
    }),

    getPostById: builder.query<Post, number>({
      query: (id) => `/posts/${id}`,
      providesTags: (result, error, id) => [{ type: "Post", id }],
    }),

    // ── SEARCH ──
    searchUsers: builder.query<User[], string>({
      query: (searchTerm) => `/users/search?q=${encodeURIComponent(searchTerm)}`,
    }),
  }),
});

// ─── Auto-Generated Hooks ───
export const {
  useLoginMutation,
  useGetUsersQuery,
  useGetUserByIdQuery,
  useCreateUserMutation,
  useUpdateUserMutation,
  useDeleteUserMutation,
  useGetPostsQuery,
  useGetPostByIdQuery,
  useSearchUsersQuery,
} = apiSlice;
```

### Store Setup:

```ts
// store.ts
import { configureStore } from "@reduxjs/toolkit";
import { apiSlice } from "./features/api/apiSlice";
import authReducer from "./features/auth/authSlice";

const store = configureStore({
  reducer: {
    auth: authReducer,
    [apiSlice.reducerPath]: apiSlice.reducer, // ← Add API reducer
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(apiSlice.middleware), // ← Add API middleware
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
```

### Custom Base Query with Error Handling:

```ts
import { fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type { BaseQueryFn, FetchArgs, FetchBaseQueryError } from "@reduxjs/toolkit/query";

// Custom base query with automatic token refresh
const baseQuery = fetchBaseQuery({
  baseUrl: "https://api.example.com/v1",
  prepareHeaders: (headers, { getState }) => {
    const token = (getState() as RootState).auth.token;
    if (token) headers.set("Authorization", `Bearer ${token}`);
    return headers;
  },
});

// Wrapper that handles 401 errors (token expired)
const baseQueryWithReauth: BaseQueryFn<string | FetchArgs, unknown, FetchBaseQueryError> =
  async (args, api, extraOptions) => {
    let result = await baseQuery(args, api, extraOptions);

    if (result.error && result.error.status === 401) {
      // Try to refresh the token
      const refreshResult = await baseQuery(
        { url: "/auth/refresh", method: "POST" },
        api,
        extraOptions
      );

      if (refreshResult.data) {
        // Store the new token
        const { token } = refreshResult.data as { token: string };
        api.dispatch(setToken(token));

        // Retry the original request
        result = await baseQuery(args, api, extraOptions);
      } else {
        // Refresh failed — log out
        api.dispatch(logout());
      }
    }

    return result;
  };

// Use the custom base query
export const apiSlice = createApi({
  baseQuery: baseQueryWithReauth, // ← Uses our custom wrapper!
  endpoints: (builder) => ({
    // ... endpoints
  }),
});
```

---

## 5. React Integration

```tsx
// components/UserManager.tsx
import {
  useGetUsersQuery,
  useCreateUserMutation,
  useUpdateUserMutation,
  useDeleteUserMutation,
} from "../features/api/apiSlice";

function UserManager() {
  // Fetch
  const { data: users, isLoading, isError, refetch } = useGetUsersQuery();

  // Mutations
  const [createUser, { isLoading: isCreating }] = useCreateUserMutation();
  const [updateUser] = useUpdateUserMutation();
  const [deleteUser] = useDeleteUserMutation();

  if (isLoading) return <p>Loading...</p>;
  if (isError) return <button onClick={refetch}>Retry</button>;

  return (
    <div>
      <button
        onClick={async () => {
          try {
            await createUser({ name: "New", email: "new@test.com", role: "user" }).unwrap();
            // Cache is automatically invalidated — users list will refetch!
          } catch (err) {
            console.error("Create failed:", err);
          }
        }}
        disabled={isCreating}
      >
        Add User
      </button>

      {users?.map((user) => (
        <div key={user.id}>
          <span>{user.name}</span>
          <button onClick={() => updateUser({ id: user.id, name: "Updated" })}>
            Edit
          </button>
          <button onClick={() => deleteUser(user.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}
```

---

## 6. Next.js Integration

### App Router:

```tsx
// app/users/page.tsx
"use client";
import { useGetUsersQuery } from "@/lib/features/api/apiSlice";

export default function UsersPage() {
  const { data: users, isLoading } = useGetUsersQuery();

  if (isLoading) return <p>Loading...</p>;

  return (
    <ul>
      {users?.map((u) => (
        <li key={u.id}>{u.name}</li>
      ))}
    </ul>
  );
}
```

### Pages Router:
Same as App Router — hooks work in both.

### SSR Support:
RTK Query supports SSR through `endpoints.initiate()` — covered in chapter 37.

---

## 7. Impact

### createApi is Your API's Single Source of Truth:
- **All endpoints** in one place
- **All types** defined alongside endpoints
- **All cache rules** centralized
- **All hooks** auto-generated

### Best Practices:
1. **One API slice** for one base URL (usually one per backend)
2. **Multiple API slices** for different backends
3. **Always add tagTypes** for cache invalidation
4. **Use prepareHeaders** for auth tokens
5. **Add refetch behaviors** based on your needs

---

## 8. Summary

- `createApi` defines your entire API — endpoints, caching, and behavior
- `fetchBaseQuery` wraps `fetch` with JSON handling and header management
- `prepareHeaders` is where you attach **auth tokens**
- `tagTypes` enable **cache invalidation**
- `endpoints` define **queries** (GET) and **mutations** (POST/PUT/DELETE)
- Add the API's **reducer** and **middleware** to your store
- Hooks are **auto-generated** based on endpoint names
- Use a **custom base query wrapper** for auth token refresh
- `keepUnusedDataFor` controls how long unused cache persists

---

**Prev:** [17_rtk_query_introduction.md](./17_rtk_query_introduction.md) | **Next:** [19_query_endpoints.md](./19_query_endpoints.md)
