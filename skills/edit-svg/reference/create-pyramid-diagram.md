# Create Pyramid Diagram — Detailed Steps

Applies **create-pyramid-diagram** in the edit-svg skill.

Before starting, examine the example SVG in `examples/srk-pyramid.svg` for visual reference.

## Visual Pattern

```
         ┌───────────────┐
         │ Knowledge     │  ← Top layer (narrowest, red tone)
         │ description   │
    ┌────┴───────┬───────┴────┐
    │  Rule                  │  ← Middle layer (orange tone)
    │  description           │
    │                        │
┌───┴───────────┬────────────┴───┐
│   Skill                    │   ← Bottom layer (widest, green tone)
│   description              │
│                            │
└────────────────────────────┘

┌──┐
│K │ Knowledge error (right side annotation)
└──┘
┌──┐
│R │ Rule error
└──┘
┌──┐
│S │ Skill slip
└──┘

┌──────────┐
│  高       │  (left side cognitive load indicator)
│  cognitive│
│  load     │
│  低       │
└──────────┘
```

## Dimension Guidelines

| Element | Value |
|---|---|
| ViewBox | 720×500 |
| Bottom layer span | 60px to 660px (width 600px) |
| Middle layer span | 120px to 600px (width 480px) |
| Top layer span | 185px to 535px (width 350px) |
| Layer height | ~120–130px each |
| Top of top layer (y) | 50 |
| Bottom of bottom layer (y) | 420 |

## Color Semantics by Layer

| Layer | Gradient start | Gradient end | Stroke | Text color |
|---|---|---|---|---|
| Top (Knowledge) | `#fef2f2` | `#fee2e2` | `#fecaca` | `#991b1b` |
| Middle (Rule) | `#fff7ed` | `#ffedd5` | `#fdba74` | `#9a3412` |
| Bottom (Skill) | `#f0fdf4` | `#dcfce7` | `#86efac` | `#166534` |

## Key SVG Elements Reference

```svg
<!-- Pyramid layer (trapezoid) -->
<polygon points="60,420 660,420 560,300 160,300" fill="url(#skillGrad)" stroke="#86efac" stroke-width="2"/>

<!-- Layer highlight (bottom edge shadow) -->
<polygon points="60,420 660,420 658,418 62,418" fill="#22c55e" opacity="0.15"/>

<!-- Layer label -->
<text x="360" y="385" text-anchor="middle" font-size="20" font-weight="700" fill="#166534">Skill（技能）</text>
<text x="360" y="408" text-anchor="middle" font-size="14" fill="#15803d">靠熟练度和直觉完成的行为</text>

<!-- Side annotation badge -->
<rect x="668" y="350" width="44" height="44" rx="22" fill="#dcfce7" stroke="#86efac" stroke-width="1.5"/>
<text x="690" y="375" text-anchor="middle" font-size="11" fill="#166534" font-weight="600">S</text>
<text x="690" y="410" text-anchor="middle" font-size="13" font-weight="600" fill="#16a34a">失误</text>

<!-- Divider lines between layers -->
<line x1="120" y1="282" x2="600" y2="282" stroke="#d1d5db" stroke-width="1" stroke-dasharray="4,3"/>

<!-- Arrow indicators between layers -->
<text x="360" y="296" text-anchor="middle" font-size="11" fill="#9ca3af">▼</text>

<!-- Gradient def -->
<linearGradient id="skillGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#f0fdf4"/>
  <stop offset="100%" stop-color="#dcfce7"/>
</linearGradient>

<!-- Cognitive load side bar -->
<rect x="10" y="50" width="42" height="370" rx="10" fill="#f3f4f6" stroke="#d1d5db" stroke-width="1"/>
<text x="31" y="235" text-anchor="middle" font-size="11" fill="#6b7280" transform="rotate(-90,31,235)">认知负荷</text>

<!-- Arrow on side bar -->
<polygon points="31,80 23,100 39,100" fill="#9ca3af"/>
<line x1="31" y1="100" x2="31" y2="370" stroke="#9ca3af" stroke-width="2"/>
```
