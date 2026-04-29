# 📌 06 — CORS (Cross-Origin Resource Sharing)

## 🌟 Introduction

**CORS** is a security feature built into your browser. It prevents one website (like `malicious-site.com`) from making requests to another website (like `your-bank.com`) and stealing your data.

By default, a browser follows the **Same-Origin Policy**: JavaScript can only talk to the exact same "origin" (Domain + Protocol + Port) it came from.

Think of it like a **Club Bouncer**:
-   The bouncer (Browser) checks every guest (Request).
-   If the guest is from a different city (Origin), the bouncer asks the club owner (Server), "Hey, do you allow guests from this city?"
-   If the owner says "Yes," the guest is allowed in.

---

## 🏗️ What defines an "Origin"?

An origin is the combination of three things:
1.  **Protocol** (`http` vs `https`)
2.  **Domain** (`example.com` vs `google.com`)
3.  **Port** (`:80` vs `:3000`)

If **any** of these are different, it's a "Cross-Origin" request.

---

## 🏗️ How it Works: The "Preflight" Request

For simple requests (like a basic `GET`), the browser just sends it. But for "complex" requests (like sending JSON or using `DELETE`), the browser sends a **Preflight Request** first.

1.  **Browser:** Sends an `OPTIONS` request. "Hey Server, I want to send a POST request with JSON. Is that okay?"
2.  **Server:** Responds with headers. "Yes, I allow POST requests from `myapp.com`."
3.  **Browser:** Now sends the **Actual Request**.

---

## 🚀 Common CORS Headers

| Header | Meaning |
| :--- | :--- |
| **`Access-Control-Allow-Origin`** | Which websites are allowed to talk to this server? (e.g., `https://myfrontend.com` or `*` for everyone). |
| **`Access-Control-Allow-Methods`** | Which HTTP actions are allowed? (GET, POST, PUT, DELETE). |
| **`Access-Control-Allow-Headers`** | Which custom headers can the frontend send? (Content-Type, Authorization). |
| **`Access-Control-Max-Age`** | How long should the browser "cache" the permission so it doesn't have to ask every time? |

---

## 🔍 Code Walkthrough: Express CORS Fix

If you see a "CORS Error" in your console, you need to fix it on the **Server**, not the Frontend.

```javascript
// Server (Express.js)
const express = require('express');
const cors = require('cors'); // Use the popular cors package
const app = express();

// ✅ Allow everyone (Easy for development)
app.use(cors());

// ✅ Allow specific origins only (Best for production)
app.use(cors({
  origin: 'https://mywebsite.com',
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

---

## 📐 Visualizing the Handshake

```text
BROWSER (myapp.com)             SERVER (api.com)
   │                               │
   │  (1) OPTIONS (Preflight)      │
   │ ────────────────────────────▶ │
   │                               │
   │  (2) Allow-Origin: myapp.com  │
   │ ◀──────────────────────────── │
   │                               │
   │  (3) ACTUAL REQUEST (POST)    │
   │ ────────────────────────────▶ │
```

---

## 🔬 Deep Technical Dive (V8 Internals)

### Network Layer Enforcement
CORS is **not** a V8 feature; it's a feature of the browser's **Network Layer**. V8 just executes the JavaScript. When the network layer receives a response from a different origin, it checks the headers. If the headers don't match, the network layer "hides" the response from V8 and throws a CORS error instead.

---

## 💼 Interview Questions

**Q1: Why does CORS exist?**
> **Ans:** It's a security measure to prevent "Cross-Site Request Forgery" (CSRF) and unauthorized access to data across different domains.

**Q2: What is a "Preflight Request"?**
> **Ans:** It's an `OPTIONS` request sent by the browser before the actual request to check if the server understands the CORS protocol and allows the specific origin/method/header.

**Q3: Can you bypass CORS?**
> **Ans:** Not in a browser. However, CORS only applies to browsers. Tools like Postman, `curl`, or your own backend server don't have CORS restrictions. A common "hack" is to use a **CORS Proxy** (your server acts as a middleman).

---

## ⚖️ Trade-offs

| Method | Benefit | Cost |
| :--- | :--- | :--- |
| **Wildcard `*`** | No more CORS errors! | Dangerous for production; anyone can steal your data. |
| **Whitelist** | Very secure. | More work to manage the list of allowed domains. |
| **Proxy Server** | Bypasses CORS entirely. | Adds extra latency (one more "hop" for your data). |

---

## 🔗 Navigation

**Prev:** [05_Rendering_Pipeline.md](05_Rendering_Pipeline.md) | **Index:** [../00_Index.md](../00_Index.md) | **Next:** [07_Web_Workers.md](07_Web_Workers.md)
