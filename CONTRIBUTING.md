---
doc_revision: 11
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: contributing
doc_role: guide
doc_scope:
  - repo
  - contributors
  - workflows
  - tooling
doc_authority: normative
doc_requires:
  - README.md
  - AGENTS.md
  - POLICY_SEED.md
  - glossary.md
  - docs/coverage_semantics.md
doc_reviewed_as_of:
  README.md: 11
  AGENTS.md: 1
  POLICY_SEED.md: 1
  glossary.md: 1
  docs/coverage_semantics.md: 1
doc_change_protocol: "POLICY_SEED.md §6"
doc_invariants:
  - policy_glossary_handshake
  - core_overlay_boundary
  - apply_is_local
  - docflow_hygiene
doc_erasure:
  - formatting
  - typos
doc_owner: maintainer
---

# Contributing

Thanks for contributing. This repo enforces a strict execution policy to protect
self-hosted runners and maintain semantic correctness. Please read
`POLICY_SEED.md` and `glossary.md` before making changes.

## Contract handshake (normative)
Execution safety is governed by `POLICY_SEED.md`. Semantic correctness is
governed by `glossary.md`. Both contracts must be satisfied for any change to be
valid.

## Architectural invariants (normative)
- **Core/overlay boundary:** the core sync engine is REST-agnostic; overlays
  encode provider semantics and safety constraints.
- **Plan/apply separation:** plan is reviewable; apply is local and explicit.

## Cross-references (normative pointers)
- `README.md` defines project scope, status, and entry points.
- `AGENTS.md` defines LLM/agent obligations and refusal rules.
- `POLICY_SEED.md` defines execution and CI safety constraints.
- `glossary.md` defines semantic meanings, axes, and commutation obligations.
- `docs/coverage_semantics.md` defines coverage evidence requirements.

## Branching model (normative)
- Routine work goes to `stage`; CI runs on every `stage` push and must be green.
- `main` is protected and receives changes via PRs from `stage`.
- Merges to `main` are regular merge commits (no squash or rebase).
- `stage` accumulates changes and may include merge commits from `main`.
- `next` mirrors `main` (no unique commits) and is updated after `main` merges.
- `release` mirrors `next` (no unique commits) and is updated only after
  `test-v*` succeeds.
- `next` and `release` are automation-only branches; human pushes are forbidden.

## Workflow authoring (normative)
Workflow logic lives in `scripts/`. YAML files should orchestrate steps and
invoke scripts rather than embed long inline logic.

## Doc hygiene
- Governance docs include YAML front-matter with `doc_revision`.
- Bump `doc_revision` for conceptual changes.
- Update `doc_reviewed_as_of` for dependency convergence.
- Manual convergence is deliberate friction; missing bumps signal missing review.

## Feature documentation
- **Design docs:** `docs/design/<feature>.md` (use `docs/design/_template.md`).
- **Implementation notes:** `docs/impl/<feature>.md` (use `docs/impl/_template.md`).
- Every feature is tagged as **green** or **entailed** via front-matter:
  - `feature_kind: green` for independent features.
  - `feature_kind: entailed` with `entailed_by: [parent_feature_id]` for
    features necessitated by others.
- Track each feature in `docs/sppf_checklist.md` and link to its GH issue ID.

## Development setup
Install toolchain (via `mise`):
```
mise install
```

Install editable package + dev tools:
```
mise exec -- python -m pip install -e .[dev]
```

Bootstrap everything:
```
scripts/bootstrap.sh
```

## Checks
Run policy checks:
```
mise exec -- python scripts/policy_check.py --workflows
```

Run docflow audit:
```
mise exec -- python scripts/docflow_audit.py --root . --fail-on-violations
```

Validate config:
```
restsync spec-check --config configs/restsync.yml
```

Generate a read-only plan:
```
restsync plan --config configs/restsync.yml
```
By default, auth is `gh` (uses `gh auth token`). In CI or headless contexts,
set `RESTSYNC_TOKEN` (or `GITHUB_TOKEN`) to supply a token explicitly.

Validate plan and fail on overlay violations:
```
restsync check --config configs/restsync.yml --output artifacts/plan_runs/plan.json
```

Plan/check output includes a short human-readable summary.

Overlay baselines (ratchet mode):
```
restsync check --config configs/restsync.yml --baseline baselines/overlay_baseline.json
restsync check --config configs/restsync.yml --baseline baselines/overlay_baseline.json --baseline-write
```

Apply changes (local only, requires explicit confirmation):
```
restsync apply --config configs/restsync.yml --confirm
```

Capture a read-only snapshot of live state:
```
restsync snapshot --config configs/restsync.yml --output artifacts/snapshots/snapshot.json
```

Generate a timestamped plan artifact:
```
scripts/plan_snapshot.sh
```

Run all checks (policy + docflow + tests):
```
scripts/checks.sh
```

Make targets are available for common tasks:
```
make bootstrap
make check
make test
make plan
make snapshot
make docflow
make policy
make clean-artifacts
```

Install git hooks (optional):
```
scripts/install_hooks.sh
```
Bypass hooks for a one-off command:
```
RESTSYNC_SKIP_HOOKS=1 git commit
```

Run tests:
```
mise exec -- python -m pytest
```

## Optional: dataflow grammar audit
If `gabion` checks are configured for this repo, install from PyPI and run:
```
mise exec -- python -m gabion check
```
