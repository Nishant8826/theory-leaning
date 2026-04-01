# 08 – Performance Optimization in Next.js

---

## What is Performance Optimization?

Performance optimization means making your web application **load faster**, **respond quicker**, and **use fewer resources**. Every millisecond of delay costs you users and revenue.

```
Google Research:
- 53% of users abandon a site if it takes more than 3 seconds to load
- A 1-second delay in page load → 7% loss in conversions
- Amazon: Every 100ms of latency costs 1% in sales
```

---

## Why Does It Matter?

| Metric | Business Impact |
|--------|----------------|
| **Page Load Time** | Directly affects bounce rate and conversions |
| **Core Web Vitals** | Google uses these for SEO ranking |
| **Bundle Size** | Larger JS = slower load on mobile devices |
| **Time to Interactive** | How fast users can click/type |

**Real-world Example:**
An e-commerce site that loads in 1.5 seconds vs 4 seconds will have drastically different conversion rates. Users won't wait — they'll go to a competitor.

---

## How to Optimize Performance in Next.js

### 1. Image Optimization with `next/image`

**What:** Next.js provides the `<Image>` component that automatically optimizes images.

**Why:** Images are typically 50–70% of a page's total weight. Unoptimized images destroy performance.

**How:**

```jsx
// ❌ BAD — Raw <img> tag
<img src="/hero-banner.png" alt="Hero" />
// Problem: Full-size 5MB image loads for everyone

// ✅ GOOD — Next.js <Image> component
import Image from 'next/image';

export default function HeroSection() {
  return (
    <Image
      src="/hero-banner.png"
      alt="Hero Banner"
      width={1200}
      height={600}
      priority        // Load immediately (above the fold)
      placeholder="blur"  // Show blur placeholder while loading
    />
  );
}
```

**Impact:** Next.js automatically:
- Converts to modern formats (WebP/AVIF)
- Resizes based on device screen size
- Lazy loads by default (images below the fold load when scrolled to)
- Serves from cache after first load

| Without `next/image` | With `next/image` |
|---------------------|-------------------|
| 5MB PNG downloaded | 200KB WebP served |
| Same image for phone & desktop | Resized per device |
| All images load at once | Lazy loaded as needed |
| No caching strategy | Cached automatically |

### 2. Font Optimization with `next/font`

**What:** Next.js can self-host Google Fonts to eliminate external network requests.

**Why:** External font requests add 200–500ms to page load and can cause layout shift (text visibly jumping when fonts load).

```jsx
// app/layout.js
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',   // Show fallback font until custom loads
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}

// Impact:
// - Font is downloaded at BUILD time and self-hosted
// - No external request to Google Fonts
// - No layout shift (CLS = 0)
```

### 3. Code Splitting (Automatic)

**What:** Next.js automatically splits your JavaScript into smaller chunks so users only download the code for the page they're visiting.

**Why:** Without code splitting, visiting `/about` would download the JavaScript for ALL pages.

```
Without Code Splitting:
  Visit /about → Downloads JS for Home, About, Products, Dashboard
  Total: 2MB 😩

With Code Splitting (Next.js default):
  Visit /about → Downloads JS for About page only
  Total: 150KB 🚀
```

This happens **automatically** — you don't need to do anything.

### 4. Dynamic Imports (Lazy Loading Components)

**What:** Load heavy components only when they're needed.

**Why:** Some components (charts, maps, rich text editors) are huge. Loading them upfront slows down the initial page load.

```jsx
// ❌ BAD — Chart library loads on initial page load
import HeavyChart from '@/components/HeavyChart';

export default function Dashboard() {
  return <HeavyChart />;
}
```

```jsx
// ✅ GOOD — Chart loads only when Dashboard is visited
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <p>Loading chart...</p>,
  ssr: false,   // Don't render on server (browser-only library)
});

export default function Dashboard() {
  return <HeavyChart />;
}
```

**Real-world Example:** A dashboard page with multiple charts. Instead of loading all chart libraries upfront (500KB+), load each chart only when the user scrolls to it.

### 5. Link Prefetching

**What:** Next.js `<Link>` component automatically prefetches linked pages in the background.

**Why:** When a user hovers near a link, Next.js has already loaded the page — clicking feels instant.

```jsx
import Link from 'next/link';

// This page is automatically prefetched when it appears in the viewport
<Link href="/products">Products</Link>

// Disable prefetching for rarely visited pages
<Link href="/terms" prefetch={false}>Terms & Conditions</Link>
```

### 6. React Suspense & Streaming

**What:** Show parts of the page as they become ready instead of waiting for everything.

**Why:** If a page has a fast header and a slow data section, the user sees the header immediately while the data area shows a loading state.

```jsx
// app/dashboard/page.js
import { Suspense } from 'react';
import UserStats from '@/components/UserStats';       // Slow (DB query)
import RecentActivity from '@/components/RecentActivity'; // Slow

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* These load independently — no blocking! */}
      <Suspense fallback={<p>Loading stats...</p>}>
        <UserStats />
      </Suspense>

      <Suspense fallback={<p>Loading activity...</p>}>
        <RecentActivity />
      </Suspense>
    </div>
  );
}
```

**Impact:** The page shell (h1, layout) renders instantly. Each data section appears as its data becomes available. No more "all or nothing" loading.

---

## ⭐ Most Important Concepts

### Core Web Vitals (Google's Key Metrics)

Google ranks websites partly based on these 3 metrics:

| Metric | What It Measures | Good Score | How Next.js Helps |
|--------|-----------------|------------|-------------------|
| **LCP** (Largest Contentful Paint) | How fast the main content loads | < 2.5s | SSR/SSG, Image optimization, Font optimization |
| **INP** (Interaction to Next Paint) | How fast the page responds to interactions | < 200ms | Smaller JS bundles, code splitting |
| **CLS** (Cumulative Layout Shift) | Visual stability (things jumping around) | < 0.1 | `next/font`, Image `width`/`height`, loading states |

### Bundle Analysis

Check what's making your JavaScript bundle large:

```bash
# Install analyzer
npm install @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});
module.exports = withBundleAnalyzer({});

# Run analysis
ANALYZE=true npm run build
```

This opens a visual treemap showing which libraries take the most space. Common offenders:
- `moment.js` → Replace with `date-fns` or `dayjs`
- `lodash` → Import individual functions: `import debounce from 'lodash/debounce'`
- Heavy UI libraries → Use dynamic imports

---

## Impact – Real Application Performance Checklist

| Optimization | When to Apply | Expected Impact |
|-------------|--------------|-----------------|
| `next/image` | Always for images | 50–80% size reduction |
| `next/font` | Always for custom fonts | Eliminate layout shift |
| Dynamic imports | Heavy third-party libraries | Reduce initial JS by 30–50% |
| Suspense streaming | Pages with slow data sections | Instant page shell |
| SSG/ISR over SSR | Non-personalized content | 10x faster response |
| Prefetching (default) | Navigation links | Instant page transitions |
| Parallel data fetching | Multiple API calls | 2–3x faster data loading |

---

## Interview Questions & Answers

### Q1: How does Next.js optimize images?
**Answer:** The `next/image` component automatically converts images to modern formats (WebP/AVIF), resizes them for the device, lazy loads off-screen images, and caches them. It reduces image payload by 50–80% compared to raw `<img>` tags.

### Q2: What are Core Web Vitals?
**Answer:** Core Web Vitals are Google's metrics for page experience: LCP (loading speed), INP (interactivity), and CLS (visual stability). Google uses them as ranking factors. Next.js helps optimize all three through SSR/SSG, code splitting, image/font optimization, and streaming.

### Q3: What is code splitting and how does Next.js handle it?
**Answer:** Code splitting divides JavaScript into smaller chunks so users only download the code needed for the current page. Next.js does this automatically — each page gets its own JS bundle. Shared code is extracted into common chunks. You can also use `dynamic()` for component-level splitting.

### Q4: When would you use `dynamic()` imports?
**Answer:** For heavy third-party libraries (chart libraries, rich text editors, maps) that shouldn't be loaded upfront. Also for components that only work in the browser (using `ssr: false`) like components that access `window` or `document`.

### Q5: How does `next/font` improve performance?
**Answer:** It downloads Google Fonts at build time and self-hosts them — eliminating external network requests. It also prevents layout shift (CLS) by loading fonts synchronously with the HTML. The `display: 'swap'` option shows a fallback font instantly while the custom font loads.

### Q6: What is React Suspense and how does it help performance?
**Answer:** Suspense lets you show parts of a page as they become ready. Instead of blocking the entire page until all data loads, fast sections render immediately while slow sections show a loading state. This dramatically improves perceived performance.

### Q7 (Scenario): Your homepage has 20 product images and takes 8 seconds to load. How would you optimize it?
**Answer:** Replace `<img>` with `<Image>` from `next/image` for auto-optimization. Set `priority` on the first 2–3 visible images and let the rest lazy load. Use `placeholder="blur"` for better perceived performance. Also, consider using ISR to pre-render the page.

### Q8 (Scenario): Your dashboard page has 5 chart components and takes 6 seconds for the initial JavaScript to load. What would you do?
**Answer:** Use `dynamic()` imports with `ssr: false` for each chart component so they're loaded only when needed. Wrap each in `<Suspense>` for independent loading. The page shell renders instantly while charts load progressively.

---

### 🔗 Navigation
- ⬅️ Previous: [07_Authentication.md](./07_Authentication.md)
- ➡️ Next: [09_SEO.md](./09_SEO.md)
