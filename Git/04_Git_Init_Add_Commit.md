# Git Init, Add, Commit

## 🧠 What is it?

These are the **three most fundamental Git commands** you'll use every single day. They form the basic workflow of Git:

| Command | What it does | Analogy |
|---------|-------------|---------|
| `git init` | Creates a new Git repository | Opening a new notebook |
| `git add` | Stages changes (prepares them to be saved) | Writing your answer in pencil |
| `git commit` | Saves staged changes permanently | Writing over it in pen (permanent!) |

Think of it as a **3-step save process**:
1. **Init** — "I want to start tracking this folder"
2. **Add** — "These are the changes I want to save"
3. **Commit** — "Save them permanently with a description"

## ❓ Why do we use it?

### `git init`
- To **start tracking** a project with Git
- Without this, Git doesn't know your folder exists
- It creates a hidden `.git` folder that stores all the tracking history

### `git add`
- To **select which changes** you want to include in the next save
- Not every change needs to be saved together — you can pick and choose
- It moves files from the **Working Directory** to the **Staging Area**

### `git commit`
- To **permanently save** your staged changes
- Each commit is a snapshot of your project at that moment
- It creates a record in the project history that you can go back to anytime

### Why not just save directly?
Because Git gives you **control**. Maybe you changed 10 files but only want to save 3 of them in this commit. The staging area lets you choose.

## ⚙️ How does it work?

### 1. `git init` — Initialize a Repository

```bash
# Navigate to your project folder
cd my-project

# Initialize Git
git init
```

**What happens:**
- Git creates a hidden `.git` folder inside your project
- This folder contains all the tracking data
- Your project is now a "Git repository"

```bash
# You'll see this message:
Initialized empty Git repository in /path/to/my-project/.git/
```

> ⚠️ **Never** manually edit or delete the `.git` folder. It contains your entire project history!

### 2. `git add` — Stage Changes

```bash
# Add a specific file
git add index.html

# Add multiple specific files
git add index.html style.css script.js

# Add all changed files (most common)
git add .

# Add all files of a specific type
git add *.js
```

**What happens:**
- The file moves from **Working Directory** to **Staging Area**
- It's now "ready to be committed"
- You can still make more changes or unstage it

```
Before git add:
  Working Directory: index.html (modified)
  Staging Area: (empty)

After git add index.html:
  Working Directory: (clean)
  Staging Area: index.html (ready to commit)
```

### 3. `git commit` — Save Changes Permanently

```bash
# Commit with a message (most common way)
git commit -m "Add homepage layout"

# Commit with a detailed message (opens text editor)
git commit

# Add and commit in one step (only works for already-tracked files)
git commit -am "Fix header alignment"
```

**What happens:**
- Git takes a snapshot of everything in the staging area
- Creates a unique hash (ID) for this commit
- Records the author, timestamp, and your message
- The staging area is now clean

```bash
# Output looks like:
[main abc1234] Add homepage layout
 1 file changed, 25 insertions(+)
```

### Complete Workflow Example:

```bash
# Step 1: Create a project and initialize Git
mkdir my-website
cd my-website
git init

# Step 2: Create some files
echo "<h1>Hello World</h1>" > index.html
echo "body { margin: 0; }" > style.css

# Step 3: Check what's happening
git status
# Shows: 2 untracked files

# Step 4: Stage the files
git add .

# Step 5: Check again
git status
# Shows: 2 files ready to be committed

# Step 6: Commit
git commit -m "Create initial homepage with basic styling"

# Step 7: Verify
git log
# Shows your commit with hash, author, date, and message
```

### Writing Good Commit Messages:

```bash
# ❌ BAD commit messages:
git commit -m "fix"
git commit -m "update"
git commit -m "done"
git commit -m "changes"
git commit -m "asdfgh"

# ✅ GOOD commit messages:
git commit -m "Add user login form with validation"
git commit -m "Fix navbar not showing on mobile screens"
git commit -m "Remove unused CSS classes for better performance"
git commit -m "Update README with installation instructions"
```

**Commit message formula:**
> **Action word** + **What was changed** + **Why (optional)**
> Example: "Fix search bar not returning results for special characters"

## 💥 Impact / When to use it?

### When to use each:
| Command | When |
|---------|------|
| `git init` | Once per project — at the very beginning |
| `git add` | Every time you want to prepare changes for saving |
| `git commit` | Every time you want to permanently save your changes |

### Benefits:
- ✅ Track every change in your project
- ✅ Choose exactly what to include in each save
- ✅ Go back to any previous commit if something breaks
- ✅ Each commit tells a story of how your project evolved

### What happens if you don't use them:
- ❌ Without `git init` — No tracking at all
- ❌ Without `git add` — Git doesn't know which changes to save
- ❌ Without `git commit` — Changes exist but aren't permanently saved

## ⚠️ Common Mistakes

1. **Running `git init` in the wrong folder** — Make sure you're in the correct project folder. Running `git init` in your Desktop or home directory is a mess!
2. **Forgetting to `git add` before committing** — If you skip `git add`, your commit will be empty or won't include your recent changes.
3. **Making huge commits** — Don't combine 20 unrelated changes in one commit. Each commit should be one logical change.
4. **Writing meaningless commit messages** — "fix" and "update" don't help. Be descriptive.
5. **Not checking `git status` before committing** — Always check what's staged before committing to avoid surprises.
6. **Running `git init` inside another Git repo** — This creates nested repos, which causes confusion. Check if `.git` already exists before running `git init`.

## 💡 Pro Tips

- 🔥 **Use `git status` before every add and commit** — It shows exactly what's going on.
- 🔥 **Use `git add -p`** — This lets you stage parts of a file (specific lines), not the whole file. Super useful for clean commits!
- 🔥 **Use `git commit -am "message"`** — This combines add + commit for files that are already tracked. Saves time!
- 🔥 **Use `.gitignore`** — Create this file to tell Git which files to ignore (like `node_modules`, `.env`, etc.).
- 🔥 **Follow conventional commits** — Many teams use prefixes like:
  ```
  feat: Add user registration
  fix: Resolve login crash on mobile
  docs: Update API documentation
  style: Format code with prettier
  refactor: Simplify validation logic
  ```

## 🎤 Interview Questions & Answers

**Q1: What does `git init` do?**
> `git init` initializes a new Git repository in the current directory. It creates a hidden `.git` folder that contains all the metadata and object database for version control. After running this command, Git starts tracking changes in that directory.

**Q2: What is the staging area in Git?**
> The staging area (also called the "index") is an intermediate zone between your working directory and the repository. When you run `git add`, files move to the staging area. It lets you review and select exactly which changes to include in the next commit, giving you fine-grained control over your saves.

**Q3: What is the difference between `git add .` and `git add -A`?**
> `git add .` stages new and modified files in the current directory and its subdirectories. `git add -A` (or `git add --all`) stages all changes including deletions across the entire repository. In modern Git versions (2.x+), they behave almost identically when run from the repo root.

**Q4: Can you modify a commit after making it?**
> Yes, you can amend the most recent commit using `git commit --amend`. This lets you change the commit message or add forgotten files. However, you should NOT amend commits that have already been pushed to a shared remote repository, as it rewrites history.

**Q5: What makes a good commit message?**
> A good commit message is short (under 72 characters for the subject line), written in imperative mood ("Add feature" not "Added feature"), and clearly describes what the change does and why. It should be specific enough that someone reading the project history can understand the change without looking at the code.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git init` | Initialize a new Git repository |
| `git add <file>` | Stage a specific file |
| `git add .` | Stage all changes in current directory |
| `git add -A` | Stage all changes (including deletions) |
| `git add -p` | Interactively stage parts of files |
| `git commit -m "message"` | Commit with an inline message |
| `git commit` | Commit (opens editor for message) |
| `git commit -am "message"` | Add + commit tracked files in one step |
| `git commit --amend` | Modify the last commit |
| `git status` | Show current state of working directory and staging |

---

Prev: [Installation & Setup](./03-installation-and-setup.md) | Next: [Git Status & Log](./05-git-status-and-log.md)

---
