# Platform-Agnostic Writing

Skills should be portable across AI platforms. Avoid platform-specific references:

- **No platform-specific tool names**: Replace tool names like `vscode_askQuestions` or `run_in_terminal` with generic action descriptions — e.g., "ask the user for confirmation" or "run the command"
- **No concrete context paths**: Describe persistent context targets by their type (personal persistent notes, project-level persistent notes, session-scoped context)
  rather than by concrete file paths like `/memories/` or `/memories/repo/`
- **Detect, don't assume**: When a capability needs to interact with platform features (context stores, tools, file structures), first detect what the platform supports, then map accordingly

Severity:
- 🟡 Minor — A single platform-specific reference that doesn't break the skill
- 🔴 Major — Multiple platform-specific references that would prevent the skill from working on another platform
