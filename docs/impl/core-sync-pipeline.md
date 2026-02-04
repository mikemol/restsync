---
doc_revision: 2
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: impl_core_sync_pipeline
doc_role: implementation
doc_scope:
  - repo
  - implementation
  - feature
  - syncing
doc_authority: informative
doc_requires:
  - README.md
  - CONTRIBUTING.md
  - POLICY_SEED.md
  - glossary.md
doc_reviewed_as_of:
  README.md: 18
  CONTRIBUTING.md: 18
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

# Implementation Notes: Core Sync Pipeline

## 0. Summary

Implement a deterministic pipeline that materializes snapshots from REST
endpoints, canonicalizes them, computes drift, and emits a stable plan. The
pipeline is REST-agnostic and delegates semantics to overlays.

## 1. Entailment Map

- Entails: `core_canonical_snapshot`, `core_shape_map`, `core_deterministic_diff`,
  `plan_schema`, `apply_gate`.

## 2. Data Shapes and Structures

- Desired-state spec: YAML with `endpoints[]`, `compare`, `apply` sections.
- Canonical snapshots: JSON with ordered lists and filtered fields.
- Plan schema: stable JSON with `want`/`have` pairs per diff.

## 3. Algorithms and Edge Cases

- Canonicalize with stable ordering, explicit include/ignore lists.
- Diff is symmetric and retains directionality in the plan.
- Treat absent optional fields consistently (null vs missing).

## 4. Integration Points

- CLI commands: `snapshot`, `plan`, `apply`.
- Overlay hook: `overlay.validate(plan, context)` before apply.
- Apply path: `restsync apply --confirm` uses plan + apply spec to write changes.
- Snapshot path: `restsync snapshot` emits canonical `have` per endpoint.

## 5. Testing Notes

- Fixtures: recorded REST responses under `tests/fixtures/`.
- Tests: canonicalization idempotence, drift symmetry, stable plan ordering.

## 6. Rollout Notes

- Start with read-only plan in CI.
- Apply is local only and requires explicit confirmation.
