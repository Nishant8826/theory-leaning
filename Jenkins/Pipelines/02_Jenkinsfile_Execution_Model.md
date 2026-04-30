# 🚀 Jenkinsfile Execution Model

## 📌 Topic Name
The CPS Engine: Controller execution vs Agent execution

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: The code in the Jenkinsfile runs on the Jenkins server, but the commands run on the agents.
*   **Expert**: The Jenkins Pipeline execution model is highly non-intuitive. The entire Groovy script inside the `Jenkinsfile` executes **strictly on the Controller** inside the **Continuation Passing Style (CPS)** engine. The Controller acts as an orchestrator. When it encounters a Step (like `sh`, `bat`, `git`), it pauses the Groovy execution, serializes the command via the Remoting Protocol, sends it to the Agent, waits for the result, and then resumes the Groovy script. Understanding this Controller/Agent split is critical for preventing JVM exhaustion and security breaches.

## 🏗️ Mental Model
Think of the Jenkinsfile as a **Construction Manager (Controller)** talking to a **Robot Worker (Agent)** via a Walkie-Talkie.
- **The Blueprint (Jenkinsfile)**: Held entirely by the Manager in the office.
- **Groovy Logic (if/else, loops)**: The Manager thinking and making decisions in the office.
- **Steps (`sh 'build'`)**: The Manager using the walkie-talkie to say, "Robot, hit this nail with a hammer."
- The Robot hits the nail, says "Done," and waits. The Robot *never* sees the blueprint.

## ⚡ Actual Behavior
- **Flyweight Executors**: The Groovy script evaluation uses a lightweight thread on the Controller. It does not consume a regular build executor.
- **Serialization**: Every time a pipeline pauses (e.g., entering an `sh` step or a `sleep`), the entire state of the Groovy variables is serialized to disk (`program.dat`). If Jenkins reboots, it reads this file and resumes exactly where it left off.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **CPS (Continuation Passing Style)**: A programming style where control is explicitly passed in the form of a continuation. Jenkins transforms your normal Groovy bytecode into CPS bytecode. This allows the JVM to pause the thread, serialize the local variables, and free up the CPU thread for other tasks.
2.  **Non-Serializable Objects**: Because the state must be written to disk, any variable you define in your script MUST implement `java.io.Serializable`. If you open a Database Connection or a Java `Matcher` object and try to pass it across a step, Jenkins will crash.
3.  **The `@NonCPS` Annotation**: Used to bypass the CPS transformation for specific methods. These methods execute purely in standard Groovy, meaning they run very fast, but they *cannot* contain Jenkins steps (like `sh`) and will be lost if the server reboots.

## 🔁 Execution Flow
1.  **Start**: Controller begins reading the `Jenkinsfile`.
2.  **Controller Execution**: Evaluates `def myVar = "Hello"`. (Runs on Controller).
3.  **Agent Allocation**: Reaches `node('linux')`. Controller asks Scheduler for an agent.
4.  **RPC Call**: Reaches `sh "echo ${myVar}"`. Controller substitutes the variable, sends the literal string `echo Hello` over the network to the agent.
5.  **Agent Execution**: Agent forks a shell, runs `echo Hello`, streams logs back.
6.  **Resumption**: Agent returns exit code `0`. Controller CPS engine wakes up and continues the script.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Controller CPU**: Parsing large JSON files or doing complex math inside the Jenkinsfile (using Groovy) burns the Controller's CPU, not the Agent's.
- **Controller I/O**: Every step execution causes the CPS engine to write state to disk. A pipeline with 10,000 tiny `sh` steps will destroy the Controller's disk IOPS.

## 📐 ASCII Diagrams (MANDATORY)
```text
    [ CONTROLLER (CPS Engine) ]                [ AGENT (Executor) ]
               |                                        |
  def x = 1 (Executes on Controller)                    |
               |                                        |
  node('linux') { ------------------ (Allocates) ----> [ Node Context ]
               |                                        |
      x = x + 1 (Executes on Controller)                |
               |                                        |
      sh "make"  -----(RPC 'make')-------------------> [ bash: make ]
               | <---(Streams Logs & Exit Code)-------  |
               |                                        |
  } -------------------------------- (Releases) ----> [ Node Context ]
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent { label 'worker' }
    stages {
        stage('Demo') {
            steps {
                script {
                    // DANGER: This loops 10,000 times ON THE CONTROLLER
                    // This generates 10,000 discrete RPC calls to the agent
                    // and 10,000 disk writes for CPS state saving.
                    for (int i = 0; i < 10000; i++) {
                        sh "echo ${i}" 
                    }

                    // CORRECT WAY: Let the Agent do the looping
                    sh '''
                        for i in {1..10000}; do
                            echo $i
                        done
                    '''
                }
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The "NotSerializableException"**: A user writes a groovy script that instantiates a `java.util.regex.Matcher` and then calls `sh`. Because the `Matcher` object is in the local scope, the CPS engine tries to save it to disk. `Matcher` is not serializable. The pipeline crashes.
2.  **Controller DDOS via Groovy**: A pipeline downloads a 500MB JSON file via `sh` into the workspace, then uses `readFile()` to pull it into a Groovy variable, and `JsonSlurper` to parse it. This loads 500MB of data directly into the Controller's JVM Heap, causing an immediate OOM crash.

## 🧪 Real-time Q&A
*   **Q**: Can I write files to the Agent using Groovy's `File` class?
*   **A**: No! `new File('/tmp/x').write('data')` will execute on the Controller and write to the Controller's disk! To write to the Agent, you must use the Jenkins `writeFile` step or an `sh` command.
*   **Q**: When should I use `@NonCPS`?
*   **A**: When iterating over complex data structures or parsing JSON/XML where you need standard JVM performance and don't need to call Jenkins steps (like `sh` or `echo`) inside the method.

## ⚠️ Edge Cases
*   **`readFile` vs `sh(..., returnStdout: true)`**: Both pull data from the Agent into the Controller's memory. Use with extreme caution on large outputs.

## 🏢 Best Practices
1.  **Keep Groovy Simple**: The Jenkinsfile should be an orchestrator, not a build script. Put complex logic in `Makefile`, `package.json`, or bash scripts executed via `sh`.
2.  **Avoid Controller-Side Iteration**: Do not use Groovy `each` or `for` loops to execute thousands of `sh` steps. Let the agent's shell handle iterations.

## ⚖️ Trade-offs
*   **CPS Engine**: Provides incredible survivability (Jenkins can reboot and pipelines resume without losing state), but imposes massive performance penalties and confusing serialization rules on developers.

## 💼 Interview Q&A
*   **Q**: A developer complains that their pipeline takes 10 minutes to parse a log file. They are using Groovy's `readFile()` and iterating through the lines in a `for` loop. How do you fix it?
*   **A**: The issue is that they are pulling the file into the Controller's memory and using the CPS engine to iterate, which adds massive overhead. I would fix it by moving the log parsing logic entirely to the Agent. I would have them write a `grep`, `awk`, or Python script, and execute it using a single `sh` step.

## 🧩 Practice Problems
1.  Write a script that intentionally throws a `NotSerializableException` by instantiating a non-serializable Java object right before a `sleep 1` step.
2.  Compare the execution time of a Groovy `for` loop executing 100 `sh 'true'` steps vs a single `sh` step containing a bash `for` loop.

---
Prev: [01_Declarative_vs_Scripted.md](../Pipelines/01_Declarative_vs_Scripted.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [03_Groovy_Sandbox.md](../Pipelines/03_Groovy_Sandbox.md)
---
