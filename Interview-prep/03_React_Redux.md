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

Hooks are functions that let you "hook into" React state and lifecycle features from function components. They were introduced in React 16.8 and allow you to use state and other React features without writing a class component.

**Why were they introduced? (Problems they solved):**
1. **Reuse stateful logic:** Before hooks, sharing stateful logic required patterns like Render Props or Higher-Order Components (HOCs), which led to "wrapper hell" (deeply nested component trees).
2. **Complex components became hard to understand:** Lifecycle methods often contained a mix of unrelated logic (e.g., `componentDidMount` might handle data fetching AND event listeners). Hooks let you split one component into smaller functions based on what pieces are related.
3. **Classes are confusing:** Humans and machines struggle with classes (e.g., understanding `this`, binding event handlers, difficulty with minification and hot reloading).

**Core Hooks to Know:**
- `useState`: Manages local state in a functional component.
- `useEffect`: Handles side effects (API calls, subscriptions, timers) - replaces lifecycle methods.
- `useContext`: Subscribes to React context without nesting.
- `useReducer`: An alternative to `useState` for complex state logic.
- `useMemo` & `useCallback`: For performance optimization (memoizing values and functions).
- `useRef`: For accessing DOM elements or persisting values across renders without triggering re-renders.

**Rules of Hooks:**
1. **Only call Hooks at the top level:** Don't call Hooks inside loops, conditions, or nested functions.
2. **Only call Hooks from React functions:** Call them from React function components or custom Hooks.

> 💡 **Interviewer Focus:** Emphasize how hooks solve "wrapper hell", allow better logic reuse, and make code cleaner. Mentioning the Rules of Hooks is a strong signal.
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

Reconciliation is the process through which React updates the real DOM. When a component's props or state change, React creates a new Virtual DOM tree and compares it with the previous one. This process of comparing two trees is called **Diffing**.

A full tree comparison has a complexity of $O(n^3)$. To make it performant, React uses a heuristic algorithm with $O(n)$ complexity based on two main assumptions:

**1. Two elements of different types will produce different trees.**
- If a `<div>` is replaced by a `<span>`, React will tear down the old tree (and its state) and build the new one from scratch.

**2. The developer can hint at which child elements are stable across renders with a `key` prop.**
- This is crucial for lists. Keys help React identify which items were added, removed, or reordered.

**How the Diffing Algorithm Works:**
- **Elements Of Different Types:** React tears down the old tree and builds the new tree from scratch. Component instances are destroyed and unmounted.
- **DOM Elements Of The Same Type:** React looks at the attributes of both, keeps the same underlying DOM node, and only updates the changed attributes (e.g., changing `className` or `style`).
- **Component Elements Of The Same Type:** React updates the props of the underlying component instance to match the new element, and calls `render` on it.

> 💡 **Interviewer Focus:** Understanding that React doesn't do a full tree comparison for performance reasons. Mentioning the $O(n)$ heuristic algorithm, "Diffing", and the importance of `keys` are key indicators of a strong candidate.
</details>
<hr/>

### ❓ Q13. **What is the Context API and when should you use it?**
<details>
<summary><b>👀 Show Answer</b></summary>

Context provides a way to pass data through the component tree without having to pass props down manually at every level (Prop Drilling). Use it for data that can be considered "global" for a tree of React components, such as the current authenticated user, theme, or preferred language.

> 💡 **Interviewer Focus:** Use Context for low-frequency updates (theme, locale) to avoid performance issues with frequent re-renders.
</details>
<hr/>

### ❓ Q14. **What is the difference between `useMemo` and `useCallback`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `useMemo` returns a **memoized value**. It only recalculates the value when one of the dependencies has changed.
- `useCallback` returns a **memoized callback function**. It is useful when passing callbacks to optimized child components that rely on reference equality to prevent unnecessary renders.

> 💡 **Interviewer Focus:** `useMemo` is for values, `useCallback` is for functions. Both are for optimization.
</details>
<hr/>

### ❓ Q15. **What are Custom Hooks and why would you use them?**
<details>
<summary><b>👀 Show Answer</b></summary>

Custom Hooks are JavaScript functions whose names start with "use" and that may call other Hooks. They allow you to extract component logic into reusable functions.
**Why:** To share logic between components without adding more components to your tree (unlike HOCs or render props).

> 💡 **Interviewer Focus:** Sharing stateful logic, not state itself.
</details>
<hr/>

### ❓ Q16. **How do you handle error boundaries in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

Error boundaries are React components that catch JavaScript errors anywhere in their child component tree, log those errors, and display a fallback UI instead of the component tree that crashed.
They are implemented using class components with `static getDerivedStateFromError()` or `componentDidCatch()`.

> 💡 **Interviewer Focus:** Note that error boundaries cannot be created using functional components and hooks yet.
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

Middleware provides a third-party extension point between dispatching an action and the moment it reaches the reducer. It is used for logging, crash reporting, talking to an asynchronous API, routing, etc.
**Examples:** Redux Thunk, Redux Saga.

> 💡 **Interviewer Focus:** Understanding that middleware intercepts actions.
</details>
<hr/>

### ❓ Q19. **What is Redux Thunk?**
<details>
<summary><b>👀 Show Answer</b></summary>

Redux Thunk is a middleware that allows you to write action creators that return a function instead of an action. The thunk can be used to delay the dispatch of an action, or to dispatch only if a certain condition is met. This is ideal for async operations like fetching data.

> 💡 **Interviewer Focus:** Essential for handling side effects in Redux without Saga.
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

React Fiber is the reconciliation engine introduced in React 16. Its main goal is to enable incremental rendering of the virtual DOM. It allows React to:
- Pause work and come back to it later.
- Assign priority to different types of work.
- Reuse previously completed work or abort it if not needed.

> 💡 **Interviewer Focus:** Mention "time-slicing" and "prioritization" of updates (e.g., user input has higher priority than data fetching).
</details>
<hr/>

### ❓ Q22. **What are the common pitfalls of `useEffect`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- **Infinite loops:** Caused by updating state that is also a dependency.
- **Stale closures:** Using state or props inside `useEffect` without including them in the dependency array.
- **Memory leaks:** Forgetting to return a cleanup function (e.g., for event listeners or timers).

> 💡 **Interviewer Focus:** Look for solutions like using functional state updates or `useRef` to avoid dependency issues.
</details>
<hr/>

### ❓ Q23. **Explain the concept of "Lifting State Up".**
<details>
<summary><b>👀 Show Answer</b></summary>

When several components need to reflect the same changing data, it is recommended to lift the shared state up to their closest common ancestor. This ensures a single source of truth and keeps components in sync.

> 💡 **Interviewer Focus:** Classic React pattern for sharing data between sibling components.
</details>
<hr/>

### ❓ Q24. **How do you optimize a React application with too many re-renders?**
<details>
<summary><b>👀 Show Answer</b></summary>

1. Use `React.memo` for pure functional components.
2. Use `useMemo` and `useCallback` to prevent unnecessary recalculations and reference changes.
3. Move state down to where it is needed instead of putting everything in top-level context or state.
4. Use windowing/lazy loading for large lists (e.g., `react-window`).

> 💡 **Interviewer Focus:** Practical performance optimization strategies.
</details>
<hr/>

### ❓ Q25. **What is the difference between `useLayoutEffect` and `useEffect`?**
<details>
<summary><b>👀 Show Answer</b></summary>

- `useEffect` runs **asynchronously** after the browser has painted the screen.
- `useLayoutEffect` runs **synchronously** after all DOM mutations but before the browser paints. Use it when you need to make DOM measurements and visual changes before the user sees them to prevent flickering.

> 💡 **Interviewer Focus:** `useLayoutEffect` can block visual updates, so use it sparingly.
</details>
<hr/>

### ❓ Q26. **How does Redux Toolkit (RTK) improve on standard Redux?**
<details>
<summary><b>👀 Show Answer</b></summary>

RTK simplifies Redux by:
- Reducing boilerplate code (creates actions and reducers simultaneously via `createSlice`).
- Including Redux Thunk by default.
- Using Immer under the hood, allowing you to write "mutative" code that is actually immutable.
- Providing `configureStore` with good defaults (DevTools, middleware).

> 💡 **Interviewer Focus:** RTK is the modern standard for Redux. Knowing Immer integration is a plus.
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

I would use **Windowing** or **Virtualization**. Instead of rendering all 10,000 DOM nodes, I would only render the items currently visible in the viewport. Libraries like `react-window` or `react-virtualized` are perfect for this.

> 💡 **Interviewer Focus:** Knowledge of performance bottlenecks with large DOMs and virtualization libraries.
</details>
<hr/>

### ❓ Q36. **How would you handle a race condition where a slower previous API request overwrites a faster subsequent request?**
<details>
<summary><b>👀 Show Answer</b></summary>

I would use an ignore flag in `useEffect` or an `AbortController`.
```javascript
useEffect(() => {
  let active = true;
  fetchData().then(data => {
    if (active) setData(data);
  });
  return () => { active = false; };
}, [query]);
```

> 💡 **Interviewer Focus:** Handling asynchronous consistency in React effects.
</details>
<hr/>

### ❓ Q37. **How do you persist Redux state across page reloads?**
<details>
<summary><b>👀 Show Answer</b></summary>

I would use `redux-persist`, or manually subscribe to the store and save the state to `localStorage` or `sessionStorage` on changes, and load it as the `preloadedState` when creating the store.

> 💡 **Interviewer Focus:** Knowledge of `localStorage` integration or middleware like `redux-persist`.
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

A combination of Redux (or Context) for state and a custom hook (e.g., `useAuth`) for accessing it. JWT tokens should be stored in secure cookies or `localStorage` (with XSS considerations), and an Axios interceptor can attach the token to requests.

> 💡 **Interviewer Focus:** Security considerations and architectural cleanliness.
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

The best practice is to handle WebSockets in a **Redux Middleware**. The middleware can listen for specific actions to connect/disconnect and dispatch actions when messages are received from the server.

> 💡 **Interviewer Focus:** Keeping side effects like WebSockets out of components and into middleware.
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

Common patterns include:
- **By Feature:** Grouping all files related to a feature (components, tests, styles) in one folder.
- **By Type:** Folders for components, hooks, pages, store, utils.
- A hybrid approach is often best for large apps, grouping by feature at the top level and by type within features.

> 💡 **Interviewer Focus:** No single right answer, but looking for scalability and maintainability.
</details>
<hr/>

### ❓ Q54. **What is the difference between `npm` and `yarn`?**
<details>
<summary><b>👀 Show Answer</b></summary>

Both are package managers. Yarn was created to solve speed and security issues in early npm versions. Today, both are very similar in speed and features, but Yarn has features like workspaces for monorepos, and npm has a massive registry.

> 💡 **Interviewer Focus:** General frontend tooling knowledge.
</details>
<hr/>

### ❓ Q55. **How would you share state between two browser tabs in a React app?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the `BroadcastChannel` API or listen to the `storage` event on `window` (which fires when `localStorage` is modified in another tab).

> 💡 **Interviewer Focus:** Advanced browser API knowledge.
</details>
<hr/>

### ❓ Q56. **How do you handle large file uploads with progress in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use `XMLHttpRequest` or Axios which support upload progress events. Update a progress bar state in React based on the percentage loaded. For very large files, use chunked uploads.

> 💡 **Interviewer Focus:** Handling async operations with progress feedback.
</details>
<hr/>

### ❓ Q57. **How would you implement an "Infinite Scroll"?**
<details>
<summary><b>👀 Show Answer</b></summary>

Use the **Intersection Observer API** to detect when a sentinel element at the bottom of the list enters the viewport, then trigger the fetch for the next page of data.

> 💡 **Interviewer Focus:** Modern browser APIs vs scroll event listeners.
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

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ Node.js](./02_Nodejs.md) | [Home](./00_Index.md) | [➡️ Next.js](./04_Nextjs.md) |
