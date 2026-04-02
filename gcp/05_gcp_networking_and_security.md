# Core Networking & Security in GCP

---

### 2. What
If Compute is the "brain", Networking is the "nervous system", and Security is the "immune system".
- **VPC (Virtual Private Cloud):** A private global network for your GCP resources. It prevents hackers on the public internet from reaching your databases.
- **Load Balancing:** A traffic cop. If 1,000,000 users visit your site, the Load Balancer distributes them evenly across 50 different servers so no single server crashes.
- **Cloud CDN (Content Delivery Network):** Caches your static files (like React Javascript bundles) in 100+ cities globally so users download them locally in milliseconds.
- **IAM (Identity & Access Management):** The bouncer. It dictates *Who* is allowed to do *What* in your cloud. 

✅ **Simple Analogy:**
- **VPC:** Your house's Wi-Fi network. Strangers on the street cannot access your smart TV.
- **Load Balancer:** The manager at a grocery store directing a massive line of customers to empty checkout lanes.
- **IAM:** The VIP guest list detailing exactly which rooms each person has the key to.

---

### 3. Why
If you spin up a Cloud SQL Database and assign it a Public IP address, bots will begin attempting to crack the password 24/7. Relying exclusively on VPC ensures your Database has zero public internet footprint! Furthermore, operating without a Load Balancer practically guarantees server downtime when your app goes viral.

---

### 4. How
Security universally resolves around **Service Accounts**. A Service Account is a "Robot User". Instead of giving your personal email address permission to delete the database, you create a Service Account, give it basic read/write access, and let your backend securely use that robot's credentials.

---

### 5. Implementation

**Mini Exercise: IAM Policies**

Imagine configuring your Cloud Architecture.
1. You have a `Frontend-Web` Cloud Run app.
2. You have a `Backend-API` Cloud Run app.
3. You have a `Cloud-SQL` Database.

*Bad Security:* Giving both apps full "Admin" access to the entire cloud.
*Good Security (IAM):* 
- The `Frontend-Web` has 0 access to the Database. It is only allowed to send HTTP requests to the `Backend-API`.
- The `Backend-API` uses a specific `db-writer-account` Service Account that can only talk to Cloud SQL.

---

### 6. Steps (Securing your Cloud)
1. Navigate to IAM & Admin inside the GCP console.
2. Click "Create Service Account".
3. Grant the absolute lowest permissions required. Do not use generic "Editor" or "Owner" roles.
4. Attach this new Service Account directly to your Cloud Run server.

---

### 7. Integration

🧠 **Think Like This:**
* **React/Next.js:** Put static files behind Cloud CDN. Users fetch data from the closest Edge Node globally.
* **Node.js + Database:** Ensure Node.js connects to Cloud SQL exclusively via an internal VPC IP address to prevent external exposure.

---

### 8. Impact
📌 **Real-World Scenario:** Netflix uses CDNs to cache movies in your specific city, ensuring zero buffering. They use VPCs to ensure hackers cannot reach their core databases. They use IAM to ensure lower-level employees cannot accidentally delete global clusters.

---

### 9. Interview Questions
1. **Explain what IAM natively dictates in GCP.**
   *Answer: IAM strictly controls "Who" (Identity) has permission to do "What" (access rights) on which GCP resource.*
2. **What is the architectural difference between a Load Balancer and a VPC?**
   *Answer: A Load Balancer distributes incoming web traffic efficiently across multiple servers to prevent crashes, while a VPC provides the private, isolated internal network that those distinct servers reside on.*
3. **What is a Content Delivery Network (CDN)?**
   *Answer: CDNs cache static assets (like images and JS files) at the physical edges of Google's network near the user, drastically decreasing load speeds.*

---

### 10. Summary
* VPCs secure your internal cloud networks natively.
* Load Balancers distribute traffic safely.
* CDNs speed up React frontend assets globally.
* IAM secures which users and robots possess permissions to manage your data.

---
Prev : [04_gcp_storage_and_databases.md](./04_gcp_storage_and_databases.md) | Next : [06_google_maps_platform_intro.md](./06_google_maps_platform_intro.md)
