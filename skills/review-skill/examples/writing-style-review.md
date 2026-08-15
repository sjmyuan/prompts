# Example: Writing-Style Review (Voice, Banned Phrases, Narration)

**Scenario**: Review of `skills/release-note-writer/SKILL.md` — a copilot
skill that guides an agent to produce release notes from a commit log.
Structure, naming, and coverage are sound; prose quality is the dominant
problem.

**Review Focus**: Writing style — directive voice, BLUF, hard caps, banned
phrases, meta-commentary, and process narration in SKILL.md, its reference,
and its example.

## Code Review Summary

**Scope**: `skills/release-note-writer/` — SKILL.md + reference + example
**Focus Areas**: Voice, BLUF, sentence caps, banned phrases, narration
**Overall Assessment**: Structurally sound but pervasively verbose and
passive. Capability steps describe work instead of directing it; all three
files carry process narration. A full style pass is required.

---

## Findings

### 🔴 Major

#### Process narration and meta-commentary across all files
- **File**: SKILL.md, reference/grouping-rubric.md, examples/release-notes-from-log.md
- **Issue**: SKILL.md says *"This step is important because grouping
  determines the section order"*; the reference opens with *"As mentioned
  in the SKILL.md, grouping…"*; the example output narrates *"I reviewed
  the commit log and then grouped…"*.
- **Impact**: Context waste; the agent re-reads self-referential prose
  instead of acting.
- **Recommendation**: Delete all why-explanations and author narration;
  let the instruction text stand alone.

### 🟡 Minor

#### Capability steps are descriptive, not directive
- **File**: [SKILL.md](SKILL.md#L40-L58)
- **Issue**: Steps open passively — *"The commit log should be read first,
  and then the changes grouped by type"* — instead of imperative commands
  (*"Read the commit log"*, *"Group changes by type"*). The agent receives
  a description of work, not an instruction to perform it.
- **Impact**: Ambiguous execution; the agent may echo the steps back
  instead of running them.
- **Recommendation**: Rewrite every step as a direct imperative command
  starting with an action verb.

#### Banned phrases and over-long sentences
- **File**: [SKILL.md](SKILL.md#L12-L30)
- **Issue**: *"It is important to note that breaking changes must be listed
  first"*; *"In order to determine the version bump"*; line 18 is 34 words
  with stacked clauses.
- **Impact**: Passive filler dilutes instruction; long clauses hide the
  action.
- **Recommendation**: Apply the banned-phrase list and the ≤20-word
  sentence cap.

#### Knowledge entries lead with context, not the fact
- **File**: [SKILL.md](SKILL.md#L22-L28)
- **Issue**: `<grouping-order>` opens *"Release notes commonly group
  changes by type, and this ordering is widely used"* before stating the
  order. BLUF violated — the verdict arrives last.
- **Recommendation**: State the ordering rule first, then one line of
  rationale.

### 🟢 Nits / Suggestions

#### Example scenario runs long
- **File**: [examples/release-notes-from-log.md](examples/release-notes-from-log.md#L1-L6)
- **Issue**: The scenario paragraph is six sentences; the convention is
  1–2.
- **Recommendation**: Trim to two sentences naming the trigger and the
  case.

---

## Positive Highlights
- Structure, naming, and example coverage are clean — the style pass does
  not require re-plumbing the skill.
- `<when-to-use-this-skill>` bullets are atomic: one scenario each, no
  justification.

## Risks & Assumptions
- Writing-style severity follows the reference rubric (isolated → Nit,
  systematic → Minor, pervasive → Major). No structural re-review was
  performed here.

## Recommended Next Steps
1. Rewrite capability steps as imperative commands. *(Resolves 🟡 voice)*
2. Strip meta-commentary and narration from all three files. *(Resolves 🔴 narration)*
3. Apply the banned-phrase list and sentence caps. *(Resolves 🟡)*
4. Re-run the review to confirm style compliance.
