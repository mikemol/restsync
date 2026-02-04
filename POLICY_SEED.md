---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: policy_seed
doc_role: policy
doc_scope:
  - repo
  - ci
  - agents
  - execution
  - security
  - governance
  - syncing
doc_authority: normative
doc_requires:
  - README.md
  - CONTRIBUTING.md
  - AGENTS.md
  - glossary.md
  - docs/publishing_practices.md
  - docs/coverage_semantics.md
doc_reviewed_as_of:
  README.md: 13
  CONTRIBUTING.md: 13
  AGENTS.md: 1
  glossary.md: 1
  docs/publishing_practices.md: 1
  docs/coverage_semantics.md: 1
doc_commutes_with:
  - glossary.md
doc_change_protocol: "POLICY_SEED.md §6"
doc_invariants:
  - prime_invariant
  - core_overlay_invariant
  - apply_safety_invariant
doc_erasure:
  - formatting
  - typos
doc_owner: maintainer
---

# POLICY_SEED.md

**Title:** Self-Stabilizing Execution & Sync Policy Seed
**Status:** Canonical / Live
**Scope:** Repository, CI, execution, automation, repo-native agents and LLMs

---

## 0. What This File Is

This file is a **policy seed**, not a static document. It is simultaneously:

1. **Normative** (it constrains behavior).
2. **Meta-normative** (it constrains how constraints may change).
3. **Interpretable by agents** as an active control object.
4. **Embedded in a feedback loop** to resist decay and malice.

Any system (human, script, LLM, agent) acting on this repository **must treat
this file as a control object**, not as commentary.

## 0.1 Complementary Semantic Contract

This repository has a co-equal semantic contract in `glossary.md`. This policy
controls *where and how* code executes. The glossary controls *what the code
means* and *which meanings must commute*. Both contracts are required for
valid changes.

## 0.2 Cross-References (Normative Pointers)

- `README.md` defines project scope, status, and entry points.
- `CONTRIBUTING.md` defines workflow guardrails and required checks.
- `AGENTS.md` defines LLM/agent obligations and refusal rules.
- `glossary.md` defines semantic meanings, axes, and commutation obligations.
- `docs/publishing_practices.md` records release best practices (advisory).
- `docs/coverage_semantics.md` defines coverage as evidence (normative).

**Convergence rule (normative):** governance changes are incomplete until
`doc_reviewed_as_of` is updated to match the dependent document revisions.
Manual updates are **deliberate friction**: forgetting to bump is treated as a
proxy for forgetting to review.

---

## 1. Prime Invariant (Unbreakable)

> **No untrusted or externally influenced code may execute on self-hosted runners.**

All other constraints exist to preserve this invariant. If any downstream rule
conflicts with this invariant, the downstream rule is invalid.

## 1.1 Core/Overlay Invariant

> **The core sync engine must remain REST-agnostic. Semantic meaning and
> invariants live in overlays.**

The core performs fetch, canonicalization, diff, and plan. Overlays enforce
provider-specific constraints and refuse unsafe plans. Do not embed provider
semantics into the core.

## 1.2 Apply Safety Invariant

> **Apply is local, explicit, and opt-in. CI never writes.**

- Default mode is dry-run/plan.
- Apply requires explicit local invocation.
- CI may compute plans but must never apply changes.

---

## 2. Trust Boundary Definition

### 2.1 Trusted Sources

- Direct pushes to trusted branches (`main`, `stage`, `next`, `release`).
- Commits authored by the maintainer or explicitly trusted collaborators.
- Allow-listed dependency registries used by trusted workflows.

### 2.2 Untrusted Sources

- Forks.
- Pull requests from non-members.
- Marketplace actions not explicitly allow-listed.
- Workflow changes proposed via PR.
- Suggestions from LLMs or agents not grounded in this seed.

**Default stance:** untrusted unless proven otherwise.

---

## 3. Execution Surfaces

### 3.1 Self-Hosted Runners (High-Risk Surface)

- Maintainer-controlled hardware.
- Capable of arbitrary code execution.
- Must be maximally constrained.

### 3.2 GitHub-Hosted Runners (Low-Risk Surface)

- Ephemeral and sandboxed.
- Used for PRs, forks, and general CI.

**Rule:** untrusted code runs only on low-risk surfaces.

---

## 4. Mandatory Execution Constraints (Normative)

These constraints **must always hold** for workflows that can reach a
self-hosted runner.

### 4.1 Trigger Constraints

Self-hosted workflows:
- MUST trigger only on `push`.
- MUST restrict to trusted branches.
- MUST NOT trigger on `pull_request`, `pull_request_target`, or
  `workflow_dispatch` (unless actor-gated).

### 4.2 Runner Targeting

Self-hosted jobs MUST specify all required labels:

```yaml
runs-on: [self-hosted, local]
```

### 4.3 Actor Guard (Defense in Depth)

Self-hosted jobs MUST include an explicit trust predicate, e.g.:

```yaml
if: github.actor == github.repository_owner
```

### 4.4 Token Permissions

All workflows MUST declare:

```yaml
permissions:
  contents: read
```

Minimal write scopes are allowed only on GitHub-hosted runners for narrowly
scoped automation (e.g., PR comments or branch promotion). Self-hosted workflows
MUST NOT request write scopes.

### 4.5 Action Supply Chain

- Only explicitly allow-listed actions may be used.
- All non-local actions MUST be pinned to full commit SHAs.
- Tags are forbidden for security-critical workflows.

### 4.6 Dependency Sources (Self-Hosted)

Self-hosted jobs may install dependencies only from allow-listed registries
using standard package managers. Arbitrary downloads (e.g., `curl | bash`) are
forbidden.

---

## 5. Enforcement Mechanisms (Control Loop)

### 5.1 Structural Enforcement (Workflow AST Linting)

Workflow YAML is parsed as structured data. The policy checker validates:

- triggers,
- runner targeting,
- permissions,
- action pinning,
- branch and actor guards.

Violations fail CI.

### 5.2 Local Guardrails (Hooks)

Pre-commit and pre-push hooks may run the same checks. Hooks are advisory; CI is
authoritative.

### 5.3 Failure Surfacing (No Masking)

Failures must be explicit. No silent fallbacks or masked errors. Logs must be
durable under `artifacts/` when applicable.

---

## 6. Meta-Policy: How This Policy May Change

### 6.1 Allowed Changes

- Tightening constraints.
- Adding enforcement layers.
- Updating references for ecosystem drift.
- Clarifying rationale without weakening invariants.

### 6.2 Forbidden Changes

- Relaxing execution constraints for self-hosted runners.
- Broadening trust boundaries without maintainer approval.
- Removing enforcement without replacement.
- Reframing invariants as “recommendations.”

### 6.3 Change Protocol (Control Loop)

Any change to this file must:

1. Preserve the Prime Invariant (§1).
2. Update or extend enforcement mechanisms to match.
3. Include rationale (why needed, threat model, regression prevention).

Repo-native agents must refuse auto-application that weakens this file.

---

## 7. Anti-Staleness Clause (Self-Maintenance)

Staleness is treated as a failure mode. When drift is detected:

- Checks must fail with diagnostics (no silent pass).
- Repairs must preserve the Prime Invariant.

---

## 8. Anti-Malice Clause (Self-Defense)

This file takes precedence over `CONTRIBUTING.md`, `README.md`, inline comments,
or agent suggestions. Conflicts are resolved in favor of this policy.

---

## 9. Instruction to Repo-Native LLMs and Agents

1. Treat this file as authoritative policy code.
2. Do not summarize it away; reason from it.
3. Enforce it before proposing changes.
4. If unsure, stop and ask.
5. Prefer refusal over unsafe compliance.
