# 🌐 Web Servers & Nginx: The Traffic Cop

To master Linux for web development, you must master the web server. Nginx is the industry standard for serving static sites and directing traffic.

## 🤔 What is a Reverse Proxy?
A reverse proxy sits in front of your web applications (like a Node.js Express app running on port 3000) and forwards client requests to those apps. 

*   **Why?** Security, load balancing, and performance! Nginx can serve static React/Next.js files 10x faster than Node.js can.

## 🛠️ Essential Nginx Commands
*   `sudo apt install nginx`: Install Nginx.
*   `sudo systemctl status nginx`: Check if the traffic cop is working.
*   `sudo systemctl restart nginx`: Apply new configuration changes.

## ⚙️ Basic Nginx Server Block (Config)
Nginx configurations live in `/etc/nginx/sites-available/`.
```nginx
server {
    listen 80;
    server_name mywebsite.com;

    location / {
        proxy_pass http://localhost:3000; # Forwarding to Node.js!
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
**Analogy:** Nginx is the receptionist answering the door (port 80) and directing visitors to the correct employee's desk (port 3000).

## 🧠 Core Concepts Summary
*   **What:** A high-performance HTTP web server and robust reverse proxy frequently positioned in front of Node/Python backend applications.
*   **Why:** It can independently serve millions of static assets (images, CSS, JS) at lightning speeds, freeing your dynamic Node app to purely calculate logic.
*   **How:** By intercepting port 80/443 internet traffic and proxying internal system requests dynamically utilizing defined `/etc/nginx/sites-available` blocks.
*   **Impact:** Transforms a struggling development backend into an enterprise-ready, load-balanced, and highly concurrent production ecosystem.

---
Prev: [21_linux_tips_2026.md](21_linux_tips_2026.md) | Index: [00_index.md](00_index.md) | Next: [23_storage_lvm_management.md](23_storage_lvm_management.md)
---
