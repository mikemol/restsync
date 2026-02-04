---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: convergence_checklist
doc_role: checklist
doc_scope:
  - repo
  - planning
  - tooling
doc_authority: informative
doc_requires: []
doc_reviewed_as_of: {}
doc_change_protocol: "POLICY_SEED.md §6"
doc_erasure:
  - formatting
  - typos
doc_owner: maintainer
---

# Convergence Checklist (Bottom-Up)

This checklist tracks concept nodes derived from `in/` and their adoption into
`out/`, `docs/`, or code. It is advisory only.

Legend: [x] done · [ ] planned · [~] partial/heuristic

## Core engine
- [ ] Canonical snapshot pipeline (fetch -> normalize -> snapshot).
- [ ] Shape-map projection (include/ignore/sort).
- [ ] Deterministic diff (symmetric difference).

## Safety and apply
- [ ] Plan format (stable JSON schema).
- [ ] Apply gate (explicit local confirmation).
- [ ] Overlay refusal rules for unsafe plans.

## Overlay model
- [ ] Overlay interface and validation.
- [ ] GitHub overlay prototype (branch protections, actions settings).

## Tooling
- [ ] Policy checks enforced in CI.
- [ ] Docflow audit enforced in CI.
