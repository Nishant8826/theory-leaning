# createAsyncThunk

---

## 1. What

`createAsyncThunk` is an RTK utility that **automates the boilerplate** of async operations. Instead of manually dispatching loading, success, and error actions, `createAsyncThunk` generates them automatically.

### What It Creates for You:
```
createAsyncThunk("users/fetch", asyncFunction)
  ↓ Generates 3 action types:
  ├── "users/fetch/pending"    → Dispatched when the async call starts
  ├── "users/fetch/fulfilled"  → Dispatched when it succeeds
  └── "users/fetch/rejected"   → Dispatched when it fails
```

### Before vs After:
```ts
// ❌ Manual thunk — lots of boilerplate
const fetchUsers = () => async (dispatch) => {
  dispatch(setLoading(true));
  dispatch(setError(null));
  try {
    const res = await fetch("/api/users");
    const data = await res.json();
    dispatch(setUsers(data));
  } catch (err) {
    dispatch(setError(err.message));
  } finally {
    dispatch(setLoading(false));
  }
};

// ✅ createAsyncThunk — clean and standardized
const fetchUsers = createAsyncThunk("users/fetch", async () => {
  const res = await fetch("/api/users");
  return res.json(); // Whatever you return = fulfilled payload
});
```

---

## 2. Why

### Problems createAsyncThunk Solves:

**1. Repetitive loading/error/success pattern:**
Every API call needs the same pattern:
```
1. Set loading = true
2. Try the API call
3. On success: set data, clear error
4. On failure: set error
5. Set loading = false
```

`createAsyncThunk` handles steps 1, 3, 4, and 5 automatically!

**2. Standardized action naming:**
Instead of inventing your own action types for each state:
```ts
"FETCH_USERS_REQUEST"  // or "FETCH_USERS_LOADING"?
"FETCH_USERS_SUCCESS"  // or "FETCH_USERS_COMPLETE"?
"FETCH_USERS_FAILURE"  // or "FETCH_USERS_ERROR"?
```
createAsyncThunk uses a consistent pattern:
```ts
"users/fetch/pending"
"users/fetch/fulfilled"
"users/fetch/rejected"
```

**3. Automatic error handling:**
Errors in your async function are automatically caught and dispatched as the `rejected` action.

---

## 3. How

### How createAsyncThunk Works:

```ts
const myThunk = createAsyncThunk(
  "sliceName/operationName",  // Action type prefix
  async (argument, thunkAPI) => {
    // Your async logic here
    // Whatever you RETURN becomes the fulfilled payload
    // Whatever you THROW becomes the rejected error
  }
);
```

### The Lifecycle:

```
dispatch(myThunk(arg))
    ↓
1. Dispatches: { type: "sliceName/operationName/pending" }
    ↓
2. Runs your async function
    ↓
3a. If SUCCESS:
    Dispatches: { type: "sliceName/operationName/fulfilled", payload: returnValue }
    ↓
3b. If ERROR:
    Dispatches: { type: "sliceName/operationName/rejected", error: errorInfo }
```

### The thunkAPI Parameter:

```ts
createAsyncThunk("action/type", async (arg, thunkAPI) => {
  // thunkAPI contains:
  thunkAPI.dispatch;      // Dispatch other actions
  thunkAPI.getState;      // Access current state
  thunkAPI.extra;         // Extra argument (like API instance)
  thunkAPI.requestId;     // Unique ID for this request
  thunkAPI.signal;        // AbortSignal for cancellation
  thunkAPI.rejectWithValue(value); // Return custom error payload
  thunkAPI.fulfillWithValue(value); // Return with meta
});
```

---

## 4. Implementation

### Basic Fetch:

```ts
// features/posts/postSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";

// Types
interface Post {
  id: number;
  title: string;
  body: string;
  userId: number;
}

interface PostState {
  posts: Post[];
  selectedPost: Post | null;
  loading: boolean;
  error: string | null;
}

const initialState: PostState = {
  posts: [],
  selectedPost: null,
  loading: false,
  error: null,
};

// ─────────────────────────────────────────────
// Async Thunks
// ─────────────────────────────────────────────

// FETCH all posts
export const fetchPosts = createAsyncThunk(
  "posts/fetchAll",
  async () => {
    const response = await fetch("https://jsonplaceholder.typicode.com/posts");
    if (!response.ok) throw new Error("Failed to fetch posts");
    const data: Post[] = await response.json();
    return data; // This becomes the "fulfilled" payload
  }
);

// FETCH single post
export const fetchPostById = createAsyncThunk(
  "posts/fetchById",
  async (postId: number) => {
    const response = await fetch(
      `https://jsonplaceholder.typicode.com/posts/${postId}`
    );
    if (!response.ok) throw new Error("Post not found");
    const data: Post = await response.json();
    return data;
  }
);

// CREATE a post
export const createPost = createAsyncThunk(
  "posts/create",
  async (postData: { title: string; body: string; userId: number }) => {
    const response = await fetch("https://jsonplaceholder.typicode.com/posts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(postData),
    });
    const data: Post = await response.json();
    return data;
  }
);

// DELETE a post with rejectWithValue for custom error handling
export const deletePost = createAsyncThunk(
  "posts/delete",
  async (postId: number, thunkAPI) => {
    try {
      const response = await fetch(
        `https://jsonplaceholder.typicode.com/posts/${postId}`,
        { method: "DELETE" }
      );

      if (!response.ok) {
        // rejectWithValue lets you send a CUSTOM error payload
        return thunkAPI.rejectWithValue({
          message: "Failed to delete post",
          statusCode: response.status,
        });
      }

      return postId; // Return the deleted ID
    } catch (error) {
      return thunkAPI.rejectWithValue({
        message: "Network error",
        statusCode: 0,
      });
    }
  }
);

// CONDITIONAL fetch — only fetch if we don't have posts
export const fetchPostsIfNeeded = createAsyncThunk(
  "posts/fetchIfNeeded",
  async (_, thunkAPI) => {
    const state = thunkAPI.getState() as { posts: PostState };

    // Skip if we already have posts
    if (state.posts.posts.length > 0) {
      // Return existing posts (no API call needed)
      return state.posts.posts;
    }

    const response = await fetch("https://jsonplaceholder.typicode.com/posts");
    return response.json();
  },
  {
    // Condition: prevent duplicate requests
    condition: (_, { getState }) => {
      const state = getState() as { posts: PostState };
      // If already loading, DON'T start another request
      if (state.posts.loading) return false;
    },
  }
);

// ─────────────────────────────────────────────
// Slice
// ─────────────────────────────────────────────
const postSlice = createSlice({
  name: "posts",
  initialState,
  reducers: {
    clearSelectedPost(state) {
      state.selectedPost = null;
    },
    clearError(state) {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // ── fetchPosts ──
      .addCase(fetchPosts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPosts.fulfilled, (state, action) => {
        state.loading = false;
        state.posts = action.payload;
      })
      .addCase(fetchPosts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Failed to fetch posts";
      })

      // ── fetchPostById ──
      .addCase(fetchPostById.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchPostById.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedPost = action.payload;
      })
      .addCase(fetchPostById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Post not found";
      })

      // ── createPost ──
      .addCase(createPost.fulfilled, (state, action) => {
        state.posts.unshift(action.payload); // Add to beginning
      })

      // ── deletePost (with rejectWithValue) ──
      .addCase(deletePost.fulfilled, (state, action) => {
        state.posts = state.posts.filter((p) => p.id !== action.payload);
      })
      .addCase(deletePost.rejected, (state, action) => {
        // action.payload contains the custom error from rejectWithValue
        if (action.payload) {
          const error = action.payload as { message: string; statusCode: number };
          state.error = `${error.message} (${error.statusCode})`;
        } else {
          state.error = action.error.message ?? "Delete failed";
        }
      });
  },
});

export const { clearSelectedPost, clearError } = postSlice.actions;
export default postSlice.reducer;
```

### Handling the Thunk Return Value in Components:

```tsx
// You can await a dispatched thunk and handle its result
const handleDelete = async (postId: number) => {
  try {
    const result = await dispatch(deletePost(postId)).unwrap();
    // .unwrap() throws if rejected, returns payload if fulfilled
    console.log("Deleted post:", result);
    toast.success("Post deleted!");
  } catch (error) {
    // Error from rejectWithValue
    console.error("Delete failed:", error);
    toast.error("Failed to delete post");
  }
};
```

---

## 5. React Integration

```tsx
// components/PostList.tsx
import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { RootState, AppDispatch } from "../store";
import {
  fetchPosts,
  createPost,
  deletePost,
  clearError,
} from "../features/posts/postSlice";

function PostList() {
  const { posts, loading, error } = useSelector(
    (state: RootState) => state.posts
  );
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(fetchPosts());
  }, [dispatch]);

  const handleCreate = async () => {
    try {
      // .unwrap() gives you the fulfilled value or throws the rejected value
      const newPost = await dispatch(
        createPost({ title: "New Post", body: "Content here", userId: 1 })
      ).unwrap();

      console.log("Created:", newPost);
    } catch (error) {
      console.error("Failed:", error);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await dispatch(deletePost(id)).unwrap();
      alert("Deleted!");
    } catch (error) {
      alert("Delete failed!");
    }
  };

  if (loading) return <div>Loading posts...</div>;

  if (error) {
    return (
      <div>
        <p>Error: {error}</p>
        <button onClick={() => dispatch(clearError())}>Dismiss</button>
        <button onClick={() => dispatch(fetchPosts())}>Retry</button>
      </div>
    );
  }

  return (
    <div>
      <button onClick={handleCreate}>Create Post</button>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <h3>{post.title}</h3>
            <p>{post.body}</p>
            <button onClick={() => handleDelete(post.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 6. Next.js Integration

### App Router:

```tsx
// app/posts/page.tsx
"use client";

import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { RootState, AppDispatch } from "@/lib/store";
import { fetchPosts } from "@/lib/features/posts/postSlice";

export default function PostsPage() {
  const { posts, loading } = useSelector((state: RootState) => state.posts);
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(fetchPosts());
  }, [dispatch]);

  if (loading) return <p>Loading...</p>;

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

> **Note:** For data fetching in Next.js, consider **RTK Query** (covered in later chapters) as it provides built-in caching, deduplication, and SSR support.

---

## 7. RTK Query Alternative

For standard API calls, **RTK Query handles all of this automatically**:

```ts
// With RTK Query — no thunks needed!
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

const apiSlice = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: "https://jsonplaceholder.typicode.com" }),
  endpoints: (builder) => ({
    getPosts: builder.query<Post[], void>({
      query: () => "/posts",
      // Loading, error, caching — ALL automatic!
    }),
    deletePost: builder.mutation<void, number>({
      query: (id) => ({ url: `/posts/${id}`, method: "DELETE" }),
    }),
  }),
});
```

---

## 8. Impact

### When to Use createAsyncThunk vs RTK Query:

| Use Case | createAsyncThunk | RTK Query |
|----------|------------------|-----------|
| Simple API calls | Works | Better ✅ |
| Caching needed | Manual | Automatic ✅ |
| Complex business logic | Better ✅ | Not ideal |
| Multiple dispatches per action | Better ✅ | Not designed for this |
| Polling | Manual | Built-in ✅ |
| Optimistic updates | Manual | Built-in ✅ |

### Best Practices:
1. Use `.unwrap()` in components to handle success/error
2. Use `rejectWithValue` for **custom error payloads**
3. Use the `condition` option to **prevent duplicate requests**
4. Use `thunkAPI.signal` for **request cancellation**
5. Prefer RTK Query for standard CRUD operations

---

## 9. Summary

- `createAsyncThunk` auto-generates **pending/fulfilled/rejected** actions
- Return value becomes the `fulfilled` payload; thrown errors become `rejected`
- Handle all three states in `extraReducers` using the **builder pattern**
- Use `.unwrap()` to get a Promise that resolves/rejects for component-level handling
- Use `rejectWithValue()` for **custom error payloads**
- Use the `condition` option to **conditionally cancel** thunks
- `thunkAPI` gives access to `dispatch`, `getState`, `signal`, and more
- For API calls, **RTK Query is usually better** than createAsyncThunk

---

**Prev:** [10_thunks.md](./10_thunks.md) | **Next:** [12_async_state_handling.md](./12_async_state_handling.md)
