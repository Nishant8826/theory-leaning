# Architecture & Best Practices

---

## 1. What

A well-structured Redux application is scalable, maintainable, and easy for new developers to understand. **Architecture** refers to how you organize your files, state tree, and logic. **Best practices** are the community-agreed rules for writing clean Redux code.

---

## 2. Why

If you throw all your Redux code into one massive file or structure it poorly, you will end up with a "Big Ball of Mud." 

Good architecture prevents:
- **Merge conflicts** when multiple developers touch state.
- **Circular dependencies** between Redux files.
- **Unclear boundaries** where API logic bleeds into UI components.

---

## 3. How

The modern Redux community strongly advocates for a **"Feature Folder"** approach (also known as the "Ducks" pattern).

Instead of separating files by *type* (actions folder, reducers folder, types folder), you group them by *feature* (auth folder, cart folder, user folder).

---

## 4. Implementation

### 1. Folder Structure (Feature-Based)

```
src/
  ├── store/
  │    ├── store.ts         # The configureStore setup
  │    ├── hooks.ts         # useAppDispatch, useAppSelector
  │    └── rootReducer.ts   # Optional: combineReducers
  ├── features/
  │    ├── auth/
  │    │    ├── authSlice.ts    # State, reducers, actions
  │    │    ├── authApi.ts      # RTK Query endpoints for Auth
  │    │    ├── authTypes.ts    # Interfaces
  │    │    └── AuthWidget.tsx  # Specific component
  │    ├── cart/
  │    │    ├── cartSlice.ts
  │    │    └── cartSelectors.ts
```

### 2. Best Practice: Keep Components "Dumb"
Do not put complex business logic or massive data transformation inside a React Component. Move it into regular Thunks, Reducers, or Selectors. `useSelector` is highly optimized when extracting pre-transformed data via `createSelector`.

### 3. Best Practice: Normalize Complex State
If your data is deeply nested (like nested comments inside nested posts), you will suffer performance issues when updating. Flatten your state into a normalized dictionary lookup `{ byId: {...}, allIds: [...] }`.
RTK provides `createEntityAdapter` to automate state normalization.

```ts
import { createEntityAdapter } from '@reduxjs/toolkit';

const usersAdapter = createEntityAdapter<User>();

const usersSlice = createSlice({
  name: 'users',
  initialState: usersAdapter.getInitialState(),
  reducers: {
    userAdded: usersAdapter.addOne,
    usersReceived: usersAdapter.setAll,
  },
});
```

### 4. Best Practice: Expose Actions, Not Implementation
Export your action creators from the slice file, and import them directly into components.

---

## 5. React Integration

By adopting Feature Folders, React components import everything they need from one place:

```tsx
// Clean, feature-focused imports
import { login, selectIsAuthenticated } from '../features/auth/authSlice';
import { useLoginMutation } from '../features/auth/authApi';
```

---

## 6. Next.js Integration

Feature folders fit cleanly alongside the `app` or `pages` directory. Usually, Redux is separated into a root `/lib` or `/store` directory next to the `/app` directory to maintain clear boundaries between routing and global state logic.

---

## 7. Impact

### Why follow this?
- **Scalability**: Want to delete the "Cart" feature? Just delete the `features/cart` folder. Everything is self-contained.
- **Discoverability**: When fixing an auth bug, developers know exactly which folder to open.
- **Efficiency**: `createEntityAdapter` and normalized state ensure you don't iterate over massive arrays to find and update a single object deeply nested inside a document.

---

## 8. Summary

- Discard old "actions/reducers/constants" folder structures.
- Group logic by domain/feature (Feature Folders).
- Co-locate Redux slices with the React components that heavily use them.
- Normalize deeply nested data using `createEntityAdapter`.
- Keep complex logic inside Redux (selectors/thunks), keeping components focused solely on rendering UI.

---

**Prev:** [26_rtk_query_vs_react_query.md](./26_rtk_query_vs_react_query.md) | **Next:** [28_typescript_with_redux.md](./28_typescript_with_redux.md)
