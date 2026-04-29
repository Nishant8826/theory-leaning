# 🏗️ Kubernetes-Native Jenkins Migration

## 📌 Topic Name
Project Blueprint: Migrating from Legacy VMs to Kubernetes (EKS/GKE)

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Moving an old Jenkins server installed on a single Linux machine into a modern Kubernetes cluster.
*   **Expert**: Migrating Jenkins from static VMs to Kubernetes is a paradigm shift from **Mutable Infrastructure** to **Immutable Infrastructure**. It involves containerizing the Controller, implementing JCasC for state management, mapping EBS/EFS volumes for persistent storage, and rewriting pipelines to utilize Ephemeral Pods instead of static agents. A Staff engineer must plan for the massive shift in **Networking Topology** (Ingress, WebSocket tunnels, internal DNS) and **Developer Workflow** (Docker Socket removal, workspace volatility).

## 🏗️ Mental Model
Think of this migration as **Moving from a House to an RV (Recreational Vehicle)**.
- **The House (Static VM)**: You have a basement full of junk (caches, old builds). It's huge, stable, but you can never move it.
- **The RV (Kubernetes)**: You can only take what fits. You have to learn how to plug into external power and water (Network/Storage) at every campsite. But you can instantly pack up and deploy the exact same RV anywhere in the world.

## ⚡ Architecture Diagram

```mermaid
graph TD
    subgraph Legacy Environment
        VM[Static EC2 Instance]
        JenkinsWar[jenkins.war]
        LocalDisk[500GB Local Disk]
        StaticAgents[Static SSH Agents]
        
        VM --> JenkinsWar
        JenkinsWar --> LocalDisk
        JenkinsWar --> StaticAgents
    end

    subgraph Kubernetes Environment (Target)
        Ingress[NGINX Ingress]
        ALB[AWS ALB: Port 443]
        TCP[TCP LB: Port 50000]
        
        StatefulSet[Jenkins StatefulSet]
        EBS[AWS EBS: /var/jenkins_home]
        
        JCasC[JCasC ConfigMap]
        
        K8sPlugin[Kubernetes Plugin]
        EphemeralPods[Ephemeral Agent Pods]

        ALB --> Ingress
        TCP --> StatefulSet
        Ingress --> StatefulSet
        StatefulSet --> EBS
        StatefulSet --> JCasC
        StatefulSet --> K8sPlugin
        K8sPlugin --> EphemeralPods
    end

    %% Migration Path
    Legacy Environment -.->|1. Export Config| JCasC
    Legacy Environment -.->|2. Rewrite Pipelines| EphemeralPods
```

## 🔬 Component Deep Dive & Migration Steps

### Phase 1: Controller Containerization & State Decoupling
*   **Legacy State**: Everything is mashed into `/var/lib/jenkins`.
*   **Action**: Do not just run `tar -czf` and drop it in Kubernetes. This is the time to clean house.
*   **Implementation**: Deploy Jenkins using the official Helm Chart. Define an EBS `PersistentVolumeClaim` (ReadWriteOnce) mounted to `/var/jenkins_home`.
*   **Configuration**: Extract all global settings (LDAP, Cloud, Global Libs) into a `jenkins.yaml` file and mount it as a K8s ConfigMap via JCasC. The Controller is now immutable; only the PVC holds state.

### Phase 2: Ingress and Remoting Networking
*   **Legacy State**: Jenkins UI is accessed via IP address or simple proxy. Agents connect via SSH.
*   **Action**: Map K8s networking correctly for Inbound WebSockets.
*   **Implementation**: Create an Ingress object for the Web UI (Port 80/443).
*   **The Trap (Port 50000)**: If agents are outside the cluster, you must expose the JNLP port (50000). Standard HTTP Ingress controllers (like standard NGINX Ingress) cannot route raw TCP. You must either configure TCP pass-through on the Ingress or provision a separate Network Load Balancer (NLB) exclusively for port 50000. *Best Practice*: Keep agents inside the cluster so they can use the internal K8s Service (`http://jenkins-agent:50000`).

### Phase 3: Agent Migration (The Hardest Part)
*   **Legacy State**: Jobs rely on `node('linux')`. The VM has Maven, Node, and Docker installed locally. Jobs rely on the fact that `node_modules` are still there from yesterday.
*   **Action**: Rewrite Jenkinsfiles to use the Kubernetes plugin.
*   **Implementation**: Replace `agent any` with `agent { kubernetes { yaml ... } }`.
*   **The Docker Socket Problem**: Legacy jobs likely use `docker build`. In K8s, mapping `/var/run/docker.sock` is a critical security vulnerability and often impossible in managed K8s (which uses `containerd`, not Docker). **You must rewrite docker builds to use Kaniko or Buildah inside the Pod.**

### Phase 4: Storage and Caching Overhaul
*   **Legacy State**: Workspaces are left dirty. Caches build up naturally on the VM.
*   **Action**: Implement distributed caching.
*   **Implementation**: Since Pods are ephemeral, builds will suddenly take 10x longer because dependencies must be downloaded every time. Implement S3-backed caching scripts or deploy a K8s-local Nexus cache to proxy Maven/NPM traffic.

## 💥 Implementation Failure Modes
1.  **The PVC Deadlock**: You deploy Jenkins as a Kubernetes `Deployment`. You apply a config change and K8s spins up Pod B while Pod A is shutting down. Both Pods try to mount the AWS EBS Volume. EBS is ReadWriteOnce (RWO) and strictly locks to a single EC2 node. Pod B hangs forever in `ContainerCreating`. **Rule**: Always deploy the Jenkins Controller as a `StatefulSet` or use `Deployment` with `strategy: Recreate` to ensure Pod A is entirely dead before Pod B requests the disk.
2.  **OOMKilled Controller**: The Controller memory limit in K8s is set to 4GB. The JVM heap (`-Xmx`) is set to 4GB. The JVM requires overhead (metaspace, thread stacks) beyond the heap. Total JVM footprint hits 4.2GB. Kubelet terminates the Pod with `OOMKilled`. **Rule**: Set K8s Memory Limit at least 20% higher than the JVM `-Xmx` parameter.
3.  **Zombie Pods**: If the Jenkins Controller crashes mid-build, the Kubernetes Plugin loses its tracking of the Agent Pods. The Pods will continue running indefinitely on the K8s cluster, consuming compute resources and generating massive cloud bills. **Rule**: Always ensure the "Jenkins Agent Garbage Collector" background task is running, and configure Pod retention policies strictly.

## ⚖️ Architectural Trade-offs
*   **Ephemerality vs Developer Velocity**: Moving to Kubernetes destroys the natural filesystem caching of VMs. Builds will initially be much slower and developers will complain. You are trading immediate raw speed for perfect reproducibility, high scalability, and infrastructure cost savings. You must invest heavily in external caching solutions to win back the developer velocity.

## 💼 Implementation Path
1.  **Audit**: Run the Jenkins "Configuration Slicing" plugin or manually audit all legacy jobs. Identify jobs using local tools, Docker socket, or hardcoded paths (`/opt/data`).
2.  **Pilot**: Stand up the Helm chart in a dev cluster. Port 3 non-critical pipelines to use Kaniko and PodTemplates.
3.  **Data Migration**: Put legacy Jenkins in "Quiet Down". Rsync only the `jobs/*/builds/` and `secrets/` directories to the new EFS/EBS volume.
4.  **Cutover**: Switch DNS. 
