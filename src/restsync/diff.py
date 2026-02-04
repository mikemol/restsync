from __future__ import annotations

from typing import Any, Dict


Diff = Dict[str, Any]


def _diff_dict(want: Dict[str, Any], have: Dict[str, Any]) -> Diff:
    diff: Diff = {}
    for key in sorted(set(want.keys()) | set(have.keys())):
        w_val = want.get(key)
        h_val = have.get(key)
        if isinstance(w_val, dict) and isinstance(h_val, dict):
            nested = _diff_dict(w_val, h_val)
            if nested:
                diff[key] = nested
        elif w_val != h_val:
            diff[key] = {"want": w_val, "have": h_val}
    return diff


def diff_values(want: Any, have: Any) -> Diff:
    if isinstance(want, dict) and isinstance(have, dict):
        return _diff_dict(want, have)
    if want == have:
        return {}
    return {"want": want, "have": have}
