# 📌 07 — Real-time Scenario & Production Problems

## 🌟 Introduction

Senior interviews go beyond theory. You'll be asked **"How would you solve this in production?"** This file covers **real-world scenarios** that top companies ask to test your system thinking and JavaScript depth.

---

## 🏗️ 1. Implement Infinite Scroll

**Scenario:** Build an infinite scroll that loads more items as the user scrolls down.

```javascript
class InfiniteScroll {
  constructor(container, loadMore) {
    this.container = container;
    this.loadMore = loadMore;
    this.loading = false;
    this.page = 1;

    // Use IntersectionObserver instead of scroll events
    this.sentinel = document.createElement('div');
    this.sentinel.className = 'scroll-sentinel';
    this.container.appendChild(this.sentinel);

    this.observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !this.loading) {
          this.fetchMore();
        }
      },
      { rootMargin: '200px' } // Start loading 200px before visible
    );

    this.observer.observe(this.sentinel);
  }

  async fetchMore() {
    this.loading = true;
    try {
      const items = await this.loadMore(this.page);
      if (items.length === 0) {
        this.observer.disconnect(); // No more data
        return;
      }
      this.renderItems(items);
      this.page++;
    } finally {
      this.loading = false;
    }
  }

  renderItems(items) {
    const fragment = document.createDocumentFragment();
    items.forEach(item => {
      const el = document.createElement('div');
      el.textContent = item.title;
      fragment.appendChild(el);
    });
    this.container.insertBefore(fragment, this.sentinel);
  }

  destroy() {
    this.observer.disconnect();
  }
}
```

**Why IntersectionObserver over scroll events?**
- No `throttle`/`debounce` needed
- Runs off the main thread (better performance)
- Handles nested scrollable containers

---

## 🏗️ 2. Implement Search with Debounce + Caching

**Scenario:** Build a search input that fetches results as the user types, with caching to avoid duplicate API calls.

```javascript
class SearchController {
  constructor(inputEl, resultsEl) {
    this.input = inputEl;
    this.results = resultsEl;
    this.cache = new Map();
    this.abortController = null;

    this.input.addEventListener(
      'input',
      this.debounce(this.handleSearch.bind(this), 300)
    );
  }

  debounce(fn, delay) {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn(...args), delay);
    };
  }

  async handleSearch(e) {
    const query = e.target.value.trim();
    if (query.length < 2) {
      this.results.innerHTML = '';
      return;
    }

    // Check cache first
    if (this.cache.has(query)) {
      this.renderResults(this.cache.get(query));
      return;
    }

    // Cancel previous in-flight request
    if (this.abortController) {
      this.abortController.abort();
    }
    this.abortController = new AbortController();

    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`, {
        signal: this.abortController.signal,
      });
      const data = await res.json();
      this.cache.set(query, data);
      this.renderResults(data);
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error('Search failed:', err);
      }
    }
  }

  renderResults(data) {
    this.results.innerHTML = data
      .map(item => `<div class="result">${item.title}</div>`)
      .join('');
  }
}
```

**Key Points Interviewers Look For:**
- ✅ Debouncing to avoid excessive API calls
- ✅ Caching to avoid duplicate requests
- ✅ AbortController to cancel stale requests
- ✅ Minimum query length check

---

## 🏗️ 3. Implement a Rate Limiter (Token Bucket)

**Scenario:** Limit how many API calls a user can make per second.

```javascript
class RateLimiter {
  constructor(maxTokens, refillRate) {
    this.maxTokens = maxTokens;
    this.tokens = maxTokens;
    this.refillRate = refillRate; // tokens per second
    this.lastRefill = Date.now();
  }

  refill() {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;
    this.tokens = Math.min(this.maxTokens, this.tokens + elapsed * this.refillRate);
    this.lastRefill = now;
  }

  async execute(fn) {
    this.refill();

    if (this.tokens < 1) {
      const waitTime = (1 - this.tokens) / this.refillRate * 1000;
      await new Promise(r => setTimeout(r, waitTime));
      this.refill();
    }

    this.tokens--;
    return fn();
  }
}

// Usage: max 5 requests per second
const limiter = new RateLimiter(5, 5);
await limiter.execute(() => fetch('/api/data'));
```

---

## 🏗️ 4. Implement Polling with Smart Backoff

**Scenario:** Poll an API for status updates, backing off when nothing changes.

```javascript
class SmartPoller {
  constructor(fn, { minInterval = 1000, maxInterval = 30000, backoffFactor = 1.5 } = {}) {
    this.fn = fn;
    this.minInterval = minInterval;
    this.maxInterval = maxInterval;
    this.backoffFactor = backoffFactor;
    this.currentInterval = minInterval;
    this.timer = null;
    this.lastResult = null;
  }

  start() {
    this.poll();
  }

  async poll() {
    try {
      const result = await this.fn();
      const hasChanged = JSON.stringify(result) !== JSON.stringify(this.lastResult);

      if (hasChanged) {
        this.currentInterval = this.minInterval; // Reset on change
        this.lastResult = result;
      } else {
        // Back off — nothing new
        this.currentInterval = Math.min(
          this.currentInterval * this.backoffFactor,
          this.maxInterval
        );
      }
    } catch (err) {
      this.currentInterval = Math.min(
        this.currentInterval * this.backoffFactor,
        this.maxInterval
      );
    }

    this.timer = setTimeout(() => this.poll(), this.currentInterval);
  }

  stop() {
    clearTimeout(this.timer);
  }
}
```

---

## 🏗️ 5. Handle Race Conditions in UI

**Scenario:** User clicks "Load Profile" rapidly. Each click fires an API call. An older response might arrive after a newer one, showing stale data.

```javascript
// Solution 1: AbortController
class ProfileLoader {
  constructor() {
    this.currentController = null;
  }

  async loadProfile(userId) {
    // Cancel any in-flight request
    if (this.currentController) {
      this.currentController.abort();
    }
    this.currentController = new AbortController();

    const res = await fetch(`/api/users/${userId}`, {
      signal: this.currentController.signal,
    });
    return res.json();
  }
}

// Solution 2: Request ID tracking
class SafeLoader {
  constructor() {
    this.latestRequestId = 0;
  }

  async load(url) {
    const requestId = ++this.latestRequestId;
    const data = await fetch(url).then(r => r.json());

    // Only use data if this is still the latest request
    if (requestId !== this.latestRequestId) {
      console.log('Stale response ignored');
      return null;
    }
    return data;
  }
}
```

---

## 🏗️ 6. Implement a Retry Queue for Offline Support

**Scenario:** User performs actions while offline. Queue them and replay when back online.

```javascript
class OfflineQueue {
  constructor() {
    this.queue = JSON.parse(localStorage.getItem('offlineQueue') || '[]');
    this.processing = false;

    window.addEventListener('online', () => this.flush());
  }

  add(request) {
    this.queue.push({
      url: request.url,
      method: request.method,
      body: request.body,
      timestamp: Date.now(),
    });
    localStorage.setItem('offlineQueue', JSON.stringify(this.queue));

    if (navigator.onLine) this.flush();
  }

  async flush() {
    if (this.processing || this.queue.length === 0) return;
    this.processing = true;

    while (this.queue.length > 0) {
      const req = this.queue[0];
      try {
        await fetch(req.url, {
          method: req.method,
          body: JSON.stringify(req.body),
          headers: { 'Content-Type': 'application/json' },
        });
        this.queue.shift(); // Remove successfully sent
        localStorage.setItem('offlineQueue', JSON.stringify(this.queue));
      } catch {
        break; // Still offline, stop retrying
      }
    }
    this.processing = false;
  }
}
```

---

## 🏗️ 7. Virtual List / Windowed Rendering

**Scenario:** Render 100,000 rows without crashing the browser.

```javascript
class VirtualList {
  constructor(container, items, rowHeight = 40) {
    this.container = container;
    this.items = items;
    this.rowHeight = rowHeight;
    this.visibleCount = Math.ceil(container.clientHeight / rowHeight) + 2;

    // Total height spacer
    this.spacer = document.createElement('div');
    this.spacer.style.height = `${items.length * rowHeight}px`;
    container.appendChild(this.spacer);

    // Content container
    this.content = document.createElement('div');
    this.content.style.position = 'relative';
    container.appendChild(this.content);

    container.style.overflow = 'auto';
    container.addEventListener('scroll', () => this.render());
    this.render();
  }

  render() {
    const scrollTop = this.container.scrollTop;
    const startIdx = Math.floor(scrollTop / this.rowHeight);
    const endIdx = Math.min(startIdx + this.visibleCount, this.items.length);

    this.content.innerHTML = '';
    this.content.style.transform = `translateY(${startIdx * this.rowHeight}px)`;

    for (let i = startIdx; i < endIdx; i++) {
      const row = document.createElement('div');
      row.style.height = `${this.rowHeight}px`;
      row.textContent = this.items[i];
      this.content.appendChild(row);
    }
  }
}
```

---

## 🏗️ 8. Implement localStorage with Expiry

```javascript
class StorageWithExpiry {
  set(key, value, ttlMs) {
    const item = {
      value,
      expiry: Date.now() + ttlMs,
    };
    localStorage.setItem(key, JSON.stringify(item));
  }

  get(key) {
    const raw = localStorage.getItem(key);
    if (!raw) return null;

    const item = JSON.parse(raw);
    if (Date.now() > item.expiry) {
      localStorage.removeItem(key);
      return null; // Expired
    }
    return item.value;
  }
}

// Usage
const store = new StorageWithExpiry();
store.set('token', 'abc123', 3600000); // 1 hour TTL
store.get('token'); // 'abc123' or null if expired
```

---

## 🏗️ 9. Implement `EventEmitter` (Node.js style)

```javascript
class EventEmitter {
  constructor() {
    this.events = new Map();
  }

  on(event, listener) {
    if (!this.events.has(event)) {
      this.events.set(event, []);
    }
    this.events.get(event).push({ listener, once: false });
    return this;
  }

  once(event, listener) {
    if (!this.events.has(event)) {
      this.events.set(event, []);
    }
    this.events.get(event).push({ listener, once: true });
    return this;
  }

  emit(event, ...args) {
    if (!this.events.has(event)) return false;

    const listeners = this.events.get(event);
    const remaining = [];

    for (const entry of listeners) {
      entry.listener.apply(this, args);
      if (!entry.once) remaining.push(entry);
    }

    if (remaining.length > 0) {
      this.events.set(event, remaining);
    } else {
      this.events.delete(event);
    }
    return true;
  }

  off(event, listener) {
    if (!this.events.has(event)) return this;
    const filtered = this.events.get(event).filter(e => e.listener !== listener);
    if (filtered.length > 0) {
      this.events.set(event, filtered);
    } else {
      this.events.delete(event);
    }
    return this;
  }

  removeAllListeners(event) {
    if (event) {
      this.events.delete(event);
    } else {
      this.events.clear();
    }
    return this;
  }
}
```

---

## 🏗️ 10. Build a Simple Router (SPA)

```javascript
class Router {
  constructor() {
    this.routes = new Map();
    this.notFound = () => document.body.innerHTML = '<h1>404</h1>';

    window.addEventListener('popstate', () => this.resolve());
  }

  addRoute(path, handler) {
    this.routes.set(path, handler);
    return this;
  }

  navigate(path) {
    window.history.pushState({}, '', path);
    this.resolve();
  }

  resolve() {
    const path = window.location.pathname;
    const handler = this.routes.get(path) || this.notFound;
    handler();
  }
}

// Usage
const router = new Router();
router
  .addRoute('/', () => { document.body.innerHTML = '<h1>Home</h1>'; })
  .addRoute('/about', () => { document.body.innerHTML = '<h1>About</h1>'; });
```

---

## 📐 Scenario Quick Reference

| Scenario | Key Pattern | Must Mention |
| :--- | :--- | :--- |
| Infinite Scroll | IntersectionObserver | Sentinel element, loading guard |
| Search Input | Debounce + AbortController | Cache, cancel stale requests |
| Rate Limiting | Token Bucket | Refill rate, burst capacity |
| Polling | Exponential Backoff | Change detection, max interval |
| Race Conditions | AbortController / Request ID | Stale response prevention |
| Offline Support | Queue + localStorage | Replay on reconnect |
| Large Lists | Virtual Scrolling | Only render visible rows |
| Expiring Cache | TTL in localStorage | Lazy cleanup on read |

---

## 🔗 Navigation

**Prev:** [06_Async_Interview_Mastery.md](06_Async_Interview_Mastery.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [08_JS_Output_Prediction.md](08_JS_Output_Prediction.md)
