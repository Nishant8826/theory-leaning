# 🐳 Staff-Level Docker & Containerization Systems Engineering

## 🛰️ Course Roadmap: From Senior to Staff/Principal
This curriculum is designed for engineers with 10+ years of experience. We move beyond "how to use Docker" to "how Docker works at the kernel level." You will master container runtime internals, networking stacks, image security, and high-scale orchestration on AWS.

---

## 🗺️ Learning Path

### 🏗️ [Core Internals](./Core/)
*Focus: Kernel primitives (Namespaces, cgroups), UnionFS, and OCI runtime mechanics.*

**What it is: The foundation of containerization.**
Deep dive into Linux kernel primitives like **Namespaces** and **cgroups**. You will learn how Docker creates the illusion of isolation and how the **Union Filesystem** (Overlay2) manages image layers at the byte level.
- [01 Containerization vs VMs](./Core/01_Containerization_vs_VMs.md)
- [02 Docker Architecture](./Core/02_Docker_Architecture.md)
- [03 Namespaces and cgroups](./Core/03_Namespaces_and_cgroups.md)
- [04 Union Filesystem](./Core/04_Union_Filesystem.md)
- [05 Container Runtime runc containerd OCI](./Core/05_Container_Runtime_runc_containerd_OCI.md)
- [06 Image Layers and Caching](./Core/06_Image_Layers_and_Caching.md)
- [07 BuildKit Internals](./Core/07_BuildKit_Internals.md)
- [08 Docker Engine API](./Core/08_Docker_Engine_API.md)
- [09 System Performance Limits](./Core/09_System_Performance_Limits.md)

### 📦 [Images & Build](./Images/)
*Focus: Execution models, multi-stage builds, and multi-architecture image engineering.*

**What it is: Advanced artifact engineering.**
Master the **Dockerfile execution model** and **BuildKit**'s parallel solver. Focus on creating high-performance, multi-architecture images while implementing security standards like **SBOM** and **Image Signing**.
- [01 Dockerfile Execution Model](./Images/01_Dockerfile_Execution_Model.md)
- [02 Layer Caching Strategies](./Images/02_Layer_Caching_Strategies.md)
- [03 Multi Stage Builds](./Images/03_Multi_Stage_Builds.md)
- [04 Multi Arch Images](./Images/04_Multi_Arch_Images.md)
- [05 Image Optimization Node React](./Images/05_Image_Optimization_Node_React.md)
- [06 Base Images and Security](./Images/06_Base_Images_and_Security.md)
- [07 SBOM and Image Signing](./Images/07_SBOM_and_Image_Signing.md)

### 🏃 [Containers & Runtime](./Containers/)
*Focus: PID 1 process models, resource limits tuning, and rootless containerization.*

**What it is: Managing the process lifecycle.**
Learn the critical importance of **PID 1**, signal propagation, and resource limits. This module covers **Rootless containers** and advanced debugging techniques for production-grade process isolation.
- [01 Container Lifecycle](./Containers/01_Container_Lifecycle.md)
- [02 Process Model PID1](./Containers/02_Process_Model_PID1.md)
- [03 Resource Limits](./Containers/03_Resource_Limits.md)
- [04 Logging and STDOUT](./Containers/04_Logging_and_STDOUT.md)
- [05 Debugging Containers](./Containers/05_Debugging_Containers.md)
- [06 Rootless Containers](./Containers/06_Rootless_Containers.md)

### 🌐 [Networking](./Networking/)
*Focus: Bridge/Overlay mechanics, service discovery, and real-time connection lifecycles.*

**What it is: Distributed systems connectivity.**
Understand the **Bridge** and **Overlay** drivers from the packet level. Master service discovery, DNS internals, and how to scale real-time protocols like **WebSockets** and **gRPC** across clusters.
- [01 Bridge Network](./Networking/01_Bridge_Network.md)
- [02 Overlay Network](./Networking/02_Overlay_Network.md)
- [03 Service Discovery and DNS](./Networking/03_Service_Discovery_and_DNS.md)
- [04 Port Mapping and NAT](./Networking/04_Port_Mapping_and_NAT.md)
- [05 Connection Lifecycle TCP TLS](./Networking/05_Connection_Lifecycle_TCP_TLS.md)
- [06 WebSockets and RealTime](./Networking/06_WebSockets_and_RealTime.md)

### 💾 [Storage](./Storage/)
*Focus: Storage drivers (Overlay2), I/O performance tuning, and persistent DB architecture.*

**What it is: Data persistence and I/O performance.**
Bypass the storage driver bottlenecks. Learn the trade-offs between **Volumes** and **Bind Mounts**, and how to tune I/O for high-throughput databases like **Postgres** and **MongoDB**.
- [01 Volumes vs Bind Mounts](./Storage/01_Volumes_vs_Bind_Mounts.md)
- [02 Storage Drivers](./Storage/02_Storage_Drivers.md)
- [03 Data Persistence](./Storage/03_Data_Persistence.md)
- [04 DB Containers Mongo Postgres](./Storage/04_DB_Containers_Mongo_Postgres.md)
- [05 IO Performance](./Storage/05_IO_Performance.md)
- [06 Backups and Snapshots](./Storage/06_Backups_and_Snapshots.md)

### 🎼 [Compose](./Compose/)
*Focus: Multi-service architecture, scaling locally, and environment secret management.*

**What it is: Local orchestration and service modeling.**
Scale your local development to match production. Implement **Multi-service architectures**, manage secrets securely, and understand how Compose manages service dependencies and internal networks.
- [01 Docker Compose Internals](./Compose/01_Docker_Compose_Internals.md)
- [02 Multi Service Architecture](./Compose/02_Multi_Service_Architecture.md)
- [03 Local Dev Environment](./Compose/03_Local_Dev_Environment.md)
- [04 Env Config and Secrets](./Compose/04_Env_Config_and_Secrets.md)
- [05 Scaling with Compose](./Compose/05_Scaling_with_Compose.md)

### 🏭 [Registry & Distribution](./Registry/)
*Focus: OCI distribution spec, self-hosted Harbor, and pull-through caching.*

**What it is: Content addressable storage at scale.**
Build your own **Harbor** registry, implement **Pull-through caching** to save bandwidth, and master the **OCI Distribution Spec** to understand how images are deduplicated across the globe.
- [01 Image Registry Architecture](./Registry/01_Image_Registry_Architecture.md)
- [02 Self Hosted Harbor](./Registry/02_Self_Hosted_Harbor.md)
- [03 Pull Through Caching](./Registry/03_Pull_Through_Caching.md)
- [04 Cloud Registries ECR GCR](./Registry/04_Cloud_Registries_ECR_GCR.md)
- [05 Content Trust and Signing](./Registry/05_Content_Trust_and_Signing.md)

### 🔐 [Security](./Security/)
*Focus: Daemon hardening, seccomp/capabilities, and runtime security (Falco).*

**What it is: Hardening the attack surface.**
Implement **Zero-Trust** security. Learn to drop kernel capabilities, use **seccomp** profiles, and monitor for runtime threats using **Falco**. This module prepares you for the **CIS Docker Benchmark**.
- [01 Docker Daemon Security](./Security/01_Docker_Daemon_Security.md)
- [02 Kernel Capabilities and seccomp](./Security/02_Kernel_Capabilities_and_seccomp.md)
- [03 Scanning Images Trivy](./Security/03_Scanning_Images_Trivy.md)
- [04 Network Policies and mTLS](./Security/04_Network_Policies_and_mTLS.md)
- [05 Runtime Security](./Security/05_Runtime_Security.md)
- [06 CIS Benchmark and Auditing](./Security/06_CIS_Benchmark_and_Auditing.md)

### 🚀 [CI/CD Integration](./CI_CD/)
*Focus: Jenkins build pipelines, layer caching in CI, and artifact lifecycle management.*

**What it is: High-velocity delivery pipelines.**
Automate everything. Integrate Docker with **Jenkins**, optimize build caching in ephemeral environments, and implement advanced deployment strategies like **Blue-Green** and **Canary**.
- [01 Jenkins Integration Architecture](./CI_CD/01_Jenkins_Integration_Architecture.md)
- [02 Automated Build Pipelines](./CI_CD/02_Automated_Build_Pipelines.md)
- [03 Caching Build Layers in CI](./CI_CD/03_Caching_Build_Layers_in_CI.md)
- [04 Blue Green and Canary Deploys](./CI_CD/04_Blue_Green_and_Canary_Deploys.md)
- [05 Artifact Management](./CI_CD/05_Artifact_Management.md)

### ☸️ [Orchestration](./Orchestration/)
*Focus: Swarm vs K8s, Fargate serverless containers, and GitOps principles.*

**What it is: Managing clusters at scale.**
Compare **Docker Swarm** with **Kubernetes**. Master serverless containerization with **AWS Fargate**, and implement **GitOps** principles to manage your infrastructure as code.
- [01 Docker Swarm Internals](./Orchestration/01_Docker_Swarm_Internals.md)
- [02 Kubernetes vs Swarm](./Orchestration/02_Kubernetes_vs_Swarm.md)
- [03 Serverless Containers Fargate](./Orchestration/03_Serverless_Containers_Fargate.md)
- [04 Infrastructure as Code Terraform](./Orchestration/04_Infrastructure_as_Code_Terraform.md)
- [05 GitOps Principles](./Orchestration/05_GitOps_Principles.md)

### 📈 [Scaling](./Scaling/)
*Focus: Horizontal scaling, auto-scaling (HPA), and global traffic management (Anycast).*

**What it is: Elasticity and traffic management.**
Master **Horizontal Scaling** and **Auto-scaling (HPA)**. Learn to manage global traffic using **Anycast** and handle session persistence in a distributed environment.
- [01 Horizontal Scaling](./Scaling/01_Horizontal_Scaling.md)
- [02 Auto scaling Mechanisms](./Scaling/02_Auto_scaling_Mechanisms.md)
- [03 Load Balancing Strategies](./Scaling/03_Load_Balancing_Strategies.md)
- [04 Global Traffic Management](./Scaling/04_Global_Traffic_Management.md)
- [05 Session Affinity and Persistence](./Scaling/05_Session_Affinity_and_Persistence.md)

### ⚡ [Performance](./Performance/)
*Focus: Profiling (pprof), MTU optimization, and cold start reduction.*

**What it is: Tuning for the last millisecond.**
Use **pprof** and **Clinic.js** to find CPU and memory bottlenecks. Optimize **MTU** settings and reduce **Cold Starts** for high-performance serverless and microservice workloads.
- [01 CPU and Memory Profiling](./Performance/01_CPU_and_Memory_Profiling.md)
- [02 Network Latency Optimization](./Performance/02_Network_Latency_Optimization.md)
- [03 Caching Strategies at Scale](./Performance/03_Caching_Strategies_at_Scale.md)
- [04 Cold Start Reduction](./Performance/04_Cold_Start_Reduction.md)
- [05 Kernel Tuning for High Throughput](./Performance/05_Kernel_Tuning_for_High_Throughput.md)

### 🛡️ [Reliability](./Reliability/)
*Focus: Health probes, circuit breakers, and chaos engineering.*

**What it is: Building self-healing systems.**
Master **Health Checks**, **Circuit Breakers**, and **Graceful Shutdowns**. Use **Chaos Engineering** to prove your system can survive the death of any component.
- [01 Health Checks and Probes](./Reliability/01_Health_Checks_and_Probes.md)
- [02 Circuit Breakers and Retries](./Reliability/02_Circuit_Breakers_and_Retries.md)
- [03 Graceful Shutdown and SIGTERM](./Reliability/03_Graceful_Shutdown_and_SIGTERM.md)
- [04 Chaos Engineering Basics](./Reliability/04_Chaos_Engineering_Basics.md)
- [05 Disaster Recovery Planning](./Reliability/05_Disaster_Recovery_Planning.md)

### 🔬 [Internals](./Internals/)
*Focus: Namespace deep dives, cgroup V2, and OCI runtime spec.*

**What it is: Advanced OS-level deep dives.**
A staff-level exploration of the **OCI Spec**, **runc**, and **Cgroup V2**. Understand how the kernel schedules container processes and how to tune the network stack for millions of connections.
- [01 Namespaces Deep Dive](./Internals/01_Namespaces_Deep_Dive.md)
- [02 Cgroups and Resource Control](./Internals/02_Cgroups_and_Resource_Control.md)
- [03 OverlayFS and Storage Drivers](./Internals/03_OverlayFS_and_Storage_Drivers.md)
- [04 OCI Spec and runc](./Internals/04_OCI_Spec_and_runc.md)
- [05 Linux Capabilities Matrix](./Internals/05_Linux_Capabilities_Matrix.md)

### 🏗️ [Projects](./Projects/)
*Focus: Hands-on deployment of secure, scalable, and observable systems.*

**What it is: Real-world integration labs.**
Hands-on projects that unify all previous modules. Build a **Socket.io cluster**, secure microservices with **Vault**, and deploy a full **Prometheus/Grafana** observability stack.
- [01 Docker Node React Deployment](./Projects/01_Docker_Node_React_Deployment.md)
- [02 RealTime SocketIO Cluster](./Projects/02_RealTime_SocketIO_Cluster.md)
- [03 Secure Microservices with Vault](./Projects/03_Secure_Microservices_with_Vault.md)
- [04 CI CD with Jenkins and ECR](./Projects/04_CI_CD_with_Jenkins_and_ECR.md)
- [05 Monitoring Stack Prometheus Grafana](./Projects/05_Monitoring_Stack_Prometheus_Grafana.md)

---
**Prev: None | Index: [00_Index.md](./00_Index.md) | Next: [01_Containerization_vs_VMs.md](./Core/01_Containerization_vs_VMs.md)**
