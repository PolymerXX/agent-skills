---
name: changelog-generator
description: Automatically generate and update CHANGELOG.md from git commit history. Use when users ask to create a changelog, update release notes, generate version history, or document recent changes. Triggers on requests like "generate changelog", "update release notes", "what changed since last release", or "create version history".
---

# Changelog Generator

Generate professional changelogs from git commit history following the Keep a Changelog format.

## Workflow

1. Analyze git history to identify commits since last tag/release
2. Categorize commits by type (Added, Changed, Fixed, etc.)
3. Generate formatted changelog entries
4. Update or create CHANGELOG.md

## Quick Start

Generate changelog for the current project:

```bash
# Get commits since last tag
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "")..HEAD --oneline

# Or get all commits if no tags exist
git log --oneline
```

## Commit Categories

Map commit prefixes to changelog sections:

| Prefix | Category | Description |
|--------|----------|-------------|
| `feat:` | Added | New features |
| `fix:` | Fixed | Bug fixes |
| `docs:` | Changed | Documentation updates |
| `refactor:` | Changed | Code refactoring |
| `perf:` | Changed | Performance improvements |
| `breaking:` | Removed/Changed | Breaking changes |
| `deps:` | Security | Dependency updates |

## Output Format

Follow Keep a Changelog format:

```markdown
# Changelog

## [Unreleased]

### Added
- New feature description

### Changed
- Change description

### Fixed
- Bug fix description

## [1.0.0] - 2024-01-15

### Added
- Initial release features
```

## Usage Patterns

**Full changelog generation:**
1. Run `scripts/generate_changelog.py` to parse git history
2. Review and edit the generated output
3. Update CHANGELOG.md

**Incremental update:**
1. Get commits since last version tag
2. Categorize new commits
3. Prepend to existing changelog

## Scripts

- `scripts/generate_changelog.py` - Parse git commits and generate changelog entries
