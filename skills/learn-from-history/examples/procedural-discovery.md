# Example: Procedural Pattern Extraction and Abstraction

**Applies**: `detect-learning-signals` → `extract-and-refine-capability` → `provision-lessons`

And later: `detect-learning-signals` → `extract-and-refine-capability` (refine phase) → `provision-lessons`

**Scenario**: A user provides Slack transcripts from the #deployments channel. The AI finds a step-by-step procedure for deploying hotfixes that was described by a senior engineer but never documented. Later, another Slack thread reveals a similar procedure for deploying regular releases — the AI abstracts both into a general deployment capability.

---

## Input (Slack Transcript — First Session)

```
#deployments channel, thread from 2026-06-12:

Alice (senior engineer):
  @here Quick reminder on the hotfix procedure since we had some confusion today:

  1. Always branch from the latest release tag, not main — use `git checkout -b hotfix/ISSUE-ID v2.3.1`
  2. After fixing, open a PR against main and ping the on-call person for expedited review
  3. Once merged, tag immediately: `git tag -a v2.3.2-hotfix1 -m "Hotfix for ENG-421"`
  4. The CI pipeline picks up the tag automatically and deploys to prod
  5. Stay in #alerts for 15 min after deploy to catch any fallout

  This is the protocol we agreed on last quarter but I realize we never wrote it down.

Bob (new team member):
  Thanks! I was about to merge directly to main. Is step 5 really necessary for every hotfix?

Alice:
  Yes, every time. We learned that the hard way after the v2.1 incident.

---

User says: "Learn from this Slack transcript and save what's worth keeping."
```

---

## Step 1: detect-learning-signals

**Source type**: Communication tool history → delegate to **analyze-communication-history**

### detect-learning-signals → analyze-communication-history

**Signal detected**: Procedural pattern — Alice describes a numbered sequence of steps for deploying a hotfix, with explicit language ("always", "the protocol we agreed on") indicating this is a team convention.

**Signal type**: Procedural pattern (signal #12)

**Signal strength**: High — 5 concrete steps, multiple team members confirming it's the agreed protocol, explicit statement that it was never written down.

### Quality gate evaluation:

| Dimension | Verdict | Reasoning |
|---|---|---|
| Reusability | ✅ Pass | Every hotfix follows this procedure; applies to all team members |
| Non-obviousness | ✅ Pass | A newcomer (Bob) was about to do it wrong; the steps are team-specific conventions |
| Actionability | ✅ Pass | 5 concrete, ordered steps anyone can follow |
| Non-duplication | ✅ Pass | Alice explicitly says "we never wrote it down" — confirmed absent from context |
| Specificity | ✅ Pass | Specific enough to follow step-by-step; general enough to apply to any hotfix |

**Verdict**: ACCEPT — but this is a multi-step procedure, not a single rule or fact. Route to **extract-capability**.

---

## Step 2: extract-capability

### Identify the procedure
Alice's message is a numbered, ordered list of 5 steps with imperative language ("always branch", "ping the on-call person", "stay in #alerts").

### Scope the task
- **Goal**: Deploy a critical fix to production following the team's hotfix protocol
- **Trigger**: A critical bug needs to be fixed in production
- **Audience**: Any developer on the team, especially newcomers

### Extract ordered steps
1. Branch from the latest release tag (not main): `git checkout -b hotfix/<issue-id> <release-tag>`
2. Fix, commit with `hotfix:` prefix, open PR against main, ping on-call for expedited review
3. After approval and merge, tag immediately: `git tag -a v<version>-hotfix<seq> -m "Hotfix for <issue-id>"`
4. CI pipeline auto-deploys the tag to production
5. Monitor #alerts channel for 15 minutes post-deploy

### Identify parameters

| What varies | Parameter | Example |
|---|---|---|
| Issue identifier | `<issue-id>` | `ENG-421` |
| Latest release tag | `<release-tag>` | `v2.3.1` |
| New version after hotfix | `<version>` | `2.3.2` |
| Hotfix sequence number | `<seq>` | `1` |

Constants: always branch from release tag (not main), always ping on-call, always monitor for 15 min, always tag after merge.

### Capability quality checks
- **Reusable**: ✅ Every hotfix follows these steps
- **Non-obvious**: ✅ Newcomers don't know to branch from tags or monitor #alerts
- **Complete**: ✅ Someone can follow these steps end-to-end
- **Team-specific**: ✅ Encodes this team's specific protocol (tag naming, #alerts channel, on-call ping)

### Formatted capability

```markdown
<deploy-hotfix>
**Objective**: Deploy a critical fix to production quickly while following the team's hotfix protocol.

**Trigger**: A critical bug needs to be patched in production.

**Steps**:
1. Create a hotfix branch from the latest release tag (not main): `git checkout -b hotfix/<issue-id> <release-tag>`
2. Apply the fix, commit with prefix `hotfix:`, push, and open a PR against `main`
3. Ping the on-call engineer for expedited review
4. After approval, merge to `main` and immediately tag: `git tag -a v<version>-hotfix<seq> -m "Hotfix for <issue-id>"`
5. The CI pipeline picks up the tag automatically and deploys to production
6. Monitor the #alerts channel for 15 minutes after deploy

**Parameters**:
| Parameter | Description | Example |
|---|---|---|
| `<issue-id>` | Bug or issue identifier | `ENG-421` |
| `<release-tag>` | Latest release tag to branch from | `v2.3.1` |
| `<version>` | New version number after the hotfix | `2.3.2` |
| `<seq>` | Hotfix sequence number for this version | `1` |

**Source**: Slack #deployments channel, Alice's protocol reminder (2026-06-12)
```

---

## Step 3: determine-provision-target

**Classification**: Multi-step procedure, team-specific, operational → project-level persistent notes (no domain skill covers deployments).

**Target**: Project conventions file, under a new "Deployment Procedures" section.

**Rationale**: This is a project-level operational procedure. There's no "deployment" domain skill to receive it. Project-level notes are the right home for team how-to guides.

---

## Step 4: generate-provision-plan

| # | Lesson Summary | Signal Type | Target File | Section | Content |
|---|---|---|---|---|---|
| 1 | Hotfix deployment protocol (5 steps + parameters) | Procedural pattern | Project conventions | Deployment Procedures → `deploy-hotfix` capability | [Formatted capability from Step 2] |

**Plan approved by user. Capability provisioned to project notes.**

---

## Second Session — Abstraction

One month later, the user provides another Slack transcript:

```
#deployments channel, thread from 2026-07-15:

Charlie (new team member):
  Hey, what's the process for deploying a regular (non-hotfix) release?
  I have ENG-512 ready to go.

Alice:
  Almost the same as hotfix, but:
  1. Branch from main, not a release tag
  2. After PR approval, don't merge directly — squash-merge to main
  3. Tag with just the version: `git tag -a v<version> -m "Release <version>"`
  4. No need to monitor #alerts for regular releases
  5. Everything else is the same — CI picks up the tag and deploys

User says: "Learn from this too and update the deployment docs."
```

---

## Step 5: detect-learning-signals (second session)

**Signal detected**: Procedural pattern — Charlie asks for a procedure, Alice describes it by referencing and differing from the hotfix procedure ("almost the same as hotfix, but…").

**Signal type**: Procedural pattern (signal #12)

**Quality gate**: PASSES all dimensions.

---

## Step 6: extract-capability (second session)

### Identify the procedure
5 steps, described in relation to the existing hotfix procedure.

### Scope the task
- **Goal**: Deploy a regular release following the team's protocol
- **Differs from hotfix in**: branch source (main vs. release tag), merge type (squash-merge vs. regular merge), tag format (no `-hotfix` suffix), no alert monitoring

### Formatted capability (concrete version)

```markdown
<deploy-release>
**Objective**: Deploy a regular (non-hotfix) release to production.

**Trigger**: A feature or fix is ready to ship.

**Steps**:
1. Branch from `main`: `git checkout -b feature/<issue-id>`
2. After PR approval, squash-merge to `main`
3. Tag with version: `git tag -a v<version> -m "Release <version>"`
4. CI pipeline auto-deploys the tag to production
5. No alert monitoring required for regular releases

**Parameters**:
| Parameter | Description | Example |
|---|---|---|
| `<issue-id>` | Issue identifier | `ENG-512` |
| `<version>` | New version number | `2.4.0` |

**Source**: Slack #deployments channel, Alice answering Charlie (2026-07-15)
```

But this overlaps heavily with the existing `<deploy-hotfix>` capability in project notes.

---

## Step 7: abstract-capability

Rule triggers: "When a candidate capability overlaps with an existing capability → apply **abstract-capability**"

### Load existing context
Read project conventions → find existing `<deploy-hotfix>` capability.

### Compare existing vs. new

| Aspect | deploy-hotfix (existing) | deploy-release (new) |
|---|---|---|
| Branch source | Latest release tag | `main` |
| Merge type | Regular merge | Squash-merge |
| Tag format | `v<version>-hotfix<seq>` | `v<version>` |
| Alert monitoring | 15 min in #alerts | None required |
| CI deploy | Auto from tag | Auto from tag |
| PR review | Expedited (ping on-call) | Standard |
| Commit prefix | `hotfix:` | (none specified) |

### Identify the abstraction
The core flow is identical: branch → PR → merge → tag → CI deploys.
What varies: branch source, merge type, tag format, review urgency, monitoring requirement, commit prefix.

### Produce the refined capability

```markdown
<deploy-to-production>
**Objective**: Deploy code to production following the team's deployment protocol, handling both hotfixes and regular releases through a unified procedure.

**Trigger**: Code is ready to ship — either a regular release or a critical hotfix.

**Steps**:
1. Create a branch from the appropriate source: `<branch-source>`
2. Commit with the appropriate prefix: `<commit-prefix>`
3. Open a PR against `main` and request review: `<review-type>`
4. After approval, merge using `<merge-type>`
5. Tag with `<tag-format>` — CI pipeline auto-deploys to production
6. If `<monitoring-required>`, monitor `<monitoring-channel>` for `<monitoring-duration>`

**Parameters**:
| Parameter | Hotfix value | Regular release value | Description |
|---|---|---|---|
| `<branch-source>` | Latest release tag (e.g., `v2.3.1`) | `main` | Where to branch from |
| `<commit-prefix>` | `hotfix:` | (feature-specific) | Commit message prefix |
| `<review-type>` | Expedited (ping on-call in Slack) | Standard PR review | How urgently review is needed |
| `<merge-type>` | Regular merge | Squash-merge | How to merge the PR |
| `<tag-format>` | `v<version>-hotfix<seq>` | `v<version>` | Git tag naming convention |
| `<monitoring-required>` | Yes | No | Whether to monitor post-deploy |
| `<monitoring-channel>` | #alerts | N/A | Which channel to monitor |
| `<monitoring-duration>` | 15 minutes | N/A | How long to monitor |

**Evolution note**: Merged `<deploy-hotfix>` (from Slack #deployments 2026-06-12) with `<deploy-release>` (from Slack #deployments 2026-07-15). The core flow (branch → PR → merge → tag → CI deploy) is identical across both. Parameterized the 6 points of variance: branch source, commit prefix, review type, merge type, tag format, and monitoring. This abstraction covers all current deployment scenarios and can accommodate future variants by adding parameter values.
```

### Validate the abstraction
- Can a newcomer derive the hotfix procedure? ✅ — fill in hotfix column
- Can they derive the regular release procedure? ✅ — fill in regular release column
- Is anything lost? No — the parameter table preserves all concrete values

---

## Step 8: determine-provision-target

**Classification**: Refined capability replacing an existing one → same target as the original.

**Target**: Project conventions file, "Deployment Procedures" section — **replace** `<deploy-hotfix>` with `<deploy-to-production>`.

---

## Step 9: generate-provision-plan

| # | Lesson Summary | Signal Type | Target File | Section | Content |
|---|---|---|---|---|---|
| 1 | Abstract `deploy-hotfix` + `deploy-release` into unified `deploy-to-production` | Procedural pattern (abstracted) | Project conventions | Deployment Procedures (replace existing) | [Refined capability from Step 7] |

**Plan approved. Old capability replaced with abstracted version.**
