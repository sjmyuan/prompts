# Example: Updating an Existing Jira Story

## Scenario
The user holds a Jira story whose description is a rough draft and asks the assistant to refine it into a proper user story, then update the ticket with the refined content.

> "Here is Jira story STS-142. Its description is a rough draft — turn it into a proper user story and update the ticket with the refined content."

**Applies**: **update-user-story-in-tracker** (the story content below was refined and confirmed first via **define-user** → **define-functionality** → **define-benefit** → **define-acceptance-criteria** → **define-out-of-scope** → **define-prerequisites** → **draft-user-story**).

## Confirmed user story (input)

## User Story
**As a** logged-in business analyst,
**I want** to export the currently filtered report data as a CSV file,
**So that** I can process it further in Excel without manual data entry.

### Acceptance Criteria
**Scenario 1: Successful export**
- **Given** I am a logged-in business analyst viewing a filtered report
- **When** I click "Export as CSV"
- **Then** a CSV file downloads containing only the filtered rows, with headers matching the report

**Scenario 2: Empty result set**
- **Given** the current filter returns no rows
- **When** I click "Export as CSV"
- **Then** a CSV file with only the header row downloads, and a notice reports the export is empty

### Out of Scope
- Excel/PDF export formats: future story
- Scheduled exports: separate feature

### Prerequisites
- Reporting module with filters is implemented
- Role-based access control is in place

---

## Step 1 — Confirming the Target
**Agent** confirms:
> **Platform**: Jira. **Interface**: Atlassian MCP server (its issue tools are available in this session). **Item**: STS-142.

## Step 2 — Loading the Mapping
Loads `reference/tracker-attribute-mapping.md` for Jira: `summary` holds the concise title, `description` holds the statement plus supporting sections, and acceptance criteria lands in a discovered "Acceptance Criteria" custom field when present, else in the description.

## Step 3 — Fetching Current Attributes
Calls the MCP get-issue tool for STS-142:

```
STS-142 (Story)
summary:     "Export filtered reports as CSV"
description: "Analyst needs CSV export. Should download current rows."
customfield_10042 (Acceptance Criteria): (empty)
```

Notes: no built-in acceptance criteria field exists; `customfield_10042` is a project custom field named "Acceptance Criteria" and is empty. `description` is an ADF rich-text field — the MCP update tool's schema expects ADF content and does not convert Markdown.

## Step 4 — Mapping Sections to Attributes
| Story content | Attribute | Value |
|---|---|---|
| Title | `summary` | keep existing (already matches) |
| Statement + Out of Scope + Prerequisites | `description` | rendered story statement + sections (ADF) |
| Acceptance criteria scenarios | `customfield_10042` | rendered Given/When/Then scenarios (ADF) |

## Step 5 — Rendering in the Field's Native Format
The fetched issue stores its rich text as ADF, and the MCP update tool's schema declares `description` and rich custom fields expect ADF (it does not convert Markdown). The agent renders the confirmed Markdown story to ADF so STS-142 renders correctly:

- Story statement lines → ADF `paragraph` nodes
- `### Acceptance Criteria`, `### Out of Scope`, `### Prerequisites` → ADF `heading` (level 3) nodes
- Bullet lines (Given/When/Then, out of scope, prerequisites) → ADF `bulletList` → `listItem` nodes, with **Given/When/Then** as `strong` text
- Line breaks → separate ADF nodes, never a literal `\n`

```
description (rendered ADF):
  paragraph    "As a logged-in business analyst, ..."
  heading      "Acceptance Criteria"
  bulletList   ["Given I am a logged-in business analyst viewing a filtered report",
                "When I click \"Export as CSV\"",
                "Then a CSV file downloads with only the filtered rows"]
  ...
```

No literal `#`, `**`, or `- ` Markdown is written into the rich-text fields.

## Step 6 — Diffing Current vs Confirmed
- `summary` — unchanged → skip
- `description` — current content differs from the confirmed story → update
- `customfield_10042` — empty → set
- state, assignee, labels — not in scope → untouched

## Step 7 — Proposing the Update
**Agent proposes:**
| Attribute | Format | Action |
|---|---|---|
| `description` | ADF | replace with the rendered statement, out-of-scope, and prerequisites |
| `customfield_10042` | ADF | write the rendered Given/When/Then scenarios |

> OK to update these two attributes on STS-142? ✅

## Step 8 — Applying the Update
Calls the MCP update-issue tool for STS-142, passing only the two confirmed attributes in their rendered ADF form (`description`, `customfield_10042`).

## Step 9 — Verifying
Re-fetches STS-142: `description` now holds ADF paragraphs, headings, and list items, and `customfield_10042` holds the rendered scenarios — no raw Markdown remains, so both render correctly in Jira. Reports the ticket link and lists what changed.

> Updated STS-142 — https://your.atlassian.net/browse/STS-142 (description, acceptance criteria — rendered as ADF).

Azure DevOps equivalent: the same flow maps to `System.Title`, `System.Description`, and `Microsoft.VSTS.Common.AcceptanceCriteria`, rendering Markdown to HTML (`<div>`/`<h3>`/`<ul><li>`) before writing — see the reference.
