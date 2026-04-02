# 06 – Components & Layouts in Next.js

---

## What are Components and Layouts?

### Components
A **component** is a reusable piece of UI. Buttons, cards, navbars, footers — all implemented as components.

### Layouts
A **layout** is a component that **wraps** your pages and provides shared UI (like a navbar and footer) across multiple pages. Instead of repeating the same UI code on every page, you define it once in a layout.

```
Without Layouts:                    With Layouts:
┌──────────────┐                   ┌──────────────┐
│   Navbar     │ (repeated)        │   Navbar     │ ← Defined ONCE
│──────────────│                   │──────────────│    in layout.js
│   Page A     │                   │   Page A     │
│──────────────│                   │──────────────│
│   Footer     │ (repeated)        │   Footer     │ ← Defined ONCE
└──────────────┘                   └──────────────┘
```

---

## Why Do They Matter?

| Problem | Solution |
|---------|---------|
| Navbar/footer duplicated in every page | Use `layout.js` to define shared UI once |
| Large components with mixed server/client logic | Split into Server + Client components |
| UI not reusable | Build small, composable components |
| Navigation causes full page reload | Layouts persist between navigations (no re-render) |

---

## How Layouts Work in Next.js

### Root Layout (Required)

Every Next.js app MUST have a root layout at `app/layout.js`. It wraps **every page** in the app.

```tsx
// app/layout.js — ROOT LAYOUT (Required)
import './globals.css';

export const metadata = {
  title: 'My App',
  description: 'Built with Next.js',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <nav>
          <a href="/">Home</a>
          <a href="/about">About</a>
          <a href="/contact">Contact</a>
        </nav>

        <main>{children}</main>

        <footer>
          <p>© 2024 My App. All rights reserved.</p>
        </footer>
      </body>
    </html>
  );
}
```

**Key Points:**
- `{children}` is where the current page content gets injected
- The root layout MUST include `<html>` and `<body>` tags
- Navbar and footer appear on ALL pages automatically

### Nested Layouts

You can create layouts for specific sections of your app.

```
app/
├── layout.js              ← Root Layout (Navbar + Footer)
├── page.js                ← Home page
├── dashboard/
│   ├── layout.js          ← Dashboard Layout (Sidebar)
│   ├── page.js            ← /dashboard
│   ├── settings/
│   │   └── page.js        ← /dashboard/settings
│   └── analytics/
│       └── page.js        ← /dashboard/analytics
```

```tsx
// app/dashboard/layout.js — NESTED LAYOUT
export default function DashboardLayout({ children }) {
  return (
    <div style={{ display: 'flex' }}>
      {/* Sidebar — shows on all dashboard pages */}
      <aside style={{ width: '250px', background: '#f0f0f0' }}>
        <h3>Dashboard</h3>
        <nav>
          <a href="/dashboard">Overview</a>
          <a href="/dashboard/settings">Settings</a>
          <a href="/dashboard/analytics">Analytics</a>
        </nav>
      </aside>

      {/* Page content */}
      <div style={{ flex: 1, padding: '20px' }}>
        {children}
      </div>
    </div>
  );
}
```

**Result:** Every `/dashboard/*` page automatically gets the sidebar. The Root Layout's navbar/footer still wraps everything.

```
Visual: /dashboard/settings

┌──────────────────────────────┐
│         Navbar (Root)        │  ← From app/layout.js
├────────┬─────────────────────┤
│Sidebar │                     │
│(Dash   │   Settings Page     │  ← From page.js
│Layout) │   Content           │
│        │                     │
├────────┴─────────────────────┤
│         Footer (Root)        │  ← From app/layout.js
└──────────────────────────────┘
```

---

## ⭐ Most Important Concepts

### 1. Server Components vs Client Components (Deep Dive)

This is the **most important concept** in modern Next.js.

#### Server Components (Default)

```tsx
// app/products/page.js — Server Component (default, no directive)
import { db } from '@/lib/db';

export default async function ProductsPage() {
  const products = await db.product.findMany(); // Direct DB query

  return (
    <ul>
      {products.map(p => <li key={p.id}>{p.name}</li>)}
    </ul>
  );
}
```

**Characteristics:**
- ✅ Can use `async/await`
- ✅ Can access database, file system, server-only APIs
- ✅ Zero JavaScript sent to browser for this component
- ❌ Cannot use `useState`, `useEffect`, `onClick`, or any browser API

#### Client Components

```tsx
// app/components/SearchBar.js — Client Component
"use client"; // ← This directive makes it a Client Component

import { useState } from 'react';

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const res = await fetch(`/api/search?q=${query}`);
    const data = await res.json();
    setResults(data);
  };

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search products..."
      />
      <button onClick={handleSearch}>Search</button>
      <ul>
        {results.map(r => <li key={r.id}>{r.name}</li>)}
      </ul>
    </div>
  );
}
```

**Characteristics:**
- ✅ Can use hooks (`useState`, `useEffect`, `useRef`)
- ✅ Can handle user events (`onClick`, `onChange`, `onSubmit`)
- ✅ Can access browser APIs (`window`, `localStorage`)
- ❌ Cannot use `async/await` at the component level
- ❌ Cannot directly access database or file system

#### When to Use Which?

| Need | Component Type |
|------|---------------|
| Fetch and display data | ✅ Server Component |
| Form input, button clicks | ✅ Client Component |
| Database queries | ✅ Server Component |
| useState, useEffect | ✅ Client Component |
| Large static content (reduce JS bundle) | ✅ Server Component |
| Animation libraries (Framer Motion) | ✅ Client Component |

### 2. Composing Server + Client Components

The **key pattern**: Server Components can import Client Components, but NOT the other way around.

```tsx
// ✅ CORRECT: Server Component using a Client Component
// app/products/page.js (Server)
import AddToCartButton from '@/components/AddToCartButton'; // Client

export default async function ProductPage() {
  const product = await db.product.findUnique({ where: { id: 1 } });

  return (
    <div>
      <h1>{product.name}</h1>           {/* Server renders this */}
      <p>${product.price}</p>           {/* Server renders this */}
      <AddToCartButton id={product.id} /> {/* Client handles interaction */}
    </div>
  );
}
```

```tsx
// components/AddToCartButton.js (Client)
"use client";

import { useState } from 'react';

export default function AddToCartButton({ id }) {
  const [added, setAdded] = useState(false);

  const handleClick = async () => {
    await fetch('/api/cart', {
      method: 'POST',
      body: JSON.stringify({ productId: id }),
    });
    setAdded(true);
  };

  return (
    <button onClick={handleClick}>
      {added ? '✅ Added' : '🛒 Add to Cart'}
    </button>
  );
}
```

**Pattern:** Keep as much as possible in Server Components (data fetching, static content). Only use Client Components for the interactive parts.

### 3. `template.js` vs `layout.js`

| Feature | `layout.js` | `template.js` |
|---------|------------|---------------|
| Re-renders on navigation | ❌ No (persists, keeps state) | ✅ Yes (re-creates) |
| Best for | Navbars, sidebars, persistent UI | Animations, page transitions, logging |

```tsx
// app/template.js — Re-renders on every navigation
export default function Template({ children }) {
  // This console.log runs on EVERY page navigation
  console.log('Page navigation happened!');

  return (
    <div className="fade-in-animation">
      {children}
    </div>
  );
}
```

### 4. Metadata for SEO

Layouts support metadata that is important for SEO:

```tsx
// app/layout.js
export const metadata = {
  title: {
    template: '%s | My Store',    // Template for child pages
    default: 'My Store',          // Fallback title
  },
  description: 'The best online store',
};
```

```tsx
// app/products/page.js
export const metadata = {
  title: 'Products',    // Renders as: "Products | My Store"
};
```

---

## Impact – Real-World Application

### E-Commerce Site Layout Architecture

```
app/
├── layout.js                ← Header + Footer (all pages)
├── page.js                  ← Homepage
├── (shop)/
│   ├── layout.js            ← Category sidebar
│   ├── products/
│   │   └── page.js          ← Product listing
│   └── cart/
│       └── page.js          ← Shopping cart
├── (dashboard)/
│   ├── layout.js            ← Admin sidebar
│   ├── orders/
│   │   └── page.js          ← Order management
│   └── inventory/
│       └── page.js          ← Inventory management
└── (auth)/
    ├── layout.js            ← Minimal layout (no nav)
    ├── login/
    │   └── page.js
    └── register/
        └── page.js
```

- **Shop pages** share a category sidebar via their own layout
- **Dashboard pages** share an admin sidebar
- **Auth pages** have a clean, minimal layout (no navigation clutter)

---

## Interview Questions & Answers

### Q1: What is the purpose of `layout.js` in Next.js?
**Answer:** `layout.js` defines shared UI that wraps child pages. It persists across navigations (doesn't re-render), making it perfect for navbars, sidebars, and footers. The root layout (`app/layout.js`) is required and must include `<html>` and `<body>` tags. Nested layouts add additional shared UI for specific sections.

### Q2: What is the difference between Server and Client Components?
**Answer:** Server Components (default) run on the server, can access databases directly, and send zero JavaScript to the browser. Client Components (marked with `"use client"`) run in the browser, support React hooks and event handlers, and are needed for interactive UI. The best practice is to use Server Components by default and only add `"use client"` where interactivity is required.

### Q3: Can a Client Component import a Server Component?
**Answer:** Not directly. A Client Component cannot `import` a Server Component. However, you can pass a Server Component as `children` (a prop) to a Client Component, and it will work correctly. This is the "composition pattern."

### Q4: What is the difference between `layout.js` and `template.js`?
**Answer:** `layout.js` persists across navigations — it doesn't re-render when the user navigates between child pages (state is preserved). `template.js` creates a new instance on every navigation — it re-renders each time (state is reset). Use `template.js` for enter/exit animations or when you need to run code on every navigation.

### Q5: What does `{children}` represent in a layout?
**Answer:** `{children}` represents the content of the current page being rendered. When a user visits `/dashboard/settings`, the `DashboardLayout`'s `{children}` will be the `SettingsPage` component. The layout wraps around whatever page is active.

### Q6: Why should you keep most components as Server Components?
**Answer:** Server Components reduce the JavaScript bundle sent to the browser, resulting in faster page loads. They execute on the server where they can directly access databases and file systems. Only the interactive parts (forms, buttons, animations) need to be Client Components. This "server-first" approach improves performance, SEO, and user experience.

### Q7 (Scenario): Your e-commerce product page shows product details and has an "Add to Cart" button. How would you structure the components?
**Answer:** The product page would be a Server Component that fetches product details directly from the database. The "Add to Cart" button would be a separate Client Component (with `"use client"`) that handles the click event and manages the cart state. The Server Component imports and renders the Client Component, passing the product ID as a prop.

### Q8 (Scenario): You have a dashboard with a sidebar. Users complain the sidebar resets when they navigate between dashboard pages. What's wrong?
**Answer:** The sidebar might be inside a `template.js` instead of a `layout.js`. Templates re-create on every navigation, causing state loss. Moving the sidebar into a `layout.js` ensures it persists across navigations and maintains state (like which menu item is expanded).

---

### 🔗 Navigation

---

← Previous: [05_API_Routes.md](05_API_Routes.md) | Next: [07_Authentication.md](07_Authentication.md) →
