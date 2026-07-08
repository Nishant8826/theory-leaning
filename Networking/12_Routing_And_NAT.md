# Routing & NAT

> 📌 **File:** 12_Routing_And_NAT.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

Routing is the process of moving packets across networks from source to destination. NAT (Network Address Translation) is the mechanism that allows private network devices to share a single public IP address to access the internet. On AWS, you manage this via Route Tables and NAT Gateways.

---

## Map it to MY STACK (CRITICAL)

```
Your Home Router:
  Laptop (192.168.1.50) ──► Router (NATs to 203.0.113.50) ──► Internet

AWS VPC:
  EC2 (10.0.10.15) ──► NAT Gateway (NATs to Elastic IP) ──► Internet
  (Allows private EC2 to run "npm install" or call Stripe API)

AWS Route Table:
  Destination    │ Target
  10.0.0.0/16    │ local         (Internal VPC traffic)
  0.0.0.0/0      │ nat-xxxxxxx   (All internet traffic goes to NAT Gateway)
```

---

## Routing Internals

```
┌──────────────────────────────────────────────────────────────────┐
│  Routing Table Evaluation                                        │
├──────────────────────────────────────────────────────────────────┤
│  Rule 1: Most Specific Route Wins (Longest Prefix Match)         │
│  If destination is 10.0.10.5:                                    │
│    Route A: 10.0.0.0/16 → local                                  │
│    Route B: 10.0.10.0/24 → local                                 │
│    → Route B is chosen (more specific!)                          │
│                                                                  │
│  Rule 2: Default Route (0.0.0.0/0) is the catch-all              │
│  If destination is 8.8.8.8 (Google DNS):                         │
│    No specific subnet matches.                                   │
│    → Falls back to 0.0.0.0/0 (Internet Gateway or NAT Gateway)   │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Postal Service)
Routing is visually exactly like how the postal service routes a letter:
- **Local Route (`10.0.0.0/16`):** Handled internally. Like sending mail to an office down the hall. No stamps, no external trucks.
- **Specific Subnet Route (`10.0.10.0/24`):** Directed routing. Sending mail to a specific floor in your building.
- **Default Route (`0.0.0.0/0`):** The external mail truck. If the address isn't in your office building, throw it in the default outgoing bin to let the postal system (the internet gateway) figure it out.

---

## NAT (Network Address Translation)

```
Why we need NAT:
  IPv4 addresses are scarce. We can't give every EC2 a public IP.
  Plus, public IPs expose EC2 directly to hacker scans.
  NAT allows 100s of private EC2s to share ONE public IP.

Inside a NAT session:
  1. EC2 (10.0.10.15:48123) sends request to stripe.com (3.18.12.5:443)
  2. Packet hits NAT Gateway (public IP: 203.0.113.80)
  3. NAT Gateway translates source:
     - Old Source: 10.0.10.15:48123
     - New Source: 203.0.113.80:55000 (random source port)
     - NAT writes translation to its mapping table.
  4. stripe.com replies to 203.0.113.80:55000
  5. NAT Gateway reads table, translates back to 10.0.10.15:48123
  6. Packet delivered to EC2.

One-Way Security:
  NAT allows: Private EC2 ──► Outbound request ──► Internet ✅
  NAT blocks: Hacker on Internet ──X── Inbound attempt ──X── Private EC2 ❌
```

#### Diagram Explanation (The Corporate Mailroom Secretary)
NAT is structurally identical to a corporate mailroom secretary:
- **Sending Out:** An employee in cubicle 12 (`10.0.10.15`) wants to mail Stripe. They write the letter, but they aren't allowed to put their private desk location on the envelope. They hand it to the secretary. The secretary crosses out the private desk name, stamps the corporate headquarters address (`203.0.113.80`) and a tracking number (`55000`) on it, and mails it out.
- **Receiving In:** Stripe replies to the corporate headquarters address with tracking number `55000`. The secretary checks their ledger logbook, sees tracking number `55000` belongs to cubicle 12, and privately walks the mail directly to the employee's desk.
If a solicitor walks up to the front door and asks to speak to "whoever is at tracking number 99999", the secretary denies entry because no such active tracking session exists!

---

## NAT Gateway vs NAT Instance vs Internet Gateway

```
Internet Gateway (IGW):
  - Bi-directional translation (Inbound + Outbound)
  - Connects Public subnets to the internet
  - Scale-free, high throughput (up to 100 Gbps)

NAT Gateway:
  - Uni-directional translation (Outbound only)
  - Connects Private subnets to the internet
  - Costs ~$32/month base + $0.045/GB data processing

NAT Instance:
  - Legacy approach. Do NOT use in production.
  - Bottlenecked by single EC2 network limits.
```

---

## Commands & Diagnostics

```bash
# View route table (Linux)
ip route show
route -n

# View active NAT mappings / connections (Linux NAT host)
conntrack -L

# Test path to external resource (shows gateways)
traceroute google.com

# Check your public IP from terminal
curl ifconfig.me
```

---

## Common Mistakes

### ❌ Placing NAT Gateway in a Private Subnet

```
If NAT Gateway is in Private Subnet:
  It has no route to the Internet Gateway (IGW).
  → Private EC2 cannot access the internet!
  
Fix: ALWAYS place the NAT Gateway in a PUBLIC Subnet.
  Private Subnet → NAT Gateway (in Public Subnet) → Internet Gateway → Internet
```

### ❌ Shared Route Table for Public and Private Subnets

```
If Public and Private subnets share the same route table:
  Either both go through IGW (making private instances public!)
  Or both go through NAT (blocking public ALB traffic!)

Fix: Create separate route tables:
  - rt-public:  0.0.0.0/0 → igw-xxxxxxx
  - rt-private: 0.0.0.0/0 → nat-xxxxxxx
```

---

## Practice Exercises

### Exercise 1: Traceroute Audit
Run `traceroute` (or `tracert` on Windows) to a public website. Document how many hops occur inside your local network before reaching the ISP.

### Exercise 2: AWS Route Verification
Inspect an AWS VPC configuration. Locate the Route Tables. Identify the target for `10.0.0.0/16` and `0.0.0.0/0`.

---

## Interview Q&A

**Q1: How does a router decide where to send a packet?**
> By looking up the destination IP in its routing table and matching it using the "longest prefix match" rule. The most specific rule wins. If no specific routes match, the packet is sent to the default route (`0.0.0.0/0`).

**Q2: What is the difference between static and dynamic routing?**
> Static routing requires manual route table entries (e.g. AWS Route Tables). Dynamic routing uses protocols (OSPF, BGP) where routers automatically share route info and calculate the shortest paths.

**Q3: How does NAT mapping work?**
> When a packet leaves the private network, the NAT device replaces the private source IP and port with its own public IP and a unique source port. It records this mapping in a translation table. When a response arrives on that port, it forwards it to the private IP.

**Q4: Why does a NAT Gateway need to be in a public subnet?**
> A NAT Gateway translates traffic and routes it to the internet. To reach the internet, it must have a route to the Internet Gateway (IGW), which only exists in public subnets.

**Q5: What are the cost implications of using an AWS NAT Gateway?**
> NAT Gateways charge an hourly rate (~$32/month) plus a data processing fee (~$0.045/GB). For high data volume, this can be expensive. Best practice: use VPC endpoints (free) for internal AWS traffic (like S3 or DynamoDB) to bypass the NAT Gateway.

---

Prev : [11 IP Addressing And Subnetting](./11_IP_Addressing_And_Subnetting.md) | Index: [00 Index](./00_Index.md) | Next : [13 Load Balancing](./13_Load_Balancing.md)
