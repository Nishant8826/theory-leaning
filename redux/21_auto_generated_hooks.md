# Auto-Generated Hooks in RTK Query

---

## 1. What

One of the most magical features of RTK Query is its ability to **automatically generate React hooks** for every endpoint you define in your API slice.

You don't write these hooks yourself — they are generated dynamically based on the names of your endpoints.

```ts
// If you define these endpoints:
endpoints: (builder) => ({
  getUsers: builder.query(...),
  createUser: builder.mutation(...),
})

// RTK Query generates these hooks automatically:
export const { useGetUsersQuery, useCreateUserMutation } = apiSlice;
```

---

## 2. Why

### The Problem:
Writing custom hooks for every API call is repetitive and tedious. You have to handle `useState` for data, loading, and error states, plus `useEffect` to trigger the fetch.

### The Solution:
RTK Query handles the Redux store connection, dispatching actions, and state selection internally, and wraps it all in a simple, easy-to-use React hook.

This gives you:
- **Zero boilerplate** in your components
- **Type safety** right out of the box
- **Consistent behavior** across all API interactions

---

## 3. How

### How RTK Query Names Hooks:

RTK Query uses a strict naming convention to generate hooks:

1. Start with `use`
2. Capitalize the endpoint name
3. Append `Query` or `Mutation` based on the endpoint type

| Endpoint Name | Endpoint Type | Generated Hook Name |
|--------------|---------------|----------------------|
| `getPosts` | `query` | `useGetPostsQuery` |
| `addPost` | `mutation` | `useAddPostMutation` |
| `updateUser` | `mutation` | `useUpdateUserMutation` |
| `userProfile`| `query` | `useUserProfileQuery` |

### What Query Hooks Return:
Query hooks return an object containing the response state:
- `data`: The transformed response data
- `isLoading`: True for the very first fetch
- `isFetching`: True for *any* fetch (initial or refetch)
- `isSuccess`: True if the query has successfully completed
- `isError`: True if an error occurred
- `error`: The error payload
- `refetch`: A function to forcefully re-trigger the query

### What Mutation Hooks Return:
Mutation hooks return a tuple `[trigger, result]`:
- `trigger`: The function you call to fire the mutation
- `result`: An object containing `data`, `isLoading`, `isSuccess`, `isError`, `error`, `reset`

---

## 4. Implementation

### Defining Endpoints and Exporting Hooks:

```ts
// features/api/postsApi.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

interface Post {
  id: number;
  title: string;
}

export const postsApi = createApi({
  reducerPath: 'postsApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (builder) => ({
    // Endpoint: getAllPosts
    getAllPosts: builder.query<Post[], void>({
      query: () => '/posts',
    }),

    // Endpoint: getPostById
    getPostById: builder.query<Post, number>({
      query: (id) => `/posts/${id}`,
    }),

    // Endpoint: addNewPost
    addNewPost: builder.mutation<Post, Partial<Post>>({
      query: (initialPost) => ({
        url: '/posts',
        method: 'POST',
        body: initialPost,
      }),
    }),
  }),
});

// Auto-generated hooks are attached to the API slice object
export const {
  useGetAllPostsQuery,
  useGetPostByIdQuery,
  useAddNewPostMutation,
} = postsApi;
```

---

## 5. React Integration

### Using Generated Query Hooks:

```tsx
import { useGetAllPostsQuery } from '../features/api/postsApi';

function PostsList() {
  // Call the generated hook
  // It automatically initiates the fetch when the component mounts
  const { data: posts, isLoading, isError } = useGetAllPostsQuery();

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>An error occurred</div>;

  return (
    <ul>
      {posts?.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Using Generated Mutation Hooks:

```tsx
import { useState } from 'react';
import { useAddNewPostMutation } from '../features/api/postsApi';

function AddPostForm() {
  const [title, setTitle] = useState('');
  
  // Call the generated hook
  const [addNewPost, { isLoading }] = useAddNewPostMutation();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Trigger the mutation
      await addNewPost({ title }).unwrap();
      setTitle('');
    } catch (err) {
      console.error('Failed to save the post', err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <button disabled={isLoading}>Save Post</button>
    </form>
  );
}
```

---

## 6. Next.js Integration

Generated hooks work exactly the same in Next.js **Client Components**.

```tsx
// app/posts/page.tsx
"use client"; // Required to use RTK Query hooks

import { useGetAllPostsQuery } from "@/lib/features/api/postsApi";

export default function PostsPage() {
  const { data: posts, isLoading } = useGetAllPostsQuery();

  if (isLoading) return <p>Loading...</p>;
  return <ul>{posts?.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

*(Note: In Server Components, you cannot use hooks. You must use the `initiate` action, which will be covered in the SSR chapter).*

---

## 7. Impact

### Why Auto-Generated Hooks Matter:
- **Consistency**: Every query and mutation has a predictable interface.
- **Productivity**: Define your schema once, get fully typed data-fetching logic for free.
- **Safety**: Because they are strongly typed, TypeScript will warn you if you pass the wrong arguments to a mutation or misspell a returned property.

---

## 8. Summary

- RTK Query dynamically generates React hooks for every endpoint.
- Naming convention: `use` + `CapitalizedEndpointName` + `Query` (or `Mutation`).
- Query hooks return state (`data`, `isLoading`, `error`) and auto-execute on mount.
- Mutation hooks return a trigger function and state, and wait for you to call them.
- They completely eliminate the need to write custom `useEffect` fetching logic.

---

**Prev:** [20_mutation_endpoints.md](./20_mutation_endpoints.md) | **Next:** [22_caching_and_invalidation.md](./22_caching_and_invalidation.md)
