# 📌 05 — Security Headers (Helmet): Browser-Side Defenses

## 🧠 Concept Explanation

### Basic → Intermediate
Security Headers are HTTP headers that tell the browser how to behave when interacting with your site. They provide an extra layer of security by restricting browser features that could be exploited by attackers.

### Advanced → Expert
At a staff level, security headers are the **Final Defense** against client-side attacks (XSS, Clickjacking).
1. **Content-Security-Policy (CSP)**: The most powerful header. It defines which scripts, styles, and images are allowed to load. It can prevent XSS even if an attacker manages to inject a `<script>` tag.
2. **HSTS (HTTP Strict Transport Security)**: Forces the browser to only communicate over HTTPS.
3. **X-Frame-Options**: Prevents your site from being embedded in an `<iframe>` (protects against Clickjacking).
4. **X-Content-Type-Options**: Prevents the browser from "sniffing" the content type and executing a `.txt` file as a `.js` file.

---

## 🏗️ Common Mental Model
"I use Helmet, so I'm secure."
**Correction**: Helmet's **default** settings are a great start, but they are often too permissive for high-security apps. Specifically, the default CSP is very loose because a strict CSP can break many existing websites. You must manually tune your CSP.

---

## ⚡ Actual Behavior: CSP and Inline Scripts
A strict CSP will block **all** inline scripts (`<script>alert(1)</script>`) and `eval()`. This breaks many analytics tools and older libraries. To fix this, you must use **Nonces** (Number used once) or **Hashes** to allow specific, trusted inline scripts.

---

## 🔬 Internal Mechanics (Networking + Browser)

### The CSP Report-Only Mode
Implementing a strict CSP can break your site. You can use the `Content-Security-Policy-Report-Only` header to see what *would* have been blocked without actually blocking it. This allows you to tune your policy in production before enforcing it.

---

## 📐 ASCII Diagrams

### How CSP Blocks XSS
```text
  1. ATTACKER INJECTS: <script src="evil.com/hack.js"></script>
     │
     ▼
  2. BROWSER CHECKS CSP: 
     "script-src 'self' trusted.com;"
     │
     ▼
  3. RESULT: evil.com is NOT in the trusted list.
     BROWSER BLOCKS the execution. App is SAFE.
```

---

## 🔍 Code Example: Custom Helmet Configuration
```javascript
const express = require('express');
const helmet = require('helmet');

const app = express();

// Use Helmet with custom CSP
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "trusted-scripts.com"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", "data:", "images.com"],
        connectSrc: ["'self'", "api.trusted.com"],
        upgradeInsecureRequests: [],
      },
    },
    referrerPolicy: { policy: 'same-origin' },
  })
);
```

---

## 💥 Production Failures & Debugging

### Scenario: The Broken Analytics
**Problem**: After enabling Helmet, your Google Analytics or Facebook Pixel stops working.
**Reason**: The default CSP blocks external scripts from domains not explicitly allowed.
**Fix**: Add the analytics domains (e.g. `*.google-analytics.com`) to the `scriptSrc` and `imgSrc` directives.

### Scenario: The Clickjacking Vulnerability
**Problem**: An attacker creates a site that overlays your "Delete Account" button with a transparent iframe of your site.
**Fix**: Ensure `X-Frame-Options` is set to `DENY` or `SAMEORIGIN`. Helmet does this by default.

---

## 🧪 Real-time Production Q&A

**Q: "Is HSTS better than a simple 301 redirect from HTTP to HTTPS?"**
**A**: **Yes.** A 301 redirect still allows the *first* request to go over HTTP, which an attacker can intercept (SSL Stripping). HSTS tells the browser to **never** even try HTTP for your domain.

---

## 🏢 Industry Best Practices
- **Use CSP Nonces**: For any unavoidable inline scripts.
- **Set `expect-ct`**: (Certificate Transparency) to prevent the use of misissued certificates.

---

## 💼 Interview Questions
**Q: What is the purpose of the `X-Content-Type-Options: nosniff` header?**
**A**: It prevents the browser from trying to guess the content type of a file. For example, if a user uploads a malicious script with a `.jpg` extension, `nosniff` prevents the browser from executing that file if the server says it's an image.

---

## 🧩 Practice Problems
1. Build a strict CSP that only allows scripts from your own domain. Observe how it blocks an inline `onclick` handler in your HTML.
2. Configure HSTS with `includeSubDomains` and `preload`. Explain the risks of doing this on a development domain.

---

**Prev:** [04_Cryptography_and_Hashing.md](./04_Cryptography_and_Hashing.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** [../Testing/01_Unit_Testing_Patterns.md](../Testing/01_Unit_Testing_Patterns.md)
