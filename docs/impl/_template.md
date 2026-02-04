---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: impl_template
doc_role: implementation
doc_scope:
  - repo
  - implementation
  - feature
doc_authority: informative
doc_requires:
  - README.md
  - CONTRIBUTING.md
  - POLICY_SEED.md
  - glossary.md
doc_reviewed_as_of:
  README.md: 16
  CONTRIBUTING.md: 16
  POLICY_SEED.md: 1
  glossary.md: 1
doc_change_protocol: "POLICY_SEED.md §6"
feature_id: feature_slug
doc_owner: maintainer
feature_kind: green
entailed_by: []
entails: []
doc_erasure:
  - formatting
  - typos
---

# Implementation Notes: <feature name>

## 0. Summary

Brief description of the implementation approach and why it matches the design.

## 1. Entailment Map

- Upstream features that entail this one
- Downstream features entailed by this one

## 2. Data Shapes and Structures

- Config schemas
- Plan JSON schema notes
- Canonicalization helpers

## 3. Algorithms and Edge Cases

- Diff logic quirks
- Ordering guarantees
- Error handling strategy

## 4. Integration Points

- CLI entrypoints
- Overlay hooks
- External dependencies

## 5. Testing Notes

- Fixture locations
- Tests added/updated
- Known gaps (tracked in checklist)

## 6. Rollout Notes

- Migration steps
- Backward compatibility
- Ops considerations
