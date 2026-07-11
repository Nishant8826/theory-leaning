# 57 – MLOps: FastAPI + Docker + AWS EKS (IT Career Prediction System)

---

## Table of Contents

1. [DevOps vs MLOps](#1-devops-vs-mlops)
2. [Project Overview: IT Career Upskilling Prediction](#2-project-overview-it-career-upskilling-prediction)
3. [FastAPI – The ML Serving Layer](#3-fastapi--the-ml-serving-layer)
4. [Python Virtual Environment](#4-python-virtual-environment)
5. [ML Model Training (train.py)](#5-ml-model-training-trainpy)
6. [Dockerizing the ML Application](#6-dockerizing-the-ml-application)
7. [AWS IAM User & CLI Setup](#7-aws-iam-user--cli-setup)
8. [kubectl, eksctl – Kubernetes CLI Tools](#8-kubectl-eksctl--kubernetes-cli-tools)
9. [AWS EKS – Managed Kubernetes](#9-aws-eks--managed-kubernetes)
10. [Kubernetes Deployment Manifest](#10-kubernetes-deployment-manifest)
11. [Full Architecture Diagram](#11-full-architecture-diagram)
12. [Complete Step-by-Step Commands](#12-complete-step-by-step-commands)
13. [Tech Stack Mapping](#13-tech-stack-mapping)
14. [Scenario-Based Q&A](#14-scenario-based-qa)
15. [Interview Q&A](#15-interview-qa)
16. [Cleanup & Cost Control](#16-cleanup--cost-control)
17. [Quick Reference Cheatsheet](#17-quick-reference-cheatsheet)

---

## 1. DevOps vs MLOps

### What

| | DevOps | MLOps |
|---|---|---|
| **Full form** | Development + Operations | Machine Learning + DevOps + Data Science |
| **Optimized for** | Software engineering workflows | Machine learning workflows |
| **Artifact built** | Application binary / Docker image | ML model + serving API |
| **CI/CD pipeline** | Build → Test → Deploy | Train → Evaluate → Package → Deploy |
| **Versioning** | Code versioning (Git) | Code + Data + Model versioning |
| **Key concern** | App reliability, uptime | Model accuracy, data drift, retraining |

### Why MLOps Exists
Traditional DevOps pipelines don't account for:
- **Model training** — a step that doesn't exist in regular software
- **Data pipelines** — the model needs fresh, clean data
- **Model drift** — a model that was 95% accurate in January may be 70% accurate in December as real-world data changes
- **Experiment tracking** — data scientists run hundreds of experiments; we need to track which model performed best

### How MLOps Works

```
Code + Data → Train Model → Evaluate → Package into API → Docker → Deploy on K8s
     ↑                                                                    │
     └────────────── Retrain trigger if accuracy drops ───────────────────┘
```

### Impact

| Without MLOps | With MLOps |
|---|---|
| Model trained once, deployed manually, never updated | Models retrained automatically when data changes |
| No versioning of models | Every model version tracked |
| "Works on data scientist's laptop" problem | Consistent, reproducible training environment |
| Slow, manual deployment of new model versions | Automated pipeline: new model → new Docker image → new deployment |

---

## 2. Project Overview: IT Career Upskilling Prediction

### What
An ML-powered REST API that predicts IT career outcomes based on:
- Years of experience
- Current package (salary)
- Skills

### Tech Stack

```
┌─────────────────────────────────────────────────────┐
│              IT Career Prediction System            │
│                                                     │
│  train.py ──► model.pkl (trained ML model)          │
│                  │                                  │
│  main.py ────────┤ FastAPI app loads model           │
│  (FastAPI)       │ serves predictions via REST API  │
│                  │                                  │
│  Dockerfile ─────► Docker Image (~3.3 GB)           │
│                  │                                  │
│  k8s-deploy.yml ─► EKS Cluster (2 pods)             │
│                      Public LoadBalancer IP         │
└─────────────────────────────────────────────────────┘
```

### Repository
```
https://github.com/CloudDevOpsHub/MLOPS-Project
```

### Project File Structure
```
MLOPS-Project/
├── train.py           ← ML training script
├── main.py            ← FastAPI app (loads model, serves predictions)
├── model.pkl          ← Saved trained model (generated after train.py)
├── requirements.txt   ← All Python dependencies
├── Dockerfile         ← Container build instructions
└── k8s-deploy.yml     ← Kubernetes Deployment + Service manifest
```

---

## 3. FastAPI – The ML Serving Layer

### What
**FastAPI** is a modern, high-performance Python web framework for building REST APIs. It's particularly popular in the ML/AI world because:
- It's fast (as fast as Node.js)
- Auto-generates interactive API docs (`/docs` endpoint)
- Built-in data validation using Pydantic
- Async support out of the box

### Why FastAPI Over Flask?
| Feature | FastAPI | Flask |
|---|---|---|
| Speed | Very fast (ASGI) | Slower (WSGI) |
| Auto docs | ✅ Built-in (Swagger UI) | ❌ Manual |
| Data validation | ✅ Pydantic | ❌ Manual |
| Async support | ✅ Native | Limited |
| ML/AI adoption | Very high | Moderate |

### How – A Simple FastAPI ML App

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI(title="IT Career Prediction API")

# Load trained model on startup
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Define the input schema
class PredictionInput(BaseModel):
    experience: float   # years of experience
    package: float      # current salary in LPA
    skills: int         # skill score (e.g., 1-10)

class PredictionOutput(BaseModel):
    prediction: str
    confidence: float

@app.get("/")
def root():
    return {"message": "IT Career Prediction API is live!"}

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    features = np.array([[data.experience, data.package, data.skills]])
    result = model.predict(features)[0]
    proba = model.predict_proba(features)[0].max()
    return {"prediction": result, "confidence": round(proba, 2)}

@app.get("/health")
def health():
    return {"status": "healthy"}
```

### Running FastAPI

```bash
# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000

# Access:
# App:       http://<IP>:8000
# API Docs:  http://<IP>:8000/docs   ← Swagger UI auto-generated
# Redoc:     http://<IP>:8000/redoc
```

### Why `--host 0.0.0.0`?
By default, uvicorn binds to `127.0.0.1` (localhost only — not accessible from outside). `0.0.0.0` means "listen on ALL network interfaces" — making it accessible via the EC2 public IP.

### Impact
Without FastAPI (or any serving layer), your trained ML model is just a `.pkl` file on disk — unusable by any application. FastAPI wraps it in an HTTP endpoint that any app, website, or mobile app can call.

---

## 4. Python Virtual Environment

### What
A **virtual environment** (`venv`) is an isolated Python installation for a specific project. It has its own `pip`, its own installed packages, and doesn't interfere with system Python or other projects.

### Why
Imagine you have:
- Project A needs `scikit-learn==1.0`
- Project B needs `scikit-learn==1.3`

Without venv, installing one breaks the other. With venv, each project has its own isolated environment.

### How

```bash
# Create virtual environment
python3 -m venv .mlops

# Activate it (Linux/Mac)
source .mlops/bin/activate

# Your prompt changes:
# (.mlops) ubuntu@ip-xxx:~/MLOPS-Project$

# Now install packages INSIDE the venv
pip install --upgrade pip
pip install -r requirements.txt

# Deactivate when done
deactivate
```

### What's in requirements.txt?

```txt
fastapi
uvicorn
scikit-learn
pandas
numpy
pydantic
pickle5
```

### Impact

| Without venv | With venv |
|---|---|
| Package conflicts between projects | Complete isolation |
| System Python gets polluted | System stays clean |
| `pip install` affects everything | Only affects this project |
| Hard to reproduce on another machine | `pip freeze > requirements.txt` captures exact versions |

---

## 5. ML Model Training (train.py)

### What
`train.py` is the script that:
1. Loads training data
2. Preprocesses it
3. Trains an ML model (e.g., Random Forest, Logistic Regression)
4. Saves the trained model to disk as `model.pkl`

### How (Typical train.py)

```python
# train.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# 1. Load data
df = pd.read_csv("data/career_data.csv")

# 2. Features and target
X = df[["experience", "package", "skills"]]
y = df["career_outcome"]

# 3. Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate
preds = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, preds):.2f}")

# 6. Save model to disk
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as model.pkl")
```

### Run It

```bash
python3 train.py
# Output: Accuracy: 0.91
# Output: Model saved as model.pkl
```

### Why This Step Matters
The FastAPI app (`main.py`) **loads `model.pkl`** on startup. If you haven't run `train.py` first, there's no model file, and the app crashes. In a production MLOps pipeline, this training step would be triggered automatically by a CI/CD pipeline when new data arrives.

---

## 6. Dockerizing the ML Application

### What
Packaging the FastAPI ML app + trained model + all dependencies into a single Docker image that can run anywhere.

### The Dockerfile

```dockerfile
# Base image: Python 3.11 slim (smaller than full Python image)
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file first (Docker layer caching — speeds up rebuilds)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project files (including model.pkl after training)
COPY . .

# Expose port 8000 (FastAPI)
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build, Tag, Push Flow

```bash
# Step 1: Build image
docker build -t it-career-api .
# Takes a few minutes; image is ~3.3 GB (Python + ML libraries are large)

# Step 2: Verify image created
docker images
# REPOSITORY        TAG     IMAGE ID       SIZE
# it-career-api     latest  abc123def456   3.3GB

# Step 3: Login to Docker Hub
docker login
# Enter DockerHub username and password

# Step 4: Tag with your Docker Hub username
docker tag it-career-api vikas4cloud/it-career-api:latest

# Step 5: Push to Docker Hub
docker push vikas4cloud/it-career-api:latest
# Image is now publicly accessible at hub.docker.com/r/vikas4cloud/it-career-api
```

### Why ~3.3 GB?
ML images are large because:
- scikit-learn depends on NumPy, SciPy (C extensions — large)
- Pandas has many dependencies
- Python base image itself is hundreds of MBs

To reduce size, use multi-stage builds or `python:3.11-slim` instead of full Python.

### Why Docker for MLOps?
Without Docker, deploying the ML app on a new server requires: install Python → create venv → install 20+ packages → copy model file → start uvicorn. With Docker: `docker run` — one command, same result everywhere.

---

## 7. AWS IAM User & CLI Setup

### What
**IAM (Identity and Access Management)** controls who can do what in AWS. To use AWS CLI (and eksctl) from the EC2 terminal, you need IAM credentials.

### Create IAM User

```
AWS Console → IAM → Users → Create User

Name: mlops-admin
Access type: Programmatic access (for CLI)
Permissions: Attach existing policies → AdministratorAccess
→ Create user → Download .csv (contains Access Key + Secret Key)
```

**Important:** Download the CSV immediately — AWS never shows the secret key again.

### Configure AWS CLI

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install -y unzip
unzip awscliv2.zip
sudo ./aws/install
aws --version

# Configure with IAM credentials
aws configure
# AWS Access Key ID:     AKIAIOSFODNN7EXAMPLE
# AWS Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# Default region name:   ap-south-1
# Default output format: json
```

### What Gets Stored

```
~/.aws/credentials
~/.aws/config
```

These files are used by AWS CLI, eksctl, and AWS SDKs to authenticate API calls.

### Impact
Without IAM credentials configured, `eksctl create cluster` fails with "no credentials found." Every AWS CLI command needs these credentials to prove you're authorized to create/manage resources.

---

## 8. kubectl, eksctl – Kubernetes CLI Tools

### kubectl

**What:** The command-line tool to interact with any Kubernetes cluster (local or cloud).

**How to install:**

```bash
# Download latest stable kubectl
curl -LO https://dl.k8s.io/release/$(curl -L -s \
  https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl

# Make it executable
chmod +x kubectl

# Move to system PATH
sudo mv kubectl /usr/local/bin/

# Verify
kubectl version --client
```

**Key commands:**

```bash
kubectl get pods              # List all pods
kubectl get deployments       # List all deployments
kubectl get svc               # List all services (with external IPs)
kubectl apply -f file.yaml    # Apply a manifest (create/update resources)
kubectl describe pod <name>   # Detailed info about a pod
kubectl logs <pod-name>       # View pod logs
kubectl delete -f file.yaml   # Delete resources defined in manifest
```

### eksctl

**What:** A CLI tool specifically for creating and managing **AWS EKS** clusters. Without it, creating an EKS cluster manually requires 20+ steps in AWS console.

**How to install:**

```bash
# Download eksctl
curl -sLO https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz

# Extract
tar -xzf eksctl_Linux_amd64.tar.gz

# Move to PATH
sudo mv eksctl /usr/local/bin/

# Verify
eksctl version
```

**Why eksctl?**
eksctl wraps CloudFormation and EKS APIs. One command creates: VPC, subnets, security groups, IAM roles, node groups, and the EKS control plane — all automatically.

---

## 9. AWS EKS – Managed Kubernetes

### What
**Amazon EKS (Elastic Kubernetes Service)** is AWS's managed Kubernetes service. "Managed" means AWS runs and maintains the Kubernetes control plane (API server, etcd) — you only manage worker nodes.

### Why EKS Over Self-Managed K8s on EC2?
| Feature | EKS (Managed) | Self-managed K8s on EC2 |
|---|---|---|
| Control plane | AWS manages it | You manage it |
| High availability | Built-in | Complex to set up |
| K8s upgrades | One-click | Manual, risky |
| AWS integration | Native (IAM, ALB, EBS) | Manual configuration |
| Cost | Control plane: ~$0.10/hr + node costs | Only node costs |

### Create EKS Cluster

```bash
eksctl create cluster \
  --name mlops-cluster \
  --region ap-south-1 \
  --nodegroup-name mlops-nodes \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 3 \
  --managed
```

**Parameter breakdown:**

| Parameter | Value | Meaning |
|---|---|---|
| `--name` | mlops-cluster | Cluster name |
| `--region` | ap-south-1 | Mumbai region |
| `--nodegroup-name` | mlops-nodes | Name for the worker node group |
| `--node-type` | t3.medium | EC2 type for worker nodes (2 vCPU, 4GB) |
| `--nodes` | 2 | Start with 2 nodes |
| `--nodes-min` | 2 | Auto-scale minimum |
| `--nodes-max` | 3 | Auto-scale maximum |
| `--managed` | flag | AWS manages node patching/updates |

**This takes 5–15 minutes** — eksctl creates CloudFormation stacks under the hood.

### After Cluster Creation

```bash
# eksctl automatically updates your ~/.kube/config
# Now kubectl points to the new EKS cluster

kubectl get nodes
# NAME                                    STATUS   ROLES    AGE   VERSION
# ip-192-168-xx-xx.ap-south-1.compute..  Ready    <none>   5m    v1.28.x
# ip-192-168-xx-xx.ap-south-1.compute..  Ready    <none>   5m    v1.28.x
```

---

## 10. Kubernetes Deployment Manifest

### What
A YAML file that tells Kubernetes: "run this Docker image, with this many replicas, expose it on this port."

### k8s-deploy.yml

```yaml
# ── Deployment: runs the ML API pods ──────────────────────────────────
apiVersion: apps/v1
kind: Deployment
metadata:
  name: it-career-api
  labels:
    app: it-career-api
spec:
  replicas: 2                        # Run 2 copies of the pod
  selector:
    matchLabels:
      app: it-career-api
  template:
    metadata:
      labels:
        app: it-career-api
    spec:
      containers:
        - name: it-career-api
          image: vikas4cloud/it-career-api:latest   # Docker Hub image
          ports:
            - containerPort: 8000
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          readinessProbe:            # K8s checks if pod is ready to serve traffic
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 5

---
# ── Service: exposes the pods to the internet ─────────────────────────
apiVersion: v1
kind: Service
metadata:
  name: it-career-api-svc
spec:
  type: LoadBalancer                 # AWS creates an ALB automatically
  selector:
    app: it-career-api
  ports:
    - protocol: TCP
      port: 80                       # External port (user hits port 80)
      targetPort: 8000               # Internal container port
```

### Deploy & Verify

```bash
# Apply the manifest
kubectl apply -f k8s-deploy.yml

# Check deployment status
kubectl get deployments
# NAME             READY   UP-TO-DATE   AVAILABLE
# it-career-api   2/2     2            2

# Check pods
kubectl get pods
# NAME                            READY   STATUS    RESTARTS
# it-career-api-xxxx-xxxx         1/1     Running   0
# it-career-api-xxxx-yyyy         1/1     Running   0

# Get external IP (from AWS Load Balancer)
kubectl get svc
# NAME                  TYPE           EXTERNAL-IP
# it-career-api-svc    LoadBalancer   a1b2c3d4.ap-south-1.elb.amazonaws.com
```

Access the live API:
```
http://a1b2c3d4.ap-south-1.elb.amazonaws.com/docs
```

---

## 11. Full Architecture Diagram

### MLOps Pipeline: End-to-End

```
┌──────────────────────────────────────────────────────────────────────┐
│                         DEVELOPER / DATA SCIENTIST                   │
│  1. Write train.py (ML training)                                     │
│  2. Write main.py (FastAPI app)                                      │
│  3. Write Dockerfile                                                 │
│  4. git push → GitHub                                                │
└─────────────────────────┬────────────────────────────────────────────┘
                          │ git clone (on EC2)
                          ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    AWS EC2 (Ubuntu T2 Medium)                        │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                  Python Virtual Env (.mlops)                │    │
│  │                                                             │    │
│  │  pip install -r requirements.txt                            │    │
│  │            │                                                │    │
│  │            ▼                                                │    │
│  │  python3 train.py ──────────► model.pkl (trained model)    │    │
│  │            │                                                │    │
│  │            ▼                                                │    │
│  │  uvicorn main:app → FastAPI live at :8000 (test)           │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  docker build -t it-career-api .                                     │
│       │                                                              │
│       ▼                                                              │
│  Docker Image (~3.3 GB)                                              │
│       │                                                              │
│       │  docker push                                                 │
│       ▼                                                              │
└──────────────────┬───────────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────┐
│         Docker Hub           │
│  vikas4cloud/it-career-api   │
│         :latest              │
└──────────────┬───────────────┘
               │ pulled by EKS nodes
               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    AWS EKS Cluster (ap-south-1)                      │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │                   mlops-cluster                            │     │
│  │                                                            │     │
│  │  Node 1 (t3.medium)        Node 2 (t3.medium)             │     │
│  │  ┌─────────────────┐       ┌─────────────────┐            │     │
│  │  │ Pod: it-career  │       │ Pod: it-career  │            │     │
│  │  │ FastAPI :8000   │       │ FastAPI :8000   │            │     │
│  │  └────────┬────────┘       └────────┬────────┘            │     │
│  │           │                         │                     │     │
│  │           └──────────┬──────────────┘                     │     │
│  │                      │                                     │     │
│  │           ┌──────────▼────────────────┐                   │     │
│  │           │  Service: LoadBalancer    │                   │     │
│  │           │  External IP / DNS        │                   │     │
│  │           │  Port 80 → 8000           │                   │     │
│  │           └──────────────────────────┘                    │     │
│  └────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
                    User hits: http://<LB-IP>/predict
                    Input: experience=5, package=8, skills=7
                    Output: {"prediction": "Senior Dev", "confidence": 0.87}
```

---

## 12. Complete Step-by-Step Commands

### Phase 1: EC2 Setup

```bash
# Connect to EC2
chmod 400 key.pem
ssh -i key.pem ubuntu@<PUBLIC-IP>

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, pip, Git
sudo apt install python3 python3-pip python3-venv git -y

# Verify
python3 --version
pip3 --version
```

### Phase 2: Project Setup & Training

```bash
# Clone project
git clone https://github.com/CloudDevOpsHub/MLOPS-Project
cd MLOPS-Project

# Create and activate virtual environment
python3 -m venv .mlops
source .mlops/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Train the ML model
python3 train.py
# Generates: model.pkl

# Test the app locally
uvicorn main:app --host 0.0.0.0 --port 8000
# Visit: http://<EC2-IP>:8000/docs
```

### Phase 3: Docker

```bash
# Install Docker
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
docker -v

# Build image
docker build -t it-career-api .

# Verify
docker images

# Login and push
docker login
docker tag it-career-api vikas4cloud/it-career-api:latest
docker push vikas4cloud/it-career-api:latest
```

### Phase 4: AWS CLI & IAM

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install -y unzip
unzip awscliv2.zip
sudo ./aws/install
aws --version

# Configure with IAM credentials
aws configure
# Access Key:    <from IAM user CSV>
# Secret Key:    <from IAM user CSV>
# Region:        ap-south-1
# Output:        json
```

### Phase 5: kubectl & eksctl

```bash
# Install kubectl
curl -LO https://dl.k8s.io/release/$(curl -L -s \
  https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client

# Install eksctl
curl -sLO https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz
tar -xzf eksctl_Linux_amd64.tar.gz
sudo mv eksctl /usr/local/bin/
eksctl version
```

### Phase 6: EKS Cluster & Deploy

```bash
# Create EKS cluster (5–15 minutes)
eksctl create cluster \
  --name mlops-cluster \
  --region ap-south-1 \
  --nodegroup-name mlops-nodes \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 3 \
  --managed

# Verify nodes
kubectl get nodes

# Deploy the app
kubectl apply -f k8s-deploy.yml

# Check status
kubectl get deployments
kubectl get pods
kubectl get svc   # ← get the EXTERNAL-IP (LoadBalancer)

# Hit the live API
curl http://<EXTERNAL-IP>/health
```

### Phase 7: Cleanup

```bash
# Delete EKS cluster
eksctl delete cluster --name mlops-cluster --region ap-south-1

# Verify deletion
# EKS Console:  https://ap-south-1.console.aws.amazon.com/eks/clusters
# CloudFormation: https://ap-south-1.console.aws.amazon.com/cloudformation/home

# If deletion gets stuck → go to CloudFormation → delete related stacks manually
```

---

## 13. Tech Stack Mapping

### MLOps Stack Compared to DevOps Stack

```
DevOps Project Stack:          MLOps Project Stack:
─────────────────────          ─────────────────────
Node.js / Next.js         →    Python / FastAPI
npm install               →    pip install -r requirements.txt
npm run build             →    python3 train.py (extra step!)
Dockerfile (Node)         →    Dockerfile (Python/ML)
Docker Hub                →    Docker Hub (or AWS ECR)
Jenkins CI/CD             →    GitHub Actions / MLflow pipelines
ECS / EC2                 →    EKS (heavier workloads need K8s)
MongoDB                   →    CSV / PostgreSQL / S3 (training data)
```

### Jenkins Pipeline for MLOps

```groovy
pipeline {
  agent any

  environment {
    DOCKER_IMAGE = 'vikas4cloud/it-career-api'
    DOCKER_TAG   = "${BUILD_NUMBER}"
  }

  stages {

    stage('Checkout') {
      steps {
        git branch: 'main',
            url: 'https://github.com/CloudDevOpsHub/MLOPS-Project.git'
      }
    }

    stage('Setup Python Env') {
      steps {
        sh '''
          python3 -m venv .mlops
          source .mlops/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Train ML Model') {
      steps {
        sh '''
          source .mlops/bin/activate
          python3 train.py
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-creds') {
            docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
            docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push('latest')
          }
        }
      }
    }

    stage('Deploy to EKS') {
      steps {
        withAWS(credentials: 'aws-creds', region: 'ap-south-1') {
          sh '''
            aws eks update-kubeconfig --name mlops-cluster --region ap-south-1
            kubectl apply -f k8s-deploy.yml
            kubectl rollout status deployment/it-career-api
          '''
        }
      }
    }

  }

  post {
    success { echo "✅ MLOps pipeline SUCCESS" }
    failure { echo "❌ Pipeline FAILED — check logs" }
  }
}
```

### Node.js App Calling the Python ML API

```javascript
// In a Next.js or Node.js backend — calling the FastAPI ML service
const axios = require('axios');

const ML_API = process.env.ML_API_URL || 'http://<EKS-LB-IP>';

async function predictCareer(experience, packageLPA, skills) {
  try {
    const response = await axios.post(`${ML_API}/predict`, {
      experience,
      package: packageLPA,
      skills
    });
    return response.data; // { prediction: "Senior Dev", confidence: 0.87 }
  } catch (error) {
    console.error('ML API call failed:', error.message);
    throw error;
  }
}

// Usage in an Express route
app.post('/api/career-prediction', async (req, res) => {
  const { experience, package: pkg, skills } = req.body;
  const result = await predictCareer(experience, pkg, skills);
  res.json(result);
});
```

### AWS Services Used in This Project

| AWS Service | Role |
|---|---|
| EC2 (t2.medium) | Development/build server |
| IAM | Authentication for CLI and EKS |
| EKS | Managed Kubernetes cluster |
| EC2 (t3.medium) | Worker nodes inside EKS |
| Elastic Load Balancer | Auto-created by K8s `LoadBalancer` service |
| CloudFormation | Used by eksctl under the hood |
| VPC, Subnets | Auto-created by eksctl |

---

## 14. Scenario-Based Q&A

---

🔍 **Scenario 1:** You trained a model last month. Business patterns have changed and the model's accuracy has dropped from 91% to 73%. How do MLOps practices help?

✅ **Answer:** In a mature MLOps setup, you'd have **model monitoring** (e.g., with Evidently AI or MLflow) that detects accuracy/data drift automatically. When drift is detected, it triggers a retraining pipeline: new data → `train.py` → new `model.pkl` → new Docker image build → push to registry → `kubectl rollout restart deployment/it-career-api` on EKS. The old model is replaced with the new one with zero downtime via Kubernetes rolling updates.

---

🔍 **Scenario 2:** A data scientist trained the model on their MacBook. It works locally but fails when deployed on the EC2 / in Docker.

✅ **Answer:** This is the classic "works on my machine" problem. The solution is Docker. The Dockerfile defines the exact Python version, all package versions from `requirements.txt`, and the OS environment. Building and running the Docker image on any machine gives identical results — no more "but it worked on my laptop."

---

🔍 **Scenario 3:** Your ML app on EKS is handling 100 requests/second. During a product launch, traffic spikes to 1,000 requests/second. How does Kubernetes help?

✅ **Answer:** Configure a **Horizontal Pod Autoscaler (HPA)** on the deployment. When CPU usage crosses a threshold (e.g., 70%), HPA automatically increases the replica count from 2 to 10 (or more, up to node capacity). EKS's managed node group with `--nodes-max 3` also scales EC2 nodes if pods can't be scheduled. After the spike, HPA scales back down — cost-efficient.

---

🔍 **Scenario 4:** eksctl delete cluster is stuck. What do you do?

✅ **Answer:** eksctl uses **AWS CloudFormation** to create clusters. If deletion is stuck, there's likely a CloudFormation stack that can't be deleted due to dependent resources (like a load balancer created by a Kubernetes Service). Go to **AWS CloudFormation Console** → find stacks with names like `eksctl-mlops-cluster-*` → manually delete them (you may need to delete the K8s LoadBalancer service first with `kubectl delete svc it-career-api-svc`). After CloudFormation stacks are gone, the cluster is fully cleaned up.

---

🔍 **Scenario 5:** You want to keep the Docker image private (not public on Docker Hub). What do you use?

✅ **Answer:** Use **AWS ECR (Elastic Container Registry)** — a private Docker registry on AWS. Create an ECR repository, authenticate with `aws ecr get-login-password`, tag and push the image to ECR. Update the `k8s-deploy.yml` image reference to the ECR URI. For EKS to pull from ECR, attach the `AmazonEC2ContainerRegistryReadOnly` IAM policy to the node group's IAM role — EKS worker nodes can then pull images from ECR without needing explicit Docker login.

---

🔍 **Scenario 6:** Your manager asks, "As a DevOps engineer, what's your role in an MLOps project?"

✅ **Answer:** DevOps engineers in MLOps own: infrastructure setup (EC2, EKS cluster creation), CI/CD pipeline for model training and Docker builds, container registry management (Docker Hub / ECR), Kubernetes deployment manifests, monitoring (pod health, resource usage), IAM and security, and cost optimization (cluster cleanup, right-sizing nodes). Data scientists own: model architecture, training code, feature engineering, and model evaluation. The boundary is: DevOps = infrastructure and automation; Data Science = model quality and data.

---

## 15. Interview Q&A

---

**Q1. What is MLOps and how is it different from DevOps?**

**A:** MLOps (Machine Learning Operations) extends DevOps principles to ML workflows. DevOps handles code: build, test, deploy. MLOps handles code + data + model: data pipelines, model training, model evaluation, versioning of models, and serving. The key additional step in MLOps is **model training** — a compute-intensive step that doesn't exist in regular DevOps. MLOps also deals with model drift (accuracy degrading over time), which has no equivalent in traditional DevOps.

---

**Q2. What is FastAPI and why is it preferred for ML model serving?**

**A:** FastAPI is a modern Python web framework for building REST APIs. It's preferred for ML serving because it's very fast (ASGI-based, similar performance to Node.js), automatically generates Swagger/OpenAPI documentation at `/docs`, has built-in request/response validation via Pydantic, and supports async operations. Compared to Flask, FastAPI requires less boilerplate for data validation and generates documentation automatically — critical for ML APIs that data scientists and frontend teams need to understand.

---

**Q3. Why do we need a Python virtual environment for ML projects?**

**A:** ML projects have complex, often conflicting dependency requirements (e.g., TensorFlow requires specific NumPy versions, PyTorch has its own requirements). A virtual environment isolates project dependencies from system Python and from other projects. It ensures reproducibility — `pip freeze > requirements.txt` captures exact versions, so any machine can recreate the same environment with `pip install -r requirements.txt`. Without it, installing one project's dependencies can break another project.

---

**Q4. What does `eksctl create cluster --managed` do?**

**A:** The `--managed` flag creates an **EKS Managed Node Group** — AWS manages the EC2 worker nodes (OS patches, Kubernetes version updates, AMI updates). Without `--managed`, you'd use an unmanaged node group where you're responsible for node maintenance. Managed node groups also support rolling updates of nodes, draining pods safely before terminating old nodes. Under the hood, eksctl creates several CloudFormation stacks: one for the VPC, one for the cluster, and one for the node group.

---

**Q5. Explain the full MLOps deployment flow in this project.**

**A:** The flow is: EC2 setup → Python venv creation → `pip install -r requirements.txt` → `python3 train.py` (generates `model.pkl`) → `uvicorn main:app` (test FastAPI locally) → `docker build` (packages app + model + dependencies into image) → `docker push` to Docker Hub → `aws configure` with IAM credentials → `eksctl create cluster` (creates EKS on AWS) → `kubectl apply -f k8s-deploy.yml` (deploys 2 pods + LoadBalancer service) → app live at LoadBalancer external IP.

---

**Q6. Why is the Docker image for ML apps so large (~3.3 GB)?**

**A:** ML libraries like scikit-learn, NumPy, SciPy, and Pandas include compiled C/Fortran extensions that are large. The Python base image itself is hundreds of MBs. Combined, a standard ML image easily reaches 2–4 GB. To reduce size: use `python:3.11-slim` or `python:3.11-alpine` as base image, use multi-stage builds (separate build and runtime stages), and only install production dependencies (`pip install --no-dev`). Deep learning frameworks (TensorFlow, PyTorch) make images even larger (8–15 GB).

---

**Q7. What is the role of `model.pkl` and how is it used in the FastAPI app?**

**A:** `model.pkl` is the **serialized trained ML model** — the output of `train.py`. Using Python's `pickle` library, the trained model object (including all learned parameters) is saved to disk. The FastAPI app loads this file at startup (`pickle.load("model.pkl")`) and keeps the model in memory. When a `/predict` request comes in, it passes the input data to `model.predict()` and returns the result. This is the bridge between the training world (data science) and the serving world (DevOps).

---

**Q8. How would you handle a zero-downtime model update on EKS?**

**A:** Train new model → generate new `model.pkl` → build new Docker image with a new tag (`v2`) → push to registry → update `k8s-deploy.yml` image tag to `v2` → `kubectl apply -f k8s-deploy.yml`. Kubernetes performs a **rolling update** by default: it starts new pods with the v2 image one at a time, waits for them to pass the readiness probe (`/health`), then terminates old pods. At no point are all pods down simultaneously — users see no interruption. To roll back if v2 is bad: `kubectl rollout undo deployment/it-career-api`.

---

**Q9. What is the difference between `kubectl apply` and `kubectl create`?**

**A:** `kubectl create` is imperative — it creates resources from scratch and fails if they already exist. `kubectl apply` is declarative — it creates resources if they don't exist, or updates them if they do (diff-based). For CI/CD pipelines, `kubectl apply` is always preferred because it's idempotent: running it multiple times with the same manifest has the same result as running it once. `kubectl create` would fail on the second run.

---

## 16. Cleanup & Cost Control

### Why Cleanup Matters
EKS costs ~$0.10/hour for the control plane + EC2 costs for worker nodes. Two t3.medium nodes = ~$0.08/hour each. Total: ~$0.26/hour = **~$6.24/day** if left running. Always delete after practice sessions.

### Cleanup Steps

```bash
# Step 1: Delete Kubernetes resources (optional but clean)
kubectl delete -f k8s-deploy.yml
# This deletes the LoadBalancer (important — otherwise CloudFormation stack deletion may hang)

# Step 2: Delete EKS cluster
eksctl delete cluster --name mlops-cluster --region ap-south-1
# Wait 5–10 minutes

# Step 3: Verify via Console
# EKS: https://ap-south-1.console.aws.amazon.com/eks/clusters
# CloudFormation: https://ap-south-1.console.aws.amazon.com/cloudformation/home

# Step 4: If CloudFormation stacks are stuck, delete them manually
# Look for stacks named: eksctl-mlops-cluster-*

# Step 5: Stop/Terminate EC2 instance if no longer needed
```

### Common Cleanup Issues

| Issue | Cause | Fix |
|---|---|---|
| CloudFormation stack stuck | K8s LoadBalancer still exists | Delete K8s Service first, then retry |
| Cluster still visible in EKS console | CloudFormation not fully deleted | Manually delete CF stacks |
| EC2 nodes still running | eksctl deletion failed midway | Terminate EC2 instances manually |

---

## 17. Quick Reference Cheatsheet

### EC2 Bootstrap (one-liner)

```bash
sudo apt update && sudo apt upgrade -y && \
sudo apt install python3 python3-pip python3-venv git docker.io unzip -y && \
sudo systemctl start docker && sudo systemctl enable docker && \
sudo usermod -aG docker $USER && newgrp docker
```

### Virtual Environment

```bash
python3 -m venv .mlops && source .mlops/bin/activate
pip install --upgrade pip && pip install -r requirements.txt
```

### Docker Workflow

```bash
docker build -t it-career-api .
docker login
docker tag it-career-api <username>/it-career-api:latest
docker push <username>/it-career-api:latest
```

### Tool Installation

```bash
# kubectl
curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x kubectl && sudo mv kubectl /usr/local/bin/

# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# eksctl
curl -sLO https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz
tar -xzf eksctl_Linux_amd64.tar.gz && sudo mv eksctl /usr/local/bin/
```

### EKS Lifecycle

```bash
# Create
eksctl create cluster --name mlops-cluster --region ap-south-1 \
  --nodegroup-name mlops-nodes --node-type t3.medium \
  --nodes 2 --nodes-min 2 --nodes-max 3 --managed

# Deploy app
kubectl apply -f k8s-deploy.yml
kubectl get svc   # get external IP

# Delete
kubectl delete -f k8s-deploy.yml   # delete LB first!
eksctl delete cluster --name mlops-cluster --region ap-south-1
```

### FastAPI Endpoints

```
GET  /          → Health check / welcome message
GET  /health    → Readiness probe endpoint
POST /predict   → ML prediction endpoint
GET  /docs      → Swagger UI (auto-generated)
GET  /redoc     → ReDoc UI (auto-generated)
```

---
## Navigation Footer

← Previous: [`56_DevSecOps_Jenkins_Trivy_SonarQube_on_AWS.md`](56_DevSecOps_Jenkins_Trivy_SonarQube_on_AWS.md) | Next: [`57_Advanced_Kubernetes_Concepts_and_Best_Practices.md`](57_Advanced_Kubernetes_Concepts_and_Best_Practices.md) →
