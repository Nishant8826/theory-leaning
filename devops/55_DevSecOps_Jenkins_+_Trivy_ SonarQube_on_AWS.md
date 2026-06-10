# 55 – DevSecOps: Jenkins + Trivy + SonarQube on AWS

---

## Table of Contents

1. [DevOps vs DevSecOps vs SRE](#1-devops-vs-devsecops-vs-sre)
2. [Why DevSecOps?](#2-why-devsecops)
3. [Core Tools Overview](#3-core-tools-overview)
4. [SonarQube – Code Quality & Security Analysis](#4-sonarqube--code-quality--security-analysis)
5. [Trivy – Container Image Vulnerability Scanner](#5-trivy--container-image-vulnerability-scanner)
6. [Infrastructure Setup on AWS EC2](#6-infrastructure-setup-on-aws-ec2)
7. [Software Installation](#7-software-installation)
8. [SonarQube Configuration](#8-sonarqube-configuration)
9. [Jenkins Configuration & Integration](#9-jenkins-configuration--integration)
10. [Full DevSecOps Pipeline](#10-full-devsecops-pipeline)
11. [Three-Tier Application Deployment](#11-three-tier-application-deployment)
12. [Reading Pipeline Results](#12-reading-pipeline-results)
13. [Tech Stack Mapping](#13-tech-stack-mapping)
14. [Interview Project Walkthrough Script](#14-interview-project-walkthrough-script)
15. [Scenario-Based Q&A](#15-scenario-based-qa)
16. [Interview Q&A](#16-interview-qa)
17. [Quick Reference Cheatsheet](#17-quick-reference-cheatsheet)

---

## 1. DevOps vs DevSecOps vs SRE

### What

| Role | Full Form | Core Focus |
|---|---|---|
| **DevOps** | Development + Operations | Automate build, test, deploy pipelines; faster delivery |
| **DevSecOps** | Development + Security + Operations | Everything DevOps does + security checks baked into every stage |
| **SRE** | Site Reliability Engineering | Operations-heavy; reliability, uptime, SLOs, incident response |

### The Key Difference — Where Security Lives

```
Traditional DevOps:
  Code → Build → Test → Deploy → 🔥 Security issue found in production → Fix

DevSecOps (Shift Left):
  Code → 🔍 SAST → Build → 🔍 Image Scan → Test → Deploy → ✅ Already secure
```

**"Shift Left"** means moving security checks earlier in the pipeline — to the left of the timeline — catching vulnerabilities before they ever reach production.

### SRE vs DevSecOps
- **SRE** asks: "Is the system running reliably? What's the error rate? Is our SLO met?"
- **DevSecOps** asks: "Is the code secure? Does the image have CVEs? Are there code smells?"
- In large orgs, DevSecOps owns the pipeline security; SRE owns production reliability.

### Impact

| Without DevSecOps | With DevSecOps |
|---|---|
| Vulnerabilities discovered in production | Caught in pipeline before deployment |
| Security team is a separate, late-stage gate | Security is automated, continuous, everyone's responsibility |
| Expensive to fix (production bugs cost 100x more) | Cheap to fix (caught during development) |
| Compliance failures, data breaches | Audit trails, enforced quality gates |

---

## 2. Why DevSecOps?

### The Cost of Late Security Fixes

```
Stage where bug is found    →    Cost to fix
─────────────────────────────────────────────
Development (your laptop)   →    $1
CI Pipeline                 →    $10
Staging                     →    $100
Production                  →    $1,000+
After a breach              →    $1,000,000+
```

The earlier you catch it, the cheaper it is to fix. That's the entire business case for DevSecOps.

### What DevSecOps Brings
- **Faster releases** — no security bottleneck at the end; checks are automated
- **Vulnerability-free deployments** — images are scanned before they run
- **Code quality gates** — bad code can't merge if SonarQube fails
- **Reduced production failures** — cleaner code, safer images
- **Compliance** — automatic audit trails for security scans

---

## 3. Core Tools Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    DevSecOps Tool Stack                      │
│                                                             │
│  Jenkins (8080)   →  CI/CD Orchestration                   │
│  SonarQube (9000) →  Static Code Analysis (SAST)           │
│  Trivy             →  Container Image Scanning (SCA/CVE)   │
│  Docker            →  Containerization                      │
│  GitHub            →  Source Code Repository               │
│  Docker Hub        →  Container Image Registry             │
└─────────────────────────────────────────────────────────────┘
```

| Tool | Type | What it checks | Runs on |
|---|---|---|---|
| **Jenkins** | CI/CD | Pipeline orchestration | Port 8080 |
| **SonarQube** | SAST | Source code — bugs, smells, duplications, security | Port 9000 |
| **Trivy** | Image Scanner | Docker image — CVEs, misconfigs, secrets | CLI tool |
| **Docker** | Container runtime | Packages and runs the app | Port varies |

---

## 4. SonarQube – Code Quality & Security Analysis

### What
SonarQube is a **Static Application Security Testing (SAST)** tool. It analyzes your **source code** (before it even runs) and finds:
- **Bugs** — code that will likely cause errors at runtime
- **Vulnerabilities** — security weaknesses (e.g., SQL injection risk, hardcoded passwords)
- **Code Smells** — bad practices that make code hard to maintain
- **Duplications** — copy-pasted code blocks
- **Coverage** — how much of the code is covered by tests

### Why
Without SonarQube, a developer might write code that has a SQL injection vulnerability or a null pointer bug — and nobody notices until a customer reports it (or worse, a hacker exploits it). SonarQube catches these automatically before the code reaches production.

### How SonarQube Works

```
Source Code (GitHub)
      │
      │  Jenkins runs SonarQube Scanner
      ▼
SonarQube Scanner (plugin)
      │
      │  Analyzes code files
      ▼
SonarQube Server (Docker, port 9000)
      │
      │  Generates report
      ▼
Quality Gate
  ├── PASSED → Pipeline continues
  └── FAILED → Pipeline stops ❌ (developer must fix issues)
```

### SonarQube Quality Gate
A **Quality Gate** is a pass/fail threshold you define. Example:
- No new bugs allowed
- Code coverage must be ≥ 80%
- No critical vulnerabilities

If the gate fails, Jenkins (via webhook) is notified and the pipeline stops.

### Impact

| With SonarQube | Without SonarQube |
|---|---|
| Bugs caught before merging | Bugs found in production |
| Consistent code standards enforced | Code quality degrades over time |
| Security vulnerabilities flagged automatically | Security issues discovered by attackers |
| Technical debt tracked and managed | Technical debt grows silently |

### SonarQube Dashboard — What You'll See

```
Project Dashboard:
  Bugs:           5        ← must be fixed
  Vulnerabilities: 2
  Code Smells:    23       ← code quality issues
  Duplications:   8.3%
  Coverage:       64.2%
  Quality Gate:   ❌ FAILED  (or ✅ PASSED)
```

---

## 5. Trivy – Container Image Vulnerability Scanner

### What
Trivy is an open-source **vulnerability scanner** for Docker images. It scans the image's OS packages, application dependencies, and configuration files for known **CVEs (Common Vulnerabilities and Exposures)**.

### Why
Just because your code is clean doesn't mean your container is safe. The base image (`node:16`, `python:3.9`) might contain hundreds of OS-level vulnerabilities. Trivy catches these before you push the image to production.

### How Trivy Works

```
docker build → image created locally
      │
      ▼
trivy image yourusername/app:latest
      │
      │  Trivy pulls vulnerability database (CVE db)
      │  Scans all layers of the image:
      │    - OS packages (apt, apk, yum)
      │    - Language packages (npm, pip, gems)
      │    - Misconfigurations
      ▼
Report:
  CRITICAL: 2  ← must fix (remote code execution, privilege escalation)
  HIGH:     8
  MEDIUM:   15
  LOW:      42
  UNKNOWN:  3
```

### Severity Levels

| Level | Meaning | Action |
|---|---|---|
| CRITICAL | Remote code execution, full system compromise possible | Block deployment immediately |
| HIGH | Significant data breach risk | Fix before next release |
| MEDIUM | Limited impact | Fix in sprint |
| LOW | Minimal risk | Track and fix eventually |

### Trivy in Jenkins Pipeline

```groovy
stage('Trivy Image Scan') {
  steps {
    sh 'trivy image --exit-code 1 --severity CRITICAL yourusername/app:latest'
    // --exit-code 1: pipeline fails if CRITICAL CVEs found
    // --severity CRITICAL: only fail on CRITICAL issues
  }
}
```

### Impact

| With Trivy | Without Trivy |
|---|---|
| Known CVEs caught before deployment | Vulnerable images running in production |
| Base image vulnerabilities surfaced | "It's not our code" blindspot exploited |
| Compliance (PCI-DSS, SOC2) requirements met | Audit failures |
| Automated, runs in seconds | Manual security review takes days |

---

## 6. Infrastructure Setup on AWS EC2

### EC2 Launch Settings

```
AWS Console → EC2 → Launch Instance

Name:           devsecops-server
AMI:            Ubuntu 22.04 LTS
Instance type:  t2.large  (2 vCPU, 8GB RAM)
                ↑ SonarQube alone needs 2GB RAM minimum
Storage:        50 GB gp3
Region:         Mumbai (ap-south-1) or your preferred region
Key pair:       Create/select → download .pem
```

### Security Group — Inbound Rules

| Port | Protocol | Purpose | Why Needed |
|---|---|---|---|
| 22 | TCP | SSH access | Connect to server |
| 8080 | TCP | Jenkins UI | Access Jenkins from browser |
| 9000 | TCP | SonarQube UI | Access SonarQube from browser |
| 3000 | TCP | Frontend App | Access web frontend |
| 5000 | TCP | App Server (Python/Node) | API layer |
| 25 | TCP | SMTP (email notifications) | Jenkins email alerts |

**Why t2.large?** SonarQube requires minimum 2GB RAM. Jenkins needs ~1GB. Running both on t2.micro (1GB total) causes constant OOM crashes.

### Connect to EC2

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

---

## 7. Software Installation

### Install Everything via Shell Script

```bash
#!/bin/bash
# devsecops-install.sh

set -e  # exit on any error

echo "=== Updating packages ==="
sudo apt update -y

echo "=== Installing Java (Jenkins requires it) ==="
sudo apt install fontconfig openjdk-17-jre -y
java -version

echo "=== Installing Jenkins ==="
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/" | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins -y
sudo systemctl start jenkins
sudo systemctl enable jenkins

echo "=== Installing Docker ==="
sudo apt-get install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
sudo systemctl start docker
sudo systemctl enable docker

echo "=== Giving Jenkins permission to run Docker ==="
sudo usermod -aG docker jenkins
sudo usermod -aG docker ubuntu

echo "=== Installing Python ==="
sudo apt install python3 python3-pip -y

echo "=== Installing Trivy ==="
sudo apt-get install wget apt-transport-https gnupg lsb-release -y
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | \
  sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb \
  $(lsb_release -sc) main" | \
  sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy -y

echo "=== Restarting Jenkins ==="
sudo systemctl restart jenkins

echo "=== Jenkins Initial Password ==="
sudo cat /var/lib/jenkins/secrets/initialAdminPassword

echo "✅ All installations complete!"
```

### Run the Script

```bash
chmod +x devsecops-install.sh
./devsecops-install.sh
```

### Verify All Tools

```bash
java -version          # OpenJDK 17
jenkins --version      # or check port 8080
docker --version       # Docker 24.x
python3 --version      # Python 3.x
trivy --version        # Trivy 0.x
```

---

## 8. SonarQube Configuration

### Run SonarQube as Docker Container

```bash
# SonarQube needs at least 512MB RAM allocated to Elasticsearch
docker run -d \
  --name sonarqube \
  -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube:lts-community
```

### Access SonarQube

```
Browser → http://<EC2-IP>:9000

Default credentials:
  Username: admin
  Password: admin
  (You'll be asked to change password on first login)
```

### Generate Authentication Token

```
SonarQube UI:
  Top-right → My Account → Security → Generate Token

  Name: jenkins-token
  Type: Global Analysis Token
  Expires: No expiration (or set as per policy)

  → Generate → COPY THE TOKEN (shown only once!)
  Example: squ_abc123def456ghi789...
```

**Why a token?** Instead of username/password in Jenkins, a token is more secure — it can be revoked without changing the password, and has specific permissions.

### Create SonarQube Webhook (back-trigger to Jenkins)

```
SonarQube UI:
  Administration → Configuration → Webhooks → Create

  Name:   Jenkins
  URL:    http://<EC2-IP>:8080/sonarqube-webhook/
  Secret: (leave empty for now)

  → Create
```

**Why the webhook?** After SonarQube finishes analysis, it calls this URL to notify Jenkins of the Quality Gate result. Jenkins waits (using `waitForQualityGate()`) for this callback before proceeding.

---

## 9. Jenkins Configuration & Integration

### Step 1: Install Required Plugins

```
Manage Jenkins → Plugins → Available

Install:
  ✅ SonarQube Scanner
  ✅ Docker
  ✅ Docker Pipeline
  ✅ Pipeline Stage View   ← visual stage view in Jenkins
  ✅ SSH Agent             ← for remote deployments
```

### Step 2: Add SonarQube Token to Jenkins Credentials

```
Manage Jenkins → Credentials → System → Global → Add Credential

Kind:        Secret text
Secret:      squ_abc123def456ghi789...  (paste token from SonarQube)
ID:          sonar-token
Description: SonarQube Authentication Token
```

### Step 3: Configure SonarQube Server in Jenkins

```
Manage Jenkins → System → SonarQube Servers

  ✅ Enable injection of SonarQube server configuration
  
  Add SonarQube:
    Name:              SonarQube
    Server URL:        http://<EC2-IP>:9000
    Server auth token: sonar-token  (select from credentials)
```

### Step 4: Configure SonarQube Scanner Tool

```
Manage Jenkins → Tools → SonarQube Scanner

  Add SonarQube Scanner:
    Name:                   sonar-scanner
    Install automatically:  ✅
    Version:                SonarQube Scanner 5.x
```

### Step 5: Add Docker Hub Credentials

```
Manage Jenkins → Credentials → System → Global → Add Credential

Kind:        Username with password
Username:    your-dockerhub-username
Password:    your-dockerhub-token
ID:          docker-hub-creds
```

---

## 10. Full DevSecOps Pipeline

### Pipeline Architecture (Visual)

```
Developer: git push
    │
    ▼
GitHub Repository
    │
    │ Jenkins polls / webhook
    ▼
┌──────────────────────────────────────────────────────────────┐
│                  Jenkins Pipeline                            │
│                                                              │
│  Stage 1: Git Checkout                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Clone repo from GitHub                             │    │
│  └───────────────────────────┬─────────────────────────┘    │
│                              │                               │
│  Stage 2: Build              ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  npm install / pip install / mvn package             │    │
│  └───────────────────────────┬─────────────────────────┘    │
│                              │                               │
│  Stage 3: SonarQube Analysis ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  sonar-scanner → sends to SonarQube server          │    │
│  │  Jenkins waits for Quality Gate callback            │    │
│  │  PASS → continue │ FAIL → pipeline stops ❌         │    │
│  └───────────────────────────┬─────────────────────────┘    │
│                              │                               │
│  Stage 4: Docker Build       ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  docker build -t username/app:tag .                 │    │
│  └───────────────────────────┬─────────────────────────┘    │
│                              │                               │
│  Stage 5: Trivy Image Scan   ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  trivy image username/app:tag                       │    │
│  │  CRITICAL found → fail │ PASS → continue            │    │
│  └───────────────────────────┬─────────────────────────┘    │
│                              │                               │
│  Stage 6: Docker Push        ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  docker push to Docker Hub / ECR                    │    │
│  └───────────────────────────┬─────────────────────────┘    │
│                              │                               │
│  Stage 7: Deploy             ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  docker-compose up / kubectl apply / docker run     │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
App running + SonarQube report + Trivy report generated
```

### Full Jenkinsfile (Declarative — DevSecOps)

```groovy
pipeline {
  agent any

  tools {
    jdk 'jdk17'
    nodejs 'nodejs16'
  }

  environment {
    SONAR_HOME       = tool 'sonar-scanner'
    DOCKER_IMAGE     = 'yourusername/three-tier-app'
    DOCKER_TAG       = "${BUILD_NUMBER}"
    CONTAINER_NAME   = 'three-tier-container'
  }

  stages {

    // ── Stage 1: Code Checkout ──────────────────────────────
    stage('Git Checkout') {
      steps {
        git branch: 'main',
            url: 'https://github.com/your-username/three-tier-app.git'
        echo "✅ Code checked out from GitHub"
      }
    }

    // ── Stage 2: Install Dependencies ──────────────────────
    stage('Install Dependencies') {
      steps {
        sh 'npm install'
        echo "✅ Dependencies installed"
      }
    }

    // ── Stage 3: SonarQube Code Analysis ───────────────────
    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv('SonarQube') {   // matches name in Jenkins System config
          sh """
            ${SONAR_HOME}/bin/sonar-scanner \
              -Dsonar.projectKey=three-tier-app \
              -Dsonar.projectName='Three Tier App' \
              -Dsonar.sources=. \
              -Dsonar.exclusions=**/node_modules/**,**/dist/**
          """
        }
      }
    }

    // ── Stage 4: SonarQube Quality Gate ────────────────────
    stage('Quality Gate') {
      steps {
        timeout(time: 2, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
          // abortPipeline: true → pipeline stops if gate FAILS
        }
      }
    }

    // ── Stage 5: Build Docker Image ────────────────────────
    stage('Build Docker Image') {
      steps {
        script {
          dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
          echo "✅ Docker image built: ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }
      }
    }

    // ── Stage 6: Trivy Image Scan ──────────────────────────
    stage('Trivy Image Scan') {
      steps {
        sh """
          trivy image \
            --format table \
            --output trivy-report.txt \
            --severity HIGH,CRITICAL \
            ${DOCKER_IMAGE}:${DOCKER_TAG}
        """
        // Archive the report as Jenkins artifact
        archiveArtifacts artifacts: 'trivy-report.txt', allowEmptyArchive: true
        echo "✅ Trivy scan complete — report saved"
      }
    }

    // ── Stage 7: Push to Docker Hub ────────────────────────
    stage('Push Docker Image') {
      steps {
        script {
          docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-creds') {
            dockerImage.push("${DOCKER_TAG}")
            dockerImage.push('latest')
          }
          echo "✅ Image pushed to Docker Hub"
        }
      }
    }

    // ── Stage 8: Deploy Application ────────────────────────
    stage('Deploy') {
      steps {
        sh """
          docker stop ${CONTAINER_NAME} || true
          docker rm ${CONTAINER_NAME}   || true
          docker run -d \
            --name ${CONTAINER_NAME} \
            -p 3000:3000 \
            --restart unless-stopped \
            ${DOCKER_IMAGE}:latest
        """
        echo "✅ Application deployed at port 3000"
      }
    }

  }

  post {
    always {
      echo "Pipeline completed — check SonarQube and Trivy reports"
    }
    success {
      echo "✅ DevSecOps pipeline PASSED — app is live and secure!"
    }
    failure {
      echo "❌ Pipeline FAILED — check stage logs, SonarQube, and Trivy output"
    }
  }
}
```

---

## 11. Three-Tier Application Deployment

### What is a Three-Tier Application?

```
┌──────────────────────────────────────────────────────────┐
│               Three-Tier Architecture                     │
│                                                          │
│  Tier 1: Frontend  (React / HTML/CSS/JS)                 │
│          Port 3000                                       │
│          What user sees in browser                       │
│               │                                          │
│               │ HTTP API calls                           │
│               ▼                                          │
│  Tier 2: Application Server  (Node.js / Python Flask)    │
│          Port 5000                                       │
│          Business logic, authentication, API             │
│               │                                          │
│               │ SQL queries                              │
│               ▼                                          │
│  Tier 3: Database  (MySQL)                               │
│          Port 3306                                       │
│          Persistent data storage                         │
└──────────────────────────────────────────────────────────┘
```

### Docker Compose for Three-Tier App

```yaml
# docker-compose.yml
version: '3.8'

services:

  # Tier 3: Database
  db:
    image: mysql:8.0
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: appdb
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppass
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Tier 2: Application Server
  backend:
    build: ./backend
    container_name: app-server
    ports:
      - "5000:5000"
    environment:
      DB_HOST: db
      DB_USER: appuser
      DB_PASS: apppass
      DB_NAME: appdb
    depends_on:
      db:
        condition: service_healthy

  # Tier 1: Frontend
  frontend:
    build: ./frontend
    container_name: frontend-app
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://<EC2-IP>:5000
    depends_on:
      - backend

volumes:
  mysql-data:
```

### Deploy with Docker Compose

```bash
# Start all three tiers
docker-compose up -d

# Check all containers running
docker-compose ps

# Check logs
docker-compose logs -f backend

# Verify MySQL data
docker exec -it mysql-db mysql -u appuser -papppass appdb -e "SHOW TABLES;"
```

### Dockerfiles for Each Tier

**Backend (Node.js):**

```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 5000
CMD ["node", "server.js"]
```

**Backend (Python Flask):**

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

**Frontend (React):**

```dockerfile
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

---

## 12. Reading Pipeline Results

### SonarQube Report — What 5 Bugs Means

```
SonarQube Report for three-tier-app:

  ┌─────────────────────────────────────────┐
  │  Reliability    │  5 Bugs              │
  │  Security       │  2 Vulnerabilities   │
  │  Maintainability│  23 Code Smells      │
  │  Duplications   │  8.3%                │
  │  Coverage       │  64.2%               │
  └─────────────────────────────────────────┘

  Quality Gate: ❌ FAILED
  Reason: Bugs > 0 (based on your gate config)
```

**What "5 bugs" means:** These are code paths that SonarQube's analysis determined will likely cause a runtime error or incorrect behavior. Example: dereferencing a variable that could be null, or an infinite loop condition.

**What to do:** Give the SonarQube report link to the developer team. They fix the flagged issues. Pipeline runs again. Gate passes. Deployment proceeds.

### Trivy Report — Reading CVEs

```
trivy-report.txt:

  Legend: C=Critical H=High M=Medium L=Low

  Library         Vulnerability       Severity  Fixed Version
  ──────────────────────────────────────────────────────────
  openssl         CVE-2023-0286       HIGH      1.1.1t
  libcurl         CVE-2023-23916      MEDIUM    7.88.1
  node            CVE-2022-32212      HIGH      18.5.0
  ...

  Total: C:2 H:8 M:15 L:42
```

**What to do with CVEs:**
- CRITICAL: Upgrade the vulnerable package or change base image immediately
- HIGH: Schedule fix in current sprint
- Use `FROM node:18-alpine` instead of `node:16-alpine` — newer base images have fewer CVEs

---

## 13. Tech Stack Mapping

### DevSecOps Pipeline Across Tech Stacks

```
Node.js Stack:
  Code → npm test → SonarQube (JS/TS) → docker build → trivy → docker push → EKS/ECS

Python Stack:
  Code → pytest → SonarQube (Python) → docker build → trivy → docker push → Lambda/EC2

Java Stack:
  Code → mvn test → SonarQube (Java) → docker build → trivy → docker push → ECS
```

### SonarQube for Different Languages

```groovy
// Node.js project
sh """
  sonar-scanner \
    -Dsonar.projectKey=my-node-app \
    -Dsonar.sources=src \
    -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info
"""

// Python project
sh """
  sonar-scanner \
    -Dsonar.projectKey=my-python-app \
    -Dsonar.sources=. \
    -Dsonar.python.coverage.reportPaths=coverage.xml
"""

// Java/Maven project
sh 'mvn sonar:sonar -Dsonar.host.url=http://<IP>:9000 -Dsonar.login=${SONAR_TOKEN}'
```

### AWS Integration: ECR + ECS DevSecOps Pipeline

```
GitHub
  │
  ▼
Jenkins (EC2)
  │
  ├── SonarQube scan (SAST)
  ├── docker build
  ├── Trivy scan (image)
  ├── docker push → AWS ECR (private registry)
  │
  ▼
AWS ECS (Fargate) — pulls from ECR, runs containers
  ├── Frontend task (port 3000)
  ├── Backend task (port 5000)
  └── RDS MySQL (managed database)
```

### Jenkins Pipeline with AWS ECR + ECS

```groovy
environment {
  AWS_REGION    = 'ap-south-1'
  ECR_REGISTRY  = '<ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com'
  IMAGE_NAME    = 'three-tier-app'
  ECS_CLUSTER   = 'production-cluster'
  ECS_SERVICE   = 'app-service'
}

stage('Push to ECR') {
  steps {
    withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
      sh """
        aws ecr get-login-password | \
          docker login --username AWS --password-stdin ${ECR_REGISTRY}
        docker tag ${IMAGE_NAME}:${BUILD_NUMBER} \
          ${ECR_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
        docker push ${ECR_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
      """
    }
  }
}

stage('Deploy to ECS') {
  steps {
    withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
      sh """
        aws ecs update-service \
          --cluster ${ECS_CLUSTER} \
          --service ${ECS_SERVICE} \
          --force-new-deployment
      """
    }
  }
}
```

### MongoDB Atlas + Node.js Backend Security Scan

```javascript
// sonar-project.properties (in repo root)
sonar.projectKey=node-mongo-api
sonar.sources=src
sonar.exclusions=node_modules/**,test/**
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.host.url=http://<EC2-IP>:9000
sonar.login=${SONAR_TOKEN}
```

---

## 14. Interview Project Walkthrough Script

**Use this when asked: "Tell me about a DevSecOps project you worked on"**

---

**Step 1 — Provision server on AWS:**
"We provisioned an Ubuntu EC2 instance (t2.large, 50GB) on AWS and opened Security Group ports for Jenkins (8080), SonarQube (9000), and the application (3000, 5000)."

**Step 2 — Install required tools:**
"We wrote a shell script to install Java, Jenkins, Docker, Python, and Trivy on the EC2 instance. Jenkins and Docker were enabled as system services. We added the Jenkins user to the Docker group so pipelines could run Docker commands."

**Step 3 — Configure Jenkins:**
"We installed plugins: SonarQube Scanner, Docker Pipeline, and Pipeline Stage View. We stored Docker Hub credentials and the SonarQube token as Jenkins secrets. We configured the SonarQube server URL in Jenkins System settings."

**Step 4 — Get application code:**
"We used a three-tier application from GitHub — React frontend, Node.js/Python backend, and MySQL database. The Jenkinsfile was part of the repository (Pipeline from SCM)."

**Step 5 — CI pipeline flow:**
"The CI pipeline had: Git Checkout → Install Dependencies → SonarQube Analysis → Quality Gate check → Docker Build. If SonarQube's Quality Gate failed, the pipeline stopped and developers were notified to fix issues."

**Step 6 — CD / deployment flow:**
"After CI passed, the CD stages ran: Trivy image scan for CVEs → Docker push to Docker Hub → docker run to deploy the container on port 3000. We used docker-compose for the three-tier setup connecting frontend, backend, and MySQL."

**Step 7 — Security angle:**
"Security was the differentiator from a regular CI/CD pipeline. SonarQube caught 5 bugs and 2 vulnerabilities in the source code before the image was even built. Trivy scanned the Docker image for OS-level CVEs. Together, these gates ensured no vulnerable code or image reached production. This is the 'Shift Left' security principle — catching issues early, where they're cheapest to fix."

---

**One-line summary for resume:**
*"Built a DevSecOps pipeline on AWS EC2 using Jenkins, Docker, Trivy, and SonarQube to automate build, security scan, and deployment of a 3-tier application with integrated CI/CD security gates."*

---

## 15. Scenario-Based Q&A

---

🔍 **Scenario 1:** SonarQube detects 5 bugs in the code. Should the pipeline deploy anyway?

✅ **Answer:** With Quality Gate configured to fail on any bug, the pipeline stops at the `waitForQualityGate` stage and marks the build as failed. The app is NOT deployed. SonarQube sends a webhook callback to Jenkins with "FAILED" status. The developer gets notified (Slack/email), fixes the bugs, pushes again, and the pipeline reruns. This is the "security gate" — no bad code gets through.

---

🔍 **Scenario 2:** Trivy finds CRITICAL CVEs in the Docker image. What do you do?

✅ **Answer:** If `--exit-code 1 --severity CRITICAL` is set in the Trivy command, the pipeline stage fails and deployment is blocked. To fix: upgrade the base image to a newer version (e.g., `node:18-alpine` instead of `node:16-alpine`), rebuild, and rescan. If it's a known false positive or an accepted risk, add it to Trivy's `.trivyignore` file with justification and a review date.

---

🔍 **Scenario 3:** A security audit requires proof that all deployed images were scanned. How do you provide evidence?

✅ **Answer:** In the Trivy stage, use `--output trivy-report.txt` and `archiveArtifacts artifacts: 'trivy-report.txt'` in Jenkins. Every build stores the Trivy report as a Jenkins artifact with timestamp and build number. Similarly, SonarQube keeps a history of all analysis runs. Together, these provide a full audit trail — "image X at build #42 was scanned on date Y with these results."

---

🔍 **Scenario 4:** Your team argues that SonarQube slows down the pipeline. How do you handle it?

✅ **Answer:** SonarQube analysis typically runs in 1-3 minutes depending on codebase size. The ROI is catching bugs that take hours (or days) to debug in production. You can speed it up by: running analysis only on changed files (`sonar.inclusions`), using incremental analysis, or running SonarQube in parallel with the build stage. The `Quality Gate` wait should have a `timeout(2, 'MINUTES')` so the pipeline doesn't hang indefinitely.

---

🔍 **Scenario 5:** How do you run SonarQube if there's no dedicated server and you want to keep costs low?

✅ **Answer:** Run SonarQube as a Docker container on the same EC2 as Jenkins: `docker run -d -p 9000:9000 sonarqube:lts-community`. It runs fine on t2.large with 8GB RAM. For very small teams, SonarCloud (SaaS version) is free for open-source projects — no server needed at all. Configure it the same way in Jenkins but point the URL to `https://sonarcloud.io`.

---

🔍 **Scenario 6:** The MySQL database container loses all data when the container restarts. How do you fix this?

✅ **Answer:** Mount a Docker volume for persistent storage: `-v mysql-data:/var/lib/mysql` in `docker run`, or `volumes: - mysql-data:/var/lib/mysql` in docker-compose. The volume lives on the host machine's disk — data survives container restarts, removals, and image upgrades. In production on AWS, use **RDS MySQL** (managed service) instead of a container — backups, replication, and snapshots are handled by AWS.

---

## 16. Interview Q&A

---

**Q1. What is DevSecOps and how does it differ from DevOps?**

**A:** DevOps automates the build, test, and deploy pipeline for speed and reliability. DevSecOps adds security automation at every stage of that pipeline — it's called "shifting security left" because security checks happen earlier (during development and CI) rather than at the end as a separate gate. Practically: DevOps might deploy and then discover a vulnerability; DevSecOps would have caught that vulnerability in the pipeline and blocked the deployment. Tools like SonarQube (code scanning) and Trivy (image scanning) are the technical implementation of DevSecOps principles.

---

**Q2. What does SonarQube scan for and how does it integrate with Jenkins?**

**A:** SonarQube performs Static Application Security Testing (SAST) — it analyzes source code without running it. It finds bugs (runtime errors), vulnerabilities (security weaknesses like SQL injection), code smells (maintainability issues), code duplications, and measures test coverage. Integration with Jenkins: install the SonarQube Scanner plugin, configure the SonarQube server URL and authentication token in Jenkins System settings. In the Jenkinsfile, use `withSonarQubeEnv('SonarQube') { sh 'sonar-scanner ...' }`. Use `waitForQualityGate abortPipeline: true` to pause the pipeline until SonarQube sends its Quality Gate result back via webhook.

---

**Q3. What is Trivy and what does it scan?**

**A:** Trivy is an open-source container image vulnerability scanner by Aqua Security. It scans: OS packages in the image layers (detecting known CVEs), application dependencies (npm, pip, gems), Infrastructure as Code misconfigurations, and secrets accidentally embedded in the image. It checks against the NVD (National Vulnerability Database) and other CVE databases. In a pipeline, run `trivy image --severity HIGH,CRITICAL imagename:tag`. With `--exit-code 1`, the pipeline fails if critical vulnerabilities are found, blocking deployment of vulnerable images.

---

**Q4. Explain the SonarQube Quality Gate concept.**

**A:** A Quality Gate is a set of configurable pass/fail conditions on your code's metrics. Example conditions: "no new bugs," "code coverage above 80%," "no critical vulnerabilities." After SonarQube analysis, it evaluates whether your code meets these conditions and returns either PASSED or FAILED. Jenkins waits for this result via the `waitForQualityGate()` step (SonarQube sends it via webhook). If FAILED, `abortPipeline: true` stops the pipeline — preventing the deployment of code that doesn't meet quality standards. It's the automated enforcement of your team's quality standards.

---

**Q5. Why do we need both SonarQube AND Trivy? Aren't they doing the same thing?**

**A:** They complement each other and cover different threat surfaces. SonarQube scans **source code** — it catches logic bugs, security vulnerabilities in your own code (SQL injection, XSS), and code quality issues before the image is even built. Trivy scans the **Docker image** after it's built — it catches vulnerabilities in the base OS (Ubuntu, Alpine), installed system packages, and runtime dependencies that your code relies on but didn't write. A developer might write perfectly clean code, but if the base image has a critical OpenSSL CVE, Trivy catches it. Together, they cover both application-level and infrastructure-level security.

---

**Q6. How do you handle a situation where Trivy reports many LOW/MEDIUM CVEs but no CRITICAL ones?**

**A:** Use `--severity HIGH,CRITICAL` to only fail on serious vulnerabilities: `trivy image --exit-code 1 --severity HIGH,CRITICAL imagename:tag`. For accepted low/medium risks, create a `.trivyignore` file in the repo listing CVE IDs to suppress with a comment explaining why and a review date. For systemic reduction of CVEs, regularly update base images (use `node:18-alpine` instead of older versions), run `trivy image --format json` to get machine-readable output for tracking over time, and integrate with a dashboard (like Grafana) to monitor CVE trends.

---

**Q7. Walk me through the complete DevSecOps pipeline you've implemented.**

**A:** "We provisioned an AWS EC2 Ubuntu t2.large instance with 50GB storage and opened ports for Jenkins (8080), SonarQube (9000), and the app (3000, 5000). We installed Java, Jenkins, Docker, Python, and Trivy via shell scripts. SonarQube was run as a Docker container. We integrated SonarQube with Jenkins using a generated token and configured a webhook for Quality Gate callbacks. The Jenkins pipeline had 8 stages: Git Checkout → Install Dependencies → SonarQube Analysis → Quality Gate check → Docker Image Build → Trivy Image Scan → Docker Push to Hub → Container Deployment. For a three-tier app (React frontend, Node.js backend, MySQL), we used docker-compose. SonarQube found 5 bugs in the codebase; Trivy completed the image scan. The pipeline demonstrates the DevSecOps principle of security-as-code — automated, repeatable, and integrated into the delivery process."

---

**Q8. What is the difference between SAST and DAST? Which tool covers which?**

**A:** SAST (Static Application Security Testing) analyzes code without running it — SonarQube is a SAST tool. It finds vulnerabilities in source code early in development. DAST (Dynamic Application Security Testing) tests the running application by sending inputs and observing behavior — tools like OWASP ZAP, Burp Suite. DAST finds vulnerabilities that only manifest at runtime (authentication bypasses, session management flaws). A mature DevSecOps pipeline uses both: SAST in the CI stage (fast, no running app needed) and DAST in a staging environment after deployment. For the class project, we implemented SAST with SonarQube and image scanning with Trivy.

---

## 17. Quick Reference Cheatsheet

### SonarQube Commands

```bash
# Run SonarQube (Docker)
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community

# Access: http://<IP>:9000  |  admin/admin

# Manual scan from CLI
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=<token>
```

### Trivy Commands

```bash
# Scan image
trivy image node:16-alpine

# Scan only HIGH and CRITICAL
trivy image --severity HIGH,CRITICAL myimage:latest

# Fail pipeline on CRITICAL
trivy image --exit-code 1 --severity CRITICAL myimage:latest

# Save report to file
trivy image --format table --output report.txt myimage:latest

# Scan local filesystem
trivy fs .

# Scan IaC files
trivy config ./terraform/
```

### Jenkins Credentials Usage

```groovy
// SonarQube token (Secret text)
withSonarQubeEnv('SonarQube') { sh 'sonar-scanner ...' }

// Docker Hub (Username/Password)
docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-creds') {
  dockerImage.push('latest')
}

// AWS credentials
withAWS(credentials: 'aws-creds', region: 'ap-south-1') {
  sh 'aws ecr get-login-password | docker login ...'
}
```

### Port Reference

| Port | Service |
|---|---|
| 22 | SSH |
| 8080 | Jenkins |
| 9000 | SonarQube |
| 3000 | Frontend App |
| 5000 | Backend App |
| 3306 | MySQL |
| 25 | SMTP (email alerts) |

---

## Navigation Footer

← Previous: [`54_Complete_CICD_Pipeline_Jenkins_+_Docker_+_AWS_(Node.js App).md`](54_Complete_CICD_Pipeline_Jenkins_+_Docker_+_AWS_(Node.js App).md) | Next: [`56_MLOps_FastAPI_Docker_AWS_EKS_(IT_Career_Prediction_System).md`](56_MLOps_FastAPI_Docker_AWS_EKS_(IT_Career_Prediction_System).md) →