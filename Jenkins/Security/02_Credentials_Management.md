# 🔐 Credentials Management

## 📌 Topic Name
Jenkins Credentials Plugin: Scopes, Binding, and Encryption

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Storing passwords and API keys in Jenkins safely so your scripts can use them without hardcoding them in Git.
*   **Expert**: The Jenkins **Credentials Provider Plugin** creates a standardized, encrypted vault within the Jenkins Controller. It stores secrets (Passwords, SSH Keys, Secret Files) encrypted on disk using AES, keyed by a master key (`secrets/master.key`). A Staff engineer manages the lifecycle of these secrets using **Scopes** (Global vs System vs Folder) to isolate blast radiuses, and injects them securely into pipelines using the `credentials()` binding or `withCredentials` block to ensure they are masked from console output and isolated from underlying OS processes.

## 🏗️ Mental Model
Think of Jenkins Credentials like a **Corporate Keycard System**.
- **Hardcoding (Bad)**: Leaving the physical key to the server room taped to the front door (Storing AWS keys in plain text in a Jenkinsfile/Git).
- **Credentials Plugin (Good)**: Storing the key in a secure lockbox in the lobby.
- **The Process**: When a worker (Pipeline) needs to enter the server room, they ask the Manager (Controller). The Manager temporarily hands them the key, they do the work, and the Manager takes the key back. The worker never permanently possesses the key.

## ⚡ Actual Behavior
- **Log Masking**: When a secret is injected into a pipeline, Jenkins automatically scans the `stdout` stream. If it sees the secret string, it replaces it with `****`.
- **The Masking Flaw**: If a secret is short (e.g., "123"), Jenkins might mask legitimate output that accidentally matches. More dangerously, if a script modifies the secret (e.g., base64 encodes it) and prints *that*, Jenkins will NOT mask it, leaking the secret.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **`master.key` & `hudson.util.Secret`**: Located in `$JENKINS_HOME/secrets/`. The `master.key` encrypts the `hudson.util.Secret` key, which in turn encrypts the actual passwords stored in the `credentials.xml` files. If you lose `master.key`, all credentials are permanently unrecoverable.
2.  **Domains and Scopes**:
    - *System*: Only available to Jenkins itself (e.g., for sending emails via SMTP). Not available to pipelines.
    - *Global*: Available to any pipeline on the system.
    - *Folder*: Available only to pipelines inside that specific folder. (Critical for multi-tenancy).

## 🔁 Execution Flow (Credential Binding)
1.  **Pipeline**: Reaches `withCredentials([string(credentialsId: 'aws-token', variable: 'AWS_KEY')])`.
2.  **Lookup**: Controller searches the Credentials Provider for ID `aws-token`.
3.  **Decryption**: Controller decrypts the value using `hudson.util.Secret`.
4.  **Injection**: Controller securely passes the plaintext value over the Remoting channel to the Agent.
5.  **Environment**: Agent injects `AWS_KEY` into the environment variables of the enclosed `sh` process.
6.  **Cleanup**: When the block ends, the environment variable is wiped from the Agent.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Disk Security**: Because the encrypted values are stored in standard XML files, anyone with read access to the Jenkins OS filesystem (or a backup tarball) can steal the `credentials.xml` and the `secrets/` folder, allowing offline decryption.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ JENKINSFILE ]
withCredentials(AWS_KEY)
       |
       | (Requests Secret)
       v
[ JENKINS CONTROLLER ]
       |
       | 1. Reads config.xml (Encrypted Blob)
       | 2. Reads secrets/master.key (AES Key)
       | 3. Decrypts Blob -> "AKIA12345..."
       |
       +--(RPC Transfer)--> [ AGENT ]
                               |
                               | (Injects into OS Process)
                               v
                        [ sh 'aws s3 ls' ]
                               |
                        (Prints: "Using Key AKIA12345...")
                               |
[ LOG MASKER ] <---------------+
(Replaces "AKIA12345" with "****")
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                // Secure injection of credentials. 
                // The 'credentials()' helper works directly in environment blocks.
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub-creds', 
                        usernameVariable: 'DOCKER_USER', 
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    // DOCKER_PASS is masked in the logs if printed
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                }
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The Environment Variable Leak**: A developer uses `env` or `printenv` inside a `withCredentials` block for debugging. The command prints all environment variables. While the specific secret might be masked, other processes on the Agent OS can read the `/proc/<pid>/environ` file and steal the secret in plaintext.
2.  **The Base64 Bypass**: A script takes a secret, base64 encodes it to pass it to an API, and logs the API request for debugging. Jenkins only masks the plaintext secret, not the base64 version. The secret is leaked in the logs.
3.  **The "Backup" Migration Failure**: An admin copies `$JENKINS_HOME/jobs` to a new server to migrate Jenkins, but forgets to copy the `secrets/` directory. None of the jobs can connect to Git or AWS because the credentials cannot be decrypted.

## 🧪 Real-time Q&A
*   **Q**: Can I use `agent { docker }` with credentials?
*   **A**: Yes, the credentials binding works seamlessly, injecting the secrets as environment variables into the Docker container.
*   **Q**: What is a "Secret text" vs "Secret file"?
*   **A**: "Secret text" is an environment variable string. "Secret file" actually writes a temporary file to the Agent's workspace, injects the file path into an environment variable, and deletes the file when the block completes (useful for TLS certs or Kubeconfigs).

## ⚠️ Edge Cases
*   **Global Scope Pollution**: If an admin puts the Production AWS keys in the "Global" scope, any developer who can create a Jenkinsfile in *any* repository can access those keys and destroy production. Always use Folder-level scopes.

## 🏢 Best Practices
1.  **Use Folders**: Isolate teams. Team A's jobs go in Folder A, and Team A's credentials go in Folder A's credential store.
2.  **Never Use Global**: Except for Jenkins-system-level things (like connecting to the central GitHub), never place deployment credentials in the Global scope.
3.  **Use `password-stdin`**: Never pass passwords as CLI arguments (e.g., `docker login -p $PASS`), as CLI arguments are visible to anyone running `ps aux` on the Agent OS. Always pipe via `stdin`.

## ⚖️ Trade-offs
*   **Jenkins Native Vault vs External Vault**: Jenkins native credentials are easy to use but rely on static AES keys on disk. Enterprise setups should transition to retrieving secrets dynamically at runtime from HashiCorp Vault or AWS Secrets Manager.

## 💼 Interview Q&A
*   **Q**: A developer claims they cannot access the `prod-db-password` credential in their pipeline. The credential exists in Jenkins. What are the two most likely reasons?
*   **A**: First, **Scope Isolation**: The credential might be created in a specific Folder, and the developer's pipeline is in a different Folder. Second, **Typo/ID Mismatch**: The developer might be using the human-readable description instead of the exact alphanumeric `credentialsId` string in their `withCredentials` block. I would verify the location of the job relative to the credential store.

## 🧩 Practice Problems
1.  Create a "Secret text" credential in a specific Folder. Try to access it from a job outside that folder and observe the failure.
2.  Write a pipeline that uses `withCredentials`, assigns the secret to a variable, modifies the string (e.g., `def leaked = secret + "123"`), and prints it. Observe how Jenkins fails to mask the modified string.
