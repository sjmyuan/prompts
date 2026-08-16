# Platform-Agnostic Writing

Used by **create-skill-file** (all steps) and **validate-created-skill** (knowledge step 4).

Skills must be portable across AI platforms:
- **Avoid platform-specific tool names**: replace `vscode_askQuestions`/`run_in_terminal` with generic actions — "ask the user for confirmation" instead of "use `vscode_askQuestions`", "run the command" instead of "use `run_in_terminal`"
- **Use abstract context type descriptions**: describe persistent context by type (personal persistent notes, project-level persistent notes, session-scoped context) rather than concrete paths like `/memories/`. Detect what the platform supports, then map accordingly.
- **Detect, don't assume**: when a capability interacts with platform features (context stores, tools, file structures), first detect what the platform supports, then map to available mechanisms
