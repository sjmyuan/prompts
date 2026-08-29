# Example: Size and Line-Stuffing Review (Structural-Integrity Gate)

**Scenario**: Review of `skills/database-migration/SKILL.md` — a skill
guiding an AI agent through DB schema migrations. The author asserts the
file "fits the 150-line budget."

**Review Focus**: File size and density — whether the char budget (the
only size gate) is met, and whether lines were merged to dodge it.
**Applies**: **review-skill-file**

## Code Review Summary

**Scope**: `skills/database-migration/SKILL.md` — full skill file
**Focus Areas**: Size limits (char budget, line count, max line length),
line-stuffing, structural-integrity gate
**Overall Assessment**: Line count passes (138 ≤ 150) but the char budget
fails (≈21,000 vs 12,000, 1.75×) at an average ≈152 chars/line. The line
count is misleading: the file looks slim yet carries the context weight of
a ~300-line skill. The line-passes/char-fails mismatch plus long stuffed
lines indicate content was reformatted (lines merged), not reduced — a
structural-integrity-gate violation.

---

## Findings

### 🔴 Blocker

#### Suspected line-merging — revert and redo (structural-integrity gate)
- **File**: [SKILL.md](SKILL.md) — whole file
- **Measurements**: 138 lines / ≈21,000 chars (budget 150 / 12,000)
- **Issue**: The line count passes, but characters are 75% over budget.
  Reformatting cannot reduce characters, so context cost is unchanged —
  classic line-merging: short lines joined into long ones to stay under
  the 150-line limit without cutting content. Chars are the only size
  gate; a line-drop without a proportional char-drop is gaming.
- **Impact**: Context consumption stays ~75% over budget while the file
  *looks* compliant; the hidden step-vs-rule-vs-fact structure is lost.
- **Action**: 🔴 Blocker — **revert and redo**. Restore the merged lines to
  one line = one idea, then reduce chars with a real lever (re-encode the
  rule list as a decision table; extract the migration-rules rubric and
  command reference into `reference/`). Do not accept the file until the
  char budget is met with structure intact.

### 🟡 Minor Issues

#### Char budget exceeded (reduce with levers once the gate is met)
- **File**: [SKILL.md](SKILL.md) — whole file
- **Issue**: 21,000 chars vs the 12,000 cap (1.75×). Severity follows the
  char budget (🟡 Minor ≤ 2×). After merged lines are reverted, apply the
  lever order: re-encode (tables/matrices) → reuse (link sibling rubrics)
  → cut weight (meta-narration) → extract to `reference/`.
- **Recommendation**: Never merge lines to get here — extract and
  re-encode so chars drop while structure improves.

#### Multiple lines bundle 2+ logical items (line-stuffing)
- **File**: [SKILL.md](SKILL.md#L34-L40)
- **Issue**: e.g. line 36: *"`git checkout -b <branch>` — always branch;
  `up`/`down` pairs; never run `down` in production"* crams a command, a
  rule, and a banned practice into one line.
- **Impact**: Hides structure — a reader cannot tell whether a line is a
  step, a rule, or a fact; inflates average line length.
- **Recommendation**: Split to one line per idea, or move the command
  reference into `<knowledge>`.

### 🟢 Nits / Suggestions

#### 31 lines exceed 120 chars (aggregated)
- **File**: [SKILL.md](SKILL.md) — whole file
- Longest line is 214 chars. Prefer wrapping to one idea per line; the
  URL/Mermaid/table-cell exceptions do not apply to these prose lines.

---

## Positive Highlights
- Section order, capability naming, and example coverage are otherwise
  sound — this is a size/density problem, not a structural one.

## Risks & Assumptions
- Character counts are estimates from reading (sum of line lengths), not
  byte-exact.
- Assumes the size limit exists to bound context cost (tokens), which
  scales with characters, not lines.

## Recommended Next Steps
1. Revert the merged/stuffed lines to one line = one idea. *(Resolves the 🔴 Blocker)*
2. Re-encode the rule list as a decision table and extract the
   migration-rules rubric + command reference into `reference/` to bring
   chars under 12,000. *(Resolves the char-budget 🟡)*
3. Re-run `scripts/measure_sizes.py --diff` against the before state to
   confirm chars dropped and structure is intact (no gaming flag).
