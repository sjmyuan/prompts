# Example: Resolving the Base Root on a Multi-Root Workspace

**Scenario**: A user requests a spike in a multi-root workspace holding a code repo (`payments/`) and a docs repo (`company-docs/`) that already has one spike folder. No location is named. The distinct point: discovery finds a sole convention winner, auto-selects it, records it, and the later delivery inherits the base without re-searching.

**Applies**: `resolve-root`

## Input

> "Spike how we migrate order-service off the legacy payment gateway."

## Phase 1 — discovery and auto-select

`resolve-root` step 3 enumerates workspace roots:

- `payments/` — code under investigation; no decision folders → code-repo anchor, no signal.
- `company-docs/` — contains `spikes/pricing-revamp/` → **tier 1 convention signal**.

Step 4 keeps tier 1 only: one candidate. Step 5 auto-selects and states the assumption:

> Placing the new spike next to the existing `spikes/` sibling at `company-docs/`.

Step 6 returns base = `/workspace/company-docs`; the spike folder becomes `company-docs/spikes/order-service-migration/`. Step 7 confirms it is not excluded and is creatable.

## Phase 1 output — durable record

The caller writes `scope.md` with the base at the top:

```markdown
# Scope: order-service-migration
Artifact root: /workspace/company-docs

## Areas
...
```

## Phase 2 — delivery inherits (no re-search)

Later the user says:

> "The spike is done. Decompose it into features."

`produce-delivery-index` reads `scope.md` `Artifact root:` → base `/workspace/company-docs` → the index is written to `company-docs/deliveries/order-service-migration/index.md` and plan folders under `deliveries/order-service-migration/{repo}/{feature}/`. No resolve call, no re-ask — delivery sits next to the spike by construction.

## Phase 3 — greenfield asks without a default

A fresh spike starts in a single-repo workspace with no docs folder, no declared home, and no conventions:

- discovery finds no tier-1/2/3 candidate (tier 4 = the only root, but it is the code repo — no anchor).
- step 5 applies the greenfield rule: ask, present no default.

> "Where should the spike artifacts live? I found no existing decision-doc folder or declared docs home."

The user names `/workspace/company-docs/spikes/`; `resolve-root` returns it and the caller records it.
