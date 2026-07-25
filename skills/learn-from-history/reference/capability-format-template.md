# Capability Format Template

Structure every extracted or abstracted capability with the following fields:

| Field | Description | Example |
|---|---|---|
| **Capability name** | Action-verb phrase in kebab-case | `deploy-hotfix`, `add-payment-method` |
| **Level** | Repo-level (single repo) or Cross-repo (orchestration across repos) | Repo-level, Cross-repo |
| **Confidence** | Tentative (1 instance) or Confirmed (2+ instances) | Tentative |
| **Objective** | One sentence describing the goal | "Deploy a critical bug fix to production safely and quickly" |
| **Trigger** | When to apply this capability | "When a critical bug is found in production" |
| **Steps** | Numbered list, each starting with an action verb. For cross-repo: reference repo-level capabilities where applicable. | `1. Branch from the latest release tag`, `2. Apply fix and open expedited PR` |
| **Parameters** | Table of what varies per instance, with type and example values | `<branch-name>`: string, e.g. `hotfix/ENG-421` |
| **Source evidence** | Where this procedure was discovered | "Slack #deployments thread, 2026-06-12" |

**For refined/abstracted capabilities**, also include:

| Field | Description |
|---|---|
| **Evolution note** | Brief note showing what was generalized and why |
| **Parameter table** | Each parameter with type, example values, and which variants introduced it |
