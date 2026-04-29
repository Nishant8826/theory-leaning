# 🌳 Webhooks vs Polling

## 📌 Topic Name
Triggering Builds: Webhooks, SCM Polling, and Event-Driven CI

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: How does Jenkins know when you push code? It either asks GitHub every minute (Polling) or GitHub tells Jenkins instantly (Webhook).
*   **Expert**: The architectural shift from **SCM Polling (Pull)** to **Webhooks (Push)** is critical for scaling Jenkins. SCM Polling is a massive CPU and network drain on the Controller, requiring a dedicated cron thread pool to constantly run `git ls-remote` across thousands of repos. Webhooks invert this, making Jenkins an event-driven HTTP API. A Staff engineer designs network perimeters (API Gateways/Reverse Proxies) to securely accept GitHub/GitLab webhooks, handle CSRF protection, and validate payload signatures to prevent unauthorized build triggers.

## 🏗️ Mental Model
Think of checking for mail.
- **SCM Polling**: You walk to the mailbox at the end of the driveway every 60 seconds, open it, check if it's empty, and walk back. Exhausting and inefficient.
- **Webhooks**: The mail carrier rings your doorbell exactly when mail is delivered.

## ⚡ Actual Behavior
- **Polling Starvation**: If you have 5,000 jobs configured to poll `* * * * *` (every minute), Jenkins will spawn thousands of threads. GitHub will likely rate-limit your IP address, and your Controller CPU will hit 100%, causing the UI to become unresponsive.
- **Webhook Filtering**: When GitHub sends a webhook, Jenkins parses the JSON payload. It extracts the branch name and only triggers jobs that are configured to care about that specific branch.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **The Polling Thread Pool**: Jenkins has a specific thread pool (configurable via system properties) dedicated to polling. If there are more polling jobs than threads, jobs will queue up, and "every minute" polling might actually happen every 10 minutes.
2.  **The Webhook Endpoint**: Jenkins exposes unauthenticated (but signature-verified) endpoints, such as `https://jenkins.corp.com/github-webhook/`.
3.  **CSRF (Cross-Site Request Forgery)**: Jenkins uses "Crumb" issuers to prevent CSRF. However, Webhooks from GitHub cannot retrieve a crumb. Therefore, webhook endpoints are explicitly whitelisted to bypass CSRF checks, relying instead on HMAC cryptographic signatures for security.

## 🔁 Execution Flow (Webhook)
1.  **Developer**: Runs `git push`.
2.  **GitHub**: Sends an HTTP POST to Jenkins `/github-webhook/`. Payload contains JSON with repository, branch, and commit hash. Includes `X-Hub-Signature`.
3.  **Jenkins Network**: Reverse Proxy (NGINX) receives traffic, terminates TLS, forwards to Jenkins port 8080.
4.  **Jenkins Core**: Plugin intercepts request, bypasses CSRF, and computes HMAC hash using the shared secret.
5.  **Verification**: If hash matches, Jenkins accepts the payload.
6.  **Scan**: Jenkins scans all jobs to find which ones map to the GitHub URL.
7.  **Trigger**: Triggers the mapped job, passing the commit hash so it checks out exactly what was pushed.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Controller Relief**: Switching 1,000 jobs from Polling to Webhooks can drop Controller idle CPU usage from 80% to 5%.
- **Webhook Spikes**: A monorepo push that triggers 50 downstream jobs can cause an instant HTTP thread spike on the Controller.

## 📐 ASCII Diagrams (MANDATORY)
```text
❌ SCM POLLING (Bad at Scale) ❌
[ JENKINS CONTROLLER ]
   |  |  |  |  |  (Thousands of 'git ls-remote' calls)
   v  v  v  v  v
[ GITHUB / GITLAB ] (Rate Limit Reached!)


✅ WEBHOOKS (Event-Driven) ✅
[ GITHUB ]
   |
   | HTTP POST (JSON Payload + Signature)
   v
[ NGINX REVERSE PROXY ] (TLS Termination)
   |
   v
[ JENKINS CONTROLLER ] ---> Triggers Build
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// In a Declarative Pipeline, triggers are defined here.
pipeline {
    agent any
    triggers {
        // BAD: Polls Git every 5 minutes (H means Hash to scatter load)
        pollSCM('H/5 * * * *') 
        
        // GOOD: If using Multibranch Pipelines, Webhooks are handled 
        // automatically without explicit trigger definitions.
    }
    stages {
        stage('Build') {
            steps { sh 'echo "Building..."' }
        }
    }
}
```

## 💥 Production Failures
1.  **The Internal Firewall Block**: Jenkins is hosted on an internal corporate network. GitHub is on the public internet. GitHub tries to send a webhook POST, but the corporate firewall drops it. **Solution**: Use an API Gateway or AWS API Gateway to securely proxy the webhook inward, or use an Smee.io payload delivery service.
2.  **Rate Limit Bans**: Due to excessive SCM Polling, GitHub temporarily bans the Jenkins NAT Gateway IP. The entire CI/CD pipeline stops working for 1 hour.
3.  **Spoofed Webhooks**: A webhook endpoint is exposed to the internet without a Shared Secret. A malicious actor sends a fake GitHub JSON payload, causing Jenkins to build a repository containing a crypto-miner.

## 🧪 Real-time Q&A
*   **Q**: If I use Webhooks, do I still need the "Poll SCM" checkbox checked?
*   **A**: In older Jenkins versions, yes (but without a schedule). In modern Jenkins (especially Multibranch), you do NOT check it. The webhook directly triggers the branch scan.
*   **Q**: What if my Jenkins server reboots while GitHub is sending a webhook?
*   **A**: The webhook is lost. GitHub will record a "502/Timeout" delivery failure. You can manually redeliver it from the GitHub UI.

## ⚠️ Edge Cases
*   **Commit Skipping**: If a developer pushes Commit A, and 10 seconds later pushes Commit B, GitHub sends two webhooks. Jenkins queues both. If Jenkins is configured for "Quiet Period" coalescing, it will merge them and only build Commit B.

## 🏢 Best Practices
1.  **Ban Polling**: Globally disable SCM Polling in the organization, or enforce a minimum interval of 1 hour.
2.  **Use HMAC Secrets**: Always configure a "Shared Secret" in the GitHub webhook settings and in the Jenkins credentials to ensure payload authenticity.
3.  **Expose Jenkins Securely**: Never expose Jenkins port 8080 directly to the internet. Always put it behind an Application Load Balancer or NGINX with WAF rules restricting inbound traffic to GitHub IP ranges.

## ⚖️ Trade-offs
*   **Push vs Pull**: Webhooks (Push) are vastly superior for performance and latency, but require complex network configuration (Ingress, DNS, WAF) if Jenkins is hosted in a private subnet. Polling (Pull) is terrible for performance but requires zero inbound network configuration.

## 💼 Interview Q&A
*   **Q**: Our Jenkins server is completely private and cannot accept inbound connections from GitHub.com. How can we achieve near real-time builds without relying on heavy SCM polling?
*   **A**: I would implement an **Event Bus** or **Queue** intermediary. For example, GitHub sends the webhook to an AWS API Gateway -> SQS Queue (which are publicly accessible). Then, a lightweight script or Jenkins plugin inside the private network constantly pulls from the SQS queue. Alternatively, we could use an AWS Lambda function triggered by GitHub that initiates a VPN connection to trigger Jenkins.

## 🧩 Practice Problems
1.  Configure a GitHub Webhook for a test repository. Push code and look at the "Recent Deliveries" tab in GitHub to inspect the raw JSON payload and HTTP headers sent to Jenkins.
2.  Configure a job with `pollSCM('* * * * *')`. Look at the Jenkins "Polling Log" on the job page to see the exact git commands being executed every minute.
