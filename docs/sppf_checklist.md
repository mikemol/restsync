---
doc_revision: 6
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

Feature tagging: new checklist lines should declare either `[green]` or
`[entailed: <feature_id>]` to capture entailment without splitting the feature
taxonomy.

## Core engine
- [ ] Core sync pipeline (fetch -> canonicalize -> diff -> plan). [green] (core_sync_pipeline)
- [ ] Canonical snapshot pipeline (fetch -> normalize -> snapshot). [entailed: core_sync_pipeline] (core_canonical_snapshot)
- [ ] Shape-map projection (include/ignore/sort). [entailed: core_sync_pipeline] (core_shape_map)
- [ ] Deterministic diff (symmetric difference). [entailed: core_sync_pipeline] (core_deterministic_diff)
- [ ] Desired-state spec (YAML schema + validation). [entailed: core_sync_pipeline] (desired_state_spec)
- [x] Snapshot capture (read-only live state). [entailed: core_sync_pipeline] (snapshot_capture)

## Safety and apply
- [ ] Plan format (stable JSON schema). [entailed: core_sync_pipeline] (plan_schema)
- [x] Apply gate (explicit local confirmation). [entailed: core_sync_pipeline] (apply_gate)
- [ ] Overlay refusal rules for unsafe plans. [entailed: overlay_model] (overlay_refusal_rules)

## Overlay model
- [ ] Overlay model and validation. [green] (overlay_model)
- [ ] GitHub overlay prototype (branch protections, actions settings). [entailed: overlay_model] (github_overlay)
- [ ] GitHub actions settings parity. [entailed: github_overlay] (github_actions_settings)
- [ ] GitHub branch rulesets parity. [entailed: github_overlay] (github_branch_rulesets)
- [ ] GitHub tag rulesets parity. [entailed: github_overlay] (github_tag_rulesets)

## Tooling
- [x] Policy checks enforced in CI. [green] (tooling_policy_ci)
- [x] Docflow audit enforced in CI. [green] (tooling_docflow_ci)
- [x] Dataflow audit enforced in CI. [green] (tooling_dataflow_ci)
