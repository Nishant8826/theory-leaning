# 🌳 Git Integration

## 📌 Topic Name
Jenkins and Git: Clones, JGit vs CLI, and Repository Workspaces

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Jenkins downloads your code from GitHub to build it.
*   **Expert**: Jenkins integrates with Git via the **Git Plugin**, which acts as a bridge between the Jenkins workspace and the remote SCM. It manages authentication, checkout behaviors, and local repository caching. A Staff engineer knows that doing a standard `git clone` for every build of a 10GB monolith will saturate network bandwidth, exhaust agent disk space, and cripple build times. Optimization requires deep understanding of **Shallow Clones**, **Reference Repositories**, and the difference between **JGit** and the native OS **Git CLI**.

## 🏗️ Mental Model
Think of Jenkins SCM integration as a **Library Book Request System**.
- **Naive Approach (Full Clone)**: Every time a student asks for a quote from a book, you print a brand new copy of the entire 1,000-page book, ship it to them, and they throw it away when done. (Massive waste of time and network).
- **Optimized Approach (Shallow Clone)**: You only print the exact page they requested.
- **Reference Approach (Cache)**: The student keeps the book on their desk. Next time, you just send them a sticky note with the 1 line of text that changed.

## ⚡ Actual Behavior
- **JGit vs Git CLI**: Jenkins defaults to using the native Git executable (`git`) installed on the Agent's OS. If it's missing, it can fall back to **JGit** (a pure Java implementation of Git running inside the JVM). JGit is notoriously slower and consumes massive heap space for large repositories. Always use the native CLI.
- **Workspace `.git`**: Jenkins leaves the `.git` directory in the agent workspace. If the same job runs on the same executor again, Jenkins will execute `git fetch` instead of `git clone`, downloading only the delta.

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **`git ls-remote`**: Before starting a build, Jenkins often runs `git ls-remote` to check the current HEAD commit of the branch. If it matches the last built commit, it aborts the build (if triggered by polling).
2.  **Shallow Clones (`--depth 1`)**: Instructs Git to only download the latest commit, ignoring the history. This reduces clone times from minutes to seconds.
3.  **Reference Repositories (`--reference`)**: You can pre-clone a massive repository to a local path on the Jenkins Agent (e.g., `/opt/git/linux.git`). When Jenkins clones the repo for a job, it uses hard links to the reference repo, using almost zero network and zero extra disk space.

## 🔁 Execution Flow (Pipeline `checkout scm`)
1.  **Pipeline Step**: Reaches `checkout scm`.
2.  **Directory Check**: Plugin checks if `.git` exists in the workspace.
3.  **Clean**: (Optional) Runs `git clean -fdx` to remove untracked build artifacts from previous runs.
4.  **Fetch**: Runs `git fetch --tags --progress origin`.
5.  **Checkout**: Runs `git checkout -f <commit-hash>`.
6.  **Branch State**: Pipeline now has the code.

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Disk Saturation**: A 5GB repository built concurrently across 10 executors on the same Agent will consume 50GB of disk space instantly.
- **Network Ingress**: Pulling a massive repo for every ephemeral K8s pod build will result in gigabytes of network ingress per minute, potentially triggering AWS NAT Gateway costs or GitHub API rate limits.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ GITHUB / BITBUCKET ]
          |
    (Network Transfer)
          |
[ JENKINS AGENT ]
          |
+---------v---------+
| WORKSPACE DIR     |
|  .git/ (Metadata) | <--- (Can be 90% of the size!)
|  src/             |
|  package.json     |
+-------------------+
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Highly Optimized Checkout for large repos
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    extensions: [
                        // Shallow clone (depth 1)
                        [$class: 'CloneOption', depth: 1, noTags: true, reference: '', shallow: true],
                        // Clean workspace before build
                        [$class: 'CleanBeforeCheckout']
                    ], 
                    userRemoteConfigs: [[url: 'git@github.com:myorg/massive-monolith.git']]
                ])
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The "OOM during Clone"**: JGit is accidentally used on a repository with 50,000 commits. The Controller or Agent JVM attempts to load the entire Git tree into heap memory to process the delta, crashing the JVM. **Solution**: Ensure Git CLI is installed and configured in Global Tool Configuration.
2.  **Git Tag Explosion**: By default, `git fetch` pulls all tags. In a repo with 100,000 automated release tags, fetching tags takes longer than downloading the code. **Solution**: Use the `noTags: true` extension.
3.  **The Dirty Workspace**: A developer removes a dependency from `package.json`, but a compiled `.o` file from the previous build is still sitting in the workspace. The build passes on Jenkins but fails on a fresh machine. **Solution**: Always use `CleanBeforeCheckout` or `WipeWorkspace`.

## 🧪 Real-time Q&A
*   **Q**: Why does my pipeline say "Detached HEAD state"?
*   **A**: Jenkins does not check out a *branch*; it checks out the specific *commit hash* that triggered the build. This ensures absolute determinism (if someone pushes to `main` while the build is running, the code doesn't change). This puts Git into a "detached HEAD" state.
*   **Q**: My build needs to push a tag back to Git. How?
*   **A**: You must configure the SSH/HTTPS credentials in the Jenkinsfile, use the `sshagent` plugin (or `withCredentials`), and run `git tag` and `git push origin` via `sh` steps.

## ⚠️ Edge Cases
*   **Git LFS (Large File Storage)**: If the repo uses LFS, you must explicitly enable the `GitLFSPull` extension in the checkout step; otherwise, you will check out 1KB pointer files instead of the actual binary assets.

## 🏢 Best Practices
1.  **Always use Shallow Clones** for CI builds. You do not need the 10-year history of the repository to compile the code.
2.  **Use Ephemeral Agents**: Using Kubernetes pods ensures a pristine workspace (no caching), but requires shallow clones to keep network overhead low.
3.  **Trust but Verify**: If using persistent agents, always use `git clean -fdx` to nuke untracked files before building.

## ⚖️ Trade-offs
*   **Persistent Workspaces vs Ephemeral Workspaces**:
    *   *Persistent*: Extremely fast checkouts (`git fetch` delta only). High risk of "dirty" workspace bugs.
    *   *Ephemeral (K8s)*: Perfect reproducibility. High network/time cost because it must `git clone` from scratch every time.

## 💼 Interview Q&A
*   **Q**: Your Jenkins server is launching 50 concurrent builds for a 2GB monorepo in a Kubernetes cluster. The cluster's network is saturated and GitHub is rate-limiting you. How do you optimize this?
*   **A**: First, I would enforce a **Shallow Clone** (`depth 1` and `noTags: true`) in the Jenkinsfile. If that is still too heavy, I would implement a **Reference Repository** in the Kubernetes cluster. I'd create a PersistentVolume containing a bare clone of the repo, mount it to every Jenkins Agent pod as Read-Only, and configure the Jenkins Git plugin to use `--reference /path/to/mount`. This would reduce network traffic by 99%.

## 🧩 Practice Problems
1.  Configure a Jenkinsfile using the explicit `checkout scm` syntax with the `CloneOption` extension set to `shallow: true`.
2.  Run a build on a persistent agent. SSH into the agent and run `git reflog` in the workspace to see exactly what commands Jenkins executed.
