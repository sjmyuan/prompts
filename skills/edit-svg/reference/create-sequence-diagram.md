# Sequence Diagram — Visual Pattern & Dimensions

Applies **create-scripted-diagram** in the edit-svg skill.

## Layout Pattern

Participants arranged horizontally at the top, messages flow chronologically downward. Each participant has a dashed vertical lifeline.

## Data Structure

- `nodes[]`: participants with `type: "process"`, `row: 0`, distributed horizontally via `branch_gap`.
- `edges[]`: messages with `from`, `to`, optional `style: "dashed"` for return messages.

## Dimension Guidelines

| Parameter | Default |
|---|---|
| Participant gap | 180–220px |
| Participant width | 120–140px |
| Participant height | 40px |
| Lifeline | Dashed vertical from participant bottom |
| Activation bar width | 10–12px |
| Message arrow Y spacing | 50–60px between messages |

## Key Additions

- Draw dashed vertical lifelines using participant center-x from script output.
- Draw activation bars: thin `<rect>` on lifelines using `PPT_PALETTE["blue_fill_end"]`.
- For self-messages, construct a loop path manually.
- Use `svg_builder.generate_section_panel()` for alt/opt/loop frames.
