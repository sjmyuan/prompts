# Skill-File Writing Style

Prose-quality rules for the skill under review: its SKILL.md, reference rubrics, and example files.
Complements conciseness (reference/conciseness-check.md) and section semantics (reference/section-semantics.md) — style flags how prose is written, structure flags what is placed where.

## Core rule: directive voice
- SKILL.md is a procedure the agent executes — write commands, not descriptions.
- Every capability step starts with an action verb. No "the agent should…", no passive voice.
- Knowledge entries state facts directly ("A well-formed skill file uses these sections…"), never "one may note that…".

## BLUF (Bottom Line Up Front)
- Open each section, knowledge entry, and rubric with the conclusion in one line, then the why.
- Capability objective = one line stating what the steps produce, before the steps.
- Never lead with evidence, background, or motivation.

## Hard caps

| Element | Cap |
|---|---|
| Frontmatter description | ≤30 words; two-part (domain + "Use when…") |
| Capability objective | 1 sentence |
| Capability step | 1 imperative instruction, one clause |
| When-to-use bullet | 1 scenario, 1 intent verb |
| Rule | 1 sentence ("When X → use **capability**") |
| Knowledge bullet | 1 fact |
| Paragraph | ≤3 sentences |
| Sentence | ≤20 words, one clause |

## Atomic bullets
- Each bullet = one claim, no justification or reasoning.
- Reasoning goes in a table or the section takeaway — never inside bullets.

## Tables over prose
- Rubrics, criteria, budgets, and severity maps are markdown tables.
- Prose's only job: one line summarizing the table.

## Sentence surgery
- Active voice, subject–verb–object, one clause.
- Banned phrases — delete or rewrite:
  - "It is important to note that…" / "It should be noted that…"
  - "In order to" → "To"
  - "As mentioned above / earlier"
  - "Please note"
  - "The goal/purpose of this section is…" / "This section describes…" (the heading is the summary)
  - "This means that" / "What this means is"
- Never restate what a heading, table, or diagram already shows.

## No meta-commentary or process narration
- Banned in all three file types: explanations of why a step exists, self-reference ("the above", "this step"), and narration of the author's actions ("I reviewed…", "we then…").
- Instruction text is self-explanatory; delete any sentence that only describes the document itself.

## Per-file rules

**SKILL.md**
- `description`: one-sentence domain summary + trigger phrase; trigger verbs match `<when-to-use-this-skill>`.
- `<when-to-use-this-skill>`: user-perspective scenarios, one per bullet, no justification.
- `<knowledge>`: noun-phrase subsection names; facts as tables or compact bullets; no procedural text.
- `<capabilities>`: numbered imperative steps; no tables, lookup lists, or constraint bullets (those belong in knowledge).
- `<rules>`: pure "when → capability" routing, one sentence, no implementation detail.

**Reference files**
- Title + rubric only; no narrative intro, no restatement of SKILL.md content.

**Example files**
- Scenario heading names the trigger and the distinguishing case; scenario = 1–2 sentences.
- Output shown as the capability would produce it — no meta-notes or narration inside the output.
- Minimum length needed to demonstrate the capability.

## The "So what?" test
- Every sentence must add a fact or answer "So what?" — otherwise delete it.
- Run this check on the final output before presenting.

## Severity

| Pattern | Severity |
|---|---|
| Isolated instance (1–2 across the skill) | 🟢 Nit |
| Systematic within one file | 🟡 Minor |
| Pervasive across multiple files | 🔴 Major |
