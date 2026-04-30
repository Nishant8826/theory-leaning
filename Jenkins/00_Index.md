# ⚙️ Jenkins Staff-Level Engineering Curriculum

## 📚 Module Overview
This curriculum is a deep, production-grade dive into **Jenkins CI/CD** and the principles of **Enterprise Build Orchestration**. It moves beyond simple job creation to explore Jenkins internals (Stapler, Remoting), distributed scaling (Dynamic Agents, Kubernetes), and high-reliability architecture (Fault Tolerance, DR).

This module covers 11 distinct domains:
1.  **Core Architecture**: Controller/Agent internals, JVM heap management, and the Remoting protocol.
2.  **Pipelines**: CPS-based execution, Groovy sandbox security, and Shared Library patterns.
3.  **SCM & Networking**: Git multibranch strategies, webhook lifecycle, and reverse proxy optimization.
4.  **Distributed Scaling**: Kubernetes-native agents, ephemeral build pods, and queue backpressure.
5.  **Security**: Identity-based access (RBAC), Secrets Management, and Supply Chain security.
6.  **Observability**: Build tracing, metrics monitoring, and production-grade debugging.
7.  **Reliability**: Fault-tolerant controller design and disaster recovery for Jenkins state.
8.  **Internals Deep Dive**: RPC mechanics, threading models, and I/O behavior.
9.  **Projects**: Building scalable, event-driven CI systems from the ground up.

---

## 📂 Curriculum Map

### 🏗️ [Core](./Core/)
- [01 Jenkins Architecture](./Core/01_Jenkins_Architecture.md)
- [02 Controller Internals](./Core/02_Controller_Internals.md)
- [03 Agents and Executors](./Core/03_Agents_and_Executors.md)
- [04 Queue and Scheduler](./Core/04_Queue_and_Scheduler.md)
- [05 Config and State Management](./Core/05_Config_and_State_Management.md)
- [06 Plugin System](./Core/06_Plugin_System.md)
- [07 Jenkins Remoting Protocol](./Core/07_Jenkins_Remoting_Protocol.md)
- [08 System Performance Limits](./Core/08_System_Performance_Limits.md)

### 🚀 [Pipelines](./Pipelines/)
- [01 Declarative vs Scripted](./Pipelines/01_Declarative_vs_Scripted.md)
- [02 Jenkinsfile Execution Model](./Pipelines/02_Jenkinsfile_Execution_Model.md)
- [03 Groovy Sandbox](./Pipelines/03_Groovy_Sandbox.md)
- [04 Shared Libraries](./Pipelines/04_Shared_Libraries.md)
- [05 Stage Execution and Parallelism](./Pipelines/05_Stage_Execution_and_Parallelism.md)
- [06 Pipeline State and Checkpointing](./Pipelines/06_Pipeline_State_and_Checkpointing.md)
- [07 Long Running Pipelines](./Pipelines/07_Long_Running_Pipelines.md)

### 🌳 [SCM](./SCM/)
- [01 Git Integration](./SCM/01_Git_Integration.md)
- [02 Webhooks vs Polling](./SCM/02_Webhooks_vs_Polling.md)
- [03 Multibranch Pipelines](./SCM/03_Multibranch_Pipelines.md)
- [04 Large Repo Challenges](./SCM/04_Large_Repo_Challenges.md)

### 🔨 [Builds](./Builds/)
- [01 Build Execution Lifecycle](./Builds/01_Build_Execution_Lifecycle.md)
- [02 Workspace Management](./Builds/02_Workspace_Management.md)
- [03 Artifacts and Storage](./Builds/03_Artifacts_and_Storage.md)
- [04 Caching Strategies](./Builds/04_Caching_Strategies.md)
- [05 Docker Builds](./Builds/05_Docker_Builds.md)

### 🌐 [Distributed](./Distributed/)
- [01 Distributed Builds](./Distributed/01_Distributed_Builds.md)
- [02 Dynamic Agents](./Distributed/02_Dynamic_Agents.md)
- [03 Kubernetes Plugin](./Distributed/03_Kubernetes_Plugin.md)
- [04 Autoscaling Strategies](./Distributed/04_Autoscaling_Strategies.md)
- [05 Network Latency Impact](./Distributed/05_Network_Latency_Impact.md)

### 🔐 [Security](./Security/)
- [01 Authentication and Authorization](./Security/01_Authentication_and_Authorization.md)
- [02 Credentials Management](./Security/02_Credentials_Management.md)
- [03 Secrets Handling](./Security/03_Secrets_Handling.md)
- [04 Sandbox and Script Security](./Security/04_Sandbox_and_Script_Security.md)
- [05 Supply Chain Security](./Security/05_Supply_Chain_Security.md)

### 🕸️ [Networking](./Networking/)
- [01 HTTP Request Flow](./Networking/01_HTTP_Request_Flow.md)
- [02 Reverse Proxy Setup](./Networking/02_Reverse_Proxy_Setup.md)
- [03 TLS and Certificates](./Networking/03_TLS_and_Certificates.md)
- [04 Webhook Delivery](./Networking/04_Webhook_Delivery.md)
- [05 Agent Controller Communication](./Networking/05_Agent_Controller_Communication.md)

### 📊 [Observability](./Observability/)
- [01 Logging Internals](./Observability/01_Logging_Internals.md)
- [02 Metrics and Monitoring](./Observability/02_Metrics_and_Monitoring.md)
- [03 Tracing Builds](./Observability/03_Tracing_Builds.md)
- [04 Debugging Production Issues](./Observability/04_Debugging_Production_Issues.md)

### 📈 [Scaling](./Scaling/)
- [01 Controller Bottlenecks](./Scaling/01_Controller_Bottlenecks.md)
- [02 Queue Backpressure](./Scaling/02_Queue_Backpressure.md)
- [03 Horizontal Scaling](./Scaling/03_Horizontal_Scaling.md)
- [04 Build Parallelism](./Scaling/04_Build_Parallelism.md)
- [05 Large Org Challenges](./Scaling/05_Large_Org_Challenges.md)

### 🛡️ [Reliability](./Reliability/)
- [01 Fault Tolerance](./Reliability/01_Fault_Tolerance.md)
- [02 Controller Failures](./Reliability/02_Controller_Failures.md)
- [03 Agent Failures](./Reliability/03_Agent_Failures.md)
- [04 Data Corruption](./Reliability/04_Data_Corruption.md)
- [05 Disaster Recovery](./Reliability/05_Disaster_Recovery.md)

### 🔬 [Internals](./Internals/)
- [01 Control Plane vs Data Plane](./Internals/01_Control_Plane_vs_Data_Plane.md)
- [02 Remoting and RPC](./Internals/02_Remoting_and_RPC.md)
- [03 Threading Model](./Internals/03_Threading_Model.md)
- [04 IO and Disk Behavior](./Internals/04_IO_and_Disk_Behavior.md)
- [05 Eventual Consistency in Jenkins](./Internals/05_Eventual_Consistency.md)

### 🛠️ [Projects](./Projects/)
- [01 Scalable CI System](./Projects/01_Scalable_CI_System.md)
- [02 Kubernetes Native Jenkins](./Projects/02_Kubernetes_Native_Jenkins.md)
- [03 Event Driven Pipeline System](./Projects/03_Event_Driven_Pipeline_System.md)
- [04 Monorepo CI Optimization](./Projects/04_Monorepo_CI_Optimization.md)
- [05 Observability for CI](./Projects/05_Observability_for_CI.md)

---
**Prev: None | Index: [00_Index.md](./00_Index.md) | Next: [01_Jenkins_Architecture.md](./Core/01_Jenkins_Architecture.md)**
