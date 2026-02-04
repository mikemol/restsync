---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: design_desired_state_spec
doc_role: design
doc_scope:
  - repo
  - design
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
  README.md: 4
  CONTRIBUTING.md: 4
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

# Feature Design: Desired-State Spec

## 0. Thesis

Define a stable, reviewable YAML spec that encodes desired state, endpoints,
shape maps, and apply mappings. The spec must be explicit enough to support
canonicalization, drift detection, and overlay validation.

## 1. Scope

- Config versioning and provider selection.
- Repo identity and base URL.
- Desired state for each endpoint.
- Shape maps for comparison.
- Apply mappings (method/url/body source).

Out of scope:
- Provider-specific invariants (overlay responsibility).

## 2. Invariants and Contracts

- `glossary.md`: Desired State, Shape Map, Canonicalization, Plan, Apply.
- `POLICY_SEED.md`: Apply is local and explicit.

## 3. Semantics

- Identity is defined by canonicalization of the desired values.
- Missing values are not equivalent to explicit null unless stated.
- Shape map projection is explicit; no implicit ignores.

## 4. Plan/Apply Semantics

- Plan must include `want`/`have` pairs derived from desired vs live.
- Apply uses `body_from` referencing desired state.

## 5. Risks and Tradeoffs

- Overly permissive spec fields can mask drift.
- Schema drift can break dogfood runs.

## 6. Test Evidence

- Schema validation tests.
- Canonicalization idempotence for desired state.

## 7. Rollout

- Seed with GitHub Actions settings for this repo.
