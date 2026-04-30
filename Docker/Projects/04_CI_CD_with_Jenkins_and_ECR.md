# 📌 Project: Full CI/CD Pipeline with Jenkins, ECR, and ECS

## 🏗️ Project Overview
This project is the culmination of the "Automated Build" and "Cloud Integration" modules. We will build a **Fully Automated Deployment Pipeline**. From the moment a developer pushes code to Git, the system will: Lint, Test, Build (Multi-arch), Scan (Trivy), Push (ECR), and Deploy (ECS Fargate) with a **Blue-Green** strategy.

## 📐 Architecture Diagram

```text
[ GIT PUSH ] -> [ JENKINS ]
                   |
          +--------+--------+
          |                 |
    [ DOCKER BUILD ]  [ TRIVY SCAN ]
          |                 |
    [ PUSH TO ECR ] <-------+
          |
    [ DEPLOY TO ECS ] (Fargate)
          |
    [ ALB FAILOVER ] (Blue/Green)
```

## 🛠️ Step 1: The Jenkins Pipeline (Groovy)
This pipeline uses the `docker` agent for a clean build environment.
```groovy
pipeline {
    agent { label 'docker-node' }
    stages {
        stage('Quality Gate') {
            steps {
                sh 'docker run --rm node:18 npm test'
            }
        }
        stage('Multi-Arch Build') {
            steps {
                // Build for both x86 and ARM (for Graviton instances)
                sh 'docker buildx build --platform linux/amd64,linux/arm64 -t ${ECR_REPO}:${BUILD_ID} --push .'
            }
        }
        stage('Security Scan') {
            steps {
                sh 'trivy image --severity CRITICAL --exit-code 1 ${ECR_REPO}:${BUILD_ID}'
            }
        }
        stage('Deploy to ECS') {
            steps {
                // Update the ECS Service with the new Image ID
                sh 'aws ecs update-service --cluster prod --service my-app --force-new-deployment'
            }
        }
    }
}
```

## ⛓️ Step 2: The ECS Task (Fargate)
We use a serverless deployment to eliminate host management.
```json
{
  "containerDefinitions": [
    {
      "name": "my-app",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/my-app:v1",
      "cpu": 256,
      "memory": 512,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": { "awslogs-group": "/ecs/my-app" }
      }
    }
  ]
}
```

## 🔬 Internal Mechanics (The Blue-Green Cutover)
1. **The Green Deployment**: ECS starts new containers (v2) alongside the old ones (v1).
2. **The Health Check**: The ALB waits for the v2 containers to pass their health checks.
3. **The Drain**: Once v2 is healthy, ALB shifts traffic from v1 to v2.
4. **The Termination**: After 5 minutes (Deregistration Delay), the v1 containers are killed.
5. **Result**: Users never see a "502 Bad Gateway" during the update.

## 💥 Production Failures & Fixes
- **Failure**: The deployment hangs forever. 
  *Fix*: Check the ECS events. Usually, it's a "Task Failed to Start" because of a missing environment variable or a crashing container.
- **Failure**: The build takes 20 minutes because it's downloading 1GB of NPM packages every time.
  *Fix*: Implement **BuildKit Remote Caching** in the Jenkinsfile.

## 💼 Interview Q&A
**Q: How do you ensure that only 'Scanned and Verified' images are deployed to production?**
**A**: I implement a **Hard Gate** in the CI pipeline. Before the image is pushed to the production registry, it must pass a **Trivy scan**. If even one "CRITICAL" vulnerability is found, the `trivy` command returns a non-zero exit code, which causes the Jenkins pipeline to fail and abort the deployment. Additionally, I use **Image Signing (Cosign)**; the ECS cluster is configured to only pull images that have a valid signature from our Jenkins build server.

## 🧪 Lab Exercise
1. Set up an AWS ECR repository.
2. Run a Jenkins job that builds a simple image and pushes it to that repository.
3. Manually trigger an ECS deployment using the AWS CLI.
4. Watch the "Rolling Update" progress in the AWS ECS Console.

---
Prev: [03_Secure_Microservices_with_Vault.md](./03_Secure_Microservices_with_Vault.md) | Index: [00_Index.md](../00_Index.md) | Next: [05_Monitoring_Stack_Prometheus_Grafana.md](./05_Monitoring_Stack_Prometheus_Grafana.md)
---
