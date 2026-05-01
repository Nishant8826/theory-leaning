# 📌 Project: Fullstack Node.js & React App

## What
### 🧠 Concept Explanation
A Fullstack app is like **A Brain and a Body**.
**Analogy:** 
- **The Brain (Node.js):** Stores the memories (Database), makes the decisions (Business Logic), and knows the secrets (API Keys).
- **The Body (React):** Moves around, interacts with the world (The User), and feels things (UI/UX).
- **The Nervous System (HTTP/Fetch):** The signals sent between the brain and the body to keep them in sync. 
If the brain doesn't tell the body "I'm logged in," the body won't show the "Profile" page.

---

### 🏗️ Mental Model
- **Frontend:** React, Tailwind CSS, TanStack Query (React Query).
- **Backend:** Node.js, Express/Fastify, PostgreSQL (Prisma).
- **Auth:** JWT stored in `HttpOnly` cookies.
- **State Management:** React Query for server state; Context/Zustand for UI state.

---

## Why
### 🏢 Best Practices
1.  **Shared Types:** Use TypeScript to share interfaces between your Frontend and Backend.
2.  **Environment Variables:** Never put your API URL in your React code; use `process.env.VITE_API_URL`.
3.  **Loading States:** Always show a spinner or "Skeleton" while waiting for the Backend.
4.  **Error Boundaries:** Use React Error Boundaries to prevent the whole app from crashing if one component fails.

---

### ⚖️ Trade-offs
*   **Fullstack Monorepo (TurboRepo):** Great for small teams, shared types, and easy deployment. But can become a mess if the projects grow too different.
*   **Separate Repos:** Better for large teams where Frontend and Backend developers work independently, but harder to keep types in sync.

---

## How
### ⚡ Actual Behavior
*   **CORS:** The browser security feature that prevents a website on `domain-a.com` from calling an API on `domain-b.com` unless specifically allowed.
*   **Hydration:** React taking the static HTML from the server and "attaching" the JavaScript logic to it.
*   **Optimistic UI:** Updating the UI instantly (e.g., adding a "Like") before the server even responds, to make the app feel faster.

---

### 🔬 Internal Mechanics (V8 + libuv + OS)
*   **Browser Fetch API:** Uses the browser's networking stack (C++) to send requests.
*   **JSON Serialization:** The main cost of communication. Both React and Node.js spend CPU time converting objects to strings and back.

---

### 🔁 Execution Flow
1.  **Frontend:** User enters email/pass and clicks "Login."
2.  **Frontend:** `fetch('/api/login')` sends data to Node.js.
3.  **Backend:** Verifies credentials, creates a JWT, and sets it in a `Set-Cookie` header.
4.  **Frontend:** Browser automatically stores the cookie. React Query invalidates the `user` query.
5.  **Frontend:** React re-renders the navbar to show the "Logout" button.

---

### 🔍 Code Example (Latest Node.js - Secure Cookie Auth)
```javascript
// Backend: Setting the cookie
app.post('/api/login', (req, res) => {
    const token = generateToken(user);
    
    res.cookie('auth_token', token, {
        httpOnly: true, // Prevents XSS theft
        secure: true,   // Only over HTTPS
        sameSite: 'strict', // Prevents CSRF
        maxAge: 3600000 // 1 hour
    });
    
    res.json({ success: true, user: { name: user.name } });
});

// Frontend: Fetching with credentials
const login = async (credentials) => {
    const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
    });
    return res.json();
};
```

---

## Impact
### 💥 Production Failures
*   **Storing JWT in LocalStorage:** Making your app vulnerable to XSS. One bad npm package in your frontend could steal all your users' tokens. (Solution: Use `HttpOnly` cookies).
*   **Zombies in React:** Leaving an open WebSocket or `setInterval` in a React component after it's been unmounted, causing memory leaks and weird bugs.

---

### 🧪 Real-time Scenarios
*   **Infinite Scroll:** Using React Query to fetch "Page 2" as the user reaches the bottom of the list.
*   **Form Validation:** Using Zod on the Backend AND the same Zod schema on the Frontend (via `react-hook-form`) for perfectly synced validation.

---

### ⚠️ Edge Cases
*   **CORS Preflight:** Understanding why some requests trigger an `OPTIONS` request and how to handle it in Express.
*   **SSR vs SPA:** Deciding if you should pre-render the HTML on the server (Next.js) for SEO or just serve a blank page and let React build it (Vite).

---

---

Prev: [03_Microservices_System.md](./03_Microservices_System.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [../00_Index.md](../00_Index.md)
