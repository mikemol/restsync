from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Optional

from restsync.auth import get_token
from restsync.canon import canonicalize
from restsync.diff import diff_values
from restsync.http import request_json
from restsync.overlay import load_overlay, validate_plan
from restsync.spec import EndpointSpec, RestsyncSpec, load_spec


class PlanError(RuntimeError):
    pass


def _format_url(spec: RestsyncSpec, template: str) -> str:
    return f"{spec.base_url}{template.format(owner=spec.repo.owner, repo=spec.repo.name)}"


def _resolve_path(root: Dict[str, Any], path: str) -> Any:
    if not path:
        return {}
    parts = path.split(".")
    current: Any = root
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            raise PlanError(f"unable to resolve path: {path}")
    return current


def _desired_for_endpoint(spec: RestsyncSpec, endpoint: EndpointSpec) -> Dict[str, Any]:
    if endpoint.name in spec.desired:
        desired = spec.desired.get(endpoint.name)
    elif endpoint.apply is not None:
        desired = _resolve_path({"desired": spec.desired}, endpoint.apply.body_from)
    else:
        desired = {}
    if not isinstance(desired, dict):
        raise PlanError(f"desired state for {endpoint.name} must be a mapping")
    return desired


def build_plan(spec: RestsyncSpec, token: Optional[str], overlay_path: Optional[Path]) -> Dict[str, Any]:
    endpoints = []
    for endpoint in sorted(spec.endpoints, key=lambda item: item.name):
        url = _format_url(spec, endpoint.url)
        live = request_json(endpoint.method, url, token)
        desired = _desired_for_endpoint(spec, endpoint)
        want = canonicalize(desired, endpoint.compare)
        have = canonicalize(live, endpoint.compare)
        drift = diff_values(want, have)
        apply_url = None
        apply_body = None
        if endpoint.apply is not None:
            apply_url = _format_url(spec, endpoint.apply.url)
            apply_body = _resolve_path({"desired": spec.desired}, endpoint.apply.body_from)
        endpoints.append(
            {
                "name": endpoint.name,
                "url": url,
                "method": endpoint.method,
                "want": want,
                "have": have,
                "drift": drift,
                "apply": asdict(endpoint.apply) if endpoint.apply else None,
                "apply_url": apply_url,
                "apply_body": apply_body,
            }
        )
    plan: Dict[str, Any] = {
        "version": spec.version,
        "provider": spec.provider,
        "base_url": spec.base_url,
        "repo": asdict(spec.repo),
        "endpoints": endpoints,
    }
    if overlay_path is not None:
        overlay, errors = load_overlay(overlay_path)
        if errors:
            plan["overlay"] = {"name": None, "errors": errors, "violations": []}
        elif overlay is not None:
            violations = validate_plan(plan, overlay)
            plan["overlay"] = {
                "name": overlay.name,
                "path": str(overlay_path),
                "violations": violations,
            }
    return plan


def _default_overlay_path(spec: RestsyncSpec, config_path: Path) -> Optional[Path]:
    if spec.overlay:
        return (config_path.parent / spec.overlay).resolve()
    candidate = config_path.parent / "overlays" / f"{spec.provider}.yml"
    if candidate.exists():
        return candidate.resolve()
    return None


def plan_from_path(path: Path) -> Dict[str, Any]:
    spec, errors = load_spec(path)
    if errors or spec is None:
        raise PlanError("invalid spec: " + "; ".join(errors))
    token = get_token(spec.auth)
    overlay_path = _default_overlay_path(spec, path)
    return build_plan(spec, token, overlay_path)


def write_plan(plan: Dict[str, Any], output: Optional[Path]) -> None:
    payload = json.dumps(plan, indent=2, sort_keys=True)
    if output is None:
        print(payload)
        return
    output.write_text(payload + "\n", encoding="utf-8")
