# AWS Global Infrastructure

---

### 2. What
AWS does not just have one giant building of computers. They have a brilliant global network specifically designed for speed and disaster survival.
- **Regions:** A physical location somewhere in the world (e.g., `us-east-1` in N. Virginia, `eu-west-2` in London). 
- **Availability Zones (AZs):** Actual isolated data center buildings *inside* a Region. Each Region has at least 3 AZs (e.g., `us-east-1a`, `us-east-1b`).
- **Edge Locations:** Small, localized data centers located in almost every major city on earth used purely for rapid caching (CloudFront CDN).

✅ **Simple Analogy:**
- **Region:** A specific Country/State.
- **Availability Zone:** Specific isolated bank vaults inside that State. If vault A loses power, vault B keeps the bank running.
- **Edge Location:** Small ATMs everywhere. You don't go to the main bank to get cash quickly; you hit the local ATM.

---

### 3. Why
If a meteor hits a data center in London, your entire app is deleted if you only saved it there! By spreading your databases across multiple **Availability Zones**, you become immune to data center fires and power outages. By picking a **Region** physically close to your users, your app loads instantly instead of waiting for data to travel across the ocean.

---

### 4. How
When you create a Server (EC2) or Database in AWS, the CLI will force you to provide a `--region` flag. If you do not provide an AZ explicitly, AWS will automatically pick one for you.

---

### 5. Implementation

**Mini Exercise: Describing Infrastructure via CLI**

```bash
# 1. Let's see all the Regions AWS offers globally
aws ec2 describe-regions --output table

# 2. Let's list the specific Availability Zones (AZs) inside the London region
aws ec2 describe-availability-zones --region eu-west-2 --output table

# Output will show eu-west-2a, eu-west-2b, and eu-west-2c 
# Each is an isolated, highly secure data center building!
```

💡 **Pro Tip:** Set a default region in your CLI so you don't have to type it every time. `aws configure set region us-east-1`.

---

### 6. Steps (Choosing a Region)
When starting a project, ask yourself:
1. **Where are my users?** Put the server near them (Latency).
2. **Does the law matter?** European GDPR laws dictate German user data cannot leave Europe. You MUST choose a European region.
3. **Are you trying to be cheap?** `us-east-1` (N. Virginia) is usually the cheapest region because it is AWS's oldest and largest hub.

---

### 7. Integration

🧠 **Think Like This:**
* **Frontend (React):** You do NOT deploy frontends to a single Region! You deploy to S3, and use CloudFront (CDN) to copy it to all **Edge Locations** globally. 
* **Backend (Node.js):** You deploy this to a specific Region, spread across 2 or 3 Availability Zones for safety.

---

### 8. Impact
📌 **Real-World Scenario:** Netflix operates out of 3 primary AWS Regions. When the `us-east-1` region went down natively during a massive storm, Netflix's global traffic automatically routed to their servers in `us-west-2` seamlessly. Users never even noticed a blip!

---

### 9. Interview Questions

Q1. What is the difference between an AWS Region and an Availability Zone (AZ)?
Answer: A Region is a geographical area (like London), while an AZ is one or more discrete, physically isolated data centers within that Region with independent power and networking.

Q2. Why does AWS place multiple Availability Zones inside a single Region?
Answer: For High Availability (HA) and fault tolerance. If one data center loses power or floods, the other AZs in the same region continue to keep your application running.

Q3. What is an Edge Location in AWS?
Answer: A small, localized data center used by the CloudFront CDN to cache static content (like HTML, CSS, images) extremely close to end-users to reduce latency.

Q4. If your company strictly serves customers in Germany due to data privacy laws, how do you handle AWS regions?
Answer: You must strictly provision all EC2 instances, S3 buckets, and RDS databases in the `eu-central-1` (Frankfurt) region to comply with data residency laws like GDPR.

Q5. How are Availability Zones connected to each other?
Answer: They are connected via high-bandwidth, ultra-low-latency fiber-optic networking provided privately by AWS, allowing for fast database replication between them.

Q6. Should you deploy a critical production database inside a single Availability Zone?
Answer: No. A critical database should utilize Multi-AZ deployment, automatically keeping a synchronous standby replica in a second AZ to prevent data loss during hardware failures.

Q7. Does every AWS Region have the exact same services and features available?
Answer: No. Newer or heavily specialized AWS services are usually rolled out to massive regions like `us-east-1` first, before slowly expanding to smaller global regions.

---

### 10. Summary
* Regions are physical global locations.
* Availability Zones (AZs) are isolated data centers within a Region.
* Deploy applications across multiple AZs for fault tolerance.
* Edge Locations deliver static content incredibly fast via CDNs.

---
Prev : [01_cloud_computing_and_aws.md](./01_cloud_computing_and_aws.md) | Next : [03_compute_ec2_ubuntu_lambda.md](./03_compute_ec2_ubuntu_lambda.md)
