# Code Comment Style

Generated code must follow the repo's comment convention and stay minimal. Comments explain *why*; the code explains *what*.

## Detect the repo's convention
1. Sample 3–5 recently modified files in the same module or language.
2. Check `.editorconfig`, CONTRIBUTING docs, or language style guides when present.
3. Note the density: no comments / terse why-comments / rich docstrings.
4. Record a one-line note in the plan file during **verify-prerequisites** (e.g., `Comment convention: sparse, why-only, no docstrings`).
5. If the repo is mixed, follow the dominant style of the files you are changing; ask the user only if genuinely split.

## Comment when (allowlist)
- Non-obvious intent or rationale a reader cannot infer from the code.
- Workarounds, hacks, or temporal coupling ("keep until X is migrated").
- Invariants or edge cases that must not be "fixed".
- Why a non-standard choice was made (performance, compatibility, team decision).

## Do NOT comment when (banlist)
- The code is self-explanatory — naming should carry the meaning.
- The comment would restate the statement (`// increments count` on `count++`).
- You want to narrate the change: `// added in step 3`, `// fixed the bug`, `// generated`.
- You want a banner or section divider (`// =====`, `// Step 1:`).
- You want to credit a tool or model (AI / Copilot / assistant mentions).
- The comment would just duplicate a docstring or a test name.

## Density matching

| Repo style | Generated code |
|---|---|
| No comments | Add none; move rationale to the commit message |
| Terse why-comments | Only 1–2 line why-comments on non-obvious lines |
| Rich docstrings | Docstrings on public API only, following the repo template; none on private/internal |

## Caps
- Line comment: ≤ 15 words, one line. If it needs more, rename the symbol or extract a helper instead.
- Docstring: 1–3 sentences per the repo template; skip entirely if the repo has none.

## Pre-commit self-check (commit-step)
Run this scan on the staged diff before committing:
- [ ] No comment restates the code it sits on.
- [ ] No narration markers (plan steps, "added/generated", banners, AI/tool names).
- [ ] Density matches the repo's sampled style.
- [ ] Deletion test: every remaining comment answers "why" — if removing it loses nothing, remove it.
