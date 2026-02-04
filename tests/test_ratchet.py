from restsync.ratchet import apply_ratchet


def test_ratchet_filters_baseline():
    baseline = [
        {"code": "a", "endpoint": "x", "message": "msg"},
    ]
    violations = [
        {"code": "a", "endpoint": "x", "message": "msg"},
        {"code": "b", "endpoint": "y", "message": "msg2"},
    ]
    result = apply_ratchet(violations, baseline)
    assert result.violations == [{"code": "b", "endpoint": "y", "message": "msg2"}]
