# 📌 04 — Service Workers

## 🌟 Introduction

A **Service Worker** is a script that the browser runs in the background, separate from your web page. It acts like a **Programmable Proxy** or a **Guardian Angel** for your app.

Its main superpower? **Offline Support.** It can intercept network requests and serve cached files even when there is no internet.

Think of it like a **Personal Assistant**:
-   The assistant sits between you (the App) and the store (the Server).
-   If the store is closed (no internet), the assistant gives you the items from their own pantry (the Cache).

---

## 🏗️ Key Features

1.  **Offline Mode:** Users can still use your app without a connection.
2.  **Push Notifications:** You can send alerts to users even if the website is closed.
3.  **Background Sync:** If a user sends a message while offline, the Service Worker waits for the internet to return and then sends it automatically.

---

## 🏗️ The Lifecycle

A Service Worker goes through three main stages:

1.  **Installing:** The browser downloads the script. This is usually where you **Pre-cache** your main CSS, JS, and HTML files.
2.  **Activating:** The new script takes control. This is where you delete old, outdated caches.
3.  **Running:** The Service Worker is now idle until it's needed (e.g., when a network request is made).

---

## 🚀 Caching Strategies

How should the Service Worker handle a request? Here are the most common strategies:

-   **Cache First:** Check the cache. If it's there, use it. If not, go to the network. (Best for images and fonts).
-   **Network First:** Try the network. If it fails, use the cache. (Best for news or live data).
-   **Stale-While-Revalidate:** Give the cached version immediately, but fetch a fresh version in the background to update the cache for next time. (Best for social media feeds).

---

## 🔍 Code Walkthrough: A Simple Cache-First SW

```javascript
// service-worker.js

const CACHE_NAME = 'my-app-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/styles.css',
  '/script.js'
];

// 1. Install Event (Pre-caching)
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

// 2. Fetch Event (Intercepting requests)
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      // If file is in cache, return it. Otherwise, fetch from network.
      return response || fetch(event.request);
    })
  );
});
```

---

## 📐 Visualizing the Flow

```text
[  APP  ] ─── (Request) ──▶ [ SERVICE WORKER ] ─── (Request) ──▶ [ SERVER ]
                                  │    ▲
                                  │    │
                            [   CACHE   ] (Pantry)
```

---

## ⚡ Comparison Table

| Feature | Regular Script | Service Worker |
| :--- | :--- | :--- |
| **Thread** | Main Thread (UI). | Worker Thread (Background). |
| **DOM Access** | ✅ Yes. | ❌ No (Cannot touch HTML). |
| **Persistence** | Reset on Refresh. | Stays active in the background. |
| **Network** | Direct. | Intercepted/Proxied. |

---

## 🔬 Deep Technical Dive (V8 Internals)

### Separate Isolates
A Service Worker runs in a completely separate **V8 Isolate**. This means it has its own memory and its own garbage collector. Because it doesn't share memory with the main page, they communicate using `postMessage()`. This isolation ensures that a slow Service Worker cannot "freeze" your UI.

---

## 💼 Interview Questions

**Q1: Why can't a Service Worker access the DOM?**
> **Ans:** Because it runs on a separate thread in the background. This allows it to run even when the page is closed (for push notifications) and prevents it from blocking the user interface.

**Q2: What is the difference between `install` and `activate`?**
> **Ans:** `install` happens when the browser first sees the worker; it's for setting up your cache. `activate` happens when the new worker is ready to take control; it's for cleaning up old data.

**Q3: How do you update a Service Worker?**
> **Ans:** If you change even one pixel in your `service-worker.js` file, the browser detects it as "new" and starts the install process again. The new worker will wait until all tabs of your site are closed before it becomes "active."

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Service Worker** | Enables PWA features (Offline/Push). | Adds complexity to your build and debugging. |
| **HTTP Caching** | Simple (set by server). | Very limited; no offline logic or background tasks. |
| **IndexedDB** | Stores structured data (like a database). | Cannot intercept network requests. |

---

## 🔗 Navigation

**Prev:** [03_Browser_Storage.md](03_Browser_Storage.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [05_Rendering_Pipeline.md](05_Rendering_Pipeline.md)
