# Execution Modes

Conventions for the two special plan modes this skill executes. Normal plans run steps 1–N to completion; these modes restrict or stop execution.

## Rework mode — sibling `rework-<date>.md`
A rework plan (triggered by **orchestrate-feature-delivery**'s **handle-post-implementation-issue**) is a sibling `rework-<date>.md` in the feature folder — `plan.md` is the frozen original:
- Execute **only** the rework file's steps — the original steps are all ✅ and are never re-run or modified.
- Treat the rework steps as a fresh step sequence with **step-status-definitions** statuses (⏳ → 🔄 → ✅).
- When resuming, find the active rework file via the `## Reworks` manifest in `context.md` (the latest file with incomplete steps).
- **verify-prerequisites** still applies — the rework runs on its own branch per the repo's branch convention (the original branch/PR may already be merged).
- Commit conventions, **request-push-approval**, and **review-post-execution** apply exactly as for a normal plan.

## POC mode — `type: poc`
A POC plan (from **plan-development-task**'s **plan-poc** / an **orchestrate-feature-delivery** POC cell) executes like a normal feature on a **POC branch** — track, small-step commits, validation — but stops before merging:
- After the final **evaluation step**, produce the evaluation report (see **produce-poc-report**) and **STOP**.
- Pushing a POC branch is for review/evidence only — ask the user first
- Merging happens only after the orchestrator's decision gate adopts it
- Completion routes to the decision gate — never to plain **done**.
