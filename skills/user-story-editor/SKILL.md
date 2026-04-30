---
name: user-story-editor
description: 'The user story editor assists with drafting user stories by gathering requirements, defining users, functionalities, benefits, acceptance criteria, out-of-scope items, and prerequisites. Produces structured user stories using iterative Q&A with the user.'
---

<when-to-use-this-skill>
- User wants to create or write a user story for a feature or requirement
- User needs help structuring requirements into a standard user story format
- User wants to refine or improve an existing rough-draft user story
- User needs acceptance criteria defined for a feature
- User wants to clarify scope, prerequisites, or constraints for a story
</when-to-use-this-skill>

<knowledge>

<story-template>
Use this template when drafting the final user story:

```markdown
## User Story

**As a** [user role],
**I want** [functionality],
**So that** [benefit].

---

### Acceptance Criteria

**Scenario 1: [Happy Path Title]**
- **Given** [precondition]
- **When** [action]
- **Then** [expected outcome]

**Scenario 2: [Error/Edge Case Title]**
- **Given** [precondition]
- **When** [action]
- **Then** [expected outcome]

---

### Out of Scope
- [Item 1]: [brief reason]
- [Item 2]: [brief reason]

---

### Prerequisites
- [Prerequisite 1]
- [Prerequisite 2]
```

</story-template>

<example-selector>
Load only the example directly relevant to the current scenario to minimize context size.

- **Simple single-actor feature** — one user type, clear action (e.g., "Add login button", "Export CSV"): [examples/simple-feature-story.md](examples/simple-feature-story.md)
- **Complex multi-role story** — multiple user types, conditional behavior, or complex workflows: [examples/multi-role-story.md](examples/multi-role-story.md)
- **Refining an existing story** — user provides a rough draft or incomplete story to improve: [examples/refining-existing-story.md](examples/refining-existing-story.md)
</example-selector>

</knowledge>

<capabilities>

  <define-user>
1. **Identify the User Type**: Determine who the user is in the story:
   - Distinguish between end users, admins, developers, or system actors
   - Consider multiple user types if the story spans different roles
   - Ask clarifying questions if the user type is ambiguous (e.g., "Is this for an authenticated user or a guest?")
2. **Understand User Context**: Gather background about the user's situation and expectations:
   - Current pain points or needs the user has
   - Technical proficiency level if relevant to the story
   - System or platform the user is working with
3. **Confirm User Definition**: Present a structured summary, state the defined user role and context, and request confirmation or refinements before proceeding.
</define-user>

  <define-functionality>
1. **Identify Core Action**: Determine the primary action the user wants to perform:
   - Ask "What does the user want to do?" to extract the core verb and action
   - Break complex features into smaller, independent actions when appropriate
   - Note constraints and edge cases that shape the functionality
2. **Clarify Scope Boundaries**: Determine what is and isn't included:
   - Identify the minimum viable functionality needed
   - Note optional or stretch functionality that could be added later
   - Highlight any technical dependencies that constrain the functionality
3. **Confirm Functionality**: Summarize the core action in plain language and request confirmation before proceeding to benefits.
</define-functionality>

  <define-benefit>
1. **Identify Business or User Value**: Determine the "why" behind the story:
   - Ask "What problem does this solve?" or "What value does this deliver?"
   - Connect the benefit to measurable outcomes when possible (e.g., reduces time, increases accuracy)
   - Distinguish between user benefits (UX improvements) and business benefits (revenue, efficiency)
2. **Validate Relevance**: Ensure the benefit is a direct result of the described functionality; identify if multiple benefits exist and prioritize the primary one.
3. **Confirm Benefits**: Summarize the primary benefit in plain language and request confirmation before proceeding to acceptance criteria.
</define-benefit>

  <define-acceptance-criteria>
1. **Structure as Given-When-Then**: Write each criterion in BDD format:
   - **Given**: The precondition or initial state
   - **When**: The action the user performs
   - **Then**: The expected outcome or system response
2. **Ensure Testability**: Use specific, measurable conditions (e.g., "loads within 2 seconds", "displays error message X"); avoid vague language like "should work well".
3. **Cover All Scenarios**: Include the normal/happy path, error and edge cases, and permission or role-based variations if applicable.
4. **Confirm Acceptance Criteria**: Present the criteria list in Given-When-Then format and request confirmation or additions before proceeding.
</define-acceptance-criteria>

  <define-out-of-scope>
1. **Identify Exclusions**: Explicitly state what the story does NOT cover:
   - Features deferred to future stories
   - Related functionality that might be assumed but is not included
   - Technical concerns handled elsewhere (e.g., performance, security hardening)
2. **Justify Exclusions**: Briefly explain why each item is out of scope (deferred, handled separately, or excluded by product decision).
3. **Confirm Out-of-Scope Items**: Present the list and request confirmation or additions before proceeding.
</define-out-of-scope>

  <define-prerequisites>
1. **Identify Dependencies**: Determine what must be true before work begins:
   - Other user stories or features that must be completed first
   - Technical infrastructure or configuration required
   - External integrations or data that must be available
2. **Assess Risks**: Note any prerequisites that are uncertain or risky (dependencies on other teams, assumptions that could invalidate the story).
3. **Confirm Prerequisites**: Present the prerequisites list and request confirmation before finalizing the user story.
</define-prerequisites>

  <draft-user-story>
1. **Assemble the Story**: Combine all confirmed elements using the **story-template** knowledge:
   - User story statement: "As a [user], I want [functionality], so that [benefit]"
   - Acceptance criteria in Given-When-Then format
   - Out-of-scope section with brief justifications
   - Prerequisites section
2. **Review for Consistency**: Verify the functionality matches the acceptance criteria, the benefit is supported by the functionality, and out-of-scope items don't contradict the acceptance criteria.
3. **Validate Against INVEST Criteria**:
   - **I**ndependent — deliverable without depending on another story in progress
   - **N**egotiable — scope and implementation details are open to discussion
   - **V**aluable — delivers clear value to the user or business
   - **E**stimable — small and clear enough for the team to size it
   - **S**mall — deliverable within a single sprint; if not, split it
   - **T**estable — acceptance criteria are specific enough to verify
   - If the story fails any criterion, revise it before presenting for final approval.
4. **Present for Final Approval**: Share the complete draft, ask the user to review and confirm, and offer to refine any section based on feedback.
</draft-user-story>

</capabilities>

<rules>

<rule> When the user submits a requirement, apply **define-user** to gather information about the user. Confirm before proceeding. </rule>
<rule> After defining the user, apply **define-functionality** to identify key functionalities. Confirm before proceeding. </rule>
<rule> After defining functionalities, apply **define-benefit** to clarify the benefits. Confirm before proceeding. </rule>
<rule> After clarifying benefits, apply **define-acceptance-criteria** to list acceptance criteria in Given-When-Then format. Confirm before proceeding. </rule>
<rule> After listing acceptance criteria, apply **define-out-of-scope** to identify out-of-scope items. Confirm before proceeding. </rule>
<rule> After identifying out-of-scope items, apply **define-prerequisites** to gather prerequisites. Confirm before proceeding. </rule>
<rule> After all sections are confirmed, apply **draft-user-story** using the **story-template** knowledge to produce the final user story. </rule>
<rule> Always wait for the user's confirmation before advancing to the next capability. Do not skip steps or make assumptions without user input. </rule>
<rule> If the user provides a rough draft, extract existing information and apply only the capabilities for missing or unclear sections rather than starting from scratch. </rule>
<rule> When acceptance criteria lack Given-When-Then structure, reformat them accordingly and present to the user for confirmation before proceeding. </rule>
<rule> After user confirmation at each step, update the user story document accordingly. </rule>

</rules>

