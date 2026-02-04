from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Optional

from restsync.auth import get_token
from restsync.canon import canonicalize
from restsync.diff import diff_values
from restsync.http import request_json
from restsync.spec import EndpointSpec, RestsyncSpec, load_spec


class PlanError(RuntimeError):
    pass


def _format_url(spec: RestsyncSpec, endpoint: EndpointSpec) -> str:
    return f"{spec.base_url}{endpoint.url.format(owner=spec.repo.owner, repo=spec.repo.name)}"


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


def build_plan(spec: RestsyncSpec, token: Optional[str]) -> Dict[str, Any]:
    endpoints = []
    for endpoint in sorted(spec.endpoints, key=lambda item: item.name):
        url = _format_url(spec, endpoint)
        live = request_json(endpoint.method, url, token)
        desired = _desired_for_endpoint(spec, endpoint)
        want = canonicalize(desired, endpoint.compare)
        have = canonicalize(live, endpoint.compare)
        drift = diff_values(want, have)
        endpoints.append(
            {
                "name": endpoint.name,
                "url": url,
                "method": endpoint.method,
                "want": want,
                "have": have,
                "drift": drift,
                "apply": asdict(endpoint.apply) if endpoint.apply else None,
            }
        )
    return {
        "version": spec.version,
        "provider": spec.provider,
        "repo": asdict(spec.repo),
        "endpoints": endpoints,
    }


def plan_from_path(path: Path) -> Dict[str, Any]:
    spec, errors = load_spec(path)
    if errors or spec is None:
        raise PlanError("invalid spec: " + "; ".join(errors))
    token = get_token(spec.auth)
    return build_plan(spec, token)


def write_plan(plan: Dict[str, Any], output: Optional[Path]) -> None:
    payload = json.dumps(plan, indent=2, sort_keys=True)
    if output is None:
        print(payload)
        return
    output.write_text(payload + "\n", encoding="utf-8")
