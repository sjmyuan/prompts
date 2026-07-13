# Create Step-Flow Diagram — Detailed Steps

Applies **create-step-flow-diagram** in the edit-svg skill.

Before starting, examine the example SVG in `examples/five-step-flow.svg` for visual reference.

## Visual Pattern

```
          Step 1          Step 2          Step 3          Step 4          Step 5
       ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────┐
       │    1     │   │    2     │   │    3     │   │    4     │   │  5   │
       │ ──────── │   │ ──────── │   │ ──────── │   │ ──────── │   │ ──── │
       │  Title   │   │  Title   │   │  Title   │   │  Title   │   │ Title│
       │  Sub     │   │  Sub     │   │  Sub     │   │  Sub     │   │ Sub  │
       │ ──────── │   │ ──────── │   │ ──────── │   │ ──────── │   │ ──── │
       │ ● Bullet │   │ ● Bullet │   │ ● Bullet │   │ ● Bullet │   │●Bull │
       │ ● Bullet │   │ ● Bullet │   │ ● Bullet │   │ ● Bullet │   │●Bull │
       └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────┘
  ───►      ────►          ────►          ────►          ────►
  (connecting arrows between steps)

  ════════════════════════════════════════════════════════════════════
  │              Bottom legend / insight text                        │
  ════════════════════════════════════════════════════════════════════

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ (loop arrow)
  (back loop from step 5 to step 1 for iteration)
```

## Dimension Guidelines

| Element | Value |
|---|---|
| ViewBox | 960×320 |
| Step box width | 115–160px |
| Step box height | 190px |
| Step box rx | 12 |
| Number circle radius | 18 |
| Number circle y (top) | 82 |
| Title y | 115 |
| Subtitle y | 135 |
| Separator line y | 148 |
| Bullet text y | 168, 186, 204, 228... |
| Arrow gap between steps | 8–12px |

## Color Progression (Steps Left to Right)

| Step | Gradient | Stroke | Circle fill |
|---|---|---|---|
| 1 (indigo) | `#eef2ff`→`#e0e7ff` | `#a5b4fc` | `#6366f1` |
| 2 (green) | `#f0fdf4`→`#dcfce7` | `#86efac` | `#22c55e` |
| 3 (orange) | `#fff7ed`→`#ffedd5` | `#fdba74` | `#f97316` |
| 4 (red) | `#fef2f2`→`#fee2e2` | `#fecaca` | `#ef4444` |
| 5 (purple) | `#f5f3ff`→`#ede9fe` | `#c4b5fd` | `#8b5cf6` |

## Key SVG Elements Reference

```svg
<!-- Step box -->
<rect x="15" y="52" width="160" height="190" rx="12" fill="url(#step1)" stroke="#a5b4fc" stroke-width="2"/>

<!-- Numbered circle -->
<circle cx="95" cy="82" r="18" fill="#6366f1"/>
<text x="95" y="88" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>

<!-- Step title and subtitle -->
<text x="95" y="115" text-anchor="middle" font-size="15" font-weight="700" fill="#1e1b4b">诊断</text>
<text x="95" y="135" text-anchor="middle" font-size="12" fill="#4f46e5">发现问题</text>

<!-- Separator line -->
<line x1="35" y1="148" x2="155" y2="148" stroke="#c7d2fe" stroke-width="1"/>

<!-- Bullet text lines -->
<text x="95" y="168" text-anchor="middle" font-size="11" fill="#374151">少了什么？→ 缺失</text>
<text x="95" y="186" text-anchor="middle" font-size="11" fill="#374151">多了什么？→ 越界</text>
<text x="95" y="208" text-anchor="middle" font-size="11" fill="#6b7280">都有→先处理越界</text>

<!-- Connecting arrow between steps -->
<line x1="175" y1="147" x2="215" y2="147" stroke="#9ca3af" stroke-width="2.5" marker-end="url(#arrow)"/>

<!-- Back loop arrow (dashed) -->
<path d="M 888 245 L 888 275 L 95 275 L 95 245" fill="none" stroke="#9ca3af" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrow)"/>
<text x="491" y="268" text-anchor="middle" font-size="11" fill="#9ca3af">未解决则迭代</text>

<!-- Bottom legend -->
<rect x="160" y="290" width="640" height="22" rx="11" fill="#f3f4f6"/>
<text x="480" y="305" text-anchor="middle" font-size="11" fill="#6b7280">技术会变，模型会变，但这个框架不会变</text>

<!-- Gradient def -->
<linearGradient id="step1" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#eef2ff"/>
  <stop offset="100%" stop-color="#e0e7ff"/>
</linearGradient>

<!-- Arrow marker -->
<marker id="arrow" markerWidth="12" markerHeight="8" refX="10" refY="4" orient="auto">
  <polygon points="0 0, 12 4, 0 8" fill="#9ca3af"/>
</marker>
```
