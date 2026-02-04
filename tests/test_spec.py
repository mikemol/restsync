from pathlib import Path

from restsync.spec import load_spec


def test_load_spec_from_repo_config():
    spec, errors = load_spec(Path("configs/restsync.yml"))
    assert errors == []
    assert spec is not None
    assert spec.provider == "github"
    assert spec.repo.owner == "mikemol"
    assert spec.repo.name == "restsync"
    assert spec.endpoints
    assert {e.name for e in spec.endpoints} == {
        "actions_permissions",
        "selected_actions",
        "workflow_permissions",
    }
