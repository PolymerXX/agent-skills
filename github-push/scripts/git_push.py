#!/usr/bin/env python3
"""
Automated Git push workflow with branch management and PR creation.

Usage:
    python git_push.py                     # Quick push with auto message
    python git_push.py -m "message"        # Push with custom message
    python git_push.py -b feature/xxx      # Create branch and push
    python git_push.py --pr                # Push and create PR
    python git_push.py --pr --title "xxx"  # Push and create PR with title
"""

import subprocess
import sys
import argparse
import re
from typing import Optional, Tuple


def run_cmd(cmd: str, check: bool = True) -> Tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def get_git_status() -> dict:
    """Get current git status."""
    status = {
        "has_changes": False,
        "staged": [],
        "unstaged": [],
        "untracked": [],
        "branch": "",
        "remote": ""
    }

    # Get current branch
    _, branch, _ = run_cmd("git branch --show-current", check=False)
    status["branch"] = branch

    # Get remote
    _, remote, _ = run_cmd("git remote", check=False)
    status["remote"] = remote.split("\n")[0] if remote else "origin"

    # Get status
    _, output, _ = run_cmd("git status --porcelain", check=False)
    if output:
        status["has_changes"] = True
        for line in output.split("\n"):
            if line.startswith("??"):
                status["untracked"].append(line[3:])
            elif line[0] != " ":
                status["staged"].append(line[3:])
            else:
                status["unstaged"].append(line[3:])

    return status


def generate_commit_message(status: dict) -> str:
    """Generate a commit message based on changes."""
    _, diff_stat, _ = run_cmd("git diff --cached --stat", check=False)

    # Count file changes
    files_changed = len(status["staged"]) + len(status["unstaged"]) + len(status["untracked"])

    # Detect change type based on files
    all_files = status["staged"] + status["unstaged"] + status["untracked"]

    if any("test" in f.lower() for f in all_files):
        prefix = "Test:"
    elif any(f.endswith((".md", ".txt", ".rst")) for f in all_files):
        prefix = "Docs:"
    elif any("fix" in f.lower() for f in all_files):
        prefix = "Fix:"
    elif files_changed == 1:
        prefix = "Update:"
    else:
        prefix = "Update:"

    # Generate description
    if files_changed == 1:
        desc = all_files[0]
    elif files_changed <= 3:
        desc = ", ".join(all_files[:3])
    else:
        desc = f"{files_changed} files"

    return f"{prefix} {desc}"


def check_sensitive_files() -> list:
    """Check for potentially sensitive files."""
    _, output, _ = run_cmd("git diff --cached --name-only", check=False)
    sensitive_patterns = [r"\.env", r"\.pem", r"\.key", r"password", r"secret", r"credential"]

    warnings = []
    for file in output.split("\n"):
        for pattern in sensitive_patterns:
            if re.search(pattern, file, re.IGNORECASE):
                warnings.append(file)
                break

    return warnings


def create_branch(branch_name: str) -> bool:
    """Create and switch to a new branch."""
    code, _, _ = run_cmd(f"git checkout -b {branch_name}")
    return code == 0


def push_changes(remote: str, branch: str, set_upstream: bool = False) -> bool:
    """Push changes to remote."""
    upstream = "-u " if set_upstream else ""
    code, _, _ = run_cmd(f"git push {upstream}{remote} {branch}")
    return code == 0


def create_pr(title: Optional[str] = None, body: Optional[str] = None) -> bool:
    """Create a pull request using GitHub CLI."""
    # Check if gh is installed
    code, _, _ = run_cmd("gh --version", check=False)
    if code != 0:
        print("Error: GitHub CLI (gh) is not installed", file=sys.stderr)
        return False

    cmd = "gh pr create"
    if title:
        cmd += f' --title "{title}"'
    if body:
        cmd += f' --body "{body}"'
    if not title and not body:
        cmd += " --fill"

    code, output, _ = run_cmd(cmd)
    if code == 0:
        print(f"PR created: {output}")
    return code == 0


def main():
    parser = argparse.ArgumentParser(description="Automated Git push workflow")
    parser.add_argument("-m", "--message", help="Commit message")
    parser.add_argument("-b", "--branch", help="Create and push to new branch")
    parser.add_argument("--pr", action="store_true", help="Create pull request after push")
    parser.add_argument("--title", help="PR title (requires --pr)")
    parser.add_argument("--body", help="PR body (requires --pr)")
    parser.add_argument("--force", action="store_true", help="Skip safety checks")
    args = parser.parse_args()

    print("🔍 Checking git status...")
    status = get_git_status()

    if not status["has_changes"]:
        print("✅ Nothing to push - working tree is clean")
        return 0

    print(f"📁 Branch: {status['branch']}")
    print(f"📝 Changes: {len(status['staged'])} staged, {len(status['unstaged'])} unstaged, {len(status['untracked'])} untracked")

    # Safety check
    if not args.force:
        warnings = check_sensitive_files()
        if warnings:
            print(f"⚠️  Warning: Potentially sensitive files detected:")
            for w in warnings:
                print(f"   - {w}")
            response = input("Continue anyway? [y/N]: ")
            if response.lower() != "y":
                print("Aborted.")
                return 1

    # Create branch if specified
    if args.branch:
        print(f"🌿 Creating branch: {args.branch}")
        if not create_branch(args.branch):
            return 1
        status["branch"] = args.branch

    # Stage all changes
    print("📦 Staging changes...")
    run_cmd("git add -A")

    # Generate or use provided commit message
    message = args.message or generate_commit_message(status)
    print(f"💬 Commit message: {message}")

    # Commit
    print("✍️  Committing...")
    code, _, _ = run_cmd(f'git commit -m "{message}"')
    if code != 0:
        return 1

    # Push
    print(f"🚀 Pushing to {status['remote']}/{status['branch']}...")
    set_upstream = args.branch is not None
    if not push_changes(status["remote"], status["branch"], set_upstream):
        return 1

    print("✅ Push successful!")

    # Create PR if requested
    if args.pr:
        print("📋 Creating pull request...")
        if not create_pr(args.title, args.body):
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
