---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: design_overlay_model
doc_role: design
doc_scope:
  - repo
  - design
  - feature
  - syncing
  - governance
doc_authority: informative
doc_requires:
  - README.md
  - CONTRIBUTING.md
  - POLICY_SEED.md
  - glossary.md
doc_reviewed_as_of:
  README.md: 4
  CONTRIBUTING.md: 4
  POLICY_SEED.md: 1
  glossary.md: 1
doc_change_protocol: "POLICY_SEED.md §6"
feature_id: overlay_model
doc_owner: maintainer
feature_kind: green
entailed_by: []
entails:
  - overlay_refusal_rules
  - github_overlay
doc_erasure:
  - formatting
  - typos
---

# Feature Design: Overlay Model

## 0. Thesis

Overlays encode provider-specific meaning and invariants on top of a generic
REST sync core. They must be able to refuse unsafe plans without mutating core
inputs or outputs.

## 1. Scope

- Define overlay interface and validation lifecycle.
- Allow overlays to constrain or refuse plans.
- Preserve the core/overlay boundary.

Out of scope:
- Provider-specific endpoint logic in the core.

## 2. Invariants and Contracts

- `POLICY_SEED.md` Core/Overlay Invariant (§1.1).
- `glossary.md` Overlay and Core definitions.
- Apply is explicit and local; overlays never apply directly.

## 3. Desired-State Semantics

Overlays may interpret desired-state metadata but must not modify canonical
snapshots or core diffs.

## 4. Plan/Apply Semantics

- Overlays receive a plan and context.
- Overlays may refuse plans with explicit diagnostics.
- Overlays must not expand or mutate the plan.

## 5. API/Endpoint Surface

Overlays do not issue HTTP requests directly; they operate on core outputs and
configuration metadata.

## 6. Risks and Tradeoffs

- Over-tight constraints can block legitimate changes.
- Under-specified overlays allow unsafe drift.

## 7. Test Evidence

- Refusal rules fire correctly on unsafe plans.
- Overlay invariants commute with canonicalization.

## 8. Rollout

- Implement overlay interface with a GitHub overlay first.
