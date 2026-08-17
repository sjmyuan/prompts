# Plan File Format

Layout for the files **export-plan** writes into a feature folder.

## plan.md

1. Start with the ratified `## Scope Boundary` block (see **scope-boundary**): **In scope**, **Out of scope**, **Rule**, **Minor exceptions**.
2. Follow with the complete numbered step list; each step states one objective in one sentence.
3. When appending a rework (per **rework-plan-convention**), append a `## Rework <date>` section (with its own boundary) to the existing `plan.md` — never overwrite implemented steps.

## context.md

Concise (see **concise-writing**): one bolded takeaway per section, tables for requirements/constraints, compact bullet lists for references.

- Original request, change type, root cause/requirement summary
- TDD rationale; boundary rationale (see **scope-boundary**); branch + base (see **plan-prerequisites**)
- Constraints, assumptions, codebase references
- For an **orchestrate-feature-delivery** cell: the agent brief's spike references (change-summary items, ADR files, solution-doc sections)
