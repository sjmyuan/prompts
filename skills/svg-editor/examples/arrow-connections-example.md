# Example: Drawing Lines with Correct Arrow Connections

**Scenario**: The user wants to create a flowchart or architecture diagram where connection lines end with arrowheads that correctly connect to the target shape. This is one of the most common sources of visual defects — the arrow tip not aligning with the shape edge, or the arrow appearing offset from the line.

**Applies `create-flowchart` / `create-architecture-diagram` (arrow marker generation)**

---

## The Core Issue

When AI manually writes SVG arrow markers without understanding `refX`/`refY`, the default SVG values `(0, 0)` cause the line endpoint to align with the **top-left corner** of the arrow triangle, not the tip or the center of the base.

**Wrong (no refX/refY — SVG default):**
```xml
<marker id="arrow" orient="auto" markerUnits="strokeWidth">
  <path d="M 0 0 L 10 5 L 0 10 z" fill="#555"/>
</marker>
```
→ Line connects to `(0, 0)` — top corner of base. Arrow appears disconnected/offset.

**Correct (refX at tip, refY at vertical center):**
```xml
<marker id="arrow" refX="10" refY="5" orient="auto" markerUnits="strokeWidth">
  <path d="M 0 0 L 10 5 L 0 10 z" fill="#555"/>
</marker>
```
→ Line endpoint connects to arrow **tip** `(10, 5)`. Arrow tip touches the target shape edge.

---

## Expected Input

User asks: "Create a simple flowchart: Start → Process → End"

## Expected Output

The agent MUST use `svg_builder.generate_arrow_marker()` which produces correct `refX`/`refY`. The agent must NOT write arrow markers manually.

### Step-by-step correct approach:

**1. Generate the arrow marker definition (in `<defs>`):**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from svg_builder import generate_arrow_marker
print(generate_arrow_marker('arrow', '#555555'))
"
```

This produces:
```xml
<marker id="arrow" markerHeight="10.0" markerUnits="strokeWidth" markerWidth="10.0" orient="auto" refX="10.0" refY="5.0" viewBox="0 0 10.0 10.0">
  <path d="M 0 0 L 10.0 5.0 L 0 10.0 z" fill="#555555" />
</marker>
```

**2. Compute connection endpoints on shape edges:**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from routing import connection_endpoints
from geometry import connection_point, center

# Source shape: process node 'Start' at (100, 140, 130, 48)
# Target shape: process node 'Process' at (100, 318, 130, 48)
src = (100, 140, 130, 48)
dst = (100, 318, 130, 48)

src_pt, dst_pt, src_side, dst_side = connection_endpoints(src, dst, 'top-to-bottom')
print(f'src_pt={src_pt}  src_side={src_side}')
print(f'dst_pt={dst_pt}  dst_side={dst_side}')
# Output: src_pt=(165.0, 188.0)  src_side=bottom
#         dst_pt=(165.0, 318.0)  dst_side=top
"
```

**3. Route the path:**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from routing import orthogonal_path, path_to_svg_d

src_pt = (165.0, 188.0)
dst_pt = (165.0, 318.0)
waypoints = orthogonal_path(src_pt, dst_pt, 'bottom', 'top')
print(path_to_svg_d(waypoints))
# Output: M 165.0 188.0 L 165.0 318.0
"
```

**4. Generate edge SVG with marker reference:**
```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from svg_builder import generate_edge_svg
print(generate_edge_svg('e1', 'M 165.0 188.0 L 165.0 318.0'))
"
```

### Visual Verification

With `refX="10.0" refY="5.0"` and `markerUnits="strokeWidth"`:

```
    ┌──────────┐
    │  Start   │  y=140
    │          │
    └────┬─────┘  y=188  ← src_pt (bottom edge center)
         │              ← line starts here
         │              ← vertical line going down
         │
    ┌────▼─────┐  y=318  ← dst_pt (top edge center)
    │ Process  │         ← arrow TIP is exactly here (refX=10 aligns tip with line end)
    │          │         ← arrow triangle extends UPWARD (backward along the line)
    └──────────┘
```

The arrow tip is at `y=318` — exactly on the top edge of the "Process" shape. The arrowhead body extends upward into the gap between shapes, covering the line.

### How orient="auto" Handles Different Directions

The same marker definition works for ALL line directions because `orient="auto"` rotates the marker:

| Line path | Marker rotation | Arrow points | refX direction | Arrow tip at |
|---|---|---|---|---|
| `M ... L 200 100` (right) | 0° | → right | rightward | x=200 |
| `M ... L 165 318` (down) | 90° CW | ↓ down | downward | y=318 |
| `M ... L 80 200` (left) | 180° | ← left | leftward | x=80 |
| `M ... L 165 80` (up) | 270° CW | ↑ up | upward | y=80 |

---

## Common Mistakes to Avoid

1. **Writing arrow markers manually without refX/refY** — ALWAYS use `svg_builder.generate_arrow_marker()`
2. **Setting refX=0 without refY** — connects to top corner, not center of base
3. **Setting refX=0, refY=half_h without understanding direction** — the base connects to the line end but the tip extends forward; this is only appropriate for specific cases (use `tip_ref=False`)
4. **Forgetting markerUnits="strokeWidth"** — without it, the arrow size is in user units and may not scale with stroke width
5. **Computing endpoint inside the shape instead of on its edge** — `connection_endpoints()` returns points ON the shape edge; the arrow tip must be at the edge, not inside the shape

## The Two Arrow Modes

| Mode | Function call | refX/refY | When to use |
|---|---|---|---|
| **Tip-ref** (default, recommended) | `generate_arrow_marker(tip_ref=True)` | `refX=arrow_width, refY=half_h` | Arrow tip touches target shape edge — standard for flowcharts, architecture diagrams |
| **Base-ref** | `generate_arrow_marker(tip_ref=False)` or `generate_arrow_marker_reverse()` | `refX=0, refY=half_h` | Line ends at base, arrow tip extends forward — rare; when line should visibly stop before target |
