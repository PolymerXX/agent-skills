---
name: github-push
description: Automate Git workflow including commit, push, branch management, and PR creation. Use when users ask to push code, commit changes, create a pull request, sync with GitHub, or upload code to remote repository. Triggers on requests like "push to GitHub", "commit and push", "create PR", "sync my changes", or "upload to remote".
---

# GitHub Push

Automate complete Git workflow: commit, push, branch management, and PR creation.

## Quick Commands

| Task | Command |
|------|---------|
| Quick push | `scripts/git_push.py` |
| Push with message | `scripts/git_push.py -m "your message"` |
| Create PR | `scripts/git_push.py --pr` |
| New branch + push | `scripts/git_push.py -b feature/xxx` |

## Workflow Decision

```
User wants to push code
        │
        ▼
┌─────────────────┐
│ Check git status │
└────────┬────────┘
         │
    Has changes?
    ├── No → "Nothing to push"
    │
    ▼ Yes
┌─────────────────┐
│ Generate commit │
│    message      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Add & Commit    │
└────────┬────────┘
         │
    Need new branch?
    ├── Yes → Create branch
    │
    ▼ No
┌─────────────────┐
│ Push to remote  │
└────────┬────────┘
         │
    Create PR?
    ├── Yes → gh pr create
    │
    ▼ No
      Done!
```

## Task 1: Quick Push

Push all changes with auto-generated message:

```bash
# Check status first
git status

# Add all changes
git add -A

# Generate message based on changes
git diff --cached --stat

# Commit and push
git commit -m "Update: brief description of changes"
git push origin HEAD
```

## Task 2: Branch Workflow

Create feature branch and push:

```bash
# Create and switch to new branch
git checkout -b feature/your-feature

# Make changes, then push
git add -A
git commit -m "Add: new feature description"
git push -u origin feature/your-feature
```

## Task 3: Create Pull Request

Push and create PR using GitHub CLI:

```bash
# Ensure changes are pushed
git push origin HEAD

# Create PR
gh pr create --title "Brief title" --body "Description of changes"

# Or with auto-fill
gh pr create --fill
```

## Commit Message Guidelines

Generate concise commit messages:

| Change Type | Format | Example |
|-------------|--------|---------|
| New feature | `Add: description` | `Add: user login page` |
| Bug fix | `Fix: description` | `Fix: null pointer in parser` |
| Update | `Update: description` | `Update: dependencies` |
| Remove | `Remove: description` | `Remove: deprecated API` |
| Refactor | `Refactor: description` | `Refactor: database module` |

## Safety Checks

Before pushing, verify:

1. **No sensitive data**: Check for API keys, passwords, .env files
2. **Correct branch**: Confirm target branch
3. **Clean status**: No unintended files staged

```bash
# Check for sensitive files
git diff --cached --name-only | grep -E '\.(env|pem|key)$'

# Verify branch
git branch --show-current

# Review staged changes
git diff --cached --stat
```

## Scripts

- `scripts/git_push.py` - Automated push with options for branch and PR creation
