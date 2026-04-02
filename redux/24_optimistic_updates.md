# Optimistic Updates in RTK Query

---

## 1. What

An **Optimistic Update** refers to updating your UI *before* the server has actually confirmed a mutation. You "optimistically" assume the server will say yes.

If the server responds with a success, you do nothing (the UI is already correct). 
If the server responds with an error, you **roll back** the UI to its previous state.

---

## 2. Why

### The Problem with Waiting:
When a user likes a post, they expect the heart icon to turn red instantly. If you wait for the API call to complete, there's a 100ms - 500ms delay. The app feels sluggish and unresponsive.

### The Solution:
Optimistic updates make your app feel **instantaneous**.
1. User clicks "Like".
2. UI instantly shows red heart.
3. Network request happens in the background.
4. If network fails, turn heart back to outline and show toast: "Failed to like post".

---

## 3. How

RTK Query provides a lifecycle method inside mutations called `onQueryStarted`. 

Within `onQueryStarted`, you can manually update the cached data of another query using `dispatch(api.util.updateQueryData(...))`.

If the mutation fails, you catch the error and invoke `.undo()` on the manual update you just made to revert the cache.

---

## 4. Implementation

```ts
// features/api/apiSlice.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

interface Post { id: number; title: string; likes: number }

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (builder) => ({
    
    getPosts: builder.query<Post[], void>({
      query: () => '/posts',
    }),

    likePost: builder.mutation<Post, number>({
      // 1. The actual mutation
      query: (id) => ({
        url: `/posts/${id}/like`,
        method: 'POST',
      }),

      // 2. The optimistic update lifecycle
      async onQueryStarted(id, { dispatch, queryFulfilled }) {
        
        // Optimistically update the 'getPosts' cache
        const patchResult = dispatch(
          apiSlice.util.updateQueryData('getPosts', undefined, (draft) => {
            // Find the post in the draft cache and update it directly (Immer is used here!)
            const post = draft.find((p) => p.id === id);
            if (post) {
              post.likes += 1;
            }
          })
        );

        try {
          // Wait for the mutation to finish successfully
          await queryFulfilled;
        } catch {
          // If the mutation fails, undo the optimistic update!
          patchResult.undo();
        }
      },
    }),

  }),
});

export const { useGetPostsQuery, useLikePostMutation } = apiSlice;
```

---

## 5. React Integration

Because all the optimistic update logic takes place inside the Redux slice, the React component stays completely clean. The component just calls the mutation trigger.

```tsx
import { useGetPostsQuery, useLikePostMutation } from '../apiSlice';

function PostList() {
  const { data: posts } = useGetPostsQuery();
  const [likePost] = useLikePostMutation();

  return (
    <ul>
      {posts?.map(post => (
        <li key={post.id}>
          {post.title} - {post.likes} Likes
          {/* Clicking this feels instant! */}
          <button onClick={() => likePost(post.id)}>👍 Like</button>
        </li>
      ))}
    </ul>
  );
}
```

---

## 6. Next.js Integration

Works identically via Client Components. Optimistic updates are particularly valuable in high-latency mobile networks, ensuring Next.js PWAs feel like native desktop apps.

---

## 7. Impact

### Why use Optimistic Updates?
- **World-Class UX:** Eliminates loading spinners for micro-interactions (likes, toggles, checkboxes, drag-and-drop).
- **Graceful Failure:** `patchResult.undo()` ensures your app never falls out of sync with the true backend state if there is a server error.

### When NOT to use them:
Do not use optimistic updates for operations involving severe consequences or external systems (e.g., executing a credit card payment, deleting a user account entirely). Only use them for reversible, low-risk UI state changes.

---

## 8. Summary

- **Optimistic Updates** change the UI instantly and revert if the server request fails.
- Achieved using the `onQueryStarted` lifecycle inside a mutation endpoint.
- `updateQueryData` allows manual, Immer-powered patching of cached query data.
- Enclose `queryFulfilled` in a try/catch block.
- Invoke `.undo()` in the catch block to rollback the cache on failure.

---

**Prev:** [23_polling_and_lazy_queries.md](./23_polling_and_lazy_queries.md) | **Next:** [25_file_uploads_rtk_query.md](./25_file_uploads_rtk_query.md)
