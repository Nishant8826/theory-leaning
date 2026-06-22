# 17 - React Router (Routing) 🗺️

> [!NOTE]
> ### 💡 Topic Quick Overview (For Beginners)
> - **What is it?** React Router is a routing library that enables single-page applications (SPAs) to have multiple page views with distinct URLs.
> - **Why do we use it?** By default, React applications run on a single HTML page. React Router updates the browser URL and swaps views dynamically without reloading the entire page.
> - **How does it work?** Define page routes inside a `<Routes>` component mapping URLs to pages, navigate using the `<Link>` component, and extract parameters using hooks like `useParams`.

---

## 🤔 What is Routing?

Routing means **navigating between different pages** in your app without refreshing the browser.

---

## 📦 Installing React Router

```bash
npm install react-router-dom
```

---

## Hinglish Explanation

React Router Single Page Applications (SPAs) me routing enable karne ki standard library hai. Yeh browser URL ke matching path ke basis par page component ko bina reload kiye dynamically swap (change) karti hai.

* **Core Components:**
  1. **`<BrowserRouter>`:** Poore application me routing context aur history APIs ko activate karne ke liye root tree par wrap kiya jata hai.
  2. **`<Routes>` aur `<Route>`:** URLs path mapping configurations define karte hain. Target URL match hone par element render hota hai.
  3. **`<Link>` vs `<NavLink>` vs `<a>`:** Simple HTML `<a>` tag use karne se page full reload ho jata hai, jo SPA rules ke khilaf hai. Iske badle `<Link>` routing support ke sath navigation handle karta hai. `<NavLink>` current active route link par automatic styling parameters detect karne me help karta hai.
* **Routing Hooks:**
  1. **`useParams()`:** Dynamic URLs se values read karta hai (jaise `/products/:id` se `:id`).
  2. **`useSearchParams()`:** URL queries filter parameters read aur change karta hai (jaise `?category=books`).
  3. **`useNavigate()`:** Button clicks ya calculations complete hone par JavaScript logic se directly navigation routes trigger karne ke kaam aata hai (jaise redirection on login success).

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

← Previous: [16_context_api.md](16_context_api.md) | Index: [00_Index.md](00_Index.md) | Next: [18_api_calls.md](18_api_calls.md) →
