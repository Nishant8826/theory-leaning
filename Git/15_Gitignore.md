# .gitignore

## 🧠 What is it?

**.gitignore** is a special file that tells Git which files and folders to **ignore** — meaning Git won't track them, won't add them to staging, and won't include them in commits.

Think of it as a **"Do Not Enter"** list for Git:
- Files on this list are invisible to Git
- They exist in your project folder but Git pretends they don't exist

Common things you want to ignore:
- `node_modules/` — Dependency folders (thousands of files!)
- `.env` — Environment variables with secrets and API keys
- `dist/` or `build/` — Compiled/generated output
- `.DS_Store` (Mac) or `Thumbs.db` (Windows) — OS-generated junk files
- Log files, temporary files, IDE settings

In simple words:
> **.gitignore** tells Git: "Don't track these files, even if they're in my project folder."

## ❓ Why do we use it?

- **Security** — Keep passwords, API keys, and secrets out of your repo. If you push `.env` to a public repo, hackers can steal your credentials!
- **Clean repos** — `node_modules/` has 100,000+ files. Nobody wants that in their repo.
- **Smaller repos** — Ignoring generated files keeps the repo small and fast to clone.
- **Avoid conflicts** — OS-specific files (`.DS_Store`) and IDE settings (`.vscode/`) are different for each developer and cause unnecessary conflicts.
- **Focus on source code** — Only track the files that matter — your actual code and configuration.

### What happens if you DON'T use `.gitignore`:
- ❌ `node_modules/` gets pushed — repo becomes massive (100MB+)
- ❌ `.env` gets pushed — your secrets are exposed to the world
- ❌ IDE settings get pushed — everyone's VS Code config conflicts
- ❌ Build files get pushed — unnecessary clutter
- ❌ OS files get pushed — annoying junk files in the repo

## ⚙️ How does it work?

### Creating a `.gitignore` File:

Create a file named `.gitignore` in the **root** of your project (the same folder as `.git`):

```bash
# Create the file
touch .gitignore

# Or create with content
echo "node_modules/" > .gitignore
```

### Basic Syntax:

```gitignore
# This is a comment

# Ignore a specific file
secrets.txt

# Ignore a specific folder (and everything inside it)
node_modules/
dist/
build/

# Ignore all files with a specific extension
*.log
*.tmp
*.cache

# Ignore files in any directory with a specific name
**/debug.log

# Ignore all files in a specific folder
logs/*

# BUT keep a specific file (exception using !)
!logs/.gitkeep

# Ignore files only in the root directory (not subdirectories)
/config.local.js

# Ignore all .txt files in the doc/ directory
doc/*.txt

# Ignore all .pdf files in any subdirectory of doc/
doc/**/*.pdf
```

### Pattern Rules:

| Pattern | What it matches | Example |
|---------|----------------|---------|
| `file.txt` | File named `file.txt` anywhere | `file.txt`, `src/file.txt` |
| `*.log` | Any file ending with `.log` | `error.log`, `debug.log` |
| `folder/` | Entire folder and contents | `node_modules/`, `dist/` |
| `/file.txt` | Only `file.txt` in root directory | Root `file.txt` only |
| `**/logs` | `logs` folder anywhere in the project | `src/logs`, `app/logs` |
| `debug.log` | `debug.log` anywhere | Any `debug.log` |
| `!important.log` | DON'T ignore this file (exception) | Overrides previous rules |
| `*.py[cod]` | `.pyc`, `.pyo`, or `.pyd` files | All Python bytecode |

### Standard `.gitignore` for Common Projects:

#### Node.js / JavaScript Project:
```gitignore
# Dependencies
node_modules/
package-lock.json  # Some teams ignore this, some don't

# Environment files
.env
.env.local
.env.production

# Build output
dist/
build/
.next/
out/

# Log files
*.log
npm-debug.log*

# OS files
.DS_Store
Thumbs.db

# IDE settings
.vscode/
.idea/
*.swp
*.swo

# Testing
coverage/

# Miscellaneous
*.cache
.temp/
```

#### Python Project:
```gitignore
# Virtual environment
venv/
.venv/
env/

# Bytecode
__pycache__/
*.py[cod]
*.pyo

# Distribution
dist/
build/
*.egg-info/

# Environment
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

#### React / Next.js Project:
```gitignore
# Dependencies
node_modules/

# Production build
build/
dist/
.next/
out/

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Testing
coverage/

# OS
.DS_Store

# IDE
.vscode/settings.json
```

### What To Do If You Already Committed a File (Then Added It to `.gitignore`):

`.gitignore` only ignores **untracked** files. If you've already committed a file, adding it to `.gitignore` won't remove it from tracking.

```bash
# Step 1: Add the file/folder to .gitignore
echo "node_modules/" >> .gitignore

# Step 2: Remove it from Git tracking (but keep it on disk)
git rm -r --cached node_modules/

# Step 3: Commit the change
git add .gitignore
git commit -m "Remove node_modules from tracking, add to .gitignore"

# Step 4: Push
git push
```

> `--cached` means "remove from Git's tracking, but don't delete the actual files."

### Check If a File Is Ignored:

```bash
# Check if a specific file is ignored
git check-ignore -v filename.txt

# See all ignored files
git status --ignored
```

### Global `.gitignore` (System-wide):

For OS-specific files you ALWAYS want to ignore:

```bash
# Create a global gitignore
git config --global core.excludesFile ~/.gitignore_global
```

Add to `~/.gitignore_global`:
```gitignore
# macOS
.DS_Store
.AppleDouble
.LSOverride

# Windows
Thumbs.db
desktop.ini

# Linux
*~

# IDEs
.vscode/
.idea/
*.swp
```

## 💥 Impact / When to use it?

### When to use it:
- **Every single project** — There's no project that doesn't need a `.gitignore`.
- **At the very beginning** — Create it BEFORE your first commit.
- **When adding new tools/frameworks** — New tools often generate files to ignore.

### Benefits:
- ✅ Keeps secrets safe (`.env`)
- ✅ Keeps repo small and clean
- ✅ Avoids unnecessary merge conflicts
- ✅ Only tracks what matters

### What happens if you don't use it:
- ❌ Sensitive data exposed publicly
- ❌ Massive repo size (node_modules = 100MB+)
- ❌ Constant conflicts from OS/IDE files
- ❌ Cluttered, unprofessional repository

## ⚠️ Common Mistakes

1. **Creating `.gitignore` AFTER committing sensitive files** — The file is already in Git's history! You need to use `git rm --cached` AND consider the file compromised (rotate any exposed secrets).
2. **Forgetting to ignore `.env`** — This is the #1 security mistake. ALWAYS ignore `.env` files.
3. **Adding `node_modules/` to Git** — Never! It's huge and can be regenerated with `npm install`.
4. **Not using a trailing `/` for directories** — `node_modules` might match a file too. `node_modules/` specifically ignores the directory.
5. **Over-ignoring** — Don't ignore files others need (like `package.json`). Only ignore generated files, secrets, and OS/IDE junk.
6. **Thinking `.gitignore` removes already-tracked files** — It doesn't! Use `git rm --cached` first.

## 💡 Pro Tips

- 🔥 **Use gitignore.io** — Go to [gitignore.io](https://www.toptal.com/developers/gitignore) and generate a `.gitignore` for your tech stack. Just type "Node, React, macOS" and get a comprehensive file!

- 🔥 **Add `.gitignore` as your first commit**:
  ```bash
  git init
  # Create .gitignore first!
  git add .gitignore
  git commit -m "Add .gitignore"
  ```

- 🔥 **Use a global gitignore for OS files** — Don't force every project to ignore `.DS_Store`. Set it globally once.

- 🔥 **Keep an empty folder with `.gitkeep`** — Git doesn't track empty folders. To keep one:
  ```bash
  mkdir logs
  touch logs/.gitkeep
  ```
  Add to `.gitignore`:
  ```
  logs/*
  !logs/.gitkeep
  ```

- 🔥 **GitHub provides templates** — When creating a new repo on GitHub, select a `.gitignore` template for your language/framework.

## 🎤 Interview Questions & Answers

**Q1: What is `.gitignore` and why is it important?**
> `.gitignore` is a text file that specifies which files and directories Git should not track. It's important for keeping sensitive data (like API keys in `.env`), large generated files (like `node_modules/`), and OS-specific files out of the repository. It ensures the repo stays clean, secure, and manageable.

**Q2: What happens if you add a file to `.gitignore` that is already tracked by Git?**
> Adding a file to `.gitignore` won't stop Git from tracking it if it was previously committed. To stop tracking it, you need to remove it from Git's index using `git rm --cached <file>`, then commit the change. The file will remain on your local disk but Git will stop tracking future changes.

**Q3: What is the difference between a local and a global `.gitignore`?**
> A local `.gitignore` is placed in a repository and applies only to that project. It's committed and shared with all collaborators. A global `.gitignore` (configured via `git config --global core.excludesFile`) applies to ALL your Git repositories on your machine. It's personal and NOT shared. Global gitignore is ideal for OS-specific and IDE-specific files.

**Q4: How do you ignore all files of a certain type except one?**
> Use the negation pattern `!`. For example, to ignore all `.log` files except `important.log`:
> ```gitignore
> *.log
> !important.log
> ```
> The `!` pattern creates an exception to the previous ignore rule.

**Q5: How can you check if a file is being ignored by Git?**
> Use `git check-ignore -v <filename>` to check if a specific file is ignored and which rule in which `.gitignore` file is causing it. Use `git status --ignored` to see all currently ignored files.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `touch .gitignore` | Create a gitignore file |
| `git rm --cached <file>` | Stop tracking a file (keep it on disk) |
| `git rm -r --cached <folder>` | Stop tracking a folder |
| `git check-ignore -v <file>` | Check if/why a file is ignored |
| `git status --ignored` | Show all ignored files |
| `git config --global core.excludesFile <path>` | Set global gitignore |
| `git add -f <file>` | Force-add an ignored file |

---

Prev: [Git Stash](./14-git-stash.md) | Next: [Git Tags](./16-git-tags.md)

---
