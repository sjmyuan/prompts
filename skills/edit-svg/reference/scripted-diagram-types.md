# Scripted Diagram Types — Layout Patterns & Dimensions

Applies **create-scripted-diagram** in the edit-svg skill.

Load [reference/computation-snippets.md](computation-snippets.md) for script patterns and [reference/design-standards.md](design-standards.md) for PPT standards.

---

## Architecture Diagram

Horizontal tier layers stacked top-to-bottom. Each tier has a colored header band and subtle background panel.

| Tier | Purpose | Example |
|---|---|---|
| Top (row 0) | Client/Presentation | Browser, Mobile App |
| Upper-mid (row 1) | Edge/Gateway | CDN, Load Balancer, API Gateway |
| Lower-mid (row 2) | Application/Services | Auth Service, Business Logic |
| Bottom (row 3) | Data/Storage | PostgreSQL, Redis Cache |

| Parameter | Default |
|---|---|
| Tier gap (vertical) | 160–200px |
| Component gap (horizontal) | 60–100px |
| Service box | `process` type, ~160×50px |
| Database box | `data` type, ~140×60px |

Draw subtle background `<rect>` for each layer band using `PPT_PALETTE["bg_panel"]`. Use `svg_builder.generate_section_panel()` for layer backgrounds.

---

## Sequence Diagram

Participants arranged horizontally at top, messages flow chronologically downward. Each participant has a dashed vertical lifeline.

- `nodes[]`: participants with `type: "process"`, `row: 0`, distributed via `branch_gap`
- `edges[]`: messages with `from`, `to`, optional `style: "dashed"` for return messages

| Parameter | Default |
|---|---|
| Participant gap | 180–220px |
| Participant width | 120–140px |
| Participant height | 40px |
| Lifeline | Dashed vertical from participant bottom |
| Activation bar width | 10–12px |
| Message arrow Y spacing | 50–60px |

Draw dashed vertical lifelines using participant center-x. Draw activation bars as thin `<rect>` on lifelines. For self-messages, construct a loop path manually. Use `svg_builder.generate_section_panel()` for alt/opt/loop frames.

---

## Concept Diagram

Central node with radial branches (1–3 levels). Nodes distributed along concentric circles via `graph_layout.distribute_along_circle()`.

- `nodes[]`: all concept nodes. Central node is level 0, branches are level 1–3.
- `edges[]`: connections from parent to child nodes.

| Parameter | Default |
|---|---|
| Center | (480, 270) |
| Level 1 radius | 160–200px |
| Level 2 radius | 280–340px |
| Central node | 110×110 (circle) or 140×50 (rounded rect) |
| Branch node | ~120×42px |

Use `routing.bezier_path()` for curved connection lines.

---

## Charts (Bar / Line / Pie)

`chart_builder` (backed by matplotlib) generates a complete PPT-styled SVG in one call.

```python
from chart_builder import render_bar_chart, render_line_chart, render_pie_chart

# Bar chart
print(render_bar_chart(['Q1','Q2','Q3','Q4'], [120,145,98,175], 'Title', ylabel='USD (k)'))

# Line chart (multi-series)
series = [{'label': 'Revenue', 'values': [120,145,98,175]}, {'label': 'Cost', 'values': [80,90,85,95]}]
print(render_line_chart(['Q1','Q2','Q3','Q4'], series, 'Title', ylabel='USD (k)'))

# Pie chart
print(render_pie_chart(['APAC','EMEA','AMER'], [35,28,37], 'Title'))
```

**Output**: Complete SVG string, no manual assembly needed.
