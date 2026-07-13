# Concept Diagram — Visual Pattern & Dimensions

Applies **create-scripted-diagram** in the edit-svg skill.

## Layout Pattern

Central node with radial branches (1–3 levels). Nodes distributed along concentric circles using `graph_layout.distribute_along_circle()`.

## Data Structure

- `nodes[]`: all concept nodes with `id`, `type`, `text`. Central node is level 0, branches are level 1–3.
- `edges[]`: connections from parent to child nodes.

## Dimension Guidelines

| Parameter | Default |
|---|---|
| Center | (480, 270) |
| Level 1 radius | 160–200px |
| Level 2 radius | 280–340px |
| Central node size | 110×110 (circle) or 140×50 (rounded rect) |
| Branch node size | ~120×42px |

## Script Snippet

```bash
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from graph_layout import distribute_along_circle
from svg_builder import get_shape_dimensions
center = (480, 270)
radius = 180
branch_count = 5
positions = distribute_along_circle(center, radius, branch_count)
for i, (px, py) in enumerate(positions):
    dims = get_shape_dimensions(f'Node {i+1}', 'process', ppt_mode=True)
    print(f'x={px - dims[\"width\"]/2:.0f} y={py - dims[\"height\"]/2:.0f} w={dims[\"width\"]:.0f} h={dims[\"height\"]:.0f}')
"
```

Use `routing.bezier_path()` for curved connection lines.
