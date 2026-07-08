# IP Addressing & Subnetting

> 📌 **File:** 05_IP_Addressing_And_Subnetting.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

IP (Internet Protocol) addressing is how devices are located on a network. Subnetting is the division of a large network into smaller, isolated sub-networks. In AWS, you design your VPC network topology using subnets to isolate your databases, application servers, and load balancers.

---

## Map it to MY STACK (CRITICAL)

```
Your laptop: Private IP (e.g., 192.168.1.50) assigned by home router.
Your server: Public IP (e.g., 54.23.189.12) assigned by AWS.

Inside AWS VPC (default network block: 10.0.0.0/16):
  - Public Subnet (10.0.1.0/24):  ALB, Bastion Host, NAT Gateway
  - Private Subnet (10.0.10.0/24): EC2 (Node.js API)
  - Data Subnet (10.0.20.0/24):    RDS (PostgreSQL), Redis
```

---

## IPv4 vs IPv6

```
┌──────────────────────────────────────────────────────────────────┐
│  IPv4: 32-bit address space                                      │
│  ├── Format: 4 decimal octets (e.g., 172.217.7.14)               │
│  └── Space: 4.3 billion addresses (exhausted!)                   │
│                                                                  │
│  IPv6: 128-bit address space                                     │
│  ├── Format: 8 hexadecimal blocks (e.g., 2001:db8::ff00:42:8329) │
│  └── Space: 340 undecillion addresses (infinite for practical use)│
└──────────────────────────────────────────────────────────────────┘
```

---

## CIDR Notation (Classless Inter-Domain Routing)

```
CIDR is the standard way to express an IP range:

  10.0.0.0/16
  └── Prefix (Base IP) = 10.0.0.0
  └── Subnet Mask = /16 (first 16 bits are fixed: 10.0.x.x)
  └── Total IPs = 65,536 (2^(32-16))

  10.0.1.0/24
  └── Prefix = 10.0.1.0
  └── Subnet Mask = /24 (first 24 bits fixed: 10.0.1.x)
  └── Total IPs = 256 (2^(32-24))

Rule: Larger slash number = smaller network (fewer IPs).
  /16 = 65,536 IPs (VPC scale)
  /24 = 256 IPs    (Subnet scale)
  /32 = 1 IP       (Single host - useful for security group rules!)
```

#### Diagram Explanation (The Zip Code System)
Subnetting is visually exactly like the postal zip code system:
- **`10.0.0.0/16` (The City: Chicago):** The first part of the code (10.0) is fixed. It contains 65,536 houses.
- **`10.0.1.0/24` (The Neighborhood: Loop):** The code narrows down (10.0.1). It contains 256 houses.
- **`10.0.1.15/32` (The Exact House):** The full address is locked. It refers to exactly one single house.

---

## Private vs Public IP Ranges (RFC 1918)

```
These ranges are reserved for private networks.
They are NOT routable on the public internet.

1. Class A: 10.0.0.0 - 10.255.255.255     (VPCs use this: 10.0.0.0/16)
2. Class B: 172.16.0.0 - 172.31.255.255   (Docker default: 172.17.0.0/16)
3. Class C: 192.168.0.0 - 192.168.255.255 (Home router default)

Any address outside these ranges is public (routable on the internet).
```

---

## AWS Reserved IPs (The Five Lost Addresses)

```
In AWS, every subnet (/24 has 256 IPs) loses 5 IPs to AWS management:

  - .0: Network Address
  - .1: VPC Router (default gateway)
  - .2: DNS Server (Route 53 resolver)
  - .3: Future AWS use
  - .255: Network Broadcast Address

So a /24 subnet has 251 usable IPs, not 256. Keep this in mind when designing!
```

---

## Commands & Diagnostics

```bash
# View active IP addresses (linux/mac)
ip addr show
ifconfig

# View active IP addresses (windows)
ipconfig

# Determine public IP of client
curl icanhazip.com

# Convert CIDR to IP range / check subnet details (install cidr)
cidr 10.0.1.0/24
```

---

## Common Mistakes

### ❌ Subnet CIDR Overlap

```
VPC: 10.0.0.0/16
  Subnet 1: 10.0.1.0/24
  Subnet 2: 10.0.1.0/25 (overlapping range!)
  → AWS will block this configuration.
  
Fix: Plan subnets sequentially:
  - Subnet 1: 10.0.1.0/24  (IPs: 10.0.1.0 to 10.0.1.255)
  - Subnet 2: 10.0.2.0/24  (IPs: 10.0.2.0 to 10.0.2.255)
```

### ❌ Inadequate IP headroom (/28 for server tier)

```
❌ Subnet /28 has 16 IPs (11 usable after AWS reservations).
   If your server scales during traffic spikes, you quickly run out of IPs!
   
✅ Use at least /24 (251 usable IPs) for app server tiers.
```

---

## Practice Exercises

### Exercise 1: Subnet Calculator
Use an online CIDR calculator to split a `10.0.0.0/16` block into 4 equal subnets. Document the IP ranges and masks for each.

### Exercise 2: hosts file override
Modify your local hosts file to map `dev.local` to `127.0.0.1`. Verify by running ping `dev.local`.

### Exercise 3: Inspect local subnet
Find your laptop's current IP address and subnet mask. Identify your local router gateway IP.

---

## Interview Q&A

**Q1: What does /24 mean in a CIDR block?**
> The subnet mask has 24 active network bits. The first 24 bits of the IP address are fixed (identifies the network), leaving 8 bits for host addresses (up to 256 hosts).

**Q2: Why can't we use 10.0.1.50 on the public internet?**
> It belongs to the RFC 1918 private address space. Routers on the public internet drop private IPs. They are only valid inside local networks.

**Q3: How many usable IPs are in a /28 subnet in AWS?**
> 11 usable IPs. A /28 has 16 total IPs (2^(32-28)), but AWS reserves 5 IPs for VPC routing, DNS, and broadcast.

**Q4: What is the difference between a public IP and a private IP?**
> Public IPs are unique worldwide and routable on the public internet. Private IPs are reusable, only valid within local networks (VPCs, home LANs), and require NAT to access the internet.

**Q5: What is CIDR overlap and how do you prevent it?**
> When two subnets in the same VPC are assigned ranges that share IP addresses. Prevent by planning subnet boundaries sequentially (e.g. `10.0.1.0/24`, `10.0.2.0/24`).

---

Prev : [04 TCP IP Model](./04_TCP_IP_Model.md) | Index: [00 Index](./00_Index.md) | Next : [06 DNS Deep Dive](./06_DNS_Deep_Dive.md)
