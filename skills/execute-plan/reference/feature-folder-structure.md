# Feature Folder Structure

Each feature implementation lives in its own folder with two files:

```
{location}/{repo}/{feature-name}/
├── plan.md                  # Step-by-step execution plan with live status tracking
├── context.md               # Background material + execution handoff
├── rework-<date>.md         # Sibling rework plan (optional — see **rework-plan-execution**)
└── evaluation-report.md     # POC only — evidence for the decision gate
```

| Item | Rule |
|---|---|
| Location | For an **orchestrate-feature-delivery** cell use the epic's delivery folder `deliveries/<epic-name>/{repo}/{feature-name}/` (already created by the orchestrator); otherwise resolve the artifact base via `resolve-artifact-location` and use `{base}/feature-implementations/{feature-name}/`. |
| Repo-first layout | When a plan belongs to a specific repo (a cell from **orchestrate-feature-delivery**), use `deliveries/<epic-name>/{repo}/{feature-name}/`; fall back to `{location}/{feature-name}/` when no repo applies. |
| Feature name | Derive a short, descriptive kebab-case name from the plan's objective (e.g., `add-auth-system`, `refactor-validation-handler`, `fix-null-pointer-in-transformer`). |
| Plan file | Contains the numbered step list with status emojis, updated in real-time as execution progresses. Serves as the live execution dashboard. |
| Context file | Captures background material — requirements docs, ADRs, user stories, spike findings, codebase references, constraints, assumptions, and decisions. When running as a dispatched agent, the executor appends an `## Execution` handoff (status, commit range, test evidence, review outcome, concerns). Background material otherwise stays unchanged. |
| Rework files | Each rework is a sibling `rework-<date>.md` in the same folder — `plan.md` stays the frozen original; the active rework file is found via the `## Reworks` manifest in `context.md` (see **rework-plan-execution**). |
| Evaluation report | POC mode only — written by **produce-poc-report** after the final evaluation step; read by the orchestrator's verification gate. |
| Permanent record | Both files are kept as a permanent record after execution completes — they are never deleted. |
