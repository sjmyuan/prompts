---
name: draft-user-story
description: Assist with drafting and refining user stories by gathering requirements, defining users, functionalities, benefits, acceptance criteria, out-of-scope items, and prerequisites. Use when users want to create, write, or refine a user story, define acceptance criteria or scope, or update the story in Jira or Azure DevOps via CLI or MCP.
---

<when-to-use-this-skill>
- User wants to create or write a user story for a feature or requirement
- User needs help structuring requirements into a standard user story format
- User wants to refine or improve an existing rough-draft user story
- User wants to update an existing user story in Jira or Azure DevOps (via CLI or MCP) with drafted or refined content
- User needs acceptance criteria defined for a feature
- User wants to clarify scope, prerequisites, or constraints for a story
</when-to-use-this-skill>

<knowledge>

<story-template>
Use the final-story layout in **reference/story-template.md** when assembling a story; it fixes the sections — statement, Given-When-Then scenarios, out of scope, prerequisites — so every capability writes to one shape.
</story-template>

<tracker-attribute-mapping>
Story sections map to platform- and project-specific tracker attributes; Jira acceptance criteria usually lives in a project custom field, Azure DevOps in a dedicated field. Fetch the item to discover real field names, write only changed sections, and render rich text in the field's native format. Full mapping: **reference/tracker-attribute-mapping.md**.
</tracker-attribute-mapping>

<context-loading-guide>
Load only the example directly relevant to the current scenario to minimize context size. Each drafting example walks through all seven core capabilities; the tracker example exercises **update-user-story-in-tracker** only.

| Load when | Provides | File |
|---|---|---|
| User requests a story for a feature with a single user type and a clear, direct action | Full walkthrough of the seven core capabilities for a simple single-actor story (e.g., Export CSV) | [examples/simple-feature-story.md](examples/simple-feature-story.md) |
| User requests a story involving multiple user roles, conditional behavior, or complex workflows | Full walkthrough of the seven core capabilities for a multi-role story | [examples/multi-role-story.md](examples/multi-role-story.md) |
| User provides a rough draft or incomplete story and wants it improved | Full walkthrough of the seven core capabilities applied to refining an existing draft | [examples/refining-existing-story.md](examples/refining-existing-story.md) |
| User asks to update a confirmed story into an existing Jira or Azure DevOps item | Walkthrough of **update-user-story-in-tracker** — attribute discovery, rendering, mapping, change-only update | [examples/update-existing-jira-story.md](examples/update-existing-jira-story.md) |
</context-loading-guide>

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
1. **Assemble the Story**: Combine all confirmed elements using the **story-template** reference:
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

<update-user-story-in-tracker>
**Objective**: Update an existing Jira or Azure DevOps user-story item through a CLI or MCP interface, writing only changed attributes in formats the tracker renders.

1. **Confirm the Update Target**: Confirm platform (Jira or Azure DevOps), interface (CLI or MCP), and the existing item key or ID; ask when not provided.
2. **Load the Attribute Mapping**: Load **reference/tracker-attribute-mapping.md** for the target platform's attribute names and content formats.
3. **Fetch Current Attributes**: Fetch the item's current attributes; note each editable field's accepted content format and how current values are stored.
4. **Map Story Sections to Attributes**: Map the confirmed story to attributes per the reference — a concise summary, the story statement and supporting sections in the description, acceptance criteria in a dedicated field when present (else in the description).
5. **Render in the Field's Format**: Convert the confirmed Markdown story into each target field's expected format per the reference; never write raw Markdown into a rich-text field.
6. **Diff Against Current Values**: Compare intended content with the fetched value and keep only attributes whose content actually changes (ignore markup differences).
7. **Present the Update Plan**: Show the proposed updates with their formats and request confirmation before writing.
8. **Apply the Updates**: Apply the confirmed updates through the chosen interface, passing only confirmed attributes in their rendered formats.
9. **Verify and Report**: Re-fetch each updated field to confirm it stores rendered rich text, not literal Markdown, then report the item key or URL.
</update-user-story-in-tracker>

</capabilities>

<rules>

<rule> In order, apply **define-user**, **define-functionality**, **define-benefit**, **define-acceptance-criteria**, **define-out-of-scope**, and **define-prerequisites**, confirming after each, then apply **draft-user-story** once all sections are confirmed. </rule>
<rule> When the user provides a rough draft, extract existing content and apply only the capabilities for missing or unclear sections. </rule>
<rule> When acceptance criteria lack Given-When-Then structure, reformat them and present to the user for confirmation. </rule>
<rule> When the user requests updating a finished or refined user story into an existing Jira or Azure DevOps item (via CLI or MCP), apply **update-user-story-in-tracker**. </rule>

</rules>

