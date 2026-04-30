# ⚙️ Controller Internals

## 📌 Topic Name
Jenkins Controller: The JVM Heart of CI/CD

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: The Controller is the "Server" part of Jenkins that hosts the UI and stores settings.
*   **Expert**: The Jenkins Controller is a stateful, disk-backed Java application running atop a Servlet Container (like Winstone/Jetty). It relies heavily on **XStream** for XML serialization of Java objects to disk (`$JENKINS_HOME`). It implements a massive in-memory object graph representing every Job, Run, and Node. Because it is NOT stateless, the Controller represents a single point of failure and a primary bottleneck for large-scale operations.

## 🏗️ Mental Model
Think of the Controller as a **Massive Librarian sitting at a desk with a huge notebook (Heap)** and **filing cabinets (Disk)**.
- **The Notebook**: Every currently active job, connected agent, and web user is tracked in their head/notebook.
- **Filing Cabinets**: When a job finishes, the librarian meticulously writes down the exact details in an XML file and files it away.
- **The Bottleneck**: Only this one librarian can assign tasks to workers (Agents). If the librarian is busy writing XML files or runs out of notebook paper (OOM), everything stops.

## ⚡ Actual Behavior
- **Memory Mapping**: When Jenkins starts up, it reads the XML files from `$JENKINS_HOME` and reconstructs the Java object graph in memory. A massive `$JENKINS_HOME` means agonizingly slow startup times (sometimes 30+ minutes).
- **CPS Engine**: The Continuation Passing Style engine constantly pauses running Groovy scripts, serializes their state, and writes them to disk (Program.dat) to ensure "survivability."

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Winstone / Jetty**: The embedded servlet container that listens on port 8080. It manages HTTP thread pools.
2.  **Guice Dependency Injection**: Jenkins uses a heavily modified version of Google Guice to inject plugins and core components at runtime.
3.  **ClassLoaders**: Jenkins creates a complex hierarchy of ClassLoaders to allow plugins to load independently and overwrite core behavior without crashing the JVM (mostly).
4.  **File System Locking**: Jenkins assumes exclusive access to `$JENKINS_HOME`. Running two Controllers against the same NFS mount will result in catastrophic data corruption.

## 🔁 Execution Flow (Startup Sequence)
1.  **Boot**: JVM launches `jenkins.war`.
2.  **Extraction**: Unpacks the WAR to `/var/cache/jenkins`.
3.  **Servlet Init**: Jetty starts and initializes the `Jenkins` singleton.
4.  **Plugin Load**: Reads `$JENKINS_HOME/plugins`, creates ClassLoaders, resolves dependencies.
5.  **Data Hydration**: Parses XML configurations for Jobs, Users, and Nodes into heap memory.
6.  **Ready**: Opens port 8080 to traffic and connects to Agents.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Garbage Collection (GC)**: The biggest enemy of the Controller. Parsing thousands of XML files creates massive object churn. G1GC is strictly recommended.
- **Inode Exhaustion**: Every build generates multiple small files (logs, build.xml). Jenkins can exhaust the Linux filesystem inodes before it exhausts disk space.
- **Threads**: Jetty defaults to a bounded thread pool (e.g., 100 threads). High concurrent UI traffic or webhook spam can exhaust this pool.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JVM HEAP ]
+------------------------------------------------+
|  [ Jenkins.instance ] (Singleton)              |
|       |--> [ ItemGroup (Folders) ]             |
|       |--> [ Project (Jobs) ]                  |
|       |      |--> [ Run (Builds) ]             |
|       |--> [ Computer (Agents) ]               |
|       |--> [ PluginManager ]                   |
+------------------------------------------------+
       | (XStream Serialize/Deserialize) |
+------------------------------------------------+
| [ $JENKINS_HOME ]                              |
|  /jobs/my-job/config.xml                       |
|  /jobs/my-job/builds/1/build.xml               |
+------------------------------------------------+
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// Running via Jenkins Script Console (Groovy) to inspect Heap state
import jenkins.model.Jenkins

// See how many jobs are loaded in memory
def jobCount = Jenkins.instance.getAllItems(Job.class).size()
println "Jobs in memory: ${jobCount}"

// Manually trigger Garbage Collection (Dangerous in prod, but useful for debugging)
System.gc()

// Print free memory
println "Free Memory: ${Runtime.getRuntime().freeMemory() / 1024 / 1024} MB"
```

## 💥 Production Failures
1.  **The "Startup Hang"**: Jenkins is restarted, but takes 45 minutes to boot. Why? Because the `jobs/` directory contains 50,000 old builds. Jenkins is parsing every single `build.xml` to rebuild its internal state. **Solution**: Implement strict Build Discarder policies.
2.  **OOM due to "Fat" Objects**: A plugin stores a massive JSON payload inside a `RunAction` object. Because every build's `RunAction` is kept in memory, 100 concurrent builds immediately exhaust the 8GB JVM heap.
3.  **High CPU due to Polling**: SCM polling is configured for `* * * * *` on 2,000 jobs. The Controller's CPU pegs at 100% just managing cron threads and `git ls-remote` commands, starving actual UI requests.

## 🧪 Real-time Q&A
*   **Q**: Can I run two Controllers behind a Load Balancer for High Availability?
*   **A**: **NO**. The Jenkins Controller is inherently stateful and locks `$JENKINS_HOME`. There is no native Active-Active clustering for OSS Jenkins. (CloudBees offers HA via custom clustering mechanisms, but OSS does not).
*   **Q**: What JVM arguments should I use?
*   **A**: Always use `-XX:+UseG1GC`, `-Xms` equal to `-Xmx`, and `-XX:+ExplicitGCInvokesConcurrent`.

## ⚠️ Edge Cases
*   **Zombie Threads**: A Groovy script in the Script Console contains an infinite loop (`while(true)`). It will consume a CPU thread forever until the Jenkins JVM is killed.
*   **Symlink Loops**: Placing symlinks inside `$JENKINS_HOME` that point back to parent directories will cause the startup parser to loop infinitely and crash.

## 🏢 Best Practices
1.  **Ephemeral Configuration**: Use **Configuration as Code (JCasC)** to define Controller settings so you can easily recreate the Controller if it dies.
2.  **Aggressive Log Rotation**: Keep max 10 builds per job. Use external systems for historical logs.
3.  **Tuning Heap**: Give the Controller enough RAM (8GB-32GB depending on scale), but monitor GC pause times closely.

## ⚖️ Trade-offs
*   **XStream XML vs Database**: Jenkins uses XML files so users can manually read/edit them or back them up easily via `rsync`. However, XML parsing is massively slower and more memory-intensive than using a proper relational database.

## 💼 Interview Q&A
*   **Q**: Why is Jenkins so memory hungry compared to modern CI tools like GitHub Actions?
*   **A**: Because Jenkins stores its entire configuration state, job hierarchy, and active pipeline execution state (CPS) as a massive, deeply nested object graph in the JVM Heap. Modern tools are stateless workers that write/read from an external database.
*   **Q**: Your Jenkins Controller has 0 bytes free on disk but `df -h` says there is space. What happened?
*   **A**: Inode exhaustion. Millions of tiny log files and `build.xml` files consumed all the filesystem's inodes. We need to clear out old builds or reformat the disk with a higher inode ratio.

## 🧩 Practice Problems
1.  Write a script in the Jenkins Script Console to find all jobs that do not have a "Build Discarder" configured and apply a 10-build limit.
2.  Use `jmap -histo:live <pid>` on the Controller process to identify the Java classes taking up the most heap space.

---
Prev: [01_Jenkins_Architecture.md](../Core/01_Jenkins_Architecture.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [03_Agents_and_Executors.md](../Core/03_Agents_and_Executors.md)
---
