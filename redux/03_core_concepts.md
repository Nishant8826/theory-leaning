# Core Concepts — Store, Reducer, Action, Dispatch

---

## 1. What

Redux has **four core building blocks** that work together like a well-oiled machine. Understanding each one is essential before writing any Redux code.

| Concept | What It Is | Analogy |
|---------|-----------|---------|
| **Store** | The single object that holds ALL your app's state | A bank vault |
| **Action** | A plain object describing WHAT happened | A deposit/withdrawal slip |
| **Reducer** | A pure function that decides HOW state changes | The bank teller |
| **Dispatch** | The function that SENDS an action to the reducer | Submitting the slip |

---

## 2. Why

### Why do we need four separate concepts?

Because **separation of concerns** makes everything predictable and debuggable:

- **Actions** = WHAT happened (decoupled from HOW it's handled)
- **Reducers** = HOW state changes (pure logic, no side effects)
- **Store** = WHERE state lives (single source of truth)
- **Dispatch** = HOW to trigger changes (the only way to update state)

This separation means:
- You can **log every action** for debugging
- You can **replay actions** for time-travel debugging
- You can **test reducers** easily (they're just pure functions)
- You can **undo/redo** by replaying actions in reverse

---

## 3. How

### How Each Concept Works:

### 🏦 **Store**

The store is created once and holds the **entire state tree** of your application.

```
Store = {
  auth: { user: null, isAuthenticated: false },
  cart: { items: [], total: 0 },
  theme: { mode: "dark" }
}
```

Key rules:
- There is only **ONE store** per application
- You **cannot modify** the store directly
- The store provides methods: `getState()`, `dispatch()`, `subscribe()`

### 📋 **Action**

An action is a **plain JavaScript object** with a `type` field (and optionally a `payload`).

```ts
// Action without payload
{ type: "INCREMENT" }

// Action with payload
{ type: "ADD_TODO", payload: "Learn Redux" }

// Action with complex payload
{ type: "LOGIN_SUCCESS", payload: { name: "Nishant", email: "nishant@example.com" } }
```

Key rules:
- Must have a `type` property (string)
- Can optionally have a `payload` (any data)
- Must be **plain objects** (no classes, no functions)

### ⚙️ **Reducer**

A reducer is a **pure function** that takes the current state and an action, and returns a **new state**.

```ts
// (currentState, action) → newState
function reducer(state, action) {
  switch (action.type) {
    case "INCREMENT":
      return { ...state, count: state.count + 1 }; // Return NEW object
    default:
      return state; // Always return current state for unknown actions
  }
}
```

Key rules:
- Must be a **pure function** (same inputs → same output, no side effects)
- Must **NEVER mutate** the current state (return a new object)
- Must handle the **default case** (return current state)
- No API calls, no random values, no `Date.now()` inside reducers

### 📤 **Dispatch**

Dispatch is the **only way** to trigger a state change. It sends an action to the store, which passes it to the reducer.

```ts
store.dispatch({ type: "INCREMENT" });
store.dispatch({ type: "ADD_TODO", payload: "Learn Redux" });
```

---

## 4. Implementation

### Complete Example with All Four Concepts:

```ts
// ============================================
// Step 1: Define Types
// ============================================
interface TodoState {
  todos: Array<{
    id: number;
    text: string;
    completed: boolean;
  }>;
  filter: "all" | "completed" | "active";
}

// Action types
type TodoAction =
  | { type: "ADD_TODO"; payload: string }
  | { type: "TOGGLE_TODO"; payload: number }
  | { type: "DELETE_TODO"; payload: number }
  | { type: "SET_FILTER"; payload: "all" | "completed" | "active" };

// ============================================
// Step 2: Define the Reducer (HOW state changes)
// ============================================
const initialState: TodoState = {
  todos: [],
  filter: "all",
};

function todoReducer(
  state: TodoState = initialState,
  action: TodoAction
): TodoState {
  switch (action.type) {
    case "ADD_TODO":
      return {
        ...state, // Copy existing state
        todos: [
          ...state.todos, // Copy existing todos
          {
            id: Date.now(), // Note: This is okay in action creators, not ideal in reducers
            text: action.payload,
            completed: false,
          },
        ],
      };

    case "TOGGLE_TODO":
      return {
        ...state,
        todos: state.todos.map((todo) =>
          todo.id === action.payload
            ? { ...todo, completed: !todo.completed } // Create new todo object
            : todo
        ),
      };

    case "DELETE_TODO":
      return {
        ...state,
        todos: state.todos.filter((todo) => todo.id !== action.payload),
      };

    case "SET_FILTER":
      return {
        ...state,
        filter: action.payload,
      };

    default:
      return state; // ALWAYS return current state for unknown actions
  }
}

// ============================================
// Step 3: Create the Store (WHERE state lives)
// ============================================
import { createStore } from "redux";

const store = createStore(todoReducer);

// ============================================
// Step 4: Dispatch Actions (TRIGGER changes)
// ============================================
console.log("Initial state:", store.getState());
// { todos: [], filter: "all" }

store.dispatch({ type: "ADD_TODO", payload: "Learn Redux" });
console.log("After adding todo:", store.getState());
// { todos: [{ id: ..., text: "Learn Redux", completed: false }], filter: "all" }

store.dispatch({ type: "TOGGLE_TODO", payload: store.getState().todos[0].id });
console.log("After toggling:", store.getState());
// { todos: [{ id: ..., text: "Learn Redux", completed: true }], filter: "all" }

// ============================================
// Step 5: Subscribe to Changes (LISTEN for updates)
// ============================================
const unsubscribe = store.subscribe(() => {
  console.log("State changed:", store.getState());
});

// When done listening:
unsubscribe();
```

### Modern Redux Toolkit Version:

```ts
// todoSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

interface TodoState {
  todos: Todo[];
  filter: "all" | "completed" | "active";
}

const initialState: TodoState = {
  todos: [],
  filter: "all",
};

const todoSlice = createSlice({
  name: "todos",
  initialState,
  reducers: {
    // RTK uses Immer internally — you can "mutate" safely!
    addTodo(state, action: PayloadAction<string>) {
      state.todos.push({
        id: Date.now(),
        text: action.payload,
        completed: false,
      });
    },
    toggleTodo(state, action: PayloadAction<number>) {
      const todo = state.todos.find((t) => t.id === action.payload);
      if (todo) {
        todo.completed = !todo.completed; // Direct "mutation" — safe with Immer!
      }
    },
    deleteTodo(state, action: PayloadAction<number>) {
      state.todos = state.todos.filter((t) => t.id !== action.payload);
    },
    setFilter(state, action: PayloadAction<"all" | "completed" | "active">) {
      state.filter = action.payload;
    },
  },
});

// Actions are auto-generated!
export const { addTodo, toggleTodo, deleteTodo, setFilter } = todoSlice.actions;

// Reducer is auto-generated!
export default todoSlice.reducer;
```

```ts
// store.ts
import { configureStore } from "@reduxjs/toolkit";
import todoReducer from "./todoSlice";

const store = configureStore({
  reducer: {
    todos: todoReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
```

---

## 5. React Integration

```tsx
// TodoApp.tsx
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "./store";
import { addTodo, toggleTodo, deleteTodo, setFilter } from "./todoSlice";
import { useState } from "react";

function TodoApp() {
  const [input, setInput] = useState("");
  const todos = useSelector((state: RootState) => state.todos.todos);
  const filter = useSelector((state: RootState) => state.todos.filter);
  const dispatch = useDispatch();

  const filteredTodos = todos.filter((todo) => {
    if (filter === "completed") return todo.completed;
    if (filter === "active") return !todo.completed;
    return true;
  });

  const handleAdd = () => {
    if (input.trim()) {
      dispatch(addTodo(input.trim())); // Dispatch the action
      setInput("");
    }
  };

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleAdd()}
        placeholder="Add a todo..."
      />
      <button onClick={handleAdd}>Add</button>

      <div>
        <button onClick={() => dispatch(setFilter("all"))}>All</button>
        <button onClick={() => dispatch(setFilter("active"))}>Active</button>
        <button onClick={() => dispatch(setFilter("completed"))}>Done</button>
      </div>

      <ul>
        {filteredTodos.map((todo) => (
          <li key={todo.id}>
            <span
              onClick={() => dispatch(toggleTodo(todo.id))}
              style={{
                textDecoration: todo.completed ? "line-through" : "none",
                cursor: "pointer",
              }}
            >
              {todo.text}
            </span>
            <button onClick={() => dispatch(deleteTodo(todo.id))}>❌</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TodoApp;
```

---

## 6. Next.js Integration

Works the same as file 01 — wrap with `Provider` in layout (App Router) or `_app.tsx` (Pages Router).

The core concepts (Store, Action, Reducer, Dispatch) are **framework-agnostic** — they work identically in React, Next.js, or any other framework.

---

## 7. Impact

### Real-World Benefits:
- **Predictability** — you always know what state looks like and why it changed
- **Testability** — reducers are pure functions, trivially easy to test
- **Debugging** — Redux DevTools show every action and state snapshot
- **Collaboration** — clear mental model helps teams reason about state

### Testing a Reducer:
```ts
// todoSlice.test.ts
import todoReducer, { addTodo, toggleTodo } from "./todoSlice";

describe("todoReducer", () => {
  it("should add a todo", () => {
    const initialState = { todos: [], filter: "all" as const };
    const newState = todoReducer(initialState, addTodo("Test"));

    expect(newState.todos).toHaveLength(1);
    expect(newState.todos[0].text).toBe("Test");
    expect(newState.todos[0].completed).toBe(false);
  });
});
```

---

## 8. Summary

- **Store** = single object holding all state (the vault)
- **Action** = plain object describing what happened (`{ type, payload }`)
- **Reducer** = pure function that computes new state from `(state, action)`
- **Dispatch** = the function that sends actions to the store
- **Flow:** `dispatch(action)` → `reducer(state, action)` → `newState` → UI updates
- Redux Toolkit (`createSlice`) auto-generates actions and lets you write "mutating" reducers safely via Immer
- Reducers must be **pure** — no side effects, no API calls, no randomness

---

**Prev:** [02_why_redux.md](./02_why_redux.md) | **Next:** [04_data_flow.md](./04_data_flow.md)
