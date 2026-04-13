# Proxies & Reverse Proxies

> 📌 **File:** 13_Proxies_And_Reverse_Proxies.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

A **proxy** sits between a client and a server, forwarding requests. A **forward proxy** acts on behalf of the client (hides the client). A **reverse proxy** acts on behalf of the server (hides the server). Nginx is the most common reverse proxy in your stack — it sits in front of Node.js handling TLS, compression, caching, and static files.

---

## Map it to MY STACK (CRITICAL)

```
Forward Proxy (client-side):
  Employee → Corporate Proxy → Internet
  Purpose: Filtering, caching, anonymity
  You rarely configure this.

Reverse Proxy (server-side):
  Internet → Nginx/ALB → Node.js (Express)
  Purpose: TLS termination, load balancing, caching, compression
  You ALWAYS configure this in production.

┌──────────────────────────────────────────────────────────────────┐
│  Your Production Setup:                                          │
│                                                                  │
│  Browser ──► CloudFront (CDN/reverse proxy)                     │
│               │                                                  │
│               ├── Static files? → Serve from S3 (cached)        │
│               │                                                  │
│               └── /api/* → ALB (reverse proxy)                  │
│                             │                                    │
│                             └── Nginx (reverse proxy on EC2)    │
│                                   │                              │
│                                   └── Node.js :3000             │
│                                                                  │
│  THREE reverse proxies in a row! Each adds value:               │
│  CloudFront: Edge caching, DDoS protection, HTTP/3             │
│  ALB: Load balancing, health checks, path routing               │
│  Nginx: Static files, gzip, rate limiting, SSL (if no ALB)     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Why this matters in real systems

### Why Not Expose Node.js Directly?

```
Node.js on port 3000 directly on the internet:

❌ Single-threaded — can't use multiple CPUs
❌ No TLS termination (must handle certs in code)
❌ Slow at serving static files (React build)
❌ No connection buffering (slow clients block workers)
❌ Crashes = complete downtime
❌ No rate limiting at connection level
❌ No gzip compression by default
❌ Runs as root to bind to port 80/443

Nginx in front of Node.js:

✅ Handles thousands of connections efficiently (event-driven C)
✅ TLS termination (OpenSSL, fast, hardware-accelerated)
✅ Serves static files blazingly fast (sendfile syscall)
✅ Buffers slow client connections (protects Node.js)
✅ Restarts Node.js if it crashes (with PM2)
✅ Rate limiting, connection limits
✅ gzip/brotli compression
✅ Runs on port 80/443, proxies to Node.js on 3000
```

---

## Nginx Configuration (Production)

```nginx
# /etc/nginx/sites-available/myapp

# Rate limiting zone
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth:10m rate=1r/s;

# Connection limiting
limit_conn_zone $binary_remote_addr zone=addr:10m;

# Upstream (your Node.js instances)
upstream node_api {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;    # PM2 cluster mode — multiple instances
    keepalive 64;              # Keep TCP connections to Node.js alive
}

# HTTP → HTTPS redirect
server {
    listen 80;
    server_name api.myapp.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name api.myapp.com;

    # TLS certificates
    ssl_certificate /etc/letsencrypt/live/api.myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.myapp.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    # Gzip compression
    gzip on;
    gzip_types application/json text/plain application/javascript text/css;
    gzip_min_length 1000;
    gzip_comp_level 6;

    # Static files (Next.js build output)
    location /_next/static/ {
        alias /var/www/myapp/.next/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    location /static/ {
        alias /var/www/myapp/public/;
        expires 30d;
        access_log off;
    }

    # API routes → Node.js
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        limit_conn addr 50;

        proxy_pass http://node_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Buffering (protects Node.js from slow clients)
        proxy_buffering on;
        proxy_buffer_size 16k;
        proxy_buffers 4 32k;
    }

    # WebSocket → Node.js
    location /socket.io/ {
        proxy_pass http://node_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400s;  # 24h for long-lived WebSocket
        proxy_send_timeout 86400s;
    }

    # Auth endpoints — stricter rate limit
    location /api/auth/ {
        limit_req zone=auth burst=5 nodelay;
        proxy_pass http://node_api;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Health check (no rate limit)
    location /health {
        proxy_pass http://node_api;
        access_log off;
    }
}
```

---

## Visual Diagram — Proxy Chain

```
Request: GET https://api.myapp.com/api/products

Browser (203.0.113.50)
  │
  │  HTTPS (TLS 1.3, HTTP/2)
  ▼
CloudFront Edge (Tokyo POP)
  │  Cache MISS for /api/* (dynamic content)
  │
  │  HTTPS (TLS 1.2)
  ▼
ALB (us-east-1)
  │  TLS terminated here
  │  Health check OK on EC2 #1 and #2
  │  Route: /api/* → Target Group
  │  Adds: X-Forwarded-For, X-Forwarded-Proto
  │
  │  HTTP (plain, inside VPC)
  ▼
Nginx (EC2, 10.0.1.10)
  │  Adds: X-Real-IP
  │  Gzip compression
  │  Rate limiting check
  │
  │  HTTP (localhost)
  ▼
Node.js (:3000)
  │  Processes request
  │  Queries MongoDB / Redis
  │  Returns JSON
  │
  Response travels back through the same chain (reversed)

Headers Node.js receives:
  Host: api.myapp.com
  X-Forwarded-For: 203.0.113.50, CloudFront-IP, ALB-IP
  X-Forwarded-Proto: https
  X-Real-IP: 203.0.113.50
  Connection: keep-alive
```

---

## Node.js — Working Behind a Proxy

```javascript
const express = require('express');
const app = express();

// ──── Trust proxy chain ────
// 'trust proxy' = trust X-Forwarded-* headers
// Set to number of proxies in chain:
// CloudFront → ALB → Nginx = 3 proxies
app.set('trust proxy', 3);

// Now req.ip returns the REAL client IP
app.use((req, res, next) => {
  console.log({
    clientIP: req.ip,                     // 203.0.113.50 (real client)
    forwardedFor: req.headers['x-forwarded-for'],  // Full proxy chain
    protocol: req.protocol,               // 'https' (from X-Forwarded-Proto)
    secure: req.secure,                   // true
    hostname: req.hostname                // api.myapp.com
  });
  next();
});

// ──── HTTPS redirect (when behind proxy) ────
app.use((req, res, next) => {
  // Don't check req.protocol directly (it's always 'http' behind Nginx)
  // Check the forwarded protocol instead
  if (req.headers['x-forwarded-proto'] !== 'https') {
    return res.redirect(301, `https://${req.hostname}${req.url}`);
  }
  next();
});

// ──── Rate limiting with real IP (behind proxy) ────
const rateLimit = require('express-rate-limit');
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  keyGenerator: (req) => {
    // req.ip already returns real client IP because trust proxy is set
    return req.ip;
  }
});
app.use('/api/', limiter);
```

---

## Proxy Caching with Nginx

```nginx
# Cache API responses at the Nginx level
proxy_cache_path /tmp/nginx_cache levels=1:2 keys_zone=api_cache:10m 
                 max_size=1g inactive=5m;

location /api/products {
    proxy_pass http://node_api;
    proxy_cache api_cache;
    proxy_cache_valid 200 60s;          # Cache 200 responses for 60s
    proxy_cache_valid 404 10s;          # Cache 404 for 10s
    proxy_cache_key $request_uri;       # Cache key = URL
    proxy_cache_bypass $http_authorization;  # Don't cache auth'd requests
    
    add_header X-Cache-Status $upstream_cache_status;
    # HIT = served from cache
    # MISS = forwarded to Node.js
    # EXPIRED = cache expired, forwarded
}
```

---

## Common Mistakes

### ❌ Not Enabling WebSocket Proxying

```nginx
# ❌ Missing Upgrade headers — WebSocket won't work through Nginx
location /socket.io/ {
    proxy_pass http://node_api;
    # WebSocket never establishes — falls back to polling
}

# ✅ Must include Connection upgrade headers
location /socket.io/ {
    proxy_pass http://node_api;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### ❌ Wrong Trust Proxy Setting

```javascript
// ❌ trust proxy = true (trusts ANY proxy)
// Attacker can spoof X-Forwarded-For header!
app.set('trust proxy', true);

// ✅ Set to exact number of proxies in your chain
app.set('trust proxy', 2);  // ALB + Nginx = 2
// or
app.set('trust proxy', 'loopback');  // Only trust localhost
```

### ❌ Not Setting Proxy Timeouts

```
Nginx default proxy_read_timeout: 60s
Node.js processes a slow query: 90s
Result: Nginx gives up at 60s → 504 Gateway Timeout

Fix: Align timeouts across the chain:
  Client timeout: 30s (AbortController)
  Nginx: 60s (proxy_read_timeout)
  ALB: 60s (idle timeout)
  Node.js: 55s (server.timeout)
  MongoDB: 30s (socketTimeoutMS)
```

---

## Practice Exercises

### Exercise 1: Nginx Setup
Install Nginx on your EC2 instance. Configure it to reverse proxy to your Node.js app on port 3000. Test with `curl`.

### Exercise 2: Static Files
Serve your Next.js static assets through Nginx with 1-year cache headers. Verify cache headers with `curl -I`.

### Exercise 3: WebSocket Proxy
Configure Nginx to proxy WebSocket connections to your Socket.IO server. Verify the transport upgrades from polling to websocket.

---

## Interview Q&A

**Q1: What is the difference between a forward proxy and a reverse proxy?**
> Forward proxy acts on behalf of the client (hides client identity, corporate filtering). Reverse proxy acts on behalf of the server (hides server topology, load balancing, TLS termination). Nginx and ALB are reverse proxies.

**Q2: Why put Nginx in front of Node.js?**
> Nginx excels at: TLS termination (hardware-accelerated), static file serving (sendfile), connection buffering (protects Node.js from slow clients), gzip compression, rate limiting, and handling thousands of concurrent connections. Node.js should focus on application logic.

**Q3: How do you get the real client IP behind multiple proxies?**
> Set `trust proxy` in Express to the number of trusted proxies. Each proxy adds to `X-Forwarded-For`. Express uses the Nth-from-right IP. Setting `trust proxy: true` is dangerous — attackers can spoof the header.

**Q4: What is proxy buffering and why does it matter?**
> Nginx buffers the full response from Node.js, then sends it to the slow client at the client's pace. Without buffering, Node.js has to wait for the slow client to receive all data, tying up a connection. Buffering frees Node.js to handle the next request immediately.

**Q5: How do you handle WebSocket connections through a reverse proxy?**
> The reverse proxy must forward the `Upgrade` and `Connection` headers for the HTTP→WebSocket upgrade. In Nginx: `proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection "upgrade"`. Also set `proxy_read_timeout` high enough for long-lived connections.


Prev : [12 Firewalls And Security](./12_Firewalls_And_Security.md) | Index: [0 Index](./0_Index.md) | Next : [14 CDN And Caching](./14_CDN_And_Caching.md)
