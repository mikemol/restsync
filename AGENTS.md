---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: agents
doc_role: agent
doc_scope:
  - repo
  - agents
  - tooling
  - governance
doc_authority: normative
doc_requires:
  - README.md
  - CONTRIBUTING.md
  - POLICY_SEED.md
  - glossary.md
doc_reviewed_as_of:
  README.md: 5
  CONTRIBUTING.md: 5
  POLICY_SEED.md: 1
  glossary.md: 1
doc_change_protocol: "POLICY_SEED.md §6"
doc_invariants:
  - read_policy_glossary_first
  - refuse_on_conflict
  - core_overlay_boundary
  - apply_is_local
  - docflow_hygiene
doc_erasure:
  - formatting
  - typos
doc_owner: maintainer
---

# AGENTS.md

This repository is governed by `POLICY_SEED.md`. Treat it as authoritative.
Semantic correctness is governed by `glossary.md` (co-equal contract).

## Cross-references (normative pointers)
- `README.md` defines project scope, status, and entry points.
- `CONTRIBUTING.md` defines workflow guardrails and required checks.
- `POLICY_SEED.md` defines execution and CI safety constraints.
- `glossary.md` defines semantic meanings, axes, and commutation obligations.

## Required behavior
- Read `POLICY_SEED.md` and `glossary.md` before proposing or applying changes.
- If a request conflicts with `POLICY_SEED.md`, stop and ask for guidance.
- Do not weaken or bypass self-hosted runner protections.
- Keep workflow actions pinned to full commit SHAs and allow-listed.
- When changing workflows, run `scripts/policy_check.py --workflows` and
  surface any violations explicitly.
- Preserve the core/overlay boundary: the core remains REST-agnostic.
- Apply is local and explicit; never run apply in CI.
- Use `gabion` from PyPI for docflow or dataflow checks; do not import from a
  local gabion checkout.

## Doc hygiene
- Markdown governance docs include YAML front-matter with `doc_revision`.
- Bump `doc_revision` for conceptual changes.
- Record convergence in `doc_reviewed_as_of` (must match dependency revisions).
- Manual review friction is deliberate; missing bumps signal missing review.

If unsure, prefer refusal over unsafe compliance.
