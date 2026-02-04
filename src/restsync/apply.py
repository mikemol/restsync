from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from restsync.http import request_json


class ApplyError(RuntimeError):
    pass


RequestFunc = Callable[[str, str, Optional[str], Optional[Dict[str, Any]]], Dict[str, Any]]


def apply_plan(
    plan: Dict[str, Any],
    token: Optional[str],
    *,
    confirm: bool,
    request_func: RequestFunc = request_json,
) -> List[str]:
    if not confirm:
        raise ApplyError("apply requires --confirm")

    overlay = plan.get("overlay") or {}
    errors = overlay.get("errors") or []
    violations = overlay.get("violations") or []
    if errors:
        raise ApplyError("overlay errors present; aborting apply")
    if violations:
        raise ApplyError("overlay violations present; aborting apply")

    applied: List[str] = []
    for endpoint in plan.get("endpoints", []):
        apply_spec = endpoint.get("apply") or None
        if not apply_spec:
            continue
        drift = endpoint.get("drift") or {}
        if not drift:
            continue
        method = apply_spec.get("method")
        apply_url = endpoint.get("apply_url") or endpoint.get("url")
        if not apply_url:
            raise ApplyError(f"missing apply URL for {endpoint.get('name')}")
        body = endpoint.get("apply_body") or endpoint.get("want") or {}
        request_func(str(method), str(apply_url), token, body)
        applied.append(str(endpoint.get("name")))
    return applied
