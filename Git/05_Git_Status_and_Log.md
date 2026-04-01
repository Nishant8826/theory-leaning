# Git Status & Log

## 🧠 What is it?

These two commands are your **eyes and ears** in Git. They help you see what's happening in your project:

| Command | What it does | Analogy |
|---------|-------------|---------|
| `git status` | Shows the **current state** of your files | Looking at your desk to see what's in progress |
| `git log` | Shows the **history** of all commits | Reading your diary to see what you did in the past |

- **`git status`** = "What's happening RIGHT NOW?"
- **`git log`** = "What happened BEFORE?"

## ❓ Why do we use it?

### `git status`
- To see which files have been **modified**
- To see which files are **staged** (ready to commit)
- To see which files are **untracked** (new files Git doesn't know about)
- To check if everything is **clean** (nothing to commit)
- To confirm your actions before committing

### `git log`
- To see the **complete history** of commits
- To find **who made a specific change** and when
- To find a **specific commit** you want to go back to
- To understand **how the project evolved** over time
- To **debug** — "what changed that broke this feature?"

## ⚙️ How does it work?

### `git status` — Check Current State

```bash
git status
```

#### Example Output 1: Untracked files (new files)
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        index.html
        style.css

nothing added to commit but untracked files present
```
This means: You have new files that Git isn't tracking yet. Use `git add` to start tracking them.

#### Example Output 2: Modified files (changed but not staged)
```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   index.html

no changes added to commit
```
This means: You changed `index.html` but haven't staged it yet.

#### Example Output 3: Staged files (ready to commit)
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   index.html
        new file:   about.html
```
This means: These files are in the staging area, ready to be committed.

#### Example Output 4: Clean working directory
```
On branch main
nothing to commit, working tree clean
```
This means: Everything is saved. No pending changes. You're all good! ✅

#### Short Status (Compact View):
```bash
git status -s
```
```
 M index.html      # Modified, not staged
M  style.css       # Modified, staged
?? newfile.js      # Untracked (new file)
A  about.html      # New file, staged
```

| Symbol | Meaning |
|--------|---------|
| `??` | Untracked (new file, not added to Git) |
| `M` (right) | Modified, not yet staged |
| `M` (left) | Modified and staged |
| `A` | New file, added to staging |
| `D` | Deleted |

---

### `git log` — View Commit History

```bash
git log
```

#### Example Output:
```
commit a1b2c3d4e5f6g7h8i9j0 (HEAD -> main)
Author: John Doe <john@example.com>
Date:   Mon Apr 1 10:30:00 2026 +0530

    Add contact page with form validation

commit k1l2m3n4o5p6q7r8s9t0
Author: John Doe <john@example.com>
Date:   Sun Mar 31 15:45:00 2026 +0530

    Fix navbar responsive issue on mobile

commit u1v2w3x4y5z6a7b8c9d0
Author: John Doe <john@example.com>
Date:   Sat Mar 30 09:15:00 2026 +0530

    Initial commit - project setup
```

Each commit shows:
- **Commit hash** — Unique ID (you only need the first 7 characters usually)
- **Author** — Who made the commit
- **Date** — When it was made
- **Message** — What was changed

#### Useful `git log` Variations:

```bash
# One-line format (compact) — MOST USEFUL!
git log --oneline
# Output:
# a1b2c3d Add contact page with form validation
# k1l2m3n Fix navbar responsive issue on mobile
# u1v2w3x Initial commit - project setup

# Show last N commits
git log -5
git log --oneline -5

# Show changes in each commit (what lines changed)
git log -p

# Show stats (which files changed and how many lines)
git log --stat

# Pretty graph view (shows branches visually)
git log --oneline --graph --all

# Filter by author
git log --author="John"

# Filter by date
git log --since="2026-03-01" --until="2026-04-01"

# Filter by commit message
git log --grep="fix"

# Show commits that changed a specific file
git log -- index.html
```

#### Beautiful Graph View:
```bash
git log --oneline --graph --all --decorate
```
```
* a1b2c3d (HEAD -> main) Add contact page
| * f4e5d6c (feature/login) Add login page
|/
* k1l2m3n Fix navbar issue
* u1v2w3x Initial commit
```

This is incredibly useful for seeing how branches relate to each other!

### `git show` — View a Specific Commit

```bash
# Show details of the latest commit
git show

# Show details of a specific commit
git show a1b2c3d
```

### `git diff` — See What Changed (Bonus!)

```bash
# See unstaged changes (what you changed but haven't added)
git diff

# See staged changes (what's ready to commit)
git diff --staged

# Compare two commits
git diff a1b2c3d k1l2m3n
```

## 💥 Impact / When to use it?

### When to use `git status`:
- **Before `git add`** — to see what files have changed
- **After `git add`** — to verify the right files are staged
- **Before `git commit`** — to double-check everything
- **Anytime you're confused** — just run `git status`!

### When to use `git log`:
- To **review history** before pushing code
- To **find a commit** you want to revert to
- To **understand what happened** in a project
- To **debug** — find which commit introduced a bug
- During **code reviews** — see what a team member changed

### Benefits:
- ✅ Never commit the wrong files accidentally
- ✅ Always know the state of your project
- ✅ Easily trace back through history
- ✅ Debug issues by finding when they were introduced

### What happens if you don't use them:
- ❌ You might commit files you didn't intend to
- ❌ You won't know if you have unsaved changes
- ❌ Debugging becomes harder without commit history

## ⚠️ Common Mistakes

1. **Not checking `git status` before committing** — This is the #1 beginner mistake. Always check before you commit!
2. **Ignoring untracked files** — New files show as "untracked". If you don't add them, they won't be in your commit.
3. **Getting overwhelmed by `git log` output** — Use `git log --oneline` for a cleaner view. Press `q` to exit the log viewer.
4. **Not knowing how to exit `git log`** — It uses a pager. Press `q` to quit, `Space` to scroll down, `b` to scroll up.
5. **Forgetting about `git diff`** — `git status` tells you WHICH files changed. `git diff` tells you WHAT lines changed. Use both!

## 💡 Pro Tips

- 🔥 **Always run `git status` before and after each step** — It's your safety net.
- 🔥 **Use `git log --oneline`** — Clean, compact, and easy to read. You'll use this 100x more than the full log.
- 🔥 **Create an alias for the graph view**:
  ```bash
  git config --global alias.lg "log --oneline --graph --all --decorate"
  ```
  Now just type `git lg` for a beautiful graph! 🎨
- 🔥 **Use `git status -s`** — Short and sweet, great for quick checks.
- 🔥 **Use `git log -p -- <filename>`** — Shows the full history of changes for a specific file. Amazing for debugging!

## 🎤 Interview Questions & Answers

**Q1: What does `git status` show?**
> `git status` shows the current state of your working directory and staging area. It tells you which files are modified, which are staged for the next commit, which are untracked (new files), and whether your branch is up-to-date with the remote. It's the most frequently used Git command for understanding what's going on.

**Q2: How can you view the commit history?**
> Use `git log` to see the full commit history, including commit hashes, author info, dates, and messages. For a compact view, use `git log --oneline`. For a visual branch graph, use `git log --oneline --graph --all`. You can also filter by author (`--author`), date (`--since`, `--until`), or message content (`--grep`).

**Q3: What is the difference between `git diff` and `git diff --staged`?**
> `git diff` (without flags) shows changes in your working directory that have NOT been staged yet. `git diff --staged` (or `--cached`) shows changes that HAVE been staged and are ready to be committed. Together, they give you a complete picture of all pending changes.

**Q4: What information does a Git commit contain?**
> Every Git commit contains: a unique SHA-1 hash (identifier), the author's name and email, a timestamp, a commit message, a pointer to the parent commit(s), and a snapshot of the staged files at that point. This information is immutable — once created, it cannot be changed (only replaced).

**Q5: How do you find which commit introduced a bug?**
> You can use `git log` with filters to narrow down commits, `git log -p` to see actual code changes, or `git bisect` which performs a binary search through your commit history to efficiently find the exact commit that introduced the bug. You can also use `git blame <file>` to see who last modified each line.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git status` | Show current state of files |
| `git status -s` | Short/compact status view |
| `git log` | Full commit history |
| `git log --oneline` | Compact one-line history |
| `git log --oneline --graph --all` | Visual branch graph |
| `git log -5` | Show last 5 commits |
| `git log -p` | Show changes in each commit |
| `git log --stat` | Show file change stats |
| `git log --author="name"` | Filter commits by author |
| `git log --grep="text"` | Filter commits by message |
| `git log -- <file>` | History of a specific file |
| `git show <hash>` | View a specific commit's details |
| `git diff` | Show unstaged changes |
| `git diff --staged` | Show staged changes |

---

Prev: [Git Init, Add, Commit](./04-git-init-add-commit.md) | Next: [Branching](./06-branching.md)

---
