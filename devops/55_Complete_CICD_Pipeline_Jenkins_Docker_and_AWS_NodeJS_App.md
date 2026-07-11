# 55 – Complete CI/CD Pipeline: Jenkins + Docker + AWS (Node.js App)

> **Session Context:** This session (part of Batch-43 focusing on Multi-Cloud with AWS, DevOps, and AI) is a hands-on workshop focused on building and explaining a **real-time CI/CD project** using **Node.js, Jenkins, Docker, and AWS EC2**. Setting up this end-to-end pipeline is highly valuable for interviews as it demonstrates a complete, production-ready DevOps workflow.

### 📋 Session Action Items
- [ ] **Infrastructure:** Create or update your AWS EC2 Ubuntu instance (`t3.large`, 45GB storage) and open ports `8080` & `3000` in the security group.
- [ ] **Setup:** Install Jenkins & Docker on the EC2 machine, and add the `jenkins` user to the `docker` group.
- [ ] **Configure:** Set up Jenkins global tools (JDK 17, Node.js 16.20, Docker) and add your Docker Hub credentials to the Global Credentials store.
- [ ] **Pipeline CI:** Set up a CI pipeline job pulling the code from the GitHub repository to build and push the Docker image.
- [ ] **Pipeline CD:** Set up a CD pipeline job linked to trigger automatically after a successful CI run.
- [ ] **Interview Prep:**
  - [ ] Practice explaining the difference between CI/CD and Delivery vs Deployment.
  - [ ] Prepare a short interview story framing this Node.js + Jenkins + Docker + AWS project.
  - [ ] Record your project explanation for practice and review.
- [ ] **Review:** Re-watch the class recording to ensure no steps or command details are missed.

### 🎯 Suggested Focus Next
- Jenkinsfile structure and syntax.
- Draft of interview answers.
- Resume bullet points reflecting this pipeline project.

---

## Table of Contents

1. [Continuous Integration vs Delivery vs Deployment](#1-continuous-integration-vs-delivery-vs-deployment)
2. [CI/CD Flow Overview](#2-cicd-flow-overview)
3. [Declarative vs Scripted Pipelines](#3-declarative-vs-scripted-pipelines)
4. [Infrastructure Setup on AWS EC2](#4-infrastructure-setup-on-aws-ec2)
5. [Jenkins Installation & Configuration](#5-jenkins-installation--configuration)
6. [Docker Installation & Jenkins Integration](#6-docker-installation--jenkins-integration)
7. [CI Pipeline – Build & Push Docker Image](#7-ci-pipeline--build--push-docker-image)
8. [CD Pipeline – Pull & Run Container](#8-cd-pipeline--pull--run-container)
9. [CI/CD Integration – Auto-Trigger CD after CI](#9-cicd-integration--auto-trigger-cd-after-ci)
10. [Advanced Scenarios](#10-advanced-scenarios)
11. [Tech Stack Mapping](#11-tech-stack-mapping)
12. [Scenario-Based Q&A](#12-scenario-based-qa)
13. [Interview Q&A](#13-interview-qa)
14. [Quick Reference Cheatsheet](#14-quick-reference-cheatsheet)
15. [Career & Interview Strategy](#15-career--interview-strategy)

---

## 1. Continuous Integration vs Delivery vs Deployment

### What
These are three stages of modern software release automation:

| Term | What it means | Who approves? |
|---|---|---|
| **Continuous Integration (CI)** | Automatically build and test code every time a developer pushes | Automated tests |
| **Continuous Delivery (CD)** | Automatically prepare a release-ready artifact — but a human approves before it goes live | Human (Change Request / CAB) |
| **Continuous Deployment (CD)** | Fully automated — code goes from commit to production with zero human intervention | Nobody — fully automated |

### Why
Without CI/CD, releases are manual, slow, and error-prone. Developers would test locally, zip files, copy to servers, and hope it works. CI/CD eliminates that by making the pipeline repeatable and automatic.

### The CR / CAB Process (Continuous Delivery)
In enterprise environments (banks, insurance, large corps):
- **CR = Change Request** — A ticket raised to describe what change is going to production
- **CAB = Change Advisory Board** — A committee that reviews and approves the CR
- A human clicks "Deploy" only after CAB approval
- This is **Continuous Delivery** — automated up to the gate, manual through it

Continuous Delivery involves manual approval before moving code from one environment to another, such as raising a Change Request (CR) in the ITIL process with a standard 2-hour window for production changes. In practice, many companies follow delivery for production because changes can affect dependent systems and business operations, whereas Continuous Deployment is fully automated with no manual approval required.

### How (Delivery vs Deployment)

```
Continuous Delivery:
  Code Push → CI (build/test) → Artifact Ready → ⏸ Human Approval → Deploy to Prod

Continuous Deployment:
  Code Push → CI (build/test) → Artifact Ready → ✅ Auto Deploy to Prod
```

### Impact

| Without CI/CD | With CI/CD |
|---|---|
| Releases take days/weeks | Releases in minutes |
| "Works on my machine" bugs | Consistent build environment (Docker) |
| Manual, error-prone deployments | Repeatable, automated pipelines |
| Fear of releasing on Fridays | Confidence to deploy anytime |

---

## 2. CI/CD Flow Overview

### The Full Pipeline

```
Developer's Laptop
      │
      │  git push
      ▼
  GitHub Repo
  (source of truth)
      │
      │  Webhook / Poll SCM
      ▼
  Jenkins CI Pipeline
  ┌─────────────────────────────────────────┐
  │ Stage 1: Checkout Code (from GitHub)    │
  │ Stage 2: npm install                    │
  │ Stage 3: npm run build                  │
  │ Stage 4: docker build -t image:tag .    │
  │ Stage 5: docker push → Docker Hub       │
  └─────────────────────────────────────────┘
      │
      │  Build triggers CD pipeline
      ▼
  Jenkins CD Pipeline
  ┌─────────────────────────────────────────┐
  │ Stage 1: docker stop old-container      │
  │ Stage 2: docker rm old-container        │
  │ Stage 3: docker pull latest image       │
  │ Stage 4: docker run -p 3000:3000        │
  └─────────────────────────────────────────┘
      │
      ▼
  App running on EC2: http://<IP>:3000
```

### Key Insight
The CI pipeline **builds and stores** the artifact (Docker image on Docker Hub).
The CD pipeline **fetches and runs** that artifact on the server.
They are **separate jobs** — separation of concerns. CI = build. CD = deploy.

### Practical CI/CD Setup: 10-Step Workflow
During the session, the hands-on implementation was divided into 10 key steps:
1. **Launch AWS EC2 Instance:** Ubuntu virtual machine, `t3.large` instance, 45GB storage, named "Starbucks".
2. **Configure Security Group:** Open port `8080` (Jenkins) and port `3000` (Node.js app) to allow inbound traffic.
3. **Install Jenkins:** Install JDK 21/17 and Jenkins using official commands, then unlock Jenkins via the web UI.
4. **Install Docker:** Install Docker using the shell script and add the `jenkins` user to the `docker` group.
5. **Install Jenkins Plugins:** Add plugins for Docker, Docker Pipeline, Docker API, Docker Build Step, and NodeJS.
6. **Configure Docker Hub Credentials:** Add credentials securely under global credentials (using ID `docker-hub-creds`).
7. **Configure Jenkins Tools:** Set up JDK 17, NodeJS 16, and Docker versions in global tool configurations.
8. **Create CI Pipeline Job:** Set up a Declarative Pipeline pulling from GitHub SCM to run `npm install`, `npm run build`, build a Docker image, and push it to Docker Hub.
9. **Create CD Pipeline Job:** Set up a Scripted Pipeline to pull the Docker image from Docker Hub and run it on port 3000.
10. **Link CI/CD Pipelines:** Configure the CD job to trigger automatically using "Build after other projects are built" once the CI job completes successfully.

---

## 3. Declarative vs Scripted Pipelines

### What
Jenkins supports two ways to write pipelines as code (Jenkinsfile):

### Declarative Pipeline
- **Structured, opinionated syntax** with defined blocks
- Uses `pipeline { }` wrapper
- Easier to read, enforces structure
- Better for most teams

```groovy
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'npm install'
      }
    }
  }
}
```

### Scripted Pipeline
- **Full Groovy code** — maximum flexibility
- Uses `node { }` wrapper
- More powerful, but harder to read
- Used when you need complex logic (loops, conditions, dynamic stages)

```groovy
node {
  stage('Deploy') {
    sh 'docker stop app || true'
    sh 'docker rm app || true'
    sh 'docker run -d --name app -p 3000:3000 myimage:latest'
  }
}
```

### Comparison Table

| Feature | Declarative | Scripted |
|---|---|---|
| Syntax | Structured blocks | Pure Groovy |
| Readability | High | Lower |
| Flexibility | Medium | Very High |
| Error handling | `post { }` block | try/catch |
| Best for | Standard CI/CD | Complex logic |
| Used in this class | CI Pipeline | CD Pipeline |

### When to Use Which
- **Declarative:** Building, testing, pushing — standard linear pipeline
- **Scripted:** Complex deployments with conditions (if dev deploy here, if prod deploy there), dynamic container management

---

## 4. Infrastructure Setup on AWS EC2

### What
We run Jenkins and Docker on a single AWS EC2 (Ubuntu) instance.

### Step-by-Step: Launch EC2

```
AWS Console → EC2 → Launch Instance

Settings:
  Name:           jenkins-cicd-server
  AMI:            Ubuntu 22.04 LTS
  Instance type:  t3.large  (2 vCPU, 8GB RAM — Jenkins needs it)
  Storage:        45 GB gp3
  Region:         Mumbai (ap-south-1)
  Key pair:       Create new → download .pem file
```

### Security Group Rules (Inbound)

| Port | Protocol | Purpose | Source |
|---|---|---|---|
| 22 | TCP | SSH access | Your IP |
| 8080 | TCP | Jenkins Web UI | 0.0.0.0/0 |
| 3000 | TCP | Node.js App | 0.0.0.0/0 |

**Why t3.large?** Jenkins is memory-intensive. Running builds, Docker, and Node.js on t2.micro/t3.micro causes OOM (Out of Memory) kills and build failures.

### Connect to EC2

```bash
# Make key read-only
chmod 400 your-key.pem

# SSH in
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

---

## 5. Jenkins Installation & Configuration

### Install Jenkins (Ubuntu)

```bash
# Update packages
sudo apt update

# Install Java (Jenkins requires JDK)
sudo apt install fontconfig openjdk-17-jre -y

# Verify Java
java -version

# Add Jenkins repo key
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

# Add Jenkins apt repository
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt-get update
sudo apt-get install jenkins -y

# Start & enable Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Get initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### First-Time Jenkins Setup

```
Browser → http://<EC2-IP>:8080

1. Paste initialAdminPassword
2. Install suggested plugins
3. Create admin user
4. Save Jenkins URL → Finish
```

### Jenkins Plugins to Install

```
Manage Jenkins → Plugins → Available

Install:
  ✅ Docker
  ✅ Docker Pipeline
  ✅ Docker API
  ✅ Docker Build Step
  ✅ NodeJS Plugin
```

### Configure Tools in Jenkins

```
Manage Jenkins → Tools

JDK:
  Name: jdk17
  Install automatically: ✅
  Version: Java 17

NodeJS:
  Name: nodejs16
  Install automatically: ✅
  Version: NodeJS 16.x

Docker:
  Name: docker
  Install automatically: ✅
  Version: latest
```

### Add Docker Hub Credentials

```
Manage Jenkins → Credentials → System → Global credentials → Add

Kind:     Username with password
Username: your-dockerhub-username
Password: your-dockerhub-password-or-token
ID:       docker-hub-creds        ← reference this in Jenkinsfile
Description: Docker Hub Login
```

**Why store credentials here?** Never hardcode passwords in Jenkinsfile. Jenkins encrypts stored credentials. In Jenkinsfile, you reference by ID — credentials are injected at runtime.

---

## 6. Docker Installation & Jenkins Integration

### Install Docker on EC2

```bash
# Add Docker's GPG key
sudo apt-get update
sudo apt-get install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### Give Jenkins Permission to Use Docker

```bash
# Add jenkins user to docker group
sudo usermod -aG docker jenkins

# Restart Jenkins to apply
sudo systemctl restart jenkins
```

**Why?** By default, only root and members of the `docker` group can run Docker commands. Jenkins runs as the `jenkins` user — without group membership, `docker build` in pipelines will fail with "permission denied".

### Verify Docker Works

```bash
docker --version
docker run hello-world
```

---

## 7. CI Pipeline – Build & Push Docker Image

### The Dockerfile (Node.js / Starbucks App)

```dockerfile
# Use official Node.js LTS image
FROM node:16-alpine

# Set working directory inside container
WORKDIR /app

# Copy dependency files first (layer caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the source code
COPY . .

# Build the app (React/Next.js frontend)
RUN npm run build

# Expose port
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
```

### CI Jenkinsfile (Declarative)

```groovy
pipeline {
  agent any

  tools {
    nodejs 'nodejs16'
    jdk 'jdk17'
  }

  environment {
    DOCKER_IMAGE = 'yourdockerhubusername/starbucks-app'
    DOCKER_TAG   = "${BUILD_NUMBER}"   // unique tag per build
  }

  stages {

    stage('Checkout Code') {
      steps {
        git branch: 'main',
            url: 'https://github.com/your-username/starbucks-app.git'
      }
    }

    stage('Install Dependencies') {
      steps {
        sh 'npm install'
      }
    }

    stage('Build Application') {
      steps {
        sh 'npm run build'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-creds') {
            dockerImage.push("${DOCKER_TAG}")
            dockerImage.push('latest')   // also tag as latest
          }
        }
      }
    }

  }

  post {
    success {
      echo "✅ CI Pipeline SUCCESS — Image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
    }
    failure {
      echo "❌ CI Pipeline FAILED — Check logs above"
    }
  }
}
```

### What Each Stage Does

```
Checkout     → git clone from GitHub into Jenkins workspace
Install      → npm install (creates node_modules)
Build        → npm run build (compiles React/Next.js → static files)
Docker Build → docker build -t image:tag . (creates Docker image)
Docker Push  → docker push to Docker Hub (stores image remotely)
```

### Pipeline from SCM
Instead of pasting Jenkinsfile in Jenkins UI, point Jenkins to GitHub:

```
New Item → Pipeline
  Definition: Pipeline script from SCM
  SCM: Git
  Repository URL: https://github.com/your-username/starbucks-app
  Branch: */main
  Script Path: Jenkinsfile
```

This way, the Jenkinsfile lives in your repo — version controlled alongside your code.

---

## 8. CD Pipeline – Pull & Run Container

### CD Jenkinsfile (Scripted)

```groovy
node {

  def DOCKER_IMAGE = 'yourdockerhubusername/starbucks-app'
  def CONTAINER_NAME = 'starbucks-container'
  def APP_PORT = '3000'

  stage('Stop Old Container') {
    // || true prevents pipeline failure if container doesn't exist
    sh "docker stop ${CONTAINER_NAME} || true"
  }

  stage('Remove Old Container') {
    sh "docker rm ${CONTAINER_NAME} || true"
  }

  stage('Pull Latest Image') {
    sh "docker pull ${DOCKER_IMAGE}:latest"
  }

  stage('Run New Container') {
    sh """
      docker run -d \
        --name ${CONTAINER_NAME} \
        -p ${APP_PORT}:${APP_PORT} \
        --restart unless-stopped \
        ${DOCKER_IMAGE}:latest
    """
  }

  stage('Verify') {
    sh "docker ps | grep ${CONTAINER_NAME}"
    echo "✅ App running at http://<EC2-IP>:${APP_PORT}"
  }

}
```

### Why `|| true`?
The first time you run the CD pipeline, there's no existing container to stop/remove. Without `|| true`, the pipeline would **fail** on `docker stop` because there's nothing to stop. `|| true` says: "if this command fails, that's fine, keep going."

### `--restart unless-stopped`
Tells Docker to automatically restart the container if:
- The EC2 instance reboots
- Docker daemon restarts
- The container crashes

It will NOT restart if you manually stop it with `docker stop`.

---

## 9. CI/CD Integration – Auto-Trigger CD after CI

### What
After the CI pipeline succeeds (image pushed to Docker Hub), the CD pipeline should start automatically without anyone clicking "Build Now."

### How to Configure in Jenkins

```
Open the CD Pipeline job → Configure

Build Triggers:
  ✅ Build after other projects are built
  Projects to watch: CI-Pipeline-Job-Name
  Trigger: Trigger only if build is stable
```

### What Happens

```
Developer: git push
    │
    ▼
GitHub Webhook fires → Jenkins CI job starts
    │
    ▼
CI Pipeline runs all stages
    │
    ▼
CI Pipeline succeeds ✅
    │
    ▼  (automatic trigger)
CD Pipeline starts
    │
    ▼
New container running on port 3000
```

### GitHub Webhook Setup (Optional but Recommended)

```
GitHub Repo → Settings → Webhooks → Add webhook

Payload URL: http://<EC2-IP>:8080/github-webhook/
Content type: application/json
Events: Just the push event
```

Without webhook, Jenkins uses **Poll SCM** (checks GitHub every N minutes). Webhooks are instant.

---

## 10. Advanced Scenarios

### Scenario A: Private Docker Registry

While public images can be pulled directly without authentication, private repositories require setting up a Docker login credential step in Jenkins prior to pulling. If your Docker Hub repo is **private**, consumers (EC2, Kubernetes, etc.) must login before pulling:

```groovy
// In CD pipeline, add login before pull
stage('Docker Login') {
  steps {
    withCredentials([usernamePassword(
      credentialsId: 'docker-hub-creds',
      usernameVariable: 'DOCKER_USER',
      passwordVariable: 'DOCKER_PASS'
    )]) {
      sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
    }
  }
}
```

### Scenario B: Deploy to a Remote VM via SSH

In real-time projects, the deployment target is often a separate virtual machine. This requires Jenkins to have SSH connectivity to the remote host to run the deployment scripts. If Jenkins runs on Server A but you want to deploy the container on Server B:

```groovy
// Install SSH Agent plugin in Jenkins first
// Add SSH private key in Jenkins credentials (type: SSH Username with private key)

stage('Deploy to Remote VM') {
  steps {
    sshagent(['remote-server-ssh-key']) {
      sh """
        ssh -o StrictHostKeyChecking=no ubuntu@<REMOTE-IP> '
          docker stop app-container || true
          docker rm app-container || true
          docker pull yourusername/starbucks-app:latest
          docker run -d --name app-container -p 3000:3000 yourusername/starbucks-app:latest
        '
      """
    }
  }
}
```

### Scenario C: Parameterized Builds (Multi-Environment)

Using parameters in Jenkins allows a single pipeline definition to dynamically target multiple environments (such as dev, QA, and prod) by mapping parameters to the respective environment configurations. Deploy to Dev, QA, or Prod based on a parameter the user picks when triggering the pipeline:

```groovy
pipeline {
  agent any

  parameters {
    choice(
      name: 'ENVIRONMENT',
      choices: ['dev', 'qa', 'prod'],
      description: 'Select deployment environment'
    )
    string(
      name: 'IMAGE_TAG',
      defaultValue: 'latest',
      description: 'Docker image tag to deploy'
    )
  }

  stages {
    stage('Deploy') {
      steps {
        script {
          def serverIP = [
            'dev':  '10.0.1.10',
            'qa':   '10.0.1.20',
            'prod': '10.0.1.30'
          ]
          def targetIP = serverIP[params.ENVIRONMENT]
          echo "Deploying ${params.IMAGE_TAG} to ${params.ENVIRONMENT} at ${targetIP}"

          sshagent(['remote-ssh-key']) {
            sh """
              ssh ubuntu@${targetIP} '
                docker pull yourusername/app:${params.IMAGE_TAG}
                docker stop app || true
                docker rm app || true
                docker run -d --name app -p 3000:3000 yourusername/app:${params.IMAGE_TAG}
              '
            """
          }
        }
      }
    }
  }
}

### Operational & Troubleshooting Guidelines
- **Initial Build Overhead:** The first execution of the build pipeline may take longer to pull base Docker images and install npm packages. Subsequent builds benefit from cached layers and dependencies.
- **Common Pipeline Failure Points:**
  - Incorrect branch name configured in SCM settings (e.g., `master` vs `main`).
  - Missing or misconfigured Docker Hub credentials in Jenkins.
  - Incorrect Docker image path or repository names.
  - Syntactical errors in the Jenkinsfile.
  - Mismatched tool versions (e.g., node, Java) between Jenkins global settings and the application code.
- **Key Advice:** Practice the setup steps repeatedly and consult the build console output logs to pinpoint issues.

---

## 11. Tech Stack Mapping

### Full Architecture: Code to Running App

```
┌─────────────────────────────────────────────────────────────────────┐
│                     DEVELOPER'S MACHINE                             │
│  Starbucks Next.js App                                              │
│  ├── pages/                                                         │
│  ├── components/                                                    │
│  ├── package.json                                                   │
│  ├── Dockerfile                                                     │
│  └── Jenkinsfile                                                    │
└────────────────────┬────────────────────────────────────────────────┘
                     │ git push
                     ▼
┌────────────────────────────────┐
│         GitHub Repository      │
│  Branch: main                  │
│  Webhook → triggers Jenkins    │
└──────────────┬─────────────────┘
               │ webhook
               ▼
┌──────────────────────────────────────────────────────────────┐
│              AWS EC2 (t3.large, Ubuntu, Mumbai)              │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │               Jenkins (port 8080)                   │    │
│  │                                                     │    │
│  │  CI Job:                      CD Job:               │    │
│  │  1. git clone                 1. docker stop        │    │
│  │  2. npm install               2. docker rm          │    │
│  │  3. npm build                 3. docker pull        │    │
│  │  4. docker build              4. docker run         │    │
│  │  5. docker push ──────────────────────────────┐    │    │
│  └─────────────────────────────────────────────┐ │    │    │
│                                                │ │    │    │
│  ┌──────────────────────┐                      │ │    │    │
│  │ App Container        │◄─────────────────────┘ │    │    │
│  │ starbucks-container  │                         │    │    │
│  │ port 3000            │                         │    │    │
│  └──────────────────────┘                         │    │    │
└──────────────────────────────────────────────┐    │    │    │
                                               │    │    │    │
                                               ▼    │    │    │
                              ┌─────────────────────────────┐ │
                              │        Docker Hub            │ │
                              │  yourusername/starbucks-app  │ │
                              │  :latest, :42, :41, ...      │ │
                              └─────────────────────────────┘ │
                                                              │
                         User's Browser: http://<IP>:3000 ◄──┘
```

### Node.js App Dockerfile (Production-Grade)

```dockerfile
# ── Stage 1: Build ──────────────────────────────────────────
FROM node:16-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# ── Stage 2: Run ────────────────────────────────────────────
FROM node:16-alpine AS runner

WORKDIR /app
ENV NODE_ENV=production

# Only copy what's needed to run
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

EXPOSE 3000
CMD ["node_modules/.bin/next", "start"]
```

**Why multi-stage?** The builder stage has all dev tools, source code, etc. The final image only has what's needed to *run* the app — smaller, more secure image.

### Jenkins + AWS Integration Pattern

```
Jenkins (EC2)
    │
    ├── Reads secrets from: Jenkins Credentials Store
    │   (Docker Hub login, SSH keys, AWS access keys)
    │
    ├── Builds Docker image locally
    │
    ├── Pushes to Docker Hub (public registry)
    │   OR ECR (AWS Elastic Container Registry — private)
    │
    └── Deploys via:
        ├── docker run (same EC2)
        ├── SSH to remote EC2
        ├── kubectl apply (EKS)
        └── aws ecs update-service (ECS Fargate)
```

### Using AWS ECR Instead of Docker Hub

```bash
# Authenticate to ECR
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS \
  --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com

# Tag image for ECR
docker tag starbucks-app:latest \
  <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/starbucks-app:latest

# Push to ECR
docker push \
  <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/starbucks-app:latest
```

In Jenkinsfile:

```groovy
environment {
  ECR_REGISTRY = '<ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com'
  IMAGE_NAME    = 'starbucks-app'
}

stage('Push to ECR') {
  steps {
    withAWS(credentials: 'aws-jenkins-creds', region: 'ap-south-1') {
      sh """
        aws ecr get-login-password | docker login --username AWS \
          --password-stdin ${ECR_REGISTRY}
        docker push ${ECR_REGISTRY}/${IMAGE_NAME}:latest
      """
    }
  }
}
```

### MongoDB + Node.js in Docker Compose (Local Dev)

```yaml
# docker-compose.yml — local development
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - MONGO_URI=mongodb://mongo:27017/starbucks
    depends_on:
      - mongo

  mongo:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

### Redis for Session Caching

```javascript
// In Node.js app: use Redis to cache session/auth tokens
const redis = require('redis');
const client = redis.createClient({ url: process.env.REDIS_URL });

// Cache menu data for 5 minutes
await client.setEx('menu:featured', 300, JSON.stringify(menuData));
```

In Docker run (CD pipeline):

```bash
docker run -d \
  --name starbucks-container \
  -p 3000:3000 \
  -e MONGO_URI=mongodb://mongo-host:27017/starbucks \
  -e REDIS_URL=redis://redis-host:6379 \
  yourusername/starbucks-app:latest
```

---

## 12. Scenario-Based Q&A

---

🔍 **Scenario 1:** A developer pushes broken code. The npm build fails. How does Jenkins handle it?

✅ **Answer:** The CI pipeline stage `Build Application` (`npm run build`) will fail. Jenkins marks the build as **FAILED** (red). The `post { failure { } }` block runs — you can send a Slack/email notification. The CD pipeline is **not triggered** because CI didn't succeed. The old container keeps running — no bad code reaches users.

---

🔍 **Scenario 2:** Your Docker Hub repo is private. The CD pipeline runs `docker pull` but fails with "unauthorized."

✅ **Answer:** Add a Docker login step before the pull in the CD pipeline. Store Docker Hub credentials in Jenkins Credentials with ID `docker-hub-creds`. Use `withCredentials` block to inject username/password at runtime and run `docker login` before `docker pull`. Never hardcode credentials in the Jenkinsfile.

---

🔍 **Scenario 3:** Jenkins and the app server are different machines. How does Jenkins deploy to the remote server?

✅ **Answer:** Install the **SSH Agent plugin** in Jenkins. Store the remote server's SSH private key in Jenkins Credentials (type: SSH Username with private key). In the CD pipeline, use `sshagent(['key-id'])` block and run `ssh ubuntu@<REMOTE-IP> 'docker run ...'` to execute commands on the remote server.

---

🔍 **Scenario 4:** Your team has Dev, QA, and Prod environments. How do you deploy to the right one?

✅ **Answer:** Use **Parameterized Builds** in Jenkins. Add a `choice` parameter called `ENVIRONMENT`. When triggering the build, the user selects Dev/QA/Prod. The pipeline maps each environment to its server IP and deploys accordingly. This way, one Jenkinsfile handles all environments.

---

🔍 **Scenario 5:** The EC2 instance reboots due to AWS maintenance. Will the app restart automatically?

✅ **Answer:** Yes, if you used `--restart unless-stopped` in the `docker run` command. Docker daemon starts on boot (because of `systemctl enable docker`), and Docker automatically restarts containers with this policy. The app is back up without manual intervention.

---

🔍 **Scenario 6:** Your manager asks "what's the difference between what we do (Delivery) and full Continuous Deployment?"

✅ **Answer:** In **Continuous Delivery**, the pipeline automates everything up to the point of deployment, but a human (after CAB approval / Change Request process) clicks the final deploy button. In **Continuous Deployment**, the pipeline goes all the way to production automatically — no human touch. Regulated industries (banking, healthcare) usually require Continuous Delivery with audit trails (CRs), while startups and tech companies often use full Continuous Deployment.

---

## 13. Interview Q&A

---

**Q1. What is the difference between Continuous Delivery and Continuous Deployment?**

**A:** Both automate the build and test phases. The difference is the final step. In **Continuous Delivery**, a human approves and triggers the production deployment — common in enterprises with Change Advisory Boards (CAB) and Change Request (CR) processes for compliance. In **Continuous Deployment**, production deployment is fully automated — every successful build automatically goes live. The choice depends on regulatory requirements and organizational risk tolerance.

---

**Q2. What is the difference between Declarative and Scripted Jenkinsfile?**

**A:** Declarative uses a structured `pipeline { }` block with predefined sections (`stages`, `steps`, `post`) — easier to read, less flexible. Scripted uses `node { }` and is pure Groovy code — maximum flexibility but harder to read and maintain. Declarative is the recommended approach for standard CI/CD. Scripted is used when you need complex logic like loops, dynamic stage creation, or error handling with try/catch that Declarative's `post` block can't handle. In the class demo, we used Declarative for CI (build/push) and Scripted for CD (container management).

---

**Q3. How does the CD pipeline get auto-triggered after CI in Jenkins?**

**A:** In the CD pipeline's configuration, under **Build Triggers**, enable "Build after other projects are built" and specify the CI pipeline's job name. Set it to trigger only when the CI build is stable (green). This way, every time CI succeeds, Jenkins automatically queues and starts the CD job. An alternative is to use Jenkins Pipeline's `build job: 'CD-Job-Name'` step at the end of the CI Jenkinsfile for tighter control.

---

**Q4. Why do we use `docker stop || true` and `docker rm || true` in the CD pipeline?**

**A:** On the very first deployment, no container exists yet. Running `docker stop non-existent-container` would return a non-zero exit code, which Jenkins interprets as a pipeline failure. Appending `|| true` tells the shell: "if this command fails, treat it as success and continue." This makes the pipeline **idempotent** — it works correctly whether it's the first run or the 100th run.

---

**Q5. How do you securely store and use credentials (Docker Hub password) in Jenkins?**

**A:** Store credentials in **Jenkins Credentials Store** (Manage Jenkins → Credentials) as "Username with password" type with a unique ID. Never hardcode passwords in Jenkinsfile. In the pipeline, use `docker.withRegistry('url', 'credential-id')` for Docker operations, or `withCredentials([usernamePassword(credentialsId: 'id', usernameVariable: 'USER', passwordVariable: 'PASS')])` for shell commands. Jenkins injects credentials as environment variables at runtime and masks them in build logs.

---

**Q6. Why do we add the `jenkins` user to the `docker` group?**

**A:** Jenkins runs pipeline commands as the `jenkins` OS user. Docker by default requires root or `docker` group membership to run commands (`docker build`, `docker run`, etc.). Without adding `jenkins` to the `docker` group, every Docker command in the pipeline fails with "permission denied on /var/run/docker.sock." After `usermod -aG docker jenkins`, we must restart Jenkins for the group change to take effect.

---

**Q7. What is the role of Docker Hub in this CI/CD pipeline?**

**A:** Docker Hub acts as the **artifact registry** — the central store for Docker images. CI builds the image and pushes it to Docker Hub. CD pulls that image from Docker Hub and runs it. This decouples the build server from the deployment server. The deployment server doesn't need the source code or build tools — it only needs Docker and the image name. This also enables deploying to multiple servers simultaneously (all pull the same image).

---

**Q8. How would you deploy to AWS ECS or EKS instead of a plain EC2 container?**

**A:** For **ECS**: After pushing the image to ECR, use `aws ecs update-service --force-new-deployment` in the CD pipeline. ECS pulls the new image and does a rolling replacement of tasks. For **EKS (Kubernetes)**: Update the deployment's image tag with `kubectl set image deployment/app app=<new-image>:tag`. Jenkins needs AWS credentials (IAM role or access key) and `kubectl` configured. The image is pulled from ECR (private) or Docker Hub (public). Both ECS and EKS handle zero-downtime deployments automatically.

---

**Q9. How would you make this pipeline production-grade?**

**A:** Several improvements:
- Add **automated tests** stage (unit tests with Jest, integration tests) before building Docker image — fail fast
- Use **semantic versioning** for image tags (`1.2.3`) instead of just `latest` or build number
- Add **Docker image vulnerability scanning** (Trivy, Snyk) stage
- Use **AWS ECR** (private) instead of Docker Hub
- Add **Slack/email notifications** on success/failure
- Implement **blue-green or canary deployment** for zero-downtime releases
- Use **Jenkins shared libraries** to avoid duplicating Jenkinsfile logic across repos
- Add **environment-specific configurations** via Jenkins parameters or config files

---

## 14. Quick Reference Cheatsheet

### EC2 Setup

```bash
# SSH
chmod 400 key.pem
ssh -i key.pem ubuntu@<IP>

# Ports to open in Security Group
22    → SSH
8080  → Jenkins
3000  → Node.js App
```

### Jenkins Install

```bash
sudo apt update
sudo apt install fontconfig openjdk-17-jre -y
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/" | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update && sudo apt-get install jenkins -y
sudo systemctl start jenkins && sudo systemctl enable jenkins
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### Docker Install + Jenkins Permission

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
sudo systemctl start docker && sudo systemctl enable docker
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Key Docker Commands (CD Pipeline)

```bash
docker stop container-name  || true   # Stop (ignore if not running)
docker rm container-name    || true   # Remove (ignore if not exists)
docker pull image:tag                 # Pull latest image
docker run -d \
  --name container-name \
  -p 3000:3000 \
  --restart unless-stopped \
  image:tag                           # Run container
docker ps                             # List running containers
docker logs container-name            # View container logs
```

### Jenkins Credentials Reference

```groovy
// Docker registry login
docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-creds') {
  dockerImage.push('latest')
}

// Generic username/password
withCredentials([usernamePassword(
  credentialsId: 'docker-hub-creds',
  usernameVariable: 'DOCKER_USER',
  passwordVariable: 'DOCKER_PASS'
)]) {
  sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
}

// SSH key for remote deploy
sshagent(['remote-server-ssh-key']) {
  sh 'ssh ubuntu@<IP> "docker pull image:latest && docker run -d ..."'
}
```

### Pipeline Trigger (auto CD after CI)

```
CD Job → Configure → Build Triggers
→ ✅ Build after other projects are built
→ Projects: CI-Job-Name
→ Trigger: Trigger only if build is stable
```

## 15. Career & Interview Strategy

### Job Opportunity Context
During the session, the instructor shared a DevOps Engineer role in Bangalore, Karnataka, emphasizing the demand for professionals with skills in:
- **Monitoring & Observability:** ELK, Prometheus, Grafana
- **Infrastructure as Code (IaC) & Configuration Management:** Terraform, Ansible
- **Containerization & Scripting:** Docker, Python, PowerShell
- **Troubleshooting & Infrastructure Management**

*Note:* A CGI referral opportunity was discussed, encouraging applicants to leverage referral emails through the company portal or HR processes.

### Framing this Project in Interviews
This Node.js + Jenkins + Docker + AWS project should be described as a core part of your DevOps engineering responsibilities. When explaining it, focus on:
- **Pipeline Architecture:** End-to-end setup of Jenkins pipelines (Declarative for CI, Scripted for CD).
- **Secret Management:** Secure handling of Docker Hub and registry credentials.
- **Containerization:** Authoring production-grade multi-stage Dockerfiles and managing images.
- **Deployment Automation:** Implementing automated trigger linkage and environment deployment.
- **Troubleshooting:** Diagnosing and resolving pipeline errors, credential misconfigurations, or tool version mismatches.

---

## Navigation Footer

← Previous: [`54_Kafka_on_Kubernetes_using_Strimzi_Operator.md`](54_Kafka_on_Kubernetes_using_Strimzi_Operator.md) | Next: [`56_DevSecOps_Jenkins_Trivy_SonarQube_on_AWS.md`](56_DevSecOps_Jenkins_Trivy_SonarQube_on_AWS.md) →
