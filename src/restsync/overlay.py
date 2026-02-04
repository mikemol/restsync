from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass(frozen=True)
class OverlayConfig:
    name: str
    allow_list_path: Optional[Path]
    raw: Dict[str, Any]


def load_overlay(path: Path) -> tuple[Optional[OverlayConfig], List[str]]:
    if not path.exists():
        return None, []
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        return None, [f"overlay config must be a mapping: {path}"]
    name = data.get("overlay")
    if not isinstance(name, str) or not name.strip():
        return None, [f"overlay config missing overlay name: {path}"]
    allow_list = data.get("allow_list")
    allow_path = None
    if allow_list:
        candidate = Path(allow_list)
        if not candidate.is_absolute():
            candidate = (Path.cwd() / candidate).resolve()
        allow_path = candidate
    return OverlayConfig(name=name.strip(), allow_list_path=allow_path, raw=data), []


def _load_allow_list(path: Optional[Path]) -> List[str]:
    if path is None or not path.exists():
        return []
    entries: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        entries.append(line)
    return entries


def _find_endpoint(plan: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    for endpoint in plan.get("endpoints", []):
        if endpoint.get("name") == name:
            return endpoint
    return None


def _violation(code: str, message: str, endpoint: Optional[str] = None) -> Dict[str, Any]:
    payload = {"code": code, "message": message}
    if endpoint:
        payload["endpoint"] = endpoint
    return payload


def _expect_want_mapping(
    want: Any, endpoint: str, code: str, message: str, violations: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    if not isinstance(want, dict):
        violations.append(_violation(code, message, endpoint=endpoint))
        return None
    return want


def _expect_enabled_toggle(
    want: Dict[str, Any],
    key: str,
    expected: bool,
    endpoint: str,
    code: str,
    violations: List[Dict[str, Any]],
) -> None:
    value = want.get(key)
    if isinstance(value, dict):
        enabled = value.get("enabled")
        if enabled is expected:
            return
        violations.append(_violation(code, f"{key}.enabled must be {expected}", endpoint=endpoint))
        return
    if isinstance(value, bool):
        if value is expected:
            return
        violations.append(_violation(code, f"{key} must be {expected}", endpoint=endpoint))
        return
    violations.append(
        _violation(
            code,
            f"{key} must be {expected} or a mapping with enabled={expected}",
            endpoint=endpoint,
        )
    )


def _validate_branch_protection(
    plan: Dict[str, Any],
    endpoint_name: str,
    branch_label: str,
    *,
    expected_status_checks: Optional[List[str]],
    expected_toggles: Dict[str, bool],
    violations: List[Dict[str, Any]],
) -> None:
    endpoint_label = str(endpoint_name)
    endpoint = _find_endpoint(plan, endpoint_name)
    if endpoint is None:
        violations.append(
            _violation(
                f"github.branch.{branch_label}.missing",
                f"missing {endpoint_name} endpoint",
                endpoint=endpoint_label,
            )
        )
        return
    want = _expect_want_mapping(
        endpoint.get("want"),
        endpoint_label,
        f"github.branch.{branch_label}.want_mapping",
        f"{endpoint_name} want must be a mapping",
        violations,
    )
    if want is None:
        return

    status_checks = want.get("required_status_checks", "__missing__")
    if expected_status_checks is None:
        if status_checks is not None:
            violations.append(
                    _violation(
                        f"github.branch.{branch_label}.required_status_checks",
                        "required_status_checks must be null",
                        endpoint=endpoint_label,
                    )
                )
    else:
        if not isinstance(status_checks, dict):
            violations.append(
                _violation(
                    f"github.branch.{branch_label}.required_status_checks",
                    "required_status_checks must be a mapping",
                    endpoint=endpoint_label,
                )
            )
        else:
            if status_checks.get("strict") is not True:
                violations.append(
                    _violation(
                        f"github.branch.{branch_label}.required_status_checks_strict",
                        "required_status_checks.strict must be true",
                        endpoint=endpoint_label,
                    )
                )
            contexts = status_checks.get("contexts")
            if not isinstance(contexts, list):
                violations.append(
                    _violation(
                        f"github.branch.{branch_label}.required_status_checks_contexts",
                        "required_status_checks.contexts must be a list",
                        endpoint=endpoint_label,
                    )
                )
            else:
                expected = set(expected_status_checks)
                actual = set(contexts)
                if actual != expected:
                    missing = sorted(expected - actual)
                    extra = sorted(actual - expected)
                    violations.append(
                        _violation(
                            f"github.branch.{branch_label}.required_status_checks_contexts",
                            "required_status_checks.contexts must match expected set"
                            f" (missing: {missing}, extra: {extra})",
                            endpoint=endpoint_label,
                        )
                    )

    for key, expected in expected_toggles.items():
        _expect_enabled_toggle(
            want,
            key,
            expected,
            endpoint_label,
            f"github.branch.{branch_label}.{key}",
            violations,
        )


def validate_plan(plan: Dict[str, Any], overlay: OverlayConfig) -> List[Dict[str, Any]]:
    if overlay.name != "github":
        return [_violation("overlay.unknown", f"unsupported overlay: {overlay.name}")]

    violations: List[Dict[str, Any]] = []
    allow_list = _load_allow_list(overlay.allow_list_path)

    actions = _find_endpoint(plan, "actions_permissions")
    if actions is None:
        violations.append(_violation("github.actions.missing", "missing actions_permissions endpoint"))
    else:
        want = actions.get("want") or {}
        if want.get("allowed_actions") != "selected":
            violations.append(
                _violation(
                    "github.actions.allowed_actions",
                    "allowed_actions must be 'selected'",
                    endpoint="actions_permissions",
                )
            )
        if want.get("sha_pinning_required") is not True:
            violations.append(
                _violation(
                    "github.actions.sha_pinning",
                    "sha_pinning_required must be true",
                    endpoint="actions_permissions",
                )
            )
        if allow_list:
            selected = _find_endpoint(plan, "selected_actions")
            if selected is None:
                violations.append(
                    _violation(
                        "github.actions.selected_actions_missing",
                        "missing selected_actions endpoint",
                        endpoint="selected_actions",
                    )
                )
            else:
                want_selected = selected.get("want") or {}
                patterns = want_selected.get("patterns_allowed") or []
                if not isinstance(patterns, list):
                    violations.append(
                        _violation(
                            "github.actions.patterns",
                            "selected_actions.patterns_allowed must be a list",
                            endpoint="selected_actions",
                        )
                    )
                else:
                    missing = sorted(set(allow_list) - set(patterns))
                    extra = sorted(set(patterns) - set(allow_list))
                    if missing:
                        violations.append(
                            _violation(
                                "github.actions.allow_list_missing",
                                f"allow_list entries missing from selected_actions.patterns_allowed: {missing}",
                                endpoint="selected_actions",
                            )
                        )
                    if extra:
                        violations.append(
                            _violation(
                                "github.actions.allow_list_extra",
                                f"selected_actions.patterns_allowed contains entries not in allow_list: {extra}",
                                endpoint="selected_actions",
                            )
                        )

    workflow = _find_endpoint(plan, "workflow_permissions")
    if workflow is None:
        violations.append(_violation("github.workflow.missing", "missing workflow_permissions endpoint"))
    else:
        want = workflow.get("want") or {}
        if want.get("default_workflow_permissions") != "read":
            violations.append(
                _violation(
                    "github.workflow.default_permissions",
                    "default_workflow_permissions must be 'read'",
                    endpoint="workflow_permissions",
                )
            )
        if want.get("can_approve_pull_request_reviews") is not False:
            violations.append(
                _violation(
                    "github.workflow.approve_reviews",
                    "can_approve_pull_request_reviews must be false",
                    endpoint="workflow_permissions",
                )
            )

    main_toggles = {
        "required_signatures": False,
        "enforce_admins": True,
        "required_linear_history": False,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": True,
        "lock_branch": False,
        "allow_fork_syncing": False,
    }
    _validate_branch_protection(
        plan,
        "branch_main_protection",
        "main",
        expected_status_checks=["audit", "dataflow-grammar"],
        expected_toggles=main_toggles,
        violations=violations,
    )

    stage_toggles = {
        "required_signatures": False,
        "enforce_admins": False,
        "required_linear_history": False,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "block_creations": False,
        "required_conversation_resolution": True,
        "lock_branch": False,
        "allow_fork_syncing": False,
    }
    _validate_branch_protection(
        plan,
        "branch_stage_protection",
        "stage",
        expected_status_checks=None,
        expected_toggles=stage_toggles,
        violations=violations,
    )

    return violations
