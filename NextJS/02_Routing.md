# 02 – Routing in Next.js

---

## What is Routing?

Routing is the system that decides **which page to show** when a user visits a URL.

- User visits `/about` → Show the About page
- User visits `/products/shoes` → Show the Shoes product page
- User visits `/dashboard/settings` → Show the Settings page inside Dashboard

In Next.js, **routing is file-based** — you don't configure routes manually. You simply create files and folders, and Next.js automatically creates the routes.

---

## Why File-Based Routing?

### In Plain React (with react-router-dom):

```jsx
// You manually define every route
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
  <Route path="/products/:id" element={<Product />} />
  <Route path="/dashboard" element={<Dashboard />} />
</Routes>
```

**Problem:** As your app grows to 50+ pages, this file becomes huge and hard to manage.

### In Next.js:

```
app/
├── page.js          → /
├── about/
│   └── page.js      → /about
├── products/
│   └── [id]/
│       └── page.js  → /products/123, /products/456
└── dashboard/
    └── page.js      → /dashboard
```

**No route configuration needed.** Just create the file = route exists.

---

## How Routing Works in Next.js

### Rule 1: `page.js` Makes a Route

A folder only becomes a route if it contains a `page.js` (or `page.tsx`) file.

```
app/
├── about/
│   └── page.js      ✅ This creates /about
├── helpers/
│   └── utils.js     ❌ This does NOT create a route (no page.js)
```

### Rule 2: Nested Folders = Nested Routes

```
app/
├── dashboard/
│   ├── page.js           → /dashboard
│   ├── settings/
│   │   └── page.js       → /dashboard/settings
│   └── analytics/
│       └── page.js       → /dashboard/analytics
```

### Rule 3: Dynamic Routes with `[param]`

When you don't know the exact URL in advance (like product IDs), use square brackets.

```
app/
├── products/
│   └── [id]/
│       └── page.js       → /products/1, /products/abc, /products/anything
```

```jsx
// app/products/[id]/page.js
export default function ProductPage({ params }) {
  return <h1>Product ID: {params.id}</h1>;
}

// Visiting /products/42 → Shows "Product ID: 42"
```

### Rule 4: Catch-All Routes with `[...slug]`

Catch multiple segments in a single route.

```
app/
├── docs/
│   └── [...slug]/
│       └── page.js
```

```jsx
// app/docs/[...slug]/page.js
export default function DocsPage({ params }) {
  return <p>Path: {params.slug.join('/')}</p>;
}

// /docs/intro          → slug = ['intro']
// /docs/guide/setup    → slug = ['guide', 'setup']
// /docs/a/b/c          → slug = ['a', 'b', 'c']
```

**Real-world Example:** Documentation sites like Next.js docs use catch-all routes. One route handler can handle `/docs/getting-started`, `/docs/api/reference`, etc.

### Rule 5: Route Groups with `(groupName)`

Organize routes without affecting the URL structure.

```
app/
├── (marketing)/
│   ├── about/
│   │   └── page.js       → /about (NOT /marketing/about)
│   └── pricing/
│       └── page.js       → /pricing
├── (dashboard)/
│   ├── settings/
│   │   └── page.js       → /settings
│   └── profile/
│       └── page.js       → /profile
```

The parentheses `()` tell Next.js: "This is for organization only — don't include it in the URL."

**Real-world Example:** Separating your marketing pages (about, pricing) from dashboard pages (settings, profile) without affecting URLs.

---

## Impact – Why It Matters

| Scenario | How Routing Helps |
|----------|-------------------|
| **Amazon** | `/products/[id]` → Dynamic route for millions of products |
| **Instagram** | `/[username]` → Dynamic route for every user's profile |
| **Blog** | `/blog/[slug]` → Each blog post gets its own URL |
| **Dashboard** | Nested routes: `/dashboard/analytics`, `/dashboard/settings` |

---

## ⭐ Most Important Concepts

### 1. Special Files in App Router

Next.js uses special file names for specific purposes:

| File | Purpose | When to Use |
|------|---------|------------|
| `page.js` | Defines the UI for a route | Every route needs one |
| `layout.js` | Shared UI wrapper for child routes | Navigation, sidebars |
| `loading.js` | Loading UI (shown while page loads) | Better UX during data fetch |
| `error.js` | Error boundary UI | Graceful error handling |
| `not-found.js` | 404 page | Custom "page not found" |
| `template.js` | Like layout but re-renders on navigation | Animations, logging |

```jsx
// app/dashboard/loading.js
export default function Loading() {
  return <div className="spinner">Loading dashboard...</div>;
}
// This automatically shows when /dashboard is loading!
```

```jsx
// app/dashboard/error.js
"use client"; // Error boundaries must be client components

export default function Error({ error, reset }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try Again</button>
    </div>
  );
}
```

### 2. Navigation Between Pages

#### Method 1: `<Link>` Component (Most Common)

```jsx
import Link from 'next/link';

export default function Navbar() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href="/products/42">Product 42</Link>
    </nav>
  );
}
```

**Why `<Link>` instead of `<a>`?**
- `<Link>` does **client-side navigation** (no full page reload → faster)
- `<Link>` **prefetches** linked pages in the background (instant transitions)
- `<a>` causes a **full page reload** (slower, loses state)

#### Method 2: `useRouter()` Hook (Programmatic Navigation)

```jsx
"use client";

import { useRouter } from 'next/navigation';

export default function LoginForm() {
  const router = useRouter();

  const handleLogin = () => {
    // ... login logic
    router.push('/dashboard');       // Navigate to dashboard
    // router.replace('/dashboard'); // Navigate without adding to browser history
    // router.back();               // Go back
  };

  return <button onClick={handleLogin}>Login</button>;
}
```

### 3. Parallel Routes (Advanced)

Show multiple pages simultaneously in the same layout.

```
app/
├── layout.js
├── @feed/
│   └── page.js        → Feed section
├── @sidebar/
│   └── page.js        → Sidebar section
└── page.js            → Main content
```

```jsx
// app/layout.js
export default function Layout({ children, feed, sidebar }) {
  return (
    <div style={{ display: 'flex' }}>
      <div>{sidebar}</div>
      <div>{children}</div>
      <div>{feed}</div>
    </div>
  );
}
```

**Real-world Example:** A social media dashboard where the feed, notifications, and sidebar load independently and can have separate loading/error states.

---

## Interview Questions & Answers

### Q1: How does routing work in Next.js?
**Answer:** Next.js uses file-based routing. In the App Router, you create folders inside the `app/` directory and add a `page.js` file inside to define a route. The folder structure directly maps to URL paths. For example, `app/about/page.js` maps to `/about`.

### Q2: What is a dynamic route in Next.js?
**Answer:** A dynamic route handles URLs where part of the path is variable. You create it by wrapping the folder name in square brackets: `[param]`. For example, `app/products/[id]/page.js` handles `/products/1`, `/products/abc`, etc. The variable value is accessible via `params.id`.

### Q3: What is the difference between `<Link>` and `<a>` tag?
**Answer:**
- `<Link>` performs **client-side navigation** — no full page reload, preserves state, and prefetches pages in the background for instant transitions.
- `<a>` triggers a **full page reload** — the browser fetches everything from scratch, losing React state and being slower.
Always use `<Link>` for internal navigation in Next.js.

### Q4: What are Route Groups and why do we use them?
**Answer:** Route Groups are created with parentheses `(groupName)`. They organize route files into logical groups without affecting the URL. For example, `app/(marketing)/about/page.js` still maps to `/about`, not `/marketing/about`. Useful for separating concerns like marketing pages vs dashboard pages.

### Q5: What is a catch-all route?
**Answer:** A catch-all route uses `[...slug]` syntax to match any number of URL segments. `app/docs/[...slug]/page.js` matches `/docs/intro`, `/docs/guide/setup`, `/docs/a/b/c`, etc. The `slug` parameter is an array of all matched segments.

### Q6: Explain the special files in the App Router.
**Answer:**
- `page.js` — Defines the page UI
- `layout.js` — Shared wrapper that persists across navigations
- `loading.js` — Shown during page loading (Suspense-based)
- `error.js` — Error boundary for graceful error handling
- `not-found.js` — Custom 404 page
- `template.js` — Like layout but re-creates on each navigation

### Q7: What is the difference between `router.push()` and `router.replace()`?
**Answer:** `router.push('/page')` adds a new entry to the browser's history stack (user can press Back). `router.replace('/page')` replaces the current history entry (user cannot press Back to the previous page). Use `replace` after login redirects to prevent going back to the login page.

### Q8 (Scenario): You're building an e-commerce site with 10,000 products. How would you structure the product page routes?
**Answer:** I'd use a dynamic route: `app/products/[id]/page.js`. This single file handles all 10,000 product URLs (`/products/1` to `/products/10000`). The `params.id` value would be used to fetch the specific product data. For SEO, I'd combine this with `generateStaticParams()` to pre-render the most popular product pages.

### Q9 (Scenario): Your dashboard has 3 sections that load independently. How would you structure it?
**Answer:** I'd use Parallel Routes with named slots: `@analytics`, `@users`, and `@reports` inside the dashboard folder. Each slot loads independently with its own `loading.js` and `error.js`. The dashboard `layout.js` receives all three as props and renders them in a grid layout.

### Q10: What happens if you create a folder without a `page.js` file?
**Answer:** It does NOT create a route. The folder is simply used for organization or to hold other files like components, utilities, or styles. Only folders that contain a `page.js` file become accessible URL routes.

---

### 🔗 Navigation

---

← Previous: [01_Introduction.md](01_Introduction.md) | Next: [03_Rendering_Methods.md](03_Rendering_Methods.md) →
