# Create Sequence Diagram — Detailed Steps

Applies **create-sequence-diagram** in the svg-editor skill.

**Steps**:
1. **Identify participants and messages**: List all actors/components and the messages exchanged between them in chronological order. Note synchronous vs. asynchronous and return messages.
2. **Build node/edge data**: Define participants as `nodes[]` with `type: "process"` and `row: 0` (all on same row). Define messages as `edges[]` with `from`, `to`, `label`, and optional `style: "dashed"` for return messages.
3. **Compute participant positions**: Run the **Compute node positions** snippet. Participants will be placed horizontally across row 0. Adjust `branch_gap` to control spacing between participants (recommend: 180–220).
4. **Compute message paths**: For each edge, run the **Route a connection** snippet. Since participants are on the same row, `connection_endpoints()` will auto-detect top-to-bottom flow with horizontal message arrows.
5. **Generate SVG elements**: Run the **Generate SVG for a shape** snippet for participants and edges. Additionally:
   - Draw dashed vertical lifelines from each participant box: `<line x1="..." y1="..." x2="..." y2="..." stroke-dasharray="4,4" stroke="#9AA0A6"/>`
   - Draw activation bars: thin `<rect>` on lifelines spanning message activity duration, using `PPT_PALETTE["blue_fill_end"]`.
   - For self-messages (same participant sending to itself), construct a loop path manually.
   - Use `svg_shapes.generate_section_panel()` for alt/opt/loop frames if needed.
6. **Validate and compute viewBox**: Run overlap check and viewBox snippets.
7. **Assemble SVG**: Follow the **SVG assembly pattern** in `<computation-snippets>`.
8. **Output**: Return raw, valid SVG code.
