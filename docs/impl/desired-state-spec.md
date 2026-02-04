---
doc_revision: 2
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: impl_desired_state_spec
doc_role: implementation
doc_scope:
  - repo
  - implementation
  - feature
  - syncing
  - configuration
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
feature_id: desired_state_spec
doc_owner: maintainer
feature_kind: entailed
entailed_by:
  - core_sync_pipeline
entails:
  - desired_state_github_settings
  - desired_state_shape_maps
doc_erasure:
  - formatting
  - typos
---

# Implementation Notes: Desired-State Spec

## 0. Summary

Implement a YAML loader and validation pass for the desired-state spec. The
loader emits a normalized in-memory structure to drive plan generation.

## 1. Entailment Map

- Entailed by: `core_sync_pipeline`.
- Entails: `desired_state_github_settings`, `desired_state_shape_maps`.

## 2. Data Shapes and Structures

- Top-level keys: `version`, `provider`, `overlay` (optional), `repo`, `base_url`,
  `auth`, `desired`, `endpoints`.
- Endpoints: `name`, `method`, `url`, `compare`, `apply`.

## 3. Algorithms and Edge Cases

- Validate endpoint uniqueness.
- Require `url` to be absolute path.
- Normalize HTTP method casing.

## 4. Integration Points

- CLI `restsync spec-check` for validation.
- Plan generation consumes parsed spec.

## 5. Testing Notes

- Fixture: `configs/restsync.yml`.
- Negative tests for missing required fields.

## 6. Rollout Notes

- Keep versioned config to allow schema evolution.
