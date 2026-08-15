# Example: Size and Line-Stuffing Review (Suspected Metric Gaming)

**Scenario**: Review of `skills/database-migration/SKILL.md` — a skill
guiding an AI agent through DB schema migrations. The author asserts the
file "fits the 150-line budget."

**Review Focus**: File size and density — whether the line-count budget
reflects the true context cost, and whether lines were merged to dodge it.
**Applies**: **review-skill-file**

## Code Review Summary

**Scope**: `skills/database-migration/SKILL.md` — full skill file
**Focus Areas**: Size limits (char budget, line count, max line length),
line-stuffing, gaming detection
**Overall Assessment**: Line count passes (138 ≤ 150) but the char budget
fails (≈21,000 vs 12,000, 1.75×) at an average ≈152 chars/line. The line
count is misleading: the file looks slim yet carries the context weight of
a ~300-line skill. The line-passes/char-fails mismatch plus long stuffed
lines indicate content was reformatted (lines merged), not reduced.

---

## Findings

### 🟡 Minor Issues

#### Char budget exceeded while line budget passes — suspected line-merging
- **File**: [SKILL.md](SKILL.md) — whole file
- **Measurements**: 138 lines / ≈21,000 chars (budget 150 / 12,000)
- **Issue**: The line count passes, but characters are 75% over budget.
  Reformatting cannot reduce characters, so context cost is unchanged —
  classic line-merging: short lines joined into long ones to stay under
  the 150-line limit without cutting content.
- **Impact**: Context consumption stays ~75% over budget while the file
  *looks* compliant; a line-count-only gate would clear it.
- **Recommendation**: Severity follows the char budget (🟡 Minor). Extract
  the migration-rules rubric and command reference into `reference/` files,
  and split merged lines so each line holds one idea. Do not accept the
  file until the char budget is met too.

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
1. Extract the migration-rules rubric and command reference into
   `reference/` to bring chars under 12,000. *(Resolves the char-budget 🟡)*
2. Split merged/stuffed lines to one idea per line. *(Resolves 🟡
   line-stuffing + 🟢 nit)*
3. Re-run the review to confirm both budgets pass.
