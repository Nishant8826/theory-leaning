# 26 – Introduction to CI/CD and Jenkins

---

## Table of Contents

1. [What is CI/CD?](#1-what-is-cicd)
2. [Continuous Integration (CI) – Deep Dive](#2-continuous-integration-ci--deep-dive)
3. [The CI Pipeline – Step by Step](#3-the-ci-pipeline--step-by-step)
4. [Jenkins – The CI/CD Engine](#4-jenkins--the-cicd-engine)
5. [Jenkins Setup – From Zero to Running](#5-jenkins-setup--from-zero-to-running)
6. [Your First Jenkins Job](#6-your-first-jenkins-job)
7. [Key Commands Reference](#7-key-commands-reference)
8. [Visual Diagrams](#8-visual-diagrams)
9. [Scenario-Based Q&A](#9-scenario-based-qa)
10. [Interview Q&A](#10-interview-qa)

---

## 1. What is CI/CD?

### What
**CI/CD** stands for **Continuous Integration / Continuous Delivery (or Deployment)**. It is a set of automated practices that allow development teams to deliver code changes more frequently, reliably, and safely.

Think of it as an **automated assembly line for software** — code goes in one end, and a tested, packaged, deployable product comes out the other.

### Why
Before CI/CD existed, releasing software looked like this:
- Developers worked on separate code for weeks or months
- Code was manually merged at the end ("integration hell")
- A dedicated QA team manually tested everything
- Deployment was a stressful, all-hands event that could take days
- Bugs discovered late were expensive and slow to fix

CI/CD solves all of this by **automating the entire path from code commit to deployment**.

### The Two Halves

| Term | What it means | Simplified |
|------|--------------|-----------|
| **Continuous Integration (CI)** | Automatically build and test code every time someone pushes a change | "Is the code working?" |
| **Continuous Delivery (CD)** | Automatically prepare a release-ready build after every successful CI | "Is it ready to ship?" |
| **Continuous Deployment (CD)** | Automatically deploy to production after every successful test | "Ship it automatically" |

> 💡 **Key insight:** "Continuous" doesn't mean "instant" — it means *automated and triggered* by every code change, not done manually on a schedule.

### Impact

| Without CI/CD | With CI/CD |
|--------------|-----------|
| Manual builds and testing | Automated on every commit |
| Bugs found weeks late | Bugs found within minutes |
| Big, risky releases every few months | Small, safe releases every day |
| "It works on my machine" chaos | Consistent, reproducible builds |
| Developer waits for QA feedback for days | Feedback in minutes |
| Deployment = stressful event | Deployment = routine, boring (good!) |

---

## 2. Continuous Integration (CI) – Deep Dive

### What
CI is the first and most foundational part of the CI/CD pipeline. It is the **automated process that kicks off every time a developer pushes code** to a shared repository.

The goal: **catch problems early, automatically, before they compound**.

### Why
The word "integration" refers to combining code from multiple developers into a single shared codebase. Without automation:
- Developer A and Developer B both change the same codebase for 2 weeks
- When they finally merge, nothing works together
- Fixing it takes another week (this is called "integration hell")

CI prevents this by integrating and testing code **continuously** — many times per day — so problems surface immediately while they're still small and easy to fix.

### How – The CI Process

Every CI run follows this sequence, triggered automatically by a `git push`:

```
Code Push → Compilation → Build → Unit Tests → Quality Gates → Artifact → Package → Deploy
```

Each stage is explained in the next section.

### The Three Core Benefits (Remember These)

1. **Improved Quality** — Automated tests catch bugs before humans ever see them
2. **Increased Productivity** — Developers stop wasting time on manual builds and testing
3. **Reduced Risk** — Small, frequent changes are far less risky than large, infrequent ones

---

## 3. The CI Pipeline – Step by Step

This is the exact workflow covered in class. Every stage has a purpose. Understand each one.

---

### Stage 1: Code Push
- **What happens:** A developer finishes a feature, commits, and pushes to GitHub (their feature branch or main)
- **Trigger:** This event *automatically triggers* the entire CI pipeline
- **Tool:** Git / GitHub

---

### Stage 2: Compilation
- **What happens:** The CI tool (Jenkins) pulls the code and checks whether it compiles without errors
- **Why:** Catches syntax errors, missing imports, type errors — the most basic level of code correctness
- **Outcome:** ✅ Compiles clean → move to next stage | ❌ Compile error → pipeline fails, developer notified immediately
- **Tool:** Java compiler (`javac`), Maven, Gradle

---

### Stage 3: Build
- **What happens:** The code is assembled into a runnable package (e.g., a `.jar` file for Java, a Docker image, etc.)
- **Why:** Compilation checks syntax; building checks that everything links together correctly
- **Tool:** Maven (`mvn build`), Gradle, npm, etc.

---

### Stage 4: Unit Testing
- **What happens:** Automated tests (written by developers) are executed against the new code
- **Why:** Verifies that each small piece of functionality (unit) works as expected
- **Outcome:** All tests pass → continue | Any test fails → pipeline stops, developer notified
- **Tool:** JUnit (Java), pytest (Python), Jest (JavaScript)

> 💡 **Unit test analogy:** Like checking each brick individually before building a wall. If one brick is broken, you catch it before the wall is built.

---

### Stage 5: Quality Gates (SonarQube)
- **What happens:** The code is scanned for quality issues — code duplication, complexity, security vulnerabilities, maintainability
- **What is SonarQube?** A tool that analyzes code quality and gives it a score/rating. If the score is below a set threshold, the pipeline fails.
- **Why:** Passing tests doesn't mean code is *good*. SonarQube catches bad patterns that tests don't.
- **Examples of what it catches:** Copy-pasted code blocks, functions that are 500 lines long, hardcoded passwords, known security vulnerabilities

---

### Stage 6: Artifact Generation
- **What happens:** A deployable output file is created — the "artifact"
- **What is an artifact?** The final packaged output of a build. For Java: a `.jar` or `.war` file. For Node: a bundle. For Docker: an image.
- **Why:** This artifact is what actually gets deployed to servers — not the raw source code
- **Tool:** Maven, Gradle, Docker

---

### Stage 7: Packaging
- **What happens:** The artifact is stored in a centralized repository for versioning and distribution
- **Why:** So the exact build can be retrieved, deployed, or rolled back at any time
- **Tool:** Nexus, JFrog Artifactory, AWS ECR (for Docker images)

---

### Stage 8: Deployment
- **What happens:** The packaged artifact is deployed to an environment (Dev, QA, Staging, or Production)
- **Why:** Makes the new code available for testing or real users
- **Tool:** Kubernetes, Ansible, Terraform, AWS CodeDeploy

---

### CI Pipeline Summary Table

| Stage | What it checks | Fails if... |
|-------|---------------|------------|
| Code Push | Triggers pipeline | - |
| Compilation | Syntax & imports correct | Code doesn't compile |
| Build | Everything links together | Build errors |
| Unit Testing | Logic works as intended | Any test fails |
| Quality Gates | Code quality & security | Score below threshold |
| Artifact Generation | Creates deployable output | Build output invalid |
| Packaging | Stores artifact for deployment | Storage/config error |
| Deployment | Runs the application | Deploy script fails |

---

## 4. Jenkins – The CI/CD Engine

### What
Jenkins is the most popular **open-source automation server** used to implement CI/CD pipelines. It watches your code repository and automatically runs your pipeline whenever code is pushed.

- **Market Share:** 60–70% of CI/CD market
- **Type:** Open-source (free)
- **Language:** Written in Java
- **Version in class:** 2.55.1
- **Plugins:** 2,000+ community-built plugins

> 💡 **Analogy:** If a CI/CD pipeline is an assembly line, Jenkins is the factory manager who coordinates every station on the line.

### Why Jenkins?
- **Free and open-source** — no licensing cost
- **Hugely flexible** — integrates with virtually any tool via plugins (GitHub, Docker, Kubernetes, Slack, SonarQube, AWS, etc.)
- **Battle-tested** — used by companies of all sizes for 15+ years
- **Large community** — thousands of plugins, tutorials, and support forums
- **Self-hosted** — you own and control your infrastructure

### Jenkins vs Alternatives

| Tool | Type | Market Share | Best For |
|------|------|-------------|----------|
| **Jenkins** | Open source, self-hosted | 60–70% | Full control, complex pipelines |
| **GitHub Actions** | Cloud, built into GitHub | Growing fast | GitHub-centric projects |
| **GitLab CI** | Cloud + self-hosted | ~10% | GitLab users |
| **CircleCI** | Cloud | ~5% | Fast SaaS setup |
| **Azure DevOps** | Cloud | Enterprise | Microsoft ecosystem |

### Jenkins Architecture

Jenkins has a **Master-Agent** (or Controller-Agent) architecture:

- **Jenkins Master (Controller):** The main server. Manages jobs, schedules builds, shows the UI, stores results
- **Jenkins Agent (Node):** Worker machines that actually run the build jobs. You can have many agents for parallel work

For small setups (like class), the master runs everything. For production, agents handle the workload.

### Jenkins Plugin System
Jenkins by itself is minimal. Plugins add nearly all functionality:

| Plugin | What it enables |
|--------|----------------|
| Git Plugin | Connect to GitHub/GitLab repos |
| Maven Plugin | Build Java projects with Maven |
| SonarQube Scanner | Run quality gate analysis |
| Docker Plugin | Build and push Docker images |
| Slack Notification | Send build status to Slack |
| Pipeline Plugin | Write pipelines as code (Jenkinsfile) |
| Email Extension | Send build failure emails |

---

## 5. Jenkins Setup – From Zero to Running

### Infrastructure Requirements (from class)

| Component | Requirement | Why |
|-----------|-------------|-----|
| **Cloud** | GCP (Google Cloud Platform) | Host the virtual machine |
| **OS** | Ubuntu 24.04 LTS | Stable Linux for Jenkins |
| **Storage** | 30 GB | Jenkins + build artifacts |
| **CPU** | 2 vCPUs | Parallel build processing |
| **RAM** | 4 GB | Jenkins + Java JVM overhead |
| **Java** | JDK 21 | Jenkins itself runs on Java |

> ⚠️ Jenkins runs on Java — Java must be installed before Jenkins. This is the most common setup mistake beginners make.

---

### Step-by-Step Installation

#### Step 1: Update System Packages
```bash
sudo apt update
# Always run this first on a fresh Ubuntu machine
# Downloads the latest package list from Ubuntu's servers
```

#### Step 2: Install Java JDK 21
```bash
sudo apt install openjdk-21-jdk -y
# Install Java Development Kit (not just JRE — we need the full JDK)
```

#### Step 3: Verify Java Installation
```bash
java -version
# Expected output: openjdk version "21.x.x"
# If this fails, Jenkins installation will also fail
```

#### Step 4: Add Jenkins Repository Key & Source
```bash
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
```

### Why is this step necessary?
Ubuntu's default software repositories do not include the Jenkins package. To install Jenkins, we must perform these two actions to prepare our system.

#### 1. The GPG Key (The "Digital Signature")
The first command (`sudo wget -O ...`) downloads and saves the Jenkins GPG key.
- **Why?** This is for **security**. It acts as a digital signature.
- **How it works:** When you run `apt install`, Ubuntu uses this key to verify that the Jenkins software hasn't been modified or tampered with by hackers. If the signature doesn't match, your system will block the installation.
- **Modern Standard:** We use `/etc/apt/keyrings/` to store the key, which is the current recommended practice for Debian-based systems like Ubuntu.

#### 2. The Repository Source (The "Download Address")
The second command (`echo "deb ..." | sudo tee ...`) adds Jenkins to your system's list of software sources.
- **Why?** It tells Ubuntu exactly **where to look** for Jenkins on the internet.
- **What happens:** It creates a file named `jenkins.list` inside the `/etc/apt/sources.list.d/` directory. This acts like adding a new "store" to your computer's shopping list, allowing `apt` to find and download the latest Jenkins package.

### 🔍 Deep Dive: What is a GPG Key?

**GPG (GNU Privacy Guard)** is a security tool used to verify the authenticity of files. In DevOps, it's the standard way to ensure the software you're installing is safe.

1. **The Analogy:** Think of a GPG key like a **wax seal** on a royal letter. If the seal is broken or looks different, you know the letter has been tampered with.
2. **The Signature:** The Jenkins developers "sign" their code with a secret private key. They then give you a **Public Key** (the file we downloaded).
3. **The Verification:** When you run `apt install jenkins`, your computer uses that Public Key to check the "seal" on the package.
   - **If it matches:** The installation proceeds (it's safe).
   - **If it doesn't match:** Ubuntu throws a massive error and stops the install (it could be a virus).

> 💡 **Why this matters:** Without GPG keys, a hacker could trick your computer into downloading a fake version of Jenkins that could steal your passwords or destroy your server.




#### Step 5: Install Jenkins
```bash
sudo apt update
sudo apt install jenkins -y
```

#### Step 6: Start Jenkins Service
```bash
sudo systemctl start jenkins
sudo systemctl enable jenkins   # Start automatically on reboot
sudo systemctl status jenkins   # Verify it's running
```

#### Step 7: Open Firewall Port 8080 (on GCP)
- In GCP Console → VPC Network → Firewall → Add rule → Allow TCP 8080
- Jenkins runs on **port 8080 by default**

#### Step 8: Access Jenkins UI
```
http://YOUR_VM_IP:8080
```

#### Step 9: Unlock Jenkins
```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
# Copy this password and paste it in the browser to unlock Jenkins
```

#### Step 10: Complete Setup Wizard
1. Install suggested plugins
2. Create first admin user
3. Set Jenkins URL
4. Jenkins is ready! 🎉

---

## 6. Your First Jenkins Job

### What is a Jenkins Job?
A **Job** (also called a **Project**) is a configured task in Jenkins. It defines:
- Where to get the code (GitHub URL)
- What to do with it (compile, test, run)
- When to run it (manual, on push, on schedule)

### Job Types

| Job Type | Use Case |
|----------|----------|
| **Freestyle Project** | Simple, UI-configured jobs — beginner-friendly ✅ |
| **Pipeline** | Complex multi-stage pipelines defined as code (Jenkinsfile) |
| **Multibranch Pipeline** | Automatically creates pipelines for each branch in a repo |
| **Folder** | Organizes multiple jobs into groups |

In class, we used the **Freestyle Project** type.

---

### Creating the Hello World Jenkins Job – Step by Step

#### Step 1: New Item
- Click **"New Item"** on Jenkins dashboard
- Enter job name: `hello-world-java`
- Select **"Freestyle project"**
- Click OK

#### Step 2: Configure Source Code Management
- Scroll to **"Source Code Management"**
- Select **Git**
- Enter your GitHub repository URL
- If private: add credentials (GitHub username + token)

#### Step 3: Configure Build Steps
- Scroll to **"Build Steps"**
- Click **"Add build step"** → **"Execute shell"**
- Enter commands:
```bash
javac HelloWorld.java
java HelloWorld
```

#### Step 4: Save and Run
- Click **Save**
- Click **"Build Now"**
- Watch the build queue → running → ✅ success (or ❌ failure)

#### Step 5: Check Console Output
- Click on the build number (e.g., `#1`)
- Click **"Console Output"**
- You should see:
```
Cloning repository https://github.com/yourname/hello-java.git
[hello-world-java] $ /bin/sh -xe /tmp/jenkins...
+ javac HelloWorld.java
+ java HelloWorld
Hello, World!
Finished: SUCCESS
```

---

### What Just Happened? (The Full Flow)

```
You clicked "Build Now"
        │
        ▼
Jenkins fetched code from GitHub
        │
        ▼
Jenkins compiled HelloWorld.java (javac)
        │
        ▼
Jenkins ran the compiled program (java HelloWorld)
        │
        ▼
Output "Hello, World!" appeared in Console
        │
        ▼
Build marked SUCCESS ✅
```

This simple job demonstrates the **entire principle** of CI — code from GitHub, automatically processed, with visible output — all without you touching a terminal.

---

## 7. Key Commands Reference

### System Commands

```bash
# Update package lists (always run first on fresh Ubuntu)
sudo apt update

# Install Java JDK 21
sudo apt install openjdk-21-jdk -y

# Check Java version
java -version

# Start Jenkins service
sudo systemctl start jenkins

# Enable Jenkins to start on reboot
sudo systemctl enable jenkins

# Check Jenkins service status
sudo systemctl status jenkins

# Restart Jenkins (after config changes)
sudo systemctl restart jenkins

# Get initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### Important Ports & Paths

| Item | Value |
|------|-------|
| Jenkins default port | `8080` |
| Jenkins home directory | `/var/lib/jenkins/` |
| Jenkins log file | `/var/log/jenkins/jenkins.log` |
| Initial admin password | `/var/lib/jenkins/secrets/initialAdminPassword` |
| Jenkins config file | `/etc/default/jenkins` |
| Jenkins workspace | `/var/lib/jenkins/workspace/` |

---

## 8. Visual Diagrams

### Diagram 1: The Full CI Pipeline

```
Developer pushes code to GitHub
              │
              ▼
    ┌─────────────────┐
    │   JENKINS       │  ← Detects the push (webhook or poll)
    │   Triggered     │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  1. COMPILE     │  ← javac / maven compile
    │  Syntax check   │  ❌ Fails? → Notify developer
    └────────┬────────┘
             │ ✅
             ▼
    ┌─────────────────┐
    │  2. BUILD       │  ← mvn build / gradle build
    │  Link & assemble│  ❌ Fails? → Notify developer
    └────────┬────────┘
             │ ✅
             ▼
    ┌─────────────────┐
    │  3. UNIT TESTS  │  ← JUnit / pytest / Jest
    │  Logic verified │  ❌ Fails? → Notify developer
    └────────┬────────┘
             │ ✅
             ▼
    ┌─────────────────┐
    │  4. SONARQUBE   │  ← Code quality & security scan
    │  Quality Gate   │  ❌ Below threshold? → Block pipeline
    └────────┬────────┘
             │ ✅
             ▼
    ┌─────────────────┐
    │  5. ARTIFACT    │  ← .jar / .war / Docker image
    │  Build output   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  6. PACKAGE     │  ← Store in Nexus / Artifactory
    │  Version stored │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  7. DEPLOY      │  ← To Dev / QA / Staging / Prod
    │  Live!          │
    └─────────────────┘
```

---

### Diagram 2: Jenkins Architecture

```
┌──────────────────────────────────────────────────────┐
│                  JENKINS MASTER                      │
│                                                      │
│  ┌───────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │   Web UI  │  │ Job Queue│  │  Plugin Manager  │  │
│  │ (port 8080│  │Scheduler │  │  2000+ plugins   │  │
│  └───────────┘  └──────────┘  └──────────────────┘  │
│                                                      │
│        Distributes work to agents ▼                  │
└──────────────────────┬───────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
  ┌────────────┐ ┌────────────┐ ┌────────────┐
  │  Agent 1   │ │  Agent 2   │ │  Agent 3   │
  │ (Java builds│ │(Docker builds│ │(Test runner│
  └────────────┘ └────────────┘ └────────────┘
```

---

### Diagram 3: Jenkins Job Flow (Hello World)

```
[GitHub Repo]
 HelloWorld.java
      │
      │ Jenkins fetches via Git plugin
      ▼
[Jenkins Workspace]
 /var/lib/jenkins/workspace/hello-world-java/
      │
      │ Execute Shell: javac HelloWorld.java
      ▼
[Compilation]
 HelloWorld.class generated
      │
      │ Execute Shell: java HelloWorld
      ▼
[Execution]
 Console Output: "Hello, World!"
      │
      ▼
[Build Result: SUCCESS ✅]
```

---

### Diagram 4: Where Jenkins Fits in the DevOps Toolchain

```
  CODE          SOURCE         CI/CD         ARTIFACT       DEPLOY
  ─────         ──────         ─────         ────────       ──────
  VS Code  →  GitHub/GitLab  →  Jenkins  →  Nexus/ECR  →  Kubernetes
                                  │
                          ┌───────┴────────┐
                          │  Integrates    │
                          │  with:         │
                          │  • SonarQube   │
                          │  • Maven/Gradle│
                          │  • Docker      │
                          │  • Slack       │
                          │  • AWS/GCP     │
                          └────────────────┘
```

---

### Diagram 5: VM Setup Requirements

```
GCP Virtual Machine
┌──────────────────────────────────┐
│  OS: Ubuntu 24.04 LTS            │
│  CPU: 2 vCPUs                    │
│  RAM: 4 GB                       │
│  Disk: 30 GB                     │
│                                  │
│  ┌────────────────────────────┐  │
│  │  Java JDK 21               │  │ ← Jenkins runs ON Java
│  │  ┌──────────────────────┐  │  │
│  │  │  Jenkins 2.55.1      │  │  │
│  │  │  Port: 8080          │  │  │
│  │  └──────────────────────┘  │  │
│  └────────────────────────────┘  │
│                                  │
│  Firewall: Allow TCP 8080        │
└──────────────────────────────────┘
         Accessible via:
    http://VM_EXTERNAL_IP:8080
```

---

## 9. Scenario-Based Q&A

---

🔍 **Scenario 1:** A developer pushes broken code at 5 PM on a Friday. The team only finds out Monday morning when someone tries to run the app.

✅ **Answer:** This wouldn't happen with CI. The moment the developer pushed, Jenkins would have triggered automatically, attempted to compile and run the tests, failed within minutes, and sent an immediate notification (email, Slack) back to the developer. The broken code is caught in minutes — not over a weekend.

---

🔍 **Scenario 2:** Your team has 10 developers, and every time two people push code close together, things break. The manual testing team is overwhelmed.

✅ **Answer:** This is exactly the "integration hell" problem CI solves. Each push to GitHub triggers a Jenkins pipeline that automatically compiles, runs unit tests, and checks quality. Each developer gets instant feedback on their own changes. The QA team is freed from regression testing basics and can focus on complex scenarios.

---

🔍 **Scenario 3:** Your manager asks "why does Jenkins need Java installed before it can be installed itself?"

✅ **Answer:** Jenkins is a Java application — its server (`jenkins.war`) runs inside a Java Virtual Machine (JVM). Without Java, Jenkins has no runtime environment to execute in. This is why the installation order is strict: OS → Java → Jenkins. If you try to install Jenkins without Java, it will either fail immediately or produce cryptic errors.

---

🔍 **Scenario 4:** A new team member asks: "Can I just use GitHub Actions instead of Jenkins? Why do we use Jenkins?"

✅ **Answer:** GitHub Actions is a great modern alternative, especially for teams fully on GitHub. Jenkins is preferred when: you need self-hosted infrastructure (data security, compliance), you have very complex multi-tool pipelines, you need the flexibility of 2,000+ plugins, or your organization already has a Jenkins setup. GitHub Actions is simpler to start with; Jenkins offers more control at scale. Both are valid — the choice depends on your team's needs.

---

🔍 **Scenario 5:** Jenkins shows "BUILD FAILURE" but you're not sure why. Where do you look?

✅ **Answer:** Click on the failed build number in Jenkins → click **"Console Output"**. This shows the full log of everything Jenkins did, line by line, including the exact error message. Common issues: compilation errors in the code, a test assertion that failed, wrong file path in the build command, or a missing dependency.

---

🔍 **Scenario 6:** Your Jenkins server is on port 8080 but you can't access it from your browser, even though Jenkins is running.

✅ **Answer:** This is a firewall issue on GCP. By default, GCP blocks all ports except 22 (SSH). You need to go to GCP Console → VPC Network → Firewall Rules → Create Rule → Allow TCP port 8080 → Apply to your VM instance. After that, `http://YOUR_IP:8080` will work.

---

🔍 **Scenario 7:** Your team's main branch keeps receiving "it works on my machine" complaints. Code passes locally but fails in the shared environment.

✅ **Answer:** This classic problem is solved by CI. Jenkins runs builds in a **clean, controlled, identical environment** every time — not a developer's customized laptop. If code passes locally but fails in Jenkins, it means the developer has something installed locally that isn't available in the standard environment. Jenkins acts as the "ground truth" build environment.

---

## 10. Interview Q&A

---

**Q1. What is CI/CD and why is it important in DevOps?**

**A:** CI/CD stands for Continuous Integration and Continuous Delivery/Deployment. CI is the automated process of building, testing, and validating code every time a developer pushes a change. CD is the automated process of delivering that validated code to a deployment environment.

It's important because it: catches bugs early (minutes, not weeks), eliminates manual build and test effort, enables teams to release frequently with confidence, reduces risk through small incremental changes, and creates a consistent and reproducible build process. In DevOps, CI/CD is the bridge between development and operations.

---

**Q2. What are the stages in a typical CI pipeline?**

**A:** A typical CI pipeline includes:
1. **Code Push** – Triggers the pipeline via GitHub webhook
2. **Compilation** – Checks that the code compiles without errors
3. **Build** – Assembles the code into a runnable package
4. **Unit Testing** – Runs automated tests to verify logic
5. **Quality Gates** – Tools like SonarQube check code quality and security
6. **Artifact Generation** – Creates the deployable output (`.jar`, Docker image, etc.)
7. **Packaging** – Stores the artifact in a repository (Nexus, Artifactory)
8. **Deployment** – Deploys to Dev, QA, Staging, or Production

Each stage acts as a quality gate — if any stage fails, the pipeline stops and the developer is notified.

---

**Q3. What is Jenkins and why does it have 60–70% market share in CI/CD?**

**A:** Jenkins is an open-source automation server written in Java. It monitors source code repositories and automatically triggers build, test, and deploy pipelines when changes are pushed.

Its dominance comes from: being free and open-source, having 2,000+ community plugins to integrate with virtually any tool, being battle-tested for 15+ years, offering a self-hosted model for security-sensitive organizations, having a massive community for support, and being highly customizable for any pipeline complexity.

---

**Q4. Why does Jenkins require Java to be installed first?**

**A:** Jenkins is itself a Java application — it runs as a `.war` (Web Application Archive) file on a Java Virtual Machine (JVM). The JVM is the runtime that executes Jenkins. Without Java installed, there is no environment for Jenkins to run in. This is why the installation sequence is strictly: Install OS → Install Java JDK → Install Jenkins.

---

**Q5. What is a Jenkins Freestyle Project vs a Pipeline?**

**A:**
- A **Freestyle Project** is configured through Jenkins' web UI — you fill in forms to specify the source repo, build steps, and post-build actions. It's beginner-friendly but limited for complex workflows.
- A **Pipeline** is defined as code in a file called `Jenkinsfile`, stored in the repository itself. It supports complex multi-stage workflows, conditional logic, parallel execution, and follows Infrastructure-as-Code principles.

In production, Pipelines (especially Declarative Pipelines) are preferred because the pipeline definition lives with the code, is version-controlled, and is far more powerful.

---

**Q6. What is SonarQube and what role does it play in CI?**

**A:** SonarQube is a code quality and security analysis tool. In a CI pipeline, it runs after unit tests and scans the codebase for: code duplication, overly complex functions, security vulnerabilities, code style violations, and maintainability issues. It assigns a quality rating and applies a "Quality Gate" — if the code doesn't meet a minimum standard, the pipeline fails and the code cannot proceed to deployment. It acts as an automated code reviewer, enforcing standards consistently on every single push.

---

**Q7. What is an artifact in the context of CI/CD?**

**A:** An artifact is the deployable output produced by a CI build. For a Java application, it's typically a `.jar` or `.war` file. For a containerized application, it's a Docker image. The artifact is the compiled, packaged version of the application that gets deployed to servers — not the raw source code. Artifacts are stored in artifact repositories like Nexus or JFrog Artifactory for versioning, so any previous version can be retrieved and redeployed.

---

**Q8. What is the default port Jenkins runs on, and what do you do if it's blocked?**

**A:** Jenkins runs on **port 8080** by default. If it's blocked (common on cloud VMs like GCP or AWS), you need to add a firewall rule to allow inbound TCP traffic on port 8080 for your server's IP. On GCP this is done through VPC Network → Firewall Rules. On AWS, it's done through Security Groups. Without this, Jenkins is running but unreachable from a browser — one of the most common beginner issues.

---

**Q9. What is the difference between Continuous Delivery and Continuous Deployment?**

**A:** Both are the "CD" part of CI/CD, but they differ in the final step:
- **Continuous Delivery** means the pipeline automatically produces a release-ready artifact and deploys it to a staging environment. The final push to **production requires a manual approval**.
- **Continuous Deployment** is fully automated — every change that passes all tests is automatically deployed all the way to **production** with no human intervention.

Continuous Delivery suits teams that need a human sign-off before production (regulated industries, large releases). Continuous Deployment suits teams with high test confidence and fast release cycles (SaaS products, startups).

---
Prev : [25_Git_&_GitHub_Deep_Dive_Branching_PRs_&_Collaboration.md](25_Git_&_GitHub_Deep_Dive_Branching_PRs_&_Collaboration.md) | Next : [27_Jenkins_Deep_Dive_Users_RBAC_CI_Pipelines_&_Local_Setup.md](27_Jenkins_Deep_Dive_Users_RBAC_CI_Pipelines_&_Local_Setup.md)
---
