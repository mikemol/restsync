---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: design_core_sync_pipeline
doc_role: design
doc_scope:
  - repo
  - design
  - feature
  - syncing
doc_authority: informative
doc_requires:
  - README.md
  - CONTRIBUTING.md
  - POLICY_SEED.md
  - glossary.md
doc_reviewed_as_of:
  README.md: 10
  CONTRIBUTING.md: 10
  POLICY_SEED.md: 1
  glossary.md: 1
doc_change_protocol: "POLICY_SEED.md §6"
feature_id: core_sync_pipeline
doc_owner: maintainer
feature_kind: green
entailed_by: []
entails:
  - core_canonical_snapshot
  - core_shape_map
  - core_deterministic_diff
  - plan_schema
  - apply_gate
doc_erasure:
  - formatting
  - typos
---

# Feature Design: Core Sync Pipeline

## 0. Thesis

Define a deterministic, REST-agnostic pipeline that fetches live state,
canonicalizes it, computes drift, and emits a stable plan. The pipeline is the
foundation for overlays and dogfooding, while keeping apply explicit and local.

## 1. Scope

- Fetch live resources from configured endpoints.
- Canonicalize and project fields using shape maps.
- Compute drift as symmetric differences.
- Emit a stable, reviewable plan.

Out of scope:
- Provider-specific semantics (overlay responsibility).
- Automatic apply or CI writes (forbidden by policy).

## 2. Invariants and Contracts

- `POLICY_SEED.md` Prime Invariant (§1) and Apply Safety Invariant (§1.2).
- `glossary.md`: Canonicalization, Drift, Plan, Apply, Core/Overlay boundary.

## 3. Desired-State Semantics

Desired state is defined by local YAML/JSON files plus a shape map. Identity is
canonicalized; ordering and irrelevant fields are erased.

## 4. Plan/Apply Semantics

- Plan must be deterministic and fully derived from canonical inputs.
- Apply is gated, local, and explicit (`restsync apply --confirm`). CI never writes.
- Plan must include enough context to justify overlay refusals.

## 5. API/Endpoint Surface

- Endpoints are defined in the desired-state spec (base URL + paths).
- The core treats responses as JSON shapes only.

## 6. Risks and Tradeoffs

- API drift can cause plan churn; shape maps must be stable.
- Overly aggressive projection can hide unsafe drift.
- Canonicalization bugs can create false diffs.

## 7. Test Evidence

- Canonicalization idempotence (canon(canon(x)) == canon(x)).
- Drift symmetry and stability.
- Stable plan ordering for identical inputs.

## 8. Rollout

- Dogfood against restsync GitHub settings in read-only plan mode.
- Add CI read-only plan generation; apply only locally.
