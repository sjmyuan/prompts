````markdown
# Example: Skill File Review

**Scenario**: Review of `skills/miniprogram/SKILL.md` — a copilot skill that guides an AI agent on WeChat Miniprogram development.

**Review Focus**: Skill structure correctness — whether `<knowledge>`, `<capabilities>`, `<rules>`, and `<examples>` sections each serve their intended purpose and are free of duplication.

## Code Review Summary

**Scope**: `skills/miniprogram/SKILL.md` — full skill file
**Focus Areas**: Section purpose compliance, duplication, information placement
**Overall Assessment**: Functional but requires restructuring — knowledge and capabilities are conflated, and rules repeat content already stated in capabilities.

---

## Findings

### 🔴 Major Issues

#### Capabilities contain reference knowledge, not procedural steps
- **File**: [SKILL.md](SKILL.md#L18-L130)
- **Issue**: Several capability sections are reference tables or factual lists rather than descriptions of *how to do something*. `<navigation-and-data-flow>` embeds two lookup tables (navigation API and data-passing patterns); `<wechat-api-usage>` lists API signatures and banned practices; `<project-structure>` describes the directory layout. These are knowledge the agent needs to recall, not actions to perform.
- **Impact**: The agent cannot distinguish "what I know" from "what I should do", making it harder to apply the correct step sequence when acting.
- **Recommendation**: Extract reference tables, directory layouts, API signatures, platform constraints, and banned-practice lists into a dedicated `<knowledge>` section. Keep capabilities as pure step-by-step procedures (e.g., "Steps to create and register a new page: 1. … 2. …").

#### Rules duplicate content already in capabilities
- **File**: [SKILL.md](SKILL.md#L133-L160)
- **Issue**: Most rules re-state implementation details already covered in capabilities. For example, the rule *"Canvas pages must set `"renderer": "webview"`"* repeats the same constraint already written inside `<canvas-operations>`. Similarly, the `try/catch` rule repeats `<storage-management>`, and the `wx.switchTab` rule repeats `<navigation-and-data-flow>`.
- **Impact**: Every constraint is maintained in two places; they can drift apart. The agent also receives redundant signal, bloating the prompt without adding guidance value.
- **Recommendation**: Rules should answer "**when** does this situation apply → **which capability** to use", not re-describe how the capability works. Example: *"When adding any new page, use **add-page**. Read `app.json` first — navigating to an unregistered page causes silent failures."*

### 🟡 Minor Issues

#### `<project-structure>` doubles as a capability and as knowledge
- **File**: [SKILL.md](SKILL.md#L18-L40)
- **Issue**: The section contains both a directory-layout reference (knowledge) and a new-page checklist (procedure). Mixing the two makes it unclear whether the agent should consult this section to recall a fact or to follow steps.
- **Recommendation**: Split into a `<project-structure>` knowledge entry (directory layout + package ownership rules) and an `<add-page>` capability (the checklist as ordered steps).

#### `<typescript-patterns>` and `<styling-conventions>` read as bullet-point knowledge, not capabilities
- **File**: [SKILL.md](SKILL.md#L95-L120)
- **Issue**: Both sections list facts and constraints (`"strict": true`, `rpx` for sizing) rather than describing a procedure to follow. A capability should answer "how do I apply TypeScript/styling in this project?", not just enumerate settings.
- **Recommendation**: Convert to step-by-step procedures ("How to type a miniprogram codebase: 1. … 2. …") or, for purely factual entries (tsconfig flags, forbidden units), move them to `<knowledge>`.

### 🟢 Nits / Suggestions

#### `<when-to-use-this-skill>` is well-formed — no change needed
- Accurately scopes the seven trigger scenarios. Good.

#### Example links are present but could align with capability names
- **File**: [SKILL.md](SKILL.md#L162-L175)
- The `<examples>` section links each example to a use-case description. After a rename from `<canvas-operations>` to `<canvas-setup-and-draw>`, the example description should use the same verb phrase for consistency.

### ⚠️ Inconsistencies (Decision Required)

#### Two styles of constraint expression inside capabilities
- **Variant A**: Prose bullets — *"Centralise access in `utils/storage.ts`; use named constants for keys"* — used in `<storage-management>`, `<typescript-patterns>`, `<styling-conventions>`
- **Variant B**: Imperative numbered steps — used in the new-page checklist inside `<project-structure>`
- **Trade-offs**: Prose bullets are compact and easy to scan; numbered steps make sequencing explicit and are easier for the agent to follow procedurally. Mixed usage makes it unclear which format is authoritative for capabilities.
- **Decision needed**: Should capabilities always use numbered steps (procedural), or are bullet lists acceptable for non-sequential guidance?

---

## Positive Highlights
- `<when-to-use-this-skill>` correctly limits skill activation to relevant scenarios.
- `<examples>` section properly defers to separate files and instructs the agent to load only the relevant one — good for context efficiency.
- Arrow references (`→ See examples/...`) at the end of each capability correctly point to the concrete code template without embedding it inline.
- The capability set covers the full miniprogram development surface (pages, components, canvas, storage, navigation, styling, TypeScript, subpackages).

---

## Risks & Assumptions
- The review assumes the intended semantics are: `<knowledge>` = facts to recall, `<capabilities>` = procedures to execute, `<rules>` = when-to-use-which-capability triggers. If the skill format has a different intended design, some findings may not apply.
- No runtime evaluation of whether the agent actually follows the skill more accurately after restructuring — that requires prompt testing.

---

## Recommended Next Steps
1. Introduce a `<knowledge>` section; move directory layout, lifecycle hooks, navigation tables, API signatures, and platform constraints into it. *(Addresses the two 🔴 major issues)*
2. Rewrite each capability as an ordered step list with a clear action verb in the section name (e.g., `<add-page>`, `<canvas-setup-and-draw>`). *(Addresses 🟡 and ⚠️)*
3. Rewrite rules as "scenario → capability" triggers; remove any rule that merely repeats a capability's content. *(Addresses the duplication 🔴)*
4. Decide on prose-bullets vs. numbered-steps as the canonical capability format and apply it consistently. *(Resolves ⚠️)*

---

## Key Review Characteristics

- **Review Type**: Skill file structural review
- **Severity Distribution**: 2 major, 2 minor, 1 nit, 1 inconsistency
- **Primary Concerns**: Section placement, duplication between rules and capabilities, procedural step format
- **Action Required**: Restructure before relying on this skill in production
- **Testing Recommendation**: After restructuring, test the skill on representative prompts to verify correct routing behavior
````
