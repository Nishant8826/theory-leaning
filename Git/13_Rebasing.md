# Rebasing

## 🧠 What is it?

**Rebasing** is an alternative to merging that **replays your commits on top of another branch**, creating a clean, linear history.

Imagine a timeline:
- **Merge** = Two rivers joining together (you can see where they split and merged)
- **Rebase** = One straight river (it looks like everything happened in order, one after another)

```
MERGE creates this:
main:    A --- B --- E --- M (merge commit)
                \         /
feature:         C --- D

REBASE creates this:
main:    A --- B --- E --- C' --- D'
(Everything is in a straight line — no merge commit!)
```

Notice: After rebasing, commits C and D become C' and D' — they're **new copies** with different hashes, because they're now based on commit E instead of B.

In simple words:
> **Rebasing** = "Take my changes and put them on top of the latest code, as if I started my work from the most recent version."

## ❓ Why do we use it?

- **Clean history** — No messy merge commits. The history reads like a straight story.
- **Easier debugging** — With a linear history, `git bisect` and `git log` are much easier to use.
- **Better readability** — When looking at commit history, it's clear what happened and in what order.
- **Keep your branch updated** — Rebase your feature branch on top of latest `main` to stay current.

### Merge vs Rebase — When to use which:

| Aspect | Merge | Rebase |
|--------|-------|--------|
| **History** | Shows branching/merging (non-linear) | Clean, straight line (linear) |
| **Extra commits** | Creates a merge commit | No extra commits |
| **Safety** | Safe (never rewrites history) | Dangerous if used on shared branches |
| **Complexity** | Simple | Slightly more complex |
| **Best for** | Shared/public branches | Personal/feature branches |

## ⚙️ How does it work?

### Basic Rebase:

```bash
# You're on your feature branch
git checkout feature/login

# Rebase your branch on top of the latest main
git rebase main
```

#### What happens step by step:

```
Before rebase:
main:    A --- B --- E
                \
feature:         C --- D (you are here)

Step 1: Git "detaches" your commits (C, D)
Step 2: Git moves to the tip of main (E)  
Step 3: Git replays your commits one by one on top of E

After rebase:
main:    A --- B --- E
                      \
feature:               C' --- D' (clean!)
```

Now your branch is up-to-date AND has a clean history!

### Rebase Workflow (Keeping Your Branch Updated):

```bash
# Step 1: Make sure main is up to date
git checkout main
git pull origin main

# Step 2: Switch to your feature branch
git checkout feature/login

# Step 3: Rebase onto main
git rebase main

# Step 4: If there are conflicts, resolve them
# (Git will pause and tell you which files have conflicts)

# Step 5: After resolving conflicts
git add .
git rebase --continue

# Step 6: If you want to cancel the rebase
git rebase --abort

# Step 7: Push (you might need --force-with-lease since history changed)
git push --force-with-lease
```

### Handling Rebase Conflicts:

```bash
git rebase main
# CONFLICT: Merge conflict in index.html
# Fix conflicts in your editor, then:

git add index.html
git rebase --continue

# If you get another conflict (in a different commit), fix it again:
git add .
git rebase --continue

# Repeat until all commits are replayed successfully
```

> Note: During rebase, you might get conflicts for EACH commit being replayed, not just once like in merge.

### Interactive Rebase — The Power Tool:

Interactive rebase (`git rebase -i`) lets you **edit, reorder, squash, or delete commits** before sharing them.

```bash
# Interactively rebase the last 4 commits
git rebase -i HEAD~4
```

This opens an editor showing your commits:

```
pick abc1234 Add login form
pick def5678 Fix typo in login
pick ghi9012 Add form validation
pick jkl3456 Fix another typo

# Commands:
# p, pick = use commit as-is
# r, reword = use commit but change message
# e, edit = use commit but stop to edit
# s, squash = merge with previous commit (keep messages)
# f, fixup = merge with previous commit (discard message)
# d, drop = delete the commit
```

#### Common Interactive Rebase Actions:

**Squash commits** (combine multiple into one):
```
pick abc1234 Add login form
squash def5678 Fix typo in login
squash ghi9012 Add form validation
squash jkl3456 Fix another typo

# Result: All 4 commits become 1 commit
```

**Reword a commit message**:
```
reword abc1234 Add login form
pick def5678 Fix typo in login

# Git will open an editor to change the first commit's message
```

**Reorder commits**:
```
pick ghi9012 Add form validation
pick abc1234 Add login form     # moved down
pick def5678 Fix typo in login

# Commits are now in a different order
```

**Drop (delete) a commit**:
```
pick abc1234 Add login form
drop def5678 Fix typo in login  # this commit is removed
pick ghi9012 Add form validation
```

### `git pull --rebase` — Cleaner Pulls:

```bash
# Instead of: git pull (which does fetch + merge)
# Use: git pull --rebase (does fetch + rebase)
git pull --rebase origin main

# Make it the default:
git config --global pull.rebase true
```

## 💥 Impact / When to use it?

### When to use rebase:
- ✅ **Updating your feature branch** with the latest `main`
- ✅ **Cleaning up commit history** before opening a PR (interactive rebase)
- ✅ **Squashing messy commits** into clean, logical ones
- ✅ **`git pull --rebase`** for cleaner pulls without merge commits

### When NOT to use rebase:
- ❌ **NEVER rebase a branch that others are working on** — Rebase rewrites commit history. If someone else has pulled your branch, rebasing creates confusion.
- ❌ **NEVER rebase `main` or shared branches** — This breaks everyone's work
- ❌ When you want to **preserve the exact history** of how things happened

### The Golden Rule of Rebasing:
> **Never rebase commits that have been pushed to a shared/public branch.**
> 
> Only rebase YOUR OWN commits on YOUR OWN branches that nobody else is using.

### Benefits:
- ✅ Clean, linear git history
- ✅ Easier to understand project evolution
- ✅ Better for debugging (git bisect works great)
- ✅ Cleaner Pull Requests

### Risks:
- ⚠️ Rewrites history (changes commit hashes)
- ⚠️ Can cause problems if used on shared branches
- ⚠️ Requires force push after rebasing

## ⚠️ Common Mistakes

1. **Rebasing shared branches** — The #1 rebase sin. NEVER rebase `main`, `develop`, or any branch others are using.
2. **Force pushing after rebase to shared branches** — This overwrites others' work. Only force push to YOUR personal branches.
3. **Not understanding that rebase rewrites history** — After rebase, commit hashes change. Old references become invalid.
4. **Panicking during rebase conflicts** — Just like merge conflicts, resolve them calmly. Use `git rebase --abort` if you need to start over.
5. **Using rebase without understanding it** — Practice on a test repo first! Create two branches, make conflicting changes, and try rebasing.
6. **Forgetting `--force-with-lease` when pushing after rebase** — Regular `git push` will be rejected. Use `--force-with-lease` (not `--force`!).

## 💡 Pro Tips

- 🔥 **Use interactive rebase to clean up before PRs**:
  ```bash
  git rebase -i HEAD~5  # Clean up last 5 commits
  ```
  Squash "fix typo" commits into the main feature commit for a cleaner PR!

- 🔥 **Always use `--force-with-lease` instead of `--force`**:
  ```bash
  git push --force-with-lease
  ```
  It's safer because it checks if someone else pushed in the meantime.

- 🔥 **Set rebase as default for pull**:
  ```bash
  git config --global pull.rebase true
  ```

- 🔥 **Use `--autosquash` with fixup commits**:
  ```bash
  # Mark a commit as a fixup for a previous commit
  git commit --fixup abc1234
  
  # Later, autosquash will combine them automatically
  git rebase -i --autosquash HEAD~5
  ```

- 🔥 **If rebase goes wrong, use reflog**:
  ```bash
  git reflog
  git reset --hard HEAD@{n}  # Go back to before the rebase
  ```

## 🎤 Interview Questions & Answers

**Q1: What is the difference between merge and rebase?**
> Both integrate changes from one branch into another, but they do it differently. **Merge** creates a new merge commit that ties two branches together, preserving the branching history. **Rebase** replays your commits on top of the target branch, creating a linear history without merge commits. Merge is safer (doesn't rewrite history), while rebase produces a cleaner log.

**Q2: What is interactive rebase?**
> Interactive rebase (`git rebase -i`) lets you modify commits before they're replayed. You can reorder commits, squash multiple commits into one, reword commit messages, edit commit content, or drop commits entirely. It's commonly used to clean up commit history before opening a Pull Request.

**Q3: When should you NOT use rebase?**
> Never rebase commits that have already been pushed to a shared/public branch (like `main` or `develop`). Since rebase rewrites commit history (changes hashes), it breaks the history for other developers who have pulled those commits. Only rebase on your personal feature branches.

**Q4: What happens when you rebase and encounter conflicts?**
> Git pauses the rebase at the conflicting commit and lets you resolve the conflict. After resolving, you run `git add` on the fixed files and then `git rebase --continue` to proceed. This might happen multiple times if several commits have conflicts. You can use `git rebase --abort` to cancel and go back to the pre-rebase state.

**Q5: What is `git pull --rebase` and why would you use it?**
> `git pull --rebase` fetches remote changes and replays your local commits on top of them instead of creating a merge commit. This results in a cleaner, linear history. It's equivalent to `git fetch` + `git rebase origin/main`. It's useful when you want to keep your history clean and avoid unnecessary merge commits from pulling.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git rebase main` | Rebase current branch onto main |
| `git rebase --continue` | Continue after resolving conflict |
| `git rebase --abort` | Cancel the rebase |
| `git rebase --skip` | Skip the current conflicting commit |
| `git rebase -i HEAD~N` | Interactive rebase (last N commits) |
| `git pull --rebase` | Pull with rebase instead of merge |
| `git push --force-with-lease` | Push after rebase (safe force) |
| `git commit --fixup <hash>` | Create a fixup commit |
| `git rebase -i --autosquash` | Auto-squash fixup commits |

---

Prev: [Pull Requests](./12-pull-requests.md) | Next: [Git Stash](./14-git-stash.md)

---
