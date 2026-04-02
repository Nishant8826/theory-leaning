# Query Endpoints — Reading Data

---

## 1. What

A **query endpoint** in RTK Query is used for **reading data** (GET requests). When you define a query, RTK Query auto-generates a React hook that handles fetching, caching, loading states, and refetching.

```ts
// Define a query
getUsers: builder.query<User[], void>({
  query: () => "/users",
})

// Use the auto-generated hook
const { data, isLoading, error } = useGetUsersQuery();
```

---

## 2. Why

Queries solve the most common frontend problem: **fetching data from an API and displaying it**. Without RTK Query, you'd write `useEffect` + `useState` for every data fetching scenario.

```tsx
// ❌ Manual approach — repeated everywhere
useEffect(() => {
  setLoading(true);
  fetch("/api/users")
    .then(res => res.json())
    .then(data => { setUsers(data); setLoading(false); })
    .catch(err => { setError(err); setLoading(false); });
}, []);

// ✅ RTK Query — one line!
const { data: users, isLoading, error } = useGetUsersQuery();
```

---

## 3. How

### Query Hook Return Values:

```ts
const result = useGetUsersQuery();

// result contains:
result.data          // The response data (undefined until loaded)
result.isLoading     // true during FIRST load (no cached data)
result.isFetching    // true during ANY fetch (including refetch)
result.isSuccess     // true if request succeeded
result.isError       // true if request failed
result.error         // Error object (if failed)
result.isUninitialized // true before the query starts
result.refetch       // Function to manually refetch
result.currentData   // Current cached data (without refetch indicator)
result.fulfilledTimeStamp // When data was last fetched
```

### Key Difference: isLoading vs isFetching:
```
First load:     isLoading = true,  isFetching = true
Refetch:        isLoading = false, isFetching = true  ← Still has old data!
Cache hit:      isLoading = false, isFetching = false ← Instant!
```

---

## 4. Implementation

### Basic Queries:

```ts
// features/api/apiSlice.ts
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

interface User {
  id: number;
  name: string;
  email: string;
}

interface Post {
  id: number;
  title: string;
  body: string;
  userId: number;
}

interface Comment {
  id: number;
  postId: number;
  name: string;
  email: string;
  body: string;
}

export const apiSlice = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "https://jsonplaceholder.typicode.com" }),
  tagTypes: ["User", "Post"],
  endpoints: (builder) => ({
    // ── Simple query (no arguments) ──
    getUsers: builder.query<User[], void>({
      query: () => "/users",
    }),

    // ── Query with a single parameter ──
    getUserById: builder.query<User, number>({
      query: (userId) => `/users/${userId}`,
    }),

    // ── Query with multiple parameters ──
    getPosts: builder.query<Post[], { userId?: number; limit?: number }>({
      query: ({ userId, limit }) => {
        let url = "/posts";
        const params = new URLSearchParams();
        if (userId) params.set("userId", String(userId));
        if (limit) params.set("_limit", String(limit));
        const queryString = params.toString();
        return queryString ? `${url}?${queryString}` : url;
      },
    }),

    // ── Query with URL path parameter ──
    getPostComments: builder.query<Comment[], number>({
      query: (postId) => `/posts/${postId}/comments`,
    }),

    // ── Query with transformed response ──
    getUserNames: builder.query<string[], void>({
      query: () => "/users",
      transformResponse: (response: User[]) => {
        // Transform the API response before caching
        return response.map((user) => user.name);
      },
    }),

    // ── Query with response validation ──
    getPostById: builder.query<Post, number>({
      query: (id) => `/posts/${id}`,
      transformResponse: (response: Post) => {
        // Validate or transform response
        if (!response.id) throw new Error("Invalid post data");
        return {
          ...response,
          title: response.title.charAt(0).toUpperCase() + response.title.slice(1),
        };
      },
    }),

    // ── Query with custom error handling ──
    searchUsers: builder.query<User[], string>({
      query: (searchTerm) => `/users?q=${encodeURIComponent(searchTerm)}`,
      transformErrorResponse: (response) => {
        // Customize the error shape
        return {
          status: response.status,
          message: "Failed to search users. Please try again.",
        };
      },
    }),
  }),
});

export const {
  useGetUsersQuery,
  useGetUserByIdQuery,
  useGetPostsQuery,
  useGetPostCommentsQuery,
  useGetUserNamesQuery,
  useGetPostByIdQuery,
  useSearchUsersQuery,
} = apiSlice;
```

---

## 5. React Integration

### Using Query Hooks:

```tsx
// components/UserList.tsx
import { useGetUsersQuery } from "../features/api/apiSlice";

function UserList() {
  const { data: users, isLoading, isFetching, isError, error, refetch } =
    useGetUsersQuery();

  if (isLoading) return <div className="skeleton-loader" />;
  if (isError) return <div>Error: {JSON.stringify(error)}</div>;

  return (
    <div>
      <h1>Users {isFetching && "(refreshing...)"}</h1>
      <button onClick={refetch}>Refresh</button>
      <ul>
        {users?.map((user) => (
          <li key={user.id}>{user.name} - {user.email}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Query with Parameters:

```tsx
// components/UserDetail.tsx
import { useGetUserByIdQuery } from "../features/api/apiSlice";

function UserDetail({ userId }: { userId: number }) {
  // Pass the parameter to the hook
  const { data: user, isLoading, isError } = useGetUserByIdQuery(userId);

  if (isLoading) return <p>Loading user...</p>;
  if (isError) return <p>User not found.</p>;

  return (
    <div>
      <h2>{user?.name}</h2>
      <p>{user?.email}</p>
    </div>
  );
}

// Dynamic parameter
function UserPage() {
  const [selectedId, setSelectedId] = useState(1);

  return (
    <div>
      <select onChange={(e) => setSelectedId(Number(e.target.value))}>
        {[1, 2, 3, 4, 5].map((id) => (
          <option key={id} value={id}>User {id}</option>
        ))}
      </select>
      {/* Hook automatically refetches when selectedId changes! */}
      <UserDetail userId={selectedId} />
    </div>
  );
}
```

### Conditional Queries (Skip):

```tsx
function UserProfile({ userId }: { userId: number | null }) {
  // Skip the query if userId is null
  const { data: user, isLoading } = useGetUserByIdQuery(userId!, {
    skip: userId === null, // Don't fetch if no userId
  });

  if (!userId) return <p>Select a user</p>;
  if (isLoading) return <p>Loading...</p>;

  return <p>{user?.name}</p>;
}
```

### Query with Polling:

```tsx
function LiveFeed() {
  // Refetch every 5 seconds
  const { data: posts } = useGetPostsQuery(
    { limit: 10 },
    { pollingInterval: 5000 } // 5 seconds
  );

  return (
    <ul>
      {posts?.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Multiple Queries in One Component:

```tsx
function Dashboard() {
  const { data: users, isLoading: usersLoading } = useGetUsersQuery();
  const { data: posts, isLoading: postsLoading } = useGetPostsQuery({ limit: 5 });

  if (usersLoading || postsLoading) return <p>Loading dashboard...</p>;

  return (
    <div>
      <h2>Users: {users?.length}</h2>
      <h2>Recent Posts: {posts?.length}</h2>
    </div>
  );
}
```

### Selecting Specific Data from Query:

```tsx
import { useMemo } from "react";
import { useGetUsersQuery } from "../features/api/apiSlice";
import { createSelector } from "@reduxjs/toolkit";

function AdminList() {
  // selectFromResult lets you select specific fields
  const { adminUsers } = useGetUsersQuery(undefined, {
    selectFromResult: ({ data }) => ({
      adminUsers: data?.filter((u) => u.email.includes("admin")) ?? [],
    }),
  });

  return (
    <ul>
      {adminUsers.map((u) => (
        <li key={u.id}>{u.name}</li>
      ))}
    </ul>
  );
}
```

---

## 6. Next.js Integration

### App Router:

```tsx
// app/users/[id]/page.tsx
"use client";

import { useGetUserByIdQuery } from "@/lib/features/api/apiSlice";
import { useParams } from "next/navigation";

export default function UserPage() {
  const params = useParams();
  const userId = Number(params.id);

  const { data: user, isLoading, isError } = useGetUserByIdQuery(userId, {
    skip: isNaN(userId),
  });

  if (isLoading) return <p>Loading...</p>;
  if (isError) return <p>User not found</p>;

  return (
    <div>
      <h1>{user?.name}</h1>
      <p>{user?.email}</p>
    </div>
  );
}
```

---

## 7. Impact

### Query Features Summary:

| Feature | How |
|---------|-----|
| Simple fetch | `useGetUsersQuery()` |
| With parameter | `useGetUserByIdQuery(id)` |
| Skip/conditional | `{ skip: condition }` |
| Polling | `{ pollingInterval: 5000 }` |
| Refetch on focus | `{ refetchOnFocus: true }` |
| Refetch on reconnect | `{ refetchOnReconnect: true }` |
| Select subset | `{ selectFromResult: ... }` |
| Transform response | `transformResponse` in endpoint |

---

## 8. Summary

- **Query endpoints** are for **reading data** (GET requests)
- `builder.query<ResponseType, ArgType>` defines the types
- Hooks return `data`, `isLoading`, `isFetching`, `isError`, `error`, `refetch`
- Use `skip` to **conditionally prevent** queries
- Use `pollingInterval` for **real-time updates**
- Use `transformResponse` to **shape data** before caching
- Use `selectFromResult` to **select specific fields** from cached data
- Queries **auto-deduplicate** — same query from multiple components = one request
- **isLoading** = first load (no data), **isFetching** = any fetch (may have stale data)

---

**Prev:** [18_create_api_and_fetch_base_query.md](./18_create_api_and_fetch_base_query.md) | **Next:** [20_mutation_endpoints.md](./20_mutation_endpoints.md)
