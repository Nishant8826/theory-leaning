# DevOps: CI/CD, CodePipeline, Docker, & ECS

---

### 2. What
- **CI/CD (Continuous Integration / Continuous Deployment):** The practice of automating deployments. When a developer pushes code to GitHub, systems test it and deploy it to AWS automatically.
- **AWS CodePipeline:** Amazon's native CI/CD service that orchestrates the entire deployment pipeline.
- **Docker:** A tool that packages your Node.js code and OS dependencies into a single portable "Container".
- **ECS (Elastic Container Service):** AWS's orchestration engine to run fleets of Docker containers securely.

---

### 3. Why
If you manually SSH into an EC2 server, type `git pull`, and run `npm install` every time you update your app, you will eventually cause downtime due to a typo. CodePipeline automates your job. ECS ensures that if your Docker container crashes, AWS instantly restarts a fresh copy.

---

### 4. How
1. Package your Node.js application cleanly into a Docker image using a `Dockerfile`.
2. Configure AWS CodePipeline to listen to the `main` branch of your GitHub repository.
3. CodePipeline commands AWS to build your Docker image and injects it into ECS.

---

### 5. Implementation

**A Classic Dockerfile for an Express AWS App**

```dockerfile
# 1. Grab a lightweight exact version of Node
FROM node:18-alpine

# 2. Assign the working directory securely
WORKDIR /app

# 3. Copy dependencies and install natively
COPY package*.json ./
RUN npm install

# 4. Copy the raw backend logic
COPY . .

# 5. Expose Port 80 for the AWS Load Balancer
EXPOSE 80

# 6. Command to start the application 
CMD ["node", "index.js"]
```

---

### 6. Steps
1. Push your raw code containing the `Dockerfile` explicitly to GitHub.
2. In the AWS Console, create a new CodePipeline.
3. Point the "Source" stage to your specific GitHub repository.
4. Point the "Deploy" stage to your ECS Cluster.
5. The pipeline runs automatically.

---

### 7. Integration

🧠 **Think Like This:**
* A Docker container guarantees that the Node.js code running on your local Mac will run identically on an Ubuntu EC2 or an ECS cluster. It prevents "It works on my machine" bugs.

---

### 8. Impact
📌 **Real-World Scenario:** By combining Docker and ECS, highly scalable companies execute deployments during peak business hours. ECS handles "Rolling Updates", slowly shutting down old code containers and spinning up new containers without users experiencing any downtime.

---

### 9. Interview Questions

Q1. What is the fundamental purpose of AWS CodePipeline?
Answer: CodePipeline is a fully managed continuous delivery service that automates the build, test, and deploy phases of your release process every time there is a code change.

Q2. What problem does Docker solve when deploying applications to AWS?
Answer: Docker bundles the application code securely with all operating system dependencies, guaranteeing the application behaves identically across all deployment environments.

Q3. What is Amazon ECS?
Answer: Amazon Elastic Container Service is a fully managed container orchestration service that allows you to easily launch, stop, and manage Docker containers across a cluster of EC2 instances.

Q4. Explain a "Rolling Deployment" within ECS.
Answer: A rolling deployment replaces old Docker containers with new Docker containers one at a time, ensuring the application remains active and avoids downtime during updates.

Q5. How does AWS ECS differ from AWS EC2?
Answer: EC2 provides raw virtual machines (servers), while ECS is a managed service that runs and orchestrates Docker containers specifically on top of those EC2 servers.

Q6. What happens if a Docker container crashes inside an ECS cluster?
Answer: ECS constantly monitors container health. If a container crashes, ECS automatically terminates the failed container and spins up a fresh replacement to maintain the desired structural capacity.

---

### 10. Summary
* Docker containerizes applications robustly.
* ECS orchestrates and manages containers efficiently.
* CodePipeline automates the entire deployment process without manual SSH.

---
Prev : [10_deploying_nodejs_backend.md](./10_deploying_nodejs_backend.md) | Next : [12_scaling_load_balancing_monitoring.md](./12_scaling_load_balancing_monitoring.md)
