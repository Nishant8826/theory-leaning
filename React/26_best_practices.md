# 26 - Best Practices & Clean Code 🧹


---

## 🤔 Why Do Best Practices Matter?

Bad code works but:
- Is hard to read and maintain
- Breaks easily when changed
- Slows down your team
- Makes debugging a nightmare

Clean code is like a **well-organized kitchen** — everything is in its place, labeled, and easy to find!

---

## ✅ Component Best Practices

### 1. Keep Components Small and Focused

```jsx
// ❌ BAD — one giant component doing everything!
function UserDashboard() {
  // 300 lines of mixed logic for header, sidebar, content, footer...
}

// ✅ GOOD — each component does ONE thing
function UserDashboard() {
  return (
    <div>
      <DashboardHeader />
      <DashboardSidebar />
      <DashboardContent />
    </div>
  );
}
```

**Rule of thumb:** If a component is longer than ~150-200 lines, consider splitting it.

---

### 2. Descriptive Naming

```jsx
// ❌ BAD — vague names
function Comp({ data, fn }) { ... }
function handleX() { ... }

// ✅ GOOD — clear, descriptive names
function UserProfileCard({ user, onEdit }) { ... }
function handleEditProfile() { ... }
```

---

### 3. Single Responsibility Principle

Each component, hook, and function should do **ONE thing**:

```jsx
// ❌ BAD — component fetches AND renders AND formats
function Users() {
  const [users, setUsers] = useState([]);
  useEffect(() => { /* fetch logic */ }, []);
  const formatName = (user) => `${user.first} ${user.last}`;
  return <ul>{users.map(u => <li>{formatName(u)}</li>)}</ul>;
}

// ✅ GOOD — separate concerns
// 1. Custom hook handles fetching
const { users } = useUsers();

// 2. Utility function handles formatting
const formatName = (user) => `${user.first} ${user.last}`;

// 3. Component just renders
function Users() {
  const { users } = useUsers();
  return <ul>{users.map(u => <li key={u.id}>{formatName(u)}</li>)}</ul>;
}
```

---

## ✅ JSX Best Practices

### 4. Avoid Inline Logic in JSX

```jsx
// ❌ BAD — complex logic inside JSX
<div>
  {users.filter(u => u.active && u.role === "admin").map(u => (
    <UserCard key={u.id} user={u} onClick={() => { setSelected(u); navigate("/profile"); }} />
  ))}
</div>

// ✅ GOOD — move logic outside JSX
const adminUsers = users.filter(u => u.active && u.role === "admin");
const handleSelectUser = (u) => {
  setSelected(u);
  navigate("/profile");
};

<div>
  {adminUsers.map(u => (
    <UserCard key={u.id} user={u} onClick={() => handleSelectUser(u)} />
  ))}
</div>
```

---

### 5. Use Fragments Instead of Extra Divs

```jsx
// ❌ BAD — unnecessary div
return (
  <div>
    <h1>Title</h1>
    <p>Subtitle</p>
  </div>
);

// ✅ GOOD — no extra div in DOM
return (
  <>
    <h1>Title</h1>
    <p>Subtitle</p>
  </>
);
```

---

### 6. Consistent Prop Naming

```jsx
// ❌ BAD — inconsistent
<Button clickMe={handleClick} txt="Submit" isDisabled={false} show_icon />

// ✅ GOOD — consistent, follows React conventions
<Button onClick={handleClick} label="Submit" disabled={false} showIcon />
```

---

## ✅ State Best Practices

### 7. Don't Overuse State

```jsx
// ❌ BAD — derived value doesn't need to be state
const [fullName, setFullName] = useState("");
const [firstName, setFirstName] = useState("");
const [lastName, setLastName] = useState("");

useEffect(() => {
  setFullName(`${firstName} ${lastName}`);
}, [firstName, lastName]);

// ✅ GOOD — derived value is just a variable
const [firstName, setFirstName] = useState("");
const [lastName, setLastName] = useState("");
const fullName = `${firstName} ${lastName}`; // Just compute it!
```

---

### 8. Initialize State Smartly

```jsx
// ❌ BAD — heavy computation on every render for initial value
const [data, setData] = useState(expensiveCompute()); // runs every render!

// ✅ GOOD — lazy initialization runs once
const [data, setData] = useState(() => expensiveCompute()); // only runs once
```

---

## ✅ Code Organization Best Practices

### 9. Import Order

```jsx
// 1. React imports
import React, { useState, useEffect } from "react";

// 2. Third-party libraries
import axios from "axios";
import { useNavigate } from "react-router-dom";

// 3. Internal components
import UserCard from "../components/UserCard";
import Button from "../components/Button";

// 4. Hooks
import { useAuth } from "../hooks/useAuth";

// 5. Utilities and constants
import { formatDate } from "../utils/formatDate";
import { API_URL } from "../constants";

// 6. Styles
import "./UserPage.css";
```

---

### 10. Constants Over Magic Values

```jsx
// ❌ BAD — "magic" numbers and strings
if (role === "admin") { ... }
setTimeout(fn, 3000);
const MAX = 100;

// ✅ GOOD — named constants
const ROLES = { ADMIN: "admin", USER: "user", EDITOR: "editor" };
const NOTIFICATION_DELAY_MS = 3000;
const MAX_RETRY_COUNT = 100;

if (role === ROLES.ADMIN) { ... }
setTimeout(fn, NOTIFICATION_DELAY_MS);
```

---

### 11. Early Returns for Cleaner Code

```jsx
// ❌ BAD — deep nesting
function UserProfile({ user }) {
  if (user) {
    if (user.isActive) {
      return <div>{user.name}</div>;
    } else {
      return <p>User is inactive</p>;
    }
  } else {
    return <p>No user found</p>;
  }
}

// ✅ GOOD — early returns
function UserProfile({ user }) {
  if (!user) return <p>No user found</p>;
  if (!user.isActive) return <p>User is inactive</p>;

  return <div>{user.name}</div>;
}
```

---

## ✅ Performance Best Practices

### 12. Keys Must Be Unique and Stable

```jsx
// ❌ BAD — index as key for dynamic lists
{items.map((item, index) => <Item key={index} {...item} />)}

// ✅ GOOD — use unique ID from data
{items.map((item) => <Item key={item.id} {...item} />)}
```

---

### 13. Memoize Wisely

```jsx
// ❌ BAD — memoizing everything, even tiny components
const SimpleText = React.memo(() => <p>Hello</p>); // No benefit

// ✅ GOOD — memoize only when it matters
const ExpensiveList = React.memo(({ items }) => {
  // Renders 1000+ items with complex logic
});
```

---

## ✅ Code Quality Tools

### 14. Use ESLint + Prettier

```bash
# Install ESLint for React
npm install --save-dev eslint eslint-plugin-react

# Install Prettier
npm install --save-dev prettier
```

```json
// .eslintrc.json
{
  "extends": ["react-app", "plugin:react/recommended"],
  "rules": {
    "no-unused-vars": "warn",
    "react/prop-types": "off"
  }
}

// .prettierrc
{
  "semi": true,
  "singleQuote": false,
  "tabWidth": 2
}
```

---

## 📋 Quick Best Practices Checklist

### ✅ Component Design
- [ ] Single responsibility per component
- [ ] Descriptive names (PascalCase for components)
- [ ] Props destructured and named clearly
- [ ] Default props set for optional props
- [ ] No more than 10 props on a component

### ✅ State
- [ ] Minimal state — compute derived values instead
- [ ] State as close to where it's needed as possible
- [ ] Never mutate state directly

### ✅ Code Quality
- [ ] ESLint + Prettier configured
- [ ] No `console.log` left in production code
- [ ] No unused variables or imports
- [ ] Magic values replaced with constants

### ✅ Performance
- [ ] Stable keys in lists
- [ ] Cleanup in useEffect (no memory leaks)
- [ ] Images have `loading="lazy"` where appropriate

---

## ❌ Common Bad Habits to Break

- ❌ `console.log` everywhere in production
- ❌ Updating state directly: `state.value = 5`
- ❌ Using `index` as key for dynamic lists
- ❌ Huge components doing 10 things
- ❌ API calls inside render (not in useEffect)
- ❌ Ignoring warnings (they exist for a reason!)
- ❌ Prop drilling more than 2-3 levels deep

---

## 📝 Summary

- **Small, focused components** — single responsibility
- **Descriptive names** — no abbreviations or magic values
- **Extract logic** — custom hooks, utility functions, services
- **ESLint + Prettier** — enforce code style automatically
- **Early returns** — avoid deep nesting
- **Stable unique keys** in lists
- **Don't over-optimize** — measure first

---

## 🎯 Practice Tasks

1. Take a "bad" component you wrote earlier and refactor it — split into smaller components
2. Install ESLint and Prettier in your project. Fix all the warnings
3. Go through any component and replace all magic values with named constants
4. Rewrite deeply nested `if/else` as early returns
5. Find and extract any repeated logic into a custom hook

---

← Previous: [25_react_vs_angular_vue.md](25_react_vs_angular_vue.md)
