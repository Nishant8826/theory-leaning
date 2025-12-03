# RTK Query
- RTK Query enables efficient data fetching, caching(default), and optimistic updates, although by default there will be pessimistic updates(we need to do optmistic mannually)
- Handling loading, error, and slow network scenarios.
- RTK Query provides automatic caching for optimized data fetching.
- RTK Query allows using RT query library inside Redux Toolkit for CRUD operations and optimistic updates.

```
Pessimistic updates assume conflicts will occur and lock data before a change, prioritizing data consistency over performance. Optimistic updates assume conflicts are rare, update the UI immediately, and only handle conflicts later if they arise, prioritizing user experience and performance.
```

### RTK Query inlcudes inside `@reduxjs/toolkit` library only 