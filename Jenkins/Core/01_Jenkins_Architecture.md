# 🏗️ Jenkins Architecture

## 📌 Topic Name
Jenkins Architecture: Control Plane, Data Plane, and Monolithic Roots

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Jenkins is a central server that tells other servers (agents) what code to build.
*   **Expert**: Jenkins is a **JVM-based Monolith** built heavily on the **Stapler web framework** and **Guice DI**. It operates a tightly coupled **Control Plane (Controller)** that manages HTTP requests, the build queue, Jenkinsfile CPS (Continuation Passing Style) execution, and agent lifecycle. The **Data Plane (Agents/Executors)** handles actual process execution. Communication relies on the **Jenkins Remoting Protocol**, a custom Java serialization over TCP/WebSocket. Because the controller is monolithic, everything from Web UI rendering to pipeline JVM state runs in the same heap space, creating complex scaling limits.

## 🏗️ Mental Model
Think of Jenkins as an **Air Traffic Control Tower (Controller)** managing **Airplanes (Agents)**.
- **The Tower**: Takes incoming flight plans (Webhooks/Git), calculates routes (Pipelines), tracks weather (Queue), and issues commands to planes.
- **The Planes**: Simply follow orders. They take off, fly, and land (execute `npm install` or `docker build`).
- **The Vulnerability**: If the Tower's radio breaks, all planes fly blind. If the Tower's radar (Heap) is overwhelmed, no new flights can be scheduled.

## ⚡ Actual Behavior
- **Controller-bound Execution**: The "Pipeline" script (Groovy) does NOT execute on the Agent. The script executes on the Controller inside the **CPS engine**. Only the `node{}` block steps (like `sh`, `bat`) are serialized and executed on the Agent via RPC.
- **State Persistence**: The Controller constantly flushes pipeline state to disk (XML files) to survive crashes. This makes disk I/O a primary bottleneck.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Stapler**: Jenkins uses Stapler to map URLs to Java objects. Every job, build, and folder is a Java object in memory, accessible via a specific URI.
2.  **Jenkins Remoting**: A bidirectional RPC protocol. The Controller serializes a Java closure, sends it over a TCP socket to the Agent, the Agent executes it, and sends the result back.
3.  **XStream**: Jenkins uses XStream to serialize Java objects to XML. Every configuration change and pipeline state is saved as XML on the Controller's disk.

## 🔁 Execution Flow
1.  **Trigger**: GitHub sends an HTTP POST Webhook to `hostname/github-webhook/`.
2.  **Routing**: Stapler parses the URL and passes the payload to the Git plugin.
3.  **Scheduling**: The Controller adds a "Build Task" to the Queue.
4.  **Allocation**: The Scheduler assigns the task to a free Executor on an Agent.
5.  **Execution**: The Controller executes the CPS Groovy script. When it hits an `sh 'npm build'` step, it sends an RPC call to the Agent.
6.  **I/O Streaming**: The Agent streams `stdout`/`stderr` back to the Controller over the Remoting channel, which writes it to the Controller's disk.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Memory (Heap)**: Every active build, queue item, and loaded plugin resides in the Controller's heap. Large logs or massive pipelines cause Garbage Collection (GC) pauses.
- **Disk I/O**: High IOPS required. The Controller synchronously writes build logs, pipeline checkpoints, and XML configurations to `$JENKINS_HOME`.
- **Threads**: Jenkins spawns multiple threads per running pipeline on the Controller. Long-running pipelines consume threads, leading to thread exhaustion.

## 📐 ASCII Diagrams (MANDATORY)
```text
      [ WEB UI / REST API ] (Stapler)
               |
+--------------+--------------+
|     JENKINS CONTROLLER      | (JVM Heap)
|  [ Queue ]   [ CPS Engine ] |
|  [ XML Config ] [ Plugins ] |
+--------------+--------------+
      | (Remoting RPC) |
  [ TCP/WS ]      [ TCP/WS ]
      |                |
[ AGENT A ]      [ AGENT B ] (Executors)
 (Node.js)        (Docker)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// Pipeline Execution Model
pipeline {
    agent any // Tells Controller to find an Executor
    stages {
        stage('Build') {
            steps {
                // This 'echo' runs on the Controller (CPS), output sent to log
                echo "Starting build..." 
                // This 'sh' sends an RPC call to the Agent to execute a shell process
                sh "npm run build"
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The "Slow Disk" Death**: Controller is placed on cheap HDD or low-IOPS EBS. Build logs back up in memory because they can't be flushed to disk fast enough. The JVM Heap fills up, causing an `OutOfMemoryError`.
2.  **Thread Exhaustion**: Thousands of pipelines are "waiting" (e.g., `input` steps or `sleep`). Each consumes a thread/memory on the Controller. System becomes unresponsive.
3.  **Remoting Disconnects**: Network latency between Controller and Agent causes the TCP connection to drop. Jenkins marks the Agent offline and aborts running builds, even if the actual `sh` command on the agent was succeeding.

## 🧪 Real-time Q&A
*   **Q**: Why doesn't Jenkins just send the whole Jenkinsfile to the agent?
*   **A**: Because Jenkins pipelines are designed to survive Controller restarts (CPS). The Controller must maintain the exact state of the Groovy execution. If it ran on the agent, a controller restart would lose track of the build.

## ⚠️ Edge Cases
*   **Fat Workspaces**: If a job archives huge artifacts directly through the Controller (instead of offloading to S3), the Controller's network interface and disk get saturated.
*   **Plugin Conflicts**: Two plugins bundle different versions of the same Java library (e.g., Jackson). Classloader isolation mitigates this, but global leakage still happens, causing `NoSuchMethodError`.

## 🏢 Best Practices
1.  **Controller is for Control**: Never execute builds on the Controller (Executors = 0).
2.  **High IOPS**: Mount `$JENKINS_HOME` on Provisioned IOPS NVMe/EBS SSDs.
3.  **Log Offloading**: Don't keep years of build logs in Jenkins. Push them to Elasticsearch/CloudWatch and delete old builds.

## ⚖️ Trade-offs
*   **Monolith vs Microservices**: Jenkins is easy to deploy (just a `.war` file) because it's a monolith, but incredibly difficult to scale horizontally because state is tightly coupled to disk and memory.

## 💼 Interview Q&A
*   **Q**: How would you troubleshoot a Jenkins Controller that is completely unresponsive to the Web UI, but builds are still running on the agents?
*   **A**: This is classic **Thread Exhaustion or GC Thrashing**. The Web UI (Stapler) requires threads to serve HTTP requests. I would SSH into the controller instance, take a Thread Dump (`jstack <pid>`), and look for threads blocked on Disk I/O or waiting for locks. I'd also check GC logs to see if it's doing "Stop-the-World" pauses continuously trying to free heap space.

## 🧩 Practice Problems
1.  Use `jstack` on a running Jenkins instance to identify the HTTP listener threads.
2.  Inspect the `$JENKINS_HOME/jobs/<job-name>/builds/` directory to see how build state and logs are persisted to XML/log files.
