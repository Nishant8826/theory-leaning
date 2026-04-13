# Firewalls & Security

> 📌 **File:** 12_Firewalls_And_Security.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Firewalls filter network traffic based on rules — allowing or blocking connections by IP, port, protocol, and direction. In AWS, you use **Security Groups** (instance-level) and **Network ACLs** (subnet-level). Together with WAF and Shield, they form your network security layers.

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────────┐
│  AWS Security Layer     │ What It Filters      │ Scope              │
├─────────────────────────┼──────────────────────┼────────────────────┤
│  Security Group (SG)    │ IP + Port (L3/L4)    │ Per EC2/RDS/Redis  │
│  Network ACL (NACL)     │ IP + Port (L3/L4)    │ Per Subnet         │
│  AWS WAF                │ HTTP content (L7)    │ Per ALB/CloudFront │
│  AWS Shield             │ DDoS protection      │ Per account/region │
│  VPC (private subnet)   │ No internet route    │ Per subnet         │
│  IAM policies           │ API-level access      │ Per user/role      │
├─────────────────────────┴──────────────────────┴────────────────────┤
│  Defense in depth: ALL layers work together.                        │
│  Don't rely on just one layer.                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Security Groups vs Network ACLs

```
┌────────────────────┬───────────────────────┬────────────────────────┐
│                    │ Security Group         │ Network ACL            │
├────────────────────┼───────────────────────┼────────────────────────┤
│  Level             │ Instance (ENI)         │ Subnet                 │
│  State             │ Stateful              │ Stateless              │
│                    │ (return traffic auto)  │ (must allow both ways) │
│  Default           │ Deny all inbound      │ Allow all in/out       │
│  Rules             │ Allow only            │ Allow + Deny           │
│  Evaluation        │ All rules evaluated   │ Rules in order (lowest │
│                    │ together              │ number wins)           │
│  Use case          │ Primary firewall ←    │ Subnet-level backup    │
│  Changed?          │ Takes effect instantly│ Takes effect instantly │
├────────────────────┴───────────────────────┴────────────────────────┤
│  "Stateful" means: If you allow inbound on port 443,              │
│  the RESPONSE is automatically allowed out. No outbound rule needed.│
│  NACLs are stateless — you must explicitly allow both directions.  │
└─────────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Bouncer vs. The Roadblock)
- **Security Groups (The Club Bouncer):** Protects a specific building/door (your EC2 instance). SGs are **Stateful**. If the Bouncer lets a user *in* to the club, he inherently remembers their face and automatically lets their data back *out* without needing a separate rule to check their ID again.
- **Network ACLs (The Neighborhood Roadblock):** Protects the entire neighborhood (your Subnet). NACLs are **Stateless**. The police at the roadblock check IDs upon entering the neighborhood, and when that exact same car tries to leave, the police have no memory of them and must check their IDs completely from scratch again! You must explicitly configure rules for both "In" and "Out".

---

## Real-World Security Group Design

```
┌─────────────── ALB Security Group ──────────────────┐
│  Inbound:                                            │
│    443 (HTTPS) from 0.0.0.0/0     ← Anyone (HTTPS)  │
│    80 (HTTP) from 0.0.0.0/0       ← Redirect to 443 │
│  Outbound:                                           │
│    All traffic                     ← ALB to targets  │
└──────────────────────────────────────────────────────┘
            │
            ▼
┌─────────── EC2 (Node.js) Security Group ────────────┐
│  Inbound:                                            │
│    3000 from sg-alb-xxxxx         ← Only from ALB    │
│    22 from 203.0.113.50/32        ← SSH from YOUR IP │
│  Outbound:                                           │
│    443 to 0.0.0.0/0              ← HTTPS (npm, APIs) │
│    27017 to sg-mongo-xxxxx       ← MongoDB            │
│    6379 to sg-redis-xxxxx        ← Redis              │
│    5432 to sg-rds-xxxxx          ← PostgreSQL          │
└──────────────────────────────────────────────────────┘
            │
            ▼
┌─────────── RDS Security Group ──────────────────────┐
│  Inbound:                                            │
│    5432 from sg-ec2-xxxxx         ← Only from EC2    │
│  Outbound:                                           │
│    All traffic                     ← Default          │
└──────────────────────────────────────────────────────┘

Key principle: Reference security groups by ID not by IP.
If EC2 IPs change, the rules still work.
```

#### Diagram Explanation (The Russian Dolls)
Look at how these Security Groups perfectly daisy-chain together. This is the ultimate "Defense in Depth" architecture:
- The **ALB** faces the terrifying public internet (`0.0.0.0/0`) but solely accepts web traffic (ports 80/443).
- The **EC2 instances** refuse to talk to the internet whatsoever! They *only* accept traffic that possesses the exact ID of the `sg-alb` Bouncer. If a hacker somehow hits the EC2 IP directly, they are dropped instantly.
- The **RDS Database** refuses to talk to anyone except the EC2 instances (`sg-ec2`). 
Because they are linked by logical Security Group IDs instead of hardcoded IPs, AWS can autoscale your EC2 instances from 2 to 20 servers under heavy load, and the database will flawlessly accept the 18 new IPs automatically!

---

## AWS WAF (Web Application Firewall)

```javascript
// WAF inspects HTTP content (Layer 7) — what Security Groups can't see

// WAF protects against:
// ✅ SQL injection:     ' OR 1=1 --
// ✅ XSS:              <script>alert(1)</script>
// ✅ Rate limiting:     Block IPs sending > 2000 req/5min
// ✅ Geo-blocking:      Block traffic from specific countries
// ✅ Bot detection:     Block known bad bots
// ✅ Size limits:       Block oversized requests

// WAF rules example:
// Rule 1: Rate limit — max 2000 requests per 5 min per IP
// Rule 2: AWS Managed Rules — SQL injection protection
// Rule 3: AWS Managed Rules — Known bad inputs
// Rule 4: Block requests with User-Agent containing "bot"
// Rule 5: Allow everything else

// Attach WAF to: ALB, CloudFront, or API Gateway
```

---

## Node.js Application-Level Security

```javascript
const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

const app = express();

// ──── Helmet — Security headers ────
app.use(helmet());
// Sets: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection,
//       Strict-Transport-Security, Content-Security-Policy, etc.

// ──── Rate Limiting ────
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                    // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later' },
  keyGenerator: (req) => req.ip  // Rate limit by IP
});

app.use('/api/', limiter);

// Stricter limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,  // Only 5 login attempts per 15 min
  message: { error: 'Too many login attempts' }
});
app.use('/api/auth/login', authLimiter);

// ──── Request Size Limits ────
app.use(express.json({ limit: '10kb' }));  // Reject huge JSON bodies
app.use(express.urlencoded({ extended: true, limit: '10kb' }));

// ──── CORS (already covered in file 06) ────
const cors = require('cors');
app.use(cors({
  origin: ['https://myapp.com'],
  credentials: true
}));

// ──── Prevent Parameter Pollution ────
const hpp = require('hpp');
app.use(hpp());

// ──── Input Sanitization ────
const mongoSanitize = require('express-mongo-sanitize');
app.use(mongoSanitize());  // Prevents MongoDB operator injection
// Removes: { email: { $gt: "" } } → { email: "" }
```

---

## Common Attacks & Defenses

```
┌───────────────────────────────────────────────────────────────────┐
│  Attack              │ Layer │ Defense                            │
├──────────────────────┼───────┼────────────────────────────────────┤
│  DDoS (volume)       │ 3/4   │ AWS Shield, CloudFront, auto-scale│
│  DDoS (application)  │ 7     │ WAF rate limiting, CloudFront     │
│  Port scanning       │ 4     │ Security groups (deny by default) │
│  SQL injection       │ 7     │ WAF rules, parameterized queries  │
│  XSS                 │ 7     │ CSP headers (helmet), input escape│
│  Brute force login   │ 7     │ Rate limiting, account lockout    │
│  SSRF                │ 7     │ Input validation, IMDSv2          │
│  Man-in-the-middle   │ 5/6   │ TLS (HTTPS), HSTS, cert pinning  │
│  DNS poisoning       │ 7     │ DNSSEC, DoH/DoT                  │
│  Credential stuffing │ 7     │ Rate limit, CAPTCHA, MFA          │
├──────────────────────┴───────┴────────────────────────────────────┤
│  Defense in depth: WAF + Security Groups + App-level security    │
│  Don't rely on one layer. Assume each layer WILL be bypassed.   │
└───────────────────────────────────────────────────────────────────┘
```

---

## Commands & Debugging Tools

```bash
# Check what ports are open on your server
nmap -sT localhost                  # TCP port scan (localhost)
nmap -sV api.myapp.com             # Detect service versions

# Check security group effect
# From your machine:
nc -zv ec2-ip 22                   # Should work (SSH allowed)
nc -zv ec2-ip 3000                 # Should fail (only ALB allowed)
nc -zv ec2-ip 27017                # Should fail (not publicly exposed)

# Check firewall rules (local Linux)
sudo iptables -L -n                # List all rules
sudo ufw status                    # UFW status (Ubuntu)

# AWS CLI: List security group rules
aws ec2 describe-security-groups --group-ids sg-xxxxx \
  --query "SecurityGroups[0].IpPermissions[*].{Port:FromPort,Source:IpRanges[0].CidrIp}"
```

---

## Common Mistakes

### ❌ Opening Port 22 (SSH) to 0.0.0.0/0

```
❌ SSH from anywhere — bots will brute-force your server
✅ SSH from your IP only: 203.0.113.50/32
✅ Better: Use AWS Systems Manager Session Manager (no SSH port needed)
✅ Best: Use EC2 Instance Connect (temporary SSH access)
```

### ❌ Database Port Open to Internet

```
❌ Security Group: Port 27017 from 0.0.0.0/0
   Your MongoDB is a public database. Will be pwned within hours.

✅ Port 27017 from sg-ec2-xxxxx only
✅ Database in private subnet (no internet route)
✅ Use MongoDB Atlas with IP whitelist
```

### ❌ Relying Only on Security Groups

```
Security groups are necessary but insufficient:
  + Application-level attacks pass through (SQL injection, XSS)
  + No rate limiting capability
  + No content inspection

Add: WAF + helmet + rate limiting + input sanitization
```

---

## Practice Exercises

### Exercise 1: Security Group Audit
Review your EC2 security groups. Identify: any rules with 0.0.0.0/0? Any database ports open publicly? Fix them.

### Exercise 2: Rate Limiting
Implement rate limiting on your Express API. Test by sending 200 rapid requests with `autocannon`. Verify responses switch to 429 after the limit.

### Exercise 3: Security Headers
Add helmet to your Express app. Use `curl -I` to verify all security headers are present. Check your site on securityheaders.com.

---

## Interview Q&A

**Q1: What is the difference between Security Groups and NACLs?**
> Security Groups are stateful (allow responses automatically), operate per-instance, and only have allow rules. NACLs are stateless (must allow both directions), operate per-subnet, and have allow + deny rules evaluated in order. SGs are your primary tool; NACLs are a backup layer.

**Q2: How would you protect a Node.js API from DDoS attacks?**
> Layer 3/4: AWS Shield Standard (free, automatic). Layer 7: CloudFront (absorbs traffic at edge) + WAF (rate limiting per IP) + ALB (distributes load). Application: express-rate-limit, Redis-based limit for distributed servers. Auto-scaling: add instances under load.

**Q3: What is a WAF and how does it differ from a firewall?**
> Traditional firewalls (Security Groups) filter by IP/port (Layer 3/4). WAF inspects HTTP content (Layer 7) — it can detect SQL injection, XSS, enforce rate limits, block specific User-Agents, and filter by geolocation. WAF sees what Security Groups can't.

**Q4: How do you prevent SSRF (Server-Side Request Forgery) in Node.js?**
> Validate and whitelist URLs before fetching. Block requests to private IP ranges (10.x, 172.16-31.x, 192.168.x, 169.254.x). Use IMDSv2 on EC2 (requires token for metadata access). Be cautious with user-provided URLs in image processing, webhooks, etc.

**Q5: What security headers should every Express app set?**
> `Strict-Transport-Security` (force HTTPS), `X-Content-Type-Options: nosniff` (prevent MIME sniffing), `X-Frame-Options: DENY` (prevent clickjacking), `Content-Security-Policy` (prevent XSS/injection), `X-XSS-Protection` (browser XSS filter). Use `helmet` middleware for all of these.


Prev : [11 Load Balancing](./11_Load_Balancing.md) | Index: [0 Index](./0_Index.md) | Next : [13 Proxies And Reverse Proxies](./13_Proxies_And_Reverse_Proxies.md)
