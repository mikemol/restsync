from __future__ import annotations

from typing import Any, Dict, Iterable

from restsync.spec import CompareSpec


def _project_keys(data: Dict[str, Any], compare: CompareSpec) -> Iterable[str]:
    if compare.include:
        keys = compare.include
    else:
        keys = data.keys()
    return [key for key in keys if key not in compare.ignore]


def _sort_list(value: list[Any]) -> list[Any]:
    try:
        return sorted(value)
    except TypeError:
        # Fall back to stable string ordering for mixed types.
        return sorted(value, key=lambda item: str(item))


def canonicalize(value: Any, compare: CompareSpec) -> Any:
    if isinstance(value, dict):
        projected: Dict[str, Any] = {}
        for key in _project_keys(value, compare):
            if key in value:
                projected[key] = canonicalize(value[key], compare)
        return projected
    if isinstance(value, list):
        items = [canonicalize(item, compare) for item in value]
        # Sort lists only when explicitly requested (top-level compare.sort).
        if compare.sort:
            return _sort_list(items)
        return items
    return value
