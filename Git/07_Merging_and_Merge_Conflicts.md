# Merging & Merge Conflicts

## 🧠 What is it?

**Merging** is the process of combining changes from one branch into another. It's how you bring your feature work back into the main codebase.

**Merge conflicts** happen when Git can't automatically combine changes because two branches modified the **same lines** in the **same file**.

Think of it like this:
- **Merge** = Two people wrote separate chapters and you combine them into one book ✅
- **Merge conflict** = Two people edited the **same paragraph** differently, and you need to decide which version to keep (or combine both) ⚠️

## ❓ Why do we use it?

- **Combine work** — After finishing a feature on a branch, you merge it into `main` to include it in the project.
- **Team collaboration** — When multiple developers work on different branches, merging brings all their work together.
- **Keep main updated** — Regular merging ensures the main branch has all the latest features and fixes.

### Why do merge conflicts happen?
- Two developers changed the **same line** in the **same file**
- One developer deleted a file that another developer was editing
- Two developers added different content at the **same location** in a file

This is **normal** and **not scary**! It just means Git needs your help deciding what the final code should look like.

## ⚙️ How does it work?

### Basic Merge:

```bash
# Step 1: Switch to the branch you want to merge INTO (usually main)
git checkout main

# Step 2: Merge the feature branch into main
git merge feature/login
```

### Types of Merges:

#### 1. Fast-Forward Merge (Simple)
When `main` hasn't changed since you created the feature branch:

```
Before:
main:           A --- B
                       \
feature/login:          C --- D

After git merge (fast-forward):
main:           A --- B --- C --- D
```

Git just moves the `main` pointer forward. No extra commit needed!

```bash
git checkout main
git merge feature/login
# Output: Fast-forward
```

#### 2. Three-Way Merge (Common)
When both `main` and the feature branch have new commits:

```
Before:
main:           A --- B --- E
                       \
feature/login:          C --- D

After git merge (creates merge commit):
main:           A --- B --- E --- M (merge commit)
                       \         /
feature/login:          C --- D
```

Git creates a special "merge commit" that combines both histories.

```bash
git checkout main
git merge feature/login
# Output: Merge made by the 'ort' strategy.
```

---

### Handling Merge Conflicts:

When Git can't merge automatically, you'll see:

```bash
git merge feature/login
# Output:
# Auto-merging index.html
# CONFLICT (content): Merge conflict in index.html
# Automatic merge failed; fix conflicts and then commit the result.
```

#### What the conflict looks like in your file:

```html
<h1>Welcome to our website</h1>
<<<<<<< HEAD
<p>This is the homepage - updated by main branch</p>
=======
<p>This is the login page - updated by feature branch</p>
>>>>>>> feature/login
```

Understanding the markers:
| Marker | Meaning |
|--------|---------|
| `<<<<<<< HEAD` | Start of YOUR current branch's version |
| `=======` | Separator between the two versions |
| `>>>>>>> feature/login` | End of the INCOMING branch's version |

#### Steps to Resolve a Merge Conflict:

```bash
# Step 1: Open the conflicted file in your editor

# Step 2: Decide what to keep:
# Option A: Keep YOUR version (HEAD)
# Option B: Keep THEIR version (feature/login)
# Option C: Keep BOTH (combine them)
# Option D: Write something completely new

# Step 3: Remove ALL conflict markers (<<<<<<, =======, >>>>>>>)

# Step 4: Save the file
```

**Example Resolution (keeping both):**
```html
<h1>Welcome to our website</h1>
<p>This is the homepage with a login feature</p>
```

```bash
# Step 5: Stage the resolved file
git add index.html

# Step 6: Complete the merge with a commit
git commit -m "Merge feature/login into main, resolve homepage conflict"
```

#### Abort a Merge (if you want to cancel):
```bash
# Cancel the merge and go back to before
git merge --abort
```

### Complete Conflict Resolution Workflow:

```bash
# 1. Attempt to merge
git checkout main
git merge feature/login

# 2. If conflict occurs, check which files have conflicts
git status
# Shows: "both modified: index.html"

# 3. Open each conflicted file and resolve manually

# 4. After fixing all conflicts
git add .
git commit -m "Merge feature/login, resolve conflicts in index.html"

# 5. Verify the merge
git log --oneline --graph
```

## 💥 Impact / When to use it?

### When to merge:
- When a **feature is complete** and tested
- When a **bug fix** needs to go into `main`
- When you want to **update your branch** with the latest `main` changes
- After a **Pull Request** is approved

### Benefits:
- ✅ Combines work from multiple developers seamlessly
- ✅ Preserves the history of both branches
- ✅ Git resolves most conflicts automatically
- ✅ You have full control over conflict resolution

### What happens if you don't merge properly:
- ❌ Features stay isolated and never make it to production
- ❌ Unresolved conflicts lead to broken code
- ❌ The longer you wait to merge, the more conflicts you'll face

## ⚠️ Common Mistakes

1. **Panicking when seeing merge conflicts** — They're normal! Every developer deals with them. Just read the markers carefully and resolve them.
2. **Leaving conflict markers in the code** — Always remove `<<<<<<<`, `=======`, and `>>>>>>>` completely. Leaving them will break your code!
3. **Not testing after resolving conflicts** — Always test your code after a merge to make sure nothing is broken.
4. **Merging without pulling latest changes** — Always pull the latest `main` before merging:
   ```bash
   git checkout main
   git pull origin main
   git merge feature/login
   ```
5. **Deleting someone else's code during conflict resolution** — Be careful! Read both versions and understand what each does before deciding.
6. **Ignoring `git status` during conflicts** — It tells you exactly which files have conflicts that need resolution.

## 💡 Pro Tips

- 🔥 **Merge `main` into your feature branch regularly** — This keeps your branch up-to-date and reduces conflicts at the end:
  ```bash
  git checkout feature/login
  git merge main
  ```
- 🔥 **Use VS Code for conflict resolution** — It highlights conflicts beautifully and gives you buttons to "Accept Current", "Accept Incoming", or "Accept Both".
- 🔥 **Keep branches short-lived** — The longer a branch lives, the more it diverges from `main`, and the more conflicts you'll face.
- 🔥 **Use `git merge --no-ff`** — Forces a merge commit even for fast-forward merges. This preserves the branch history:
  ```bash
  git merge --no-ff feature/login
  ```
- 🔥 **Communicate with your team** — If multiple people are editing the same files, coordinate to minimize conflicts.

## 🎤 Interview Questions & Answers

**Q1: What is a merge conflict in Git?**
> A merge conflict occurs when Git cannot automatically merge two branches because both branches have modified the same lines in the same file. Git marks the conflicting sections in the file with special markers (`<<<<<<<`, `=======`, `>>>>>>>`), and the developer must manually resolve the conflict by choosing which changes to keep.

**Q2: How do you resolve a merge conflict?**
> 1. Run `git status` to see which files have conflicts. 2. Open each conflicted file and look for the conflict markers. 3. Decide which version to keep (or combine both). 4. Remove all conflict markers. 5. Stage the resolved files with `git add`. 6. Complete the merge with `git commit`. You can also use `git merge --abort` to cancel the merge entirely.

**Q3: What is the difference between a fast-forward merge and a three-way merge?**
> A fast-forward merge happens when the target branch (e.g., `main`) has no new commits since the feature branch was created. Git simply moves the pointer forward. A three-way merge happens when both branches have new commits. Git creates a special "merge commit" that combines both histories. You can force a merge commit even for fast-forward cases using `--no-ff`.

**Q4: What does `git merge --abort` do?**
> `git merge --abort` cancels an in-progress merge and restores your branch to the state it was in before the merge attempt. This is useful when you encounter conflicts that you're not ready to resolve, or when you realize you're merging the wrong branch.

**Q5: How can you prevent merge conflicts?**
> While you can't always avoid them, you can minimize them by: merging `main` into your feature branch regularly, keeping branches short-lived, communicating with your team about who's working on which files, making small focused commits, and using a clear branching strategy.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git merge <branch>` | Merge a branch into current branch |
| `git merge --no-ff <branch>` | Merge with a merge commit (no fast-forward) |
| `git merge --abort` | Cancel an in-progress merge |
| `git status` | Check which files have conflicts |
| `git add <file>` | Mark a conflict as resolved |
| `git commit` | Complete the merge after resolving conflicts |
| `git log --oneline --graph` | View merge history visually |
| `git diff` | See current conflicts/changes |

---

Prev: [Branching](./06-branching.md) | Next: [Undo Changes](./08-undo-changes.md)

---
