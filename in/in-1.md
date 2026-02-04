---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: in_1
doc_role: idea
doc_scope:
  - repo
  - architecture
  - syncing
doc_authority: informative
doc_requires:
  - POLICY_SEED.md
  - glossary.md
  - CONTRIBUTING.md
  - README.md
doc_reviewed_as_of:
  POLICY_SEED.md: 1
  glossary.md: 1
  CONTRIBUTING.md: 1
  README.md: 2
doc_change_protocol: "POLICY_SEED.md §6"
doc_erasure:
  - formatting
  - typos
doc_owner: maintainer
---

# Inbox Note: Core + Overlay Model

This note assumes the governance contracts in `POLICY_SEED.md` and
`glossary.md`, plus workflow guardrails in `CONTRIBUTING.md` and scope in
`README.md`.

Initial concept:
- A REST-agnostic core fetches, canonicalizes, and diffs.
- Overlays encode provider semantics and refuse unsafe plans.
- Apply is explicit and local; CI never writes.
