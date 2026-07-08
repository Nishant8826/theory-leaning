# How The Internet Actually Works

> 📌 **File:** 02_How_The_Internet_Actually_Works.md | **Level:** Full-Stack Dev → Networking Expert

---

## What is it?

The internet is not a cloud — it is a collection of physical cables buried underground and beneath oceans, connecting computers worldwide. When your React app makes a `fetch('/api/products')` call, the request travels as physical pulses of light through these cables. Understanding this physical routing is the foundation of network engineering.

---

## Map it to MY STACK (CRITICAL)

```
Your React App (Frontend)
   │
   │  1. Resolves IP of your API using DNS (Lesson 06)
   │  2. Opens a TCP connection to that IP (Lesson 08)
   │  3. Sends HTTP GET request (Lesson 07)
   ▼
Your Node.js API (Backend)

The "Network" is everything in between.
Latency (speed) is determined by how far packets must travel through
these physical cables. 
- Tokyo to New York: ~200ms round-trip (physical limit of light in fiber).
- Your app server to your database (same AWS region): < 1ms.
```

---

## The Physical Journey of a Packet

```
┌──────────────────────────────────────────────────────────────────┐
│  The Path of an HTTP Request                                     │
├──────────────────────────────────────────────────────────────────┤
│  1. Your Laptop (Home WiFi)                                      │
│     ├── Translates data to radio waves                           │
│     └── Sends to your home router                                │
│                                                                  │
│  2. Home Router (Local Gateway)                                  │
│     ├── Converts waves to electrical signals                      │
│     └── Sends through ISP copper/fiber cable (Comcast/Verizon)   │
│                                                                  │
│  3. ISP Routing Station                                          │
│     └── Routes packet onto the global backbone fiber network     │
│                                                                  │
│  4. Undersea Trans-Oceanic Cables (if crossing continents)       │
│     └── Packets travel as pulses of light at ~120,000 miles/sec  │
│                                                                  │
│  5. AWS Data Center (us-east-1, Virginia)                        │
│     └── Direct fiber connection to AWS routers                   │
│                                                                  │
│  6. AWS Hypervisor Virtual Switch                                │
│     └── Delivers packet to your EC2 virtual machine              │
└──────────────────────────────────────────────────────────────────┘
```

#### Diagram Explanation (The Highway Analogy)
Think of packet routing exactly like driving a car across the country:
- **Local Roads:** Your home WiFi network.
- **On-Ramp:** Your home router/modem.
- **Interstate Highway:** The Tier 1 ISP fiber backbone.
- **Toll Booths:** Routers along the path that inspect the IP destination and point the car in the right direction.
- **Destination:** The AWS data center parking lot.

---

## Bandwidth vs Latency (The Water Pipe Analogy)

```
Bandwidth = Width of the pipe (how much water can flow at once)
Latency = Length of the pipe (how long it takes for one drop to travel)

For Web Developers:
  - Bandwidth determines file download speeds (e.g., loading a 5MB image).
  - Latency determines API response speed (e.g., GET /user).

Adding more servers or upgrading bandwidth does NOT improve latency.
Light cannot travel faster through glass. The only way to improve latency
is to move your servers closer to the user (using a CDN / Lesson 15).
```

---

## Commands & Diagnostics

```bash
# Test basic latency to a server (ping uses ICMP protocol)
ping google.com

# Trace the exact routers (hops) your packet visits
traceroute google.com   # Linux/Mac
tracert google.com      # Windows

# Find the owner/location of an IP address
whois 8.8.8.8
```

---

## Common Mistakes

### ❌ Ignoring Geography when choosing AWS Regions

```
❌ Deploying Node.js API in Virginia (us-east-1) and database in Oregon (us-west-2)
   Every API query makes a cross-country network trip:
   Node -> DB -> Node = ~70ms latency overhead!
   
✅ Deploy compute (Node) and data (MongoDB/RDS) in the SAME AWS region.
```

### ❌ Ping testing behind firewalls

```
❌ Checking if a server is online using ping, getting 100% packet loss, 
   and assuming the server is dead.
   Many corporate firewalls (and AWS Security Groups by default) block ICMP
   packets. The web server might be perfectly healthy on port 80/443!
```

---

## Practice Exercises

### Exercise 1: Traceroute Analysis
Run a `traceroute` to `google.com` and count how many hops (routers) your packet passes through. Identify the IP address where the packet leaves your home ISP network.

### Exercise 2: Regional Latency Test
Ping `speedtest.tokyo.linode.com` and `speedtest.newark.linode.com` from your terminal. Compare the latency (RTT) and explain the difference based on geography.

### Exercise 3: Undersea Cable Search
Visit [submarinecablemap.com](https://www.submarinecablemap.com/). Find the name of the undersea cable that connects your country/region to the rest of the global internet.

---

## Interview Q&A

**Q1: What is the difference between latency and bandwidth?**
> Latency is the time it takes for a single packet to travel from source to destination (measured in milliseconds). Bandwidth is the volume of data that can be sent over the network per second (measured in Mbps/Gbps).

**Q2: Why is the latency between London and New York never less than ~30ms?**
> The physical speed of light in fiber optic cables is ~200,000 km/s. The physical distance between London and New York is ~5,500 km. The math dictates a absolute physical limit of ~28ms for a one-way trip, plus routing overhead.

**Q3: What does a traceroute command show?**
> It lists every router (hop) a packet passes through on its path to the destination, along with the round-trip latency to each hop.

**Q4: How does a router know where to send an incoming packet?**
> Routers inspect the destination IP address in the packet header and consult their internal routing tables to find the best next hop.

**Q5: Why is it bad to run database queries across regions?**
> Cross-region latency is typically 50-200ms. If an API request makes 3 database queries sequentially, it adds 150-600ms of purely network latency overhead to the request.

---

Prev : [01 Introduction And Setup](./01_Introduction_And_Setup.md) | Index: [00 Index](./00_Index.md) | Next : [03 OSI Model Vs Real World](./03_OSI_Model_Vs_Real_World.md)
