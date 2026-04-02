# Polling and Lazy Queries

---

## 1. What

**Polling** means repeatedly making the same API request at specific time intervals (e.g., getting live score updates every 5 seconds).

**Lazy Queries** are queries that do **not** trigger automatically when a component mounts. Instead, they wait for you to manually trigger them (e.g., waiting for someone to click a "Search" button).

Both are built-in features of RTK Query.

---

## 2. Why

### Why Polling?
If your application depends on constantly changing data (like sports scores, stock tickers, or chat messages), you need the app to continuously ask the server for updates without user interaction.

### Why Lazy Queries?
By default, `useQuery` fires exactly when the component mounts. But sometimes you need data fetching tied to an action (like submitting a search form) rather than component mounting. If you use a normal query in a search bar, it will fire instantly on mount with an empty search term, which is wasteful and often results in an error.

---

## 3. How

### How Polling Works:
You simply pass a `pollingInterval` (in milliseconds) to your `useQuery` hook. RTK Query handles the `setInterval`/`clearInterval` logic automatically, ensuring no memory leaks when the component unmounts.

### How Lazy Queries Work:
Instead of `useSomeQuery`, you use `useLazySomeQuery`. This hook returns a trigger function (just like a mutation) and the result state. The fetch only starts when you call the trigger function.

---

## 4. Implementation

*(Assuming an already defined `apiSlice` with `getPosts` and `searchUsers` endpoints)*

### Polling Implementation:

```tsx
import { useGetPostsQuery } from '../features/api/apiSlice';

function LiveFeed() {
  // Pass an options object as the second argument
  const { data: posts, isFetching } = useGetPostsQuery(
    undefined, // First arg is the query arg (undefined if none)
    { 
      pollingInterval: 5000, // Fetch every 5 seconds
      skip: false // You can conditionally pause polling by setting skip: true
    }
  );

  return (
    <div>
      <h3>Live Feed {isFetching && "🔄"}</h3>
      <ul>
        {posts?.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Lazy Query Implementation:

```tsx
import { useState } from 'react';
import { useLazySearchUsersQuery } from '../features/api/apiSlice';

function SearchSearch() {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Notice we use use*Lazy*SearchUsersQuery
  const [triggerSearch, { data: users, isFetching, isUninitialized }] = useLazySearchUsersQuery();

  const handleSearch = () => {
    // Only fetch when the user explicitly clicks the button
    triggerSearch(searchTerm);
  };

  return (
    <div>
      <input 
        value={searchTerm} 
        onChange={(e) => setSearchTerm(e.target.value)} 
        placeholder="Enter username..." 
      />
      <button onClick={handleSearch} disabled={isFetching}>
        {isFetching ? "Searching..." : "Search"}
      </button>

      {isUninitialized && <p>Type a name and press search.</p>}

      <ul>
        {users?.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 5. React Integration

Both Polling and Lazy Queries cleanly integrate into functional React components, eliminating the need for custom `useEffect` hooks, `setTimeout`, or storing manual search state variables before fetching.

You can also dynamically pause and resume polling:
```tsx
const [isPolling, setIsPolling] = useState(true);

const { data } = useGetPostsQuery(undefined, {
  pollingInterval: isPolling ? 3000 : 0, // 0 means disabled
});
```

---

## 6. Next.js Integration

Be cautious with polling in Next.js applications, especially if integrated deeply with SSR. Polling is strictly a Client Side event. Ensure `pollingInterval` is only utilized inside components labeled with `"use client"`. 

Lazy Queries work great in Client Components for search/filter features on Next.js pages.

---

## 7. Impact

### Benefits of Built-in Polling:
- Avoids complex `useEffect` cleanup bugs.
- Can be paused via `skip` or setting interval to `0`.
- Only runs while the component is mounted.

### Benefits of Lazy Queries:
- Saves bandwidth avoiding unnecessary initial calls.
- Provides an `isUninitialized` flag so you can show a "Ready to search" empty state instead of "No results found".

---

## 8. Summary

- **Polling** allows continuous fetching at a set interval via `{ pollingInterval: ms }`.
- **Lazy Queries** defer fetching until manually triggered via `useLazyEndpointQuery()`.
- Both features are built directly into RTK Query auto-generated hooks.
- Polling pauses when interval is 0, or when the browser loses focus (can be customized).
- Lazy queries are perfect for "Search on submit" patterns.

---

**Prev:** [22_caching_and_invalidation.md](./22_caching_and_invalidation.md) | **Next:** [24_optimistic_updates.md](./24_optimistic_updates.md)
