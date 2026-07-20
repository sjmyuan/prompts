# Hand-Crafted Diagram Types — Visual Patterns & Dimensions

Applies **create-handcrafted-diagram** in the edit-svg skill.

Load [reference/design-standards.md](reference/design-standards.md) for PPT design rules.

---

## Comparison Diagram

### Visual Patterns

**Two-column comparison** — side-by-side panels with colored headers, item rows, and summary sections.

```
┌───────────────────────┐ ┌───────────────────────┐
│ Panel Header (colored)│ │ Panel Header (colored)│
├───────────────────────┤ ├───────────────────────┤
│ ┌─ Item ────────────┐ │ │ ┌─ Item ────────────┐ │
│ │ ✕ Description [t] │ │ │ │ ⚠ Description [t] │ │
│ └───────────────────┘ │ │ └───────────────────┘ │
│ ┌──── Summary (dash) ┐│ │ ┌──── Summary (dash) ┐│
│ │  Conclusion text    ││ │ │  Conclusion text    ││
│ └────────────────────┘│ │ └────────────────────┘│
└───────────────────────┘ └───────────────────────┘
```

**Three-column comparison** — equal-width columns with dimension rows.

**Two-panel with internal flow** — panels contain embedded flowchart-like process steps.

| Element | Value |
|---|---|
| ViewBox width | 800–960 |
| ViewBox height | 420–628 |
| Column width (2-col) | ~300–350px each, 20–40px gap |
| Column width (3-col) | ~225px each, 20–30px gap |
| Column header height | 36–52px |
| Item box height | 44–68px, `rx="6"–8` |
| Summary box height | 50–80px, `stroke-dasharray="4,3"` |
| Panel background `rx` | 12–14 |

| Meaning | Header fill | Header text | Item stroke | Tag text |
|---|---|---|---|---|
| Problem/Negative | `#e74c3c` | white | `#fecaca` | `#ef4444` |
| Warning/Analysis | `#f39c12` | white | `#fdba74` | `#e67e22` |
| Solution/Positive | `#27ae60` | white | `#86efac` | `#27ae60` |
| Info/Neutral | `#3b82f6` | white | `#a5b4fc` | `#3b82f6` |

### Key SVG Elements

```svg
<!-- Panel background -->
<rect x="30" y="55" width="350" height="390" rx="12" fill="url(#panelGrad)" stroke="#93c5fd" stroke-width="2"/>

<!-- Panel header (merges into panel via extension rect) -->
<rect x="30" y="55" width="350" height="52" rx="12" fill="#3b82f6"/>
<rect x="30" y="95" width="350" height="12" fill="#3b82f6"/>

<!-- Item row -->
<rect x="55" y="155" width="250" height="44" rx="8" fill="#fff" stroke="#bfdbfe" stroke-width="1.5"/>
<circle cx="75" cy="177" r="10" fill="#dbeafe"/>
<text x="75" y="182" text-anchor="middle" font-size="12" fill="#3b82f6">✕</text>
<text x="95" y="177" font-size="14" fill="#374151" dominant-baseline="middle">Description</text>
<text x="270" y="177" font-size="11" fill="#9ca3af" text-anchor="end" dominant-baseline="middle">tag</text>

<!-- Summary box (dashed) -->
<rect x="55" y="340" width="250" height="80" rx="8" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1" stroke-dasharray="4,3"/>
<text x="180" y="365" text-anchor="middle" font-size="13" fill="#1d4ed8" font-weight="600">Summary</text>
```

---

## Pyramid Diagram

Trapezoid layers stacked vertically, narrowing toward the top.

```
         ┌───────────────┐  ← top layer (narrow, red tone)
    ┌────┴───────┬───────┴────┐  ← middle (orange)
┌───┴───────────┬────────────┴───┐  ← bottom (wide, green)
└───────────────────────────────┘
```

| Element | Value |
|---|---|
| ViewBox | 720×500 |
| Bottom layer span | 60→660px (width 600px) |
| Middle layer span | 120→600px (width 480px) |
| Top layer span | 185→535px (width 350px) |
| Layer height | ~120–130px each |

| Layer | Gradient start | Gradient end | Stroke | Text color |
|---|---|---|---|---|
| Top (Knowledge) | `#fef2f2` | `#fee2e2` | `#fecaca` | `#991b1b` |
| Middle (Rule) | `#fff7ed` | `#ffedd5` | `#fdba74` | `#9a3412` |
| Bottom (Skill) | `#f0fdf4` | `#dcfce7` | `#86efac` | `#166534` |

### Key SVG Elements

```svg
<!-- Trapezoid layer -->
<polygon points="60,420 660,420 560,300 160,300" fill="url(#skillGrad)" stroke="#86efac" stroke-width="2"/>

<!-- Layer highlight (bottom edge shadow) -->
<polygon points="60,420 660,420 658,418 62,418" fill="#22c55e" opacity="0.15"/>

<!-- Layer label -->
<text x="360" y="385" text-anchor="middle" font-size="20" font-weight="700" fill="#166534">Skill（技能）</text>
<text x="360" y="408" text-anchor="middle" font-size="14" fill="#15803d">Description text</text>

<!-- Side annotation badge -->
<rect x="668" y="350" width="44" height="44" rx="22" fill="#dcfce7" stroke="#86efac" stroke-width="1.5"/>
<text x="690" y="375" text-anchor="middle" font-size="11" fill="#166534" font-weight="600">S</text>

<!-- Divider line between layers -->
<line x1="120" y1="282" x2="600" y2="282" stroke="#d1d5db" stroke-width="1" stroke-dasharray="4,3"/>
```

---

## Step-Flow Diagram

Horizontal step boxes laid left-to-right with connecting arrows, optional back-loop.

```
  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │    1     │   │    2     │   │    3     │
  │  Title   │──►│  Title   │──►│  Title   │
  │ ● Bullet │   │ ● Bullet │   │ ● Bullet │
  └──────────┘   └──────────┘   └──────────┘
     └──────────────────────────────────► (back loop)
```

| Element | Value |
|---|---|
| ViewBox | 960×320 |
| Step box width | 115–160px |
| Step box height | 190px, `rx="12"` |
| Number circle radius | 18 |
| Arrow gap | 8–12px |

| Step | Gradient | Stroke | Circle fill |
|---|---|---|---|
| 1 (indigo) | `#eef2ff`→`#e0e7ff` | `#a5b4fc` | `#6366f1` |
| 2 (green) | `#f0fdf4`→`#dcfce7` | `#86efac` | `#22c55e` |
| 3 (orange) | `#fff7ed`→`#ffedd5` | `#fdba74` | `#f97316` |
| 4 (red) | `#fef2f2`→`#fee2e2` | `#fecaca` | `#ef4444` |
| 5 (purple) | `#f5f3ff`→`#ede9fe` | `#c4b5fd` | `#8b5cf6` |

### Key SVG Elements

```svg
<!-- Step box -->
<rect x="15" y="52" width="160" height="190" rx="12" fill="url(#step1)" stroke="#a5b4fc" stroke-width="2"/>

<!-- Numbered circle -->
<circle cx="95" cy="82" r="18" fill="#6366f1"/>
<text x="95" y="88" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">1</text>

<!-- Labels -->
<text x="95" y="115" text-anchor="middle" font-size="15" font-weight="700" fill="#1e1b4b">Title</text>
<text x="95" y="135" text-anchor="middle" font-size="12" fill="#4f46e5">Subtitle</text>
<line x1="35" y1="148" x2="155" y2="148" stroke="#c7d2fe" stroke-width="1"/>
<text x="95" y="168" text-anchor="middle" font-size="11" fill="#374151">● Bullet</text>

<!-- Connecting arrow -->
<line x1="175" y1="147" x2="215" y2="147" stroke="#9ca3af" stroke-width="2.5" marker-end="url(#arrow)"/>

<!-- Back loop -->
<path d="M 888 245 L 888 275 L 95 275 L 95 245" fill="none" stroke="#9ca3af" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrow)"/>
```

---

## Container / Boundary Diagram

A dashed-boundary container with items inside and external items around edges.

```
╔══════════════╗
║  Container   ║  ← dashed border
║  ┌────────┐  ║     ┌──────────┐
║  │ Item A │  ║     │ External │
║  └────────┘  ║     └──────────┘
╚══════════════╝
   ┌─ Sub-step ─┐  ← bottom strategy flow
```

| Element | Value |
|---|---|
| ViewBox | 800×500 |
| Main container x/w | 50 / 700, rx=12 |
| Container border | dashed `stroke-dasharray="8,4"` |
| Border label badge | Pill-shaped rect overlapping border |
| Internal item | 190×56px |
| External item | 100×46px, rx=6 |

### Key SVG Elements

```svg
<!-- Main container (dashed border) -->
<rect x="50" y="50" width="700" height="310" rx="12" fill="#F5F7FA" stroke="#B0BEC5" stroke-width="2" stroke-dasharray="8,4"/>

<!-- Container label badge -->
<rect x="320" y="38" width="160" height="26" rx="13" fill="#fff" stroke="#B0BEC5" stroke-width="1.5"/>
<text x="400" y="56" text-anchor="middle" font-size="12" font-weight="700" fill="#546E7A">Label</text>

<!-- Internal item -->
<rect x="190" y="130" width="190" height="56" rx="6" fill="#E3F2FD" stroke="#90CAF9" stroke-width="1.5"/>
<text x="285" y="153" text-anchor="middle" font-size="13" font-weight="600" fill="#1565C0">Title</text>
<text x="285" y="173" text-anchor="middle" font-size="9" fill="#64B5F6">Detail line</text>

<!-- External item -->
<rect x="65" y="75" width="100" height="46" rx="6" fill="#FFF8E1" stroke="#FFB74D" stroke-width="1.5"/>

<!-- Arrow between items -->
<line x1="115" y1="75" x2="115" y2="38" stroke="#FF7043" stroke-width="1.5" marker-end="url(#arrow)"/>
```

---

## Donut Chart

Donut ring with annotated segments, center total label, and side annotation boxes.

```
     ┌──────────────────┐
     │  Annotation Box  │
     │  80% description │◄───── ┌───────┐
     │  bullet 1        │       │  NNN  │
     └──────────────────┘       │ total │
                                └───────┘
```

| Parameter | Value |
|---|---|
| Center (cx, cy) | (330, 210) |
| Outer radius (r) | 80 |
| Stroke width | 40 |
| ViewBox | 800×470 |

**Stroke-dasharray calculation** (r=80 → circumference=502.65): `segment_length = percentage * 502.65 / 100`

### Key SVG Elements

```svg
<!-- Background ring -->
<circle cx="330" cy="210" r="80" fill="none" stroke="#eee" stroke-width="40"/>

<!-- Colored segment (80%) -->
<circle cx="330" cy="210" r="80" fill="none" stroke="#EF5350" stroke-width="40"
  stroke-dasharray="402.12 502.65" stroke-dashoffset="0"
  transform="rotate(-90 330 210)" stroke-linecap="butt"/>

<!-- Center hole -->
<circle cx="330" cy="210" r="57" fill="#fff" stroke="#E0E0E0" stroke-width="1"/>
<text x="330" y="202" text-anchor="middle" font-size="21" font-weight="700" fill="#212121">1600万+</text>
<text x="330" y="222" text-anchor="middle" font-size="11" fill="#9E9E9E">Label</text>

<!-- Annotation box -->
<rect x="30" y="140" width="145" height="78" rx="8" fill="#E8F5E9" stroke="#A5D6A7" stroke-width="1.5"/>
<circle cx="52" cy="165" r="7" fill="#66BB6A"/>
<text x="68" y="169" font-size="12" font-weight="700" fill="#2E7D32">20% Label</text>
<text x="48" y="191" font-size="9" fill="#4A4A4A">Detail text</text>

<!-- Annotation connector -->
<line x1="235" y1="179" x2="175" y2="179" stroke="#66BB6A" stroke-width="1.5" marker-end="url(#arrow)"/>
```
