# 🚀 Pipeline State and Checkpointing

## 📌 Topic Name
Pipeline State: CPS Serialization, Survivability, and Checkpoints

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: If Jenkins reboots while a job is running, the job remembers where it was and keeps going.
*   **Expert**: This survivability is achieved via the **Continuation Passing Style (CPS)** engine. Every time a pipeline hits a blocking step (like `sh`, `sleep`, or `input`), the CPS engine pauses the thread, serializes the entire Groovy variable scope (the "continuation") to an XML file (`program.dat`), and frees the CPU. Upon controller restart, Jenkins deserializes `program.dat` into heap memory and resumes execution. However, this serialization requires every object to implement `java.io.Serializable`. For true "rollback" capabilities, CloudBees Enterprise offers the Checkpoint plugin, though OSS relies on declarative `restartFromStage`.

## 🏗️ Mental Model
Think of the CPS Engine as playing a **Video Game with Auto-Save**.
- **Playing (Executing)**: You are running around doing things (Groovy code).
- **Entering a Boss Fight (Step Execution)**: Right before you enter the boss room (execute `sh 'make'`), the game saves your entire inventory and health to the memory card (`program.dat`).
- **Power Outage (Controller Crash)**: The console loses power.
- **Booting Up**: The console reads the memory card. You spawn right outside the boss room with the exact same inventory you had.

## ⚡ Actual Behavior
- **Survivable Network Drops**: If the Controller restarts, the Agent might finish the `sh` command while the Controller is down. When the Controller boots up, it reconnects to the Agent, asks "How did that command go?", receives the exit code, and resumes the script.
- **Restart from Stage (Declarative)**: Jenkins keeps a historical record of the pipeline AST execution. You can click "Restart from Stage X", and Jenkins will re-run the pipeline from that point, injecting the previously saved environment variables.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **`program.dat` and `flowNodeStore/`**: For every pipeline run, Jenkins writes a binary file (`program.dat`) representing the heap state, and multiple XML files (`flowNodeStore`) tracking the DAG execution history (every step is a "Node").
2.  **`stash` and `unstash`**: Used to save file state (workspaces) across nodes. Files are zipped on Agent A, sent over Remoting, saved on the Controller disk, and then sent to Agent B. *Warning: Stashing large binaries will crash the Controller.*
3.  **Kryo Serialization**: Jenkins uses the River/Kryo serialization libraries to handle the complex graph of Groovy objects.

## 🔁 Execution Flow (Controller Restart Scenario)
1.  **Pipeline**: Hits `sh 'long-compile.sh'`.
2.  **Save**: CPS Engine writes `program.dat` to disk.
3.  **RPC**: Sends command to Agent.
4.  **Crash**: Controller process `kill -9`.
5.  **Agent**: Continues compiling, finishes, buffers output, waits for Controller.
6.  **Boot**: Controller starts, reads `$JENKINS_HOME/jobs/.../builds/.../program.dat`.
7.  **Reconnect**: Controller establishes Remoting channel to Agent.
8.  **Sync**: Agent flushes buffered logs and exit code to Controller. Pipeline resumes.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Extreme Disk I/O**: The constant serialization of `program.dat` is why Jenkins requires high IOPS SSDs. If a pipeline has a loop executing 1,000 tiny `echo` steps, it will write to disk 1,000 times.
- **Heap Bloat**: If a developer loads a 100MB string into a local variable, that 100MB is serialized to disk and held in the heap, causing massive memory bloat.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ CONTROLLER (CPS Engine) ]                [ AGENT (Executor) ]
               |                                        |
      (Groovy Variable X=1)                             |
               |                                        |
  [ BLOCKING STEP: sh 'make' ]                          |
               |                                        |
  1. Serialize Heap to Disk (program.dat)               |
               |                                        |
  2. Send RPC Command ------------------------>  [ Execute 'make' ]
               |                                        |
  3. CONTROLLER CRASHES (Power off)            [ Still executing... ]
               X                                        |
                                               [ Process Exits (0) ]
                                               [ Buffers Logs ]
               |                                        |
  4. CONTROLLER RESTARTS                                |
               |                                        |
  5. Deserialize program.dat into Heap                  |
               |                                        |
  6. Reconnect to Agent ---------------------->  [ Send Buffered Logs ]
               | <-----------------------------  [ Send Exit Code 0 ]
  7. Resume Pipeline Execution                          |
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent none
    stages {
        stage('Build') {
            agent { label 'linux' }
            steps {
                sh 'echo "Compiling code..." > binary.bin'
                // Save the file state to the Controller
                stash name: 'compiled-bin', includes: 'binary.bin' 
            }
        }
        stage('Test') {
            // Might run on a completely different physical machine
            agent { label 'linux' } 
            steps {
                // Retrieve the file state from the Controller
                unstash 'compiled-bin' 
                sh 'cat binary.bin'
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The "Unstash OOM"**: A developer uses `stash` to save a 5GB Docker tarball. When the `stash` step runs, the Controller tries to stream 5GB into memory and write it to its own local disk. The JVM throws `OutOfMemoryError` and crashes the entire CI/CD platform. **Solution**: Use S3/Artifactory for artifacts. `stash` is only for tiny text files.
2.  **NotSerializableException**: Attempting to pass a `java.util.regex.Matcher` object across a step boundary causes the CPS serialization to fail.

## 🧪 Real-time Q&A
*   **Q**: Does Jenkins OSS have Checkpoints?
*   **A**: No. The `checkpoint` step is a paid feature of CloudBees CI. It allows a pipeline to completely halt, free up all executors, and then be manually "resumed" weeks later. OSS only has "Restart from Stage," which just re-runs the code from that point using the original git commit.

## ⚠️ Edge Cases
*   **Agent Reboot**: If the *Agent* reboots during an `sh` step, the process dies. The Controller will see the TCP connection drop, mark the build as failed, and will *not* auto-resume it. Survivability only applies to the Controller.

## 🏢 Best Practices
1.  **Avoid Stash**: Never stash anything larger than 5MB. Use external storage for artifacts.
2.  **Keep Variables Small**: Nullify large strings (`myBigString = null`) before hitting a blocking step like `sh` or `sleep` so they are garbage collected and not serialized to `program.dat`.
3.  **Idempotent Stages**: Design stages so that if you use "Restart from Stage," they don't break (e.g., use `CREATE IF NOT EXISTS` instead of `CREATE`).

## ⚖️ Trade-offs
*   **Survivability vs Performance**: The CPS engine provides unmatched resilience against Controller crashes, but the cost is terrible disk I/O performance and confusing serialization errors for developers.

## 💼 Interview Q&A
*   **Q**: A pipeline takes a local variable `List data = []`, appends 100,000 items to it, and then calls `sleep 10`. What is the impact on the Jenkins Controller?
*   **A**: Because `sleep` is a blocking Pipeline step, the CPS engine will serialize the entire local scope to disk to survive a potential restart. The `data` list containing 100,000 items will be serialized via Kryo, written to `program.dat`, and held in the JVM Heap. This creates unnecessary CPU overhead, Disk I/O, and Heap bloat. The list should be cleared before the `sleep` step.

## 🧩 Practice Problems
1.  Write a script that creates a 10MB text file, stashes it, unstashes it in a new stage, and verify the file transfer. Check the Controller's disk at `$JENKINS_HOME/jobs/` to find the stash archive.
2.  Trigger a long `sh 'sleep 60'` command and manually restart the Jenkins service (`systemctl restart jenkins`). Verify the job resumes successfully.

---
Prev: [05_Stage_Execution_and_Parallelism.md](../Pipelines/05_Stage_Execution_and_Parallelism.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [07_Long_Running_Pipelines.md](../Pipelines/07_Long_Running_Pipelines.md)
---
