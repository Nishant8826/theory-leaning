# Load Balancing

> 📌 **File:** 12_Load_Balancing.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

A load balancer distributes incoming network traffic across multiple servers (EC2 instances, ECS tasks). This prevents any single server from becoming overloaded, provides redundancy (if one server dies, traffic goes to the others), and enables zero-downtime deployments. AWS ALB (Application Load Balancer) is your primary tool.

---

## Map it to MY STACK (CRITICAL)

```
Without Load Balancer:
  Browser ──► EC2 (single Node.js instance)
  If EC2 crashes → Outage.
  If traffic spikes → Server melts.
  If deploying update → Downtime during restart.

With Application Load Balancer (ALB):
  Browser ──► ALB (stable entry point)
               ├──► EC2 Instance 1 (Node.js)
               ├──► EC2 Instance 2 (Node.js)
               └──► EC2 Instance 3 (Node.js)
  If Instance 1 dies → ALB routes to 2 and 3 (0 downtime) ✅
  If traffic spikes → Auto-scaling adds instances under ALB ✅
  If deploying → Update 1 at a time under ALB (0 downtime) ✅
```

---

## ALB vs NLB vs CLB

```
┌──────────────────────────────────────────────────────────────────┐
│  AWS Load Balancer Types                                         │
├──────────────────────────────────────────────────────────────────┤
│  ALB: Application Load Balancer (Layer 7)                        │
│  ├── Inspects HTTP headers, paths, cookies, methods              │
│  ├── Routes: /api/* → API Service, /static/* → S3/Frontend       │
│  ├── Handles TLS termination (ACM SSL certificates)              │
│  └── Use Case: Web applications, APIs, microservices (REST/WS)  │
│                                                                  │
│  NLB: Network Load Balancer (Layer 4)                            │
│  ├── Raw TCP/UDP routing (does not inspect HTTP payload)         │
│  ├── Ultra-high performance (millions of requests/second)        │
│  ├── Static IP addresses (ALB has dynamic IPs)                   │
│  └── Use Case: Real-time gaming, raw TCP sockets, VoIP           │
│                                                                  │
│  CLB: Classic Load Balancer (Legacy)                             │
│  └── Do NOT use for new projects. Legacy Layer 4/7.              │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Post Office)
Think of load balancers visually exactly like a busy Post Office sorting facility:
- **ALB (The Smart Mail sorter - Layer 7):** Inspects the actual letter inside the envelope. They read "Ah, this envelope is addressed to the billing department (`/api/billing`), I will route it to the billing clerks (Billing Target Group)".
- **NLB (The Raw Package mover - Layer 4):** Does not read the letters. They just check the weight and destination postal zip code (IP and Port) and throw the boxes onto conveyor belts at lightning speeds. They process millions of packages without caring what's inside.

---

## Key Configuration Concepts

### 1. Listeners and Rules

```
ALB listens on ports:
  - Port 80 (HTTP)  → Rules: Redirect to HTTPS (Port 443)
  - Port 443 (HTTPS) → Rules: Target Group routing

HTTP listener redirect rule (Terraform snippet):
  redirect {
    port        = "443"
    protocol    = "HTTPS"
    status_code = "HTTP_301"
  }
```

### 2. Target Groups and Routing

```
ALB routes traffic based on rules to TARGET GROUPS:

  Rule 1: Path is /api/*  → Route to tg-backend (EC2 instances :3000)
  Rule 2: Path is /ws/*   → Route to tg-websocket (EC2 instances :8080)
  Rule 3: Default (/*)    → Route to tg-frontend (S3 or Next.js EC2)

Target Group 1 (tg-backend):
  - ec2-instance-1 (10.0.1.10:3000) - Healthy
  - ec2-instance-2 (10.0.1.11:3000) - Healthy
```

### 3. Health Checks (Critical for Zero-Downtime)

```
ALB checks backend health every N seconds:

  Path: /health                 (dedicated route in your Express app)
  Interval: 30 seconds          (how often to check)
  Timeout: 5 seconds            (how long to wait for response)
  Healthy threshold: 2 checks   (mark healthy after 2 successes)
  Unhealthy threshold: 3 checks (mark unhealthy after 3 failures)

If health check fails:
  → ALB immediately stops routing traffic to that instance
  → Requests only go to remaining healthy instances
  → No user sees an error!
```

```javascript
// Express health check endpoint
app.get('/health', (req, res) => {
  // Check DB connection status
  const dbHealthy = mongoose.connection.readyState === 1;
  
  if (dbHealthy) {
    res.status(200).send('OK');
  } else {
    res.status(503).send('Database unavailable');
  }
});
```

---

## Advanced Load Balancer Patterns

### Sticky Sessions (Session Affinity)

```
Problem: User logs in, session is stored on Server 1 memory.
Next request goes to Server 2 → User is suddenly logged out!

Solution 1: Sticky Sessions (ALB-managed)
  ALB injects a cookie (AWSALB) in response.
  Browser sends cookie in subsequent requests.
  ALB reads cookie and always routes that user to Server 1.
  ❌ Hard to scale, server crash drops sessions.

Solution 2: Stateless Servers (Best Practice)
  Store session data in shared Redis cache or use JWT.
  ALB can distribute traffic randomly (Round Robin).
  Any server can handle any request.
  ✅ Scale horizontally, no sticky session issues.
```

### Connection Draining (Deregistration Delay)

```
During deployment or scale-in:
  We want to remove Server 1.
  We can't just kill it — active users might be downloading files or checking out.

Connection Draining:
  1. We tell ALB we are removing Server 1.
  2. ALB stops sending NEW requests to Server 1.
  3. ALB waits N seconds (default 300s) for active requests to finish.
  4. Once requests finish or timeout, Server 1 is safely terminated.
```

---

## Load Balancer Security

```
1. SSL/TLS Termination
   ALB handles HTTPS encryption/decryption.
   Browser ──► HTTPS ──► ALB ──► HTTP ──► EC2
   Saves CPU on EC2. Certs managed via AWS Certificate Manager (ACM).

2. Security Group Configuration (Best Practice)
   ALB Security Group:
     - Inbound: Allow 80/443 from 0.0.0.0/0 (open to world)
     - Outbound: Allow 3000 to EC2 Security Group
   
   EC2 Security Group:
     - Inbound: Allow 3000 ONLY from ALB Security Group ID!
     - Inbound: Allow 22 (SSH) from Bastion host only
   
   Nobody on the internet can connect directly to your EC2 instances.
   They MUST go through the ALB!
```

---

## Practice Exercises

### Exercise 1: Health Check Endpoint
Build a `/health` endpoint in Express that checks MongoDB connectivity. Test locally using curl.

### Exercise 2: Simulated Failure
Create a simple load balancer configuration using local Nginx (upstream). Run two instances of your Node app. Kill one instance and verify Nginx automatically routes traffic to the survivor.

### Exercise 3: AWS Terraform Setup
Write a basic Terraform block defining an ALB, a target group, a listener redirecting 80 to 443, and health check settings.

---

## Interview Q&A

**Q1: What is the difference between Layer 4 and Layer 7 load balancing?**
> Layer 4 (NLB) routes traffic based on IP and TCP/UDP ports. It is ultra-fast, handles millions of requests/sec, and is protocol-agnostic. Layer 7 (ALB) inspects the HTTP headers, URL paths, cookies, and query parameters. ALB allows routing requests to different backends based on paths (e.g. `/api/*` vs `/static/*`).

**Q2: How does an ALB achieve zero-downtime deployments?**
> Rolling updates: new instances are spun up and register with ALB. ALB checks their health. Once healthy, ALB starts routing traffic to new instances. Old instances are deregistered, connection draining waits for pending requests to finish, and old instances are terminated.

**Q3: Why should EC2 security groups only allow traffic from the ALB?**
> Direct access to EC2 bypasses the load balancer, exposing ports directly to the internet (security risk, DDoS vector, bypasses WAF). Restricting inbound access to the ALB Security Group ID ensures all traffic is filtered, encrypted, and monitored.

**Q4: What is connection draining (deregistration delay)?**
> The grace period given to a server being removed from service. ALB stops routing new requests to the instance but allows active requests to complete within the delay window (default 300 seconds) before terminating the instance.

**Q5: How do you handle session state across load-balanced servers?**
> Keep servers stateless. Do not store sessions in local memory. Store session data in a central Redis cache, or use self-contained JWT tokens signed by the server. This allows any instance under the load balancer to handle any request.

---

Prev : [11 Routing And NAT](./11_Routing_And_NAT.md) | Index: [00 Index](./00_Index.md) | Next : [13 Firewalls And Security](./13_Firewalls_And_Security.md)
