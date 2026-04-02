# 07 - Event Handling 🖱️


---

## 🤔 What is Event Handling?

When a user **clicks a button**, **types in an input**, **submits a form**, or **moves the mouse** — those are **events**. Event handling means writing code that **reacts** to those events.

---

## 🆚 React Events vs HTML Events

| Feature | HTML | React |
|---|---|---|
| Event name | `onclick` | `onClick` |
| Syntax | `onclick="handler()"` | `onClick={handler}` |
| Pass function | `onclick="do()"` | `onClick={do}` |
| Event object | `event` | `event` (same!) |

> 💡 React event names are **camelCase**: `onclick` → `onClick`, `onchange` → `onChange`, `onsubmit` → `onSubmit`

---

## 🖱️ Common Events in React

```jsx
<button onClick={handleClick}>Click</button>
<input onChange={handleChange} />
<form onSubmit={handleSubmit}>...</form>
<input onFocus={handleFocus} />
<input onBlur={handleBlur} />
<div onMouseEnter={handleHover} />
<input onKeyDown={handleKeyPress} />
```

---

## 🔧 Basic Click Event

```jsx
function AlertButton() {
  // Define the handler (event function)
  const handleClick = () => {
    alert("Button was clicked! 🎉");
  };

  return <button onClick={handleClick}>Click Me</button>;
  //                     ↑ Pass function reference, NOT a call!
  //                       onClick={handleClick}   ✅
  //                       onClick={handleClick()} ❌ (calls it immediately!)
}
```

---

## 📩 Using the Event Object

React passes an **event object** to your handler automatically:

```jsx
function InputLogger() {
  const handleChange = (event) => {
    console.log("Value:", event.target.value);
    console.log("Input name:", event.target.name);
  };

  return (
    <input
      name="username"
      onChange={handleChange}
      placeholder="Type something..."
    />
  );
}
```

Common `event` properties:
- `event.target.value` — current value of input
- `event.target.name` — name attribute of element
- `event.target.checked` — for checkboxes
- `event.preventDefault()` — stop default behavior (like form submit reload)

---

## 🌍 Real-World Examples

### Example 1: Button with State

```jsx
function LikeButton() {
  const [liked, setLiked] = useState(false);

  const handleLike = () => {
    setLiked(!liked);
  };

  return (
    <button
      onClick={handleLike}
      style={{ color: liked ? "red" : "gray" }}
    >
      {liked ? "❤️ Liked" : "🤍 Like"}
    </button>
  );
}
```

### Example 2: Controlled Input

```jsx
function SearchBar() {
  const [query, setQuery] = useState("");

  const handleChange = (e) => {
    setQuery(e.target.value);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search..."
        value={query}
        onChange={handleChange}
      />
      <p>You searched for: <strong>{query}</strong></p>
    </div>
  );
}
```

### Example 3: Form Submit (preventDefault)

```jsx
function LoginForm() {
  const [email, setEmail] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();  // Stops page from reloading!
    alert(`Logging in with: ${email}`);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Enter email"
      />
      <button type="submit">Login</button>
    </form>
  );
}
```

### Example 4: Passing Arguments to Handler

```jsx
function ProductList() {
  const products = ["Apple", "Banana", "Orange"];

  const handleClick = (productName) => {
    alert(`You selected: ${productName}`);
  };

  return (
    <ul>
      {products.map((product) => (
        <li key={product}>
          {product}
          {/* Use arrow function to pass arguments */}
          <button onClick={() => handleClick(product)}>Select</button>
        </li>
      ))}
    </ul>
  );
}
```

### Example 5: Keyboard Event

```jsx
function EnterPress() {
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      alert("Enter key pressed! ✅");
    }
  };

  return (
    <input
      onKeyDown={handleKeyDown}
      placeholder="Press Enter..."
    />
  );
}
```

---

## 🛑 Event Propagation (Bubbling)

Events "bubble up" from child to parent by default:

```jsx
function Parent() {
  return (
    <div onClick={() => console.log("Parent clicked!")}>
      <button onClick={(e) => {
        e.stopPropagation();  // Stops event from reaching Parent!
        console.log("Button clicked!");
      }}>
        Click Me
      </button>
    </div>
  );
}
```

Use `e.stopPropagation()` to stop events from bubbling up.

---

## ❌ Common Mistakes / Tips

- ❌ `onClick={handleClick()}` — This **calls** the function immediately (wrong!)
- ✅ `onClick={handleClick}` — This **assigns** the function (correct)
- ❌ Forgetting `e.preventDefault()` for form submissions
- ✅ Use `e.target.value` to get input values
- 💡 Arrow function in JSX: `onClick={() => doSomething(arg)}` — use when passing arguments

---

## 📝 Summary

- React events are camelCase: `onClick`, `onChange`, `onSubmit`
- Always pass the **function reference**, not the call: `onClick={fn}` not `onClick={fn()}`
- Use `e.preventDefault()` for forms to prevent page reload
- Use `e.target.value` to read input values
- Use arrow functions `() => fn(arg)` when you need to pass arguments
- Use `e.stopPropagation()` to stop event bubbling

---

## 🎯 Practice Tasks

1. Create a button that changes its own text when clicked (e.g., "Click Me" → "Clicked! ✅")
2. Create a form with name + email inputs and an alert on submit (use `e.preventDefault()`)
3. Build a color picker — clicking color buttons changes the background color of a div
4. Build a hover card that shows a message when you hover over it (`onMouseEnter` / `onMouseLeave`)
5. Create an input that detects Enter key and shows the typed value in an alert

---

← Previous: [06_state.md](06_state.md) | Next: [08_conditional_rendering.md](08_conditional_rendering.md) →
