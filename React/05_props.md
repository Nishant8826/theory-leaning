# 05 - Props 📦


---

## 🤔 What are Props?

**Props** (short for **Properties**) are how you **pass data from a parent component to a child component**.

```
Parent sends data → via Props → Child receives and displays it
```

---

## 🌍 Real-World Example

Imagine you have a `UserCard` component. Instead of hardcoding data, you pass it via props:

```jsx
// Parent Component (App.jsx)
function App() {
  return (
    <div>
      <UserCard name="Nishant" role="Developer" age={25} />
      <UserCard name="Priya" role="Designer" age={23} />
      <UserCard name="Raj" role="Manager" age={30} />
    </div>
  );
}
```

```jsx
// Child Component (UserCard.jsx)
function UserCard({ name, role, age }) {
  return (
    <div className="card">
      <h2>{name}</h2>
      <p>Role: {role}</p>
      <p>Age: {age}</p>
    </div>
  );
}

export default UserCard;
```

---

## 📡 How Props Work

Props flow in **one direction only** — from **Parent → Child** (called "unidirectional data flow").

```
App (Parent)
  ↓ sends props
UserCard (Child) — receives and uses the props
```

> 🔒 Props are **read-only** — the child cannot change the data it receives via props. (For changeable data, use **State** → next topic!)

---

## 🔧 Using Props: Two Ways

### Way 1: Destructuring (Recommended ✅)
```jsx
function Greeting({ name, message }) {
  return <p>{message}, {name}!</p>;
}

// Usage
<Greeting name="Nishant" message="Hello" />
```

### Way 2: Using the `props` object
```jsx
function Greeting(props) {
  return <p>{props.message}, {props.name}!</p>;
}

// Usage
<Greeting name="Nishant" message="Hello" />
```

Both work, but **destructuring is cleaner and more common**.

---

## 🎨 Passing Different Prop Types

```jsx
function Profile({ name, age, isAdmin, hobbies, address }) {
  return (
    <div>
      <p>Name: {name}</p>           {/* String */}
      <p>Age: {age}</p>             {/* Number */}
      <p>Admin: {isAdmin ? "Yes" : "No"}</p>  {/* Boolean */}
      <p>City: {address.city}</p>   {/* Object */}
      <ul>
        {hobbies.map((h, i) => <li key={i}>{h}</li>)}  {/* Array */}
      </ul>
    </div>
  );
}

// Pass it:
<Profile
  name="Nishant"                   // String
  age={25}                         // Number (use {} for non-string!)
  isAdmin={true}                   // Boolean
  hobbies={["Coding", "Gaming"]}   // Array
  address={{ city: "Mumbai" }}     // Object
/>
```

> 💡 **Important:** Use `{}` for numbers, booleans, arrays, objects. Use `""` only for strings.

---

## 🛡️ Default Props

What if a parent doesn't pass a prop? Use **default values**!

```jsx
function Button({ label = "Click Me", color = "blue" }) {
  return (
    <button style={{ backgroundColor: color }}>
      {label}
    </button>
  );
}

// No props passed — uses defaults
<Button />

// Override defaults
<Button label="Submit" color="green" />
```

---

## 🧒 Passing JSX as Props: `children`

You can pass **JSX content** between component tags using the special `children` prop:

```jsx
function Card({ children, title }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className="card-body">
        {children}  {/* Whatever is passed between tags */}
      </div>
    </div>
  );
}

// Usage — everything between tags becomes `children`
<Card title="About Me">
  <p>I am a React developer.</p>
  <button>Contact Me</button>
</Card>
```

---

## 🔄 Props vs State

| Feature | Props | State |
|---|---|---|
| Who sets it | Parent component | The component itself |
| Can change? | ❌ Read-only | ✅ Changes over time |
| Direction | Parent → Child | Internal to component |
| Example | `name`, `age` | `count`, `isOpen` |

---

## ❌ Common Mistakes / Tips

- ❌ Trying to change props inside the child component
- ❌ Forgetting `{}` around non-string values: `age="25"` vs `age={25}`
- ❌ Misspelling prop names (case-sensitive!)
- ✅ Always destructure props for cleaner code
- ✅ Provide default values for optional props
- 💡 String props: `name="Nishant"` — Number/Boolean: `age={25}` / `isAdmin={true}`

---

## 📝 Summary

- Props = **data passed from parent to child**
- Props are **read-only** — never change them in child
- Use **destructuring** for cleaner code
- `children` is a special prop for nested JSX
- Different types: strings, numbers, booleans, arrays, objects, functions
- Default values prevent errors when props aren't passed

---

## 🎯 Practice Tasks

1. Create a `MovieCard` component that accepts: `title`, `year`, `rating`, `genre` as props
2. Render 4 different `MovieCard` components with different data
3. Add a **default prop** for a `badge` that shows "New" if not provided
4. Create a `Container` component that uses `children` prop to wrap any content
5. Try passing a **function** as a prop — can you call it from inside the child?

---

← Previous: [04_components.md](04_components.md) | Next: [06_state.md](06_state.md) →
