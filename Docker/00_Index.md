# 🐳 Mastering Docker: From Zero to Staff Engineer

Welcome to the ultimate Docker learning system. This curriculum is designed to take you from a complete beginner to a Staff/Principal Engineer level, capable of designing and debugging large-scale containerized systems.

---

## 🗺️ Curriculum Map

### 🟢 Phase 1: Core Fundamentals
- [01_What_is_Docker_and_Why.md](Core/01_What_is_Docker_and_Why.md)
- [02_Containers_vs_Virtual_Machines.md](Core/02_Containers_vs_Virtual_Machines.md)
- [03_Docker_Architecture_Overview.md](Core/03_Docker_Architecture_Overview.md)
- [04_Installation_and_Setup_Windows_Linux_Mac.md](Core/04_Installation_and_Setup_Windows_Linux_Mac.md)
- [50_The_Future_of_Docker_Wasm_and_Beyond.md](Core/50_The_Future_of_Docker_Wasm_and_Beyond.md)

### 🟡 Phase 2: Images & The Build System
- [05_The_Anatomy_of_an_Image.md](Images/05_The_Anatomy_of_an_Image.md)
- [06_Dockerfile_Basics_and_Instructions.md](Images/06_Dockerfile_Basics_and_Instructions.md)
- [07_Layer_Caching_and_Optimization.md](Images/07_Layer_Caching_and_Optimization.md)
- [08_Multi_Stage_Builds_for_Production.md](Images/08_Multi_Stage_Builds_for_Production.md)
- [09_BuildKit_The_Modern_Build_Engine.md](Images/09_BuildKit_The_Modern_Build_Engine.md)
- [10_Multi_Arch_Images_Buildx.md](Images/10_Multi_Arch_Images_Buildx.md)

### 🔵 Phase 3: Container Lifecycle & Runtime
- [11_Container_Lifecycle_Commands.md](Runtime/11_Container_Lifecycle_Commands.md)
- [12_Interactive_vs_Detached_Modes.md](Runtime/12_Interactive_vs_Detached_Modes.md)
- [13_Exec_Logs_and_Inspecting_State.md](Runtime/13_Exec_Logs_and_Inspecting_State.md)
- [14_Resource_Limits_CPU_and_Memory.md](Runtime/14_Resource_Limits_CPU_and_Memory.md)

### 🟠 Phase 4: Networking Deep Dive
- [15_Docker_Network_Drivers_Bridge_Host_None.md](Networking/15_Docker_Network_Drivers_Bridge_Host_None.md)
- [16_Port_Mapping_and_NAT_Internals.md](Networking/16_Port_Mapping_and_NAT_Internals.md)
- [17_DNS_and_Service_Discovery_in_Docker.md](Networking/17_DNS_and_Service_Discovery_in_Docker.md)
- [18_Advanced_Networking_Overlay_and_Macvlan.md](Networking/18_Advanced_Networking_Overlay_and_Macvlan.md)

### 🟤 Phase 5: Storage & Persistence
- [19_Volumes_vs_Bind_Mounts.md](Storage/19_Volumes_vs_Bind_Mounts.md)
- [20_Storage_Drivers_and_OverlayFS_Internals.md](Storage/20_Storage_Drivers_and_OverlayFS_Internals.md)
- [21_Tmpfs_Mounts_and_Data_Security.md](Storage/21_Tmpfs_Mounts_and_Data_Security.md)

### 🟣 Phase 6: Orchestration with Docker Compose
- [22_Docker_Compose_Declarative_Containers.md](Orchestration/22_Docker_Compose_Declarative_Containers.md)
- [23_Managing_Multi_Container_Applications.md](Orchestration/23_Managing_Multi_Container_Applications.md)
- [24_Compose_Profiles_and_Environment_Variables.md](Orchestration/24_Compose_Profiles_and_Environment_Variables.md)

### 📦 Phase 6.5: Registry & Distribution
- [24b_Registry_and_Image_Distribution.md](Distribution/24b_Registry_and_Image_Distribution.md)

### 🔴 Phase 7: Internals & Kernel Level
- [25_Linux_Namespaces_The_Isolation_Engine.md](Internals/25_Linux_Namespaces_The_Isolation_Engine.md)
- [26_Control_Groups_Cgroups_Resource_Management.md](Internals/26_Control_Groups_Cgroups_Resource_Management.md)
- [27_Docker_Engine_to_containerd_to_runc_Flow.md](Internals/27_Docker_Engine_to_containerd_to_runc_Flow.md)
- [28_The_Copy_on_Write_CoW_Mechanism.md](Internals/28_The_Copy_on_Write_CoW_Mechanism.md)
- [41_Docker_Engine_API_and_SDKs.md](Internals/41_Docker_Engine_API_and_SDKs.md)
- [52_Container_Forensics_and_Recovery.md](Internals/52_Container_Forensics_and_Recovery.md)

### 🛡️ Phase 8: Security & Supply Chain
- [29_Docker_Security_Best_Practices.md](Security/29_Docker_Security_Best_Practices.md)
- [30_Rootless_Docker_Running_without_Sudo.md](Security/30_Rootless_Docker_Running_without_Sudo.md)
- [31_Image_Scanning_and_Vulnerability_Management.md](Security/31_Image_Scanning_and_Vulnerability_Management.md)
- [32_Capabilities_Seccomp_and_AppArmor.md](Security/32_Capabilities_Seccomp_and_AppArmor.md)
- [42_Docker_Content_Trust_and_Signatures.md](Security/42_Docker_Content_Trust_and_Signatures.md)

### 🚀 Phase 9: CI/CD & Production Operations
- [33_Docker_in_Jenkins_Pipelines.md](Ops/33_Docker_in_Jenkins_Pipelines.md)
- [34_Logging_Drivers_and_Aggregation.md](Ops/34_Logging_Drivers_and_Aggregation.md)
- [35_Monitoring_Docker_Stats_Prometheus_Grafana.md](Ops/35_Monitoring_Docker_Stats_Prometheus_Grafana.md)
- [36_Debugging_Production_Incidents.md](Ops/36_Debugging_Production_Incidents.md)
- [43_Advanced_Dev_Workflows_Dev_Containers.md](Ops/43_Advanced_Dev_Workflows_Dev_Containers.md)
- [51_Docker_Plugins_and_Contexts.md](Ops/51_Docker_Plugins_and_Contexts.md)

### 🏢 Phase 10: Scaling & Architecture
- [37_Horizontal_Scaling_Strategies.md](Scaling/37_Horizontal_Scaling_Strategies.md)
- [38_Docker_vs_Kubernetes_When_to_Move.md](Scaling/38_Docker_vs_Kubernetes_When_to_Move.md)
- [39_Cost_Optimization_and_Resource_Tuning.md](Scaling/39_Cost_Optimization_and_Resource_Tuning.md)
- [40_High_Availability_and_Disaster_Recovery.md](Scaling/40_High_Availability_and_Disaster_Recovery.md)

### 🏗️ Phase 11: Capstone Project - Full Stack MERN
- [44_Project_MERN_Architecture_Overview.md](Project/44_Project_MERN_Architecture_Overview.md)
- [45_Project_MERN_Backend_Dockerization.md](Project/45_Project_MERN_Backend_Dockerization.md)
- [46_Project_MERN_Frontend_Optimization.md](Project/46_Project_MERN_Frontend_Optimization.md)
- [47_Project_MERN_Database_and_Persistence.md](Project/47_Project_MERN_Database_and_Persistence.md)
- [48_Project_MERN_Full_Stack_Compose.md](Project/48_Project_MERN_Full_Stack_Compose.md)
- [49_Project_MERN_Production_Hardening.md](Project/49_Project_MERN_Production_Hardening.md)

---

## 🎓 How to use this system
Each module follows a strict progression:
1. **🟢 Simple Explanation**: No-jargon intro.
2. **🟡 Practical Usage**: Real commands and code.
3. **🔵 Intermediate Concepts**: Architecture and behavior.
4. **🔴 Internals**: Kernel level and deep flow.
5. **⚫ Staff-Level Insights**: Trade-offs, costs, and performance.

---
Next: [01_What_is_Docker_and_Why.md](Core/01_What_is_Docker_and_Why.md)
---
