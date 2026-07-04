# PPT Design Standards & Layout Principles

## PPT Design Requirements

All SVG output must meet professional presentation standards for PPT/Keynote/Google Slides.

- **Dimensions**: 16:9 aspect ratio (`viewBox="0 0 960 540"` default). Diagram fills 60–85% of slide area. Include a **title bar** (bold centered title, `#1A73E8` background, white text).
- **Visual effects**: Drop shadows on key shapes (`colors.get_shadow_filter()` or hand-crafted `<filter id="shadow">`), soft linear gradients for fills, rounded corners (`rx="6"`+).
- **Typography**: Set `font-family` on root `<svg>` element. Use `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif` for modern look, or `'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif` for Chinese content. Title: 16–22px bold. Body: 13–15px. Annotations: 9–11px. Min readable: 9px.
- **Text centering**: Use `text-anchor="middle"` with `dominant-baseline="middle"` on text inside shapes for reliable vertical centering.
- **Color contrast**: WCAG AA (≥4.5:1) for all text vs background. Light fills with dark text. Validate via `colors.wcag_aa_check()`.
- **Simplicity**: 5–8 main elements per diagram. ≤15 words per shape. Group elements with subtle background panels. Min 40px between groups, 20px within groups.

## SVG Layout Principles

**Two approaches** — see SKILL.md `<knowledge>` for the breakdown of script-based vs hand-crafted. Apply the right rules for each:

### Script-based layout principles
- **Canvas**: `viewBox="0 0 960 540"` default. Leave 20–40px padding.
- **Spacing**: Min 20px gap between adjacent shapes. Group-related: 10–15px internal, 30–40px external.
- **Connection corridor**: Min 40px gap between shapes needing connection lines. Multi-line: 60px+.
- **Line clearance**: Any line bend ≥25px away from any other element's edge.
- **Sizing**: Same semantic type → uniform size. Compute via `svg_builder.get_shape_dimensions()`.
- **Overlap avoidance**: Use `geometry.overlap()` / `geometry.find_overlapping()` — never manually check.

### Hand-crafted layout principles
- **Canvas**: Variable viewBox (800–960 wide, 320–628 tall). Adjust aspect ratio to content.
- **Spacing**: 10–15px between sibling items, 30–50px between sections.
- **Panel structure**: Layer `<rect>` backgrounds (`rx="12"`–`14"`) behind grouped elements.
- **Panel headers**: Full-width `<rect>` at top of panel area, same `rx` as panel, with an extension `<rect>` below (same color) to create a seamless header merge.
- **Title placement**: Centered at y=30–36 using `text-anchor="middle"`.
- **Z-order**: Backgrounds → panels → section lines → items → text. Connections drawn after panels, before items.
- **Shadow filter**: Hand-crafted `<filter id="shadow">` with `feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#00000020"`.
- **Alignment**: Same-row items across columns must share identical y-coordinates. Bullet text in same column uses consistent vertical spacing.

## Color Semantics by Purpose

| Purpose | Header fill | Accent | Item stroke | Best for |
|---|---|---|---|---|
| Problem/Negative | `#e74c3c` / `#ef4444` | `#fee2e2` | `#fecaca` | Errors, failures, warnings |
| Warning/Analysis | `#f39c12` / `#f59e0b` | `#ffedd5` | `#fdba74` | Root cause, analysis |
| Solution/Positive | `#27ae60` / `#22c55e` | `#dcfce7` | `#86efac` | Solutions, success |
| Info/Neutral | `#3b82f6` / `#6366f1` | `#dbeafe` | `#a5b4fc` | Information, processes |
| Knowledge (pyramid top) | `#fecaca` | `#fee2e2` | `#fecaca` | High-cognitive-load concepts |
| Skill (pyramid base) | `#86efac` | `#dcfce7` | `#86efac` | Low-cognitive-load concepts |

## Gradient Definitions (hand-crafted)

```svg
<linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#f8fafc"/>
  <stop offset="100%" stop-color="#f1f5f9"/>
</linearGradient>

<linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#6366f1"/>
  <stop offset="100%" stop-color="#8b5cf6"/>
</linearGradient>
```

## Shadow Filter (hand-crafted)

```svg
<filter id="shadow" x="-5%" y="-5%" width="110%" height="115%">
  <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#00000020"/>
</filter>
```

## Arrow Marker (hand-crafted)

```svg
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
  <path d="M 0 0 L 10 5 L 0 10 z" fill="#78909C"/>
</marker>
```

