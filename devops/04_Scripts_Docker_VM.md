# 🛠️ Scripts, Docker & VM Setup — Practical Reference

> **File:** `04_Scripts_Docker_VM.md`
> **Topic:** Docker Installation Scripts, Container Deployment, GCP VM Creation Commands
> **Level:** 🟢 Beginner Friendly

---

## 📚 Table of Contents

1. [Docker Installation Script](#1-docker-installation-script)
2. [Running a Docker Container](#2-running-a-docker-container)
3. [GCP VM Creation Command](#3-gcp-vm-creation-command)
4. [Scenario-Based Q&A](#4-scenario-based-qa)
5. [Interview Q&A](#5-interview-qa)

---

## 1. Docker Installation Script

### 📖 What
A shell script that automatically installs Docker Engine on a Linux machine using Docker's official installation script.

### 🤔 Why
Docker is the foundation of modern containerized deployments. Instead of manually running multiple commands to install it, this script automates the entire process in two lines.

### ⚙️ How

```bash
# Step 1: Download the official Docker installation script
curl -fsSL https://get.docker.com -o install-docker.sh

# Step 2: Run the installation script with sudo privileges
sudo sh install-docker.sh
```

**Flag Breakdown:**
| Flag | Meaning |
|------|---------|
| `-f` | Fail silently on HTTP errors |
| `-s` | Silent mode — don't show progress bar |
| `-S` | Show errors even in silent mode |
| `-L` | Follow redirects (if the URL redirects) |
| `-o` | Output to a file instead of stdout |

### 💥 Impact
- **With script:** Docker installed in ~2 minutes with zero manual steps
- **Without script:** You'd need to manually add repositories, GPG keys, update package lists, and install — 10+ commands and easy to make mistakes

---

## 2. Running a Docker Container

### 📖 What
This command runs a pre-built Docker container that emulates a Windows 11 React-based interface in a web browser.

### 🤔 Why
Demonstrates how Docker can run complex applications with a single command — no installation, no configuration, no dependency management.

### ⚙️ How

```bash
docker run -d --restart unless-stopped --name win11react -p 3000:3000 blueedge/win11react:latest
```

**Flag Breakdown:**

| Flag | Meaning |
|------|---------|
| `-d` | Run in **detached mode** (background) — you get your terminal back |
| `--restart unless-stopped` | Automatically restart the container if it crashes or the server reboots, unless you manually stop it |
| `--name win11react` | Give the container a friendly name instead of a random one |
| `-p 3000:3000` | Map port 3000 on host to port 3000 in the container |
| `blueedge/win11react:latest` | The Docker image name and tag to use |

### 💥 Impact
- **With Docker:** One command to run a full Windows 11 React app — no Node.js installation, no npm setup, no build process
- **Without Docker:** You'd need to clone the repo, install Node.js, install dependencies, configure the build, and start the server — 15+ minutes of setup

```
┌───────────────────────────────────────────────┐
│              HOW DOCKER RUN WORKS              │
│                                               │
│   Your Machine (Host)                         │
│   ┌──────────────────────────────────────┐    │
│   │  Port 3000 ◄──── mapped to ────►    │    │
│   │                                      │    │
│   │   Docker Container                   │    │
│   │   ┌──────────────────────────────┐   │    │
│   │   │  win11react App              │   │    │
│   │   │  Running on Port 3000       │   │    │
│   │   │  (Isolated environment)      │   │    │
│   │   └──────────────────────────────┘   │    │
│   └──────────────────────────────────────┘    │
│                                               │
│   Access: http://localhost:3000               │
└───────────────────────────────────────────────┘
```

---

## 3. GCP VM Creation Command

### 📖 What
A `gcloud` CLI command that creates a Linux virtual machine on Google Cloud Platform with Ubuntu 24.04, configures monitoring, and sets up network firewall rules.

### 🤔 Why
In DevOps, we automate infrastructure creation using CLI commands or IaC tools rather than clicking through GUIs. This command creates a fully configured VM in one shot — reproducible and scriptable.

### ⚙️ How

```bash
gcloud compute instances create linuxfirst \
  --project=nishant-learn \
  --zone=us-central1-c \
  --machine-type=e2-medium \
  --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
  --metadata=enable-osconfig=TRUE \
  --maintenance-policy=MIGRATE \
  --provisioning-model=STANDARD \
  --service-account=370978152656-compute@developer.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write \
  --tags=http-server,https-server \
  --create-disk=auto-delete=yes,boot=yes,device-name=linuxfirst,image=projects/ubuntu-os-cloud/global/images/ubuntu-2404-noble-amd64-v20260316,mode=rw,size=10,type=pd-balanced \
  --shielded-vtpm \
  --shielded-integrity-monitoring \
  --labels=goog-ops-agent-policy=v2-template-1-5-0
```

**Key Parameters Explained:**

| Parameter | Value | What It Does |
|-----------|-------|-------------|
| `--project` | `nishant-learn` | Which GCP project to create the VM in |
| `--zone` | `us-central1-c` | Physical location of the VM |
| `--machine-type` | `e2-medium` | 2 vCPUs, 4 GB RAM (cost-effective general purpose) |
| `--tags` | `http-server,https-server` | Enables firewall rules for web traffic (ports 80 & 443) |
| `--create-disk` | Ubuntu 24.04, 10GB, pd-balanced | Boot disk with Ubuntu OS |
| `--shielded-vtpm` | — | Enables virtual Trusted Platform Module for security |
| `--maintenance-policy=MIGRATE` | — | If Google needs to maintain hardware, your VM moves seamlessly (no downtime) |

### 💥 Impact
- **With CLI:** Create identical VMs in seconds, scriptable, repeatable, version-controllable
- **With GUI:** Click through 8+ screens, manual, error-prone, can't be saved as code

---

## 4. Scenario-Based Q&A

### 🔍 Scenario 1: New Team Member Setup
A new intern joins and needs Docker on their Linux machine. They've never used Linux before.

✅ **Answer:** Give them the two-line Docker installation script. Instead of following a 10-step manual process, they run `curl -fsSL https://get.docker.com -o install-docker.sh && sudo sh install-docker.sh` and Docker is ready. Then `docker run hello-world` to verify it works.

---

### 🔍 Scenario 2: Demo Environment Needed in 5 Minutes
Your manager wants to see a demo of a React application running right now, but you don't have Node.js installed.

✅ **Answer:** Use Docker! Run `docker run -d -p 3000:3000 blueedge/win11react:latest` and show them the app at `http://localhost:3000`. No Node.js required — Docker containers include everything the app needs.

---

### 🔍 Scenario 3: Reproducible Infrastructure
Your team needs to create the same VM setup across 3 different environments (dev, staging, production).

✅ **Answer:** Save the `gcloud` command as a shell script with variables for environment-specific values. Run the same script for each environment, ensuring consistency. Better yet, use Terraform to define the VM as code.

---

## 5. Interview Q&A

### Q1: What does `docker run -d` do?
> **Answer:** The `-d` flag runs the container in **detached mode** (background). Without it, the container runs in the foreground and occupies your terminal. With `-d`, you get your terminal back and the container runs in the background.

### Q2: What does the `--restart unless-stopped` policy mean?
> **Answer:** It means Docker will automatically restart the container if it crashes or if the Docker daemon/host restarts — UNLESS you explicitly stop the container with `docker stop`. It's ideal for production services that should always be running.

### Q3: What is port mapping in Docker (`-p 3000:3000`)?
> **Answer:** Port mapping connects a port on the host machine to a port inside the container. `-p 3000:3000` means "traffic hitting port 3000 on my machine should be forwarded to port 3000 inside the container." Format: `-p HOST_PORT:CONTAINER_PORT`.

### Q4: Why use CLI to create a VM instead of the GCP Console GUI?
> **Answer:** CLI commands are **scriptable, repeatable, and version-controllable**. You can save the command in a script, put it in Git, and create identical VMs every time. GUI clicks can't be saved, reviewed, or automated.

### Q5: What is the difference between `curl` and `wget`?
> **Answer:** Both download files from the internet. `curl` is more versatile — it supports more protocols, can send data (POST requests), and can output to stdout. `wget` is simpler and better for recursive downloads. In DevOps, `curl` is more commonly used because of its flexibility.

---

← Previous: [03_Cloud_Computing_And_Data_Centers.md](03_Cloud_Computing_And_Data_Centers.md) | Next: [05_DevOps_Basics_Tools_and_Roles.md](05_DevOps_Basics_Tools_and_Roles.md) →
