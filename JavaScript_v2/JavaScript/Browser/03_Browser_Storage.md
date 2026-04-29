# 📌 03 — Browser Storage

## 🧠 Concept Explanation

The browser provides multiple storage mechanisms, each with different persistence, capacity, synchronous/async access, and scope:

| Storage | Capacity | Persistence | Scope | API |
|---------|----------|-------------|-------|-----|
| localStorage | 5-10MB | Until cleared | Origin | Sync |
| sessionStorage | 5-10MB | Tab session | Tab+Origin | Sync |
| IndexedDB | 50MB-2GB | Until cleared | Origin | Async |
| Cache API | Disk quota | Until cleared | Origin | Async |
| Cookies | 4KB/cookie | Configurable | Domain+Path | Sync |
| Memory (JS vars) | Heap limit | Page session | Page | Sync |

## 🔬 Internal Mechanics

### localStorage Internals (Blink)

localStorage is backed by SQLite in Chrome. The spec requires it to be **synchronous** — meaning `localStorage.setItem()` blocks the main thread until the write is confirmed. This is a critical performance issue:

```javascript
// This BLOCKS the main thread until write is complete
localStorage.setItem('large-data', JSON.stringify(bigObject))
// Browser writes to SQLite on the same thread as JS execution
// For large writes: can cause 50-100ms main thread blocks

// Profiler shows: "Storage" category blocking tasks
```

### IndexedDB — Async with V8 Structured Clone

IndexedDB uses the structured clone algorithm for serialization. Values are cloned when stored and when retrieved — both operations happen asynchronously via the IDB backend thread.

```javascript
const db = await openDB('myapp', 1, {
  upgrade(db) {
    db.createObjectStore('users', { keyPath: 'id' })
  }
})

// Write: structured clone serialization → async write to disk
await db.put('users', { id: 1, name: 'Alice', data: largeObject })

// Read: disk → structured clone deserialization → JS object
const user = await db.get('users', 1)
// user is a NEW object (not the same reference you stored)
```

## 🔁 Execution Flow — IndexedDB Transaction

```
IDBTransaction lifecycle:
1. db.transaction(['store'], 'readwrite')  → creates transaction scope
2. Store operations on transaction
3. Transaction auto-commits when:
   a. All requests complete AND
   b. No new requests are added before returning to event loop
4. OR: transaction.abort() to rollback ALL operations in transaction

Key: Transactions must be completed in ONE event loop task
     (cannot add requests across microtask boundaries!)
```

## 🔍 Code Examples

### Example 1 — localStorage Performance Safe Usage

```javascript
// BAD: Parsing JSON on every read
function getUser() {
  return JSON.parse(localStorage.getItem('user'))  // Sync + parse cost
}

// BETTER: In-memory cache with localStorage as backup
class StorageCache {
  constructor(key) {
    this.key = key
    this._cache = null
  }
  
  get() {
    if (!this._cache) {
      const raw = localStorage.getItem(this.key)
      this._cache = raw ? JSON.parse(raw) : null
    }
    return this._cache
  }
  
  set(value) {
    this._cache = value
    // Debounce localStorage write to avoid main-thread blocking
    clearTimeout(this._writeTimer)
    this._writeTimer = setTimeout(() => {
      localStorage.setItem(this.key, JSON.stringify(value))
    }, 100)
  }
}
```

### Example 2 — IndexedDB with idb Library

```javascript
import { openDB } from 'idb'

class UserStore {
  constructor() {
    this.db = openDB('myapp', 2, {
      upgrade(db, oldVersion, newVersion, transaction) {
        if (oldVersion < 1) {
          db.createObjectStore('users', { keyPath: 'id', autoIncrement: true })
        }
        if (oldVersion < 2) {
          // Migration: add index
          const store = transaction.objectStore('users')
          store.createIndex('by_email', 'email', { unique: true })
        }
      }
    })
  }
  
  async getByEmail(email) {
    const db = await this.db
    const tx = db.transaction('users', 'readonly')
    const index = tx.store.index('by_email')
    return index.get(email)  // O(log n) via B-tree index
  }
  
  async saveAll(users) {
    const db = await this.db
    const tx = db.transaction('users', 'readwrite')
    await Promise.all([
      ...users.map(user => tx.store.put(user)),
      tx.done  // Wait for transaction commit
    ])
  }
  
  async clearExpired(maxAge) {
    const db = await this.db
    const cutoff = Date.now() - maxAge
    const tx = db.transaction('users', 'readwrite')
    const cursor = await tx.store.openCursor()
    while (cursor) {
      if (cursor.value.createdAt < cutoff) await cursor.delete()
      await cursor.continue()
    }
  }
}
```

### Example 3 — Storage Quota and Eviction

```javascript
// Check available storage quota
const estimate = await navigator.storage.estimate()
console.log({
  usage: (estimate.usage / 1024 / 1024).toFixed(1) + 'MB',
  quota: (estimate.quota / 1024 / 1024).toFixed(1) + 'MB',
  percentUsed: (estimate.usage / estimate.quota * 100).toFixed(1) + '%'
})

// Request persistent storage (prevents eviction under storage pressure)
const isPersisted = await navigator.storage.persist()
if (isPersisted) {
  console.log('Storage will not be cleared by browser automatically')
} else {
  console.log('Storage may be cleared if device runs low on space')
}

// Storage eviction order (when device is low on space):
// Best Effort → Persistent
// 1. Caches (Service Worker Cache API) — evicted first
// 2. IndexedDB — evicted under pressure
// 3. localStorage — evicted last
// Persistent storage: requires user permission, evicted only by user
```

## 💥 Production Failures

### Failure — localStorage QuotaExceededError

```javascript
function saveToLocalStorage(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value))
  } catch (e) {
    if (e.name === 'QuotaExceededError') {
      // localStorage is full (5-10MB limit)
      // Strategy 1: Clear old data
      clearOldestLocalStorageItems()
      // Strategy 2: Move to IndexedDB
      // Strategy 3: Alert user
      console.error('Storage quota exceeded')
    } else {
      throw e
    }
  }
}

// Production note: Private/incognito mode may have 0MB localStorage!
// Always wrap localStorage in try/catch
```

### Failure — IDB Transaction Timeout

```javascript
// BUG: awaiting non-IDB operation inside transaction
async function buggyIDB(db) {
  const tx = db.transaction('users', 'readwrite')
  const user = await tx.store.get(1)
  
  await fetch('/api/enrich-user/' + user.id)  // Non-IDB async!
  // Transaction has auto-committed by now (microtask boundary crossed)
  // Next IDB operation will fail with TransactionInactiveError
  
  await tx.store.put({ ...user, enriched: true })  // ERROR!
}

// Fix: Complete all IDB operations before any external async
async function fixedIDB(db) {
  const user = await db.get('users', 1)  // Get outside transaction
  const enriched = await fetch('/api/enrich-user/' + user.id)
  await db.put('users', { ...user, ...await enriched.json() })  // Separate transaction
}
```

## ⚠️ Edge Cases

### localStorage in Private/Incognito Mode

```javascript
// In Safari private mode: localStorage throws immediately
// In Chrome incognito: localStorage works but is session-only (cleared on tab close)
// In Firefox private: localStorage is isolated and session-only

function isLocalStorageAvailable() {
  try {
    const test = '__storage_test__'
    localStorage.setItem(test, test)
    localStorage.removeItem(test)
    return true
  } catch(e) {
    return false
  }
}
```

## 🏢 Industry Best Practices

1. **Use localStorage only for tiny data** — User preferences, theme, auth tokens.
2. **Use IndexedDB for large/structured data** — Caches, offline data, user content.
3. **Always handle QuotaExceededError** — Set, delete, retry pattern.
4. **Use idb or Dexie.js** — Raw IDB API is verbose and error-prone.
5. **Request persistent storage** for critical offline apps.

## 💼 Interview Questions

**Q1: Why is localStorage synchronous and what are the performance implications?**
> localStorage was designed for simplicity — the original spec made it synchronous to avoid callback complexity (before Promises). The performance implication is that every read/write blocks the main thread. A 50KB JSON.stringify followed by localStorage.setItem can block the main thread for 5-20ms. This can cause visible jank (dropped frames) if done during user interaction. The browser must write to SQLite on the main thread. Always debounce localStorage writes and use IndexedDB for large data.

**Q2: What is an IDB transaction and why do they auto-commit?**
> IDB transactions group related operations atomically — either all succeed or all fail (rollback). They auto-commit when: (1) all outstanding requests complete AND (2) no new requests are added before control returns to the event loop (before the next microtask checkpoint). This design prevents transactions from being held open indefinitely, which would lock database access for other tabs/origins. The consequence: you cannot mix IDB operations with other async operations (fetch, setTimeout) inside a transaction.

## 🔗 Navigation

**Prev:** [02_Event_Delegation.md](02_Event_Delegation.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Service_Workers.md](04_Service_Workers.md)
