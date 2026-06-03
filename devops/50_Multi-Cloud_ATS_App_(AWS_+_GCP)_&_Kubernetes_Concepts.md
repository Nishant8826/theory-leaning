# 50 – Multi-Cloud ATS App (AWS + GCP) & Kubernetes Concepts

> **Batch-43 | Project 6 – AI-Powered Resume Screening + K8s Interview Prep**
> Repo: https://github.com/CloudDevOpsHub/batch-43

---

## Table of Contents

1. [Project Overview – ATS Application](#1-project-overview--ats-application)
2. [Architecture Explained](#2-architecture-explained)
3. [Step-by-Step Implementation](#3-step-by-step-implementation)
4. [App Functionality](#4-app-functionality)
5. [Kubernetes – Liveness Probe](#5-kubernetes--liveness-probe)
6. [Kubernetes – Readiness Probe](#6-kubernetes--readiness-probe)
7. [Liveness vs Readiness – Side-by-Side](#7-liveness-vs-readiness--side-by-side)
8. [Kubernetes – Affinity & Anti-Affinity](#8-kubernetes--affinity--anti-affinity)
9. [Kubernetes – Taints & Tolerations](#9-kubernetes--taints--tolerations)
10. [Kubernetes – Ingress](#10-kubernetes--ingress)
11. [Kubernetes – Network Policy](#11-kubernetes--network-policy)
12. [Real-World Analogies Summary](#12-real-world-analogies-summary)
13. [Visual Diagrams](#13-visual-diagrams)
14. [Scenario-Based Q&A](#14-scenario-based-qa)
15. [Interview Q&A](#15-interview-qa)
16. [Tech Stack Mapping](#16-tech-stack-mapping)
17. [Code / Practical Examples](#17-code--practical-examples)
18. [Navigation Footer](#navigation-footer)

---

## 1. Project Overview – ATS Application

### What
An **ATS (Application Tracking System)** is software companies use to screen resumes. This project builds an **AI-powered ATS** that:
- Takes a Job Description (JD) and a resume (PDF) as input
- Uses **Google Gemini AI** to analyze how well the resume matches the JD
- Returns a **match percentage** and **feedback** for the candidate

### Why Build This?
- Real-world multi-cloud project (AWS + GCP) for your portfolio
- Demonstrates Python, Streamlit, API integration, and cloud deployment
- Mirrors what actual HR tech companies build at scale

### Tech Stack at a Glance

| Component | Technology | Cloud |
|---|---|---|
| Application | Python + Streamlit | — |
| Hosting | EC2 Ubuntu (T2 Large) | AWS |
| AI Engine | Gemini API | GCP |
| Secret Storage | `.streamlit/secrets.toml` | Local (on EC2) |
| Port | 8501 (Streamlit default) | AWS Security Group |

---

## 2. Architecture Explained

### What
The app uses a **two-cloud architecture**:
- **AWS** hosts and runs the application
- **GCP** provides the AI brain (Gemini) via API call

```
User (Browser)
      │
      │ HTTP :8501
      ▼
AWS EC2 (Ubuntu T2 Large)
      │  Python + Streamlit app
      │  uploads JD + Resume PDF
      │
      │  API call (HTTPS)
      ▼
GCP Gemini API
      │  Processes: JD + Resume text
      │  Returns: match % + feedback
      ▼
AWS EC2 displays result
      │
      ▼
User sees AI screening output
```

### Why Two Clouds?
- **AWS EC2** is reliable, familiar, and cost-effective for running web apps
- **GCP Gemini** is Google's most capable LLM — better at document analysis and structured feedback than most alternatives
- This is a real pattern in enterprise: use the best service from each cloud

---

## 3. Step-by-Step Implementation

### Step 1: Provision EC2 Instance

**What:** Launch an Ubuntu Linux server on AWS to host the app.

**Why T2 Large / 30GB?**
- Python + Streamlit + PDF processing is memory-heavy
- T2 Micro / Small will run out of RAM and crash
- 30GB storage accommodates Python env, libraries, and uploaded files

```bash
# EC2 Configuration:
AMI:          Ubuntu 22.04 LTS
Instance:     t2.large (2 vCPU, 8GB RAM)
Storage:      30 GB gp2
Key Pair:     Create/use existing .pem key
Security Group: (configured in Step 8)
```

---

### Step 2: Install Python 3, pip, and venv

**SSH into the EC2 instance:**
```bash
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

**Install required tools:**
```bash
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git
python3 --version   # verify: Python 3.10.x or higher
```

---

### Step 3: Clone the Project

```bash
git clone https://github.com/CloudDevOpsHub/batch-43.git
cd batch-43
ls   # see project files
```

---

### Step 4: Create and Activate a Virtual Environment

**Why venv?**
Isolates this project's dependencies. Prevents conflicts with system Python packages.

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Your prompt changes to show (venv):
# (venv) ubuntu@ip-10-0-1-5:~/batch-43$
```

---

### Step 5: Install Dependencies

```bash
# Install all project requirements
pip install -r requirements.txt

# Install Google Generative AI library separately
pip install google-generativeai

# Verify
pip list | grep -E "streamlit|google"
```

---

### Step 6: Create GCP API Key (Gemini)

**Why needed:** The app calls the GCP Gemini API. GCP requires authentication via an API key.

**Steps in GCP Console:**
```
1. Go to: https://console.cloud.google.com
2. Create a new project (or use existing)
3. Navigate to: APIs & Services → Library
4. Search: "Generative Language API" → Enable it
5. Navigate to: APIs & Services → Credentials
6. Click: Create Credentials → API Key
7. Copy the generated key (looks like: AIzaSy...)
8. Restrict the key: Application restrictions → None (for dev)
   OR restrict to your EC2 IP for security
```

**Fixing 403 Errors:**
```
Common causes of 403 (Forbidden):
├── API not enabled in GCP project → Enable Generative Language API
├── API key is from wrong project → Verify in GCP Console
├── Key has IP restrictions that block EC2 → Update restriction
├── Billing not enabled on GCP project → Add billing account
└── Quota exceeded → Check quotas in GCP Console
```

---

### Step 7: Store API Key in `secrets.toml`

**What:** Streamlit has a built-in secrets management system. Secrets are stored in `.streamlit/secrets.toml` and accessed in code via `st.secrets`.

**Why not hardcode?**
- Hardcoded keys in code = leaked keys when you push to GitHub
- `.streamlit/secrets.toml` is added to `.gitignore` by convention

```bash
# Create the .streamlit directory
mkdir -p .streamlit

# Create the secrets file
nano .streamlit/secrets.toml
```

**Content of `secrets.toml`:**
```toml
# .streamlit/secrets.toml
GOOGLE_API_KEY = "AIzaSyYOUR_ACTUAL_KEY_HERE"
```

**Add to `.gitignore` (CRITICAL):**
```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

**Access in Python code:**
```python
import streamlit as st
api_key = st.secrets["GOOGLE_API_KEY"]
```

---

### Step 8: Open Port 8501 in AWS Security Group

**Why:** Streamlit runs on port **8501** by default. AWS blocks all ports by default — you must explicitly allow traffic.

```
AWS Console → EC2 → Your Instance → Security tab
→ Click Security Group → Edit Inbound Rules
→ Add Rule:
   Type:        Custom TCP
   Port Range:  8501
   Source:      0.0.0.0/0  (all IPs — for development)
               OR your-IP/32 (your IP only — more secure)
→ Save Rules
```

---

### Step 9: Run the Streamlit App

```bash
# Make sure venv is active
source venv/bin/activate

# Run Streamlit (binds to all interfaces so it's accessible externally)
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

**Access the app:**
```
http://<EC2-PUBLIC-IP>:8501
```

**Run in background (so it keeps running after you close SSH):**
```bash
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
# or using tmux (recommended):
tmux new-session -d -s ats 'streamlit run app.py --server.port 8501 --server.address 0.0.0.0'
```

---

## 4. App Functionality

### How It Works (User Flow)

```
1. User opens browser → http://EC2-IP:8501

2. User pastes Job Description text into text box

3. User uploads their Resume as a PDF file

4. User clicks "Analyze" button

5. App extracts text from PDF (using PyPDF2 or similar)

6. App sends to Gemini API:
   - The Job Description text
   - The extracted resume text
   - A prompt: "Analyze match percentage and give feedback"

7. Gemini AI returns:
   - Match percentage (e.g., 72%)
   - Missing keywords
   - Strengths in the resume
   - Suggestions for improvement

8. Streamlit displays the results
```

### Impact
- Recruiters screen 100+ resumes/day manually → This does it in seconds
- Candidates know exactly what's missing before applying
- Removes human bias from initial screening

---

## 5. Kubernetes – Liveness Probe

### What
A **Liveness Probe** is a Kubernetes health check that continuously asks: **"Is this container still alive and functioning?"**

If the liveness probe fails (the container stops responding), Kubernetes **automatically restarts the container**.

> **Analogy: Heartbeat Monitor** — like a hospital heart monitor. If it flatlines, the doctors (Kubernetes) take action immediately.

### Why
Without liveness probes:
- A container can get stuck in a broken state (memory leak, deadlock, infinite loop) without crashing
- Kubernetes sees it as "running" (process still exists) but the app is unresponsive
- Users get errors, but Kubernetes does nothing

With liveness probes:
- Kubernetes detects unresponsive containers and restarts them automatically
- Self-healing infrastructure

### How (Step-by-Step)

```
1. Kubernetes sends the probe request at regular intervals
2. Container responds → probe succeeds → container stays running
3. Container doesn't respond (3 consecutive failures by default) →
   probe fails → Kubernetes kills and restarts the container
```

**Three types of liveness probes:**

| Type | How it checks | Use when |
|---|---|---|
| HTTP GET | Sends HTTP request to `/health` endpoint | Web apps, APIs |
| TCP Socket | Tries to open a TCP connection to a port | Databases, non-HTTP apps |
| Exec | Runs a command inside the container | Custom checks, scripts |

### Impact

| With Liveness Probe | Without Liveness Probe |
|---|---|
| Hung app auto-restarts in seconds | Hung app stays broken until manual intervention |
| Downtime measured in seconds | Downtime measured in hours |
| Self-healing cluster | Requires on-call engineer to fix manually |

---

## 6. Kubernetes – Readiness Probe

### What
A **Readiness Probe** asks: **"Is this container ready to receive traffic?"**

If the readiness probe fails, Kubernetes **removes the pod from the load balancer** — stops sending it traffic — but does NOT restart it. The pod keeps running and Kubernetes keeps checking. When it passes again, traffic resumes.

> **Analogy: "Open for Business" Sign** — a restaurant might be open (alive) but still setting up tables. The readiness probe is the sign on the door. Until it flips to "Open," no customers enter.

### Why
Apps don't become ready instantly after starting. They need time to:
- Load configuration files
- Connect to the database
- Warm up caches
- Complete initialization tasks

Without readiness probes:
- Traffic hits pods that aren't ready yet → users get errors
- Rolling deployments can route traffic to half-started pods

With readiness probes:
- New pods only receive traffic when they're truly ready
- Zero-downtime deployments are possible

### How (Step-by-Step)

```
1. Pod starts → readiness probe begins checking
2. Probe fails → pod NOT added to Service endpoints
   (no traffic reaches this pod yet)
3. App finishes initializing → probe succeeds
4. Pod added to Service endpoints → traffic starts flowing
5. If probe fails later → pod removed from rotation (not restarted)
6. Pod recovers → added back automatically
```

### Impact

| With Readiness Probe | Without Readiness Probe |
|---|---|
| Traffic only reaches ready pods | Requests hit pods mid-startup → 500 errors |
| Zero-downtime rolling deployments | Downtime during every deployment |
| Automatic traffic re-routing during issues | Manual intervention to remove bad pods |

---

## 7. Liveness vs Readiness – Side-by-Side

| | **Liveness Probe** | **Readiness Probe** |
|---|---|---|
| **Question** | "Is the container alive?" | "Is the container ready for traffic?" |
| **On failure** | **Restart the container** | **Remove from load balancer** (no restart) |
| **Timing** | Runs throughout container lifetime | Checked at startup AND throughout |
| **Primary use** | Detect deadlocks, memory leaks, hangs | Detect slow startup, temp unavailability |
| **Analogy** | Heartbeat monitor | "Open for Business" sign |
| **Example** | App freezes → restart | App loading → wait → serve |

---

## 8. Kubernetes – Affinity & Anti-Affinity

### What
**Affinity** and **Anti-Affinity** are Kubernetes rules that control **which nodes pods are scheduled on** — based on relationships between pods and nodes.

- **Affinity:** "I want to be NEAR this" (run on the same node or same zone as something)
- **Anti-Affinity:** "I want to be FAR from this" (run on different nodes from something)

> **Analogy:**
> - Affinity = Friends choosing to sit at the same table
> - Anti-Affinity = Exam students made to sit in separate rooms

### Why

**Affinity use cases:**
- A web app and its Redis cache should be on the **same node** for low latency (avoid network hops)
- All pods of a microservice should run in the **same availability zone** as its database

**Anti-Affinity use cases:**
- Two replicas of the same service should be on **different nodes** so one node failure doesn't kill both
- Primary and backup database pods should be in **different availability zones**

### How — Two Types

**Node Affinity:** Attracts pods toward specific **nodes** (based on node labels)
```
"Schedule this pod only on nodes labeled: disk=ssd"
"Prefer nodes in zone: ap-south-1a"
```

**Pod Affinity / Anti-Affinity:** Attracts or repels pods based on **other pods** already running

```
Pod Affinity:
"Schedule this pod on a node that already has a pod labeled: app=redis"

Pod Anti-Affinity:
"Do NOT schedule this pod on a node that already has a pod labeled: app=nginx"
```

### Required vs Preferred

| Setting | Meaning |
|---|---|
| `requiredDuringSchedulingIgnoredDuringExecution` | **Hard rule** — pod won't schedule if rule can't be met |
| `preferredDuringSchedulingIgnoredDuringExecution` | **Soft rule** — try to meet it, but schedule anyway if can't |

### Impact

| With Affinity/Anti-Affinity | Without |
|---|---|
| Related pods co-located → lower latency | Random placement → inconsistent performance |
| Replicas spread across nodes → HA | All replicas may land on one node → SPOF |
| Precise control over scheduling | No guarantees on pod placement |

---

## 9. Kubernetes – Taints & Tolerations

### What
**Taints** and **Tolerations** work together to **control which pods can (or cannot) run on specific nodes**.

- **Taint** = A mark placed on a **node** that says "no ordinary pods allowed here"
- **Toleration** = A permission placed on a **pod** that says "I'm allowed on tainted nodes"

> **Analogy: VIP Entry Pass**
> - Taint = A VIP-only club (node)
> - Toleration = The VIP pass (pod)
> - Without the pass, the pod (person) can't enter

### Why

Real-world scenarios where you need dedicated nodes:
- **GPU nodes** — Only AI/ML workloads should run here (GPU is expensive)
- **High-memory nodes** — Only memory-intensive databases
- **Maintenance** — Node being drained for upgrades (taint it so no new pods land)
- **Compliance** — PCI-DSS or HIPAA workloads must run on specific certified nodes

### How (Step-by-Step)

**Step 1 – Add a taint to a node:**
```bash
kubectl taint nodes <node-name> key=value:effect

# Examples:
kubectl taint nodes gpu-node-1 hardware=gpu:NoSchedule
kubectl taint nodes db-node-2  tier=database:NoSchedule
```

**Three taint effects:**

| Effect | What happens to a pod WITHOUT toleration |
|---|---|
| `NoSchedule` | New pod is NOT scheduled on this node |
| `PreferNoSchedule` | Kubernetes tries to avoid this node (soft) |
| `NoExecute` | Existing pods are EVICTED + new pods blocked |

**Step 2 – Add a toleration to a pod:**
```yaml
tolerations:
- key: "hardware"
  operator: "Equal"
  value: "gpu"
  effect: "NoSchedule"
```

### Taint vs Affinity

| | Taint / Toleration | Affinity |
|---|---|---|
| **Set on** | Node (taint) + Pod (toleration) | Pod only |
| **Direction** | Node **repels** pods (unless toleration) | Pod **seeks** or **avoids** nodes/pods |
| **Primary use** | Dedicated / restricted nodes | Co-location, spreading |

### Impact

| With Taints & Tolerations | Without |
|---|---|
| GPU nodes reserved for ML workloads | Regular pods consume GPU resources unnecessarily |
| Maintenance drains work cleanly | Pods keep scheduling on nodes being repaired |
| Compliance workloads isolated | Sensitive data mixed with general workloads |

---

## 10. Kubernetes – Ingress

### What
An **Ingress** is a Kubernetes resource that **manages external access to services** inside the cluster using HTTP/HTTPS routing rules.

Without Ingress: every service needs its own Load Balancer (expensive — each costs ~$20/month on AWS).
With Ingress: **one Load Balancer handles all traffic**, routing to the right service based on the URL/hostname.

> **Analogy: Main Gate + Security Guard**
> The Ingress is the main gate of the building. One entrance, but the guard (Ingress Controller) knows exactly which floor (service) to send each visitor to.

### Why

```
Without Ingress:
  app.company.com   → Load Balancer 1 → Service A
  api.company.com   → Load Balancer 2 → Service B
  blog.company.com  → Load Balancer 3 → Service C
  Cost: 3 × $20 = $60/month

With Ingress:
  app.company.com   ─┐
  api.company.com   ─┼──► Single Load Balancer ──► Ingress Controller
  blog.company.com  ─┘                              routes to correct service
  Cost: 1 × $20 = $20/month
```

### How

**Components:**
1. **Ingress Resource** — YAML file defining routing rules
2. **Ingress Controller** — The software that reads those rules and actually routes traffic (e.g., Nginx Ingress Controller, AWS ALB Ingress Controller)

**Routing types:**

| Type | Example | Routes to |
|---|---|---|
| Host-based | `app.company.com` | Web service |
| Host-based | `api.company.com` | API service |
| Path-based | `company.com/app` | Web service |
| Path-based | `company.com/api` | API service |

### Impact

| With Ingress | Without Ingress |
|---|---|
| One load balancer for all services | One LB per service — high cost |
| Centralized SSL/TLS termination | SSL configured per service |
| Single entry point with routing rules | Manage multiple public IPs |
| Easy to add new services | New service = new LB = more cost |

---

## 11. Kubernetes – Network Policy

### What
A **Network Policy** defines rules for **how pods can communicate with each other** and with external endpoints — like a firewall inside the cluster.

By default, Kubernetes allows **all-to-all** communication. Any pod can talk to any other pod. Network Policies restrict this.

> **Analogy: Security Guard controlling internal access**
> Inside the building, without a security guard, anyone can walk into any room. Network Policy is the internal access control system.

### Why

In a microservices architecture:
- The **frontend** should talk to the **backend API**
- The **backend API** should talk to the **database**
- The **frontend should NOT** talk directly to the **database**
- No pod should talk to pods in other namespaces unless explicitly allowed

Without Network Policies, if an attacker compromises the frontend pod, they can directly query the database. Network Policies limit the blast radius.

### How

**Traffic directions:**
- **Ingress** (incoming traffic to a pod)
- **Egress** (outgoing traffic from a pod)

**Selectors:**
- `podSelector` — which pods this policy applies to
- `namespaceSelector` — allow traffic from specific namespaces
- `ipBlock` — allow/deny specific IP ranges

### Impact

| With Network Policy | Without Network Policy |
|---|---|
| Compromised frontend can't reach DB | Attacker pivots from frontend to database |
| Microservices have enforced boundaries | Any pod can talk to any pod |
| Compliance requirements met (PCI-DSS) | No network isolation |
| "Least privilege" for networking | Overly permissive network |

---

## 12. Real-World Analogies Summary

| Kubernetes Concept | Real-World Analogy |
|---|---|
| **Liveness Probe** | 🫀 Heartbeat monitor in a hospital — flatlines = immediate intervention |
| **Readiness Probe** | 🪧 "Open for Business" sign — customers wait until the sign flips |
| **Affinity** | 👫 Friends choosing to sit at the same table |
| **Anti-Affinity** | 📚 Exam students placed in separate rooms |
| **Taint** | 🚫 VIP-only club — regular guests not allowed |
| **Toleration** | 🎫 VIP pass — grants entry to the restricted club |
| **Ingress** | 🏢 Main gate of a building — one entrance, internal routing |
| **Network Policy** | 🔐 Internal security guard — controls room-to-room access |

---

## 13. Visual Diagrams

### Multi-Cloud ATS Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Cloud                                │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           EC2 Ubuntu (T2 Large, 30GB)                    │  │
│  │                                                          │  │
│  │  Python Virtual Environment (venv)                       │  │
│  │  ├── Streamlit (web framework)                           │  │
│  │  ├── PyPDF2 (PDF text extraction)                        │  │
│  │  └── google-generativeai (Gemini SDK)                    │  │
│  │                                                          │  │
│  │  .streamlit/secrets.toml                                 │  │
│  │    GOOGLE_API_KEY = "AIzaSy..."                          │  │
│  │                                                          │  │
│  │  Port 8501 (opened in Security Group)                    │  │
│  └────────────────────────────┬─────────────────────────────┘  │
│                               │                                 │
└───────────────────────────────┼─────────────────────────────────┘
                                │ HTTPS API call
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        GCP Cloud                                │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Gemini API (Generative Language API)           │  │
│  │                                                          │  │
│  │  Input:  Job Description + Resume Text                   │  │
│  │  Output: Match % + Missing Keywords + Feedback           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

User → http://EC2-IP:8501 → Streamlit App → GCP Gemini → Results
```

---

### ATS App User Flow

```
User opens browser
      │
      ▼
Streamlit UI (port 8501)
      │
      ├── [Text Box]  Paste Job Description
      ├── [File Upload] Upload Resume PDF
      └── [Button] Click "Analyze"
            │
            ▼
      PyPDF2 extracts text from PDF
            │
            ▼
      Build prompt:
        "Given this JD: [JD text]
         And this resume: [resume text]
         Calculate match % and give feedback"
            │
            ▼
      google-generativeai sends to Gemini API
      (authenticated with GOOGLE_API_KEY)
            │
            ▼
      Gemini returns JSON/text:
        - Match: 74%
        - Missing: Python, AWS, Docker
        - Strengths: Communication, Project Management
        - Recommendation: Add cloud certifications
            │
            ▼
      Streamlit displays results to user
```

---

### Kubernetes Probes Flow

```
Pod Lifecycle with Probes:
─────────────────────────────────────────────────────

Pod starts
    │
    ▼
Container process launches
    │
    ├─── READINESS PROBE begins checking
    │         │
    │    App still starting (DB connections, cache warmup)
    │    Probe FAILS → Pod NOT in Service endpoints
    │    (no traffic reaches pod yet)
    │         │
    │    App ready (30 seconds later)
    │    Probe PASSES → Pod added to Service endpoints
    │    ✅ Traffic starts flowing
    │
    └─── LIVENESS PROBE begins checking (ongoing)
              │
         App healthy → Probe PASSES → Container runs
              │
         Memory leak → App freezes → Probe FAILS (3x)
              │
         Kubernetes RESTARTS container
              │
         Back to top ↑ (new container, probes restart)
```

---

### Affinity & Anti-Affinity

```
AFFINITY (keep together):
─────────────────────────
Node A                    Node B
┌─────────────────┐      ┌─────────────────┐
│  Web Pod   ✅   │      │                 │
│  Cache Pod ✅   │      │   (empty)       │
│  (same node =   │      │                 │
│   low latency)  │      │                 │
└─────────────────┘      └─────────────────┘

ANTI-AFFINITY (keep apart for HA):
────────────────────────────────────
Node A                    Node B
┌─────────────────┐      ┌─────────────────┐
│  Nginx Pod 1 ✅ │      │  Nginx Pod 2 ✅  │
│                 │      │                 │
│ (if Node A      │      │ (backup survives │
│  goes down)     │      │  on Node B)      │
└─────────────────┘      └─────────────────┘
Node A failure → only Pod 1 lost, Pod 2 still serves traffic
```

---

### Taints & Tolerations

```
Without Toleration:              With Toleration:
──────────────────               ─────────────────
GPU Node                         GPU Node
[TAINTED: hardware=gpu]          [TAINTED: hardware=gpu]
        │                                │
Regular Pod (no toleration)      ML Pod (has toleration)
        │                                │
        ✗ BLOCKED                        ✓ ALLOWED
   "NoSchedule"                  toleration matches taint
```

---

### Ingress Routing

```
Internet
    │
    ▼
┌─────────────────────────────────┐
│    Load Balancer (single LB)    │
└─────────────┬───────────────────┘
              │
              ▼
┌─────────────────────────────────┐
│      Ingress Controller         │
│      (e.g., Nginx Ingress)      │
│                                 │
│  Rules:                         │
│  app.company.com  → web-svc     │
│  api.company.com  → api-svc     │
│  /static          → cdn-svc     │
└──────┬──────────┬───────────────┘
       │          │
       ▼          ▼
  web-service  api-service
  (Pod 1,2,3)  (Pod 4,5,6)
```

---

### Network Policy – Allow/Deny

```
WITHOUT Network Policy (default):
──────────────────────────────────
Frontend Pod ←──────────────► Database Pod  ✅ (allowed — dangerous!)
Backend Pod  ←──────────────► Database Pod  ✅
Any Pod      ←──────────────► Any Pod       ✅

WITH Network Policy:
────────────────────
Frontend Pod ────────────────► Backend Pod   ✅ (allowed by policy)
Frontend Pod ────────────────► Database Pod  ✗  (BLOCKED by policy)
Backend Pod  ────────────────► Database Pod  ✅ (allowed by policy)
Unknown Pod  ────────────────► Database Pod  ✗  (BLOCKED — default deny)
```

---

## 14. Scenario-Based Q&A

---

🔍 **Scenario 1:** You deployed a Node.js app on Kubernetes. After running fine for hours, the app occasionally freezes — users get timeouts, but the pod shows as "Running." Kubernetes never restarts it. How do you fix this?

✅ **Answer:** The pod is alive (process running) but not functional — a classic liveness probe missing scenario. Add a **Liveness Probe** that hits the app's `/health` endpoint every 30 seconds. Set `failureThreshold: 3`. Now when the app freezes, the probe fails 3 consecutive times → Kubernetes automatically restarts the container → users get a brief blip instead of hours of downtime.

---

🔍 **Scenario 2:** Your team does rolling deployments. During each deployment, new pods start but take 45 seconds to connect to the database and warm up. Users are hitting 502 errors for ~45 seconds during every deploy. How do you solve this?

✅ **Answer:** Add a **Readiness Probe** with `initialDelaySeconds: 45` (or better — probe the `/ready` endpoint that returns 200 only when DB is connected). The new pods will not receive traffic until the readiness probe passes. The old pods (still healthy) continue serving until new pods are ready. Zero-downtime rolling deployment achieved.

---

🔍 **Scenario 3:** Your company has 3 EC2 nodes in a K8s cluster. Two nodes are t3.large (general), one is g4dn.xlarge (GPU, very expensive). Your data science team deploys ML model pods that need GPU. But regular web app pods are also landing on the GPU node, wasting expensive GPU resources. How do you fix this?

✅ **Answer:** **Taint** the GPU node: `kubectl taint nodes gpu-node hardware=gpu:NoSchedule`. Now no regular pods can land on it. Add a **Toleration** to the ML deployment pods YAML (`tolerations: - key: hardware, value: gpu`). ML pods run on the GPU node; regular pods stay on the t3.large nodes. GPU resources saved for actual ML workloads.

---

🔍 **Scenario 4:** Your microservices cluster has 5 replicas of an API service. You're worried that if 2 nodes go down simultaneously, you might lose most or all replicas (if they all landed on those nodes). How do you ensure high availability?

✅ **Answer:** Add **Pod Anti-Affinity** to the API service deployment. Set `requiredDuringScheduling` with anti-affinity rule: "Do not schedule this pod on a node that already has a pod with label `app=api-service`." This forces each of the 5 replicas onto 5 different nodes. Even if 2 nodes go down, 3 replicas are still healthy and serving traffic.

---

🔍 **Scenario 5:** Your Kubernetes cluster hosts 8 different microservices, each behind its own LoadBalancer service. Your AWS bill shows 8 load balancers at $20/month each = $160/month just for load balancers. How do you cut this cost?

✅ **Answer:** Switch all LoadBalancer services to ClusterIP (internal only). Deploy an **Ingress Controller** (AWS ALB Ingress or Nginx). Write an **Ingress resource** with host-based and path-based routing rules for all 8 services. Now one ALB handles all external traffic — cost drops from $160/month to $20/month. Add TLS termination at the Ingress level as a bonus.

---

🔍 **Scenario 6:** Your ATS app's Streamlit is running on EC2 but you're getting a 403 Forbidden error when calling the Gemini API. How do you debug it?

✅ **Answer:** Systematic debugging:
1. **Is the API enabled?** → GCP Console → APIs & Services → Enabled APIs → look for "Generative Language API"
2. **Correct project?** → Check the API key was generated from the same GCP project where the API is enabled
3. **IP restriction?** → If the key has IP restrictions, add the EC2's public IP to the allowed list
4. **Billing enabled?** → GCP requires billing to be enabled even for free-tier API calls
5. **Quota exceeded?** → GCP Console → APIs & Services → Quotas → check Generative Language API limits
6. **Test the key directly:** `curl -H "Content-Type: application/json" "https://generativelanguage.googleapis.com/v1/models?key=YOUR_KEY"` — should return model list if key is valid

---

## 15. Interview Q&A

---

**Q1. What is the difference between a Liveness Probe and a Readiness Probe in Kubernetes?**

**A:** A Liveness Probe checks if a container is alive and functioning. When it fails, Kubernetes restarts the container. A Readiness Probe checks if a container is ready to accept traffic. When it fails, the pod is removed from the load balancer endpoints — it's not restarted, just taken out of rotation until it recovers. Liveness = "Is it running at all?" Readiness = "Is it ready to serve?" Real example: a Java app that takes 60 seconds to start — liveness passes immediately (JVM started), readiness fails until Spring Boot fully initializes.

---

**Q2. Can a pod have both a liveness and readiness probe? When would you use both?**

**A:** Yes, and using both is the best practice. The readiness probe handles startup and temporary unavailability — keeps traffic away until ready. The liveness probe handles ongoing health — detects hung/deadlocked containers and restarts them. Example: a Node.js app with a database connection. Readiness checks `db.isConnected()` → prevents traffic during DB reconnect. Liveness checks `/health` HTTP → restarts if the event loop hangs.

---

**Q3. What is the difference between Node Affinity and Pod Affinity?**

**A:** Node Affinity attracts or repels pods based on **node labels** — "Schedule this pod only on nodes with SSD storage" or "Prefer nodes in us-east-1a." Pod Affinity/Anti-Affinity controls scheduling based on **other pods** already running — "Schedule near pods labeled app=redis" (for performance) or "Don't schedule near pods labeled app=nginx" (for availability). Node Affinity = relationship between pod and node. Pod Affinity = relationship between pods.

---

**Q4. What is the difference between Taints/Tolerations and Affinity?**

**A:** Taints/Tolerations are set on the **node** to repel pods — it's the node saying "I only accept specific pods." Affinity is set on the **pod** to attract itself toward certain nodes or other pods — it's the pod choosing where to go. They solve opposite sides of the same problem. Taints are typically used for dedicated infrastructure (GPU nodes, maintenance) where you want to strictly prevent unwanted pods. Affinity is used for performance optimization (co-location) and availability (spreading).

---

**Q5. Explain Kubernetes Ingress and why it's preferred over LoadBalancer service type.**

**A:** A LoadBalancer service creates a cloud load balancer (e.g., AWS ELB) per service — expensive at scale. Ingress is an API object that defines HTTP/HTTPS routing rules, handled by an Ingress Controller (like Nginx or AWS ALB Controller). One Ingress Controller uses one load balancer and routes traffic to multiple services based on hostname or path. Benefits: significant cost reduction, centralized SSL/TLS termination, single entry point for the cluster, and easier to manage routing rules as YAML instead of cloud console clicks.

---

**Q6. What is a Network Policy and what is the default behavior in Kubernetes without one?**

**A:** Without any Network Policies, Kubernetes allows **all traffic between all pods** in the cluster — any pod can reach any other pod on any port. A Network Policy is a YAML resource that defines allow-rules for ingress (incoming) and egress (outgoing) traffic to/from pods using selectors. Once any Network Policy selects a pod, all traffic to that pod is denied by default except what the policy explicitly allows. Example: allow only the API pod to reach the database pod, blocking everything else.

---

**Q7. Why should you use `NoExecute` taint effect during node maintenance instead of `NoSchedule`?**

**A:** `NoSchedule` prevents **new** pods from being scheduled on the node but leaves existing pods running. During maintenance (patching the OS, replacing hardware), you want existing pods to move off the node too — that's what `NoExecute` does. It evicts currently running pods AND blocks new ones. The pods are rescheduled to other nodes automatically (assuming resources are available). You'd also typically use `kubectl drain` alongside taints for a proper maintenance workflow.

---

**Q8. How does Streamlit handle secrets and why is it better than hardcoding API keys?**

**A:** Streamlit has a built-in secrets management system using `.streamlit/secrets.toml`. Keys are stored in this file and accessed in code via `st.secrets["KEY_NAME"]`. This is better than hardcoding because: (1) the `.toml` file is never committed to Git (add to `.gitignore`), so keys don't leak through version control, (2) different environments (dev, prod) can have different secrets files, (3) it's clean and readable in code. For production, this pattern is upgraded to AWS Secrets Manager or GCP Secret Manager, fetched at runtime.

---

**Q9. What is the Taint effect `PreferNoSchedule` and when would you use it?**

**A:** `PreferNoSchedule` is a soft taint — Kubernetes will try to avoid scheduling pods on this node but will still do so if there's no other option (unlike `NoSchedule` which is a hard block). Use case: you want to gradually migrate workloads off a node (perhaps upgrading its hardware next week) but don't want to hard-drain it yet. Or for nodes that have slightly different hardware where you prefer other nodes but allow fallback. Think of it as a "polite suggestion" rather than a strict rule.

---

**Q10. Describe the full flow of deploying an app on Kubernetes with all the discussed concepts applied.**

**A:** Full production-grade K8s deployment:
1. **Deployment** with 3 replicas, resource requests/limits
2. **Readiness Probe** on `/ready` with `initialDelaySeconds: 30` — no traffic until warm
3. **Liveness Probe** on `/health` with `failureThreshold: 3` — auto-restart if hung
4. **Pod Anti-Affinity** — spread 3 replicas across 3 different nodes for HA
5. **Node Affinity** — prefer nodes in the same AZ as the database
6. **Tolerations** — if the node is tainted for this app tier, add matching toleration
7. **Service** (ClusterIP) — internal access only
8. **Ingress** — expose via `api.company.com` with TLS, single load balancer
9. **NetworkPolicy** — allow only frontend pods to reach this service; deny all others

---

## 16. Tech Stack Mapping

### ATS Project – Full Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit (Python) | Web UI — file upload + results display |
| **Backend** | Python 3 | PDF parsing, API calls, business logic |
| **AI Engine** | GCP Gemini API | Resume vs JD matching and scoring |
| **Hosting** | AWS EC2 (Ubuntu T2 Large) | Application server |
| **Port** | 8501 | Streamlit default (opened in SG) |
| **Secrets** | `.streamlit/secrets.toml` | Stores GOOGLE_API_KEY |
| **Dependencies** | `requirements.txt` | Managed via pip + venv |
| **Source Control** | GitHub | Clone + version management |

---

### Kubernetes Concepts in a Node.js/React Deployment

```
┌────────────────────────────────────────────────────────────────┐
│                  Production K8s Cluster                        │
│                                                                │
│  Ingress Controller (Nginx)                                    │
│  ├── app.company.com  → React Frontend Service                 │
│  └── api.company.com  → Node.js API Service                    │
│                                                                │
│  Node.js API Deployment (3 replicas)                           │
│  ├── Liveness Probe:  HTTP GET /health every 30s               │
│  ├── Readiness Probe: HTTP GET /ready (checks DB conn)         │
│  ├── Anti-Affinity:   Spread across 3 nodes                    │
│  └── Network Policy:  Only accept from Frontend pods           │
│                                                                │
│  PostgreSQL StatefulSet                                        │
│  ├── Toleration: tier=database (runs on dedicated DB node)     │
│  ├── Node Affinity: prefer storage-optimized nodes             │
│  └── Network Policy: only accept from API pods                 │
│                                                                │
│  Redis Cache Deployment                                        │
│  ├── Pod Affinity: run on same node as API (low latency)       │
│  └── Network Policy: only accept from API pods                 │
│                                                                │
│  Nodes:                                                        │
│  ├── node-1 (t3.large)   — API replica 1 + Redis              │
│  ├── node-2 (t3.large)   — API replica 2                       │
│  ├── node-3 (t3.large)   — API replica 3 + Frontend            │
│  └── node-4 (db.r5.large)— PostgreSQL [TAINTED: tier=database] │
└────────────────────────────────────────────────────────────────┘
```

---

### Jenkins Pipeline → K8s Deploy with Probes

```
Jenkins Pipeline
    │
    ├── Stage: Build → docker build → push to ECR
    │
    ├── Stage: Update K8s Deployment manifest
    │   (update image tag in deployment.yaml)
    │
    ├── Stage: kubectl apply -f deployment.yaml
    │   K8s starts rolling update:
    │       New pod starts
    │       Readiness Probe runs → FAILS (app loading)
    │       Old pod continues serving traffic
    │       Readiness Probe PASSES (30s later)
    │       New pod joins Service endpoints
    │       Old pod removed → deleted
    │       Repeat for next replica
    │
    └── Stage: Verify rollout
        kubectl rollout status deployment/myapp
```

---

## 17. Code / Practical Examples

### Example 1: EC2 Setup Script for ATS Project

```bash
#!/bin/bash
# setup_ats.sh – Run on fresh EC2 Ubuntu 22.04 instance

set -e

echo "=== [1/6] System Update ==="
sudo apt-get update -y && sudo apt-get upgrade -y

echo "=== [2/6] Install Python + Git ==="
sudo apt-get install -y python3 python3-pip python3-venv git tmux

echo "=== [3/6] Clone Project ==="
git clone https://github.com/CloudDevOpsHub/batch-43.git
cd batch-43

echo "=== [4/6] Virtual Environment ==="
python3 -m venv venv
source venv/bin/activate

echo "=== [5/6] Install Dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt
pip install google-generativeai

echo "=== [6/6] Create secrets directory ==="
mkdir -p .streamlit
cat << 'EOF' > .streamlit/secrets.toml
# Replace with your actual GCP Gemini API key
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
EOF

echo ""
echo "✅ Setup complete!"
echo "Next steps:"
echo "  1. Edit .streamlit/secrets.toml with your API key"
echo "  2. Run: source venv/bin/activate"
echo "  3. Run: streamlit run app.py --server.port 8501 --server.address 0.0.0.0"
echo "  4. Access at: http://$(curl -s ifconfig.me):8501"
```

---

### Example 2: Liveness and Readiness Probe YAML

```yaml
# deployment-with-probes.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nodejs-api
  labels:
    app: nodejs-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nodejs-api
  template:
    metadata:
      labels:
        app: nodejs-api
    spec:
      containers:
      - name: nodejs-api
        image: 123456789.dkr.ecr.ap-south-1.amazonaws.com/nodejs-api:latest
        ports:
        - containerPort: 3000

        # ─── READINESS PROBE ──────────────────────────────────────
        # Pod won't receive traffic until this passes
        readinessProbe:
          httpGet:
            path: /ready        # endpoint that checks DB connection, cache, etc.
            port: 3000
          initialDelaySeconds: 30   # wait 30s before first check (app startup time)
          periodSeconds: 10         # check every 10 seconds
          failureThreshold: 3       # fail 3 times before marking not-ready
          successThreshold: 1       # pass once to be marked ready

        # ─── LIVENESS PROBE ───────────────────────────────────────
        # Container is restarted if this fails
        livenessProbe:
          httpGet:
            path: /health       # lightweight health check endpoint
            port: 3000
          initialDelaySeconds: 60   # give app time to start before checking liveness
          periodSeconds: 30         # check every 30 seconds
          failureThreshold: 3       # restart after 3 consecutive failures
          timeoutSeconds: 5         # request must respond within 5 seconds

        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

---

### Example 3: Pod Anti-Affinity (Spread Replicas Across Nodes)

```yaml
# deployment-anti-affinity.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nodejs-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nodejs-api
  template:
    metadata:
      labels:
        app: nodejs-api
    spec:
      # ─── ANTI-AFFINITY: No two replicas on the same node ──────
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:   # hard rule
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - nodejs-api
            topologyKey: "kubernetes.io/hostname"   # "one per node"
            # Use "topology.kubernetes.io/zone" to spread across AZs instead

      containers:
      - name: nodejs-api
        image: my-api:latest
        ports:
        - containerPort: 3000
```

---

### Example 4: Taints & Tolerations for GPU Node

```bash
# ─── TAINT THE GPU NODE ─────────────────────────────────────────
kubectl taint nodes gpu-node-1 hardware=gpu:NoSchedule
kubectl taint nodes gpu-node-1 hardware=gpu:NoExecute   # also evict existing pods

# Verify taint applied
kubectl describe node gpu-node-1 | grep Taints
```

```yaml
# ml-deployment.yaml – ML pod with matching toleration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ml-model
  template:
    metadata:
      labels:
        app: ml-model
    spec:
      # ─── TOLERATION: Allow this pod on the tainted GPU node ───
      tolerations:
      - key: "hardware"
        operator: "Equal"
        value: "gpu"
        effect: "NoSchedule"
      - key: "hardware"
        operator: "Equal"
        value: "gpu"
        effect: "NoExecute"

      # ─── NODE AFFINITY: Prefer the GPU node ───────────────────
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            preference:
              matchExpressions:
              - key: hardware
                operator: In
                values:
                - gpu

      containers:
      - name: ml-server
        image: ml-model:latest
        resources:
          limits:
            nvidia.com/gpu: 1   # request 1 GPU
```

---

### Example 5: Ingress with TLS and Multiple Services

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"   # auto SSL via cert-manager
spec:
  tls:
  - hosts:
    - app.company.com
    - api.company.com
    secretName: company-tls   # cert-manager auto-populates this

  rules:
  # ─── Host-based routing ───────────────────────────────────────
  - host: app.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80

  - host: api.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 3000

  # ─── Path-based routing on same host ─────────────────────────
  - host: company.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 3000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

---

### Example 6: Network Policy – Frontend Can Reach API, Not Database

```yaml
# network-policy-api.yaml
# Rule: Only pods labeled app=frontend can talk to the API service

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow-frontend-only
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-service      # This policy applies to API pods

  policyTypes:
  - Ingress
  - Egress

  ingress:
  # ─── Only allow traffic FROM frontend pods ────────────────────
  - from:
    - podSelector:
        matchLabels:
          app: frontend     # only frontend pods can reach API
    ports:
    - protocol: TCP
      port: 3000

  egress:
  # ─── Allow API to reach database ──────────────────────────────
  - to:
    - podSelector:
        matchLabels:
          app: postgresql
    ports:
    - protocol: TCP
      port: 5432

  # ─── Allow API to reach Redis cache ───────────────────────────
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379

  # ─── Allow DNS resolution ─────────────────────────────────────
  - to: []
    ports:
    - protocol: UDP
      port: 53
```

```yaml
# network-policy-database.yaml
# Rule: Database only accepts connections from API pods

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-allow-api-only
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: postgresql

  policyTypes:
  - Ingress

  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-service    # ONLY api pods
    ports:
    - protocol: TCP
      port: 5432
  # All other traffic (including frontend, other namespaces) = BLOCKED
```

---

### Example 7: Node.js Health and Readiness Endpoints

```javascript
// health.js – Add these routes to your Express app
// Used by Kubernetes liveness and readiness probes

const express = require('express');
const router = express.Router();

let isReady = false;

// Called by Readiness Probe
// Returns 200 only when app is fully initialized
router.get('/ready', async (req, res) => {
    try {
        // Check database connection
        await db.query('SELECT 1');

        // Check Redis connection
        await redis.ping();

        // Check required env vars
        if (!process.env.DB_HOST || !process.env.REDIS_URL) {
            return res.status(503).json({
                status: 'not_ready',
                reason: 'Missing required environment variables'
            });
        }

        res.status(200).json({ status: 'ready' });
    } catch (error) {
        res.status(503).json({
            status: 'not_ready',
            reason: error.message
        });
    }
});

// Called by Liveness Probe
// Returns 200 as long as the process is alive and event loop is unblocked
router.get('/health', (req, res) => {
    res.status(200).json({
        status: 'alive',
        uptime: process.uptime(),
        timestamp: new Date().toISOString()
    });
});

// Mark app as ready after initialization
async function initialize() {
    await connectDatabase();
    await connectRedis();
    await loadConfiguration();
    isReady = true;
    console.log('✅ App initialized and ready');
}

module.exports = { router, initialize };
```

---

### Example 8: Jenkins Pipeline – Build → Push → Deploy to K8s

```groovy
// Jenkinsfile – Full CI/CD to Kubernetes with probes in deployment
pipeline {
    agent any

    environment {
        ECR_REPO   = "123456789.dkr.ecr.ap-south-1.amazonaws.com/myapp"
        K8S_NS     = "production"
        DEPLOY_NAME = "nodejs-api"
    }

    stages {
        stage('Build & Test') {
            steps {
                sh 'npm ci && npm test'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $ECR_REPO:$BUILD_NUMBER .
                    docker tag $ECR_REPO:$BUILD_NUMBER $ECR_REPO:latest
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region ap-south-1 | \
                      docker login --username AWS --password-stdin $ECR_REPO
                    docker push $ECR_REPO:$BUILD_NUMBER
                    docker push $ECR_REPO:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    # Update image tag in deployment
                    kubectl set image deployment/$DEPLOY_NAME \
                      $DEPLOY_NAME=$ECR_REPO:$BUILD_NUMBER \
                      -n $K8S_NS

                    # Wait for rolling update to complete
                    # (readiness probes ensure no pod gets traffic until ready)
                    kubectl rollout status deployment/$DEPLOY_NAME \
                      -n $K8S_NS \
                      --timeout=300s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    echo "=== Pod Status ==="
                    kubectl get pods -n $K8S_NS -l app=$DEPLOY_NAME

                    echo "=== Deployment Status ==="
                    kubectl describe deployment $DEPLOY_NAME -n $K8S_NS | \
                      grep -A5 "Conditions"
                '''
            }
        }
    }

    post {
        failure {
            sh '''
                echo "Deployment failed. Rolling back..."
                kubectl rollout undo deployment/$DEPLOY_NAME -n $K8S_NS
            '''
        }
    }
}
```

---

## Navigation Footer

← Previous: [`50_Multi-Cloud_ATS_App_(AWS_+_GCP)_&_Kubernetes_Concepts.md`](50_Multi-Cloud_ATS_App_(AWS_+_GCP)_&_Kubernetes_Concepts.md) | Next: [`51_Multi-Cloud_Comparison_(AWS_vs_GCP_vs_Azure)_&_Azure_DevOps.md`](51_Multi-Cloud_Comparison_(AWS_vs_GCP_vs_Azure)_&_Azure_DevOps.md) →