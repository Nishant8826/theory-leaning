# 📌 03 — Browser Storage

## 🌟 Introduction

Browsers allow us to store data locally so the user doesn't have to download everything every time they visit.

Think of it like different storage spaces in your house:
1.  **LocalStorage:** Your **Home Office** (Stays forever, easy to access).
2.  **SessionStorage:** A **Post-it Note** (Temporary, thrown away when you close the tab).
3.  **Cookies:** Your **ID Badge** (Very small, sent to the server every time you visit).
4.  **IndexedDB:** The **Garage/Warehouse** (Huge, complex, good for massive amounts of data).

---

## 🏗️ Storage Comparison Table

| Feature | LocalStorage | SessionStorage | Cookies | IndexedDB |
| :--- | :--- | :--- | :--- | :--- |
| **Capacity** | 5-10MB | 5-10MB | < 4KB | Almost Unlimited |
| **Expires** | Never | When tab closes | Manual date | Never |
| **Access** | Synchronous | Synchronous | Synchronous | Asynchronous |
| **Sent to Server?**| No | No | **Yes** | No |

---

## 🏗️ LocalStorage vs SessionStorage

Both use the same simple API: `getItem`, `setItem`, `removeItem`.

```javascript
// LocalStorage (Stays after browser restart)
localStorage.setItem('theme', 'dark');
console.log(localStorage.getItem('theme')); // "dark"

// SessionStorage (Gone when you close the tab)
sessionStorage.setItem('temp_form_data', 'Hello');
```

> [!WARNING]
> **Performance Tip:** LocalStorage is **Synchronous**. If you try to save a massive 5MB JSON string, your entire website will freeze for a few milliseconds while the browser writes to the disk.

---

## 🏗️ Cookies (The ID Badge)

Cookies are mainly used for **Authentication**. Every time you make a request to a website, the browser automatically attaches your cookies.

-   **HttpOnly:** A security flag that prevents JavaScript from reading the cookie (stops XSS attacks).
-   **Secure:** Only sends the cookie over HTTPS.

---

## 🏗️ IndexedDB (The Powerhouse)

If you are building an offline app (like Google Docs or a Game), you use **IndexedDB**. It’s a real database inside your browser that can store gigabytes of data.

```javascript
// It's asynchronous, so it uses callbacks or promises
const request = indexedDB.open("MyDatabase", 1);

request.onsuccess = (event) => {
  const db = event.target.result;
  console.log("Database opened successfully!");
};
```

---

## 📐 Visualizing the Choice

```text
Do you need to send data to the server?
   │
   ├─ YES ──▶ [ Cookies ]
   │
   └─ NO ──▶ How much data?
               │
               ├─ SMALL (<5MB) ──▶ How long?
               │                     │
               │                     ├─ PERMANENT ──▶ [ LocalStorage ]
               │                     └─ TEMPORARY ──▶ [ SessionStorage ]
               │
               └─ LARGE (>5MB) ──▶ [ IndexedDB ]
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### SQLite Backend
In browsers like Chrome, `LocalStorage` and `IndexedDB` are actually backed by a **SQLite database** on your hard drive. When you call `localStorage.setItem`, the browser has to communicate with the operating system to write a file. This is why it’s slower than just changing a variable in memory.

---

## 💼 Interview Questions

**Q1: What is the main difference between LocalStorage and SessionStorage?**
> **Ans:** LocalStorage data persists even after the browser is closed and reopened. SessionStorage data is deleted as soon as the specific tab or window is closed.

**Q2: Why shouldn't you store sensitive data (like passwords) in LocalStorage?**
> **Ans:** LocalStorage is accessible by any JavaScript running on your page. if a hacker manages to run a malicious script (XSS), they can easily steal everything in your LocalStorage. Use **HttpOnly Cookies** for sensitive tokens.

**Q3: When would you use IndexedDB over LocalStorage?**
> **Ans:** Use IndexedDB when you have large amounts of structured data, need to perform complex searches/filtering, or are building a "Progressive Web App" (PWA) that works offline.

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **LocalStorage** | Easiest to use. | Blocks the main thread on large writes. |
| **Cookies** | Great for server-side auth. | Very small and adds overhead to every network request. |
| **IndexedDB** | Powerful and non-blocking. | Very complex API (hard to write manually). |

---

## 🔗 Navigation

**Prev:** [02_Event_Delegation.md](02_Event_Delegation.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [04_Service_Workers.md](04_Service_Workers.md)
