from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


class MetricsError(RuntimeError):
    pass


def _count_changes(drift: Any) -> int:
    if isinstance(drift, dict):
        if "want" in drift and "have" in drift:
            return 1
        total = 0
        for value in drift.values():
            total += _count_changes(value)
        return total
    return 0


def collect_metrics(plan: Dict[str, Any]) -> Dict[str, Any]:
    endpoints = plan.get("endpoints", [])
    total_endpoints = len(endpoints)
    endpoints_with_drift = 0
    total_changes = 0
    changes_by_endpoint: Dict[str, int] = {}
    for endpoint in endpoints:
        name = endpoint.get("name", "<unknown>")
        drift = endpoint.get("drift") or {}
        count = _count_changes(drift)
        changes_by_endpoint[name] = count
        if count:
            endpoints_with_drift += 1
            total_changes += count

    overlay = plan.get("overlay") or {}
    violations = overlay.get("violations") or []
    errors = overlay.get("errors") or []
    violation_codes: Dict[str, int] = {}
    for violation in violations:
        code = violation.get("code", "overlay.violation")
        violation_codes[code] = violation_codes.get(code, 0) + 1

    metrics: Dict[str, Any] = {
        "metrics_version": 1,
        "spec_version": plan.get("version"),
        "provider": plan.get("provider"),
        "repo": plan.get("repo"),
        "endpoints_total": total_endpoints,
        "endpoints_with_drift": endpoints_with_drift,
        "changes_total": total_changes,
        "changes_by_endpoint": changes_by_endpoint,
        "overlay": {
            "name": overlay.get("name"),
            "path": overlay.get("path"),
            "violations": len(violations),
            "errors": len(errors),
            "violation_codes": violation_codes,
        },
    }
    return metrics


def write_metrics(metrics: Dict[str, Any], output: Optional[Path]) -> None:
    payload = json.dumps(metrics, indent=2, sort_keys=True)
    if output is None:
        print(payload)
        return
    output.write_text(payload + "\n", encoding="utf-8")
