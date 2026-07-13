# Architecture Diagram — Visual Pattern & Dimensions

Applies **create-scripted-diagram** in the edit-svg skill.

## Layout Pattern

Horizontal tier layers stacked top-to-bottom. Each tier has a colored header band and a subtle background panel.

| Tier | Purpose | Example |
|---|---|---|
| Top (row 0) | Client/Presentation | Browser, Mobile App |
| Upper-mid (row 1) | Edge/Gateway | CDN, Load Balancer, API Gateway |
| Lower-mid (row 2) | Application/Services | Auth Service, Business Logic |
| Bottom (row 3) | Data/Storage | PostgreSQL, Redis Cache |

## Dimension Guidelines

| Parameter | Default |
|---|---|
| Tier gap (vertical) | 160–200px |
| Component gap (horizontal) | 60–100px |
| Service box | `process` type, ~160×50px |
| Database box | `data` type, ~140×60px |
| Tier band height | panel height + 30px padding |
| Tier band `rx` | 6 |

## Key Additions

- Draw subtle background `<rect>` for each layer band using `PPT_PALETTE["bg_panel"]`.
- Use `svg_builder.generate_section_panel()` for layer backgrounds.
