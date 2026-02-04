from __future__ import annotations

import argparse
from pathlib import Path
import sys

from restsync.plan import plan_from_path, write_plan, PlanError
from restsync.spec import load_spec


def _cmd_spec_check(args: argparse.Namespace) -> int:
    path = Path(args.config)
    spec, errors = load_spec(path)
    if errors:
        for err in errors:
            print(f"spec-check: {err}", file=sys.stderr)
        return 2
    print(f"spec-check: ok ({spec.provider} {spec.repo.owner}/{spec.repo.name})")
    return 0


def _cmd_plan(args: argparse.Namespace) -> int:
    try:
        plan = plan_from_path(Path(args.config))
    except PlanError as exc:
        print(f"plan: {exc}", file=sys.stderr)
        return 2
    output = Path(args.output) if args.output else None
    write_plan(plan, output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="restsync")
    parser.add_argument(
        "--config",
        default="configs/restsync.yml",
        help="Path to restsync config (default: configs/restsync.yml)",
    )
    sub = parser.add_subparsers(dest="command")

    spec_check = sub.add_parser("spec-check", help="Validate config shape")
    spec_check.set_defaults(func=_cmd_spec_check)

    plan = sub.add_parser("plan", help="Generate a read-only plan")
    plan.add_argument(
        "--output",
        help="Write plan JSON to a file instead of stdout",
    )
    plan.set_defaults(func=_cmd_plan)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
