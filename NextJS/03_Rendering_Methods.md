# 03 – Rendering Methods in Next.js

---

## What is Rendering?

Rendering is the process of converting your React code into the actual HTML that users see in the browser.

The **most critical question in Next.js** is: **WHERE and WHEN does this rendering happen?**

- **Where?** → On the Server or in the Browser (Client)
- **When?** → At Build time, on every Request, or after a delay

Next.js gives you **4 rendering strategies**, and choosing the right one for each page is what makes your app fast, SEO-friendly, and cost-effective.

---

## Why Do Rendering Methods Matter?

| Concern | Wrong Choice | Right Choice |
|---------|-------------|-------------|
| **SEO** | CSR → Google sees empty page | SSR/SSG → Google sees full content |
| **Speed** | SSR everything → Server is slow | SSG → Pages are pre-built, instant |
| **Freshness** | SSG → Content might be stale | ISR/SSR → Content stays updated |
| **Cost** | SSR → Server runs on every request (expensive) | SSG → No server needed (cheap) |

---

## The 4 Rendering Methods

### 1. CSR – Client-Side Rendering

**What?** The browser downloads an empty HTML shell, then JavaScript builds the page in the browser.

**How it works:**
```
Browser requests page
        ↓
Server sends empty HTML + JavaScript bundle
        ↓
Browser downloads JavaScript
        ↓
JavaScript runs and builds the page
        ↓
User finally sees the content (SLOW!)
```

```jsx
"use client";

import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/api/stats')
      .then(res => res.json())
      .then(setData);
  }, []);

  if (!data) return <p>Loading...</p>;

  return <div>Total Users: {data.users}</div>;
}
```

| Pros | Cons |
|------|------|
| Interactive & dynamic | Bad for SEO (empty HTML) |
| Less server load | Slow initial load |
| Great for private/authenticated pages | User sees loading spinner first |

**When to use:** Private dashboards, admin panels, user settings — pages that don't need SEO.

**Real-world Example:** An admin analytics dashboard showing real-time charts and data.

---

### 2. SSR – Server-Side Rendering

**What?** The server builds the full HTML page on **every request** and sends it to the browser.

**How it works:**
```
Browser requests page
        ↓
Server fetches data from database/API
        ↓
Server renders complete HTML
        ↓
Sends full HTML to browser (FAST first paint!)
        ↓
React hydrates the page (makes it interactive)
```

```jsx
// App Router — SSR by default with dynamic data
// app/feed/page.js
export default async function FeedPage() {
  // This runs on the server on EVERY request
  const res = await fetch('https://api.example.com/feed', {
    cache: 'no-store'    // ← This forces SSR (no caching)
  });
  const posts = await res.json();

  return (
    <div>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </article>
      ))}
    </div>
  );
}
```

```jsx
// Pages Router (Legacy) — SSR with getServerSideProps
export async function getServerSideProps() {
  const res = await fetch('https://api.example.com/feed');
  const posts = await res.json();
  return { props: { posts } };
}

export default function FeedPage({ posts }) {
  return (
    <div>
      {posts.map(post => <p key={post.id}>{post.title}</p>)}
    </div>
  );
}
```

| Pros | Cons |
|------|------|
| Great SEO (full HTML) | Slower than SSG (server works on every request) |
| Always fresh data | Higher server costs |
| Personalized content possible | Can be slow if API/DB is slow |

**When to use:** Social media feeds, search results, pages with frequently changing + personalized data.

**Real-world Example:** Instagram's feed — it's different for every user and constantly updating.

---

### 3. SSG – Static Site Generation

**What?** Pages are built into static HTML files **at build time** (when you run `npm run build`). The same pre-built HTML is served to every user.

**How it works:**
```
Developer runs `npm run build`
        ↓
Next.js fetches data and generates HTML for each page
        ↓
HTML files are stored on a CDN
        ↓
User requests page → CDN instantly serves pre-built HTML
        ↓
React hydrates the page
```

```jsx
// App Router — SSG is DEFAULT behavior
// app/about/page.js
export default function AboutPage() {
  return (
    <div>
      <h1>About Us</h1>
      <p>We are a tech company founded in 2020.</p>
    </div>
  );
}
// This page is automatically statically generated at build time!
```

```jsx
// SSG with data fetching (fetch is cached by default)
// app/blog/page.js
export default async function BlogPage() {
  // Cached by default → SSG behavior
  const res = await fetch('https://api.example.com/posts');
  const posts = await res.json();

  return (
    <div>
      {posts.map(post => <h2 key={post.id}>{post.title}</h2>)}
    </div>
  );
}
```

```jsx
// SSG with dynamic routes — generateStaticParams
// app/blog/[slug]/page.js
export async function generateStaticParams() {
  const res = await fetch('https://api.example.com/posts');
  const posts = await res.json();

  // Tell Next.js which pages to pre-build
  return posts.map(post => ({
    slug: post.slug,
  }));
}

export default async function BlogPost({ params }) {
  const res = await fetch(`https://api.example.com/posts/${params.slug}`);
  const post = await res.json();

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
```

| Pros | Cons |
|------|------|
| Fastest possible load time | Content can become stale |
| Excellent SEO | Needs rebuild for content updates |
| Cheapest to host (just static files) | Not suitable for personalized content |
| Can be served from CDN globally | Build time increases with more pages |

**When to use:** Blogs, documentation, marketing pages, landing pages — content that doesn't change frequently.

**Real-world Example:** A company's "About Us" or "Pricing" page that rarely changes.

---

### 4. ISR – Incremental Static Regeneration

**What?** A hybrid of SSG and SSR. Pages are statically generated at build time **but can be automatically updated** after a specified time interval — without rebuilding the entire site.

**How it works:**
```
Build time → Pages are statically generated (like SSG)
        ↓
User visits page → Gets the cached static page (fast!)
        ↓
After the revalidation time expires (e.g., 60 seconds)
        ↓
Next request triggers regeneration in the BACKGROUND
        ↓
New HTML replaces the old cached version
        ↓
Next user gets the updated page
```

```jsx
// App Router — ISR with revalidate
// app/products/page.js
export default async function ProductsPage() {
  const res = await fetch('https://api.example.com/products', {
    next: { revalidate: 60 }    // ← Revalidate every 60 seconds
  });
  const products = await res.json();

  return (
    <div>
      {products.map(p => (
        <div key={p.id}>
          <h2>{p.name}</h2>
          <p>${p.price}</p>
        </div>
      ))}
    </div>
  );
}
```

```jsx
// Pages Router (Legacy) — ISR with revalidate
export async function getStaticProps() {
  const res = await fetch('https://api.example.com/products');
  const products = await res.json();

  return {
    props: { products },
    revalidate: 60,    // ← Regenerate every 60 seconds
  };
}
```

| Pros | Cons |
|------|------|
| Fast like SSG | Content might be up to `revalidate` seconds stale |
| Auto-updates without rebuild | Slightly more complex than pure SSG |
| Great for pages with periodic updates | First request after expiry still gets old page |
| Scales well | Need to choose good revalidate intervals |

**When to use:** E-commerce product pages, news articles, pricing pages — content that updates but not in real-time.

**Real-world Example:** Amazon product listings — prices and stock change every few minutes, but showing data that's 60 seconds old is acceptable.

---

## ⭐ The Ultimate Comparison Table

| Feature | CSR | SSR | SSG | ISR |
|---------|-----|-----|-----|-----|
| **Where rendered** | Browser | Server | Server (at build) | Server (at build + background) |
| **When rendered** | On every visit | On every request | Once at build time | At build + periodic updates |
| **Speed** | Slow first load | Medium | Fastest | Fast (cached) |
| **SEO** | ❌ Bad | ✅ Great | ✅ Great | ✅ Great |
| **Data freshness** | Always fresh | Always fresh | Can be stale | Mostly fresh |
| **Server cost** | Low | High | Lowest | Low |
| **Personalized?** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Best for** | Dashboards | Feeds, search | Blogs, docs | E-commerce, news |

---

## ⭐ Decision Flowchart

```
Does the page need SEO?
├── NO → Use CSR (dashboards, admin panels)
└── YES ↓
      Does the content change per user?
      ├── YES → Use SSR (feeds, search results)
      └── NO ↓
            Does the content change frequently?
            ├── NO → Use SSG (blogs, docs, marketing)
            └── YES → Use ISR (products, news, pricing)
```

---

## Impact – Real Application Architecture

Here's how a real e-commerce site like Amazon might use ALL four rendering methods:

| Page | Rendering | Why |
|------|-----------|-----|
| Homepage | ISR (60s) | Content updates periodically, needs SEO |
| Product Page | ISR (30s) | Price/stock changes, needs SEO |
| Search Results | SSR | Different for every search query |
| User Dashboard | CSR | Private, no SEO needed |
| About Us | SSG | Rarely changes |
| Blog | SSG | Content updates only on publish |
| Cart | CSR | Fully dynamic, user-specific |

---

## Interview Questions & Answers

### Q1: What are the different rendering methods in Next.js?
**Answer:** Next.js supports 4 rendering methods:
1. **CSR** — Page built in browser using JavaScript
2. **SSR** — Page built on server on every request
3. **SSG** — Page built at build time as static HTML
4. **ISR** — Page built at build time but auto-updated at intervals

### Q2: What is the difference between SSR and SSG?
**Answer:** SSR generates HTML on the server for **every request** (always fresh data but slower). SSG generates HTML **once at build time** and serves the same static file to all users (fastest but content can go stale). Use SSR for personalized/frequently changing content, SSG for static content.

### Q3: When would you choose ISR over SSG?
**Answer:** When content changes periodically but not on every request. ISR gives you the speed of SSG with the ability to auto-update. For example, an e-commerce product page where the price changes every few minutes — ISR with `revalidate: 60` gives fast performance without needing a full rebuild.

### Q4: Why is CSR bad for SEO?
**Answer:** With CSR, the server sends an empty HTML shell (`<div id="root"></div>`). Search engine crawlers receive this empty page and have nothing to index. SSR/SSG send fully rendered HTML that crawlers can read and index immediately.

### Q5: What does `cache: 'no-store'` do in the App Router?
**Answer:** It tells Next.js to NOT cache the fetch response, effectively turning the page into SSR. The data is fetched fresh on every request. Without this, `fetch()` responses are cached by default (SSG behavior).

### Q6: What does `next: { revalidate: 60 }` do?
**Answer:** It tells Next.js to cache the page/data for 60 seconds. After 60 seconds, the next incoming request triggers a background regeneration. The stale page is served while the new version generates, and the cache is updated for subsequent requests. This is ISR.

### Q7: What is hydration and why can it cause issues?
**Answer:** Hydration is when React attaches event listeners to server-rendered HTML. Issues ("hydration mismatch") occur when the server-rendered HTML doesn't match what the client tries to render — for example, using `Date.now()` or `window.innerWidth` during rendering, which produces different results on server vs client.

### Q8 (Scenario): You're building a news site. Articles update every 5 minutes. Which rendering method would you use?
**Answer:** ISR with `revalidate: 300` (5 minutes). Articles are pre-rendered at build time for speed and SEO, and automatically update every 5 minutes. This balances speed, SEO, and data freshness without the cost of SSR.

### Q9 (Scenario): A user reports that the product price on your site is wrong. But your database is correct. What could be the issue?
**Answer:** This is likely an ISR caching issue. If you're using ISR with `revalidate: 3600` (1 hour), the cached page might be showing an old price. Reducing the revalidation interval or using On-Demand Revalidation (manually triggering regeneration via `revalidateTag()` or `revalidatePath()`) would fix this.

### Q10: Can you mix rendering methods in a single Next.js app?
**Answer:** Yes, absolutely. Each page/route can use a different rendering method. For example, your blog uses SSG, your search page uses SSR, and your dashboard uses CSR — all in the same Next.js application. This is one of Next.js's greatest strengths.

---

### 🔗 Navigation

---

← Previous: [02_Routing.md](02_Routing.md) | Next: [04_Data_Fetching.md](04_Data_Fetching.md) →
