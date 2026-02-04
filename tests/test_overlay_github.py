from pathlib import Path

from restsync.overlay import load_overlay, validate_plan


def _load_allow_list(overlay):
    if overlay.allow_list_path is None:
        return []
    lines = []
    for line in overlay.allow_list_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def _baseline_plan(patterns):
    return {
        "endpoints": [
            {
                "name": "actions_permissions",
                "want": {
                    "allowed_actions": "selected",
                    "sha_pinning_required": True,
                },
            },
            {
                "name": "selected_actions",
                "want": {
                    "patterns_allowed": patterns,
                },
            },
            {
                "name": "workflow_permissions",
                "want": {
                    "default_workflow_permissions": "read",
                    "can_approve_pull_request_reviews": False,
                },
            },
            {
                "name": "branch_main_protection",
                "want": {
                    "required_status_checks": {
                        "strict": True,
                        "contexts": ["audit", "dataflow-grammar"],
                    },
                    "required_signatures": False,
                    "enforce_admins": True,
                    "required_linear_history": False,
                    "allow_force_pushes": False,
                    "allow_deletions": False,
                    "block_creations": False,
                    "required_conversation_resolution": True,
                    "lock_branch": False,
                    "allow_fork_syncing": False,
                },
            },
            {
                "name": "branch_stage_protection",
                "want": {
                    "required_status_checks": None,
                    "required_signatures": False,
                    "enforce_admins": False,
                    "required_linear_history": False,
                    "allow_force_pushes": False,
                    "allow_deletions": False,
                    "block_creations": False,
                    "required_conversation_resolution": True,
                    "lock_branch": False,
                    "allow_fork_syncing": False,
                },
            },
        ]
    }


def test_overlay_flags_missing_allow_list_entries(tmp_path):
    overlay_path = Path("configs/overlays/github.yml")
    overlay, errors = load_overlay(overlay_path)
    assert errors == []
    assert overlay is not None

    plan = {
        "endpoints": [
            {
                "name": "actions_permissions",
                "want": {
                    "allowed_actions": "selected",
                    "sha_pinning_required": True,
                },
            },
            {
                "name": "selected_actions",
                "want": {
                    "patterns_allowed": [],
                },
            },
            {
                "name": "workflow_permissions",
                "want": {
                    "default_workflow_permissions": "read",
                    "can_approve_pull_request_reviews": False,
                },
            },
        ]
    }

    violations = validate_plan(plan, overlay)
    assert any(v["code"] == "github.actions.allow_list_missing" for v in violations)


def test_overlay_accepts_branch_protection_baseline(tmp_path):
    overlay_path = Path("configs/overlays/github.yml")
    overlay, errors = load_overlay(overlay_path)
    assert errors == []
    assert overlay is not None

    patterns = _load_allow_list(overlay)
    plan = _baseline_plan(patterns)

    violations = validate_plan(plan, overlay)
    assert violations == []


def test_overlay_flags_missing_branch_protection(tmp_path):
    overlay_path = Path("configs/overlays/github.yml")
    overlay, errors = load_overlay(overlay_path)
    assert errors == []
    assert overlay is not None

    patterns = _load_allow_list(overlay)
    plan = _baseline_plan(patterns)
    plan["endpoints"] = [ep for ep in plan["endpoints"] if ep["name"] != "branch_main_protection"]

    violations = validate_plan(plan, overlay)
    assert any(v["code"] == "github.branch.main.missing" for v in violations)
