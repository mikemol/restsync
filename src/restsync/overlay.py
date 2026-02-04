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
            selected = want.get("selected_actions") or {}
            patterns = selected.get("patterns") or []
            if not isinstance(patterns, list):
                violations.append(
                    _violation(
                        "github.actions.patterns",
                        "selected_actions.patterns must be a list",
                        endpoint="actions_permissions",
                    )
                )
            else:
                missing = sorted(set(allow_list) - set(patterns))
                extra = sorted(set(patterns) - set(allow_list))
                if missing:
                    violations.append(
                        _violation(
                            "github.actions.allow_list_missing",
                            f"allow_list entries missing from selected_actions.patterns: {missing}",
                            endpoint="actions_permissions",
                        )
                    )
                if extra:
                    violations.append(
                        _violation(
                            "github.actions.allow_list_extra",
                            f"selected_actions.patterns contains entries not in allow_list: {extra}",
                            endpoint="actions_permissions",
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

    return violations
