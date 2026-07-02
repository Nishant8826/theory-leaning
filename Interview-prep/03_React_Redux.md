# 🚀 Interview Preparation - React & Redux

> **Domain:** Web Development / Frontend  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / Lead

---

## 🟢 Beginner Level

### ❓ Q1. **What is React and why is it used?**
<details>
<summary><b>👀 Show Answer</b></summary>

React is a declarative, efficient, and flexible JavaScript library for building user interfaces. It lets you compose complex UIs from small and isolated pieces of code called "components".

**Why use it:**
- **Component-Based:** Code reusability and maintainability.
- **Virtual DOM:** High performance by minimizing real DOM manipulation.
- **Declarative UI:** Easier to reason about state changes.

**🏢 Industry Example:**  
When migrating a legacy monolithic application (like a massive e-commerce dashboard originally in jQuery) to React, engineers often break down the UI into isolated components (e.g., `ProductCard`, `CartWidget`). This allows multiple teams to work concurrently on different features without stepping on each other's toes, drastically reducing time-to-market for new features.

> 💡 **Interviewer Focus:** Look for understanding of component architecture and the problem React solves (efficient UI updates).
</details>
<hr/>

### ❓ Q2. **What is JSX?**
<details>
<summary><b>👀 Show Answer</b></summary>

JSX stands for JavaScript XML. It is a syntax extension for JavaScript that allows you to write HTML-like code inside JavaScript. It is transpiled (usually by Babel) into standard `React.createElement()` calls.

> 💡 **Interviewer Focus:** Ensure they know it's not actually HTML and needs compilation.
</details>
<hr/>

### ❓ Q3. **What is the difference between State and Props?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Props** (Properties) are read-only components passed from a parent component to a child component. They are immutable within the child.
- **State** is a local data storage that is local to the component and can be mutated by the component itself (using `useState` or `setState`). State changes trigger re-rendering.

> 💡 **Interviewer Focus:** This is fundamental. Props are external/read-only, State is internal/mutable.
</details>
<hr/>

### ❓ Q4. **What are React Hooks?**
<details>
<summary><b>👀 Show Answer</b></summary>

Hooks are built-in functions introduced in React 16.8 that allow functional components to hook into React's state management and lifecycle systems.

**Problems Hooks Solved (Why do they exist?):**
1. **No more "Class" confusion:** Learning React class components was hard because developers had to constantly deal with the confusing `this` keyword and bind events manually.
2. **Easy code sharing:** Before Hooks, sharing common logic between components required complicated, nested patterns (Render Props and Higher-Order Components). Hooks allow you to package custom logic into standard functions.
3. **Organized code:** In class components, code for a single feature (like fetching data and cleaning up timers) had to be split across different lifecycle methods (`componentDidMount`, `componentWillUnmount`). Hooks let you group related logic together.

**Most Common Hooks to Know:**
- `useState`: Lets a component "remember" and update data (local state).
- `useEffect`: Lets a component run side effects, like fetching data from an API or setting timers.
- `useRef`: Lets you reference DOM elements directly or store variables that don't trigger a re-render when they change.
- `useContext`: Makes it easy to share global data (like themes or user logins) across many components.

**The Two Golden Rules of Hooks:**
1. **Only call Hooks at the top level:** Do not put Hooks inside loops, conditions (`if` statements), or nested functions. This ensures React always calls them in the exact same order on every render.
2. **Only call Hooks from React functions:** You can only call Hooks from React function components or your own custom Hooks, not from standard JavaScript functions.

> 💡 **Interviewer Focus:** Show that you understand *why* Hooks were created (to replace class components, eliminate the confusing `this` keyword, simplify state sharing, and avoid "wrapper hell"). Mentioning the Rules of Hooks shows you have practical coding experience.
</details>
<hr/>

### ❓ Q5. **Explain the `useState` hook.**
<details>
<summary><b>👀 Show Answer</b></summary>

`useState` hook is a built-in react hook used to add state to functional components. It returns a pair: the current state value and a function that lets you update it.
```javascript
const [count, setCount] = useState(0);
```

> 💡 **Interviewer Focus:** Check if they understand array destructuring used in the syntax and that the setter function replaces the state (it doesn't merge for objects like `setState` in classes).
</details>
<hr/>

### ❓ Q6. **What is the Virtual DOM?**
<details>
<summary><b>👀 Show Answer</b></summary>

The Virtual DOM is a lightweight copy of the real DOM in memory. When state changes, React creates a new Virtual DOM and compares it with the previous one (Diffing). It then updates only the changed parts in the real DOM (Reconciliation).

> 💡 **Interviewer Focus:** Look for keywords like "Diffing", "Reconciliation", and "Performance".
</details>
<hr/>

### ❓ Q7. **Why do we need `keys` in React lists?**
<details>
<summary><b>👀 Show Answer</b></summary>

Keys help React identify which items have changed, are added, or are removed. They should be given to the elements inside the array to give the elements a stable identity, which improves performance during the diffing process.

> 💡 **Interviewer Focus:** Warn against using array indices as keys for dynamic lists.
</details>
<hr/>

### ❓ Q8. **What is the difference between controlled and uncontrolled components?**
<details>
<summary><b>👀 Show Answer</b></summary>

The difference lies in **how the data/state of form elements (like inputs) is managed**.

**1. Controlled Components**
In a controlled component, the form data is handled by a **React component**. The current value of the input is driven by React state, and changes are handled via callback functions.
- **Source of Truth:** React State.
- **How it works:** You bind the `value` prop to a state variable and update it via `onChange`.
- **Code Example:**
```javascript
const [name, setName] = useState('');
<input type="text" value={name} onChange={(e) => setName(e.target.value)} />
```

**2. Uncontrolled Components**
In an uncontrolled component, the form data is handled by the **DOM itself**. You pull the values from the DOM when you need them, usually on form submission.
- **Source of Truth:** The DOM.
- **How it works:** You use a `ref` (via `useRef`) to access the DOM element directly.
- **Code Example:**
```javascript
const inputRef = useRef(null);
const handleSubmit = () => {
  console.log(inputRef.current.value);
};
<input type="text" ref={inputRef} />
```

**Key Differences at a Glance:**

| Feature | Controlled | Uncontrolled |
| :--- | :--- | :--- |
| **Source of Truth** | React State | DOM |
| **Value Access** | Available on every keystroke | Available only when pulled (e.g., submit) |
| **Performance** | Can cause more re-renders | Better for large forms (less re-renders) |
| **Validation** | Easy to validate on the fly | Harder to validate instantly |

**When to use which?**
- Use **Controlled** for: Instant field validation, disabling submit buttons based on valid input, enforcing specific input formats (like credit cards), and dynamic inputs.
- Use **Uncontrolled** for: Simple forms where you only need the value on submit, non-interactive UI elements, or when integrating with non-React libraries.

**🏢 Industry Example:**  
In a real-world **FinTech application (e.g., Stripe checkout)**, a credit card input is always **Controlled**. You need to validate the card length, format the string with spaces, and detect the card type (Visa/Mastercard) *on every keystroke*. Conversely, if you are building an admin dashboard and integrating a legacy drag-and-drop file uploader library, you'd use an **Uncontrolled** approach using refs.

> 💡 **Interviewer Focus:** Controlled components are the recommended approach in React for most use cases because they give you full control over the data flow.
</details>
<hr/>

### ❓ Q9. **What is Redux?**
<details>
<summary><b>👀 Show Answer</b></summary>

Redux is a **predictable state container** for JavaScript apps. It helps you manage global state (data shared across many parts of your app) in a centralized and predictable way.

**Why use Redux?**
1. **Centralized State:** Instead of passing props down multiple levels (prop drilling) or spreading state across many components, Redux keeps all application state in a single, centralized location called the **Store**.
2. **Predictability:** State is read-only. The only way to change it is by dispatching an **Action** (an object describing what happened). This makes the state predictable and traceable.
3. **Debugging:** Redux DevTools allow you to see when, where, and why your state changed. You can even do "time-travel debugging" (stepping back and forth through state changes).
4. **Consistency:** It ensures that your app behaves consistently across client, server, and native environments.

**Key Concepts:**
- **Store:** The single source of truth that holds the state.
- **Action:** A plain JavaScript object that describes *what* happened (e.g., `{ type: 'ADD_TODO', payload: 'Learn Redux' }`).
- **Reducer:** A pure function that takes the current state and an action, and returns the *new* state.


> 💡 **Interviewer Focus:** Emphasize keywords like **Predictable**, **Centralized Store**, **Actions**, and **Reducers**. Mention that it is library-agnostic but most commonly used with React.
</details>
<hr/>

### ❓ Q10. **What are the core principles of Redux?**
<details>
<summary><b>👀 Show Answer</b></summary>

Redux is built on three core principles:

1. **Single Source of Truth:**
   - The state of your whole application is stored in an object tree within a single **store**.
   - **Why it matters:** This makes it easy to inspect the app state, persist it (e.g., to local storage), and share data between components without prop drilling.

2. **State is Read-Only:**
   - The only way to change the state is to emit (dispatch) an **action**, an object describing what happened.
   - **Why it matters:** This ensures that views or network callbacks cannot mutate the state directly. All changes are centralized and happen one by one in a strict order.

3. **Changes are made with Pure Functions (Reducers):**
   - To specify how the state tree is transformed by actions, you write pure functions called **reducers**.
   - **Why it matters:** Reducers take the current state and an action, and return a *new* state object (they do not mutate the original state). Because they are pure functions, they are predictable and easy to test.

> 💡 **Interviewer Focus:** This is a fundamental Redux question. You must list all three principles. Emphasize that state immutability and pure functions are key to Redux's predictability.
</details>
<hr/>

## 🟡 Intermediate Level

### ❓ Q11. **Explain the `useEffect` hook and its dependency array.**
<details>
<summary><b>👀 Show Answer</b></summary>

`useEffect` is a React hook used to handle side effects in functional components.  It serves the purpose of lifecycle methods like `componentDidMount`, `componentDidUpdate`, and `componentWillUnmount`.

- **No array:** Runs on every render.
- **Empty array `[]`:** Runs once on mount.
- **Array with values `[dep1, dep2]`:** Runs on mount and when dependencies change.

> 💡 **Interviewer Focus:** Deep understanding of the dependency array and cleanup functions.
</details>
<hr/>

### ❓ Q12. **How does React's Reconciliation work?**
<details>
<summary><b>👀 Show Answer</b></summary>

Reconciliation is React's way of updating the browser screen quickly and efficiently. 

**The "Spot the Difference" Analogy:**
Think of it like playing a game of **Spot the Difference** between two drawings. Instead of erasing the entire canvas and drawing everything from scratch (which is slow and takes a lot of effort), React compares the old drawing with the new drawing, finds the exact spots that changed, and only updates those parts on the real screen.
- **Diffing:** The process of comparing the new UI layout (Virtual DOM) with the old one to find differences.
- **Reconciliation:** The process of applying only those differences to the real browser screen (Real DOM).

To keep this comparison incredibly fast, React uses two main shortcut rules (heuristics):

1. **If the element type changes, rebuild from scratch:** If an element changes type (e.g., changing from a `<div>` container to a `<span>` text tag), React assumes the entire section is completely different. It tears down the old element and its children and builds a new one from scratch.
2. **If elements have name tags (keys), reuse them:** In lists, React uses the `key` prop as a unique name tag for each item. If you rearrange the list, React uses these keys to simply move the existing elements around instead of deleting and rebuilding them.

**How React Decides to Update (The Diffing Rules):**
- **Different HTML Tags (e.g., `<a>` to `<img>`):** React destroys the old element and builds the new one.
- **Same HTML Tags (e.g., `<div class="old">` to `<div class="new">`):** React keeps the element on the screen and only changes the updated attributes (like the class name or style).
- **Same React Components:** React keeps the component instance alive, updates its inputs (props), and triggers a clean re-render.

> 💡 **Interviewer Focus:** Show that you understand the performance benefit of this process. Mention that standard tree comparison is slow ($O(n^3)$), but React's shortcut rules make it extremely fast ($O(n)$). Highlighting terms like **Diffing**, **Reconciliation**, and **Keys** is key.
</details>
<hr/>

### ❓ Q13. **What is the Context API and when should you use it?**
<details>
<summary><b>👀 Show Answer</b></summary>

Context provides a way to pass data through the component tree without having to pass props down manually at every level (Prop Drilling). Use it for data that can be considered "global" for a tree of React components, such as the current authenticated user, theme, or preferred language.

**🏢 Industry Example:**  
In a **Multi-tenant SaaS Platform (like Slack or Jira)**, users can select a "Dark Mode" theme or their preferred language (i18n). Passing `theme` or `language` as props through 20 levels of components is a nightmare. Wrapping the app in a `<ThemeProvider>` and `<LocaleProvider>` using Context API allows deep components (like a tiny `Button` deep in a settings modal) to instantly know if they should render dark backgrounds or Spanish text.

> 💡 **Interviewer Focus:** Use Context for low-frequency updates (theme, locale) to avoid performance issues with frequent re-renders.
</details>
<hr/>

### ❓ Q14. **What is the difference between `useMemo` and `useCallback`?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
Both hooks are used for performance optimization in React by caching values between renders, but they serve different purposes:
*   **`useMemo`** caches the **result of a calculation** (a value).
*   **`useCallback`** caches the **function definition itself** (a function reference).

In fact, `useCallback(fn, deps)` is just syntactic sugar for `useMemo(() => fn, deps)`.

---

### 1. `useMemo` (Caching Values)
Used to avoid running expensive CPU-heavy computations on every single render.

#### **Code Example:**
```javascript
import { useMemo } from 'react';

function ProductList({ products, filterTerm }) {
  // Expensive calculation: filtering and sorting thousands of items
  const filteredProducts = useMemo(() => {
    console.log("Filtering products..."); // Only logs when products or filterTerm changes
    return products
      .filter(p => p.name.includes(filterTerm))
      .sort((a, b) => a.price - b.price);
  }, [products, filterTerm]); // Recalculates only when these change

  return (
    <ul>
      {filteredProducts.map(p => <li key={p.id}>{p.name} - ${p.price}</li>)}
    </ul>
  );
}
```

---

### 2. `useCallback` (Caching Function References)
Used to maintain **reference equality** of callback functions passed down as props to optimized child components.

#### **The Reference Problem in React:**
In JavaScript, functions are objects, and objects are compared by reference. In React, a function defined inside a component is recreated on every render:
```javascript
const handleSave = () => { ... }; // New function instance on every single render!
```
If you pass `handleSave` as a prop to a child component, the child will re-render on every parent render—**even if** the child is wrapped in `React.memo`—because the function reference changed. `useCallback` preserves the reference.

#### **Code Example:**
```javascript
import { useState, useCallback, memo } from 'react';

// Optimized Child Component
const HeavyButton = memo(({ onClick, label }) => {
  console.log(`Rendering button: ${label}`); // Only renders once, doesn't re-render on parent changes
  return <button onClick={onClick}>{label}</button>;
});

function ParentComponent() {
  const [count, setCount] = useState(0);

  // useCallback keeps the exact same function reference between renders
  const handleClick = useCallback(() => {
    console.log("Button clicked!");
  }, []); // Empty dependencies = function reference never changes

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment Count</button>
      
      {/* HeavyButton will NOT re-render when count updates */}
      <HeavyButton onClick={handleClick} label="Submit Form" />
    </div>
  );
}
```

---

### 📊 Comparison at a Glance

| Feature | `useMemo` | `useCallback` |
| :--- | :--- | :--- |
| **What it caches** | The **value returned** by a function. | The **function instance** itself. |
| **What it returns** | Whatever the callback computes (objects, arrays, strings). | The exact callback function passed in. |
| **Primary Use Case** | Skipping expensive, heavy recalculations. | Maintaining reference equality for props passed to `React.memo` children. |
| **Syntax** | `useMemo(() => value, [deps])` | `useCallback(() => { ... }, [deps])` |

---

### ⚠️ Common Interviewer Trap: Over-Optimization
**"Should we wrap every function and value in `useCallback`/`useMemo`?"**
*   **No.** Caching has an overhead cost. React must allocate memory to store the previous values/functions and run a dependency array reference comparison (`===`) on every single render.
*   Wrapping a cheap calculation (like `1 + 1` or a simple click event handler on a standard `<button>`) makes your application **slower** due to this overhead.
*   **Only use them when:**
    1.  Performing heavy, complex calculations (e.g. loops, filters, data parses).
    2.  Passing callback functions to child components wrapped in `React.memo`.
    3.  A function or value is used as a dependency in another hook (like `useEffect`).

</details>
<hr/>

### ❓ Q15. **What are Custom Hooks and why would you use them?**
<details>
<summary><b>👀 Show Answer</b></summary>

Custom Hooks are JavaScript functions whose names start with "use" and that may call other Hooks. They allow you to extract component logic into reusable functions.
**Why:** To share logic between components without adding more components to your tree (unlike HOCs or render props).

**Industry-Based Example (`useDebounce`):**
In real-world applications (like an e-commerce search bar), making an API call on every keystroke can overload the server and degrade performance. We can create a custom `useDebounce` hook to delay the API call until the user has stopped typing.

```javascript
import { useState, useEffect } from 'react';

function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    // Update debounced value after delay
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cancel the timeout if value changes (also on delay change or unmount)
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Usage in a Search component:
// const debouncedSearchTerm = useDebounce(searchTerm, 500);
// useEffect(() => {
//   if (debouncedSearchTerm) {
//     fetchResults(debouncedSearchTerm);
//   }
// }, [debouncedSearchTerm]);
```

> 💡 **Interviewer Focus:** Sharing stateful logic, not state itself. Be prepared to explain an example like `useAuth`, or `useDebounce`.
</details>
<hr/>

### ❓ Q16. **How do you handle error boundaries in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

Error boundaries are special React components that act like a `try...catch` block for UI components. If a component deep in your application crashes (e.g., due to a broken API response or undefined state), the Error Boundary catches the crash, logs the error, and displays a fallback UI (like "Something went wrong") instead of letting the entire page go blank.

**How to Implement Them:**
Currently, Error Boundaries **must be written as Class Components** because they rely on lifecycle methods that do not have functional/Hook equivalents yet.

A class component becomes an Error Boundary when it implements one or both of these methods:
1. `static getDerivedStateFromError(error)`: Used to update state (e.g., `hasError: true`) so the next render shows the fallback UI.
2. `componentDidCatch(error, errorInfo)`: Used to log error information to an external monitoring service (like Sentry or LogRocket).

**Simple Code Example:**
```javascript
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  // 1. Update state so next render shows fallback UI
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  // 2. Log the error to a service
  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h2>Oops, something went wrong. Please refresh.</h2>;
    }
    return this.props.children;
  }
}

// Usage:
// <ErrorBoundary>
//   <MyComponent />
// </ErrorBoundary>
```

**Where they CANNOT catch errors:**
- Event handlers (e.g., inside an `onClick` function). You must use regular `try...catch` here instead.
- Asynchronous code (like `setTimeout` or `fetch` calls).
- Server-side rendering.
- Errors thrown inside the Error Boundary component itself.

> 💡 **Interviewer Focus:** Know that they must be Class Components. Be ready to explain the two key lifecycle methods (`getDerivedStateFromError` and `componentDidCatch`), and name a few limitations (e.g., event handlers and async code).
</details>
<hr/>

### ❓ Q17. **What is React.memo?**
<details>
<summary><b>👀 Show Answer</b></summary>

`React.memo` is a higher-order component. If your component renders the same result given the same props, you can wrap it in `React.memo` for a performance boost by memoizing the result. React will skip rendering the component and reuse the last rendered result.

> 💡 **Interviewer Focus:** It only checks for prop changes. Shallow comparison by default.
</details>
<hr/>

### ❓ Q18. **Explain Redux Middleware and give an example.**
<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
**Redux Middleware** is an interceptor that sits between dispatching an action and the moment it reaches the reducer. 

#### **📦 The Post Office Analogy:**
*   **Action:** You mail a package.
*   **Reducer:** The destination sorting facility.
*   **Middleware:** The post office clerk checking the package. The clerk intercepts the package before it travels, inspects it (logging), adds insurance (modifying data), or redirects/blocks it (asynchronous actions/security).

Whenever an action is dispatched, it runs through the middleware first. The middleware can inspect, modify, cancel, or delay the action, or run asynchronous code.

#### **💻 Simple Code Example (Custom Logger Middleware):**
Every middleware in Redux has access to the `store` (which has `dispatch` and `getState`) and follows a triple-nested function pattern:
```javascript
const loggerMiddleware = (store) => (next) => (action) => {
  console.log('1. Action Dispatched:', action.type);
  console.log('2. Current State:', store.getState());
  
  // 'next(action)' passes the action to the next middleware, or finally the reducer
  const result = next(action); 
  
  console.log('3. New State:', store.getState());
  return result;
};
```

---

> 💡 **Interviewer Focus:**
- Explain that middleware **intercepts actions** before they update the state.
- Give common examples of middleware usage: logging (`redux-logger`), handling async APIs (`redux-thunk`, `redux-saga`), and crash reporting.

</details>
<hr/>

### ❓ Q19. **What is Redux Thunk?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
**Redux Thunk** is a middleware that allows you to write action creators that return a **function** instead of a plain action object.

#### **❌ The Problem with Basic Redux:**
By default, Redux only understands actions that are plain JavaScript objects (e.g., `{ type: 'ADD_TODO', payload: 'Buy Milk' }`). Because objects are synchronous, you **cannot** put asynchronous logic (like `fetch` API calls) directly inside an action.

#### **✅ The Solution (Redux Thunk):**
Redux Thunk intercepts dispatched items. 
*   If you dispatch a **plain object**, Thunk does nothing and passes it to the reducer.
*   If you dispatch a **function**, Thunk catches it, calls the function, and passes the `dispatch` and `getState` methods into it. You can then run your async code inside that function and dispatch a standard action once the data arrives.

#### **💻 Simple Code Example (Fetching User Data Async):**
```javascript
// A Thunk Action Creator (returns a function instead of a plain object)
const fetchUser = (userId) => {
  return async (dispatch, getState) => {
    // 1. Dispatch a sync action to show a loading spinner in UI
    dispatch({ type: 'FETCH_USER_START' });

    try {
      // 2. Perform the async API request
      const response = await fetch(`/api/users/${userId}`);
      const data = await response.json();

      // 3. Dispatch a sync action with the data once it resolves
      dispatch({ type: 'FETCH_USER_SUCCESS', payload: data });
    } catch (error) {
      // 4. Dispatch a sync action if the request fails
      dispatch({ type: 'FETCH_USER_FAILURE', error: error.message });
    }
  };
};
```

---

> 💡 **Interviewer Focus:**
- Emphasize that Thunk is "syntactic sugar" for writing async logic in Redux.
- Make sure to outline the flow: Dispatch a function $\to$ Thunk interceptor runs it $\to$ Run async task $\to$ Dispatch final standard action object.

</details>
<hr/>

### ❓ Q20. **What is the difference between Redux and Context API?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Context API** is built into React and is best for passing down data to deeply nested components (low frequency updates). It is not a state management system by itself.
- **Redux** is a full state management system with a centralized store, middleware, and DevTools. It is better for large-scale applications with complex state transitions and frequent updates.

> 💡 **Interviewer Focus:** When to use which. Redux is for complex, high-frequency state; Context is for simple, low-frequency state.
</details>
<hr/>

## 🔴 Advanced Level

### ❓ Q21. **How does React Fiber work?**
<details>
<summary><b>👀 Show Answer</b></summary>

React Fiber is the complete rewrite of React's core reconciliation algorithm introduced in React 16. Its main goal is to make rendering asynchronous, cooperative, and interruptible, allowing the UI to remain highly responsive.

---

### 1. 🍳 The Analogy: The Single-Chef Restaurant
To understand Fiber, think of a restaurant with a single chef (representing JavaScript's **single thread**):
*   **Before Fiber (Stack Reconciler):** The chef receives a massive 10-course banquet order. Once they start cooking, they **cannot stop** until all 10 courses are done. If a new customer walks in wanting a glass of water, they must wait. The front door is frozen, and the restaurant feels stuck.
    *   *In React:* For large component trees, React rendered synchronously. The browser couldn't process typing, clicks, or animations, causing screen lag/jank.
*   **With Fiber (Fiber Reconciler):** The chef works in tiny intervals. They chop one onion, check if anyone needs water. Stirs the soup, greets a customer. If a customer places an urgent order (high-priority input), the chef pauses the banquet prep, handles the urgent order, and resumes the banquet exactly where they left off.
    *   *In React:* React now splits rendering into tiny chunks (time-slicing), yielding to browser events in between.

---

### 2. 🔗 How Fiber Solved It (Linked List Structure)
JavaScript's call stack is synchronous and recursive; you cannot pause a running function recursion. Fiber solves this by converting the virtual DOM tree into a **singly linked list** of "Fiber" nodes.

Each Fiber node is a plain JavaScript object representing a unit of work with three key pointers:
*   `child`: Points to the **first child only**.
*   `sibling`: Points to the **next sibling**.
*   `return`: Points to the **parent** (where to return when work is done).

```text
         ┌────────────────────────┐
         │   Parent Fiber (App)   │◄────────────────┐
         └───────────┬────────────┘                 │
                     │                              │
                   child                          return
                     │                              │
                     ▼                              │
         ┌────────────────────────┐      ┌──────────┴─────────────┐
         │ First Child (Sidebar)  ├─────►│ Sibling (MainContent)  │
         └───────────┬────────────┘      └────────────────────────┘
                     │
                   return
                     │
                     └──────────────────────────────┘
```

Because it is a linked list, React does not use recursion anymore. It traverses the tree using a simple loop that can be paused at any node and resumed later:
```javascript
let nextUnitOfWork = firstFiberNode;

while (nextUnitOfWork && hasTimeLeftInCurrentFrame()) {
  nextUnitOfWork = performUnitOfWork(nextUnitOfWork);
}
```

---

### 3. ⏱️ The Two-Phase Architecture
To ensure the user never sees a half-rendered UI when rendering is paused, Fiber divides the process into two phases:

| Phase | Description | Interruptible? |
| :--- | :--- | :--- |
| **1. Render Phase** (Reconciliation) | React traverses the tree, runs the diffing algorithm, and builds a list of changes (in memory). | **Yes** (Can pause, discard, or restart if a higher-priority update arrives). |
| **2. Commit Phase** | React takes the calculated changes and applies them directly to the real browser DOM. | **No** (Must run synchronously to avoid visual glitches or flickering). |

---

### 4. ⚡ Update Prioritization
Fiber uses a scheduler to categorize updates into different priority levels:
*   **Immediate/Sync:** User input (typing, clicking buttons).
*   **High:** Transitions/animations (dropdown opening).
*   **Normal:** Network requests (data fetching).
*   **Low/Idle:** Background tasks (analytics logging).

If a high-priority update (typing) occurs while React is in the middle of a low-priority render, React will **abort** the low-priority render, handle the typing immediately, and restart/resume the low-priority render.

> 💡 **Interviewer Focus:** Explain the transition from Stack to Fiber. Crucial buzzwords to mention are **Asynchronous/Interruptible rendering**, **Unit of work (linked list structure)**, **Render vs Commit phases**, **Time-slicing**, and **Update Prioritization**.
</details>
<hr/>

### ❓ Q22. **What are the common pitfalls of `useEffect`?**
<details>
<summary><b>👀 Show Answer</b></summary>

> 💡 **What is a "Pitfall"?**  
> In programming, a **pitfall** is a hidden trap or common mistake that is very easy to make. The code might compile and look perfectly fine, but it leads to bugs, memory leaks, or performance drops (like infinite loops) at runtime.

While `useEffect` is powerful, it is one of the most misunderstood React hooks. Here are the 4 most common pitfalls, along with code examples and how to solve them:

---

### 1. 🔄 Infinite Re-rendering Loops
*   **The Problem:** Updating a state variable inside the effect and listing that same state variable in the dependency array. Every state update triggers a re-render, which fires the effect, which updates state, and so on.
*   **Example (Bad):**
    ```javascript
    useEffect(() => {
      setCount(count + 1); // 🔴 Triggers infinite loop
    }, [count]);
    ```
*   **The Solution:** Use functional state updates so the state variable doesn't need to be in the dependency array:
    ```javascript
    useEffect(() => {
      setCount(prev => prev + 1); // ✅ Safe, no 'count' dependency needed
    }, []);
    ```
*   **Reference Identity Trigger:** If you include objects or arrays directly in the dependency array, they get reconstructed on every render (creating a new memory reference).
    ```javascript
    const filterOptions = { status: 'active' }; // New reference on every render!
    useEffect(() => {
      fetchFilteredData(filterOptions);
    }, [filterOptions]); // 🔴 Fires on every single render
    ```
    *Solution:* Move the object outside the component, use `useMemo` to memoize it, or pass primitive properties (e.g., `filterOptions.status`) instead.

---

### 2. 🧊 Stale Closures (The Stale State Trap)
*   **The Problem:** An effect captures variables from the render in which it was created. If you omit variables from the dependency array (e.g., to force an effect to run only once on mount), the effect will reference outdated values.
*   **Example (Bad):**
    ```javascript
    useEffect(() => {
      const interval = setInterval(() => {
        console.log("Count is:", count); // 🔴 Always logs initial count (e.g., 0)
      }, 1000);
      return () => clearInterval(interval);
    }, []); // count is missing here
    ```
*   **The Solution:** Include all variables used inside the effect in the dependency array, or use a React ref (`useRef`) to hold the mutable value without triggering re-runs.

---

### 3. 🧹 Memory Leaks and Uncleaned Subscriptions
*   **The Problem:** Setting up timers (`setInterval`/`setTimeout`), WebSockets, or global DOM event listeners inside an effect without cleaning them up. When the component unmounts, the listeners remain active in the browser.
*   **Example (Bad):**
    ```javascript
    useEffect(() => {
      window.addEventListener('resize', handleResize);
      // 🔴 Missing cleanup! Keeps listening after component is unmounted.
    }, []);
    ```
*   **The Solution:** Always return a cleanup function to clean up resources:
    ```javascript
    useEffect(() => {
      window.addEventListener('resize', handleResize);
      return () => window.removeEventListener('resize', handleResize); // ✅ Cleaned up
    }, []);
    ```

---

### 4. 🏎️ Race Conditions in Data Fetching
*   **The Problem:** If a user switches between tabs or profiles quickly, multiple network requests are made. If a slower previous request finishes *after* a faster subsequent request, it overwrites the state with stale data.
*   **Example (Bad):**
    ```javascript
    useEffect(() => {
      fetchUserData(userId).then(data => setUser(data)); // 🔴 Slow query overwrites fast query
    }, [userId]);
    ```
*   **The Solution:** Use an `active` boolean flag (or `AbortController`) inside the cleanup function to ignore stale responses:
    ```javascript
    useEffect(() => {
      let active = true;

      fetchUserData(userId).then(data => {
        if (active) {
          setUser(data);
        }
      });

      return () => {
        active = false; // ✅ Stale calls will be ignored
      };
    }, [userId]);
    ```

---

> 💡 **Interviewer Focus:** Look for solutions like using **functional state updates**, handling **cleanups**, and applying **ignore flags** or **AbortControllers** to solve race conditions.
</details>
<hr/>

### ❓ Q23. **Explain the concept of "Lifting State Up".**
<details>
<summary><b>👀 Show Answer</b></summary>

In React, data flows downward (**unidirectional data flow**). Sibling components cannot directly share data with each other. 

When two or more components need access to the same state or need to remain in sync, you must **"lift"** that state up to their **closest common ancestor**. The parent component then acts as the single source of truth, passing the state down to the children as `props`, along with callback functions to update that state.

---

### 1. 📂 Visualizing the Flow

Instead of siblings communicating horizontally:
```text
[ Sibling A (Input) ] ─── ( Cannot talk directly ) ───► [ Sibling B (Display) ]
```

We lift the state to the parent:
```text
          ┌─────────────────────────┐
          │  Parent Component       │  ◄── holds state: [text, setText]
          └────┬───────────────┬────┘
               │               │
      passes text &            │ passes text
     setText callback          │ as prop
               │               │
               ▼               ▼
     ┌──────────────────┐    ┌──────────────────┐
     │ Sibling A        │    │ Sibling B        │
     │ (InputComponent) │    │ (DisplayComponent)│
     └──────────────────┘    └──────────────────┘
```

---

### 2. 💻 Code Example
Here is how you share text input from one sibling component and display it in another:

```javascript
import React, { useState } from 'react';

// 1. Parent Component (Common Ancestor)
function Parent() {
  const [text, setText] = useState(""); // Shared State

  return (
    <div style={{ padding: '20px', border: '1px solid black' }}>
      <h2>Parent Component</h2>
      {/* Pass state and state-updater function as props */}
      <InputComponent text={text} onTextChange={setText} />
      <DisplayComponent text={text} />
    </div>
  );
}

// 2. Sibling A: Updates the state
function InputComponent({ text, onTextChange }) {
  return (
    <div>
      <label>Type here: </label>
      <input 
        type="text" 
        value={text} 
        onChange={(e) => onTextChange(e.target.value)} 
      />
    </div>
  );
}

// 3. Sibling B: Reads the state
function DisplayComponent({ text }) {
  return (
    <div style={{ marginTop: '10px', color: 'blue' }}>
      <strong>Display Sibling:</strong> {text || "(empty)"}
    </div>
  );
}
```

---

### 3. ⚖️ Trade-offs & Best Practices

#### **Pros:**
*   **Single Source of Truth:** Changes are made in one place, making the app much easier to debug and test.
*   **Consistency:** Avoids synchronization bugs where siblings display different values for the same state.

#### **Cons (Prop Drilling):**
*   If Sibling A and Sibling B are located 10 levels deep in separate component trees, you have to lift the state all the way up to a root component. 
*   This forces all 9 intermediate components to pass down props (e.g., `text` and `setText`) that they don't actually use or care about.

#### **How to avoid Prop Drilling when lifting state up too high:**
*   Use React's **Context API** (built-in).
*   Use a global state management library (like **Zustand**, **Redux**, or **Recoil**).

---

> 💡 **Interviewer Focus:** Highlight unidirectional data flow, explain that React state is shared by passing it down as props and passing callbacks up, and discuss **Prop Drilling** as the main limitation of this pattern.
</details>
<hr/>

### ❓ Q24. **How do you optimize a React application with too many re-renders?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. Use `React.memo` for pure functional components.
2. Use `useMemo` and `useCallback` to prevent unnecessary recalculations and reference changes.
3. Move state down to where it is needed instead of putting everything in top-level context or state.
4. Use windowing/lazy loading for large lists (e.g., `react-window`).

**🏢 Industry Example:**  
In a **Live Crypto or Stock Trading Dashboard**, price updates happen via WebSockets multiple times per second. If the global state triggers a re-render of the entire dashboard, the app will freeze. In the industry, we solve this by:
- Storing the high-frequency price updates in localized state or using atomic state libraries (like Jotai/Zustand).
- Wrapping individual `StockRow` components in `React.memo` so a price change in "Bitcoin" only re-renders the Bitcoin row, leaving the "Ethereum" row untouched.

> 💡 **Interviewer Focus:** Practical performance optimization strategies.
</details>
<hr/>

### ❓ Q25. **What is the difference between `useLayoutEffect` and `useEffect`?**
<details>
<summary><b>👀 Show Answer</b></summary>

The difference between these two hooks lies entirely in **when they execute relative to the browser painting the screen**.

---

### 1. ⏱️ The Rendering Lifecycle Timeline
Here is the sequence of events during a state update:

```text
1. State Update triggered (e.g. user clicks a button)
2. React renders the component tree (calculates Virtual DOM changes)
3. React mutates the real DOM nodes (in-memory changes)
   │
   ├─► 4. useLayoutEffect runs SYNCHRONOUSLY
   │      (React blocks the browser from drawing to run your effect code)
   ▼
5. Browser paints the screen (pixels are drawn, user sees the changes)
   │
   └─► 6. useEffect runs ASYNCHRONOUSLY
          (Deferred work; does not block the UI)
```

---

### 2. ⚡ Key Differences at a Glance

| Feature | `useEffect` | `useLayoutEffect` |
| :--- | :--- | :--- |
| **Execution Timing** | **Asynchronous:** Runs *after* the browser paints. | **Synchronous:** Runs *before* the browser paints. |
| **Blocks UI?** | **No.** Keeps the app responsive and smooth. | **Yes.** Blocks the main thread until the code completes. |
| **Primary Use Case** | Data fetching, event listeners, subscriptions, telemetry. | DOM measurements (height, width, scroll position) and style changes. |
| **Server Rendering** | Runs only on the client (safe on server). | Throws a warning on the server because the server has no layout/DOM. |

---

### 3. 🛠️ Concrete Example: The Tooltip Flicker Problem
Imagine you want to render a tooltip right next to a button. You need to measure the button's position first to align the tooltip.

#### **If you use `useEffect`:**
1. React renders the tooltip at default coordinates `(0, 0)`.
2. The browser paints the tooltip at `(0, 0)`.
3. `useEffect` runs, measures the button's actual position, calculates the tooltip should be at `(150, 200)`, and updates the state.
4. React re-renders and paints the tooltip at `(150, 200)`.
*   **Result:** The user sees a split-second **visual flicker** where the tooltip jumps from `(0, 0)` to `(150, 200)`.

#### **If you use `useLayoutEffect`:**
1. React renders the tooltip at `(0, 0)`.
2. *Before the browser draws anything*, `useLayoutEffect` runs, measures the button, calculates `(150, 200)`, and updates the state synchronously.
3. React re-renders immediately.
4. The browser paints the final tooltip at `(150, 200)`.
*   **Result:** No visual flicker. The tooltip appears at `(150, 200)` instantly.

```javascript
import React, { useState, useLayoutEffect, useRef } from 'react';

function TooltipButton() {
  const buttonRef = useRef(null);
  const [tooltipHeight, setTooltipHeight] = useState(0);

  // Measure the DOM element before painting to prevent visual jumps
  useLayoutEffect(() => {
    if (buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      setTooltipHeight(rect.height); // Update state synchronously
    }
  }, []);

  return (
    <>
      <button ref={buttonRef}>Hover Me</button>
      <div style={{ marginTop: `${tooltipHeight}px` }}>Tooltip content</div>
    </>
  );
}
```

---

> 💡 **Interviewer Focus:** Standardize on `useEffect` 99% of the time to keep the main thread unblocked. Only use `useLayoutEffect` when you are measuring/mutating the DOM and must prevent **visual flickering**.
</details>
<hr/>

### ❓ Q26. **How does Redux Toolkit (RTK) improve on standard Redux?**
<details>
<summary><b>👀 Show Answer</b></summary>

### 1. ⚔️ Are they different libraries?
**No.** They are not competing libraries. 
*   **Standard Redux (Core):** Is the underlying engine. It defines the architecture of state, dispatch, actions, and reducers.
*   **Redux Toolkit (RTK):** Is an official, opinionated, battery-included wrapper package built *on top of* Core Redux. 

RTK is the **official recommended standard** for writing Redux logic today. It does not replace Redux; it simplifies how you write it.

---

### 2. 📊 Core Redux vs. Redux Toolkit Comparison

| Feature | Standard (Core) Redux | Redux Toolkit (RTK) |
| :--- | :--- | :--- |
| **Boilerplate** | High. You must write action constants, action creators, and reducers in separate files. | Low. Everything is wrapped in a single **Slice** using `createSlice`. |
| **Store Config** | Manual setup. You must configure DevTools, combine reducers, and apply middlewares (like Thunk) manually. | Automated. `configureStore` automatically sets up DevTools, Thunk, and combines reducers. |
| **Immutability** | Manual. You must copy state with spread operators (`...`). Mutating state directly causes severe bugs. | Handled automatically. Integrates **Immer**, allowing you to write "mutative-looking" code. |
| **Async Logic** | Requires downloading and manually attaching third-party libraries (e.g., Redux Thunk, Redux Saga). | Included out-of-the-box. Redux Thunk is built-in; RTK also includes **RTK Query** for API requests. |

---

### 3. 💻 Code Comparison: Creating a Counter

#### **Traditional Redux (Boilerplate Heavy)**
```javascript
// 1. Action Types
const INCREMENT = 'counter/increment';

// 2. Action Creator
export const increment = () => ({ type: INCREMENT });

// 3. Reducer (Must handle immutability manually)
const initialState = { value: 0 };
export default function counterReducer(state = initialState, action) {
  switch (action.type) {
    case INCREMENT:
      return {
        ...state,
        value: state.value + 1 // 🔴 Must use spread operator to avoid mutation
      };
    default:
      return state;
  }
}
```

#### **Redux Toolkit (RTK Modern Approach)**
```javascript
import { createSlice } from '@reduxjs/toolkit';

// createSlice automatically creates the action types, action creators, and reducer
const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => {
      state.value += 1; // ✅ Safe! Immer handles immutability under the hood.
    }
  }
});

export const { increment } = counterSlice.actions;
export default counterSlice.reducer;
```

---

### 4. 🧠 The Magic of Immer in RTK
In Core Redux, mutating state directly (e.g., `state.value = 10` or `state.todos.push(newTodo)`) is a major bug because React uses reference comparison to see if the state changed. If the reference doesn't change, React won't re-render.

RTK uses a library called **Immer** under the hood. Immer tracks your code changes on a temporary "draft state" and outputs a completely new, immutable state copy for Redux. This lets you write standard JavaScript mutative code (like `push()`, `splice()`, or assignment `=` operators) safely.

---

> 💡 **Interviewer Focus:** Highlight that RTK is **Redux without the boilerplate**. Focus on: **`createSlice`** (combining actions/reducers), **Immer** (safe mutations), and **`configureStore`** (simplifying middleware/DevTools setup).
</details>
<hr/>

### ❓ Q26a. **What is the Immer library and how does it work?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Immer** is a tiny JavaScript library that allows you to work with immutable state in a more convenient, readable way. It is built around the **copy-on-write** mechanism.

---

### 1. 💡 The Core Problem: Nested Updates in Pure JS
In JavaScript, mutating nested objects is extremely verbose when done immutably:
```javascript
// Manual update in vanilla JS:
const nextState = {
  ...state,
  user: {
    ...state.user,
    address: {
      ...state.user.address,
      city: 'New York'
    }
  }
};
```
This is called "Spread Operator Hell". It is hard to read and easy to make mistakes (accidentally mutating a level by forgetting to spread it).

---

### 2. 🛡️ How Immer Solves It: The "Draft" Concept
Immer lets you write code by simply modifying a **temporary draft** of the state. Once your modifications are complete, Immer outputs the next state based on your mutations to the draft.

```text
 [ Base State ] (Read-only)
       │
       ▼
 [ Draft State ] (Proxy-based, mutable)  ◄── You mutate this directly (e.g. draft.count++)
       │
       ▼
 [ Next State ] (Fully immutable copy with updates applied)
```

#### **How it looks in code using Immer's `produce` function:**
```javascript
import { produce } from 'immer';

const baseState = {
  user: {
    name: 'Alice',
    address: { city: 'Boston' }
  }
};

const nextState = produce(baseState, (draft) => {
  draft.user.address.city = 'New York'; // ✅ Direct mutation on draft!
});

console.log(baseState.user.address.city); // 'Boston' (Unchanged)
console.log(nextState.user.address.city); // 'New York' (Updated)
```

---

### 3. ⚙️ How it works under the hood (ES6 Proxies)
Immer uses **ES6 Proxies** to implement the "copy-on-write" pattern:
1.  **Intercepting reads/writes:** When you call `produce`, Immer wraps your `baseState` in a Proxy object called the `draft`.
2.  **Tracking changes:** The Proxy intercepts any read or write operations you make inside the recipe function.
3.  **Shallow copying on write:** As soon as you attempt to *write* (modify) a property on the draft, the Proxy intercepts the mutation, creates a shallow copy of that specific node in the tree, and applies your mutation to that copy.
4.  **Reusing unchanged parts (Structural Sharing):** Any parts of the state tree that were *not* modified are reused directly (by reference). This makes Immer extremely fast and memory-efficient.

---

### 4. 🔗 Immer in Redux Toolkit (RTK)
Redux Toolkit wraps the reducers you define inside `createSlice` in Immer's `produce` function automatically. That is why you can safely write:
```javascript
reducers: {
  addTodo: (state, action) => {
    state.todos.push(action.payload); // Safe mutation!
  }
}
```

---

> 💡 **Interviewer Focus:** Explain the **Draft state** concept, **ES6 Proxies**, **structural sharing** (reusing unmodified references), and why it solves the problem of nested object copying ("spread operator hell").
</details>
<hr/>

### ❓ Q27. **Explain the concept of "Selectors" in Redux and why `reselect` is used.**
<details>
<summary><b>👀 Show Answer</b></summary>

Selectors are functions that extract specific pieces of state from the store.
`reselect` is a library for creating memoized selectors. They are useful because they only recalculate when the specific part of the state tree they depend on changes, preventing unnecessary re-renders in components using those selectors.

> 💡 **Interviewer Focus:** Performance optimization in Redux.
</details>
<hr/>

### ❓ Q28. **How would you implement a custom Redux middleware?**
<details>
<summary><b>👀 Show Answer</b></summary>

Redux middleware uses a curried function pattern:
```javascript
const customMiddleware = store => next => action => {
  // Perform side effect or log here
  console.log('Dispatching:', action);
  let result = next(action); // Pass to next middleware or reducer
  console.log('Next State:', store.getState());
  return result;
};
```

> 💡 **Interviewer Focus:** Understanding the `store => next => action` signature.
</details>
<hr/>

## 🟣 Expert Level

### ❓ Q29. **Design a state management strategy for a large-scale application with frequent, high-volume data updates.**
<details>
<summary><b>👀 Show Answer</b></summary>

**Strategy:**
1. **Hybrid Approach:** Use Redux/RTK for global, complex, and highly shared state (like user session, cart). Use local component state or Context for UI state (dropdowns, modals).
2. **Normalization:** Normalize the store state to avoid duplication and make lookups O(1).
3. **Memoization:** Heavy use of `reselect` for memoized selectors to prevent component re-renders.
4. **Throttling/Debouncing:** Throttle or debounce actions that trigger frequent updates (e.g., search inputs, window resize).
5. **Consider alternatives:** For extreme cases, look into MobX (mutative) or Recoil/Jotai (atomic state) if Redux boilerplate becomes a bottleneck.

**🏢 Industry Example:**  
In an **Enterprise ERP System (e.g., SAP or Salesforce UI)**:
- We use **React Query / RTK Query** for server state (caching API responses, deduplicating requests for user profiles).
- We use **Redux Toolkit (RTK)** for client-side global state (e.g., the current active workspace, multi-step wizard data).
- We use **Context API** for Theme and Localization.
- We use component-level `useState` for simple UI toggles (is dropdown open?). 
This separation of concerns ensures the global store isn't polluted with cached API data or transient UI state.

> 💡 **Interviewer Focus:** High-level architectural thinking, trade-offs between libraries, and performance considerations.
</details>
<hr/>

### ❓ Q30. **Explain how Concurrent Mode and Suspense work in React 18.**
<details>
<summary><b>👀 Show Answer</b></summary>

Concurrent Mode is a set of new features that help React apps stay responsive and gracefully adjust to the user’s device capabilities and network speed.
- **Transitions:** `useTransition` allows you to mark updates as non-urgent, so urgent updates (like typing) aren't blocked by heavy rendering.
- **Suspense:** Allows components to "wait" for something (like data or code loading) before rendering, showing a fallback UI. In React 18, it works with server-side rendering and data fetching frameworks.

> 💡 **Interviewer Focus:** React 18 features, non-blocking rendering, and user experience improvement.
</details>
<hr/>

### ❓ Q31. **How do you prevent memory leaks in a React application?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. **Clean up effects:** Always return a cleanup function in `useEffect` for event listeners, timers, and subscriptions.
2. **Cancel async operations:** Use `AbortController` to cancel fetch requests if the component unmounts before the request completes.
3. **Avoid holding references:** Don't store large objects in refs or global variables if they are not needed after unmount.

> 💡 **Interviewer Focus:** Practical debugging and memory management skills.
</details>
<hr/>

### ❓ Q32. **Compare Redux Saga and Redux Thunk.**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Redux Thunk:** Uses functions to handle async logic. Simple to understand, less boilerplate, good for small to medium apps.
- **Redux Saga:** Uses ES6 Generators (`yield`). Better for complex async flows (like race conditions, cancellation, background tasks). Easier to test because effects are declarative objects. More boilerplate and steeper learning curve.

> 💡 **Interviewer Focus:** Understanding when the complexity of Saga is justified.
</details>
<hr/>

### ❓ Q33. **What is Server Component (RSC) in React and how is it different from SSR?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **SSR (Server-Side Rendering):** Renders the HTML on the server and sends it to the client. The client still downloads the full JS bundle to hydrate the page.
- **RSC (React Server Components):** Components that execute *only* on the server. They reduce the bundle size because the code for the component stays on the server, and only the generated content is sent to the client. They cannot use hooks or browser APIs.

> 💡 **Interviewer Focus:** This is the cutting edge of React. Understanding the zero-bundle-size benefit.
</details>
<hr/>

## 🔷 Scenario-Based & Real-World Questions

### ❓ Q34. **How would you implement a search input that fetches data from an API, ensuring it doesn't overload the server with requests?**
<details>
<summary><b>👀 Show Answer</b></summary>

I would use **Debouncing**. Debouncing ensures that the API call is only made after the user has stopped typing for a specified amount of time (e.g., 300ms).

```javascript
useEffect(() => {
  const handler = setTimeout(() => {
    fetchData(searchTerm);
  }, 300);

  return () => clearTimeout(handler); // Cleanup on unmount or searchTerm change
}, [searchTerm]);
```

> 💡 **Interviewer Focus:** Understanding of `setTimeout` in `useEffect` cleanup for debouncing.
</details>
<hr/>

### ❓ Q35. **You have a list of 10,000 items to render. How do you ensure the UI remains smooth?**
<details>
<summary><b>👀 Show Answer</b></summary>

To render 10,000 items smoothly in React, you must use **List Virtualization** (also known as **Windowing**). 

---

### 1. ⚠️ The Core Problem: DOM Node Bloat
If you render 10,000 items natively (using a simple `.map()`):
*   The browser has to create and memory-allocate **10,000 real DOM nodes**.
*   Every state update or layout recalculation (reflow) forces the browser to traverse and recalculate positions for all 10,000 nodes.
*   This causes high memory usage, laggy scrolling, and a long initial page load time.

---

### 2. 🪟 Key Concept: List Virtualization (Windowing)
Instead of creating all 10,000 DOM elements, list virtualization **only renders the items currently visible in the user's viewport**, plus a tiny buffer of off-screen items above and below to prevent blank spots when scrolling quickly.

#### **Visualizing Virtualization:**
```text
┌───────────────────────────────────┐  ◄── Scroll Container (Total height = 10,000 * 50px)
│ (Scroll offset area)              │
├───────────────────────────────────┤
│ [ Buffer Item - Ready in DOM ]    │  ◄── Pre-rendered to prevent blank flashes
├───────────────────────────────────┤
│ ┌───────────────────────────────┐ │
│ │ [ Rendered Item 15 ]          │ │  ◄── Visible Viewport (The "Window")
│ │ [ Rendered Item 16 ]          │ │      Only these ~5-10 items
│ │ [ Rendered Item 17 ]          │ │      exist in the real DOM!
│ └───────────────────────────────┘ │
├───────────────────────────────────┤
│ [ Buffer Item - Ready in DOM ]    │
├───────────────────────────────────┤
│ (Remaining 9,980 items)           │  ◄── NOT created or rendered in the DOM
└───────────────────────────────────┘
```

---

### 3. ⚙️ How it Works Under the Hood
1.  **Outer Container:** A wrapper element with `overflow-y: auto` is created. This defines the viewport size (e.g., `height: 400px`).
2.  **Inner Container:** A spacer element inside the wrapper is set to the height of the *entire* list (`Total Items (10,000) * Item Height (50px) = 500,000px`). This creates a native scrollbar.
3.  **Dynamic Positioning:** When the user scrolls, the library calculates the current scroll offset, determines which items should be visible, and renders only those items, absolute-positioning them inside the inner container using `top: index * Item Height`.

---

### 4. 🛠️ How to Implement It in React

#### **A. Recommended Libraries:**
*   `react-window` (Lightweight, recommended for 90% of use cases).
*   `react-virtualized` (Feature-rich, but heavier).
*   `react-virtuoso` (Great for variable/dynamic item heights).

#### **B. Code Example (using `react-window`):**
```javascript
import { FixedSizeList as List } from 'react-window';

const Row = ({ index, style }) => (
  // style contains the absolute positioning (top/height) computed by the library
  <div style={style} className={index % 2 ? 'ListItemOdd' : 'ListItemEven'}>
    Row {index}
  </div>
);

function App() {
  return (
    <List
      height={500}          // Height of the visible window
      itemCount={10000}     // Total items
      itemSize={50}         // Height of each row in pixels
      width={300}           // Width of the list container
    >
      {Row}
    </List>
  );
}
```

---

### 5. 💡 Alternative & Complementary Approaches

*   **Pagination / Infinite Scroll:** Fetch and render data in batches (e.g., 20 or 50 items at a time) as the user reaches the bottom of the page.
*   **CSS `content-visibility: auto`:** A modern CSS property that tells the browser to skip rendering layout and paint for off-screen elements.
*   **Component Optimization:** Wrap list items in `React.memo` and use stable `key` props (never array index) to prevent unnecessary re-renders of rows.

---

> 💡 **Interviewer Focus:** Explain **DOM node limit bottlenecks**, the concept of **Windowing**, how the **outer/inner container** structure calculates scroll height, and name standard libraries like **`react-window`**.
</details>
<hr/>

### ❓ Q36. **How would you handle a race condition where a slower previous API request overwrites a faster subsequent request?**
<details>
<summary><b>👀 Show Answer</b></summary>

This is a classic asynchronous bug in React. It occurs because network requests resolve at unpredictable times.

---

### 1. 🏎️ The Step-by-Step Scenario
Imagine you have a profile viewer page:
1.  **Time 0ms:** The user clicks on **User A**. React fires **Request A** (fetching User A's data).
2.  **Time 100ms:** The user quickly clicks on **User B**. React fires **Request B** (fetching User B's data).
3.  **Time 200ms:** **Request B completes quickly** (takes 100ms). The UI updates to display **User B**.
4.  **Time 1000ms:** **Request A completes slowly** due to server lag (takes 1000ms). The promise resolves and calls `setUser(dataA)`.
*   **The Bug:** The UI is now showing **User A's data**, but the user is currently on **User B's page**.

---

### 2. 🛡️ Solution 1: The Boolean Ignore Flag (Recommended for simplicity)
Use a local boolean flag inside your `useEffect`. When the component re-renders (due to dependency changes) or unmounts, the cleanup function sets the flag to `false`, causing the resolved stale promise to ignore the state update.

```javascript
useEffect(() => {
  let active = true; // Flag initialized on every effect execution

  fetchUserData(userId).then(data => {
    if (active) {
      setUser(data); // Only update state if this is still the active request
    }
  });

  return () => {
    active = false; // Cleanup runs before next effect runs, setting flag to false
  };
}, [userId]);
```

#### **How this works in the scenario:**
*   When the user clicks User B, `userId` changes.
*   Before running the effect for User B, React runs the **cleanup function of User A's effect**, which sets `active = false` for Request A.
*   When Request A finally resolves, the code checks `if (active)`. Since `active` is `false`, `setUser(dataA)` is skipped.

---

### 3. 🚫 Solution 2: AbortController (Network-level cancellation)
Instead of just ignoring the data when it arrives, you can cancel the actual HTTP request using the browser's native `AbortController` API. This saves network bandwidth and CPU cycles on the client.

```javascript
useEffect(() => {
  const controller = new AbortController();
  const signal = controller.signal;

  fetch(`/api/user/${userId}`, { signal })
    .then(res => res.json())
    .then(data => {
      setUser(data);
    })
    .catch(err => {
      if (err.name === 'AbortError') {
        console.log('Fetch successfully aborted!');
      } else {
        // Handle other network/parsing errors
      }
    });

  return () => {
    controller.abort(); // Cancel the fetch request immediately
  };
}, [userId]);
```

---

### 4. 🚀 The Modern Solution: RTK Query (Redux Native)
In modern React development, you rarely write manual `useEffect` wrappers for API calls. Since this is a React/Redux environment, the recommended approach is to use **RTK Query** (part of Redux Toolkit).

RTK Query handles race conditions, caching, request deduplication, and cancellation automatically under the hood:

#### **A. How RTK Query Solves Race Conditions (Endpoints & Arguments)**
Each endpoint generates hooks that cache data based on the argument passed to the query (e.g., `userId`):
*   When `userId` changes from `A` to `B`, the hook unsubscribes from User A and subscribes to User B.
*   If User A's slow request completes later, RTK Query saves it in the cache for User A, but **does not trigger state updates or re-renders** for the component currently displaying User B.

#### **B. Subscription-Based Caching**
*   RTK Query manages state using a subscription model. Multiple components can subscribe to the same data (using the same query argument).
*   It deduplicates duplicate queries, only sending a single network request for multiple concurrent subscriptions.

#### **C. Automatic Cancellation**
*   RTK Query uses `AbortController` under the hood. If a query argument changes or a component unmounts before a network request completes, RTK Query automatically aborts the request, saving server bandwidth.

#### **RTK Query Code Example:**
```javascript
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

// 1. Define your API slice
export const userApi = createApi({
  reducerPath: 'userApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api/' }),
  endpoints: (builder) => ({
    getUserById: builder.query({
      // RTK Query handles cache indexing, race conditions, and abort signals automatically!
      query: (userId) => `user/${userId}`,
    }),
  }),
});

// 2. Export the auto-generated hook
export const { useGetUserByIdQuery } = userApi;

// 3. Usage inside a component
function UserProfile({ userId }) {
  // Hook automatically manages loading, error, and cached state safely
  const { data: user, isLoading } = useGetUserByIdQuery(userId);

  if (isLoading) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

---

> 💡 **Interviewer Focus:** Detail the **chronological sequence** of the race condition bug. Explain both the **boolean flag cleanup pattern** and the **`AbortController` API** to demonstrate network-level optimization. Mentioning **React Query** or **RTK Query** shows strong industry experience.
</details>
<hr/>

### ❓ Q37. **How do you persist Redux state across page reloads?**
<details>
<summary><b>👀 Show Answer</b></summary>

To persist Redux state across page reloads, you must serialize the Redux state tree and save it to a persistent browser storage API (usually **`localStorage`** or **`sessionStorage`**), then load it as the initial state during store creation.

There are two primary ways to implement this:

---

### 1. 🛠️ Method A: Manual Store Subscription (Lightweight & Native)
You can manually listen for state changes using `store.subscribe()` and save selected parts of your state to `localStorage`. When the app loads, you retrieve and pass this data to the store configuration as `preloadedState`.

#### **Code Example:**
```javascript
import { configureStore } from '@reduxjs/toolkit';
import rootReducer from './reducers';

// 1. Helper to load state from localStorage
const loadState = () => {
  try {
    const serializedState = localStorage.getItem('redux_state');
    if (serializedState === null) return undefined; // Let reducers set initial state
    return JSON.parse(serializedState);
  } catch (err) {
    console.error("Could not load state", err);
    return undefined;
  }
};

// 2. Helper to save state to localStorage
const saveState = (state) => {
  try {
    const serializedState = JSON.stringify(state);
    localStorage.setItem('redux_state', serializedState);
  } catch (err) {
    console.error("Could not save state", err);
  }
};

// Load initial state
const preloadedState = loadState();

export const store = configureStore({
  reducer: rootReducer,
  preloadedState, // 3. Hydrate the store
});

// 4. Save state changes (filtered to prevent performance hits)
store.subscribe(() => {
  saveState({
    cart: store.getState().cart // ✅ Only persist the cart slice (Best practice!)
  });
});
```

---

### 2. 🤖 Method B: Using `redux-persist` (Automated Middleware)
For larger applications, the library `redux-persist` is widely used. It automatically manages storing, retrieving, and rehydrating state under the hood.

#### **Step 1: Configure Store with Persisted Reducer**
```javascript
import { configureStore } from '@reduxjs/toolkit';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage'; // Defaults to localStorage
import rootReducer from './rootReducer';

const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['cart'] // Only persist the cart slice (ignores temporary UI state)
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false, // Required: redux-persist uses non-serializable actions
    }),
});

export const persistor = persistStore(store);
```

#### **Step 2: Wrap App in `PersistGate`**
```javascript
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { store, persistor } from './store';

ReactDOM.render(
  <Provider store={store}>
    {/* PersistGate delays loading the UI until state is rehydrated */}
    <PersistGate loading={<div>Loading saved items...</div>} persistor={persistor}>
      <App />
    </PersistGate>
  </Provider>,
  document.getElementById('root')
);
```

---

### 3. ⚠️ Critical Best Practices & Pitfalls

*   **Only Persist What's Needed (Whitelisting):** Never persist your entire Redux store. Avoid persisting temporary UI flags (e.g. `isModalOpen`, `isLoading`, API response errors). Use a `whitelist` to target specific slices like user settings or checkout carts.
*   **Performance Considerations:** Writing to `localStorage` is **synchronous** and blocks the main thread. If you save massive state updates on every keypress, your app will feel laggy. For manual subscription, use a `throttle` helper (like lodash's `throttle`) to limit writes to once every second.
*   **State Migrations (Schema Changes):** If you deploy a code update that changes the structure of your Redux state, a user's browser will still load the old structural layout from `localStorage`, causing app crashes. `redux-persist` allows you to define migration functions to version and update old client schemas safely.

---

> 💡 **Interviewer Focus:** Explain how **store serialization** works. Highlight **`store.subscribe()`** and **`preloadedState`** for manual implementation. Discuss the use of **`redux-persist`** with **`PersistGate`**, and detail performance precautions (throttling/filtering) and state migrations.
</details>
<hr/>

### ❓ Q38. **How would you implement a theme switcher (Dark/Light mode) in a React app?**
<details>
<summary><b>👀 Show Answer</b></summary>

I would use the **Context API** to provide the current theme and a toggle function to the entire app tree. Styled-components or CSS variables can then consume this context to apply styles.

> 💡 **Interviewer Focus:** Good use case for Context API (global, low-frequency update).
</details>
<hr/>

### ❓ Q39. **What is the best way to handle authentication state globally?**
<details>
<summary><b>👀 Show Answer</b></summary>

Handling authentication globally requires a clean separation between **client-side state management** (Redux/React state) and **secure token storage** (JWTs).

---

### 1. 🛡️ Token Storage Strategy: Where to keep the JWT?

How you store tokens is a major security consideration (XSS vs. CSRF vulnerabilities):

| Location | Security Risk | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **`httpOnly` Cookie (Safest)** | Protected against **XSS** (JS cannot read the cookie). Vulnerable to **CSRF** (mitigated by `SameSite=Strict` and anti-CSRF tokens). | Automatically sent by browser on requests; highly secure. | Server must configure cookie domains and CORS headers correctly. |
| **In-Memory (Redux)** | Safe from storage scrapers. Lost on page reload. | Extremely fast access. | Requires a **Refresh Token** stored in an `httpOnly` cookie to fetch a new access token on reload. |
| **`localStorage` / `sessionStorage`** | Highly vulnerable to **XSS** attacks (malicious scripts can steal the token). | Easy to implement; works across subdomains. | Storing sensitive credentials here is **discouraged** in enterprise production. |

---

### 2. 🧩 The Core Implementation (Redux Toolkit)

A standard implementation uses a dedicated Redux slice (`authSlice`) to track the logged-in user profile, and RTK Query to fetch data and attach headers.

#### **Step A: The Auth Slice**
```javascript
import { createSlice } from '@reduxjs/toolkit';

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    isAuthenticated: false,
    token: null, // If using in-memory token strategy
  },
  reducers: {
    setCredentials: (state, action) => {
      const { user, token } = action.payload;
      state.user = user;
      state.token = token;
      state.isAuthenticated = true;
    },
    logOut: (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
    }
  }
});

export const { setCredentials, logOut } = authSlice.actions;
export default authSlice.reducer;
```

#### **Step B: Automatic Token Attachment (RTK Query)**
If storing the token in-memory in Redux (or retrieving it from cookies), you use `prepareHeaders` to automatically attach it to every API request:

```javascript
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: '/api/',
    prepareHeaders: (headers, { getState }) => {
      // Pull token from the auth slice state
      const token = getState().auth.token;
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  endpoints: (builder) => ({
    // API endpoints go here
  }),
});
```

---

### 3. 🎣 The Custom `useAuth` Hook (Decoupling UI from Redux)
To keep components clean and prevent imports of dispatch actions everywhere, wrap authentication logic in a custom hook:

```javascript
import { useSelector, useDispatch } from 'react-redux';
import { logOut, setCredentials } from './authSlice';

export function useAuth() {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.auth.user);
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

  const handleLogin = (userData) => {
    dispatch(setCredentials(userData));
  };

  const handleLogout = () => {
    dispatch(logOut());
    // Also hit API logout endpoint to clear HttpOnly cookies if applicable
  };

  return {
    user,
    isAuthenticated,
    login: handleLogin,
    logout: handleLogout
  };
}
```

---

### 4. 🔀 Handling Token Expiration (HTTP 401 Interceptor)
If an API request fails with a `401 Unauthorized` status (due to token expiration):
1.  **Axios Interceptor** or **RTK Query custom baseQuery** intercepts the response.
2.  It attempts to fetch a new access token using a refresh token endpoint (silent refresh).
3.  If refresh fails, it dispatches the `logOut()` action to redirect the user to the login page.

---

> 💡 **Interviewer Focus:** Emphasize security. Walk through **`httpOnly` cookies** vs **localStorage**, demonstrate how to intercept outgoing requests to attach JWTs, and showcase how a **custom `useAuth` hook** cleanups UI component logic.
</details>
<hr/>

### ❓ Q40. **How would you create a multi-step form in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

Keep the form state in a parent component or Redux store. Render different child components for each step based on a `currentStep` state. Validate each step before proceeding.

> 💡 **Interviewer Focus:** State management strategy for complex forms.
</details>
<hr/>

### ❓ Q41. **How do you test a custom hook?**
<details>
<summary><b>👀 Show Answer</b></summary>

I would use `@testing-library/react-hooks` and its `renderHook` function. This allows me to test the hook's return values and effects without creating a dummy component.

> 💡 **Interviewer Focus:** Familiarity with modern testing tools for hooks.
</details>
<hr/>

### ❓ Q42. **How would you implement "Undo/Redo" functionality using Redux?**
<details>
<summary><b>👀 Show Answer</b></summary>

By using a library like `redux-undo` or manually structuring the state to have `past`, `present`, and `future` arrays. Actions would move the `present` to `past` on new updates, and pop from `past`/`future` for undo/redo.

> 💡 **Interviewer Focus:** Understanding state history management.
</details>
<hr/>

### ❓ Q43. **A component is re-rendering because its object prop changes reference, but the data is the same. How do you fix this?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `useMemo` in the parent component to memoize the object, or pass primitive values instead of the object if possible. If passing a function, use `useCallback`.

> 💡 **Interviewer Focus:** Reference equality in JavaScript and React optimization.
</details>
<hr/>

### ❓ Q44. **How would you implement a Global Modal system in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use Redux or Context to store the active modal type and props. Render a single `ModalContainer` at the root of the app that listens to this state and renders the appropriate modal using **React Portals** to mount it outside the main DOM tree.

> 💡 **Interviewer Focus:** Use of Portals for modals and centralized state control.
</details>
<hr/>

### ❓ Q45. **How do you handle WebSocket connections in a React/Redux app?**
<details>
<summary><b>👀 Show Answer</b></summary>

The critical architectural rule for WebSockets in React is: **Do NOT manage the global socket connection inside component `useEffect` hooks.** 
*   **Why?** Component mounting/unmounting and re-rendering can cause multiple duplicate connections, memory leaks, and disconnected streams during page navigation.

Instead, WebSockets should be managed in the **Redux Middleware layer** or through **RTK Query's streaming cache endpoints**.

---

### 📡 Option A: Custom Redux Middleware (Classic & Scalable)
A custom middleware runs outside the React render cycle, maintaining a single persistent socket connection. It translates actions to socket messages and translates socket events to Redux actions.

#### **1. The Socket Middleware Code:**
```javascript
export const socketMiddleware = () => {
  let socket = null; // Private variable to store the active socket reference

  return (store) => (next) => (action) => {
    switch (action.type) {
      case 'ws/connect':
        if (socket !== null) {
          socket.close(); // Close existing connection if any
        }
        
        socket = new WebSocket(action.payload.url);

        // Bind event listeners to dispatch Redux actions
        socket.onopen = () => store.dispatch({ type: 'ws/connected' });
        socket.onclose = () => store.dispatch({ type: 'ws/disconnected' });
        socket.onerror = (err) => store.dispatch({ type: 'ws/error', payload: err });
        
        socket.onmessage = (event) => {
          const messageData = JSON.parse(event.data);
          store.dispatch({ type: 'ws/messageReceived', payload: messageData });
        };
        break;

      case 'ws/disconnect':
        if (socket !== null) {
          socket.close();
        }
        socket = null;
        break;

      case 'ws/sendMessage':
        if (socket && socket.readyState === WebSocket.OPEN) {
          socket.send(JSON.stringify(action.payload));
        }
        break;

      default:
        // Pass standard Redux actions through
        return next(action);
    }
  };
};
```

---

### 🚀 Option B: RTK Query Streaming Updates (Modern & Declarative)
If you are using Redux Toolkit, RTK Query provides `onCacheEntryAdded`, a lifecycle callback that lets you stream real-time updates directly into your cached state.

```javascript
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const chatApi = createApi({
  reducerPath: 'chatApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api/' }),
  endpoints: (builder) => ({
    getMessages: builder.query({
      query: (channelId) => `messages/${channelId}`,
      // 1. Lifecycle hook triggered when a component queries getMessages
      async onCacheEntryAdded(channelId, { updateCachedData, cacheDataLoaded, cacheEntryRemoved }) {
        const ws = new WebSocket(`ws://localhost:8080/channel/${channelId}`);

        try {
          // Wait for the initial HTTP query resolution before listing to socket
          await cacheDataLoaded;

          ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            // 2. Directly update the Redux cache draft!
            updateCachedData((draft) => {
              draft.push(message); 
            });
          };
        } catch {
          // Query was cancelled or failed
        }

        // 3. Cleanup: Automatically run when component unmounts and cache expires
        await cacheEntryRemoved;
        ws.close();
      },
    }),
  }),
});
```

---

### 🏢 Industry Example (Real-Time Support Chat)
In an application like **Intercom** or **Slack**:
*   A user opens a channel. The component calls `useGetMessagesQuery(channelId)`.
*   RTK Query fetches the last 50 messages from the database.
*   Once loaded, the socket connects and starts streaming new messages, appending them directly to the in-memory array.
*   When the user navigates away, the socket is automatically closed by the `cacheEntryRemoved` listener.

---

> 💡 **Interviewer Focus:** Explain the separation of concerns. Component hooks are for subscription declarations, **middleware** or **RTK Query hooks** are for connection and lifecycle management. Show code structure for either a **custom middleware** or **`onCacheEntryAdded`** to prove design depth.
</details>
<hr/>

### ❓ Q46. **What is the difference between shallow rendering and full DOM rendering in testing?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Shallow Rendering:** Renders only the component itself and not its children. Good for isolated unit tests.
- **Full DOM Rendering:** Renders the component and all its children. Necessary for integration tests and testing behavior that depends on child components.

> 💡 **Interviewer Focus:** React Testing Library promotes full DOM rendering to mimic user behavior.
</details>
<hr/>

### ❓ Q47. **How would you optimize a heavy computation in a component?**
<details>
<summary><b>👀 Show Answer</b></summary>

Wrap the computation in `useMemo` so it only re-runs when its dependencies change. If it's extremely heavy, consider moving it to a **Web Worker** to avoid blocking the main UI thread.

> 💡 **Interviewer Focus:** `useMemo` and Web Workers for performance.
</details>
<hr/>

### ❓ Q48. **How do you prevent Cross-Site Scripting (XSS) in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

React automatically escapes variables in JSX, preventing most XSS attacks. However, avoid using `dangerouslySetInnerHTML` unless absolutely necessary, and always sanitize the content first using a library like `DOMPurify`.

> 💡 **Interviewer Focus:** Security awareness in React development.
</details>
<hr/>

### ❓ Q49. **How would you implement a custom `useLocalStorage` hook?**
<details>
<summary><b>👀 Show Answer</b></summary>

```javascript
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    const item = window.localStorage.getItem(key);
    return item ? JSON.parse(item) : initialValue;
  });

  const setValue = value => {
    setStoredValue(value);
    window.localStorage.setItem(key, JSON.stringify(value));
  };

  return [storedValue, setValue];
}
```

> 💡 **Interviewer Focus:** Ability to write useful custom hooks combining state and side effects.
</details>
<hr/>

### ❓ Q50. **How do you handle localized text (i18n) in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use a library like `react-i18next` or `formatjs`. They provide hooks and components to translate strings based on the current locale, which can be stored in Redux or Context.

> 💡 **Interviewer Focus:** Familiarity with localization ecosystems.
</details>
<hr/>

### ❓ Q51. **What is "Prop Drilling" and how do you avoid it?**
<details>
<summary><b>👀 Show Answer</b></summary>

Prop drilling is the process of passing props through multiple levels of components just to get them to a deeply nested component. Avoid it by using the Context API, Redux, or component composition (passing components as props).

**🏢 Industry Example:**  
Imagine a **Food Delivery App**. The `App` component holds the `userId`. The user is viewing a `RestaurantPage`, which renders a `MenuList`, which renders a `CategorySection`, which renders a `MenuItem`, which finally renders an `AddToCartButton`. Passing `userId` through 5 layers just so the button can make an API call is Prop Drilling. In industry, we either use Redux so the `AddToCartButton` can fetch `userId` directly from the store, or we use component composition (passing the button itself as a prop (`children`)) so intermediate components don't need to know about the props.

> 💡 **Interviewer Focus:** Understanding clean architecture and state distribution.
</details>
<hr/>

### ❓ Q52. **How would you implement a "Pull to Refresh" feature?**
<details>
<summary><b>👀 Show Answer</b></summary>

Listen to touch events (`onTouchStart`, `onTouchMove`, `onTouchEnd`) on a container. Calculate the pull distance. If it exceeds a threshold, trigger the data fetch and show a loading spinner. (In React Native, use the built-in `RefreshControl`).

> 💡 **Interviewer Focus:** Handling touch gestures and state.
</details>
<hr/>

### ❓ Q53. **How do you structure folders in a large React project?**
<details>
<summary><b>👀 Show Answer</b></summary>

For large-scale React applications, folder structures based purely on file type (e.g. all hooks in `/hooks`, all components in `/components`) quickly break down because developers have to hop between 5 different folders to make changes to a single feature.

Instead, the industry standard is to use a **Feature-Based (Domain-Driven) / Hybrid Structure** with **Co-location**.

---

### 1. 📂 Structure by Type (For Small/Medium Projects)
This is organized by technical concerns. Good for small apps, but leads to high file-hopping in large projects.

```text
src/
├── assets/             # Images, fonts, SVG assets
├── components/         # Shared global UI components (Button, Input)
├── hooks/              # Global custom hooks (useAuth, useLocalStorage)
├── pages/              # Page view components
├── store/              # Redux slices and config
├── utils/              # Helper functions (formatting, validation)
└── App.jsx
```

---

### 2. 🚀 Feature-Based / Hybrid Structure (Recommended for Large Projects)
This organizes folders around business domains/features (e.g. `auth`, `products`, `cart`). Each feature folder contains its own local components, hooks, slices, and tests.

```text
src/
├── assets/                 # Shared static assets (logos, icons)
├── components/             # App-wide shared UI elements (Layout, Button, Modal)
├── config/                 # Environment variables, third-party API configs
├── context/                # App-wide global contexts (ThemeContext)
├── utils/                  # Shared helper utilities (date formatters)
│
├── features/               # ◄── Core business logic domains
│   ├── auth/               # Auth feature domain
│   │   ├── components/     # Local components (LoginForm, SignupForm)
│   │   ├── hooks/          # Local hooks (useSession)
│   │   ├── services/       # Local API queries / RTK endpoints
│   │   ├── authSlice.js    # Local Redux Slice
│   │   └── index.js        # Public API / Barrel file for auth module
│   │
│   ├── products/           # Products feature domain
│   │   ├── components/     # ProductCard, ProductGrid
│   │   ├── hooks/          # useProductDetails
│   │   └── ProductPage.jsx # Parent Page component for products
│   │
│   └── cart/               # Cart feature domain
│
├── routes/                 # App routing configuration
├── store/                  # Root Redux store configuration
└── App.jsx
```

---

### 3. ⚠️ Key Architectural Concepts

#### **A. Co-location**
Keep files close to where they are used. If a sub-component (`ProductCardItem`) or a test file is only used inside the `ProductGrid` component, store them in the same directory rather than splitting them up.
```text
components/
└── ProductGrid/
    ├── ProductGrid.jsx
    ├── ProductGrid.test.jsx
    ├── ProductGrid.module.css
    └── ProductCardItem.jsx      # Child component kept close
```

#### **B. Barrel Files (`index.js`)**
Use an `index.js` file inside the root of each feature or component folder to export its public API. This keeps import paths clean:
*   **Instead of:** `import LoginForm from '@/features/auth/components/LoginForm'`
*   **You import:** `import { LoginForm } from '@/features/auth'`

#### **C. Path Aliasing**
Avoid relative path hell (`../../../../components/Button`). Configure Webpack/Vite and tsconfig to use path aliases like `@/` to reference the root `src` directory:
```javascript
// Clean, maintainable imports
import { Button } from '@/components';
import { useAuth } from '@/features/auth';
```

---

> 💡 **Interviewer Focus:** Explain that technical-type folder structures scale poorly. Champion the **feature-based directory design** based on co-location, explain public APIs using **barrel exports (`index.js`)**, and mention **path aliasing** (`@/`) to demonstrate scale readiness.
</details>
<hr/>

### ❓ Q54. **What is the difference between `npm` and `yarn?**
<details>
<summary><b>👀 Show Answer</b></summary>

Both are package managers. Yarn was created to solve speed and security issues in early npm versions. Today, both are very similar in speed and features, but Yarn has features like workspaces for monorepos, and npm has a massive registry.

> 💡 **Interviewer Focus:** General frontend tooling knowledge.
</details>
<hr/>

### ❓ Q55. **How would you share state between two browser tabs in a React app?**
<details>
<summary><b>👀 Show Answer</b></summary>

Sharing state or communicating between multiple tabs of the **same origin** (domain and port) is a common requirement for syncing carts, themes, or user authentication status.

Here are the three primary methods to implement this:

---

### 1. 📢 Method 1: The `BroadcastChannel` API (Modern & Recommended)
The `BroadcastChannel` API is designed specifically for one-to-many communication between different browser tabs, windows, iframes, or Web Workers under the same origin. It behaves like a clean publish-subscribe system.

#### **Code Example:**
```javascript
import React, { useEffect, useState } from 'react';

function ThemeSync() {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    // 1. Create/join a channel named 'theme_channel'
    const channel = new BroadcastChannel('theme_channel');

    // 2. Listen for messages from other tabs
    channel.onmessage = (event) => {
      const { type, payload } = event.data;
      if (type === 'SET_THEME') {
        setTheme(payload);
      }
    };

    return () => {
      channel.close(); // Clean up on unmount
    };
  }, []);

  const changeTheme = (newTheme) => {
    setTheme(newTheme);

    // 3. Broadcast the change to all other tabs
    const channel = new BroadcastChannel('theme_channel');
    channel.postMessage({ type: 'SET_THEME', payload: newTheme });
  };

  return <button onClick={() => changeTheme('dark')}>Go Dark</button>;
}
```

---

### 🗄️ Method 2: The `storage` Event Listener (Classic & Bulletproof)
When a tab writes data to **`localStorage`**, the browser fires a **`storage`** event on the `window` object of **all other open tabs** of the same origin (but *not* the tab that triggered the change). 

This is highly reliable for syncing state like shopping carts or logout events.

#### **Code Example:**
```javascript
import React, { useEffect, useState } from 'react';

function CartSync() {
  const [cart, setCart] = useState([]);

  useEffect(() => {
    const handleStorageChange = (event) => {
      // Listen specifically for the 'cart' key
      if (event.key === 'cart' && event.newValue) {
        setCart(JSON.parse(event.newValue)); // Sync state in this tab
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const updateCart = (newCart) => {
    setCart(newCart);
    // Writing to localStorage automatically alerts all other tabs
    localStorage.setItem('cart', JSON.stringify(newCart));
  };
}
```

---

### ⚙️ Method 3: Shared Workers (For Complex Background Work)
A **Shared Worker** is a single JavaScript background thread that can be accessed by multiple tabs/windows under the same origin. 
*   **Best Use Case:** When you need a single centralized state coordinator (e.g. keeping **only one active WebSocket connection** open for all tabs to share, instead of opening 10 sockets for 10 tabs).
*   **How it works:** The tabs connect to the Shared Worker using `new SharedWorker('worker.js')` and communicate with it using `port.postMessage()` and `port.onmessage`.

---

### ⚖️ Comparison Table

| Method | Best For | Browser Support | Complexity |
| :--- | :--- | :--- | :--- |
| **`BroadcastChannel`** | Real-time messages, state sync, temporary events. | Modern browsers (96%+). | Very Low (Clean API). |
| **`storage` Event** | Persistent data syncing (carts, user session logs). | Universal (Legacy + Modern). | Very Low. |
| **Shared Workers** | Centralized networking (WebSockets), heavy calculations. | Firefox & Chrome (Safari lacks support). | High (Requires external JS worker file). |

---

> 💡 **Interviewer Focus:** Highlight the **BroadcastChannel API** as the modern standard. Detail the **LocalStorage `storage` event listener** as a highly reliable fallback for session syncing (e.g., logging out of one tab logs out all tabs). Mention **Shared Workers** for complex networking optimizations.
</details>
<hr/>

### ❓ Q56. **How do you handle large file uploads with progress in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

For handling file uploads with progress indicators in React, the implementation depends on the file size.

---

### 1. 📊 Method 1: Standard Upload Progress (For files < 50MB)
The native `fetch` API **does not support upload progress tracking** (it only supports reading download streams). To track upload progress, you must use **Axios** (which wraps browser `XMLHttpRequest`) or native `XMLHttpRequest`.

#### **Code Example (using Axios):**
```javascript
import React, { useState } from 'react';
import axios from 'axios';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('/api/upload', formData, {
        // Axios hooks into XHR's upload progress event
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setProgress(percentCompleted); // Update React progress bar state
        },
      });
      alert('Upload completed!');
    } catch (err) {
      console.error('Upload failed', err);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={uploadFile}>Upload</button>
      <div style={{ width: '100%', bg: '#eee' }}>
        <div style={{ width: `${progress}%`, height: '10px', background: 'green' }} />
      </div>
      <span>{progress}%</span>
    </div>
  );
}
```

---

### 🗃️ Method 2: Chunked Uploads (For Large Files/GBs)
For extremely large files (e.g. videos or high-res graphics), uploading in a single request is highly vulnerable to network timeouts or dropouts. The enterprise standard is **Chunked / Resumable Uploads**.

#### **How it works:**
1.  **Slice the File:** Use the browser's native `File.prototype.slice()` (derived from `Blob`) to split the file into small chunks (e.g. 5MB each).
2.  **Upload Sequentially/Concurrently:** Upload each chunk as a separate HTTP request with headers specifying `chunkIndex`, `totalChunks`, and a unique `fileId`.
3.  **Merge on Server:** Once the server receives all chunks, it merges them back into the original file.
4.  **Resumability (Bonus):** If the network drops at chunk 40 out of 100, the client can ask the server which chunk it last saved, and resume from chunk 41 instead of restarting the entire upload.

#### **Client-side Slicing Code:**
```javascript
const uploadInChunks = async (file) => {
  const CHUNK_SIZE = 5 * 1024 * 1024; // 5MB chunks
  const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
  const fileId = `${file.name}-${file.size}`; // Unique identifier

  for (let index = 0; index < totalChunks; index++) {
    const start = index * CHUNK_SIZE;
    const end = Math.min(start + CHUNK_SIZE, file.size);
    
    // Slice file to create a chunk (in-memory Blob reference, very light)
    const chunk = file.slice(start, end);

    const formData = new FormData();
    formData.append('chunk', chunk);
    formData.append('chunkIndex', index);
    formData.append('totalChunks', totalChunks);
    formData.append('fileId', fileId);

    // Upload current chunk
    await axios.post('/api/upload-chunk', formData);

    // Calculate overall progress
    const currentProgress = Math.round(((index + 1) / totalChunks) * 100);
    setProgress(currentProgress);
  }
};
```

---

### ⚠️ Best Practices for File Uploads
*   **Do not load the entire file into JS memory:** `file.slice()` does not load the chunk into memory; it only references the slice boundaries, keeping the browser memory footprints very low.
*   **Security (Sanitization):** Always validate file headers/MIME types on the **backend**, not just frontend validation, to prevent malicious script uploads.
*   **Use Protocols:** In production, consider standard protocols like **TUS** (resumable upload protocol) using client wrappers like `tus-js-client` or libraries like **Uppy**.

---

> 💡 **Interviewer Focus:** Point out that native **`fetch` does not support upload progress**. Detail **Axios's `onUploadProgress`** (XHR under the hood). Demonstrate conceptual mastery by detailing **file chunking (`file.slice()`)** and how to handle **resumable network failures** at scale.
</details>
<hr/>

### ❓ Q57. **How would you implement an "Infinite Scroll"?**
<details>
<summary><b>👀 Show Answer</b></summary>

Implementing an infinite scroll in React can be done in two ways, but only one is recommended for modern web performance.

---

### 1. ❌ The Traditional Way: Scroll Event Listeners (Not Recommended)
This involves attaching a listener to the `window` scroll event and checking how close the user is to the bottom of the page.

*   **Why it is bad:** 
    *   The `scroll` event fires continuously (hundreds of times per second), overloading the main thread.
    *   Accessing measurements like `window.scrollY` or `offsetHeight` forces the browser to run synchronous layout calculations (**layout thrashing**), causing scroll lag (jank).
    *   Requires manual throttling/debouncing to remain somewhat performant.

---

### 2.  The Modern Way: The Intersection Observer API (Recommended)
The **Intersection Observer API** allows you to asynchronously monitor if a DOM element (the "sentinel") intersects with another element or the browser's viewport.

#### **How it works:**
1.  Place a hidden `div` (the sentinel/indicator) at the very bottom of your list (e.g., right under your loader).
2.  Set up an `IntersectionObserver` instance targeting that sentinel.
3.  When the user scrolls and the sentinel enters the viewport, the observer's callback fires asynchronously to load the next page of items.

#### **React Implementation Code:**
```javascript
import React, { useState, useEffect, useRef } from 'react';

function InfiniteScrollList() {
  const [items, setItems] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  
  const sentinelRef = useRef(null); // Reference to the sentinel element

  useEffect(() => {
    // 1. If we are currently loading or have no more pages, do not observe
    if (loading || !hasMore) return;

    // 2. Define the observer callback
    const observer = new IntersectionObserver((entries) => {
      const sentinel = entries[0];
      if (sentinel.isIntersecting) {
        setPage((prevPage) => prevPage + 1); // Trigger fetch of next page
      }
    }, {
      root: null, // Defaults to the browser viewport
      threshold: 0.1 // Fires when 10% of the sentinel is visible
    });

    // 3. Start observing the sentinel node
    if (sentinelRef.current) {
      observer.observe(sentinelRef.current);
    }

    // 4. Cleanup: Unobserve/disconnect on unmount or hook dependency changes
    return () => {
      observer.disconnect();
    };
  }, [loading, hasMore]);

  // Trigger data fetching whenever page changes
  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      const newItems = await fetchItemsFromAPI(page);
      
      if (newItems.length === 0) {
        setHasMore(false); // Stop observing since database is exhausted
      } else {
        setItems((prev) => [...prev, ...newItems]);
      }
      setLoading(false);
    };

    loadData();
  }, [page]);

  return (
    <div>
      <ul>
        {items.map((item) => <li key={item.id}>{item.name}</li>)}
      </ul>
      
      {/* 5. The Sentinel Element */}
      <div ref={sentinelRef} style={{ height: '20px' }}>
        {loading && <p>Loading next page...</p>}
      </div>
    </div>
  );
}
```

---

### 3. ⚠️ Key Edge Cases to Handle
*   **Loading State Lock:** Always wrap your fetching logic in a `loading` flag. If the user scrolls up and down quickly, the observer might fire multiple times, triggering duplicate API calls for the same page.
*   **Double-triggering on Mount:** If your initial API payload is very short (e.g. only 2 items) and doesn't push the sentinel off-screen, the sentinel will remain in the viewport, immediately triggering page 2. Ensure your default page limit is large enough to push the sentinel below the fold.
*   **Cleanups:** Always run `observer.disconnect()` in the `useEffect` cleanup return statement to prevent memory leaks.

---

> 💡 **Interviewer Focus:** Explain **Layout Thrashing** and why window scroll listeners are bad for performance. Explain **Intersection Observer** as an asynchronous, layout-safe alternative. Detail **loading state locks** and **sentinel elements** in your code walk.
</details>
<hr/>

### ❓ Q58. **What is a "Higher-Order Component" (HOC)?**
<details>
<summary><b>👀 Show Answer</b></summary>

An HOC is a pure function that takes a component and returns a new component. It is a pattern derived from React's compositional nature.
```javascript
const EnhancedComponent = withLogging(MyComponent);
```

> 💡 **Interviewer Focus:** Used for cross-cutting concerns (auth, logging).
</details>
<hr/>

### ❓ Q59. **Why might you use `useReducer` instead of `useState`?**
<details>
<summary><b>👀 Show Answer</b></summary>

`useReducer` is usually preferable when you have complex state logic that involves multiple sub-values or when the next state depends on the previous one. It also lets you optimize performance for components that trigger deep updates because you can pass `dispatch` down instead of callbacks.

> 💡 **Interviewer Focus:** State management complexity.
</details>
<hr/>

### ❓ Q60. **How do you mock an API call in Jest?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `jest.mock('axios')` or `jest.spyOn`.
```javascript
axios.get.mockResolvedValue({ data: { name: 'Test' } });
```

> 💡 **Interviewer Focus:** Testing skills and isolation of units.
</details>
<hr/>

### ❓ Q61. **What is code splitting and how do you do it in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

Code splitting allows you to split your bundle into smaller chunks which can then be loaded on demand. In React, this is done using `React.lazy()` and `Suspense`.

> 💡 **Interviewer Focus:** Performance optimization for initial load time.
</details>
<hr/>

### ❓ Q62. **How do you handle cleanup in `useEffect`?**
<details>
<summary><b>👀 Show Answer</b></summary>

Return a function from the effect. This function runs before the component unmounts and before the effect re-runs (if dependencies changed).

> 💡 **Interviewer Focus:** Preventing memory leaks.
</details>
<hr/>

### ❓ Q63. **What is Strict Mode in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

A tool for highlighting potential problems in an application. It does not render any visible UI. It activates additional checks and warnings for its descendants (e.g., identifying unsafe lifecycles, warning about legacy string ref API). In React 18, it mounts components twice in dev mode to help find effect bugs.

> 💡 **Interviewer Focus:** Awareness of development tools and React 18 behavior.
</details>
<hr/>

### ❓ Q64. **How would you test if a button click calls a function?**
<details>
<summary><b>👀 Show Answer</b></summary>

Create a mock function using `jest.fn()`. Pass it as a prop to the component. Use React Testing Library to find the button and simulate a click. Expect the mock function to have been called.

> 💡 **Interviewer Focus:** Basic RTL and Jest usage.
</details>
<hr/>

### ❓ Q65. **What are synthetic events in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

React implements a synthetic event system to ensure events have consistent properties across different browsers. It is a cross-browser wrapper around the browser’s native event.

> 💡 **Interviewer Focus:** Cross-browser compatibility handling.
</details>
<hr/>

### ❓ Q66. **How do you access the DOM element directly in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

By using the `useRef` hook. You attach the ref to the JSX element via the `ref` prop.

> 💡 **Interviewer Focus:** Correct use of refs for DOM manipulation when necessary.
</details>
<hr/>

### ❓ Q67. **What is the difference between a functional and a class component?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Functional:** Just a JS function that returns JSX. Uses hooks for state and lifecycle. Simpler and preferred in modern React.
- **Class:** ES6 class extending `React.Component`. Uses `this.state` and lifecycle methods. Legacy but still supported.

> 💡 **Interviewer Focus:** Modern React leans heavily towards functional components.
</details>
<hr/>

### ❓ Q68. **What is hydration in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

Hydration is the process of React attaching event listeners to the HTML that was rendered on the server, making the static page interactive.

> 💡 **Interviewer Focus:** Understanding SSR and client-side transition.
</details>
<hr/>

### ❓ Q69. **How do you pass data from a child to a parent component?**
<details>
<summary><b>👀 Show Answer</b></summary>

Pass a function from the parent to the child as a prop. The child calls this function and passes the data as an argument.

> 💡 **Interviewer Focus:** Basic React data flow (unidirectional).
</details>
<hr/>

### ❓ Q70. **What is the difference between `React.createElement` and JSX?**
<details>
<summary><b>👀 Show Answer</b></summary>

JSX is syntactic sugar for `React.createElement`. Babel transpiles JSX into `React.createElement` calls.

> 💡 **Interviewer Focus:** JSX is not magic, it's just a nicer syntax for JS calls.
</details>
<hr/>

### ❓ Q71. **What is the difference between `useTransition` and `useDeferredValue` in React 18?**
<details>
<summary><b>👀 Show Answer</b></summary>

Both are concurrent features used to prioritize UI updates:
- **`useTransition`:**
  - Used when you have access to the state-updating code.
  - Returns a pending state variable and a startTransition function to wrap state updates.
  - Marks state updates as non-urgent (e.g. filtering a long list).
- **`useDeferredValue`:**
  - Used when you receive a value from a parent prop and do not have access to the state setter.
  - Returns a deferred version of the value that lags behind the fast updates, preventing stuttering in children.

> 💡 **Interviewer Focus:** When to choose input transition wrappers vs property deferrals.
</details>
<hr/>

### ❓ Q72. **Explain React 18's Automatic Batching.**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Legacy React:** Batched state updates only inside React event handlers. Updates inside promises, timeouts, or native event handlers triggered separate re-renders.
- **React 18 Automatic Batching:** Batches multiple state updates into a single re-render, regardless of where they originate (inside promises, timeouts, or async callbacks), optimizing rendering performance.

> 💡 **Interviewer Focus:** Performance advantages and how to opt-out using `flushSync` when immediate DOM updates are required.
</details>
<hr/>

### ❓ Q73. **Explain the execution sequence of React Strict Mode double rendering.**
<details>
<summary><b>👀 Show Answer</b></summary>

In development mode, React Strict Mode double-invokes components, lifecycle methods, and state setter functions:
- **Purpose:** To detect side effects and impure render logic (e.g., mutating local variables or modifying global state during rendering).
- **Behavior:** Pure functions yield identical outputs on double rendering, but impure code causes noticeable differences, helping catch bugs before production.

> 💡 **Interviewer Focus:** Identifying side effects and understanding that double rendering is disabled in production builds.
</details>
<hr/>

### ❓ Q74. **What are the limits of Error Boundaries in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

Error Boundaries (components implementing `getDerivedStateFromError` or `componentDidCatch`) catch rendering errors, but **cannot** catch:
- Errors inside Event Handlers (e.g. button click exceptions).
- Asynchronous code (e.g. `setTimeout` or `fetch` callbacks).
- Server-side rendering errors.
- Errors thrown in the Error Boundary component itself.

> 💡 **Interviewer Focus:** Error boundaries boundaries and handling event errors with try/catch.
</details>
<hr/>

### ❓ Q75. **What is the difference between React Server Components (RSC) and Client Components?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Server Components:** Execute *only* on the server. They can query databases and read file systems directly, and their JS bundle code is never sent to the client, reducing download size.
- **Client Components:** (Marked with `'use client'`). Executed on the server (initial pre-rendering) and hydrated on the client. They support state, effects, and browser APIs.

> 💡 **Interviewer Focus:** Defining boundaries between server-side operations and client hydration.
</details>
<hr/>

### ❓ Q76. **How does the React virtual DOM reconciliation diffing algorithm achieve $O(N)$ complexity?**
<details>
<summary><b>👀 Show Answer</b></summary>

Finding the minimum modifications to transform one tree to another has $O(N^3)$ complexity. React uses two heuristics to reduce this to $O(N)$:
1. **Different Types:** If two elements have different types (e.g. swapping `<div>` for `<span>`), React tears down the entire tree and builds a new one.
2. **Keys:** The `key` prop allows identifying elements across renders, preventing tearing down list elements when items are reordered.

> 💡 **Interviewer Focus:** Diffing heuristics and key props optimization.
</details>
<hr/>

### ❓ Q77. **How do you prevent Context API re-render issues in large apps?**
<details>
<summary><b>👀 Show Answer</b></summary>

If a Context value changes, *all* consumer components re-render, even if they only read a subset of the context object.
- **Mitigation:**
  - **Split Context:** Separate state context from dispatcher context.
  - **Memoization:** Wrap children in `React.memo` or use `useMemo` for the context value.
  - Use state managers (Redux/Zustand) for high-frequency state updates.

> 💡 **Interviewer Focus:** Mitigating context consumer performance bottlenecks.
</details>
<hr/>

### ❓ Q78. **What is the purpose of `forwardRef` and `useImperativeHandle`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **`forwardRef`**: Passes a ref through a component to one of its child elements.
- **`useImperativeHandle`**: Customizes the instance value exposed to parent components when using refs. Allows defining select API methods (like `.focus()` or `.toggle()`) instead of exposing the raw DOM element.

> 💡 **Interviewer Focus:** Encapsulating DOM access and exposing custom component controls.
</details>
<hr/>

### ❓ Q79. **How do you test custom hooks in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the `renderHook` helper from React Testing Library:
```javascript
import { renderHook, act } from '@testing-library/react';
import useCounter from './useCounter';

test('should increment counter', () => {
  const { result } = renderHook(() => useCounter());
  act(() => {
    result.current.increment();
  });
  expect(result.current.count).toBe(1);
});
```
- Wrap state-modifying actions inside the `act()` block to ensure state changes propagate before assertions run.

> 💡 **Interviewer Focus:** Writing isolated hook tests using `renderHook` and `act()`.
</details>
<hr/>

### ❓ Q80. **What is Redux Thunk and how does it handle asynchronous actions?**
<details>
<summary><b>👀 Show Answer</b></summary>

Redux Thunk is a middleware that allows writing action creators that return a **function (thunk)** instead of an action object.
- **How it works:**
  - The middleware intercepts actions.
  - If the action is a function, Thunk calls it, passing `dispatch` and `getState` arguments.
  - The function executes async calls (fetch APIs) and dispatches standard synchronous actions when complete.

> 💡 **Interviewer Focus:** Thunk source code structure (it is only ~14 lines of code) and asynchronous logic control.
</details>
<hr/>

### ❓ Q81. **How do you configure RTK Query tag invalidations for auto-caching?**
<details>
<summary><b>👀 Show Answer</b></summary>

RTK Query uses a tag system to automate re-fetching:
- **`providesTags`**: Queries declare tags for the data they return (e.g. `['Post']`).
- **`invalidatesTags`**: Mutations declare which tags they invalidate (e.g. `['Post']` on adding a new post).
- When the mutation runs, RTK Query detects the invalidation and automatically triggers queries subscribed to that tag to refresh data.

> 💡 **Interviewer Focus:** Decoupled data cache synchronization.
</details>
<hr/>

### ❓ Q82. **Explain Redux Reselect selector memoization rules.**
<details>
<summary><b>👀 Show Answer</b></summary>

Reselect's `createSelector` memoizes output:
- It recalculates values only if the input selectors return different values (using reference equality checks `===`).
- If inputs do not change, it returns the cached result, preventing heavy calculations on the store state during re-renders.

> 💡 **Interviewer Focus:** Preventing unnecessary selectors executions.
</details>
<hr/>

### ❓ Q83. **How do you handle WebSocket streaming inside Redux?**
<details>
<summary><b>👀 Show Answer</b></summary>

Do not manage WebSockets directly inside components. Implement them inside a custom **Redux Middleware**:
- The middleware initializes the WebSocket connection during app startup.
- It listens for server events and dispatches Redux actions (`dispatch({ type: 'WS_DATA', payload })`) to update the store state.
- Components dispatch standard actions to send messages over the socket.

> 💡 **Interviewer Focus:** Separation of concerns in state managers.
</details>
<hr/>

### ❓ Q84. **What is the difference between `useLayoutEffect` and `useEffect` rendering queues?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **`useEffect`:** Runs asynchronously **after** the browser paints the screen, preventing blocking UI rendering.
- **`useLayoutEffect`:** Runs synchronously **after** DOM mutations but **before** the browser paints the screen. Use it to measure DOM layouts and execute visual changes before rendering, avoiding visual flicker.

> 💡 **Interviewer Focus:** Rendering sequence queues.
</details>
<hr/>

### ❓ Q85. **What is the performance footprint of CSS-in-JS libraries like Styled Components?**
<details>
<summary><b>👀 Show Answer</b></summary>

Runtime CSS-in-JS libraries:
- Parse styles and inject `<style>` tags into the DOM during runtime.
- This creates CPU overhead on render passes and increases bundle size.
- **Alternative:** Zero-runtime CSS-in-JS (Vanilla Extract, Tailwind) compiles styles to static CSS at build time, improving performance.

> 💡 **Interviewer Focus:** CSS runtime parsing costs.
</details>
<hr/>

### ❓ Q86. **How do you debug memory leaks in React applications?**
<details>
<summary><b>👀 Show Answer</b></summary>

- Use Chrome DevTools heap snapshots to isolate detached DOM nodes.
- Common leaks in React:
  - Not clearing `setInterval` or event listeners inside `useEffect` cleanup functions.
  - Subscribing to observables or sockets without unsubscribing on component unmount.

> 💡 **Interviewer Focus:** Cleanup routines in useEffect lifecycle hooks.
</details>
<hr/>

### ❓ Q87. **What is the role of the dependency array in `useMemo` and `useCallback`?**
<details>
<summary><b>👀 Show Answer</b></summary>

The dependency array tells React when to recalculate the cached value or recreate the function.
- **Warning:** Omitting dependencies causes closures to capture stale variable values (stale closures), causing application logic bugs.

> 💡 **Interviewer Focus:** Stale closure bugs diagnosis.
</details>
<hr/>

### ❓ Q88. **How does React's profiling tool measure rendering performance?**
<details>
<summary><b>👀 Show Answer</b></summary>

Using the React Profiler (API or DevTools):
- Measures compile and rendering durations.
- Identifies "commit times" and lists which component triggered updates, helping locate unnecessary re-renders.

> 💡 **Interviewer Focus:** React Profiler metrics.
</details>
<hr/>

### ❓ Q89. **What are React Portals and what is a typical use case?**
<details>
<summary><b>👀 Show Answer</b></summary>

Portals render children into a DOM node located outside the main parent component hierarchy.
- **Use Case:** Modals, tooltips, or overlays. By rendering them outside parent trees, they escape CSS bounds (like `overflow: hidden` or `z-index` limits) while preserving React event propagation contexts.

> 💡 **Interviewer Focus:** Portal architectures and event bubbles.
</details>
<hr/>

### ❓ Q90. **Explain how RTK Query implements optimistic updates.**
<details>
<summary><b>👀 Show Answer</b></summary>

Optimistic updates update the cache instantly before API requests complete:
1. When a mutation runs, use `onQueryStarted` to manually patch the cache state.
2. If the API request succeeds, do nothing (the cache matches).
3. If the request fails, execute the rollback function returned by the cache patch helper.

> 💡 **Interviewer Focus:** Enhancing user experience latency.
</details>
<hr/>

### ❓ Q91. **What is the difference between shallow copy and deep copy in Redux states update?**
<details>
<summary><b>👀 Show Answer</b></summary>

Redux checks if state has changed using reference checks.
- Modifying nested state in place violates immutability.
- Use shallow copying (spread `{ ...state }`) on the modified branches. Unmodified branches preserve references, avoiding unnecessary re-renders.

> 💡 **Interviewer Focus:** Immutability and reference tracking.
</details>
<hr/>

### ❓ Q92. **How does lazy loading using React.lazy and Suspense optimize bundles?**
<details>
<summary><b>👀 Show Answer</b></summary>

`React.lazy` splits components into separate JS chunks.
- When compiled, these chunks are loaded asynchronously via network requests only when the component is rendered.
- `<Suspense>` manages the loading state, showing a fallback skeleton while the chunk downloads.

> 💡 **Interviewer Focus:** Dynamic code-splitting.
</details>
<hr/>

### ❓ Q93. **What is the difference between Redux Saga and Redux Thunk?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Redux Thunk:** Uses async/await functions. Easy to write and test, but can get messy on complex side-effects orchestration.
- **Redux Saga:** Uses ES6 Generators and declarative effects. Highly testable, runs as a background thread-like loop, and is ideal for complex asynchronous structures (e.g. canceling requests).

> 💡 **Interviewer Focus:** Saga effects (`takeLatest`, `call`, `put`).
</details>
<hr/>

### ❓ Q94. **What is the role of `React.Children` API?**
<details>
<summary><b>👀 Show Answer</b></summary>

Provides utilities (like `React.Children.map` or `React.Children.toArray`) to safely manipulate and inspect the `children` prop array without running into errors if `children` is a single element or function.

> 💡 **Interviewer Focus:** Component utility patterns.
</details>
<hr/>

### ❓ Q95. **How do you prevent XSS when using dangerouslySetInnerHTML?**
<details>
<summary><b>👀 Show Answer</b></summary>

Always sanitize HTML strings using a library like **DOMPurify** before passing them to the prop, removing script tags and javascript execution paths.

> 💡 **Interviewer Focus:** XSS mitigations.
</details>
<hr/>

### ❓ Q96. **What is the difference between ref forwarding and standard prop passing?**
<details>
<summary><b>👀 Show Answer</b></summary>

Standard props do not pass refs to child components.
- Wrap components in `forwardRef` to expose inner DOM elements, allowing parent components to call methods on the inner element.

> 💡 **Interviewer Focus:** Ref delegation.
</details>
<hr/>

### ❓ Q97. **Explain the purpose of the `useSyncExternalStore` hook.**
<details>
<summary><b>👀 Show Answer</b></summary>

A hook designed for state managers (Redux/Zustand) in React 18 to subscribe to external data stores, preventing tearing anomalies under concurrent rendering.

> 💡 **Interviewer Focus:** Concurrent state safety.
</details>
<hr/>

### ❓ Q98. **How do you test components wrapping Context API?**
<details>
<summary><b>👀 Show Answer</b></summary>

Wrap the test component inside the context provider in the test suite:
```javascript
render(
  <MyProvider value={mockValue}>
    <MyComponent />
  </MyProvider>
);
```

> 💡 **Interviewer Focus:** Context mocking patterns.
</details>
<hr/>

### ❓ Q99. **Explain how state batching works under React 17 vs 18.**
<details>
<summary><b>👀 Show Answer</b></summary>

- React 17 only batched state updates inside React native event handlers.
- React 18 implements Automatic Batching across all scopes (including promises, timeouts, and native callbacks), consolidating multiple updates into a single re-render.

> 💡 **Interviewer Focus:** Batching evolutions.
</details>
<hr/>

### ❓ Q100. **What is the role of `useId` hook?**
<details>
<summary><b>👀 Show Answer</b></summary>

Generates unique, stable ID strings that are consistent across server and client renders, preventing hydration mismatch errors on accessibility elements.

> 💡 **Interviewer Focus:** Accessibility hydration optimization.
</details>
<hr/>

### ❓ Q101. **What is Redux Toolkit (RTK) and how does it solve classic Redux boilerplate issues?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
**Redux Toolkit (RTK)** is the official, recommended way to write Redux logic. It was created to address the three common complaints about classic Redux:
1. "Configuring a Redux store is too complicated."
2. "I have to add a lot of packages to get Redux to do anything useful."
3. "Redux requires too much boilerplate code."

---

### 🛠️ Classic Redux vs. Redux Toolkit

#### 1. Store Configuration
*   **Classic Redux:** Required manually configuring middleware, enhancers, compose tools, and setting up Redux DevTools extension bindings.
*   **Redux Toolkit:** `configureStore()` automatically combines your slice reducers, adds default middlewares (like `redux-thunk` for async operations, and dev checks for state mutation/non-serializable values), and turns on Redux DevTools out of the box.

#### 2. Writing Reducer Logic (Immer Integration)
*   **Classic Redux:** Reducers had to be pure functions that did not mutate state. Developers had to write complex nested object copies using the spread operator (`...`).
*   **Redux Toolkit:** `createSlice()` integrates **Immer** under the hood. This allows you to write code that looks like it is "mutating" state directly (e.g. `state.push()`), but Immer automatically translates it into safe, immutable state updates.

**Classic Redux (Manual nesting copy):**
```javascript
case ADD_TODO:
  return {
    ...state,
    todos: [
      ...state.todos,
      { id: action.id, text: action.text, completed: false }
    ]
  };
```

**Redux Toolkit (Mutative-looking syntax with Immer):**
```javascript
const todoSlice = createSlice({
  name: 'todos',
  initialState: [],
  reducers: {
    addTodo: (state, action) => {
      // Immer automatically handles immutable copy operations behind the scenes!
      state.push({ id: action.payload.id, text: action.payload.text, completed: false });
    }
  }
});
```

#### 3. Action Creators and Action Types
*   **Classic Redux:** Required manually defining string action constants (e.g. `const ADD_TODO = 'ADD_TODO'`) and writing separate Action Creator functions.
*   **Redux Toolkit:** `createSlice()` automatically generates corresponding action creators and action types behind the scenes based on your reducer names.

---

> 💡 **Interviewer Focus:**
- Emphasize **Immer** and how it simplifies reducer logic without violating state immutability.
- Explain that **Redux Toolkit is still Redux** under the hood; it is just a set of tools and best practices wrapper.
- Highlight `createSlice` and `configureStore` as the core APIs.

</details>
<hr/>

### ❓ Q102. **What is "Hydration" in React, and how do you resolve a "Hydration Mismatch" error?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
**Hydration** is the process where client-side JavaScript reads the static pre-rendered HTML sent by the server, matches it with the React component structure, and attaches event listeners (like click handlers) to make the page interactive.

---

### 🚨 What is a Hydration Mismatch?
A **Hydration Mismatch** occurs when the HTML rendered on the server is different from the HTML rendered during the first paint on the client. When React runs the hydration phase, it detects this difference and throws an error (e.g., *"Text content did not match..."* or *"Expected server HTML to contain a `<div>` in `<a>`"*).

#### **Common Causes:**
1.  **Directly using client-only variables during SSR:** Using values like `window`, `localStorage`, `document`, or client-specific screen width/height, which are `undefined` on the Node server but defined in the browser.
2.  **Date/Time Stamps:** Using `new Date()` or random values (like `Math.random()`) during rendering. The server renders the date at `12:00:00`, but the client loads the JS and renders it at `12:00:01`, causing a discrepancy.
3.  **Invalid HTML Nesting:** Browsers auto-correct malformed HTML. For example, if you render a `<div>` inside a `<p>` tag (which is invalid HTML), the browser parses it into separate blocks, while React's virtual DOM structure still expects them nested.

---

### 🛠️ Solutions to Resolve Mismatches

#### 1. Use `useEffect` for Client-Side Only Data (Recommended)
Force the client-only rendering to occur *after* the initial hydration has completed:

```javascript
import { useState, useEffect } from 'react';

function MyComponent() {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true); // Runs only in the browser after hydration
  }, []);

  // Server renders the loading state, client renders the client-only value post-hydration
  return (
    <div>
      {isClient ? localStorage.getItem('theme') : 'Loading theme...'}
    </div>
  );
}
```

#### 2. Suppress Warnings (For unavoidable discrepancies)
If a mismatch cannot be avoided (e.g., rendering timestamps), you can suppress the React warning by adding the `suppressHydrationWarning` prop:
```javascript
<span suppressHydrationWarning>
  {new Date().toLocaleTimeString()}
</span>
```
*Note: This only works one level deep, and does not fix underlying layout mismatches.*

#### 3. Disable SSR for Specific Components (Next.js Dynamic Imports)
If a component relies heavily on browser APIs, you can import it dynamically and disable Server-Side Rendering:
```javascript
import dynamic from 'next/dynamic';

const MapComponent = dynamic(() => import('./MapComponent'), {
  ssr: false, // Disables server-side pre-rendering for this component
});
```

---

> 💡 **Interviewer Focus:**
- Define **Hydration** clearly (attaching event listeners to server HTML).
- Discuss the dangers of using client APIs (`window`/`localStorage`) during initial render.
- Explain the role of `useEffect` to safely shift browser-specific rendering to the client.

</details>
<hr/>

### ❓ Q103. **What are the new hooks and features introduced in React 19?**
<details>
<summary><b>👀 Show Answer</b></summary>

**Answer:**
React 19 introduces several enhancements focused on simplifying asynchronous states, forms, and performance optimization:

---

### 1. Actions (Asynchronous State Management)
React 19 introduces native support for **Actions**—functions that execute async operations (like API calls) inside event handlers. React automatically handles pending states, errors, and sequential execution.

```javascript
// Before React 19: Manual isLoading state tracking
const [isPending, setIsPending] = useState(false);
const handleClick = async () => {
  setIsPending(true);
  await updateData();
  setIsPending(false);
};

// React 19: Using transitions for automatic pending state tracking
const [isPending, startTransition] = useTransition();
const handleClick = () => {
  startTransition(async () => {
    await updateData(); // React tracks this async lifecycle automatically
  });
};
```

---

### 2. New Hooks in React 19

#### A. `useActionState` (Formerly `useFormState`)
Designed specifically for handling HTML form actions. It takes a form submission function and returns the state (response) and a form dispatch trigger. It automatically tracks `isPending`.
```javascript
const [state, formAction, isPending] = useActionState(
  async (prevState, formData) => {
    const error = await updateProfile(formData.get("username"));
    if (error) return error;
    return "Profile updated successfully!";
  },
  null
);

return (
  <form action={formAction}>
    <input type="text" name="username" />
    <button type="submit" disabled={isPending}>Update</button>
    {state && <p>{state}</p>}
  </form>
);
```

#### B. `useFormStatus`
Eliminates passing props manually to deep child elements inside forms. It behaves like a Context reader, accessing parent form status (like `pending`).
```javascript
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus(); // Reads status of parent form element
  return <button type="submit" disabled={pending}>Submit</button>;
}
```

#### C. `useOptimistic`
Used to render optimistic UI updates during asynchronous actions, making the interface feel faster. If the request fails, React rolls back the state automatically.
```javascript
// Returns optimisticState and a function to trigger the optimistic update
const [optimisticTodos, addOptimisticTodo] = useOptimistic(
  todos,
  (state, newTodo) => [...state, { text: newTodo, pending: true }]
);
```

#### D. The `use` API
A new API that allows reading Promises or Context inline. Unlike React hooks, `use` can be called inside conditional statements and loops.
```javascript
import { use } from 'react';

function WeatherWidget({ weatherPromise }) {
  // Suspends component until the promise resolves
  const weather = use(weatherPromise); 
  return <p>Temperature: {weather.temp}°C</p>;
}
```

---

### 3. The React Compiler (React Forget)
Perhaps the biggest architectural change: React 19 introduces a build-time **React Compiler**.
*   **What it does:** Automatically memoizes components, props, and dependencies.
*   **Why it matters:** It renders manually caching values/callbacks with `useMemo` and `useCallback` largely obsolete. React automatically optimizes rendering performance.

---

> 💡 **Interviewer Focus:**
- Contrast React 19's **Actions** with manual loading state boilerplate.
- Detail the purpose of `useActionState`, `useFormStatus`, and `useOptimistic` in modern form designs.
- Highlight the **React Compiler** as the future of automatic rendering performance optimizations.

</details>
<hr/>

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ Node.js](./02_Nodejs.md) | [Home](./00_Index.md) | [➡️ Next.js](./04_Nextjs.md) |
