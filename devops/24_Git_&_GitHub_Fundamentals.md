# 24 – Git & GitHub Fundamentals

---

## Table of Contents

1. [What is Version Control?](#1-what-is-version-control)
2. [Git – The Local Version Control Tool](#2-git--the-local-version-control-tool)
3. [GitHub – The Cloud Hosting Platform](#3-github--the-cloud-hosting-platform)
4. [Git vs GitHub – Side-by-Side Comparison](#4-git-vs-github--side-by-side-comparison)
5. [Market Landscape](#5-market-landscape)
6. [The Git Workflow – Step by Step](#6-the-git-workflow--step-by-step)
7. [Core Git Commands Explained](#7-core-git-commands-explained)
8. [First-Time Git Configuration](#8-first-time-git-configuration)
9. [Visual Diagrams](#9-visual-diagrams)
10. [Scenario-Based Q&A](#10-scenario-based-qa)
11. [Interview Q&A](#11-interview-qa)

---

## 1. What is Version Control?

### What
Version control is a system that **tracks and manages changes** to files over time. Think of it like Google Docs' version history — but far more powerful, built specifically for code.

### Why
Without version control:
- You'd manually save files like `project_v1.py`, `project_v2_final.py`, `project_v2_FINAL_REAL.py` 😅
- Two developers editing the same file would overwrite each other's work
- One bad change could destroy months of work with no way to recover
- There'd be no record of *who* changed *what* and *when*

With version control:
- Every change is recorded with a timestamp and author
- You can travel back to any point in history
- Multiple people can work on the same codebase simultaneously
- The entire project history is preserved forever

### How
The system works by taking **snapshots** (called commits) of your project at different points in time. Each snapshot stores only the *differences* from the previous version, making it space-efficient.

### Impact

| Without Version Control | With Version Control |
|--------------------------|----------------------|
| Manual file duplication | Automatic history tracking |
| Easy to lose work | Always recoverable |
| Hard to collaborate | Seamless teamwork |
| No accountability | Full audit trail |
| Single point of failure | Distributed copies |

---

## 2. Git – The Local Version Control Tool

### What
Git is a **free, open-source, distributed version control system** that runs on your local machine. It was created by **Linus Torvalds** (the same person who created Linux) in **2005**.

> 💡 "Distributed" means every developer has a full copy of the entire project history on their own machine — not just the latest version.

### Why
Git was built because the Linux kernel development team needed a fast, reliable, and distributed way to manage contributions from thousands of developers worldwide. Previous tools were too slow or required constant server connectivity.

### How
Git manages your code through **three local areas**:

```
Working Directory  →  Staging Area  →  Local Repository
  (your files)       (what you've      (committed history)
                      selected)
```

1. You **edit files** in your Working Directory
2. You **stage changes** (choose what to include)
3. You **commit** (save a permanent snapshot)

### Impact
- ✅ Works 100% offline — no internet needed
- ✅ Extremely fast (everything is local)
- ✅ Full history available even without server access
- ❌ Without a remote (like GitHub), code stays only on your machine

---

## 3. GitHub – The Cloud Hosting Platform

### What
GitHub is a **web-based cloud platform** that hosts Git repositories online. It is owned by **Microsoft** (acquired in 2018 for $7.5 billion). Think of it as "Dropbox for code" — but with collaboration superpowers.

### Why
Git alone stores everything locally. GitHub solves the problem of:
- Sharing code with teammates or the world
- Having a central backup in the cloud
- Providing a web interface to browse code, history, and issues
- Enabling collaboration features like Pull Requests, Code Reviews, Actions (CI/CD)

### How
1. You do your work **locally using Git**
2. You **push** your commits to GitHub
3. Your teammates **pull** those commits to their machines
4. Changes are reviewed, merged, and tracked on the GitHub platform

### Impact
- ✅ 24/7 availability of your codebase from anywhere
- ✅ Built-in collaboration and code review tools
- ✅ Free public repositories (open source friendly)
- ✅ Integrates with deployment, testing, and project management tools
- ❌ Requires internet to sync
- ❌ Code is on Microsoft's servers (use self-hosted GitLab for full control)

---

## 4. Git vs GitHub – Side-by-Side Comparison

| Feature | Git | GitHub |
|--------|-----|--------|
| **Type** | Software / Tool | Web Platform / Service |
| **Where it runs** | Your local machine | Cloud (Microsoft servers) |
| **Created by** | Linus Torvalds (2005) | Tom Preston-Werner (2008) |
| **Owned by** | Open Source Community | Microsoft |
| **Internet needed?** | ❌ No | ✅ Yes |
| **Purpose** | Track changes locally | Host & collaborate remotely |
| **Can it exist alone?** | ✅ Yes | ❌ Needs Git |
| **Cost** | Free | Free (paid plans available) |
| **Alternatives** | SVN, Mercurial | GitLab, Bitbucket, Azure Repos |

> 🔑 **Key Insight:** Git is the **engine**, GitHub is the **garage** where you park and share your work.

---

## 5. Market Landscape

### Git Adoption
- **99% of developers** use Git as their version control system
- It has essentially replaced all older systems (SVN, CVS, Perforce)

### Hosting Platform Market Share

```
Git Hosting Market Share (2026 estimate)
─────────────────────────────────────────
GitHub     ████████████████████████████  70%
GitLab     ████████                      10%
Bitbucket  ████████                      10%
Others     ████████                      10%
```

### Why GitHub Dominates
- First mover advantage (launched 2008)
- Largest open-source community
- Microsoft's backing and integration (VS Code, Azure)
- GitHub Actions for CI/CD
- Copilot AI integration

---

## 6. The Git Workflow – Step by Step

This is the **exact workflow** practiced in class — the same one used by professional developers every day.

### Setup Phase (One-Time)
```
[Install Git] → [Create GitHub Account] → [Configure Identity]
```

### Daily Development Workflow
```
[Edit Files] → [git add] → [git commit] → [git push] → [GitHub]
```

### Full First-Time Project Setup
```
Step 1: git init              → Create a local repo
Step 2: git add *             → Stage all files
Step 3: git commit -m "msg"   → Commit to local repo
Step 4: git branch -M main    → Rename branch to "main"
Step 5: git remote add origin → Link to GitHub repo
Step 6: git push origin main  → Upload to GitHub
```

### File Status Lifecycle

```
Untracked (Red)
      │
      │  git add
      ▼
  Tracked/Staged (Green)
      │
      │  git commit
      ▼
  Committed (Snapshot saved)
      │
      │  git push
      ▼
  Remote (GitHub)
```

---

## 7. Core Git Commands Explained

### `git init`
- **What:** Initializes a brand new Git repository in the current folder
- **What it creates:** A hidden `.git/` folder that stores all version history
- **When to use:** Once, at the start of every new project

```bash
git init
# Output: Initialized empty Git repository in /your/project/.git/
```

---

### `git add *`
- **What:** Moves files from *Untracked* → *Staged* (tells Git "include these in the next snapshot")
- **`*`** means "add everything"; you can also add specific files: `git add file.py`
- **Analogy:** Like putting items into a shopping cart before checkout

```bash
git add *          # Add all files
git add index.html # Add a specific file
git add src/       # Add an entire folder
```

---

### `git commit -m "message"`
- **What:** Takes a permanent snapshot of your staged changes
- **`-m`** flag lets you write a message describing what you changed
- **Analogy:** Clicking "Save Version" with a label attached
- **Best practice:** Write meaningful messages — e.g., `"Add login page UI"` not `"stuff"`

```bash
git commit -m "Initial commit: project setup"
```

---

### `git branch -M main`
- **What:** Renames the current branch to `main`
- **Why:** Git historically named the default branch `master`; GitHub and the industry now uses `main` as the standard
- **`-M`** forces the rename even if a branch named `main` already exists

```bash
git branch -M main
```

---

### `git remote add origin [URL]`
- **What:** Links your local repository to a remote GitHub repository
- **`origin`** is just a nickname for the remote URL (you could name it anything, but `origin` is the universal convention)
- **When to use:** Once per project, after creating the repo on GitHub

```bash
git remote add origin https://github.com/username/repo-name.git
```

---

### `git push origin main`
- **What:** Uploads your local commits to GitHub
- **`origin`** = the remote (GitHub)
- **`main`** = the branch you're pushing
- **Analogy:** Uploading your saved file to the cloud

```bash
git push origin main
```

---

## 8. First-Time Git Configuration

Before Git can commit anything, it needs to know **who you are**. This is a one-time setup.

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Why is this needed?
Every commit records **who made it**. Without this config, Git won't know how to label your commits, which breaks collaboration and accountability.

### `--global` flag
This saves the config for **all repositories** on your machine. Without `--global`, it only applies to the current project.

### Verify your config
```bash
git config --list
# Shows all current Git configuration settings
```

---

## 9. Visual Diagrams

### Diagram 1: Git's Three Areas

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR LOCAL MACHINE                   │
│                                                         │
│  ┌──────────────┐   git add   ┌──────────────┐          │
│  │   Working    │ ──────────► │   Staging    │          │
│  │  Directory   │             │    Area      │          │
│  │              │             │              │          │
│  │ (your files) │ ◄────────── │  (selected   │          │
│  │              │  git restore│   changes)   │          │
│  └──────────────┘             └──────┬───────┘          │
│                                      │ git commit        │
│                                      ▼                   │
│                               ┌──────────────┐          │
│                               │    Local     │          │
│                               │  Repository  │          │
│                               │  (.git dir)  │          │
│                               └──────┬───────┘          │
└──────────────────────────────────────┼──────────────────┘
                                       │ git push
                                       ▼
                              ┌─────────────────┐
                              │     GITHUB      │
                              │  (Remote Repo)  │
                              │   origin/main   │
                              └─────────────────┘
```

---

### Diagram 2: Full First-Time Setup Flow

```
[You on Local Machine]                    [GitHub]
        │                                     │
        │  1. git init                        │
        │  (create .git folder)               │
        │                                     │
        │  2. Write your code                 │
        │                                     │
        │  3. git add *                       │
        │  (stage changes)                    │
        │                                     │
        │  4. git commit -m "msg"             │
        │  (save snapshot)                    │
        │                                     │
        │  5. git branch -M main              │
        │  (set branch name)                  │
        │                                     │
        │  6. git remote add origin [URL]     │ ← You create an
        │  (link to GitHub)                   │   empty repo here
        │                                     │
        │  7. git push origin main ──────────►│
        │                                     │ Code is now on GitHub!
```

---

### Diagram 3: Market Share Visualization

```
Version Control Tool Usage
──────────────────────────
Git       ██████████████████████████████████████████████████ 99%
Others    █ 1%

Git Hosting Platforms
─────────────────────
GitHub    ██████████████████████████████████  70%
GitLab    █████  10%
Bitbucket █████  10%
Others    █████  10%
```

---

### Diagram 4: File Status Lifecycle

```
           ┌──────────────────────────────────────────┐
           │                git add                   │
           │                                          │
   New  ───►  UNTRACKED  ──────────►  STAGED  ──────► COMMITTED
   File        (Red)      git add     (Green)  commit  (Snapshot)
                │                                          │
                │◄─────────────────────────────────────────│
                          modify file again
```

---

## 10. Scenario-Based Q&A

---

🔍 **Scenario 1:** You've been working on a feature for 3 days. Your teammate accidentally overwrites a key file. You need to restore yesterday's version.

✅ **Answer:** Because you committed your work daily using `git commit`, you can use `git log` to find yesterday's commit hash and `git checkout <commit-hash> -- filename` to restore exactly that file. Without Git, this recovery would be impossible.

---

🔍 **Scenario 2:** You're starting a new project on your laptop and want to eventually share it with your team on GitHub.

✅ **Answer:** Run `git init` in your project folder, write your code, then `git add *` and `git commit -m "Initial commit"`. Create a new repo on GitHub, then connect it with `git remote add origin [URL]` and upload with `git push origin main`. Your team can now clone it.

---

🔍 **Scenario 3:** You joined a new company and they use GitLab instead of GitHub. Will your Git skills still work?

✅ **Answer:** Yes, completely. Git is the underlying tool — GitLab and GitHub are just different hosting platforms. All the commands (`git add`, `git commit`, `git push`, etc.) remain identical. Only the remote URL changes.

---

🔍 **Scenario 4:** You ran `git push origin main` but got an error saying Git doesn't know who you are.

✅ **Answer:** You haven't configured your Git identity yet. Run:
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```
Then retry the push. This is a one-time setup per machine.

---

🔍 **Scenario 5:** You want to push only `index.html` and not the rest of your messy files.

✅ **Answer:** Instead of `git add *` (which stages everything), use `git add index.html` to stage only that specific file. Then commit and push as usual. This gives you fine-grained control over what goes into each commit.

---

🔍 **Scenario 6:** Your manager asks "Where is our codebase stored?" and the answer should be accessible 24/7 from anywhere.

✅ **Answer:** The code is hosted on GitHub (a cloud platform). Any team member with access can pull, view, or contribute at any time, from anywhere in the world, without needing to be on the same network.

---

## 11. Interview Q&A

---

**Q1. What is the difference between Git and GitHub?**

**A:** Git is a **version control tool** installed locally on your machine that tracks changes to your code. GitHub is a **cloud-based hosting platform** that stores Git repositories online and enables collaboration. Git can work without GitHub, but GitHub depends on Git. Think of Git as the engine and GitHub as the cloud garage where you park your code.

---

**Q2. Why was Git created, and who created it?**

**A:** Git was created by **Linus Torvalds in 2005** to manage the Linux kernel source code. He needed a distributed, fast, and reliable version control system after the previous tool (BitKeeper) became unavailable. Git was designed to handle large projects with thousands of contributors efficiently.

---

**Q3. What is the difference between `git add` and `git commit`?**

**A:**
- `git add` moves files to the **Staging Area** — it tells Git "I want to include these changes in my next snapshot." It does NOT save permanently.
- `git commit` takes the staged changes and creates a **permanent snapshot** in the local repository with a unique ID and message.

Think of it as: `git add` = putting items in a cart, `git commit` = placing the order.

---

**Q4. What does `git remote add origin [URL]` do?**

**A:** It creates a **named connection** between your local repository and a remote repository (e.g., on GitHub). `origin` is the conventional nickname for the primary remote. Without this step, Git doesn't know where to push your code. You only run this once per project.

---

**Q5. What is a branch, and why did we run `git branch -M main`?**

**A:** A branch is an **independent line of development**. `git branch -M main` renames the current branch to `main`. GitHub and the industry moved from the old default name `master` to `main` for inclusivity. The `-M` flag forces the rename. This ensures your local branch name matches GitHub's expected default branch name.

---

**Q6. What is the significance of the `.git` folder created by `git init`?**

**A:** The `.git` folder is the **heart of your repository**. It stores the entire history of your project — every commit, every branch, every configuration. Deleting this folder would erase all version history (though your current files remain). You should never manually edit files inside `.git`.

---

**Q7. Why does Git have a Staging Area? Why not just commit directly?**

**A:** The Staging Area gives you **fine-grained control** over what goes into each commit. Imagine you've made 10 changes — 7 are related to a bug fix and 3 are unfinished experiments. You can `git add` only the 7 bug-fix files and commit them cleanly, leaving the other 3 for later. This creates a **clean, meaningful commit history** instead of a chaotic one.

---

**Q8. What is `git push` and how is it different from `git commit`?**

**A:**
- `git commit` saves a snapshot to your **local** repository only — no internet required
- `git push` uploads those local commits to the **remote** repository (e.g., GitHub)

You can have many local commits that aren't pushed yet. `git push` is what actually shares your work with the world or your team.

---

**Q9. GitHub holds 70% of the market — what are its main competitors and when would you choose them?**

**A:**
- **GitLab (10%)** – Often chosen for **self-hosted installations** (your own server), strong CI/CD built-in, preferred in enterprise for privacy
- **Bitbucket (10%)** – Tight integration with **Atlassian tools** (Jira, Confluence), popular in teams already using those tools
- **GitHub (70%)** – Best for **open source**, largest community, best Copilot/AI integration, Microsoft Azure synergy

---

**Q10. What happens if two developers push to the same branch at the same time?**

**A:** Git will reject the second push with a conflict error. The second developer must first **pull** the latest changes (`git pull`), resolve any conflicts in the files manually, commit the resolved version, and then push again. This is why branches and pull requests exist — to prevent this scenario in team environments.

---

*Notes created from class session: April 20, 2026*  
*Topic: Git & GitHub Fundamentals — DevOps Series*

> ← Previous: [`23_aws_lambda_&_serverless_architecture`](23_aws_lambda_&_serverless_architecture.md) | Next: [`25_Git_&_GitHub_Deep_Dive_Branching_PRs_&_Collaboration`](25_Git_&_GitHub_Deep_Dive_Branching_PRs_&_Collaboration.md) →