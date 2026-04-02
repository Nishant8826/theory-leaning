# Interview Preparation: GCP & Maps Platform

---

### 2. What
Google Cloud Platform (GCP) and Google Maps Platform are highly lucrative skills in the engineering world. Interviewers will test your understanding of Serverless computing (Cloud Run), Database selection (SQL vs NoSQL), and API Security concepts.

---

### 3. Conceptual Fundamentals

**Q: Elaborate on the structural difference between Compute Engine and Cloud Run.**
*Answer:* Compute Engine is Infrastructure-as-a-Service (IaaS) where you provision raw Virtual Machines requiring manual OS patches, load balancing, and scaling configurations. Cloud Run is a fully managed Serverless compute platform that abstracts the infrastructure entirely, automatically deploying stateless Docker containers from zero to thousands based purely on incoming HTTP traffic.

**Q: Compare Cloud Storage, Cloud SQL, and Firestore.**
*Answer:* 
- Cloud Storage is an Object Database used purely for unstructured binary files (images, videos).
- Cloud SQL is a managed Relational Database enforcing strict schemas (PostgreSQL) optimized for complex transactional queries.
- Firestore is a Serverless NoSQL Document Database optimized for massive horizontal scale and rapid, schema-less JSON storage ideal for real-time applications.

---

### 4. Scenario-Based Questions

**Scenario 1: You are building an Uber clone. A user requests a ride. The mobile app needs to show an interactive map and tell the user exactly how far away the driver is. Explain the architecture.**
*Answer:* The mobile frontend will render the map using the *Maps JavaScript/Android API* (secured via HTTP restrictions). When determining the exact drive distance and calculating the ride price, the frontend MUST NOT calculate it directly. The frontend sends the driver and user coordinates to a Node.js backend hosted securely on *Cloud Run*. The backend utilizes the *Distance Matrix API* (secured via IP address restrictions) to mathematically calculate the route, ensuring the client cannot manipulate pricing. The backend saves the transit log to *Cloud SQL* and returns the final price to the user.

**Scenario 2: Your company's Google Maps API bill suddenly spiked to $10,000 this week. How do you triage and resolve this?**
*Answer:* First, I would verify the Cloud Billing Dashboard to isolate exactly which specific API (e.g., Maps JS or Autocomplete) caused the spike. Second, I would ensure our API keys possess proper *Application Restrictions* (HTTP/IP) to verify hackers haven't stolen an unrestricted key. Third, I would check the frontend code for uncontrolled infinite loops causing rapid re-rendering of Map components. Finally, I would immediately apply an *API Quota* inside the GCP Console to strictly hard-cap daily requests to a safe financial boundary while we deploy Redis caching optimizations.

---

### 5. Practical Knowledge Checks

**Q: Why might you decouple a React Single Page Application (SPA) natively from a Node.js backend entirely?**
*Answer: Because rendering static HTML/JS files requires zero active server processes. By decoupling, the frontend safely resides in Cloud Storage, drastically reducing active server compute costs. The Cloud Run Node.js backend is then only invoked when explicit database logic is required.*

**Q: Describe a "Cold Start" in GCP Cloud Run.**
*Answer: When a serverless container has scaled perfectly to zero due to inactivity, the next incoming HTTP request encounters a Cold Start. This is a slight delay as GCP provisions the hardware, pulls the Docker image, and spins up the Node service before responding.*

**Q: Why separate your infrastructure into multiple GCP Projects (e.g., Dev and Prod)?**
*Answer: Constructing identical isolated projects provides absolute security. If a junior developer runs a destructive script locally utilizing dev credentials, it physically cannot interact with or delete the Production Cloud SQL database.*

---

### Conclusion
Understanding how to compose infrastructure—knowing exactly when to use a VM vs Serverless, SQL vs NoSQL, and frontend vs backend Maps routing—is the defining factor of a Senior Cloud Engineer. 

Review the architectural flows, prioritize API Key security, and you will be excellently prepared for your GCP evaluations!

---
Prev : [15_best_practices_and_security.md](./15_best_practices_and_security.md) | Next : None (End of Guide)
