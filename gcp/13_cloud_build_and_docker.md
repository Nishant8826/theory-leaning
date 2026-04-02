# DevOps & CI/CD with Cloud Build

---

### 2. What
- **CI/CD (Continuous Integration / Continuous Deployment):** The philosophy of automating deploying code. When a developer types `git push`, robots automatically test the code and deploy it to the live server.
- **Cloud Build:** Google's native serverless CI/CD platform. It reads a simple config file, runs your tests, builds your Docker images, and pushes them straight to production.

---

### 3. Why
Manually building a Docker image on your laptop and uploading it takes 10+ minutes and freezes your computer. If you skip a step, the website breaks. Implementing CI/CD via Cloud Build ensures deployments are perfectly identical, safe, and entirely hand-free every single time.

---

### 4. How
1. You connect your GitHub Repository directly to GCP Cloud Build.
2. You place a file called `cloudbuild.yaml` in your project root.
3. Every time you push to the `main` branch, Cloud Build reads the YAML file, executes the Docker build within Google's mega-computers, and triggers a Cloud Run deployment seamlessly.

---

### 5. Implementation

**Building a CI/CD Pipeline YAML File**

```yaml
# File: cloudbuild.yaml (in your project root)

steps:
  # STEP 1: Build the Docker Image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-app-image', '.']

  # STEP 2: Push the Image to Google Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-app-image']

  # STEP 3: Deploy the new Image to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'my-app-service'
      - '--image'
      - 'gcr.io/$PROJECT_ID/my-app-image'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'

images:
  - 'gcr.io/$PROJECT_ID/my-app-image'
```

---

### 6. Steps
1. Navigate to the GCP Console $\rightarrow$ "Cloud Build" $\rightarrow$ "Triggers".
2. Click "Connect Repository" and authorize GitHub.
3. Select your repository and set the trigger to fire upon pushes strictly to the `^main$` branch.
4. Push your code! Watch the Cloud Build logs visually in the console as it builds the Dockerfile.

---

### 7. Integration

🧠 **Think Like This:**
* Your local machine is only for writing raw Javascript.
* The moment you type `git push`, Cloud Build acts as the middleman. It compiles the React/Node code natively inside a temporary Linux container, builds the Docker image, and explicitly pushes it to Cloud Run.

---

### 8. Impact
📌 **Real-World Scenario:** A sprawling 50-person engineering team pushes small React and Node updates 30 times a day. By utilizing CI/CD pipelines, no human being is manually uploading files or interacting with FTP passwords. The entire process becomes securely automated natively.

---

### 9. Interview Questions
1. **Explain the purpose of the `cloudbuild.yaml` file.**
   *Answer: It acts as an executable blueprint defining the distinct sequential structural steps (e.g., test, build, push, deploy) the Cloud Build service must execute intuitively when triggered.*
2. **Why is it essential to only trigger deployments off specific branches (like `main`)?**
   *Answer: This segregates experimental code (in feature branches) safely away from the automated CI/CD pipeline, guaranteeing only thoroughly reviewed, finalized code reaches live production end-users!*
3. **What is Google Container Registry (GCR / Artifact Registry)?**
   *Answer: It is GCP's native isolated storage service specifically engineered to securely house compiled Docker Image artifacts locally, allowing Cloud Run to pull them rapidly for deployment.*

---

### 10. Summary
* CI/CD automates all deployment steps based on GitHub triggers.
* Cloud Build serves as Google's native compilation and deployment robotic pipeline.
* Use `cloudbuild.yaml` to elegantly orchestrate Docker Image building and routing.

---
Prev : [12_deploying_nodejs_backend.md](./12_deploying_nodejs_backend.md) | Next : [14_scaling_monitoring_cost.md](./14_scaling_monitoring_cost.md)
