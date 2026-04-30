# 🔐 Secrets Handling

## 📌 Topic Name
Advanced Secrets Management: Vault, Cloud Managers, and Zero-Trust CI

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Instead of keeping passwords inside Jenkins, Jenkins asks a highly secure external vault for the password right when it needs it.
*   **Expert**: Relying on Jenkins' native XML-backed credential store is an anti-pattern at enterprise scale because it decentralizes secret lifecycle management. A Staff engineer integrates Jenkins with external Secret Managers (e.g., **HashiCorp Vault, AWS Secrets Manager, Azure Key Vault**). This enables **Dynamic Secrets** (generating ephemeral, short-lived AWS STS tokens or DB credentials that expire after the build) and ensures **Zero-Trust**. The Jenkins Controller acts only as a broker, and agents assume execution roles via Workload Identity (OIDC/IRSA) to retrieve secrets directly, preventing Controller compromise from leaking production keys.

## 🏗️ Mental Model
Think of Secrets Management like a **Bank Vault**.
- **Native Jenkins**: Keeping thousands of dollars in a cash register (Jenkins XML). If the store is robbed, all the money is gone.
- **External Vault**: The cashier has no cash. When a transaction happens, a secure pneumatic tube connects directly to the bank vault, delivers exact change for that one transaction, and closes.
- **Dynamic Secrets**: Instead of giving the worker a master key to the bank, the vault prints a temporary key card that only works for 5 minutes and then self-destructs.

## ⚡ Actual Behavior
- **Vault Plugin Integration**: Jenkins can authenticate to HashiCorp Vault using AppRole or Kubernetes Auth. The plugin fetches the secret at pipeline runtime and injects it securely, just like native credentials.
- **Cloud-Native Identity**: The most secure method bypasses Jenkins credentials entirely. A Jenkins Agent running as an AWS EKS Pod is assigned an IAM Role (IRSA). The pipeline runs `aws secretsmanager get-secret-value`. Jenkins never handles the secret; it stays completely within the Agent OS and Cloud boundary.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **HashiCorp Vault Plugin**: Intercepts the `withCredentials` step. Instead of looking at local XML, it makes a REST API call to the Vault Server over TLS, retrieves the lease, and injects it.
2.  **Short-Lived Leases**: If Vault generates an AWS STS token for a deployment, that token is only valid for 1 hour. Even if the token is leaked in a build log, it is useless to an attacker an hour later.
3.  **Environment Variable Risks**: Regardless of where the secret comes from, if it is injected as an Environment Variable, it is vulnerable to memory scraping or OS-level `ps` inspection on the Agent.

## 🔁 Execution Flow (Workload Identity / IRSA)
1.  **Jenkins K8s Plugin**: Spawns Agent Pod with `serviceAccountName: deployer-sa`.
2.  **AWS EKS**: Injects temporary Web Identity Token into the Pod.
3.  **Pipeline**: Executes `sh 'aws s3 cp app.jar s3://prod-bucket'`.
4.  **AWS CLI**: Automatically reads the token from the pod filesystem, calls AWS STS, and assumes the `DeployerRole`.
5.  **Execution**: Upload succeeds.
6.  *Crucial Detail*: Jenkins Native Credentials were NEVER used. No access keys were stored in Jenkins.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Vault Latency**: Querying an external Vault API adds a few hundred milliseconds of network latency to the start of a stage.
- **Rate Limiting**: If 500 parallel builds all hit AWS Secrets Manager simultaneously, you may trigger AWS API rate limits, failing the builds.

## 📐 ASCII Diagrams (MANDATORY)
```text
✅ ZERO-TRUST ARCHITECTURE (Bypassing Jenkins Storage) ✅

[ JENKINS CONTROLLER ] (Has ZERO AWS Credentials)
         |
    (Spawns Pod)
         v
[ JENKINS AGENT (K8s Pod) ] <--- (OIDC Token) ---> [ AWS IAM (STS) ]
         |                                              |
    (sh 'aws secretsmanager ...')                       | (Returns Temp Creds)
         |                                              v
         +-------------------------------------> [ AWS SECRETS MANAGER ]
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// Example: Using HashiCorp Vault Plugin natively in Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Deploy with Vault') {
            steps {
                // Jenkins asks Vault for the secret at runtime
                withVault(vaultSecrets: [[
                    path: 'secret/data/production/database', 
                    secretValues: [
                        [envVar: 'DB_PASSWORD', vaultKey: 'password']
                    ]
                ]]) {
                    sh 'deploy-tool --password $DB_PASSWORD'
                }
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The Terraform State Leak**: A pipeline retrieves an AWS Access Key from Vault to run `terraform apply`. Terraform writes the retrieved secrets (e.g., a generated RDS password) in plain text into the `terraform.tfstate` file in the workspace. Jenkins saves the workspace. The secret is compromised despite using Vault. **Solution**: Use remote state (S3) with encryption and strict IAM.
2.  **Plugin Configuration Drift**: The Vault server is migrated to a new URL. The Jenkins Global Configuration is not updated. Every single deployment job in the company fails simultaneously because they cannot reach Vault.
3.  **OOM due to Secret Size**: A user stores a 5MB base64 encoded TLS certificate chain in AWS Secrets Manager and pulls it into a Jenkins environment variable. Environment variables have length limits in Linux (often 128KB), causing the shell process to crash instantly.

## 🧪 Real-time Q&A
*   **Q**: Should I use the Jenkins Vault plugin or just run the `vault` CLI in my pipeline?
*   **A**: Using the native Vault plugin is better for Jenkins because it automatically integrates with the Log Masker. If you use the CLI, Jenkins doesn't know what string is a secret, and if you accidentally `echo` it, it will print in plain text.
*   **Q**: What is the most secure way to pass a secret to a Docker container?
*   **A**: Do not pass secrets as build arguments (`--build-arg`) as they get baked into the Docker image layers. Use Docker BuildKit's `--secret` mount, or mount them as a tmpfs volume at runtime.

## ⚠️ Edge Cases
*   **Core Dumps**: If a C++ or Go application crashes during a Jenkins build, the OS might generate a core dump file. This core dump contains the complete memory state of the process, including any decrypted secrets that were injected via environment variables.

## 🏢 Best Practices
1.  **No Static Credentials**: Set an OKR to achieve zero static long-lived credentials (like AWS IAM Access Keys) in Jenkins. Everything should be dynamic (STS/OIDC).
2.  **Secret Files, Not Strings**: Prefer injecting secrets as temporary files (e.g., `/tmp/secret.txt`) rather than Environment Variables, as EnvVars are much easier to accidentally leak to child processes.
3.  **Audit Logs**: Rely on the external Vault's audit logs to track exactly which Jenkins job requested which secret at what time.

## ⚖️ Trade-offs
*   **Jenkins Native vs External Vault**: Native is fast, free, and simple. External Vaults require heavy infrastructure maintenance and high availability SLA guarantees (if Vault goes down, Jenkins goes down), but offer enterprise-grade security and rotation.

## 💼 Interview Q&A
*   **Q**: A pipeline needs to deploy to AWS, Azure, and GCP. How would you architect the credentials management to avoid storing static keys for all three clouds in Jenkins?
*   **A**: I would utilize **Workload Identity Federation (OIDC)**. I would run the Jenkins Agents on Kubernetes. I would configure AWS IRSA, Azure Workload Identity, and GCP Workload Identity to all trust the Kubernetes cluster's OIDC issuer. The Jenkins pipeline would simply specify a Kubernetes `ServiceAccount`. When the pod launches, the respective cloud providers will validate the pod's identity token and issue short-lived, dynamic credentials. Jenkins itself never holds a single secret.

## 🧩 Practice Problems
1.  If you have an AWS account, configure a Jenkins pipeline to assume an IAM role using OIDC instead of storing an IAM Access Key.
2.  Write a script that demonstrates how an environment variable can leak. (e.g., inject a secret, start a background process `sleep 60 &`, and `cat /proc/$!/environ`).

---
Prev: [02_Credentials_Management.md](../Security/02_Credentials_Management.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [04_Sandbox_and_Script_Security.md](../Security/04_Sandbox_and_Script_Security.md)
---
