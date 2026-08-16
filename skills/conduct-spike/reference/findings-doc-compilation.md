# Findings-Doc Compilation

Full procedure for the `compile-findings-doc` capability — loaded on demand when the spike reaches findings-doc compilation, so the solution-doc procedure is never pulled in. Dispatch briefs: **reference/findings-doc-brief.md**; evidence-map rules: **reference/findings-document-guide.md**.

1. Determine the document strategy: **per-area** (2+ loosely-coupled areas) or **one consolidated doc** (tightly-coupled or single-area). Ask the user.
2. Dispatch findings-doc compilation to `solution-doc-writer` per **multi-agent-orchestration**; brief per **reference/findings-doc-brief.md**.
3. Verify the compiled doc via `question-everything`'s **verify-sub-agent-results**.
4. Validate per **reference/findings-document-guide.md**: each area's evidence map embedded inline — `file:line` entry points, call-chain sequence diagrams, an **Evidence & Verification** section per area (ledger: claim → verdict → `file:line` → confidence, 5-tag model; searched-negatives). Never vague references; never present inference as evidence.
5. Cross-reference between findings docs (if per-area): note cross-area constraints.
6. Ask: "Does this accurately capture the current state? Anything to add, correct, or remove?"
7. Save to `<spike-folder>/docs/findings-<area>.md` per **spike-artifact-layout**, then set the area's findings link and mark it `spiking` in `scope.md` per **scope-map-status**; findings docs are the **current-state baseline and evidence home** — update the evidence map on new evidence, no round/version tracking.
