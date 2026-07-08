# Introduction & Setup

> 📌 **File:** 01_Introduction_And_Setup.md | **Level:** Full-Stack Dev → Networking Expert

---

## Welcome to Networking for Full-Stack Developers

As a full-stack developer, you write code that runs across networks. Your React frontend fetches data from a Node.js API, which queries a MongoDB cluster, which syncs with a Redis cache. In production, this architecture is deployed across subnets, firewalls, and load balancers.

**If you don't understand networking, you cannot build secure, high-performance, scaleable applications. You are at the mercy of connection timeouts, CORS errors, and 502 Bad Gateways.**

This curriculum bridges the gap. We skip academic theories and focus entirely on how networking applies to **your code, your databases, and your cloud deployments.**

---

## The Ultimate Networking Stack for Devs

Here is the exact network path of a request in a modern production app:

```
[User Browser] (Tokyo)
      │
      │  HTTPS (TLS 1.3) over Undersea Fiber Cables (Lesson 02, 10)
      ▼
[CloudFront CDN] (Tokyo Edge - Lesson 15)
      │
      │  Cache HIT? Return React build instantly (Lesson 15)
      │  Cache MISS? Route to US Origin
      ▼
[Application Load Balancer] (AWS us-east-1 - Lesson 12)
      │
      │  Terminates SSL, routes /api/* to private subnet
      ▼
[Nginx Reverse Proxy] (EC2 - Lesson 14)
      │
      │  Gzip compression, Rate limiting (Lesson 13)
      ▼
[Node.js Express App] (PM2 Cluster - Lesson 18, 19)
      │
      │  Processes request, queries database
      ├──► [Redis Cache] (Elasticache - Lesson 23)
      └──► [PostgreSQL / MongoDB] (Private Data Subnet - Lesson 23, 24)
```

---

## Local Development Tooling

To follow this curriculum, install these network diagnostic tools on your machine:

```bash
# macOS (using Homebrew)
brew install curl wget nmap netcat termshark

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install curl wget nmap netcat-openbsd tshark -y

# Windows (using winget)
winget install Curl.Curl
winget install Wireshark.Wireshark
winget install nmap.nmap
```

---

## Verifying Your Local Environment

Run these commands to verify your tools are installed and working:

```bash
# 1. Verify curl can fetch a web page
curl -I https://www.google.com

# 2. Check your active local IP address
# Linux/macOS
ifconfig | grep "inet "
# Windows
ipconfig

# 3. Check what port is listening on your machine (e.g. 3000)
# macOS/Linux
lsof -i :3000
# Windows
netstat -ano | findstr 3000
```

---

## Curriculum Navigation

Use the footer links in every file to navigate sequentially, or return to the [00 Index](./00_Index.md) for the master guide.

---

Prev : N/A | Index: [00 Index](./00_Index.md) | Next : [02 How The Internet Actually Works](./02_How_The_Internet_Actually_Works.md)
