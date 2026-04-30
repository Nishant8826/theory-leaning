# 🌳 Large Repo Challenges

## 📌 Topic Name
Scaling SCM: Monorepos, Sparse Checkouts, and Git LFS

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Downloading a giant codebase takes too long and crashes the build server.
*   **Expert**: Monorepos (e.g., massive 50GB repositories with 10 years of history) stress the fundamental design of Git and Jenkins. Standard `git clone` downloads the entire history of every file, saturating network bandwidth and Agent disk space. A Staff engineer mitigates this using **Sparse Checkouts** (downloading only specific directories), **Shallow Clones** (truncating history), **Git LFS** (offloading binaries), and **Filesystem Watchers** to selectively trigger builds only when relevant sub-directories change.

## 🏗️ Mental Model
Think of a Monorepo as the **Library of Congress**.
- **Naive Build**: The developer only changed a typo in one poem in one book. Jenkins asks the library to copy the *entire* Library of Congress, ship it in trucks, just to compile that one poem.
- **Optimized Build**: Jenkins calls the library and says, "Only send me the 'Poetry' section (Sparse Checkout), and I only need the current versions, not the historical drafts (Shallow Clone)."

## ⚡ Actual Behavior
- **Timeout Defaults**: The Jenkins Git plugin has a default timeout of 10 minutes for clone/fetch operations. For massive repos, the network transfer often exceeds this, causing the build to fail before it even starts.
- **Workspace Bloat**: If 5 concurrent builds for a 10GB monorepo hit the same Agent, it immediately consumes 50GB of disk space, likely triggering a `No space left on device` error.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Sparse Checkout**: Git updates the working directory to only include directories matching a specific pattern (e.g., `src/backend/*`). The `.git` metadata folder still contains the entire tree, but the working files are minimal.
2.  **Git LFS (Large File Storage)**: Replaces large audio/video/binary files with tiny text pointers in Git. The actual binaries are stored in an external LFS server (S3). Jenkins must explicitly run `git lfs pull`.
3.  **Path Filtering (Monorepo Triggers)**: In a multibranch pipeline, you don't want a change in `frontend/` to trigger the `backend/` build. Jenkins uses "Included Regions" to parse the git diff and abort the build if the changed paths don't match the regex.

## 🔁 Execution Flow (Optimized Monorepo Checkout)
1.  **Trigger**: Webhook fires. Jenkins parses the JSON and looks at `commits[].modified`.
2.  **Filter**: Jenkins compares the modified files against the `includedRegions` regex. If no match, build is aborted (SUCCESS).
3.  **Init**: If match, Agent allocates workspace.
4.  **Shallow Fetch**: `git fetch --depth 1 origin <commit>`
5.  **Sparse Config**: `git sparse-checkout set "backend/"`
6.  **Checkout**: `git checkout <commit>` (Only populates `backend/` files).

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Git GC Overhead**: Running `git gc` on a massive repo consumes heavy CPU and memory. Jenkins agents should ideally avoid heavy Git maintenance tasks.
- **Controller Latency**: If the Controller uses JGit to parse a massive commit tree for path filtering, it can cause severe GC pauses on the Controller.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ GITHUB: 50GB MONOREPO ]
    |
    | (1) Path Filter: Did 'backend/' change? -> YES
    |
    | (2) git fetch --depth=1 (Downloads 100MB instead of 50GB)
    V
[ JENKINS AGENT ]
    |
    | (3) git sparse-checkout set "backend/"
    V
[ WORKSPACE ]
  .git/ (Metadata)
  backend/ (Files populated)
  (frontend/ is NOT downloaded)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent any
    options {
        // Increase the default 10m timeout for large clones
        checkoutToSubdirectory('src')
        timeout(time: 60, unit: 'MINUTES') 
    }
    stages {
        stage('Checkout Sparse') {
            steps {
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    extensions: [
                        // 1. Truncate history
                        [$class: 'CloneOption', depth: 1, noTags: true, timeout: 60],
                        // 2. Only download specific folders
                        [$class: 'SparseCheckoutPaths', sparseCheckoutPaths: [[path: 'backend/']]],
                        // 3. Handle LFS binaries
                        [$class: 'GitLFSPull']
                    ], 
                    userRemoteConfigs: [[url: 'git@github.com:myorg/monorepo.git']]
                ])
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The Monorepo Build Storm**: A developer merges a Dependabot PR that touches a root `package-lock.json`. Because every microservice job triggers on root file changes, 500 pipelines launch simultaneously, bringing down the entire Jenkins cluster. **Solution**: Use strict path exclusions.
2.  **LFS Smudge Hang**: A user forgets to configure Jenkins with LFS credentials. The `git lfs pull` command hangs indefinitely waiting for a password prompt on `stdin`, locking the executor forever.
3.  **Network Saturation**: 10 ephemeral K8s pods spin up and attempt to clone a 20GB repo simultaneously, maxing out the Node's 10Gbps ENI.

## 🧪 Real-time Q&A
*   **Q**: How do I stop Jenkins from building the Backend when I only change the Frontend?
*   **A**: If using separate jobs, use the "Polling ignores commits in certain paths" behavior in the Git plugin. If using a single Jenkinsfile, use the `when { changeset "backend/**" }` declarative directive to skip stages dynamically.
*   **Q**: What is a "Reference Repository"?
*   **A**: A bare clone of the massive repo stored permanently on the Agent's hard drive. When Jenkins clones, it uses `--reference`, linking to the local bare clone instead of downloading over the network.

## ⚠️ Edge Cases
*   **Submodules**: If your large repo relies on dozens of Git submodules, you must explicitly enable the `SubmoduleOption` extension, and realize that `depth=1` might not apply recursively to submodules without specific configuration.

## 🏢 Best Practices
1.  **Always Depth 1**: There is almost zero reason for a CI server to download the 10-year history of a repository.
2.  **Isolate Jenkinsfiles**: In a monorepo, do not use a single massive Jenkinsfile. Use multiple Multibranch pipelines that point to the same repo but reference different Jenkinsfile paths (e.g., `backend/Jenkinsfile`, `frontend/Jenkinsfile`).
3.  **Offload Tarballs**: Instead of `git clone`, consider having a GitHub Action zip the repo into a `.tar.gz`, put it in S3, and have Jenkins download and unzip the tarball (bypassing Git entirely).

## ⚖️ Trade-offs
*   **Monorepo vs Polyrepo**: Monorepos simplify dependency management for developers but shift a massive engineering burden onto the CI/CD platform team to optimize checkout and build times.

## 💼 Interview Q&A
*   **Q**: Your pipeline is failing during the checkout stage with a `TimeoutException` after exactly 10 minutes. The repository is 15GB. How do you fix this?
*   **A**: The default Git clone timeout in Jenkins is 10 minutes. First, I would increase the timeout in the `CloneOption` extension. However, that's treating the symptom. To treat the cause, I would implement a **Shallow Clone** (`depth 1`) to drop the history, and a **Sparse Checkout** if the build only needs a specific sub-directory. If the repo is heavy due to binaries, I would verify that Git LFS is being used properly and not downloading unnecessary media files.

## 🧩 Practice Problems
1.  Configure a Jenkins job to checkout a public GitHub repository using Sparse Checkout to only pull the `docs/` directory.
2.  Write a Declarative Pipeline with two stages. Use the `when { changeset "path/**" }` directive so Stage 1 only runs if `frontend/` changes, and Stage 2 only runs if `backend/` changes.

---
Prev: [03_Multibranch_Pipelines.md](../SCM/03_Multibranch_Pipelines.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [01_Build_Execution_Lifecycle.md](../Builds/01_Build_Execution_Lifecycle.md)
---
