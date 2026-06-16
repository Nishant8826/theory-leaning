# Nginx

Exposing a Node.js process directly to internet traffic is a security and performance risk. Node.js is not optimized for SSL termination (which is CPU-intensive) or serving static files (which blocks the event loop with disk I/O). Placing Nginx in front of Node.js as a reverse proxy secures your application, terminates SSL certificates, caches static assets, and load-balances traffic across multiple Node instances.

### What is Nginx?
**Nginx** is a high-performance web server, reverse proxy, load balancer, and HTTP cache. It utilizes an asynchronous, event-driven architecture that allows it to handle thousands of concurrent connections with low memory usage.

### Nginx Roles in Node.js Architectures
1. **Reverse Proxy**: Acts as a gateway, receiving client requests and forwarding them to internal Node.js processes without revealing your internal network structure.
2. **SSL Termination**: Handles decryption and encryption of SSL certificates at the network boundary, freeing up Node.js CPU resources for business logic.
3. **Load Balancing**: Distributes incoming client traffic across multiple Node.js server instances (e.g. running in a cluster) using algorithms like Round-Robin.
4. **Static Asset Caching**: Serves static files (CSS, JS, images) directly from disk, bypassing Node.js completely and keeping the event loop responsive.

## Deep Dive

### Client Header Forwarding
When Nginx proxies a request to Node.js, the Node application reads the request's origin IP as `127.0.0.1` (the proxy IP) instead of the actual client's IP.
To fix this, Nginx must append client metadata headers:
* **`X-Real-IP`**: The client's physical IP address.
* **`X-Forwarded-For`**: A list of IP addresses that the request has passed through.
* **`X-Forwarded-Proto`**: The protocol used by the client (HTTP or HTTPS).

On the Node.js side, configure the web framework (e.g. `app.set('trust proxy', true)` in Express) to read these forwarded headers, enabling secure rate-limiting and logging.

## Visual Explanation

### Reverse Proxy and SSL Termination Architecture
```text
  [ Client Request ]
          │
          ▼ (HTTPS - Port 443)
  +──────────────────────────────────────────────────────────+
  | [ Nginx Gateway ]                                        |
  |   1. Decrypt SSL Certificate (SSL Termination)           |
  |   2. Serve Static files directly if path matches /public |
  |   3. Forward HTTP to Node.js upstream                    |
  +───────────────────────┬──────────────────────────────────+
                          │ (HTTP - Port 3000)
                          ▼
  +──────────────────────────────────────────────────────────+
  | [ Node.js Process ]                                      |
  |   - Executes Business Logic / Database Queries           |
  +──────────────────────────────────────────────────────────+
```

## Real-World Example
Consider an e-commerce API. When a user requests `/index.html`, Nginx serves the file directly from the filesystem cache. When the user requests `/api/products`, Nginx matches the path, acts as a reverse proxy, appends the client's IP address to the headers, and routes the request to an upstream Node.js process, optimizing performance.

## Code Examples

### Production-Ready `nginx.conf` Configuration File

```nginx
# nginx.conf
# Conceptual configuration representing a production proxy setup

user nginx;
worker_processes auto; # Match worker processes to host CPU cores
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024; # Max concurrent connections per worker
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Define Upstream Node.js application server cluster
    upstream nodejs_app {
        server 127.0.0.1:3000; # Node Instance 1
        server 127.0.0.1:3001; # Node Instance 2
        # Round-robin load balancing is enabled by default
    }

    # Redirect all HTTP traffic to HTTPS automatically
    server {
        listen 80;
        server_name api.myapp.com;
        return 301 https://$host$request_uri;
    }

    # Secure HTTPS Server Configuration
    server {
        listen 443 ssl http2;
        server_name api.myapp.com;

        # SSL Certificates Configurations (SSL Termination)
        ssl_certificate /etc/letsencrypt/live/myapp.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # 1. OPTIMIZATION: Serve static files directly, bypassing Node.js
        location /public/ {
            alias /usr/src/app/public/;
            expires 30d; # Cache static files in browser for 30 days
            add_header Cache-Control "public, no-transform";
        }

        # 2. PROXY: Forward API requests to the upstream Node.js cluster
        location / {
            proxy_pass http://nodejs_app; # Forward to upstream cluster
            
            # Configure HTTP protocol settings
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            
            # Forward client connection metadata headers
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Set timeouts to prevent slow connections from hanging
            proxy_connect_timeout 5s;
            proxy_read_timeout 60s;
        }
    }
}
```

## Best Practices
* **Expose Only the Proxy**: Never expose your Node.js application port (e.g. 3000) directly to the public internet. Configure firewall settings to allow traffic only on ports 80 (HTTP) and 443 (HTTPS) through Nginx.
* **Serve Static Files with Nginx**: Configure Nginx to serve static files (CSS, JS, images) directly from disk, keeping the Node.js event loop free for API processing.
* **Configure Header Forwarding**: Always configure header forwarding (`X-Real-IP`, `X-Forwarded-For`) in Nginx to ensure your Node.js application can log client IPs and enforce rate limits correctly.
* **Configure Connection Timeouts**: Set reasonable connection timeouts in Nginx to close idle connections quickly, protecting your servers from resource exhaustion.

## Interview Questions

**Q:** What is Nginx, and what is its role when deployed in front of Node.js?

> **Answer:**
> Nginx is a high-performance web server and reverse proxy. When deployed in front of Node.js, it acts as a gateway that routes client requests, load-balances traffic across Node instances, terminates SSL certificates, and serves static files directly, improving security and performance.

**Q:** Why should you configure Nginx to forward `X-Real-IP` and `X-Forwarded-For` headers to your Node.js application?

> **Answer:**
> When Nginx acts as a reverse proxy, it forwards requests to Node.js locally. By default, Node reads the request's origin IP as `127.0.0.1` (the proxy's local IP). Forwarding `X-Real-IP` and `X-Forwarded-For` headers ensures the Node application can identify the client's actual IP address, enabling accurate request logging and rate limiting.

**Q:** What is SSL Termination, and why is it recommended to handle it at the Nginx layer rather than inside Node.js?

> **Answer:**
> SSL Termination is the process of decrypting SSL-encrypted HTTPS traffic at the network boundary, forwarding decrypted HTTP traffic to the backend, and encrypting responses.
> It is recommended to handle it at the Nginx layer because SSL decryption is CPU-intensive. Handling encryption inside Node.js consumes CPU cycles on the single-threaded event loop, which blocks request processing. Nginx is optimized to handle SSL termination efficiently using background worker threads.

**Q:** How would you configure Nginx to handle WebSocket connections and HTTP/2 proxying concurrently, explaining the configuration directives required?

> **Answer:**
> To handle WebSockets and HTTP/2 concurrently:
> 1. **HTTP/2 Configuration**: Enable HTTP/2 on the server listener directive: `listen 443 ssl http2;`. Nginx terminates HTTP/2 and forwards standard HTTP/1.1 requests to Node.js backend.
> 2. **WebSocket Upgrade Headers**: WebSockets start as a standard HTTP request and upgrade to a TCP stream using handshake headers. Configure Nginx to forward these headers inside the proxy location block:
> ```nginx
> proxy_http_version 1.1;
> proxy_set_header Upgrade $http_upgrade;
> proxy_set_header Connection "upgrade";
> ```
> - `proxy_http_version 1.1` is required because WebSockets require HTTP/1.1 to handshake.
> - `Upgrade` and `Connection` headers tell Nginx to keep the TCP socket open, allowing two-way real-time communication between the client and Node.js.

---
Previous : [79_AWS_Deployment.md](79_AWS_Deployment.md) | Index : [00_index.md](00_index.md) | Next : [81_Reverse_Proxy.md](81_Reverse_Proxy.md)
