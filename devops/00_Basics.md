# DevOps Basics

## 1. What is DevOps?

### Definition
**DevOps** is a combination of cultural philosophies, practices, and tools that increases an organization's ability to deliver applications and services at high velocity. It is not just a job title or a tool; it is a mindset of collaboration between **Development (Dev)** and **Operations (Ops)** teams.

### The Purpose of DevOps
In traditional software development, developers would write code and "throw it over the wall" to the operations team to deploy and manage. This often led to friction, slow releases, and manual errors. DevOps breaks down these silos.

*   **Development:** Focuses on creating new features and fixing bugs.
*   **Operations:** Focuses on stability, security, and maintenance of the infrastructure.

DevOps integrates these two, ensuring that everyone is responsible for the entire lifecycle of the software—from design to production support.

### Why DevOps Matters
Modern software companies need to react to market changes quickly. DevOps allows them to:
*   **Faster Delivery:** Release features to customers multiple times a day instead of once every few months.
*   **Automation:** Reduce manual work and human error in testing, deployment, and infrastructure setup.
*   **Collaboration:** Improve communication and shared responsibility between teams.
*   **Scalability:** Manage complex or changing systems efficiently with minimal risk.
*   **Reliability:** Ensure quality through automated testing and continuous monitoring.

---

## 2. Roles and Responsibilities in DevOps

DevOps is a team effort, and several specialized roles help manage different parts of the pipeline.

### DevOps Engineer
The "bridge" between Dev and Ops.
*   **Responsibilities:** Automating the software development lifecycle (SDLC), managing CI/CD pipelines, and ensuring smooth deployments.
*   **Skills:** Scripting, CI/CD tools, Cloud knowledge.
*   **Tools:** Jenkins, GitLab CI, Git.

### Site Reliability Engineer (SRE)
Originated at Google, SREs apply software engineering principles to operations tasks.
*   **Responsibilities:** Ensuring system uptime, performance, and reliability. They focus on "Service Level Objectives" (SLOs) and "Error Budgets."
*   **Skills:** System architecture, coding, problem-solving under pressure.
*   **Tools:** Prometheus, Grafana, Kubernetes.

### Cloud Engineer
Focuses on the infrastructure provided by cloud vendors.
*   **Responsibilities:** Designing and maintaining cloud-based systems, cost optimization, and resource management.
*   **Skills:** Deep knowledge of AWS, Azure, or GCP.
*   **Tools:** AWS Management Console, CLI, CloudFormation.

### Platform Engineer
Builds internal platforms that other developers use to deploy their code.
*   **Responsibilities:** Creating "Internal Developer Portals" to provide self-service tools for development teams.
*   **Skills:** Infrastructure as Code, API design.
*   **Tools:** Terraform, Backstage, Kubernetes.

### CI/CD Engineer
Specializes in the automation of building, testing, and deploying code.
*   **Responsibilities:** Optimizing the speed and reliability of the build pipeline.
*   **Skills:** Automation scripts, testing frameworks.
*   **Tools:** GitHub Actions, CircleCI, ArgoCD.

### Security/DevSecOps Engineer
Integrates security into every stage of the DevOps pipeline.
*   **Responsibilities:** Vulnerability scanning, compliance automation, and securing the cloud environment.
*   **Skills:** Cybersecurity, network security, risk assessment.
*   **Tools:** Snyk, SonarQube, Lacework, HashiCorp Vault.

---

## 3. Tools and Technologies Used in DevOps

DevOps relies heavily on automation. Here are the categories of tools you will encounter in the industry:

### Version Control
Allows teams to track changes in code and collaborate.
*   **Tools:** Git (the standard), GitHub, GitLab, Bitbucket.
*   **Why:** Essential for "Source of Truth" and enabling multiple developers to work on the same project without conflict.

### CI/CD Tools (Continuous Integration / Continuous Deployment)
Automates the process of building, testing, and shipping code.
*   **Tools:** Jenkins, GitHub Actions, GitLab CI, CircleCI.
*   **Why:** Ensures that every code change is automatically verified and ready for production.

### Containerization
Packages an application and its dependencies into a single "container" that runs anywhere.
*   **Tools:** Docker, Podman.
*   **Why:** Eliminates the "it works on my machine" problem by providing a consistent environment.

### Container Orchestration
Manages and scales hundreds or thousands of containers.
*   **Tools:** Kubernetes (K8s), OpenShift.
*   **Why:** Automates deployment, scaling, and management of containerized applications across a cluster of servers.

### Infrastructure as Code (IaC)
Defines servers, databases, and networks using code instead of manual configuration.
*   **Tools:** Terraform, Pulumi, AWS CloudFormation.
*   **Why:** Allows infrastructure to be version-controlled, easily replicated, and treated like application code.

### Configuration Management
Automates the setup and maintenance of software on existing servers.
*   **Tools:** Ansible, Chef, Puppet.
*   **Why:** Ensures that all servers are configured identically and prevents "configuration drift."

### Monitoring & Logging
Tracks the health and performance of applications.
*   **Tools:** Prometheus, Grafana (Monitoring), ELK Stack (Elasticsearch, Logstash, Kibana), Datadog.
*   **Why:** Helps identify bugs or performance bottlenecks before customers do.

### Cloud Platforms
Provides the raw resources (servers, storage, etc.) needed to run applications.
*   **Tools:** Amazon Web Services (AWS), Microsoft Azure, Google Cloud Platform (GCP).
*   **Why:** Offers scalable, on-demand infrastructure without the need for physical data centers.

---

## 4. Clear DevOps Roadmap for Beginners

If you are starting from scratch, follow this step-by-step path:

1.  **Linux Fundamentals:** Learn the command line. Most servers and DevOps tools run on Linux.
    *   *Focus:* File systems, permissions, SSH, processes.
2.  **Networking Basics:** Understand how computers talk to each other.
    *   *Focus:* IP addresses, DNS, HTTP/S, Firewalls, Load Balancers.
3.  **Version Control (Git):** Learn to manage code versions.
    *   *Focus:* Commits, branches, merges, pull requests.
4.  **Programming/Scripting:** Automate repetitive tasks.
    *   *Focus:* Python is highly recommended, followed by Bash scripting.
5.  **CI/CD Concepts:** Understand the flow of code from a laptop to a production server.
    *   *Focus:* Build stages, automated testing, deployment strategies.
6.  **Containers (Docker):** Learn to package applications.
    *   *Focus:* Writing Dockerfiles, managing images, and volumes.
7.  **Container Orchestration (Kubernetes):** Learn to manage containers at scale.
    *   *Focus:* Pods, Deployments, Services, ConfigMaps.
8.  **Infrastructure as Code (IaC):** Learn to provision cloud resources.
    *   *Focus:* Terraform is the industry standard (HCL language).
9.  **Cloud Platforms:** Pick one major provider and learn its core services.
    *   *Focus:* AWS (EC2, S3, RDS, IAM) is a great starting point.
10. **Monitoring and Observability:** Learn to troubleshoot systems.
    *   *Focus:* Setting up alerts and dashboards.
11. **Security in DevOps (DevSecOps):** Learn to secure the entire pipeline.
    *   *Focus:* Secret management, dependency scanning, and IAM roles.

---

## 5. Summary

DevOps is the "glue" that connects software development with professional-grade infrastructure. It emphasizes **automation** to reduce errors, **collaboration** to improve speed, and **infrastructure** that is treated exactly like code. By mastering these principles and tools, you enable your team to build, ship, and run high-quality software faster than ever before.

---
Next: [01_cloud_platforms.md](01_cloud_platforms.md)
---
