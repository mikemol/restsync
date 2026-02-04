#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _build_badge(metrics: Dict[str, Any], label: str) -> Dict[str, Any]:
    changes = _as_int(metrics.get("changes_total"))
    overlay = metrics.get("overlay") or {}
    violations = _as_int(overlay.get("violations"))
    errors = _as_int(overlay.get("errors"))

    if errors:
        color = "red"
        message = f"errors {errors} | violations {violations}"
    elif violations:
        color = "orange"
        message = f"drift {changes} | violations {violations}"
    elif changes:
        color = "yellow"
        message = f"drift {changes} | violations {violations}"
    else:
        color = "brightgreen"
        message = "clean"

    return {
        "schemaVersion": 1,
        "label": label,
        "message": message,
        "color": color,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to metrics JSON")
    parser.add_argument("--output", required=True, help="Path to badge JSON")
    parser.add_argument("--label", default="plan health", help="Badge label")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    metrics = json.loads(input_path.read_text(encoding="utf-8"))
    badge = _build_badge(metrics, args.label)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(badge, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
