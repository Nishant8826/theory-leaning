# Common Mistakes & Debugging

---

## 1. What

Even with Redux Toolkit reducing boilerplate, developers still run into common pitfalls. This section identifies the most frequent mistakes made by beginners and provides strategies for debugging them using the **Redux DevTools**.

---

## 2. Why

Understanding these mistakes early saves hours of frustration. Many Redux issues fail silently — meaning the app doesn't crash, but the UI just fails to update. 

---

## 3. The 5 Most Common Mistakes

### ❌ Mistake 1: Mutating state directly without RTK's Immer context
If you manually mutate a variable outside of an RTK `createSlice` reducer, React won't detect the change.
```ts
// INSIDE a RTK Slice (✅ Good - Immer handles it)
increment(state) { state.count += 1; }

// OUTSIDE a Slice, e.g., in a component directly mutating the hook result (❌ Bad)
const user = useAppSelector(state => state.auth.user);
user.name = "Nishant"; // React will NOT re-render!
```

### ❌ Mistake 2: Missing `export default` for Reducers
When adding a slice to the store, people often accidentally export the slice object instead of its `.reducer`.
```ts
// ❌ WRONG
export default userSlice; 
// store.ts: reducer: { user: userSlice } <- Error!

// ✅ RIGHT
export default userSlice.reducer; 
// store.ts: reducer: { user: userReducer }
```

### ❌ Mistake 3: Infinite Loops with `useSelector`
Returning a new object/array literal in `useSelector` forces a re-render on *every single dispatch anywhere in the app*.
```tsx
// ❌ WRONG - Creates a new array reference every time ANY action fires
const filtered = useAppSelector(state => state.todos.filter(t => t.active));

// ✅ RIGHT - Use createSelector inside the slice to memoize the reference
const filtered = useAppSelector(selectActiveTodos);
```

### ❌ Mistake 4: Forgetting RTK Query Tag Invalidation
You run a mutation, it succeeds, but the screen doesn't update.
**Reason:** You forgot to add `invalidatesTags: ['YourTag']` to the mutation, or you forgot to add `providesTags: ['YourTag']` to the query.

### ❌ Mistake 5: Treating Asynchronous Thunks as Synchronous
You dispatch a thunk and try to read the state on the next line.
```tsx
// ❌ WRONG
dispatch(fetchUsers());
console.log(users); // Still empty! The request hasn't finished!

// ✅ RIGHT
// Either use a useEffect listening to 'users', or unwrap the result:
const result = await dispatch(fetchUsers()).unwrap();
console.log(result);
```

---

## 4. Debugging with Redux DevTools

The **Redux DevTools Extension** is a browser plugin (Chrome/Firefox) that provides an X-ray view into your Redux store. RTK enables it automatically.

### Key Features to Use:
1. **The Action List:** On the left, see every single action that fired in chronological order.
   - *Example: You'll see `users/fetch/pending` followed by `users/fetch/fulfilled`.*
2. **The "Diff" Tab:** See exactly which properties changed state between action `n` and action `n+1`. If Diff is empty, your reducer didn't do anything.
3. **The "State" Tab:** View the entire global JSON tree at that specific point in time.
4. **Time Travel (Slider at bottom):** Scrub backwards to "undo" actions and watch your UI revert in real-time.

---

## 5. React Integration Debugging

If a component isn't rendering:
1. **Check DevTools:** Did the action fire?
2. **Check State:** Did the state branch actually update in the DevTools?
3. **Check useSelector:** Is your component selecting the correct path? Add a `console.log` inside the component body right beneath the `useSelector` to check what it is evaluating to.

---

## 6. Next.js Integration Debugging

**"Cannot read properties of undefined (reading 'getState')"**
If you see this error, you likely tried to access the Redux store from a Server Component. Remember: Redux is strictly client-side unless using hydration techniques (refer back to File 29). Ensure the component tree utilizing `useAppSelector` is wrapped inside a `'use client'` boundary.

---

## 7. Summary

- **Never** mutate Redux state directly outside of `createSlice` reducers.
- **Always** export `.reducer` from slices.
- If UI is stale after a mutation, check your `invalidatesTags` definitions.
- If your app is sluggish, search for `useAppSelector` calls returning new arrays or objects inline. Fix them via `createSelector`.
- Rely entirely on the **Redux DevTools** — it is the single most powerful asset provided by the Redux ecosystem.

---

**Prev:** [30_advanced_topics.md](./30_advanced_topics.md) | **Next:** None
