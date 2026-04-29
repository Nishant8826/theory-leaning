# 📌 08 — State Management Patterns

## 🌟 Introduction

As your app grows from 1 page to 100 pages, keeping track of data (like "Is the user logged in?" or "What’s in the shopping cart?") becomes very difficult. This data is called **State**.

**State Management** is the system for how your app remembers things.

Think of it like a **Bank**:
-   **The Vault (The Store):** There is only one central place where the money (State) is kept.
-   **The Clerk (The Action):** You don't just walk into the vault. You talk to a clerk and say, "I want to deposit $10."
-   **The Ledger (The Reducer):** The clerk writes the change in a book. The money is never "deleted," only "updated."

---

## 🏗️ The 2 Main Styles

1.  **Redux Style (Unidirectional):** Very strict. Data only moves in one direction. It’s like a one-way street. It is great for large, complex apps where you need to track every single change.
2.  **MobX/Vue Style (Reactive):** Very flexible. You just change a variable, and the UI "reacts" and updates itself. It’s like a spreadsheet.

---

## 🏗️ The Redux Flow (The Loop)

1.  **Action:** A message describing what happened. `{ type: 'ADD_ITEM', item: 'Laptop' }`
2.  **Reducer:** A function that takes the old state + the action, and returns the **NEW** state.
3.  **Store:** The object that holds the state and notifies the UI.

---

## 🔍 Code Walkthrough: Redux from Scratch

```javascript
function createStore(reducer, initialState) {
  let state = initialState;
  const listeners = [];

  const getState = () => state;

  const subscribe = (fn) => listeners.push(fn);

  const dispatch = (action) => {
    state = reducer(state, action); // Calculate new state
    listeners.forEach(fn => fn()); // Tell everyone the state changed
  };

  return { getState, subscribe, dispatch };
}

// A simple Reducer
const counterReducer = (state, action) => {
  if (action.type === 'INC') return { count: state.count + 1 };
  return state;
};

const store = createStore(counterReducer, { count: 0 });

store.subscribe(() => console.log("State updated!", store.getState()));
store.dispatch({ type: 'INC' }); // State updated! { count: 1 }
```

---

## 🚀 Why Use a Central Store?

1.  **Single Source of Truth:** You don't have to worry about the header saying "3 items" while the cart says "2 items."
2.  **Predictability:** Because state can only change through "Actions," you always know exactly **why** the data changed.
3.  **Time Travel Debugging:** You can record every action and "play them back" to see exactly how a bug happened.

---

## 📐 Visualizing the Redux Loop

```text
    [ UI ] ────(Click)───▶ [ ACTION ]
      ▲                       │
      │                       ▼
    [ STORE ] ◀──(New State)── [ REDUCER ]
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Immutability & Memory
In Redux, we never "mutate" state (e.g., `state.count = 5`). We always return a **new object**. You might think this is slow, but modern V8 engines are optimized for this. When you create a new object that is 90% the same as the old one, V8 uses **"Structural Sharing"** or optimized allocation to ensure you don't waste memory. This also makes the "Equality Check" (`oldState === newState`) extremely fast, as it only compares the memory address.

---

## 💼 Interview Questions

**Q1: Why does Redux need "Pure Functions" for Reducers?**
> **Ans:** A pure function always gives the same output for the same input and has no side effects. This makes the app predictable. If a reducer changed a global variable or made an API call, you could never "Time Travel" or undo actions correctly.

**Q2: What is the difference between local state and global state?**
> **Ans:** Local state (like "Is this dropdown open?") should stay inside the component. Global state (like "User Profile") should go into the central Store because many components need to see it.

**Q3: What are "Selectors" in state management?**
> **Ans:** Selectors are functions that "select" or "calculate" a piece of data from the store (e.g., `getCartTotal(state)`). They help keep your components clean by moving the math out of the UI.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Redux** | Very predictable; great tools. | Lots of "Boilerplate" code (Actions, Types, Reducers). |
| **Zustand / Jotai** | Minimal code; easy to learn. | Fewer advanced tools for massive apps. |
| **Context API** | Built into React; no libraries. | Can cause performance issues if not used carefully. |

---

## 🔗 Navigation

**Prev:** [07_Reactive_Patterns.md](07_Reactive_Patterns.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [../Performance/01_Code_Optimization.md](../Performance/01_Code_Optimization.md)
