# Size Remediation — Actions for Files Over Budget

Apply when a file exceeds the char budget — the **only** size gate; line count is informational, for scanability.
Reformatting cannot reduce chars, so the real levers are structural: re-encode, reuse, cut weight, redistribute, or reduce.

## Structural-integrity gate — must pass before and after any reduction

**Chars are the only size gate.** A reduction is valid only if it measurably cuts chars while keeping one line = one idea.
Never reduce a line by removing its line break — joining bullets/steps keeps the content, hides the structure, and barely cuts chars.

Before reducing, snapshot the structure: `count(<capabilities>)`, `count(steps per capability)`, `count(<knowledge> subsections)`, `count(<when-to-use-this-skill> bullets)`, `count(<rules>)`, `count(guide rows)`, plus chars and lines.

After reducing, re-measure and apply the gate:
- **Pass** — char count dropped meaningfully AND structure preserved (same counts, or a structural drop matched by a real dedup-driven char drop).
- **🔴 Blocker — revert and redo** — lines dropped but chars barely moved (line-merging/gaming): restore one-line-one-idea, then reduce with a real lever below.
- **🔴 Blocker** — any line now bundles 2+ former bullets/steps (line-stuffing): split back to one line = one idea.

Run `scripts/measure_sizes.py` before and after to compare (it reports chars, lines, structural counts, and stuffed-line hits; `--diff` flags gaming).

## Reduction levers, in order

Apply each lever before the next; stop once the char budget is met.

### Re-encode — denser form, not shorter words
1. Convert procedural steps into decision/state tables or option matrices — the same meaning in fewer chars AND more structure.
2. Keep tables narrow (few columns, short cells) so the wide-cell exemption is not abused.

### Reuse — single owner, don't copy
3. Before writing a rubric, grep sibling skills; if it exists (e.g., writing-style, size-limits), link it via a relative path instead of re-describing it.

### Cut weight — eliminate, don't shrink
4. Delete meta-narration ("this capability…", "note that"), why-explanations, redundant preambles, low-value edge cases.
5. Run the "So what?" test on every line; delete lines that fail.

### Redistribute — move content, don't cut it (fixes the per-file budget)
6. **Extract to `reference/`** — Move large rubrics, tables, criteria, or API lists out of `<knowledge>` and out of capability steps into `reference/*.md`;
   leave a one-line pointer in `<knowledge>` plus a `<context-loading-guide>` row.
7. **Two-stage extraction** — If a chunk is too big even for one reference file, move it capabilities → `<knowledge>` (as tables) → `reference/`; each hop shrinks SKILL.md further.
8. **Extract sub-procedures** — If a capability step is itself a long procedure, lift it into a reference procedure file with a pointer back.
9. **Split into a new skill** — If the chunk has its own trigger scenarios, knowledge, and examples and does not need shared state,
   extract it into its own skill with its own budget.
   Use only when genuinely standalone — otherwise you add cross-skill overhead without removing context.

### Reduce — the only true context-cost fix (cuts total chars)
10. **Dedupe** — Remove content restated elsewhere: rules re-stating capabilities, capability preambles re-describing delegated skills
    ("per X" instead of 5 lines), when-to-use re-stating the description, knowledge re-stating reference files.
11. **Merge related capabilities** — Collapse 2–3 small capabilities into one to remove objective/preamble boilerplate and repeated "load X" first-steps.
    Legitimate only when real chars are cut (deduped content) — never just joined lines.
12. **Trim steps** — Drop edge cases, meta-commentary, and "why" explanations; keep only imperative steps.
13. **Tables over prose** — Convert repetitive bullet lists into compact tables, especially in `<knowledge>`.
14. **Condense knowledge** — Replace prose entries with a one-line pointer plus a compact table.
15. **Cut optional material** — Drop `<rules>` in single-capability skills; drop duplicated or low-value examples.

### Escalate — when reduction is exhausted
16. **Accept and flag** — Hub-scope skills may legitimately stay over budget after dedupe; record the residual overrun per the severity table as a known trade-off.
17. **Surface the decision** — Present split-vs-accept as an ⚠️ Inconsistency for the user to decide; do not silently pick.

## Anti-patterns — never suggest; flag as 🔴 Blocker
- **Merging bullet steps into one sentence** — hides step structure, kills one-step-one-line scanability, only games the line count. Revert and redo with a real lever.
- **Line-merging** — joining short lines into long ones to pass the line budget; detected when lines drop but chars barely do.
- **Cutting structural sections** — never remove `<when-to-use-this-skill>`, capability definitions, or other required sections.
- **Over-trimming steps** — trimming until steps are ambiguous saves chars but loses correctness.
- **Stripping example traceability** — removing an example's "Applies <capability>" reference to save chars.

## Severity signal
If a file still exceeds **>2×** the char budget after all levers, that is the 🔴 Major signal that a real skill split is required — more trimming will not suffice.
