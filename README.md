# Agent Skills

My collection of custom Claude Code skills for AI-powered development workflows.

## Skills

| Skill | Description |
|-------|-------------|
| [changelog-generator](./changelog-generator) | Auto-generate CHANGELOG.md from git commit history |
| [github-push](./github-push) | Automated git workflow with branch management and PR creation |
| [langgraph-agent-generator](./langgraph-agent-generator) | Generate LangGraph agent boilerplate code |

## Usage

These skills are designed to work with [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Each skill contains:

- `SKILL.md` - Skill definition and instructions
- `scripts/` - Executable Python scripts (optional)
- `references/` - Reference documentation (optional)
- `assets/` - Templates and resources (optional)

## Skills Overview

### changelog-generator

Automatically generate and update CHANGELOG.md from git commit history following the Keep a Changelog format.

```bash
python changelog-generator/scripts/generate_changelog.py --version 1.0.0
```

### github-push

Complete git workflow automation: commit, push, branch management, and PR creation.

```bash
# Quick push
python github-push/scripts/git_push.py

# Push with custom message
python github-push/scripts/git_push.py -m "Add new feature"

# Create branch and PR
python github-push/scripts/git_push.py -b feature/xxx --pr
```

### langgraph-agent-generator

Generate production-ready LangGraph agent code with multiple patterns:

- **ReAct Agent** - Single agent with tool calling
- **Multi-Agent** - Supervisor pattern with specialized agents
- **Workflow Agent** - Complex branching logic with retry mechanisms

Templates are located in `langgraph-agent-generator/assets/`.

## License

MIT
