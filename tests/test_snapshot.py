from pathlib import Path

import pytest

from restsync.snapshot import build_snapshot, SnapshotError, snapshot_from_path
from restsync.spec import load_spec


def test_snapshot_from_path_validates():
    with pytest.raises(SnapshotError):
        snapshot_from_path(Path("/nonexistent.yml"))


def test_build_snapshot_uses_have_only():
    spec, errors = load_spec(Path("configs/restsync.yml"))
    assert errors == []
    assert spec is not None

    # dataflow-bundle: method, token, url
    def fake_request(method, url, token):
        return {"enabled": True}

    snapshot = build_snapshot(spec, token=None, request_func=fake_request)
    assert "endpoints" in snapshot
