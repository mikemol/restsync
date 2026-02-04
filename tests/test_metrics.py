from restsync.metrics import collect_metrics


def test_collect_metrics_counts_changes_and_overlay():
    plan = {
        "version": 1,
        "provider": "github",
        "repo": {"owner": "octo", "name": "restsync"},
        "endpoints": [
            {
                "name": "actions_permissions",
                "drift": {
                    "allowed_actions": {"want": "selected", "have": "all"},
                    "nested": {"x": {"want": 1, "have": 2}},
                },
            },
            {"name": "workflow_permissions", "drift": {}},
        ],
        "overlay": {
            "name": "github",
            "path": "overlays/github.yml",
            "violations": [
                {"code": "overlay.violation", "message": "first"},
                {"code": "overlay.violation", "message": "second"},
                {"code": "overlay.custom", "message": "third"},
            ],
            "errors": ["overlay failed to load"],
        },
    }

    metrics = collect_metrics(plan)

    assert metrics["metrics_version"] == 1
    assert metrics["spec_version"] == 1
    assert metrics["provider"] == "github"
    assert metrics["repo"]["name"] == "restsync"
    assert metrics["endpoints_total"] == 2
    assert metrics["endpoints_with_drift"] == 1
    assert metrics["changes_total"] == 2
    assert metrics["changes_by_endpoint"]["actions_permissions"] == 2
    assert metrics["changes_by_endpoint"]["workflow_permissions"] == 0
    assert metrics["overlay"]["violations"] == 3
    assert metrics["overlay"]["errors"] == 1
    assert metrics["overlay"]["violation_codes"]["overlay.violation"] == 2
    assert metrics["overlay"]["violation_codes"]["overlay.custom"] == 1
