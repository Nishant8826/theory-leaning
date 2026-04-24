# 📌 Authentication and Authorization

## 🧠 Concept Explanation (Story Format)

When you check in at an airport:
1. You show your passport → Guard verifies you are who you claim to be → **Authentication** ("Are you really Alice?")
2. Guard checks your boarding pass → Verifies you have permission for this specific flight → **Authorization** ("Alice, are you allowed on Flight 101?")

In your Node.js app:
- **Authentication:** "Who is this user?" → JWT token, session, Google OAuth
- **Authorization:** "What can this user do?" → "Can they access this endpoint? Edit this post? Access admin panel?"

Both are separate concerns. Getting either wrong = security breach.

---

## 🏗️ Basic Design (Naive)

```javascript
// ❌ Using sessions stored in server memory
app.post('/login', async (req, res) => {
  const user = await db.findUser(req.body.email);
  req.session.userId = user.id; // Stored in server memory!
  // Problem: If you have 10 servers → user's session is only on ONE server
  // If load balancer routes to different server → user seems logged out!
});

// ❌ No authorization checks
app.delete('/posts/:id', async (req, res) => {
  await db.deletePost(req.params.id); // ANY logged-in user can delete ANY post!
});
```

---

## ⚡ Optimized Design

```
Authentication Flow:
1. User logs in with email + password
2. Node.js verifies credentials against DB
3. Node.js generates JWT (signed token) → returns to client
4. Client stores JWT in memory or httpOnly cookie
5. Every subsequent request includes JWT in Authorization header
6. Node.js validates JWT signature → extracts user info

JWT is STATELESS — any server can validate it without checking DB!
```

---

## 🔍 Key Components

### JWT (JSON Web Tokens)

```javascript
const jwt = require('jsonwebtoken');
const JWT_SECRET = process.env.JWT_SECRET; // Must be 256+ bit secret!

// JWT Structure: header.payload.signature
// Decoded payload: { userId: '123', email: 'alice@example.com', role: 'user', iat: 1234, exp: 1234 }

// Generate JWT
function generateTokens(userId, role) {
  const accessToken = jwt.sign(
    { userId, role },          // Payload (public data — not sensitive!)
    JWT_SECRET,                // Secret for signing
    { expiresIn: '15m' }       // Short-lived: 15 minutes
  );
  
  const refreshToken = jwt.sign(
    { userId, tokenVersion: 1 },  // Version for invalidation
    process.env.REFRESH_SECRET,
    { expiresIn: '7d' }        // Long-lived: 7 days
  );
  
  return { accessToken, refreshToken };
}

// Verify JWT (middleware)
function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  const token = authHeader.split(' ')[1];
  
  try {
    const payload = jwt.verify(token, JWT_SECRET);
    req.user = payload; // Attach user info to request
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired', code: 'TOKEN_EXPIRED' });
    }
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

### Login Flow

```javascript
app.post('/auth/login', rateLimitLoginAttempts, async (req, res) => {
  const { email, password } = req.body;
  
  // 1. Validate input
  if (!email || !password) return res.status(400).json({ error: 'Email and password required' });
  
  // 2. Find user (timing-safe: don't reveal if email exists)
  const result = await db.query('SELECT * FROM users WHERE email = $1', [email.toLowerCase()]);
  const user = result.rows[0];
  
  // 3. Verify password
  const isValid = user && await bcrypt.compare(password, user.password_hash);
  
  // 4. Return same error for both "wrong email" and "wrong password" — prevents enumeration!
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid email or password' });
  }
  
  // 5. Check if account is active
  if (user.is_banned) return res.status(403).json({ error: 'Account suspended' });
  
  // 6. Generate tokens
  const { accessToken, refreshToken } = generateTokens(user.id, user.role);
  
  // 7. Store refresh token in DB (so we can invalidate it)
  await db.query(
    'INSERT INTO refresh_tokens (user_id, token_hash, expires_at) VALUES ($1, $2, $3)',
    [user.id, await bcrypt.hash(refreshToken, 8), new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)]
  );
  
  // 8. Set refresh token as httpOnly cookie (can't be accessed by JS — XSS protection!)
  res.cookie('refreshToken', refreshToken, {
    httpOnly: true,      // Not accessible by JavaScript
    secure: true,        // HTTPS only
    sameSite: 'strict',  // CSRF protection
    maxAge: 7 * 24 * 60 * 60 * 1000  // 7 days
  });
  
  // 9. Return access token in body (short-lived, stored in memory on client)
  res.json({
    accessToken,
    user: { id: user.id, name: user.name, email: user.email, role: user.role }
  });
});

// Token refresh endpoint
app.post('/auth/refresh', async (req, res) => {
  const refreshToken = req.cookies.refreshToken;
  if (!refreshToken) return res.status(401).json({ error: 'No refresh token' });
  
  try {
    const payload = jwt.verify(refreshToken, process.env.REFRESH_SECRET);
    
    // Verify token is in DB (not revoked)
    const stored = await db.query(
      'SELECT * FROM refresh_tokens WHERE user_id = $1 AND expires_at > NOW()',
      [payload.userId]
    );
    
    // Check if current token matches any stored hash
    let tokenValid = false;
    for (const row of stored.rows) {
      if (await bcrypt.compare(refreshToken, row.token_hash)) {
        tokenValid = true;
        break;
      }
    }
    
    if (!tokenValid) return res.status(401).json({ error: 'Refresh token revoked' });
    
    // Issue new access token
    const user = await db.query('SELECT * FROM users WHERE id = $1', [payload.userId]);
    const { accessToken } = generateTokens(user.rows[0].id, user.rows[0].role);
    
    res.json({ accessToken });
  } catch (e) {
    res.status(401).json({ error: 'Invalid refresh token' });
  }
});

// Logout
app.post('/auth/logout', authenticate, async (req, res) => {
  // Revoke refresh token from DB
  await db.query('DELETE FROM refresh_tokens WHERE user_id = $1', [req.user.userId]);
  
  // Clear cookie
  res.clearCookie('refreshToken');
  
  res.json({ message: 'Logged out' });
});
```

### Role-Based Access Control (RBAC)

```javascript
// Roles: user, moderator, admin

// Authorization middleware factory
function authorize(...roles) {
  return (req, res, next) => {
    if (!req.user) return res.status(401).json({ error: 'Unauthorized' });
    
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: `Forbidden: requires role: ${roles.join(' or ')}` });
    }
    
    next();
  };
}

// Usage
app.get('/admin/users', authenticate, authorize('admin'), adminController.listUsers);
app.delete('/admin/users/:id', authenticate, authorize('admin'), adminController.deleteUser);
app.put('/posts/:id/moderate', authenticate, authorize('admin', 'moderator'), moderationController.flagPost);

// Resource-level authorization (check ownership)
function authorizeOwnership(resourceGetter) {
  return async (req, res, next) => {
    const resource = await resourceGetter(req.params.id);
    
    if (!resource) return res.status(404).json({ error: 'Not found' });
    
    if (resource.userId !== req.user.userId && req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Forbidden: not your resource' });
    }
    
    req.resource = resource; // Attach for use in handler
    next();
  };
}

app.put('/posts/:id', 
  authenticate,
  authorizeOwnership((id) => db.query('SELECT * FROM posts WHERE id = $1', [id]).then(r => r.rows[0])),
  postController.updatePost
);
```

### OAuth 2.0 / Social Login (Google, GitHub)

```javascript
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  callbackURL: `${process.env.API_URL}/auth/google/callback`
}, async (accessToken, refreshToken, profile, done) => {
  try {
    // Find or create user
    let user = await db.query(
      'SELECT * FROM users WHERE google_id = $1', [profile.id]
    );
    
    if (!user.rows[0]) {
      // First time: create account
      user = await db.query(
        'INSERT INTO users (google_id, email, name, avatar_url) VALUES ($1, $2, $3, $4) RETURNING *',
        [profile.id, profile.emails[0].value, profile.displayName, profile.photos[0].value]
      );
    }
    
    done(null, user.rows[0]);
  } catch (error) {
    done(error);
  }
}));

// Routes
app.get('/auth/google', passport.authenticate('google', { scope: ['profile', 'email'] }));

app.get('/auth/google/callback',
  passport.authenticate('google', { session: false, failureRedirect: '/login?error=auth_failed' }),
  (req, res) => {
    // Generate our own JWT for the user
    const { accessToken, refreshToken } = generateTokens(req.user.id, req.user.role);
    
    res.cookie('refreshToken', refreshToken, { httpOnly: true, secure: true, sameSite: 'strict' });
    res.redirect(`${process.env.FRONTEND_URL}?token=${accessToken}`);
    // Frontend extracts token from URL, stores in memory, removes from URL
  }
);
```

### Two-Factor Authentication (2FA)

```javascript
const speakeasy = require('speakeasy');
const qrcode = require('qrcode');

// Setup 2FA
app.post('/auth/2fa/setup', authenticate, async (req, res) => {
  const secret = speakeasy.generateSecret({
    name: `MyApp (${req.user.email})`,
    length: 32
  });
  
  // Store secret temporarily (not activated until verified)
  await redis.setex(`2fa_setup:${req.user.userId}`, 300, secret.base32);
  
  // Generate QR code for Google Authenticator
  const qrCodeUrl = await qrcode.toDataURL(secret.otpauth_url);
  
  res.json({ qrCode: qrCodeUrl, secret: secret.base32 });
});

// Verify and activate 2FA
app.post('/auth/2fa/verify', authenticate, async (req, res) => {
  const { token } = req.body;
  const secret = await redis.get(`2fa_setup:${req.user.userId}`);
  
  const verified = speakeasy.totp.verify({
    secret,
    encoding: 'base32',
    token,
    window: 1  // Allow 1 step variance (30 seconds each way)
  });
  
  if (!verified) return res.status(400).json({ error: 'Invalid 2FA token' });
  
  // Activate 2FA
  await db.query('UPDATE users SET totp_secret = $1, totp_enabled = true WHERE id = $2',
    [secret, req.user.userId]);
  await redis.del(`2fa_setup:${req.user.userId}`);
  
  res.json({ message: '2FA enabled successfully' });
});

// Login with 2FA
app.post('/auth/login', async (req, res) => {
  // ... (normal login validation) ...
  
  if (user.totp_enabled) {
    // Issue temporary token that only allows 2FA verification
    const tempToken = jwt.sign(
      { userId: user.id, pending2FA: true },
      JWT_SECRET,
      { expiresIn: '5m' }
    );
    return res.json({ requires2FA: true, tempToken });
  }
  
  // ... (issue full JWT if no 2FA) ...
});

app.post('/auth/2fa/validate', async (req, res) => {
  const { tempToken, totpToken } = req.body;
  
  const payload = jwt.verify(tempToken, JWT_SECRET);
  if (!payload.pending2FA) return res.status(400).json({ error: 'Invalid flow' });
  
  const user = await db.query('SELECT * FROM users WHERE id = $1', [payload.userId]);
  
  const verified = speakeasy.totp.verify({
    secret: user.rows[0].totp_secret,
    encoding: 'base32',
    token: totpToken,
    window: 1
  });
  
  if (!verified) return res.status(401).json({ error: 'Invalid 2FA code' });
  
  // Issue full JWT
  const { accessToken, refreshToken } = generateTokens(user.rows[0].id, user.rows[0].role);
  // ... return tokens
});
```

---

## ⚖️ Trade-offs

| JWT | Sessions (Redis) |
|-----|-----------------|
| Stateless (no DB lookup) | Stateful (DB/Redis lookup) |
| Can't invalidate before expiry | Instant invalidation |
| Self-contained | Requires central store |
| Good for microservices | Requires shared session store |
| Larger header size | Smaller cookie |
| Harder to invalidate on logout | Easy to invalidate on logout |

**Recommendation:** Use JWT with short expiry (15min) + refresh tokens (7 days) stored in DB. Best of both worlds: stateless performance + ability to revoke.

---

## 📊 Scalability Discussion

### Scaling Authentication

```
Stateless JWT: Scales perfectly!
- Any server can validate JWT (just needs the secret)
- No shared state needed
- Auth service can have multiple instances

If you need to revoke tokens:
- Keep a "token revocation list" in Redis
- Check Redis on every request (adds ~1ms)
- Or: Use short-lived tokens (15min) — compromise = max 15min exposure

Session-based auth at scale:
- Sessions stored in Redis (shared across all servers)
- Works but Redis becomes a dependency
- Use Redis Cluster for HA
```

---

## 💼 Interview Questions (WITH SOLUTIONS)

### Q1: What is the difference between authentication and authorization?

**Solution:**
- **Authentication:** Verifying WHO you are. "Are you really Alice?"
  - Mechanisms: Password + bcrypt, JWT, OAuth, biometrics, API keys
  - Question: "Who are you?"
  
- **Authorization:** Verifying WHAT you can do. "Alice, can you delete this post?"
  - Mechanisms: RBAC (role-based), ABAC (attribute-based), ownership checks
  - Question: "What are you allowed to do?"

Both must work correctly for security. A bug in authentication lets anyone in. A bug in authorization lets wrong users access wrong data.

---

### Q2: How does JWT work? How is it verified?

**Solution:**
A JWT has three parts: `header.payload.signature`

1. **Header:** Algorithm used (e.g., HS256)
2. **Payload:** Claims (userId, role, expiry) — base64 encoded, NOT encrypted!
3. **Signature:** `HMAC(header + "." + payload, secret)` — proves the token wasn't tampered with

**Verification:**
```javascript
// Server receives token from client
const token = req.headers.authorization.split(' ')[1];

// 1. Decode header + payload (anyone can do this — not secret!)
// 2. Recompute signature: HMAC(header + "." + payload, SERVER_SECRET)
// 3. If computed signature === token signature → valid!
//    If different → token was tampered with → REJECT
// 4. Check expiry (exp claim) → if expired → REJECT

const payload = jwt.verify(token, JWT_SECRET); // Does all steps automatically!
```

**Key point:** JWT payload is NOT encrypted — don't put sensitive data (passwords, credit cards) in it! It's only signed (integrity), not private.

---

### Q3: How do you handle JWT token expiry and logout?

**Solution:**
**Short-lived access tokens + long-lived refresh tokens:**

```
Access Token:  15-minute expiry → stored in JS memory
Refresh Token: 7-day expiry    → stored in httpOnly cookie

Flow:
1. Login → get both tokens
2. Every API call → use access token (fast, no DB lookup)
3. Access token expires → use refresh token to get new access token
4. Logout → delete refresh token from DB + clear cookie

Token refresh in React:
```

```javascript
// Axios interceptor to auto-refresh tokens
axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401 && error.response?.data?.code === 'TOKEN_EXPIRED') {
      try {
        // Try to get new access token
        const { data } = await axios.post('/auth/refresh', {}, { withCredentials: true });
        localStorage.setItem('accessToken', data.accessToken);
        
        // Retry the failed request with new token
        error.config.headers.Authorization = `Bearer ${data.accessToken}`;
        return axios(error.config);
      } catch (refreshError) {
        // Refresh also failed → logout
        localStorage.removeItem('accessToken');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);
```

---

### Q4: How do you implement permission-based access control (beyond just user/admin)?

**Solution:**
**RBAC (Role-Based Access Control):**
```javascript
const permissions = {
  user: ['post:read', 'post:create', 'comment:read', 'comment:create', 'profile:update:own'],
  moderator: ['post:read', 'post:create', 'post:delete', 'post:moderate', 'comment:delete', 'profile:update:own'],
  admin: ['*'] // All permissions
};

function hasPermission(user, permission) {
  const userPermissions = permissions[user.role] || [];
  return userPermissions.includes('*') || userPermissions.includes(permission);
}

// Middleware
function requirePermission(permission) {
  return (req, res, next) => {
    if (!hasPermission(req.user, permission)) {
      return res.status(403).json({ error: `Permission '${permission}' required` });
    }
    next();
  };
}

app.delete('/posts/:id', authenticate, requirePermission('post:delete'), postController.delete);
```

**ABAC (Attribute-Based Access Control — more flexible):**
```javascript
// Policies are rules evaluated at runtime
const policy = {
  canEditPost: (user, post) => {
    return user.id === post.userId || user.role === 'admin' || user.role === 'moderator';
  },
  canViewPremiumContent: (user, content) => {
    return user.subscriptionPlan === 'premium' && new Date() < new Date(user.subscriptionExpiry);
  }
};

app.put('/posts/:id', authenticate, async (req, res) => {
  const post = await db.getPost(req.params.id);
  if (!policy.canEditPost(req.user, post)) {
    return res.status(403).json({ error: 'Cannot edit this post' });
  }
  // ...
});
```

---

### Q5: What is the difference between OAuth and JWT?

**Solution:**
These are different things that work together:

- **OAuth 2.0:** A **protocol** for granting access. "Allow App X to access your Google data on your behalf." It defines the flow — redirects, authorization codes, access tokens.

- **JWT:** A **token format**. A self-contained, signed token containing claims. Can be used as the token in OAuth flows, OR independently for auth.

```
OAuth 2.0 Flow (Social Login):
1. User clicks "Login with Google"
2. Browser redirects to Google
3. User approves → Google sends authorization code
4. Your server exchanges code for Google access token
5. Your server fetches user info from Google
6. Your server creates/finds user in YOUR DB
7. Your server issues YOUR OWN JWT to the client
(Google's token is only used to get user info from Google — never sent to your API)

Your own auth (no OAuth):
1. User enters email + password
2. Your server validates credentials
3. Your server issues JWT
4. Client uses JWT for all subsequent requests
```

---

## 🧩 Practice Problems (WITH SOLUTIONS)

### Problem 1: Design the authentication system for a multi-tenant SaaS app

**Solution:**
```javascript
// Multi-tenant: Each organization has separate user spaces
// A user from Org A cannot access Org B's data!

// 1. JWT payload includes tenant context
function generateToken(userId, orgId, role) {
  return jwt.sign(
    { userId, orgId, role },  // Include orgId in every token!
    JWT_SECRET,
    { expiresIn: '15m' }
  );
}

// 2. Every DB query is scoped by orgId
app.get('/projects', authenticate, async (req, res) => {
  // ALWAYS filter by orgId — even if user provides projectId
  const projects = await db.query(
    'SELECT * FROM projects WHERE org_id = $1',
    [req.user.orgId]  // From JWT — user can't change this!
  );
  res.json(projects.rows);
});

// 3. Resource access checks include orgId
app.get('/projects/:id', authenticate, async (req, res) => {
  const project = await db.query(
    'SELECT * FROM projects WHERE id = $1 AND org_id = $2',
    [req.params.id, req.user.orgId]  // BOTH id AND org_id!
  );
  if (!project.rows[0]) return res.status(404).json({ error: 'Not found' });
  res.json(project.rows[0]);
});

// 4. Roles are per-tenant
const orgRoles = {
  owner: ['*'],
  admin: ['project:*', 'member:manage', 'billing:read'],
  member: ['project:read', 'project:create', 'task:*'],
  viewer: ['project:read', 'task:read']
};

// 5. Row-Level Security in PostgreSQL (ultimate protection)
await db.query('SET app.current_org = $1', [req.user.orgId]);
// All subsequent queries automatically filtered by RLS policy!
// Even if your Node.js code forgets to add WHERE org_id = X, DB rejects it
```

---

### Problem 2: How do you invalidate all sessions for a user (e.g., account compromise)?

**Solution:**
```javascript
// When a user's account is compromised (password breach, suspicious activity):

// Strategy 1: Token versioning
// Add tokenVersion to JWT payload and users table
// When compromised: Increment tokenVersion in DB
// Old tokens with old version → INVALID

app.post('/admin/revoke-all-sessions/:userId', authenticate, authorize('admin'), async (req, res) => {
  // Increment token version — invalidates ALL existing tokens!
  await db.query(
    'UPDATE users SET token_version = token_version + 1 WHERE id = $1',
    [req.params.userId]
  );
  
  res.json({ message: 'All sessions revoked' });
});

// In auth middleware, check token version
function authenticate(req, res, next) {
  const payload = jwt.verify(token, JWT_SECRET);
  
  // Check token version matches DB (slight DB hit but guarantees revocation)
  const user = await db.query('SELECT token_version FROM users WHERE id = $1', [payload.userId]);
  
  if (payload.tokenVersion !== user.rows[0].token_version) {
    return res.status(401).json({ error: 'Session expired, please login again' });
  }
  
  req.user = payload;
  next();
}

// Strategy 2: Refresh token revocation (simpler)
async function revokeAllSessions(userId) {
  // Delete all refresh tokens for the user
  await db.query('DELETE FROM refresh_tokens WHERE user_id = $1', [userId]);
  
  // Access tokens still valid for up to 15 minutes
  // For immediate revocation: Add userId to blocklist in Redis
  await redis.setex(`blocked_user:${userId}`, 900, '1'); // 15 min (access token lifetime)
}

// Check blocklist in middleware
const isBlocked = await redis.get(`blocked_user:${req.user.userId}`);
if (isBlocked) return res.status(401).json({ error: 'Account access suspended' });
```

---

### Navigation
**Prev:** [22_Security_Basics.md](22_Security_Basics.md) | **Index:** [00_Index.md](../00_Index.md) | **Next:** None (End of HLD) → Continue to [LLD/01_Object_Oriented_Design.md](../LLD/01_Object_Oriented_Design.md)
