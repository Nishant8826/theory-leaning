# 📊 Log Aggregation

## 📌 Topic Name
Log Aggregation: System Logs, Pipeline Logs, and Splunk/ELK Integration

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Collecting all the text output from Jenkins and the builds and sending it to a central search engine so you don't have to click through the UI to read errors.
*   **Expert**: Jenkins produces two distinct streams of telemetry: **System Logs** (Tomcat/Jetty, plugin errors, Remoting failures) and **Build Logs** (the `stdout`/`stderr` of pipeline executions). In a distributed environment, navigating to individual build URLs or SSHing into the Controller to grep `/var/log/jenkins/jenkins.log` is an anti-pattern. A Staff engineer implements decoupled log forwarding—streaming both System and Build logs directly into an aggregation platform (ELK, Splunk, Datadog)—enabling centralized alerting, correlation of agent disconnects with pipeline failures, and long-term compliance retention.

## 🏗️ Mental Model
Think of Log Aggregation as a **Court Reporter and a Filing Room**.
- **Without Aggregation**: Every time a trial (Build) happens, the transcript is left on the judge's desk in that specific courtroom. If you want to find out who lied in a trial 3 months ago, you have to walk to 50 different courtrooms.
- **With Aggregation**: The court reporter (Log Forwarder) instantly types the transcript and wires it to a massive, indexed filing room (Elasticsearch). You can sit at a computer, search the word "Exception", and see every trial across the country where it was said.

## ⚡ Actual Behavior
- **System Logs**: Jenkins uses `java.util.logging` (JUL). By default, these write to the local filesystem. They contain critical data like JVM crashes, LDAP auth failures, and Git timeout errors.
- **Pipeline Logs**: Streamed from the Agent over the Remoting channel to the Controller, which saves them as flat text files in `$JENKINS_HOME/jobs/.../builds/X/log`.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Filebeat/Fluentd Sidecars**: The most robust way to aggregate System Logs is to run a log shipper on the Controller OS. It tails `/var/log/jenkins/jenkins.log` and ships it over HTTPS.
2.  **Logstash/Splunk Plugins**: Instead of waiting for the Controller to write the pipeline log to disk, plugins like `logstash` can intercept the log stream inside the Jenkins JVM and transmit it directly to the aggregator in real-time.
3.  **JSON Formatting**: Plain text logs are difficult to query. Advanced setups configure Jenkins to output logs in structured JSON format, injecting metadata like `build_number`, `job_name`, and `agent_name` into every log line.

## 🔁 Execution Flow (Pipeline Log Forwarding)
1.  **Execution**: Agent runs `sh 'npm install'`.
2.  **Streaming**: Agent sends `stdout` string to Controller via TCP.
3.  **Interception**: Controller JVM receives the string. The Logstash Plugin intercepts it.
4.  **Enrichment**: Plugin adds `{"job": "frontend", "build": 42}`.
5.  **Transmission**: Plugin sends HTTP POST / UDP packet to Logstash server.
6.  **Indexing**: Elasticsearch indexes the log line.
7.  **Disk Write**: Controller writes the original string to the local disk (fallback).

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Plugin Overhead**: Intercepting and formatting every single line of a 50MB build log inside the Controller JVM adds significant CPU overhead.
- **Network Saturation**: Streaming logs for 100 concurrent builds directly from the JVM to an external SIEM can saturate the Controller's outbound network interface.

## 📐 ASCII Diagrams (MANDATORY)
```text
   [ JENKINS AGENT ] 
          | (Remoting stream)
          v
[ JENKINS CONTROLLER JVM ]
    |                |
    | (1) System     | (2) Pipeline
    |     Logs       |     Logs
    v                v
[ /var/log/ ]    [ Logstash Plugin ]
    |                |
[ Fluentd ]          | (HTTP/UDP)
    |                |
    +-------+--------+
            |
            v
   [ ELASTICSEARCH / SPLUNK ]
            |
    [ KIBANA DASHBOARD ]
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// Example: Sending specific pipeline data to ELK
pipeline {
    agent any
    options {
        // Automatically sends the entire build log to Logstash 
        // (Requires Logstash plugin configured globally)
        logstash() 
    }
    stages {
        stage('Build') {
            steps {
                sh 'make build'
            }
        }
    }
    post {
        failure {
            // Sending a custom structured event upon failure
            script {
                def payload = """{"event": "build_failed", "job": "${env.JOB_NAME}", "commit": "${env.GIT_COMMIT}"}"""
                sh "curl -X POST -H 'Content-Type: application/json' -d '${payload}' https://logstash.corp.com/jenkins"
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The Silent OOM Crash**: Jenkins goes offline. You SSH into the server, but the `jenkins.log` file is truncated or corrupted because the JVM crashed violently. If you don't have remote log aggregation, the final error message is lost forever.
2.  **The "No Space Left" Log Bloat**: You configure Jenkins to log `java.net` networking debug logs to trace a bug. You forget to turn it off. In 12 hours, the log file hits 50GB, the disk fills up, and Jenkins crashes.
3.  **SIEM DDOS**: A pipeline contains a bug: `cat /dev/urandom`. It generates 10GB of random text per second. The Logstash plugin dutifully streams all of it to your corporate Splunk cluster, maxing out your Splunk ingestion license for the month in 5 minutes ($10,000 mistake).

## 🧪 Real-time Q&A
*   **Q**: Can I stop Jenkins from writing pipeline logs to its local disk to save space?
*   **A**: Native Jenkins fundamentally relies on writing logs to disk. While plugins exist to redirect output, completely disabling local disk logs often breaks the Jenkins UI (Blue Ocean) because it expects to read the file from `$JENKINS_HOME`.
*   **Q**: How do I trace why an agent disconnected?
*   **A**: You must correlate the Agent's local OS logs (`/var/log/messages` or Docker container logs) with the Controller's System Logs to see which side dropped the TCP connection.

## ⚠️ Edge Cases
*   **Multi-line Stack Traces**: Java exceptions span multiple lines. If your log forwarder isn't configured for multiline processing (e.g., matching the regex `^Caused by:`), Elasticsearch will parse a 50-line stack trace as 50 separate, meaningless log events.

## 🏢 Best Practices
1.  **Decouple Log Shipping**: Prefer running an OS-level agent (Filebeat/FluentBit) to tail the log files rather than using Jenkins plugins to send HTTP requests. If Jenkins is struggling with CPU, you don't want it wasting cycles formatting JSON logs.
2.  **Structured Logging**: Configure Jenkins to use Logback or JSON formatters for the System logs to make Kibana parsing trivial.
3.  **Log Rotation**: Always configure `logrotate` on the Jenkins Linux OS to compress and delete `/var/log/jenkins/jenkins.log` daily.

## ⚖️ Trade-offs
*   **Inline Plugins vs OS Forwarders**:
    *   *Plugins*: Easy to setup, injects Jenkins context automatically, but adds JVM overhead.
    *   *OS Forwarders*: Zero JVM overhead, highly resilient, but harder to correlate specific log lines to specific Pipeline builds without complex regex parsing.

## 💼 Interview Q&A
*   **Q**: Developers complain that randomly, 1 out of 50 builds fail with an "Agent disconnected" error. Looking at the build log gives no clues. How would you investigate this using a centralized logging platform?
*   **A**: An agent disconnect is usually a symptom of a deeper infrastructure issue, not a pipeline bug. I would open our SIEM (e.g., Kibana) and query the **Jenkins System Logs** around the exact timestamp of the failure. I would search for the Agent's name and look for "Ping Timeout" or "EOFException". Simultaneously, I would query the **Kubernetes/EC2 infrastructure logs** for that specific Agent node to see if the Kubelet logged an `OOMKilled` event or if AWS triggered an instance termination. Aggregation allows me to correlate the Jenkins application failure with the underlying infrastructure event.

## 🧩 Practice Problems
1.  SSH into your Jenkins Controller. Find the location of the system logs (`/var/log/jenkins/jenkins.log` or `journalctl -u jenkins`). `tail -f` the log and click around the UI to watch events stream in.
2.  Navigate to "Manage Jenkins" -> "System Log" -> "Add new log recorder". Create a custom logger for `hudson.plugins.git` to debug Git checkout issues.
