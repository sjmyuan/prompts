# Example: Sub-Agent Integration Review (Dispatch-Style Skill)

**Scenario**: Review of `skills/parallel-doc-splitter/SKILL.md` — a copilot skill that splits a large specification into chapters, dispatches a drafting sub-agent per chapter, then merges the drafts into one document.

**Review Focus**: Agent integration (Axis 2) — dispatch brief contract, output contract, verification, availability fallback, and self-containment for embedded execution. Skill-to-skill pipeline checks skipped (no cross-skill references).
**Applies**: **review-skill-file**

## Code Review Summary

**Scope**: `skills/parallel-doc-splitter/SKILL.md` — full skill file  
**Focus Areas**: Sub-agent dispatch contract, output contract, verification, availability fallback, embedded-execution self-containment  
**Overall Assessment**: Solid orchestration design with four agent-integration gaps — one Major, three Minor.

---

## Findings

### 🔴 Major Issues

#### Dispatched drafts are merged without verification
- **File**: [SKILL.md](SKILL.md#L41-L52) (capability `<dispatch-chapter-drafting>`)
- **Issue**: The capability dispatches a drafting agent per chapter and merges the returned drafts directly into the final document with no verification step. Sub-agent output must be treated as unverified claims; merging unverified drafts propagates hallucinations into the shipped document.
- **Recommendation**: Add a verification step — question each returned draft, then dispatch a NEW same-type agent (never the original instance) to verify claims against primary sources before merging. See **reference/pipeline-integration.md** Axis 2 Direction A point 4 and `question-everything` **reference/verification-protocol.md**.

### 🟡 Minor Issues

#### Dispatch brief has no output contract
- **File**: [SKILL.md](SKILL.md#L44) (step 2 of `<dispatch-chapter-drafting>`)
- **Issue**: The brief instructs the agent to "draft the chapter," but does not require a structured return format (heading list, claim→source mapping, open questions). The orchestrator cannot compare or merge drafts without a fixed shape.
- **Recommendation**: Require each drafting agent to return a structured summary: chapter outline, claim→source references, and flagged gaps.

#### No fallback when no sub-agent is available
- **File**: [SKILL.md](SKILL.md#L41-L52)
- **Issue**: The capability assumes a drafting agent exists. On platforms without one, execution fails instead of falling back to direct drafting in the orchestrating agent.
- **Recommendation**: Add a detect-and-fallback rule: "When no suitable drafting agent is detected, draft chapters directly; keep the same merge step."

#### Chapter-splitting is not self-contained for embedded execution
- **File**: [SKILL.md](SKILL.md) knowledge (`<chapter-splitting>`)
- **Issue**: The split algorithm assumes the "earlier conversation" already identified the document's chapter boundaries; a dispatched agent that loads this skill has no such context and will fail headless.
- **Recommendation**: Move the chapter-detection heuristics into the skill so it re-derives boundaries from the document itself, or document an explicit input schema for the seeding brief.

---

## Positive Highlights
- The skill names the agent type it expects (`document-drafter`) and states the dispatch brief's minimum content — partial bidirectional awareness.
- Per-chapter dispatch preserves the orchestrator's context; the rationale is stated in knowledge.
- Merge rules for parallel results (de-duplicate headings, resolve conflicting sections) are explicit.

---

## Risks & Assumptions
- Review assumes the four-section skill semantics and that sub-agent dispatch is the platform's supported mechanism; the missing-verification severity assumes unverified agent output cannot be trusted by default.

---

## Recommended Next Steps
1. Add a verification loop before merging drafted chapters. *(Resolves 🔴 Major)*
2. Define an output contract in the dispatch brief template. *(Resolves 🟡 Minor)*
3. Add availability detection with a direct-execution fallback. *(Resolves 🟡 Minor)*
4. Make chapter-splitting self-contained or document its seed input schema. *(Resolves 🟡 Minor)*

One Major and three Minors block production use until verification is added.
