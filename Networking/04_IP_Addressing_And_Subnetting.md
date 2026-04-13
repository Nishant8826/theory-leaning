# IP Addressing & Subnetting

> 📌 **File:** 04_IP_Addressing_And_Subnetting.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

IP addressing is the postal system of the internet — every device gets a unique address so packets know where to go. Subnetting divides networks into segments (like neighborhoods). You use this every time you configure an AWS VPC, set up security groups, or connect to a database.

---

## Map it to MY STACK (CRITICAL)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Where You See IP Addresses                                        │
├────────────────────────────────┬─────────────────────────────────────┤
│  Your laptop                   │ 192.168.1.50 (private, from router)│
│  EC2 instance (private)        │ 10.0.1.45 (VPC internal)           │
│  EC2 instance (public)         │ 54.23.189.12 (internet-facing)     │
│  MongoDB Atlas                 │ cluster0-shard-00-00.xxxxx.net     │
│  Redis ElastiCache             │ 10.0.2.30 (private only)           │
│  RDS PostgreSQL                │ 10.0.3.15 (private subnet)         │
│  ALB                           │ DNS name (multiple IPs behind it)  │
│  CloudFront                    │ Edge IP (varies by user location)  │
│  Route 53                      │ Maps domain → IP                   │
│  Security Group                │ Allow/deny by IP + port            │
│  VPC CIDR                      │ 10.0.0.0/16 (65,536 addresses)    │
└────────────────────────────────┴─────────────────────────────────────┘
```

### Your AWS VPC — IP Addressing in Practice

```
VPC: 10.0.0.0/16 (65,536 IPs)
├── Public Subnet A:  10.0.1.0/24 (256 IPs) → us-east-1a
│   ├── 10.0.1.10 → EC2 (Node.js API)
│   ├── 10.0.1.11 → EC2 (Node.js API #2)
│   └── 10.0.1.20 → NAT Gateway
│
├── Public Subnet B:  10.0.2.0/24 (256 IPs) → us-east-1b
│   └── 10.0.2.10 → EC2 (Node.js API #3)
│
├── Private Subnet A: 10.0.10.0/24 (256 IPs) → us-east-1a
│   ├── 10.0.10.5 → RDS PostgreSQL (primary)
│   └── 10.0.10.15 → ElastiCache Redis
│
└── Private Subnet B: 10.0.11.0/24 (256 IPs) → us-east-1b
    └── 10.0.11.5 → RDS PostgreSQL (standby)

Why this layout:
- Public subnets: Have routes to Internet Gateway (can be reached from internet)
- Private subnets: No internet gateway route (database servers, no direct access)
- Split across AZs: High availability (us-east-1a fails → 1b still works)
- /24 = 256 IPs each (251 usable — AWS reserves 5)
```

---

## Why this matters in real systems

### Scenario: "Can't connect to my database"

```
Your Node.js (10.0.1.10) → MongoDB Atlas (external):

1. Is the security group allowing outbound to port 27017? ✅
2. Is NAT gateway configured for the subnet? (If private subnet)
3. Is MongoDB Atlas whitelist including your EC2's public IP?
4. Is DNS resolving the Atlas hostname?

Your Node.js (10.0.1.10) → RDS PostgreSQL (10.0.10.5):

1. Are they in the same VPC? ✅
2. Does the RDS security group allow inbound from 10.0.1.0/24 on port 5432?
3. Is the route table routing 10.0.10.0/24 internally? (local route)
4. Is the DB listener bound to 10.0.10.5:5432?

The fix is ALWAYS about: right IP, right port, right security group, right subnet.
```

---

## How does it actually work?

### IPv4 Address Structure

```
An IPv4 address is 32 bits, written as 4 octets:

  192.168.1.50
  │   │   │ │
  │   │   │ └─ Host part (this specific device)
  │   │   └─── Subnet
  │   └─────── 
  └─────────── Network part (which network)

Binary:
  192     . 168     . 1       . 50
  11000000. 10101000. 00000001. 00110010
  
Total possible addresses: 2^32 = 4,294,967,296 (~4.3 billion)
Not enough for all devices → IPv6 (2^128 addresses)
```

### Public vs Private IP Ranges

```
┌──────────────────────────────────────────────────────────────┐
│  Range              │ Type    │ Usage                        │
├─────────────────────┼─────────┼──────────────────────────────┤
│  10.0.0.0/8         │ Private │ AWS VPC default (large)      │
│  172.16.0.0/12      │ Private │ Docker default (172.17.0.0)  │
│  192.168.0.0/16     │ Private │ Home/office routers          │
│  127.0.0.0/8        │ Loopback│ localhost (127.0.0.1)        │
│  169.254.0.0/16     │ Link-local│ Auto-assign when no DHCP   │
│  Everything else    │ Public  │ Internet-routable addresses  │
├─────────────────────┴─────────┴──────────────────────────────┤
│                                                              │
│  Private IPs cannot be reached from the internet directly.   │
│  You need NAT Gateway or Internet Gateway to translate.      │
│                                                              │
│  Your EC2: Private 10.0.1.10 → NAT → Public 54.23.189.12   │
│  Your laptop: Private 192.168.1.50 → Router → Public IP     │
└──────────────────────────────────────────────────────────────┘
```

### CIDR Notation (How Subnets Work)

```
CIDR: 10.0.1.0/24

/24 means: First 24 bits are the NETWORK, last 8 bits are HOST

10.0.1.0/24:
  Network: 10.0.1.________ (first 24 bits fixed)
  Hosts:   10.0.1.0 to 10.0.1.255
  Total:   256 addresses (2^8)
  Usable:  251 in AWS (5 reserved)

Common CIDR blocks:
┌───────────┬────────────┬──────────┬─────────────────────────┐
│  CIDR     │ Addresses  │ Usable   │ Common Use              │
├───────────┼────────────┼──────────┼─────────────────────────┤
│  /32      │ 1          │ 1        │ Single host (whitelist) │
│  /28      │ 16         │ 11       │ Small subnet            │
│  /24      │ 256        │ 251      │ Standard subnet         │
│  /20      │ 4,096      │ 4,091    │ Large subnet            │
│  /16      │ 65,536     │ 65,531   │ VPC default             │
│  /8       │ 16,777,216 │ —        │ Entire 10.x.x.x range  │
│  /0       │ All        │ —        │ "Anywhere" (0.0.0.0/0) │
└───────────┴────────────┴──────────┴─────────────────────────┘

AWS reserves 5 IPs per subnet:
  10.0.1.0   — Network address
  10.0.1.1   — VPC router
  10.0.1.2   — DNS server
  10.0.1.3   — Reserved for future use
  10.0.1.255 — Broadcast address
```

### Subnet Calculation Example

```
You need to design a VPC with:
  - 2 public subnets (web servers)
  - 2 private subnets (databases)
  - Room for future expansion

VPC CIDR: 10.0.0.0/16 (65,536 IPs total)

  Public A:  10.0.1.0/24   → 251 usable IPs (us-east-1a)
  Public B:  10.0.2.0/24   → 251 usable IPs (us-east-1b)
  Private A: 10.0.10.0/24  → 251 usable IPs (us-east-1a)  
  Private B: 10.0.11.0/24  → 251 usable IPs (us-east-1b)
  Reserved:  10.0.20.0/24+ → Future subnets

Used: 4 × 256 = 1,024 IPs
Remaining: 64,512 IPs for future subnets

Why /24 per subnet?
  - 251 usable addresses per subnet
  - Enough for most applications
  - Clean, easy-to-understand layout
  - Can always add more subnets later
```

---

## Visual Diagram — VPC Networking

```
                    Internet
                       │
               ┌───────┴───────┐
               │ Internet      │
               │ Gateway (IGW) │
               └───────┬───────┘
                       │
    ┌──────────────────┼──────────────────┐
    │              VPC: 10.0.0.0/16       │
    │                  │                  │
    │    ┌─────────────┼─────────────┐    │
    │    │  Public Subnet            │    │
    │    │  10.0.1.0/24              │    │
    │    │  ┌─────┐    ┌─────┐      │    │
    │    │  │EC2  │    │EC2  │      │    │
    │    │  │.10  │    │.11  │      │    │
    │    │  └─────┘    └─────┘      │    │
    │    └───────────────────────────┘    │
    │              │ (internal routing)   │
    │    ┌─────────┼─────────────────┐    │
    │    │  Private Subnet           │    │
    │    │  10.0.10.0/24             │    │
    │    │  ┌─────┐    ┌─────┐      │    │
    │    │  │RDS  │    │Redis│      │    │
    │    │  │.5   │    │.15  │      │    │
    │    │  └─────┘    └─────┘      │    │
    │    └───────────────────────────┘    │
    │                                    │
    └────────────────────────────────────┘

EC2 (10.0.1.10) → RDS (10.0.10.5): Same VPC, routed internally
EC2 (10.0.1.10) → Internet: Through IGW (public IP mapped via NAT)
RDS (10.0.10.5) → Internet: ❌ No route (private subnet, no IGW)
Internet → RDS: ❌ Blocked (private subnet + security group)
```

#### Diagram Explanation (The AWS Neighborhood)
Think of a VPC exactly like planning a gated neighborhood:

- **The VPC (The Property Line):** Defined by `10.0.0.0/16`, this is the grand piece of land AWS gives you. It's totally private by default.
- **Internet Gateway (The Front Gate):** The only physical way out to the public internet. Nothing gets in or out without passing through this.
- **Public Subnet (The Front Lawn):** Because this subnet (e.g. `10.0.1.0/24`) is explicitly connected to the Internet Gateway, the EC2 instances inside it have public internet access. This is where your load balancers or public web servers live.
- **Private Subnet (The Safe Room):** Notice that the private subnet (`10.0.10.0/24`) has absolutely no line connecting it to the Internet Gateway. Your RDS (Database) and Redis live here. A hacker cannot reach them because there is literally no physical path from the internet. Only your web servers in the public subnet know the internal "hallways" to reach the safe room.

---

## Commands & Debugging Tools

```bash
# Your machine's IP configuration
ipconfig /all                    # Windows
ifconfig                         # Mac/Linux
ip addr show                     # Linux (modern)

# Your public IP (as seen by the internet)
curl https://ifconfig.me
curl https://api.ipify.org

# Test if an IP is reachable
ping 10.0.1.10                   # ICMP echo
ping -c 4 8.8.8.8               # Google DNS (test internet connectivity)

# Check routing table
route print                      # Windows
ip route show                    # Linux
netstat -rn                      # Mac

# Calculate subnet
ipcalc 10.0.1.0/24              # Linux tool — shows range, broadcast, etc.

# AWS CLI: Describe VPC subnets
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-xxxxx"
aws ec2 describe-instances --query "Reservations[].Instances[].{ID:InstanceId,IP:PrivateIpAddress,Public:PublicIpAddress}"
```

---

## Node.js Implementation

```javascript
const os = require('os');
const dns = require('dns');
const net = require('net');

// ──── Get machine's IP addresses ────
function getLocalIPs() {
  const interfaces = os.networkInterfaces();
  const result = {};
  
  Object.entries(interfaces).forEach(([name, addrs]) => {
    const ipv4 = addrs.find(a => a.family === 'IPv4' && !a.internal);
    if (ipv4) {
      result[name] = {
        ip: ipv4.address,
        netmask: ipv4.netmask,
        mac: ipv4.mac,
        // Calculate network address from IP and netmask
        network: ipv4.address.split('.').map((octet, i) => 
          parseInt(octet) & parseInt(ipv4.netmask.split('.')[i])
        ).join('.')
      };
    }
  });
  
  return result;
}

console.log('Local IPs:', JSON.stringify(getLocalIPs(), null, 2));

// ──── Check CIDR membership ────
function isIPInCIDR(ip, cidr) {
  const [network, bits] = cidr.split('/');
  const mask = -1 << (32 - parseInt(bits));
  
  const ipInt = ip.split('.').reduce((acc, octet) => (acc << 8) + parseInt(octet), 0);
  const netInt = network.split('.').reduce((acc, octet) => (acc << 8) + parseInt(octet), 0);
  
  return (ipInt & mask) === (netInt & mask);
}

console.log('10.0.1.50 in 10.0.1.0/24?', isIPInCIDR('10.0.1.50', '10.0.1.0/24'));  // true
console.log('10.0.2.50 in 10.0.1.0/24?', isIPInCIDR('10.0.2.50', '10.0.1.0/24'));  // false
console.log('10.0.1.50 in 10.0.0.0/16?', isIPInCIDR('10.0.1.50', '10.0.0.0/16'));  // true

// ──── Test port reachability ────
function testPort(host, port, timeout = 3000) {
  return new Promise((resolve) => {
    const socket = new net.Socket();
    socket.setTimeout(timeout);
    
    socket.on('connect', () => {
      console.log(`✅ ${host}:${port} is reachable`);
      socket.destroy();
      resolve(true);
    });
    
    socket.on('timeout', () => {
      console.log(`⏰ ${host}:${port} timed out`);
      socket.destroy();
      resolve(false);
    });
    
    socket.on('error', (err) => {
      console.log(`❌ ${host}:${port} error: ${err.message}`);
      resolve(false);
    });
    
    socket.connect(port, host);
  });
}

// Test common services
(async () => {
  await testPort('127.0.0.1', 3000);    // Your Express server
  await testPort('8.8.8.8', 53);         // Google DNS
  await testPort('127.0.0.1', 27017);    // Local MongoDB
  await testPort('127.0.0.1', 6379);     // Local Redis
})();
```

---

## Security Groups — IP-Based Firewall Rules

```
Your EC2 Security Group (real example):

Inbound Rules:
┌────────┬──────────┬──────────────────┬────────────────────────┐
│ Port   │ Protocol │ Source           │ Purpose                │
├────────┼──────────┼──────────────────┼────────────────────────┤
│ 443    │ TCP      │ 0.0.0.0/0       │ HTTPS from anywhere    │
│ 80     │ TCP      │ 0.0.0.0/0       │ HTTP (redirect to 443) │
│ 22     │ TCP      │ 203.0.113.50/32 │ SSH from YOUR IP only  │
│ 3000   │ TCP      │ sg-alb-xxxxx    │ API from ALB only      │
└────────┴──────────┴──────────────────┴────────────────────────┘

RDS Security Group:
┌────────┬──────────┬──────────────────┬────────────────────────┐
│ 5432   │ TCP      │ 10.0.1.0/24     │ PostgreSQL from app    │
│        │          │                  │ subnet only            │
│ 5432   │ TCP      │ sg-ec2-xxxxx    │ Or reference SG by ID  │
└────────┴──────────┴──────────────────┴────────────────────────┘

0.0.0.0/0  = "anywhere" (the entire internet)
x.x.x.x/32 = "this exact IP only"
10.0.1.0/24 = "any IP in this subnet"
sg-xxxxx   = "any instance in this security group"
```

#### Diagram Explanation (The Security Bouncers)
Think of Security Groups like bouncers at different doors of a club:

- **The EC2 Bouncer (Public):** The rule `443 | TCP | 0.0.0.0/0` means "Let absolutely anyone in the world (`0.0.0.0/0`) connect to my server, but *only* if they are knocking on Port 443 (HTTPS)." This makes sense for a public web server. The SSH rule limits access *only* to your specific home IP address so nobody else can hijack your terminal.
- **The RDS Bouncer (Private):** The rule `5432 | TCP | 10.0.1.0/24` means "Only let traffic into my database if it is coming from the `10.0.1.x` subnet." Even better, you can say `sg-ec2-xxxxx`, meaning "Only let traffic in if the bouncer at the EC2 door specifically approved them first."

---

## Common Mistakes

### ❌ Opening 0.0.0.0/0 on Database Ports

```
❌ RDS inbound: Port 5432 from 0.0.0.0/0
   → Your database is accessible from the ENTIRE internet
   → Will get brute-forced within hours

✅ RDS inbound: Port 5432 from 10.0.1.0/24 (app subnet only)
   → Only your EC2 instances can reach the database
```

### ❌ Hardcoding IP Addresses

```javascript
// ❌ Hardcoded IPs (break when infrastructure changes)
const DB_HOST = '10.0.10.5';
const REDIS_HOST = '10.0.10.15';

// ✅ Use DNS names / environment variables
const DB_HOST = process.env.DB_HOST;  // RDS endpoint DNS name
const REDIS_HOST = process.env.REDIS_HOST;  // ElastiCache endpoint
// AWS services provide DNS names that resolve to current IPs
```

### ❌ Wrong Subnet Type for Service

```
❌ Database in public subnet (directly internet-accessible)
✅ Database in private subnet (only reachable from VPC)

❌ Web server in private subnet (can't receive internet traffic)
✅ Web server in public subnet (or behind ALB in public subnet)
```

---

## Practice Exercises

### Exercise 1: Subnet Calculation
Calculate the IP range, usable addresses, and broadcast address for:
1. `10.0.5.0/24`
2. `172.16.0.0/20`
3. `192.168.1.0/28`

### Exercise 2: VPC Design
Design a VPC for an app with: 2 web servers, 1 PostgreSQL (HA), 1 Redis, 1 MongoDB (Atlas external). Define subnets, security groups, and routing.

### Exercise 3: Security Group Audit
List the security group rules for your EC2 instance. Identify: which rules are too permissive? What should be tightened?

---

## Interview Q&A

**Q1: What is the difference between public and private IP addresses?**
> Public IPs are globally unique and internet-routable. Private IPs (10.x, 172.16-31.x, 192.168.x) are used within internal networks and cannot be directly reached from the internet. NAT translates between them.

**Q2: What is CIDR notation and why is /24 common?**
> CIDR (Classless Inter-Domain Routing) specifies a network prefix length. /24 means 24 bits for network, 8 bits for hosts = 256 addresses. It's the sweet spot: enough addresses for most subnets, easy to calculate (last octet is the host), and maps cleanly to subnet masks (255.255.255.0).

**Q3: Why should databases be in private subnets?**
> Private subnets have no route to the Internet Gateway, making them unreachable from the internet. This is defense-in-depth: even if security groups are misconfigured, the database can't be reached externally. Application servers in public subnets connect internally.

**Q4: What is NAT and why do private subnets need it?**
> NAT (Network Address Translation) maps private IPs to public IPs. Private subnet instances need NAT Gateway to make outbound internet requests (npm install, API calls, updates) while remaining unreachable from inbound internet traffic.

**Q5: How do IPv4 and IPv6 differ for your applications?**
> IPv4: 32-bit, ~4.3 billion addresses, running out. IPv6: 128-bit, virtually unlimited. Most AWS services support dual-stack. Your Node.js apps work on both (`::` binds to both). IPv6 is direct (no NAT needed), which can simplify architectures but requires security group attention.


Prev : [03 TCP IP Model](./03_TCP_IP_Model.md) | Index: [0 Index](./0_Index.md) | Next : [05 DNS Deep Dive](./05_DNS_Deep_Dive.md)
