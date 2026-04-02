# createSlice

---

## 1. What

`createSlice` is the **most important function in Redux Toolkit**. It creates a "slice" of your Redux state — meaning it generates the **reducer**, **action creators**, and **action types** all in one call.

### Before createSlice (3 separate things):
```
1. Action Types:   const INCREMENT = "counter/INCREMENT"
2. Action Creators: function increment() { return { type: INCREMENT } }
3. Reducer:        function counterReducer(state, action) { switch... }
```

### With createSlice (ONE thing):
```ts
const counterSlice = createSlice({
  name: "counter",
  initialState: { count: 0 },
  reducers: {
    increment(state) { state.count += 1; }
    // ☝️ This creates the action type, action creator, AND reducer case!
  }
});
```

---

## 2. Why

### Problems createSlice Solves:

**1. No more string constants:**
```ts
// ❌ Legacy — typos cause silent bugs!
const ICREMENT = "counter/ICREMENT"; // Typo! No error, just broken.

// ✅ createSlice — action types are auto-generated
counterSlice.actions.increment.type; // "counter/increment" — always correct
```

**2. No more manual immutability:**
```ts
// ❌ Legacy — deeply nested updates are painful
return {
  ...state,
  users: {
    ...state.users,
    [userId]: {
      ...state.users[userId],
      address: {
        ...state.users[userId].address,
        city: newCity // 😩 Four levels of spreading!
      }
    }
  }
};

// ✅ createSlice + Immer — just mutate!
state.users[userId].address.city = newCity; // 🎉 One line!
```

**3. No more action creator functions:**
```ts
// ❌ Legacy — write these manually for every action
function addTodo(text: string) {
  return { type: "ADD_TODO", payload: text };
}

// ✅ createSlice — auto-generated!
export const { addTodo } = todoSlice.actions;
// addTodo("Learn Redux") → { type: "todos/addTodo", payload: "Learn Redux" }
```

---

## 3. How

### How createSlice Works Internally:

```
createSlice({
  name: "todos",                    ← Used as prefix for action types
  initialState: { items: [] },      ← Starting state
  reducers: {                       ← Each key = one action + reducer case
    addTodo(state, action) {        ← Function name = action type suffix
      state.items.push(action.payload);
    }
  }
})
```

**What it produces:**

```ts
// 1. Action type: "todos/addTodo"
// 2. Action creator: (payload) => ({ type: "todos/addTodo", payload })
// 3. Reducer function that handles "todos/addTodo"
```

### The name Property:
```ts
name: "todos"
// This means ALL action types from this slice start with "todos/"
// "todos/addTodo", "todos/deleteTodo", "todos/toggleTodo"
```

---

## 4. Implementation

### Basic createSlice:

```ts
// features/todos/todoSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

// Step 1: Define the state type
interface Todo {
  id: string;
  text: string;
  completed: boolean;
  priority: "low" | "medium" | "high";
  createdAt: string;
}

interface TodoState {
  items: Todo[];
  filter: "all" | "active" | "completed";
  searchQuery: string;
}

// Step 2: Define initial state
const initialState: TodoState = {
  items: [],
  filter: "all",
  searchQuery: "",
};

// Step 3: Create the slice
const todoSlice = createSlice({
  name: "todos", // Prefix for all action types

  initialState,

  reducers: {
    // ─────────────────────────────────────────────
    // Simple action — no payload needed
    // ─────────────────────────────────────────────
    clearAll(state) {
      state.items = [];
    },

    // ─────────────────────────────────────────────
    // Action with payload
    // ─────────────────────────────────────────────
    addTodo(state, action: PayloadAction<{ text: string; priority: Todo["priority"] }>) {
      state.items.push({
        id: crypto.randomUUID(),
        text: action.payload.text,
        completed: false,
        priority: action.payload.priority,
        createdAt: new Date().toISOString(),
      });
    },

    // ─────────────────────────────────────────────
    // Toggle a boolean value
    // ─────────────────────────────────────────────
    toggleTodo(state, action: PayloadAction<string>) {
      const todo = state.items.find((t) => t.id === action.payload);
      if (todo) {
        todo.completed = !todo.completed; // Direct mutation — safe with Immer!
      }
    },

    // ─────────────────────────────────────────────
    // Delete an item
    // ─────────────────────────────────────────────
    deleteTodo(state, action: PayloadAction<string>) {
      state.items = state.items.filter((t) => t.id !== action.payload);
    },

    // ─────────────────────────────────────────────
    // Update a specific field
    // ─────────────────────────────────────────────
    updateTodoText(
      state,
      action: PayloadAction<{ id: string; text: string }>
    ) {
      const todo = state.items.find((t) => t.id === action.payload.id);
      if (todo) {
        todo.text = action.payload.text;
      }
    },

    // ─────────────────────────────────────────────
    // Set a filter value
    // ─────────────────────────────────────────────
    setFilter(state, action: PayloadAction<TodoState["filter"]>) {
      state.filter = action.payload;
    },

    // ─────────────────────────────────────────────
    // Set search query
    // ─────────────────────────────────────────────
    setSearchQuery(state, action: PayloadAction<string>) {
      state.searchQuery = action.payload;
    },

    // ─────────────────────────────────────────────
    // Reorder items
    // ─────────────────────────────────────────────
    reorderTodos(
      state,
      action: PayloadAction<{ fromIndex: number; toIndex: number }>
    ) {
      const { fromIndex, toIndex } = action.payload;
      const [movedItem] = state.items.splice(fromIndex, 1);
      state.items.splice(toIndex, 0, movedItem);
    },
  },
});

// Step 4: Export actions (auto-generated!)
export const {
  clearAll,
  addTodo,
  toggleTodo,
  deleteTodo,
  updateTodoText,
  setFilter,
  setSearchQuery,
  reorderTodos,
} = todoSlice.actions;

// Step 5: Export reducer
export default todoSlice.reducer;

// Step 6: Export selectors (optional but recommended)
export const selectAllTodos = (state: { todos: TodoState }) =>
  state.todos.items;

export const selectFilteredTodos = (state: { todos: TodoState }) => {
  const { items, filter, searchQuery } = state.todos;

  let filtered = items;

  // Apply filter
  if (filter === "active") filtered = filtered.filter((t) => !t.completed);
  if (filter === "completed") filtered = filtered.filter((t) => t.completed);

  // Apply search
  if (searchQuery) {
    filtered = filtered.filter((t) =>
      t.text.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }

  return filtered;
};
```

### createSlice with Prepare Callback:

Sometimes you need to customize how the action payload is created:

```ts
const todoSlice = createSlice({
  name: "todos",
  initialState: { items: [] as Todo[] },
  reducers: {
    // Using "prepare" to customize the action creator
    addTodo: {
      // The reducer — handles the state change
      reducer(state, action: PayloadAction<Todo>) {
        state.items.push(action.payload);
      },
      // The prepare callback — customizes the action payload
      prepare(text: string, priority: Todo["priority"] = "medium") {
        return {
          payload: {
            id: crypto.randomUUID(),
            text,
            completed: false,
            priority,
            createdAt: new Date().toISOString(),
          },
        };
      },
    },
  },
});

// Now you can call it with simpler arguments:
dispatch(addTodo("Learn Redux", "high"));
// Instead of passing the full object
```

### createSlice with extraReducers:

Handle actions from OTHER slices or from `createAsyncThunk`:

```ts
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

// Async thunk (covered in detail later)
export const fetchTodos = createAsyncThunk("todos/fetch", async () => {
  const response = await fetch("/api/todos");
  return response.json();
});

const todoSlice = createSlice({
  name: "todos",
  initialState: {
    items: [] as Todo[],
    loading: false,
    error: null as string | null,
  },
  reducers: {
    // Your regular reducers...
    addTodo(state, action: PayloadAction<string>) {
      state.items.push({
        id: crypto.randomUUID(),
        text: action.payload,
        completed: false,
        priority: "medium",
        createdAt: new Date().toISOString(),
      });
    },
  },
  // Handle actions defined OUTSIDE this slice
  extraReducers: (builder) => {
    builder
      .addCase(fetchTodos.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTodos.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchTodos.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Failed to fetch";
      });
  },
});
```

---

## 5. React Integration

```tsx
// TodoApp.tsx
import { useSelector, useDispatch } from "react-redux";
import { RootState, AppDispatch } from "./store";
import {
  addTodo,
  toggleTodo,
  deleteTodo,
  setFilter,
  setSearchQuery,
  selectFilteredTodos,
} from "./features/todos/todoSlice";
import { useState } from "react";

function TodoApp() {
  const [input, setInput] = useState("");
  const filteredTodos = useSelector(selectFilteredTodos);
  const filter = useSelector((state: RootState) => state.todos.filter);
  const dispatch = useDispatch<AppDispatch>();

  const handleAdd = () => {
    if (input.trim()) {
      dispatch(addTodo({ text: input.trim(), priority: "medium" }));
      setInput("");
    }
  };

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="What needs to be done?"
      />
      <button onClick={handleAdd}>Add</button>

      <input
        placeholder="Search todos..."
        onChange={(e) => dispatch(setSearchQuery(e.target.value))}
      />

      <div>
        {(["all", "active", "completed"] as const).map((f) => (
          <button
            key={f}
            onClick={() => dispatch(setFilter(f))}
            style={{ fontWeight: filter === f ? "bold" : "normal" }}
          >
            {f}
          </button>
        ))}
      </div>

      <ul>
        {filteredTodos.map((todo) => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => dispatch(toggleTodo(todo.id))}
            />
            <span
              style={{
                textDecoration: todo.completed ? "line-through" : "none",
              }}
            >
              {todo.text} [{todo.priority}]
            </span>
            <button onClick={() => dispatch(deleteTodo(todo.id))}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## 6. Next.js Integration

`createSlice` works **identically** in Next.js. The slice definition doesn't change — only the store setup differs (covered in `06_configure_store.md`).

```tsx
// app/todos/page.tsx
"use client";

import { useSelector, useDispatch } from "react-redux";
import { addTodo, selectFilteredTodos } from "@/lib/features/todos/todoSlice";
// ... same React code as above
```

---

## 7. Impact

### createSlice is the Heart of RTK:
- **Every feature** in your app starts with a slice
- It enforces **good patterns** automatically (Immer, action naming, type safety)
- It's the foundation for **scalable architecture** (feature-based folders)

### Best Practices:
1. **One slice per feature** — `authSlice`, `cartSlice`, `todoSlice`
2. **Co-locate selectors** — define selectors in the same file as the slice
3. **Use PayloadAction** — for type-safe action payloads
4. **Use prepare callbacks** — when you need to compute payload values (like IDs)
5. **Use extraReducers** — for handling actions from thunks or other slices

---

## 8. Summary

- `createSlice` creates **reducer + action creators + action types** in one call
- The `name` property is used as a prefix for action types
- **Immer** is built in — you can "mutate" state directly
- `PayloadAction<T>` provides type-safe payloads
- Use **prepare callbacks** to customize action creation
- Use **extraReducers** (with `builder`) to handle external actions (thunks, other slices)
- Export **actions**, **reducer**, and **selectors** from the slice file
- One slice per feature is the recommended pattern

---

**Prev:** [06_configure_store.md](./06_configure_store.md) | **Next:** [08_create_action_and_create_reducer.md](./08_create_action_and_create_reducer.md)
