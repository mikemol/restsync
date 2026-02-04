from pathlib import Path

from restsync.overlay import load_overlay, validate_plan


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
