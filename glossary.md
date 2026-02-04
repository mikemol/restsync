---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: glossary
doc_role: glossary
doc_scope:
  - repo
  - semantics
  - tooling
  - syncing
doc_authority: normative
doc_requires:
  - README.md
  - CONTRIBUTING.md
  - AGENTS.md
  - POLICY_SEED.md
doc_reviewed_as_of:
  README.md: 6
  CONTRIBUTING.md: 6
  AGENTS.md: 1
  POLICY_SEED.md: 1
doc_commutes_with:
  - POLICY_SEED.md
doc_change_protocol: "POLICY_SEED.md §6"
doc_invariants:
  - rule_of_polysemy
  - core_overlay_boundary
  - plan_apply_separation
  - canonicalization_determinism
doc_erasure:
  - formatting
  - typos
doc_owner: maintainer
---

# Glossary (Normative)

> **Glossary Contract (Normative):**
> This glossary defines the semantic typing discipline for the project.
> Any term reused in code, tests, or documentation must conform to exactly one
> glossary entry, declare its axis, state its commutation law, and identify
> what is erased by aliasing or projection.
>
> **Security Contract (Normative Pointer):**
> Execution and CI safety are governed by `POLICY_SEED.md`.
>
> **Repository Cross-References (Normative Pointers):**
> `README.md` defines project scope and status.
> `CONTRIBUTING.md` defines workflow guardrails and required checks.
> `AGENTS.md` defines LLM/agent obligations and refusal rules.

## 0. Rule of Polysemy

Polysemy is permitted only when:

1. the meanings lie on orthogonal axes, and
2. any interaction is declared to commute (or declared non-interacting), and
3. there is a test or enforcement obligation for the commutation claim.

If any of (1-3) are absent, reuse is invalid.

---

## 1. Core (Sync Engine)

**Meaning:** The REST-agnostic engine that fetches, canonicalizes, diffs, and
plans changes without provider semantics.

**Axis:** Architecture boundary (core vs overlay).

**Desired Commutation (Overlay Independence):**
Replacing one overlay with another must not change the core contract or its
data model. The core only interprets shape maps and transport concerns.

**Failure Modes:**
- Provider-specific logic in core code.
- Core emitting provider-only fields in canonical snapshots.

**Normative Rule:**
> The core must remain REST-agnostic. Provider invariants live in overlays.

**Erasure:** Provider semantics are erased at the core boundary.

---

## 2. Overlay (Semantic Gate)

**Meaning:** A layer that encodes provider meaning, invariants, and refusal
criteria for unsafe plans.

**Axis:** Semantics and safety.

**Desired Commutation (Core Stability):**
Overlays must not mutate core data structures or bypass canonicalization.

**Failure Modes:**
- Overlay mutates raw responses without canonicalization.
- Overlay applies changes without a plan.

**Normative Rule:**
> Overlays may restrict or refuse, but they may not expand the core contract.

**Erasure:** Overlay-specific constraints are erased from the core boundary.

---

## 3. Desired State

**Meaning:** The local, versioned specification of intended configuration.

**Axis:** Configuration (desired vs live).

**Desired Commutation (Canonicalization):**
Ordering, irrelevant fields, and serialization choices must not change desired
state identity after canonicalization.

**Failure Modes:**
- Non-deterministic ordering creates false drift.
- Hidden defaults are treated as explicit intent.

**Normative Rule:**
> Desired state identity is defined by canonicalized content, not formatting.

**Erasure:** Formatting differences are erased by canonicalization.

---

## 4. Live State / Snapshot

**Meaning:** The fetched representation of a live REST resource, normalized
into a canonical snapshot.

**Axis:** Observation (live vs desired).

**Desired Commutation (Transport Independence):**
Transport or pagination variations must not change snapshot identity.

**Failure Modes:**
- Pagination order changes produce different snapshots.
- Unstable API defaults are treated as differences.

**Normative Rule:**
> Snapshots must be canonicalized before diffing.

**Erasure:** Transport-layer artifacts are erased.

---

## 5. Canonicalization

**Meaning:** The deterministic normalization of JSON/YAML data into a
comparison-ready form.

**Axis:** Representation.

**Desired Commutation (Determinism):**
Multiple passes yield identical output: `canon(canon(x)) = canon(x)`.

**Failure Modes:**
- Canonicalization depends on non-deterministic ordering.
- Canonicalization loses intentional fields.

**Normative Rule:**
> Canonicalization must be deterministic and idempotent.

**Erasure:** Ordering, formatting, and ignored fields.

---

## 6. Drift

**Meaning:** The symmetric difference between desired state and live snapshot
under canonicalization and shape-map constraints.

**Axis:** Difference (desired vs live).

**Desired Commutation (Symmetry):**
`drift(desired, live) = drift(live, desired)` in terms of field set, with
context preserved for directionality.

**Failure Modes:**
- One-sided diff hiding deletions or additions.

**Normative Rule:**
> Drift must be computed as a symmetric difference on canonical forms.

**Erasure:** Irrelevant fields excluded by shape maps.

---

## 7. Plan

**Meaning:** A structured, reviewable description of drift and intended actions.

**Axis:** Execution (plan vs apply).

**Desired Commutation (Plan Stability):**
Equivalent desired/live pairs produce equivalent plans after canonicalization.

**Failure Modes:**
- Plan includes non-deterministic ordering.
- Plan omits safety-relevant fields.

**Normative Rule:**
> Plan is the only pre-apply artifact used to reason about safety.

**Erasure:** Transport artifacts and ignored fields.

---

## 8. Apply

**Meaning:** The explicit execution of a plan to mutate live resources.

**Axis:** Execution (apply vs plan).

**Desired Commutation (Explicitness):**
Apply must be triggered only by explicit user intent and must match a plan.

**Failure Modes:**
- Apply in CI.
- Apply without a reviewed plan.

**Normative Rule:**
> Apply is local, explicit, and never runs in CI.

**Erasure:** None. Apply is irreversible and must be fully accounted for.

---

## 9. Shape Map

**Meaning:** A declaration of which fields are compared, ignored, or sorted for
canonicalization and diff.

**Axis:** Comparison semantics.

**Desired Commutation (Field Projection):**
Equivalent resources under the shape map should compare equal.

**Failure Modes:**
- Shape maps ignore safety-critical fields.
- Shape maps include volatile fields.

**Normative Rule:**
> Shape maps must be explicit and reviewed; defaults are suspect.

**Erasure:** Ignored fields are erased by projection.
