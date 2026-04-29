# ⚙️ Queue and Scheduler

## 📌 Topic Name
Jenkins Queue and Scheduler: Backpressure and Task Allocation

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: When you start a job, it goes into a line (Queue) until a server is free to run it.
*   **Expert**: The Jenkins Queue is a complex, in-memory **state machine** managing `Queue.Item` objects. The Scheduler evaluates these items against node availability, labels, and concurrent build restrictions. It is the primary mechanism for handling **Backpressure**. When the system is overloaded, the Queue absorbs the shock, but if it grows too large, the Controller's heap is exhausted. A Staff engineer understands how queue states (Waiting, Blocked, Buildable) transition and how to debug scheduler deadlocks.

## 🏗️ Mental Model
Think of the Jenkins Queue as a **Busy Airport Taxi Stand**.
- **The Passengers (Jobs)**: Arrive and take a ticket.
- **The Dispatcher (Scheduler)**: Looks at the passenger's needs ("I need a minivan" -> `label 'linux-docker'`).
- **The Taxis (Executors)**: Pull up. The Dispatcher assigns the right passenger to the right taxi.
- **Backpressure**: If 10,000 passengers arrive and there are only 5 taxis, the line (Queue) wraps around the block. The Dispatcher (Controller CPU) spends all its energy just managing the line, eventually collapsing.

## ⚡ Actual Behavior
- **Queue Coalescing**: If a job is triggered 5 times in rapid succession while sitting in the queue, Jenkins will often "collapse" (coalesce) them into a single run to save resources.
- **Quiet Period**: A configurable delay before a task actually enters the queue, allowing for SCM coalescing (e.g., waiting for a developer to finish pushing multiple commits).

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Queue Task Lifecycle**:
    - **Waiting**: In the Quiet Period.
    - **Blocked**: Cannot run because a concurrent build of the same job is running, or it's locked by a plugin.
    - **Buildable**: Ready to run, waiting for a matching executor.
    - **Left**: Task is assigned to an executor and removed from the queue.
2.  **Maintainer Thread**: A background thread in the Controller (`hudson.model.Queue.MaintainerTask`) that wakes up periodically (default 5s) to evaluate the queue and assign tasks to idle executors.
3.  **Consistent Hashing**: Used in some modern scheduler plugins to assign jobs to specific nodes to maximize workspace cache hits.

## 🔁 Execution Flow
1.  **Trigger**: Webhook initiates a build.
2.  **Item Creation**: A `Queue.WaitingItem` is created and placed in memory.
3.  **Quiet Period**: Item transitions to `Queue.BuildableItem`.
4.  **Scheduler Loop**: The Maintainer Thread scans all `BuildableItems`.
5.  **Label Matching**: Scheduler cross-references the job's `NodeLabel` with all connected Agents' labels.
6.  **Allocation**: Finds an Agent with an `Idle` executor.
7.  **Hand-off**: The item becomes a `Run` (e.g., `WorkflowRun`), is handed to the Executor, and removed from the Queue.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **CPU Spikes**: If you have 500 items in the queue and 1,000 agents, the Scheduler thread must perform an $O(N \times M)$ evaluation every few seconds. This causes massive CPU spikes on the Controller.
- **Memory Consumption**: Every queued item is an object in the JVM heap. A queue of 50,000 items will trigger continuous GC cycles.
- **Disk I/O**: The Queue state is periodically written to disk (`$JENKINS_HOME/queue.xml`) so it survives a controller restart.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ TRIGGERS ] ---> (Quiet Period) ---> [ THE QUEUE ]
                                          |
                                   (Maintainer Thread)
                                          |
                                 +--------+--------+
                                 |                 |
                          (Label Match?)    (Concurrency Lock?)
                                 |                 |
                             [ BUILDABLE ]     [ BLOCKED ]
                                 |
                        [ ASSIGN TO EXECUTOR ]
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// Inspecting the Queue via Script Console to debug deadlocks
import hudson.model.*

def q = Jenkins.instance.queue
println "Total Items in Queue: ${q.items.length}"

q.items.each { item ->
    println "Task: ${item.task.name}"
    println "Why stuck: ${item.why}"
    println "Since: ${new Date(item.inQueueSince)}"
    println "---"
}

// Clear the entire queue (Emergency ONLY)
// q.clear() 
```

## 💥 Production Failures
1.  **The "Queue Explosion"**: A rogue script triggers a parameterized job 100,000 times in a loop. The Controller heap fills with `Queue.Item` objects. The server throws `OutOfMemoryError` and crashes.
2.  **Scheduler Starvation**: You have one massive "Monorepo" job that triggers 50 downstream jobs. The downstream jobs require the same node label as the upstream job. The upstream job consumes all executors, meaning the downstream jobs stay in the queue forever. This is a classic **Distributed Deadlock**.
3.  **The "Offline Agent" Trap**: A job is hardcoded to `agent { label 'mac-mini-01' }`. That physical machine is turned off. The job stays in the queue as `Buildable` forever, creating visual clutter and minor CPU overhead.

## 🧪 Real-time Q&A
*   **Q**: Can I change the priority of jobs in the queue?
*   **A**: Natively, Jenkins evaluates the queue mostly in FIFO order. To change this, you MUST install the **Priority Sorter Plugin**, which allows you to define weights and priorities (e.g., Hotfix jobs jump the line).
*   **Q**: Why is my job "Pending" when there are idle executors?
*   **A**: Usually, it's either a **Label Mismatch** (the job needs `label 'linux'`, but the idle agents only have `label 'ubuntu'`), or the job has `Disable Concurrent Builds` checked and another instance is running.

## ⚠️ Edge Cases
*   **Flyweight Tasks**: Pipeline `stage` blocks execute on the Controller using "Flyweight" tasks that bypass the normal queue limits and execute immediately on hidden threads.
*   **Cloud Provisioning**: If using dynamic agents (e.g., EC2 plugin), a job entering the queue triggers an API call to AWS to launch an instance. The job remains in the queue for several minutes while the instance boots.

## 🏢 Best Practices
1.  **Monitor Queue Length**: Alert immediately if the queue length exceeds your total executor count by more than 2x for more than 10 minutes.
2.  **Avoid Hardcoding Nodes**: Never use `agent { label 'specific-machine-name' }`. Always use capabilities `agent { label 'docker && aws' }` to allow the scheduler flexibility.
3.  **Aggressive Timeout**: Use the `timeout` step in pipelines to ensure hung builds eventually die, freeing up executors.

## ⚖️ Trade-offs
*   **Quiet Period**: A long quiet period (e.g., 60s) reduces redundant builds (saving compute), but frustrates developers waiting for instant feedback.

## 💼 Interview Q&A
*   **Q**: You have 100 nodes, but the queue has 50 items stuck in it with the message "Waiting for next available executor". How do you debug this?
*   **A**: First, I use the Script Console to inspect `queue.items` and read the exact `why` reason. If it's waiting for an executor, I check the job's required labels vs. the online nodes. If the labels match, I check if the node is "Temporarily Offline" or if its disk space is below the safety threshold (Jenkins automatically takes nodes offline if `< 1GB` free). Finally, I check for concurrent build locks.

## 🧩 Practice Problems
1.  Write a Groovy script to find and cancel all items in the queue that have been stuck for more than 2 hours.
2.  Configure a job with a 30-second Quiet Period, trigger it 5 times rapidly, and observe how Jenkins coalesces them into a single build.
