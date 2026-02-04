---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: coverage_semantics
doc_role: policy
doc_scope:
  - repo
  - testing
  - coverage
  - analysis
  - governance
doc_authority: normative
doc_requires:
  - POLICY_SEED.md
  - glossary.md
  - README.md
  - CONTRIBUTING.md
  - AGENTS.md
doc_reviewed_as_of:
  POLICY_SEED.md: 1
  glossary.md: 1
  README.md: 9
  CONTRIBUTING.md: 9
  AGENTS.md: 1
doc_change_protocol: "POLICY_SEED.md §6"
doc_invariants:
  - coverage_is_evidence
  - rule_coverage_required
  - ratchet_only
doc_erasure:
  - formatting
  - typos
doc_owner: maintainer
---

# Coverage Semantics (Normative)

Coverage is not a vanity metric in this repository. It is **evidence** that the
semantic invariants described in `glossary.md` and `POLICY_SEED.md` are enforced
by tests.

This policy is scoped by `README.md`, `CONTRIBUTING.md`, and `AGENTS.md`.

## 1. Coverage Axes (Evidence Types)

### 1.1 Execution coverage (advisory)
Line/branch coverage shows what code executed, but **does not** guarantee
semantic correctness. Use it for trend monitoring and gap discovery.

### 1.2 Rule coverage (required)
Each normative rule or invariant must be exercised by tests that include:
- **Positive case:** detects a violation.
- **Negative case:** avoids a false positive.
- **Edge case:** aliasing, ordering, or boundary conditions.

### 1.3 Grammar/AST feature coverage (required for new features)
When a new parsing or diff feature is added, include a fixture where the feature
**changes the analysis outcome**.

### 1.4 Convergence/commutation coverage (required for invariants)
Metamorphic tests must cover commutation laws in `glossary.md`:
- canonicalization idempotence
- shape-map projection invariance

## 2. Ratchet Policy (No Regression)

Coverage is ratcheted:
- Existing gaps may be baseline-accepted for execution coverage.
- **New or modified rules** MUST include rule/grammar/convergence coverage.
- New tests must be specific to the invariant they protect.

## 3. Reporting (Current Practice)

Measurement command (advisory, not gating by default):
```
mise exec -- python -m pytest --cov=src/restsync --cov-report=term-missing
```

## 4. Interpretation Guidance

When assessing coverage:
- Prefer **rule coverage** over raw percentages.
- Treat low execution coverage in core sync logic as a risk signal.
- Require convergence tests whenever canonicalization or diff heuristics change.

Coverage is evidence, not proof. The goal is to make regressions hard to hide.
