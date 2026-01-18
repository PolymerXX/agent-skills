#!/usr/bin/env python3
"""
Generate changelog from git commit history.
Usage: python generate_changelog.py [--since TAG] [--version VERSION]
"""

import subprocess
import re
import sys
from datetime import datetime
from collections import defaultdict

# Commit type to changelog category mapping
CATEGORY_MAP = {
    'feat': 'Added',
    'feature': 'Added',
    'add': 'Added',
    'fix': 'Fixed',
    'bugfix': 'Fixed',
    'docs': 'Changed',
    'doc': 'Changed',
    'refactor': 'Changed',
    'perf': 'Changed',
    'performance': 'Changed',
    'breaking': 'Changed',
    'remove': 'Removed',
    'deprecated': 'Deprecated',
    'security': 'Security',
    'deps': 'Security',
}

CATEGORY_ORDER = ['Added', 'Changed', 'Deprecated', 'Removed', 'Fixed', 'Security']


def get_commits(since_tag=None):
    """Get git commits, optionally since a specific tag."""
    if since_tag:
        cmd = ['git', 'log', f'{since_tag}..HEAD', '--pretty=format:%H|%s|%an|%ai']
    else:
        cmd = ['git', 'log', '--pretty=format:%H|%s|%an|%ai']

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return []

    commits = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split('|', 3)
            if len(parts) == 4:
                commits.append({
                    'hash': parts[0][:8],
                    'message': parts[1],
                    'author': parts[2],
                    'date': parts[3][:10]
                })
    return commits


def categorize_commit(message):
    """Categorize a commit message by its prefix."""
    # Match conventional commit format: type(scope): message or type: message
    match = re.match(r'^(\w+)(?:\([^)]+\))?:\s*(.+)$', message, re.IGNORECASE)
    if match:
        commit_type = match.group(1).lower()
        description = match.group(2)
        category = CATEGORY_MAP.get(commit_type, 'Changed')
        return category, description

    # No prefix found, categorize as Changed
    return 'Changed', message


def generate_changelog(commits, version='Unreleased'):
    """Generate changelog markdown from commits."""
    categorized = defaultdict(list)

    for commit in commits:
        category, description = categorize_commit(commit['message'])
        categorized[category].append(description)

    lines = []
    date_str = datetime.now().strftime('%Y-%m-%d') if version != 'Unreleased' else ''
    header = f"## [{version}]" + (f" - {date_str}" if date_str else "")
    lines.append(header)
    lines.append("")

    for category in CATEGORY_ORDER:
        if category in categorized:
            lines.append(f"### {category}")
            for desc in categorized[category]:
                lines.append(f"- {desc}")
            lines.append("")

    return '\n'.join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate changelog from git commits')
    parser.add_argument('--since', help='Generate changelog since this tag')
    parser.add_argument('--version', default='Unreleased', help='Version number for this release')
    args = parser.parse_args()

    commits = get_commits(args.since)
    if not commits:
        print("No commits found.", file=sys.stderr)
        return

    changelog = generate_changelog(commits, args.version)
    print(changelog)


if __name__ == '__main__':
    main()
