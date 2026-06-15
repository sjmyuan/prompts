# Create Sequence Diagram — Detailed Steps

Applies **create-sequence-diagram** in the svg-editor skill.

**Steps**:
1. **Identify participants and messages**: List all actors/components and the messages exchanged between them in chronological order. Note synchronous vs. asynchronous and return messages.
2. **Build JSON for compute_all.py**: Use `diagram_type: "sequence"`. Define participants as `nodes[]` with `type: "process"` and `row: 0`. Define messages as `edges[]` with `from`, `to`, `label`, and optional `style: "dashed"` for return messages.
3. **Run compute_all.py**: Execute `python3 scripts/compute_all.py '<json>'`. The script handles participant spacing, lifeline positioning, and message path computation.
4. **Review validation**: Check `validation.all_clear`.
5. **Assemble SVG**: Use the script's SVG fragments. Additionally:
   - Draw dashed vertical lifelines from each participant box: `<line x1="..." y1="..." x2="..." y2="..." stroke-dasharray="4,4" stroke="#9AA0A6"/>`
   - Draw activation bars: thin `<rect>` on lifelines spanning message activity duration, using `PPT_PALETTE["blue_fill_end"]`.
   - For self-messages (same participant sending to itself), construct a loop path manually.
   - Use `svg_shapes.generate_section_panel()` for alt/opt/loop frames if needed.
6. **Output**: Return raw, valid SVG code.
