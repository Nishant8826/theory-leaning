# GitHub Workflow

## 🧠 What is it?

A **GitHub workflow** is a structured way of working with GitHub in a team. It defines **how** and **when** you create branches, make changes, push code, review code, and merge it.

The most popular workflow is called **GitHub Flow** — it's simple and works great for most teams:

```
1. Create a branch from main
2. Make changes and commit
3. Push the branch to GitHub
4. Open a Pull Request (PR)
5. Team reviews the code
6. Merge the PR into main
7. Delete the branch
```

Think of it like a restaurant kitchen:
- You don't cook in the dining area (don't code on `main`)
- You prepare food in the kitchen (work on a branch)
- The head chef checks the food (code review via Pull Request)
- If approved, it goes to the customer (merged into `main`)

## ❓ Why do we use it?

- **Organized teamwork** — Everyone knows the process
- **Code quality** — Every change is reviewed before merging
- **No broken code in `main`** — The main branch stays clean and deployable
- **Easy rollbacks** — If something breaks, you know which PR caused it
- **History is clear** — Each feature/fix has its own branch and PR
- **Industry standard** — Almost every tech company uses this workflow

Without a workflow:
- ❌ Everyone pushes to `main` → broken code everywhere
- ❌ No code review → bugs slip through
- ❌ No process → confusion and conflicts

## ⚙️ How does it work?

### GitHub Flow — Step by Step:

#### Step 1: Start from the Latest `main`

```bash
git checkout main
git pull origin main
```

Always make sure you have the latest code before starting anything new.

#### Step 2: Create a Feature Branch

```bash
git checkout -b feature/user-profile
```

Name it descriptively based on what you're building.

#### Step 3: Make Changes and Commit

```bash
# Edit your files...
# Then stage and commit

git add .
git commit -m "Add user profile page layout"

# Make more changes...
git add .
git commit -m "Add profile picture upload feature"
```

Make small, focused commits. Each commit should do ONE thing.

#### Step 4: Push the Branch to GitHub

```bash
git push -u origin feature/user-profile
```

Your branch is now on GitHub for others to see.

#### Step 5: Open a Pull Request (PR) on GitHub

1. Go to your repo on GitHub
2. You'll see a prompt: "feature/user-profile had recent pushes — Compare & pull request"
3. Click **"Compare & pull request"**
4. Fill in:
   - **Title**: Clear description of the feature (e.g., "Add user profile page")
   - **Description**: What you did, why, screenshots if UI changes
5. Select **reviewers** (teammates who should review your code)
6. Click **"Create pull request"**

#### Step 6: Code Review

Your teammates will:
- Read your code changes
- Leave comments or suggestions
- Request changes if needed
- Approve when everything looks good

```
Common review feedback:
- "Can you rename this variable to be more descriptive?"
- "This function is too long, can you split it?"
- "Add error handling for this API call"
- "LGTM!" (Looks Good To Me) ✅
```

If changes are requested:
```bash
# Fix the issues locally
git add .
git commit -m "Address review: rename variables, add error handling"
git push
# The PR updates automatically!
```

#### Step 7: Merge the Pull Request

Once approved:
1. Click **"Merge pull request"** on GitHub
2. Choose merge strategy:
   - **Merge commit** — Preserves all commits (default)
   - **Squash and merge** — Combines all commits into one
   - **Rebase and merge** — Replays commits on top of main
3. Click **"Confirm merge"**
4. Click **"Delete branch"** (cleanup!)

#### Step 8: Update Local Main

```bash
git checkout main
git pull origin main
git branch -d feature/user-profile  # Delete local branch too
```

### Complete Visual Flow:

```
┌─────────────────────────────────────────────────────┐
│ 1. git checkout main && git pull                     │
│ 2. git checkout -b feature/xyz                       │
│ 3. Make changes → git add → git commit              │
│ 4. git push -u origin feature/xyz                    │
│ 5. Open Pull Request on GitHub                       │
│ 6. Code Review (teammates review your changes)       │
│ 7. Merge PR on GitHub                                │
│ 8. git checkout main && git pull (get merged code)   │
│ 9. git branch -d feature/xyz (cleanup)               │
└─────────────────────────────────────────────────────┘
```

### Writing a Good Pull Request:

```markdown
## What does this PR do?
Adds the user profile page where users can view and edit their information.

## Changes Made
- Created ProfilePage component
- Added profile picture upload with preview
- Added form validation for email and phone
- Added API integration for saving profile data

## Screenshots
![Profile page screenshot](link-to-screenshot)

## How to Test
1. Log in as any user
2. Navigate to /profile
3. Try editing your name and uploading a photo
4. Verify changes are saved

## Related Issues
Closes #42
```

### Fork & Contribute Workflow (Open Source):

```bash
# 1. Fork the repo on GitHub (click "Fork" button)

# 2. Clone YOUR fork
git clone https://github.com/YOUR-username/repo.git
cd repo

# 3. Add the original repo as "upstream"
git remote add upstream https://github.com/ORIGINAL-author/repo.git

# 4. Create a branch
git checkout -b fix/typo-readme

# 5. Make changes, commit, push to YOUR fork
git add .
git commit -m "Fix typo in README"
git push origin fix/typo-readme

# 6. Open a PR from YOUR fork to the ORIGINAL repo on GitHub

# 7. Keep your fork updated
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## 💥 Impact / When to use it?

### When to use GitHub Flow:
- **Any team project** — Even teams of 2 should use PRs
- **Open-source contributions** — Fork + PR is the standard
- **Personal projects** — Good practice even when working alone
- **Job interviews** — Knowing this workflow is expected

### Benefits:
- ✅ Clean, reviewable code
- ✅ `main` is always deployable
- ✅ Easy to track what changed and why
- ✅ Team members learn from each other through code reviews
- ✅ Easy to revert — just revert the specific PR

### What happens without a workflow:
- ❌ `main` branch breaks frequently
- ❌ No code review → more bugs
- ❌ Hard to track who did what
- ❌ Merge conflicts become nightmares

## ⚠️ Common Mistakes

1. **Pushing directly to `main`** — Always use a branch and a Pull Request. Protect the `main` branch in GitHub settings!
2. **Making PRs too large** — A PR with 50+ file changes is hard to review. Keep PRs small and focused.
3. **Not writing PR descriptions** — Reviewers need context. Explain what you did and why.
4. **Not updating your branch before opening a PR** — Merge the latest `main` into your branch first to avoid conflicts.
5. **Ignoring review feedback** — Code review isn't criticism, it's collaboration. Address feedback or discuss it.
6. **Not deleting branches after merging** — Old branches pile up. Delete them to keep the repo clean.

## 💡 Pro Tips

- 🔥 **Enable branch protection** — In GitHub repo settings, protect `main` to require PR reviews before merging.
- 🔥 **Use PR templates** — Create a `.github/pull_request_template.md` file so every PR has a consistent format.
- 🔥 **Request specific reviewers** — Tag people who know the area of code you changed.
- 🔥 **Use draft PRs** — Open a "Draft" PR when your work is in progress. It signals that it's not ready for review yet.
- 🔥 **Link PRs to issues** — Use keywords like "Closes #42" in your PR description to auto-close issues when merged.
- 🔥 **Review your own PR before requesting reviews** — Click "Files changed" and read through everything. You'll catch mistakes!

## 🎤 Interview Questions & Answers

**Q1: What is GitHub Flow?**
> GitHub Flow is a lightweight, branch-based workflow for teams using GitHub. The process is: create a branch from `main`, make changes and commit, push the branch, open a Pull Request for code review, address feedback, merge into `main`, and delete the branch. It keeps the `main` branch always deployable and ensures all code is reviewed before integration.

**Q2: What is a Pull Request?**
> A Pull Request (PR) is a feature on GitHub that lets you propose changes to a repository. It shows the differences between your branch and the target branch, allows teammates to review your code, leave comments, suggest changes, and ultimately approve and merge the changes. It's the primary tool for code review on GitHub.

**Q3: What is the difference between a fork and a clone?**
> A clone creates a local copy of a repository on your computer. A fork creates a copy of someone else's repository under YOUR GitHub account. Forks are used in open-source contributions — you fork the original repo, make changes in your fork, and submit a Pull Request back to the original. Cloning is just downloading; forking creates your own remote copy.

**Q4: What are some common merge strategies in a Pull Request?**
> 1. **Merge commit**: Creates a merge commit preserving all individual commits — maintains full history. 2. **Squash and merge**: Combines all commits into a single commit — creates a cleaner history on `main`. 3. **Rebase and merge**: Replays commits on top of `main` without a merge commit — creates a linear history.

**Q5: Why is code review important?**
> Code review catches bugs before they reach production, improves code quality and consistency, spreads knowledge across the team (everyone learns different parts of the codebase), helps junior developers learn from seniors, ensures coding standards are followed, and creates documentation through PR descriptions and comments.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git checkout main && git pull` | Start from latest main |
| `git checkout -b feature/xyz` | Create a feature branch |
| `git add . && git commit -m "msg"` | Stage and commit changes |
| `git push -u origin feature/xyz` | Push branch to GitHub |
| `git checkout main && git pull` | Update local after merge |
| `git branch -d feature/xyz` | Delete merged local branch |
| `git remote add upstream <url>` | Add upstream for forks |
| `git fetch upstream` | Get latest from original repo |
| `git merge upstream/main` | Merge upstream changes |

---

Prev: [Git Push, Pull, Fetch](./10-git-push-pull-fetch.md) | Next: [Pull Requests](./12-pull-requests.md)

---
