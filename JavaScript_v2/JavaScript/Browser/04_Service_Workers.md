# 📌 04 — Service Workers

## 🧠 Concept Explanation

Service Workers are JavaScript files that run in a separate thread (not the main page thread) and act as a **programmable network proxy** between your web app and the network. They enable:
- **Offline support** — Cache resources, serve from cache when offline
- **Background sync** — Defer failed requests until connectivity returns
- **Push notifications** — Receive push messages even when the page is closed
- **Request interception** — Modify, redirect, or respond to any network request

Service Workers are NOT accessible to the DOM and run in a separate Worker context with their own V8 Isolate and event loop.

## 🔬 Internal Mechanics

### Service Worker Lifecycle

```
INSTALL → ACTIVATE → RUNNING (idle/active)

1. INSTALL:
   - SW script downloaded and parsed
   - `install` event fires
   - Typically: pre-cache critical resources
   - New SW waits (WAITING state) until all existing tabs using old SW are closed
   
2. ACTIVATE:
   - Old SW terminated
   - New SW takes control
   - `activate` event fires
   - Typically: clean up old caches
   - Does NOT control currently open pages (only future navigations)
   
3. RUNNING:
   - Idle: SW may be terminated to save memory (can restart anytime)
   - Active: Handling fetch/message/push events
   - Fetch events: intercept network requests from controlled pages
```

### The Cache API (not localStorage)

```javascript
// Cache API is the SW's primary storage mechanism
// Stores Request → Response pairs
// Backed by disk cache (separate from browser's network cache)

const cache = await caches.open('my-cache-v1')
await cache.put(request, response)  // Store
const cached = await cache.match(request)  // Retrieve
await cache.delete(request)  // Delete
```

### Controlled Scope

```
Origin: https://app.example.com
SW scope: https://app.example.com/  (controls all same-origin resources)
  OR restricted: https://app.example.com/app/  (controls /app/* only)

SW cannot control:
- Cross-origin requests (different origin)
- Pages outside its scope
```

## 🔁 Execution Flow — Fetch Interception

```javascript
self.addEventListener('fetch', (event) => {
  // This intercepts EVERY network request from controlled pages
  // event.request: the Request object
  // event.respondWith(): provide the response
  
  event.respondWith(
    // Strategy: Cache First
    caches.match(event.request)
      .then(cached => {
        if (cached) return cached  // Serve from cache
        
        return fetch(event.request)  // Network fallback
          .then(response => {
            // Clone response (streams can only be consumed once)
            const toCache = response.clone()
            caches.open('dynamic-v1')
              .then(cache => cache.put(event.request, toCache))
            return response
          })
      })
      .catch(() => caches.match('/offline.html'))  // Offline fallback
  )
})
```

## 🧠 Memory Behavior

```
Service Worker memory lifecycle:
- SW runs in a separate Renderer thread (not main page thread)
- V8 Isolate separate from page's Isolate
- SW may be KILLED by browser when idle (to save memory/battery)
- SW is restarted for new events (fetch, push, message)
- State must be in Cache API or IndexedDB (not memory variables!)
- Memory variables: LOST when SW is killed and restarted

Critical: Don't store important state in SW variables!
let count = 0  // This is RESET every time SW restarts
```

## 📐 ASCII Diagram — SW Caching Strategies

```
CACHE FIRST (offline-first):
  Request → Cache hit? → YES → Serve cache
                      → NO  → Network → Serve + cache response

NETWORK FIRST (freshness-first):
  Request → Network → Success → Serve + update cache
                   → Fail    → Cache → Serve cache
                              → No cache → Error

STALE WHILE REVALIDATE (balanced):
  Request → Cache hit? → YES → Serve cache immediately
                               + fetch network in background → update cache
                      → NO  → Network → Serve + cache

CACHE ONLY (full offline):
  Request → Cache → Serve (no network ever)

NETWORK ONLY (no caching):
  Request → Network → Serve (standard browser behavior)
```

## 🔍 Code Examples

### Example 1 — Installation and Pre-caching

```javascript
// service-worker.js
const CACHE_NAME = 'app-v2'
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/css/main.css',
  '/js/app.js',
  '/fonts/inter.woff2',
  '/images/logo.svg'
]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Pre-caching static assets')
        return cache.addAll(STATIC_ASSETS)
        // cache.addAll fetches each URL and stores the response
        // If ANY fails: install fails, SW not installed
      })
      .then(() => self.skipWaiting())  // Activate immediately
  )
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))  // Delete old caches
      ))
      .then(() => self.clients.claim())  // Take control of all pages immediately
  )
})
```

### Example 2 — Background Sync

```javascript
// Register sync in main page:
async function saveMessageOffline(message) {
  // Store in IndexedDB (survives page close)
  await idb.put('pending-messages', message)
  
  // Register sync tag (fires when online)
  const registration = await navigator.serviceWorker.ready
  await registration.sync.register('sync-messages')
}

// Handle sync in Service Worker:
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-messages') {
    event.waitUntil(syncPendingMessages())
  }
})

async function syncPendingMessages() {
  const db = await openDB('app', 1)
  const messages = await db.getAll('pending-messages')
  
  for (const message of messages) {
    try {
      await fetch('/api/messages', {
        method: 'POST',
        body: JSON.stringify(message)
      })
      await db.delete('pending-messages', message.id)
    } catch (e) {
      // Still offline — sync will retry
      throw e  // Throwing causes sync to retry
    }
  }
}
```

### Example 3 — Push Notifications

```javascript
// Main page: subscribe to push
async function subscribeToPush() {
  const registration = await navigator.serviceWorker.ready
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
  })
  
  // Send subscription to server
  await fetch('/api/push-subscribe', {
    method: 'POST',
    body: JSON.stringify(subscription)
  })
}

// Service Worker: handle push
self.addEventListener('push', (event) => {
  const data = event.data.json()
  
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/icons/notification.png',
      badge: '/icons/badge.png',
      data: { url: data.url }
    })
  )
})

self.addEventListener('notificationclick', (event) => {
  event.notification.close()
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  )
})
```

## 💥 Production Failures

### Failure 1 — Stale SW Update (Users Stuck on Old Version)

```javascript
// Problem: By default, new SW waits until ALL tabs are closed
// Users on long sessions may be on old SW for days

// Fix 1: skipWaiting + clients.claim in new SW
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())  // Don't wait for old clients
  )
})
self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim())  // Take immediate control
})

// Fix 2: Prompt user to update (React pattern)
navigator.serviceWorker.addEventListener('controllerchange', () => {
  window.location.reload()  // Reload to get new SW
  // Or: Show "Update available" banner with manual reload option
})
```

### Failure 2 — Infinite Loop from Caching SW Script

```javascript
// DO NOT cache the service worker file itself!
// This creates: page loads SW → SW caches itself → update never detected

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url)
  
  // NEVER cache the SW script
  if (url.pathname === '/service-worker.js') return
  
  // NEVER cache Chrome extensions
  if (url.protocol === 'chrome-extension:') return
  
  event.respondWith(/* caching strategy */)
})
```

## ⚠️ Edge Cases

### SW Scope and Path Matching

```javascript
// SW registration:
navigator.serviceWorker.register('/sw.js', { scope: '/app/' })
// SW only intercepts fetches for /app/* paths
// Requests to /api/* are NOT intercepted (outside scope)

// Service-Worker-Allowed header: can expand scope beyond registration directory
// Server must send: Service-Worker-Allowed: /
// Then SW at /app/sw.js can have scope: '/'
```

### importScripts in SW

```javascript
// SW can import other scripts synchronously (SW context only)
importScripts('/js/sw-utils.js', '/js/idb-min.js')
// These are fetched synchronously (SW has no modules by default)
// For ESM SW: add type:'module' to register() options (Chrome 91+)
```

## 🏢 Industry Best Practices

1. **Version cache names** — `app-v2`, `app-v3`. Activate deletes old versions.
2. **Never cache the SW itself** — Browser handles SW update detection.
3. **Use Workbox** — Google's SW library handles strategies, cleanup, versioning.
4. **Test offline behavior** — DevTools → Application → Service Workers → Offline.
5. **Implement a reload prompt** — When new SW activates, prompt users to reload.

## ⚖️ Trade-offs

| Strategy | Freshness | Offline | Complexity | Use Case |
|---------|-----------|---------|------------|---------|
| Cache First | Stale | Yes | Low | Static assets |
| Network First | Fresh | Yes (fallback) | Medium | API data |
| Stale-While-Revalidate | Eventually fresh | Yes | Medium | Frequent content |
| Cache Only | Always stale | Yes | Lowest | Offline-first apps |

## 💼 Interview Questions

**Q1: Why can't Service Workers access the DOM?**
> Service Workers run in a separate thread (Worker context) with no access to the window object, document, or DOM API. This is by design — SWs handle background tasks (caching, push, sync) that should not block or interact with the UI. The main page and SW communicate via `postMessage` / `BroadcastChannel`. This separation also means SWs can run even when the page is closed.

**Q2: Why does `skipWaiting()` exist and when should you use it?**
> By default, a new SW waits until all tabs using the old SW are closed before activating. This prevents inconsistencies (old page + new cache can cause mismatches). `skipWaiting()` forces the new SW to activate immediately, even with old pages open. Use it when: your app can handle cache mismatches gracefully, or you always reload pages after SW update (via `clients.claim()` + reload). Don't use it if old pages reading from an old cache format would break with new cache format.

## 🔗 Navigation

**Prev:** [03_Browser_Storage.md](03_Browser_Storage.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [05_Rendering_Pipeline.md](05_Rendering_Pipeline.md)
