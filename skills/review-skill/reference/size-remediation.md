# Size Remediation — Actions for Files Over Budget

Apply when a file exceeds **both** the line and char budget (or the char budget alone). The char budget is the binding constraint — reformatting cannot reduce chars, so the only real levers are redistribution and reduction.

## Priority order: redistribute → reduce → escalate

### Redistribute — move content, don't cut it (fixes the per-file budget)
1. **Extract to `reference/`** — Move large rubrics, tables, criteria, or API lists out of `<knowledge>` and out of capability steps into `reference/*.md`; leave a one-line pointer in `<knowledge>` plus a `<context-loading-guide>` row.
2. **Two-stage extraction** — If a chunk is too big even for one reference file, move it capabilities → `<knowledge>` (as tables) → `reference/`; each hop shrinks SKILL.md further.
3. **Extract sub-procedures** — If a capability step is itself a long procedure, lift it into a reference procedure file with a pointer back.
4. **Split into a new skill** — If the chunk has its own trigger scenarios, knowledge, and examples and does not need shared state, extract it into its own skill with its own budget. Use only when genuinely standalone — otherwise you add cross-skill overhead without removing context.

### Reduce — the only true context-cost fix (cuts total chars)
5. **Dedupe** — Remove content restated elsewhere: rules re-stating capabilities, capability preambles re-describing delegated skills ("per X" instead of 5 lines), when-to-use re-stating the description, knowledge re-stating reference files.
6. **Merge related capabilities** — Collapse 2–3 small capabilities into one to remove objective/preamble boilerplate and repeated "load X" first-steps. Do not merge when the split isolates genuinely different procedures.
7. **Trim steps** — Drop edge cases, meta-commentary, and "why" explanations; keep only imperative steps.
8. **Tables over prose** — Convert repetitive bullet lists into compact tables, especially in `<knowledge>`.
9. **Condense knowledge** — Replace prose entries with a one-line pointer plus a compact table.
10. **Cut optional material** — Drop `<rules>` in single-capability skills; drop duplicated or low-value examples.

### Escalate — when reduction is exhausted
11. **Accept and flag** — Hub-scope skills may legitimately stay over budget after dedupe; record the residual overrun per the severity table as a known trade-off.
12. **Surface the decision** — Present split-vs-accept as an ⚠️ Inconsistency for the user to decide; do not silently pick.

## Anti-patterns — never suggest; flag when seen
- **Merging bullet steps into one sentence** — hides step structure, kills one-step-one-line scanability, only games the line count. Flag as 🟡 line-stuffing/gaming.
- **Line-merging** — joining short lines into long ones to pass the line budget (see `<size-limits>` gaming detection).
- **Cutting structural sections** — never remove `<when-to-use-this-skill>`, capability definitions, or other required sections.
- **Over-trimming steps** — trimming until steps are ambiguous saves chars but loses correctness.
- **Stripping example traceability** — removing an example's "Applies <capability>" reference to save chars.

## Severity signal
If a file still exceeds **>2×** the char budget after redistribute + reduce, that is the 🔴 Major signal that a real skill split is required — more trimming will not suffice.
