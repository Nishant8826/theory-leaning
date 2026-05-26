# 🚀 Interview Preparation - React & Redux

> **Domain:** Web Development / Frontend  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / Lead

---

## 🟢 Beginner Level

### ❓ Q1. **What is React and why is it used?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** React is a popular tool for building user interfaces (what the user sees on screen) using JavaScript.
- **Why:** It makes building complex websites easier by breaking them down into reusable components.
- **Impact:** It drastically speeds up development and improves app performance.

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

**👶 Simple Explanation:**
- **What:** JSX is a syntax that lets you write HTML code directly inside your JavaScript files.
- **Why:** Writing HTML in JS makes it much easier to visualize what a component will look like compared to writing complex JavaScript code to create every element.
- **How:** You write familiar tags like `<div>` in your `.jsx` files, and tools like Babel convert it into standard JavaScript for the browser.

JSX stands for JavaScript XML. It is a syntax extension for JavaScript that allows you to write HTML-like code inside JavaScript. It is transpiled (usually by Babel) into standard `React.createElement()` calls.

> 💡 **Interviewer Focus:** Ensure they know it's not actually HTML and needs compilation.
</details>
<hr/>

### ❓ Q3. **What is the difference between State and Props?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Props are data passed *into* a component from the outside, while State is data managed *inside* a component.
- **Why:** You need both to build interactive apps. Props act like function arguments, and State acts like local variables that can change.
- **How:** Pass props like HTML attributes `<User name="John" />`. Use `useState` to create state.
- **Impact:** Understanding this difference is the most important concept in React.

- **Props** (Properties) are read-only components passed from a parent component to a child component. They are immutable within the child.
- **State** is a local data storage that is local to the component and can be mutated by the component itself (using `useState` or `setState`). State changes trigger re-rendering.

> 💡 **Interviewer Focus:** This is fundamental. Props are external/read-only, State is internal/mutable.
</details>
<hr/>

### ❓ Q4. **What are React Hooks?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Hooks are special functions in React (starting with `use`, like `useState`) that give simple function components superpower features like state and lifecycle.
- **Why:** Before hooks, you had to write complex "Class" components to use state. Hooks make code simpler, shorter, and easier to reuse.
- **Impact:** They completely changed how React is written, making functional components the modern standard.

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

**👶 Simple Explanation:**
- **What:** `useState` is a hook that lets your component "remember" data between screen renders.
- **Why:** If you just use normal JavaScript variables, they get reset every time the screen updates. State stays preserved.
- **How:** It gives you a variable (the data) and a setter function (to change the data). Calling the setter function automatically updates the screen.

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

**👶 Simple Explanation:**
- **What:** The Virtual DOM is a lightweight, "fake" copy of the browser's actual HTML structure kept in memory.
- **Why:** Directly changing the browser's real DOM is very slow. React changes its fast Virtual DOM first, compares it to the old one, and only updates the exact things that changed in the real DOM.
- **Impact:** This is the core reason why React applications are so fast and smooth.

The Virtual DOM is a lightweight copy of the real DOM in memory. When state changes, React creates a new Virtual DOM and compares it with the previous one (Diffing). It then updates only the changed parts in the real DOM (Reconciliation).

> 💡 **Interviewer Focus:** Look for keywords like "Diffing", "Reconciliation", and "Performance".
</details>
<hr/>

### ❓ Q7. **Why do we need `keys` in React lists?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Keys are unique IDs you give to elements when you render a list (like an array) in React.
- **Why:** If a list changes (items reordered, added, or removed), React needs to know *which* exact items changed so it doesn't redraw the whole list unnecessarily.
- **How:** Add a `key={item.id}` prop to the outermost element in your `map()` loop.

Keys help React identify which items have changed, are added, or are removed. They should be given to the elements inside the array to give the elements a stable identity, which improves performance during the diffing process.

> 💡 **Interviewer Focus:** Warn against using array indices as keys for dynamic lists.
</details>
<hr/>

### ❓ Q8. **What is the difference between controlled and uncontrolled components?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Controlled components have their form data (like what you type in an input) controlled by React State. Uncontrolled components let the browser handle the data itself.
- **Why:** Controlled gives you instant access to the text (great for live validation). Uncontrolled is a "fire and forget" approach where you only check the value when you submit.

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

**👶 Simple Explanation:**
- **What:** Redux is a third-party library that acts like a giant, centralized "data vault" (called a Store) for your entire application.
- **Why:** In large apps, passing data through dozens of layers of components (from the top level to a deeply nested button) becomes a nightmare. Redux lets any component directly access the vault.

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

**🏢 Industry Example:**  
Think of a complex app like **Uber or Airbnb**. The user's authentication token, selected location, and shopping cart/ride status need to be accessed by the Navigation Bar, the Map Component, and the Checkout Sidebar simultaneously. Instead of passing this data up and down the component tree (Prop Drilling), Redux acts as a "Global Brain" where any component can connect and read exactly what it needs.

> 💡 **Interviewer Focus:** Emphasize keywords like **Predictable**, **Centralized Store**, **Actions**, and **Reducers**. Mention that it is library-agnostic but most commonly used with React.
</details>
<hr/>

### ❓ Q10. **What are the core principles of Redux?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Redux has three strict rules: 1. One central data vault (Store), 2. Data cannot be directly modified (Read-Only), 3. Changes are made using strict instruction functions (Reducers).
- **Why:** Following these rules ensures that data changes in a massive application are always predictable and easy to track down if bugs occur.

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

**👶 Simple Explanation:**
- **What:** `useEffect` is a hook that lets you run some code *after* React has updated the screen (e.g., fetching data, starting a timer).
- **Why:** You can't put side effects directly in your component's main body because they would run randomly and block the UI from rendering.
- **How:** You provide a function to run, and an array of dependencies to tell React exactly *when* to re-run it.

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

**👶 Simple Explanation:**
- **What:** Reconciliation is React's process of figuring out the fastest way to update the browser's screen to match the newest data.
- **Why:** Without it, React would have to erase and redraw the entire screen on every click, which is extremely slow.
- **How:** It uses a "Diffing" algorithm to spot differences between the old screen (in memory) and the new screen.

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

**👶 Simple Explanation:**
- **What:** Context is a built-in React tool that lets you teleport data directly to any component that needs it, skipping all the components in between.
- **Why:** It solves the "Prop Drilling" problem where you have to pass data through components that don't even care about the data just to reach a nested child.

Context provides a way to pass data through the component tree without having to pass props down manually at every level (Prop Drilling). Use it for data that can be considered "global" for a tree of React components, such as the current authenticated user, theme, or preferred language.

**🏢 Industry Example:**  
In a **Multi-tenant SaaS Platform (like Slack or Jira)**, users can select a "Dark Mode" theme or their preferred language (i18n). Passing `theme` or `language` as props through 20 levels of components is a nightmare. Wrapping the app in a `<ThemeProvider>` and `<LocaleProvider>` using Context API allows deep components (like a tiny `Button` deep in a settings modal) to instantly know if they should render dark backgrounds or Spanish text.

> 💡 **Interviewer Focus:** Use Context for low-frequency updates (theme, locale) to avoid performance issues with frequent re-renders.
</details>
<hr/>

### ❓ Q14. **What is the difference between `useMemo` and `useCallback`?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Both are tools to "remember" things so React doesn't waste time recreating them on every render. `useMemo` remembers a *value* (like the result of tough math), and `useCallback` remembers a *function*.
- **Why:** They prevent slow components from freezing up and stop child components from re-rendering needlessly.

- `useMemo` returns a **memoized value**. It only recalculates the value when one of the dependencies has changed.
- `useCallback` returns a **memoized callback function**. It is useful when passing callbacks to optimized child components that rely on reference equality to prevent unnecessary renders.

> 💡 **Interviewer Focus:** `useMemo` is for values, `useCallback` is for functions. Both are for optimization.
</details>
<hr/>

### ❓ Q15. **What are Custom Hooks and why would you use them?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Custom hooks are just regular JavaScript functions you write yourself that happen to use React's built-in hooks inside them.
- **Why:** If you have logic you want to use in multiple components (like fetching user data or detecting window size), you bundle it into a custom hook to avoid copy-pasting code.

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

**👶 Simple Explanation:**
- **What:** Error boundaries act like a safety net for your app. If a component crashes, the boundary catches the error and shows a fallback screen (like "Oops, something went wrong!") instead of a blank white page.
- **Why:** It keeps the entire app from breaking if just one small piece fails.

Error boundaries are React components that catch JavaScript errors anywhere in their child component tree, log those errors, and display a fallback UI instead of the component tree that crashed.
They are implemented using class components with `static getDerivedStateFromError()` or `componentDidCatch()`.

> 💡 **Interviewer Focus:** Note that error boundaries cannot be created using functional components and hooks yet.
</details>
<hr/>

### ❓ Q17. **What is React.memo?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** It's a wrapper for components that tells React: "Only re-draw this component if its props change."
- **Why:** Normally, if a parent component updates, all its children update too. `React.memo` acts as a shield to block those unnecessary updates, speeding up your app.

`React.memo` is a higher-order component. If your component renders the same result given the same props, you can wrap it in `React.memo` for a performance boost by memoizing the result. React will skip rendering the component and reuse the last rendered result.

> 💡 **Interviewer Focus:** It only checks for prop changes. Shallow comparison by default.
</details>
<hr/>

### ❓ Q18. **Explain Redux Middleware and give an example.**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Middleware in Redux is like a "middleman" that intercepts actions *after* they are sent, but *before* they reach the data vault (store).
- **Why:** You use it to do extra work automatically on every action, like logging the action to a server or fetching data from an API before updating the store.

Middleware provides a third-party extension point between dispatching an action and the moment it reaches the reducer. It is used for logging, crash reporting, talking to an asynchronous API, routing, etc.
**Examples:** Redux Thunk, Redux Saga.

> 💡 **Interviewer Focus:** Understanding that middleware intercepts actions.
</details>
<hr/>

### ❓ Q19. **What is Redux Thunk?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Redux Thunk is a popular middleware that lets Redux handle asynchronous code (like `setTimeout` or `fetch`).
- **Why:** Normally, Redux actions must be simple objects. Thunk lets you write actions that are functions, allowing you to fetch data from an API and *then* update Redux when the data arrives.

Redux Thunk is a middleware that allows you to write action creators that return a function instead of an action. The thunk can be used to delay the dispatch of an action, or to dispatch only if a certain condition is met. This is ideal for async operations like fetching data.

> 💡 **Interviewer Focus:** Essential for handling side effects in Redux without Saga.
</details>
<hr/>

### ❓ Q20. **What is the difference between Redux and Context API?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Context API is a built-in React tool for simply passing data down the tree. Redux is an external powerhouse library for managing complex data.
- **Why:** Use Context for simple things that rarely change (like dark mode). Use Redux when you have tons of data changing all the time (like a live trading app).

- **Context API** is built into React and is best for passing down data to deeply nested components (low frequency updates). It is not a state management system by itself.
- **Redux** is a full state management system with a centralized store, middleware, and DevTools. It is better for large-scale applications with complex state transitions and frequent updates.

> 💡 **Interviewer Focus:** When to use which. Redux is for complex, high-frequency state; Context is for simple, low-frequency state.
</details>
<hr/>

## 🔴 Advanced Level

### ❓ Q21. **How does React Fiber work?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** React Fiber is the internal "engine" of React that controls how and when updates are drawn to the screen.
- **Why:** Before Fiber, large updates could freeze the browser. Fiber allows React to pause work, prioritize urgent things (like typing), and finish background work later.

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

**👶 Simple Explanation:**
- **What:** The most common mistakes developers make when using `useEffect`.
- **Why:** `useEffect` can be tricky because it runs automatically based on dependencies. If you get those wrong, you can break your app or slow it down.

- **Infinite loops:** Caused by updating state that is also a dependency.
- **Stale closures:** Using state or props inside `useEffect` without including them in the dependency array.
- **Memory leaks:** Forgetting to return a cleanup function (e.g., for event listeners or timers).

> 💡 **Interviewer Focus:** Look for solutions like using functional state updates or `useRef` to avoid dependency issues.
</details>
<hr/>

### ❓ Q23. **Explain the concept of "Lifting State Up".**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Moving state (data) from a child component up to its parent component.
- **Why:** If two sibling components need to share the same data, they can't easily pass it directly to each other. By moving the data up to their shared parent, the parent can pass it down to both as props.

When several components need to reflect the same changing data, it is recommended to lift the shared state up to their closest common ancestor. This ensures a single source of truth and keeps components in sync.

> 💡 **Interviewer Focus:** Classic React pattern for sharing data between sibling components.
</details>
<hr/>

### ❓ Q24. **How do you optimize a React application with too many re-renders?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Techniques to stop React from re-drawing components when nothing actually changed.
- **Why:** Re-rendering takes processing power. Too much of it makes the app feel sluggish and unresponsive.

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

**👶 Simple Explanation:**
- **What:** `useLayoutEffect` is identical to `useEffect`, but it runs slightly *earlier* (before the user sees the screen update).
- **Why:** If you use `useEffect` to move an element visually, the user might see it jump (flicker). `useLayoutEffect` hides the jump by fixing the element *before* painting the screen.

- `useEffect` runs **asynchronously** after the browser has painted the screen.
- `useLayoutEffect` runs **synchronously** after all DOM mutations but before the browser paints. Use it when you need to make DOM measurements and visual changes before the user sees them to prevent flickering.

> 💡 **Interviewer Focus:** `useLayoutEffect` can block visual updates, so use it sparingly.
</details>
<hr/>

### ❓ Q26. **How does Redux Toolkit (RTK) improve on standard Redux?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Redux Toolkit (RTK) is the official, modern, and much easier way to write Redux code.
- **Why:** Old Redux required writing massive amounts of repetitive "boilerplate" code across multiple files. RTK bundles everything together cleanly and configures best practices out-of-the-box.

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

**👶 Simple Explanation:**
- **What:** Selectors are functions that "select" or fetch a specific slice of data from the giant Redux store. `reselect` is a tool that "remembers" the result so it doesn't have to recalculate it.
- **Why:** If your store has thousands of items and you just want the count, you don't want to recount them every time the screen updates.

Selectors are functions that extract specific pieces of state from the store.
`reselect` is a library for creating memoized selectors. They are useful because they only recalculate when the specific part of the state tree they depend on changes, preventing unnecessary re-renders in components using those selectors.

> 💡 **Interviewer Focus:** Performance optimization in Redux.
</details>
<hr/>

### ❓ Q28. **How would you implement a custom Redux middleware?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Writing your own "middleman" function for Redux that runs between when an action is dispatched and when the data is saved.
- **Why:** You need this if you want to automatically trigger custom logic, like sending analytics events every time the user clicks a specific button.

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

**👶 Simple Explanation:**
- **What:** A high-level plan for managing data in massive, fast-updating apps.
- **Why:** If you put everything in Redux, your app becomes slow and hard to manage. Mixing different tools for different jobs keeps the app fast.

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

**👶 Simple Explanation:**
- **What:** Features in React 18 that let React "multitask" (Concurrent Mode) and "wait" for data before showing a screen (Suspense).
- **Why:** Multitasking means if you are typing in a search box, React won't freeze the screen while trying to draw thousands of search results.

Concurrent Mode is a set of new features that help React apps stay responsive and gracefully adjust to the user’s device capabilities and network speed.
- **Transitions:** `useTransition` allows you to mark updates as non-urgent, so urgent updates (like typing) aren't blocked by heavy rendering.
- **Suspense:** Allows components to "wait" for something (like data or code loading) before rendering, showing a fallback UI. In React 18, it works with server-side rendering and data fetching frameworks.

> 💡 **Interviewer Focus:** React 18 features, non-blocking rendering, and user experience improvement.
</details>
<hr/>

### ❓ Q31. **How do you prevent memory leaks in a React application?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Memory leaks happen when you delete a component from the screen, but it leaves behind background tasks (like a running timer) that keep eating up computer memory.
- **Why:** Over time, the app gets slower and crashes. You fix it by "cleaning up" when the component dies.

1. **Clean up effects:** Always return a cleanup function in `useEffect` for event listeners, timers, and subscriptions.
2. **Cancel async operations:** Use `AbortController` to cancel fetch requests if the component unmounts before the request completes.
3. **Avoid holding references:** Don't store large objects in refs or global variables if they are not needed after unmount.

> 💡 **Interviewer Focus:** Practical debugging and memory management skills.
</details>
<hr/>

### ❓ Q32. **Compare Redux Saga and Redux Thunk.**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Both are Redux plugins for handling API calls. Thunk is simple (just returning functions). Saga is powerful but complex (uses a special JS feature called "Generators").
- **Why:** Thunk is great for 90% of apps. Saga is needed if you have crazy rules, like "Cancel this API call if the user clicks a button twice within 1 second."

- **Redux Thunk:** Uses functions to handle async logic. Simple to understand, less boilerplate, good for small to medium apps.
- **Redux Saga:** Uses ES6 Generators (`yield`). Better for complex async flows (like race conditions, cancellation, background tasks). Easier to test because effects are declarative objects. More boilerplate and steeper learning curve.

> 💡 **Interviewer Focus:** Understanding when the complexity of Saga is justified.
</details>
<hr/>

### ❓ Q33. **What is Server Component (RSC) in React and how is it different from SSR?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** React Server Components (RSC) are components that run *only* on the backend server, never in the user's browser.
- **Why:** Because they don't run in the browser, they don't send any JavaScript code to the user, making your website load incredibly fast.

- **SSR (Server-Side Rendering):** Renders the HTML on the server and sends it to the client. The client still downloads the full JS bundle to hydrate the page.
- **RSC (React Server Components):** Components that execute *only* on the server. They reduce the bundle size because the code for the component stays on the server, and only the generated content is sent to the client. They cannot use hooks or browser APIs.

> 💡 **Interviewer Focus:** This is the cutting edge of React. Understanding the zero-bundle-size benefit.
</details>
<hr/>

## 🔷 Scenario-Based & Real-World Questions

### ❓ Q34. **How would you implement a search input that fetches data from an API, ensuring it doesn't overload the server with requests?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** A technique to pause API calls until the user stops typing.
- **Why:** If a user types "apple", you don't want to search the database for "a", then "ap", then "app". Debouncing waits a fraction of a second and only searches "apple".

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

**👶 Simple Explanation:**
- **What:** "Windowing" means only drawing the 10 or 20 items the user can actually see on their screen right now, ignoring the other 9,980 items.
- **Why:** The browser will crash or freeze if you try to draw 10,000 HTML elements at once.

I would use **Windowing** or **Virtualization**. Instead of rendering all 10,000 DOM nodes, I would only render the items currently visible in the viewport. Libraries like `react-window` or `react-virtualized` are perfect for this.

> 💡 **Interviewer Focus:** Knowledge of performance bottlenecks with large DOMs and virtualization libraries.
</details>
<hr/>

### ❓ Q36. **How would you handle a race condition where a slower previous API request overwrites a faster subsequent request?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** A race condition is when you make Search A then Search B, but Search A takes so long that it arrives *after* Search B, accidentally replacing your newest results with old ones.
- **Why:** You solve this by ignoring or cancelling older API calls the moment a newer one starts.

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

**👶 Simple Explanation:**
- **What:** Saving Redux data (like a shopping cart) so it doesn't disappear when the user hits "refresh".
- **Why:** By default, all React and Redux state is wiped out completely if the browser page is reloaded.

I would use `redux-persist`, or manually subscribe to the store and save the state to `localStorage` or `sessionStorage` on changes, and load it as the `preloadedState` when creating the store.

> 💡 **Interviewer Focus:** Knowledge of `localStorage` integration or middleware like `redux-persist`.
</details>
<hr/>

### ❓ Q38. **How would you implement a theme switcher (Dark/Light mode) in a React app?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Creating a global switch that flips the colors of the whole app.
- **Why:** Context API is perfect for this because every component on the page needs to know whether to draw itself with light colors or dark colors.

I would use the **Context API** to provide the current theme and a toggle function to the entire app tree. Styled-components or CSS variables can then consume this context to apply styles.

> 💡 **Interviewer Focus:** Good use case for Context API (global, low-frequency update).
</details>
<hr/>

### ❓ Q39. **What is the best way to handle authentication state globally?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Securely remembering if a user is logged in and keeping their "login badge" (Token) safe.
- **Why:** Every part of the app needs to know if the user is logged in (to show/hide private pages). The token must be sent to the backend on every request.

A combination of Redux (or Context) for state and a custom hook (e.g., `useAuth`) for accessing it. JWT tokens should be stored in secure cookies or `localStorage` (with XSS considerations), and an Axios interceptor can attach the token to requests.

> 💡 **Interviewer Focus:** Security considerations and architectural cleanliness.
</details>
<hr/>

### ❓ Q40. **How would you create a multi-step form in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Building forms that are broken into multiple pages (like a checkout process: Address -> Payment -> Review).
- **Why:** You keep all the data in one central "parent" location, and just swap out which "child" page is visible depending on what step the user is on.

Keep the form state in a parent component or Redux store. Render different child components for each step based on a `currentStep` state. Validate each step before proceeding.

> 💡 **Interviewer Focus:** State management strategy for complex forms.
</details>
<hr/>

### ❓ Q41. **How do you test a custom hook?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Using tools to test if your custom hook logic works.
- **Why:** Hooks are functions, but they must run *inside* React. Testing libraries let you "fake" a component so you can test the hook directly.

I would use `@testing-library/react-hooks` and its `renderHook` function. This allows me to test the hook's return values and effects without creating a dummy component.

> 💡 **Interviewer Focus:** Familiarity with modern testing tools for hooks.
</details>
<hr/>

### ❓ Q42. **How would you implement "Undo/Redo" functionality using Redux?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Letting users press "Ctrl+Z" to undo a mistake in the app.
- **Why:** Since Redux keeps data changes predictable, you can literally save the "history" of the state and just jump back to an older version.

By using a library like `redux-undo` or manually structuring the state to have `past`, `present`, and `future` arrays. Actions would move the `present` to `past` on new updates, and pop from `past`/`future` for undo/redo.

> 💡 **Interviewer Focus:** Understanding state history management.
</details>
<hr/>

### ❓ Q43. **A component is re-rendering because its object prop changes reference, but the data is the same. How do you fix this?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Fixing a bug where React thinks an object changed (because it was recreated) even though the data inside it is exactly the same.
- **Why:** In JavaScript, two identical-looking objects aren't "equal." Using `useMemo` forces React to reuse the *exact same* object from memory.

Use `useMemo` in the parent component to memoize the object, or pass primitive values instead of the object if possible. If passing a function, use `useCallback`.

> 💡 **Interviewer Focus:** Reference equality in JavaScript and React optimization.
</details>
<hr/>

### ❓ Q44. **How would you implement a Global Modal system in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Creating a single popup (modal) system for the whole app instead of copying popup code 50 times.
- **Why:** It keeps your code clean. Any component can just say "Open Login Modal" to the global store, and the single main Modal component handles the rest.

Use Redux or Context to store the active modal type and props. Render a single `ModalContainer` at the root of the app that listens to this state and renders the appropriate modal using **React Portals** to mount it outside the main DOM tree.

> 💡 **Interviewer Focus:** Use of Portals for modals and centralized state control.
</details>
<hr/>

### ❓ Q45. **How do you handle WebSocket connections in a React/Redux app?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Connecting the app to a live, continuous data stream (like a chat room or live sports score).
- **Why:** You manage this in Redux Middleware so the connection stays open in the background, rather than disconnecting and reconnecting every time the user clicks a button.

The best practice is to handle WebSockets in a **Redux Middleware**. The middleware can listen for specific actions to connect/disconnect and dispatch actions when messages are received from the server.

**🏢 Industry Example:**  
In a **Customer Support Chat Application (like Intercom or Zendesk)**, connecting the WebSocket inside a React component's `useEffect` can lead to memory leaks or multiple active connections on re-renders. Instead, we build a custom Redux middleware. When the user logs in, we dispatch `{ type: 'WS_CONNECT' }`. The middleware intercepts this, establishes the socket, and attaches listeners. When a message arrives, the middleware dispatches `{ type: 'MESSAGE_RECEIVED', payload: data }`, which the Redux reducers safely process to update the chat UI globally.

> 💡 **Interviewer Focus:** Keeping side effects like WebSockets out of components and into middleware.
</details>
<hr/>

### ❓ Q46. **What is the difference between shallow rendering and full DOM rendering in testing?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Two ways to test components. Shallow is like testing a car's steering wheel without the engine attached. Full DOM is like test-driving the whole car.
- **Why:** Full DOM testing is much more popular now because it ensures everything actually works together the way a user would experience it.

- **Shallow Rendering:** Renders only the component itself and not its children. Good for isolated unit tests.
- **Full DOM Rendering:** Renders the component and all its children. Necessary for integration tests and testing behavior that depends on child components.

> 💡 **Interviewer Focus:** React Testing Library promotes full DOM rendering to mimic user behavior.
</details>
<hr/>

### ❓ Q47. **How would you optimize a heavy computation in a component?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Handling a piece of code that does crazy math and takes a full second to run.
- **Why:** If you run this math every time the user types a letter, the app will completely freeze. You fix this by "remembering" the math answer (`useMemo`) or sending the math to a background process (Web Worker).

Wrap the computation in `useMemo` so it only re-runs when its dependencies change. If it's extremely heavy, consider moving it to a **Web Worker** to avoid blocking the main UI thread.

> 💡 **Interviewer Focus:** `useMemo` and Web Workers for performance.
</details>
<hr/>

### ❓ Q48. **How do you prevent Cross-Site Scripting (XSS) in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** XSS is when a hacker types malicious JavaScript code into a comment box on your website, trying to steal passwords.
- **Why:** React is inherently safe and will just render the code as text instead of executing it. But if you force React to render raw HTML (`dangerouslySetInnerHTML`), you open the door to hackers.

React automatically escapes variables in JSX, preventing most XSS attacks. However, avoid using `dangerouslySetInnerHTML` unless absolutely necessary, and always sanitize the content first using a library like `DOMPurify`.

> 💡 **Interviewer Focus:** Security awareness in React development.
</details>
<hr/>

### ❓ Q49. **How would you implement a custom `useLocalStorage` hook?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Creating a hook that acts exactly like `useState`, but it also automatically saves the data to the browser's hard drive (`localStorage`).
- **Why:** So if the user closes the browser and comes back tomorrow, their data (like a "dark mode" preference) is still there.

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

**👶 Simple Explanation:**
- **What:** Making your app support multiple languages (English, Spanish, French).
- **Why:** You can't just hardcode text like `<button>Submit</button>`. You use tools that swap "Submit" for "Enviar" automatically based on the user's language setting.

Use a library like `react-i18next` or `formatjs`. They provide hooks and components to translate strings based on the current locale, which can be stored in Redux or Context.

> 💡 **Interviewer Focus:** Familiarity with localization ecosystems.
</details>
<hr/>

### ❓ Q51. **What is "Prop Drilling" and how do you avoid it?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Passing data from a great-grandparent component down to a great-grandchild by handing it through every single component in between.
- **Why:** It makes the middle components messy with data they don't even use. We avoid it by using "teleporters" like Context API or Redux.

Prop drilling is the process of passing props through multiple levels of components just to get them to a deeply nested component. Avoid it by using the Context API, Redux, or component composition (passing components as props).

**🏢 Industry Example:**  
Imagine a **Food Delivery App**. The `App` component holds the `userId`. The user is viewing a `RestaurantPage`, which renders a `MenuList`, which renders a `CategorySection`, which renders a `MenuItem`, which finally renders an `AddToCartButton`. Passing `userId` through 5 layers just so the button can make an API call is Prop Drilling. In industry, we either use Redux so the `AddToCartButton` can fetch `userId` directly from the store, or we use component composition (passing the button itself as a prop (`children`)) so intermediate components don't need to know about the props.

> 💡 **Interviewer Focus:** Understanding clean architecture and state distribution.
</details>
<hr/>

### ❓ Q52. **How would you implement a "Pull to Refresh" feature?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Building the common mobile app feature where you drag the screen down to reload the feed.
- **Why:** On the web, you have to manually track exactly where the user's finger starts and stops to see if they dragged "down" far enough to trigger a reload.

Listen to touch events (`onTouchStart`, `onTouchMove`, `onTouchEnd`) on a container. Calculate the pull distance. If it exceeds a threshold, trigger the data fetch and show a loading spinner. (In React Native, use the built-in `RefreshControl`).

> 💡 **Interviewer Focus:** Handling touch gestures and state.
</details>
<hr/>

### ❓ Q53. **How do you structure folders in a large React project?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** How to organize your hundreds of files so you don't go crazy.
- **Why:** Instead of throwing 100 components into one `/components` folder, you group them by feature (e.g., all files related to the "ShoppingCart" go in one folder).

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

**👶 Simple Explanation:**
- **What:** Both are "App Stores" for JavaScript. They are tools you use in the terminal to download libraries (like React, or Redux) into your project.
- **Why:** They are mostly identical now, but people have personal preferences on which one they use to install packages.

Both are package managers. Yarn was created to solve speed and security issues in early npm versions. Today, both are very similar in speed and features, but Yarn has features like workspaces for monorepos, and npm has a massive registry.

> 💡 **Interviewer Focus:** General frontend tooling knowledge.
</details>
<hr/>

### ❓ Q55. **How would you share state between two browser tabs in a React app?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** If a user logs out in Tab A, you want Tab B to instantly log them out too.
- **Why:** React state only lives in one specific tab. You have to use special browser tricks (like `BroadcastChannel` or `localStorage`) to send messages between separate tabs.

Use the `BroadcastChannel` API or listen to the `storage` event on `window` (which fires when `localStorage` is modified in another tab).

> 💡 **Interviewer Focus:** Advanced browser API knowledge.
</details>
<hr/>

### ❓ Q56. **How do you handle large file uploads with progress in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Showing a "50% uploaded" bar when a user uploads a huge 1GB video.
- **Why:** Standard `fetch()` calls don't let you see the progress. You have to use older tools like `XMLHttpRequest` or libraries like `Axios` which can track the percentage.

Use `XMLHttpRequest` or Axios which support upload progress events. Update a progress bar state in React based on the percentage loaded. For very large files, use chunked uploads.

> 💡 **Interviewer Focus:** Handling async operations with progress feedback.
</details>
<hr/>

### ❓ Q57. **How would you implement an "Infinite Scroll"?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Making a page that loads more items automatically when you reach the bottom (like Instagram or TikTok).
- **Why:** Instead of calculating scroll math (which is slow), modern browsers give you a tool (`Intersection Observer`) that just says "Hey, the invisible box at the bottom of the page is now visible, load more stuff!"

Use the **Intersection Observer API** to detect when a sentinel element at the bottom of the list enters the viewport, then trigger the fetch for the next page of data.

> 💡 **Interviewer Focus:** Modern browser APIs vs scroll event listeners.
</details>
<hr/>

### ❓ Q58. **What is a "Higher-Order Component" (HOC)?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** An HOC (Higher-Order Component) is a function that takes a normal component, adds some "superpowers" to it (like checking if the user is logged in), and returns the upgraded component.
- **Why:** It's an older React pattern (mostly replaced by hooks) used to share logic between components.

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

**👶 Simple Explanation:**
- **What:** `useReducer` is like `useState`'s big brother. It manages complex state using the same rules as Redux (actions and reducers).
- **Why:** If you have an object with 10 different properties that update together based on specific rules, `useState` gets very messy. `useReducer` keeps it clean.

`useReducer` is usually preferable when you have complex state logic that involves multiple sub-values or when the next state depends on the previous one. It also lets you optimize performance for components that trigger deep updates because you can pass `dispatch` down instead of callbacks.

> 💡 **Interviewer Focus:** State management complexity.
</details>
<hr/>

### ❓ Q60. **How do you mock an API call in Jest?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Pretending to make a real network request during a test, but returning fake data instantly instead.
- **Why:** You don't want your tests to actually hit your real database because it's slow, unpredictable, and could delete real data.

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

**👶 Simple Explanation:**
- **What:** Breaking your massive website code into smaller pieces so the user only downloads what they need right now.
- **Why:** If your app is 5MB, a mobile user will stare at a blank screen for 10 seconds. Code splitting loads the 100KB homepage first, and only loads the "Settings" page code if the user actually clicks it.

Code splitting allows you to split your bundle into smaller chunks which can then be loaded on demand. In React, this is done using `React.lazy()` and `Suspense`.

> 💡 **Interviewer Focus:** Performance optimization for initial load time.
</details>
<hr/>

### ❓ Q62. **How do you handle cleanup in `useEffect`?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Providing a "cleanup" function inside `useEffect` that React runs when the component is deleted.
- **Why:** To stop timers or disconnect from WebSockets so your app doesn't slow down or crash in the background.

Return a function from the effect. This function runs before the component unmounts and before the effect re-runs (if dependencies changed).

> 💡 **Interviewer Focus:** Preventing memory leaks.
</details>
<hr/>

### ❓ Q63. **What is Strict Mode in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** A wrapper (`<React.StrictMode>`) you put around your app during development that aggressively checks for bad code.
- **Why:** It purposely runs your components twice to expose hidden bugs (like missing cleanups in `useEffect`) before you release your app to users.

A tool for highlighting potential problems in an application. It does not render any visible UI. It activates additional checks and warnings for its descendants (e.g., identifying unsafe lifecycles, warning about legacy string ref API). In React 18, it mounts components twice in dev mode to help find effect bugs.

> 💡 **Interviewer Focus:** Awareness of development tools and React 18 behavior.
</details>
<hr/>

### ❓ Q64. **How would you test if a button click calls a function?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Writing an automated test to prove a button actually works.
- **Why:** You pass a "fake" function to the button, simulate a click, and then check if the fake function successfully recorded that it was clicked.

Create a mock function using `jest.fn()`. Pass it as a prop to the component. Use React Testing Library to find the button and simulate a click. Expect the mock function to have been called.

> 💡 **Interviewer Focus:** Basic RTL and Jest usage.
</details>
<hr/>

### ❓ Q65. **What are synthetic events in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** React's custom wrapper around normal browser events (like clicks or keyboard presses).
- **Why:** Every browser (Chrome, Safari, old Internet Explorer) handles events slightly differently. React creates a "Synthetic" event to guarantee it behaves exactly the same everywhere.

React implements a synthetic event system to ensure events have consistent properties across different browsers. It is a cross-browser wrapper around the browser’s native event.

> 💡 **Interviewer Focus:** Cross-browser compatibility handling.
</details>
<hr/>

### ❓ Q66. **How do you access the DOM element directly in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Bypassing React to directly touch an HTML element (like an `<input>`).
- **Why:** You shouldn't do this often, but it's necessary for things React can't easily do, like instantly putting the blinking cursor (focus) inside an input box.

By using the `useRef` hook. You attach the ref to the JSX element via the `ref` prop.

> 💡 **Interviewer Focus:** Correct use of refs for DOM manipulation when necessary.
</details>
<hr/>

### ❓ Q67. **What is the difference between a functional and a class component?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** The two ways to write React code. Functional components are modern, short, and use Hooks. Class components are the old, bulky way using ES6 Classes.
- **Why:** Almost all new React code is written as Functional components because they are easier to read, write, and test.

- **Functional:** Just a JS function that returns JSX. Uses hooks for state and lifecycle. Simpler and preferred in modern React.
- **Class:** ES6 class extending `React.Component`. Uses `this.state` and lifecycle methods. Legacy but still supported.

> 💡 **Interviewer Focus:** Modern React leans heavily towards functional components.
</details>
<hr/>

### ❓ Q68. **What is hydration in React?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Turning a "dead" webpage into a "live" React app.
- **Why:** When doing Server-Side Rendering, the server sends pure, static HTML so the user sees it instantly. "Hydration" is when React boots up in the background and attaches click listeners to make the buttons actually work.

Hydration is the process of React attaching event listeners to the HTML that was rendered on the server, making the static page interactive.

> 💡 **Interviewer Focus:** Understanding SSR and client-side transition.
</details>
<hr/>

### ❓ Q69. **How do you pass data from a child to a parent component?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** Data in React normally only flows downwards (Parent -> Child). To send data back up, you use a callback function.
- **Why:** The parent gives the child a "walkie-talkie" (a function). When the child has news (like a button click), it talks into the walkie-talkie to alert the parent.

Pass a function from the parent to the child as a prop. The child calls this function and passes the data as an argument.

> 💡 **Interviewer Focus:** Basic React data flow (unidirectional).
</details>
<hr/>

### ❓ Q70. **What is the difference between `React.createElement` and JSX?**
<details>
<summary><b>👀 Show Answer</b></summary>

**👶 Simple Explanation:**
- **What:** JSX is just a pretty disguise for writing messy JavaScript functions.
- **Why:** Writing `<div>Hello</div>` is incredibly easy. Writing `React.createElement('div', null, 'Hello')` over and over would be terrible.

JSX is syntactic sugar for `React.createElement`. Babel transpiles JSX into `React.createElement` calls.

> 💡 **Interviewer Focus:** JSX is not magic, it's just a nicer syntax for JS calls.
</details>
<hr/>

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ Node.js](./02_Nodejs.md) | [Home](./00_Index.md) | [➡️ Next.js](./04_Nextjs.md) |
