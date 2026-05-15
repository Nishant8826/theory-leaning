# Reverse Proxy Nginx

## Why This Exists
In a production environment, you rarely expose your application containers (like Node.js, Python, or Go) directly to the internet. Doing so creates security vulnerabilities and limits your ability to scale. 

Nginx acts as a **Reverse Proxy**—a secure gateway that sits in front of your application containers. It accepts incoming traffic from the internet and forwards it to the appropriate container. It handles heavy lifting like SSL termination (HTTPS), load balancing, caching, and serving static files, allowing your application to focus purely on business logic.

## Real World Analogy
Think of Nginx as the **Receptionist at a large office building**.
- Visitors (Clients) don't just walk into the CEO's office (App Container).
- They first talk to the Receptionist (Nginx).
- The Receptionist checks their credentials (SSL), directs them to the right department (Routing), and ensures no single department gets overwhelmed with visitors (Load Balancing).

## Core Concepts
- **Reverse Proxy**: A server that sits between client devices and backend servers, forwarding client requests to the appropriate server.
- **Load Balancing**: Distributing incoming network traffic across a group of backend servers to ensure no single server bears too much demand.
- **SSL Termination**: The process of decrypting encrypted traffic at the proxy server before sending it to the backend server.
- **Upstream**: The backend servers (containers) that Nginx forwards traffic to.

## Architecture / Flow

```text
Internet
   │
   ▼
[Port 80/443]
   │
   ▼
+-------------------------+
| Nginx Container         | (Handles SSL, Gzip, Static Files)
+-------------------------+
   │
   ├───► [App Container 1] (Port 3000)
   │
   ├───► [App Container 2] (Port 3000)
   │
   └───► [App Container 3] (Port 3000)
```

## Practical Commands
```bash
# Run Nginx with default configuration
docker run -d --name my-nginx -p 8080:80 nginx:alpine

# Run Nginx with a custom configuration file
docker run -d --name custom-nginx \
  -v ./my-nginx.conf:/etc/nginx/nginx.conf:ro \
  -p 80:80 nginx:alpine

# Reload Nginx configuration without stopping the container
docker exec my-nginx nginx -s reload
```

## Hands-On Exercise
Let's set up Nginx as a reverse proxy for a simple web service.

1. Create a file named `default.conf`:
   ```nginx
   server {
       listen 80;
       server_name localhost;

       location / {
           proxy_pass http://webapp:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
2. Create a `docker-compose.yml` to tie them together:
   ```yaml
   version: '3.8'
   services:
     webapp:
       image: whalesay # A simple image for testing
       command: cowsay "Hello from the backend!"
       # In real life, this would be your Node/Python app listening on port 5000

     proxy:
       image: nginx:alpine
       ports:
         - "80:80"
       volumes:
         - ./default.conf:/etc/nginx/conf.d/default.conf:ro
       depends_on:
         - webapp
   ```

## Mini Project
**Task**: Set up Nginx as a Load Balancer for two instances of a Node.js application.

1. Create a `nginx.conf` with load balancing:
   ```nginx
   events {}
   http {
       upstream myapp {
           server app1:3000;
           server app2:3000;
       }

       server {
           listen 80;
           location / {
               proxy_pass http://myapp;
           }
       }
   }
   ```

   > [!NOTE]
   > **Configuration Breakdown:**
   > - **`events {}`**: Required by Nginx. It handles connection processing. Even if empty, it must be present in the file.
   > - **`http { ... }`**: This block holds all the configuration for handling HTTP web traffic.
   > - **`upstream myapp { ... }`**: This defines a pool of servers called `myapp`. Nginx will balance traffic between `app1:3000` and `app2:3000`. This is the core of **Load Balancing**.
   > - **`listen 80;`**: Tells Nginx to listen for incoming traffic on port 80.
   > - **`proxy_pass http://myapp;`**: Tells Nginx to forward any request matching `/` to the `myapp` pool of servers defined above.

2. Create a `docker-compose.yml`:
   ```yaml
   version: '3.8'
   services:
     app1:
       image: nginx:alpine # Using nginx as a dummy app
       command: /bin/sh -c "echo 'App 1' > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'"
     
     app2:
       image: nginx:alpine
       command: /bin/sh -c "echo 'App 2' > /usr/share/nginx/html/index.html && nginx -g 'daemon off;'"

     balancer:
       image: nginx:alpine
       ports:
         - "8080:80"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf:ro
   ```
3. Run `docker compose up -d` and refresh `localhost:8080` to see traffic alternating between App 1 and App 2.

## Real Production Usage
- **SSL Certificates**: In production, use **Certbot** (Let's Encrypt) to get free SSL certificates and configure Nginx to use them.
- **Security Headers**: Add headers like `X-Frame-Options` and `X-Content-Type-Options` to protect against common web vulnerabilities.
- **DDoS Protection**: Use Nginx `limit_req` to rate-limit requests and prevent brute-force attacks.

## Common Mistakes
- **Hardcoding container IPs**: Never use container IPs in `proxy_pass`. Always use the service name defined in Docker Compose (e.g., `http://webapp:5000`).
- **Forgetting `resolver`**: When using Nginx outside of Docker Compose (on the host) to proxy to Docker containers, you often need to specify a resolver (like `127.0.0.11` for Docker DNS).

## Debugging Guide
- **502 Bad Gateway**: This means Nginx cannot reach the backend. Check if the backend container is running and exposed on the correct port.
- **Check Nginx logs**: Use `docker logs <nginx-container-name>` to see access and error logs.

## Best Practices
- **Use Alpine Images**: `nginx:alpine` is much smaller and more secure than the standard `nginx:latest`.
- **Read-Only Volumes**: Mount configuration files as read-only (`:ro`) to prevent the container from modifying them.

## Interview Questions
1. **What is the difference between a Forward Proxy and a Reverse Proxy?**
   *Answer*: A forward proxy protects clients (e.g., a corporate proxy), while a reverse proxy protects servers (e.g., Nginx in front of an app).
2. **How does Nginx handle load balancing?**
   *Answer*: By using the `upstream` directive. The default algorithm is Round Robin, but it also supports Least Connections and IP Hash.

## Summary
Nginx is the standard for reverse proxying in Docker environments. It provides security, scalability, and performance benefits, acting as the front door for your microservices architecture.

---
Prev: [Index](../00_index.md) | Index: [Index](../00_index.md) | Next: [02_redis_mysql_mongodb_containers.md](./02_redis_mysql_mongodb_containers.md)
