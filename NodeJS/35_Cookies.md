# Cookies

Cookies are the standard mechanism for maintaining session state in web browsers. If you do not configure cookie security flags correctly, attackers can write scripts to steal session tokens (via XSS) or trigger actions on behalf of authenticated users (via CSRF). Understanding cookie security is essential for building secure web applications.

### HTTP Cookie Exchange
Cookies are key-value text pairs managed by the browser:
1. **Server Response**: The server instructs the browser to store a cookie by adding a `Set-Cookie` header in the HTTP response:
   ```http
   Set-Cookie: session_id=abc123; Path=/; HttpOnly
   ```
2. **Client Request**: For subsequent HTTP requests matching the cookie's path and domain, the browser automatically appends the stored cookie to the request's `Cookie` header:
   ```http
   Cookie: session_id=abc123
   ```

### Cookie Security Attributes
To prevent attacks, configure three security flags on every cookie:
* **`HttpOnly`**: Blocks client-side JavaScript (like `document.cookie`) from accessing the cookie. This prevents malicious scripts (XSS attacks) from stealing session tokens.
* **`Secure`**: Instructs the browser to only transmit the cookie over encrypted **HTTPS** connections, preventing packet-sniffing attacks on public Wi-Fi networks.
* **`SameSite`**: Controls whether cookies are sent along with cross-site requests, protecting against **CSRF (Cross-Site Request Forgery)** attacks:
  * `Strict`: The cookie is only sent in first-party contexts (when the site in the URL matches the site hosting the cookie).
  * `Lax` (Default in modern browsers): The cookie is withheld on cross-site subrequests (like image loads) but sent when a user navigates to the origin site (e.g. clicking a link).
  * `None`: The cookie is sent on all cross-site requests, but requires the `Secure` flag to be set.

## Deep Dive

### Signed Cookies
While `HttpOnly` prevents scripts from reading cookies, a user can still modify cookie values in their browser's developer tools.
To prevent tampering:
* **Sign the cookie**: Express can sign cookies using a secret key. It appends a cryptographic signature (HMAC) to the cookie value.
* **Verify on receipt**: When the client sends the cookie back, the server verifies the signature. If the client modified the value, the signature check fails, and the server rejects the cookie.

## Visual Explanation

### Cookie Security Flags Defense
```text
  [ Attacker launches XSS Script ] ── Attempts to read ──> [ document.cookie ]
                                                                   │
                                                                   ▼
                                                       Returns EMPTY string!
                                              (HttpOnly flag blocked script access)

  [ Attacker launches CSRF Link ] ── Cross-site Request ──> [ target.com/transfer ]
                                                                   │
                                                                   ▼
                                                       Cookie is WITHHELD!
                                              (SameSite=Strict flag blocked cookie payload)
```

## Real-World Example
Consider storing a session ID in a cookie. You configure the cookie with: `res.cookie('sessionId', id, { httpOnly: true, secure: true, sameSite: 'lax' })`. This configuration prevents JavaScript from accessing the token, ensures it is only transmitted over HTTPS, and blocks it from being sent in cross-site requests, protecting the user's session from multiple attack vectors.

## Code Examples

### Cookie Configuration and Signed Cookies in Express

```javascript
// cookie-demo.js
// Dependency required: npm install express cookie-parser
const express = require('express');
const cookieParser = require('cookie-parser');

const app = express();

const COOKIE_SECRET = 'my-cryptographic-cookie-signing-secret-key';

// 1. Initialize cookie-parser middleware with a secret key for signed cookies
app.use(cookieParser(COOKIE_SECRET));

// 2. Setting secure cookies
app.get('/api/set-session', (req, res) => {
  // Set a standard secure session cookie
  res.cookie('standard_session', 'session-data-abc', {
    maxAge: 3600000,   // Expires in 1 hour (in milliseconds)
    httpOnly: true,    // Protects against XSS attacks
    secure: false,     // Set to 'true' in production (requires HTTPS)
    sameSite: 'lax',   // Protects against CSRF attacks
    path: '/'          // Accessible across all application paths
  });

  // Set a signed cookie to prevent client-side tampering
  res.cookie('user_tier', 'premium', {
    maxAge: 3600000,
    httpOnly: true,
    sameSite: 'lax',
    signed: true       // Enables cryptographic signature
  });

  res.send('Secure session and signed tier cookies successfully written.');
});

// 3. Reading cookies
app.get('/api/get-session', (req, res) => {
  // Read standard cookies
  const standardSession = req.cookies.standard_session;
  
  // Read signed cookies (automatically verified and decrypted)
  // If the client modified the cookie value, it will not appear in req.signedCookies
  const userTier = req.signedCookies.user_tier;

  res.json({
    standardSession,
    userTier,
    tampered: req.cookies.user_tier ? 'Yes (Value was not signed or signature check failed)' : 'No'
  });
});

// 4. Clearing cookies
app.get('/api/logout', (req, res) => {
  res.clearCookie('standard_session', { path: '/' });
  res.clearCookie('user_tier', { path: '/' });
  res.send('Cookies cleared.');
});

app.listen(3000, () => console.log('Cookie server running on port 3000'));
```

## Best Practices
* **Always Set HttpOnly**: Set `httpOnly: true` on all session and authorization cookies to protect them from XSS extraction.
* **Force Secure in Production**: Set `secure: true` in production environments. You can configure this dynamically based on the environment: `secure: process.env.NODE_ENV === 'production'`.
* **Use SameSite=Lax/Strict**: Use `sameSite: 'lax'` or `sameSite: 'strict'` to defend against CSRF attacks.
* **Use Signed Cookies for State**: Use signed cookies (`signed: true`) when storing application state (like user settings or cart IDs) in cookies to prevent users from tampering with the values.

## Interview Questions

**Q:** What is the difference between the `Set-Cookie` and `Cookie` HTTP headers?

> **Answer:**
> `Set-Cookie` is a response header sent by the server to instruct the browser to store a cookie. `Cookie` is a request header sent by the browser to transmit stored cookies back to the server.

**Q:** What does the `HttpOnly` flag do, and what type of attack does it prevent?

> **Answer:**
> The `HttpOnly` flag prevents client-side scripts (like JavaScript's `document.cookie`) from reading the cookie. It prevents XSS (Cross-Site Scripting) attacks from stealing session tokens.

**Q:** Explain how signed cookies work in Express and how the server detects client-side tampering.

> **Answer:**
> When a signed cookie is created, Express takes the cookie value, combines it with a secret key, and generates a cryptographic hash (HMAC) signature. It appends this signature to the cookie value (e.g. `s:premium.signatureHash`).
> When the client sends the cookie back, Express extracts the value and regenerates the signature using its secret key. If the client modified the cookie value, the regenerated signature will not match the signature hash, and Express will reject the cookie, omitting it from `req.signedCookies`.

**Q:** Discuss the security implications of utilizing `SameSite=None` cookies. What browser requirements are enforced, and how does this affect authentication flows across domains?

> **Answer:**
> Setting `SameSite=None` permits browsers to send cookies on cross-site requests (e.g. when an iframe on `site-a.com` calls an API on `site-b.com`).

**Q:** Browser Requirements

> **Answer:**
> 

**Q:** Authentication Implications

> **Answer:**
> 

---
Previous : [34_JWT.md](34_JWT.md) | Index : [00_index.md](00_index.md) | Next : [36_Sessions.md](36_Sessions.md)
