from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class RatchetResult:
    violations: List[Dict[str, Any]]
    baseline: List[Dict[str, Any]]


def _normalize_violation(entry: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "code": entry.get("code"),
        "endpoint": entry.get("endpoint"),
        "message": entry.get("message"),
    }


def load_baseline(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("baseline must be a list")
    normalized: List[Dict[str, Any]] = []
    for entry in payload:
        if isinstance(entry, dict):
            normalized.append(_normalize_violation(entry))
    return normalized


def write_baseline(path: Path, violations: List[Dict[str, Any]]) -> None:
    normalized = [_normalize_violation(v) for v in violations]
    path.write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def apply_ratchet(
    violations: List[Dict[str, Any]],
    baseline: Optional[List[Dict[str, Any]]],
) -> RatchetResult:
    baseline = baseline or []
    normalized = [_normalize_violation(v) for v in violations]
    baseline_set = {json.dumps(v, sort_keys=True) for v in baseline}
    remaining = [v for v in normalized if json.dumps(v, sort_keys=True) not in baseline_set]
    return RatchetResult(violations=remaining, baseline=baseline)
