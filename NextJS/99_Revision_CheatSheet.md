# 99 – Next.js Revision Cheat Sheet 🚀

> Quick reference for all major concepts. Use this for last-minute revision before interviews or starting a project.

---

## 1. What is Next.js?

- React framework by Vercel
- File-based routing, SSR/SSG/ISR/CSR, API routes, image optimization
- **App Router** (modern, `app/` folder) vs **Pages Router** (legacy, `pages/` folder)
- All components are **Server Components** by default (use `"use client"` for interactivity)

---

## 2. Routing Quick Reference

| Pattern | Example | URL |
|---------|---------|-----|
| Static | `app/about/page.js` | `/about` |
| Dynamic | `app/products/[id]/page.js` | `/products/123` |
| Catch-all | `app/docs/[...slug]/page.js` | `/docs/a/b/c` |
| Route Group | `app/(marketing)/about/page.js` | `/about` |
| Parallel | `app/@sidebar/page.js` | Named slot in layout |
| API Route | `app/api/users/route.js` | `/api/users` |

**Special Files:**
| File | Purpose |
|------|---------|
| `page.js` | Page UI |
| `layout.js` | Persistent shared wrapper |
| `loading.js` | Loading state (Suspense) |
| `error.js` | Error boundary |
| `not-found.js` | 404 page |
| `template.js` | Like layout but re-renders on nav |
| `route.js` | API endpoint |

---

## 3. Rendering Methods

| Method | When | Where | SEO | Speed | Use For |
|--------|------|-------|-----|-------|---------|
| **SSG** | Build time | Server | ✅ | Fastest | Blogs, docs, marketing |
| **SSR** | Every request | Server | ✅ | Medium | Feeds, search, personalized |
| **ISR** | Build + revalidate | Server | ✅ | Fast | Products, news, pricing |
| **CSR** | In browser | Client | ❌ | Slow initial | Dashboards, admin panels |

**Quick Fetch Rules:**
```jsx
fetch(url)                              // → SSG (cached forever)
fetch(url, { cache: 'no-store' })       // → SSR (fresh every request)
fetch(url, { next: { revalidate: 60 }}) // → ISR (cached 60s)
```

---

## 4. Data Fetching

- **Server Component:** `async/await` with `fetch()` directly
- **Client Component:** `useEffect` + `fetch()` or SWR/React Query
- **Database direct:** Server Components can call `prisma.user.findMany()` directly
- **Parallel fetching:** `Promise.all([fetchA(), fetchB()])` for speed
- **Page config:** `export const dynamic = 'force-dynamic'` for full SSR

---

## 5. API Routes

```jsx
// app/api/users/route.js
import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({ users: [] });
}

export async function POST(request) {
  const body = await request.json();
  return NextResponse.json({ created: true }, { status: 201 });
}
```

---

## 6. Server vs Client Components

| Feature | Server | Client |
|---------|--------|--------|
| Directive | None (default) | `"use client"` |
| Hooks | ❌ No | ✅ Yes |
| Events (onClick) | ❌ No | ✅ Yes |
| DB access | ✅ Yes | ❌ No |
| async/await | ✅ Yes | ❌ No (at component level) |
| JS bundle | ✅ Zero | ❌ Adds to bundle |

**Pattern:** Server Component fetches data → imports Client Component for interactivity.

---

## 7. Authentication (NextAuth.js)

- **Setup:** `app/api/auth/[...nextauth]/route.js`
- **Wrap app:** `<SessionProvider>` in a Client `providers.js`
- **Server check:** `const session = await getServerSession()`
- **Client check:** `const { data: session } = useSession()`
- **Middleware protection:** `export { default } from 'next-auth/middleware'`
- **JWT vs DB sessions:** JWT = stateless (faster), DB = revocable

---

## 8. Performance

| Technique | Implementation |
|-----------|---------------|
| Image optimization | `import Image from 'next/image'` |
| Font optimization | `import { Inter } from 'next/font/google'` |
| Code splitting | Automatic per page |
| Dynamic imports | `const Chart = dynamic(() => import('./Chart'))` |
| Streaming | `<Suspense fallback={<Loading />}>` |
| Prefetching | `<Link>` auto-prefetches |

---

## 9. SEO

```jsx
// Static metadata
export const metadata = {
  title: 'Page Title',
  description: 'Page description',
  openGraph: { title: '...', images: ['...'] },
};

// Dynamic metadata
export async function generateMetadata({ params }) {
  const data = await fetchData(params.id);
  return { title: data.title };
}
```

- **Sitemap:** `app/sitemap.js`
- **Robots:** `app/robots.js`
- **Structured Data:** JSON-LD `<script>` tag

---

## 10. Deployment

| Platform | Difficulty | Best For |
|----------|-----------|----------|
| Vercel | Easiest | Most Next.js projects |
| AWS | Hard | Enterprise, full control |
| Docker | Medium | Consistent environments |
| Static Export | Easy | No server features needed |

**Environment Variables:**
- `NEXT_PUBLIC_*` → available in browser
- No prefix → server only (secrets, DB URLs)

---

## 11. Middleware

```jsx
// middleware.js (project root)
export function middleware(request) {
  if (!request.cookies.get('token')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  return NextResponse.next();
}
export const config = { matcher: ['/dashboard/:path*'] };
```

---

## 12. Server Actions

```jsx
// Action file
"use server";
export async function createPost(formData) {
  await db.post.create({ data: { title: formData.get('title') } });
  revalidatePath('/blog');
}

// Usage
<form action={createPost}>
  <input name="title" />
  <button>Create</button>
</form>
```

---

## 13. Caching (4 Layers)

| Layer | Scope | Duration | Opt Out |
|-------|-------|----------|---------|
| Request Memoization | Single render | Automatic | N/A |
| Data Cache | Fetch responses | Forever / revalidate | `cache: 'no-store'` |
| Full Route Cache | Static pages | Forever | `dynamic = 'force-dynamic'` |
| Router Cache | Client navigation | 30s–5min | `router.refresh()` |

**Revalidation:**
- `revalidatePath('/blog')` — By path
- `revalidateTag('posts')` — By tag
- On-demand via webhooks

---

## Quick Decision Guide

```
Need SEO?
├── NO → CSR (dashboard, admin)
└── YES → Does content change per user?
    ├── YES → SSR (cache: 'no-store')
    └── NO → Does content change often?
        ├── NO → SSG (default fetch)
        └── YES → ISR (next: { revalidate: N })

Need interactivity (clicks, forms, hooks)?
├── YES → "use client" (Client Component)
└── NO → Server Component (default)

Need a backend endpoint?
├── External consumers → API Route (route.js)
└── Internal form/mutation → Server Action ("use server")
```

---

### 🔗 Navigation
- ⬅️ Previous: [14_Caching.md](./14_Caching.md)
- ➡️ Next: [100_Project_Ideas.md](./100_Project_Ideas.md)
