# Introduction to Git

## 🧠 What is it?

Git is a **Version Control System (VCS)** — a tool that keeps track of every change you make to your code over time.

Think of it like a **save game system** in a video game. Every time you "save" (commit), Git remembers the exact state of your project. You can go back to any previous save whenever you want.

- Git was created by **Linus Torvalds** in 2005 (yes, the same person who created Linux).
- It is **free** and **open-source**.
- It works **locally on your computer** — you don't need the internet to use Git.

In simple words:
> **Git = A tool that tracks changes in your code, lets you go back in time, and helps teams work together without messing up each other's code.**

## ❓ Why do we use it?

Imagine you're building a website. You make a change and suddenly everything breaks. Without Git, you'd have no easy way to go back to the working version.

Here's why Git is essential:

- **Track Changes** — Know exactly what changed, when, and who changed it.
- **Undo Mistakes** — Made a bad change? Go back to a previous version instantly.
- **Collaboration** — Multiple developers can work on the same project without overwriting each other's work.
- **Backup** — Your entire project history is saved. Nothing is truly lost.
- **Branching** — Try out new features safely without affecting the main code.

**Real-world example:**
You're working in a team of 5 developers. Everyone is writing code for different features. Without Git, you'd be emailing ZIP files to each other and manually merging code. With Git, everyone works on their own branch and merges seamlessly.

## ⚙️ How does it work?

Git works by taking **snapshots** of your project at different points in time.

### Key Concepts:

1. **Repository (Repo)** — A folder that Git is tracking. It contains your project files + a hidden `.git` folder where Git stores all the history.

2. **Commit** — A "snapshot" or "save point" of your project at a specific moment. Each commit has:
   - A unique ID (hash)
   - A message describing what changed
   - A timestamp
   - Author info

3. **Three Stages of Git:**

```
Working Directory  →  Staging Area  →  Repository
(your files)        (ready to save)   (saved/committed)
```

| Stage | What it means |
|-------|--------------|
| **Working Directory** | Where you edit your files (your normal folder) |
| **Staging Area** | A "preparation zone" — you pick which changes to include in the next commit |
| **Repository** | The actual saved history (inside the `.git` folder) |

### Basic Flow:

```bash
# Step 1: Initialize a Git repository
git init

# Step 2: Make changes to your files (edit code, create files, etc.)

# Step 3: Add changes to staging area
git add .

# Step 4: Save (commit) the changes
git commit -m "Initial commit"
```

### Visual Flow:

```
You edit a file → git add (stage it) → git commit (save it permanently)
```

## 💥 Impact / When to use it?

### When to use Git:
- **Every software project** — whether solo or team-based
- **Learning to code** — tracking your progress and experiments
- **Writing documentation** — yes, even for non-code files!
- **Any project where you want version history**

### Benefits:
- ✅ Complete history of every change
- ✅ Safe experimentation with branches
- ✅ Easy collaboration with team members
- ✅ Industry standard — every company uses it
- ✅ Free and works offline

### What happens if you DON'T use Git:
- ❌ You lose track of what changed and when
- ❌ Can't easily undo mistakes
- ❌ Collaborating becomes a nightmare (overwriting each other's code)
- ❌ No backup of your code history
- ❌ You'll suffer in interviews (Git is a MUST-KNOW skill)

## ⚠️ Common Mistakes

1. **Not using Git at all** — Many beginners code without any version control. Start using Git from Day 1!
2. **Confusing Git with GitHub** — Git is the tool. GitHub is a website that hosts Git repositories online. They are different things.
3. **Not committing often enough** — Make small, frequent commits. Don't wait until the whole feature is done.
4. **Writing bad commit messages** — "fix" or "update" tells nothing. Write meaningful messages like "fix login button not responding on mobile".
5. **Committing sensitive data** — Never commit passwords, API keys, or secrets. Use `.gitignore` to exclude them.

## 💡 Pro Tips

- 🔥 **Commit early, commit often** — Small commits are easier to understand and debug.
- 🔥 **Learn Git from the command line first** — GUIs are nice, but the terminal gives you full control and understanding.
- 🔥 **Use meaningful commit messages** — Future you (and your team) will thank you.
- 🔥 **Every project = a Git repo** — Even practice projects. Build the habit.
- 🔥 **Don't fear the terminal** — Git commands look scary at first, but you'll only use about 10-15 commands regularly.

## 🎤 Interview Questions & Answers

**Q1: What is Git?**
> Git is a distributed version control system that tracks changes in source code during software development. It allows multiple developers to work together, maintains a complete history of changes, and lets you revert to previous versions when needed.

**Q2: What is the difference between Git and other version control systems?**
> Git is a **distributed** VCS, meaning every developer has a full copy of the entire repository history on their local machine. Older systems like SVN are **centralized** — they depend on a single central server. Git is faster, works offline, and is more reliable.

**Q3: What are the three stages/areas in Git?**
> The three stages are:
> 1. **Working Directory** — where you modify files
> 2. **Staging Area (Index)** — where you prepare changes for the next commit
> 3. **Repository** — where committed snapshots are permanently stored

**Q4: Who created Git and why?**
> Linus Torvalds created Git in 2005 for managing the development of the Linux kernel. The previous tool they used (BitKeeper) revoked its free license, so Torvalds built Git — making it fast, distributed, and open-source.

**Q5: Is Git only for code?**
> No! Git can track changes in any text-based file — documentation, configuration files, notes, etc. However, it's not ideal for large binary files like videos or images (there are tools like Git LFS for that).

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git init` | Initialize a new Git repository |
| `git status` | Check the current state of your files |
| `git add <file>` | Add a file to the staging area |
| `git add .` | Add all changed files to staging |
| `git commit -m "message"` | Save staged changes with a message |
| `git log` | View commit history |
| `git --version` | Check installed Git version |

---

Prev: — | Next: [Git vs GitHub](./02-git-vs-github.md)

---
