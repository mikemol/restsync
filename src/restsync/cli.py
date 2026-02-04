from __future__ import annotations

import argparse
from pathlib import Path
import sys

from restsync.apply import apply_plan, ApplyError
from restsync.auth import get_token
from restsync.plan import plan_from_path, write_plan, PlanError
from restsync.ratchet import apply_ratchet, load_baseline, write_baseline
from restsync.snapshot import snapshot_from_path, write_snapshot, SnapshotError
from restsync.summary import summarize_plan
from restsync.spec import load_spec
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
    print(summarize_plan(plan))
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    try:
        plan = plan_from_path(Path(args.config))
    except PlanError as exc:
        print(f"check: {exc}", file=sys.stderr)
        return 2
    output = Path(args.output) if args.output else None
    write_plan(plan, output)
    print(summarize_plan(plan))
    overlay = plan.get("overlay") or {}
    violations = overlay.get("violations") or []
    errors = overlay.get("errors") or []
    if errors:
        for err in errors:
            print(f"check: overlay error: {err}", file=sys.stderr)
        return 2
    baseline_path = Path(args.baseline) if args.baseline else None
    if args.baseline_write:
        if baseline_path is None:
            print("check: --baseline-write requires --baseline", file=sys.stderr)
            return 2
        write_baseline(baseline_path, violations)
        print(f"check: wrote baseline to {baseline_path}")
        return 0
    if violations and baseline_path is not None:
        baseline = load_baseline(baseline_path)
        ratchet = apply_ratchet(violations, baseline)
        violations = ratchet.violations
    if violations:
        for v in violations:
            code = v.get("code", "overlay.violation")
            message = v.get("message", "")
            endpoint = v.get("endpoint")
            suffix = f" ({endpoint})" if endpoint else ""
            print(f"check: {code}{suffix}: {message}", file=sys.stderr)
        return 3
    print("check: ok")
    return 0


def _cmd_snapshot(args: argparse.Namespace) -> int:
    try:
        snapshot = snapshot_from_path(Path(args.config))
    except SnapshotError as exc:
        print(f"snapshot: {exc}", file=sys.stderr)
        return 2
    output = Path(args.output) if args.output else None
    write_snapshot(snapshot, output)
    print("snapshot: ok")
    return 0


def _cmd_apply(args: argparse.Namespace) -> int:
    config_path = Path(args.config)
    spec, errors = load_spec(config_path)
    if errors or spec is None:
        for err in errors:
            print(f"apply: {err}", file=sys.stderr)
        return 2
    token = get_token(spec.auth)
    try:
        plan = plan_from_path(config_path)
    except PlanError as exc:
        print(f"apply: {exc}", file=sys.stderr)
        return 2
    output = Path(args.output) if args.output else None
    write_plan(plan, output)
    print(summarize_plan(plan))
    try:
        applied = apply_plan(plan, token, confirm=args.confirm)
    except ApplyError as exc:
        print(f"apply: {exc}", file=sys.stderr)
        return 3
    if applied:
        print(f"apply: updated {', '.join(applied)}")
    else:
        print("apply: no changes")
    return 0


def build_parser() -> argparse.ArgumentParser:
    config_parent = argparse.ArgumentParser(add_help=False)
    config_parent.add_argument(
        "--config",
        default="configs/restsync.yml",
        help="Path to restsync config (default: configs/restsync.yml)",
    )

    parser = argparse.ArgumentParser(prog="restsync", parents=[config_parent])
    sub = parser.add_subparsers(dest="command")

    spec_check = sub.add_parser(
        "spec-check",
        help="Validate config shape",
        parents=[config_parent],
    )
    spec_check.set_defaults(func=_cmd_spec_check)

    plan = sub.add_parser(
        "plan",
        help="Generate a read-only plan",
        parents=[config_parent],
    )
    plan.add_argument(
        "--output",
        help="Write plan JSON to a file instead of stdout",
    )
    plan.set_defaults(func=_cmd_plan)

    check = sub.add_parser(
        "check",
        help="Generate a plan and fail on violations",
        parents=[config_parent],
    )
    check.add_argument(
        "--output",
        help="Write plan JSON to a file instead of stdout",
    )
    check.add_argument(
        "--baseline",
        help="Path to an overlay baseline file (JSON)",
    )
    check.add_argument(
        "--baseline-write",
        action="store_true",
        help="Write current violations to the baseline and exit",
    )
    check.set_defaults(func=_cmd_check)

    snapshot = sub.add_parser(
        "snapshot",
        help="Capture the current live state (read-only)",
        parents=[config_parent],
    )
    snapshot.add_argument(
        "--output",
        help="Write snapshot JSON to a file instead of stdout",
    )
    snapshot.set_defaults(func=_cmd_snapshot)

    apply = sub.add_parser(
        "apply",
        help="Apply the desired state (requires --confirm)",
        parents=[config_parent],
    )
    apply.add_argument(
        "--confirm",
        action="store_true",
        help="Confirm that you want to apply changes",
    )
    apply.add_argument(
        "--output",
        help="Write plan JSON to a file instead of stdout",
    )
    apply.set_defaults(func=_cmd_apply)

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
