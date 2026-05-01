# 📌 Topic: Node.js in Jenkins

## 🧠 Concept Explanation
Jenkins is an open-source automation server that enables developers to build, test, and deploy their software. In a Node.js context, Jenkins acts as the "Guardian of Quality," ensuring that only verified code reaches your users.

**The Factory Assembly Line Analogy (Deep Dive):**
Imagine a high-tech car factory (Your CI/CD Pipeline).
*   **The Blueprint (The Jenkinsfile):** This is a long document that tells every robot in the factory exactly what to do. If the blueprint says "Test the brakes," the robot must do it.
*   **The Raw Materials (The Code):** You push your code to GitHub. This is like delivering steel and rubber to the factory gate.
*   **The Conveyor Belt (The Pipeline Stages):**
    *   **The Unboxing (npm ci):** A robot takes the materials out of the crates. It uses a very specific list (`package-lock.json`) to make sure it has the exact right bolts and screws.
    *   **The Stress Test (npm test):** Before the car moves on, a machine pushes every button and slams the doors 1,000 times. If a handle breaks, the whole assembly line stops (Build Failure).
    *   **The Packaging (Build):** The car is painted and put into a shipping container (A Docker image or a `dist` folder).
    *   **The Delivery (Deploy):** The container is loaded onto a ship and sent to the dealership (The Production Server).

---

## 🏗️ Mental Model
Think of Jenkins as a **Disposable Laboratory**.
1.  **Isolation:** For every build, Jenkins creates a brand new, empty room (The Workspace).
2.  **Environment:** It sets up the tools (Node.js, npm, Docker) needed for that specific project.
3.  **Action:** It runs your scripts.
4.  **Verdict:** If every script returns "All good" (Exit code 0), the lab is cleaned up and the build passes. If any script screams "Error!" (Exit code 1+), the lab is preserved for investigation and the build fails.

---

## ⚡ Actual Behavior
When a Node.js build runs in Jenkins:
1.  **Worker Allocation:** Jenkins finds an available "Agent" (a machine or a Docker container) that has Node.js installed.
2.  **The `npm ci` Command:** Unlike `npm install`, `npm ci` (Clean Install) is strictly for CI. It deletes your `node_modules` and re-installs them from scratch based *only* on the lockfile. This ensures that the build in Jenkins is identical to the build on your laptop.
3.  **Environment Variables:** Jenkins injects secrets (like DB passwords or API keys) into the process's `process.env`. This allows the tests to run against a real database without hardcoding passwords in the code.
4.  **Log Streaming:** Every line of output from `stdout` and `stderr` is captured and streamed to the Jenkins UI in real-time, allowing you to watch the build "live."

---

## 🔬 Internal Mechanics (V8 + libuv + OS)
*   **Child Processes:** Jenkins doesn't "run" Node.js inside its own process. It uses the OS `spawn()` or `exec()` commands to start a new, independent Node.js process. This means if your code crashes, it doesn't crash Jenkins.
*   **The Exit Code Protocol:** This is the language of CI/CD.
    *   `0`: Success.
    *   `1`: General Error (e.g., a test failed).
    *   `127`: Command not found (e.g., you tried to run `npm` but it's not installed).
    Jenkins monitors the PID of the spawned process and waits for it to exit.
*   **Filesystem I/O:** Builds are very I/O intensive. `npm install` involves creating tens of thousands of small files. On a slow disk (like an old HDD), a build might take 10 minutes, while on an NVMe SSD, it takes 30 seconds.
*   **Shared NPM Cache:** To avoid downloading the same version of `express` 500 times a day, we configure Jenkins to use a "Persistent Volume" for the `~/.npm` directory. When Node.js starts an install, it checks this local OS folder first, saving massive amounts of network bandwidth.
*   **Zombies:** If a build is cancelled, Jenkins sends a `SIGTERM` to the process tree. If your Node.js code doesn't handle this or has "hanging" asynchronous tasks (like a database connection that won't close), the process can become a "Zombie," eating up RAM on the Jenkins server even though the build is officially over.

---

## 🔁 Execution Flow
1.  Developer pushes code to GitHub.
2.  GitHub triggers a Webhook to Jenkins.
3.  Jenkins clones the repo.
4.  **Stage: Install** runs `npm ci`.
5.  **Stage: Test** runs `npm test`.
6.  **Stage: Security** runs `npm audit`.
7.  **Stage: Deploy** runs a deployment script.
8.  Jenkins sends a "Success" message to Slack.

---

## 🧠 Resource Behavior
*   **Disk:** `node_modules` is huge. Cleaning up old workspaces is critical to prevent Jenkins from running out of disk space.
*   **CPU:** Spikes during `npm install` (unzipping) and `npm test`.

---

## 📐 ASCII Diagrams
```text
[ GITHUB ] --(Webhook)--> [ JENKINS ]
                             |
                   +---------v---------+
                   |  PIPELINE STAGES  |
                   |  1. Checkout      |
                   |  2. Install       |
                   |  3. Test & Lint   |
                   |  4. Build & Push  |
                   +-------------------+
```

---

## 🔍 Code Example (Latest Node.js - A Declarative Jenkinsfile)
```groovy
pipeline {
    agent { docker { image 'node:20-alpine' } }
    
    environment {
        NPM_CONFIG_CACHE = "${env.WORKSPACE}/.npm"
    }

    stages {
        stage('Install') {
            steps {
                // 'npm ci' is better for CI than 'npm install'
                sh 'npm ci'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Security Audit') {
            steps {
                sh 'npm audit --audit-level=high'
            }
        }
        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }
    }
    
    post {
        failure {
            echo "Build Failed! Notifying the team..."
        }
    }
}
```

---

## 💥 Production Failures
*   **The "NPM Install" Hang:** A private registry (like Artifactory) is down, causing the build to wait forever for a package. (Solution: Set a `timeout` in the Jenkinsfile).
*   **Flaky Tests:** Tests that fail 10% of the time for no reason, causing the pipeline to fail randomly.
*   **Secret Leak:** Printing environment variables (like `DATABASE_URL`) in the Jenkins console log.

---

## 🧪 Real-time Scenarios
*   **Pull Request Checks:** Ensuring that no one can merge code into `main` unless the Jenkins build passes.
*   **Environment-specific Builds:** Building a different artifact for `staging` vs `production`.

---

## ⚠️ Edge Cases
*   **Architecture Mismatch:** Building a C++ addon (like `bcrypt`) on a Linux Jenkins agent and trying to run it on a macOS server. (Solution: Always build inside a Docker container that matches production).
*   **Missing `.npmrc`:** Forgetting to provide the credentials for private npm packages.

---

## 🏢 Best Practices
1.  **Use `npm ci`:** It is faster and ensures you get the exact versions from `package-lock.json`.
2.  **Cache `node_modules`:** Use the Jenkins "Pipeline Caching" plugin or Docker layer caching.
3.  **Run in Docker:** Ensures the build environment is identical every time.
4.  **Parallel Stages:** Run Lint and Test at the same time to save time.

---

## ⚖️ Trade-offs
*   **Jenkins:** Extremely powerful, highly customizable, but hard to manage and requires your own servers.
*   **GitHub Actions:** Managed by GitHub, easy to set up, but can be expensive and less flexible for complex workflows.

---

## 💼 Interview Q&A
*   **Q:** Why use `npm ci` instead of `npm install` in a CI/CD pipeline?
*   **A:** `npm ci` is designed for automated environments. It deletes the `node_modules` folder first, ensuring a clean state, and it fails if the `package-lock.json` is not in sync with `package.json`.

---

## 🧩 Practice Problems
1.  Write a Jenkinsfile stage that runs `eslint` and fails the build if there are any "error" level linting issues.
2.  Research how to use "Credentials" in Jenkins to securely store a Docker Hub password.

---
Prev: [../Observability/04_Debugging_Production.md](../Observability/04_Debugging_Production.md) | Index: [NodeJS/00_Index.md](../00_Index.md) | Next: [02_Build_Pipelines.md](./02_Build_Pipelines.md)
