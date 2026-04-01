# Installation & Setup

## 🧠 What is it?

Before you can use Git, you need to **install** it on your computer and **configure** it with your details (name and email). This is a one-time setup.

- **Installation** = Downloading and installing the Git software
- **Setup/Configuration** = Telling Git who you are (your name and email), so every commit is tagged with your identity

Think of it like setting up a new phone — you install it once, sign in with your account, and then you're good to go.

## ❓ Why do we use it?

- **Installation** — Without installing Git, you can't use any Git commands. It's the foundation.
- **Configuration** — Git attaches your name and email to every commit. This is important because:
  - In a team, everyone needs to know **who made which change**
  - GitHub uses your email to link commits to your profile
  - It's required — Git won't let you commit without a configured identity

## ⚙️ How does it work?

### Step 1: Install Git

#### On Windows:
1. Go to [https://git-scm.com/downloads](https://git-scm.com/downloads)
2. Download the Windows installer
3. Run the installer — use the **default settings** (just click Next, Next, Next...)
4. After installation, open **Command Prompt** or **Git Bash** and verify:

```bash
git --version
# Output: git version 2.xx.x
```

#### On Mac:
```bash
# Option 1: Using Homebrew (recommended)
brew install git

# Option 2: Install Xcode Command Line Tools
xcode-select --install

# Verify installation
git --version
```

#### On Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install git

# Verify installation
git --version
```

### Step 2: Configure Git (One-time Setup)

After installation, tell Git who you are:

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use the same email as your GitHub account)
git config --global user.email "your.email@example.com"
```

### Step 3: Verify Your Configuration

```bash
# See all your Git configuration
git config --list

# Check specific settings
git config user.name
git config user.email
```

### Step 4: Set Default Branch Name (Optional but Recommended)

```bash
# Set default branch to 'main' instead of 'master'
git config --global init.defaultBranch main
```

### Step 5: Set Default Text Editor (Optional)

```bash
# Set VS Code as default editor
git config --global core.editor "code --wait"

# Set Notepad++ as default editor (Windows)
git config --global core.editor "'C:/Program Files/Notepad++/notepad++.exe' -multiInst -notabbar -nosession"

# Set nano as default editor (Linux/Mac)
git config --global core.editor "nano"
```

### Understanding Config Levels:

| Level | Flag | Where it applies | Config file location |
|-------|------|-----------------|---------------------|
| **System** | `--system` | All users on computer | `/etc/gitconfig` |
| **Global** | `--global` | Your user account (all repos) | `~/.gitconfig` |
| **Local** | `--local` | Current repository only | `.git/config` |

Priority: **Local > Global > System** (local settings override global ones)

## 💥 Impact / When to use it?

### When to use it:
- **Installation** — Once, when you first set up your computer for development
- **Global config** — Once, after installing Git
- **Local config** — When you want different settings for a specific project (e.g., work email vs personal email)

### Benefits:
- ✅ Every commit is properly attributed to you
- ✅ GitHub can link your commits to your profile
- ✅ Team members can see who made each change
- ✅ You can have different identities for different projects

### What happens if you don't configure Git:
- ❌ Git will refuse to let you commit (it needs your name and email)
- ❌ Your commits won't be linked to your GitHub profile
- ❌ In a team, nobody will know who made which changes

## ⚠️ Common Mistakes

1. **Forgetting to configure name and email** — Git won't work without this. Do it right after installation.
2. **Using a different email than GitHub** — If your Git email doesn't match your GitHub email, your commits won't show on your GitHub profile (no green squares!).
3. **Not verifying installation** — Always run `git --version` after installing to make sure it worked.
4. **Skipping `--global` flag** — Without `--global`, the config only applies to the current repository, not all future repos.
5. **Installing an old version** — Always download from the official site to get the latest stable version.

## 💡 Pro Tips

- 🔥 **Use Git Bash on Windows** — It gives you a Unix-like terminal with better Git integration than Command Prompt.
- 🔥 **Match your Git email with GitHub** — This ensures your commits show up on your GitHub contribution graph.
- 🔥 **Use `--global` for general setup** — and `--local` for project-specific overrides (e.g., work vs. personal projects).
- 🔥 **Set up SSH keys** — Instead of typing your GitHub password every time, set up SSH for secure, passwordless access:
  ```bash
  ssh-keygen -t ed25519 -C "your.email@example.com"
  ```
- 🔥 **Create Git aliases** for commands you use often:
  ```bash
  git config --global alias.st status
  git config --global alias.co checkout
  git config --global alias.br branch
  git config --global alias.cm "commit -m"
  ```
  Now you can type `git st` instead of `git status`!

## 🎤 Interview Questions & Answers

**Q1: How do you install Git and verify the installation?**
> Download Git from git-scm.com (for Windows) or use a package manager like `brew` (Mac) or `apt` (Linux). After installation, verify by running `git --version` in the terminal, which should display the installed version number.

**Q2: What is the purpose of `git config`?**
> `git config` is used to set configuration values for Git. The most important settings are `user.name` and `user.email`, which identify you as the author of commits. It has three levels: `--system` (all users), `--global` (your account), and `--local` (current repo only).

**Q3: What is the difference between `--global` and `--local` configuration?**
> `--global` configuration applies to all Git repositories on your user account. `--local` configuration applies only to the current repository. Local settings override global ones. This is useful when you want a different email for work projects vs. personal projects.

**Q4: How can you see all your Git configuration settings?**
> Run `git config --list` to see all settings. You can also check specific values like `git config user.name` or `git config user.email`. To see where each setting comes from, use `git config --list --show-origin`.

**Q5: Why should your Git email match your GitHub email?**
> GitHub uses the email in your commits to link them to your GitHub account. If the emails don't match, your commits won't appear on your GitHub contribution graph (the green squares), and they won't be associated with your profile.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git --version` | Check installed Git version |
| `git config --global user.name "Name"` | Set your name globally |
| `git config --global user.email "email"` | Set your email globally |
| `git config --list` | View all configuration settings |
| `git config user.name` | Check your configured name |
| `git config --global init.defaultBranch main` | Set default branch name |
| `git config --global core.editor "code --wait"` | Set default text editor |
| `git config --global alias.st status` | Create a command shortcut |
| `ssh-keygen -t ed25519 -C "email"` | Generate SSH key for GitHub |

---

Prev: [Git vs GitHub](./02-git-vs-github.md) | Next: [Git Init, Add, Commit](./04-git-init-add-commit.md)

---
