# Tracker Attribute Mapping (Jira & Azure DevOps)

Used by **update-user-story-in-tracker** (steps 2, 4, 5, 9).

## Story section → attribute
| Story section | Target concept | Where it lands |
|---|---|---|
| Title | Summary / Title — short one-liner, never the full statement | Jira `summary`; Azure DevOps `System.Title` |
| Story statement (As a / I want / So that) | Description | Jira `description`; Azure DevOps `System.Description` |
| Acceptance criteria (Given/When/Then) | Dedicated AC field when present, else Description | Jira: discovered custom field; Azure DevOps `Microsoft.VSTS.Common.AcceptanceCriteria` |
| Out of scope | Description (or a dedicated field when present) | appended to Description |
| Prerequisites | Description (or a dedicated field when present) | appended to Description |

The drafted story has no separate title. When the item's summary must change, ask the user for a concise one-liner or keep the existing summary — never dump the whole statement into the title field.

## Discover fields first
Real field names and keys are project-specific; Jira acceptance criteria is usually a project custom field (`customfield_xxxxx`). Before writing:
1. Fetch the existing item (by key or ID). Its returned fields are the ground truth for names, values, and formats.
2. When the interface exposes an editable-field list or field metadata, list it and match names to the story concepts case-insensitively (e.g., a field whose name contains "acceptance").
3. Match the field's content format: ADF (Jira rich fields), HTML (Azure DevOps rich fields), or plain (title, tags, numbers). When unsure, confirm against the interface's own schema or help before writing.

## Jira via Atlassian CLI or MCP
- Target is an issue key, e.g. `PROJ-123`.
- Detect which interface is available: an Atlassian/Jira MCP tool set or an installed CLI. If neither is clearly present, ask the user.
- MCP: an Atlassian MCP server typically exposes issue tools (fetch/get and update/edit). Inspect the tool's input schema and pass the issue key plus only the confirmed attributes.
- CLI: Jira CLIs vary. Run the issue subcommand's help to confirm exact flags; never assume them.
- Acceptance criteria: write it to a discovered "Acceptance Criteria" custom field when present; otherwise fold the scenarios into the description.
- Content format: Jira rich-text fields (description, rich custom fields) store ADF. Confirm whether the CLI/MCP converts Markdown or expects ADF, then render accordingly (see **Write content that renders**).
- Story points, priority, labels, and workflow fields are project/team-owned — change them only when the user explicitly asks.

## Azure DevOps via az boards CLI or MCP
- Target is a work item ID, e.g. `12345`, of type **User Story**.
- Stable field names: `System.Title`, `System.Description`, `Microsoft.VSTS.Common.AcceptanceCriteria`, `Microsoft.VSTS.Scheduling.StoryPoints`, `System.Tags`.
- Acceptance criteria is a dedicated field — write the Given/When/Then scenarios there.
- Content format: Description and Acceptance Criteria are HTML fields. Render Markdown to HTML (see **Write content that renders**) or confirm the tool converts it, so the ticket renders lists and line breaks.
- CLI: `az boards work-item show --id <id>` fetches the item; `az boards work-item update --id <id>` writes it. Organization and project come from config or the `--org`/`--project` flags.
- Confirm the exact title/description/acceptance-criteria flags with `az boards work-item update --help` before writing.
- MCP: an Azure DevOps MCP server exposes work-item tools; inspect the schema for title, description, and acceptance-criteria arguments.
- Never change state, area path, iteration path, assignee, or story points unless the user asks.

## Write content that renders
Rich-text fields store structured markup, not Markdown. Writing literal Markdown (`# `, `**`, `- `) into an ADF or HTML field stores text that does not render as intended. Render the confirmed story into each field's native format before writing; only plain-text fields (summary, tags, numbers) receive plain text.

When the interface's schema or help declares it accepts and converts Markdown, pass Markdown. When the field stores ADF or HTML, render the Markdown to that format first. Confirm which path applies before writing — never guess.

Render the story's Markdown to the field's format:

| Story element | Jira ADF | Azure DevOps HTML |
|---|---|---|
| Paragraph (story statement) | `paragraph` with `text` | `<div>` text or `<p>` |
| Section heading (`### Acceptance Criteria`) | `heading` (level 3) | `<h3>` or bold text |
| Bullet list (Given/When/Then, out of scope) | `bulletList` of `listItem` | `<ul><li>…</li></ul>` |
| Bold label (**Given**) | `text` with `strong` mark | `<b>` or `<strong>` |
| Line breaks | separate paragraphs or list items | `<br>` or separate `<div>` blocks, never a literal newline |

Before writing, the rendered value must contain the field's markup structure (ADF nodes or HTML tags), never raw Markdown such as `# `, `**`, or `- `.

## Change-only update
- Write only attributes whose current value differs from the confirmed story content.
- When a mapped attribute already matches, skip it and state that it was skipped.
- Never overwrite workflow or ownership attributes as a side effect of updating story content.

## Verify after writing
- Re-fetch each updated field and confirm it now holds rendered rich text with the intended content — no literal Markdown (`# `, `**`, `- `) remains.
- Confirm workflow and ownership fields were untouched.
- Report the item's key, ID, or URL and list exactly which attributes changed.
