---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: impl_overlay_model
doc_role: implementation
doc_scope:
  - repo
  - implementation
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
  README.md: 9
  CONTRIBUTING.md: 9
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

# Implementation Notes: Overlay Model

## 0. Summary

Define a minimal overlay interface that can validate and refuse plans while
preserving the core pipeline and plan determinism.

## 1. Entailment Map

- Entails: `overlay_refusal_rules`, `github_overlay`.

## 2. Data Shapes and Structures

- Overlay registration: name + module path + config section.
- Validation signature: `validate(plan, context) -> violations`.

## 3. Algorithms and Edge Cases

- Rule ordering must be stable for reproducible diagnostics.
- Violations must include enough context to explain refusal.

## 4. Integration Points

- CLI invokes overlay validation after plan generation.
- Apply is blocked if any overlay violations are present.

## 5. Testing Notes

- Unit tests for refusal rules.
- Integration tests for overlay registration and invocation.

## 6. Rollout Notes

- Ship with a GitHub overlay as the first implementation.
