# Commit Conventions

Small-step commit rules applied throughout execution:

| Rule | Detail |
|---|---|
| Commit frequency | One commit per step, after the step is validated and marked ✅ |
| Commit size | A single logical change — the step's objective only |
| Message format | Follow the repo's existing convention (check recent `git log`); default to `type(scope): summary` |
| Message content | Neutral description of the change. NEVER include AI-related words or hints: `AI`, `Copilot`, `assistant`, `agent`, `LLM`, `model`, `generated`, `automated`, or any reference to how the change was produced |
| Staging | Stage only the files belonging to this step (`git add <file>...`); never blind `git add -A` |
| Push gating | Never push to remote without explicit user confirmation (see **request-push-approval**) |
| Pre-commit check | Commit only after the step's validation checkpoint (tests/lint) passes |
