# Deploying React & Next.js on GCP

---

### 2. What
Deploying means moving your local frontend code onto Google's servers so the public can access it.
- **Static React (Vite/CRA):** These are just plain HTML/CSS/JS files. We host them in **Cloud Storage** (like a folder acting as a simple web server).
- **Next.js:** Because Next.js uses server-side logic, it requires an active Node.js server. We host it using **Cloud Run**.

---

### 3. Why
Hosting strategies affect costs dramatically. Running a heavily managed Cloud Run server for a completely static React page is a waste of money. Hosting it in a Storage Bucket is almost free and infinitely scalable. Conversely, Next.js *must* have a server to function correctly.

---

### 4. How
For Next.js, we containerize it (Docker) and deploy it to Cloud Run. For plain React, we build the static files (`npm run build`) and upload them to a public Cloud Storage bucket.

---

### 5. Implementation

**A. Deploying Next.js via Cloud Run (CLI)**

```bash
# 1. Ensure you have a Dockerfile in your Next.js project
# 2. Deploy it in one command:
gcloud run deploy my-next-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Wait 60 seconds... Google provides your secure HTTPS URL!
```

**B. Deploying Static React to Cloud Storage (CLI)**

```bash
# 1. Build your static app locally
npm run build 

# 2. Create a public bucket
gsutil mb -l us-central1 gs://my-react-bucket
gsutil iam ch allUsers:objectViewer gs://my-react-bucket

# 3. Securely upload your "dist" folder
gsutil rsync -R dist/ gs://my-react-bucket

# 4. Tell GCP this bucket is a website
gsutil web set -m index.html -e index.html gs://my-react-bucket
```

---

### 6. Steps
1. Determine if your framework requires a backend server natively (Next.js) or if it's purely static (Vite).
2. Choose Cloud Run for server-based frontends.
3. Choose Cloud Storage + Cloud CDN for purely static frontends.

---

### 7. Integration

🧠 **Think Like This:**
When deploying a frontend that uses Google Maps, you must pass the API key correctly during deployment.
For Cloud Run, inject it explicitly:
`gcloud run deploy --update-env-vars NEXT_PUBLIC_MAPS_KEY=AIza...`

---

### 8. Impact
📌 **Real-World Scenario:** By deploying static files to Cloud Storage paired with a CDN, your website becomes essentially "uncrashable". If a million users visit simultaneously to view your Maps application, Google's edge nodes serve the files effortlessly without relying on a central database server.

---

### 9. Interview Questions
1. **Why is deploying a Client-Side React app to Cloud Storage preferred over Compute Engine?**
   *Answer: Because rendering static HTML/JS files does not require an active server process. Housing them in Cloud Storage is infinitely cheaper and requires zero maintenance.*
2. **What does the `--allow-unauthenticated` flag do in Cloud Run?**
   *Answer: It tells Google Cloud to open the container publicly to the internet, allowing any user to visit the URL without requiring a specialized Google IAM validation token.*

---

### 10. Summary
* Next.js utilizes Server-Side functionality, hence requires Cloud Run.
* Static React (Vite) uses Cloud Storage for zero-maintenance hosting.
* Use environment flags during deployment to safely pass Map API keys into production!

---
Prev : [10_gcp_console_and_cli.md](./10_gcp_console_and_cli.md) | Next : [12_deploying_nodejs_backend.md](./12_deploying_nodejs_backend.md)
