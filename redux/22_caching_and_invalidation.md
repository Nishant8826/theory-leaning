# Caching and Invalidation in RTK Query

---

## 1. What

**Caching** means storing the result of an API request so that if you ask for the same data again, it's served instantly from memory instead of making another network request.

**Invalidation** means telling RTK Query that the cached data is now "stale" or "out of date," so it needs to fetch fresh data from the server.

RTK Query uses an automated, tag-based cache invalidation system.

---

## 2. Why

### The Caching Problem:
If you fetch a list of posts on the Home Page, and then navigate to the Profile Page (which also shows posts), you shouldn't have to wait for the posts to download again.

### The Invalidation Problem:
If you **create a new post**, the cached list of posts is now missing the new item. You must invalidate the old cache so the app fetches the updated list.

### Why Tag-Based?
Instead of manually writing code to say "update the store array and push the new post object," you simply "tag" the data. When a mutation occurs, you tell RTK Query which tags are invalid, and it automatically refetches the affected queries.

---

## 3. How

### The Tag System:

1. **Declare Tags**: Tell the API slice what types of flags exist (`tagTypes: ['Post']`).
2. **Provide Tags**: A Query endpoint labels its returned data with tags (`providesTags: ['Post']`).
3. **Invalidate Tags**: A Mutation endpoint declares which tags it affects (`invalidatesTags: ['Post']`).

```
Query (getPosts) --------> providesTags: ['Post']
                             ^
                             | (matches)
                             v
Mutation (addPost) ------> invalidatesTags: ['Post']
```
When `addPost` succeeds, any query providing the `'Post'` tag is immediately refetched.

---

## 4. Implementation

### Advanced Tagging Pattern:

Usually, providing just `['Post']` is too broad. If you update Post #1, you don't want to refetch Post #2.

The standard pattern is to provide specific IDs:

```ts
// features/api/apiSlice.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

interface Post { id: number; title: string; body: string }

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  // 1. Declare the tag type
  tagTypes: ['Post'],
  endpoints: (builder) => ({
    
    // ── QUERY ──
    getPosts: builder.query<Post[], void>({
      query: () => '/posts',
      // 2. Provide tags for the whole list, AND each individual item
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: 'Post' as const, id })),
              { type: 'Post', id: 'LIST' },
            ]
          : [{ type: 'Post', id: 'LIST' }],
    }),

    // ── MUTATION: Create (affects the LIST) ──
    addPost: builder.mutation<Post, Partial<Post>>({
      query: (body) => ({ url: '/posts', method: 'POST', body }),
      // 3. Invalidate the generic LIST tag.
      // This forces getPosts to refetch.
      invalidatesTags: [{ type: 'Post', id: 'LIST' }],
    }),

    // ── MUTATION: Update (affects a SPECIFIC item) ──
    updatePost: builder.mutation<Post, Partial<Post> & Pick<Post, 'id'>>({
      query: ({ id, ...patch }) => ({ url: `/posts/${id}`, method: 'PUT', body: patch }),
      // 4. Invalidate the specific item.
      // This forces any query providing THIS specific ID to refetch.
      invalidatesTags: (result, error, { id }) => [{ type: 'Post', id }],
    }),

  }),
});
```

---

## 5. React Integration

Because caching works internally, your React components stay incredibly simple.

```tsx
import { useGetPostsQuery, useAddPostMutation } from '../apiSlice';

function PostsContainer() {
  const { data: posts, isLoading } = useGetPostsQuery();
  const [addPost] = useAddPostMutation();

  const handleCreate = async () => {
    // When this succeeds, invalidatesTags runs.
    // useGetPostsQuery automatically refetches in the background!
    await addPost({ title: 'New Post', body: '...' });
  };

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <button onClick={handleCreate}>Add Post</button>
      <ul>{posts?.map(p => <li key={p.id}>{p.title}</li>)}</ul>
    </div>
  );
}
```

---

## 6. Next.js Integration

Works identically in Next.js Client Components. The cache lives in the Redux store on the client side, significantly speeding up client-side navigation between pages that share data.

---

## 7. Impact

### Why Tag Invalidation is a Game Changer:
Manual state synchronization is notoriously bug-prone. If you delete an item, you often forget to remove it from every slice of state.
With RTK Query's tag system, you declare relationships declaratively. You never manually edit arrays or filter objects; you just say "this data is now garbage," and Redux goes and gets the fresh truth from the server.

### Cache Lifetime:
By default, when components stop using a cached query hook, RTK Query keeps the data for **60 seconds**. If you request it again within 60s, it's instant. If 60s pass, the cache is garbage collected.

---

## 8. Summary

- **Caching** prevents redundant network requests.
- **Invalidation** forces a refetch when data changes.
- **`tagTypes`** defines the "labels" available in your API.
- **`providesTags`** in queries applies labels to fetched data.
- **`invalidatesTags`** in mutations marks labels as stale.
- Use the `{ type: 'Item', id: 'LIST' }` pattern for precise, granular updates without over-fetching.

---

**Prev:** [21_auto_generated_hooks.md](./21_auto_generated_hooks.md) | **Next:** [23_polling_and_lazy_queries.md](./23_polling_and_lazy_queries.md)
