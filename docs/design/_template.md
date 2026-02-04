---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: design_template
doc_role: design
doc_scope:
  - repo
  - design
  - feature
doc_authority: informative
doc_requires:
  - README.md
  - CONTRIBUTING.md
  - POLICY_SEED.md
  - glossary.md
doc_reviewed_as_of:
  README.md: 15
  CONTRIBUTING.md: 15
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

# Feature Design: <feature name>

## 0. Thesis

One-paragraph statement of intent and why this feature exists.

## 1. Scope

- In-scope behavior
- Out-of-scope behavior

## 2. Invariants and Contracts

- Policy invariants that apply (cite `POLICY_SEED.md` sections)
- Semantic invariants that apply (cite `glossary.md` entries)

## 3. Desired-State Semantics

Describe desired-state representation, shape-map requirements, and canonical
fields. Include examples or schema references.

## 4. Plan/Apply Semantics

- What the plan must include (stability requirements)
- Apply gating (explicit, local, and safe)
- Refusal conditions

## 5. API/Endpoint Surface (if applicable)

- Endpoints or resources touched
- Required permissions and auth mode
- Expected failure modes

## 6. Risks and Tradeoffs

- Security risks
- Drift risks
- Maintenance costs

## 7. Test Evidence

- Positive/negative/edge cases
- Canonicalization idempotence
- Drift symmetry

## 8. Rollout

- Initial dogfood scope
- CI read-only plan integration
- Local apply checklist
