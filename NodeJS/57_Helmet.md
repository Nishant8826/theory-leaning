# Helmet

By default, Express response headers expose framework details (like the `X-Powered-By: Express` header), making it easy for attackers to identify your framework and search for known exploits. Additionally, browsers rely on HTTP headers to enforce security policies. Helmet sets these headers to secure your application and protect users from common web vulnerabilities.

### HTTP Security Headers
Helmet is an Express middleware collection that sets HTTP headers to secure your application:
* **`Content-Security-Policy` (CSP)**: Restricts the sources from which the browser can load scripts, images, and other resources. This is a powerful defense against **Cross-Site Scripting (XSS)** and data injection attacks.
* **`X-Frame-Options`**: Controls whether your site can be embedded inside an `<iframe>` on another website, defending against **Clickjacking** attacks.
* **`Strict-Transport-Security` (HSTS)**: Forces browsers to connect to your domain exclusively over secure HTTPS, preventing SSL-stripping attacks.
* **`X-Content-Type-Options`**: Set to `nosniff`. This prevents browsers from guessing (sniffing) the MIME type of a file based on its content, forcing them to adhere to the declared `Content-Type` header (protects against script injection in file uploads).
* **`Referrer-Policy`**: Controls how much referrer information (the URL from which the user clicked a link) is sent along with requests.

## Deep Dive

### Content Security Policy (CSP) Configuration
The default CSP configuration in Helmet is strict. If your Node.js application serves server-rendered views (like EJS) that load external scripts (e.g. from Google Fonts, CDNs, or analytics APIs), the browser will block them unless you configure the CSP explicitly:
* **`directives`**: Define policy rules for different resource types:
  * `default-src`: Fallback policy for resources without explicit rules.
  * `script-src`: Restricts script file sources.
  * `style-src`: Restricts CSS styling sources.

## Visual Explanation

### Clickjacking Vulnerability and X-Frame-Options Mitigation
```text
Clickjacking Attack Scenario:
+-----------------------------------------------------------+
| [ Attacker's Malicious Site ]                             |
|   - Display: "Click here to win a free iPad!" (Button)    |
|   - Layer: Transparent <iframe> loading your bank site    |
|     (Positioned exactly over the button)                  |
+-----------------------------------------------------------+
  - User clicks "win iPad" ──> Clicks transparent bank iframe "Transfer money" button!

Mitigation using X-Frame-Options: SAMEORIGIN
Browser inspects response header: X-Frame-Options: SAMEORIGIN
  - Result: Browser blocks the iframe from rendering inside the attacker's site, securing the user.
```

## Real-World Example
Suppose you deploy an Express API. By default, it sends the header `X-Powered-By: Express`. An attacker scanning network packets identifies this and targets your server with Express-specific exploits. Adding `app.use(helmet())` strips this header and adds security headers, protecting your server.

## Code Examples

### Integrating and Configuring Helmet in Express

```javascript
// helmet-server.js
// Dependency required: npm install express helmet
const express = require('express');
const helmet = require('helmet');

const app = express();

// 1. Basic Integration (Enables 15 standard security headers automatically)
app.use(helmet());

// 2. Custom Content Security Policy (CSP) Configuration
// Configure this if you need to load resources from external CDNs
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"], // Only load resources from our own domain
      scriptSrc: ["'self'", 'https://apis.google.com'], // Allow scripts from Google APIs
      styleSrc: ["'self'", 'https://fonts.googleapis.com'], // Allow styles from Google Fonts
      fontSrc: ["'self'", 'https://fonts.gstatic.com'],     // Allow font files from Google
      objectSrc: ["'none'"], // Block Object/Embed plugins (like Flash)
      upgradeInsecureRequests: [] // Force HTTP requests to upgrade to HTTPS automatically
    }
  })
);

// 3. Custom X-Frame-Options (Clickjacking defense)
// Deny embedding in all frame hosts, including same origin
app.use(helmet.frameguard({ action: 'deny' }));

app.get('/api/status', (req, res) => {
  // In addition to headers set by Helmet, Express's X-Powered-By is stripped
  res.json({ status: 'UP' });
});

app.listen(3000, () => console.log('Helmet-secured server running on port 3000'));
```

## Best Practices
* **Load Helmet Early**: Place `app.use(helmet())` at the top of your middleware chain, before any routes or static file servers, to ensure all responses are secured.
* **Force HTTPS (HSTS)**: Ensure HSTS is enabled in production. Configure the `max-age` directive to at least 1 year (31,536,000 seconds) to ensure browsers remember the HTTPS rule.
* **Test CSP Directives**: Test your CSP configurations in a staging environment to ensure you do not accidentally block required third-party scripts or fonts.

## Interview Questions

**Q:** What is Helmet in Express.js?

> **Answer:**
> Helmet is a security middleware for Express applications that sets various HTTP headers in responses to secure the application against common web vulnerabilities.

**Q:** How does setting the `X-Content-Type-Options: nosniff` header improve security?

> **Answer:**
> It prevents browsers from guessing (sniffing) the MIME type of a file based on its contents, forcing them to use the type declared in the `Content-Type` header. This prevents attackers from uploading a script disguised as an image and executing it in the browser.

**Q:** What is a Clickjacking attack, and how does the `X-Frame-Options` header defend against it?

> **Answer:**
> Clickjacking is an attack where a user is tricked into clicking an element on a website while actually clicking a hidden, transparent iframe of another website layered on top of it.
> The `X-Frame-Options` header defends against this by telling the browser whether it is allowed to render the site inside a frame (`<frame>`, `<iframe>`, or `<object>`). Setting it to `DENY` or `SAMEORIGIN` prevents other domains from embedding your site inside their pages.

**Q:** In a single-page application (SPA) architecture utilizing a separate Node.js API server and static CDN frontend, how should Content Security Policy (CSP) headers be configured? Discuss the roles of the API server and the CDN.

> **Answer:**
> In an SPA architecture:

**Q:** CDN (Frontend Host)

> **Answer:**
> 

**Q:** API Server

> **Answer:**
> 

---
Previous : [56_OWASP_Top_Risks.md](56_OWASP_Top_Risks.md) | Index : [00_index.md](00_index.md) | Next : [58_CORS.md](58_CORS.md)
