# ⚙️ Agents and Executors

## 📌 Topic Name
Jenkins Agents & Executors: The Execution Data Plane

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Agents are the machines where your builds actually run. Executors are the "slots" on those machines.
*   **Expert**: The Jenkins execution model strictly separates the Control Plane from the Data Plane. **Agents (Nodes)** are JVM processes (`remoting.jar`) running on separate OS instances. **Executors** are independent threads running within an Agent's JVM that fetch tasks from the Controller's Queue. Communication relies on the **Remoting Protocol**, which transmits serialized Java objects (closures) over a bi-directional TCP channel. A Staff engineer optimizes agent topology to avoid network saturation, manage JVM lifecycle via inbound/outbound connection methods (JNLP vs SSH), and isolate build environments.

## 🏗️ Mental Model
Think of the Controller as a **Restaurant Manager** and Agents as the **Kitchens**.
- **Agents (Kitchens)**: Physical spaces where work happens (Linux VM, Kubernetes Pod).
- **Executors (Stoves)**: The physical capacity. If a kitchen has 4 stoves, it can cook 4 meals concurrently. If all stoves are full, new orders wait in the Queue.
- **Remoting (Waitstaff)**: The waitstaff carry instructions (Recipes/Closures) from the Manager to the Kitchen, and bring back status updates (Logs).

## ⚡ Actual Behavior
- **Dumb Agents**: The Agent JVM (`agent.jar`) has very little logic. It simply accepts bytecode from the Controller, executes it, and streams `stdout`/`stderr` back.
- **Workspace Affinity**: When an executor finishes a build, it keeps the Workspace files on disk. Subsequent builds on the *same* agent/executor can reuse the `.git` cache or `node_modules`, dramatically speeding up builds.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Remoting Protocol (TCP)**: A custom RPC protocol. It can run over direct TCP, HTTP/WebSocket (JNLP), or SSH tunnels.
2.  **Inbound vs. Outbound**:
    - **Inbound (JNLP/WebSocket)**: The Agent initiates the connection to the Controller (useful when Agents are behind a NAT/Firewall).
    - **Outbound (SSH)**: The Controller initiates the connection to the Agent (useful for static internal VMs).
3.  **Process Tree Killer**: When a build aborts, Jenkins must kill all child processes (e.g., a background Tomcat server spawned by a shell script). It injects unique environment variables (`BUILD_ID`) and uses OS-level process tree scanning to find and `kill -9` orphans.

## 🔁 Execution Flow
1.  **Queue**: Controller places a `Queue.Task` in the queue.
2.  **Match**: Scheduler finds an Idle Executor on an Agent with matching `labels`.
3.  **Lease**: The Executor is leased, changing status to `Busy`.
4.  **RPC**: Controller serializes the build steps (e.g., `FilePath.act()`) and sends it over the Remoting channel.
5.  **Execution**: Agent executes the process (forks `bash` or `cmd.exe`).
6.  **Streaming**: Agent continuously streams the output buffer over TCP to the Controller.
7.  **Cleanup**: Process completes, Controller updates XML state, Executor returns to `Idle`.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Agent Memory**: The `agent.jar` JVM only needs ~256MB. The actual build processes (Webpack, Maven, Docker) consume the OS memory.
- **Network Saturation**: Streaming massive artifacts or huge logs back to the Controller can saturate the network interface of both the Agent and the Controller.
- **Disk I/O**: Compiling code causes massive random I/O. Using SSDs for Agent workspaces is critical.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINS CONTROLLER ]
        |
   (Queue / Scheduler)
        |
  [ REMOTING CHANNEL ] <--- (TCP / WebSocket / SSH) --->
        |
+------------------------------------------------------+
| [ AGENT JVM (agent.jar) ]                            |
|                                                      |
|  [ Executor 1 ] ---> (Forks) ---> [ /bin/bash ]      |
|                                         |            |
|  [ Executor 2 ] ---> (Forks) ---> [ docker build ]   |
|                                                      |
|  [ WORKSPACE DISK ( /var/jenkins_home/workspace ) ]  |
+------------------------------------------------------+
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// Pipeline demonstrating executor allocation
pipeline {
    // Controller evaluates this to find a matching agent
    agent { label 'linux && x86_64' } 
    stages {
        stage('Run') {
            steps {
                // This command executes on the allocated Executor
                sh '''
                    echo "Running on executor: $EXECUTOR_NUMBER"
                    echo "Workspace path: $WORKSPACE"
                    sleep 60
                '''
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The "Workspace Leak"**: A build runs `npm install`, generating 200,000 files. The build finishes, but the workspace isn't cleaned up. After 10 builds, the Agent disk hits 100% and crashes. **Solution**: Use `cleanWs()` in a `post` block.
2.  **Remoting Timeout (Ping Failure)**: A heavy build (e.g., compiling a massive C++ binary) starves the OS of CPU. The `agent.jar` JVM doesn't get enough CPU time to respond to the Controller's "Ping". Controller assumes Agent is dead and aborts the build. **Solution**: Increase Ping Timeout or ensure Agent has sufficient CPU overhead.
3.  **Process Leaks**: A build script starts a daemon `nohup my-daemon &`. The build finishes, but the Process Tree Killer fails to kill it. Over time, the Agent is saturated with zombie daemons.

## 🧪 Real-time Q&A
*   **Q**: How many executors should I run per Agent?
*   **A**: The golden rule is **1 Executor per physical CPU core**. If you have an 8-core VM, configure 8 executors. Over-provisioning leads to severe context-switching and thrashing during heavy compile jobs.
*   **Q**: What is a "Heavyweight" vs "Flyweight" executor?
*   **A**: "Heavyweight" is a normal executor on an agent. "Flyweight" is a special hidden executor on the Controller used exclusively to run Pipeline `stage` and `node` allocation logic without consuming a real build slot.

## ⚠️ Edge Cases
*   **Cross-OS Pathing**: An agent running Windows and an agent running Linux will have different path separators (`\` vs `/`). Writing Pipeline code that assumes `/tmp` exists will fail on Windows agents.
*   **Offline Agents**: If an Agent goes offline *during* a build, the build is immediately aborted. It will NOT automatically resume on another agent.

## 🏢 Best Practices
1.  **Use Dynamic Agents**: Prefer Kubernetes Pods or EC2 Auto Scaling over static VMs. Ephemeral agents ensure a pristine build environment every time.
2.  **Isolate Workloads**: Tag agents meticulously (e.g., `label 'gpu-build'`, `label 'ios-build'`).
3.  **Never Use Master Executor**: Always set `# of executors = 0` on the `Built-In Node` (the Controller) to prevent builds from crashing the control plane.

## ⚖️ Trade-offs
*   **Static vs Ephemeral Agents**:
    *   *Static (VMs)*: Faster builds due to persistent caches (`.m2`, `.npm`), but high risk of environment drift and "it works on my agent" bugs.
    *   *Ephemeral (K8s/Docker)*: Perfectly reproducible builds, but slower execution due to downloading dependencies from scratch every time (unless external caching is implemented).

## 💼 Interview Q&A
*   **Q**: You have a Jenkins setup where builds randomly abort with `java.nio.channels.ClosedChannelException`. What is happening?
*   **A**: This indicates the TCP connection between the Controller and the Agent was severed. This is usually caused by network latency, an overly aggressive firewall dropping "idle" connections, or the Agent JVM experiencing a massive Garbage Collection pause (OOM) that prevents it from responding to remoting pings. I would check the Agent JVM memory and network routing.

## 🧩 Practice Problems
1.  Configure a Jenkins Agent via SSH, then manually kill the SSH connection on the OS level and observe how the Controller reacts.
2.  Write a Pipeline that utilizes a specific `label` to run on one agent, and use the `stash`/`unstash` commands to move a file to a different agent.

---
Prev: [02_Controller_Internals.md](../Core/02_Controller_Internals.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [04_Queue_and_Scheduler.md](../Core/04_Queue_and_Scheduler.md)
---
