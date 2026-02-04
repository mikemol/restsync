---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: design_github_overlay
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
  README.md: 8
  CONTRIBUTING.md: 8
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

# Feature Design: GitHub Overlay

## 0. Thesis

Provide a GitHub-specific overlay that enforces repo governance invariants and
refuses unsafe plans. The overlay makes restsync safe to dogfood against this
repository’s configuration.

## 1. Scope

- GitHub Actions settings and allow-lists.
- Branch rulesets for `main`, `stage`, `next`, `release`.
- Tag rulesets for `v*` and `test-v*`.

Out of scope:
- Issue/project settings not tied to policy.
- Non-GitHub providers.

## 2. Invariants and Contracts

- `POLICY_SEED.md` execution constraints and allow-listed actions.
- `glossary.md` Core/Overlay boundary and Apply semantics.
- `docs/allowed_actions.txt` as the allow-list source.

## 3. Desired-State Semantics

Desired state is a YAML spec with GitHub endpoints and shape maps for:
- Actions permissions and workflow defaults.
- Rulesets (branch + tag) with explicit include/exclude criteria.

## 4. Plan/Apply Semantics

- Overlay refuses plans that weaken allow-lists or permissions.
- Overlay refuses changes that violate branch/tag protections.
- Apply remains local and explicit.

## 5. API/Endpoint Surface

Expected GitHub endpoints (subject to API availability):
- `GET/PUT /repos/{owner}/{repo}/actions/permissions`
- `GET/PUT /repos/{owner}/{repo}/actions/permissions/workflow`
- Rulesets APIs for branch/tag protections

## 6. Risks and Tradeoffs

- GitHub API drift or missing endpoints.
- Personal repo limitations on actor-restricted rulesets.

## 7. Test Evidence

- Fixture-based tests for actions permissions diffs.
- Overlay refusal when permissions drift from policy.

## 8. Rollout

- Start in read-only plan mode in CI.
- Apply locally after manual review.
