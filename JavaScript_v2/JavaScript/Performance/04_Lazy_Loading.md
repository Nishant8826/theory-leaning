# 📌 04 — Lazy Loading

## 🧠 Concept Explanation

Lazy loading defers loading of non-critical resources until they are needed. It improves initial page load time, reduces bandwidth, and decreases Time to Interactive (TTI). Key techniques: code splitting, image lazy loading, intersection-observer-based loading, route-based splitting.

## 🔍 Code Examples

### Code Splitting with Dynamic Import

```javascript
// Route-based code splitting (React)
import { lazy, Suspense } from 'react'
import { Routes, Route } from 'react-router-dom'

// Each route is a separate chunk (loaded on demand)
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))
const AdminPanel = lazy(() => import('./pages/AdminPanel'))  // Only loaded when navigated to

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/admin" element={<AdminPanel />} />
      </Routes>
    </Suspense>
  )
}

// Component-based splitting
const HeavyChart = lazy(() => import('./HeavyChart'))
function ReportPage({ showChart }) {
  return showChart ? (
    <Suspense fallback={<Skeleton />}>
      <HeavyChart />  {/* Loaded only when showChart=true */}
    </Suspense>
  ) : null
}
```

### Prefetching Strategy

```javascript
// Prefetch on hover (user intent signal)
const prefetchCache = new Set()

function prefetch(url) {
  if (prefetchCache.has(url)) return
  prefetchCache.add(url)
  
  const link = document.createElement('link')
  link.rel = 'prefetch'
  link.href = url
  document.head.appendChild(link)
}

// On navigation hover: prefetch the target page's JS chunk
document.querySelectorAll('a[data-prefetch]').forEach(link => {
  link.addEventListener('mouseenter', () => {
    prefetch(link.dataset.prefetch)
  }, { passive: true })
})

// Dynamic import prefetching
function prefetchModule(importFn) {
  // webpack magic comment for prefetch hints:
  return import(/* webpackPrefetch: true */ './HeavyFeature')
}
```

### Image Lazy Loading

```javascript
// Native (modern browsers): loading="lazy"
// <img src="photo.jpg" loading="lazy" width="800" height="600">

// Custom: IntersectionObserver
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return
    const img = entry.target
    
    // Load image
    const tempImg = new Image()
    tempImg.onload = () => {
      img.src = img.dataset.src
      img.classList.add('loaded')
    }
    tempImg.src = img.dataset.src
    
    imageObserver.unobserve(img)
  })
}, { rootMargin: '200px' })  // Start loading 200px before entering viewport

document.querySelectorAll('img[data-src]').forEach(img => imageObserver.observe(img))
```

## 🏢 Industry Best Practices

1. **Split by route first** — Route-based splitting is the highest-value, lowest-complexity split.
2. **Prefetch on hover** — 200-300ms user intent signal is enough to prefetch.
3. **Set width/height on images** — Prevents CLS when lazy-loaded images load.
4. **Use Webpack Bundle Analyzer** — Identify large chunks that should be split.
5. **Prioritize above-fold content** — Preload, not lazy-load, critical above-fold assets.

## 💼 Interview Questions

**Q1: What is the difference between lazy loading, prefetching, and preloading?**
> Lazy loading: defer loading until needed (user scrolls, navigates). Reduces initial bundle size. Prefetching: load resource when browser is idle, anticipating future need. Lower priority. Uses `link rel=prefetch` or `import(/* webpackPrefetch */)`. Preloading: load resource as high priority during current page load. Use for critical fonts, LCP images, JS needed immediately. Uses `link rel=preload`. Lazy = defer; Prefetch = idle future; Preload = urgent now.

## 🔗 Navigation

**Prev:** [03_Memory_Leaks.md](03_Memory_Leaks.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [05_Bundle_Optimization.md](05_Bundle_Optimization.md)
