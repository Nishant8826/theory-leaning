# ⚙️ Jenkins Remoting Protocol

## 📌 Topic Name
Jenkins Remoting: The RPC Backbone of Distributed Execution

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: The way the Jenkins server talks to its worker machines.
*   **Expert**: Jenkins Remoting is a bidirectional, custom **Remote Procedure Call (RPC)** protocol. It allows the Controller JVM to serialize Java closures (`Callable` objects), transmit them over a network channel (TCP, WebSocket, or SSH), and execute them inside an Agent JVM. It relies heavily on **Java Serialization**. A Staff engineer understands that this chatty protocol is highly sensitive to network latency and packet loss, and represents a significant security attack surface if exposed to untrusted networks.

## 🏗️ Mental Model
Think of Remoting as a **Teleportation Device for Code**.
- The Controller has a piece of logic: "I want to delete a file named `temp.txt`."
- Instead of sending a bash command (`rm temp.txt`), it packages the actual Java Bytecode that knows how to delete a file.
- It "teleports" (serializes) this Bytecode over the wire.
- The Agent catches it, unpacks it into its own JVM, and runs it locally.
- The result (Success/Exception) is teleported back.

## ⚡ Actual Behavior
- **Bidirectional**: The Controller can call the Agent, but the Agent can also call back to the Controller (e.g., to fetch a credential or write to the master log).
- **Classloading over the Wire**: If the Agent receives a `Callable` but doesn't have the Java `.class` definition for it, the Agent will literally *ask* the Controller to stream the bytecode over the network, dynamically loading the class into the Agent JVM.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Channel**: The logical connection between Controller and Agent. It multiplexes multiple concurrent RPC calls over a single underlying TCP connection.
2.  **Serialization (ObjectOutputStream)**: The native Java mechanism used to turn objects into byte streams. Historically, this has been a massive source of CVEs (Remote Code Execution vulnerabilities) because maliciously crafted byte streams could execute arbitrary code upon deserialization.
3.  **JNLP (Java Network Launch Protocol)**: The legacy name for inbound agents. Modern Jenkins uses a proprietary TCP protocol (often port 50000) or WebSockets multiplexed over HTTP port 8080.

## 🔁 Execution Flow (Executing a Shell Command)
1.  **Controller**: Evaluates a pipeline step: `sh 'ls -la'`.
2.  **Serialization**: Instantiates a `ProcStarter` Java object and implements it as a `Callable`.
3.  **Transmission**: Sends the serialized object over the TCP Channel.
4.  **Deserialization**: Agent receives the bytes and recreates the `ProcStarter` object.
5.  **Execution**: Agent executes the OS-level shell process.
6.  **I/O Routing**: The Agent intercepts `stdout` from the shell and streams it back over the Channel to the Controller.
7.  **Return**: Process exits, Agent sends the exit code back.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Network Bandwidth**: Moving massive artifacts via Remoting (e.g., `stash`/`unstash`) is highly inefficient and saturates the TCP window. Always use S3/Artifactory instead.
- **Latency Amplification**: Because of "Classloading over the Wire," a high-latency connection (e.g., Controller in US, Agent in Asia) will cause a build to take 10x longer, not just because data transfer is slow, but because the JVM is waiting for hundreds of round-trips just to load classes.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ CONTROLLER JVM ]                          [ AGENT JVM ]
      |                                          |
 [ Callable ]                                    |
      |--(1) Serialize to Bytes                  |
      |                                          |
      +========== [ TCP CHANNEL ] ==============>+
                                                 |
                                     (2) Deserialize
                                                 |
                                     (3) Need Class Def?
      +<========= [ TCP CHANNEL ] ===============+
      |
 (4) Stream Bytecode
      +========== [ TCP CHANNEL ] ==============>+
                                                 |
                                     (5) Execute Code
                                                 |
      +<========= [ TCP CHANNEL ] ===============+ (6) Return Result
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// Under the hood, this Pipeline step relies entirely on Remoting.
node('linux-agent') { // Establishes context on the Agent JVM
    
    // The Controller packages this command and sends it via RPC
    def output = sh(script: 'uname -a', returnStdout: true).trim()
    
    // The result is sent back over the RPC channel to the Controller memory
    echo "Agent OS: ${output}" 
}
```

## 💥 Production Failures
1.  **The "Ping Timeout"**: A heavily loaded agent stops responding to TCP Keep-Alive pings because its JVM is paused doing Garbage Collection. The Controller assumes the agent is dead, closes the channel, and aborts a 3-hour build at the 99% mark.
2.  **Serialization Errors**: A pipeline tries to pass a non-serializable object (like an open Database Connection or a complex Regex Matcher) from the Controller out to a node block. The system crashes with `NotSerializableException`.
3.  **High Latency Crawl**: An agent in Sydney connects to a Controller in London (250ms ping). A build that takes 1 minute locally takes 45 minutes on the agent because every logging statement and class load requires a 250ms round trip.

## 🧪 Real-time Q&A
*   **Q**: Should I use JNLP (TCP 50000) or WebSockets?
*   **A**: Use **WebSockets**. It routes over the standard HTTP(S) port (443/8080), meaning you don't have to open special firewall ports or configure complex Load Balancer TCP listeners.
*   **Q**: Can I run Remoting over the public internet?
*   **A**: Absolutely not, unless wrapped in TLS (WebSockets over HTTPS). Unencrypted Remoting traffic can be intercepted and easily manipulated to gain Root access to your controller.

## ⚠️ Edge Cases
*   **Workspace Archiving**: When you click "Archive Artifacts", Jenkins uses Remoting to copy the file from the Agent disk to the Controller disk. For a 5GB Docker image, this will destroy your network performance.

## 🏢 Best Practices
1.  **Keep Agents Close**: Deploy Agents in the same Cloud Region/VPC as the Controller to ensure sub-millisecond latency.
2.  **Enable WebSockets**: Simplify your network topology by tunneling Remoting through HTTPS.
3.  **Offload Heavy Data**: Do not use Remoting for data transfer. Have the agent push directly to S3/Nexus using CLI tools.

## ⚖️ Trade-offs
*   **RPC Architecture**: Allows for incredibly tight integration and complex logic execution, but creates extreme sensitivity to network stability compared to a "dumb" messaging queue architecture.

## 💼 Interview Q&A
*   **Q**: A build is running on an agent. The network cable connecting the agent and the controller is temporarily unplugged for 2 minutes and then plugged back in. What happens to the build?
*   **A**: The build will fail. The Jenkins Remoting protocol relies on a persistent, stateful TCP connection. When the connection drops, the TCP socket is closed. Jenkins cannot "reconnect" to a running process. The Controller marks the agent offline, aborts the job, and the Agent's Process Tree Killer kills the orphaned build processes.

## 🧩 Practice Problems
1.  Use `tcpdump` or Wireshark to capture traffic on port 50000 between a Controller and an Agent to see the binary RPC protocol in action.
2.  Configure a Jenkins agent to connect using WebSockets instead of the dedicated TCP port.

---
Prev: [06_Plugin_System.md](../Core/06_Plugin_System.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [08_System_Performance_Limits.md](../Core/08_System_Performance_Limits.md)
---
