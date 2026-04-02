# 19 - Error Handling in React ⚠️


---

## 🤔 Why Error Handling?

Things go wrong — APIs fail, users type invalid inputs, code has bugs. Good error handling means your app **doesn't crash** and users see helpful messages instead of a broken screen.

> **Real-world analogy:**
> A good pilot doesn't just know how to fly in clear weather. They also know what to do when an engine fails (error!). React error handling is your app's emergency plan.

---

## 📦 Types of Errors in React

| Type | Example |
|---|---|
| **API Errors** | Network down, 404, 500 |
| **Runtime Errors** | Undefined property, null access |
| **User Input Errors** | Invalid form data |
| **Component Errors** | Component throws during render |

---

## 🧱 Error Boundaries (React's Built-in Safety Net)

An **Error Boundary** is a component that **catches JavaScript errors** in the component tree and shows a fallback UI instead of crashing the whole app.

> Think of it like a try/catch for your UI!

```tsx
import React from "react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  // Catches render errors in children
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  // Log error details
  componentDidCatch(error, errorInfo) {
    console.error("Error caught:", error, errorInfo);
    // You can send this to an error reporting service like Sentry
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: "20px", border: "2px solid red", borderRadius: "8px" }}>
          <h2>😢 Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            🔄 Try Again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
```

### How to Use Error Boundary:

```tsx
import ErrorBoundary from "./ErrorBoundary";

function App() {
  return (
    <ErrorBoundary>
      <Navbar />
      <ErrorBoundary>  {/* Wrap individual sections too! */}
        <UserProfile />
      </ErrorBoundary>
      <Footer />
    </ErrorBoundary>
  );
}
```

> 💡 Error boundaries only catch errors in **render/lifecycle**, NOT in event handlers or async code!

---

## 🌐 API Error Handling

```tsx
function UserData() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetch("https://api.example.com/user");

        if (!res.ok) {
          // HTTP error (4xx, 5xx)
          throw new Error(`HTTP Error ${res.status}: ${res.statusText}`);
        }

        const json = await res.json();
        setData(json);
      } catch (err) {
        if (err.name === "AbortError") return; // Ignore cancel errors
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  // Handle states
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={() => window.location.reload()} />;
  if (!data) return <p>No data available</p>;

  return <UserCard user={data} />;
}

// Reusable error component
function ErrorMessage({ message, onRetry }) {
  return (
    <div className="error-box">
      <p>❌ {message}</p>
      {onRetry && <button onClick={onRetry}>🔄 Retry</button>}
    </div>
  );
}
```

---

## 📋 Form Validation Error Handling

```tsx
function LoginForm() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState("");
  const [loading, setLoading] = useState(false);

  const validate = () => {
    const newErrors = {};
    if (!form.email) newErrors.email = "Email is required";
    else if (!/\S+@\S+\.\S+/.test(form.email)) newErrors.email = "Invalid email format";
    if (!form.password) newErrors.password = "Password is required";
    else if (form.password.length < 6) newErrors.password = "Password must be 6+ characters";
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validate();

    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setLoading(true);
    setSubmitError("");

    try {
      await axios.post("/api/login", form);
      alert("Login successful! 🎉");
    } catch (err) {
      setSubmitError(
        err.response?.data?.message || "Login failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {submitError && (
        <div style={{ color: "red", background: "#ffe0e0", padding: "10px", borderRadius: "8px" }}>
          ❌ {submitError}
        </div>
      )}

      <div>
        <input
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          style={{ borderColor: errors.email ? "red" : "" }}
        />
        {errors.email && <span style={{ color: "red" }}>{errors.email}</span>}
      </div>

      <div>
        <input
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          style={{ borderColor: errors.password ? "red" : "" }}
        />
        {errors.password && <span style={{ color: "red" }}>{errors.password}</span>}
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "Logging in... ⏳" : "Login"}
      </button>
    </form>
  );
}
```

---

## 🛡️ Axios Error Handling (Detailed)

```tsx
try {
  const res = await axios.get("/api/user");
  setUser(res.data);
} catch (error) {
  if (error.response) {
    // Server responded with error (4xx, 5xx)
    console.error("Server error:", error.response.status, error.response.data);
    setError(`Server error: ${error.response.status}`);
  } else if (error.request) {
    // Request was made but no response (network issue)
    console.error("Network error — no response");
    setError("Network error. Check your connection.");
  } else {
    // Something else
    console.error("Unexpected error:", error.message);
    setError("Unexpected error occurred.");
  }
}
```

---

## 🔔 Toast Notifications for Errors

Instead of showing errors inline, use toast notifications for a better UX:

```bash
npm install react-toastify
```

```tsx
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/items/${id}`);
      toast.success("Item deleted! ✅");
    } catch {
      toast.error("Failed to delete item ❌");
    }
  };

  return (
    <div>
      <ToastContainer position="top-right" />
      <button onClick={() => handleDelete(1)}>Delete</button>
    </div>
  );
}
```

---

## ❌ Common Mistakes / Tips

- ❌ Not handling errors at all — blank screen or crash for users
- ❌ Showing raw error messages to users (show friendly ones!)
- ❌ Not checking `res.ok` when using `fetch`
- ✅ Always have `loading`, `error`, `data` states for async operations
- ✅ Use ErrorBoundary to catch render errors globally
- ✅ Show friendly messages and retry options to users
- 💡 Log full errors to console (or Sentry), but show simplified messages to users

---

## 📝 Summary

- **Error Boundaries** — catch render errors in component trees (class component)
- **API errors** — handle with `try/catch`, check `res.ok` for `fetch`
- **Form errors** — validate before submit, show inline messages
- **Axios errors** — check `err.response`, `err.request`, fallback
- Always show **user-friendly messages**, not raw errors
- Use `react-toastify` for quick toast-style notifications

---

## 🎯 Practice Tasks

1. Create an `ErrorBoundary` component and wrap your app with it. Trigger an error and see it catch!
2. Fetch from a **fake broken URL** and show a friendly error message with a retry button
3. Add **inline validation** to a form — show error messages under each field
4. Handle **network errors** separately from API errors in axios
5. Install `react-toastify` and show success/error toasts for CRUD operations

---

← Previous: [18_api_calls.md](18_api_calls.md) | Next: [20_custom_hooks.md](20_custom_hooks.md) →
