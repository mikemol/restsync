from __future__ import annotations

from typing import Any, Dict, Iterable

from restsync.spec import CompareSpec


def _project_keys(data: Dict[str, Any], compare: CompareSpec, depth: int) -> Iterable[str]:
    if depth == 0 and compare.include:
        keys = compare.include
    else:
        keys = data.keys()
    if compare.ignore:
        return [key for key in keys if key not in compare.ignore]
    return list(keys)


def _sort_list(value: list[Any]) -> list[Any]:
    try:
        return sorted(value)
    except TypeError:
        # Fall back to stable string ordering for mixed types.
        return sorted(value, key=lambda item: str(item))


def canonicalize(
    value: Any,
    compare: CompareSpec,
    *,
    depth: int = 0,
    key: str | None = None,
) -> Any:
    if key and key in compare.unwrap_enabled:
        if isinstance(value, dict):
            enabled = value.get("enabled")
            if isinstance(enabled, bool):
                return enabled
        if isinstance(value, bool):
            return value
    if isinstance(value, dict):
        projected: Dict[str, Any] = {}
        for key in _project_keys(value, compare, depth):
            if key in value:
                projected[key] = canonicalize(
                    value[key],
                    compare,
                    depth=depth + 1,
                    key=key,
                )
        return projected
    if isinstance(value, list):
        items = [canonicalize(item, compare, depth=depth + 1) for item in value]
        # Sort lists only when explicitly requested (top-level compare.sort).
        if compare.sort:
            return _sort_list(items)
        return items
    return value
