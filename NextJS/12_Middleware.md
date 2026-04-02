# 12 – Middleware in Next.js

---

## What is Middleware?

Middleware is code that runs **BEFORE a request is completed** — it sits between the user's request and the final response. Think of it as a security checkpoint or a gatekeeper.

```
User makes a request → /dashboard
        ↓
MIDDLEWARE runs first
  ├── Is user logged in? → YES → Allow access to /dashboard
  └── Is user logged in? → NO  → Redirect to /login
        ↓
Page renders and responds
```

---

## Why Use Middleware?

| Use Case | Without Middleware | With Middleware |
|----------|-------------------|----------------|
| **Auth Protection** | Check session on every page individually | One file protects all routes |
| **Redirects** | Manual redirect logic per page | Centralized redirect rules |
| **Geo-based Content** | Detect country on every page | Detect once in middleware |
| **Rate Limiting** | Add logic per API route | Add once in middleware |
| **A/B Testing** | Complex client-side logic | Rewrite URL to variant page |

**Real-world Example:**
Amazon detects your country and automatically shows the correct currency and language. This happens in middleware before any page loads.

---

## How Middleware Works in Next.js

### Basic Setup

Create a single file `middleware.js` (or `.ts`) at the **root** of your project (same level as `app/` folder).

```
my-app/
├── app/
│   ├── page.js
│   └── dashboard/
│       └── page.js
├── middleware.js       ← HERE (root level)
├── package.json
└── next.config.js
```

### Basic Example: Auth Protection

```jsx
// middleware.js
import { NextResponse } from 'next/server';

export function middleware(request) {
  const token = request.cookies.get('session-token');

  // If trying to access /dashboard and not logged in → redirect
  if (request.nextUrl.pathname.startsWith('/dashboard') && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Allow the request to continue
  return NextResponse.next();
}

// Specify which routes middleware should run on
export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*', '/profile/:path*'],
};
```

### How the Flow Works:

```
User visits /dashboard/settings
        ↓
Middleware intercepts (matches '/dashboard/:path*')
        ↓
Checks for 'session-token' cookie
        ↓
├── Cookie EXISTS → NextResponse.next() → Page renders normally
└── Cookie MISSING → NextResponse.redirect('/login') → User goes to login
```

---

## ⭐ Most Important Concepts

### 1. The `matcher` Config

`matcher` controls WHICH routes the middleware runs on:

```jsx
// Run on specific paths
export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*'],
};

// Run on ALL paths except static files and api
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

| Pattern | Matches |
|---------|---------|
| `'/dashboard'` | Only `/dashboard` exactly |
| `'/dashboard/:path*'` | `/dashboard`, `/dashboard/settings`, `/dashboard/a/b/c` |
| `'/api/:path*'` | All API routes |
| `'/((?!api\|_next).*)` | Everything except `/api` and `/_next` |

### 2. What Middleware CAN Do

```jsx
import { NextResponse } from 'next/server';

export function middleware(request) {
  // 1. READ request data
  const path = request.nextUrl.pathname;
  const cookies = request.cookies;
  const headers = request.headers;
  const ip = request.ip;
  const geo = request.geo; // { country, city, region }

  // 2. REDIRECT to another page
  return NextResponse.redirect(new URL('/login', request.url));

  // 3. REWRITE to a different page (URL doesn't change)
  return NextResponse.rewrite(new URL('/variant-b', request.url));

  // 4. SET headers on the response
  const response = NextResponse.next();
  response.headers.set('X-Custom-Header', 'my-value');
  return response;

  // 5. SET cookies
  const response = NextResponse.next();
  response.cookies.set('visited', 'true', { maxAge: 86400 });
  return response;

  // 6. CONTINUE to the page (allow access)
  return NextResponse.next();
}
```

### 3. What Middleware CANNOT Do

| ❌ Cannot Do | Why |
|-------------|-----|
| Access database directly | Middleware runs on the Edge Runtime (limited APIs) |
| Use Node.js-specific APIs | No `fs`, `path`, `child_process` |
| Render components/HTML | Middleware processes requests, not rendering |
| Use heavy libraries | Edge Runtime has size limits |
| Modify request body | Can only read, redirect, rewrite, or set headers |

### 4. Real-World Middleware Patterns

#### A/B Testing

```jsx
// middleware.js
export function middleware(request) {
  // Randomly assign users to variant A or B
  const variant = Math.random() < 0.5 ? 'a' : 'b';

  // Check if user already has a variant assigned
  const existingVariant = request.cookies.get('ab-variant')?.value;

  if (existingVariant) {
    // Use existing variant
    const url = request.nextUrl.clone();
    url.pathname = `/variant-${existingVariant}${url.pathname}`;
    return NextResponse.rewrite(url);
  }

  // Assign new variant
  const url = request.nextUrl.clone();
  url.pathname = `/variant-${variant}${url.pathname}`;
  const response = NextResponse.rewrite(url);
  response.cookies.set('ab-variant', variant, { maxAge: 60 * 60 * 24 * 30 });
  return response;
}
```

#### Geo-Based Redirects

```jsx
// middleware.js
export function middleware(request) {
  const country = request.geo?.country || 'US';

  // Redirect Indian users to the IN store
  if (country === 'IN' && !request.nextUrl.pathname.startsWith('/in')) {
    return NextResponse.redirect(new URL('/in' + request.nextUrl.pathname, request.url));
  }

  // Redirect UK users to the UK store
  if (country === 'GB' && !request.nextUrl.pathname.startsWith('/uk')) {
    return NextResponse.redirect(new URL('/uk' + request.nextUrl.pathname, request.url));
  }

  return NextResponse.next();
}
```

#### Rate Limiting (Simple)

```jsx
// middleware.js
const rateLimit = new Map();

export function middleware(request) {
  const ip = request.ip ?? 'unknown';
  const now = Date.now();
  const windowMs = 60 * 1000; // 1 minute
  const maxRequests = 100;

  const requestLog = rateLimit.get(ip) || [];
  const recentRequests = requestLog.filter(time => now - time < windowMs);

  if (recentRequests.length >= maxRequests) {
    return new Response('Too Many Requests', { status: 429 });
  }

  recentRequests.push(now);
  rateLimit.set(ip, recentRequests);

  return NextResponse.next();
}

export const config = {
  matcher: '/api/:path*',
};
```

---

## Impact — Middleware vs Other Protection Methods

| Method | Runs Where | Speed | Best For |
|--------|-----------|-------|----------|
| **Middleware** | Edge (before server) | Fastest | Auth redirects, geo-routing, A/B testing |
| **Server Component check** | Server (during render) | Fast | Page-level auth, data-dependent access |
| **Client-side check** | Browser (after load) | Slowest | UI-level access (hide/show elements) |
| **API Route check** | Server (on API call) | Fast | Protecting API endpoints |

**Best Practice:** Use middleware for route-level protection. Use Server Component checks for data-level authorization. Use API route checks for API security.

---

## Interview Questions & Answers

### Q1: What is middleware in Next.js?
**Answer:** Middleware is code that runs before a request reaches the page or API route. It can redirect users, rewrite URLs, set cookies/headers, and gate access. It's defined in a single `middleware.js` file at the project root and runs on the Edge Runtime for maximum speed.

### Q2: Where do you create the middleware file?
**Answer:** At the root of the project, same level as the `app/` directory. It must be named `middleware.js` or `middleware.ts`. There can only be ONE middleware file per project.

### Q3: What is the `matcher` config in middleware?
**Answer:** `matcher` specifies which routes the middleware should run on. Without it, middleware runs on every request (including static files, images). Using `matcher: ['/dashboard/:path*']` ensures middleware only processes dashboard routes, improving performance.

### Q4: What is the difference between `redirect` and `rewrite` in middleware?
**Answer:** `redirect` changes the URL in the browser (user sees the new URL). `rewrite` serves a different page but keeps the original URL in the browser. Rewrites are used for A/B testing where you want users to see different content without changing the URL.

### Q5: Why does middleware run on the Edge Runtime instead of Node.js?
**Answer:** The Edge Runtime runs on CDN nodes close to the user, making middleware extremely fast (sub-millisecond). It has a smaller API surface than Node.js (no file system, no heavy libraries), but the speed advantage is critical for operations like auth checks that run on every request.

### Q6 (Scenario): You want to protect all `/admin/*` routes, redirect `/old-blog/*` to `/blog/*`, and detect user country for all pages. How would you structure middleware?
**Answer:** All three can be handled in the single `middleware.js` file. Check the pathname: if it starts with `/admin`, verify auth token. If it starts with `/old-blog`, redirect to `/blog`. For all other routes, read `request.geo.country` and set a cookie or header. Use `matcher` to cover all needed paths.

### Q7 (Scenario): Your middleware is slowing down your site because it runs on every request, including CSS and image files. How do you fix it?
**Answer:** Add a `matcher` config to exclude static files: `matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']`. This ensures middleware only runs on page requests, not on static asset requests.

---

### 🔗 Navigation

---

← Previous: [11_App_Router.md](11_App_Router.md) | Next: [13_Server_Actions.md](13_Server_Actions.md) →
