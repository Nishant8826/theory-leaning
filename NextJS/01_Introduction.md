# 01 – Introduction to Next.js

---

## What is Next.js?

Next.js is a **React framework** built by Vercel that gives you everything you need to build fast, production-ready web applications.

Think of it this way:
- **React** is a library — it gives you tools to build UI components.
- **Next.js** is a framework — it gives you the **full structure** (routing, rendering, optimization, API handling) on top of React.

In simple words: **React builds the bricks. Next.js builds the entire house.**

---

## Why Next.js?

### Problems with plain React (Create React App):

| Problem | Impact |
|---------|--------|
| No built-in routing | You need `react-router-dom` manually |
| Only Client-Side Rendering (CSR) | Slow initial load, bad for SEO |
| No built-in API support | You need a separate backend server |
| No image optimization | Large images slow down your site |
| No built-in code splitting | Entire app loads even if user visits one page |

### How Next.js solves these:

| Feature | How Next.js Helps |
|---------|-------------------|
| File-based Routing | Just create a file → it becomes a URL |
| SSR / SSG / ISR | Multiple rendering strategies for speed & SEO |
| API Routes | Build backend APIs inside the same project |
| Image Optimization | `<Image>` component auto-optimizes images |
| Automatic Code Splitting | Only loads the code needed for the current page |

---

## How Does Next.js Work?

### The Flow (Simplified):

```
Developer writes pages/components
        ↓
Next.js decides HOW to render each page
(SSR? SSG? CSR? ISR?)
        ↓
On build or on request → HTML is generated
        ↓
Browser receives ready-to-display HTML + JavaScript
        ↓
React "hydrates" the page (makes it interactive)
```

### Key Concept: Hydration

When the server sends pre-rendered HTML to the browser, React then "attaches" event listeners and makes the page interactive. This process is called **hydration**.

```
Server HTML (static, no clicks work)
        ↓
React Hydration
        ↓
Fully Interactive Page (buttons work, forms submit)
```

---

## Impact – Why It Matters

### Real-World Examples:

**1. E-Commerce (Amazon-like site)**
- Product pages need to load **instantly** and be **indexable by Google**.
- Next.js uses SSG/ISR to pre-render product pages → fast load + great SEO.

**2. Social Media (Instagram-like feed)**
- User feed is dynamic and personalized → SSR renders it on every request.
- Profile pages are mostly static → SSG for speed.

**3. Blog / Documentation**
- Content rarely changes → SSG generates all pages at build time.
- Result: Lightning-fast page loads.

**4. Dashboard Apps**
- Data is private and real-time → CSR is fine (no SEO needed).
- Next.js still helps with routing, API routes, and code splitting.

---

## Setting Up a Next.js Project

### Prerequisites:
- Node.js (v18 or higher)
- npm or yarn

### Create a New Project:

```bash
npx create-next-app@latest my-app
```

### During Setup, You'll Be Asked:

```
✔ Would you like to use TypeScript? → Yes/No
✔ Would you like to use ESLint? → Yes
✔ Would you like to use Tailwind CSS? → Yes/No
✔ Would you like to use `src/` directory? → Yes (recommended)
✔ Would you like to use App Router? → Yes (recommended)
✔ Would you like to customize the import alias? → No
```

### Folder Structure (App Router):

```
my-app/
├── src/
│   ├── app/
│   │   ├── layout.js       ← Root layout (wraps every page)
│   │   ├── page.js         ← Home page (/)
│   │   ├── globals.css     ← Global styles
│   │   └── about/
│   │       └── page.js     ← About page (/about)
│   └── components/         ← Reusable components
├── public/                 ← Static assets (images, icons)
├── package.json
├── next.config.js          ← Next.js configuration
└── .env.local              ← Environment variables
```

### Start the Dev Server:

```bash
cd my-app
npm run dev
```

Your app is now running at `http://localhost:3000` 🎉

---

## ⭐ Most Important Concepts

### 1. Pages Router vs App Router

Next.js has two routing systems:

| Feature | Pages Router (Legacy) | App Router (Modern) |
|---------|----------------------|---------------------|
| Folder | `pages/` | `app/` |
| Released | Next.js 1–12 | Next.js 13+ |
| Layouts | Manual `_app.js` | Nested `layout.js` |
| Data Fetching | `getServerSideProps`, `getStaticProps` | `async` components, `fetch()` |
| Server Components | ❌ Not supported | ✅ Default |
| Status | Still supported | ✅ Recommended |

> **Takeaway:** Always use the **App Router** for new projects.

### 2. Server Components vs Client Components

```
Server Component (default):
  - Runs on the server
  - Cannot use useState, useEffect, onClick
  - Great for fetching data and displaying content

Client Component (opt-in with "use client"):
  - Runs in the browser
  - CAN use hooks and event handlers
  - Needed for interactive UI
```

```jsx
// ✅ Server Component (default) — no directive needed
export default async function ProductPage() {
  const res = await fetch('https://api.example.com/products');
  const data = await res.json();

  return (
    <div>
      {data.map(p => <p key={p.id}>{p.name}</p>)}
    </div>
  );
}
```

```jsx
// ✅ Client Component — needs "use client" at the top
"use client";

import { useState } from 'react';

export default function LikeButton() {
  const [liked, setLiked] = useState(false);

  return (
    <button onClick={() => setLiked(!liked)}>
      {liked ? '❤️' : '🤍'}
    </button>
  );
}
```

---

## Interview Questions & Answers

### Q1: What is Next.js and how is it different from React?
**Answer:** Next.js is a React-based framework that provides built-in features like file-based routing, server-side rendering, static site generation, and API routes. React alone is a UI library focused on building components — it doesn't include routing, rendering strategies, or backend support out of the box.

### Q2: What are the main benefits of using Next.js?
**Answer:**
- Automatic file-based routing
- Multiple rendering methods (SSR, SSG, ISR, CSR)
- Built-in API routes (full-stack capability)
- Automatic code splitting & optimization
- Image and font optimization
- Great SEO capabilities

### Q3: What is hydration in Next.js?
**Answer:** Hydration is the process where React takes server-rendered HTML and attaches JavaScript event listeners to make the page interactive. The server sends a static HTML snapshot, and React "hydrates" it in the browser to enable clicks, form submissions, and other interactions.

### Q4: What is the difference between Pages Router and App Router?
**Answer:** The Pages Router (`pages/` directory) was the original system (Next.js 1–12) that uses special functions like `getServerSideProps` for data fetching. The App Router (`app/` directory, Next.js 13+) is the modern system that supports React Server Components by default, nested layouts, and uses native `async/await` for data fetching. The App Router is recommended for all new projects.

### Q5: When would you NOT use Next.js?
**Answer:**
- Simple single-page apps with no SEO requirements
- Purely client-side dashboards with no public-facing pages
- Projects where a completely different backend architecture is needed
- Tiny prototypes where plain React is enough

### Q6: What is the difference between a Server Component and a Client Component?
**Answer:** Server Components run on the server, have zero JS bundle cost for the client, and can directly access databases or file systems. Client Components run in the browser, support React hooks (`useState`, `useEffect`), and handle user interactions. By default, all components in the App Router are Server Components unless marked with `"use client"`.

### Q7 (Scenario): Your blog pages aren't appearing on Google. You're using Create React App. What would you suggest?
**Answer:** CRA uses Client-Side Rendering, meaning Google's crawler sees an empty HTML shell. I'd recommend migrating to Next.js using Static Site Generation (SSG) for blog posts. SSG pre-renders full HTML at build time, making it easily crawlable by search engines.

### Q8 (Scenario): You're building a private employee dashboard. Should you use SSR or CSR?
**Answer:** CSR is the better choice. The dashboard is private (no SEO needed), data is user-specific, and CSR provides a smooth SPA-like experience. Next.js still adds value with routing, code splitting, and API routes even in a CSR-heavy app.

---

### 🔗 Navigation

---

← Previous: []() | Next: [02_Routing.md](02_Routing.md) →
