# 14 – Caching in Next.js

---

## What is Caching?

Caching means **storing data or rendered pages** so they can be served faster on subsequent requests, instead of computing everything from scratch every time.

```
Without Caching:
  User requests /products → Server queries DB → Server renders HTML → Sends response
  Next user requests /products → Server queries DB AGAIN → Renders AGAIN → Sends AGAIN
  (Same work repeated every time)

With Caching:
  First user requests /products → Server queries DB → Renders HTML → CACHES result
  Next user requests /products → Serve cached result instantly (0ms DB work!)
```

---

## Why Does Caching Matter?

| Metric | Without Caching | With Caching |
|--------|----------------|-------------|
| Response time | 500ms–2s | 5–50ms |
| Server load | High (every request = work) | Low (serve from cache) |
| Database queries | On every request | Once per cache cycle |
| Hosting costs | High | Low |
| User experience | Noticeable loading | Instant |

**Real-world Example:**
Amazon's product page is viewed millions of times per day. Querying the database for every single visit would melt their servers. Instead, the page is cached and refreshed periodically.

---

## How Caching Works in Next.js

Next.js has **4 layers of caching**. Understanding them is essential.

### The 4 Caching Mechanisms

```
┌──────────────────────────────────────────────────────────┐
│ Layer 1: Request Memoization (during a single render)    │
│ Layer 2: Data Cache (fetch results on the server)        │
│ Layer 3: Full Route Cache (entire rendered pages)        │
│ Layer 4: Router Cache (client-side navigation cache)     │
└──────────────────────────────────────────────────────────┘
```

---

### Layer 1: Request Memoization

**What?** If you call the same `fetch()` URL multiple times during a single page render, Next.js deduplicates them into ONE actual network request.

**Why?** In a component tree, multiple components might need the same data. Without memoization, the same API would be called 3–4 times.

```tsx
// These components are separate but both need user data

// components/UserHeader.js
async function UserHeader() {
  const user = await fetch('/api/user/1');  // Fetched here
  return <h1>{user.name}</h1>;
}

// components/UserSidebar.js
async function UserSidebar() {
  const user = await fetch('/api/user/1');  // Same URL → NOT fetched again!
  return <p>Email: {user.email}</p>;         // Uses memoized result
}

// Only 1 actual network request happens, even though fetch is called twice
```

**Impact:** You don't need to fetch data at the top and pass it down as props. Each component can fetch what it needs independently — Next.js handles deduplication.

---

### Layer 2: Data Cache

**What?** Fetch responses are stored on the server and reused across requests and users.

**Why?** Avoid calling external APIs or databases repeatedly for the same data.

```tsx
// Cached FOREVER (until revalidation or rebuild)
const res = await fetch('https://api.example.com/products');

// Cached for 60 seconds (ISR behavior)
const res = await fetch('https://api.example.com/products', {
  next: { revalidate: 60 }
});

// NOT cached (SSR behavior — fresh on every request)
const res = await fetch('https://api.example.com/products', {
  cache: 'no-store'
});
```

| Fetch Option | Data Cache Behavior |
|-------------|-------------------|
| Default `fetch(url)` | ✅ Cached indefinitely |
| `{ next: { revalidate: N } }` | ✅ Cached for N seconds |
| `{ cache: 'no-store' }` | ❌ Not cached |

---

### Layer 3: Full Route Cache

**What?** The entire rendered HTML + React Server Component payload is cached for static routes.

**Why?** If a page is fully static (SSG), why re-render it on every request? Serve the pre-built HTML.

```tsx
// This page is fully static → Full Route Cache applies
export default function AboutPage() {
  return <h1>About Us</h1>;
}
// The rendered HTML is cached → served instantly from CDN
```

```tsx
// This page is dynamic → Full Route Cache is SKIPPED
export default async function FeedPage() {
  const res = await fetch('https://api.example.com/feed', {
    cache: 'no-store'   // Forces dynamic rendering
  });
  const posts = await res.json();
  return <div>{posts.map(p => <p key={p.id}>{p.title}</p>)}</div>;
}
// HTML is rendered on every request → no route cache
```

---

### Layer 4: Router Cache (Client-Side)

**What?** When you navigate between pages, Next.js stores the previously visited pages in browser memory. Going "back" serves from this cache instantly.

**Why?** Prevents unnecessary server requests when users navigate back and forth.

```
User visits /products → Page fetched from server → Stored in Router Cache
User clicks /about → /about fetched from server → Stored in Router Cache
User clicks Back → /products served from Router Cache → INSTANT! (no server request)
```

**Duration:**
- Static pages: cached for 5 minutes
- Dynamic pages: cached for 30 seconds
- Prefetched pages via `<Link>`: cached for 5 minutes

---

## ⭐ Most Important Concepts

### 1. Opting Out of Caching

Sometimes you NEED fresh data on every request:

```tsx
// Method 1: Per-fetch opt-out
await fetch(url, { cache: 'no-store' });

// Method 2: Per-page opt-out
export const dynamic = 'force-dynamic';

// Method 3: Per-page zero revalidation
export const revalidate = 0;
```

### 2. On-Demand Revalidation

Instead of waiting for the timer to expire, manually trigger cache refresh:

```tsx
// app/actions/posts.js
"use server";

import { revalidatePath } from 'next/cache';
import { revalidateTag } from 'next/cache';

export async function publishPost(formData) {
  await db.post.create({ data: { title: formData.get('title') } });

  // Clear cache for the blog page
  revalidatePath('/blog');

  // Or clear cache for all fetches with the tag 'posts'
  revalidateTag('posts');
}
```

For tag-based revalidation, tag your fetches:

```tsx
// Fetch with a tag
const res = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] }
});

// Later, calling revalidateTag('posts') refreshes THIS cached data
```

**Real-world Example:** 
A CMS admin publishes a new blog post → calls `revalidateTag('posts')` → the blog listing page instantly reflects the new post without waiting for the timer.

### 3. Revalidation via API (Webhook Pattern)

```tsx
// app/api/revalidate/route.js
import { revalidateTag } from 'next/cache';
import { NextResponse } from 'next/server';

export async function POST(request) {
  const { tag, secret } = await request.json();

  // Verify the webhook secret
  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  revalidateTag(tag);
  return NextResponse.json({ revalidated: true });
}

// Your CMS calls: POST /api/revalidate { tag: "posts", secret: "abc123" }
// → Blog page cache is refreshed
```

### 4. Complete Caching Summary Table

| Cache Layer | What It Caches | Duration | Where | Opt Out |
|-------------|---------------|----------|-------|---------|
| **Request Memoization** | Duplicate fetch calls | Single render only | Server | N/A (auto) |
| **Data Cache** | Fetch responses | Forever / revalidate time | Server | `cache: 'no-store'` |
| **Full Route Cache** | Rendered HTML | Forever (static) | Server / CDN | `dynamic = 'force-dynamic'` |
| **Router Cache** | Visited pages | 30s (dynamic) / 5min (static) | Browser | `router.refresh()` |

---

## Impact — Caching Strategy for a Real E-Commerce App

| Page / Data | Caching Strategy | Why |
|-------------|-----------------|-----|
| About page | Full Route Cache (SSG) | Never changes |
| Product listing | Data Cache with `revalidate: 60` | Prices update periodically |
| Product detail | Data Cache with tag `product-{id}` | On-demand revalidation when admin updates |
| User cart | `cache: 'no-store'` | Always user-specific, real-time |
| Blog posts | SSG + `revalidateTag('posts')` | Cache until new post is published |
| Search results | `cache: 'no-store'` | Different for every query |
| Static assets (images, CSS) | CDN + browser cache | Immutable after build |

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Not understanding default caching | Data appears stale | Know that `fetch()` is cached by default |
| Using `cache: 'no-store'` everywhere | Defeats the purpose, slow | Only use for truly dynamic data |
| Setting revalidation too low | Too many regenerations, high server cost | Balance freshness vs cost (e.g., 60s for products) |
| Forgetting `revalidatePath` after mutations | UI shows old data after form submit | Always revalidate after create/update/delete |
| Not using tags for granular cache control | Revalidating too broadly | Tag related fetches, revalidate specific tags |

---

## Interview Questions & Answers

### Q1: How many caching layers does Next.js have and what are they?
**Answer:** Four layers: (1) Request Memoization — deduplicates same fetch calls in a single render, (2) Data Cache — stores fetch responses on the server, (3) Full Route Cache — caches entire rendered HTML for static pages, (4) Router Cache — stores visited pages in browser memory for instant back-navigation.

### Q2: How is fetch cached by default in the App Router?

### Q3: What is the difference between `revalidatePath` and `revalidateTag`?
**Answer:** `revalidatePath('/blog')` purges the cache for a specific URL path. `revalidateTag('posts')` purges the cache for all fetch calls tagged with `'posts'`. Tags are more granular and flexible — a single tag can revalidate multiple fetches across multiple pages.

### Q4: What is Request Memoization?
**Answer:** During a single page render, if multiple components call `fetch()` with the same URL, Next.js only makes ONE actual network request and shares the result. This means components can independently fetch the data they need without worrying about duplicate calls.

### Q5: How does the Router Cache work?
**Answer:** When you visit pages via client-side navigation (`<Link>`), Next.js stores the page in browser memory. Navigating back to a visited page serves from this cache instantly (no server request). Static pages are cached for 5 minutes, dynamic pages for 30 seconds.

### Q6 (Scenario): Your blog uses ISR with `revalidate: 3600` (1 hour). An urgent correction needs to go live immediately. How?
**Answer:** Use on-demand revalidation. Call `revalidateTag('posts')` or `revalidatePath('/blog/article-slug')` from a Server Action or API webhook. This purges the cache immediately, and the next visitor gets the corrected content.

### Q7 (Scenario): A developer adds `cache: 'no-store'` to every fetch call "just to be safe." What's wrong with this approach?
**Answer:** This disables all server-side caching, turning every page into SSR. Every request triggers a full server render and database query, dramatically increasing server load, response times, and hosting costs. Caching should be disabled only for data that truly needs to be fresh on every request (like user-specific data).

---

### 🔗 Navigation

---

← Previous: [13_Server_Actions.md](13_Server_Actions.md) | Next: [99_Revision_CheatSheet.md](99_Revision_CheatSheet.md) →
