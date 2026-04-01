# Git Tags

## 🧠 What is it?

A **Git tag** is a permanent label you attach to a specific commit — like a bookmark on an important page in your project's history.

Tags are most commonly used to mark **release versions** like `v1.0.0`, `v2.3.1`, etc.

Unlike branches, tags **don't move** — they always point to the same commit.

| | Branch | Tag |
|---|--------|-----|
| **Moves?** | Yes | No |
| **Purpose** | Active development | Mark a release/milestone |
| **Example** | `feature/login` | `v1.0.0` |

## ❓ Why do we use it?

- **Version releases** — Mark versions like `v1.0.0`, `v2.0.0`
- **Milestones** — Mark important points in project history
- **Deployment** — CI/CD can trigger deploys based on tags
- **Reference** — Easily refer to a specific project state
- **Package publishing** — npm/PyPI use tags for versions

## ⚙️ How does it work?

### Two Types of Tags:

#### 1. Lightweight Tags (Simple bookmark)
```bash
git tag v1.0.0
git tag v1.0.0 abc1234   # Tag a specific commit
```

#### 2. Annotated Tags (Recommended — has metadata)
```bash
git tag -a v1.0.0 -m "First stable release"
git tag -a v1.0.0 abc1234 -m "First stable release"
```

### View Tags:
```bash
git tag                    # List all tags
git tag -l "v1.*"          # List matching tags
git show v1.0.0            # Show tag details
```

### Push Tags to Remote:
```bash
git push origin v1.0.0     # Push specific tag
git push origin --tags      # Push ALL tags
git push --follow-tags      # Push commits + annotated tags
```

### Delete Tags:
```bash
git tag -d v1.0.0                    # Delete local
git push origin --delete v1.0.0      # Delete remote
```

### Checkout a Tag:
```bash
git checkout v1.0.0                       # Detached HEAD
git checkout -b hotfix/v1.0.1 v1.0.0      # Create branch from tag
```

### Semantic Versioning:
```
v MAJOR.MINOR.PATCH → v1.2.3
```
| Part | When to increment | Example |
|------|------------------|---------|
| **MAJOR** | Breaking changes | `v1.0.0` → `v2.0.0` |
| **MINOR** | New features (backward compatible) | `v1.0.0` → `v1.1.0` |
| **PATCH** | Bug fixes | `v1.0.0` → `v1.0.1` |

## 💥 Impact / When to use it?

- ✅ Clear version history
- ✅ Easy rollback to specific versions
- ✅ CI/CD deployment triggers
- ❌ Without tags: no clear release identification

## ⚠️ Common Mistakes

1. **Forgetting to push tags** — `git push` doesn't push tags! Use `--tags`.
2. **Using lightweight tags for releases** — Always use annotated (`-a`).
3. **Inconsistent naming** — Stick to `v1.0.0` format.
4. **Tagging before testing** — Test first, then tag!

## 💡 Pro Tips

- 🔥 Use `git push --follow-tags` to push commits and tags together
- 🔥 Make it default: `git config --global push.followTags true`
- 🔥 Use annotated for releases, lightweight for personal bookmarks

## 🎤 Interview Questions & Answers

**Q1: What are Git tags?**
> Tags are references pointing to specific commits, used to mark releases or milestones. Unlike branches, they don't move.

**Q2: Lightweight vs annotated tags?**
> Lightweight is just a name. Annotated (`-a`) stores tagger info, date, message, and can be signed. Use annotated for releases.

**Q3: How to push tags?**
> `git push origin <tag>` for one tag, `git push origin --tags` for all, or `git push --follow-tags` for annotated only.

**Q4: What is semantic versioning?**
> MAJOR.MINOR.PATCH — MAJOR for breaking changes, MINOR for features, PATCH for bug fixes.

## 📌 Commands Summary

| Command | Description |
|---------|-------------|
| `git tag` | List all tags |
| `git tag -a v1.0.0 -m "msg"` | Create annotated tag |
| `git push origin v1.0.0` | Push specific tag |
| `git push origin --tags` | Push all tags |
| `git tag -d v1.0.0` | Delete local tag |
| `git push origin --delete v1.0.0` | Delete remote tag |
| `git checkout v1.0.0` | Checkout a tag |

---

Prev: [.gitignore](./15-gitignore.md) | Next: [Git Best Practices](./17-git-best-practices.md)

---
