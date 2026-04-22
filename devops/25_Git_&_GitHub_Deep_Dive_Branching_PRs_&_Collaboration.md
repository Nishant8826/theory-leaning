# 25 – Git & GitHub Deep Dive: Branching, PRs & Collaboration

---

## Table of Contents

1. [Git as a Distributed System](#1-git-as-a-distributed-system)
2. [Essential Git Commands](#2-essential-git-commands)
3. [Fork vs Clone – Cloud vs Local](#3-fork-vs-clone--cloud-vs-local)
4. [Branching Strategy](#4-branching-strategy)
5. [Pull Request (PR) Workflow](#5-pull-request-pr-workflow)
6. [Merge Conflicts & Resolution](#6-merge-conflicts--resolution)
7. [GitHub Repository Settings & Features](#7-github-repository-settings--features)
8. [Advanced Git Concepts](#8-advanced-git-concepts)
9. [DevOps Engineer's Role in GitHub](#9-devops-engineers-role-in-github)
10. [Visual Diagrams](#10-visual-diagrams)
11. [Scenario-Based Q&A](#11-scenario-based-qa)
12. [Interview Q&A](#12-interview-qa)

---

## 1. Git as a Distributed System

### What
Git is an **open-source, distributed version control system** operated primarily through the **CLI (Command Line Interface)**. "Distributed" means every developer has the **full copy** of the repository — history, branches, and all — on their own machine.

### Why
Centralized systems (like older SVN) had a single server. If that server went down, no one could work. Git solved this by giving every team member a complete, independent copy. Work continues even when offline or when the server is unavailable.

### How
- You clone a remote repo → get a full local copy
- All commits, branches, and history are available locally
- You sync with the remote only when you need to (push/pull)

### Impact

| Centralized VCS (old) | Distributed VCS (Git) |
|----------------------|----------------------|
| Single server = single point of failure | Every copy is a full backup |
| Must be online to work | Work fully offline |
| Slow (network call for every operation) | Fast (local operations) |
| Limited collaboration model | Flexible branching & merging |

> 💡 **Real world:** Even if GitHub goes down for an hour, every developer still has the complete codebase locally and can keep working.

---

## 2. Essential Git Commands

### `git clone [URL]`
- **What:** Downloads a full copy of a remote repository to your local machine
- **When:** First time you want to start working on an existing project
- **Creates:** A local folder with all files, branches, and history

```bash
git clone https://github.com/videolan/vlc.git
# Creates a /vlc folder with the complete repo
```

---

### `git status`
- **What:** Shows the current state of your working directory and staging area
- **When:** Run this constantly — before add, before commit, when confused
- **Tells you:** Which files are modified, staged, untracked, or clean

```bash
git status
# On branch main
# Changes not staged for commit:
#   modified: index.html
# Untracked files:
#   new-feature.py
```

---

### `git pull`
- **What:** Fetches the latest changes from the remote AND merges them into your local branch
- **When:** First thing every morning before you start work — "sync up"
- **Equivalent to:** `git fetch` + `git merge` combined

```bash
git pull origin main
# Downloads and merges any new commits your teammates pushed overnight
```

---

### `git config --global --list`
- **What:** Displays all globally configured Git settings on your machine
- **When:** To verify which user account is active (important on shared/new machines)

```bash
git config --global --list
# user.name=John Doe
# user.email=john@company.com
```

> ⚠️ Always verify this on a new machine or before your first commit at a new job — commits are permanently tagged with whatever name/email is configured here.

---

### Command Quick Reference

| Command | What it does | When to use |
|---------|-------------|-------------|
| `git init` | Create a new local repo | Starting a brand new project |
| `git clone [URL]` | Copy remote repo locally | Joining an existing project |
| `git status` | Check current state | Constantly — before every action |
| `git add [file]` | Stage changes | After editing, before committing |
| `git commit -m "msg"` | Save local snapshot | After staging |
| `git push origin [branch]` | Upload to GitHub | After committing |
| `git pull origin [branch]` | Download + merge from GitHub | Start of day / before new work |
| `git config --global --list` | Check git identity | New machine setup / troubleshooting |

---

## 3. Fork vs Clone – Cloud vs Local

These two words confuse almost every beginner. The difference is simple once you understand where each operation happens.

### Fork

#### What
A **Fork** is a **cloud-to-cloud copy** of a repository. It creates your own personal copy of someone else's GitHub repo — entirely on GitHub's servers. No download happens.

#### Why
- You want to contribute to an open-source project but don't have write access to the original
- You want your own separate cloud copy to experiment with freely
- The standard way to contribute to any public project on GitHub

#### How
1. Go to a repo on GitHub (e.g., `github.com/videolan/vlc`)
2. Click the **Fork** button (top right)
3. GitHub creates `github.com/YOUR_USERNAME/vlc` — your cloud copy
4. You now have full control over your fork

```
Original Repo (GitHub)          Your Fork (GitHub)
github.com/videolan/vlc  ──────► github.com/yourname/vlc
         (Cloud)        FORK            (Cloud)
```

---

### Clone

#### What
A **Clone** is a **cloud-to-local copy**. It downloads a repository from GitHub (or any remote) to your actual machine.

#### Why
- You need to actually work on the code (write, run, test)
- Editing code directly on GitHub's website is impractical for real development

#### How
```bash
git clone https://github.com/yourname/vlc.git
# Downloads to your machine → /vlc folder
```

```
Your Fork (GitHub)              Your Machine (Local)
github.com/yourname/vlc  ──────► /home/you/vlc/
         (Cloud)         CLONE        (Local)
```

---

### Fork + Clone Together (Open Source Workflow)

```
[Original Repo]  →FORK→  [Your Fork]  →CLONE→  [Your Machine]
  (GitHub)                 (GitHub)               (Local)
                                                     │
                                              Edit & commit
                                                     │
                                              git push to fork
                                                     │
                                           Raise Pull Request
                                                     │
                                      Original repo reviews & merges
```

### Fork vs Clone – Side by Side

| | Fork | Clone |
|--|------|-------|
| **Where it happens** | Cloud → Cloud (GitHub → GitHub) | Cloud → Local (GitHub → Your Machine) |
| **Purpose** | Get your own remote copy | Download to work on locally |
| **Who can do it** | Anyone (on public repos) | Anyone with repo access |
| **Linked to original?** | Yes (can submit PRs back) | Yes (via remote URL) |
| **Command/Action** | GitHub UI button | `git clone [URL]` |

---

## 4. Branching Strategy

### What
A **branch** is an independent copy of the codebase where you can safely make changes without affecting the main production code. Branches are the foundation of team collaboration in Git.

### Why
Imagine 10 developers all editing the same codebase directly. It would be chaos — constant overwrites, broken code, no way to isolate bugs. Branches let each developer work in their own bubble until the work is ready to be reviewed and merged.

### How – The Golden Rule
> ❌ **Never commit directly to `main` or `master`**
> ✅ **Always create a feature branch for every piece of work**

### Branch Naming Convention
A good branch name tells you: **what type of work + what it does + ticket reference**

```
Pattern:  [type]-[description]-[ticket-id]
Examples:
  feature-alarm-jira123        ← New feature
  bugfix-login-timeout-jira456 ← Bug fix
  hotfix-payment-crash-jira789 ← Urgent production fix
```

### Branch Types

| Branch | Purpose | Who touches it |
|--------|---------|----------------|
| `main` / `master` | Production code — always working | DevOps / automation only |
| `develop` | Integration branch — work in progress | Developers merge here first |
| `feature-*` | Individual features or tasks | Individual developers |
| `bugfix-*` | Fixing a reported bug | Individual developers |
| `hotfix-*` | Emergency fix for production | Senior developers |
| `release-*` | Preparing a release version | Release managers |

### How to Create and Use a Branch

```bash
# Step 1: Make sure you're on main and up to date
git checkout main
git pull origin main

# Step 2: Create and switch to your feature branch
git checkout -b feature-alarm-jira123

# Step 3: Make your changes, then add and commit
git add .
git commit -m "Add alarm notification feature - JIRA-123"

# Step 4: Push your feature branch to GitHub
git push origin feature-alarm-jira123

# Step 5: Go to GitHub and open a Pull Request
```

### Impact

| Without Branching | With Branching |
|-------------------|---------------|
| Everyone edits `main` directly | Safe isolated workspaces |
| One broken commit breaks everyone | Bad code never reaches main until reviewed |
| No way to work on multiple features | 10 features developed simultaneously |
| Rollback is hard | Just revert or delete the branch |

---

## 5. Pull Request (PR) Workflow

### What
A **Pull Request (PR)** is a formal request to merge your feature branch into the main branch. It's not a Git command — it's a **GitHub feature** that enables code review, discussion, and controlled merging.

### Why
Code review is one of the most important quality gates in software development. A PR ensures:
- At least one other person reviews your code before it goes live
- There's a discussion thread documenting *why* changes were made
- Tests can be run automatically before merging
- The merge only happens with explicit approval

### How – The PR Lifecycle

```
Step 1: Developer finishes work on feature branch
Step 2: Developer pushes the branch to GitHub
Step 3: Developer opens a PR on GitHub (base: main ← compare: feature-branch)
Step 4: Developer writes description explaining what & why
Step 5: Manager / reviewer is notified
Step 6: Reviewer reads the code, leaves comments or approval
Step 7: Developer addresses comments and pushes fixes
Step 8: Reviewer approves ✅
Step 9: PR is merged into main
Step 10: Feature branch is deleted (optional but recommended)
```

### PR Review — What Reviewers Look For
- ✅ Does the code do what it says it does?
- ✅ Are there any bugs or edge cases missed?
- ✅ Is it readable and well-documented?
- ✅ Does it follow team coding standards?
- ✅ Are there any security concerns?

### PR Best Practices
- Keep PRs **small and focused** — one feature or bug fix per PR
- Write a **clear description** — what, why, and how to test
- **Link the Jira/issue ticket** in the PR description
- Don't open a PR late Friday afternoon 😄
- Respond to reviewer comments **within 24 hours**

### Impact

| Without PRs | With PRs |
|-------------|----------|
| Bugs go straight to production | Caught during review |
| No knowledge sharing | Team learns from each other |
| No documentation of decisions | Discussion thread as permanent record |
| One person's mistake breaks everyone | Controlled, reviewed merges |

---

## 6. Merge Conflicts & Resolution

### What
A **merge conflict** happens when two developers edit the **same line(s)** in the **same file** on **different branches**, and Git can't automatically decide which version to keep.

### Why It Happens
Git is smart enough to auto-merge most changes. But when two people touch the exact same part of a file, Git needs a human to decide which version wins.

### How a Conflict Looks

```
<<<<<<< HEAD (your branch)
  color: red;
=======
  color: blue;
>>>>>>> feature-theme-jira456 (incoming branch)
```

- Everything between `<<<<<<< HEAD` and `=======` is **your current version**
- Everything between `=======` and `>>>>>>>` is the **incoming version**
- You must **manually pick one** (or combine them), then delete the markers

### Resolution Steps

```
Step 1: Try to merge (git merge or via PR)
Step 2: Git reports a conflict
Step 3: Open the conflicted file(s)
Step 4: Find the conflict markers (<<<<<<<, =======, >>>>>>>)
Step 5: Decide what the final code should look like
Step 6: Remove ALL conflict markers
Step 7: git add [resolved-file]
Step 8: git commit -m "Resolve merge conflict in styles.css"
Step 9: Continue with the merge / push
```

### How to Avoid Conflicts (Best Practices)
- Pull from main **before starting new work** and **regularly during development**
- Keep PRs **small** — less code = less chance of conflict
- Communicate with teammates about who's editing what
- Manager should review and coordinate merges carefully

---

## 7. GitHub Repository Settings & Features

### What
GitHub provides a rich set of tools beyond just storing code. As a DevOps engineer, you're responsible for setting up and maintaining these correctly.

> 💡 The instructor emphasized: **90% of GitHub work happens through the UI**, not the CLI.

---

### Repository Settings

#### Visibility
- **Public:** Anyone on the internet can see the code (used for open source)
- **Private:** Only invited collaborators can see it (used for company code)

#### Collaborators
- Add team members with specific permission levels:
  - **Read** – can view code
  - **Write** – can push branches
  - **Maintain** – can manage settings
  - **Admin** – full control

#### Branch Protection Rules
The most important setting a DevOps engineer configures:
- Require PR before merging to `main`
- Require at least 1 approval before merge
- Block direct pushes to `main`
- Require status checks (tests) to pass before merging

```
Settings → Branches → Add rule → Branch name: main
  ✅ Require pull request reviews before merging
  ✅ Require status checks to pass before merging
  ✅ Include administrators
  ❌ Allow force pushes (leave unchecked)
```

---

### Issues Tab
- **What:** A built-in **bug tracker and feature request system**
- **Used for:** Reporting bugs, suggesting features, tracking tasks
- Can be linked to PRs (closing an issue automatically when a PR merges)
- Labels, assignees, milestones — full project management

---

### Insights Tab
- **What:** Analytics dashboard for the repository
- **Shows:** Contributor activity, commit frequency, PR/issue metrics, traffic
- **Used by:** Engineering managers to track project health and team contributions

---

### Actions Tab
- **What:** GitHub's built-in **CI/CD (Continuous Integration / Continuous Deployment)** system
- **Used for:** Automatically running tests, building code, deploying applications when code is pushed or merged
- Configured via YAML files in `.github/workflows/`

---

## 8. Advanced Git Concepts

These were briefly introduced in class. Think of these as tools you'll need later in your DevOps journey.

---

### `git rebase`
- **What:** Re-applies your commits on top of another branch's latest commits — creates a cleaner, linear history
- **vs Merge:** Merge preserves the true history (including branch divergence); Rebase rewrites history to look linear
- **Use with caution:** Never rebase commits that have already been pushed to a shared remote

```
Before rebase:          After rebase:
A - B - C  (main)       A - B - C - D' - E'  (main)
         \
          D - E  (feature)
```

---

### `git reset`
- **What:** Moves the current branch pointer backwards to an earlier commit
- **Types:**
  - `--soft`: Keep changes staged
  - `--mixed`: Keep changes unstaged
  - `--hard`: ❗ **Discard all changes permanently**
- **Use case:** Undo commits that haven't been pushed yet

```bash
git reset --hard HEAD~1   # ⚠️ Deletes the last commit AND all its changes
git reset --soft HEAD~1   # Undo commit but keep changes staged
```

---

### `git revert`
- **What:** Creates a **new commit** that undoes the changes of a previous commit
- **Why it's safer than reset:** Doesn't rewrite history — safe to use on shared branches
- **Use case:** Undo a commit that's already been pushed/merged

```bash
git revert abc1234   # Creates a new "undo" commit
```

---

### Squash Merge
- **What:** Combines all commits from a feature branch into a **single commit** before merging
- **Why:** Keeps the main branch history clean — one PR = one commit, not 47 "WIP" commits
- Configured as an option in the GitHub PR merge dialog

```
Feature branch: A → B → C → D → E (5 messy commits)
After squash merge: main gets one clean commit "Add alarm feature JIRA-123"
```

---

### Fast-Forward Merge
- **What:** If the feature branch is ahead of main with no divergence, Git simply "moves" the main pointer forward
- **Result:** No merge commit created — the history looks perfectly linear
- **When it happens:** Automatically when there are no conflicting changes

---

### `git stash`
- **What:** Temporarily shelves (saves) uncommitted changes so you can switch branches without committing
- **When:** Urgent bug on another branch needs fixing, but your current work isn't ready to commit
- **Rarely used in real-time** (per instructor)

```bash
git stash          # Save current changes
git checkout main  # Switch branch freely
git stash pop      # Restore saved changes later
```

---

### Common Base Branching Strategy
- **What:** Before both developers start their features, they both branch from the same commit on main
- **Why:** Reduces conflicts because both features share a common starting point
- Managed by the DevOps engineer or tech lead

---

## 9. DevOps Engineer's Role in GitHub

This is a critical distinction: **developers write code, DevOps engineers manage the platform**.

### DevOps Responsibilities in GitHub

| Responsibility | What it involves |
|----------------|-----------------|
| **Repository Setup** | Create repos, set visibility, configure settings |
| **Branch Protection** | Enforce PR rules, block direct pushes to main |
| **Security** | Manage access, rotate tokens, enable secret scanning |
| **CI/CD via Actions** | Set up automated testing and deployment pipelines |
| **Onboarding** | Add/remove collaborators, manage permissions |
| **Best Practices** | Enforce naming conventions, PR templates, commit standards |
| **Audit & Compliance** | Use Insights to track activity, maintain audit logs |

### The 90% UI Rule
> The instructor emphasized: **90% of GitHub work happens through the web UI, not the CLI.**

- Developers: heavy CLI use for daily git operations
- DevOps Engineers: heavy UI use for configuration, monitoring, and management
- Managers/Reviewers: 100% UI for code reviews and PR approvals

---

## 10. Visual Diagrams

### Diagram 1: Fork → Clone → PR Full Workflow

```
┌──────────────────────────────────────────────────────────────────┐
│                          GITHUB (Cloud)                          │
│                                                                  │
│  [Original Repo]  ──FORK──►  [Your Fork]                        │
│  videolan/vlc                yourname/vlc                        │
│                                    │                             │
│                                    │ ◄── git push (your branch) │
│                                    │                             │
│                         [Pull Request]                           │
│                         Developer → Manager review → Merge       │
└────────────────────────────┬─────────────────────────────────────┘
                             │ git clone
                             ▼
                    ┌─────────────────┐
                    │  Your Machine   │
                    │   (Local)       │
                    │                 │
                    │  Edit → Add →   │
                    │  Commit → Push  │
                    └─────────────────┘
```

---

### Diagram 2: Branching Strategy

```
main  ●────────────────────────────────────────────► (production)
      │                          ▲         ▲
      │                          │ PR+Merge │ PR+Merge
      │                          │         │
      ├──► feature-alarm-jira123 ●──●──●───┘
      │    (Developer A)
      │
      └──► bugfix-login-jira456  ●──●─────────────►
           (Developer B)
```

---

### Diagram 3: Pull Request Lifecycle

```
[Developer]                    [GitHub]                  [Reviewer/Manager]
     │                            │                              │
     │── push feature branch ────►│                              │
     │                            │                              │
     │── Open Pull Request ───────►│── notify ──────────────────►│
     │                            │                              │
     │                            │◄── review comments ─────────│
     │                            │                              │
     │◄── make changes ───────────│                              │
     │                            │                              │
     │── push fixes ─────────────►│                              │
     │                            │                              │
     │                            │◄── Approved ✅ ──────────────│
     │                            │                              │
     │                            │── Auto Merge ──────────────►main
     │                            │                              │
     │                    Feature branch deleted                 │
```

---

### Diagram 4: Merge vs Squash vs Rebase

```
REGULAR MERGE:
main:    A ── B ─────────────────── M  (M = merge commit)
                \                  /
feature:         C ── D ── E ── F ─

SQUASH MERGE:
main:    A ── B ── [CDEF]              (all feature commits squashed to one)
feature: C ── D ── E ── F (squashed, then branch deleted)

REBASE:
main:    A ── B ── C' ── D' ── E' ── F'  (feature commits replayed on top)
(clean linear history, no merge commit)
```

---

### Diagram 5: Conflict Resolution

```
Your Branch:  "color: red;"
Main Branch:  "color: blue;"

Conflict file shows:
┌─────────────────────────────────┐
│ <<<<<<< HEAD                    │
│   color: red;                   │  ← Your version
│ =======                         │
│   color: blue;                  │  ← Incoming version
│ >>>>>>> feature-theme           │
└─────────────────────────────────┘

You decide → "color: purple;" (or pick one, or combine)
Remove ALL markers → git add → git commit
```

---

## 11. Scenario-Based Q&A

---

🔍 **Scenario 1:** You want to contribute to the VLC media player open-source project but you don't have write access to their repo.

✅ **Answer:** Fork the `videolan/vlc` repository — this creates `yourname/vlc` on GitHub. Clone your fork locally, create a feature branch, make your changes, push to your fork, then open a Pull Request from your fork's branch to the original `videolan/vlc` repo. The VLC maintainers review and merge if they approve.

---

🔍 **Scenario 2:** Your manager says "never push directly to main." How do you enforce this technically, not just by policy?

✅ **Answer:** In GitHub, go to **Settings → Branches → Add branch protection rule**. Set the rule for `main` and check "Require a pull request before merging" and "Include administrators." This makes it technically impossible to push directly — even admins must go through a PR. This is a key DevOps responsibility.

---

🔍 **Scenario 3:** You're halfway through a feature when your manager calls saying there's a critical bug in production that needs fixing immediately.

✅ **Answer:** Use `git stash` to temporarily save your incomplete work without committing it. Switch to `main`, create a `hotfix-` branch, fix the bug, raise a PR, get it merged. Then come back to your feature branch and run `git stash pop` to restore your incomplete work and continue where you left off.

---

🔍 **Scenario 4:** A junior developer asks: "My PR has 52 commits — all named 'WIP', 'fix', 'fix again', 'finally fixed'. Will that mess up main's history?"

✅ **Answer:** Yes, it would make the history unreadable. The solution is a **Squash Merge** — all 52 commits get collapsed into a single, clean commit with a proper message before merging into main. This is why squash merge is often enabled as the default merge strategy for PRs.

---

🔍 **Scenario 5:** Two developers both edited `App.java` on their separate branches. Now merging causes a conflict. What do you do?

✅ **Answer:** Open the conflicted file, find the `<<<<<<< / ======= / >>>>>>>` markers, and read both versions carefully. Decide what the final code should be (keeping one, the other, or combining both). Delete all conflict markers, save the file, then run `git add App.java` followed by `git commit -m "Resolve merge conflict in App.java"`. The merge continues.

---

🔍 **Scenario 6:** Your manager wants to track which developers are contributing the most code and how active the repository is.

✅ **Answer:** Go to the GitHub repository → **Insights** tab. This shows contributor graphs, commit frequency, PR/issue open-close rates, and traffic analytics. No CLI needed — it's all in the GitHub UI.

---

🔍 **Scenario 7:** You committed a secret API key to main by accident. What do you do?

✅ **Answer:** First, **immediately revoke/rotate that API key** in whatever service issued it — assume it's already compromised. Then use `git revert` to create a new commit that removes the key (safer than `git reset` on a shared branch). Enable **GitHub Secret Scanning** in repository settings to detect this automatically in future. Consider using `.gitignore` and environment variables to prevent this pattern entirely.

---

## 12. Interview Q&A

---

**Q1. What is the difference between `git fetch` and `git pull`?**

**A:** Both download changes from the remote, but:
- `git fetch` downloads the changes but does **not** merge them into your local branch. Your working directory stays untouched. You can inspect what changed before deciding to merge.
- `git pull` = `git fetch` + `git merge`. It downloads AND immediately merges the remote changes into your current branch.

Use `git fetch` when you want to see what's changed before merging. Use `git pull` when you trust the remote and just want to sync up quickly.

---

**Q2. What is the difference between Fork and Clone?**

**A:**
- **Fork** is a cloud-to-cloud operation — it copies a repo from someone else's GitHub account to your GitHub account. No download happens.
- **Clone** is a cloud-to-local operation — it downloads a repo from GitHub to your machine.

The typical open-source workflow is: Fork first (get your own cloud copy), then Clone (download your fork to work on it locally).

---

**Q3. What is a Pull Request and why is it important?**

**A:** A Pull Request (PR) is a GitHub feature that lets you formally request to merge a feature branch into the main branch. It enables:
- Code review by peers or managers before code reaches production
- Discussion and documentation of why changes were made
- Automated checks (tests, linting) before merging
- Approval gates (require N approvals before merge)

PRs are the primary quality control mechanism in professional software development.

---

**Q4. What is a merge conflict and how do you resolve it?**

**A:** A merge conflict occurs when two branches have modified the same lines in the same file and Git cannot automatically decide which version to keep. Resolution steps:
1. Open the conflicted file
2. Find the `<<<<<<<`, `=======`, and `>>>>>>>` markers
3. Manually decide what the final code should look like
4. Delete all conflict markers
5. `git add` the resolved file
6. `git commit` to complete the merge

Prevention: pull from main regularly, keep PRs small, coordinate with teammates.

---

**Q5. What is the difference between `git revert` and `git reset`?**

**A:**
- `git reset` moves the branch pointer backwards, **rewriting history**. It's dangerous on shared branches because it removes commits others may have already pulled.
- `git revert` creates a **new commit** that undoes the changes of a previous commit, without rewriting history. It's safe to use on shared branches.

Rule: Use `git reset` only on local commits not yet pushed. Use `git revert` for commits that have already been pushed or merged.

---

**Q6. What is squash merging and when would you use it?**

**A:** Squash merging takes all the commits from a feature branch and combines them into a single commit before merging into main. It's used when:
- A developer has many small "WIP" commits with poor messages
- You want a clean, readable main branch history (one PR = one commit)
- The individual commits in the feature branch aren't meaningful to the team

The trade-off is that individual commit history from the branch is lost after the squash.

---

**Q7. What does a DevOps engineer do in GitHub that a developer doesn't?**

**A:** DevOps engineers are responsible for the *platform and infrastructure* of GitHub, not the code itself:
- Setting up repositories, visibility (public/private), and access controls
- Configuring branch protection rules (requiring PRs, blocking direct pushes to main)
- Setting up GitHub Actions for CI/CD pipelines
- Managing collaborator permissions and onboarding/offboarding
- Monitoring repository health via Insights
- Enforcing security (secret scanning, dependency alerts)
- Defining and enforcing team-wide Git conventions

Developers use Git daily for coding; DevOps engineers configure the environment that makes Git safe and efficient at scale.

---

**Q8. What are branch protection rules and why are they important?**

**A:** Branch protection rules are settings in GitHub that enforce policies on specific branches (usually `main`). They can:
- Require a Pull Request before any merge
- Require a minimum number of approvals
- Require passing CI checks (tests, builds) before merging
- Prevent force pushes that rewrite history
- Apply the rules even to admins

Without them, any developer (or an accidental command) could push broken code directly to production. Branch protection makes the quality gates automatic and enforceable, not just a matter of discipline.

---

**Q9. What is `git rebase` and how is it different from `git merge`?**

**A:** Both integrate changes from one branch into another, but differently:
- `git merge` creates a **merge commit** that ties the two branch histories together. The history shows exactly when branches diverged and merged (true history).
- `git rebase` re-applies your commits **on top of** the target branch, creating a clean linear history with no merge commit. It looks like you started your work after the latest commit on main.

Rebase produces cleaner history but should **never be used on shared/pushed branches** because it rewrites commit hashes, causing problems for anyone else who has pulled those commits.

---

> ← Previous: [`24_Git_&_GitHub_Fundamentals`](24_Git_&_GitHub_Fundamentals.md) | Next: [`26_Introduction_to_CICD_and_Jenkins.md`](26_Introduction_to_CICD_and_Jenkins.md) →