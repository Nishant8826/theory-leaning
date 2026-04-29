# 🚀 Stage Execution and Parallelism

## 📌 Topic Name
Pipeline Concurrency: Parallel Stages, Threads, and Synchronization

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Running multiple jobs at the same time to make the build finish faster.
*   **Expert**: Pipeline parallelism is orchestrated by the Controller's CPS engine using **Flyweight Threads**. The `parallel` directive forks the execution graph, allowing independent stages to request distinct Executors (Agents) concurrently. A Staff engineer must navigate the complexities of **Thread Starvation**, **Workspace Contention** (if parallel branches share a node), and the **Fail-Fast** directive to optimize wall-clock time without deadlocking the infrastructure.

## 🏗️ Mental Model
Think of a Pipeline as a **Manufacturing Assembly Line**.
- **Sequential**: Build Frame -> Install Engine -> Paint Car. (Takes 3 hours).
- **Parallel**: Build Frame -> (Install Engine AND Paint Doors AND Stitch Seats simultaneously) -> Final Assembly. (Takes 1.5 hours).
- **The Catch**: You need more workers (Executors) and more space (Workspaces) at the same time. If you only have 2 workers, trying to do 3 things in parallel means one task still waits in the queue.

## ⚡ Actual Behavior
- **Flyweight Threads**: When you declare 5 parallel branches, the Controller spawns 5 lightweight CPS threads to track them.
- **Node Allocation**: If `parallel` is inside a `node` block, all branches execute on the SAME physical machine and share the SAME workspace folder. If they write to the same file concurrently, data corruption occurs.
- **Fail Fast**: By default, if one parallel branch fails, the others continue running until completion. `failFast true` kills the sibling branches immediately to save resources.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **DAG (Directed Acyclic Graph)**: Jenkins models parallel execution as a DAG. The visualization UI (Blue Ocean) renders this graph.
2.  **Thread Locality**: Groovy variables defined *outside* the parallel block are shared across all branches. Variables defined *inside* are thread-local.
3.  **Synchronization**: Standard Java synchronization (`synchronized(this)`) is **dangerous** and often banned by the CPS engine because holding a lock across a thread pause (e.g., during an `sh` step) will freeze the Controller.

## 🔁 Execution Flow
1.  **Main Thread**: Pipeline reaches `parallel` block.
2.  **Fork**: Controller creates CPS threads for Branch A, B, and C.
3.  **Scheduling**: Branch A requests a Linux node, B requests Windows, C requests Mac.
4.  **Execution**: The branches run concurrently on different agents.
5.  **Join**: The Main Thread pauses and waits for A, B, and C to complete.
6.  **Aggregation**: Once all return, Main Thread resumes.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Controller Memory**: Massive parallel matrices (e.g., testing 10 OSs against 10 browser versions = 100 branches) consume massive CPS heap space and can crash the UI when it tries to render 100 blocks.
- **Executor Exhaustion**: A parallel block requesting 10 nodes will immediately consume 10 executors from the queue. If everyone does this, the queue backs up instantly.

## 📐 ASCII Diagrams (MANDATORY)
```text
                  [ STAGE: SETUP ]
                         |
           +-------------+-------------+ (Fork)
           |             |             |
      [ TEST UI ]   [ TEST API ]  [ TEST DB ]  <-- (Parallel Branches)
       (Node A)      (Node B)      (Node C)
           |             |             |
           +-------------+-------------+ (Join)
                         |
                 [ STAGE: DEPLOY ]
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent none // Do not allocate a top-level node
    stages {
        stage('Parallel Testing') {
            failFast true // If one fails, kill the others
            parallel {
                stage('Unit Tests') {
                    agent { label 'linux' }
                    steps { sh 'make test-unit' }
                }
                stage('Integration Tests') {
                    agent { label 'linux' }
                    steps { sh 'make test-int' }
                }
                stage('Windows Tests') {
                    agent { label 'windows' }
                    steps { bat 'make.bat test' }
                }
            }
        }
    }
}
```

## 💥 Production Failures
1.  **Workspace Overwrite (Race Condition)**: Two parallel stages execute inside the same `node{}` block. Stage A runs `npm run test`, which modifies `package-lock.json`. Stage B runs `npm run lint` and tries to read the same file. The file is corrupted, and builds fail randomly. **Solution**: Use `dir('subfolder') {}` to isolate workspaces.
2.  **The Matrix DDOS**: A developer configures a `matrix` directive with 5 dimensions, resulting in 200 parallel builds. The Jenkins queue is flooded, starving all other teams for hours.
3.  **UI Hang**: Opening the classic Jenkins UI for a build with 50 parallel branches causes the browser to freeze because it tries to render thousands of HTML DOM elements for the visual pipeline graph.

## 🧪 Real-time Q&A
*   **Q**: How can I limit parallel execution so I don't hog all executors?
*   **A**: You can use the `lock` step (Lockable Resources plugin) to throttle concurrency, or write a custom Groovy script using the `collate` method to chunk tasks into batches of 5.
*   **Q**: Can I dynamically generate parallel stages?
*   **A**: In Scripted pipeline, yes (using a `Map` of closures). In Declarative, you must use the `matrix` directive for dynamic generation.

## ⚠️ Edge Cases
*   **Log Interleaving**: In older Jenkins versions, console output for parallel stages was a garbled mess. Modern Jenkins uses `Block` scoping to keep logs separate, but reading the raw text log file on disk will still show interleaved lines.

## 🏢 Best Practices
1.  **Agent None**: Always use `agent none` at the top of a pipeline if you use parallelism, and allocate agents *inside* the parallel stages. This prevents tying up a "Master" executor just to sit and wait.
2.  **Use `failFast`**: Turn this on by default to save compute resources unless you strictly need to know the result of every single test suite regardless of peers.
3.  **Isolate State**: Treat parallel branches as completely independent functions. Never rely on one branch setting a variable that another branch reads.

## ⚖️ Trade-offs
*   **Wall-Clock Time vs Queue Wait Time**: Highly parallel builds finish faster *if* the infrastructure is idle. If the infrastructure is busy, a parallel build just sits in the queue longer, offering zero overall speedup while adding overhead.

## 💼 Interview Q&A
*   **Q**: You have a Declarative Pipeline with a `parallel` block containing 3 stages. However, they seem to be running sequentially, one after the other. What is the most likely cause?
*   **A**: The most likely cause is that all 3 stages require a specific node label (e.g., `agent { label 'mac' }`), but there is only **1 Executor** available with that label. The Controller correctly spawns the 3 parallel threads, but the Scheduler forces them to queue up and execute sequentially on that single available executor.

## 🧩 Practice Problems
1.  Write a Scripted Pipeline that dynamically takes a list of 5 URLs and creates parallel stages to `curl` each one simultaneously.
2.  Simulate a "Fail Fast" scenario: Create 3 parallel stages. Make one `sleep 5` and then `exit 1`. Make the others `sleep 60`. Observe how the long-running ones are aborted.
