# 08 - Conditional Rendering 🔀


---

## 🤔 What is Conditional Rendering?

Conditional rendering means **showing or hiding parts of your UI** based on a condition.

> **Real-world analogy:**
> Think of an ATM machine. If you enter the wrong PIN, it shows "Incorrect PIN ❌". If correct, it shows "Welcome! ✅". The ATM renders **different UI conditionally**.

---

## 🔧 Methods of Conditional Rendering

### Method 1: `if` / `else` Statement (Outside JSX)

```tsx
function Greeting({ isLoggedIn }) {
  if (isLoggedIn) {
    return <h1>Welcome back! 👋</h1>;
  } else {
    return <h1>Please log in 🔐</h1>;
  }
}

// Usage
<Greeting isLoggedIn={true} />   // → Welcome back!
<Greeting isLoggedIn={false} />  // → Please log in
```

---

### Method 2: Ternary Operator `condition ? "yes" : "no"` (✅ Most popular)

```tsx
function AuthStatus({ user }) {
  return (
    <div>
      {user ? (
        <p>Hello, {user.name}! 🎉</p>
      ) : (
        <p>You are not logged in. Please <a href="/login">Login</a></p>
      )}
    </div>
  );
}
```

---

### Method 3: Short-circuit `&&` (Show or nothing)

Use when you only want to show something, and nothing otherwise:

```tsx
function Notification({ hasAlert }) {
  return (
    <div>
      <h1>Dashboard</h1>
      {hasAlert && <p>🚨 You have new notifications!</p>}
      {/* If hasAlert is false → renders nothing */}
    </div>
  );
}
```

> ⚠️ **Gotcha:** Don't use `0 && <Component />` because React renders `0` as text!
> ```tsx
> {0 && <Alert />}         // ❌ Renders "0" on screen
> {count > 0 && <Alert />} // ✅ Boolean condition
> ```

---

### Method 4: `||` Fallback (Default value)

```tsx
function UserName({ name }) {
  return <p>{name || "Anonymous User"}</p>;
  // If name is empty/null/undefined → shows "Anonymous User"
}
```

---

### Method 5: Switch/Object Map (Multiple conditions)

```tsx
function StatusBadge({ status }) {
  const statusMap = {
    active: { label: "Active ✅", color: "green" },
    pending: { label: "Pending ⏳", color: "orange" },
    inactive: { label: "Inactive ❌", color: "red" },
  };

  const info = statusMap[status] || { label: "Unknown", color: "gray" };

  return (
    <span style={{ color: info.color }}>
      {info.label}
    </span>
  );
}

// Usage
<StatusBadge status="active" />
<StatusBadge status="pending" />
```

---

## 🌍 Real-World Examples

### Example 1: Login/Logout Toggle

```tsx
function AuthPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <div>
      {isLoggedIn ? (
        <div>
          <h2>🏠 Dashboard</h2>
          <p>Welcome back!</p>
          <button onClick={() => setIsLoggedIn(false)}>Logout</button>
        </div>
      ) : (
        <div>
          <h2>🔐 Login Required</h2>
          <button onClick={() => setIsLoggedIn(true)}>Login</button>
        </div>
      )}
    </div>
  );
}
```

### Example 2: Loading Spinner

```tsx
function DataFetcher() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  // Simulate data load
  useEffect(() => {
    setTimeout(() => {
      setData({ name: "Nishant", role: "Developer" });
      setLoading(false);
    }, 2000);
  }, []);

  if (loading) return <p>⏳ Loading...</p>;
  if (!data) return <p>❌ No data found</p>;

  return <p>✅ {data.name} — {data.role}</p>;
}
```

### Example 3: Role-Based UI

```tsx
function Dashboard({ role }) {
  return (
    <div>
      <h1>Dashboard</h1>

      {role === "admin" && (
        <button>🛠️ Manage Users</button>
      )}

      {role === "editor" && (
        <button>✏️ Edit Content</button>
      )}

      {(role === "admin" || role === "editor") && (
        <button>📊 View Reports</button>
      )}
    </div>
  );
}

<Dashboard role="admin" />  // Shows: Manage Users + View Reports
<Dashboard role="editor" /> // Shows: Edit Content + View Reports
<Dashboard role="viewer" /> // Shows: nothing extra
```

---

## ❌ Common Mistakes / Tips

- ❌ Using `if` inside JSX return (use ternary or `&&` instead)
- ❌ `{0 && <Component />}` — renders `0` on screen
- ✅ Use `{count > 0 && <Component />}` for safe short-circuit
- ✅ Early return pattern: `if (loading) return <Spinner />;`
- 💡 Ternary = two outcomes, `&&` = one outcome (or nothing)

---

## 📝 Summary

| Method | Use When |
|---|---|
| `if/else` | Outside JSX, multiple complex conditions |
| Ternary `? :` | Two possible outputs inside JSX |
| `&&` | Show something or nothing |
| `\|\|` | Fallback / default value |
| Object map | Multiple values (like status codes) |

---

## 🎯 Practice Tasks

1. Build a **Login page**: show "Login Form" if logged out, show "Dashboard" if logged in
2. Build a **Notification Bell**: show a red dot only if there are unread notifications
3. Build a **Role Badge**: Admin = 🛡️, User = 👤, Guest = 👋
4. Build a **Loading screen**: show "Loading..." for 2 seconds, then show the content
5. Show a **"No results found"** message using `&&` when a search returns empty

---

← Previous: [07_event_handling.md](07_event_handling.md) | Next: [09_lists_and_keys.md](09_lists_and_keys.md) →
