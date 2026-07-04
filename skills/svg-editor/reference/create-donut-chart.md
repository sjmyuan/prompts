# Create Donut Chart — Detailed Steps

Applies **create-donut-chart** in the svg-editor skill.

Before starting, examine the example SVG in `examples/survival-rate-chart.svg` for visual reference.

## Visual Pattern

```
  ┌────────────────────┐                    ┌──────────────────────┐
  │  Label (20%)       │◄──────────────────►│  Annotation Box      │
  │  bullet 1          │     ┌───────┐      │  80% description     │
  │  bullet 2          │     │  NNN  │      │  bullet 1            │
  └────────────────────┘     │ total │      │  bullet 2            │
                             └───────┘      └──────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │          Data source / additional context                        │
  └─────────────────────────────────────────────────────────────────┘
```

## Donut Geometry

| Parameter | Value |
|---|---|
| Center (cx, cy) | (330, 210) |
| Outer radius (r) | 80 |
| Stroke width | 40 |
| ViewBox | 800×470 |

**Stroke-dasharray calculation:**
- Total circumference = `2 * PI * r = 2 * 3.14159 * 80 = 502.65`
- Segment length = `percentage * 502.65 / 100`
- First segment: `stroke-dasharray="segment_len (total - segment_len)" stroke-dashoffset="0"`
- Second segment: `stroke-dasharray="segment2_len (total - segment2_len)" stroke-dashoffset="-(segment1_len)"`

## Key SVG Elements Reference

```svg
<!-- Background donut ring -->
<circle cx="330" cy="210" r="80" fill="none" stroke="#EEEEEE" stroke-width="40"/>

<!-- Colored segment (e.g., 80% red) -->
<circle cx="330" cy="210" r="80" fill="none" stroke="#EF5350" stroke-width="40"
  stroke-dasharray="402.12 502.65" stroke-dashoffset="0"
  transform="rotate(-90 330 210)" stroke-linecap="butt"/>

<!-- Colored segment (e.g., 20% green) -->
<circle cx="330" cy="210" r="80" fill="none" stroke="#66BB6A" stroke-width="40"
  stroke-dasharray="100.53 502.65" stroke-dashoffset="-402.12"
  transform="rotate(-90 330 210)" stroke-linecap="butt"/>

<!-- Center hole -->
<circle cx="330" cy="210" r="57" fill="#FFFFFF" stroke="#E0E0E0" stroke-width="1"/>
<text x="330" y="202" text-anchor="middle" font-size="21" font-weight="700" fill="#212121">1600万+</text>
<text x="330" y="222" text-anchor="middle" font-size="11" fill="#9E9E9E">存量一人公司</text>

<!-- Annotation box (left) -->
<rect x="30" y="140" width="145" height="78" rx="8" fill="#E8F5E9" stroke="#A5D6A7" stroke-width="1.5"/>
<circle cx="52" cy="165" r="7" fill="#66BB6A"/>
<text x="68" y="169" font-size="12" font-weight="700" fill="#2E7D32">20% 跑通闭环</text>
<text x="48" y="191" font-size="9" fill="#4A4A4A">自带客户或行业积累</text>
<text x="48" y="207" font-size="9" fill="#4A4A4A">AI 是放大器，不是发动机</text>

<!-- Connecting line (annotation → donut) -->
<line x1="235" y1="179" x2="175" y2="179" stroke="#66BB6A" stroke-width="1.5" marker-end="url(#arrow-green)"/>

<!-- Annotation box (right) -->
<rect x="520" y="145" width="190" height="78" rx="8" fill="#FFF5F5" stroke="#FFCDD2" stroke-width="1.5"/>
<circle cx="542" cy="170" r="7" fill="#EF5350"/>
<text x="558" y="174" font-size="12" font-weight="700" fill="#C62828">80% 悄悄退场</text>
<text x="538" y="196" font-size="9" fill="#4A4A4A">未跑通商业闭环</text>
<text x="538" y="212" font-size="9" fill="#4A4A4A">核心原因：没有市场需求</text>

<!-- Bottom data source box -->
<rect x="200" y="345" width="400" height="58" rx="8" fill="#F5F7FA" stroke="#CFD8DC" stroke-width="1"/>
<text x="400" y="370" text-anchor="middle" font-size="13" font-weight="600" fill="#546E7A">2025 年新设 731.5 万户，同比增长</text>
<text x="528" y="370" font-size="14" font-weight="700" fill="#FF7043">+42.3%</text>
```
