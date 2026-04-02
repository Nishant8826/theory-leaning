# 17 - React Router (Routing) 🗺️


---

## 🤔 What is Routing?

Routing means **navigating between different pages** in your app without refreshing the browser.

---

## 📦 Installing React Router

```bash
npm install react-router-dom
```

---

## 🔧 Basic Setup (React Router v6)

```jsx
// main.jsx or App.jsx
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

// Pages
import Home from "./pages/Home";
import About from "./pages/About";
import Contact from "./pages/Contact";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <BrowserRouter>
      {/* Navigation */}
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">Contact</Link>
      </nav>

      {/* Routes — only matching route renders */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="*" element={<NotFound />} />  {/* 404 catch-all */}
      </Routes>
    </BrowserRouter>
  );
}
```

---

## 🔑 Core Components

| Component | Use |
|---|---|
| `<BrowserRouter>` | Wraps the app, enables routing |
| `<Routes>` | Container for all Route definitions |
| `<Route path="" element={}>` | Defines a route (URL → component) |
| `<Link to="">` | Navigation link (no page refresh!) |
| `<NavLink to="">` | Like Link, but knows if it's active |
| `<Navigate to="">` | Redirect programmatically in JSX |

---

## 🔄 `<Link>` vs `<NavLink>` vs `<a>`

```jsx
// ❌ Regular <a> — reloads the page!
<a href="/about">About</a>

// ✅ <Link> — no reload, SPA navigation
<Link to="/about">About</Link>

// ✅ <NavLink> — adds "active" class automatically when on that page
<NavLink to="/about" style={({ isActive }) => ({ color: isActive ? "blue" : "black" })}>
  About
</NavLink>
```

---

## 🌍 Real-World Complete Example

### Folder Structure
```
src/
├── pages/
│   ├── Home.jsx
│   ├── About.jsx
│   ├── Products.jsx
│   ├── ProductDetail.jsx  ← dynamic route
│   └── NotFound.jsx
├── components/
│   └── Navbar.jsx
└── App.jsx
```

### App.jsx
```jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Products from "./pages/Products";
import ProductDetail from "./pages/ProductDetail";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/products/:id" element={<ProductDetail />} />  {/* Dynamic! */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```

### Navbar.jsx
```jsx
import { NavLink } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <NavLink to="/" style={({ isActive }) => ({ color: isActive ? "blue" : "gray" })}>
        Home
      </NavLink>
      <NavLink to="/products" style={({ isActive }) => ({ color: isActive ? "blue" : "gray" })}>
        Products
      </NavLink>
    </nav>
  );
}
```

---

## 🔗 Dynamic Routes (URL Parameters)

```jsx
// Route definition
<Route path="/products/:id" element={<ProductDetail />} />

// ProductDetail.jsx — reads the :id from URL
import { useParams } from "react-router-dom";

function ProductDetail() {
  const { id } = useParams(); // Gets "123" from /products/123

  return (
    <div>
      <h2>Product #{id}</h2>
      <p>Showing details for product with ID: {id}</p>
    </div>
  );
}
```

---

## 🔍 Query Parameters (Search/Filter)

```jsx
// URL: /search?q=react&category=books
import { useSearchParams } from "react-router-dom";

function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get("q") || "";
  const category = searchParams.get("category") || "all";

  return (
    <div>
      <p>Searching: {query} in {category}</p>
      <button onClick={() => setSearchParams({ q: "javascript", category: "courses" })}>
        Search JS Courses
      </button>
    </div>
  );
}
```

---

## 🧭 Programmatic Navigation

```jsx
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const navigate = useNavigate();

  const handleLogin = () => {
    // ... login logic
    navigate("/dashboard");           // Go to dashboard
    navigate("/home", { replace: true }); // Replace history (no back button)
    navigate(-1);                    // Go back (like browser back button)
  };

  return <button onClick={handleLogin}>Login</button>;
}
```

---

## 🔒 Protected Routes

```jsx
function ProtectedRoute({ children }) {
  const { user } = useAuth(); // From Context

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

// Usage
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>
```

---

## 📁 Nested Routes

```jsx
<Routes>
  <Route path="/dashboard" element={<DashboardLayout />}>
    <Route index element={<DashboardHome />} />         {/* /dashboard */}
    <Route path="profile" element={<Profile />} />      {/* /dashboard/profile */}
    <Route path="settings" element={<Settings />} />    {/* /dashboard/settings */}
  </Route>
</Routes>

// DashboardLayout.jsx
import { Outlet } from "react-router-dom";

function DashboardLayout() {
  return (
    <div>
      <Sidebar />
      <Outlet />  {/* Child routes render here! */}
    </div>
  );
}
```

---

## ❌ Common Mistakes / Tips

- ❌ Using `<a href="">` instead of `<Link to="">` — it reloads the page!
- ❌ Forgetting to wrap app with `<BrowserRouter>`
- ❌ Defining routes outside `<Routes>`
- ✅ Put `<BrowserRouter>` in `main.jsx` (not App.jsx) for full app coverage
- ✅ Always have a `*` catch-all route for 404 pages
- 💡 `useParams()` for URL params, `useSearchParams()` for query strings, `useNavigate()` for redirecting

---

## 📝 Summary

- React Router enables **SPA navigation** (no page reload)
- Install: `npm install react-router-dom`
- `BrowserRouter` → wraps app | `Routes` → container | `Route` → mapping
- `Link`/`NavLink` for navigation, `useNavigate` for programmatic
- `useParams()` for `:id` in URL, `useSearchParams()` for `?key=value`
- Use nested routes + `<Outlet>` for layouts

---

## 🎯 Practice Tasks

1. Create a 3-page app: Home, About, Contact — with a working navbar
2. Add a **Products** page with a list of products. Clicking one opens `/products/:id`
3. Build a **404 Not Found** page using the `*` route
4. Add a **protected route** — `/dashboard` only accessible when "logged in"
5. Add `NavLink` to the navbar with highlighted active link styling

---

← Previous: [16_context_api.md](16_context_api.md) | Next: [18_api_calls.md](18_api_calls.md) →
