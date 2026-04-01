# 04 – Data Fetching in Next.js

---

## What is Data Fetching?

Data fetching is the process of **getting data from a source** (database, API, file system) and displaying it on your page.

Every web application needs data:
- An e-commerce site fetches **product data**
- A blog fetches **article content**
- A dashboard fetches **user statistics**

Next.js gives you multiple ways to fetch data depending on **where** and **when** you need it.

---

## Why is Data Fetching Important?

| Bad Approach | Problem |
|-------------|---------|
| Fetch everything on the client | Slow load, bad SEO, loading spinners |
| Fetch everything on every request (SSR) | Expensive server costs |
| Cache forever without revalidation | Users see stale data |

Next.js solves this by letting you choose the **right strategy for each piece of data**.

---

## How Data Fetching Works in Next.js

### App Router (Modern — Recommended)

In the App Router, Server Components can **directly use `async/await`** to fetch data. No special functions needed.

#### 1. Basic Server-Side Fetch (Default = Cached / SSG)

```jsx
// app/products/page.js — Server Component
export default async function ProductsPage() {
  // This fetch is CACHED by default (SSG behavior)
  const res = await fetch('https://api.example.com/products');
  const products = await res.json();

  return (
    <ul>
      {products.map(product => (
        <li key={product.id}>
          {product.name} — ${product.price}
        </li>
      ))}
    </ul>
  );
}
```

**What happens:** Next.js fetches this data at **build time** and caches it. Every user gets the same pre-built page. Super fast.

#### 2. Server-Side Fetch — Fresh on Every Request (SSR)

```jsx
// app/feed/page.js
export default async function FeedPage() {
  // 'no-store' = fetch fresh data on every request
  const res = await fetch('https://api.example.com/feed', {
    cache: 'no-store'
  });
  const posts = await res.json();

  return (
    <div>
      {posts.map(post => <p key={post.id}>{post.title}</p>)}
    </div>
  );
}
```

**What happens:** Data is fetched **every time a user visits** the page. Always fresh, but the server does work on every request.

#### 3. Server-Side Fetch — Revalidate Periodically (ISR)

```jsx
// app/news/page.js
export default async function NewsPage() {
  // Revalidate every 5 minutes (300 seconds)
  const res = await fetch('https://api.example.com/news', {
    next: { revalidate: 300 }
  });
  const articles = await res.json();

  return (
    <div>
      {articles.map(a => <h2 key={a.id}>{a.title}</h2>)}
    </div>
  );
}
```

**What happens:** Page is cached for 300 seconds. After that, the next visitor triggers a background regeneration. Best of both worlds.

#### 4. Client-Side Fetch (CSR)

```jsx
// app/dashboard/page.js
"use client";

import { useState, useEffect } from 'react';

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/stats')
      .then(res => res.json())
      .then(data => {
        setStats(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading dashboard...</p>;

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Total Users: {stats.totalUsers}</p>
      <p>Revenue: ${stats.revenue}</p>
    </div>
  );
}
```

**What happens:** The page loads first (empty), then JavaScript fetches data and renders it. Good for private/authenticated pages.

---

## ⭐ Most Important Concepts

### 1. Fetch Caching Behavior (App Router)

This is **critical** to understand:

| Fetch Option | Behavior | Rendering |
|-------------|----------|-----------|
| `fetch(url)` (default) | Cached indefinitely | SSG |
| `fetch(url, { cache: 'no-store' })` | Never cached | SSR |
| `fetch(url, { next: { revalidate: 60 } })` | Cached for 60s | ISR |

```jsx
// These three lines produce completely different behaviors:
await fetch(url);                              // SSG — cached forever
await fetch(url, { cache: 'no-store' });       // SSR — fresh every time
await fetch(url, { next: { revalidate: 60 }}); // ISR — cached for 60s
```

### 2. Fetching Data from a Database Directly

In Server Components, you can **skip the API entirely** and query the database directly:

```jsx
// app/users/page.js — Server Component
import { db } from '@/lib/database';

export default async function UsersPage() {
  // Direct database query — no API needed!
  const users = await db.user.findMany();

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name} - {user.email}</li>
      ))}
    </ul>
  );
}
```

**Why this is powerful:** In traditional React, you'd need:
1. Build a backend API endpoint
2. Fetch from the frontend
3. Handle loading/error states

With Server Components, step 1 and 2 are **eliminated**. The component IS the server.

### 3. Parallel vs Sequential Data Fetching

#### ❌ Sequential (Slow) — One after another

```jsx
export default async function Page() {
  const user = await fetchUser();        // Takes 1 second
  const posts = await fetchPosts();      // Takes 1 second
  const comments = await fetchComments();// Takes 1 second
  // Total: 3 seconds 😩
}
```

#### ✅ Parallel (Fast) — All at the same time

```jsx
export default async function Page() {
  // Start ALL fetches simultaneously
  const [user, posts, comments] = await Promise.all([
    fetchUser(),        // Takes 1 second
    fetchPosts(),       // Takes 1 second
    fetchComments(),    // Takes 1 second
  ]);
  // Total: 1 second 🚀
}
```

**Real-world Example:** A product page needs product details, reviews, and related products. Fetching them in parallel saves 2–3 seconds of load time.

### 4. Route Segment Config (Page-Level Defaults)

Instead of setting cache options on every `fetch()`, you can set defaults for the entire page:

```jsx
// app/dashboard/page.js

// Force this entire page to be dynamic (SSR)
export const dynamic = 'force-dynamic';

// Or force it to be static (SSG)
export const dynamic = 'force-static';

// Set revalidation for the whole page 
export const revalidate = 60; // ISR: 60 seconds
```

### 5. Using SWR or React Query for Client-Side Fetching

For client-side fetching with caching, retries, and real-time updates:

```jsx
"use client";

import useSWR from 'swr';

const fetcher = (url) => fetch(url).then(res => res.json());

export default function Notifications() {
  const { data, error, isLoading } = useSWR('/api/notifications', fetcher, {
    refreshInterval: 5000, // Auto-refresh every 5 seconds
  });

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error loading notifications</p>;

  return (
    <ul>
      {data.map(n => <li key={n.id}>{n.message}</li>)}
    </ul>
  );
}
```

**Real-world Example:** A notification bell icon that auto-updates every 5 seconds without page refresh.

---

## Impact – Real Application Architecture

| Page | Data Source | Strategy | Why |
|------|-----------|----------|-----|
| Product Listing | Database | ISR (30s) | Changes periodically, needs SEO |
| User Profile | Database | SSR | Personalized, needs SEO |
| Admin Dashboard | API | CSR + SWR | Private, real-time data |
| Blog Post | CMS (Headless) | SSG | Content changes only on publish |
| Search Results | Search API | SSR | Different for every query |
| Notification Bell | API | CSR + polling | Real-time, small component |

---

## Pages Router (Legacy) — For Reference

```jsx
// SSG — getStaticProps (runs at build time)
export async function getStaticProps() {
  const res = await fetch('https://api.example.com/posts');
  const posts = await res.json();
  return { props: { posts }, revalidate: 60 };
}

// SSR — getServerSideProps (runs on every request)
export async function getServerSideProps(context) {
  const { id } = context.params;
  const res = await fetch(`https://api.example.com/posts/${id}`);
  const post = await res.json();
  return { props: { post } };
}

// Static Paths — getStaticPaths (for dynamic SSG routes)
export async function getStaticPaths() {
  const res = await fetch('https://api.example.com/posts');
  const posts = await res.json();
  const paths = posts.map(post => ({ params: { id: post.id.toString() } }));
  return { paths, fallback: 'blocking' };
}
```

---

## Interview Questions & Answers

### Q1: How does data fetching work in the App Router?
**Answer:** In the App Router, Server Components can directly use `async/await` with the native `fetch()` API. By default, fetch responses are cached (SSG). You can opt into SSR with `cache: 'no-store'` or ISR with `next: { revalidate: seconds }`. No special functions like `getServerSideProps` are needed.

### Q2: What is the difference between `cache: 'no-store'` and `next: { revalidate: 60 }`?
**Answer:** `cache: 'no-store'` means fetch fresh data on **every request** (SSR behavior). `next: { revalidate: 60 }` means cache the response for 60 seconds; after that, the next request triggers a background regeneration (ISR behavior). ISR is more efficient because most users hit the cache.

### Q3: Can you fetch data directly from a database in Next.js without writing an API?
**Answer:** Yes, in Server Components (App Router), you can import your database client and query directly. The code runs only on the server and is never sent to the client's browser. This eliminates the need for intermediary API endpoints for read operations.

### Q4: What is the difference between `getStaticProps` and `getServerSideProps`?
**Answer:** `getStaticProps` runs at **build time** (SSG) and generates static pages. `getServerSideProps` runs on **every request** (SSR) and generates dynamic pages. Both are Pages Router patterns. In the App Router, you control this via `fetch()` cache options instead.

### Q5: How do you fetch data in parallel in Next.js?
**Answer:** Use `Promise.all()` to fire multiple fetch calls simultaneously instead of awaiting them sequentially. This drastically reduces load time since all requests run concurrently.

### Q6: What is SWR and when would you use it?
**Answer:** SWR (stale-while-revalidate) is a React hook library by Vercel for client-side data fetching. It provides automatic caching, revalidation, error retry, and real-time data. Use it in Client Components for interactive data like notifications, live dashboards, or any data that needs periodic auto-refresh.

### Q7 (Scenario): Your e-commerce product page takes 4 seconds to load. You're making 4 sequential API calls. How would you fix this?
**Answer:** Replace sequential fetches with `Promise.all()` to run all 4 API calls in parallel. If each takes ~1 second, the total drops from 4 seconds to ~1 second. Additionally, consider ISR caching so most users don't wait for API calls at all.

### Q8 (Scenario): You're fetching user-specific data in a Server Component, but all users see the same data. What's wrong?
**Answer:** The fetch is likely cached by default (SSG behavior). Adding `cache: 'no-store'` to the fetch options, or setting `export const dynamic = 'force-dynamic'` at the page level, forces the data to be fetched fresh on every request per user.

---

### 🔗 Navigation
- ⬅️ Previous: [03_Rendering_Methods.md](./03_Rendering_Methods.md)
- ➡️ Next: [05_API_Routes.md](./05_API_Routes.md)
