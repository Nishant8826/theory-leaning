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

> 💡 **Interviewer Focus:** Ensure the candidate highlights DevOps as a cultural mindset, not just a set of tools (like Docker or Jenkins), and explains the feedback loop.

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

Infrastructure as Code (IaC) is the management of infrastructure (networks, virtual machines, load balancers, connection topologies) in a descriptive model, using configuration files rather than manual interactive configuration tools.
- **Benefits:** Prevents configuration drift, permits versioning via Git, and automates environment creation.
- **Tools:** Terraform, AWS CloudFormation, Ansible.

> 💡 **Interviewer Focus:** The automation capabilities and auditable history of cloud configuration.

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

A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble a Docker Image.
- **`FROM`**: Sets the base image (e.g., `FROM node:18-alpine`).
- **`WORKDIR`**: Defines the working directory inside the container.
- **`COPY`**: Copies files from the host machine to the container.
- **`RUN`**: Executes commands during the image build process (e.g., `RUN npm install`).
- **`EXPOSE`**: Documents the port the container listens on at runtime.
- **`CMD`**: Specifies the default command to execute when the container starts.

> 💡 **Interviewer Focus:** Distinguishing `RUN` (build time execution) from `CMD` (runtime execution).

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

> 💡 **Interviewer Focus:** Point out that monitoring tells you *that* a system is broken, while logging helps you figure out *why* it broke.

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

- **`Git Merge`:**
  - Combines two branches by creating a new "merge commit" in the history.
  - Preserves the historical timeline of when commits were actually made, but can result in a messy git history graph.
- **`Git Rebase`:**
  - Re-applies commits from your branch on top of another branch.
  - Rewrites history to create a clean, linear sequence of commits.
  - **Rule:** Never rebase branches that have been pushed to public repositories, as it rewrites commits that others are collaborating on.

> 💡 **Interviewer Focus:** Safety constraints of rebasing and avoiding merge conflicts in public branches.

</details>

<hr/>

### ❓ Q11. **Explain the role of the Jenkins server in CI/CD.**

<details>
<summary><b>👀 Show Answer</b></summary>

Jenkins is an open-source automation server. It acts as the pipeline runner, executing workflow jobs defined in code (Jenkinsfile) to pull code from Git repositories, trigger builds, run test suites, build Docker containers, and handle deployments.

> 💡 **Interviewer Focus:** Understanding Jenkins agent nodes, master-agent architecture, and plugin dependencies management.

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
1. Creates a new branch named `<branch>` from the current commit.
2. Switches (checks out) the workspace to that newly created branch.

> 💡 **Interviewer Focus:** Basic Git CLI mechanics.

</details>

<hr/>

### ❓ Q15. **What is SSH and why is it used?**

<details>
<summary><b>👀 Show Answer</b></summary>

SSH (Secure Shell) is a cryptographic network protocol used to secure remote command-line login sessions, shell executions, and file transfers over insecure networks. It relies on public/private key pairs for authentication.

> 💡 **Interviewer Focus:** Key pair management and blocking password-based logins.

</details>

<hr/>

### ❓ Q16. **What is Nginx?**

<details>
<summary><b>👀 Show Answer</b></summary>

Nginx is a high-performance web server, reverse proxy, load balancer, and HTTP cache. It utilizes an asynchronous event-driven architecture, enabling it to process thousands of concurrent connections with minimal memory usage.

> 💡 **Interviewer Focus:** Web infrastructure layouts.

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

It builds a Docker image from the Dockerfile located in the current directory (`.`) and tags (`-t`) the resulting image with the name `app`.

> 💡 **Interviewer Focus:** Basic Docker CLI mechanics.

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

They are components of asymmetric encryption:
- **Public Key:** Shared publicly. Used to encrypt data or verify digital signatures.
- **Private Key:** Kept strictly secret by the owner. Used to decrypt data encrypted by the public key or generate digital signatures.

> 💡 **Interviewer Focus:** Secure key pairs management.

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

Multi-stage builds allow developers to use multiple `FROM` statements in a single Dockerfile, creating separate temporary build stages to compile code, and copying only the final output binary to a minimal runner stage.
- **Why it is useful:** It keeps the final production Docker image extremely small by excluding build-time tools, compiler engines, and dependencies (like SDKs, compiler utilities, or source code files).

```dockerfile
# Stage 1: Build compilation
FROM golang:1.20 AS builder
WORKDIR /src
COPY . .
RUN go build -o myapp

# Stage 2: Final runner image
FROM alpine:latest
WORKDIR /app
# Copy only the compiled binary from the builder stage
COPY --from=builder /src/myapp .
CMD ["./myapp"]
```

> 💡 **Interviewer Focus:** Image optimization and reducing the security attack surface by keeping the production runtime environment minimal.

</details>

<hr/>

### ❓ Q28. **Explain the difference between Blue-Green and Rolling Deployments.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Rolling Deployment:**
  - Slowly replaces instances of the old application version (v1) with the new version (v2) one by one or in small batches.
  - Pros: Requires no extra infrastructure capacity.
  - Cons: Slow rollouts; during deployment, both v1 and v2 live in production concurrently (can cause session issues). Rollbacks require redeploying.
- **Blue-Green Deployment:**
  - Provisions a complete duplicate environment (Green) running the new version next to the production environment (Blue) running the old version.
  - Once Green passes all tests, traffic is routed instantly from Blue to Green at the load balancer or DNS level.
  - Pros: Instant switch; rollback is as simple as flipping the router switch back to Blue if Green fails.
  - Cons: Doubles infrastructure costs during deployment.

> 💡 **Interviewer Focus:** Managing data schema compatibilities during transition phases and cost implications.

</details>

<hr/>

### ❓ Q29. **How does Kubernetes manage containers? Explain Pods, Deployments, and Services.**

<details>
<summary><b>👀 Show Answer</b></summary>

- **Pod:** The smallest deployable unit in Kubernetes. Represents a wrapper wrapper containing one or more containers sharing network and storage resources.
- **Deployment:** Declares the desired state of pods (e.g., "run exactly 5 replicas of app container v2"). It manages creating, updating, and deleting pods automatically to maintain this state.
- **Service:** An abstraction that defines a logical set of pods and a policy to access them. Since pods are ephemeral and their IP addresses change constantly, the Service provides a stable, permanent IP address and DNS name to route traffic to the pods.

> 💡 **Interviewer Focus:** Understanding that Pods are ephemeral, and Services act as internal load balancers to route traffic to them.

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

> 💡 **Interviewer Focus:** SSL termination configurations and headers injection (like `X-Forwarded-For`) to pass the client's actual IP to the backend.

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

An Ingress Controller is a specialized proxy (e.g. Nginx, Traefik) that runs inside the Kubernetes cluster. It implements Ingress resources, routing external HTTP/HTTPS traffic to internal Kubernetes Services based on URL paths or host domain names.

> 💡 **Interviewer Focus:** HTTP routing ingress interfaces.

</details>

<hr/>

### ❓ Q37. **What is a Jenkinsfile?**

<details>
<summary><b>👀 Show Answer</b></summary>

A Jenkinsfile is a text configuration file that defines a Jenkins build pipeline as code. It contains the sequence of stages, steps, variables, and environments required to compile, test, package, and deploy code, stored inside the Git repository.

> 💡 **Interviewer Focus:** Pipeline-as-code management.

</details>

<hr/>

### ❓ Q38. **Explain the purpose of health checks in a containerized environment.**

<details>
<summary><b>👀 Show Answer</b></summary>

Health checks verify container status dynamically:
- **Liveness Probes:** Check if a container is running. If it fails, the system restarts the container.
- **Readiness Probes:** Check if the container is ready to accept user network traffic. If it fails, the container is removed from target load balancer pools.

> 💡 **Interviewer Focus:** Self-healing configurations.

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

- **Terraform (Infrastructure Provisioning):** Declarative tool designed to build and manage cloud infrastructure elements (VPCs, database instances, DNS entries) and track their states.
- **Ansible (Configuration Management):** Procedural/hybrid tool designed to configure software, patch packages, and manage files *inside* existing servers via SSH (agentless).

> 💡 **Interviewer Focus:** Target orchestration areas (IaC provisioning vs host configuration).

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
   - GitHub Actions / GitLab CI triggers the pipeline.
2. **Build and Test Stage:**
   - Run code linter and security scanner (e.g., SonarQube, Snyk).
   - Execute Unit Tests.
   - Compile code and build a Docker image using a multi-stage Dockerfile.
   - Run vulnerability scans on the Docker image (e.g., using Trivy).
3. **Artifact Registry Stage:**
   - Push the verified Docker image to a private registry (like AWS ECR or Docker Hub) tagged with the unique Git commit hash.
4. **Staging / QA Deployment:**
   - Deploy the container image to a Staging environment.
   - Run automated Integration and End-to-End (E2E) testing suites (e.g., Cypress/Playwright).
5. **Production Deployment (CD):**
   - Deploy to production using a GitOps controller (like ArgoCD) or via blue-green deployment.
   - If using Blue-Green, deploy the new image to the Green environment, validate liveness/readiness probes, and flip the ALB listener rule to route traffic to Green.
6. **Post-Deployment Verification:**
   - Monitor error logs (e.g., via Sentry) and resource metrics (Prometheus). If error counts spike, trigger automatic rollback.

> 💡 **Interviewer Focus:** Guardrails, security scans at every stage, unique tagging of images, and automated rollbacks on failure.

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
- **Secure Management:**
  - Enable **KMS encryption at rest** for Kubernetes etcd database.
  - Use external secrets providers (like HashiCorp Vault, AWS Secrets Manager) coupled with the **External Secrets Operator (ESO)** to inject parameters securely.
  - Retrieve secrets dynamically using Vault sidecar containers, keeping values strictly in-memory.

> 💡 **Interviewer Focus:** Eliminating base64 encoding vulnerabilities and securing etcd storage.

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

> 💡 **Interviewer Focus:** Pipeline configuration structure.

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

> 💡 **Interviewer Focus:** Decoupled platform services patterns.

</details>

<hr/>

### ❓ Q70. **How do you prevent resource starvation in Kubernetes?**

<details>
<summary><b>👀 Show Answer</b></summary>

Set explicit resource bounds in container manifests:
- **`requests`**: The minimum CPU and Memory resources the scheduler guarantees to allocate.
- **`limits`**: The maximum CPU and Memory resources the container is allowed to consume. If a container exceeds memory limits, it is terminated with an Out-of-Memory (`OOMKilled`) error.

> 💡 **Interviewer Focus:** Enforcing limits to protect other workloads sharing the same node.

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
   - Add the new column to the database (leaving the old column active).
   - Deploy version 2 of the application code, which writes to *both* old and new columns, but reads only from the old column.
2. **Phase 2: Transition (Backfill):**
   - Run a background script to copy historical data from the old column to the new column for old records.
3. **Phase 3: Switch:**
   - Deploy version 3 of the application code, which reads and writes *only* to the new column.
4. **Phase 4: Contract (Remove):**
   - Remove the old column from the database.

```
[Phase 1: Expand]  ──> [Phase 2: Backfill] ──> [Phase 3: Switch] ──> [Phase 4: Contract]
Write to Old & New       Migrate old rows      Write/Read only New      Drop old columns
```

> 💡 **Interviewer Focus:** Zero-downtime database release strategies and backward compatibility.

</details>

<hr/>

### ❓ Q78. **Explain how Taints, Tolerations, Affinity, and Anti-Affinity interact during Kubernetes scheduling.**

<details>
<summary><b>👀 Show Answer</b></summary>

These rules guide the Kubernetes Scheduler on which nodes are allowed or forced to run specific pods:
- **Taints & Tolerations (Node-Centric):**
  - **Taint:** Applied to a *node* to repel pods (e.g., `gpu=true:NoSchedule`). Pods will not run on this node unless they explicitly tolerate the taint.
  - **Toleration:** Applied to a *pod* allowing it to schedule on a tainted node (e.g., a GPU-heavy training job tolerates the GPU taint).
- **Node Affinity (Pod-Centric):**
  - Commands the scheduler to place a pod on specific nodes based on labels (e.g., "run this pod on nodes in zone `us-east-1a`"). Can be hard (`requiredDuringSchedulingIgnoredDuringExecution`) or soft (`preferredDuringScheduling...`).
- **Pod Anti-Affinity (Pod-to-Pod Relations):**
  - Prevents pods of the same type from scheduling on the same node (e.g., "do not run two replicas of the web-app pod on the same physical VM node"). Essential for ensuring high availability during server failures.

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
- Place dependency install steps (`COPY package.json` and `RUN npm install`) *before* copying application source code. This ensures changes to source files do not invalidate the cached dependency layer, saving build times.

```dockerfile
# Optimal ordering:
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
```

> 💡 **Interviewer Focus:** Reducing build times in pipelines.

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

Dynamic path routing forwards incoming requests to different backend service pools based on the request URL path matching rules:

```nginx
location /api/ {
    proxy_pass http://api_backend_upstream;
}
location /static/ {
    root /var/www/static_assets;
}
```

> 💡 **Interviewer Focus:** Reverse proxy configurations.

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

1. Retrieve secrets dynamically from a provider (Vault) during execution instead of caching them during startup.
2. If using mounted secrets, the application must watch for file updates (using fsnotify) and hot-reload keys in-memory on modifications, keeping active connections alive.

> 💡 **Interviewer Focus:** Zero-downtime credentials upgrades.

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

- **ReplicaSet (Deployment):** Runs a specified number of pods across the cluster, scheduling them to nodes based on resource availability.
- **DaemonSet:** Runs exactly **one** copy of a pod on every node in the cluster (e.g., for logging agents or monitoring tools).

> 💡 **Interviewer Focus:** Pod scheduling models.

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
