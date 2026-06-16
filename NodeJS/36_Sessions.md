# Sessions

Using the default in-memory session store (`MemoryStore`) in packages like `express-session` is a common production mistake. Because it stores session data in the server's local RAM, it creates a memory leak as active users increase. Additionally, in-memory sessions are lost when the server restarts and prevent you from scaling your application across multiple servers.

### Stateful vs. Stateless Authentication
* **Stateful (Sessions)**: The server stores session data (like user ID and permissions) in a database or cache, and sends a unique Session ID to the client in a cookie. The server must query the session store for every request to check authentication.
* **Stateless (JWT)**: The server signs a token containing the user's data and sends it to the client. The client sends the token in the headers of subsequent requests. The server validates the token locally without querying a database.

### Session Exchange Flow
1. **Login**: The user submits credentials. The server verifies them, generates a unique Session ID, creates a session record in its store, and writes the Session ID to an `HttpOnly` cookie.
2. **Subsequent Requests**: The browser sends the Session ID cookie automatically. The server reads the ID, queries the session store to retrieve the user's session data, and processes the request.

## Deep Dive

### The Production Memory Leak Risk
The default storage engine for `express-session` is `MemoryStore`.
* **Memory Leak**: It stores session objects in a simple JavaScript object map in memory. Since this map does not automatically clean up expired sessions or limit memory usage, the V8 heap will eventually exhaust its RAM limits and crash under load.
* **Horizontal Scaling Failure**: If you run multiple server instances behind a load balancer, a user's session created on Server A will not exist on Server B, causing random logout errors unless you implement sticky sessions.

### Redis Session Storage
To run sessions at scale, use an external in-memory database like **Redis** as your session store:
* **Performance**: Redis runs in-memory, keeping session lookups fast (~1-2ms).
* **Decoupling**: Sessions are preserved when the application servers restart or redeploy.
* **Scaling**: Multiple server instances connect to the same Redis cluster, allowing you to scale your application horizontally.

## Visual Explanation

### Stateful Session Verification using Redis
```text
  [ Client Browser ] ─── Request with Session ID Cookie ───> [ Express Application ]
                                                                   │
                                                                   ▼ (Read cookie)
                                                             [ Session ID: sess:abc123 ]
                                                                   │
                                                                   ▼ (Fast Cache Lookup)
  [ Redis Database ] <── Query key 'sess:abc123' ───────────── [ Session Store ]
         │
         └── returns ──> Session Payload: { userId: 42, role: 'admin' }
                               │
                               ▼
                    [ Process request logic ] ──> Send HTTP Response
```

## Real-World Example
Consider an online banking platform. To ensure security, you must be able to terminate a user's session instantly if suspicious activity is detected. Using stateful sessions backed by Redis, you can delete the user's session key in Redis. The user's next request will fail session validation and force them to log in again, providing a security control that is difficult to implement with stateless JWTs.

## Code Examples

### Setting up Express Sessions with a Redis Store

```javascript
// session-server.js
// Dependencies required: npm install express express-session redis connect-redis
const express = require('express');
const session = require('express-session');
const { createClient } = require('redis');
const RedisStore = require('connect-redis').default;

const app = express();
app.use(express.json());

// 1. Initialize Redis Client
const redisClient = createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379'
});

redisClient.connect()
  .then(() => console.log('Successfully connected to Redis session store.'))
  .catch(err => console.error('Redis connection error:', err.message));

// 2. Configure Express-Session Middleware
app.use(session({
  // Use RedisStore to move session storage out of local RAM
  store: new RedisStore({
    client: redisClient,
    prefix: 'sess:' // Key prefix in Redis
  }),
  secret: process.env.SESSION_SECRET || 'my-secure-session-signing-secret',
  name: 'sid', // Cookie name to obscure implementation details
  resave: false, // Prevents saving session if unmodified
  saveUninitialized: false, // Don't create sessions for anonymous visitors
  cookie: {
    httpOnly: true,
    secure: false, // Set to true in production (requires HTTPS)
    sameSite: 'lax',
    maxAge: 1000 * 60 * 30 // Session expires after 30 minutes
  }
}));

// 3. User Login (Initialize Session)
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;

  // Validate credentials...
  if (username === 'admin' && password === 'password123') {
    // Regenerate session to prevent Session Fixation attacks
    req.session.regenerate((err) => {
      if (err) return res.status(500).json({ error: 'Session regeneration failed' });

      // Save user details to the session object
      req.session.userId = 101;
      req.session.username = 'admin';

      // Save session modifications explicitly
      req.session.save((err) => {
        if (err) return res.status(500).json({ error: 'Session save failed' });
        res.json({ message: 'Login successful' });
      });
    });
    return;
  }
  res.status(401).json({ error: 'Invalid credentials' });
});

// 4. Read Session Data
app.get('/api/profile', (req, res) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: 'Unauthorized: No active session' });
  }

  res.json({
    userId: req.session.userId,
    username: req.session.username
  });
});

// 5. Destroy Session (Logout)
app.post('/api/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) return res.status(500).json({ error: 'Logout failed' });
    res.clearCookie('sid'); // Clear browser cookie
    res.send('Logged out successfully.');
  });
});

app.listen(3000, () => console.log('Session server running on port 3000'));
```

## Best Practices
* **Never use MemoryStore in Production**: Always configure an external store (like Redis or PostgreSQL) to prevent memory leaks and support scaling.
* **Regenerate Sessions on Login**: Always call `req.session.regenerate()` when a user authenticates to protect against **Session Fixation** attacks.
* **Limit Session Expirations**: Set reasonable session timeouts (e.g. 30 minutes) and use secure cookie flags (`HttpOnly`, `Secure`, `SameSite`).
* **Save Sessions Explicitly**: Call `req.session.save()` manually after modifying session data inside redirect paths to ensure changes are written to the database before the next request arrives.

## Interview Questions

**Q:** What is the difference between stateful session-based authentication and stateless token-based authentication?

> **Answer:**
> Stateful authentication stores session data on the server (e.g., in a database or Redis) and references it via a Session ID stored in a client cookie. Stateless authentication stores claims directly inside a cryptographically signed token (JWT) held by the client, allowing the server to verify requests locally without querying a database.

**Q:** Why does the default `MemoryStore` in `express-session` cause memory leaks, and how do you resolve it?

> **Answer:**
> The default `MemoryStore` stores session data in a simple JavaScript object in the server's local RAM. It does not automatically clean up expired sessions or limit memory usage, causing memory consumption to grow indefinitely as active users increase. To resolve this, configure an external store like Redis (`connect-redis`) to manage session data.

**Q:** What is a Session Fixation attack, and how do you protect against it in a Node.js application?

> **Answer:**
> A Session Fixation attack occurs when an attacker forces a target user to use a pre-determined Session ID (e.g. by sending them a link containing a session cookie ID). If the server maintains this same Session ID after the user logs in, the attacker can use the ID to access the user's authenticated session.
> To protect against this, always regenerate the session ID (using `req.session.regenerate()`) immediately after a user authenticates, assigning them a new Session ID.

**Q:** How would you architecture a high-availability session clustering system across multiple data centers, ensuring that session data remains available if a primary Redis cluster goes down?

> **Answer:**
> To build a high-availability session system:
> 1. **Configure Redis Replication**: Deploy Redis in a Master-Replica configuration using **Redis Sentinel** or **Redis Cluster** to handle automatic failover if the primary node crashes.
> 2. **Multi-Region Sync**: Use active-passive or active-active Redis replication configurations to sync session data across data centers asynchronously.
> 3. **Fallback Database**: Configure the application's session middleware with a fallback connection strategy. If the primary Redis cluster goes down, the session store client catches the connection error and falls back to writing session data to a highly available relational database (like PostgreSQL with multi-region replicas) or a distributed NoSQL database.
> 4. **Circuit Breakers**: Implement a circuit breaker pattern to prevent connection failures from blocking server processes, keeping the application stable.

---
Previous : [35_Cookies.md](35_Cookies.md) | Index : [00_index.md](00_index.md) | Next : [37_MongoDB.md](37_MongoDB.md)
