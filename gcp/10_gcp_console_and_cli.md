# Working with GCP: Console, CLI, and Projects

---

### 2. What
To manage your cloud infrastructure, Google gives you two main tools:
- **GCP Console:** The visual website dashboard. You click buttons to create servers, databases, and API keys.
- **gcloud CLI:** A terminal command-line tool. You type commands to orchestrate those exact same resources efficiently without a mouse.

Everything you create lives inside a **GCP Project**. A Project is a master folder. All your databases, VMs, and Maps API keys belong to one specific Project.

✅ **Simple Analogy:**
- *GCP Project:* A house.
- *GCP Console:* Designing the house visually with an architect.
- *gcloud CLI:* The robotic construction crew that instantly builds exactly what you type out.

---

### 3. Why
While the Console UI is lovely for beginners checking their billing dashboard, professionals configure infrastructure via the CLI locally. Utilizing the CLI allows you to write automated bash scripts that can instantly generate 5 servers and a database in identical configurations sequentially without clicking 50 different tedious web pages.

---

### 4. How
1. Install the `Google Cloud CLI` on your local computer.
2. Open your VS Code terminal and type `gcloud init`. 
3. This opens a browser securely authenticating your Google account.
4. You are now securely bridged to your cloud directly from your terminal!

---

### 5. Implementation

**Mini Exercise: Basic CLI Usage**

```bash
# 1. Authenticate your computer
gcloud auth login

# 2. Create a brand new project securely
gcloud projects create my-cool-delivery-app-123

# 3. Tell your CLI terminal to "focus" entirely on this new project
gcloud config set project my-cool-delivery-app-123

# 4. Enable the Compute Engine API so we can make VMs!
gcloud services enable compute.googleapis.com

# 5. List all active Virtual Machines in this project
gcloud compute instances list
```

---

### 6. Steps (Starting a New Application)
1. Go to the visual GCP Console.
2. Click the dropdown at the top and click "New Project" (e.g., `uber-clone-dev`).
3. **Billing Basics:** Search for "Billing" in the top bar. You **MUST** attach a credit card to the project. GCP gives a generous Free Tier, but APIs (especially Maps) require an active card to prevent spam.
4. Open your local terminal, run `gcloud config set project uber-clone-dev` and start deploying!

---

### 7. Integration

🧠 **Think Like This:**
* **Local Development Strategy:** Always create at least TWO projects in GCP: `app-name-dev` and `app-name-prod`. 
* You connect your local Node.js environment strictly to `app-name-dev` via your CLI. This guarantees if you accidentally drop your entire user database through a local SQL typo, you only destroyed the fake test Database, keeping your production users completely safe.

---

### 8. Impact
📌 **Real-World Scenario:** By utilizing the `gcloud CLI`, DevOps engineers can integrate GCP commands directly into GitHub Actions. When a developer pushes code, an automated script runs `gcloud run deploy...` pushing the app out to millions globally without human intervention.

---

### 9. Interview Questions
1. **What is the fundamental purpose of a "Project" in Google Cloud?**
   *Answer: A Project is the absolute base-level organizing entity. It logically isolates resources, APIs, IAM permissions, and billing boundaries securely for a specific application.*
2. **What is the `gcloud` CLI?**
   *Answer: It is the primary command-line tool provided by Google Cloud to manage authentication, local environments, and the provisioning/deployment of cloud resources programmatically.*
3. **Why is attaching a valid Billing Account strictly required even if utilizing the Free Tier?**
   *Answer: Because it verifies user identity securely mitigating malicious spam networks, and provides a seamless structure allowing the system to charge appropriately immediately if your application scales massively past the free baseline quotes.*

---

### 10. Summary
* The Console is visual; The gcloud CLI is terminal-based.
* Always organize apps into specific distinct GCP Projects.
* Creating isolated `-dev` and `-prod` projects natively secures your cloud data.
* Billing must be actively attached to unlock the Maps and Compute APIs.

---
Prev : [09_implementing_maps_in_backend.md](./09_implementing_maps_in_backend.md) | Next : [11_deploying_react_and_nextjs.md](./11_deploying_react_and_nextjs.md)
