# Plan Input Schema

A plan consumed by this skill consists of numbered steps. Each step must have:
- **Step number**: Sequential integer starting from 1
- **Title**: Short descriptive name of the step
- **Objective**: What the step achieves

The plan may be provided as:
- An existing `plan.md` file in a feature folder (created by **export-plan** in plan-development-task, an **orchestrate-feature-delivery** cell folder, or a previous execution)
- A plan summarized in the conversation by plan-development-task
- A plan described ad-hoc by the user

This skill is responsible for materializing the plan into `plan.md` with the **step-tracking-format** if it does not already exist as a file.
