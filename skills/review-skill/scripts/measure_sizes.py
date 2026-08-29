#!/usr/bin/env python3
"""Measure copilot-skill file sizes against the review-skill size-limits doctrine.

Usage:
    python3 measure_sizes.py <path> [<path> ...]
    python3 measure_sizes.py --diff <before> <after>

Each <path> is a skill directory (walks all *.md) or an individual .md file.
Reports per file:
  - chars  — Unicode code points, the budget unit (use this, NOT bytes)
  - bytes  — for reference only; emoji/multi-byte chars inflate bytes above chars
  - lines
  - lines >120 and >200 chars, excluding documented exemptions:
    frontmatter `description`, table rows (start with `|`), mermaid blocks
  - likely line-stuffing: bullet/step lines >120 chars containing `;`
  - structural snapshot for SKILL.md (capabilities, steps, bullets, sections)
  - budget status per file type (SKILL.md 12,000/150, reference/ 12,000/150,
    examples/ 9,000/150), with severity (SKILL.md: <=2x Minor, >2x Major)

`--diff` compares two files (e.g. a skill before/after a size reduction) and
flags gaming — lines dropped while chars barely dropped (line-merging).

Pure standard library — no dependencies, works on any platform with python3.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BUDGETS = {
    "SKILL.md": (12_000, 150),
    "reference": (12_000, 150),
    "examples": (9_000, 150),
}

TAG_RE = re.compile(r"<([a-z][a-z0-9-]+)>")


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


def structural_counts(text: str) -> dict[str, int]:
    """Structural snapshot of a SKILL.md body (capabilities, steps, bullets, sections)."""
    body = text.split("---", 2)[2] if text.startswith("---") else text
    caps = re.search(r"<capabilities>(.*?)</capabilities>", body, re.S)
    caps_block = caps.group(1) if caps else ""
    counts: dict[str, int] = {
        "capabilities": len(TAG_RE.findall(caps_block)),
        "steps": sum(1 for ln in caps_block.splitlines() if re.match(r"^\s*\d+\.\s", ln)),
        "bullets": sum(1 for ln in caps_block.splitlines() if re.match(r"^\s*[-*]\s", ln)),
    }
    for tag in ("when-to-use-this-skill", "knowledge", "capabilities", "rules", "context-loading-guide"):
        counts[tag] = body.count(f"<{tag}>")
    return counts


def line_stats(text: str) -> tuple[list, list, list]:
    """Return (over120, over200, stuffed) line findings using documented exemptions."""
    lines = text.splitlines()
    exempt: set[int] = set()
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
            exempt.add(idx)
            continue  # frontmatter `description` is exempt; other fields are short
        if stripped.startswith("```mermaid"):
            in_mermaid = True
            exempt.add(idx)
            continue
        if in_mermaid:
            if stripped.startswith("```"):
                in_mermaid = False
            exempt.add(idx)
            continue  # mermaid blocks are exempt
        if stripped.startswith("|"):
            exempt.add(idx)
            continue  # table rows (wide-cell exemption)
        n = len(raw)
        if n > 200:
            over200.append((idx, n))
        elif n > 120:
            over120.append((idx, n))

    stuffed: list[tuple[int, int]] = []
    for idx, raw in enumerate(lines, 1):
        if idx in exempt:
            continue
        s = raw.strip()
        if len(s) > 120 and re.match(r"^\s*(?:[-*]|\d+\.)\s", s) and s.count(";") >= 1:
            stuffed.append((idx, len(s)))

    return over120, over200, stuffed


def scan(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    chars = len(text)
    nbytes = len(text.encode("utf-8"))
    nlines = len(lines)

    over120, over200, stuffed = line_stats(text)
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
    if stuffed:
        print(f"  >120 stuffed-like (bullet/step with ';'): {len(stuffed)}  e.g. {stuffed[:8]}")
    if category == "SKILL.md":
        counts = structural_counts(text)
        print("  structure: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    print()


def diff(a: Path, b: Path) -> None:
    ta, tb = a.read_text(encoding="utf-8"), b.read_text(encoding="utf-8")
    ca, cb = len(ta), len(tb)
    la, lb = len(ta.splitlines()), len(tb.splitlines())
    d_chars, d_lines = cb - ca, lb - la
    print(f"diff {a.name} -> {b.name}")
    print(f"  chars {ca} -> {cb}  ({d_chars:+d})")
    print(f"  lines {la} -> {lb}  ({d_lines:+d})")
    if d_lines < 0 and d_chars > d_lines * 30:
        print("  ⚠ GAMING? lines dropped but chars barely dropped — suspected line-merging")
    elif d_chars < 0:
        print("  OK: chars reduced")
    else:
        print("  ⚠ no char reduction")
    ca_counts = structural_counts(ta) if a.name == "SKILL.md" else {}
    cb_counts = structural_counts(tb) if b.name == "SKILL.md" else {}
    if ca_counts:
        for k in ca_counts:
            if ca_counts[k] != cb_counts.get(k):
                print(f"  structure {k}: {ca_counts[k]} -> {cb_counts.get(k)}")
    print()


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 0
    if argv[0] == "--diff":
        if len(argv) != 3:
            print("usage: measure_sizes.py --diff <before> <after>", file=sys.stderr)
            return 2
        diff(Path(argv[1]), Path(argv[2]))
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
