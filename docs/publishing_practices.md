---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: publishing_practices
doc_role: practices
doc_scope:
  - repo
  - release
  - packaging
  - ci
doc_authority: informative
doc_requires:
  - POLICY_SEED.md
  - CONTRIBUTING.md
doc_reviewed_as_of:
  POLICY_SEED.md: 1
  CONTRIBUTING.md: 11
doc_change_protocol: "POLICY_SEED.md §6"
doc_erasure:
  - formatting
  - typos
doc_owner: maintainer
---

# Publishing Practices (Best-Practice Register)

This document records the current best practices for publishing restsync as a
Python package. It is advisory, but referenced from `POLICY_SEED.md` so the
practices remain visible and reviewable. See `CONTRIBUTING.md` for workflow
guardrails.

## 1. Metadata completeness (PEP 621)
Provide a complete `pyproject.toml` metadata block before first release:
- `readme`
- `requires-python`
- `authors` / `maintainers`
- `license` (SPDX expression)
- `keywords` and `classifiers`
- `project.urls` (repo, docs, issues)

## 2. License clarity
Use a single SPDX license expression in `project.license` and add a `LICENSE`
file. Avoid conflicting classifiers.

## 3. Build artifacts explicitly
Build both sdist and wheel artifacts before upload:
- `python -m build`

## 4. TestPyPI dry run
Upload to TestPyPI first, then install from TestPyPI to validate metadata and
entry points.

## 5. Trusted Publishing (OIDC)
Use GitHub OIDC trusted publishing for releases. Avoid long-lived API tokens.
Tag-only triggers and pinned actions are required.

## 6. Harden the release workflow
Release workflows should:
- be dedicated (no PR triggers),
- use pinned action SHAs,
- request minimal permissions,
- run only from trusted branches/tags,
- keep workflow logic in `scripts/`.
