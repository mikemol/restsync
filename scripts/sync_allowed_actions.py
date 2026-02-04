#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def _load_allowed_actions(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    actions: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        actions.append(line)
    return actions


def _update_config(config_path: Path, actions: list[str]) -> bool:
    lines = config_path.read_text(encoding="utf-8").splitlines()
    new_lines: list[str] = []
    updated = False
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        if line.strip() == "patterns_allowed:":
            indent = len(line) - len(line.lstrip(" "))
            i += 1
            # Skip existing list items at deeper indent.
            while i < len(lines):
                next_line = lines[i]
                next_indent = len(next_line) - len(next_line.lstrip(" "))
                if next_line.strip().startswith("-") and next_indent > indent:
                    i += 1
                    continue
                break
            for action in actions:
                new_lines.append(" " * (indent + 2) + f"- {action}")
            updated = True
            continue
        i += 1
    if not updated:
        raise SystemExit("patterns_allowed not found in config")
    updated_text = "\n".join(new_lines) + "\n"
    if updated_text != config_path.read_text(encoding="utf-8"):
        config_path.write_text(updated_text, encoding="utf-8")
        return True
    return False


def _extract_patterns(config_path: Path) -> list[str]:
    lines = config_path.read_text(encoding="utf-8").splitlines()
    patterns: list[str] = []
    in_patterns = False
    base_indent = 0
    for line in lines:
        if line.strip() == "patterns_allowed:":
            in_patterns = True
            base_indent = len(line) - len(line.lstrip(" "))
            continue
        if in_patterns:
            indent = len(line) - len(line.lstrip(" "))
            if indent <= base_indent:
                break
            stripped = line.strip()
            if stripped.startswith("- "):
                patterns.append(stripped[2:].strip())
    return patterns


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync docs/allowed_actions.txt into configs/restsync.yml",
    )
    parser.add_argument(
        "--config",
        default="configs/restsync.yml",
        help="Path to restsync config",
    )
    parser.add_argument(
        "--allowed-actions",
        default="docs/allowed_actions.txt",
        help="Path to allowed actions list",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if config differs from allowed actions",
    )
    args = parser.parse_args()

    allowed_path = Path(args.allowed_actions)
    config_path = Path(args.config)
    actions = _load_allowed_actions(allowed_path)

    if args.check:
        current = _extract_patterns(config_path)
        if current != actions:
            raise SystemExit("config patterns_allowed is out of sync with allowed_actions")
        return

    changed = _update_config(config_path, actions)
    if changed:
        print(f"Updated {config_path} from {allowed_path}.")
    else:
        print("Config already matches allowed actions.")


if __name__ == "__main__":
    main()
