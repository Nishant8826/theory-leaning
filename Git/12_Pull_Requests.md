# Pull Requests

## 🧠 What is it?

A **Pull Request (PR)** is a way to propose changes to a codebase and ask your team to **review** and **approve** them before merging.

Think of it like submitting an assignment:
- You write your code (the assignment)
- You submit it (open a PR)
- The teacher reviews it (code review)
- They either approve it (merge) or ask you to fix things (request changes)

It's called a "Pull Request" because you're **requesting** that the project maintainer **pulls** your changes into the main branch.

> PRs are the **cornerstone of team collaboration** on GitHub. Every professional team uses them.

## ❓ Why do we use it?

- **Code Quality** — Every change is reviewed by at least one other person before merging
- **Bug Prevention** — Reviewers catch bugs that the author missed
- **Knowledge Sharing** — Team members learn about different parts of the codebase
- **Documentation** — PRs serve as a record of what was changed and why
- **Discussion** — Team can discuss implementation approaches in the PR comments
- **Safety** — Prevents broken code from reaching `main`

Without Pull Requests:
- ❌ Untested code goes directly into production
- ❌ No one reviews the code for bugs or bad practices
- ❌ Hard to track what changes were made and why
- ❌ New team members don't learn from experienced developers

## ⚙️ How does it work?

### Creating a Pull Request — Complete Workflow:

```bash
# Step 1: Make sure you're on the latest main
git checkout main
git pull origin main

# Step 2: Create a feature branch
git checkout -b feature/shopping-cart

# Step 3: Make changes and commit
git add .
git commit -m "Add shopping cart page with item list"
git add .
git commit -m "Add quantity selector and remove button"

# Step 4: Push the branch to GitHub
git push -u origin feature/shopping-cart
```

### Step 5: Open the PR on GitHub

1. Go to your repository on GitHub
2. Click the **"Pull requests"** tab
3. Click **"New pull request"**
4. Set:
   - **Base branch**: `main` (where you want to merge INTO)
   - **Compare branch**: `feature/shopping-cart` (your changes)
5. Click **"Create pull request"**
6. Fill in the details:

```markdown
## 🎯 What does this PR do?
Adds a shopping cart page where users can view items, adjust quantity, and remove products.

## 📝 Changes Made
- Created `ShoppingCart` component with item display
- Added quantity selector with +/- buttons
- Added remove item functionality
- Added cart total calculation
- Added empty cart state with "Continue Shopping" link

## 📸 Screenshots
<!-- Add screenshots of the UI changes -->

## ✅ How to Test
1. Add items to cart from the product page
2. Go to /cart
3. Try adjusting quantity (should update total)
4. Try removing an item
5. Remove all items (should show empty state)

## 📋 Checklist
- [ ] Code follows project conventions
- [ ] Tests pass
- [ ] No console errors
- [ ] Responsive on mobile

## 🔗 Related
Closes #15
```

7. Add **reviewers** (people to review your code)
8. Add **labels** (e.g., `feature`, `bug`, `documentation`)
9. Click **"Create pull request"**

### Step 6: Code Review Process

#### As a Reviewer:

1. Go to the PR → Click **"Files changed"**
2. Review the code changes (green = added, red = removed)
3. Leave comments:
   - Click on a line number to comment on specific code
   - Use **"Start a review"** to batch comments
4. Submit your review:
   - **Approve** ✅ — Code looks good
   - **Request changes** ❌ — Issues need fixing
   - **Comment** 💬 — General feedback, no approval/rejection

#### Common Review Comments:

```
✅ "LGTM!" (Looks Good To Me)
✅ "Nice implementation, clean code!"

🔧 "Can you add error handling for the API call?"
🔧 "This variable name is unclear. How about `cartTotal` instead of `ct`?"
🔧 "Consider using optional chaining here: `user?.name`"

❓ "Why did you choose this approach over using context?"
❓ "Should we add a loading state here?"
```

#### As the PR Author (Addressing Feedback):

```bash
# Fix the issues locally
# ... edit files based on review feedback ...

git add .
git commit -m "Address review: add error handling and rename variables"
git push
# The PR updates automatically!
```

### Step 7: Merge the PR

Once approved, choose a merge strategy:

| Strategy | What it does | Best for |
|----------|-------------|----------|
| **Merge commit** | Creates a merge commit with all individual commits | Preserving full history |
| **Squash and merge** | Combines all commits into ONE commit | Clean main branch |
| **Rebase and merge** | Replays commits on top of main (linear) | Linear history lovers |

Most teams prefer **Squash and merge** for a clean `main` branch.

### Step 8: After Merging

```bash
# Update your local main
git checkout main
git pull origin main

# Delete the local branch
git branch -d feature/shopping-cart
```

On GitHub: Click "Delete branch" button on the merged PR.

### PR Features on GitHub:

| Feature | What it does |
|---------|-------------|
| **Draft PRs** | Marks PR as work-in-progress (not ready for review) |
| **Assignees** | Who is responsible for the PR |
| **Reviewers** | Who should review the code |
| **Labels** | Tags like `bug`, `feature`, `urgent` |
| **Milestones** | Link PR to a project milestone |
| **Linked Issues** | Auto-close issues when PR is merged |
| **CI/CD Status** | Shows if automated tests pass |

### Auto-Closing Issues:

Use these keywords in your PR description to auto-close issues:

```markdown
Closes #42
Fixes #42
Resolves #42
```

When the PR is merged, issue #42 will be automatically closed!

## 💥 Impact / When to use it?

### When to use Pull Requests:
- **Every code change in a team** — No exceptions!
- **Open-source contributions** — The standard way to contribute
- **Even for personal projects** — Good practice for building habits
- **Hotfixes** — Even urgent fixes should go through a quick review

### Benefits:
- ✅ Higher code quality through peer review
- ✅ Fewer bugs reach production
- ✅ Team learns from each other
- ✅ Clear documentation of changes
- ✅ Easy to revert specific changes
- ✅ CI/CD can run tests automatically on PRs

### What happens without PRs:
- ❌ Broken code reaches production
- ❌ Bugs go unnoticed
- ❌ No record of why changes were made
- ❌ Team members don't grow as developers

## ⚠️ Common Mistakes

1. **Creating huge PRs** — A PR with 1000+ lines is impossible to review properly. Split into smaller PRs (200-400 lines is ideal).
2. **Vague PR titles/descriptions** — "Update code" tells nothing. Write clear descriptions of what and why.
3. **Not responding to review comments** — Address every comment — either fix the issue or explain why you disagree.
4. **Merging without approval** — Don't merge your own PR. Wait for at least one approval.
5. **Not running tests before opening a PR** — Make sure your code works! Don't waste reviewers' time on broken code.
6. **Letting PRs sit too long** — Review PRs within 24 hours. Stale PRs lead to merge conflicts.
7. **Being defensive about feedback** — Code review is about improving code, not criticizing you personally.

## 💡 Pro Tips

- 🔥 **Review your own PR before requesting reviews** — Click "Files changed" and read through everything. You'll catch obvious issues.
- 🔥 **Use Draft PRs for work in progress** — Open a draft PR early so teammates can see your approach and give early feedback.
- 🔥 **Add a PR template** — Create `.github/pull_request_template.md`:
  ```markdown
  ## What does this PR do?
  
  ## Changes Made
  
  ## How to Test
  
  ## Screenshots (if applicable)
  
  ## Checklist
  - [ ] Tests pass
  - [ ] Code follows conventions
  - [ ] Documentation updated
  ```
- 🔥 **Use "Suggest changes" in reviews** — GitHub lets reviewers suggest specific code changes that the author can accept with one click.
- 🔥 **Keep the conversation positive** — Use phrases like "What do you think about..." instead of "This is wrong."
- 🔥 **Set up branch protection rules** — Require at least 1 approval before merging:
  ```
  Repo → Settings → Branches → Add rule
  → Require pull request reviews before merging
  ```

## 🎤 Interview Questions & Answers

**Q1: What is a Pull Request?**
> A Pull Request is a feature on GitHub that lets you propose changes from one branch to another (usually from a feature branch to `main`). It provides a platform for code review, discussion, and collaboration before changes are integrated. Reviewers can approve changes, request modifications, or leave comments on specific lines of code.

**Q2: How do you handle merge conflicts in a Pull Request?**
> When a PR has conflicts, you need to resolve them before merging. You can either: 1) Use GitHub's web editor for simple conflicts, 2) Pull the target branch into your feature branch locally, resolve conflicts, and push. The steps are: `git checkout feature-branch` → `git merge main` → resolve conflicts → `git add .` → `git commit` → `git push`.

**Q3: What is the difference between "Merge commit", "Squash and merge", and "Rebase and merge"?**
> **Merge commit** creates a merge commit preserving all individual commits and branch history. **Squash and merge** combines all the PR's commits into a single commit on the target branch, creating a cleaner history. **Rebase and merge** replays the PR's commits on top of the target branch, creating a linear history without a merge commit.

**Q4: What makes a good Pull Request?**
> A good PR is small and focused (one feature or fix), has a clear title and description explaining what and why, includes screenshots for UI changes, references related issues, has been self-reviewed before requesting reviews, passes all automated tests, and follows the project's contribution guidelines.

**Q5: Why shouldn't you merge your own Pull Request?**
> Merging your own PR defeats the purpose of code review. The goal is to have another pair of eyes check your work for bugs, code quality, and consistency. Having at least one other person review ensures better code quality, catches mistakes you might have missed, and promotes team collaboration and knowledge sharing.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git checkout -b feature/xyz` | Create a branch for your PR |
| `git push -u origin feature/xyz` | Push branch to open a PR |
| `git push` | Push updates to an open PR |
| `git checkout main && git pull` | Update local after PR merge |
| `git branch -d feature/xyz` | Delete branch after merge |
| `git merge main` | Update your PR branch with latest main |
| `git log --oneline` | Review commits before opening PR |

---

Prev: [GitHub Workflow](./11-github-workflow.md) | Next: [Rebasing](./13-rebasing.md)

---
