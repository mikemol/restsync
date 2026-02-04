---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: impl_github_overlay
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
  README.md: 4
  CONTRIBUTING.md: 4
  POLICY_SEED.md: 1
  glossary.md: 1
doc_change_protocol: "POLICY_SEED.md §6"
feature_id: github_overlay
doc_owner: maintainer
feature_kind: entailed
entailed_by:
  - overlay_model
entails:
  - github_actions_settings
  - github_branch_rulesets
  - github_tag_rulesets
doc_erasure:
  - formatting
  - typos
---

# Implementation Notes: GitHub Overlay

## 0. Summary

Implement a GitHub overlay that validates plan diffs against repo governance
rules, focusing on Actions settings and rulesets first.

## 1. Entailment Map

- Entailed by: `overlay_model`.
- Entails: `github_actions_settings`, `github_branch_rulesets`, `github_tag_rulesets`.

## 2. Data Shapes and Structures

- Overlay config: GitHub owner/repo, endpoints, allow-list path.
- Actions settings: allowed_actions, default_workflow_permissions,
  can_approve_pull_request_reviews.

## 3. Algorithms and Edge Cases

- Treat missing fields as drift only if explicitly configured.
- Compare allow-list entries as sets with stable ordering.

## 4. Integration Points

- Load allow-list from `docs/allowed_actions.txt`.
- Validate plan before apply; emit refusal diagnostics.

## 5. Testing Notes

- Use recorded GitHub API responses as fixtures.
- Assert refusals for unsafe permission changes.

## 6. Rollout Notes

- Use read-only plan mode in CI.
- Apply locally with explicit token and confirmation.
