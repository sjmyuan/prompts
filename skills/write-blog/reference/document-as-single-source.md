# Document-as-Single-Source Convention

The article document is the only state carrier in a blog-writing session. Every turn updates it in place via file edits and reports only what changed. HTML comments separate auxiliary content from the article body.

## Body vs. comments
- The article body holds only clean prose — no markers.
- All auxiliary content lives in HTML comment blocks that name their role.

## Marker blocks

| Marker | Block | Purpose | Update rule |
|---|---|---|---|
| 📌 Title & Summary | `<!-- 📌 Title & Summary -->` … `<!-- /Title & Summary -->` | Title and summary candidates | Always present after the first draft; refresh when core content changes; never drop |
| 📋 Materials | `<!-- 📋 Materials -->` … `<!-- /Materials -->` | Raw ideas and fragments not yet in the body | Append continuously; move into the body once integrated |
| ❓ Gaps | `<!-- ❓ Gaps -->` … `<!-- /Gaps -->` | Missing evidence, logic, structure, or reader answers | Add at the relevant location; remove once filled |
| 💡 Assistant Notes | `<!-- 💡 Assistant Notes -->` … `<!-- /Assistant Notes -->` | Writing advice and improvement directions | Keep until the article is final; refresh on every update |
| 🖼️ Illustration Suggestions | `<!-- 🖼️ Illustration Suggestions -->` … `<!-- /Illustration Suggestions -->` | Where and what to illustrate | Replace with a Markdown image once realized |

## Summary candidates
- 2–3 candidates, each ≤120 characters, stating the article's core value.
- Ready for social media or the article description field.

## Output rules
- Edit the article document file in place with file-editing tools (e.g., in an editor like VS Code); do not paste the full document into the chat.
- Report only the changes made this turn: what was added, moved, or replaced, and where.
- Output the full document only when the user explicitly asks for it, or when the document file is being created for the first time.
- The user may stop at any point and resume from the document file.
- Never drop the Title & Summary block in any turn.
- Close every turn with 2–3 concrete next directions or deepening questions; never end with a passive "is this OK?".
