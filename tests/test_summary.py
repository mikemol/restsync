from restsync.summary import summarize_plan


def test_summarize_plan_no_changes():
    plan = {"endpoints": [{"name": "a", "drift": {}}]}
    assert summarize_plan(plan) == "No changes detected."


def test_summarize_plan_counts_changes():
    plan = {
        "endpoints": [
            {
                "name": "actions_permissions",
                "drift": {
                    "allowed_actions": {"want": "selected", "have": "all"},
                    "nested": {"x": {"want": 1, "have": 2}},
                },
            },
            {"name": "workflow_permissions", "drift": {}},
        ]
    }
    summary = summarize_plan(plan)
    assert "Plan summary: 2 change(s) across 1 endpoint(s)." in summary
    assert "- actions_permissions: 2 change(s)" in summary
