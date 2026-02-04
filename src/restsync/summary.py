from __future__ import annotations

from typing import Any, Dict, List


class SummaryError(RuntimeError):
    pass


def summarize_plan(plan: Dict[str, Any]) -> str:
    endpoints = plan.get("endpoints", [])
    lines: List[str] = []
    total_changes = 0
    for endpoint in endpoints:
        name = endpoint.get("name", "<unknown>")
        drift = endpoint.get("drift") or {}
        if not drift:
            continue
        count = _count_changes(drift)
        total_changes += count
        lines.append(f"- {name}: {count} change(s)")
    if not lines:
        return "No changes detected."
    header = f"Plan summary: {total_changes} change(s) across {len(lines)} endpoint(s)."
    return "\n".join([header] + lines)


def _count_changes(drift: Any) -> int:
    if isinstance(drift, dict):
        if "want" in drift and "have" in drift:
            return 1
        count = 0
        for value in drift.values():
            count += _count_changes(value)
        return count
    return 0
