---
doc_revision: 1
reader_reintern: "Reader-only: re-intern if doc_revision changed since you last read this doc."
doc_id: out_2
doc_role: hypothesis
doc_scope:
  - repo
  - tooling
  - governance
  - syncing
  - research
doc_authority: informative
doc_requires:
  - POLICY_SEED.md
  - glossary.md
  - CONTRIBUTING.md
  - README.md
doc_reviewed_as_of:
  POLICY_SEED.md: 1
  glossary.md: 1
  CONTRIBUTING.md: 11
  README.md: 11
doc_change_protocol: "POLICY_SEED.md §6"
doc_erasure:
  - formatting
  - typos
doc_owner: maintainer
---

# Hypothesis: "Rsync for REST" + Overlay Semantics

## 0. Thesis
We want a reliable way to sync repository or service configuration against a
desired state without embedding provider-specific semantics in the core engine.
The alternative to heavy stateful tools is a REST-agnostic core plus a semantic
overlay that encodes meaning constraints. The core remains generic; overlays
supply invariants and refusals.

## 1. Design Goals
- **Golden config without heavy state.** Desired state lives in local files.
- **Drift detection via symmetric difference.** Canonicalize and diff live JSON.
- **Low semantic coupling.** Core does not encode provider semantics.
- **Overlay gate for invariants.** Overlays refuse unsafe plans.
- **Safe apply.** Apply is local and explicit (no CI writes).

## 2. Architecture Sketch

### 2.1 Generic REST Sync Core
Inputs:
- `base_url`, `auth`
- endpoint list
- shape map (fields to compare, ignore, sort)

Outputs:
- canonical snapshots
- diff / plan
- optional apply (PATCH/PUT/POST)

Core responsibilities:
- fetch
- normalize
- diff
- plan

Core does not understand provider policies, only JSON shapes.

### 2.2 Semantic Overlay
Overlay responsibilities:
- define bundles of settings that commute
- encode invariants (e.g., tag or workflow constraints)
- refuse apply if invariants are violated
- output human-readable explanations in `out/`

The overlay is the semantic gate on top of a generic sync engine.

## 3. Data Shapes (Sketch)

### 3.1 Desired State (YAML)
```yaml
repo: example/acme
base_url: https://api.example.com
endpoints:
  - name: actions_permissions
    method: GET
    url: /repos/{owner}/{repo}/actions/permissions
    compare:
      include: [allowed_actions, selected_actions, default_workflow_permissions]
      ignore: [url]
    apply:
      method: PUT
      url: /repos/{owner}/{repo}/actions/permissions
      body_from: .desired.actions_permissions
```

### 3.2 Canonical Snapshot (JSON)
```json
{
  "actions_permissions": {
    "allowed_actions": "selected",
    "default_workflow_permissions": "read",
    "can_approve_pull_request_reviews": false
  }
}
```

### 3.3 Diff Output (plan)
```json
{
  "actions_permissions": {
    "drift": {
      "allowed_actions": {"want": "selected", "have": "all"}
    }
  }
}
```

## 4. Risks / Constraints
- API drift or missing endpoints require adapter updates.
- Apply requires admin scopes; keep local and explicit.
- Some provider rulesets may not be exposed uniformly.
