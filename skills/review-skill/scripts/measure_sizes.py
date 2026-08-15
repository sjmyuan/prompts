#!/usr/bin/env python3
"""Measure copilot-skill file sizes against the review-skill size-limits doctrine.

Usage:
    python3 measure_sizes.py <path> [<path> ...]

Each <path> is a skill directory (walks all *.md) or an individual .md file.
Reports per file:
  - chars  — Unicode code points, the budget unit (use this, NOT bytes)
  - bytes  — for reference only; emoji/multi-byte chars inflate bytes above chars
  - lines
  - lines >120 and >200 chars, excluding documented exemptions:
    frontmatter `description`, table rows (start with `|`), mermaid blocks
  - budget status per file type (SKILL.md 12,000/150, reference/ 12,000/150,
    examples/ 9,000/150), with severity (SKILL.md: <=2x Minor, >2x Major)

Pure standard library — no dependencies, works on any platform with python3.
"""

from __future__ import annotations

import sys
from pathlib import Path

BUDGETS = {
    "SKILL.md": (12_000, 150),
    "reference": (12_000, 150),
    "examples": (9_000, 150),
}


def classify(path: Path) -> str | None:
    """Budget category for a file, or None if not a skill doc (.md under skills/)."""
    if path.name == "SKILL.md":
        return "SKILL.md"
    parts = path.parts
    if "reference" in parts:
        return "reference"
    if "examples" in parts:
        return "examples"
    return None


def scan(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    chars = len(text)
    nbytes = len(text.encode("utf-8"))
    nlines = len(lines)

    over120: list[tuple[int, int]] = []
    over200: list[tuple[int, int]] = []
    in_frontmatter = False
    in_mermaid = False

    for idx, raw in enumerate(lines, 1):
        stripped = raw.strip()
        if idx == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue  # frontmatter `description` is exempt; other fields are short
        if stripped.startswith("```mermaid"):
            in_mermaid = True
            continue
        if in_mermaid:
            if stripped.startswith("```"):
                in_mermaid = False
            continue  # mermaid blocks are exempt
        if stripped.startswith("|"):
            continue  # table rows (wide-cell exemption)
        n = len(raw)
        if n > 200:
            over200.append((idx, n))
        elif n > 120:
            over120.append((idx, n))

    category = classify(path)
    budget = "n/a"
    if category:
        char_cap, line_cap = BUDGETS[category]
        char_over = chars > char_cap
        line_over = nlines > line_cap
        if char_over or line_over:
            ratio = chars / char_cap
            severity = "Major" if category == "SKILL.md" and ratio > 2 else "Minor"
            budget = f"OVER {severity}: {chars}/{char_cap} chars, {nlines}/{line_cap} lines"
        else:
            budget = "OK"

    print(f"{path}  [{category or 'other'}]")
    print(f"  chars={chars} bytes={nbytes} lines={nlines}  budget: {budget}")
    if over200:
        print(f"  >200 chars: {len(over200)}  e.g. {over200[:8]}")
    if over120:
        print(f"  >120 chars: {len(over120)}  e.g. {over120[:8]}")
    print()


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 0
    for arg in argv:
        p = Path(arg)
        if p.is_dir():
            for f in sorted(p.rglob("*.md")):
                scan(f)
        else:
            scan(p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
