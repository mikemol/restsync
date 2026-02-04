---
doc_revision: 14
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: readme
doc_role: readme
doc_scope:
  - repo
  - overview
  - tooling
  - syncing
doc_authority: informative
doc_requires:
  - POLICY_SEED.md
  - glossary.md
  - AGENTS.md
  - CONTRIBUTING.md
doc_reviewed_as_of:
  POLICY_SEED.md: 1
  glossary.md: 1
  AGENTS.md: 1
  CONTRIBUTING.md: 14
doc_change_protocol: "POLICY_SEED.md §6"
doc_erasure:
  - formatting
  - typos
doc_owner: maintainer
---

# restsync

![plan health](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/mikemol/restsync/main/docs/badges/plan-health.json)

Restsync is an "rsync for REST" tool: a desired-state sync engine that
compares live REST resources against a local spec, produces a plan, and (when
explicitly authorized) applies the diff. The core is REST-agnostic; semantic
overlays encode provider-specific invariants.

## Status
- Early scaffold. Core engine and overlays are planned.
- Governance layer is active and enforced.

## Architecture (planned)
- **Core sync engine:** fetch, canonicalize, diff, and plan without provider
  semantics.
- **Semantic overlays:** enforce invariants and meaning constraints before apply.
- **Safety gates:** no implicit writes; apply is local and explicit.

## Governance
This repository is governed by two co-equal contracts:
- `POLICY_SEED.md` (execution and CI safety)
- `glossary.md` (semantic meanings and commutation obligations)

LLM/agent behavior is governed by `AGENTS.md`.
Contributor workflows are defined in `CONTRIBUTING.md`.

## Quick start (placeholder)
Install development tools (via `mise`):
```
mise install
```

Install editable package + dev tools:
```
mise exec -- python -m pip install -e .[dev]
```

Run policy and docflow checks:
```
mise exec -- python scripts/policy_check.py --workflows
mise exec -- python scripts/docflow_audit.py --root . --fail-on-violations
```

Run dataflow audit (gabion):
```
mise exec -- python -m gabion check --report artifacts/audit_reports/dataflow_report.md
```

Validate config:
```
restsync spec-check --config configs/restsync.yml
```

Generate a read-only plan:
```
restsync plan --config configs/restsync.yml --metrics artifacts/plan_runs/metrics.json
```
By default, auth is `gh` (uses `gh auth token`). In CI or headless contexts,
set `RESTSYNC_TOKEN` (or `GITHUB_TOKEN`) to supply a token explicitly.

Validate plan and fail on overlay violations:
```
restsync check --config configs/restsync.yml --output artifacts/plan_runs/plan.json --metrics artifacts/plan_runs/metrics.json
```

Plan and check output includes a short human-readable summary plus optional metrics JSON.

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

Generate timestamped plan + metrics artifacts:
```
scripts/plan_snapshot.sh
```

Update badge JSON from current plan metrics:
```
scripts/update_badges.sh
```

Run tests:
```
mise exec -- python -m pytest
```

## Quick commands (make)
```
make bootstrap
make check
make test
make plan
make snapshot
make docflow
make dataflow
make policy
make badges
make clean-artifacts
```

## License
Apache-2.0. See `LICENSE`.
