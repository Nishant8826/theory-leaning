# 🔐 Audit Logs and Compliance

## 📌 Topic Name
Traceability: Audit Trail, Compliance, and Forensics

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Keeping a record of who changed what, so if the server breaks, you know who did it.
*   **Expert**: In highly regulated environments (FinTech, Healthcare), CI/CD pipelines are the gateways to Production. Compliance frameworks (SOC2, PCI-DSS) mandate strict **Non-Repudiation**. The Jenkins **Audit Trail Plugin** captures every HTTP request, configuration change, and job execution, writing them to an immutable external datastore (e.g., Elasticsearch, AWS CloudWatch). A Staff engineer configures these logs to track exactly *who* requested a change, *what* was changed, and *when*, creating an irrefutable timeline for forensic analysis during a security incident.

## 🏗️ Mental Model
Think of Audit Logging as an **Airplane Black Box**.
- **Without Audit Logs**: The plane crashes (Production goes down). You look at the rubble. You have no idea if it was pilot error, mechanical failure, or a hijacking.
- **With Audit Logs**: You retrieve the Black Box. It tells you: "At 10:04 AM, Copilot 'John' flipped the 'Deploy' switch from 'Off' to 'On'."
- **The Catch**: The Black Box must be indestructible. If the pilot can erase the Black Box, the logs are useless.

## ⚡ Actual Behavior
- **XML Diffing**: When a user clicks "Save" on a job configuration, Jenkins creates a new version of the `config.xml`. Advanced audit systems (like JobConfigHistory) store the XML diffs, allowing you to see exactly which line of the configuration was modified.
- **Log Forging**: If audit logs are simply written to `/var/log/jenkins/audit.log` on the Controller, a compromised Admin can easily `rm -f audit.log`. Audit logs MUST be streamed off-box instantly.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Servlet Filters**: The Audit Trail plugin often implements a Java Servlet Filter. It intercepts every single HTTP request hitting the Jenkins web server (Winstone/Jetty), logs the user's Session ID, the URL path, and the HTTP method (GET/POST), and then allows the request to proceed.
2.  **Syslog Forwarding**: The standard mechanism for off-box logging. Jenkins formats the audit event and sends it via UDP/TCP to a Syslog daemon (e.g., Fluentd, Splunk Universal Forwarder) running on the same OS, which securely transmits it to the SIEM.
3.  **JobConfigHistory Plugin**: Creates a hidden folder (`$JENKINS_HOME/config-history`) that acts like a local Git repository for XML files, saving every iteration.

## 🔁 Execution Flow (Malicious Config Change)
1.  **Attacker**: Logs into Jenkins UI using stolen credentials (`alice_dev`).
2.  **Action**: Navigates to `job/Prod-Deploy/configure`. Changes the deployment target. Clicks Save.
3.  **Audit Filter**: Intercepts HTTP POST. Records: `[alice_dev] POST /job/Prod-Deploy/configSubmit`.
4.  **Config History**: Saves the diff showing the target change.
5.  **Syslog Agent**: Streams the event to Splunk/Datadog.
6.  **Alerting**: SIEM triggers a P1 alert: "Prod-Deploy modified by non-admin user."

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Disk I/O Penalty**: Logging every single HTTP GET request for a busy Jenkins instance (e.g., 500 users refreshing the dashboard) will thrash the disk and bloat log files rapidly.
- **Syslog Blocking**: If the Syslog server goes down, and Jenkins is configured to block until the log is written, the entire Jenkins UI will freeze.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ USER (Alice) ]
       |
  (Clicks 'Save' on Job)
       v
[ JENKINS CONTROLLER ]
       |
       |-- 1. [ JobConfigHistory ] -> Saves XML diff to disk
       |
       |-- 2. [ Audit Trail Plugin ] -> Formats Syslog string
       |
       v
[ FLUENTD / SPLUNK FORWARDER ] (On local VM)
       |
  (Encrypted TLS Stream)
       v
[ SIEM (Datadog / Splunk) ] -> (Immutable, Alerting)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```yaml
# JCasC Configuration for Audit Trail Plugin
unclassified:
  auditTrail:
    loggers:
      - syslog:
          facility: "USER"
          messageFormat: "JENKINS_AUDIT: %user% %uri% %action%"
          syslogServerHostname: "127.0.0.1" # Send to local Fluentd agent
          syslogServerPort: 514
    pattern: ".*/(?:configure|build|configSubmit|doDelete|script).*" # Only log dangerous actions
```

## 💥 Production Failures
1.  **The "Who Did It?" Mystery**: A critical production pipeline is deleted. The team looks at the Jenkins logs. The logs only say "Job deleted." There is no Audit Trail plugin installed, so there is no record of the user session that issued the HTTP DELETE request.
2.  **Audit Log Disk Full**: The Audit plugin is misconfigured to log every single static asset load (CSS, JS, images). The `audit.log` grows to 500GB in three days, crashing the Controller due to `No space left on device`.
3.  **Compliance Audit Failure**: An auditor asks for proof that only authorized personnel deployed code in Q3. The team cannot provide logs linking specific Jenkins build executions to SSO identities, resulting in a SOC2 compliance violation.

## 🧪 Real-time Q&A
*   **Q**: Does Jenkins natively track who clicked "Build"?
*   **A**: Yes, the `CauseAction` object attached to a build shows if it was triggered by a Timer, an SCM Webhook, or a specific User ID. This is visible in the Build API.
*   **Q**: Can I use Git instead of JobConfigHistory?
*   **A**: Absolutely. Moving to GitOps (JCasC and Jenkinsfiles) is vastly superior. If your configuration is in Git, Git *is* your immutable audit trail, making the JobConfigHistory plugin obsolete.

## ⚠️ Edge Cases
*   **API Tokens**: If a script uses an API Token to trigger a build, the Audit log will record the user who *owns* the token. If multiple teams share a "service account" API token, non-repudiation is destroyed because you cannot prove which specific human ran the script.

## 🏢 Best Practices
1.  **Filter the Noise**: Configure the Audit Trail regex to only log state-changing operations (`POST`, `configure`, `delete`, `build`, `script`). Ignore `GET` requests to static assets or job dashboards.
2.  **Stream Instantly**: Never rely on local file rotation for audit logs. Stream them to a SIEM immediately.
3.  **GitOps is the Ultimate Audit**: If users cannot configure jobs in the UI, you don't need to audit UI clicks. You only need to audit Git Pull Requests.

## ⚖️ Trade-offs
*   **Comprehensive Logging vs Performance**: Logging every action guarantees a perfect forensic timeline but incurs massive I/O overhead and Splunk ingestion costs. Selective logging saves money but risks missing the specific action an attacker took.

## 💼 Interview Q&A
*   **Q**: During a post-mortem, you need to prove who executed an unauthorized system Groovy script via the `/script` console endpoint. Where do you look?
*   **A**: Native Jenkins logs do not capture this by default. I would need to look at the **Audit Trail Plugin** logs (forwarded to our SIEM) and filter for HTTP POST requests to the `/script` URI. The log payload would contain the username (extracted from the SSO session cookie) and the timestamp. If we didn't have an audit plugin, I would have to look at the Reverse Proxy (NGINX) access logs, but those might not contain the authenticated Jenkins username.

## 🧩 Practice Problems
1.  Examine the JSON API of a recent Jenkins build (`http://<jenkins>/job/<job>/<build>/api/json`). Look at the `actions` array to find the `UserIdCause` to see exactly who triggered it.
2.  Write a Regex pattern that matches Jenkins configuration URLs but ignores static asset URLs (e.g., `.png`, `.css`).
