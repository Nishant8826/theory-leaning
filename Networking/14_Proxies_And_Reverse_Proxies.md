# Proxies & Reverse Proxies

> 📌 **File:** 14_Proxies_And_Reverse_Proxies.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

A proxy sits between a client and a server, forwarding requests. A forward proxy acts on behalf of the client (hides the client). A reverse proxy acts on behalf of the server (hides the server). Nginx is the most common reverse proxy in your stack — it sits in front of Node.js handling TLS, compression, caching, and static files.

---

## Map it to MY STACK (CRITICAL)

```
Forward Proxy (client-side):
  Employee → Corporate Proxy → Internet
  Purpose: Filtering, caching, anonymity

Reverse Proxy (server-side):
  Internet → Nginx/ALB → Node.js (Express)
  Purpose: TLS termination, load balancing, caching, compression

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
└──────────────────────────────────────────────────────────────────┘
```

---

## Why this matters in real systems

### Why Not Expose Node.js Directly?

```
Node.js on port 3000 directly on the internet:
  ❌ Single-threaded — can't use multiple CPUs
  ❌ No TLS termination (must handle certs in code)
  ❌ Slow at serving static files
  ❌ No connection buffering (slow clients block workers)
  ❌ Crashes = complete downtime
  ❌ No rate limiting at connection level

Nginx in front of Node.js:
  ✅ Handles thousands of connections efficiently (event-driven C)
  ✅ TLS termination (OpenSSL, fast, hardware-accelerated)
  ✅ Serves static files blazingly fast (sendfile syscall)
  ✅ Buffers slow client connections (protects Node.js)
  ✅ Rate limiting, connection limits
  ✅ gzip/brotli compression
  ✅ Runs on port 80/443, proxies to Node.js on 3000
```

---

## Nginx Configuration (Production)

```nginx
# /etc/nginx/sites-available/myapp

limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=addr:10m;

upstream node_api {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;    # Cluster mode
    keepalive 64;
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

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    # Gzip compression
    gzip on;
    gzip_types application/json text/plain application/javascript text/css;

    # Static files (Next.js build output)
    location /_next/static/ {
        alias /var/www/myapp/.next/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
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

        # Timeouts & Buffering
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        proxy_buffering on;
    }

    # WebSocket → Node.js
    location /socket.io/ {
        proxy_pass http://node_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

---

## Visual Diagram — Proxy Chain

```
Request: GET https://api.myapp.com/api/products

Browser (203.0.113.50) 
  ──HTTPS──► CloudFront (CDN Edge)
  ──HTTPS──► ALB (Load Balancer - terminates TLS)
  ──HTTP───► Nginx (EC2 proxy, gzip, rate limit)
  ──HTTP───► Node.js (:3000)

Headers Node.js receives:
  Host: api.myapp.com
  X-Forwarded-For: 203.0.113.50, CloudFront-IP, ALB-IP
  X-Forwarded-Proto: https
  X-Real-IP: 203.0.113.50
```

#### Diagram Explanation (The Corporate Hierarchy)
Think of a Reverse Proxy Chain like the structural hierarchy of a large corporation handling incoming customer requests:
- **CloudFront (The International Receptionist):** Intercepts requests immediately. Serves static files on edge.
- **ALB (The Regional Manager):** Distributes incoming traffic to EC2 workers.
- **Nginx (The Department Secretary):** Verifies the request (rate limits, security checks), decompresses data (gzip), and acts as a buffer.
- **Node.js (The Worker):** Executes business logic, building a response.

---

## Node.js — Working Behind a Proxy

```javascript
const express = require('express');
const app = express();

// Trust proxy chain (CloudFront → ALB → Nginx = 3 proxies)
app.set('trust proxy', 3);

app.use((req, res, next) => {
  console.log({
    clientIP: req.ip,                     // 203.0.113.50 (real client)
    forwardedFor: req.headers['x-forwarded-for'],
    protocol: req.protocol,               // 'https'
    secure: req.secure,                   // true
    hostname: req.hostname
  });
  next();
});

// HTTPS redirect (when behind proxy)
app.use((req, res, next) => {
  if (req.headers['x-forwarded-proto'] !== 'https') {
    return res.redirect(301, `https://${req.hostname}${req.url}`);
  }
  next();
});
```

---

## Practice Exercises

### Exercise 1: Nginx Setup
Install Nginx on your EC2 instance. Configure it to reverse proxy to your Node.js app on port 3000. Test with `curl`.

### Exercise 2: Static Files
Serve your Next.js static assets through Nginx with 1-year cache headers. Verify cache headers with `curl -I`.

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

---

Prev : [13 Load Balancing](./13_Load_Balancing.md) | Index: [00 Index](./00_Index.md) | Next : [15 CDN And Caching](./15_CDN_And_Caching.md)
