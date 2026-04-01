# Branching

## 🧠 What is it?

A **branch** in Git is like a **parallel universe** for your code. It lets you create a separate copy of your project where you can work on something without affecting the main code.

Imagine you're writing a book:
- The **main branch** is the published book
- A **new branch** is like a draft notebook where you try new chapter ideas
- If the new chapter is good, you add it to the book (merge)
- If it's bad, you throw away the notebook (delete the branch)

In technical terms:
> A branch is simply a **pointer** to a specific commit. When you create a new branch, Git creates a new pointer — it doesn't copy all your files.

### Key Terms:
- **`main`** (or `master`) — The default/primary branch. This is your "production-ready" code.
- **`HEAD`** — A pointer that tells Git which branch you're currently on.
- **Feature branch** — A branch created to work on a specific feature or bug fix.

## ❓ Why do we use it?

- **Work on features without breaking the main code** — Build a new feature on a separate branch. If it fails, the main branch is untouched.
- **Multiple people can work simultaneously** — Each developer works on their own branch, no stepping on each other's toes.
- **Experiment safely** — Try crazy ideas without risk. Just delete the branch if it doesn't work out.
- **Organized workflow** — Each branch = one task. Makes code reviews and tracking progress much easier.
- **Bug isolation** — Fix a bug on a dedicated branch without mixing it with feature work.

### Real-world example:
You're working on an e-commerce website. Your team needs to:
- Add a payment feature
- Fix a cart bug
- Redesign the homepage

Without branches: Everyone edits the same code → 💥 chaos!

With branches:
```
main
├── feature/payment
├── bugfix/cart-error
└── feature/homepage-redesign
```
Each person works independently. When done, they merge back into `main`. Clean and organized! ✅

## ⚙️ How does it work?

### Create a New Branch:
```bash
# Create a new branch
git branch feature/login

# Create and switch to it immediately (MOST COMMON)
git checkout -b feature/login

# Modern way (Git 2.23+) — Create and switch
git switch -c feature/login
```

### Switch Between Branches:
```bash
# Switch to an existing branch
git checkout main
git checkout feature/login

# Modern way (Git 2.23+)
git switch main
git switch feature/login
```

### List All Branches:
```bash
# List local branches (* shows current branch)
git branch
# Output:
#   feature/login
# * main
#   bugfix/cart

# List all branches (local + remote)
git branch -a

# List remote branches only
git branch -r
```

### Delete a Branch:
```bash
# Delete a merged branch
git branch -d feature/login

# Force delete (even if not merged) — be careful!
git branch -D feature/login
```

### Rename a Branch:
```bash
# Rename current branch
git branch -m new-name

# Rename a specific branch
git branch -m old-name new-name
```

### Complete Branching Workflow Example:

```bash
# Step 1: You're on the main branch
git branch
# * main

# Step 2: Create a new branch for the login feature
git checkout -b feature/login

# Step 3: Make your changes
# ... edit files, write code ...

# Step 4: Stage and commit on this branch
git add .
git commit -m "Add login form with email and password fields"

# Step 5: Make more changes and commits
# ... more editing ...
git add .
git commit -m "Add form validation for login"

# Step 6: Switch back to main when done
git checkout main

# Step 7: Merge the feature branch into main (covered in next topic)
git merge feature/login

# Step 8: Delete the feature branch (it's merged now)
git branch -d feature/login
```

### Visual Representation:

```
Before branching:
main:  A --- B --- C

After creating feature/login at commit C:
main:    A --- B --- C
                      \
feature/login:         D --- E (new commits)

After merging:
main:    A --- B --- C --- D --- E
```

### Branch Naming Conventions:

| Type | Naming Pattern | Example |
|------|---------------|---------|
| Feature | `feature/description` | `feature/user-auth` |
| Bug Fix | `bugfix/description` | `bugfix/login-crash` |
| Hotfix | `hotfix/description` | `hotfix/security-patch` |
| Release | `release/version` | `release/v1.2.0` |
| Experiment | `experiment/description` | `experiment/new-ui` |

## 💥 Impact / When to use it?

### When to create a new branch:
- When you start working on a **new feature**
- When you need to **fix a bug**
- When you want to **experiment** with something
- When you want to **isolate your work** from others
- **Basically always** — never commit directly to `main` in a team!

### Benefits:
- ✅ Main branch stays clean and stable
- ✅ Multiple features can be developed in parallel
- ✅ Easy to abandon failed experiments
- ✅ Clear history of what was done for each feature
- ✅ Makes code reviews through Pull Requests possible

### What happens if you don't use branches:
- ❌ Everyone commits to `main` → constant conflicts
- ❌ Half-done features end up in production
- ❌ Can't work on multiple things at once
- ❌ Debugging becomes harder — all changes are mixed together
- ❌ No way to review code before merging

## ⚠️ Common Mistakes

1. **Working directly on `main`** — Always create a branch! The `main` branch should only receive tested, reviewed code.
2. **Forgetting which branch you're on** — Always check with `git branch` or `git status` before making changes.
3. **Not pulling latest `main` before creating a branch** — Always pull the latest changes first:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/new-stuff
   ```
4. **Creating branches with bad names** — `branch1`, `test`, `my-branch` tell nothing. Use descriptive names like `feature/user-profile-page`.
5. **Not deleting merged branches** — Old branches pile up and create clutter. Delete them after merging.
6. **Having uncommitted changes when switching branches** — Either commit or stash your changes before switching branches.

## 💡 Pro Tips

- 🔥 **Use `git checkout -b` or `git switch -c`** — Creating and switching in one command is faster and you'll never forget to switch.
- 🔥 **Keep branches short-lived** — Long-running branches lead to merge conflicts. Merge frequently!
- 🔥 **Follow a naming convention** — Use prefixes like `feature/`, `bugfix/`, `hotfix/` for clarity.
- 🔥 **Pull latest `main` before creating a new branch** — This ensures your branch starts with the most recent code.
- 🔥 **Use `git branch -v`** — Shows the last commit on each branch, giving you more context.
- 🔥 **Tab completion** — Most terminals support tab completion for branch names. Start typing and press Tab!

## 🎤 Interview Questions & Answers

**Q1: What is a branch in Git?**
> A branch in Git is a lightweight, movable pointer to a commit. It allows you to diverge from the main line of development and work independently on features, bug fixes, or experiments without affecting the main code. Creating a branch doesn't copy files — it just creates a new pointer, making it extremely fast and cheap.

**Q2: What is the difference between `git branch` and `git checkout -b`?**
> `git branch <name>` only creates a new branch but keeps you on the current branch. `git checkout -b <name>` creates a new branch AND switches to it immediately. In practice, `git checkout -b` is used more often because you almost always want to switch to the new branch right after creating it.

**Q3: What is HEAD in Git?**
> HEAD is a special pointer that tells Git which branch (and which commit) you are currently working on. When you switch branches with `git checkout` or `git switch`, HEAD moves to point to the new branch. It's essentially "you are here" marker in your Git history.

**Q4: How do you delete a branch in Git?**
> Use `git branch -d <branch-name>` to delete a merged branch. If the branch hasn't been merged and you want to force delete it, use `git branch -D <branch-name>` (capital D). You cannot delete the branch you're currently on — switch to another branch first.

**Q5: What is a good branching strategy?**
> A common strategy is **Git Flow** or **GitHub Flow**. In GitHub Flow: the `main` branch is always deployable. For every new feature or bug fix, create a branch off `main`, make your changes, open a Pull Request, get it reviewed, and merge it back. This keeps the workflow simple and the main branch stable.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git branch` | List all local branches |
| `git branch <name>` | Create a new branch |
| `git branch -a` | List all branches (local + remote) |
| `git branch -d <name>` | Delete a merged branch |
| `git branch -D <name>` | Force delete a branch |
| `git branch -m <new>` | Rename current branch |
| `git branch -v` | List branches with last commit |
| `git checkout <branch>` | Switch to a branch |
| `git checkout -b <name>` | Create and switch to new branch |
| `git switch <branch>` | Switch to a branch (modern) |
| `git switch -c <name>` | Create and switch (modern) |

---

Prev: [Git Status & Log](./05-git-status-and-log.md) | Next: [Merging & Merge Conflicts](./07-merging-and-merge-conflicts.md)

---
