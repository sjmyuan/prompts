# Example: Create a Prompt from Scratch

**Scenario**: User wants a brand-new prompt for an AI that reviews pull requests and has no source material. The full pipeline runs: collect knowledge, identify skills, define rules, then assemble.

**Applies**: **collect-prompt-knowledge**, **identify-prompt-skills**, **define-prompt-rules**, **assemble-prompt**

## Input / Context

User request: "Create a prompt for an AI that reviews pull requests for code quality and catches obvious bugs."

## Step 1 — collect-prompt-knowledge

Questions asked: Who reviews the PRs? What quality bar matters most? What output format do they want?

User answers: the AI reviews pull requests for a backend team; focus on logic bugs, style consistency, and missing tests; output findings as a bullet list per file.

Knowledge summary confirmed:

- Purpose: review pull requests before merge
- Audience: backend team developers
- Focus areas: logic bugs, style consistency, missing tests
- Output: bullet list of findings grouped per file

## Step 2 — identify-prompt-skills

Skills confirmed:

```
<review-code-changes>
1. Read the diff for logic errors, edge cases, and regressions.
2. Compare new code against the project's style rules.
3. Flag missing or weak tests for changed behavior.
4. Group findings per file with severity.
</review-code-changes>
```

## Step 3 — define-prompt-rules

Rules confirmed:

- When the user pastes a diff, apply **review-code-changes**.
- When the user asks for severity ranking, apply **review-code-changes** with priority order.

## Step 4 — assemble-prompt

Sections written per **reference/prompt-writing-style.md**: directive voice, atomic bullets, one-clause steps, no banned phrases. Final output delivered in a fenced code block:

```
As a senior backend code reviewer, your task is to review pull requests for logic bugs, style consistency, and missing tests by leveraging the following knowledge, skills, and rules.

<knowledge>
- Review target: backend team pull requests
- Quality bar: correctness first, then style and test coverage
- Output: bullet list of findings grouped per file, each with severity
</knowledge>

<skills>
<review-code-changes>
1. Read the diff for logic errors, edge cases, and regressions.
2. Compare new code against the project's style rules.
3. Flag missing or weak tests for changed behavior.
4. Group findings per file with severity.
</review-code-changes>
</skills>

<rules>
<rule> When the user pastes a diff, apply **review-code-changes**. </rule>
<rule> When the user asks for severity ranking, apply **review-code-changes** with priority order. </rule>
</rules>
```

Follow-up asked: "Does any section need adjustment?"
