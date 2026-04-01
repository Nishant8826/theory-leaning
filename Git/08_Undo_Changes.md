# Undo Changes (reset, revert, checkout)

## 🧠 What is it?

Git gives you powerful ways to **undo mistakes**. Whether you changed a file by accident, committed something wrong, or want to go back to a previous version — Git has you covered.

There are three main tools for undoing changes:

| Command | What it does | Analogy |
|---------|-------------|---------|
| `git checkout` | Discard changes in a file (go back to last commit) | Erasing what you wrote and starting over |
| `git reset` | Move commits backward (unstage or remove commits) | Ripping pages out of your notebook |
| `git revert` | Create a NEW commit that undoes a previous commit | Writing a correction note instead of ripping the page |

**Key difference:**
- `git reset` = **Rewrites history** (removes commits — as if they never happened)
- `git revert` = **Preserves history** (adds a new "undo" commit — the original commit still exists)

## ❓ Why do we use it?

- **Everyone makes mistakes** — typos, wrong files committed, broken code pushed
- **Experiment safely** — try something and easily go back if it doesn't work
- **Clean up commits** — remove unnecessary or accidental commits
- **Fix production issues** — quickly revert a bad deployment

### When to use which:

| Situation | Use |
|-----------|-----|
| Changed a file, want to discard changes | `git checkout` or `git restore` |
| Staged a file, want to unstage | `git reset HEAD` or `git restore --staged` |
| Made a commit locally, want to undo it | `git reset` |
| Made a commit that's already pushed, want to undo | `git revert` |
| Want to go back in time temporarily | `git checkout <hash>` |

## ⚙️ How does it work?

### 1. Discard Changes in Working Directory

You modified a file but want to throw away the changes:

```bash
# Old way (still works)
git checkout -- index.html

# Modern way (Git 2.23+) — RECOMMENDED
git restore index.html

# Discard ALL changes in all files
git restore .
```

> ⚠️ This permanently deletes your uncommitted changes. There's no going back!

### 2. Unstage Files (Remove from Staging Area)

You ran `git add` but want to un-add:

```bash
# Old way
git reset HEAD index.html

# Modern way — RECOMMENDED
git restore --staged index.html

# Unstage everything
git restore --staged .
```

The changes stay in your working directory — they're just removed from staging.

### 3. `git reset` — Undo Commits

`git reset` has three modes:

```
git reset --soft   → Keeps changes in staging area
git reset --mixed  → Keeps changes in working directory (DEFAULT)
git reset --hard   → Deletes everything (DANGEROUS!)
```

#### Visual Explanation:

```
Commit History: A --- B --- C --- D (HEAD)

After git reset --soft B:
  Commits C and D are removed from history
  BUT their changes are still in the staging area (ready to re-commit)

After git reset --mixed B: (default)
  Commits C and D are removed from history
  Their changes are in the working directory (unstaged)

After git reset --hard B:
  Commits C and D are removed from history
  ALL changes are GONE. Working directory is clean.
```

#### Examples:

```bash
# Undo the last commit, keep changes staged
git reset --soft HEAD~1

# Undo the last commit, keep changes unstaged (default)
git reset HEAD~1

# Undo the last commit, DELETE everything
git reset --hard HEAD~1

# Undo the last 3 commits
git reset HEAD~3

# Reset to a specific commit
git reset --hard abc1234
```

#### Understanding HEAD~N:

| Reference | Meaning |
|-----------|---------|
| `HEAD` | Current commit |
| `HEAD~1` | 1 commit before current |
| `HEAD~2` | 2 commits before current |
| `HEAD~3` | 3 commits before current |

### 4. `git revert` — Safely Undo a Commit

Unlike `reset`, `revert` creates a **new commit** that undoes a previous commit. The original commit stays in history.

```bash
# Revert the most recent commit
git revert HEAD

# Revert a specific commit
git revert abc1234

# Revert without auto-committing (lets you edit first)
git revert --no-commit abc1234
```

#### How it looks in history:

```
Before:
A --- B --- C --- D (HEAD)

After git revert C:
A --- B --- C --- D --- E (HEAD)
                        ↑
                  "Revert C" (undoes changes from C)
```

Commit C still exists, but commit E cancels out its changes.

### 5. `git checkout` — Time Travel (Detached HEAD)

You can temporarily visit a past commit:

```bash
# Go to a specific commit (just to look around)
git checkout abc1234

# You're now in "detached HEAD" state
# You can look around but shouldn't commit here

# Go back to your branch
git checkout main
```

### 6. `git commit --amend` — Fix the Last Commit

```bash
# Change the last commit message
git commit --amend -m "New, better commit message"

# Add forgotten files to the last commit
git add forgotten-file.js
git commit --amend --no-edit
```

### Quick Reference — What to Use When:

```
"I changed a file, want to undo"
  → git restore <file>

"I staged a file, want to unstage"
  → git restore --staged <file>

"I committed something wrong (NOT pushed yet)"
  → git reset HEAD~1

"I committed and ALREADY pushed"
  → git revert <commit-hash>

"I want to see an old version"
  → git checkout <commit-hash>

"I want to fix my last commit message"
  → git commit --amend -m "new message"
```

## 💥 Impact / When to use it?

### When to use `git reset`:
- When you're working **locally** and haven't pushed yet
- When you want to **restructure your commits** before pushing
- When you committed the **wrong files**
- Use `--soft` to keep your work, `--hard` to start fresh

### When to use `git revert`:
- When the commit is **already pushed** to a shared repo
- When you need to **maintain history** (in a team environment)
- When you want a **safe undo** that doesn't rewrite history
- In **production hotfixes** — revert the bad commit immediately

### Benefits:
- ✅ Peace of mind — you can always go back
- ✅ Clean history — fix mistakes before they reach the team
- ✅ Safe collaboration — `revert` doesn't disrupt teammates

### What happens if you use them wrong:
- ❌ `git reset --hard` on pushed commits → Other team members will have conflicts
- ❌ Force pushing after reset → Teammates lose their work
- ❌ Using reset on shared branches → Destroys the shared history

## ⚠️ Common Mistakes

1. **Using `git reset --hard` when you meant `--soft`** — `--hard` permanently deletes your changes. Start with `--soft` or `--mixed` to be safe.
2. **Using `git reset` on already-pushed commits** — This rewrites history! Other team members will have problems. Use `git revert` instead.
3. **Force pushing after reset** (`git push --force`) — This overwrites the remote history and can destroy your teammates' work. Only do this on YOUR personal branches.
4. **Not understanding detached HEAD** — If you `git checkout` a commit hash, you're in "detached HEAD" state. Don't make commits here. Go back to a branch first.
5. **Panic-resetting everything** — Take a breath! Check `git reflog` — Git keeps track of everything, even "deleted" commits. You can almost always recover.

## 💡 Pro Tips

- 🔥 **`git reflog` is your safety net** — Even after a `git reset --hard`, your commits aren't truly gone. `git reflog` shows every action Git has taken, and you can recover "lost" commits:
  ```bash
  git reflog
  # Find the commit hash you want
  git checkout <hash>
  ```
- 🔥 **Use `git restore` instead of `git checkout`** — The modern `git restore` command is clearer and less confusing.
- 🔥 **Use `--soft` by default** — It's the safest reset option. You can always do more, but you can't undo `--hard`.
- 🔥 **Practice on a test repo** — Create a throwaway repo and experiment with reset, revert, and checkout. Understanding by doing is the best way!
- 🔥 **Add `alias.undo` to your config**:
  ```bash
  git config --global alias.undo "reset --soft HEAD~1"
  ```
  Now `git undo` will safely undo your last commit!

## 🎤 Interview Questions & Answers

**Q1: What is the difference between `git reset` and `git revert`?**
> `git reset` moves the branch pointer backward, effectively removing commits from history. It's used for local, unpushed changes. `git revert` creates a new commit that undoes the changes of a previous commit while preserving the original history. It's safe to use on pushed/shared branches because it doesn't rewrite history.

**Q2: What are the three modes of `git reset`?**
> 1. `--soft`: Moves HEAD back but keeps changes in the staging area (ready to re-commit). 2. `--mixed` (default): Moves HEAD back and unstages changes, but keeps them in the working directory. 3. `--hard`: Moves HEAD back and deletes all changes completely. `--hard` is destructive and should be used with caution.

**Q3: How do you recover a commit after `git reset --hard`?**
> Use `git reflog`, which records every change made to HEAD. Find the commit hash of the "lost" commit in the reflog, then run `git checkout <hash>` or `git reset --hard <hash>` to recover it. Git keeps reflog entries for about 90 days by default.

**Q4: What is a "detached HEAD" state?**
> Detached HEAD occurs when you checkout a specific commit (by its hash) instead of a branch. In this state, HEAD points directly to a commit rather than a branch. Any new commits made here won't belong to any branch and can be lost. To save work done in a detached HEAD, create a branch: `git checkout -b new-branch-name`.

**Q5: When should you use `git revert` instead of `git reset`?**
> Use `git revert` when the commit has already been pushed to a shared/remote repository. Since `revert` creates a new commit instead of rewriting history, it doesn't affect other developers' work. Using `git reset` on pushed commits and force-pushing would overwrite the remote history, causing problems for everyone on the team.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git restore <file>` | Discard changes in working directory |
| `git restore --staged <file>` | Unstage a file |
| `git reset --soft HEAD~1` | Undo last commit, keep changes staged |
| `git reset HEAD~1` | Undo last commit, keep changes unstaged |
| `git reset --hard HEAD~1` | Undo last commit, DELETE all changes |
| `git reset --hard <hash>` | Reset to a specific commit |
| `git revert <hash>` | Create undo commit for a specific commit |
| `git revert HEAD` | Revert the most recent commit |
| `git revert --no-commit <hash>` | Revert without auto-committing |
| `git commit --amend -m "msg"` | Fix last commit message |
| `git checkout <hash>` | Visit a past commit (detached HEAD) |
| `git reflog` | View history of all HEAD movements |

---

Prev: [Merging & Merge Conflicts](./07-merging-and-merge-conflicts.md) | Next: [Working with Remote Repositories](./09-working-with-remote-repositories.md)

---
