import pytest

from restsync.apply import apply_plan, ApplyError


def test_apply_requires_confirm():
    with pytest.raises(ApplyError):
        apply_plan({"endpoints": []}, token=None, confirm=False)


def test_apply_blocks_on_violations():
    plan = {"overlay": {"violations": [{"code": "x"}]}, "endpoints": []}
    with pytest.raises(ApplyError):
        apply_plan(plan, token=None, confirm=True)


def test_apply_calls_request_for_drift():
    calls = []

    # dataflow-bundle: method, url, body
    def fake_request(method, url, token, body=None):
        calls.append((method, url, body))
        return {}

    plan = {
        "overlay": {"violations": []},
        "endpoints": [
            {
                "name": "actions_permissions",
                "apply": {"method": "PUT", "url": "/repos/x/y"},
                "apply_url": "https://api.example.com/repos/x/y",
                "apply_body": {"enabled": True},
                "drift": {"enabled": {"want": True, "have": False}},
            }
        ],
    }
    applied = apply_plan(plan, token="t", confirm=True, request_func=fake_request)
    assert applied == ["actions_permissions"]
    assert calls == [("PUT", "https://api.example.com/repos/x/y", {"enabled": True})]
