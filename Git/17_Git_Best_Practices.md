# Git Best Practices

## 🧠 What is it?

Git best practices are **proven rules and habits** that professional developers follow to keep their codebase clean, organized, and collaborative.

Think of it like kitchen hygiene rules:
- A professional kitchen has rules about cleanliness, labeling, and organization
- Without them, the kitchen becomes a mess and food quality drops
- Similarly, without Git best practices, your codebase becomes chaotic

These aren't strict laws — they're **guidelines** that the industry has agreed upon through years of experience.

## ❓ Why do we use it?

- **Prevent disasters** — Avoid losing code, breaking production, or exposing secrets
- **Better collaboration** — Everyone follows the same rules, reducing confusion
- **Clean history** — Easy to understand what happened and when
- **Faster debugging** — Good practices make it easy to find and fix bugs
- **Professional growth** — Companies expect developers to follow these practices

## ⚙️ How does it work?

### 1. 📝 Write Meaningful Commit Messages

```bash
# ❌ BAD
git commit -m "fix"
git commit -m "update"
git commit -m "stuff"
git commit -m "WIP"
git commit -m "asdfgh"

# ✅ GOOD
git commit -m "Fix login button not responding on mobile"
git commit -m "Add email validation to registration form"
git commit -m "Remove unused CSS classes from navbar"
git commit -m "Update README with deployment instructions"
```

**Formula:** `Action verb` + `What changed` + `Why (optional)`

**Conventional Commits format:**
```bash
feat: Add user profile page
fix: Resolve cart total calculation error
docs: Update API documentation
style: Format code with prettier
refactor: Simplify authentication logic
test: Add unit tests for payment module
chore: Update dependencies to latest versions
```

### 2. 🌿 Branch Strategy

**Never commit directly to `main`!**

```bash
# ✅ Always create a branch
git checkout main
git pull origin main
git checkout -b feature/user-dashboard

# Work, commit, push, then open a Pull Request
```

**Branch naming conventions:**
```
feature/description    → feature/user-auth
bugfix/description     → bugfix/cart-crash
hotfix/description     → hotfix/security-patch
docs/description       → docs/api-guide
refactor/description   → refactor/clean-utils
```

### 3. 🔄 Commit Often, Push Regularly

```bash
# ❌ BAD: One giant commit with everything
git commit -m "Built entire user module with auth, profile, settings"

# ✅ GOOD: Small, focused commits
git commit -m "Add user registration form"
git commit -m "Add form validation for email and password"
git commit -m "Add API integration for user creation"
git commit -m "Add success/error notifications"
```

**Rules:**
- Each commit = **one logical change**
- Commit every **30-60 minutes** of work
- Push at the end of each day at minimum

### 4. 🔒 Never Commit Secrets

```bash
# ❌ NEVER commit these:
.env
config/secrets.js
private-key.pem
database-password.txt

# ✅ Always use .gitignore
echo ".env" >> .gitignore
echo "*.pem" >> .gitignore
```

**If you accidentally committed a secret:**
1. **Rotate the secret immediately** — Change the password/API key
2. Remove it from tracking: `git rm --cached .env`
3. Add to `.gitignore`
4. Consider the old secret compromised forever

### 5. 📋 Pull Before Push

```bash
# ✅ Always pull before pushing
git pull origin main
# Then push
git push origin main

# Even better — make it a habit:
git pull --rebase && git push
```

### 6. 🔍 Review Before Committing

```bash
# Always check what you're about to commit
git status          # What files changed?
git diff            # What lines changed?
git diff --staged   # What's staged?

# Then commit
git add .
git commit -m "Your message"
```

### 7. 📄 Always Have a `.gitignore`

Create it BEFORE your first commit:
```gitignore
node_modules/
.env
dist/
build/
.DS_Store
Thumbs.db
*.log
.vscode/settings.json
```

### 8. 📖 Maintain a Good README

Every repo should have a `README.md` with:
- Project name and description
- How to install and run
- How to contribute
- Technologies used
- Screenshots (for UI projects)

### 9. 🏷️ Use Tags for Releases

```bash
git tag -a v1.0.0 -m "First production release"
git push origin v1.0.0
```

### 10. 🧹 Clean Up After Merging

```bash
# Delete merged branches
git branch -d feature/old-feature
git push origin --delete feature/old-feature

# Prune stale remote branches
git fetch --prune
```

### 11. 🔄 Keep PRs Small and Focused

| ❌ Bad PR | ✅ Good PR |
|-----------|-----------|
| 50+ files changed | 5-15 files changed |
| Multiple features | One feature/fix |
| Hours to review | 15-30 min to review |
| High chance of bugs | Easy to catch issues |

### 12. 🛡️ Protect the Main Branch

On GitHub:
```
Settings → Branches → Add rule → "main"
✅ Require pull request reviews
✅ Require status checks to pass
✅ Require linear history
❌ Allow force pushes (NEVER!)
```

## 💥 Impact / When to use it?

### When to use these practices:
- **Always** — From your first project to your last
- **In teams** — Essential for collaboration
- **Solo projects** — Build good habits early
- **Interviews** — Interviewers check your Git practices

### Benefits:
- ✅ Professional-looking repositories
- ✅ Fewer conflicts and bugs
- ✅ Easier debugging and rollbacks
- ✅ Better team collaboration
- ✅ Faster onboarding for new team members

### What happens without best practices:
- ❌ Messy, unreadable commit history
- ❌ Secrets exposed in public repos
- ❌ Constant merge conflicts
- ❌ Production breaks frequently
- ❌ Nobody understands what changed or why

## ⚠️ Common Mistakes

1. **"I'll clean up later"** — You won't. Write good commits from the start.
2. **Force pushing to shared branches** — This destroys teammates' work.
3. **Giant PRs** — Nobody can properly review 2000 lines. Split them up.
4. **Not using `.gitignore`** — Leads to exposed secrets and bloated repos.
5. **Committing generated files** — `node_modules/`, `dist/`, `build/` should be in `.gitignore`.
6. **Working directly on `main`** — Always use feature branches.
7. **Not pulling before pushing** — Leads to rejected pushes and more conflicts.
8. **Ignoring code reviews** — Reviews exist to improve quality, not slow you down.

## 💡 Pro Tips

- 🔥 **Set up Git hooks** — Automatically check code before commits:
  ```bash
  # Use husky for Node.js projects
  npx husky install
  npx husky add .husky/pre-commit "npm run lint"
  ```

- 🔥 **Use conventional commits** — Tools can auto-generate changelogs from them.

- 🔥 **Create Git aliases** for your workflow:
  ```bash
  git config --global alias.st status
  git config --global alias.co checkout
  git config --global alias.br branch
  git config --global alias.lg "log --oneline --graph --all --decorate"
  git config --global alias.undo "reset --soft HEAD~1"
  git config --global alias.save "stash push -m"
  ```

- 🔥 **Use `.gitkeep` for empty directories** — Git doesn't track empty folders.

- 🔥 **Squash before merging** — Use "Squash and merge" in PRs for a clean `main` history.

## 🎤 Interview Questions & Answers

**Q1: What are some Git best practices you follow?**
> I always use feature branches and never commit directly to main. I write descriptive commit messages using conventional commits format. I keep PRs small and focused. I use `.gitignore` to exclude secrets and generated files. I pull before pushing, review changes before committing, and protect the main branch with PR reviews.

**Q2: How do you write a good commit message?**
> A good commit message starts with an action verb, clearly describes what changed, and optionally explains why. It should be under 72 characters for the subject. I follow conventional commits: `feat:`, `fix:`, `docs:`, etc. Example: "feat: Add email validation to registration form".

**Q3: How do you handle sensitive data in Git?**
> I never commit secrets. I use `.gitignore` for `.env` files and sensitive configs. I use environment variables for secrets. If a secret is accidentally committed, I rotate it immediately and remove it from tracking with `git rm --cached`. I consider any committed secret as compromised.

**Q4: What branching strategy do you prefer?**
> I prefer GitHub Flow for most projects: create a branch from `main`, make changes, push, open a PR, get review, merge. For larger projects, Git Flow with `main`, `develop`, `feature/`, `release/`, and `hotfix/` branches works well. The key is: never commit directly to `main`.

**Q5: How do you keep a clean Git history?**
> I make small, focused commits with clear messages. I use interactive rebase to squash fixup commits before PRs. I use "Squash and merge" for PR merges. I use `git pull --rebase` to avoid unnecessary merge commits. I delete branches after merging.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git status` | Check before every action |
| `git diff` | Review changes before staging |
| `git diff --staged` | Review staged changes |
| `git add -p` | Stage changes selectively |
| `git commit -m "type: msg"` | Meaningful commit message |
| `git pull --rebase` | Clean pull without merge commits |
| `git push --force-with-lease` | Safe force push |
| `git branch -d <name>` | Delete merged branches |
| `git fetch --prune` | Clean stale remote branches |
| `git log --oneline --graph` | Visual commit history |
| `git stash push -m "msg"` | Save work temporarily |
| `git tag -a v1.0.0 -m "msg"` | Tag releases |

---

Prev: [Git Tags](./16-git-tags.md) | Next: —

---
