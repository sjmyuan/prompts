# Comparison Diagram — Visual Pattern & Dimensions

Applies **create-handcrafted-diagram** in the edit-svg skill.

## Example SVGs

- `examples/diagnosis-comparison.svg` — Two-column comparison
- `examples/supply-vs-demand-thinking.svg` — Two-column with step flow inside each column
- `examples/channel-better-than-block-decision-flow.svg` — Three-column comparison
- `examples/solve-vs-align-decision-mode.svg` — Two-panel with complex internal flows

## Visual Patterns

### Two-column comparison
```
┌─────────────────────────┐ ┌─────────────────────────┐
│  Panel Header (colored) │ │  Panel Header (colored) │
├─────────────────────────┤ ├─────────────────────────┤
│ ┌─ Item 1 ────────────┐ │ │ ┌─ Item 1 ────────────┐ │
│ │ ✕ Description [tag] │ │ │ │ ⚠ Description [tag] │ │
│ └─────────────────────┘ │ │ └─────────────────────┘ │
│ ┌─ Item 2 ────────────┐ │ │ ┌─ Item 2 ────────────┐ │
│ │ ✕ Description [tag] │ │ │ │ ⚠ Description [tag] │ │
│ └─────────────────────┘ │ │ └─────────────────────┘ │
│ ┌─ Item N ────────────┐ │ │ ┌─ Item N ────────────┐ │
│ │ ✕ Description [tag] │ │ │ │ ⚠ Description [tag] │ │
│ └─────────────────────┘ │ │ └─────────────────────┘ │
│ ┌──── Summary (dashed) ┐│ │ ┌──── Summary (dashed) ┐│
│ │  Conclusion text      ││ │  Conclusion text      ││
│ └──────────────────────┘│ │ └──────────────────────┘│
└─────────────────────────┘ └─────────────────────────┘
```

### Three-column comparison (channel-better-than-block pattern)
```
┌──────────┐ ┌──────────┐ ┌──────────┐
│  Header1 │ │  Header2 │ │  Header3 │
├──────────┤ ├──────────┤ ├──────────┤
│ Row 1    │ │ Row 1    │ │ Row 1    │
│ text     │ │ text     │ │ text     │
├──────────┤ ├──────────┤ ├──────────┤
│ Row 2    │ │ Row 2    │ │ Row 2    │
│ text     │ │ text     │ │ text     │
├──────────┤ ├──────────┤ ├──────────┤
│ Row 3    │ │ Row 3    │ │ Row 3    │
│ text     │ │ text     │ │ text     │
└──────────┘ └──────────┘ └──────────┘
┌──────────── Bottom principle ────────────┐
└──────────────────────────────────────────┘
```

### Two-panel with internal flow (solve-vs-align pattern)
```
┌─── Panel 1 ───────────────────┐ ┌─── Panel 2 ───────────────────┐
│  Header                       │ │  Header                       │
│  ┌─ Problem ─┐                │ │  ┌─ Problem ─┐                │
│  │           │                │ │  │           │                │
│  └───┬───────┘                │ │  └───┬───────┘                │
│      │                        │ │      │                        │
│  ┌───▼───────┐                │ │  ┌───▼──────────┐            │
│  │ AI Solve  │                │ │  │ AI Assist    │ (dashed)   │
│  └───┬───────┘                │ │  └───┬──────────┘            │
│      │                        │ │      │                        │
│  ┌───▼───────┐                │ │  ┌───▼──────────┐            │
│  │ Solution  │                │ │  │Team Discussion│            │
│  └───────────┘                │ │  └───┬──────┬───┘            │
│                               │ │  ┌───▼┐  ┌─▼────┐           │
│                               │ │  │Pref│  │Concern│           │
│                               │ │  └──┬─┘  └──┬───┘           │
│                               │ │     └───┬───┘                │
│                               │ │     ┌───▼────┐               │
│                               │ │     │Consensus│              │
│                               │ └─────┴────────┘               │
└───────────────────────────────┘ └──────────────────────────────┘
```

## Dimension Guidelines

| Element | Value |
|---|---|
| ViewBox width | 800–960 |
| ViewBox height | 420–628 (taller if complex internal flows) |
| Column width (2-col) | ~300–350px each, 20–40px gap |
| Column width (3-col) | ~225px each, 20–30px gap |
| Title y | 30–36 |
| Column header height | 36–52px |
| Item box height | 44–68px |
| Item box rx | 6–8 |
| Inter-item gap | 10–15px |
| Summary box height | 50–80px |
| Summary dashed border | `stroke-dasharray="4,3"` |
| Panel background rx | 12–14 |

## Color Semantics

| Meaning | Header fill | Header text | Item stroke | Tag text |
|---|---|---|---|---|
| Problem/Negative | `#e74c3c` / `#ef4444` | white | `#fecaca` | `#ef4444` / `#c0392b` |
| Warning/Analysis | `#f39c12` / `#f59e0b` | white | `#fdba74` | `#e67e22` |
| Solution/Positive | `#27ae60` / `#22c55e` | white | `#86efac` | `#27ae60` |
| Info/Neutral | `#3b82f6` / `#6366f1` | white | `#a5b4fc` | `#3b82f6` |

## Key SVG Elements Reference

```svg
<!-- Panel background with gradient -->
<rect x="30" y="55" width="350" height="390" rx="12" fill="url(#blueGrad)" stroke="#93c5fd" stroke-width="2"/>

<!-- Panel header (colored, merges into panel via extension rect) -->
<rect x="30" y="55" width="350" height="52" rx="12" fill="#3b82f6"/>
<rect x="30" y="95" width="350" height="12" fill="#3b82f6"/>
<text x="180" y="88" text-anchor="middle" font-size="22" font-weight="700" fill="#ffffff">缺失</text>

<!-- Item inside panel -->
<rect x="55" y="155" width="250" height="44" rx="8" fill="#ffffff" stroke="#bfdbfe" stroke-width="1.5"/>
<circle cx="75" cy="177" r="10" fill="#dbeafe"/>
<text x="75" y="182" text-anchor="middle" font-size="12" fill="#3b82f6">✕</text>
<text x="95" y="177" font-size="14" fill="#374151" dominant-baseline="middle">Item text</text>
<text x="270" y="177" font-size="11" fill="#9ca3af" text-anchor="end" dominant-baseline="middle">tag</text>

<!-- Summary box (dashed border) -->
<rect x="55" y="340" width="250" height="80" rx="8" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1" stroke-dasharray="4,3"/>
<text x="180" y="365" text-anchor="middle" font-size="13" fill="#1d4ed8" font-weight="600">Summary text</text>

<!-- Linear gradient def -->
<linearGradient id="blueGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#eff6ff"/>
  <stop offset="100%" stop-color="#dbeafe"/>
</linearGradient>
```
