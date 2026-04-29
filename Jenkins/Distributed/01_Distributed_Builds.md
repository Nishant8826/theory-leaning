# 🌐 Distributed Builds

## 📌 Topic Name
Jenkins Topology: Controller/Agent Separation and Blast Radius

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Using many computers to run builds instead of just one big computer.
*   **Expert**: Jenkins is fundamentally a **Distributed Compute Engine**. The Controller coordinates state, while the Agents perform the compute-intensive I/O operations. A Staff engineer designs the network topology to minimize **Blast Radius** and ensure **High Availability (HA)** of the execution plane. This involves understanding the limits of the Remoting protocol across WANs, utilizing labels for heterogeneous compute (GPU, ARM, Windows), and implementing a hub-and-spoke model to prevent "Noisy Neighbor" starvation.

## 🏗️ Mental Model
Think of a single Jenkins instance as a **Command Center (Controller)** and its **Troops (Agents)**.
- If all the troops are in the command center (Executors = 20 on the Controller), the building will collapse from exhaustion.
- If you spread the troops across the globe, communication (Remoting latency) takes too long.
- The ideal model: The Command Center is isolated and protected. The troops are stationed in nearby outposts (same AWS Region), strictly communicating via secure radio channels (WebSockets/TLS).

## ⚡ Actual Behavior
- **Controller Fragility**: If the Controller dies, the Agents are orphaned. Any currently running builds on the Agents will usually finish their current shell command, but cannot report the status back and will ultimately fail.
- **Agent Resiliency**: If an Agent dies, only the build running on that specific Agent fails. The Controller remains perfectly healthy and assigns the next build to a different Agent.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Label Expressions**: The matching engine in the Scheduler. `agent { label 'linux && (gpu || high-mem)' }`. This allows the Controller to map specific workload requirements to specialized hardware without hardcoding IP addresses.
2.  **Node Monitors**: Background threads on the Controller that constantly evaluate Agent health (Response Time, Free Disk Space, Free Temp Space). If an Agent drops below thresholds (e.g., <1GB free disk), the Controller automatically marks it `Offline` to prevent build failures.
3.  **Remoting Buffers**: The TCP channel between Controller and Agent has finite memory buffers. If an agent produces massive logs faster than the Controller can write them to disk, the buffer fills up, creating backpressure that slows down the Agent's execution.

## 🔁 Execution Flow (Topology Design)
1.  **Control Plane**: Deployed in a high-availability management VPC (e.g., `us-east-1`).
2.  **Execution Plane (Agents)**: Deployed across multiple Subnets/AZs.
3.  **Communication**: Agents connect inbound via WebSockets over port 443 through an internal Load Balancer.
4.  **Routing**: Job requests `label 'ios'`. Scheduler routes it to a Mac Mini fleet in a dedicated physical datacenter connected via Direct Connect.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Controller Starvation**: A single Controller can realistically manage ~1,000 to 2,000 connected Agents. Beyond that, the JVM spends all its CPU cycles just sending "Ping" packets to ensure the agents are alive.
- **Network Ingress/Egress**: Distributing builds across Cloud Regions (e.g., Controller in AWS, Agents in Azure) will incur massive data egress costs when workspaces/logs are synced.

## 📐 ASCII Diagrams (MANDATORY)
```text
      [ VPC: MANAGEMENT ]
+----------------------------+
|  [ JENKINS CONTROLLER ]    |
|   (Executors: 0)           |
+----------------------------+
       |             |
 (WebSocket)      (WebSocket)
       |             |
 [ VPC: LINUX ]   [ ON-PREM: MAC ]
+-------------+   +--------------+
| [ AGENT 1 ] |   | [ MAC MINI ] |
| [ AGENT 2 ] |   | [ MAC MINI ] |
| [ AGENT 3 ] |   +--------------+
+-------------+
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// Advanced node allocation demonstrating distributed routing
pipeline {
    agent none
    stages {
        stage('Compile x86') {
            // Routes to standard AWS EC2 instances
            agent { label 'aws && linux && x86_64' }
            steps { sh 'make target=x86' }
        }
        stage('Compile ARM') {
            // Routes to specialized AWS Graviton instances
            agent { label 'aws && linux && arm64' }
            steps { sh 'make target=arm' }
        }
        stage('Build iOS App') {
            // Routes over VPN to on-prem physical Mac Mini fleet
            agent { label 'on-prem && macos' }
            steps { sh 'xcodebuild ...' }
        }
    }
}
```

## 💥 Production Failures
1.  **The "Master Executor" Crash**: An admin leaves 2 executors enabled on the `Built-In Node` (the Controller). A developer writes a pipeline that runs a memory-intensive Docker build. It lands on the Controller, consumes 100% of RAM, triggers an OS Out of Memory (OOM) killer, and deletes the Jenkins process. The entire CI/CD system goes down.
2.  **Cross-Region Latency Sink**: A company in London deploys agents in an AWS Sydney region to utilize cheaper Spot instances. Builds that take 5 minutes locally take 50 minutes in Sydney due to the 300ms latency on the Jenkins Remoting Protocol serializing class files.
3.  **Disk Space False Positive**: An agent has 500GB of disk space. But Jenkins marks it offline because the `java.io.tmpdir` (`/tmp`) partition is full, triggering the "Free Temp Space" node monitor.

## 🧪 Real-time Q&A
*   **Q**: Can multiple Controllers share the same fleet of Agents?
*   **A**: Technically yes (using plugins like Swarm), but it is a massive anti-pattern. Controllers will fight over resources and cause unpredictable capacity planning. 1 Controller : N Agents.
*   **Q**: Should I use Inbound (Agent connects to Controller) or Outbound (Controller connects to Agent via SSH)?
*   **A**: Inbound (WebSockets/JNLP) is preferred in modern cloud environments because the Agent can be behind a NAT and the Controller doesn't need to manage thousands of SSH keys.

## ⚠️ Edge Cases
*   **Windows Agents**: Managing Windows agents via SSH is notoriously difficult. Using inbound JNLP launched via a Windows Service is the standard workaround.

## 🏢 Best Practices
1.  **Executors = 0 on Controller**: This is the most important rule in Jenkins. The Controller must never run builds.
2.  **Tagging/Labels**: Over-tag your nodes. Instead of just `linux`, use `linux, ubuntu, 22.04, docker-host, x86_64`. This gives pipelines granular routing control.
3.  **Colocation**: Keep your Controller and your primary Agent fleets in the same local network / VPC to ensure low latency and zero egress fees.

## ⚖️ Trade-offs
*   **Single Controller (Many Agents) vs Multiple Controllers**: A single controller is easy to maintain but forms a massive Single Point of Failure. Multiple controllers (Controller-per-Team) contain the blast radius but require mature IaC to manage configuration drift.

## 💼 Interview Q&A
*   **Q**: We have 500 static agents. The Jenkins Controller UI is extremely slow, and CPU usage is constantly at 95%. No builds are currently running. What is the architecture flaw?
*   **A**: The Controller is suffering from **Remoting Ping Exhaustion**. Managing 500 static TCP connections requires the Controller to constantly spawn threads to send and receive heartbeat pings to ensure the nodes are alive. To resolve this, we should transition from static agents to dynamic/ephemeral agents (e.g., Kubernetes or EC2 Auto Scaling) so that the Controller only manages agents when there is actual work to do in the queue.

## 🧩 Practice Problems
1.  Navigate to "Manage Jenkins" -> "Nodes". Configure the `Built-In Node` to have 0 executors.
2.  Inspect the "Node Monitors" configuration page. Identify the thresholds for Disk Space, Temp Space, and Response Time.
