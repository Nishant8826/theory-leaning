# Thunks — Async Logic in Redux

---

## 1. What

A **thunk** is a function that wraps an expression to **delay its evaluation**. In Redux, a thunk is a function that:
- Gets dispatched like a regular action
- Has access to `dispatch` and `getState`
- Can contain **async logic** (API calls, timers, etc.)

### Why the name "Thunk"?
The word "thunk" is a programming term meaning "a function that wraps another function to delay execution."

### Simple Analogy:
```
Regular Action:   "Here's what happened"  →  { type: "ADD_ITEM", payload: "apple" }
Thunk Action:     "Here's what to DO"     →  (dispatch, getState) => { /* async work */ }
```

Normal actions are **plain objects** (data). Thunks are **functions** (behavior).

---

## 2. Why

### The Problem: Reducers Can't Be Async!

Reducers must be **pure functions** — no side effects, no API calls, no randomness.

```ts
// ❌ NEVER DO THIS in a reducer!
reducers: {
  async fetchUsers(state) {
    const response = await fetch("/api/users"); // ❌ Side effect!
    state.users = await response.json();         // ❌ Async in reducer!
  }
}
```

### But Real Apps Need Async Logic!
- Fetching data from APIs
- Sending data to servers
- Delayed operations (timers)
- Complex conditional logic based on current state

### Thunks Are the Solution:
Thunks let you put async logic **outside reducers** but still interact with the Redux store.

```ts
// ✅ Thunk — async logic lives here, NOT in the reducer
const fetchUsers = () => async (dispatch: AppDispatch) => {
  dispatch(setLoading(true));
  try {
    const response = await fetch("/api/users");
    const users = await response.json();
    dispatch(setUsers(users)); // Dispatch a regular action with the data
  } catch (error) {
    dispatch(setError("Failed to fetch users"));
  } finally {
    dispatch(setLoading(false));
  }
};
```

---

## 3. How

### How Thunks Work:

```
Normal Flow:
dispatch(action) → action goes to reducer → state updates

Thunk Flow:
dispatch(thunkFunction) → middleware intercepts it → thunkFunction runs →
  inside thunk: dispatch(realAction) → action goes to reducer → state updates
```

### Step by Step:

```
1. You dispatch a FUNCTION (not an object)
2. The thunk middleware checks: "Is this a function?"
3. YES → Call the function with (dispatch, getState)
4. The function runs your async code
5. When the async code is done, it dispatches REAL actions (objects)
6. Those actions go through reducers as normal
```

### The Thunk Middleware (Simplified):

```ts
// This is roughly what the thunk middleware does:
const thunkMiddleware = (store) => (next) => (action) => {
  // If the "action" is actually a function...
  if (typeof action === "function") {
    // Call it with dispatch and getState
    return action(store.dispatch, store.getState);
  }
  // Otherwise, pass it along as a normal action
  return next(action);
};
```

---

## 4. Implementation

### Manual Thunk (Understanding the Concept):

```ts
// features/users/userSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserState {
  users: User[];
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  users: [],
  loading: false,
  error: null,
};

const userSlice = createSlice({
  name: "users",
  initialState,
  reducers: {
    setLoading(state, action: PayloadAction<boolean>) {
      state.loading = action.payload;
    },
    setUsers(state, action: PayloadAction<User[]>) {
      state.users = action.payload;
      state.error = null;
    },
    addUser(state, action: PayloadAction<User>) {
      state.users.push(action.payload);
    },
    setError(state, action: PayloadAction<string>) {
      state.error = action.payload;
    },
  },
});

export const { setLoading, setUsers, addUser, setError } = userSlice.actions;
export default userSlice.reducer;
```

```ts
// features/users/userThunks.ts
import { AppDispatch, RootState } from "../../store";
import { setLoading, setUsers, addUser, setError } from "./userSlice";

// ─────────────────────────────────────────────
// FETCH all users
// ─────────────────────────────────────────────
export const fetchUsers = () => {
  // This is the thunk — a function that returns a function
  return async (dispatch: AppDispatch, getState: () => RootState) => {
    // Check if already loading (using getState)
    const { loading } = getState().users;
    if (loading) return; // Don't fetch if already fetching

    dispatch(setLoading(true));

    try {
      const response = await fetch("https://jsonplaceholder.typicode.com/users");

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const users = await response.json();
      dispatch(setUsers(users));
    } catch (error) {
      dispatch(
        setError(error instanceof Error ? error.message : "Unknown error")
      );
    } finally {
      dispatch(setLoading(false));
    }
  };
};

// ─────────────────────────────────────────────
// CREATE a new user
// ─────────────────────────────────────────────
export const createUser = (userData: { name: string; email: string }) => {
  return async (dispatch: AppDispatch) => {
    dispatch(setLoading(true));

    try {
      const response = await fetch("https://jsonplaceholder.typicode.com/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });

      const newUser = await response.json();
      dispatch(addUser(newUser));
    } catch (error) {
      dispatch(
        setError(error instanceof Error ? error.message : "Failed to create user")
      );
    } finally {
      dispatch(setLoading(false));
    }
  };
};

// ─────────────────────────────────────────────
// Conditional thunk — uses getState
// ─────────────────────────────────────────────
export const fetchUsersIfEmpty = () => {
  return async (dispatch: AppDispatch, getState: () => RootState) => {
    const { users } = getState().users;

    // Only fetch if we don't have any users yet
    if (users.length === 0) {
      dispatch(fetchUsers());
    }
  };
};
```

---

## 5. React Integration

```tsx
// components/UserList.tsx
import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { RootState, AppDispatch } from "../store";
import { fetchUsers, createUser } from "../features/users/userThunks";

function UserList() {
  const { users, loading, error } = useSelector(
    (state: RootState) => state.users
  );
  const dispatch = useDispatch<AppDispatch>();

  // Fetch users on mount
  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Users ({users.length})</h1>
      <button
        onClick={() =>
          dispatch(createUser({ name: "New User", email: "new@example.com" }))
        }
      >
        Add User
      </button>

      <ul>
        {users.map((user) => (
          <li key={user.id}>
            {user.name} — {user.email}
          </li>
        ))}
      </ul>
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

import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { RootState, AppDispatch } from "@/lib/store";
import { fetchUsers } from "@/lib/features/users/userThunks";

export default function UsersPage() {
  const { users, loading, error } = useSelector(
    (state: RootState) => state.users
  );
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);

  if (loading) return <p>Loading users...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Users</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Pages Router with SSR:

```tsx
// pages/users.tsx
import { GetServerSideProps } from "next";
import { useSelector } from "react-redux";
import { RootState } from "@/lib/store";
import { setUsers } from "@/lib/features/users/userSlice";
import { wrapper } from "@/lib/store"; // next-redux-wrapper

export const getServerSideProps: GetServerSideProps =
  wrapper.getServerSideProps((store) => async () => {
    const response = await fetch("https://jsonplaceholder.typicode.com/users");
    const users = await response.json();

    // Dispatch on the SERVER
    store.dispatch(setUsers(users));

    return { props: {} };
  });

export default function UsersPage() {
  const users = useSelector((state: RootState) => state.users.users);
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

---

## 7. Impact

### Manual Thunks vs createAsyncThunk:

| Feature | Manual Thunks | createAsyncThunk |
|---------|---------------|-------------------|
| Boilerplate | More (manual loading/error) | Less (auto-generates) |
| Flexibility | Maximum | Good (with options) |
| TypeScript | Manual typing | Better type inference |
| Loading states | Manual dispatch | Auto pending/fulfilled/rejected |
| Best for | Simple or custom flows | Standard API calls |

### When to Use Thunks:
- ✅ **API calls** — fetching, creating, updating, deleting data
- ✅ **Conditional dispatching** — only dispatch if certain state conditions are met
- ✅ **Multi-step logic** — dispatch multiple actions in sequence
- ✅ **Accessing state** — use `getState()` to make decisions

### When NOT to Use Thunks:
- ❌ **Simple synchronous updates** — just use regular actions
- ❌ **Data fetching with caching** — use RTK Query instead
- ❌ **Complex event streams** — consider middleware or sagas

---

## 8. Summary

- A **thunk** is a function that gets dispatched instead of a plain action object
- Thunks receive `(dispatch, getState)` as arguments
- They allow **async logic** (API calls, timers) while keeping reducers pure
- Flow: `dispatch(thunk)` → middleware runs the function → thunk dispatches actions → reducers update state
- RTK includes thunk middleware **by default** — no setup needed
- Manual thunks give maximum flexibility but require more boilerplate
- `createAsyncThunk` (next chapter) reduces the boilerplate significantly
- For data fetching with caching, prefer **RTK Query** over thunks

---

**Prev:** [09_immer_and_immutability.md](./09_immer_and_immutability.md) | **Next:** [11_create_async_thunk.md](./11_create_async_thunk.md)
