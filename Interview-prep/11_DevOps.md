# 🚀 Interview Preparation - DevOps

> **Domain:** Software Delivery / Systems Engineering / SRE  
> **Level:** Beginner to Expert  
> **Target Role:** Software Engineer / Senior Engineer / DevOps Engineer / SRE

---

## 🟢 Beginner Level

### ❓ Q1. **What is DevOps and what is CI/CD?**

<details>
<summary><b>👀 Show Answer</b></summary>

* **DevOps:** A cultural and engineering philosophy that bridges the gap between software development (Dev) and IT operations (Ops). The goal is to shorten the software development lifecycle, increase deployment frequency, and build more dependable releases.
* **CI/CD (Continuous Integration / Continuous Delivery):**
  - **Continuous Integration (CI):** The practice of automating the integration of code changes from multiple developers into a single shared repository. Every code commit triggers automated builds and tests to identify integration bugs early.
  - **Continuous Delivery (CD):** The practice of automatically packaging and prepping code changes for a release to production. Actual deployment may require manual approval.
  - **Continuous Deployment (CD):** Fully automated pipeline where every change that passes tests is deployed to production automatically.
- **Real-Time Experience Focus (CI/CD Automation):**
  - Designed and built end-to-end CI/CD pipelines using **Jenkins, Docker, and AWS**, which **reduced deployment time by 60%** and improved release reliability across environments.
  - Automating the build, test, and container packaging workflow ensures that developers get immediate feedback on commits, preventing integration issues before they reach production.

> 💡 **Interviewer Focus:** Ensure the candidate highlights DevOps as a cultural mindset, not just a set of tools (like Docker or Jenkins), explains the feedback loop, and demonstrates experience building stable pipelines.

</details>

<hr/>

### ❓ Q2. **What is version control and what are the standard Git workflows?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Version Control (Git):** A tool to track modifications to source code over time, enabling collaboration among developers without overwriting each other's work.
- **Git Workflows:**
  - **GitFlow:** A branching model with strict long-lived branches: `master` (production), `develop` (pre-production), `feature/` (new features), `release/` (preparation for prod), and `hotfix/` (quick patches).
  - **Trunk-Based Development:** Developers merge small, frequent commits into a single branch (the "trunk", usually `main`) multiple times a day. It avoids long-lived branches and merge hell.

> 💡 **Interviewer Focus:** Trade-off analysis. GitFlow is good for scheduled release cycles; Trunk-Based is preferred for modern high-frequency CI/CD.

</details>

<hr/>

### ❓ Q3. **What is Docker and what is a container?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Docker:** An open-source platform used to build, ship, and run applications inside lightweight, portable containers.
- **Container:** A standardized unit of software that packages up code and all its dependencies (runtime, system libraries, configuration files) so the application runs quickly and reliably from one computing environment to another.
- Containers share the host operating system's kernel, making them lightweight and fast to start.

> 💡 **Interviewer Focus:** Portability ("works on my machine" resolution) and runtime predictability.

</details>

<hr/>

### ❓ Q4. **What is the difference between a Container and a Virtual Machine (VM)?**

<details>
<summary><b>👀 Show Answer</b></summary>

| Feature | Container | Virtual Machine (VM) |
| :--- | :--- | :--- |
| **Architecture** | Shares the host OS kernel. | Has its own full Guest OS. |
| **Hypervisor** | Not required (uses container runtime like Docker). | Requires a Hypervisor (ESXi, VirtualBox). |
| **Startup Time** | Milliseconds. | Minutes. |
| **Resource Usage** | Extremely low (shares RAM/CPU dynamically). | High (pre-allocates RAM and disk space). |
| **Size** | Megabytes. | Gigabytes. |
| **Isolation** | Process-level isolation (less secure). | Hardware-level isolation (more secure). |

> 💡 **Interviewer Focus:** Highlighting the resource utilization and virtualization overhead of VMs vs the OS kernel sharing of containers.

</details>

<hr/>

### ❓ Q5. **What is Infrastructure as Code (IaC)?**

<details>
<summary><b>👀 Show Answer</b></summary>

**Infrastructure as Code (IaC)** is the practice of provisioning, managing, and configuring cloud infrastructure (networks, virtual machines, database instances, load balancers, security policies) using machine-readable configuration files (like Terraform HCL, CloudFormation YAML, or JSON) instead of manual interactive tools (clicking inside the AWS Console).

To understand IaC, compare the manual way to the code way:
*   **The Manual Way (Click-Ops):**
    *   To set up a production MERN app, a developer logs into the AWS console, creates a VPC, configures subnets, launches an EC2 instance, links it to an RDS database, and opens ports on a Security Group.
    *   **The Problem:** If you need to replicate this exact environment for Staging or Development, you must repeat all those clicks from memory. It is highly error-prone, impossible to track changes, and leads to **configuration drift** (where Staging and Prod settings mismatch).
*   **The IaC Way:**
    *   You write a configuration file detailing your desired AWS resources (e.g. VPC, subnets, EC2, RDS).
    *   **Terraform HCL Snippet Example:**
        ```hcl
        # 1. Define the Cloud Provider
        provider "aws" {
          region = "us-east-1"
        }

        # 2. Declare a custom VPC resource
        resource "aws_vpc" "mern_vpc" {
          cidr_block           = "10.0.0.0/16"
          enable_dns_hostnames = true
          tags = { Name = "MERN-Production-VPC" }
        }

        # 3. Declare a Public Subnet inside that VPC
        resource "aws_subnet" "public_subnet" {
          vpc_id                  = aws_vpc.mern_vpc.id
          cidr_block              = "10.0.1.0/24"
          availability_zone       = "us-east-1a"
          map_public_ip_on_launch = true
          tags = { Name = "MERN-Public-Subnet" }
        }
        ```
    *   You run a command (e.g., `terraform apply`), and the tool automatically calls the AWS APIs to provision the resources exactly as defined in the configuration files.

#### Core Benefits of IaC:
1.  **Repeatability & Speed:** Spinning up an entire multi-tier environment takes seconds by running a script, rather than hours of clicking.
2.  **Version Controlled (GitOps):** Your infrastructure files live in Git. Every change is tracked, auditable, and requires a Pull Request review (just like application code).
3.  **Self-Documentation:** The codebase acts as the documentation for the infrastructure. Anyone can look at the Git repository and see exactly how the network is laid out.
4.  **No Configuration Drift:** IaC tools compare the active cloud state with your configuration files. If someone manually changes a port in the AWS Console, the next IaC run will detect it and change it back to match the code.

#### Key Approaches:
*   **Declarative (The "What" - e.g. Terraform, CloudFormation):** You define the desired end-state ("I want a VPC with 2 public subnets"). The tool determines the creation order and executes the API requests. (Highly preferred for infrastructure).
*   **Imperative (The "How" - e.g. AWS CLI script, bash):** You specify the list of commands/steps to execute sequentially ("Step 1: Run `aws ec2 create-vpc`", "Step 2: Get ID and run subnet script").

> 💡 **Interviewer Focus:** Understanding configuration drift, the benefits of tracking cloud structures in Git, and the trade-offs between declarative (Terraform) vs imperative (scripts) approaches.

</details>

<hr/>

### ❓ Q6. **What is the purpose of environment variables in software deployment?**

<details>
<summary><b>👀 Show Answer</b></summary>

Environment variables allow separating application configuration code from the codebase (following the **Twelve-Factor App** principles).
- Instead of hardcoding database credentials, URLs, or API keys inside the code, you inject them at runtime based on the target environment (Dev, Staging, Production).
- This keeps credentials secure (not committed to public Git repos) and allows the same container build to be deployed across different environments without code alterations.

> 💡 **Interviewer Focus:** Security best practices (never commit secrets to source control) and configuration separation.

</details>

<hr/>

### ❓ Q7. **What is a Dockerfile? Explain its basic directives.**

<details>
<summary><b>👀 Show Answer</b></summary>

A Dockerfile is a text document containing instructions to build a Docker Image.
- **`FROM`**: Sets the base image (e.g., `FROM node:20-alpine`).
- **`WORKDIR`**: Defines the working directory inside the container.
- **`COPY`**: Copies files from the host machine to the container.
- **`RUN`**: Executes commands during the image build process (e.g., `RUN npm ci`).
- **`EXPOSE`**: Documents the port the container listens on at runtime.
- **`CMD`**: Specifies the default command to execute when the container starts.
- **Real-World Node.js / Express Example:**
  ```dockerfile
  # Use a lightweight Node runtime base image
  FROM node:20-alpine AS runner
  WORKDIR /usr/src/app
  # Copy package files first to leverage Docker layer caching
  COPY package*.json ./
  # Install production dependencies only, bypassing devDependencies
  RUN npm ci --only=production
  # Copy application source files
  COPY . .
  EXPOSE 5000
  # Ensure the app doesn't run as root for security (least privilege)
  USER node
  CMD ["node", "server.js"]
  ```

> 💡 **Interviewer Focus:** Distinguishing `RUN` (build time) from `CMD` (runtime), using lightweight base images (alpine/distroless), and implementing container security best practices like running processes as a non-root user.

</details>

<hr/>

### ❓ Q8. **What is monitoring vs logging in system reliability?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Monitoring (Metrics):**
  - High-level numeric data tracked over time (e.g., CPU utilization, RAM usage, request latency, error rates).
  - Used to identify *when* a system is failing or experiencing performance degradation (triggers alerts).
- **Logging (Logs):**
  - Detailed text outputs generated by application events (e.g., stack traces, print statements, transaction records).
  - Used to debug *why* a specific failure or exception occurred.
- **Real-Time Experience Focus (Centralized Observability):**
  - In our Node.js/Express backends, we implemented centralized application logging using **Winston** and **Morgan**.
  - **Morgan** captures standard HTTP traffic logs (method, status, response time), while **Winston** manages application errors and custom logging levels (debug, info, error), outputting logs in structured JSON format. This enables easy parsing, indexing, and debugging via centralized logging agents (like AWS CloudWatch Logs or ELK stack).

> 💡 **Interviewer Focus:** Point out that monitoring tells you *that* a system is broken, logging helps you figure out *why* it broke, and the importance of structured logging (JSON) for production observability.

</details>

<hr/>

### ❓ Q9. **What is Kubernetes (K8s) in short?**

<details>
<summary><b>👀 Show Answer</b></summary>

Kubernetes is an open-source container orchestration engine for automating deployment, scaling, and management of containerized applications.
- If your app runs across 100 containers, Kubernetes manages scheduling them to physical servers, scaling them up/down based on traffic, load-balancing traffic among them, and replacing containers automatically if they crash.

> 💡 **Interviewer Focus:** Knowing that Kubernetes manages container scheduling, scaling, and self-healing.

</details>

<hr/>

### ❓ Q10. **What is the difference between Git merge and Git rebase?**

<details>
<summary><b>👀 Show Answer</b></summary>

Both commands are used to integrate changes from one branch (e.g. `feature`) into another (e.g. `main`), but they do it in completely different ways:

#### 1. Differences Summary
*   **Git Merge:** Combines the histories of two branches by creating a new "Merge Commit" that has multiple parent commits. It preserves the exact historical timeline of when changes were made and how branches diverged and merged.
*   **Git Rebase:** Re-applies your branch's commits one by one on top of the latest commit of the target branch. This rewrites the commit history by assigning new parent commits to your work, resulting in a single linear commit history.

---

#### 2. Visual Branch History

##### **Starting State:**
```text
      A---B (main)
       \
        C---D (feature-branch)
```
*(You branched off `A`. Commit `B` was pushed to `main` while you worked on `C` and `D`.)*

##### **Option A: `git merge main`**
```text
      A-------B (main)
       \       \
        C---D---M (feature-branch)  <-- New Merge Commit (M)
```
*   **How it works:** Git creates a new commit `M` (Merge commit) that has two parents: `B` and `D`.
*   **Pros:** Non-destructive. It does not alter your history; it simply adds a new commit.
*   **Cons:** Can make your Git history graph look like a messy spiderweb of merge loops at scale.

##### **Option B: `git rebase main`**
```text
      A---B (main)
           \
            C'---D' (feature-branch)  <-- Commits C & D are rewritten
```
*   **How it works:** Git temporarily stashes your commits `C` and `D`, moves your starting point on `feature-branch` from `A` to the latest commit `B`, and then applies your commits on top. Since the parent commits changed, `C` and `D` are rewritten into brand new commits (`C'` and `D'`).
*   **Pros:** Keeps history perfectly linear, clean, and easy to read.
*   **Cons:** Rewrites history (creates new commit hashes).
*   **Golden Rule of Rebase:** **Never rebase public/shared branches.** If you rewrite commits that other developers have already pulled and are working on, it will break their local history and cause severe merge conflicts.

> 💡 **Interviewer Focus:** Safety constraints of rebasing (not rebasing shared main/prod branches), and trade-offs in clean history (Rebase) vs accurate history (Merge).

</details>

<hr/>

### ❓ Q11. **Explain the role of the Jenkins server in CI/CD.**

<details>
<summary><b>👀 Show Answer</b></summary>

**Jenkins** is a self-hosted automation server that orchestrates and executes your CI/CD pipelines. It automates the entire lifecycle of software delivery once code changes are committed to version control.

#### 1. Core Execution Pipeline Flow
When a developer pushes code to a Git repository, a Git webhook triggers Jenkins to run a pipeline containing the following automated stages:
*   **Checkout:** Pulls the latest code version from Git.
*   **Test:** Executes automated unit, integration, and security tests. If any step fails, Jenkins halts execution immediately and logs a build failure.
*   **Package/Build:** Compiles application binaries and builds container packages (such as Docker images).
*   **Deliver/Push:** Authenticates and pushes the build artifacts to a centralized storage (like an S3 bucket or Amazon ECR registry).
*   **Deploy:** Automates updates to host servers, updating ECS services, or applying Kubernetes manifests to roll out new container versions.

##### **Example: Jenkinsfile Orchestrated by Jenkins**
```groovy
// Jenkinsfile - Defines the automated pipeline stages executed by the Jenkins Server
pipeline {
    agent any // Tells Jenkins to run this on any available build node
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/user/express-api.git'
            }
        }
        stage('Test') {
            steps {
                sh 'npm install && npm test'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t express-api:latest .'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker stop api-service || true && docker run -d --name api-service -p 5000:5000 express-api:latest'
            }
        }
    }
}
```

---

#### 2. Why Jenkins Automation is Critical
Without an automation server like Jenkins, deployments must be executed manually:
1.  **Manual Testing:** Running tests locally, which risks code slipping to production if a local test suite is bypassed.
2.  **Manual Packaging:** Compiling binaries or Docker images on local developer machines, leading to inconsistent environments ("it works on my machine").
3.  **Manual Delivery:** Manually logging into production nodes via SSH to run containers or pull files, exposing direct credentials to developers.

**The Solution:** Jenkins isolates deployment secrets, runs every task in a standardized clean container or build executor, and guarantees that every single merge goes through identical, audited checks before release.

> 💡 **Interviewer Focus:** Master-Agent execution architecture (master coordinates; agents execute heavy compiler jobs), automating feedback loops on Git commits, and replacing manual deployment steps with code-driven pipelines.

</details>

<hr/>

### ❓ Q12. **What is a container registry?**

<details>
<summary><b>👀 Show Answer</b></summary>

A container registry is a storage system for hosting and sharing container images.
- Common registries: Docker Hub, Amazon ECR, Google Artifact Registry.
- Pipelines push compiled images to the registry, and deployments pull images from the registry to run on servers.

> 💡 **Interviewer Focus:** Registry security configurations (credentials, token rotation, image scanning).

</details>

<hr/>

### ❓ Q13. **What is the difference between stateless and stateful applications?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Stateless:** The application does not store client transaction history or persistent states locally. Any instance can process any incoming request. Extremely easy to scale out (add replicas) and replace.
- **Stateful:** The application depends on persistent local storage or sessions (like a SQL database). Scaling requires clustering and managing data replication, volume mappings, and failovers.

> 💡 **Interviewer Focus:** Separating state storage (databases) from compute layers (stateless backend containers).

</details>

<hr/>

### ❓ Q14. **What does the command `git checkout -b <branch>` do?**

<details>
<summary><b>👀 Show Answer</b></summary>

It is a shorthand command that:
1. Creates a new branch named `<branch>` from the current active commit.
2. Switches (checks out) your workspace to that newly created branch.

#### What happens if the branch already exists?
If you run `git checkout -b <branch>` and the branch name already exists, Git will fail and output the following error:
```bash
fatal: A branch named '<branch>' already exists.
```

#### How to handle this scenario:
*   **To just switch to the existing branch:**
    ```bash
    git checkout <branch>
    # OR (modern Git command):
    git switch <branch>
    ```
*   **To force recreate or reset the existing branch** (overwriting its previous history and resetting it to point to your current commit):
    ```bash
    git checkout -B <branch>
    # OR (modern Git command):
    git switch -C <branch>
    ```
    *(Note the capital `-B` or `-C` flag, which forces the creation/reset of the branch).*

> 💡 **Interviewer Focus:** Basic Git CLI mechanics, handling branch conflicts, and awareness of modern Git commands (`git switch`).

</details>

<hr/>

### ❓ Q15. **What is SSH and why is it used?**

<details>
<summary><b>👀 Show Answer</b></summary>

**SSH (Secure Shell)** is a cryptographic network protocol (running on TCP port 22 by default) used to establish an encrypted connection between a client and a remote server. It is primarily used for secure remote command-line login, remote command execution, and secure file transfers (via SFTP and SCP) over insecure networks.

#### 1. How SSH Key-Based Authentication Works
Instead of insecure username/password pairs, SSH uses asymmetric cryptography (public/private key pairs):
1.  **Key Generation:** The user generates a key pair on their local machine (typically using RSA or Ed25519 algorithms).
2.  **Public Key Placement:** The public key (`id_ed25519.pub`) is copied and appended to the remote server's `~/.ssh/authorized_keys` file.
3.  **Private Key Secret:** The private key (`id_ed25519`) remains strictly on the client machine and must have restricted read permissions (`chmod 600 id_ed25519`).
4.  **Challenge-Response Exchange:** When connecting, the server encrypts a random challenge message using the user's public key. The client decrypts it using their private key and sends a hash of the response back to the server, verifying their identity without ever transmitting the private key over the network.

#### 2. Basic SSH Command Snippets
*   **Generate an Ed25519 SSH Key Pair:**
    ```bash
    ssh-keygen -t ed25519 -C "dev-pc"
    ```
*   **Copy Public Key to Remote Server:**
    ```bash
    ssh-copy-id -i ~/.ssh/id_ed25519.pub ubuntu@10.0.1.5
    ```
*   **Connect to Remote Server Using Private Key:**
    ```bash
    ssh -i ~/.ssh/id_ed25519 ubuntu@10.0.1.5
    ```

#### 3. Security Hardening Best Practices (`/etc/ssh/sshd_config`)
To protect remote servers from brute-force attacks, system administrators configure:
*   `PasswordAuthentication no` - Disables password logins entirely, forcing SSH key authentication.
*   `PermitRootLogin no` - Disables direct root user logins; users must log in as a standard user and escalate privileges via `sudo`.
*   `Port 2222` - Changes default SSH port 22 to a non-standard port to avoid automated script scans.

> 💡 **Interviewer Focus:** Understanding asymmetric cryptography in key authentication, secure key permissions (`chmod 600`), and basic SSH daemon configuration hardening options.

</details>

<hr/>

### ❓ Q16. **What is Nginx and how is it used in Node.js architectures?**

<details>
<summary><b>👀 Show Answer</b></summary>

Nginx is a high-performance web server, reverse proxy, load balancer, and HTTP cache. It utilizes an asynchronous event-driven architecture, enabling it to process thousands of concurrent connections with minimal memory usage.
- **Role in Node.js Deployments:**
  - Node.js is single-threaded and shouldn't handle CPU-intensive tasks like SSL handshake decryption or raw static file serving directly in production.
  - Nginx is placed in front of the Node.js API servers as a **Reverse Proxy** to manage SSL termination, request rate-limiting, Gzip compression, and header management, forwarding validated requests to Node.js.

> 💡 **Interviewer Focus:** Web infrastructure layouts and utilizing Nginx to offload security and asset delivery overhead from the Node application runtime.

</details>

<hr/>

### ❓ Q17. **What is configuration drift?**

<details>
<summary><b>👀 Show Answer</b></summary>

Configuration drift occurs when manual updates, modifications, or hotfixes are applied directly to running servers or cloud environments without updating the corresponding IaC templates. Over time, this makes environments inconsistent and leads to unexpected deployment failures.

> 💡 **Interviewer Focus:** Enforcing automated deployments to eliminate manual server logins.

</details>

<hr/>

### ❓ Q18. **What does the command `docker build -t app .` do?**

<details>
<summary><b>👀 Show Answer</b></summary>

This command compiles a set of instructions written in a `Dockerfile` into a runnable **Docker Image**. 

Here is the exact technical breakdown of each part of the command:
1.  **`docker build`**: Calls the Docker CLI tool to build an image.
2.  **`-t app`**: The tag flag. It names (tags) the resulting image `app`. 
    *   You can also specify a version suffix like `app:v1.0` or `app:latest`. If no version tag is provided, Docker defaults to `latest` (i.e. `app:latest`).
3.  **`.` (The Dot)**: Specifies the **Build Context**.
    *   The build context is the directory containing all the local files that the Docker builder is allowed to access and copy (via `COPY` or `ADD` directives) during the build.
    *   The dot `.` tells Docker that the build context is the **current working directory**, and it will search for a file named `Dockerfile` in this folder by default.

---

#### Under the Hood: What happens when you run it?
1.  **Sending the Context:** The Docker client packages all files in the current folder (excluding patterns defined in `.dockerignore`) and sends them to the **Docker Daemon** (which performs the actual build).
2.  **Step-by-Step Layer Execution:** The Daemon parses the `Dockerfile` line-by-line. For each instruction (like `RUN npm install` or `COPY . .`), Docker spins up a temporary container, runs the instruction, commits the results as a read-only filesystem layer, and caches it.
3.  **Completion:** Once all layers are successfully built, the Daemon tags the final layer as `app:latest` and deletes the temporary containers.

#### The Crucial Role of `.dockerignore`:
Because the `.` context sends all files in the folder to the Daemon, you must write a `.dockerignore` file. This prevents copying bulky or sensitive folders (like `node_modules`, `.git`, or `.env` files) into the daemon context, which keeps image sizes small and prevents credentials leaks.

*   **To run the built image:**
    ```bash
    docker run -d -p 5000:5000 app
    ```

> 💡 **Interviewer Focus:** Differentiating between the Docker CLI client and the Daemon (context transfer), the default tag behavior (`:latest`), and the critical role of `.dockerignore` in optimizing build performance.

</details>

<hr/>

### ❓ Q19. **What is Git branching strategy?**

<details>
<summary><b>👀 Show Answer</b></summary>

A set of rules defined by a development team specifying how branches are named, when features are merged, and how releases are managed (e.g. GitFlow, Trunk-Based, Feature Branching). It keeps code commits organized and prevents merge conflicts.

> 💡 **Interviewer Focus:** Branching strategies matching release frequency.

</details>

<hr/>

### ❓ Q20. **What is the purpose of load balancers?**

<details>
<summary><b>👀 Show Answer</b></summary>

Load balancers distribute incoming network traffic across multiple servers (targets). This prevents single-instance exhaustion, optimizes resource utilization, and ensures high availability (if one server goes down, traffic is routed to healthy nodes).

> 💡 **Interviewer Focus:** Standard load balancing architectures.

</details>

<hr/>

### ❓ Q21. **What is a reverse proxy?**

<details>
<summary><b>👀 Show Answer</b></summary>

A reverse proxy sits in front of backend servers, receiving client requests and forwarding them to target backends. It acts as an abstraction layer, handling security termination (SSL), rate limiting, caching, and request routing.

> 💡 **Interviewer Focus:** Reverse proxy security advantages.

</details>

<hr/>

### ❓ Q22. **What is the purpose of the `/etc/hosts` file?**

<details>
<summary><b>👀 Show Answer</b></summary>

It is a local operating system text file that maps hostnames directly to IP addresses. It overrides external DNS lookups for the system, allowing developers to route domain names to local or test IPs.

> 💡 **Interviewer Focus:** Local network resolution overrides.

</details>

<hr/>

### ❓ Q23. **What is port forwarding in network configurations?**

<details>
<summary><b>👀 Show Answer</b></summary>

Port forwarding redirects a communication request from one address and port combination to another while data is traversing a network gateway (e.g. exposing port 80 of a container as port 8080 on the host VM).

> 💡 **Interviewer Focus:** Container host port binding mechanisms.

</details>

<hr/>

### ❓ Q24. **Explain what an agent is in Jenkins.**

<details>
<summary><b>👀 Show Answer</b></summary>

An agent (or worker node) is a machine or container configured to run build job steps directed by the Jenkins master. This allows distributing workload compilation across multiple physical nodes to save master resources.

> 💡 **Interviewer Focus:** Scalable executor configurations.

</details>

<hr/>

### ❓ Q25. **What is the difference between public keys and private keys?**

<details>
<summary><b>👀 Show Answer</b></summary>

Public and private keys are the two components of **Asymmetric Cryptography** (public-key cryptography). Unlike symmetric encryption which uses the same key to lock and unlock data, asymmetric systems use a mathematically linked key pair where **what one key encrypts, only the other key can decrypt**. 

Here is a direct technical comparison:

| Feature | Public Key | Private Key |
| :--- | :--- | :--- |
| **Confidentiality** | Shared freely with the public (e.g. uploaded to GitHub or hosted on servers). | Kept strictly secret by the owner. Never shared. |
| **Main Function 1** | **Encryption:** Anyone can use it to encrypt data destined for you. | **Decryption:** Only you can use it to decrypt data that was encrypted with your public key. |
| **Main Function 2** | **Signature Verification:** Used by others to verify that you signed a file or commit. | **Digital Signing:** Used by you to sign files, code, or Git commits to prove you sent them. |

---

#### Detailed Cryptographic Operations
1.  **Asymmetric Encryption (Confidentiality):**
    *   If user A wants to send a secret database password to user B:
    *   User A encrypts the password using **User B's Public Key**.
    *   Once encrypted, the file cannot be decrypted by User A or anyone else on the network—it can **only** be decrypted using **User B's Private Key**.
2.  **Digital Signatures (Authenticity & Integrity):**
    *   If you want to prove you built a Docker image:
    *   You generate a hash of the image and encrypt it with your **Private Key** (this is your digital signature).
    *   Others decrypt the signature using your **Public Key** and compare hashes. If they match, they are certain that the image came from you and has not been modified.

#### Common DevOps Use Cases
*   **SSH Logins:** The remote server holds your public key in `authorized_keys`. Your local machine uses the private key to authenticate.
*   **SSL/TLS (HTTPS):** Web servers (like Nginx) use a private key to decrypt web traffic. Web browsers use the server's public key (included in the SSL certificate) to encrypt traffic.
*   **Git Commit Signing:** Developers sign Git commits using their GPG private key to prevent email spoofing on commit logs.

> 💡 **Interviewer Focus:** Cryptographic logic (what one key encrypts, only the other can decrypt), key permissions management, and identifying when to use key pairs (SSL/TLS handshake, SSH keys, GPG signatures).

</details>

<hr/>

## 🟡 Intermediate Level

### ❓ Q26. **What is the difference between Continuous Delivery and Continuous Deployment?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Continuous Delivery:**
  - Code changes are automatically built, tested, and packaged into a deployable artifact (like a Docker image).
  - The actual release to production requires **manual intervention** (e.g., a manager clicking an approval button in the UI).
- **Continuous Deployment:**
  - Bypasses the manual approval step.
  - Every change that passes all validation tests throughout the pipeline is deployed directly to production automatically.

> 💡 **Interviewer Focus:** Risk mitigation differences. Continuous Deployment requires extremely comprehensive automated testing suites (unit, integration, and E2E) to be safe.

</details>

<hr/>

### ❓ Q27. **What is a Docker Multi-Stage Build and why is it useful?**

<details>
<summary><b>👀 Show Answer</b></summary>

Multi-stage builds allow developers to use multiple `FROM` statements in a single Dockerfile. Each `FROM` instruction begins a new temporary build stage. You can compile code, build assets, and run tests in early stages, and then selectively copy only the final compiled outputs (like static files or binaries) to a minimal, lightweight runner stage.

- **Why it is useful:** 
  1. **Minimal Image Size:** Excludes build-time compilers, SDKs, devDependencies, and raw source code from the final production runtime.
  2. **Reduced Security Attack Surface:** The final container lacks package managers (like npm/yarn) and terminal utilities (like curl or git), reducing vulnerability vectors.
  3. **Leverages Cache:** Stages can be cached independently, speeding up subsequent CI/CD pipeline builds.

---

#### 🛠️ Production 3-Tier Stack Application Example
In a standard 3-tier application consisting of a **React/Next.js Frontend**, **Node.js Backend (Express/TS)**, and a **MySQL Database**, we build multi-stage Dockerfiles for the compute layers and orchestrate them together.

##### 1. Tier 1: Next.js Frontend (`frontend/Dockerfile`)
This utilizes Next.js's native `standalone` output mode to bundle only the necessary files for production, drastically reducing image size from >1GB to ~100MB.

```dockerfile
# Stage 1: Dependencies install
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Stage 2: Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Set environment to production during build (required for Next.js optimizations)
ENV NODE_ENV=production
RUN npm run build

# Stage 3: Runner stage (Production)
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
# Run as non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy standalone build bundle, static assets, and public files
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

###### 📝 Line-by-Line Explanation:
* **`FROM node:20-alpine AS deps`**: Uses a lightweight Node.js base image on Alpine Linux for installing dependencies, designated as the `deps` stage.
* **`WORKDIR /app`**: Creates and sets the active working directory inside the container to `/app`.
* **`COPY package*.json ./`**: Copies the package description files. Copying these first ensures that dependency installation steps can use Docker cache if dependencies are unchanged.
* **`RUN npm ci`**: Installs dependencies cleanly and deterministically directly from the lockfile, which is faster and safer for pipelines.
* **`FROM node:20-alpine AS builder`**: Starts a fresh build stage named `builder` to perform compilation without bloating the final image with dependencies tools.
* **`COPY --from=deps /app/node_modules ./node_modules`**: Copies the pre-installed `node_modules` from the `deps` stage directly, avoiding repeating the download.
* **`COPY . .`**: Copies the rest of the application files to the builder directory.
* **`ENV NODE_ENV=production`**: Sets the build-time environment variable to production (which tells Next.js to enable tree-shaking, minification, and output standalone optimizations).
* **`RUN npm run build`**: Builds the application, outputting static files and the optimized Next.js server engine.
* **`FROM node:20-alpine AS runner`**: Starts the third, final production runtime stage. This is the only stage included in the final pushed image.
* **`WORKDIR /app`** & **`ENV NODE_ENV=production`**: Configures runtime work directory and forces the Node process to execute in production mode.
* **`RUN addgroup --system --gid 1001 nodejs`**: Creates a low-privilege system group named `nodejs` for the container runtime process.
* **`RUN adduser --system --uid 1001 nextjs`**: Creates a restricted system user named `nextjs` associated with that group.
* **`COPY --from=builder /app/public ./public`**: Copies public static files (images, icons) directly from the `builder` stage.
* **`COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./`**: Copies Next.js's optimized node-server bundle. The `--chown` flag assigns user permissions to our restricted non-root user.
* **`COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static`**: Copies the compiled front-end JS chunks/CSS.
* **`USER nextjs`**: Discards root access and forces the container's execution steps to run under the restricted user (`nextjs`) to mitigate security risks.
* **`EXPOSE 3000`**: Informs the container runtime that the container intends to use network port 3000.
* **`ENV PORT=3000`** & **`ENV HOSTNAME="0.0.0.0"`**: Configures default port variables and binds host networking endpoints.
* **`CMD ["node", "server.js"]`**: The runtime command that starts up the standalone Next.js production server.

---

##### 2. Tier 2: Node.js Backend API Server (`backend/Dockerfile`)
Compiles TypeScript, drops devDependencies, and runs in a minimal environment.

```dockerfile
# Stage 1: Build & compile TypeScript
FROM node:20-alpine AS builder
WORKDIR /usr/src/app
COPY package*.json tsconfig.json ./
RUN npm ci
COPY ./src ./src
RUN npm run build # Compiles TS to JS inside /dist

# Stage 2: Clean install production dependencies only
FROM node:20-alpine AS production-deps
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm ci --only=production

# Stage 3: Minimal runtime execution
FROM node:20-alpine AS runner
WORKDIR /usr/src/app
ENV NODE_ENV=production
# Copy compiled Javascript from builder
COPY --from=builder /usr/src/app/dist ./dist
# Copy production node_modules from production-deps
COPY --from=production-deps /usr/src/app/node_modules ./node_modules
COPY package*.json ./

USER node
EXPOSE 5000
CMD ["node", "dist/server.js"]
```

###### 📝 Line-by-Line Explanation:
* **`FROM node:20-alpine AS builder`**: Begins the build stage to compile TypeScript code.
* **`WORKDIR /usr/src/app`**: Sets the default internal workspace folder.
* **`COPY package*.json tsconfig.json ./`**: Copies configuration dependencies and TypeScript config specifications.
* **`RUN npm ci`**: Installs all dependencies, including development tools (like `typescript` and compiler CLI libraries).
* **`COPY ./src ./src`**: Copies typescript source files.
* **`RUN npm run build`**: Runs compiler scripts (`tsc`) to convert TS source into runnable Javascript inside `/dist`.
* **`FROM node:20-alpine AS production-deps`**: Starts a separate temporary stage to acquire a clean, production-only `node_modules` folder.
* **`RUN npm ci --only=production`**: Runs dependencies downloads, skipping heavy devDependencies (like linters, compilers, and test suites) to save space.
* **`FROM node:20-alpine AS runner`**: Starts the final runtime image stage.
* **`COPY --from=builder /usr/src/app/dist ./dist`**: Pulls the compiled production JS files from the `builder` stage.
* **`COPY --from=production-deps /usr/src/app/node_modules ./node_modules`**: Copies production-only dependencies from the `production-deps` stage.
* **`USER node`**: Switches to the built-in non-root user `node` for security hardening.
* **`EXPOSE 5000`**: Tells Docker the backend API server will listen on port 5000.
* **`CMD ["node", "dist/server.js"]`**: Boots the application by executing the compiled entrypoint JS file.

---

##### 3. Tier 3 & Orchestration: Multi-Container Setup (`docker-compose.yml`)
Connects the React/Next.js frontend, Node.js backend, and Tier 3 (MySQL database) securely.

```yaml
version: '3.8'

services:
  # Tier 3: Database layer
  db:
    image: mysql:8.0
    container_name: mysql_db
    restart: always
    environment:
      MYSQL_DATABASE: app_db
      MYSQL_ROOT_PASSWORD: root_secure_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - app_network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p$$MYSQL_ROOT_PASSWORD"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Tier 2: Backend API layer
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: node_backend
    restart: always
    environment:
      DB_HOST: db
      DB_USER: root
      DB_PASSWORD: root_secure_password
      DB_NAME: app_db
      PORT: 5000
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "5000:5000"
    networks:
      - app_network

  # Tier 1: Frontend layout layer
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: nextjs_frontend
    restart: always
    environment:
      NEXT_PUBLIC_API_URL: http://backend:5000
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - app_network

volumes:
  mysql_data:

networks:
  app_network:
    driver: bridge
```

###### 📝 Block-by-Block Explanation:
* **`version: '3.8'`**: Defines the Docker Compose syntax version for compatibility parsing.
* **`services:`**: Initiates the block detailing each container configuration in the stack.
* **`db:`**: Defines the database service container.
  * **`image: mysql:8.0`**: Uses the official, pre-compiled MySQL 8.0 database image.
  * **`restart: always`**: Sets the policy to automatically reboot the database if it crashes or host restarts.
  * **`environment:`**: Passes environment configs initializing the database name and root password.
  * **`ports: - "3306:3306"`**: Maps standard MySQL port 3306 on the host VM to container port 3306.
  * **`volumes: - mysql_data:/var/lib/mysql`**: Mounts a named volume to ensure database files are preserved on the host disk even if the container is destroyed/rebuilt.
  * **`healthcheck:`**: Periodically tests container health. `mysqladmin ping` checks if the SQL daemon is fully ready to accept sockets connection.
* **`backend:`**: Configures the API server container.
  * **`build:`**: Instructs Compose to compile the container image locally pointing to `/backend` directory.
  * **`environment:`**: Supplies environmental variables detailing DB host credentials (passing the database service name `db` as host endpoint).
  * **`depends_on: db: condition: service_healthy`**: Crucial coordination step. The backend will delay its startup sequence until the database container reports its health check as healthy.
  * **`ports: - "5000:5000"`**: Maps backend routing ports.
  * **`networks: - app_network`**: Attaches container to the shared bridge network.
* **`frontend:`**: Defines the user layout tier.
  * **`environment: NEXT_PUBLIC_API_URL`**: Passes API connection strings.
  * **`depends_on: - backend`**: Ensures the backend exists before launching frontend.
* **`volumes: mysql_data:`**: Declares the persistent, named volume storage schema.
* **`networks: app_network: driver: bridge`**: Defines an isolated, software-defined bridge network so container microservices can securely communicate using local hostname resolution (e.g. `backend` routes directly to the API server).

---

> 💡 **Interviewer Focus:** Image optimization (Next.js standalone build sizes), separating build compilation (TypeScript/webpack compilation) from runner containers, secure non-root user permissions, container dependencies coordination (using `depends_on` healthchecks), and configuration injections.

</details>

<hr/>

### ❓ Q28. **What are software deployments and their types, along with their popularity and real-world industry adoption?**

<details>
<summary><b>👀 Show Answer</b></summary>

A **software deployment** is the process of building, packaging, distributing, and running new software updates or configuration modifications on target environments (virtual machines, containers, or serverless clusters), making those changes available to end users. 

In the real industry, organizations use different deployment strategies (types) to balance risk, downtime, resource capacity, and deployment costs:

---

#### 1. Software Deployment Types & Strategies

1.  **Rolling Deployment (Incremental Rollout):**
    *   *What it is in simple terms:* You upgrade your servers **one by one** (or in small groups) until all of them are running the new version.
    *   *How it works step-by-step (e.g. updating 4 servers from v1 to v2):*
        1.  The deployment system takes **Server 1** offline. (The other 3 servers remain online and handle all user traffic).
        2.  The system installs v2 on Server 1 and runs health checks.
        3.  Once Server 1 is confirmed healthy, it is brought back online.
        4.  The system repeats this exact process sequentially for Server 2, Server 3, and Server 4.
    *   **Pros:** Zero downtime. Requires no extra host resources since it runs within the existing server footprint.
    *   **Cons:** v1 and v2 run concurrently in production during rollout, requiring backward database compatibility. Rollbacks require redeploying the previous build.
2.  **Canary Deployment (Progressive Exposure):**
    *   *What it is in simple terms:* You release the new version to **only a small percentage of users** (like 2%) first to test it, and if it works fine, you gradually roll it out to everyone else.
    *   *How it works step-by-step (e.g. updating 10 servers from v1 to v2):*
        1.  You deploy v2 to just **1 server** (representing 10% of your total servers).
        2.  You configure the Load Balancer/Router to send **90% of user traffic** to the 9 servers running v1, and **10% of traffic** to the 1 server running v2.
        3.  You run this setup for a trial period (e.g., a few hours) while monitoring application logs and error metrics.
        4.  *If errors occur:* You instantly shut down the v2 server and route 100% of traffic back to v1. Only 10% of users experienced the bug (limiting the "blast radius").
        5.  *If no errors occur:* You gradually upgrade the remaining 9 servers to v2.
    *   **Pros:** Minimizes the "blast radius" of code errors. Safest progressive delivery strategy.
    *   **Cons:** Complex traffic-routing rules are required at the service mesh or load balancer level.
3.  **Blue-Green Deployment (Instant Switch):**
    *   *What it is in simple terms:* You build a **complete duplicate set of servers** running the new version, test it in isolation, and then instantly switch all user traffic to it.
    *   *How it works step-by-step:*
        1.  You have your active production environment, called **Blue**, running v1.
        2.  You spin up an entirely separate, identical environment, called **Green**, running v2.
        3.  Since Green is not connected to the public router yet, users cannot access it. You run QA and automated tests directly against Green to verify its health in production.
        4.  Once verified, you update the Load Balancer/DNS routing rules to instantly point all incoming user requests to **Green** instead of Blue.
        5.  *If Green fails:* You instantly point the router back to **Blue** (v1). No code rollbacks are required.
    *   **Pros:** Near-instant deployment and near-instant rollback (just flip routing back to Blue). No version concurrency in production.
    *   **Cons:** Expensive, as it doubles resource costs during the deployment validation window.
4.  **Recreate Deployment (Downtime Swap):**
    *   *What it is in simple terms:* You turn off **all old servers first** (causing a brief downtime), and then turn on the new servers.
    *   *How it works step-by-step:*
        1.  You stop and terminate **all** running instances of v1.
        2.  During this time, the application is completely offline for users (downtime phase).
        3.  The system provisions and boots up all new instances of v2.
        4.  Once v2 servers pass health checks, the router starts sending traffic to them, bringing the app back online.
    *   **Pros:** Simplest setup. Zero risk of version concurrency conflicts since v1 and v2 never run at the same time.
    *   **Cons:** Causes direct service downtime between shutdown and boot phases.
5.  **Shadow Deployment (Traffic Mirroring):**
    *   *What it is in simple terms:* You run the new version silently in the background and **copy real user requests** to it to test performance, but the users never see its responses.
    *   *How it works step-by-step:*
        1.  Users send requests to the active v1 servers.
        2.  The API Gateway/Router receives the request and duplicates (forks) it.
        3.  The original request goes to v1, which returns the response to the user.
        4.  The duplicated copy of the request is sent to v2 in the background.
        5.  v2 processes the request (allowing you to test its CPU usage, memory, and database writes), but its final response is discarded. The user is unaware of this secondary check.
    *   **Pros:** Perfect for testing performance, capacity limits, and logic accuracy with real traffic safely.
    *   **Cons:** Difficult to configure, and doubles backend query load on database layers.

---

#### 2. Industry Popularity & Adoption Order

| Rank | Strategy | Adoption Level | Real-World Industry Context |
| :--- | :--- | :--- | :--- |
| **1** | **Rolling** | **High** (Standard default) | It is the default deployment mechanism in **Kubernetes** (`RollingUpdate`) and **AWS ECS**. It provides zero downtime without requiring extra server budget. |
| **2** | **Canary** | **Medium-High** (Enterprise standard) | Considered the gold standard for high-traffic platforms (like Netflix, Spotify). It minimizes blast radius by limiting initial user exposure. |
| **3** | **Blue-Green** | **Medium** | Preferred for critical financial or transactional backends where rollbacks must be instantaneous, but avoided by resource-conscious teams due to double host costs. |
| **4** | **Recreate** | **Low** | Typically restricted to non-production environments (Dev/Staging), batch processing APIs, or legacy databases that cannot support concurrent version connections. |
| **5** | **Shadow** | **Very Low** (Advanced edge case) | Restricted to large enterprises testing critical core infrastructure changes (like upgrading API gateways or core database engines). |

> 💡 **Interviewer Focus:** Evaluating trade-offs of each strategy, explaining rollback mechanics, managing data compatibility, and selecting strategies based on SLA constraints and budgets.

</details>

<hr/>

### ❓ Q29. **How does Kubernetes manage containers? Explain Pods, Deployments, and Services.**

<details>
<summary><b>👀 Show Answer</b></summary>

Kubernetes does not run containers directly. Instead, it manages containers through abstraction objects to provide scaling, durability, networking, and discovery. The core architecture relies on three primary resources: **Pods**, **Deployments**, and **Services**.

---

#### 1. Pods: The Atomic Unit of Execution
A **Pod** is the smallest deployable unit in Kubernetes. It acts as a logical wrapper for your containers.
* **Shared Environment:** All containers inside a single Pod share the same **Network Namespace** (same IP address, port space, and local loopback interface) and **Storage Volumes**.
* **Co-location:** Containers in a Pod are scheduled onto the same physical worker node and started/stopped together.
* **Single vs. Multi-Container:** The standard pattern is **one container per Pod**. Multi-container Pods are reserved for tight coupling patterns, such as the *Sidecar Pattern* (e.g., a main Node.js app container sharing a volume with a log-shipping container).
* **Life Cycle:** Pods are **ephemeral** and disposable. When a node crashes, the Pods on it are destroyed and not resurrected. Instead, a controller creates new ones from scratch with new IP addresses.

---

#### 2. Deployments: Managing State & Scale
A **Deployment** is a declarative controller that manages the lifecycle of your Pods.
* **Reconciliation Loop:** You declare your desired state (e.g., "I want exactly 3 replicas of my API container running"), and the Deployment Controller runs a continuous control loop (actual state vs. desired state) to ensure that exact count is maintained. If a container crashes, the controller spawns a replacement.
* **ReplicaSets:** Behind the scenes, a Deployment creates and manages a **ReplicaSet**, which directly handles creating and terminating pods.
* **Release Orchestration:** Deployments handle updates seamlessly without downtime using strategies like:
  * **RollingUpdate (Default):** Spawns new version pods (v2) incrementally, waits for health checks to pass, and terminates old pods (v1) one by one.
  * **Recreate:** Terminates all v1 pods first, then spawns all v2 pods (causes brief downtime, but avoids running two versions concurrently).
* **Rollbacks:** Keeps a revision history. You can roll back to a previous stable build instantly with a single command (`kubectl rollout undo deployment/api`).

---

#### 3. Services: Reliable Networking & Service Discovery
Since Pods are constantly created and destroyed, their IP addresses change frequently. A **Service** provides a stable, permanent IP address and DNS name to route traffic to a dynamic group of Pods.
* **Decoupling:** Frontend code doesn't need to know the IPs of backend pods; it simply calls the Service name (e.g., `http://express-api-service`).
* **Load Balancing:** When traffic hits the service, it automatically load-balances requests across all healthy target Pods in the backend pool.
* **Service Types:**
  * **ClusterIP (Default):** Exposes the Service on a cluster-internal IP. Accessible only within the Kubernetes cluster.
  * **NodePort:** Exposes the Service on each node's IP at a static port (usually `30000-32767`). Allows external traffic access.
  * **LoadBalancer:** Requests a physical load balancer (like AWS NLB/ALB) from your cloud provider to route external traffic to your service.
  * **ExternalName:** Maps the service to an external DNS domain name.

---

#### 🔗 The Glue: Labels and Selectors
Kubernetes uses **Labels** (key-value pairs attached to objects) and **Selectors** (queries to search for labels) to link resources together dynamically.

```
 [Client Traffic] ──> [Service: Selector (app=express-api)]
                               │
               ┌───────────────┼───────────────┐
               ▼               ▼               ▼
           [Pod v1.0]      [Pod v1.0]      [Pod v1.0]
         (label: app=express-api)
```

* The **Service** queries for `app: express-api` to build its list of target endpoints.
* The **Deployment** uses a selector for `app: express-api` to monitor and manage the lifecycle of those Pods.

---

#### 📄 Manifest Example (Express API Deployment & Service)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: express-api-deployment       # Name of the deployment resource
spec:
  replicas: 3                        # Desired state: maintain exactly 3 running pods
  selector:
    matchLabels:
      app: express-api               # Deployment manages pods that have this label
  template:                          # Template for creating new pods
    metadata:
      labels:
        app: express-api             # Label attached to every pod spawned by this template
    spec:
      containers:
      - name: express-api
        image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/express-api:v1.0
        ports:
        - containerPort: 5000        # The port inside the pod the container listens on
---
apiVersion: v1
kind: Service
metadata:
  name: express-api-service          # The stable internal DNS name: express-api-service
spec:
  selector:
    app: express-api                 # Route traffic to pods matching this label
  ports:
  - protocol: TCP
    port: 80                         # Port client calls on the service (internal cluster port)
    targetPort: 5000                 # Target port on the container to route traffic to
  type: ClusterIP                    # Cluster-internal routing only
```

---

#### 🛠️ Essential Kubernetes Commands (`kubectl` CLI)
Here are the key commands used in real-world scenarios to deploy, scale, and debug Pods, Deployments, and Services:

##### 1. Creation & Deletion
*   **Apply Manifests:** Creates or updates resources defined in a YAML file.
    ```bash
    kubectl apply -f manifest.yaml
    ```
*   **Delete Resources:** Gracefully destroys resources defined in a YAML file.
    ```bash
    kubectl delete -f manifest.yaml
    ```

##### 2. Inspection & Observability
*   **Check Resource Status:** Lists resources in the current namespace (e.g. pods, deployments, services).
    ```bash
    kubectl get pods
    kubectl get deployments
    kubectl get services -o wide
    # Get all resources at once
    kubectl get all
    ```
*   **Describe Details:** Inspects specific resource details, state transitions, and scheduling event histories (highly useful for diagnosing scheduler errors, port conflicts, or pull failures).
    ```bash
    kubectl describe pod <pod-name>
    kubectl describe deployment/express-api-deployment
    ```
*   **Fetch Container Logs:** Streams standard output and standard error logs from running containers.
    ```bash
    kubectl logs <pod-name>
    # Stream/follow live logs
    kubectl logs -f <pod-name>
    # If the pod runs multiple containers, specify the container name:
    kubectl logs <pod-name> -c express-api
    ```
*   **Execute Shell (SSH substitute):** Spawns an interactive terminal shell inside a running container to troubleshoot configuration or database connections.
    ```bash
    kubectl exec -it <pod-name> -- sh
    ```

##### 3. Management & Scaling
*   **Manual Scaling:** Dynamically adjusts the replica numbers without editing the raw template file.
    ```bash
    kubectl scale deployment/express-api-deployment --replicas=5
    ```
*   **Port-Forwarding (Local Tunneling):** Tunnels network connections from a local port directly to a pod or service port within the cluster network.
    ```bash
    kubectl port-forward service/express-api-service 8080:80
    # Accessible locally at http://localhost:8080
    ```

##### 4. Rollouts & Rollbacks
*   **Monitor Rollout Progress:** Shows status steps of rolling updates.
    ```bash
    kubectl rollout status deployment/express-api-deployment
    ```
*   **View Revision History:** Lists past deployment configurations.
    ```bash
    kubectl rollout history deployment/express-api-deployment
    ```
*   **Undo/Rollback Release:** Reverts the deployment back to the previous deployment revision.
    ```bash
    kubectl rollout undo deployment/express-api-deployment
    ```

> 💡 **Interviewer Focus:** Explain how labels act as the dynamic registry linking Services to Pods, contrast the lifecycle of ephemeral Pods with persistent Services, and describe the self-healing role of the Deployment reconciliation loop.

</details>

<hr/>

### ❓ Q30. **Explain how Nginx acts as a Reverse Proxy.**

<details>
<summary><b>👀 Show Answer</b></summary>

A reverse proxy sits in front of backend application servers and intercepts client requests before forwarding them to the backends.
- **Why use Nginx as a reverse proxy:**
  - **Load Balancing:** Distributes client requests across multiple backend application servers.
  - **SSL Termination:** Handles SSL decryption at Nginx, freeing backend servers from the CPU cost of encryption.
  - **Caching & Compression:** Caches static assets and compresses responses (gzip) to save bandwidth.
  - **Security:** Hides the IP addresses and structure of backend application servers from the public internet.
- **Nginx configuration proxy block for Node.js:**
  ```nginx
  server {
      listen 80;
      server_name api.example.com;
      
      location /api/ {
          proxy_pass http://node_api_backend:5000;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection 'upgrade';
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_cache_bypass $http_upgrade;
      }
  }
  ```

> 💡 **Interviewer Focus:** SSL termination configurations, caching static files, and header injection to pass the client's actual IP to Node.js backend.

</details>

<hr/>

### ❓ Q31. **What is Prometheus and Grafana? How do they work together?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Prometheus:** 
  - An open-source metrics monitoring and alerting system.
  - Relies on a **pull model**, regularly fetching numeric metrics from target applications via HTTP endpoints (e.g., `/metrics`).
  - Stores metrics in a Time-Series Database (TSDB).
- **Grafana:**
  - A visualization and dashboard builder.
  - Connects to Prometheus as a data source to query metrics using PromQL (Prometheus Query Language) and render them in real-time charts, graphs, and alerts.

> 💡 **Interviewer Focus:** Pull model vs push model metrics collection architectures.

</details>

<hr/>

### ❓ Q32. **Explain the concept of Immutable Infrastructure.**

<details>
<summary><b>👀 Show Answer</b></summary>

Immutable Infrastructure is an operations model where servers are never modified in-place after they are provisioned.
- If an application update or patch is required, a new server image (AMI) is built, and new server instances are spun up to replace the old ones. The old servers are decommissioned.
- **Benefits:** Prevents configuration drift and guarantees that environments (testing, staging, production) are identical.

> 💡 **Interviewer Focus:** Contrasting mutable infrastructure (SSHing into servers to pull code or update dependencies) with immutable infrastructure workflows.

</details>

<hr/>

### ❓ Q33. **What is GitOps?**

<details>
<summary><b>👀 Show Answer</b></summary>

GitOps is a CD model for cloud-native applications. It uses Git as a single source of truth for declarative infrastructure configurations.
- Automators (like ArgoCD) read Git configurations and automatically synchronize the live state of Kubernetes clusters to match Git commits, blocking drift modifications.

> 💡 **Interviewer Focus:** Sync control automation.

</details>

<hr/>

### ❓ Q34. **What is a Docker Volume and why is it used?**

<details>
<summary><b>👀 Show Answer</b></summary>

A Docker Volume is a mechanism to persist data generated by and used by Docker containers outside the container's union file system.
- **Why it is used:** Containers are ephemeral (data is lost on container deletion). Volumes bypass container copy-on-write systems, storing database data directly on the host VM disk, which survives restarts.

> 💡 **Interviewer Focus:** Stateful storage configurations.

</details>

<hr/>

### ❓ Q35. **What is the difference between Docker Compose and Kubernetes?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Docker Compose:** Designed for local development or simple host setups. Uses a single YAML file to deploy multi-container environments on a single machine.
- **Kubernetes:** A production-grade container orchestrator designed to scale across thousands of physical server machines (clusters), managing auto-scaling, replication, cluster networks, and self-healing dynamically.

> 💡 **Interviewer Focus:** Local scripting vs production orchestration tools.

</details>

<hr/>

### ❓ Q36. **Explain what an Ingress Controller is in Kubernetes.**

<details>
<summary><b>👀 Show Answer</b></summary>

An Ingress Controller is a specialized proxy (e.g. Nginx, Traefik, or AWS Load Balancer Controller) that runs inside the Kubernetes cluster. It implements Ingress resources, routing external HTTP/HTTPS traffic to internal Kubernetes Services based on URL paths or host domain names.
*   **Ingress Resource Example:**
    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: app-ingress
      annotations:
        kubernetes.io/ingress.class: "nginx"
    spec:
      rules:
      - host: myapp.com
        http:
          paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: express-api-service
                port:
                  number: 80
          - path: /
            pathType: Prefix
            backend:
              service:
                name: react-frontend-service
                port:
                  number: 80
    ```

> 💡 **Interviewer Focus:** HTTP routing ingress interfaces, how Ingress differs from a NodePort/LoadBalancer Service, and path-based vs host-based routing configurations.

</details>

<hr/>

### ❓ Q37. **What is a Jenkinsfile?**

<details>
<summary><b>👀 Show Answer</b></summary>

A Jenkinsfile is a text configuration file that defines a Jenkins build pipeline as code. It contains the sequence of stages, steps, variables, and environments required to compile, test, package, and deploy code, stored inside the Git repository.
*   **MERN Stack Declarative Jenkinsfile Example:**
    ```groovy
    pipeline {
        agent any
        environment {
            REGISTRY = "123456789012.dkr.ecr.us-east-1.amazonaws.com"
            IMAGE_NAME = "express-api"
            IMAGE_TAG = "${env.BUILD_NUMBER}"
        }
        stages {
            stage('Install Dependencies') {
                steps {
                    sh 'npm install'
                }
            }
            stage('Run Tests') {
                steps {
                    sh 'npm test'
                }
            }
            stage('Build Docker Image') {
                steps {
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
            stage('Push to ECR') {
                steps {
                    sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${REGISTRY}"
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }
    ```

> 💡 **Interviewer Focus:** Pipeline-as-code management, declarative vs scripted pipeline syntax, and ECR login authentication inside build agents.

</details>

<hr/>

### ❓ Q38. **Explain the purpose of health checks in a containerized environment.**

<details>
<summary><b>👀 Show Answer</b></summary>

Health checks verify container status dynamically:
*   **Liveness Probes:** Check if a container is running. If it fails, the container is restarted automatically.
*   **Readiness Probes:** Check if the container is ready to accept user network traffic. If it fails, the container is removed from target load balancer pools.
*   **Kubernetes Probes Example (Express API checking `/healthz`):**
    ```yaml
    spec:
      containers:
      - name: express-api
        image: express-api:v1
        livenessProbe:
          httpGet:
            path: /healthz
            port: 5000
          initialDelaySeconds: 15
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /healthz
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
    ```

> 💡 **Interviewer Focus:** Self-healing configurations, setting appropriate initial delays, and avoiding infinite restart loops if probes check external dependencies incorrectly.

</details>

<hr/>

### ❓ Q39. **What does the command `git stash` do?**

<details>
<summary><b>👀 Show Answer</b></summary>

It temporarily shelves (stashes) uncommitted modifications (staged and unstaged files) in a local cache, resetting the working directory to match the clean `HEAD` commit. This allows switching branches quickly without committing incomplete code.

> 💡 **Interviewer Focus:** Git workflow utilities.

</details>

<hr/>

### ❓ Q40. **How does Nginx handle load balancing algorithms?**

<details>
<summary><b>👀 Show Answer</b></summary>

Nginx supports multiple algorithms defined in its `upstream` configuration block:
- **Round-Robin** (Default): Distributes requests sequentially.
- **Least Connections**: Routes to the server with the fewest active connections.
- **IP Hash**: Uses the client's IP to calculate a hash key, routing requests from the same client to the same server for session persistence.

> 💡 **Interviewer Focus:** Session persistence vs balanced distribution.

</details>

<hr/>

### ❓ Q41. **What is container escape vulnerability?**

<details>
<summary><b>👀 Show Answer</b></summary>

A security vulnerability where a malicious process running inside a container breaks process boundaries to gain direct execution access and root privileges on the underlying host operating system.

> 💡 **Interviewer Focus:** Security risks of containers sharing host kernels.

</details>

<hr/>

### ❓ Q42. **What is semantic versioning (SemVer)?**

<details>
<summary><b>👀 Show Answer</b></summary>

A version numbering system: `MAJOR.MINOR.PATCH`.
- **MAJOR**: Incremented on breaking API modifications.
- **MINOR**: Incremented on backward-compatible feature additions.
- **PATCH**: Incremented on backward-compatible bug fixes.

> 💡 **Interviewer Focus:** Dependency version bounds rules.

</details>

<hr/>

### ❓ Q43. **Explain the purpose of Docker Swarm.**

<details>
<summary><b>👀 Show Answer</b></summary>

Docker Swarm is a clustering and container orchestration utility built directly into the Docker Engine. It enables managing a group of Docker hosts as a single virtual system, scaling services across hosts with less complexity than Kubernetes.

> 💡 **Interviewer Focus:** Swarm simplicity vs Kubernetes scalability.

</details>

<hr/>

### ❓ Q44. **What is ChatOps?**

<details>
<summary><b>👀 Show Answer</b></summary>

ChatOps integrates operational tools and deployment pipelines into chat environments (like Slack or Microsoft Teams). Teams trigger deployment scripts, query server health, or check build logs by sending commands to chat bots directly.

> 💡 **Interviewer Focus:** Collaborative operations automation.

</details>

<hr/>

### ❓ Q45. **What is the difference between Ansible and Terraform?**

<details>
<summary><b>👀 Show Answer</b></summary>

*   **Terraform (Infrastructure Provisioning):** Declarative tool designed to build and manage cloud infrastructure elements (VPCs, database instances, DNS entries) and track their states.
    *   *Example (Terraform code):*
        ```hcl
        resource "aws_instance" "app_server" {
          ami           = "ami-0c55b159cbfafe1f0"
          instance_type = "t2.micro"
          tags = { Name = "ExpressAPIServer" }
        }
        ```
*   **Ansible (Configuration Management):** Procedural/hybrid tool designed to configure software, patch packages, and manage files *inside* existing servers via SSH (agentless).
    *   *Example (Ansible Task):*
        ```yaml
        - name: Install and start Nginx web server
          apt:
            name: nginx
            state: present
          notify: Start Nginx
        ```

> 💡 **Interviewer Focus:** Target orchestration areas (IaC provisioning vs host configuration), state file management in Terraform vs push-based SSH tasks in Ansible.

</details>

<hr/>

### ❓ Q46. **What is standard input, standard output, and standard error in Unix?**

<details>
<summary><b>👀 Show Answer</b></summary>

They are standard I/O data streams in Unix-like operating systems:
- **`stdin` (0):** The stream where data enters the command (usually keyboard).
- **`stdout` (1):** The stream where standard output is printed (screen).
- **`stderr` (2):** The stream where error messages are written separately from stdout.

> 💡 **Interviewer Focus:** Redirecting logs and error streams in shell scripts.

</details>

<hr/>

### ❓ Q47. **What is a build artifact?**

<details>
<summary><b>👀 Show Answer</b></summary>

A build artifact is the compiled, packaged output of a CI pipeline build stage (e.g. a compiled JAR file, a ZIP directory, or a Docker image) that is ready to be stored in a registry and deployed to target hosts.

> 💡 **Interviewer Focus:** Decoupling build stages from deployment execution.

</details>

<hr/>

### ❓ Q48. **Explain the role of a reverse proxy in rate limiting.**

<details>
<summary><b>👀 Show Answer</b></summary>

A reverse proxy (like Nginx) intercepts client requests at the network edge, matching client IPs or tokens to rate limits. It blocks clients exceeding limits immediately, returning `HTTP 429` errors before requests hit backend app servers, preserving server resources.

> 💡 **Interviewer Focus:** Edge-based security architectures.

</details>

<hr/>

### ❓ Q49. **What are Helm charts in Kubernetes?**

<details>
<summary><b>👀 Show Answer</b></summary>

Helm is a package manager for Kubernetes. A Helm Chart is a collection of templated YAML files describing Kubernetes resources, combined with a `values.yaml` file containing parameter configuration values, enabling customizable, reproducible application deployments.

> 💡 **Interviewer Focus:** Packaging configurations in Kubernetes.

</details>

<hr/>

### ❓ Q50. **What is a dynamic inventory in Ansible?**

<details>
<summary><b>👀 Show Answer</b></summary>

A dynamic inventory script queries cloud providers (like AWS APIs) in real-time to generate the target host lists for Ansible playbooks dynamically, rather than relying on static IP files, which fail when auto-scaling groups spin hosts up and down.

> 💡 **Interviewer Focus:** Ansible scaling capabilities.

</details>

<hr/>

## 🔴 Advanced Level

### ❓ Q51. **How do you design a complete CI/CD pipeline from code commit to zero-downtime production deployment?**

<details>
<summary><b>👀 Show Answer</b></summary>

A production-ready pipeline follows a structured flow with feedback loops:
1. **Commit Stage (CI Trigger):**
   - Developer pushes a commit to a feature branch.
   - GitHub Actions / Jenkins triggers the pipeline.
2. **Build and Test Stage:**
   - Run code linter and security scanner (e.g., ESLint, SonarQube, Snyk).
   - Execute Unit/Integration Tests.
   - Compile code and build a Docker image using a multi-stage Dockerfile.
   - Run vulnerability scans on the Docker image (e.g., using Trivy).
3. **Artifact Registry Stage:**
   - Push the verified Docker image to a private registry (like AWS ECR) tagged with the unique Git commit hash.
4. **Staging / QA Deployment:**
   - Deploy the container image to a Staging environment.
   - Run automated End-to-End (E2E) testing suites (e.g., Cypress).
5. **Production Deployment (CD):**
   - Deploy to production using a GitOps controller (like ArgoCD) or via blue-green deployment.
   - If using Blue-Green, deploy the new image to the Green environment, validate liveness/readiness probes, and flip the ALB listener rule to route traffic to Green.
6. **Post-Deployment Verification:**
   - Monitor error logs (e.g., via Sentry/Winston) and resource metrics (Prometheus). If error counts spike, trigger automatic rollback.
- **Real-Time Experience Focus (Jenkins Pipeline):**
  - Architected CI/CD pipelines using **Jenkins, Docker, and AWS** (ECR/ECS), which reduced deployment time by 60% and improved release reliability. The pipeline builds the Node/Express Docker container, executes testing workflows, and deploys to ECS tasks via a blue-green strategy.

> 💡 **Interviewer Focus:** Guardrails, security scans at every stage, unique tagging of images, automated rollbacks on failure, and pipeline duration optimizations.

</details>

<hr/>

### ❓ Q52. **What is Canary Deployment and how do you implement it?**

<details>
<summary><b>👀 Show Answer</b></summary>

A **Canary Deployment** is a release strategy where you expose the new version of an application (v2) to a tiny fraction of users (e.g., 5%) while routing the remaining 95% to the old stable version (v1).
- **Implementation:**
  - **Kubernetes Traffic Splitting:** Use a Service Mesh (like Istio or Linkerd) or an Ingress Controller (like Nginx Ingress or Traefik) to split traffic based on percentages in the configuration.
  - **Monitoring:** Track application error rates, response latencies, and server metrics during the canary phase.
  - **Rollout:** If the metrics for v2 are healthy, scale up the routing percentage (10% -> 50% -> 100%). If error rates spike, route 100% of traffic back to v1 immediately.

```
                    ┌─── [Nginx Ingress Router] ───┐
                    │                              │
             (90% Traffic)                  (10% Traffic)
                    │                              │
         [Stable Pods (v1)]             [Canary Pods (v2)]
```

> 💡 **Interviewer Focus:** Automated canary analysis (ACA) and implementing metrics checks to drive automated progressive delivery.

</details>

<hr/>

### ❓ Q53. **How does Auto-Scaling work in Kubernetes? Compare HPA, VPA, and Cluster Autoscaler.**

<details>
<summary><b>👀 Show Answer</b></summary>

Kubernetes scales at both the container layer and the underlying server node layer:
- **Horizontal Pod Autoscaler (HPA):**
  - Adjusts the *number of pod replicas* in a deployment dynamically based on CPU/Memory usage or custom metrics (e.g., requests per second).
  - Best for: Handling spikes in user traffic by distributing load across more containers.
- **Vertical Pod Autoscaler (VPA):**
  - Adjusts the *resource limits (CPU and Memory allocated)* of existing containers within a pod.
  - Requires restarting the pod to apply changes (unless using modern in-place updates).
  - Note: HPA and VPA should not be run together on the same metrics.
- **Cluster Autoscaler (CA):**
  - Scales the *number of physical server nodes* in the cluster.
  - Triggers when pods fail to schedule because of insufficient CPU/Memory resources on existing nodes (scales up), or when nodes are underutilized for a period (scales down).

> 💡 **Interviewer Focus:** How HPA and Cluster Autoscaler interact (HPA spawns more pods -> nodes run out of capacity -> Cluster Autoscaler spawns more nodes).

</details>

<hr/>

### ❓ Q54. **What is GitOps and how do tools like ArgoCD work?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **GitOps:** An operational framework that takes DevOps best practices (version control, collaboration, CI/CD) and applies them to infrastructure management. The Git repository is the **single source of truth** for the desired state of the infrastructure.
- **How ArgoCD works (Pull-Based CD):**
  - ArgoCD is installed as a controller inside the Kubernetes cluster.
  - It continuously monitors the Git repository containing Kubernetes manifest files and compares it to the live cluster state.
  - If a difference is detected (e.g., someone pushed a new container version to Git, or someone manually modified a live pod via kubectl), ArgoCD flags it as `OutOfSync`.
  - It automatically applies the Git configuration to the cluster to reconcile the state, correcting manual changes and preventing configuration drift.

> 💡 **Interviewer Focus:** Pull-based (ArgoCD) vs push-based (Jenkins/GitHub Actions running kubectl commands) security profiles. Pull-based doesn't require storing cluster credentials in external CI tools.

</details>

<hr/>

### ❓ Q55. **How do you secure a containerized software supply chain?**

<details>
<summary><b>👀 Show Answer</b></summary>

Securing the supply chain requires locking down code, build pipelines, registries, and runtimes:
1. **Source Code:** Implement branch protection rules, require pull request sign-offs, and scan repository dependencies for CVEs (using GitHub Dependabot or Snyk).
2. **Build Stage:** Use official, minimal base images (like Alpine or Distroless). Distroless images contain only the application and runtime dependencies without shell utilities or package managers, reducing vulnerability risks.
3. **Image Scanning:** Run container image scans inside the CI pipeline (using tools like Trivy or Clair) and fail builds if high/critical vulnerabilities are found.
4. **Registry Signing:** Sign container images using **Cosign** (part of Sigstore) to prove image origin and authenticity.
5. **Runtime Validation:** Configure Kubernetes admission controllers to verify signatures and block unsigned images from running in the cluster.

> 💡 **Interviewer Focus:** Distroless base images benefit and implementing image signing routines.

</details>

<hr/>

### ❓ Q56. **How do you manage secrets securely in Kubernetes?**

<details>
<summary><b>👀 Show Answer</b></summary>

Kubernetes default Secrets are stored as base64-encoded strings, which is not secure.
*   **Secure Management:**
    *   Enable **KMS encryption at rest** for the Kubernetes `etcd` database.
    *   Use external secrets providers (like AWS Secrets Manager) coupled with the **External Secrets Operator (ESO)** to sync secrets to the cluster automatically.
*   **Kubernetes Secret YAML Manifest Example:**
    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: mern-db-secret
    type: Opaque
    data:
      # Value is base64 encoded: echo -n 'mongodb://admin:secret@host:27017' | base64
      MONGO_URI: bW9uZ29kYjovL2FkbWluOnNlY3JldEBob3N0OjI3MDE3
    ```
*   **Container Environment Variable Mapping:**
    ```yaml
    spec:
      containers:
      - name: express-api
        image: express-api:v1.0
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: mern-db-secret
              key: MONGO_URI
    ```

> 💡 **Interviewer Focus:** Eliminating base64 encoding vulnerabilities, securing etcd storage, and avoiding hardcoded secrets in configurations.

</details>

<hr/>

### ❓ Q57. **Explain database migration rollbacks inside an automated CD pipeline.**

<details>
<summary><b>👀 Show Answer</b></summary>

Rolling back database migrations automatically on application deployment failure is dangerous because it can destroy user data written since the deployment.
- **Best Practice:** Keep migrations **backward compatible** (Expand-and-Contract pattern). If the new application version fails, roll back only the compute container code, leaving the database changes intact on disk. Run manual cleanup scripts afterwards.

> 💡 **Interviewer Focus:** Decoupling code rollbacks from database state rollbacks.

</details>

<hr/>

### ❓ Q58. **What is the role of a Service Mesh in a microservices ecosystem?**

<details>
<summary><b>👀 Show Answer</b></summary>

A Service Mesh (like Istio) manages service-to-service communication. It runs a sidecar proxy (Envoy) next to every pod to handle:
- **Traffic Management:** Routing rules, canary splits, retries, and circuit breakers.
- **Security:** Enforcing **mutual TLS (mTLS)** encryption and access validation for all internal communications automatically.
- **Observability:** Distributed tracing and network latency aggregation.

> 💡 **Interviewer Focus:** Decoupling networking logic (mTLS, retries) from application code.

</details>

<hr/>

### ❓ Q59. **Explain log aggregation architecture using the ELK Stack at scale.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Filebeat (Shipper):** Lightweight agent running on nodes that forwards log files to Logstash.
- **Logstash (Filter):** Collects, parses, and structures logs (e.g. converting text to JSON fields) before shipping.
- **Elasticsearch (Search Engine):** Stores and indexes logs for real-time full-text search.
- **Kibana (Visualization):** The user interface to search logs and build dashboards.
- **Scale Optimization:** Place a buffer queue (Kafka or Redis) in front of Logstash to handle traffic ingestion bursts and prevent Elasticsearch database exhaustion.

```
[Host Logs] ──> [Filebeat] ──> [Kafka Queue] ──> [Logstash] ──> [Elasticsearch] ──> [Kibana]
```

> 💡 **Interviewer Focus:** Buffer queues utilization to handle logging surges.

</details>

<hr/>

### ❓ Q60. **How do you handle configuration management at scale?**

<details>
<summary><b>👀 Show Answer</b></summary>

Use declarative configuration tools:
- Avoid manual edits. Manage configuration files inside Git (Infrastructure-as-Code).
- Deploy configurations using **Ansible** (procedural host setups) or via Kubernetes ConfigMaps and Secrets updated dynamically by GitOps workflows (ArgoCD).

> 💡 **Interviewer Focus:** Enforcing git-to-server validation systems.

</details>

<hr/>

### ❓ Q61. **What is a Kubernetes Admission Controller?**

<details>
<summary><b>👀 Show Answer</b></summary>

It is a plugin that intercept API requests to the Kubernetes API server *after* authentication and authorization, but *before* object persistence in etcd.
- **Mutating Webhooks:** Can modify objects (e.g. inject sidecars).
- **Validating Webhooks:** Reject requests that violate constraints (e.g. blocking containers running as root).

> 💡 **Interviewer Focus:** Custom cluster policy enforcement.

</details>

<hr/>

### ❓ Q62. **Explain the difference between container runtime interfaces: containerd vs Docker Engine.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Docker Engine:** A complete developer suite containing image builders, CLI tools, and background services.
- **containerd:** A lightweight, low-level container runtime (originally developed by Docker, now part of CNCF) designed for integration into orchestrators like Kubernetes. It strips away builder tools, prioritizing execution efficiency.

> 💡 **Interviewer Focus:** Standard OCI interfaces and orchestrator runtime footprints.

</details>

<hr/>

### ❓ Q63. **What is the concept of a Chaos Monkey and Chaos Engineering?**

<details>
<summary><b>👀 Show Answer</b></summary>

Chaos Engineering is the practice of intentionally injecting faults (shutting down servers, dropping network packets, inducing memory leaks) into production environments to verify system resiliency and confirm that self-healing systems respond automatically.

> 💡 **Interviewer Focus:** Resiliency validation in production.

</details>

<hr/>

### ❓ Q64. **Explain how Prometheus monitors Kubernetes nodes using Node Exporter.**

<details>
<summary><b>👀 Show Answer</b></summary>

Node Exporter runs as a DaemonSet (one pod per physical node) in Kubernetes. It queries the local Linux kernel for hardware-level metrics (CPU usage, disk I/O, network packets) and exposes them on a `/metrics` HTTP endpoint. Prometheus regularly scrapes this endpoint to aggregate cluster metrics.

> 💡 **Interviewer Focus:** Metric exporting agents.

</details>

<hr/>

### ❓ Q65. **What is the purpose of the `/healthz` endpoint?**

<details>
<summary><b>👀 Show Answer</b></summary>

It is a convention for application health checking. The endpoint verifies internal app status (verifying database connectivity, checking caches, memory limits) and returns a simple status code (e.g. `200 OK` or `500 Error`) to warn load balancers.

> 💡 **Interviewer Focus:** Internal health validation.

</details>

<hr/>

### ❓ Q66. **Explain what an ingress resource does vs a load balancer service.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **LoadBalancer Service:** Provisions a dedicated, physical cloud load balancer (costly) per service, routing all incoming traffic on a single port directly.
- **Ingress Resource:** Exposes multiple HTTP/HTTPS services using a single entry point (ALB/Nginx). It matches domains or URL paths to route traffic internally, saving load balancer costs.

> 💡 **Interviewer Focus:** Ingress routing architectures.

</details>

<hr/>

### ❓ Q67. **How do you build a CI/CD pipeline using GitHub Actions?**

<details>
<summary><b>👀 Show Answer</b></summary>

Configure YAML workflow files in the `.github/workflows/` directory. Use GitHub-hosted runners or self-hosted runners to execute job steps (running actions, executing shell commands, caching dependencies, and managing environment secrets).
*   **GitHub Actions Workflow YAML Example (`.github/workflows/deploy.yml`):**
    ```yaml
    name: MERN Deploy Pipeline
    on:
      push:
        branches: [ main ]
    jobs:
      build-and-test:
        runs-on: ubuntu-latest
        steps:
        - name: Checkout Code
          uses: actions/checkout@v3
        - name: Setup Node.js
          uses: actions/setup-node@v3
          with:
            node-version: '20'
        - name: Install dependencies & run tests
          run: |
            npm ci
            npm test
        - name: Deploy via SSH
          uses: appleboy/ssh-action@master
          with:
            host: ${{ secrets.SERVER_HOST }}
            username: ubuntu
            key: ${{ secrets.SSH_PRIVATE_KEY }}
            script: |
              cd /var/www/express-api
              git pull origin main
              npm install --only=production
              pm2 restart express-api-service
    ```

> 💡 **Interviewer Focus:** Pipeline configuration structure, executing commands sequentially, cache strategy, and securing environment secrets.

</details>

<hr/>

### ❓ Q68. **Explain the concept of immutable tags in container registries.**

<details>
<summary><b>👀 Show Answer</b></summary>

Immutable tags block registries from overwriting existing tagged images (e.g. once `app:v1.0.0` is pushed, nobody can push a different image with the same tag). This ensures consistency and guarantees that deploying `v1.0.0` always runs the exact same image byte-code.

> 💡 **Interviewer Focus:** Security and reproducibility of releases.

</details>

<hr/>

### ❓ Q69. **What is a sidecar container pattern?**

<details>
<summary><b>👀 Show Answer</b></summary>

A design pattern where a helper container is deployed in the same pod alongside the main application container. The sidecar shares network namespaces and storage volumes, handling peripheral tasks (like log shipping, security proxies, or metrics exporting) without modifying application code.
*   **Sidecar Pattern YAML Manifest Example (Application + Log Shipper):**
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: app-with-sidecar
    spec:
      volumes:
      - name: shared-logs
        emptyDir: {}
      containers:
      - name: express-api
        image: express-api:v1
        volumeMounts:
        - name: shared-logs
          mountPath: /var/log/app
      - name: logstash-sidecar
        image: logstash:8.0
        volumeMounts:
        - name: shared-logs
          mountPath: /var/log/app
        command: ["/bin/sh", "-c", "tail -f /var/log/app/server.log"]
    ```

> 💡 **Interviewer Focus:** Decoupled platform services patterns, shared resource namespaces (network loopback and volume mounts), and sidecar lifecycle management.

</details>

<hr/>

### ❓ Q70. **How do you prevent resource starvation in Kubernetes?**

<details>
<summary><b>👀 Show Answer</b></summary>

Set explicit resource bounds in container manifests:
*   **`requests`**: The minimum CPU and Memory resources the scheduler guarantees to allocate.
*   **`limits`**: The maximum CPU and Memory resources the container is allowed to consume. If a container exceeds memory limits, it is terminated with an Out-of-Memory (`OOMKilled`) error.
*   **Kubernetes Resources Manifest Example:**
    ```yaml
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"      # 250 millicores (0.25 vCPU)
      limits:
        memory: "512Mi"  # Hard limit (killed if exceeded)
        cpu: "500m"      # Throttled if exceeded
    ```

> 💡 **Interviewer Focus:** Enforcing limits to protect other workloads sharing the same node, understanding the difference between CPU throttling and memory termination, and selecting request bounds based on app resource baselines.

</details>

<hr/>

### ❓ Q71. **What is the difference between Ansible push execution vs pull execution?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Push Mode** (Default): Ansible runs on a control machine, logging into target nodes via SSH to execute commands (agentless).
- **Pull Mode** (`ansible-pull`): Nodes run a cron utility that regularly pulls playbooks from a central Git repository and executes them locally on the node (scalable for thousands of hosts).

> 💡 **Interviewer Focus:** Configuration management execution modes.

</details>

<hr/>

### ❓ Q72. **Explain the concept of Policy as Code.**

<details>
<summary><b>👀 Show Answer</b></summary>

Policy as Code uses configuration code files to define and enforce security, operational compliance, and access rules (e.g., using **Open Policy Agent (OPA)** or **Kyverno**). Rules are checked automatically during PR reviews or inside admission controllers.

> 💡 **Interviewer Focus:** Enforcing organizational compliance rules in CI/CD.

</details>

<hr/>

### ❓ Q73. **How does DNS resolution work inside a Kubernetes cluster?**

<details>
<summary><b>👀 Show Answer</b></summary>

Kubernetes runs a cluster-internal DNS service (**CoreDNS**). When a pod attempts to resolve a domain name (like `database-service`), it queries CoreDNS, which resolves the name to the stable IP address of the corresponding Kubernetes Service.

> 💡 **Interviewer Focus:** Service names resolution paths.

</details>

<hr/>

### ❓ Q74. **What is a deployment window and why are organizations moving away from it?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Deployment Window:** Scheduled off-peak hours (e.g. Sundays at 2 AM) when deployments are allowed, designed to minimize user impact on failure.
- **Move away:** Modern organizations use automated testing, canary rollouts, and blue-green deployments to release updates continuously during business hours with zero downtime and low risk.

> 💡 **Interviewer Focus:** Progressive delivery benefits.

</details>

<hr/>

### ❓ Q75. **What is the difference between a synthetic test and a real-user monitoring (RUM) metric?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Synthetic Testing:** Automated scripts run scheduled checks simulating user paths from test servers, generating baseline latency and functionality metrics under controlled conditions.
- **Real User Monitoring (RUM):** Captures actual performance and errors experienced by real clients loading the site on their local devices in real-time.

> 💡 **Interviewer Focus:** User experience validation.

</details>

<hr/>

## 🟣 Expert Level

### ❓ Q76. **Explain SRE Indicators: SLA, SLO, and SLI, and how to calculate Error Budgets.**

<details>
<summary><b>👀 Show Answer</b></summary>

These concepts form the foundation of Site Reliability Engineering (SRE):
- **SLI (Service Level Indicator):** A quantitative measure of a service's performance in real-time.
  - *Example:* The percentage of successful HTTP requests (status < 500) over a 5-minute window.
- **SLO (Service Level Objective):** A target reliability metric defined for the SLI.
  - *Example:* "HTTP request success rate (SLI) must be $\ge 99.9\%$ over a rolling 30-day period."
- **SLA (Service Level Agreement):** A legal agreement with customers detailing consequences (financial refunds) if the SLO target is not met.
- **Error Budget:** The allowable room for failure, calculated as $100\% - \text{SLO}$.
  - For a $99.9\%$ SLO, the error budget is $0.1\%$.
  - If a service receives 1,000,000 requests in a month, the error budget allows exactly 1,000 failed requests.
  - If the budget is exhausted, further deployments are frozen, and engineering focus shifts entirely to stability improvements.

> 💡 **Interviewer Focus:** How error budgets align incentives between Dev (speed of releases) and Ops (system stability).

</details>

<hr/>

### ❓ Q77. **How does the Expand-and-Contract (Parallel Change) pattern handle database migrations in CD?**

<details>
<summary><b>👀 Show Answer</b></summary>

When deploying updates with database schema changes (like renaming a column), you cannot run the schema update and code update at the exact same millisecond. Doing so leads to downtime. The **Expand-and-Contract** pattern solves this:
1. **Phase 1: Expand (Add):**
   - Add the new field/column to the database (leaving the old field active).
   - Deploy version 2 of the application code, which writes to *both* old and new fields, but reads only from the old field.
2. **Phase 2: Transition (Backfill):**
   - Run a background script/job to copy historical data from the old field to the new field for old records.
3. **Phase 3: Switch:**
   - Deploy version 3 of the application code, which reads and writes *only* to the new field.
4. **Phase 4: Contract (Remove):**
   - Remove/drop the old field/column from the database schema.
- **MERN / MongoDB Example:**
  - In MongoDB, if we split a user's full `name` string into `firstName` and `lastName`:
  - **Expand:** Add `firstName` and `lastName` fields. Update Express API schema to write to both `name` and `firstName`/`lastName` on user sign-ups.
  - **Backfill:** Run a script to split the `name` field for existing documents and populate `firstName`/`lastName`.
  - **Switch:** Update Express API to query and read from `firstName`/`lastName` exclusively.
  - **Contract:** Run `$unset` to remove the `name` field from user documents, saving storage space.

```
[Phase 1: Expand]  ──> [Phase 2: Backfill] ──> [Phase 3: Switch] ──> [Phase 4: Contract]
Write to Old & New       Migrate old rows      Write/Read only New      Drop old fields
```

> 💡 **Interviewer Focus:** Zero-downtime database release strategies, backward compatibility of APIs, and data consistency during transitions.

</details>

<hr/>

### ❓ Q78. **Explain how Taints, Tolerations, Affinity, and Anti-Affinity interact during Kubernetes scheduling.**

<details>
<summary><b>👀 Show Answer</b></summary>

These rules guide the Kubernetes Scheduler on which nodes are allowed or forced to run specific pods:
*   **Taints & Tolerations (Node-Centric):**
    *   **Taint:** Applied to a *node* to repel pods (e.g., `gpu=true:NoSchedule`). Pods will not run on this node unless they explicitly tolerate the taint.
    *   **Toleration:** Applied to a *pod* allowing it to schedule on a tainted node (e.g. running GPU jobs on GPU nodes).
*   **Node Affinity (Pod-Centric):**
    *   Commands the scheduler to place a pod on specific nodes based on labels (e.g., "run this pod on nodes in zone `us-east-1a`").
*   **Pod Anti-Affinity (Pod-to-Pod Relations):**
    *   Prevents pods of the same type from scheduling on the same node. Essential for ensuring high availability.
*   **YAML Manifest Example (Toleration & Anti-Affinity):**
    ```yaml
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values: [ express-api ]
            topologyKey: "kubernetes.io/hostname"
      tolerations:
      - key: "workload-type"
        operator: "Equal"
        value: "production"
        effect: "NoSchedule"
      containers:
      - name: express-api
        image: express-api:v1
    ```

> 💡 **Interviewer Focus:** Designing cluster placement topologies to prevent co-locating all replica containers on the same physical VM host or rack.

</details>

<hr/>

### ❓ Q79. **How do you debug high network latency between microservices inside a Kubernetes cluster?**

<details>
<summary><b>👀 Show Answer</b></summary>

Debugging internal cluster networking requires analyzing layers from container to overlay network:
1. **Observe and Trace:** Consult distributed traces (e.g., Jaeger) to isolate which service hop has high latency. Check metric dashboards for CPU throttling on target pods (which delays connection processing).
2. **Inspect DNS Resolution:** Slow DNS lookups can mimic network latency. Test if lookups are slow by checking CoreDNS logs, metric queries, or resolving services via IP directly.
3. **Validate CNI and Overlay Network:**
   - The CNI (like Calico or Flannel) manages the virtual overlay network. Check for packet drops using tools like `iperf` or `mtr` between pods on different nodes.
   - Inspect MTU size mismatches, which cause IP fragmentation and packet drops.
4. **Investigate Conntrack Table Limits:**
   - Linux tracks TCP connections in a conntrack table. Under extreme traffic, the table can fill up, causing the kernel to drop packets. Check conntrack metrics on host VMs using `sysctl net.netfilter.nf_conntrack_count`.
5. **Analyze Service Mesh Routing:** If using a service mesh (Istio), inspect sidecar proxy logs (Envoy) to verify if routing rules, retries, or mutual TLS handshakes are adding overhead.

> 💡 **Interviewer Focus:** conntrack table limits, CNI overlay network overhead, and CoreDNS lookups optimization (ndots configuration).

</details>

<hr/>

### ❓ Q80. **Discuss security isolation models in container runtimes: runc vs. gVisor vs. Kata Containers.**

<details>
<summary><b>👀 Show Answer</b></summary>

Standard containers share the host kernel, which presents security risks if a container process escalates privileges (container escape).
- **runc (Standard):**
  - The default container runtime. Relies on standard Linux kernel namespaces and cgroups for isolation.
  - Pros: High performance, near-zero virtualization overhead.
  - Cons: Weakest isolation. If a vulnerability is found in the shared host kernel, the container can compromise the host.
- **gVisor (User-Space Kernel):**
  - Created by Google. It implements a user-space kernel (written in Go) called Sentry that intercepts and handles system calls from the container.
  - The container cannot talk to the host kernel directly.
  - Pros: High security isolation, fast startup.
  - Cons: Performance overhead for system-call heavy workloads.
- **Kata Containers (Micro-VMs):**
  - Runs each pod inside a dedicated, lightweight virtual machine (using a hypervisor like QEMU or Firecracker).
  - Has its own separate guest kernel.
  - Pros: Strongest hardware-level isolation (safest for multi-tenant SaaS environments).
  - Cons: Slightly slower startup and higher memory overhead compared to standard containers.

> 💡 **Interviewer Focus:** Trade-off decisions when running untrusted user code in multi-tenant cloud platforms.

</details>

<hr/>

### ❓ Q81. **Discuss GitOps pull-based vs. push-based CD reconciliation mechanisms.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Push-Based CD:** The CI pipeline (e.g. Jenkins runner) executes a script that pushes commands directly to the cluster (`kubectl apply`).
  - *Risk:* CI runners require admin access keys to the cluster. If the CI server is compromised, attackers gain full access to the production cluster.
- **Pull-Based CD:** A GitOps controller runs inside the cluster, polling Git and pulling configurations to apply locally.
  - *Benefit:* The cluster does not expose external API keys. All credentials stay inside the cluster boundary, which is significantly more secure.

> 💡 **Interviewer Focus:** Securing deployment paths and cluster credentials boundary optimization.

</details>

<hr/>

### ❓ Q82. **How do you design and execute a Chaos Engineering experiment safely in production?**

<details>
<summary><b>👀 Show Answer</b></summary>

1. **Define Steady State:** Measure normal metrics baseline (error rates, CPU, latency).
2. **Formulate Hypothesis:** "If node AZ-1 is terminated, Route 53 will redirect traffic in under 60 seconds with no data loss."
3. **Minimize Blast Radius:** Inject the fault into a small subset of requests or users first.
4. **Automated Stop Mechanism (Kill Switch):** Configure scripts to automatically abort the experiment and restore nodes immediately if baseline metrics degrade beyond set thresholds.

> 💡 **Interviewer Focus:** Operational guardrails and minimizing blast radius configurations during production testing.

</details>

<hr/>

### ❓ Q83. **How do you design high-availability disaster recovery for stateful Kubernetes workloads?**

<details>
<summary><b>👀 Show Answer</b></summary>

For stateful applications (like databases running on Kubernetes):
- Use CSI drivers supporting **multi-zone volume replication** (such as Portworx or Ceph/Rook).
- Schedule database pods across AZs using Pod Anti-Affinity.
- Configure automatic snapshot backups written to S3.
- Use tools like Velero to backup Kubernetes manifest configurations and persistent volume states to external object stores for fast restoration.

> 💡 **Interviewer Focus:** Persistent volumes synchronization challenges across different physical zones.

</details>

<hr/>

### ❓ Q84. **Explain dynamic configuration injection at runtime without rebuilding container images or restarting service processes.**

<details>
<summary><b>👀 Show Answer</b></summary>

1. Mount configuration files dynamically inside containers using Kubernetes ConfigMaps.
2. If using standard volume mounts, updates to ConfigMaps are eventually synced into the container by the kubelet.
3. Configure the application process to run a file-system watcher (using fsnotify or chokidar). When the mounted ConfigMap file updates, the application triggers a configuration reload in-memory without restarting.

> 💡 **Interviewer Focus:** Dynamically syncing mounted configurations vs environment variables (which require process restarts to update).

</details>

<hr/>

### ❓ Q85. **How do you build a secure DevSecOps pipeline enforcing Policy-as-Code?**

<details>
<summary><b>👀 Show Answer</b></summary>

1. Define policies using standard declarative languages (Rego for OPA).
2. **CI phase:** Use `conftest` to evaluate Terraform configurations or Kubernetes manifests against security rules (e.g. denying configurations that run containers in privileged mode).
3. **CD phase:** Configure a validating admission webhook (OPA Gatekeeper) inside the Kubernetes API server to block applying any resource manifests that violate the security policies.

> 💡 **Interviewer Focus:** Automating compliance validation boundaries from code checkout to cluster runtimes.

</details>

<hr/>

### ❓ Q86. **Explain what container image layer caching is and how to design Dockerfiles to optimize it.**

<details>
<summary><b>👀 Show Answer</b></summary>

Docker builds images sequentially, caching each layer generated by instructions like `RUN` or `COPY`. If a layer is unmodified, Docker uses the cached version.
- **Optimization:** Order Dockerfile instructions from least frequently changed to most frequently changed.
- Place dependency install steps (`COPY package*.json` and `RUN npm ci`) *before* copying application source code. This ensures changes to source files do not invalidate the cached dependency layer, saving build times.
- **Optimal MERN Node.js backend Dockerfile structure:**
  ```dockerfile
  FROM node:20-alpine
  WORKDIR /usr/src/app
  # Copy package configuration first to cache npm installs
  COPY package*.json ./
  RUN npm ci --only=production
  # Copy the rest of the source code (changes frequently)
  COPY . .
  EXPOSE 5000
  CMD ["node", "server.js"]
  ```

> 💡 **Interviewer Focus:** Reducing build times in pipelines by optimizing cache hit ratios.

</details>

<hr/>

### ❓ Q87. **How does standard Linux namespaces and cgroups isolate container processes on the host kernel?**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Namespaces:** Provides process-level isolation. They restrict what a process can see:
  - `pid`: Isolates process IDs.
  - `net`: Isolates network interfaces.
  - `mnt`: Isolates mount points.
  - `uts`: Isolates hostnames.
- **Control Groups (cgroups):** Enforce physical resource boundaries. They restrict what a process can *consume* (CPU, Memory, Disk I/O limits).

> 💡 **Interviewer Focus:** OS-level container isolation mechanics.

</details>

<hr/>

### ❓ Q88. **What is Git cherry-pick and how does it affect branch history?**

<details>
<summary><b>👀 Show Answer</b></summary>

`git cherry-pick <commit-hash>` copies the changes from a specific commit on another branch and applies them as a new commit on the current branch.
- **History Impact:** It duplicates the commit changes, generating a new commit hash on the current branch. This can cause merge conflicts later if you merge the original source branch.

> 💡 **Interviewer Focus:** Porting hotfixes across branches.

</details>

<hr/>

### ❓ Q89. **What is dynamic path routing in Nginx?**

<details>
<summary><b>👀 Show Answer</b></summary>

Dynamic path routing forwards incoming requests to different backend service pools based on the request URL path matching rules.
*   **Production Nginx Server Block Example (React frontend SPA & Node.js API):**
    ```nginx
    server {
        listen 80;
        server_name myapp.com;

        # 1. Route API requests to Express backend containers
        location /api/ {
            proxy_pass http://express-api-service:5000/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # 2. Route root path to React SPA build assets
        location / {
            root /usr/share/nginx/html;
            index index.html;
            try_files $uri $uri/ /index.html; # fallback routing for React router
        }
    }
    ```

> 💡 **Interviewer Focus:** Reverse proxy configurations, WebSocket upgrades configuration (`Upgrade` / `Connection`), proxy headers mapping, and SPA fallback rules.

</details>

<hr/>

### ❓ Q90. **Explain how Kubernetes Service topology routing works.**

<details>
<summary><b>👀 Show Answer</b></summary>

Service topology routing allows directing network traffic to endpoints based on the cluster's network topology (e.g. routing traffic preferentially to pods running on the same node or within the same AZ to minimize network latency and egress costs).

> 💡 **Interviewer Focus:** Network latency and egress cost optimizations.

</details>

<hr/>

### ❓ Q91. **What is Git tag and how is it used in deployment pipelines?**

<details>
<summary><b>👀 Show Answer</b></summary>

A Git tag is a static pointer to a specific commit in history. It is used to mark release milestones (e.g. `v1.2.0`). In CI/CD, pushing a git tag often acts as the trigger to run production deployment jobs.

> 💡 **Interviewer Focus:** Release automation triggers.

</details>

<hr/>

### ❓ Q92. **How does Nginx handle Gzip compression and buffering?**

<details>
<summary><b>👀 Show Answer</b></summary>

Nginx compresses HTTP responses on-the-fly using gzip to reduce payload transfer sizes. It buffers responses from backend application servers, preventing slow client connections from tying up backend resources.

> 💡 **Interviewer Focus:** Page speed optimization configurations.

</details>

<hr/>

### ❓ Q93. **What is Kubernetes taint-based eviction?**

<details>
<summary><b>👀 Show Answer</b></summary>

If a node becomes unhealthy (e.g. network partition or out of memory), the control plane automatically taints the node (e.g. `node.kubernetes.io/unreachable`). Pods on the node that do not tolerate this taint are automatically evicted and rescheduled to healthy nodes.

> 💡 **Interviewer Focus:** Cluster self-healing under hardware failures.

</details>

<hr/>

### ❓ Q94. **Explain how Jenkins pipelines can be configured for parallel stage execution.**

<details>
<summary><b>👀 Show Answer</b></summary>

Use the `parallel` directive inside declarative pipelines:

```groovy
stage('Test') {
    parallel {
        stage('Unit Tests') { steps { sh 'npm test' } }
        stage('Linter') { steps { sh 'npm run lint' } }
    }
}
```

This runs both stages simultaneously on separate executors, reducing total pipeline execution times.

> 💡 **Interviewer Focus:** Pipeline optimization.

</details>

<hr/>

### ❓ Q95. **What is a sidecar proxy injection mechanism?**

<details>
<summary><b>👀 Show Answer</b></summary>

In Service Meshes (like Istio), a mutating admission webhook intercepts Pod creation requests. It automatically modifies the pod manifest, adding the sidecar proxy container definition (Envoy) and redirecting local pod iptables traffic through the proxy.

> 💡 **Interviewer Focus:** Service mesh configuration injection.

</details>

<hr/>

### ❓ Q96. **How do you handle secrets rotation in Kubernetes applications without causing downtime?**

<details>
<summary><b>👀 Show Answer</b></summary>

1.  **Mounted Secrets File Watcher:** Instead of loading secrets as environment variables (which require pod restarts to update), mount the Secret as a file volume. Kubernetes automatically updates the mounted files when the secret changes. The Node.js application can watch for file changes using `fs.watch()` or `chokidar` and hot-reload keys in-memory.
2.  **Secret File Watcher Example (Node.js):**
    ```javascript
    const fs = require('fs');
    const path = '/etc/secrets/mongo-uri';
    
    let dbConnectionUri = fs.readFileSync(path, 'utf8').trim();
    
    // Watch for file modifications (Kubernetes updates symlinks when secret rotates)
    fs.watch(path, (event) => {
      if (event === 'change') {
        dbConnectionUri = fs.readFileSync(path, 'utf8').trim();
        console.log("Secret rotated! Re-initiating DB connections pool...");
        reconnectDatabase(dbConnectionUri);
      }
    });
    ```
3.  **Reloader Operator:** Use community tools like Stakater's **Reloader** operator, which monitors ConfigMaps/Secrets changes and triggers rolling restarts of Deployments automatically.

> 💡 **Interviewer Focus:** Zero-downtime credentials upgrades, environment variable limitations (requires process restart) vs file mount watchers.

</details>

<hr/>

### ❓ Q97. **Explain the purpose of the Prometheus Alertmanager.**

<details>
<summary><b>👀 Show Answer</b></summary>

Alertmanager processes alerts triggered by Prometheus rules. It deduplicates alerts, groups matching warnings, silences notifications during maintenance windows, and routes them to destinations (Slack, PagerDuty, Email).

> 💡 **Interviewer Focus:** Notification fatigue prevention.

</details>

<hr/>

### ❓ Q98. **What is the difference between deployment replicas and daemonsets?**

<details>
<summary><b>👀 Show Answer</b></summary>

*   **ReplicaSet (Deployment):** Runs a specified number of pods across the cluster, scheduling them to nodes based on resource availability.
*   **DaemonSet:** Runs exactly **one** copy of a pod on every node in the cluster (e.g., for logging agents or monitoring tools).
*   **Kubernetes DaemonSet YAML Manifest Example (FluentBit Log Collector):**
    ```yaml
    apiVersion: apps/v1
    kind: DaemonSet
    metadata:
      name: fluent-bit-collector
    spec:
      selector:
        matchLabels:
          name: fluent-bit
      template:
        metadata:
          labels:
            name: fluent-bit
        spec:
          containers:
          - name: fluent-bit
            image: fluent/fluent-bit:2.0
            volumeMounts:
            - name: varlog
              mountPath: /var/log
          volumes:
          - name: varlog
            hostPath:
              path: /var/log
    ```

> 💡 **Interviewer Focus:** Pod scheduling models, use cases for DaemonSets (logging, metrics agent, ingress proxy), and tolerations to run daemon pods on master/tainted nodes.

</details>

<hr/>

### ❓ Q99. **How do you troubleshoot a pod stuck in `Pending` state?**

<details>
<summary><b>👀 Show Answer</b></summary>

Run `kubectl describe pod <pod-name>` to view scheduler events. Common causes:
- Insufficient CPU or Memory resources on cluster nodes.
- Unmet taints, tolerations, or affinity rules.
- Persistent Volume Claims (PVC) failing to bind.

> 💡 **Interviewer Focus:** Cluster capacity and scheduler constraints diagnosis.

</details>

<hr/>

### ❓ Q100. **Explain how zero-downtime rolling updates update active users connections in Kubernetes.**

<details>
<summary><b>👀 Show Answer</b></summary>

1. The deployment creates a new pod (v2).
2. Once the v2 readiness probe passes, it is added to the Service endpoint list.
3. The load balancer starts routing new traffic to v2.
4. The old pod (v1) is sent a `SIGTERM` signal.
5. The Service immediately stops routing new connections to v1.
6. The application on v1 processes active concurrent requests (graceful shutdown) before exiting, ensuring zero connection drops.

> 💡 **Interviewer Focus:** Graceful shutdown lifecycle (`preStop` hooks and SIGTERM handling).

</details>

<hr/>

### 🧭 Navigation

| ⬅️ Previous | 🏠 Index | ➡️ Next |
| :--- | :---: | ---: |
| [⬅️ AWS](./10_AWS.md) | [Home](./00_Index.md) | [➡️ JS Output Questions](./12_JS_Output_Questions.md) |
