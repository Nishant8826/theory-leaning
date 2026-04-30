# 🚀 Long Running Pipelines

## 📌 Topic Name
Managing Long Running Pipelines: Input, Milestones, and Resource Starvation

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Jobs that wait for human approval or run for days can block other jobs from running.
*   **Expert**: Long-running pipelines expose the flaws in thread and executor allocation. The `input` step pauses execution waiting for human intervention, but if configured poorly, it holds an Executor slot and a workspace hostage for days, starving the queue. A Staff engineer uses `agent none`, `milestone` for concurrency control, and timeouts to ensure that long-running deployments (e.g., multi-region rollout over 48 hours) do not consume physical compute resources or create "Zombie" builds.

## 🏗️ Mental Model
Think of a Pipeline as a **Customer in a Restaurant**.
- **Eating (Executing)**: The customer is actively using a table (Executor).
- **Waiting for a friend (Input Step)**: The customer stops eating, but refuses to leave the table for 3 hours. Other customers (Jobs) line up outside because the tables are full.
- **The Solution (`agent none`)**: The customer leaves the table, goes to the bar (Flyweight Thread on Controller), and only asks for a table again when their friend arrives.

## ⚡ Actual Behavior
- **The `input` Step**: By default, `input` pauses the pipeline. If this step occurs *inside* a `node` or `agent` block, the Executor on that physical agent remains locked in a `Busy` state, doing absolutely nothing, until a human clicks "Proceed".
- **The `milestone` Step**: A built-in concurrency control. It ensures older builds do not overwrite newer builds. If Build 2 reaches Milestone A before Build 1 does, Build 1 is automatically aborted.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Flyweight Threads**: When an `input` step is reached *outside* a node block, the CPS engine serializes the state to disk, releases the Flyweight thread, and effectively consumes zero CPU/RAM while waiting.
2.  **Thread Starvation**: If thousands of pipelines are paused on `input` steps *inside* node blocks, the entire Jenkins cluster's executor pool is exhausted. No new PRs can be tested.
3.  **Timeouts**: The `timeout` step wraps a block of code and spawns a background Watcher Thread. If the timer expires, the Watcher throws a `org.jenkinsci.plugins.workflow.steps.FlowInterruptedException`, aborting the pipeline gracefully.

## 🔁 Execution Flow (Proper `input` usage)
1.  **Pipeline Start**: `agent none` is declared.
2.  **Build Stage**: `agent { label 'docker' }` allocated. Build runs. Agent released.
3.  **Approval Stage**: (No agent allocated). Reaches `input 'Deploy to Prod?'`.
4.  **Suspension**: Pipeline serializes state and sleeps. Zero executors used.
5.  **Human Action**: User clicks 'Proceed' in the UI.
6.  **Resume**: Pipeline wakes up.
7.  **Deploy Stage**: `agent { label 'docker' }` allocated. Deploy runs.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Executor Exhaustion**: The most common and devastating failure mode of long-running pipelines.
- **Log Rotation Prevention**: If a build runs for 30 days, Jenkins cannot delete its workspace or rotate its logs, potentially causing Disk Space alerts.

## 📐 ASCII Diagrams (MANDATORY)
```text
❌ BAD DESIGN (Holds Executor Hostage) ❌
[ NODE ALLOCATED ] -----------------------------------------------> [ NODE RELEASED ]
   |                                                                    |
[ sh 'build' ] ----> [ input 'Wait for QA' (2 DAYS) ] ----> [ sh 'deploy' ]
                     (Executor sits idle 100% of the time)

✅ GOOD DESIGN (Releases Compute) ✅
[ NODE ] ---> [ RELEASED ]       (Flyweight)        [ NODE ] ---> [ RELEASED ]
   |              |                   |                 |              |
[ sh 'build' ] ---+       [ input 'Wait for QA' ]       +--- [ sh 'deploy' ]
                          (Zero Executors used)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent none // CRITICAL: Start with no agent
    options {
        // Abort the build if it takes longer than 2 hours total
        timeout(time: 2, unit: 'HOURS') 
    }
    stages {
        stage('Build') {
            agent { label 'linux' }
            steps { sh 'make build' }
            // Agent is automatically released here
        }
        stage('Production Approval') {
            steps {
                // Executes on Controller flyweight thread. No Executor wasted.
                timeout(time: 1, unit: 'DAYS') {
                    input message: 'Deploy to Production?', submitter: 'release-managers'
                }
            }
        }
        stage('Deploy') {
            agent { label 'linux' }
            steps { sh 'make deploy' }
        }
    }
}
```

## 💥 Production Failures
1.  **The Friday Afternoon Freeze**: A team triggers 50 deployments on Friday at 4 PM. The pipelines all hit an `input` step asking for QA approval. The QA team goes home. 50 Executors are locked all weekend. On Saturday, an emergency hotfix cannot run because the queue is starved.
2.  **Out of Order Deployments**: Build #10 takes 30 minutes to build. Build #11 takes 5 minutes. Build #11 deploys v2.0 to Production. Then Build #10 finishes and deploys v1.0, downgrading production. **Solution**: Use `milestone`.

## 🧪 Real-time Q&A
*   **Q**: How does `milestone` prevent out-of-order deployments?
*   **A**: By inserting `milestone(1)` after the build stage and `milestone(2)` after the deploy stage. If Build #11 passes `milestone(1)`, and then Build #10 arrives at `milestone(1)`, Jenkins aborts Build #10.
*   **Q**: Can I time out an `input` step without failing the build?
*   **A**: Yes, you can wrap the `input` in a `try/catch` block, catch the `FlowInterruptedException`, and set `currentBuild.result = 'SUCCESS'` (or `ABORTED`), allowing the pipeline to exit cleanly instead of failing.

## ⚠️ Edge Cases
*   **Workspace Loss**: If you use `agent none` and release the executor during the `input` step, the Deploy stage will likely run on a *different* agent. The workspace from the Build stage is gone. You MUST use external storage (Artifactory, Docker Registry) to move artifacts between these stages, NOT `stash`.

## 🏢 Best Practices
1.  **Never put `input` inside an `agent` block**.
2.  **Always wrap `input` in a `timeout`**. A build should never wait infinitely.
3.  **Disable Concurrent Builds**: For deployment pipelines, use `options { disableConcurrentBuilds() }` to ensure deployments queue up sequentially rather than race each other.

## ⚖️ Trade-offs
*   **Interactive vs Automated**: Requiring human input increases safety but destroys CI/CD metrics (Lead Time for Changes) and complicates pipeline state management.

## 💼 Interview Q&A
*   **Q**: A pipeline takes a database backup, waits for a DB Admin to click "Approve", and then runs a migration. How do you ensure the workspace containing the backup script isn't lost while waiting, without locking an executor?
*   **A**: You cannot rely on the Jenkins workspace. The backup script and any state must be packaged and pushed to a remote repository (like S3 or Artifactory) during the first stage. After the `input` step passes, the second stage (which may run on a completely different agent) will pull the script/state from S3 and execute it.

## 🧩 Practice Problems
1.  Write a pipeline with `agent any` at the top. Add an `input` step. Run the job and observe in the Jenkins UI that an executor is actively consumed. Rewrite it with `agent none` to fix it.
2.  Create a pipeline with two milestones. Start Build 1, let it sleep. Start Build 2, let it pass Milestone 1. Observe Build 1 being automatically aborted.

---
Prev: [06_Pipeline_State_and_Checkpointing.md](../Pipelines/06_Pipeline_State_and_Checkpointing.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [01_Git_Integration.md](../SCM/01_Git_Integration.md)
---
