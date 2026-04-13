# Routing & NAT

> 📌 **File:** 10_Routing_And_NAT.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Routing determines the PATH packets take across networks. NAT (Network Address Translation) translates between private and public IP addresses. Every AWS VPC you configure uses route tables, internet gateways, and NAT gateways — all routing and NAT concepts. When your EC2 instance can't reach the internet or your database, it's almost always a routing problem.

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────────┐
│  AWS Resource            │ Routing/NAT Concept                      │
├──────────────────────────┼──────────────────────────────────────────┤
│  VPC Route Table         │ Routing rules for a subnet               │
│  Internet Gateway (IGW)  │ NAT for public EC2 ↔ internet           │
│  NAT Gateway             │ NAT for private subnet → internet        │
│  Elastic IP              │ Static public IP (1:1 NAT mapping)      │
│  VPC Peering             │ Route between two VPCs                    │
│  Transit Gateway         │ Central router for many VPCs             │
│  Default route (0.0.0.0/0)│ "Send everything else HERE"             │
│  Local route             │ "Keep VPC traffic inside VPC"            │
│  Security Group          │ NOT routing — it's firewall (allow/deny)│
└──────────────────────────┴──────────────────────────────────────────┘
```

### Your VPC Route Tables (Real Example)

```
PUBLIC Subnet Route Table:
┌───────────────────┬────────────────┬───────────────────────────────┐
│ Destination       │ Target         │ Purpose                        │
├───────────────────┼────────────────┼───────────────────────────────┤
│ 10.0.0.0/16       │ local          │ Stay inside VPC                │
│ 0.0.0.0/0         │ igw-xxxxx      │ Everything else → Internet    │
└───────────────────┴────────────────┴───────────────────────────────┘
→ EC2 in this subnet CAN be reached from internet (with public IP)
→ EC2 CAN reach internet directly

PRIVATE Subnet Route Table:
┌───────────────────┬────────────────┬───────────────────────────────┐
│ Destination       │ Target         │ Purpose                        │
├───────────────────┼────────────────┼───────────────────────────────┤
│ 10.0.0.0/16       │ local          │ Stay inside VPC                │
│ 0.0.0.0/0         │ nat-xxxxx      │ Everything else → NAT Gateway │
└───────────────────┴────────────────┴───────────────────────────────┘
→ RDS/Redis CANNOT be reached from internet (no IGW route)
→ RDS CAN reach internet via NAT (for patches, backups)
```

---

## How does it actually work?

### Routing Decision (How Routers Choose)

```
Packet arrives at router: destination = 54.23.189.12

Router checks route table (most specific match wins):
  10.0.1.0/24   → send to local interface    (doesn't match)
  10.0.0.0/16   → send to local VPC          (doesn't match)
  0.0.0.0/0     → send to Internet Gateway   (MATCH! default route)

Rule: Longest prefix match wins (/24 beats /16 beats /0)

Example:
  Packet to 10.0.1.50:
    10.0.1.0/24 ← matches (24-bit prefix)
    10.0.0.0/16 ← also matches (16-bit prefix) 
    Winner: /24 (more specific)
```

### NAT — How Your Private EC2 Reaches the Internet

```
Your EC2 (private): 10.0.10.5
Wants to: npm install express (registry.npmjs.org)

Without NAT:
  Packet: src=10.0.10.5, dst=104.16.23.35 (npmjs.org)
  Internet router: "10.0.10.5? That's a private IP. DROP."
  → Request fails

With NAT Gateway (10.0.1.20, public IP 54.23.189.99):
  1. EC2 sends: src=10.0.10.5, dst=104.16.23.35
  2. NAT rewrites: src=54.23.189.99, dst=104.16.23.35
  3. npmjs.org responds: src=104.16.23.35, dst=54.23.189.99
  4. NAT rewrites back: src=104.16.23.35, dst=10.0.10.5
  5. EC2 receives response

  EC2 can ACCESS internet but internet CANNOT access EC2!
```

### Visual Diagram

```
                         Internet
                            │
                    ┌───────┴───────┐
                    │     IGW       │   Public IP ↔ Private IP
                    └───────┬───────┘   (1:1 NAT for public EC2)
                            │
       ┌────────────────────┼────────────────────┐
       │                VPC: 10.0.0.0/16         │
       │                    │                     │
       │  ┌─────────────────┴──────────────────┐  │
       │  │    Public Subnet (10.0.1.0/24)     │  │
       │  │  ┌────────┐       ┌─────────────┐  │  │
       │  │  │  EC2   │       │ NAT Gateway │  │  │
       │  │  │ .10    │       │ .20         │  │  │
       │  │  │ ↕ IGW  │       │ ↕ IGW       │  │  │
       │  │  └────────┘       └──────┬──────┘  │  │
       │  └──────────────────────────┼─────────┘  │
       │                             │             │
       │  ┌──────────────────────────┼─────────┐  │
       │  │   Private Subnet (10.0.10.0/24)    │  │
       │  │  ┌────────┐       ┌────────┐       │  │
       │  │  │  RDS   │       │ Redis  │       │  │
       │  │  │ .5     │       │ .15    │       │  │
       │  │  │ ↕ NAT  │       │ ↕ NAT  │       │  │
       │  │  └────────┘       └────────┘       │  │
       │  └────────────────────────────────────┘  │
       └──────────────────────────────────────────┘

EC2 (.10) → Internet: Through IGW (has public IP)
RDS (.5) → Internet: Through NAT Gateway → IGW
Internet → EC2: Through IGW (if security group allows)
Internet → RDS: ❌ BLOCKED (no IGW route, no public IP)
EC2 → RDS: Direct (local route within VPC, 10.0.0.0/16 → local)
```

#### Diagram Explanation (The Internal Highway System)
Think of Routing and NAT like traffic control in a large corporate campus mapping exactly to your AWS subnets:
- **VPC & Local Routes:** Any car (EC2 instance) driving around the campus (`10.0.x.x`) can automatically navigate to any other building (RDS instance) because they share the same internal road network (`local` route).
- **Public Subnet (The Front Office):** Buildings here have direct driveways to the public road (Internet Gateway). Anyone from the public can drive in if they are allowed (via Security Groups), and cars inside can drive out to the public.
- **Private Subnet (The Vault):** Buildings here have NO driveways to the public road. If an employee (EC2) inside the Vault needs to go get lunch from the outside world (like downloading an npm package), they have to ask a secure courier (`NAT Gateway`) located up in the Front Office to go get the lunch for them and bring it back!

---

## Node.js — Diagnosing Routing Issues

```javascript
const dns = require('dns');
const http = require('http');
const net = require('net');

// ──── Check if a service is reachable ────
async function diagnoseConnection(host, port, label) {
  console.log(`\n── Diagnosing: ${label} (${host}:${port}) ──`);
  
  // Step 1: DNS resolution
  try {
    const start = Date.now();
    const { address } = await dns.promises.lookup(host);
    console.log(`  DNS: ${host} → ${address} (${Date.now() - start}ms)`);
  } catch (err) {
    console.log(`  ❌ DNS FAILED: ${err.code} — ${err.message}`);
    console.log(`  → Check: VPC DNS enabled? Security group allows UDP 53?`);
    return;
  }
  
  // Step 2: TCP connection
  return new Promise((resolve) => {
    const start = Date.now();
    const socket = new net.Socket();
    socket.setTimeout(5000);
    
    socket.on('connect', () => {
      console.log(`  TCP: Connected in ${Date.now() - start}ms ✅`);
      console.log(`  → Routing is working!`);
      socket.destroy();
      resolve(true);
    });
    
    socket.on('timeout', () => {
      console.log(`  ❌ TCP TIMEOUT after 5s`);
      console.log(`  → Check: Route table, NAT Gateway, Security Group inbound`);
      socket.destroy();
      resolve(false);
    });
    
    socket.on('error', (err) => {
      console.log(`  ❌ TCP ERROR: ${err.code}`);
      if (err.code === 'ECONNREFUSED') {
        console.log(`  → Port ${port} not listening (service down?)`);
      } else if (err.code === 'EHOSTUNREACH') {
        console.log(`  → No route to host (check route table)`);
      } else if (err.code === 'ENETUNREACH') {
        console.log(`  → Network unreachable (check IGW/NAT)`);
      }
      resolve(false);
    });
    
    socket.connect(port, host);
  });
}

// Diagnose all connections
(async () => {
  await diagnoseConnection('localhost', 3000, 'Local Express');
  await diagnoseConnection('cluster0.xxxxx.mongodb.net', 27017, 'MongoDB Atlas');
  await diagnoseConnection('my-cache.xxxxx.cache.amazonaws.com', 6379, 'Redis');
  await diagnoseConnection('my-db.xxxxx.rds.amazonaws.com', 5432, 'PostgreSQL RDS');
  await diagnoseConnection('google.com', 443, 'Internet (Google)');
})();
```

---

## Common Mistakes

### ❌ Private Subnet Without NAT Gateway

```
Problem: EC2 in private subnet can't run npm install or reach external APIs.

EC2 (10.0.10.5) → npm install express → TIMEOUT
Route table: 0.0.0.0/0 → ??? (no target!)

Fix: Add NAT Gateway in public subnet, add route:
  0.0.0.0/0 → nat-gateway-id

⚠️ NAT Gateway costs ~$32/month + data processing fees
For dev environments: use public subnet instead (cheaper)
```

### ❌ Wrong Route Table Association

```
Problem: New subnet uses VPC's main route table (no IGW route)

Every VPC has a "main" route table (private by default).
New subnets use the main table unless explicitly associated.

Fix: Always explicitly associate subnets with the correct route table.
Don't rely on the main route table for public subnets.
```

---

## Practice Exercises

### Exercise 1: Route Table Design
Design route tables for a VPC with: 2 public subnets, 2 private subnets, 1 NAT Gateway. Show which route table associates with which subnet.

### Exercise 2: Connectivity Debugging
Your EC2 can ping `10.0.10.5` (RDS) but not connect on port 5432. Is it routing or security group? How do you determine which?

### Exercise 3: traceroute Analysis
Run `traceroute google.com` from your machine. Identify your router, ISP, and the point where traffic enters Google's network.

---

## Interview Q&A

**Q1: What is the difference between an Internet Gateway and a NAT Gateway?**
> Internet Gateway provides 1:1 NAT — instances with public IPs can be reached from the internet. NAT Gateway provides many:1 NAT — private instances share NAT's public IP for outbound traffic only. IGW enables inbound + outbound; NAT enables outbound only.

**Q2: How does routing work in AWS VPCs?**
> Each subnet is associated with a route table. The table has rules: destination CIDR → target. `local` keeps traffic within VPC. `igw-xxx` routes to internet. `nat-xxx` routes through NAT. Most specific match wins (/24 over /16 over /0).

**Q3: Why should databases be in private subnets?**
> No route to IGW means no inbound internet traffic can reach them, even if security groups are misconfigured. Defense in depth: security group + no route + private IP = triple protection.

**Q4: What is the AWS NAT Gateway idle timeout problem?**
> NAT Gateway has a 350-second idle timeout for TCP connections. If a database connection is idle > 350s, NAT silently drops the mapping. Next query fails with ECONNRESET. Fix: TCP keep-alive < 350 seconds on database connections.

**Q5: What is VPC Peering and when would you use it?**
> Connects two VPCs so instances can communicate using private IPs. Used for: multi-account architectures, shared services (logging, monitoring), cross-region databases. Routes must be added in both VPCs. No transitive peering — for that, use Transit Gateway.


Prev : [09 TLS SSL Handshake](./09_TLS_SSL_Handshake.md) | Index: [0 Index](./0_Index.md) | Next : [11 Load Balancing](./11_Load_Balancing.md)
