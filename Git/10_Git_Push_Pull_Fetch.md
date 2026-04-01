# Git Push, Pull, Fetch

## 🧠 What is it?

These three commands handle communication between your **local repo** and the **remote repo** (like GitHub):

| Command | What it does | Direction | Analogy |
|---------|-------------|-----------|---------|
| `git push` | Upload your commits to the remote | Local → Remote | Sending a letter |
| `git pull` | Download AND merge remote changes | Remote → Local | Receiving and reading a letter |
| `git fetch` | Download remote changes WITHOUT merging | Remote → Local | Checking your mailbox (but not opening the letters) |

In simple words:
- **push** = "Send my work to GitHub"
- **pull** = "Get the latest work from GitHub and merge it into my code"
- **fetch** = "Check if there's anything new on GitHub, but don't change my local code yet"

## ❓ Why do we use it?

### `git push`
- To **share your work** with the team
- To **backup** your commits on GitHub
- To make your code available for **code review** (Pull Requests)
- To **deploy** — many services auto-deploy from GitHub

### `git pull`
- To **get the latest code** from your team
- To **stay updated** before starting new work
- To **get merged changes** after a Pull Request is approved

### `git fetch`
- To **check for updates** without modifying your local work
- To **review changes** before merging them
- To **see what your teammates have done** without disrupting your current work
- When you want to be **careful** and review first, then merge manually

### Why `fetch` when we have `pull`?
> `git pull` = `git fetch` + `git merge`
> 
> Sometimes you want to SEE what changed before automatically merging it into your code. That's when `fetch` is useful.

## ⚙️ How does it work?

### 1. `git push` — Upload Your Changes

```bash
# Push to the default remote and branch
git push

# Push a specific branch to a specific remote
git push origin main

# Push a new branch to remote for the first time
git push -u origin feature/login
# -u sets upstream tracking (so future pushes just need 'git push')

# Push all branches
git push --all

# Push tags
git push --tags
```

#### Push Workflow:

```bash
# 1. Make changes to your code
#    ... edit files ...

# 2. Stage changes
git add .

# 3. Commit
git commit -m "Add user authentication"

# 4. Push to remote
git push
```

#### What if push fails?

```bash
git push
# Error: Updates were rejected because the remote contains work that you don't have locally.
```

This means someone else pushed changes that you don't have. You need to `pull` first:

```bash
git pull origin main   # Get their changes
git push               # Now push yours
```

### 2. `git pull` — Download and Merge Changes

```bash
# Pull from the default remote and branch
git pull

# Pull from a specific remote and branch
git pull origin main

# Pull with rebase instead of merge (cleaner history)
git pull --rebase origin main
```

#### What `git pull` does internally:

```
git pull = git fetch + git merge

Step 1 (fetch): Download new commits from remote
Step 2 (merge): Merge those commits into your current branch
```

#### Pull Workflow:

```bash
# Always pull before starting work!
git checkout main
git pull origin main

# Now create your feature branch
git checkout -b feature/new-stuff
```

#### What if pull causes conflicts?

```bash
git pull origin main
# CONFLICT (content): Merge conflict in index.html
# Automatic merge failed; fix conflicts and then commit the result.

# Resolve the conflict in your editor, then:
git add .
git commit -m "Resolve merge conflict from pull"
```

### 3. `git fetch` — Download Without Merging

```bash
# Fetch from the default remote
git fetch

# Fetch from a specific remote
git fetch origin

# Fetch a specific branch
git fetch origin main

# Fetch all remotes
git fetch --all
```

#### Using fetch + merge (manual pull):

```bash
# Step 1: Fetch the latest changes
git fetch origin

# Step 2: See what changed (compare local vs remote)
git log main..origin/main --oneline
# Shows commits that are on the remote but not in your local main

# Step 3: Review the changes
git diff main origin/main

# Step 4: If everything looks good, merge
git merge origin/main
```

### Comparing Push, Pull, and Fetch:

```
YOUR COMPUTER                    GITHUB
┌──────────────┐                ┌──────────────┐
│              │ ── git push → │              │
│  Local Repo  │               │  Remote Repo │
│              │ ← git pull ── │              │
│              │ ← git fetch ─ │  (download   │
│              │   (download   │   only)       │
│              │    only)      │              │
└──────────────┘                └──────────────┘

push:  Local → Remote (upload commits)
pull:  Remote → Local (download + merge)
fetch: Remote → Local (download only, no merge)
```

### Force Push (⚠️ Dangerous!):

```bash
# Force push — overwrites remote history
git push --force

# Safer force push — only overwrites if no new commits
git push --force-with-lease
```

> ⚠️ **Never force push to shared branches** like `main` or `develop`. Only use it on YOUR personal feature branches.

### Practical Example — Daily Workflow:

```bash
# Morning: Start your day by getting latest changes
git checkout main
git pull origin main

# Create a new branch for your work
git checkout -b feature/search-bar

# Work on your feature...
# ... edit files ...
git add .
git commit -m "Add search bar component"

# ... more work ...
git add .
git commit -m "Add search bar styling"

# End of day: Push your branch to remote
git push -u origin feature/search-bar

# Next morning: Check for updates
git fetch origin
git log --oneline origin/main..HEAD  # See what's new on main

# Merge latest main into your branch
git merge origin/main
```

## 💥 Impact / When to use it?

### When to use each:

| Situation | Command |
|-----------|---------|
| Finished a feature, want to share it | `git push` |
| Starting work, need latest code | `git pull` |
| Want to check for updates without changing your code | `git fetch` |
| Someone finished a code review, you need their changes | `git pull` |
| Want to back up your work on GitHub | `git push` |
| Want to review changes before merging | `git fetch` + `git diff` |

### Benefits:
- ✅ Keep your local and remote repos in sync
- ✅ Share work instantly with your team
- ✅ Get the latest changes before conflicts grow
- ✅ Review changes before merging (with fetch)

### What happens if you don't use them:
- ❌ Your code is only local — no backup
- ❌ Your team can't access your work
- ❌ You'll fall behind and face bigger merge conflicts

## ⚠️ Common Mistakes

1. **Pushing without pulling first** — Always pull before pushing to avoid rejection errors.
2. **Using `git push --force` on shared branches** — This destroys other people's work. Use `--force-with-lease` if you absolutely must force push.
3. **Not fetching regularly** — If you don't check for updates, you'll be surprised by big changes later.
4. **Pulling without committing first** — If you have uncommitted changes, `git pull` might fail or cause messy conflicts. Commit or stash first.
5. **Confusing `fetch` with `pull`** — Remember: `fetch` downloads but doesn't merge. `pull` does both.
6. **Pushing sensitive data** — Always check what you're pushing. Passwords, API keys, and `.env` files should never be pushed!

## 💡 Pro Tips

- 🔥 **Always pull before push** — Make it a habit:
  ```bash
  git pull && git push
  ```
- 🔥 **Use `git pull --rebase`** — Creates a cleaner, linear history instead of merge commits:
  ```bash
  git pull --rebase origin main
  ```
  Make it default:
  ```bash
  git config --global pull.rebase true
  ```
- 🔥 **Use `--force-with-lease` instead of `--force`** — It's safer because it only pushes if nobody else has pushed new commits:
  ```bash
  git push --force-with-lease
  ```
- 🔥 **Fetch before checking teammate's branches** — 
  ```bash
  git fetch origin
  git checkout origin/teammate-branch  # Review their code
  ```
- 🔥 **Set up `git push` default behavior**:
  ```bash
  git config --global push.default current
  # Now 'git push' automatically uses the current branch name
  ```

## 🎤 Interview Questions & Answers

**Q1: What is the difference between `git pull` and `git fetch`?**
> `git fetch` downloads new commits and branches from the remote repository but does NOT merge them into your local branch. `git pull` does both — it fetches and then automatically merges the remote changes into your current branch. In essence, `git pull` = `git fetch` + `git merge`. Fetch is safer when you want to review changes before integrating them.

**Q2: What happens if you try to push but the remote has newer commits?**
> Git will reject the push with an error saying "Updates were rejected because the remote contains work that you do not have locally." You need to first pull (or fetch and merge) the remote changes, resolve any conflicts if necessary, and then push again. You should NOT force push unless you know what you're doing.

**Q3: What is `git push --force-with-lease`?**
> It's a safer alternative to `git push --force`. While `--force` overwrites the remote branch regardless of its state, `--force-with-lease` only pushes if the remote branch hasn't been updated since your last fetch. This prevents accidentally overwriting a teammate's work that you haven't seen yet.

**Q4: When should you use `git pull --rebase`?**
> Use `git pull --rebase` when you want a clean, linear commit history instead of merge commits. It replays your local commits on top of the remote changes instead of creating a merge commit. This makes the history easier to read. It's commonly used in teams that prefer a clean git history.

**Q5: What does `git push -u origin main` do?**
> The `-u` flag (or `--set-upstream`) sets up a tracking relationship between your local `main` branch and `origin/main`. After setting this once, you can simply use `git push` and `git pull` without specifying the remote and branch every time. Git remembers the association.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git push` | Push commits to the tracked remote branch |
| `git push origin main` | Push to a specific remote and branch |
| `git push -u origin <branch>` | Push and set upstream tracking |
| `git push --all` | Push all branches |
| `git push --tags` | Push all tags |
| `git push --force-with-lease` | Safe force push |
| `git pull` | Fetch and merge remote changes |
| `git pull origin main` | Pull from a specific remote/branch |
| `git pull --rebase` | Pull with rebase (clean history) |
| `git fetch` | Download remote changes without merging |
| `git fetch origin` | Fetch from a specific remote |
| `git fetch --all` | Fetch from all remotes |

---

Prev: [Working with Remote Repositories](./09-working-with-remote-repositories.md) | Next: [GitHub Workflow](./11-github-workflow.md)

---
