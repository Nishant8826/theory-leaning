# Git Stash

## 🧠 What is it?

**Git Stash** is like a **temporary pocket** where you can save your unfinished work without committing it. It lets you "pause" your current changes, do something else, and then "resume" later.

Think of it like this:
- You're cooking dinner 🍳
- Suddenly someone rings the doorbell 🔔
- You put your cooking aside temporarily (stash)
- Handle the visitor (switch branch, fix a bug)
- Come back and continue cooking (pop the stash)

In technical terms:
> `git stash` saves your uncommitted changes (both staged and unstaged) and reverts your working directory to the last commit. You can re-apply the saved changes later.

## ❓ Why do we use it?

The most common scenarios:

1. **Need to switch branches but have uncommitted work**
   ```
   You: *working on feature/login*
   Boss: "Hey, there's an urgent bug on main!"
   You: *can't switch branches with uncommitted changes*
   Solution: Stash your work → switch to main → fix bug → switch back → pop stash
   ```

2. **Want to pull latest changes but have local modifications**
   ```
   git pull won't work if you have uncommitted changes that conflict.
   Solution: Stash → pull → pop stash
   ```

3. **Accidentally started working on the wrong branch**
   ```
   You made changes but realize you're on main instead of a feature branch.
   Solution: Stash → create/switch to correct branch → pop stash
   ```

4. **Want to temporarily clean your working directory**
   ```
   You want to run tests or check something with a clean state.
   Solution: Stash → run tests → pop stash
   ```

## ⚙️ How does it work?

### Basic Stash:

```bash
# Save your current changes to the stash
git stash

# Add a descriptive message (RECOMMENDED)
git stash save "WIP: login form validation"
# or (modern syntax)
git stash push -m "WIP: login form validation"
```

Output:
```
Saved working directory and index state WIP on feature/login: abc1234 Last commit message
```

Your working directory is now clean! ✅

### Bring Changes Back:

```bash
# Apply the most recent stash AND remove it from stash list
git stash pop

# Apply the most recent stash but KEEP it in stash list
git stash apply

# Apply a specific stash (by index)
git stash pop stash@{2}
git stash apply stash@{1}
```

**Difference between `pop` and `apply`:**

| Command | Re-applies changes? | Removes from stash? |
|---------|---------------------|---------------------|
| `git stash pop` | ✅ Yes | ✅ Yes (if no conflicts) |
| `git stash apply` | ✅ Yes | ❌ No (stays in stash) |

### View Your Stashes:

```bash
# List all stashes
git stash list
# Output:
# stash@{0}: WIP on feature/login: abc1234 Add login page
# stash@{1}: WIP on main: def5678 Fix header
# stash@{2}: On feature/cart: WIP: cart total calculation
```

Stashes work like a **stack** (Last In, First Out):
- `stash@{0}` = Most recent stash
- `stash@{1}` = Second most recent
- etc.

### See What's in a Stash:

```bash
# Show what changed in the most recent stash
git stash show

# Show detailed changes (like git diff)
git stash show -p

# Show a specific stash
git stash show stash@{1}
git stash show -p stash@{1}
```

### Delete Stashes:

```bash
# Delete a specific stash
git stash drop stash@{0}

# Delete ALL stashes (careful!)
git stash clear
```

### Stash Specific Files:

```bash
# Stash only specific files
git stash push -m "stash only styles" style.css layout.css

# Stash including untracked (new) files
git stash -u
# or
git stash --include-untracked

# Stash everything including ignored files
git stash -a
# or
git stash --all
```

### Create a Branch from a Stash:

```bash
# Create a new branch and apply the stash to it
git stash branch new-feature-branch

# Create from a specific stash
git stash branch new-branch stash@{2}
```

This is super useful when you realize your stashed work should be on its own branch!

### Complete Workflow Example:

```bash
# Scenario: You're working on a feature, but need to fix an urgent bug

# 1. You're on feature/login with uncommitted changes
git status
# Shows: modified files

# 2. Stash your work
git stash push -m "WIP: login form validation in progress"

# 3. Your directory is now clean
git status
# Shows: nothing to commit, working tree clean

# 4. Switch to main and fix the bug
git checkout main
git pull origin main
git checkout -b hotfix/security-patch

# ... fix the bug ...
git add .
git commit -m "Fix security vulnerability in auth"
git push -u origin hotfix/security-patch

# 5. Go back to your feature branch
git checkout feature/login

# 6. Restore your stashed work
git stash pop
# Your unfinished work is back! ✅

# 7. Continue working on your feature
git status
# Shows: your modified files are back
```

## 💥 Impact / When to use it?

### When to use Git Stash:
- When you need to **switch branches** but have uncommitted work
- When you need to **pull changes** but have local modifications
- When you **started work on the wrong branch**
- When you want to **temporarily clean** your working directory
- When you want to **save partial work** without a messy commit

### When NOT to use Git Stash:
- **For long-term storage** — Stashes are meant to be temporary. If you need to keep changes for days, commit them on a branch instead.
- **When a commit would be better** — If your work is at a logical checkpoint, a "WIP" commit is better than a stash.
- **When you have too many stashes** — If you have 10+ stashes, you're probably misusing it. Keep it clean!

### Benefits:
- ✅ Quick and easy to use
- ✅ No messy "WIP" commits in your history
- ✅ Can switch contexts instantly
- ✅ Stash works across branches

### What happens if you don't use stash:
- ❌ You'd have to commit unfinished work (messy history)
- ❌ Or lose your changes when switching branches
- ❌ Or create temporary branches for every small context switch

## ⚠️ Common Mistakes

1. **Forgetting about stashes** — Stashes are easy to forget. Use `git stash list` regularly to check.
2. **Stashing without a message** — `git stash` with no message makes it hard to remember what each stash contains. Always use `-m "description"`.
3. **Having too many stashes** — If you have 5+ stashes, you're hoarding. Review and drop old ones.
4. **Confusing `pop` and `apply`** — `pop` removes the stash after applying. `apply` keeps it. Use `pop` unless you specifically need to keep the stash.
5. **Stashing untracked files** — By default, `git stash` doesn't include new (untracked) files. Use `git stash -u` to include them.
6. **Not handling stash conflicts** — If `git stash pop` causes conflicts, the stash isn't removed. You need to resolve conflicts and then manually drop the stash.

## 💡 Pro Tips

- 🔥 **Always add a message**:
  ```bash
  git stash push -m "WIP: halfway through cart redesign"
  ```
  Future you will thank present you!

- 🔥 **Use `-u` flag to include new files**:
  ```bash
  git stash -u  # Includes untracked (new) files
  ```

- 🔥 **Use `git stash branch`** — If you realize your stashed work deserves its own branch:
  ```bash
  git stash branch feature/cart-redesign
  ```

- 🔥 **Create an alias for stash with message**:
  ```bash
  git config --global alias.save "stash push -m"
  # Now: git save "my stash message"
  ```

- 🔥 **Pop stash into a different branch** — Stashes aren't branch-specific. You can stash on one branch and pop on another:
  ```bash
  git checkout feature/login
  git stash push -m "this work belongs on another branch"
  git checkout feature/signup
  git stash pop  # Apply it here instead!
  ```

## 🎤 Interview Questions & Answers

**Q1: What is `git stash` and when would you use it?**
> `git stash` temporarily saves your uncommitted changes (both staged and unstaged) without creating a commit. It cleans your working directory so you can switch branches or pull changes. Common use cases include: switching to fix an urgent bug on another branch, pulling latest changes when you have local modifications, or temporarily cleaning your workspace.

**Q2: What is the difference between `git stash pop` and `git stash apply`?**
> Both re-apply stashed changes to your working directory. The difference is: `git stash pop` removes the stash from the stash list after applying it. `git stash apply` applies the changes but keeps the stash in the list, so you can apply it again or to another branch. If `pop` encounters conflicts, the stash is NOT removed.

**Q3: How do you stash untracked (new) files?**
> By default, `git stash` only saves tracked files that have been modified. To include untracked (new) files, use `git stash -u` or `git stash --include-untracked`. To include even gitignored files, use `git stash -a` or `git stash --all`.

**Q4: Can you stash changes on one branch and apply them on another?**
> Yes! Stashes are not branch-specific. You can stash changes on one branch, switch to any other branch, and pop/apply the stash there. This is useful when you accidentally started working on the wrong branch. You can even create a new branch from a stash using `git stash branch <branch-name>`.

**Q5: What happens if `git stash pop` causes a conflict?**
> If applying a stash causes a merge conflict, Git will show the conflicted files just like a regular merge conflict. You need to resolve the conflicts manually, then stage the files with `git add`. Importantly, the stash is NOT automatically removed when there are conflicts (even with `pop`), so you need to manually drop it with `git stash drop` after resolving.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git stash` | Stash current changes |
| `git stash push -m "message"` | Stash with a description |
| `git stash -u` | Stash including untracked files |
| `git stash list` | View all stashes |
| `git stash show` | Preview stash changes |
| `git stash show -p` | Preview stash changes in detail |
| `git stash pop` | Apply and remove most recent stash |
| `git stash apply` | Apply stash (keep it in list) |
| `git stash pop stash@{N}` | Apply and remove specific stash |
| `git stash drop stash@{N}` | Delete a specific stash |
| `git stash clear` | Delete ALL stashes |
| `git stash branch <name>` | Create a branch from a stash |

---

Prev: [Rebasing](./13-rebasing.md) | Next: [.gitignore](./15-gitignore.md)

---
