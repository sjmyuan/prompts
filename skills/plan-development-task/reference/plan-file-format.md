# Plan File Format

Layout for the files **export-plan** writes into a feature folder.

## plan.md

1. Start with the ratified `## Scope Boundary` block (see **scope-boundary**): **In scope**, **Out of scope**, **Rule**, **Minor exceptions**.
2. Follow with the complete numbered step list; each step states one objective in one sentence.
3. A rework is a **new sibling file** `rework-<date>.md` (per **rework-plan-convention**): `# Rework <date>` + one-line trigger, its own **Scope Boundary**, and numbered steps — `plan.md` is the frozen original and is never modified.

## context.md

Concise (see **concise-writing**): one bolded takeaway per section, tables for requirements/constraints, compact bullet lists for references.

- Original request, change type, root cause/requirement summary
- TDD rationale; boundary rationale (see **scope-boundary**); branch + base (see **plan-prerequisites**)
- Constraints, assumptions, codebase references
- `## Reworks` manifest: one table row per rework (date, mode, cell, trigger, file, status) so resume finds the active file
- For an **orchestrate-feature-delivery** cell: the agent brief's spike references (ADR files, solution-doc sections)
