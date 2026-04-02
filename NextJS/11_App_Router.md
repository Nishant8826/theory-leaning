# 11 – App Router (Deep Dive)

---

## What is the App Router?

The App Router is Next.js's **modern routing system** introduced in Next.js 13. It lives in the `app/` directory and replaces the older `pages/` directory (Pages Router).

It's not just a routing upgrade — it fundamentally changes how you build Next.js apps:
- React Server Components are the default
- Layouts are nested and persistent
- Data fetching uses native `async/await`
- Streaming and Suspense are built-in

---

## Why Was the App Router Introduced?

### Problems with the Pages Router:

| Problem | Impact |
|---------|--------|
| Layouts were manual and fragile (`_app.js`, `_document.js`) | Sharing UI across pages was messy |
| All components were Client Components | Unnecessary JavaScript sent to browser |
| Data fetching used special functions (`getServerSideProps`) | Not composable, page-level only |
| No built-in loading/error states | Manual loading spinners and error handling |
| No streaming | Entire page blocked until all data loaded |

### How the App Router Fixes These:

| Feature | Pages Router | App Router |
|---------|-------------|------------|
| Routing | `pages/` directory | `app/` directory |
| Components | All Client by default | Server by default |
| Layouts | `_app.js` (one global layout) | Nested `layout.js` (per route) |
| Data Fetching | `getServerSideProps()` | `async/await` in components |
| Loading States | Manual | Automatic `loading.js` |
| Error Handling | Manual | Automatic `error.js` |
| Streaming | Not supported | Built-in with Suspense |

---

## How the App Router Works

### File Convention

The App Router uses **file conventions** — specific file names serve specific purposes:

```
app/
├── layout.js          ← Root layout (wraps everything)
├── page.js            ← Home page (/)
├── loading.js         ← Loading UI for home
├── error.js           ← Error UI for home
├── not-found.js       ← Custom 404 page
├── template.js        ← Re-renders on navigation
│
├── dashboard/
│   ├── layout.js      ← Dashboard layout (sidebar)
│   ├── page.js        ← /dashboard
│   ├── loading.js     ← Loading for dashboard
│   ├── error.js       ← Error for dashboard
│   │
│   ├── settings/
│   │   └── page.js    ← /dashboard/settings
│   └── analytics/
│       └── page.js    ← /dashboard/analytics
│
├── blog/
│   ├── page.js        ← /blog (list all posts)
│   └── [slug]/
│       └── page.js    ← /blog/my-first-post (dynamic)
│
├── (marketing)/       ← Route Group (no URL impact)
│   ├── about/
│   │   └── page.js    ← /about
│   └── pricing/
│       └── page.js    ← /pricing
│
└── api/
    └── users/
        └── route.js   ← API Route: /api/users
```

### Component Rendering Hierarchy

When a user visits `/dashboard/settings`:

```
RootLayout (app/layout.js)
  └── DashboardLayout (app/dashboard/layout.js)
        └── SettingsPage (app/dashboard/settings/page.js)
```

If `loading.js` exists:
```
RootLayout
  └── DashboardLayout
        └── Loading... (shown until SettingsPage is ready)
              └── SettingsPage (replaces Loading when ready)
```

---

## ⭐ Most Important Concepts

### 1. Server Components — The Default

Every component in the App Router is a Server Component **unless** you add `"use client"`.

```jsx
// ✅ Server Component (default)
// This code NEVER reaches the user's browser
export default async function UsersPage() {
  // Direct database query — safe, no API needed
  const users = await prisma.user.findMany();

  return (
    <ul>
      {users.map(u => <li key={u.id}>{u.name}</li>)}
    </ul>
  );
}
```

**Why this matters:**
- Zero JS sent to browser for this component (faster load)
- Can safely use database queries, file system, secrets
- Reduces the total JavaScript bundle significantly

### 2. Nested Layouts (Persistent)

```jsx
// app/layout.js — Global: Navbar + Footer
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <nav>Global Navbar</nav>
        <main>{children}</main>
        <footer>Global Footer</footer>
      </body>
    </html>
  );
}
```

```jsx
// app/dashboard/layout.js — Dashboard: Sidebar
export default function DashboardLayout({ children }) {
  return (
    <div style={{ display: 'flex' }}>
      <aside>
        <h3>Dashboard</h3>
        <a href="/dashboard">Overview</a>
        <a href="/dashboard/settings">Settings</a>
      </aside>
      <section>{children}</section>
    </div>
  );
}
```

**Critical behavior:** When you navigate from `/dashboard/settings` to `/dashboard/analytics`:
- ❌ Root layout does NOT re-render
- ❌ Dashboard layout does NOT re-render
- ✅ Only the page content changes

This means sidebar state, scroll position, and input values are **preserved**.

### 3. Loading & Error States (Automatic)

```jsx
// app/dashboard/loading.js
export default function Loading() {
  return (
    <div className="loading-container">
      <div className="spinner" />
      <p>Loading dashboard data...</p>
    </div>
  );
}
// Automatically wraps the page in a Suspense boundary
```

```jsx
// app/dashboard/error.js
"use client"; // Error boundaries must be Client Components

import { useEffect } from 'react';

export default function Error({ error, reset }) {
  useEffect(() => {
    // Log the error to your monitoring service
    console.error('Dashboard error:', error);
  }, [error]);

  return (
    <div>
      <h2>Something went wrong in the Dashboard!</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try Again</button>
    </div>
  );
}
```

**Impact:** No more manual try-catch in every component. The error stays contained in the section that failed — the rest of the app keeps working.

### 4. Intercepting Routes (Advanced)

Show a modal from one route while keeping the current page visible.

**Real-world Example:** Instagram — clicking a photo opens a modal. Refreshing the page shows the full photo page.

```
app/
├── feed/
│   └── page.js            ← Feed page
├── photo/
│   └── [id]/
│       └── page.js        ← Full photo page (/photo/123)
└── @modal/
    └── (.)photo/
        └── [id]/
            └── page.js    ← Modal version (intercepted)
```

- Click a photo link → Modal opens over the feed (intercepted route)
- Refresh/direct visit `/photo/123` → Full photo page loads

### 5. Parallel Routes

Render multiple pages simultaneously within one layout.

```
app/
├── layout.js
├── page.js
├── @team/
│   ├── page.js
│   └── loading.js
├── @analytics/
│   ├── page.js
│   └── loading.js
```

```jsx
// app/layout.js
export default function Layout({ children, team, analytics }) {
  return (
    <div>
      <div>{children}</div>
      <div>{team}</div>       {/* Loads independently */}
      <div>{analytics}</div>  {/* Loads independently */}
    </div>
  );
}
```

**Impact:** Each slot (`@team`, `@analytics`) has its own loading and error states. If analytics data fails, the team section still works.

---

## Impact — Pages Router vs App Router Migration

| Feature | Pages Router | App Router Equivalent |
|---------|-------------|----------------------|
| `pages/index.js` | `app/page.js` |
| `pages/about.js` | `app/about/page.js` |
| `pages/_app.js` | `app/layout.js` |
| `pages/_document.js` | `app/layout.js` (includes `<html>`, `<body>`) |
| `pages/api/users.js` | `app/api/users/route.js` |
| `getServerSideProps` | `fetch(url, { cache: 'no-store' })` |
| `getStaticProps` | `fetch(url)` (default cached) |
| `getStaticPaths` | `generateStaticParams()` |

---

## Interview Questions & Answers

### Q1: What is the App Router and how is it different from the Pages Router?
**Answer:** The App Router (Next.js 13+) uses the `app/` directory with React Server Components as the default, nested layouts via `layout.js`, automatic loading/error states, and native `async/await` data fetching. The Pages Router uses `pages/` with all Client Components and special functions like `getServerSideProps`. The App Router is the recommended approach for new projects.

### Q2: What happens when you navigate between pages that share a layout?
**Answer:** The shared layout does NOT re-render. Only the page content (the `children` inside the layout) changes. This preserves state (like form inputs, scroll position, sidebar state) and makes navigation feel instant.

### Q3: How do loading states work in the App Router?
**Answer:** By creating a `loading.js` file in a route folder, Next.js automatically wraps the `page.js` with a React Suspense boundary. The loading UI is shown while the page's async data loads, and it's replaced by the actual content once ready.

### Q4: What are Route Groups and why would you use them?
**Answer:** Route Groups use parentheses `(groupName)` in folder names to organize routes without affecting the URL. For example, `app/(marketing)/about/page.js` maps to `/about`, not `/marketing/about`. They're useful for applying different layouts to different sections (marketing pages vs dashboard pages) while keeping URLs clean.

### Q5: What are Parallel Routes?
**Answer:** Parallel Routes (using `@slotName` folders) render multiple pages simultaneously within one layout. Each slot loads independently with its own loading and error states. Useful for dashboards where different sections fetch data independently.

### Q6: What are Intercepting Routes?
**Answer:** Intercepting Routes let you load a route within the context of the current page (like a modal) while keeping the original page visible. If the user refreshes or navigates directly to the URL, the full page loads instead. Instagram uses this pattern — clicking a photo shows a modal, refreshing shows the full photo page.

### Q7 (Scenario): You're migrating from Pages Router to App Router. What's your approach?
**Answer:** Migrate incrementally — both routers can coexist. Start by creating the `app/` directory. Move simple pages first, converting `getServerSideProps` to `fetch({ cache: 'no-store' })` and `getStaticProps` to default cached `fetch()`. Move layouts from `_app.js` to `app/layout.js`. Convert pages to Server Components where possible, adding `"use client"` only where needed.

---

### 🔗 Navigation

---

← Previous: [10_Deployment.md](10_Deployment.md) | Next: [12_Middleware.md](12_Middleware.md) →
