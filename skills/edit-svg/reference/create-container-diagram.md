# Create Container/Boundary Diagram — Detailed Steps

Applies **create-container-diagram** in the edit-svg skill.

Before starting, examine the example SVGs in `examples/` for visual reference:
- `examples/niche-market-strategy.svg` — Dashed boundary container with niche markets around edges
- `examples/feedback-architecture.svg` — Complex container with side panels and flow lines

## Visual Pattern (niche-market-strategy)

```
                                      ╔══════════════╗
         ┌──────────┐                 ║  大 市 场    ║
         │细分市场  │                 ╚══════════════╝
         │投入小    │    ┌───────────────────────────────┐
         └────▲─────┘    │  ┌─────────┐  ┌─────────┐    │
              │          │  │大公司 A │  │大公司 B │    │
              │          │  │投入大    │  │重流程   │    │
              │          │  └─────────┘  └─────────┘    │
         ┌────┴─────┐    │  ┌─────────┐  ┌─────────┐    │
         │细分市场  │◄───│  │大公司 C │  │大公司 D │    │
         │影响力    │    │  │决策慢   │  │看不上小  │    │
         └──────────┘    │  └─────────┘  └─────────┘    │
              │          └───────────────────────────────┘
         ┌────▼─────┐                  │
         │细分市场  │                  │
         │从角落扎根│                  │
         └──────────┘                  │
                                       │
                  ┌───┐    ┌───┐    ┌───┐
                  │切入 │──►│站稳 │──►│扩展 │
                  └───┘    └───┘    └───┘
```

## Dimension Guidelines

| Element | Value |
|---|---|
| ViewBox | 800×500 |
| Main container x/w | `x=50, width=700` |
| Main container y/h | `y=50, height=310` |
| Main container rx | 12 |
| Container border | dashed `stroke-dasharray="8,4"` |
| Border label badge | Pill-shaped rect overlapping border |
| Internal item width | 190px |
| Internal item height | 56px |
| External item width | 100px |
| External item height | 46px |
| External item rx | 6 |
| Bottom strategy height | 70px |

## Key SVG Elements Reference

```svg
<!-- Main container (dashed border) -->
<rect x="50" y="50" width="700" height="310" rx="12" fill="#F5F7FA" stroke="#B0BEC5" stroke-width="2" stroke-dasharray="8,4"/>

<!-- Container label badge (overlapping border) -->
<rect x="320" y="38" width="160" height="26" rx="13" fill="#FFFFFF" stroke="#B0BEC5" stroke-width="1.5"/>
<text x="400" y="56" text-anchor="middle" font-size="12" font-weight="700" fill="#546E7A">大 市 场</text>

<!-- Internal items (companies inside container) -->
<rect x="190" y="130" width="190" height="56" rx="6" fill="#E3F2FD" stroke="#90CAF9" stroke-width="1.5"/>
<text x="285" y="153" text-anchor="middle" font-size="13" font-weight="600" fill="#1565C0">大公司 A</text>
<text x="285" y="173" text-anchor="middle" font-size="9" fill="#64B5F6">投入大 · 覆盖广</text>

<!-- External items (niche markets around edges) -->
<rect x="65" y="75" width="100" height="46" rx="6" fill="#FFF8E1" stroke="#FFB74D" stroke-width="1.5"/>
<text x="115" y="94" text-anchor="middle" font-size="11" font-weight="600" fill="#E65100">细分市场</text>
<text x="115" y="110" text-anchor="middle" font-size="9" fill="#FF9800">投入小 · 决策快</text>

<!-- Connecting arrow (external → container or container → external) -->
<line x1="115" y1="75" x2="115" y2="38" stroke="#FF7043" stroke-width="1.5" marker-end="url(#arrow-orange)"/>

<!-- Arrow marker -->
<marker id="arrow-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
  <path d="M 0 0 L 10 5 L 0 10 z" fill="#FF7043"/>
</marker>

<!-- Internal subgroup (dashed boundary around grouped items) -->
<rect x="170" y="110" width="460" height="180" rx="10" fill="none" stroke="#BBDEFB" stroke-width="1" stroke-dasharray="4,4" opacity="0.6"/>

<!-- Bottom strategy flow (pill-shaped rects with arrows) -->
<rect x="238" y="395" width="105" height="30" rx="15" fill="#E3F2FD" stroke="#90CAF9" stroke-width="1.2"/>
<text x="290" y="414" text-anchor="middle" font-size="11" font-weight="600" fill="#1565C0">切入细分市场</text>
<line x1="348" y1="410" x2="378" y2="410" stroke="#78909C" stroke-width="1.5" marker-end="url(#arrow-gray)"/>
```
