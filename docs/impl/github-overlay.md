---
doc_revision: 2
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
  README.md: 18
  CONTRIBUTING.md: 18
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
- Rulesets: branch/tag rulesets with explicit ref-name patterns, enforcement,
  and rule definitions (e.g., required PRs, required status checks, force-push
  and deletion blocks).

## 3. Algorithms and Edge Cases

- Treat missing fields as drift only if explicitly configured.
- Compare allow-list entries as sets with stable ordering.
- Accept two valid branch-protection postures for `next`/`release`:
  org repos with actor-restricted rulesets, or personal repos with
  non-fast-forward/deletion blocks plus workflow guardrails.

## 4. Integration Points

- Load allow-list from `docs/allowed_actions.txt`.
- Validate plan before apply; emit refusal diagnostics.
- Validate branch/tag rulesets against gabion’s branching model (see
  `../gabion/README.md` and `../gabion/CONTRIBUTING.md`).

## 5. Testing Notes

- Use recorded GitHub API responses as fixtures.
- Assert refusals for unsafe permission changes.
- Include fixtures for branch/tag rulesets and mirror workflows (`mirror-next`,
  `promote-release`) to ensure overlay accepts the expected automation posture.

## 6. Rollout Notes

- Use read-only plan mode in CI.
- Apply locally with explicit token and confirmation.
