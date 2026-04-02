# Best Practices & Security in GCP

---

### 2. What
This file covers the absolute mandatory architectural rules you must follow to prevent data breaches, API key theft, and messy spaghetti-code project structures when operating in Google Cloud Platform. 

---

### 3. Why
Hackers use automated bots that scrape public GitHub repositories 24/7 searching strictly for `AIz...` (Google Maps API keys) and database passwords. If they find your Maps API key, they can run up a $50,000 bill on your account in a single day. Security is not optional; it is mandatory. 

---

### 4. How
- **Project Structure:** Use two entirely separate GCP Projects: `[App-Name]-Dev` and `[App-Name]-Prod`.
- **API Key Protection:** Implement HTTP Referrer Restrictions for Maps frontend keys, and IP Restrictions for backend keys.
- **Service Accounts:** Obey the Principle of Least Privilege. 

---

### 5. Implementation

**A. API Key Protection (Critical for Google Maps)**

Never leave your Maps API key completely unrestricted.

1. **Frontend Key (React):** This key is physically shipped to the user's browser, so anyone can see it by right-clicking "Inspect Element". 
   - *Fix:* Go to the GCP Credentials console. Add "Application Restrictions". Select "HTTP referrers". Add `https://your-website.com/*`. Now, even if a hacker steals the key, Google Maps will reject any requests that do not originate from your exact domain!
2. **Backend Key (Node.js):**
   - *Fix:* Set Application Restrictions to "IP addresses". Only input the exact static external IP address of your Cloud Run server. 

**B. Securing Environment Variables**

Instead of passing raw passwords directly in code, use Google Secret Manager.

```javascript
// Node.js: Fetching a password dynamically from Secret Manager
const { SecretManagerServiceClient } = require('@google-cloud/secret-manager');
const client = new SecretManagerServiceClient();

async function getSecret() {
  const name = 'projects/my-project/secrets/DB_PASSWORD/versions/latest';
  const [version] = await client.accessSecretVersion({ name });
  const rawPassword = version.payload.data.toString('utf8');
  return rawPassword; 
}
```

---

### 6. Steps
1. Navigate to APIs & Services > Credentials.
2. Click your Maps API Key.
3. Under "API restrictions", strictly select the 2 or 3 APIs this key specifically needs (e.g., Places API, Geocoding API). Do not allow it access to all 200+ GCP APIs!
4. Under "Application restrictions", restrict it to your Website URL.
5. Setup a `dev` GCP project for local testing, isolated from your `prod` user data. 

---

### 7. Integration

🧠 **Think Like This:**
* Treat your React Maps API key like a house key that you give out to the public, but you specifically change the locks on the door (using HTTP Restrictions) to only allow your exact friends inside.
* Treat your Node.js Maps API Key like a bank vault key perfectly locked inside a secure safe (using Google Secret Manager).

---

### 8. Impact
📌 **Real-World Scenario:** A junior developer accidentally pushes their raw Google Maps API key inside an `index.html` file to a public GitHub repo. Because they properly configured "HTTP Referrer Restrictions" tying the key *only* to `their-website.com`, the hacker steals the key but fails entirely to use it on their own servers, generating a $0 bill.

---

### 9. Interview Questions
1. **How do you secure an API key that must be shipped to a React client (like the Maps JS API)?**
   *Answer: By strictly enforcing HTTP Referrer restrictions in the GCP Console, ensuring requests utilizing the key are only honored if they physically originate from the authorized production web domain.*
2. **Explain the Principle of Least Privilege.**
   *Answer: A security doctrine stating that a user, API key, or Service Account must be granted the absolute minimum permissions strictly necessary to perform its specific task, preventing broad damage during a breach.*
3. **Why use Google Secret Manager instead of hardcoded strings in production?**
   *Answer: It ensures sensitive values are audited, version-controlled, securely encrypted, and accessible purely via IAM policies rather than existing in plain text inside your GitHub repository.*

---

### 10. Summary
* Protect Frontend Maps keys with HTTP Restrictions.
* Protect Backend Maps keys with IP Restrictions.
* Use Service Accounts strictly adhering to the Principle of Least Privilege.
* Create separate Development and Production Projects to protect real user data.

---
Prev : [14_scaling_monitoring_cost.md](./14_scaling_monitoring_cost.md) | Next : [16_gcp_interview_preparation.md](./16_gcp_interview_preparation.md)
