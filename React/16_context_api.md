# 16 - Context API 🌐


---

## 🤔 What is Context API?

Context API lets you **share data globally** across your whole app without passing props through every level.

---

## 😫 The Problem: Prop Drilling

```
App (holds user data)
  └── Layout
        └── Sidebar
              └── UserMenu
                    └── UserAvatar  ← Only this needs the data!
```

Without Context, you'd have to pass `user` as a prop through **every** level, even if Layout and Sidebar don't need it. That's **prop drilling** — messy and annoying!

---

## 🧰 Context API: 3 Steps

### Step 1: Create the Context
```jsx
// UserContext.js
import { createContext } from "react";

const UserContext = createContext(null); // Create context with default value
export default UserContext;
```

### Step 2: Provide the Context (Wrap components)
```jsx
// App.jsx
import UserContext from "./UserContext";

function App() {
  const user = { name: "Nishant", role: "Admin" };

  return (
    <UserContext.Provider value={user}>
      {/* All children can now access `user` directly! */}
      <Layout />
    </UserContext.Provider>
  );
}
```

### Step 3: Consume the Context (Use it anywhere!)
```jsx
// UserAvatar.jsx — deep inside the tree, no prop drilling!
import { useContext } from "react";
import UserContext from "./UserContext";

function UserAvatar() {
  const user = useContext(UserContext); // Get data directly!

  return (
    <div>
      <span>👤 {user.name}</span>
      <span>🛡️ {user.role}</span>
    </div>
  );
}
```

---

## 🌍 Real-World Example: Theme Switcher

```jsx
// ThemeContext.js
import { createContext, useContext, useState } from "react";

const ThemeContext = createContext();

// Custom provider component (best practice — keep logic here!)
export function ThemeProvider({ children }) {
  const [isDark, setIsDark] = useState(false);

  const toggleTheme = () => setIsDark(!isDark);

  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Custom hook for easy access
export function useTheme() {
  return useContext(ThemeContext);
}
```

```jsx
// App.jsx
import { ThemeProvider } from "./ThemeContext";

function App() {
  return (
    <ThemeProvider>
      <Navbar />
      <HomePage />
      <Footer />
    </ThemeProvider>
  );
}
```

```jsx
// Navbar.jsx — can use theme without any props!
import { useTheme } from "./ThemeContext";

function Navbar() {
  const { isDark, toggleTheme } = useTheme();

  return (
    <nav style={{ background: isDark ? "#333" : "#fff", color: isDark ? "#fff" : "#000" }}>
      <h1>MyApp</h1>
      <button onClick={toggleTheme}>
        {isDark ? "☀️ Light Mode" : "🌙 Dark Mode"}
      </button>
    </nav>
  );
}
```

```jsx
// Footer.jsx — also uses theme without any props!
import { useTheme } from "./ThemeContext";

function Footer() {
  const { isDark } = useTheme();
  return (
    <footer style={{ background: isDark ? "#222" : "#f5f5f5" }}>
      <p>© 2025 MyApp</p>
    </footer>
  );
}
```

---

## 🔐 Real-World Example: Auth Context

```jsx
// AuthContext.js
import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = (userData) => setUser(userData);
  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
```

```jsx
// LoginPage.jsx
import { useAuth } from "./AuthContext";

function LoginPage() {
  const { login } = useAuth();

  const handleLogin = () => {
    login({ name: "Nishant", email: "nishant@dev.com" });
  };

  return <button onClick={handleLogin}>Login</button>;
}

// Navbar.jsx
function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav>
      {user ? (
        <>
          <span>Welcome, {user.name}!</span>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <a href="/login">Login</a>
      )}
    </nav>
  );
}
```

---

## 📦 Multiple Contexts

You can have multiple providers — just nest them:

```jsx
function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <LanguageProvider>
          <Router>
            <AppRoutes />
          </Router>
        </LanguageProvider>
      </ThemeProvider>
    </AuthProvider>
  );
}
```

---

## 🆚 Context API vs Redux vs Props

| | Props | Context API | Redux |
|---|---|---|---|
| Best for | Local component data | App-wide simple state | Complex, large apps |
| Setup | None | Minimal | More setup needed |
| Performance | Fast | Re-renders all consumers | Optimized with selectors |
| DevTools | None | Basic | Excellent |
| Use for | Component customization | Theme, auth, language | Cart, notifications, complex state |

---

## ❌ Common Mistakes / Tips

- ❌ Using Context for rapidly changing state (causes many re-renders!)
- ❌ Putting all app state in one Context (split into multiple)
- ✅ Create a **custom hook** (`useTheme`, `useAuth`) for cleaner consumption
- ✅ Keep the Context provider in a separate file (e.g., `ThemeContext.jsx`)
- 💡 For simple apps, Context is fine. For complex apps, consider Zustand or Redux Toolkit

---

## 📝 Summary

- Context API solves **prop drilling** by sharing state globally
- Three steps: **Create** → **Provide** → **Consume**
- Use `createContext()` to create, `Provider` to wrap, `useContext()` to read
- Create **custom hooks** for clean, reusable context access
- Best for: theme, auth, language, global UI state

---

## 🎯 Practice Tasks

1. Build a **theme toggle** (dark/light mode) using Context that applies to the whole app
2. Build an **auth system** — login shows "Welcome, [Name]", logout shows "Login" button — using Context
3. Build a **language switcher** (English/Hindi) using Context
4. Create a **shopping cart context** that can be accessed from both a product page and a cart page
5. Try using multiple contexts in the same app (theme + auth)

---

← Previous: [15_lifting_state_up.md](15_lifting_state_up.md) | Next: [17_react_router.md](17_react_router.md) →
