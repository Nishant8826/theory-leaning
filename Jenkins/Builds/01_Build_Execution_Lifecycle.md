# 🔨 Build Execution Lifecycle

## 📌 Topic Name
The Build Lifecycle: Setup, Execution, and Teardown

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: A build starts, downloads code, runs commands, saves files, and cleans up.
*   **Expert**: The Jenkins build lifecycle is orchestrated by the CPS engine, moving through discrete phases: **Environment Provisioning** (Agent allocation), **SCM Acquisition**, **Task Execution** (shell steps), **Artifact Archival**, and **Teardown** (`post` blocks). A Staff engineer focuses on the strict determinism of this lifecycle, ensuring **Idempotency** (clean workspaces), proper **Exception Handling** (preventing dirty teardowns), and the asynchronous streaming of I/O back to the Controller.

## 🏗️ Mental Model
Think of the Build Lifecycle as renting a **Hotel Room**.
- **Check-in (Setup)**: You get the keys to a specific room (Agent Executor allocated).
- **Unpacking (Checkout)**: You bring your luggage in (Git Clone).
- **Activity (Build/Test)**: You do your work inside the room (`sh 'make'`).
- **Saving Souvenirs (Artifacts)**: You mail a package home so it's not lost when you leave (`archiveArtifacts`).
- **Check-out (Teardown)**: Housekeeping cleans the room (`cleanWs()`), and you hand the keys back (Executor released).

## ⚡ Actual Behavior
- **The `post` Block Guarantee**: In Declarative pipelines, the `post` block is implemented as a massive `finally` block in Java. It is practically guaranteed to run, even if the build steps throw massive exceptions, ensuring cleanup logic (like tearing down test databases) always executes.
- **Fail Fast**: If a step returns a non-zero exit code (e.g., `bash` returns `1`), the CPS engine immediately throws an `AbortException`. It halts the current stage, skips all subsequent stages, and jumps directly to the `failure` / `always` post conditions.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Environment Variables**: During Setup, Jenkins injects a massive Map of environment variables (`BUILD_NUMBER`, `WORKSPACE`, `GIT_COMMIT`) into the Agent's OS process.
2.  **Process Forking**: The `sh` step doesn't just run commands; it writes your script to a temporary file (e.g., `/tmp/jenkins-script.sh`), injects the `BUILD_ID`, and uses `Runtime.exec()` or `ProcessBuilder` to fork a new OS process to run the script.
3.  **Catching Errors**: The `catchError` and `warnError` steps manipulate the underlying `Run.Result` object without throwing an `AbortException`, allowing the pipeline to continue while marking the overall status as unstable/failed.

## 🔁 Execution Flow
1.  **Initialization**: Jenkins creates `Run` object in Heap, allocates Build Number.
2.  **Agent Binding**: Evaluates `agent` block, requests Executor, sets `$WORKSPACE`.
3.  **SCM**: Executes Git Checkout (often implicitly in Declarative).
4.  **Stages**: Sequentially evaluates `stage` blocks.
5.  **Step Execution**: Forks OS processes, streams `stdout`/`stderr` to Controller.
6.  **Status Evaluation**: Sets `currentBuild.result` to SUCCESS, FAILURE, or ABORTED.
7.  **Post Actions**: Executes `always`, `success`, `failure`, `cleanup` blocks based on the final result.
8.  **Completion**: Releases Executor, flushes final XML state to disk.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Zombie Processes**: If the build is aborted by a user clicking the "X" button, Jenkins sends a `SIGTERM` to the Agent process. If the shell script ignores it, Jenkins uses the "Process Tree Killer" to hunt down processes sharing the `BUILD_ID` environment variable and `SIGKILL`s them.
- **Log Buffering**: The Agent buffers stdout. If the build generates 1GB of text per second, it will saturate the Remoting channel and consume Agent OS memory.

## 📐 ASCII Diagrams (MANDATORY)
```text
           [ TRIGGER ]
                |
[ ALLOCATE EXECUTOR ] (Wait in Queue)
                |
[ SCM CHECKOUT ] (Network I/O)
                |
    +-----------+-----------+
    |           |           |
[ STAGE 1 ] [ STAGE 2 ] [ STAGE 3 ] (Process Forking & CPU)
    |           |           |
    +-----------+-----------+
                |
    (Exception Thrown? Yes/No)
                |
[ ARTIFACT ARCHIVAL ] (Network I/O to Storage)
                |
[ POST CONDITIONS ] (always, success, failure)
                |
[ CLEAN WORKSPACE ] (Disk I/O)
                |
[ RELEASE EXECUTOR ]
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent any
    stages {
        stage('Build and Test') {
            steps {
                // If this fails, Jenkins throws an AbortException
                sh 'make build'
                
                // We want tests to run even if some fail, but mark build UNSTABLE
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh 'make test'
                }
            }
        }
    }
    post {
        always {
            // This runs regardless of build success or failure
            echo "Archiving test reports..."
            junit 'reports/**/*.xml'
        }
        cleanup {
            // Absolute last thing to run before releasing the node
            cleanWs()
        }
    }
}
```

## 💥 Production Failures
1.  **The Silent Zombie**: A build script starts a detached background process (`nohup redis-server &`). The build finishes successfully. Because of a bug in the Process Tree Killer (or OS incompatibility), the Redis server is left running on the Agent. The next build that lands on this Agent fails because port 6379 is already in use.
2.  **The Disk Hog**: A pipeline builds a 10GB Docker image but has no `post { cleanup { cleanWs() } }` block. After 10 builds, the Agent's 100GB SSD is full, and all subsequent builds fail instantly with I/O errors.
3.  **Aborted Build Chaos**: A user aborts a build halfway through a Terraform apply. The state file is locked or corrupted because the OS process was forcefully killed (`SIGKILL`), requiring manual infrastructure intervention.

## 🧪 Real-time Q&A
*   **Q**: What is the difference between `failure` and `aborted` in the `post` block?
*   **A**: `failure` triggers when a step returns a non-zero exit code (e.g., tests fail). `aborted` triggers when a human clicks the "Stop" button or a `timeout` expires.
*   **Q**: How do I stop a failing test from killing the whole pipeline?
*   **A**: Wrap the test command in a `catchError` block, or write the shell script to always return 0 (e.g., `make test || true`), though `catchError` is the preferred Jenkins-native way.

## ⚠️ Edge Cases
*   **Controller Crash during `post`**: If the Controller crashes while executing the `post` block, when it reboots, it will generally mark the build as failed and will *not* re-run the `post` block, potentially leaving temporary infrastructure running.

## 🏢 Best Practices
1.  **Mandatory Cleanup**: Every pipeline MUST have a `post { cleanup { cleanWs() } }` block to ensure deterministic, clean environments for the next executor.
2.  **Fail Fast**: Don't waste compute time. If unit tests fail, don't run integration tests. Let the pipeline crash early.
3.  **Idempotent Shell Scripts**: Assume your `sh` scripts might be run twice or aborted halfway. Use `mkdir -p` and `rm -f`.

## ⚖️ Trade-offs
*   **Strict `post` blocks vs Scripted `try/finally`**: Declarative `post` blocks are highly readable and safer, but Scripted `try/catch/finally` gives you granular control over exactly which lines of code trigger specific rollbacks.

## 💼 Interview Q&A
*   **Q**: Your pipeline spins up a temporary database container, runs tests, and then spins it down. Occasionally, the tests fail, and the database container is left running on the agent forever. How do you fix this?
*   **A**: The spin-down logic was likely placed at the end of the `steps` block. When the tests fail, Jenkins throws an exception and skips the rest of the `steps` block. I would fix this by moving the container spin-down logic into the `post { always { ... } }` block of that specific stage, or the global `post` block, guaranteeing it runs regardless of the test outcome.

## 🧩 Practice Problems
1.  Write a Pipeline that intentionally fails in the `steps` block (`sh 'exit 1'`). Use the `post` block to print a message to the console verifying that the `post` block still executed.
2.  Use the `catchError` block around a failing shell step and observe how the stage turns yellow (Unstable) instead of red (Failed) in the Blue Ocean UI.
