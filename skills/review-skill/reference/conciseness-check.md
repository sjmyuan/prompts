# Conciseness Check

Apply **Occam's Razor**: the simplest solution that works is the best — every element (step, rule, sentence, example) must justify its existence.
Prefer fewer lines, simpler phrasing, and direct instruction over elaborate explanation.
During review, examine all files (SKILL.md, references, and examples) for unnecessary content:

**SKILL.md:**
- Avoid verbose introductions or context-setting that merely restates the section name. The XML tag (e.g., `<capabilities>`) already signals intent.
- Avoid meta-commentary explaining *why* a step exists — the step text itself should be self-explanatory.
- Use bullet points or short phrases instead of full sentences where clarity allows.
- Do not repeat information already captured in other sections or in reference files.
- Avoid listing edge cases or exhaustive detail inside capability steps — those belong in reference files loaded on demand.
- Avoid over-engineered capability structures — a single, well-written capability is better than multiple split capabilities that add complexity without proportional value.
- Enforce **one line = one idea**: each line holds a single claim, step, item, or rule.
  A line bundling 2+ logical items (list items joined by `;`/`and`, multiple short facts) is line-stuffing — a violation even if the total line count is within budget.

**Reference files (`reference/`):**
- Contain only the specific rubric, criteria, or data the capability needs — no surrounding narrative or introductory text.
- Do not repeat or paraphrase content already in SKILL.md.

**Examples (`examples/`):**
- Each example should be the minimum length needed to demonstrate the capability.
- Avoid lengthy input/output sections that test irrelevant edge cases.
- Scenario descriptions should be brief — one or two sentences plus the essential input and output.

Flag conciseness violations as:
- A single file with notable verbosity → 🟢 Nit (can tighten, but not a structural problem).
- Multiple files or a systematic pattern of verbosity → 🟡 Minor (token waste reduces efficiency).
- The whole skill could be cut by >30% without losing meaning → 🔴 Major (severe bloat; must be refactored).
