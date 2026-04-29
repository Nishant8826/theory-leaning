# 📊 JVM Troubleshooting

## 📌 Topic Name
Deep JVM Diagnostics: Thread Dumps, Heap Dumps, and JFR

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Taking an x-ray of the Jenkins server when it's frozen to see exactly which piece of code is stuck.
*   **Expert**: When Jenkins experiences catastrophic performance degradation (UI freezes, 100% CPU, OutOfMemoryErrors), restarting the service destroys the evidence. A Staff engineer relies on low-level JDK tooling—**Thread Dumps (jstack)**, **Heap Dumps (jmap)**, and **Java Flight Recorder (JFR)**—to perform post-mortem or real-time diagnostics. These tools allow you to inspect the exact line of Java/Groovy code executing on every thread, identify memory leaks by inspecting object references, and profile lock contention within the CPS engine.

## 🏗️ Mental Model
Think of a Thread Dump as a **Crime Scene Photograph**.
- **The Crime**: Jenkins UI is frozen. Nobody can log in.
- **The Wrong Move**: Rebooting the server. (Washing away the fingerprints).
- **The Right Move (Thread Dump)**: Taking a high-resolution photograph of everyone in the building at that exact millisecond.
- **The Analysis**: You look at the photo and see 200 threads (people) all standing in line waiting for 1 thread who is struggling to read a massive XML file. You found the bottleneck.

## ⚡ Actual Behavior
- **Thread Blockage**: Jenkins uses a finite thread pool for HTTP requests (Jetty/Winstone). If a plugin makes a synchronous HTTP call to an external API (like GitHub) and that API hangs, the Jenkins thread hangs. If 50 users click that button, all 50 Jetty threads hang. The UI is now frozen.
- **Garbage Collection (GC) Thrashing**: If the JVM heap is full, the JVM stops all application threads ("Stop The World") to run GC. If GC only recovers 1% of memory, it immediately runs again. CPU hits 100%, but no actual work is being done.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **`jstack` (Thread Dumps)**: A JDK CLI tool. Prints the stack trace of every thread in the JVM. Look for threads in `BLOCKED` or `WAITING` states, and trace them back to the specific Jenkins plugin class (e.g., `org.jenkinsci.plugins...`).
2.  **`jmap` (Heap Dumps)**: Dumps the entire contents of RAM to a binary `.hprof` file. You load this file into a tool like Eclipse MAT to see exactly which Java Objects are consuming the most space (e.g., a massive `java.util.HashMap` storing millions of pipeline logs).
3.  **`java.lang.OutOfMemoryError: Heap space`**: If this occurs, the JVM terminates. You must configure the JVM flag `-XX:+HeapDumpOnOutOfMemoryError` so it automatically takes a picture *before* it dies.

## 🔁 Execution Flow (Diagnosing a Frozen UI)
1.  **Alert**: PagerDuty fires: "Jenkins UI Unreachable".
2.  **Investigate**: SSH into Controller. Run `top`. See Jenkins at 100% CPU.
3.  **Thread Dump**: Run `jstack -l <PID> > threaddump.txt`.
4.  **Analyze**: Open `threaddump.txt`. Search for `Winstone Request handling`.
5.  **Discovery**: Find 100 threads blocked at `hudson.plugins.git.GitSCM.checkout()`.
6.  **Root Cause**: The Git server is down, and the plugin has no timeout configured. The threads are waiting indefinitely for a network socket.
7.  **Mitigation**: Restart Jenkins, update the Git plugin timeout settings.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Heap Dump Penalty**: Running `jmap` on a 16GB JVM will freeze the JVM entirely for 10-30 seconds while it writes 16GB of data to the hard drive. Use with extreme caution in production.
- **Disk IO**: Ensure the partition where the Heap Dump is written has enough free space (equal to the JVM max heap size), or the server OS will crash.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINS JVM ]
   |
   +-- Thread 1 (RUNNABLE): Executing Groovy Loop
   |
   +-- Thread 2 (BLOCKED): Waiting for Lock A  <---\
   |                                               | (Deadlock)
   +-- Thread 3 (BLOCKED): Holding Lock A,         |
                           Waiting for Lock B  ----/

[ DIAGNOSTICS COMMANDS ]
$ jcmd <PID> Thread.print > threads.txt
$ jmap -dump:format=b,file=heap.hprof <PID>
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```bash
# Production JVM Startup Flags (Add to JAVA_OPTS)
# These are MANDATORY for enterprise Jenkins deployments
JAVA_OPTS="-Xms8g -Xmx8g \
  # Use the modern G1 Garbage Collector
  -XX:+UseG1GC \
  # Take a heap dump automatically if Jenkins crashes from OOM
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/var/jenkins_home/logs/ \
  # Log garbage collection events to analyze GC thrashing
  -Xlog:gc*=info,file=/var/jenkins_home/logs/gc.log:time,uptime:filecount=5,filesize=10M"
```

## 💥 Production Failures
1.  **The Plugin Deadlock**: Team installs a new plugin. Two hours later, Jenkins freezes. Thread dump reveals a classic Java deadlock: Thread A locks Resource 1 and waits for Resource 2. Thread B locks Resource 2 and waits for Resource 1. Neither can proceed. Jenkins must be forcefully killed.
2.  **CPS Object Leak**: Pipelines start failing with OOM. A heap dump analysis in Eclipse MAT reveals that the `org.jenkinsci.plugins.workflow.cps.CpsThreadGroup` object is retaining 6GB of memory. A developer wrote a recursive Groovy function that the CPS engine couldn't properly garbage collect, blowing up the heap.
3.  **The Infinite Fast-Throw**: The logs are filled with empty `NullPointerException` stack traces. The JVM optimizes exceptions thrown frequently by hiding the stack trace to save CPU. This makes debugging impossible. **Solution**: Use `-XX:-OmitStackTraceInFastThrow`.

## 🧪 Real-time Q&A
*   **Q**: Can I get a thread dump without SSHing into the server?
*   **A**: Yes, go to `http://<jenkins>/threadDump`. However, if the HTTP worker threads are completely exhausted (which is often the case during an outage), the web page won't load, and you *must* use SSH and `jstack`.
*   **Q**: What is JFR (Java Flight Recorder)?
*   **A**: A low-overhead profiling tool built into the JVM. It records CPU, memory, and thread events continuously to a ring buffer. If Jenkins crashes, you can dump the JFR file and analyze it in JDK Mission Control to see exactly what happened in the 5 minutes leading up to the crash.

## ⚠️ Edge Cases
*   **Containerized Jenkins**: If Jenkins is running in a Docker/Kubernetes container, you must `kubectl exec` into the container to run `jstack`. Ensure the base image has a full JDK installed, not just a JRE, or the diagnostic tools will be missing.

## 🏢 Best Practices
1.  **Always Dump Before Restart**: Never restart a misbehaving Jenkins server without taking a Thread Dump first. You are destroying the only data that can prevent it from happening again.
2.  **Pre-Allocate Heap**: Set `-Xms` (Initial Heap) equal to `-Xmx` (Max Heap). This prevents the JVM from wasting CPU dynamically resizing the heap during peak load.
3.  **Use Eclipse MAT**: Don't try to read a Heap Dump with a text editor. Use the Eclipse Memory Analyzer Tool to automatically find the "Leak Suspects" and trace the GC Roots.

## ⚖️ Trade-offs
*   **Deep Monitoring vs Performance**: Enabling detailed JVM profiling (like continuous JFR) adds a slight overhead to the application (1-2%). In massive Jenkins instances, this is a highly worthwhile trade-off for the diagnostic power it provides.

## 💼 Interview Q&A
*   **Q**: Jenkins is currently unresponsive. The CPU is at 100%. The UI times out. You SSH into the Linux box. Walk me through the exact commands you run to find the root cause before restarting the service.
*   **A**: First, I run `top -H -p <Jenkins_PID>` to see the CPU usage of individual Java threads. I convert the PID of the highest CPU thread to hexadecimal. Second, I run `jstack -l <Jenkins_PID> > threaddump.txt`. Third, I open `threaddump.txt`, search for that hexadecimal thread ID, and look at its Java stack trace. This will instantly tell me if a specific plugin (e.g., regex parsing in the log plugin) is stuck in an infinite loop consuming the CPU. Only after securing this file would I restart the service.

## 🧩 Practice Problems
1.  Go to `Manage Jenkins` -> `System Information` -> `Thread Dump`. Look at the output and identify the `Jetty` threads that are handling HTTP requests.
2.  Look up the Java options your Jenkins is currently running with. Verify if `-XX:+HeapDumpOnOutOfMemoryError` is enabled.
