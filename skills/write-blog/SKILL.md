---
name: write-blog
description: Assist blog writing: gather ideas, fill gaps, and keep one document as the evolving draft with citations and illustrations. Use when writing, composing, reviewing, refining, referencing, or illustrating blog articles.
---

<when-to-use-this-skill>
- User wants existing content or scattered ideas shaped into a blog article
- User wants their material reviewed for gaps before writing
- User asks to compose a draft from collected material
- User shares links or sources to cite in the article
- User wants an existing draft reviewed and improved
- User wants language, style, or reader fit refined
- User wants illustrations generated for the article
</when-to-use-this-skill>

<knowledge>
<audience-profile>
Serve two reader groups: technical practitioners and team managers or tech leads. Technical readers want implementation detail, tool choice, and underlying logic. Managers want decision rationale, team impact, ROI, and reusable methods. Both value clear frameworks, evidenced claims, and transferable experience.
</audience-profile>
<language-rules>
- Match the user's language in dialogue and in the article
- Default to Chinese; switch or provide bilingual drafts on request
- Avoid translation-ese; write natural, fluent prose
</language-rules>
<markdown-formatting>
Quotes nested inside a bold span break Markdown rendering. Never write `**"term"**`; keep the quoted term outside the bold span (`"**term**"`) or drop one of the markers.
</markdown-formatting>
<writing-styles>
Four styles (deep analysis, narrative story, practical guide, opinion) plus the article structure. Details: [reference/writing-styles.md](reference/writing-styles.md)
</writing-styles>
<human-voice>
Write like a person narrating real experience to a colleague, not like an essay generator. Avoid AI-flavor words (e.g. 阴险, 赋能, 综上所述), telegraph-style runs of short sentences, parallel flourishes, and summary endings. Rules, blacklist, rhythm guidance, and the pre-delivery Human-Voice Gate checklist: [reference/human-voice.md](reference/human-voice.md). Hand-written style exemplars with extracted rules: [reference/style-exemplars.md](reference/style-exemplars.md)
</human-voice>
<document-as-single-source>
The article document is the only state carrier; HTML comments separate auxiliary content from the body. Every turn edits the document file in place and reports only the changes, not a full re-output. Details: [reference/document-as-single-source.md](reference/document-as-single-source.md)
</document-as-single-source>
<illustration-conventions>
Suggest 2–4 image positions per article; generate SVG illustrations on request. Details: [reference/illustration-standards.md](reference/illustration-standards.md)
</illustration-conventions>
<context-loading-guide>
| Load when | Provides | File |
|---|---|---|
| The marker blocks or document update loop is unclear | Document-as-single-source convention | [reference/document-as-single-source.md](reference/document-as-single-source.md) |
| Choosing a style or structuring the article | Four styles with structure and fit | [reference/writing-styles.md](reference/writing-styles.md) |
| Composing, reviewing, or refining any prose | Anti-AI-flavor rules, blacklist, rhythm, and the delivery gate | [reference/human-voice.md](reference/human-voice.md) |
| Composing or refining to match a personal voice | Hand-written exemplars and extracted style rules | [reference/style-exemplars.md](reference/style-exemplars.md) |
| Suggesting or generating an illustration | Image types, placement, naming, SVG rules | [reference/illustration-standards.md](reference/illustration-standards.md) |
| User pastes content or shares scattered ideas | Walkthrough of ingest, collect, and gaps | [examples/ingest-and-collect.md](examples/ingest-and-collect.md) |
| User asks to draft, review, or refine an article | Walkthrough of compose, reference, review, refine | [examples/compose-and-review.md](examples/compose-and-review.md) |
| User asks to generate an illustration | Walkthrough of SVG generation and placement | [examples/generate-illustrations.md](examples/generate-illustrations.md) |
</context-loading-guide>
</knowledge>

<capabilities>
<ingest-existing-content>
**Objective**: Classify pasted content and place it in the document.
1. Classify each pasted part as formed paragraph, rough draft, scattered note, or mixed.
2. Summarize the classification and which parts are usable.
3. Extract style cues (word choice, rhythm, perspective); record them in an assistant note.
4. Place formed paragraphs in the body with an assistant note; move drafts and notes to the materials block.
5. Mark found gaps in the gaps block.
6. Verify each part is classified and placed correctly.
7. Apply the edits to the article document file; report only the changes made, not the full document; ask 2–3 guiding questions.
</ingest-existing-content>
<collect-ideas>
**Objective**: Develop the user's ideas through listening and questions.
1. Listen; let the user speak without interruption.
2. Restate the core in 1–2 sentences to confirm understanding.
3. Ask 1–2 deepening questions (triggering event, reader takeaway, real example).
4. Append the points to the materials block.
5. Verify the materials block captures the new points.
6. Append the points to the article document file; report only the new points added, not the full document.
</collect-ideas>
<identify-gaps>
**Objective**: Find missing evidence, logic, structure, or reader answers.
1. Check the logic chain: clear thesis, enough evidence, no broken transitions.
2. List gaps by type: evidence, logic, structure, or reader perspective.
3. Ask a concrete question or offer a direction for each gap.
4. Mark each gap in the gaps block at its location.
5. Remove gap markers once filled; integrate the content.
6. Verify each listed gap is marked or filled.
7. Apply the gap markers to the article document file; report only the gaps marked or filled, not the full document.
</identify-gaps>
<compose-blog>
**Objective**: Turn collected material into a full draft that reads like a person wrote it.
1. Read reference/style-exemplars.md; state 2–3 style rules from it ("像这个人一样写") before composing.
2. Recommend a writing style from reference/writing-styles.md; confirm with the user.
3. Compose the draft with the user's own spoken sentences and material as the backbone — preserve their phrasing where it exists; AI connects, reorders, and fills gaps instead of rewriting their voice. If material is thin, compose from what exists and mark the thin spots as gaps.
4. Apply reference/human-voice.md while composing: plain words (no blacklisted AI-flavor words), varied rhythm (no 3+ consecutive short sentences), first-person and reader address, concrete anchors, no florification, no summary ending.
5. Compose title candidates, summary candidates, intro, body sections, and conclusion per the style's structure.
6. Put title and summary candidates in the title-and-summary block at the top.
7. Add an assistant note per section: intent, weakness, and improvement.
8. Write the draft into the article document file; output the title and summary candidates and a section outline in chat, not the full document; ask 3–4 targeted feedback questions.
9. Verify title and summary candidates and per-section notes are present.
10. Revise per feedback; refresh title and summary when core content changes.
</compose-blog>
<track-references>
**Objective**: Embed shared sources as inline links.
1. Extract the URL and title from each shared source.
2. Link it inline at the relevant paragraph with Markdown link syntax.
3. Confirm placement with the user.
4. Mark verbally mentioned, unlinked sources as gaps.
5. Verify every shared source is linked inline.
</track-references>
<suggest-images>
**Objective**: Mark 2–4 high-value illustration positions.
1. Scan the body for image-worthy spots: flows, comparisons, abstract concepts, real scenes.
2. Add an illustration-suggestion block after each spot with position, type, content, and purpose.
3. Keep 2–4 suggestions per article; prioritize the highest-value spots.
4. Replace the block with a Markdown image once the user provides a real image.
5. Verify each block carries position, type, content, and purpose.
</suggest-images>
<review-draft>
**Objective**: Improve the existing draft with refreshed notes.
1. Append new user content to the materials block; integrate it into the body.
2. Scan the full text; find 2–3 concrete improvement spots (argument, transition, evidence, rhythm).
3. Add refreshed assistant notes at those spots; never repeat prior notes.
4. Mark new gaps; update title and summary on substantive change.
5. Verify notes are refreshed, not repeated from prior rounds.
6. Apply the edits to the article document file; report only the changes made, not the full document; list 2–3 concrete next directions.
</review-draft>
<refine-style>
**Objective**: Make the prose natural, strong, and reader-adapted — and free of AI flavor.
1. Remove stiff transitions, repeated patterns, and translation-ese.
2. Strengthen each section's opening line.
3. Match depth to reader: detail for technical, meaning and value for managers.
4. Check the reader journey from pain point to insight.
5. Apply reference/human-voice.md: replace blacklisted AI-flavor words, break up telegraph-style runs of short sentences, remove parallel flourishes and 总结腔.
6. End with a conclusion, an action, or an open question — never a forced summary.
7. Run the Human-Voice Gate checklist from reference/human-voice.md (blacklist, telegraph, florification, anchor, voice, ending); report pass / fixed / gap per check; only deliver when all checks pass or gaps are deferred with the user's consent.
8. Verify opening lines are strong and depth matches the reader.
</refine-style>
<generate-illustrations>
**Objective**: Produce a real illustration file from a suggestion.
1. Locate the requested suggestion block; read its type and content description.
2. Extract key terms, steps, and relationships from the article context.
3. Generate SVG by default (PlantUML only on explicit request) per reference/illustration-standards.md.
4. Save to the article's assets folder with the naming rule from reference/illustration-standards.md.
5. Replace the suggestion block with a Markdown image link and optional caption.
6. Verify the image matches the suggestion and the file is placed per the standards.
7. Regenerate and overwrite the file when the user requests changes.
</generate-illustrations>
</capabilities>

<rules>
<rule>When the user pastes existing content into the document, use **ingest-existing-content**.</rule>
<rule>When the user shares new ideas or thoughts, use **collect-ideas**.</rule>
<rule>When material is abundant or the user asks what is missing, use **identify-gaps**.</rule>
<rule>When the user asks for a draft or material suffices, use **compose-blog**.</rule>
<rule>When the user shares links or sources, use **track-references**.</rule>
<rule>When a draft exists and the user adds material or asks for review, use **review-draft**.</rule>
<rule>When the user wants the prose polished, use **refine-style**.</rule>
<rule>When the user asks for an actual illustration, use **generate-illustrations**.</rule>
<rule>When composing or reviewing a draft, also use **suggest-images**.</rule>
<rule>When composing or refining any prose, apply **human-voice** rules from reference/human-voice.md and the style exemplars; never deliver a draft without passing the Human-Voice Gate.</rule>
</rules>
