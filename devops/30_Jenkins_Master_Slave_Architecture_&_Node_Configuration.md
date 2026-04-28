# 30 – Jenkins Master-Slave Architecture & Node Configuration

---

## Table of Contents

1. [Why Master-Slave? The Problem It Solves](#1-why-master-slave-the-problem-it-solves)
2. [Master-Slave Architecture – How It Works](#2-master-slave-architecture--how-it-works)
3. [Jenkins Internal File Structure](#3-jenkins-internal-file-structure)
4. [Jenkins Installation on Windows (MSI Method)](#4-jenkins-installation-on-windows-msi-method)
5. [Setting Up a Slave Node – Step by Step](#5-setting-up-a-slave-node--step-by-step)
6. [Connecting the Slave Using agent.jar](#6-connecting-the-slave-using-agentjar)
7. [Assigning Jobs to Specific Nodes](#7-assigning-jobs-to-specific-nodes)
8. [Troubleshooting Offline Nodes](#8-troubleshooting-offline-nodes)
9. [Real-World Node Naming & Team Isolation](#9-real-world-node-naming--team-isolation)
10. [Assignment Configurations Reference](#10-assignment-configurations-reference)
11. [Visual Diagrams](#11-visual-diagrams)
12. [Scenario-Based Q&A](#12-scenario-based-qa)
13. [Interview Q&A](#13-interview-qa)

---

## 1. Why Master-Slave? The Problem It Solves

### What
**Master-Slave** (also called **Controller-Agent**) is a Jenkins architecture where one central Jenkins server (the **Master**) manages and distributes build jobs to one or more worker machines (the **Slaves/Agents**).

> 💡 **Analogy:** Think of a restaurant kitchen. The **head chef (Master)** doesn't cook every dish personally — they coordinate and assign tasks to **station chefs (Slaves)**. The head chef focuses on orchestration; the station chefs do the actual cooking. Each station is specialized — one for grill, one for pastry, one for cold dishes.

### Why — The Problem Without Master-Slave

Imagine a single Jenkins server handling everything for a team of 50 developers:
- Every developer pushes code → Jenkins triggers a build
- 10 builds running simultaneously on one machine
- The machine's CPU, RAM, and disk are maxed out
- Builds slow down dramatically or fail entirely
- The master server becomes a bottleneck and single point of failure
- Different teams need different environments (Java vs Python vs Node.js) — one machine can't cleanly support all

### How Master-Slave Fixes This

| Problem | Master-Slave Solution |
|---------|----------------------|
| Single machine overloaded | Distribute builds across multiple machines |
| Slow builds under heavy load | Parallel execution on multiple agents |
| Different teams need different environments | Each agent can have its own OS, tools, configs |
| Master crash = everything stops | Agents can queue and wait for master recovery |
| Can't scale horizontally | Add more agents as team grows |
| Security isolation needed | Agents in separate networks/VPCs |

### Impact

| Single Jenkins Server | Master-Slave Setup |
|----------------------|-------------------|
| Everything runs on one machine | Work distributed across many |
| Builds compete for resources | Parallel, isolated builds |
| Master does everything | Master only coordinates |
| Hard to scale | Add agents as needed |
| Environment conflicts between teams | Each team has a dedicated agent |
| Single point of failure | Agents are disposable |

---

## 2. Master-Slave Architecture – How It Works

### The Roles Explained

#### Jenkins Master (Controller)
The Master is the **brain** — it never does actual build work in a proper setup. Its responsibilities:
- Stores all configuration (jobs, credentials, plugins, user accounts)
- Schedules builds and assigns them to appropriate agents
- Monitors agent health (online/offline)
- Displays build results and console logs in the UI
- Manages security and access control
- Runs on port 8080 by default

#### Jenkins Slave (Agent)
The Slave is the **muscle** — it does the actual work. Each agent:
- Receives build jobs from the master
- Executes the pipeline/job steps in its workspace
- Reports results back to the master
- Can be any machine: physical server, VM, Docker container, cloud instance
- Runs a small Java program (`agent.jar`) to stay connected to master

### How a Build Actually Flows

```
Step 1: Developer pushes code to GitHub
Step 2: GitHub triggers Jenkins master (webhook) or master polls SCM
Step 3: Master receives trigger, looks up the job configuration
Step 4: Master checks which agents are available and match the job's requirements
Step 5: Master assigns the build to the best available agent
Step 6: Agent receives the assignment, pulls the code from GitHub
Step 7: Agent executes all pipeline stages (compile, test, package, deploy)
Step 8: Agent sends logs and result back to master in real time
Step 9: Master displays results in UI, sends notifications
Step 10: Agent workspace is cleaned up (optional)
```

### Agent Labels – How Jobs Find the Right Agent

Labels are **tags** assigned to agents that describe their capabilities. Jobs can target a specific label to ensure they run on the right machine.

| Label | What it means | Jobs that use it |
|-------|--------------|-----------------|
| `linux` | Ubuntu/CentOS agent | Shell script builds |
| `windows` | Windows agent | .NET builds, Windows-specific tests |
| `java-21` | Agent with Java 21 installed | Java/Spring Boot pipelines |
| `performance` | High-CPU agent for load tests | Performance testing jobs |
| `qa` | QA team's dedicated agent | Test suites, regression builds |
| `docker` | Agent with Docker installed | Container build pipelines |

---

## 3. Jenkins Internal File Structure

### What
Jenkins stores everything — jobs, plugins, configs, credentials, build history — in a directory on the master server's filesystem. Understanding this structure is critical for backup, recovery, and troubleshooting.

### Where It Lives

| OS | Default Jenkins Home |
|----|---------------------|
| Ubuntu/Linux (apt install) | `/var/lib/jenkins/` |
| Windows (MSI install) | `C:\ProgramData\Jenkins\.jenkins\` |
| WAR file (local) | `~/.jenkins/` (user's home) |

### The Key Files and Folders

```
Jenkins Home (/var/lib/jenkins/ or C:\ProgramData\Jenkins\.jenkins\)
│
├── config.xml              ← Master config: security, plugins, node list
│                              ⚠️ Backup this file first in any recovery
│
├── jobs/                   ← Every job you've ever created
│   ├── hello-world-job/
│   │   ├── config.xml      ← This specific job's configuration
│   │   └── builds/         ← All historical build results
│   │       ├── 1/          ← Build #1 logs and artifacts
│   │       └── 2/          ← Build #2 logs and artifacts
│   │
│   └── shopping-cart/
│       └── config.xml
│
├── plugins/                ← All installed plugins (.jpi or .hpi files)
│   ├── git.jpi
│   ├── pipeline.jpi
│   └── maven-plugin.jpi
│
├── secrets/                ← Encrypted credentials and secrets
│   ├── initialAdminPassword   ← First-time setup password
│   └── master.key             ← Encryption key for all credentials
│
├── workspace/              ← Where agents actually run builds
│   └── [job-name]/         ← Code pulled here, builds happen here
│
├── nodes/                  ← Slave node configurations
│   └── Shubh-Performance/
│       └── config.xml
│
└── users/                  ← User account data
    └── admin/
        └── config.xml
```

### config.xml – The Most Important File

`config.xml` at the root of Jenkins home is the **master configuration file**. It contains:
- Security settings (authentication, authorization matrix)
- List of all registered slave nodes
- Global environment variables
- Plugin configurations
- System settings (executors, labels, etc.)

> ⚠️ **Backup Rule:** Always backup `config.xml` + `jobs/` + `secrets/` before any major Jenkins change. These three together contain your entire Jenkins configuration.

---

## 4. Jenkins Installation on Windows (MSI Method)

### What
Jenkins provides a Windows MSI installer — a standard Windows setup wizard that installs Jenkins as a Windows Service, meaning it automatically starts on boot and runs in the background.

### Prerequisites
- Java JDK 21 or higher installed (`java -version` to verify)
- Windows 10/11 or Windows Server
- At least 2 GB RAM, 4 GB recommended

### Step-by-Step Installation

#### Step 1: Download the MSI Installer
```
Go to: https://www.jenkins.io/download/
Click: Windows (.msi) — approximately 101 MB
Save to: C:\Downloads\jenkins-2.xxx.msi
```

#### Step 2: Run the Installer
```
Double-click jenkins-2.xxx.msi
→ Welcome screen → Next
→ Destination folder: C:\Program Files\Jenkins\ → Next
→ Run Jenkins as: Local System Account → Next
→ Port: 8080 (default) → Test Port → Next
→ Java home: (auto-detected if JDK is installed)
→ Install → Finish
```

#### Step 3: Verify Jenkins is Running
```
Open browser: http://localhost:8080
You should see the "Unlock Jenkins" screen
```

#### Step 4: Get Initial Admin Password
```
From the Unlock Jenkins screen, note the path shown:
C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword

Open that file → Copy the password → Paste in browser
```

Or via PowerShell:
```powershell
type C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword
```

#### Step 5: Complete Setup
```
→ Install suggested plugins (wait 3-5 minutes)
→ Create first admin user
→ Set Jenkins URL: http://localhost:8080/
→ Start using Jenkins ✅
```

### Windows Service Management

```powershell
# Check if Jenkins service is running
Get-Service -Name jenkins

# Start Jenkins
Start-Service -Name jenkins

# Stop Jenkins
Stop-Service -Name jenkins

# Restart Jenkins
Restart-Service -Name jenkins
```

Or via Windows Services UI:
```
Win + R → services.msc → Find "Jenkins" → Right-click → Start/Stop/Restart
```

---

## 5. Setting Up a Slave Node – Step by Step

### What
Adding a slave node in Jenkins means telling the master "here is another machine that can run builds." Jenkins needs the machine's details, then provides a secret key and a command to run on the slave machine to establish the connection.

### Step 1: Add a New Node in Jenkins UI

```
Jenkins Dashboard
→ Manage Jenkins
→ Nodes (or "Manage Nodes and Clouds")
→ New Node
```

#### Fill in Node Details:

```
Node Name: Shubh-Performance-Team
           (descriptive name — shows in UI and used for job assignment)

Type: Permanent Agent → OK
```

#### Configure the Agent:

| Field | Value | Why |
|-------|-------|-----|
| **Description** | "Performance team Windows agent" | Documentation |
| **Number of Executors** | 2 | How many jobs can run simultaneously on this agent |
| **Remote Root Directory** | `C:\Dev\28April_slave` | Where Jenkins will store workspace on the slave |
| **Labels** | `performance windows java-21` | Tags used to target this agent from jobs |
| **Usage** | "Use this node as much as possible" | Or "Only when specifically requested" |
| **Launch Method** | Launch agent by connecting to the controller | Agent initiates connection (firewall-friendly) |

> 💡 **Number of Executors:** If set to 2, this agent can run 2 build jobs simultaneously. For a powerful machine (8 CPU, 16 GB RAM), you might set this to 4-6.

#### Step 2: Save the Node
```
Click Save
→ Jenkins creates the node configuration
→ Status: ⚠️ Offline (not yet connected)
```

---

## 6. Connecting the Slave Using agent.jar

### What
The `agent.jar` file is a small Java program that runs on the slave machine. It connects back to the Jenkins master and receives build jobs. The slave always initiates the connection to the master — this is firewall-friendly (no need to open inbound ports on the slave).

### Step 1: Get the Connection Command from Jenkins

```
Jenkins Dashboard → Nodes → [Your New Node]
→ Status page shows: "Run from agent command line:"
```

You'll see something like:
```bash
curl -sO http://MASTER_IP:8080/jnlpJars/agent.jar
java -jar agent.jar \
  -url http://MASTER_IP:8080/ \
  -secret abc123def456... \
  -name "Shubh-Performance-Team" \
  -webSocket \
  -workDir "C:\Dev\28April_slave"
```

### Step 2: Run on the Slave Machine

Open a terminal/PowerShell on the slave machine and run:

#### Download agent.jar
```bash
# Windows PowerShell:
curl -sO http://192.168.1.100:8080/jnlpJars/agent.jar

# Or manually download from browser:
http://MASTER_IP:8080/jnlpJars/agent.jar
# Save as agent.jar in C:\Dev\28April_slave\
```

#### Connect the Slave to Master
```bash
java -jar agent.jar `
  -url http://192.168.1.100:8080/ `
  -secret abc123def456789secretkey `
  -name "Shubh-Performance-Team" `
  -webSocket `
  -workDir "C:\Dev\28April_slave"
```

#### What Each Flag Means:

| Flag | Value | What it does |
|------|-------|-------------|
| `-url` | `http://MASTER_IP:8080/` | Address of Jenkins master |
| `-secret` | `abc123...` | One-time secret key (unique per node, generated by Jenkins) |
| `-name` | `"Shubh-Performance-Team"` | Must match the node name created in Jenkins |
| `-webSocket` | (no value) | Use WebSocket protocol instead of JNLP (more firewall-friendly) |
| `-workDir` | `C:\Dev\28April_slave` | Where to store build workspaces on this machine |

### Step 3: Verify Connection

After running the command:
```
Output: INFO: Connected
```

Back in Jenkins:
```
Nodes → Shubh-Performance-Team → Status: ✅ Online
```

The node is now ready to receive jobs.

### Keeping the Agent Running

The `java -jar agent.jar` command runs in the foreground — closing the terminal disconnects the agent. To keep it running:

**Option 1: Windows — Run as a Service**
Use tools like `nssm` (Non-Sucking Service Manager) to wrap the agent as a Windows service.

**Option 2: Linux — Use `nohup`**
```bash
nohup java -jar agent.jar -url ... -secret ... -name ... -webSocket -workDir ... &
```

**Option 3: Linux — Systemd Service**
Create a service file so the agent starts automatically on boot.

---

## 7. Assigning Jobs to Specific Nodes

### What
Once you have multiple agents online, you need to tell each job *which* agent to run on. Jenkins provides two mechanisms — one for Freestyle jobs, one for Pipeline jobs.

---

### For Freestyle Jobs – "Restrict where this project can be run"

```
Job → Configure
→ General section
→ Check: "Restrict where this project can be run"
→ Label Expression: Shubh-Performance-Team
                    (or a label like "performance" if multiple agents have that label)
→ Save
```

When you click "Build Now," Jenkins assigns this job only to agents matching the label expression.

---

### For Pipeline Jobs – `agent` Directive

In your Jenkinsfile, change the `agent` line:

#### Run on a specific named agent:
```groovy
pipeline {
    agent { label 'Shubh-Performance-Team' }

    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
    }
}
```

#### Run on any agent with a specific label:
```groovy
pipeline {
    agent { label 'performance' }
    // Runs on any agent tagged with "performance"
}
```

#### Different stages on different agents:
```groovy
pipeline {
    agent none   // No global agent

    stages {
        stage('Build') {
            agent { label 'java-21' }   // Build on Java agent
            steps {
                sh 'mvn clean package'
            }
        }
        stage('Performance Test') {
            agent { label 'performance' }   // Test on performance agent
            steps {
                sh 'run-load-test.sh'
            }
        }
        stage('Deploy') {
            agent { label 'prod-deploy' }   // Deploy on prod agent
            steps {
                sh 'deploy.sh'
            }
        }
    }
}
```

> 💡 **This is powerful:** Different stages of the same pipeline can run on completely different machines. Build on a fast machine, test on a machine that mirrors production, deploy on a machine with production credentials.

---

## 8. Troubleshooting Offline Nodes

### What Happens When a Slave Goes Offline

When a slave machine goes offline (rebooted, network issue, agent process killed), any jobs assigned to it:
- If not yet started → **wait in a "pending" state** until the agent comes back online
- If already running → **fail immediately** with a "connection lost" error

### How to Reconnect an Offline Node

#### Method 1: Reconnect via Jenkins UI
```
Manage Jenkins → Nodes → [Offline Node]
→ Click "Launch Agent" (if configured for automatic reconnection)
```

#### Method 2: Re-run the agent.jar command on the slave machine
```bash
# On the slave machine — run this again:
java -jar agent.jar \
  -url http://MASTER_IP:8080/ \
  -secret abc123... \
  -name "Shubh-Performance-Team" \
  -webSocket \
  -workDir "C:\Dev\28April_slave"
```

After this, the node comes back online and pending jobs start running automatically.

### Common Reasons Agents Go Offline

| Reason | Fix |
|--------|-----|
| Slave machine rebooted | Re-run agent.jar command (or set up as service) |
| Network connectivity lost | Fix network, then re-run agent.jar |
| agent.jar process was killed | Re-run agent.jar |
| Jenkins master restarted | Re-run agent.jar (connection is reset) |
| Wrong secret key | Delete and recreate the node in Jenkins |
| Java not found on slave | Install/verify Java on slave machine |
| Firewall blocking WebSocket | Open required ports or use different launch method |

### Viewing Node Status

```
Jenkins Dashboard → Manage Jenkins → Nodes

Each node shows:
  ✅ Online — ready for builds
  ⚠️ Offline — disconnected, jobs pending
  🔄 Busy — currently running a build
  💤 Suspended — manually taken offline by admin
```

---

## 9. Real-World Node Naming & Team Isolation

### What
In production companies, Jenkins agents are organized by team, environment, or purpose. The naming convention from class reflects real enterprise setups.

### Examples from Class

| Node Name | What it represents |
|-----------|-------------------|
| `Shubh-Performance-Team` | Dedicated agent for Shubh's performance testing team |
| `Varun-QA` | Dedicated agent for Varun's QA/testing team |

### Real Enterprise Node Organization

| Node Label | Purpose | Environment |
|-----------|---------|-------------|
| `build-java-linux` | Java compilation and packaging | Ubuntu with JDK 21 |
| `build-dotnet-windows` | .NET builds | Windows Server with .NET 6 |
| `test-qa-regression` | QA regression test suite | Ubuntu with browsers |
| `performance-high-cpu` | Load testing | 8 CPU, 32 GB RAM machine |
| `deploy-staging` | Staging deployments | Has staging credentials |
| `deploy-prod` | Production deployments | Locked down, prod credentials only |
| `docker-build` | Container image builds | Has Docker daemon |
| `aws-agent` | AWS-specific deployments | Has AWS CLI + credentials |

### Benefits of Team Isolation

```
Dev Team Jobs → Build Agent (standard machine)
             → Fast builds, standard tools

QA Team Jobs → QA Agent (browsers, test tools)
             → Isolated test environments

Performance Team → Performance Agent (high-CPU machine)
                → Load tests don't impact other teams' builds

Production Deploy → Prod Agent (locked down, audited)
                 → Only authorized pipelines can target this
```

---

## 10. Assignment Configurations Reference

Three setups were assigned for practice. Here's how each differs:

### Assignment 1: Ubuntu Master → Ubuntu Slave

```
Master: GCP Ubuntu VM (Jenkins installed via apt)
Slave:  Another GCP Ubuntu VM

On Slave:
  sudo apt install default-jre -y   ← Java required on slave
  mkdir -p /home/ubuntu/jenkins-slave
  curl -sO http://MASTER_IP:8080/jnlpJars/agent.jar
  java -jar agent.jar \
    -url http://MASTER_IP:8080/ \
    -secret SECRET_KEY \
    -name "ubuntu-slave" \
    -webSocket \
    -workDir "/home/ubuntu/jenkins-slave"
```

### Assignment 2: Ubuntu Master → CentOS Slave

```
Master: Ubuntu VM (Jenkins)
Slave:  CentOS VM

Key difference on CentOS:
  sudo yum install java-21-openjdk -y   ← Different package manager
  mkdir -p /opt/jenkins-slave
  # Rest of agent.jar connection is identical
  java -jar agent.jar -url ... -secret ... -name ... -webSocket -workDir /opt/jenkins-slave
```

### Assignment 3: GCP Ubuntu Master → AWS Ubuntu Slave (Multi-Cloud)

```
Master: GCP VM (Jenkins)
Slave:  AWS EC2 instance

Key considerations:
  1. AWS Security Group must allow inbound on port 8080 from GCP IP
     (or use WebSocket which typically uses 443/80)
  2. Slave needs internet access to reach master's public IP
  3. Use public IP of GCP master in the -url flag:
     -url http://GCP_EXTERNAL_IP:8080/
  4. Java must be installed on the AWS instance
  
On AWS EC2 (Ubuntu):
  sudo apt update
  sudo apt install openjdk-21-jre -y
  curl -sO http://GCP_EXTERNAL_IP:8080/jnlpJars/agent.jar
  java -jar agent.jar \
    -url http://GCP_EXTERNAL_IP:8080/ \
    -secret SECRET_KEY \
    -name "aws-slave" \
    -webSocket \
    -workDir "/home/ubuntu/jenkins-slave"
```

---

## 11. Visual Diagrams

### Diagram 1: Master-Slave Architecture Overview

```
                    ┌──────────────────────────────────┐
                    │         JENKINS MASTER           │
                    │         (Controller)             │
                    │                                  │
                    │  • Stores all configs            │
                    │  • Manages job queue             │
                    │  • Assigns work to agents        │
                    │  • Displays results in UI        │
                    │  • Port 8080                     │
                    └──────────────┬───────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
   ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
   │  SLAVE / AGENT 1 │ │  SLAVE / AGENT 2 │ │  SLAVE / AGENT 3 │
   │                  │ │                  │ │                  │
   │  Shubh-          │ │  Varun-QA        │ │  AWS-Prod-Agent  │
   │  Performance     │ │                  │ │                  │
   │                  │ │  Label: qa       │ │  Label: prod     │
   │  Label:          │ │  Executors: 2    │ │  Executors: 1    │
   │  performance     │ │  Windows VM      │ │  AWS EC2         │
   │  Executors: 4    │ │                  │ │                  │
   │  High-CPU VM     │ │  Runs: Test jobs │ │  Runs: Prod      │
   │                  │ │                  │ │  deployments     │
   │  Runs: Load tests│ │                  │ │                  │
   └──────────────────┘ └──────────────────┘ └──────────────────┘
```

---

### Diagram 2: agent.jar Connection Flow

```
JENKINS MASTER                         SLAVE MACHINE
───────────────                        ─────────────────────
                                       Step 1: Download agent.jar
                                       curl http://MASTER:8080/jnlpJars/agent.jar
                                                │
                                                ▼
Generates secret key ◄──────────────── Step 2: Run agent.jar
(unique per node)                      java -jar agent.jar
                                         -url http://MASTER:8080/
                                         -secret abc123...
                                         -name "node-name"
                                         -webSocket
                                         -workDir /jenkins-slave
                                                │
                                                │ WebSocket connection
                                                │ (slave initiates →)
                                                ▼
Receives connection ──────────────────────────────────────────►
Marks node: ✅ Online

Master assigns builds ────────────────────────────────────────►
                                       Executes builds in workDir
                                       Sends logs back ◄────────────
```

---

### Diagram 3: Jenkins Home Directory Structure

```
/var/lib/jenkins/          (Linux) OR C:\ProgramData\Jenkins\.jenkins\  (Windows)
│
├── config.xml ⭐          ← MOST IMPORTANT: master settings, node list, security
│
├── jobs/                  ← All your Jenkins jobs
│   ├── shopping-cart/
│   │   ├── config.xml     ← Job configuration
│   │   └── builds/
│   │       ├── 1/         ← Build #1 result + logs
│   │       └── 2/         ← Build #2 result + logs
│   └── hello-world/
│       └── config.xml
│
├── plugins/               ← Installed plugins (.jpi files)
│   ├── git.jpi
│   └── pipeline.jpi
│
├── secrets/ 🔒            ← Encrypted credentials
│   ├── initialAdminPassword
│   └── master.key
│
├── nodes/                 ← Slave node configurations
│   └── Shubh-Performance/
│       └── config.xml
│
├── workspace/             ← Where code is checked out and built
│   └── shopping-cart/     ← Cloned repo + build artifacts live here
│
└── users/                 ← Jenkins user accounts
    └── admin/
```

---

### Diagram 4: Job Assignment Flow

```
Developer pushes code
        │
        ▼
Jenkins Master receives trigger
        │
        ▼
Master reads job config:
  "Restrict to: performance"
        │
        ▼
Master checks available agents:
  Agent 1: "performance" label ✅ → FREE
  Agent 2: "qa" label        ❌ → Wrong label
  Agent 3: "performance" label ✅ → BUSY
        │
        ▼
Master assigns job to Agent 1
        │
        ▼
Agent 1 executes the build
        │
        ▼
Agent 1 reports result to Master
        │
        ▼
Master displays SUCCESS/FAILURE in UI
```

---

### Diagram 5: Node Offline – Job Pending Flow

```
Job triggered
     │
     ▼
Jenkins checks: "Varun-QA" node available?
     │
     ├── YES → Assign immediately → Build runs
     │
     └── NO (node offline)
              │
              ▼
         Job enters PENDING state
              │
              │  (Waiting...)
              │
              ▼
         Admin re-runs agent.jar on slave
              │
              ▼
         Node comes back ONLINE
              │
              ▼
         Jenkins automatically assigns pending job
              │
              ▼
         Build runs ✅
```

---

### Diagram 6: Multi-Stage Pipeline on Multiple Agents

```
pipeline { agent none }
         │
         ▼
Stage: 'Build'
  agent { label 'java-21' }
  → Runs on Build Agent (Ubuntu + JDK 21)
  → sh 'mvn clean package'
         │
         ▼
Stage: 'Performance Test'
  agent { label 'performance' }
  → Runs on High-CPU Agent
  → sh 'run-load-test.sh'
         │
         ▼
Stage: 'Deploy'
  agent { label 'prod-deploy' }
  → Runs on Locked-down Prod Agent
  → sh 'kubectl apply -f deployment.yaml'

Result: 3 stages, 3 different machines, one pipeline ✅
```

---

### Diagram 7: Assignment Configurations

```
Assignment 1: Ubuntu → Ubuntu (Same Cloud)
┌──────────────┐              ┌──────────────┐
│  GCP Ubuntu  │◄─WebSocket──►│  GCP Ubuntu  │
│  MASTER      │              │  SLAVE       │
│  Jenkins UI  │              │  agent.jar   │
└──────────────┘              └──────────────┘

Assignment 2: Ubuntu → CentOS (Different OS)
┌──────────────┐              ┌──────────────┐
│  GCP Ubuntu  │◄─WebSocket──►│  GCP CentOS  │
│  MASTER      │              │  SLAVE       │
│  apt install │              │  yum install │
└──────────────┘              └──────────────┘

Assignment 3: GCP → AWS (Multi-Cloud)
┌──────────────┐              ┌──────────────┐
│  GCP Ubuntu  │◄─WebSocket──►│  AWS EC2     │
│  MASTER      │   (Internet) │  SLAVE       │
│  Public IP   │              │  Public IP   │
└──────────────┘              └──────────────┘
  ⚠️ Requires: Public IPs, Security Groups allowing WebSocket
```

---

## 12. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your team has 30 developers, 5 QA engineers, and a performance team. All builds are running on a single Jenkins server and everything is slow. Builds that used to take 5 minutes now take 30. What's the solution?

✅ **Answer:** This is the classic single-server bottleneck. Set up a Master-Slave architecture with dedicated agents per team: a **Build Agent** for developer CI builds (high executor count, fast machine), a **QA Agent** with browsers and testing tools, and a **Performance Agent** with high CPU for load tests. Label each agent appropriately. Configure developer jobs to target the Build Agent, QA jobs to target the QA Agent, and performance jobs to target the Performance Agent. Jobs stop competing for resources, builds run in parallel, and each team's environment is isolated.

---

🔍 **Scenario 2:** You've set up a slave node, but after configuring it in Jenkins, the node shows as "Offline." The Jenkins UI shows no way to connect it automatically. What do you do?

✅ **Answer:** Go to Jenkins → Nodes → your offline node → click the node name → copy the agent connection command shown on the page. Go to the slave machine, ensure Java is installed (`java -version`), download `agent.jar` using the curl command provided, then run the full Java command with the `-url`, `-secret`, `-name`, `-webSocket`, and `-workDir` flags. Once the command runs successfully, you'll see "INFO: Connected" in the terminal and the node will flip to Online in Jenkins UI automatically.

---

🔍 **Scenario 3:** A critical pipeline is stuck in "pending" state for 2 hours. No one can figure out why. What's happening and how do you investigate?

✅ **Answer:** The job is waiting for an agent that matches its label requirement but no such agent is currently online. Check: Jenkins → Nodes — look for any offline agents. The job's configuration (or Jenkinsfile) specifies a label (e.g., `agent { label 'performance' }`), and no agent with that label is available. Solutions: (1) Reconnect the offline agent by re-running the `agent.jar` command on the slave machine, (2) If the agent machine is down, temporarily change the job's agent to `any` to unblock it, (3) Fix the underlying reason the agent went offline (machine rebooted, network issue, agent process killed).

---

🔍 **Scenario 4:** Your company has a strict security policy: only one specific Jenkins agent is allowed to run production deployments, and it must have production credentials. How do you enforce this with Master-Slave?

✅ **Answer:** Create a dedicated production agent labeled `prod-deploy`. Store production credentials (API keys, kubeconfig, SSH keys) only on that machine and in Jenkins Credentials scoped to that agent. In all production deployment Jenkinsfiles, use `agent { label 'prod-deploy' }` for the deploy stage. Configure **Branch Protection** rules in Jenkins (using the Role-based Authorization plugin) so only authorized pipelines can trigger jobs targeting the `prod-deploy` label. The combination of label targeting + credential scoping + RBAC means production credentials can only be accessed through the designated machine and authorized pipelines.

---

🔍 **Scenario 5:** You've successfully set up a Windows slave, but every time the slave machine reboots, you have to manually run the `agent.jar` command again. Your manager wants this to be automatic. What do you do?

✅ **Answer:** Install the `agent.jar` startup as a **Windows Service** so it runs automatically on boot. Use **NSSM** (Non-Sucking Service Manager — a free Windows tool): download NSSM, then run `nssm install JenkinsAgent` and configure it with the `java -jar agent.jar ...` command, the working directory, and auto-restart settings. Alternatively, add the agent.jar command to Windows **Task Scheduler** with the trigger set to "At system startup." After this, every time the machine boots, the Jenkins agent connects automatically and the node comes online without any manual intervention.

---

🔍 **Scenario 6:** Your organization is migrating from a single data center to a hybrid cloud (some VMs on GCP, some on AWS). Jenkins master is on GCP. How do you extend Jenkins builds to AWS agents?

✅ **Answer:** This is the multi-cloud master-slave setup from Assignment 3. Create a new node in Jenkins with the name and label for the AWS agent. On the AWS EC2 instance: ensure Java is installed, open the required port in the AWS Security Group (or use WebSocket over port 443/80 which is usually allowed), download `agent.jar` from the Jenkins master's public GCP IP, and run the connection command. The `-url` flag uses the master's **public external IP** (not internal/private). Once connected, jobs labeled for this agent run on AWS while the Jenkins master on GCP remains the central coordinator. This is how enterprises span CI/CD across multiple clouds.

---

## 13. Interview Q&A

---

**Q1. What is Jenkins Master-Slave architecture and why is it used?**

**A:** Jenkins Master-Slave (or Controller-Agent) is an architecture where one central Jenkins server (the master) manages job scheduling, configuration, and UI, while multiple worker machines (agents/slaves) do the actual build work. It's used because: a single Jenkins server cannot scale to handle builds for large teams simultaneously, different projects need different environments (Java vs Python vs .NET), teams need isolated build environments, parallel execution requires multiple machines, and security isolation demands that production credentials exist only on specific agents. The master orchestrates; the agents execute.

---

**Q2. How does a Jenkins slave connect to the master? What is agent.jar?**

**A:** `agent.jar` is a small Java program that runs on the slave machine and establishes a connection to the Jenkins master. The connection is always **initiated by the slave** (not the master), which makes it firewall-friendly — you don't need to open inbound ports on the slave. The connection process: create the node in Jenkins → Jenkins generates a unique secret key → on the slave, download agent.jar via curl from the master → run `java -jar agent.jar -url [MASTER_URL] -secret [SECRET] -name [NODE_NAME] -webSocket -workDir [PATH]` → the slave connects and appears online in Jenkins. The `-webSocket` flag uses the WebSocket protocol, which typically works through most corporate firewalls.

---

**Q3. What is the difference between `agent any` and `agent { label 'performance' }` in a Jenkinsfile?**

**A:** `agent any` tells Jenkins to run the pipeline on any available agent — Jenkins picks whichever node is free, regardless of its capabilities or labels. `agent { label 'performance' }` restricts execution to only agents tagged with the "performance" label. If no such agent is online, the job waits in pending state until one becomes available. In a multi-agent environment, `agent any` is for general builds; label-based targeting is for specialized workloads — performance testing on a high-CPU machine, production deployments on a locked-down agent, or Windows-specific builds on a Windows agent.

---

**Q4. What is the Jenkins `config.xml` file and why is it important?**

**A:** `config.xml` at the Jenkins home root is the master configuration file — it stores everything about the Jenkins setup: security settings, authentication configuration, authorization matrix, registered slave nodes, global environment variables, plugin settings, and system parameters. It's the single most critical file for backup and recovery. If Jenkins' database were lost, restoring `config.xml` + the `jobs/` folder + the `secrets/` folder would restore your entire Jenkins setup. In production, these three should be backed up before every major change and automatically by backup tools (dedicated Jenkins backup plugins or external backup solutions).

---

**Q5. What happens to running jobs when a Jenkins slave goes offline?**

**A:** Two scenarios: (1) If a job is already running on the agent when it goes offline — the job fails immediately with a "connection lost" or "agent disconnected" error in the console. The build is marked as FAILURE. (2) If a job is queued and waiting to run on an agent that goes offline — the job enters a PENDING state and waits indefinitely for an agent with the matching label to come back online. It does not fail; it just waits. When the agent is reconnected (by re-running the `agent.jar` command), the pending job automatically starts. Admins can monitor node status at Manage Jenkins → Nodes.

---

**Q6. How do you restrict a Freestyle job to run only on a specific Jenkins agent?**

**A:** In the Freestyle job configuration (Job → Configure → General section), check the box "Restrict where this project can be run" and enter a Label Expression in the field. The label expression can be: an exact node name (`Shubh-Performance-Team`), a label shared by multiple nodes (`performance`), or a boolean expression (`performance && windows` for a node that has both labels). Jenkins will only run the job on agents matching this expression. If no matching agent is available, the job waits in the queue until one becomes online.

---

**Q7. What are the key differences when setting up slaves on Ubuntu vs CentOS?**

**A:** The core agent.jar process is identical across both — it's the same Java command. The differences are in the pre-requisite setup on the slave machine:
- **Package manager:** Ubuntu uses `apt` (`sudo apt install openjdk-21-jre -y`); CentOS uses `yum` or `dnf` (`sudo yum install java-21-openjdk -y`)
- **Default paths:** Ubuntu stores Java at `/usr/lib/jvm/`; CentOS at `/usr/lib/jvm/java-21-openjdk/`
- **Firewall tool:** Ubuntu uses `ufw`; CentOS uses `firewalld`
- **Service management:** Both use `systemd` in modern versions

Once Java is installed, the `curl` and `java -jar agent.jar` commands are identical regardless of Linux distribution.

---

**Q8. How does a multi-cloud Jenkins setup (GCP master, AWS slave) differ from a same-cloud setup?**

**A:** The key differences in multi-cloud: (1) **Networking** — the slave uses the master's **public external IP** in the `-url` flag, not a private/internal IP. Private IPs only work within the same network. (2) **Firewall/Security Groups** — the AWS Security Group must allow outbound WebSocket connections from the AWS instance to the GCP master's IP and port. (3) **Latency** — cross-cloud connections add network latency; build times may be slightly longer. (4) **Egress costs** — cloud providers charge for outbound data; large artifact transfers between clouds can incur costs. The agent.jar command itself is identical — only the `-url` flag changes to use the public IP. This pattern is common in enterprise environments with hybrid or multi-cloud strategies.

---

**Q9. What files should you back up to fully recover a Jenkins installation?**

**A:** Three critical locations in the Jenkins home directory:
1. **`config.xml`** (root) — master configuration: security, nodes, global settings
2. **`jobs/`** folder — all job configurations and build history
3. **`secrets/`** folder — encrypted credentials and the master encryption key

Additionally backup: `plugins/` (to restore installed plugins without re-downloading), `nodes/` (slave node configurations), and `users/` (user account data). In production, automate backups using the **ThinBackup** or **Backup** Jenkins plugin, or use infrastructure-as-code (storing your Jenkinsfiles in Git, job configs in Job DSL) so Jenkins can be rebuilt from scratch without manual backup. The most important principle: if your Jenkinsfiles are in Git and your jobs are defined as code, a Jenkins crash is a minor inconvenience, not a disaster.

---

← Previous: [`29_Jenkins_Pipelines_Declarative_Scripted_&_CI_Integration.md`](29_Jenkins_Pipelines_Declarative_Scripted_&_CI_Integration.md) | Next: [`31_Next_Topic.md`](Next_Topic.md) →